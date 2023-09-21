import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Shot:
    """Shot class to store data from a shot."""
    def __init__(self, path: str, signals:list = []):
        self.path = path
        self.signals = signals
        self.data = {} # Dictionary of signals. Each signal is a dictionary with keys "time" and "value"
        self.tokamak = None
        self.shot_id = None
        self.events = {}
        
        #For now, default to loading from csv file
        self.load_csv()
        

    def load_csv(self):
        """Loads the data of a shot from the database into shot object.

        """
        
        df = pd.read_csv(self.path)
        if 'time' not in df.columns:
            print('Warning: no time column found in shot data. Creating dummy time column.')
            df["time"] = np.arange(len(df))

        for column in df.columns:
            if column=="time":
                continue
            self.data[column] = {"time": df["time"], "value": df[column]}
        
        try:
            self.shot_id = self.data["shot_id"]
        except:
            try:
                self.shot_id = self.data["shot"]
            except:
                pass
        try:
            self.device = self.data["tokamak"]
        except:
            pass
        self.signals = df.columns

    def compute_flattop_current(self):
        pass


def plot_shot(shot: Shot, signal: str, **kwargs):
    return plt.plot(shot.data[signal]["time"], shot.data[signal]["value"], **kwargs)

def plot_standard_shot(shots):
    fig, axs = plt.subplots(ncols=1, nrows=2, sharex=True)
    for shot in shots:
        plt.sca(axs[0])
        plot_shot(shot, "Plasma_Current (A)", label="Plasma Current (A)")
        plt.sca(axs[1])
        plot_shot(shot, "Plasma_Density (particlesm3)", label="Plasma_Density (particlesm3)")


    return fig, axs

if __name__ == "__main__":

    print("Example shot.py")
    my_shot = Shot(path="shots/shot_2023010101.csv", signals=[])

    # Plot using matplotlib directly
    fig, axs = plt.subplots(ncols=1, nrows=2, sharex=True)
    plt.sca(axs[0])
    axs[0].set_ylim([0,2000])
    plot_shot(my_shot, "Plasma_Current (A)", color="tab:red")
    plt.sca(axs[1])
    plot_shot(my_shot, "Plasma_Density (particlesm3)")
    plt.show()


    # Plot using the plot_standard_shot function
    my_shot2 = Shot(path="shots/shot_2023010102.csv", signals=[])
    fig, axs = plot_standard_shot([my_shot,my_shot2])
    plt.show()
