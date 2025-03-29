import pandas as pd

class TireData:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def create_df(self):
        self.df = pd.read_csv(self.file_path)
        return self.df
    
    def check_df(self):
        # Check basic info about the data
        print('DATAFRAME')
        print(self.df)
        
        print('BASIC INFO')
        print(self.df.info())

        # Check for missing values
        print('MISSING INFO')
        print(self.df.isnull().sum())

        # Summary statistics
        print('SUMMARY STATISTICS')
        print(self.df.describe())
    
    #FEATURE ENGINEERING
    def create_starting_grid(self):
        self.df['StartingPosition'] = self.df['DriverID']
    
    def calc_driver_positions(self):
        self.df['Position'] = self.df.groupby('LapNumber')['LapTime'].rank(method='min', ascending=True).astype(int)

    def calc_laptime_avg(self):
        self.avg_lap_time = self.df.groupby('LapNumber')['LapTime'].mean().reset_index()
        self.avg_lap_time.rename(columns={'LapTime': 'AvgLapTime'}, inplace = True)
        self.df = pd.merge(self.df, self.avg_lap_time, on = 'LapNumber')

    def calc_laptime_delta(self):
        self.df['LapTimeDelta'] = self.df['LapTime'] - self.df['AvgLapTime']
    
    def add_pitstops(self):
        self.df['PitStop'] = self.df['TireWear'] == 0
    
    def calc_cumwear(self, group):
        cumulative_wear = []
        current_wear = 0
        for _, row in group.iterrows():
            if row['PitStop']:  # Reset the wear after a pit stop
                current_wear = 0
            current_wear += row['TireWear']
            cumulative_wear.append(current_wear)

        return pd.Series(cumulative_wear, index=group.index)
    
    def add_laps_since_pitting(self, group):
        laps_since_pitting = []
        laps = 0 
        for _, row in group.iterrows():
            if row['PitStop']:
                laps = 0
            else:
                laps += 1
            laps_since_pitting.append(laps)
        return pd.Series(laps_since_pitting, index = group.index)

    def calc_degrade_rate(self):
        self.df['DegradationRate'] = self.df['TireWear'] / self.df['LapsSincePit']

    def calc_tire_efficiency(self):
        self.df['TireEfficiency'] = self.df['LapTime'] / (1 + self.df['TireWear'])

    def calc_pit_time_loss(self, group):
        '''
        Calculate the time lost due to a car Pitting
        '''
        time_lost = 0
        times_lost = []
        for _, row in group.iterrows():
            if row['PitStop']:
                time_lost = row['LapTimeDelta']
            times_lost.append(time_lost)
        return pd.Series(times_lost, index = group.index)         

    def calc_avg_pit_time(self, group):
        pit_times = []
        pit_time = 0
        avg_pit_time = 0
        avg_pit_times = []
        
        for _, row in group.iterrows():
            if row['PitStop']:
                pit_time = row['PitTime']
                pit_times.append(pit_time)
                avg_pit_time = sum(pit_times) / len(pit_times)
            avg_pit_times.append(avg_pit_time)
        return pd.Series(avg_pit_times, index = group.index)

    def calc_postion_change(self):
        positions = []
        positions_loss = []
        
        for _, row in self.df.iterrows():
            positions.append(row['Position'])
        
        for i, position in enumerate(positions):
            if i != 0:
                positions_loss.append(
                    -1 * (position - positions[i-1])
                )
            else:
                positions_loss.append(0)

        self.df['PositionChange'] = pd.Series(positions_loss, index = self.df.index) 

    def calc_performance_gain_after_pit(self):
        
        performance_gains = []
        for i, row in self.df.iterrows():
            if i != 0:
                if self.df.loc[i - 1, 'PitStop']:
                    performance_gains.append(
                        row['AvgLapTime'] - row['LapTime']
                    )
                else:
                    performance_gains.append(0)
            else:
                performance_gains.append(0)
        
        self.df['PerformanceGainAfterPit'] = pd.Series(performance_gains, index = self.df.index)

    def feature_engineer(self):
        self.create_starting_grid()
        self.calc_driver_positions()
        self.calc_laptime_avg()
        self.calc_laptime_delta()
        self.add_pitstops()
        self.df['CumulativeTireWear'] = self.df.groupby('DriverID', group_keys=False).apply(self.calc_cumwear)
        self.df['LapsSincePit'] = self.df.groupby('DriverID', group_keys = False).apply(self.add_laps_since_pitting)
        self.calc_degrade_rate()
        self.calc_tire_efficiency()
        self.df['PitTime'] = self.df.groupby('DriverID', group_keys = False).apply(self.calc_pit_time_loss)
        self.df['AvgPitTime'] = self.df.groupby('DriverID', group_keys = False).apply(self.calc_avg_pit_time)
        self.calc_postion_change()
        self.calc_performance_gain_after_pit()
    
    def convert_to_csv(self):
        self.df.to_csv('f1_tire_strategy_simulation_feature_engineered.csv', index=False)

if __name__ == '__main__':
    file_path = 'f1_tire_strategy_simulation_v2.csv'
    data = TireData(file_path)
    df = data.create_df()
    data.feature_engineer()
    data.check_df()
    data.convert_to_csv()
    
