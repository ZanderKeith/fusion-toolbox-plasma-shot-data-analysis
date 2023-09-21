from fusion_toolbox.plotting_gui.shot import Shot
import tkinter
import os

import numpy as np

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                                NavigationToolbar2Tk)
from matplotlib.figure import Figure

class View:

    def __init__(self):
        self._load_data()
        self._make_window()
        self._make_buttons()

        # Plot the first shot in the list
        self.current_shot_id = list(self.shot_dict.keys())[0]
        self.update_signals(self.current_shot_id)

        tkinter.mainloop()

    def _load_data(self):
        # Get all file names in the current directory
        self.shot_files = os.listdir("data/shots")

        self.shot_dict = {}
    
        for shot_file in self.shot_files:
            # Create a shot object
            shot = Shot("data/shots/" + shot_file)
            # Add it to the list
            self.shot_dict[shot.shot_id] = shot

    def _make_window(self):
                # Start making the GUI
        self.root = tkinter.Tk()
        self.root.wm_title("Plasma Shot Data Analysis")

        self.fig = Figure(figsize=(5, 4), dpi=100)
        #t = np.arange(0, 3, .01)
        #ax = fig.add_subplot()
        #line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
        #ax.set_xlabel("time [s]")
        #ax.set_ylabel("f(t)")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()

        self.canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
        self.canvas.mpl_connect("key_press_event", key_press_handler)
    
    def _make_buttons(self):
        button_quit = tkinter.Button(master=self.root, text="Quit", command=self.root.destroy)

        #slider_update = tkinter.Scale(self.root, from_=1, to=5, orient=tkinter.HORIZONTAL,
        #                            command=self.update_frequency, label="Frequency [Hz]")

        next_shot_button = tkinter.Button(master=self.root, text="Next Shot", command=self.plot_next_shot)

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        button_quit.pack(side=tkinter.BOTTOM)
        #slider_update.pack(side=tkinter.BOTTOM)
        next_shot_button.pack(side=tkinter.BOTTOM)
        self.toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
    
    def update_frequency(new_val, line, canvas):
            # retrieve frequency
            f = float(new_val)

            # update data
            y = 2 * np.sin(2 * np.pi * f * t)
            line.set_data(t, y)

            # required to update canvas and attached toolbar!
            canvas.draw()

    def update_signals(self, shot_id):
        
        # Get all axes in the figure
        axes = self.fig.get_axes()
        for ax in axes:
            self.fig.delaxes(ax)

        # Get the shot object
        shot = self.get_shot(shot_id)

        # Create a new axis for each available signal
        for i, signal in enumerate(shot.signals):
            try:
                time = shot.data[signal]["time"]
                data = shot.data[signal]["value"]

                ax = self.fig.add_subplot(len(shot.signals), 1, i+1)
                ax.plot(time, data)
                ax.set_xlabel("Time [s]")
                ax.set_ylabel(signal)
            except:
                break

        self.canvas.draw()

    def get_shot(self, shot_number)->Shot:
        """Returns the Shot object of a particular shot number

        Args:
            shot int: the shot number
        """
        return self.shot_dict[shot_number]
            

    def get_next_shot(self, shot_number):
        """Returns the next shot in the list"""

        # Find the index of the shot in the dictionary
        shot_list = list(self.shot_dict.keys())
        i = shot_list.index(shot_number)
        
        # Return the next shot
        return shot_list[i+1]
    
    def plot_next_shot(self):
        # Get the next shot
        next_shot_id = self.get_next_shot(self.current_shot_id)

        # Plot it
        self.update_signals(next_shot_id)

        self.current_shot_id = next_shot_id


