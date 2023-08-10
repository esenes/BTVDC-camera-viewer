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

        # global variables
        self.camName = None
        self.imageData = None
        self.plotParams = None
        self.acqParameters = None
        self.acqStatus = None

        # connect signals from events in the widgets
        self.tab1.camera_connect_signal.connect( self.start_new_camera )
        self.tab1.camera_disconnect_signal.connect( self.stop_camera )
        self.tab1.new_plot_param_signal.connect( self.trigger_plot_param_update )

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

    def trigger_plot_param_update(self):
        self.image_widget.chart.refresh_plot_param( self.tab1.plot_parameters )


    # Camera connection
    def start_new_camera(self):
        # subscribe
        try:
            self.camName = self.tab1.current_cam_name
            self.japc.subscribeParam(self.camName+'/LastImage', onValueReceived=self.new_img_callback, getHeader=True, unixtime=True)
            self.japc.subscribeParam(self.camName+'/AcquiredParameters', onValueReceived=self.new_params_callback, getHeader=True, unixtime=True)
            self.japc.subscribeParam(self.camName+'/AcquisitionStatus', onValueReceived=self.new_status_callback, getHeader=True, unixtime=True)
            self.japc.startSubscriptions()
            self.update_messageBox(f'Connected to {self.camName}')
        except:
            self.update_messageBox(f'Failed to connect to {self.camName}')

    def new_img_callback(self, paramName, value, headerInfo):
        self.imageData = value['image2D']
        self.image_widget.chart.refresh_image( self.imageData )

    def new_params_callback(self, paramName, value, headerInfo):
        self.acqParameters = value
        self.update_params_in_widget()

    def new_status_callback(self, paramName, value, headerInfo):
        self.acqStatus = value
        self.update_status_in_widget()
    
    def stop_camera(self):
            self.japc.stopSubscriptions()
            self.japc.clearSubscriptions()
            self.update_messageBox(f'Closed connection to {self.camName}')

    def update_params_in_widget(self):
        # pass values to widget for param update
        self.tab1.refresh_params( self.acqParameters )
        pass

    def update_status_in_widget(self):
        # pass values to widget for status update
        self.tab1.refresh_status()
        pass


def main():
    app = QApplication(sys.argv)
    window = Ui_camera_app()
    # closing routine
    ret = app.exec_()
    ## window.japc.stopSubscriptions()
    sys.exit(ret)

if __name__ == '__main__':
	main()
