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
    def calc_laptime_delta(self):
        self.avg_lap_time = self.df.groupby('LapNumber')['LapTime'].mean().reset_index()
        self.avg_lap_time.rename(columns={'LapTime': 'AvgLapTime'}, inplace = True)
        self.df = pd.merge(self.df, self.avg_lap_time, on = 'LapNumber')
        self.df['LapTimeDelta'] = self.df['LapTime'] - self.df['AvgLapTime']
    
    def calc_cum_tirewear(self):
        self.df['PitInstance'] = self.df['TotalPitStops'].ne(self.df['TotalPitStops'].shift()).cumsum()
        self.df['cumsum'] = self.df.groupby('value_change')['amount'].cumsum()


if __name__ == '__main__':
    file_path = 'f1_tire_strategy_simulation_v2.csv'
    data = TireData(file_path)
    df = data.create_df()
    data.calc_laptime_delta()
    data.check_df()
    
