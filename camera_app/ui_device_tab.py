import numpy as np

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

class Ui_device_tab(QtWidgets.QWidget):

    new_plot_param_signal = pyqtSignal()
    camera_connect_signal = pyqtSignal()
    camera_disconnect_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(Ui_device_tab, self).__init__(parent)
        uic.loadUi("./ui_device_tab.ui", self)
        self.show()

        # appearance menu
        self.cmap_list = ['jet', 'inferno', 'gray']
        self.scale_list = ['linear', 'log']

        # useful params inside this widget
        self.japc = None
        self.current_cam_name = None
        self.camList = None

        # broadcasterd params
        self.acqParameters = None

        # data to pass when emitting signals
        self.imageData = None
        self.plot_parameters = { 'cmap': self.cmap_list[0], 'cauto':True, 'cmin':0, 'cmax':4096, 'scale': self.scale_list[0] }

    def setup_device_tab(self, japc):
        ## japc
        self.japc = japc

        ## combo boxes
        # load cam list
        self.current_cam_name = self.camList[0]
        self.camName_comboBox.addItems( self.camList )
        self.camName_comboBox.activated.connect( self.action_select_cam )
        # manage colormap
        ## temp
        self.colormap_comboBox.addItems( self.cmap_list )
        self.colormap_comboBox.activated.connect( self.action_select_cmap )
        ## lin

        ## autoscale
        self.colormap_auto_checkBox.stateChanged.connect( self.action_set_cautoscale )
        ## cmin
        # self.colormap_min.setText( str(self.plot_parameters['cmin']) )
        self.colormap_min.editingFinished.connect( self.action_change_cmin )
        ## max
        # self.colormap_max.setText( str(self.plot_parameters['cmax']) )
        self.colormap_max.editingFinished.connect( self.action_change_cmax )

        # manage scale
        self.scale_comboBox.addItems( self.scale_list )
        self.scale_comboBox.activated.connect( self.action_select_scale )
        # manage start button 
        self.startButton.clicked.connect(self.action_start_button)

    def action_start_button(self):
        # opening connection
        if self.startButton.isChecked():
            self.startButton.setText('STOP')
            self.startButton.setStyleSheet("background-color:#ff9999")
            self.camera_connect_signal.emit()
        else:
            self.startButton.setText('START')
            self.startButton.setStyleSheet("background-color:#63f29a")
            self.camera_disconnect_signal.emit()

    ##### NEW DATA AVAILABLE
    def refresh_params(self, new_params):
        self.acqParameters = new_params
        # panel refresh
        self.acqExposure_lineEdit.setText( str(self.acqParameters['acqCameraExposureTimeUs']) )
        self.acqGain_lineEdit.setText( str(self.acqParameters['acqCameraGain']) )
        self.acqDelay_lineEdit.setText( str(self.acqParameters['acqCameraTriggerDelay']) )

    def refresh_status(self):
        print('new status tab1')
        pass       


    ##### USER ACTIONS ON THE PANEL
    def action_select_cam(self):
        self.current_cam_name = self.camName_comboBox.currentText()

    def action_select_cmap(self):
        self.plot_parameters['cmap'] = self.colormap_comboBox.currentText()
        self.new_plot_param_signal.emit()

    def action_select_scale(self):
        self.plot_parameters['scale'] = self.scale_comboBox.currentText()
        self.new_plot_param_signal.emit()

    def action_change_cmin(self):
        try:
            new_cmin = float( self.colormap_min.text())
            if new_cmin >= 0.:
                if new_cmin < self.plot_parameters['cmax'] :
                    self.plot_parameters['cmin'] = new_cmin
                    self.new_plot_param_signal.emit()
                else:
                    # message to the message box 
                    print('Min must be smaller than max')
        except:
            # message to the message box 
            print('Bad numerical input')

    def action_change_cmax(self):
        try:
            new_cmin = float( self.colormap_max.text())
            if new_cmin >= 0.:
                if new_cmin > self.plot_parameters['cmin'] :
                    self.plot_parameters['cmax'] = new_cmin
                    self.new_plot_param_signal.emit()
                else:
                    # message to the message box 
                    print('Max must be larger than min')
        except:
            # message to the message box 
            print('Bad numerical input')
        

    def action_set_cautoscale(self):
        if self.colormap_auto_checkBox.isChecked():
            self.plot_parameters['cauto'] = True
        else:
            self.plot_parameters['cauto'] = False
        self.new_plot_param_signal.emit()

