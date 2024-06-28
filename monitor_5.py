from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QPixmap
from VentanaPaciente import AbrirVentanaPaciente
from RegistrarDatosPaciente import RegistrarDatosPaciente
from DatosPaciente import AbrirDatosPaciente
from apneas_combobox import AbrirApneas
import serial
import time
fs_ppg=100
fs_acc=8
from pyqtgraph import PlotWidget, plot
import numpy as np
from scipy.signal import find_peaks, butter, sosfiltfilt
import pyqtgraph as pg
from numpy import append
from random import randint
import threading
import pygame
umbral=18500
import matplotlib.pyplot as plt
import os
import reportlab
from io import BytesIO
from reportlab.lib import utils
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

#firebase
import firebase_admin
from firebase_admin import firestore
import json
from firebase_admin import credentials, db
from credentials_firebase import cred
db=firestore.client() #defino database
ID=None
bandera_definir_ID=False
ALARMA_ACTIVA = False
ARCHIVO_ALARMA = "C:\\Users\\OneDrive\\Escritorio\\Alarma.wav"  #Reemplaza con la ruta de tu archivo de sonido
umbral_hr=100
umbral_spo2=80


class Ui_MainWindow(object):
    #pasar_id = QtCore.pyqtSignal(str)
    def setupUi(self, MainWindow):
        #MONITOR CENTRAL
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(2300, 1800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.monitor = QtWidgets.QFrame(self.centralwidget)
        self.monitor.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.monitor.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.monitor.setFrameShadow(QtWidgets.QFrame.Raised)
        self.monitor.setObjectName("monitor")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.monitor)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        #CUADRO ARRIBA
        self.cuadroarriba = QtWidgets.QFrame(self.monitor)
        self.cuadroarriba.setEnabled(True)
        self.cuadroarriba.setMinimumSize(QtCore.QSize(100, 100))
        self.cuadroarriba.setMaximumSize(QtCore.QSize(16777215, 200))
        self.cuadroarriba.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cuadroarriba.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cuadroarriba.setObjectName("cuadroarriba")

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.cuadroarriba)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(8)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.boton_paciente = QtWidgets.QPushButton(self.cuadroarriba)
        self.boton_paciente.setMinimumSize(QtCore.QSize(100, 50))
        self.boton_paciente.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.boton_paciente.setFont(font)
        self.boton_paciente.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.boton_paciente.setObjectName("boton_paciente")
        self.horizontalLayout_4.addWidget(self.boton_paciente)

        self.boton_historial = QtWidgets.QPushButton(self.cuadroarriba)
        self.boton_historial.setMinimumSize(QtCore.QSize(100, 50))
        self.boton_historial.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.boton_historial.setFont(font)
        self.boton_historial.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.boton_historial.setObjectName("boton_historial")
        self.horizontalLayout_4.addWidget(self.boton_historial)

        self.timeEdit_duracion = QtWidgets.QTimeEdit(self.cuadroarriba)
        self.timeEdit_duracion.setDisplayFormat("hh:mm:ss")
        self.timeEdit_duracion.setMinimumSize(QtCore.QSize(250, 65))
        self.timeEdit_duracion.setMaximumSize(QtCore.QSize(300, 16777215))
        self.timeEdit_duracion.setObjectName("timeEdit_duracion")
        self.timeEdit_duracion.setStyleSheet("color: white;")
        self.horizontalLayout_4.addWidget(self.timeEdit_duracion)

        self.label_ID = QtWidgets.QLabel(self.cuadroarriba)
        self.label_ID.setMinimumSize(QtCore.QSize(200, 65))
        self.label_ID.setMaximumSize(QtCore.QSize(400, 16777215))
        self.label_ID.setObjectName("label_ID")
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(True)
        self.label_ID.setWordWrap(True)
        self.label_ID.setFont(font)
        self.label_ID.setStyleSheet("background-color: rgb(0,0,0); \n " "color: rgb(255, 255, 255);")
        self.horizontalLayout_4.addWidget(self.label_ID)

        self.label_nombre = QtWidgets.QLabel(self.cuadroarriba)
        self.label_nombre.setMinimumSize(QtCore.QSize(200, 65))
        self.label_nombre.setMaximumSize(QtCore.QSize(700, 16777215))
        self.label_nombre.setObjectName("label_nombre")
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        self.label_nombre.setFont(font)
        self.label_nombre.setStyleSheet("background-color: rgb(0,0,0); \n " "color: rgb(255, 255, 255);")
        self.horizontalLayout_4.addWidget(self.label_nombre)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        self.fechayhora = QtWidgets.QDateTimeEdit(self.cuadroarriba)
        self.fechayhora.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.fechayhora.setMinimumSize(QtCore.QSize(400, 90))
        self.fechayhora.setMaximumSize(QtCore.QSize(500, 16777215))
        self.fechayhora.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.fechayhora.setObjectName("fechayhora")
        self.horizontalLayout_4.addWidget(self.fechayhora)
        self.verticalLayout_2.addWidget(self.cuadroarriba)

        #CUADRO MEDIO
        self.cuadromedio = QtWidgets.QFrame(self.monitor)
        self.cuadromedio.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cuadromedio.setStyleSheet("border-color: rgb(156, 156, 156);")
        self.cuadromedio.setFrameShape(QtWidgets.QFrame.Box)
        self.cuadromedio.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cuadromedio.setLineWidth(1)
        self.cuadromedio.setObjectName("cuadromedio")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.cuadromedio)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 2)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        #SENALES Y ALARMAS
        self.frame_senales = QtWidgets.QFrame(self.cuadromedio)
        self.frame_senales.setMinimumSize(QtCore.QSize(0, 800))
        self.frame_senales.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_senales.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_senales.setObjectName("frame_senales")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_senales)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")

        #ALARMAS Y DOC
        self.frame_alarmas = QtWidgets.QFrame(self.frame_senales)
        self.frame_alarmas.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_alarmas.setMaximumSize(QtCore.QSize(1683940, 80))
        self.frame_alarmas.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_alarmas.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_alarmas.setObjectName("frame_alarmas")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_alarmas)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.alarmas = QtWidgets.QWidget(self.frame_alarmas)
        self.alarmas.setMaximumSize(QtCore.QSize(1645433, 130))
        self.alarmas.setObjectName("alarmas")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.alarmas)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label_doc = QtWidgets.QLabel(self.alarmas)
        self.label_doc.setMinimumSize(QtCore.QSize(400, 0))
        self.label_doc.setMaximumSize(QtCore.QSize(16777215, 130))
        self.label_doc.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_doc.setObjectName("label_doc")
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        self.label_doc.setFont(font)
        self.label_doc.setStyleSheet("background-color: rgb(0,0,0); \n " "color: rgb(255, 255, 255);")
        self.horizontalLayout_2.addWidget(self.label_doc)
        spacerItem1 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        #ALARMA RESPIRACION
        self.alarma_torax_2 = QtWidgets.QLabel(self.alarmas)
        self.alarma_torax_2.setMinimumSize(QtCore.QSize(500, 0))
        self.alarma_torax_2.setMaximumSize(QtCore.QSize(16777215, 130))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.alarma_torax_2.setFont(font)
        self.alarma_torax_2.setStyleSheet("background-color: rgb(237, 218, 233);")
        self.alarma_torax_2.setAlignment(QtCore.Qt.AlignCenter)
        self.alarma_torax_2.setWordWrap(True)
        self.alarma_torax_2.setObjectName("alarma_torax_2")
        self.horizontalLayout_2.addWidget(self.alarma_torax_2)

        #ALARMA SPO2
        self.alarma_spo2 = QtWidgets.QLabel(self.alarmas)
        self.alarma_spo2.setMinimumSize(QtCore.QSize(500, 0))
        self.alarma_spo2.setMaximumSize(QtCore.QSize(16777215, 130))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.alarma_spo2.setFont(font)
        self.alarma_spo2.setStyleSheet("background-color: rgb(217, 244, 250);")
        self.alarma_spo2.setAlignment(QtCore.Qt.AlignCenter)
        self.alarma_spo2.setWordWrap(True)
        self.alarma_spo2.setObjectName("alarma_spo2")
        self.horizontalLayout_2.addWidget(self.alarma_spo2)

        #ALARMA FC
        self.alarma_fc = QtWidgets.QLabel(self.alarmas)
        self.alarma_fc.setMinimumSize(QtCore.QSize(500, 0))
        self.alarma_fc.setMaximumSize(QtCore.QSize(16777215, 130))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.alarma_fc.setFont(font)
        self.alarma_fc.setStyleSheet("background-color: rgb(223, 249, 211);")
        self.alarma_fc.setAlignment(QtCore.Qt.AlignCenter)
        self.alarma_fc.setWordWrap(True)
        self.alarma_fc.setObjectName("alarma_fc")
        self.horizontalLayout_2.addWidget(self.alarma_fc)
        self.verticalLayout_5.addWidget(self.alarmas)
        self.verticalLayout.addWidget(self.frame_alarmas)

        #SENAL ACC
        self.frame_acc = QtWidgets.QFrame(self.frame_senales)
        self.frame_acc.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_acc.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame_acc.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_acc.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_acc.setObjectName("frame_acc")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_acc)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.widget = QtWidgets.QWidget(self.frame_acc)
        self.widget.setMinimumSize(QtCore.QSize(300, 0))
        self.widget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_6.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_acc = QtWidgets.QLabel(self.widget)
        self.label_acc.setMinimumSize(QtCore.QSize(50, 0))
        self.label_acc.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_acc.setFont(font)
        self.label_acc.setStyleSheet("color: rgb(252, 31, 182);")
        self.label_acc.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_acc.setAlignment(QtCore.Qt.AlignCenter)
        self.label_acc.setWordWrap(True)
        self.label_acc.setObjectName("label_acc")
        self.verticalLayout_6.addWidget(self.label_acc)
        self.horizontalLayout_10.addWidget(self.widget)
        self.frame_acc_senal = QtWidgets.QFrame(self.frame_acc)
        self.frame_acc_senal.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame_acc_senal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_acc_senal.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_acc_senal.setObjectName("frame_acc_senal")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_acc_senal)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.graphicsView_acc = pg.PlotWidget(self.frame_acc_senal)
        self.graphicsView_acc.setObjectName("graphicsView_acc")
        self.horizontalLayout_3.addWidget(self.graphicsView_acc)

        #SENAL SPO2
        self.frame_spo2_2 = QtWidgets.QFrame(self.frame_acc_senal)
        self.frame_spo2_2.setMinimumSize(QtCore.QSize(280, 300))
        self.frame_spo2_2.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame_spo2_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_spo2_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_spo2_2.setObjectName("frame_spo2_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_spo2_2)
        self.verticalLayout_7.setContentsMargins(20, 110, 20, 130)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
       
        self.label_spo2 = QtWidgets.QLabel(self.frame_spo2_2)
        self.label_spo2.setMinimumSize(QtCore.QSize(230, 70))
        self.label_spo2.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_spo2.setFont(font)
        self.label_spo2.setStyleSheet("color: rgb(51, 181, 209)")
        self.label_spo2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_spo2.setWordWrap(True)
        self.label_spo2.setObjectName("label_spo2")
        self.verticalLayout_7.addWidget(self.label_spo2)
        self.lcdNumber_spo2 = QtWidgets.QLCDNumber(self.frame_spo2_2)
        self.lcdNumber_spo2.setMinimumSize(QtCore.QSize(200, 400))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        self.lcdNumber_spo2.setFont(font)
        self.lcdNumber_spo2.setStyleSheet("color: rgb(51, 181, 209);\n"
"font: 20pt \"MS Shell Dlg 2\";")
        self.lcdNumber_spo2.setObjectName("lcdNumber_spo2")
        self.verticalLayout_7.addWidget(self.lcdNumber_spo2)
        self.horizontalLayout_3.addWidget(self.frame_spo2_2)
        self.horizontalLayout_10.addWidget(self.frame_acc_senal)
        self.verticalLayout.addWidget(self.frame_acc)

        #SENAL Fc
        self.frame_fc = QtWidgets.QFrame(self.frame_senales)
        self.frame_fc.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_fc.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame_fc.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_fc.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_fc.setObjectName("frame_fc")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_fc)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.widget_fc_label = QtWidgets.QWidget(self.frame_fc)
        self.widget_fc_label.setMinimumSize(QtCore.QSize(300, 0))
        self.widget_fc_label.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widget_fc_label.setObjectName("widget_fc_label")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.widget_fc_label)
        self.gridLayout_13.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_fc = QtWidgets.QLabel(self.widget_fc_label)
        self.label_fc.setMinimumSize(QtCore.QSize(70, 0))
        self.label_fc.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_fc.setFont(font)
        self.label_fc.setStyleSheet("color: rgb(92, 180, 51);\n""")
        self.label_fc.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fc.setWordWrap(True)
        self.label_fc.setObjectName("label_fc")
        self.gridLayout_13.addWidget(self.label_fc, 0, 0, 1, 1)
        self.horizontalLayout_12.addWidget(self.widget_fc_label)
        self.frame_fc_senal = QtWidgets.QFrame(self.frame_fc)
        self.frame_fc_senal.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame_fc_senal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_fc_senal.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_fc_senal.setObjectName("frame_fc_senal")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_fc_senal)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.graphicsView_fc = pg.PlotWidget(self.frame_fc_senal)
        self.graphicsView_fc.setObjectName("graphicsView_fc")
        self.verticalLayout_14.addWidget(self.graphicsView_fc)
        self.horizontalLayout_12.addWidget(self.frame_fc_senal)
        self.frame_fc_num = QtWidgets.QFrame(self.frame_fc)
        self.frame_fc_num.setMinimumSize(QtCore.QSize(300, 200))
        self.frame_fc_num.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.frame_fc_num.setFont(font)
        self.frame_fc_num.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_fc_num.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_fc_num.setObjectName("frame_fc_num")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.frame_fc_num)
        self.gridLayout_15.setContentsMargins(0, 120, 0, 260)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.verticalLayout_label_lcd = QtWidgets.QVBoxLayout()
        self.verticalLayout_label_lcd.setObjectName("verticalLayout_label_lcd")
        self.label_bpm = QtWidgets.QLabel(self.frame_fc_num)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_bpm.setFont(font)
        self.label_bpm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_bpm.setStyleSheet("color: rgb(92, 180, 51);")
        self.label_bpm.setObjectName("label")
        self.verticalLayout_label_lcd.addWidget(self.label_bpm)
        self.lcdNumber_FC = QtWidgets.QLCDNumber(self.frame_fc_num)
        self.lcdNumber_FC.setMinimumSize(QtCore.QSize(250, 400))
        self.lcdNumber_FC.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_FC.setStyleSheet("color: rgb(92, 180, 51);\n" "font: 25pt \"MS Shell Dlg 2\";")
        self.lcdNumber_FC.setFrameShape(QtWidgets.QFrame.Box)
        self.lcdNumber_FC.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcdNumber_FC.setObjectName("lcdNumber_FC")
        self.verticalLayout_label_lcd.addWidget(self.lcdNumber_FC)
        self.verticalLayout_label_lcd.setContentsMargins(0, 100, 50, 50)
        self.verticalLayout_label_lcd.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_15.addLayout(self.verticalLayout_label_lcd, 0, 0, 1, 2)

        self.horizontalLayout_12.addWidget(self.frame_fc_num)

        self.verticalLayout.addWidget(self.frame_fc)
        self.horizontalLayout_5.addWidget(self.frame_senales)


        #TENDENCIAS
        self.tendencias = QtWidgets.QFrame(self.cuadromedio)
        self.tendencias.setMinimumSize(QtCore.QSize(650, 500))
        self.tendencias.setMaximumSize(QtCore.QSize(700, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tendencias.setFont(font)
        self.tendencias.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.tendencias.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tendencias.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tendencias.setObjectName("tendencias")

        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tendencias)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")

        self.frame_ultimashs = QtWidgets.QFrame(self.tendencias)
        self.frame_ultimashs.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_ultimashs.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_ultimashs.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_ultimashs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ultimashs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ultimashs.setObjectName("frame_ultimashs")

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_ultimashs)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.label_ultimas = QtWidgets.QLabel(self.frame_ultimashs)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_ultimas.setFont(font)
        self.label_ultimas.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_ultimas.setObjectName("label_ultimas")
        self.horizontalLayout_6.addWidget(self.label_ultimas)

        self.comboBox = QtWidgets.QComboBox(self.frame_ultimashs)
        self.comboBox.setMinimumSize(QtCore.QSize(97, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.horizontalLayout_6.addWidget(self.comboBox)
        self.verticalLayout_11.addWidget(self.frame_ultimashs)

        self.frame_6 = QtWidgets.QFrame(self.tendencias)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 800))
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 1000))
        self.frame_6.setObjectName("frame_6")

        self.gridLayout = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")

        #IZQUIERDA LABELS
        self.frame_izq = QtWidgets.QFrame(self.frame_6)
        self.frame_izq.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.frame_izq.setFont(font)
        self.frame_izq.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.frame_izq.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_izq.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_izq.setObjectName("frame_izq")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_izq)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.frame = QtWidgets.QFrame(self.frame_izq)
        self.frame.setMinimumSize(QtCore.QSize(100, 0))
        self.frame.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.label_uno_izq = QtWidgets.QLabel(self.frame)
        self.label_uno_izq.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_uno_izq.setFont(font)
        self.label_uno_izq.setWordWrap(True)
        self.label_uno_izq.setAlignment(QtCore.Qt.AlignCenter)
        self.label_uno_izq.setObjectName("label_uno_izq")
        self.gridLayout_2.addWidget(self.label_uno_izq, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame)

        self.frame_dos = QtWidgets.QFrame(self.frame_izq)
        self.frame_dos.setMinimumSize(QtCore.QSize(110, 0))
        self.frame_dos.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_dos.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dos.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dos.setObjectName("frame_dos")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_dos)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.label_dos_izq = QtWidgets.QLabel(self.frame_dos)
        self.label_dos_izq.setMinimumSize(QtCore.QSize(110, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_dos_izq.setFont(font)
        self.label_dos_izq.setWordWrap(True)
        self.label_dos_izq.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dos_izq.setObjectName("label_dos_izq")
        self.gridLayout_3.addWidget(self.label_dos_izq, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_dos)

        self.frame_tres = QtWidgets.QFrame(self.frame_izq)
        self.frame_tres.setMinimumSize(QtCore.QSize(100, 0))
        self.frame_tres.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_tres.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tres.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tres.setObjectName("frame_tres")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_tres)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.label_5_izq = QtWidgets.QLabel(self.frame_tres)
        self.label_5_izq.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_5_izq.setFont(font)
        self.label_5_izq.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5_izq.setWordWrap(True)
        self.label_5_izq.setObjectName("label_5_izq")
        self.gridLayout_4.addWidget(self.label_5_izq, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_tres)

        self.frame_5 = QtWidgets.QFrame(self.frame_izq)
        self.frame_5.setMinimumSize(QtCore.QSize(100, 0))
        self.frame_5.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")

        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.label_5_izq_2 = QtWidgets.QLabel(self.frame_5)
        self.label_5_izq_2.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_5_izq_2.setFont(font)
        self.label_5_izq_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5_izq_2.setWordWrap(True)
        self.label_5_izq_2.setObjectName("label_5_izq_2")
        self.gridLayout_5.addWidget(self.label_5_izq_2, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_5)

        self.frame_cuatro = QtWidgets.QFrame(self.frame_izq)
        self.frame_cuatro.setMinimumSize(QtCore.QSize(100, 0))
        self.frame_cuatro.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_cuatro.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_cuatro.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_cuatro.setObjectName("frame_cuatro")

        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_cuatro)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.label_cuatro_izq = QtWidgets.QLabel(self.frame_cuatro)
        self.label_cuatro_izq.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_cuatro_izq.setFont(font)
        self.label_cuatro_izq.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cuatro_izq.setWordWrap(True)
        self.label_cuatro_izq.setObjectName("label_cuatro_izq")
        self.gridLayout_6.addWidget(self.label_cuatro_izq, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_cuatro)
        self.gridLayout.addWidget(self.frame_izq, 0, 0, 5, 1)

        #DERECHA LCDNUMBERS
        self.frame_2_der = QtWidgets.QFrame(self.frame_6)
        self.frame_2_der.setMinimumSize(QtCore.QSize(55, 0))
        self.frame_2_der.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_2_der.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2_der.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2_der.setObjectName("frame_2_der")

        self.gridLayout_11 = QtWidgets.QGridLayout(self.frame_2_der)
        self.gridLayout_11.setObjectName("gridLayout_11")

        self.lcdNumber_NApneas = QtWidgets.QLCDNumber(self.frame_2_der)
        self.lcdNumber_NApneas.setMinimumSize(QtCore.QSize(350, 0))
        self.lcdNumber_NApneas.setMaximumSize(QtCore.QSize(350, 16777215))
        self.lcdNumber_NApneas.setObjectName("lcdNumber_NApneas")

        self.gridLayout_11.addWidget(self.lcdNumber_NApneas, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem4, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_2_der, 0, 1, 1, 1)

        self.frame_dos_der = QtWidgets.QFrame(self.frame_6)
        self.frame_dos_der.setMinimumSize(QtCore.QSize(55, 0))
        self.frame_dos_der.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_dos_der.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dos_der.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dos_der.setObjectName("frame_dos_der")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frame_dos_der)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.lcdNumber_maxPR = QtWidgets.QLCDNumber(self.frame_dos_der)
        self.lcdNumber_maxPR.setMinimumSize(QtCore.QSize(350, 0))
        self.lcdNumber_maxPR.setMaximumSize(QtCore.QSize(450, 16777215))
        self.lcdNumber_maxPR.setObjectName("lcdNumber_maxPR")
        self.gridLayout_10.addWidget(self.lcdNumber_maxPR, 0, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem5, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_dos_der, 1, 1, 1, 1)

        self.frame_tres_der = QtWidgets.QFrame(self.frame_6)
        self.frame_tres_der.setMinimumSize(QtCore.QSize(55, 0))
        self.frame_tres_der.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_tres_der.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tres_der.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tres_der.setObjectName("frame_tres_der")

        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_tres_der)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.lcdNumber_MinSpo2 = QtWidgets.QLCDNumber(self.frame_tres_der)
        self.lcdNumber_MinSpo2.setMinimumSize(QtCore.QSize(350, 0))
        self.lcdNumber_MinSpo2.setMaximumSize(QtCore.QSize(450, 16777215))
        self.lcdNumber_MinSpo2.setObjectName("lcdNumber_MinSpo2")
        self.gridLayout_9.addWidget(self.lcdNumber_MinSpo2, 0, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem6, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_tres_der, 2, 1, 1, 1)

        self.frame_2 = QtWidgets.QFrame(self.frame_6)
        self.frame_2.setMinimumSize(QtCore.QSize(55, 0))
        self.frame_2.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_8.setObjectName("gridLayout_8")

        self.lcdNumber_minFC = QtWidgets.QLCDNumber(self.frame_2)
        self.lcdNumber_minFC.setMinimumSize(QtCore.QSize(350, 0))
        self.lcdNumber_minFC.setMaximumSize(QtCore.QSize(450, 16777215))
        self.lcdNumber_minFC.setObjectName("lcdNumber_minFC")
        self.gridLayout_8.addWidget(self.lcdNumber_minFC, 0, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem7, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 3, 1, 1, 1)

        self.frame_cuatro_der = QtWidgets.QFrame(self.frame_6)
        self.frame_cuatro_der.setMinimumSize(QtCore.QSize(55, 0))
        self.frame_cuatro_der.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.frame_cuatro_der.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_cuatro_der.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_cuatro_der.setObjectName("frame_cuatro_der")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_cuatro_der)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.lcdNumber_maxFC = QtWidgets.QLCDNumber(self.frame_cuatro_der)
        self.lcdNumber_maxFC.setMinimumSize(QtCore.QSize(350, 0))
        self.lcdNumber_maxFC.setMaximumSize(QtCore.QSize(450, 16777215))
        self.lcdNumber_maxFC.setObjectName("lcdNumber_maxFC")

        self.gridLayout_7.addWidget(self.lcdNumber_maxFC, 0, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem8, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_cuatro_der, 4, 1, 1, 1)
        self.verticalLayout_11.addWidget(self.frame_6)

        self.label_vacio = QtWidgets.QLabel(self.tendencias)
        self.label_vacio.setObjectName("label_vacio")
        self.verticalLayout_11.addWidget(self.label_vacio)

        #ALARMAS CONFIGURABLES
        self.frame_alarmasconf = QtWidgets.QFrame(self.tendencias)
        self.frame_alarmasconf.setMinimumSize(QtCore.QSize(0, 400))
        self.frame_alarmasconf.setMaximumSize(QtCore.QSize(16777215, 650))
        self.frame_alarmasconf.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.frame_alarmasconf.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_alarmasconf.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_alarmasconf.setObjectName("frame_alarmasconf")

        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_alarmasconf)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        
        #Titulo
        self.frame_titconfig = QtWidgets.QFrame(self.frame_alarmasconf)
        self.frame_titconfig.setMinimumSize(QtCore.QSize(0, 63))
        self.frame_titconfig.setMaximumSize(QtCore.QSize(16777215, 63))
        self.frame_titconfig.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_titconfig.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_titconfig.setObjectName("frame_titconfig")

        self.gridLayout_15 = QtWidgets.QGridLayout(self.frame_titconfig)
        self.gridLayout_15.setContentsMargins(4, 0, 4, 0)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName("gridLayout_15")

        self.label_2 = QtWidgets.QLabel(self.frame_titconfig)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout_15.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout_10.addWidget(self.frame_titconfig)

        self.frame_config = QtWidgets.QFrame(self.frame_alarmasconf)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.frame_config.setFont(font)
        self.frame_config.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_config.setMaximumSize(QtCore.QSize(16777215, 400))
        self.frame_config.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.frame_config.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_config.setObjectName("frame_config")

        self.gridLayout_16 = QtWidgets.QGridLayout(self.frame_config)
        self.gridLayout_16.setContentsMargins(3, 0, 3, 0)
        self.gridLayout_16.setSpacing(6)
        self.gridLayout_16.setObjectName("gridLayout_16")

        #ALARMA CONF FC
        self.label_FC_conf = QtWidgets.QLabel(self.frame_config)
        self.label_FC_conf.setMinimumSize(QtCore.QSize(240, 120))
        self.label_FC_conf.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_FC_conf.setFont(font)
        self.label_FC_conf.setAlignment(QtCore.Qt.AlignCenter)
        self.label_FC_conf.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.label_FC_conf.setWordWrap(True)
        self.label_FC_conf.setObjectName("label_FC_conf")
        self.gridLayout_16.addWidget(self.label_FC_conf, 0, 0, 1, 1)

        self.lineEdit_conf_FC = QtWidgets.QLineEdit(self.frame_config)
        self.lineEdit_conf_FC.setMinimumSize(QtCore.QSize(0, 120))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_conf_FC.setFont(font)
        self.lineEdit_conf_FC.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_conf_FC.setObjectName("lineEdit_conf_FC")
        self.lineEdit_conf_FC.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.gridLayout_16.addWidget(self.lineEdit_conf_FC, 0, 1, 1, 1)

        #ALARMA CONF SPO2
        self.label_SpO2_conf = QtWidgets.QLabel(self.frame_config)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_SpO2_conf.setFont(font)
        self.label_SpO2_conf.setAlignment(QtCore.Qt.AlignCenter)
        self.label_SpO2_conf.setMinimumSize(QtCore.QSize(0, 120))
        self.label_SpO2_conf.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.label_SpO2_conf.setWordWrap(True)
        self.label_SpO2_conf.setObjectName("label_SpO2_conf")
        self.gridLayout_16.addWidget(self.label_SpO2_conf, 1, 0, 1, 1)

        self.lineEdit_SpO2_conf = QtWidgets.QLineEdit(self.frame_config)
        self.lineEdit_SpO2_conf.setMinimumSize(QtCore.QSize(0, 120))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_SpO2_conf.setFont(font)
        self.lineEdit_SpO2_conf.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_SpO2_conf.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.lineEdit_SpO2_conf.setObjectName("lineEdit_SpO2_conf")
        self.gridLayout_16.addWidget(self.lineEdit_SpO2_conf, 1, 1, 1, 1)

        #ALARMA CONF RESPIRACION
        self.label_Resp_conf = QtWidgets.QLabel(self.frame_config)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_Resp_conf.setFont(font)
        self.label_Resp_conf.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Resp_conf.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.label_Resp_conf.setMinimumSize(QtCore.QSize(0, 120))
        self.label_Resp_conf.setWordWrap(True)
        self.label_Resp_conf.setObjectName("label_Resp_conf")
        self.gridLayout_16.addWidget(self.label_Resp_conf, 2, 0, 1, 1)

        self.comboBox_resp_conf = QtWidgets.QComboBox(self.frame_config)
        self.comboBox_resp_conf.setMinimumSize(QtCore.QSize(0, 120))
        self.comboBox_resp_conf.setStyleSheet("background-color: rgb(156,156,156); \n " "color: rgb(0, 0, 0);")
        self.comboBox_resp_conf.setObjectName("comboBox_resp_conf")
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_resp_conf.setFont(font)
        self.comboBox_resp_conf.addItem("")
        self.comboBox_resp_conf.addItem("")
        self.comboBox_resp_conf.addItem("")
        self.comboBox_resp_conf.addItem("")
        self.gridLayout_16.addWidget(self.comboBox_resp_conf, 2, 1, 1, 1)
        self.verticalLayout_10.addWidget(self.frame_config)
        self.verticalLayout_11.addWidget(self.frame_alarmasconf)
        
        self.label_pokayoke = QtWidgets.QLabel(self.tendencias)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_pokayoke.setFont(font)
        self.label_pokayoke.setMinimumSize(QtCore.QSize(0, 100))
        self.label_pokayoke.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pokayoke.setStyleSheet("color: red;")
        self.label_pokayoke.setWordWrap(True)
        self.label_pokayoke.setObjectName("label_pokayoke")
        
        self.verticalLayout_11.addWidget(self.label_pokayoke)
        self.horizontalLayout_5.addWidget(self.tendencias)
        self.verticalLayout_2.addWidget(self.cuadromedio)
        self.horizontalLayout.addWidget(self.monitor)
        MainWindow.setCentralWidget(self.centralwidget)

        #CONECTAR BOTONES y flags
        self.comboBox_resp_conf.currentIndexChanged.connect(self.umbral_respiracion)
        self.lineEdit_conf_FC.returnPressed.connect(self.umbral_fc)
        self.lineEdit_SpO2_conf.returnPressed.connect(self.umbral_SPO2)
        self.boton_paciente.clicked.connect(self.abrir_ventana_paciente)
        self.boton_historial.clicked.connect(self.abrir_apnea)
        self.ventana_apnea = None
        self.ventana_paciente = None

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    #UMBRALES ALARMAS CONF
    def umbral_respiracion(self,index):
        global umbral
        if index==0:
            umbral=18500
        if index==1:
            umbral=20000
        if index==2:
            umbral=17500

    def umbral_fc(self):
        global umbral_hr
        umbral_hr = int(self.lineEdit_conf_FC.text())
        if umbral_hr<70 or umbral_hr>180:
            self.label_pokayoke.setText('El valor ingresado no es válido.\nDebe estar entre 70 y 180 lpm')
            umbral_hr=100
        else:
            self.label_pokayoke.setText('')

        
    def umbral_SPO2(self):
        global umbral_spo2
        umbral_spo2 = int(self.lineEdit_SpO2_conf.text())
        if umbral_spo2>100 or umbral_spo2<50:
            self.label_pokayoke.setText('El valor ingresado no es válido.\nDebe estar entre 50 y 100 %')
            umbral_spo2=80
        else:
            self.label_pokayoke.setText('')

    #VENTANA PACIENTE o sea la primera que aparece cuando tocas paciente en monitor
    def abrir_ventana_paciente(self):
        if self.ventana_paciente is None:
            self.ventana_paciente = QtWidgets.QMainWindow()
            self.ui3 = AbrirVentanaPaciente()
            self.ui3.setupUi(self.ventana_paciente)
            self.ui3.boton_guardar.clicked.connect(self.leer_id)
            self.ui3.boton_atras.clicked.connect(self.cerrar_ventana_paciente)
            self.registrar_paciente = None
        self.ventana_paciente.show()

    def cerrar_ventana_paciente(self):
        if self.ventana_paciente is not None:
            self.ventana_paciente.close()
            self.ventana_paciente = None

    #ID
    def leer_id(self):
        self.id=self.ui3.lineEdit_ID.text()
        doc=db.document('pacientes/'+str(self.id))
        document=db.collection('pacientes').document(str(self.id)).get()
        if document.exists:
            global ID
            ID=self.id
            global bandera_definir_ID
            bandera_definir_ID=True
            self.visualizar_datos_paciente()

            #self.pasar_id.emit(self.id)
        else:
            self.abrir_registrar_paciente()

    #REGISTRAR PACIENTE aparece cuando tocas guardar en ventana paciente
    def abrir_registrar_paciente(self):
        if  self.registrar_paciente is None:
            self.registrar_paciente = QtWidgets.QMainWindow()
            self.ui2 = RegistrarDatosPaciente()
            self.ui2.setupUi(self.registrar_paciente)
            self.ui2.boton_historial.clicked.connect(self.abrir_apnea)
            self.ui2.boton_guardar.clicked.connect(self.guardar_texto)
        self.registrar_paciente.show()

    #VISUALIZAR DATOS aparece cuando tenes el ID ya
    def visualizar_datos_paciente(self):
        self.visualizar_paciente = QtWidgets.QMainWindow()
        self.ui3 = AbrirDatosPaciente()
        self.ui3.setupUi(self.visualizar_paciente)
        self.ui3.boton_historial.clicked.connect(self.abrir_apnea)
        self.ui3.boton_atras.clicked.connect(self.cerrar_visualizar)
        self.visualizar_paciente.show()
        document=db.collection('pacientes').document(str(self.id)).get()
        datos = document.to_dict()
        nombre = datos.get("Nombre")
        apellido = datos.get("Apellido")
        fecha_nacimiento = datos.get("fecha_nacimiento")
        fecha_utin=datos.get("fecha_utin")
        peso_actual=datos.get("peso_actual")
        peso_nacimiento=datos.get("peso_nacimiento")
        medico=datos.get("id_medico")
        self.ui3.label_10.setText(str(self.id))
        self.ui3.label_16.setText(str(nombre))
        self.ui3.label_11.setText(str(apellido))
        self.ui3.label_13.setText(str(fecha_nacimiento))
        self.ui3.label_17.setText(str(fecha_utin))
        self.ui3.label_19.setText(str(peso_actual))
        self.ui3.label_15.setText(str(peso_nacimiento))
        self.ui3.label_18.setText(str(medico))
        self.label_nombre.setText(str(nombre)+str(" ")+str(apellido)+str(" ")+str(fecha_utin)+str(" ")+str(peso_actual)+str('g'))
        self.label_doc.setText('Dr: '+ str(medico))

    def cerrar_visualizar(self):
        self.visualizar_paciente.close()

    #GUARDAR TEXTO
    def guardar_texto(self):
        #self.guardar_paciente = QtWidgets.QMainWindow()
        nombre = self.ui2.lineEdit_nombre.text()
        apellido= self.ui2.lineEdit_apellido.text()
        fechanac= self.ui2.lineEdit_fechanac.text()
        fechaingreso = self.ui2.lineEdit_fechaingreso.text()
        #meses = self.ui2.lineEdit_meses.text()
        pesoactual = self.ui2.lineEdit_pesoactual.text()
        pesonacer = self.ui2.lineEdit_pesonacer.text()
        idmedico = self.ui2.lineEdit_idmedico.text()
        self.id = nombre[:3] + apellido[:3] + fechaingreso
        #self.pasar_id.emit(self.id)

        self.label_nombre.setText(str(nombre)+str(" ")+str(apellido)+str(" ")+str(fechaingreso)+str(" ")+str(pesoactual))
        self.label_doc.setText('Dr: '+ str(idmedico))
        doc = db.document('pacientes/'+str(self.id))
        document=db.collection('pacientes').document(str(self.id)).get()
        if document.exists:
            pass
        else:
            nuevo_data = {
                # Define los campos y valores que deseas en el nuevo documento
                'Apellido': apellido,
                'Nombre': nombre,
                'fecha_nacimiento': fechanac,
                'fecha_utin': fechaingreso,
                'id_medico': idmedico,
                'peso_actual': pesoactual,
                'peso_nacimiento': pesonacer,
                'n_apneas': 0
            }
            doc.set(nuevo_data)
        global ID
        ID=self.id
        global bandera_definir_ID
        bandera_definir_ID=True
        self.registrar_paciente.close()

    #APNEAS que se abre siempre que tocas historial
    def abrir_apnea(self):
        if self.ventana_apnea is None:
            self.ventana_apnea = QtWidgets.QMainWindow()
            self.ui4 = AbrirApneas()
            self.ui4.setupUi(self.ventana_apnea)
            self.ui4.boton_atras.clicked.connect(self.cerrar_apnea)
            self.ui4.pushButton_PDF.clicked.connect(self.descargar_pdf)
        self.ventana_apnea.show()
        self.ui4.label_idescribir.setText(str(self.id))
        global ID
        if ID != None:
            doc1 = db.document('pacientes/'+ID).get()
            data = doc1.to_dict()
            self.n_apneas = data.get('n_apneas')
            nombre=data.get('Nombre')
            apellido=data.get('Apellido')
            self.ui4.label_nombreap.setText(nombre+ str(" ") + apellido)
            self.ui4.comboBox.addItem('Resumen')
            _translate = QtCore.QCoreApplication.translate
            self.ui4.comboBox.setItemText(0, _translate("MainWindow", 'Resumen'))
            apneas = []
            HRs_min = []
            spo2s_min = []
            PRs = []
            for i in range(self.n_apneas):
                self.ui4.comboBox.addItem(str(i+1))
                _translate = QtCore.QCoreApplication.translate
                self.ui4.comboBox.setItemText(i+1, _translate("MainWindow", str(i+1)))
                doc1 = db.document('pacientes/'+ID+'/Apneas/Apnea'+str(i+1)).get()
                data = doc1.to_dict()
                HR_min = data.get('HR_min')
                HRs_min.append(HR_min)
                spo2_min=data.get('SpO2_min')
                spo2s_min.append(spo2_min)
                PR=data.get('pausa_respiratoria')
                PRs.append(PR)
                apneas.append('Apnea'+str(i+1))
            self.grafico_path=self.generar_grafico(apneas, HRs_min, spo2s_min, PRs)
            self.ui4.label_Napenas.setText(str(self.n_apneas))
            pixmap = QPixmap(self.grafico_path)
            
            if not pixmap.isNull():
            # Establecer la imagen en el QLabel
                self.ui4.label_grafico.setPixmap(pixmap)
                # Ajustar el tamaño del QLabel al tamaño de la imagen
                self.ui4.label_grafico.setScaledContents(True)
            else:
                pass
            self.ui4.comboBox.setCurrentIndex(0)
            self.ui4.comboBox.currentIndexChanged.connect(self.historial_apneas)
        else:
            pass
    
    #PDF    
    def descargar_pdf(self):
        doc1 = db.document('pacientes/'+ID).get()
        data = doc1.to_dict()
        nombre=data.get('Nombre')
        apellido=data.get('Apellido')
        fecha_nac=data.get('fecha_nacimiento')
        fecha_utin=data.get('fecha_utin')
        id_medico=data.get('id_medico')
        peso_actual=data.get('peso_actual')
        peso_nacimiento=data.get('peso_nacimiento')
        apneas=data.get('n_apneas')
        # Crea un nuevo archivo PDF
        descargas_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # Construye la ruta completa al archivo PDF en la carpeta "Descargas"
        nombre_archivo_base=str(ID)
        ruta_completa_pdf = os.path.join(descargas_path,nombre_archivo_base)

        contador = 1

        # Construye el nombre completo del archivo PDF
        ruta_completa_pdf = os.path.join(descargas_path, f"{nombre_archivo_base}_{contador}.pdf")

        # Incrementa el contador mientras el archivo ya existe
        while os.path.exists(ruta_completa_pdf):
            contador += 1
            ruta_completa_pdf = os.path.join(descargas_path, f"{nombre_archivo_base}_{contador}.pdf")

        # Crea un objeto de documento PDF
        pdf = SimpleDocTemplate(ruta_completa_pdf, pagesize=letter)
        

        # Configura estilos para el documento
        estilos = getSampleStyleSheet()
        estilo_titulo = estilos["Title"]
        estilo_normal = estilos["Normal"]
        datos_paciente = f"{nombre} {apellido}<br/>Fecha de Nacimiento: {fecha_nac}<br/>Fecha de ingreso a UTIN: {fecha_utin}<br/>Peso actual: {peso_actual}<br/>Peso al nacer: {peso_nacimiento}"
        datos_medico = id_medico
        maquina = 'Monitor Apnea Nro de registro 0000'
        hospital = 'Cemic'
        textedit = self.ui4.textEdit.toPlainText()
        # Lista de elementos a agregar al PDF
        contenido = [
            Paragraph("Informe Médico", estilo_titulo),
            Paragraph(f"Fecha de Descarga: {self.get_fecha_actual()}", estilo_normal),
            Paragraph(f"Datos del Paciente: {datos_paciente}", estilo_normal),
            Paragraph(f"Datos del Médico: {datos_medico}", estilo_normal),
            Paragraph(f"Máquina: {maquina}", estilo_normal),
            Paragraph(f"Hospital: {hospital}", estilo_normal),
            Spacer(0, 20),
            Paragraph(f"{textedit}", estilo_normal),
            Paragraph("Detalles de las Apneas", estilo_titulo),
            Paragraph(f"Total de Apneas: {apneas}", estilo_normal),
            Spacer(0, 20),
            Paragraph("Detalles de cada Apnea:", estilo_normal),
        ]
        HRs_min=[]
        spo2s_min=[]
        PRs=[]
        for i in range(apneas):
            doc2 = db.document('pacientes/'+ID+'/Apneas/Apnea'+str(i+1)).get()
            data2 = doc2.to_dict()
            HR_min = data2.get('HR_min')
            HRs_min.append(HR_min)
            spo2_min=data2.get('SpO2_min')
            spo2s_min.append(spo2_min)
            PR=data2.get('pausa_respiratoria')
            PRs.append(PR)

        # Agrega detalles de cada apnea
        for i in range(apneas):
            contenido.append(Paragraph(f"Apnea {i+1}:", estilo_normal))
            contenido.append(Paragraph(f"  - FC mínima: {HRs_min[i]}", estilo_normal))
            contenido.append(Paragraph(f"  - SpO2 mínima: {spo2s_min[i]}", estilo_normal))
            contenido.append(Paragraph(f"  - Pausa Respiratoria: {PRs[i]}", estilo_normal))
            contenido.append(Spacer(0, 10))

        contenido.append(Spacer(0, apneas*35))

        # Agrega el gráfico de barras al PDF
        if self.grafico_path:
            #contenido.append(Paragraph("Gráfico de Barras para cada Apnea y Parámetro", estilo_titulo))
            contenido.append(Paragraph("<img src='{}' width='500' height='300'/>".format(self.grafico_path), estilo_normal))
            contenido.append(Spacer(0, 20))  # Agregar espacio después del gráfico

        # Agrega el contenido al PDF
        pdf.build(contenido)

        return ruta_completa_pdf

    def get_fecha_actual(self):
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generar_grafico(self,apneas, HRs_min, spo2s_min, PRs):
        colores=['#FA92F2', '#92E4FA', '#94E28E']
        ancho_barra = 0.2
        posiciones = np.arange(len(apneas))

        plt.bar(posiciones - 1.5 * ancho_barra, HRs_min, width=ancho_barra, color=colores[0], label='FC mínima')
        plt.bar(posiciones - 0.5 * ancho_barra, spo2s_min, width=ancho_barra, color=colores[1], label='SpO2 mínima')
        plt.bar(posiciones + 0.5 * ancho_barra, PRs, width=ancho_barra, color=colores[2], label='Pausa Respiratoria')

        plt.xlabel('Apneas')
        plt.ylabel('Valores')
        plt.title('Gráfico de Barras para cada Apnea y Parámetro')
        #plt.xticks(posiciones, apneas)
        plt.xticks(posiciones, [i + 1 for i in range(len(apneas))])
        plt.legend()

        contador = 1
        descargas_path = os.path.join(os.path.expanduser("~"), "Downloads")
        grafico_path = os.path.join(descargas_path, f"{ID}_{contador}.png")
        
        while os.path.exists(grafico_path):
            contador += 1
            grafico_path = os.path.join(descargas_path, f"{ID}_{contador}.png")
        plt.savefig(grafico_path)
        plt.close()

        print(grafico_path)
        return grafico_path

    #HISTORIAL CON DATOS
    def historial_apneas(self, index):
        global ID
        if index==0:
            self.ui4.lineEdit_HRmax.setText('')
            self.ui4.lineEdit_HRmin.setText('')
            self.ui4.lineEdit_HRprom.setText('')
            self.ui4.lineEdit_inicio.setText('')
            self.ui4.lineEdit_PR.setText('')
            self.ui4.lineEdit_spo2min.setText('')
            self.ui4.lineEdit_spo2prom.setText('')
        if ID!=None and index!=0:
            doc1 = db.document('pacientes/'+ID+'/Apneas/Apnea'+str(index)).get()
            data = doc1.to_dict()
            HR_max = data.get('HR_max')
            HR_min = data.get('HR_min')
            HR_prom=data.get('HR_promedio')
            inicio=data.get('Inicio')
            spo2_min=data.get('SpO2_min')
            spo2_prom=data.get('SpO2_promedio')
            PR=data.get('pausa_respiratoria')
            self.ui4.lineEdit_HRmax.setText(str(HR_max))
            self.ui4.lineEdit_HRmin.setText(str(HR_min))
            self.ui4.lineEdit_HRprom.setText(str(HR_prom))
            self.ui4.lineEdit_inicio.setText(str(inicio))
            self.ui4.lineEdit_PR.setText(str(PR))
            self.ui4.lineEdit_spo2min.setText(str(spo2_min))
            self.ui4.lineEdit_spo2prom.setText(str(spo2_prom))
        else:
            pass

    def cerrar_apnea(self):
        if self.ventana_apnea is not None:
            self.ventana_apnea.close()
            self.ventana_apnea = None

    #FECHA
    def updateDateTime(self):
        self.fechayhora.setDateTime(QDateTime.currentDateTime())

    #LABELS DESC
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "  Monitor"))

        self.boton_paciente.setText(_translate("MainWindow", "Paciente"))
        self.boton_historial.setText(_translate("MainWindow", "Historial"))

        self.label_doc.setText(_translate("MainWindow", "Dr."))
        self.alarma_torax_2.setText(_translate("MainWindow", "ALARMA Respiración"))
        self.alarma_spo2.setText(_translate("MainWindow", "ALARMA SpO2"))
        self.alarma_fc.setText(_translate("MainWindow", "ALARMA FC"))
        self.label_acc.setText(_translate("MainWindow", "Mov. Tórax"))
        self.label_spo2.setText(_translate("MainWindow", "   SpO2%"))
        self.label_fc.setText(_translate("MainWindow", "PPG"))
        self.label_bpm.setText(_translate("MainWindow", "BPM"))
        self.label_uno_izq.setText(_translate("MainWindow", "Nº APNEAS"))
        self.label_dos_izq.setText(_translate("MainWindow", "Pausa rp. máx"))
        self.label_5_izq.setText(_translate("MainWindow", "Mínimo SpO2"))
        self.label_5_izq_2.setText(_translate("MainWindow", "Mínima FC"))
        self.label_cuatro_izq.setText(_translate("MainWindow", "Máxima FC"))
        self.label_ultimas.setText(_translate("MainWindow", "Últimas   "))
        self.comboBox.setItemText(0, _translate("MainWindow", "     30 min"))
        self.comboBox.setItemText(1, _translate("MainWindow", "     1 hs"))
        self.comboBox.setItemText(2, _translate("MainWindow", "     12 hs"))
        self.comboBox.setItemText(3, _translate("MainWindow", "     24 hs"))
        self.comboBox_resp_conf.setItemText(0, _translate("MainWindow", "  Sensibilidad Media"))
        self.comboBox_resp_conf.setItemText(1, _translate("MainWindow", "  Sensibilidad Baja"))
        self.comboBox_resp_conf.setItemText(2, _translate("MainWindow", "  Sensibilidad Alta"))
        self.label_ID.setText(_translate("MainWindow", "  Paciente: "))
        self.label_nombre.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate("MainWindow", "Configuración de alarmas"))
        self.label_FC_conf.setText(_translate("MainWindow", "FC [lpm] < "))
        self.label_SpO2_conf.setText(_translate("MainWindow", "SpO2 [%] < "))
        self.label_Resp_conf.setText(_translate("MainWindow", "Respiración"))
        self.lineEdit_conf_FC.setText(_translate("MainWindow", "100"))
        self.lineEdit_SpO2_conf.setText(_translate("MainWindow", "80"))
        self.label_pokayoke.setText(_translate("MainWindow", ""))


