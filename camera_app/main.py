import sys
import numpy as np

import pyjapc

from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5 import uic

import config_loader


class Ui_camera_app(QMainWindow ):
    def __init__(self):
        super(Ui_camera_app, self).__init__()

        uic.loadUi('./ui_main_panel.ui', self)

        # start JAPC
        # self.japc = None
        self.japc = pyjapc.PyJapc(selector='', incaAcceleratorName='SPS')

        # init panel
        self.setup_ui(self.japc)

        # show window
        self.show()

        # connect signals from events in the widgets
        self.tab1.new_img_signal.connect( self.trigger_img_update )
        self.tab1.new_plot_param_signal.connect( self.trigger_plot_param_update )
        self.tab1.camera_start_signal.connect( self.start_new_camera )

    def setup_ui(self, japc):
        # read the cam list
        ### LOAD FROM A FILE
        camList = ['CA.BTV0910.DigiCam', 'CAS.BTV0420.DigiCam']
        self.tab1.camList = camList

        # pass japc to the tab
        self.tab1.setup_device_tab( self.japc )
        self.tab3.setup_calibration_tab( self.japc )

    def update_messageBox(self, msg):
        self.messageBox.setText(msg)

    def trigger_img_update(self):
        self.image_widget.chart.refresh_image( self.tab1.imageData )

    def trigger_plot_param_update(self):
        self.image_widget.chart.refresh_plot_param( self.tab1.plot_parameters )

    def start_new_camera(self):
        self.tab3.camera_start( self.tab1.current_cam_name)

def main():
    app = QApplication(sys.argv)
    window = Ui_camera_app()
    # closing routine
    ret = app.exec_()
    ## window.japc.stopSubscriptions()
    sys.exit(ret)


if __name__ == '__main__':
	main()

