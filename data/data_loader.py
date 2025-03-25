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
    
    def feature_engineer(self):
        self.calc_laptime_avg()
        self.calc_laptime_delta()
        self.add_pitstops()
        self.df['CumulativeTireWear'] = self.df.groupby('DriverID', group_keys=False).apply(self.calc_cumwear)

if __name__ == '__main__':
    file_path = 'f1_tire_strategy_simulation_v2.csv'
    data = TireData(file_path)
    df = data.create_df()
    data.feature_engineer()
    data.check_df()
    