class Worker(QtCore.QObject):
    data_updated = QtCore.pyqtSignal(list,list)
    data_updated2 = QtCore.pyqtSignal(list,list,int)
    data_updated3 = QtCore.pyqtSignal(int)
    alarm_acc= QtCore.pyqtSignal(bool, str)
    alarm_hr= QtCore.pyqtSignal(bool)
    alarm_spo2=QtCore.pyqtSignal(bool)
    funcion_30_min=QtCore.pyqtSignal()
    stopped = QtCore.pyqtSignal()


    def __init__(self, arduino_port, baud_rate, sample_rate_ppg, sample_rate_acc):
        super(Worker, self).__init__()
        self.arduino_port = arduino_port
        self.baud_rate = baud_rate
        self.sample_rate_ppg = sample_rate_ppg
        self.sample_rate_acc = sample_rate_acc
        self.valSignalP_ARD = []
        self.acc_data=[]
        self.x_array = []
        self.red_data=[]
        self.x2_array=[]
        self.m = 0
        self.m2 = 0
        self.spo2=[]
        self.valid=0
        self.hr_data=[]
        self.t_inicio=0
        self.inicios=[]
        self.label_spo2=97
        self.hr=60
        self.hr_array=[]
        self.flag_acc=False
        self.spo2_acortado=[]
        self.hr_array_acortado=[]
        self.color='None'
        global ID
        self.serialArduinoA = None
        pygame.init()

    def connect_arduino(self):
        self.serialArduinoA = serial.Serial(self.arduino_port,self.baud_rate)
        print("Arduino connected")
        self.get_data()
        #self.save_data()

    def get_data(self):
        global bandera_definir_ID
        while(1):
            if bandera_definir_ID:
                self.funcion_30_min.emit()
                doc1 = db.document('pacientes/'+ID).get()
                data = doc1.to_dict()
                self.n_apneas = data.get('n_apneas')
                bandera_definir_ID=False
            line = self.serialArduinoA.readline().decode('utf-8').strip()
            if line.startswith("Buffer: "):
                data = line[len("Buffer: "):]
                data = data.split(",")
                data_float = [float(valor) for valor in data]
                if data_float[0]==data_float[28]: #chequeo que haya llegado el mensaje completo
                    accelerometer_data=data_float[1:3]
                    ppg_data=data_float[3:28]

                    if (len(self.acc_data)<fs_acc*15):
                        self.acc_data+=accelerometer_data
                        for i in range (0,2):
                            self.x_array.append((self.m/self.sample_rate_acc))
                            self.m+=1
                        self.data_updated.emit(self.x_array, self.acc_data)
                        if self.valid==0:
                            self.spo2_data_valid=[97,97]
                        self.spo2+=self.spo2_data_valid
                        self.data_updated3.emit(self.label_spo2)

                    else:
                        self.acc_data+=accelerometer_data
                        for i in range (0,2):
                            self.x_array.append((self.m/self.sample_rate_acc))
                            self.m+=1
                        #self.data_updated.emit(self.x_array, self.acc_data)

                        if self.valid==0:
                            self.spo2_data_valid=[97,97]

                        self.spo2+=self.spo2_data_valid
                        if (self.m/self.sample_rate_acc)%15==0:
                            self.spo2_acortado.append(self.spo2_data_valid[0])
                            if ID!=None:
                                db.collection('pacientes').document(ID).update({'spO2':self.spo2_acortado})
                            else:
                                pass


                        self.data_updated3.emit(self.label_spo2)


                        self.red_data+=ppg_data
                        for i in range (0,25):
                            self.x2_array.append((self.m2/self.sample_rate_ppg))
                            self.m2+=1
                        #self.data_updated2.emit(self.x2_array, self.red_data, self.hr)
                        self.acc_data_graf=self.acc_data
                        self.red_data_graf=self.red_data
                        self.x_array_graf=self.x_array
                        self.x2_array_graf=self.x2_array
                        self.grafico_thread = threading.Thread(target=self.actualizar_grafico)
                        self.grafico_thread.start()

                        self.flush_buffer_to_file()
                        self.x_array = self.x_array[int(2):]
                        self.acc_data = self.acc_data[int(2):]
                        self.x2_array = self.x2_array[25:]
                        self.red_data = self.red_data[25:]
                        self.spo2=self.spo2[int(2):]

                    if (len(self.red_data) < fs_ppg * 15):
                        self.red_data+=ppg_data
                        for i in range (0,25):
                            self.x2_array.append((self.m2/self.sample_rate_ppg))
                            self.m2+=1
                        self.data_updated2.emit(self.x2_array, self.red_data, self.hr)
                else:
                    self.get_data()

            if line.startswith("SPO2= "):
                spo2_data = line[len("SPO2= "):]
                spo2_data = spo2_data.split(",")
                spo2_data_int=[int(valor) for valor in spo2_data]
                if spo2_data_int[1]==1 and spo2_data_int[0]>60:
                    self.spo2_data_valid=[spo2_data_int[0],spo2_data_int[0]]
                    self.label_spo2=spo2_data_int[0]
                    self.valid=1

    def actualizar_grafico(self):
        self.data_updated.emit(self.x_array_graf[:(len(self.x_array_graf)-2)], self.acc_data_graf[:(len(self.acc_data_graf)-2)])
        self.data_updated2.emit(self.x2_array_graf[:(len(self.x2_array_graf)-21)], self.red_data_graf[:(len(self.red_data_graf)-21)], self.hr)
        time.sleep(0.05)
        self.data_updated.emit(self.x_array_graf[:(len(self.x_array_graf)-2)], self.acc_data_graf[:(len(self.acc_data_graf)-2)])
        self.data_updated2.emit(self.x2_array_graf[:(len(self.x2_array_graf)-16)], self.red_data_graf[:(len(self.red_data_graf)-16)], self.hr)
        time.sleep(0.05) #0.1
        self.data_updated.emit(self.x_array_graf[:(len(self.x_array_graf)-2)], self.acc_data_graf[:(len(self.acc_data_graf)-2)])
        self.data_updated2.emit(self.x2_array_graf[:(len(self.x2_array_graf)-11)], self.red_data_graf[:(len(self.red_data_graf)-11)], self.hr)
        time.sleep(0.05) #0.15
        self.data_updated.emit(self.x_array_graf, self.acc_data_graf)
        self.data_updated2.emit(self.x2_array_graf[:(len(self.x2_array_graf)-6)], self.red_data_graf[:(len(self.red_data_graf)-6)], self.hr)
        time.sleep(0.05) #0.2
        self.data_updated.emit(self.x_array_graf, self.acc_data_graf)
        self.data_updated2.emit(self.x2_array_graf, self.red_data_graf, self.hr)

    def save_data(self):
        global ID
        db.collection('pacientes').document(ID).update({'n_apneas':self.n_apneas})
        doc=db.document('pacientes/'+ID+'/Apneas/Apnea'+str(self.n_apneas))
        document=db.collection('pacientes').document(ID).collection('Apneas').document('Apnea'+str(self.n_apneas)).get()

        if document.exists:
            pass
        else:
            inicio=self.inicios[len(self.inicios)-2]
            # guardar los datos aquí
            hr_apnea = self.hr_array[int((inicio - 15) * 4):int((inicio + self.pausa_respiratoria - 15) * 4)]
            nuevo_data = {
                'pausa_respiratoria': float(self.pausa_respiratoria),
                'HR_max': int(np.max(hr_apnea)),
                'HR_min': int(np.min(hr_apnea)),
                'HR_promedio': int(np.mean(hr_apnea)),
                'Inicio': float(inicio),
                'SpO2_min': int(np.min(self.spo2)),
                'SpO2_promedio': int(np.mean(self.spo2)),
            }
            doc.set(nuevo_data)

        self.funcion_30_min.emit()

    def flush_buffer_to_file(self): #buffer con 15 segundos de señal
        #Todo el procesamiento
        global ALARMA_ACTIVA
        global umbral
        sos=butter(60, 8, btype='lowpass', fs=fs_ppg, analog=False, output='sos')
        self.red_data=sosfiltfilt(sos, self.red_data)
        picos=find_peaks(self.red_data, distance=50)[0]
        cant_picos=len(picos)
        self.hr=int((cant_picos/15)*60)
        if (self.m/self.sample_rate_acc)%15==0:
            self.hr_array_acortado.append(self.hr)
            global ID
            if ID!=None:
                db.collection('pacientes').document(ID).update({'hr': self.hr_array_acortado})
            else:
                pass

        self.hr_array.append(self.hr)

        cadena_con_comas = ', '.join(map(str, self.red_data))
        elementos = cadena_con_comas.split(', ')
        self.red_data = [float(elemento) for elemento in elementos]

        #alarma hr
        global umbral_hr, umbral_spo2, umbral
        if self.hr<umbral_hr or self.hr>180:
            flag_hr=True
            self.alarm_hr.emit(flag_hr)
        else:
            flag_hr=False
            self.alarm_hr.emit(flag_hr)

        #alarma spo2
        if self.spo2[len(self.spo2)-1] < umbral_spo2:
            flag_spo2=True
            self.alarm_spo2.emit(flag_spo2)
        else:
            flag_spo2=False
            self.alarm_spo2.emit(flag_spo2)

        acc_ventana = self.acc_data[len(self.acc_data)-2:]
        for i in range(2):
            if acc_ventana[i]>umbral:
                self.t_inicio=self.x_array[i+len(self.acc_data)-2]
                self.inicios.append(self.t_inicio)
                #global ID
                if ID!=None:
                    if self.flag_acc==True and self.color=='red':
                        self.n_apneas+=1
                        if (len(self.inicios)>=2):
                            self.pausa_respiratoria=self.inicios[len(self.inicios)-1]-self.inicios[len(self.inicios)-2]
                            if self.pausa_respiratoria>20:
                                print("pausa respiratoria:", self.pausa_respiratoria)

                        self.guardado_thread = threading.Thread(target=self.save_data)
                        self.guardado_thread.start()
                else:
                    pass
                self.flag_acc=False
                pygame.mixer.music.stop()
                self.alarm_acc.emit(self.flag_acc,self.color)
            else:
                if len(self.inicios)>0:
                    if (self.x_array[i+len(self.acc_data)-2]-self.inicios[len(self.inicios)-1]>10 and self.x_array[i+len(self.acc_data)-2]-self.inicios[len(self.inicios)-1]<20):
                        self.flag_acc=True
                        self.color='yellow'
                        hilo_alarma = threading.Thread(target=self.reproducir_alarma)
                        hilo_alarma.start()
                        hilo_alarma.join()
                        self.alarm_acc.emit(self.flag_acc,self.color)
                    if (self.x_array[i+len(self.acc_data)-2]-self.inicios[len(self.inicios)-1]>20):
                        self.flag_acc=True
                        self.color='red'
                        self.alarm_acc.emit(self.flag_acc,self.color)

        pass

    def reproducir_alarma(self):
        global ARCHIVO_ALARMA
        pygame.mixer.music.load(ARCHIVO_ALARMA)
        pygame.mixer.music.play(-1)  # -1 significa reproducción en bucle

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.graph_widget = self.ui.graphicsView_acc.getPlotItem()
        self.graph_widget.showGrid(x=True, y=True)
        y_min = 6000
        y_max = 21000
        self.graph_widget.vb.setYRange(y_min, y_max)
        # Oculta las etiquetas del eje Y
        self.graph_widget.getAxis('left').setTicks([[]])

        self.graph_widget2 = self.ui.graphicsView_fc.getPlotItem()
        self.graph_widget2.showGrid(x=True, y=True)
        # Oculta las etiquetas del eje Y
        self.graph_widget2.getAxis('left').setTicks([[]])

        self.worker_thread = None
        #self.get_data_thread = None
        #self.save_data_thread = None
        #self.ui.boton_inicio.clicked.connect(self.start_reading)
        self.start_reading()
        #self.ui.boton_detener.clicked.connect(self.stop_reading)
        self.ui.comboBox.currentIndexChanged.connect(self.ejecutar_funcion)
        self.max_ppg=-10**10
        self.min_ppg=10**10
        self.start_time = time.time()

    def start_reading(self):
        print("hola")
        arduino_port = 'COM3'
        baud_rate = 57600
        sample_rate_ppg = 100
        sample_rate_acc = 8
        #DURACION
        self.timer2 = QtCore.QTimer()
        self.elapsed_time = QtCore.QTime(0, 0)
        self.timer2.timeout.connect(self.update_duracion)
        self.timer2.start(1000)
        #self.detener=False

        self.worker = Worker(arduino_port, baud_rate, sample_rate_ppg,sample_rate_acc)
        self.worker_thread = QtCore.QThread()
        #self.save_data_thread=QtCore.QThread()
        self.worker.data_updated.connect(self.update_plot)
        self.worker.data_updated2.connect(self.update_plot2)
        self.worker.data_updated3.connect(self.update_plot3)
        self.worker.alarm_acc.connect(self.alarm_acc)
        self.worker.alarm_hr.connect(self.alarm_hr)
        self.worker.alarm_spo2.connect(self.alarm_spo2)
        self.worker.funcion_30_min.connect(self.funcion_30_min)
        self.worker.stopped.connect(self.stop_thread)
        self.worker.moveToThread(self.worker_thread)
        global ID
        '''
        if ID!=None:
            self.funcion_30_min()
        else:
            pass
        '''
        self.worker_thread.started.connect(self.worker.connect_arduino)
        self.worker_thread.start()


        #self.get_data_thread = threading.Thread(target=self.get_data)

    def update_duracion(self):
        self.elapsed_time= self.elapsed_time.addSecs(1)
        self.ui.timeEdit_duracion.setTime(self.elapsed_time)

    @QtCore.pyqtSlot(list,list)
    def update_plot(self, x_array, acc_data):
        self.graph_widget.clear()
        self.graph_widget.plot(x_array, acc_data, pen = pg.mkPen(color = 'pink', width = 3))
        # Crear un objeto QPen con color rojo y ancho 3
        estilo_linea = pg.mkPen(color='red', width=2)

        # Establecer el estilo de la línea como punteada
        estilo_linea.setStyle(QtCore.Qt.DashLine)

        # Agregar la línea al gráfico con el estilo personalizado
        linea_umbral = self.graph_widget.addLine(y=umbral, pen=estilo_linea)

    @QtCore.pyqtSlot(list,list,int)
    def update_plot2(self, x2_array, red_data, hr):
        elapsed_time = time.time() - self.start_time
        self.graph_widget2.clear()
        maximo=np.max(red_data)
        if maximo>self.max_ppg:
            self.max_ppg=maximo
        minimo=np.min(red_data)
        if minimo<self.min_ppg:
            self.min_ppg=minimo
        self.graph_widget2.vb.setYRange(self.min_ppg-10, self.max_ppg+10)
        if elapsed_time >= 5:
            # Actualizar el rango de los ejes cada 5 segundos
            self.max_ppg = -10**10
            self.min_ppg = 10**10
            self.start_time = time.time()
        self.graph_widget2.plot(x2_array, red_data, pen = pg.mkPen(color = 'green', width = 3))
        self.ui.lcdNumber_FC.display(hr)

    @QtCore.pyqtSlot(int)
    def update_plot3(self,label_spo2):
        self.ui.lcdNumber_spo2.display(label_spo2)

    def alarm_acc(self,flag,color):
        if flag:
            if color=='red':
                self.ui.alarma_torax_2.setStyleSheet("background-color: red;")
                font = QtGui.QFont()
                font.setFamily("MS Shell Dlg 2")
                font.setPointSize(10)
                font.setBold(True)
                font.setItalic(False)
                #font.setWeight(75)
                self.ui.alarma_torax_2.setFont(font)
                self.ui.alarma_torax_2.setWordWrap(True)
            if color=='yellow':
                self.ui.alarma_torax_2.setStyleSheet("background-color: yellow;")
                font = QtGui.QFont()
                font.setFamily("MS Shell Dlg 2")
                font.setPointSize(10)
                font.setBold(True)
                font.setItalic(False)
                #font.setWeight(75)
                self.ui.alarma_torax_2.setFont(font)
                self.ui.alarma_torax_2.setWordWrap(True)
        else:
            font = QtGui.QFont()
            font.setFamily("MS Shell Dlg 2")
            font.setPointSize(10)
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(75)
            self.ui.alarma_torax_2.setFont(font)
            self.ui.alarma_torax_2.setWordWrap(True)
            self.ui.alarma_torax_2.setStyleSheet("background-color: rgb(237, 218, 233);")

    def alarm_hr(self,flag):
        if flag:
            self.ui.alarma_fc.setStyleSheet("background-color: red;")
            font = QtGui.QFont()
            font.setFamily("MS Shell Dlg 2")
            font.setPointSize(10)
            font.setBold(True)
            font.setItalic(False)
            #font.setWeight(75)
            self.ui.alarma_fc.setFont(font)
            self.ui.alarma_fc.setWordWrap(True)
        else:
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.ui.alarma_fc.setFont(font)
            self.ui.alarma_fc.setWordWrap(True)
            self.ui.alarma_fc.setStyleSheet("background-color: rgb(223, 249, 211);")

    def alarm_spo2(self,flag):
        if flag:
            self.ui.alarma_spo2.setStyleSheet("background-color: red;")
            font = QtGui.QFont()
            font.setFamily("MS Shell Dlg 2")
            font.setPointSize(10)
            font.setBold(True)
            font.setItalic(False)
            #font.setWeight(75)
            self.ui.alarma_spo2.setFont(font)
            self.ui.alarma_spo2.setWordWrap(True)
        else:
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.ui.alarma_spo2.setFont(font)
            self.ui.alarma_spo2.setWordWrap(True)
            self.ui.alarma_spo2.setStyleSheet("background-color: rgb(217, 244, 250);")

    def ejecutar_funcion(self, index):
        # Define tus funciones aquí
        funciones = [self.funcion_30_min, self.funcion_1_hs, self.funcion_12_hs, self.funcion_24_hs]
        # Ejecuta la función correspondiente según la selección
        funciones[index]()

    def funcion_30_min(self):
        #global ID
        # Realiza la consulta para contar documentos que cumplan con la condición
        midnight =QtCore.QTime(0, 0)
        segundos=midnight.secsTo(self.elapsed_time)
        doc1 = db.document('pacientes/'+ID).get()
        data = doc1.to_dict()
        n_apneas=data.get('n_apneas')
        if n_apneas>0:
            valor_de_filtrado=segundos-30*60
            query = db.collection('pacientes').document(ID).collection('Apneas').where('Inicio', ">=", valor_de_filtrado)
            documentos_filtrados = query.stream()
            cantidad_apneas=0
            pausa_respiratorias=[]
            for documento in documentos_filtrados:
                cantidad_apneas+=1
                pausa_respiratorias.append(documento.get('pausa_respiratoria'))

            # Cuenta la cantidad de documentos que cumplan con la condición
            #cantidad_apneas = len(list(documentos_filtrados))
            self.ui.lcdNumber_NApneas.display(cantidad_apneas)
            hr = data.get('hr')
            heart_rate=hr[len(hr)-120:]
            heart_rate_min=np.min(heart_rate)
            self.ui.lcdNumber_minFC.display(heart_rate_min)
            heart_rate_max=np.max(heart_rate)
            self.ui.lcdNumber_maxFC.display(heart_rate_max)
            spo2=data.get('spO2')
            SPO2=spo2[len(spo2)-120:]
            spo2_min=np.min(SPO2)
            self.ui.lcdNumber_MinSpo2.display(spo2_min)
            pausa_respiratorias=sorted(pausa_respiratorias, reverse=True)
            self.ui.lcdNumber_maxPR.display(pausa_respiratorias[0])
        else:
            pass

    def funcion_1_hs(self):
        print("Función para 1 hora")

    def funcion_12_hs(self):
        print("Función para 12 horas")

    def funcion_24_hs(self):
        print("Función para 24 horas")

    def stop_reading(self):
        self.worker.stop_reading()

    def stop_thread(self):
        print("End")

        self.worker_thread.quit()
        self.worker_thread.wait()
        #self.detener=True

        #MainWindow.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()