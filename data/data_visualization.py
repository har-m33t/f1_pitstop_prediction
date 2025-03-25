import seaborn as sns
import matplotlib.pyplot as plt
from data_loader import TireData

class VisualData:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_data(self):
        data = TireData(self.file_path)
        self.df = data.create_df()
    
    def plot_tire_wear(self):
        sns.lineplot(x = 'LapNumber', y = 'TireWear', hue = 'TireType', data = self.df)
        plt.title('Tire Wear Progression Over Laps')
        plt.show()
    
    def plot_pit_stops(self):
        sns.scatterplot(x = 'LapNumber', y = 'DriverID', hue = 'TotalPitStops', data = self.df)
        plt.title('Pit Stop Timing Analysis')
        plt.yticks(range(0, 21, 1))
        plt.show()
    
    def plot_lap_times(self):
        sns.lineplot(x = 'LapNumber', y = 'LapTime', hue = 'TireType', data = self.df)
        plt.title('Lap Time Comparison')
        plt.show()

if __name__ == '__main__':
    file_path = 'f1_tire_strategy_simulation_v2.csv'
    visuals = VisualData(file_path)
    visuals.load_data()
    #visuals.plot_pit_stops()
    #visuals.plot_tire_wear()
    visuals.plot_lap_times()
