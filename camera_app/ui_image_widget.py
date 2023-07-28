import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QSizePolicy

class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5.5, height=5.8, dpi=100):
        
        # init data for receiving from other widgets
        self.img = None
        self.plot_params = { 'cmap': 'jet', 'cauto': True, 'cmin': 0, 'cmax': 4096, 'scale': 'lin' } # defaults 

        # create fig, axis, plot and colorbar
        self.fig = Figure(figsize=(width, height), dpi=dpi, frameon=False, tight_layout=True)
        self.ax = self.fig.add_subplot(111)

        self.img = self.ax.imshow(np.zeros((1200, 1920)), cmap=self.plot_params['cmap'], vmin=self.plot_params['cmin'], vmax=self.plot_params['cmax'])
        self.cbar = self.fig.colorbar(self.img, ax=self.ax)

        # canvas stuff
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot_function(self, data):
        if self.plot_params['cauto']:
            self.img = self.ax.imshow(data, cmap=self.plot_params['cmap'])
        else:
            self.img = self.ax.imshow(data, cmap=self.plot_params['cmap'], vmin=self.plot_params['cmin'], vmax=self.plot_params['cmax'])

    def refresh_image(self, data):
        self.ax.cla()
        self.plot_function(data)
        self.draw()

    def refresh_plot_param(self, data):
        self.plot_params = data
        if not(self.plot_params['cauto']): 
            self.cbar.mappable.set_clim(vmin=self.plot_params['cmin'], vmax=self.plot_params['cmax'])

class Ui_image_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("./ui_image_widget.ui", self)
        self.show()
        
        self.chart = Canvas(self)

