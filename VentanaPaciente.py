from PyQt5 import QtCore, QtGui, QtWidgets

class AbrirVentanaPaciente(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 1000)
        MainWindow.setMinimumSize(QtCore.QSize(800, 1000))
        MainWindow.setMaximumSize(QtCore.QSize(800, 1000))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 1000))
        self.centralwidget.setMaximumSize(QtCore.QSize(800, 1000))
        self.centralwidget.setObjectName("centralwidget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.marco = QtWidgets.QFrame(self.centralwidget)
        self.marco.setMinimumSize(QtCore.QSize(800, 1000))
        self.marco.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.marco.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.marco.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.marco.setFrameShadow(QtWidgets.QFrame.Raised)
        self.marco.setObjectName("marco")
        
        self.gridLayout_3 = QtWidgets.QGridLayout(self.marco)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.frame_botones = QtWidgets.QFrame(self.marco)
        self.frame_botones.setMinimumSize(QtCore.QSize(350, 70))
        self.frame_botones.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_botones.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_botones.setObjectName("frame_botones")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_botones)
        self.horizontalLayout.setContentsMargins(0, 3, 0, 0)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.boton_guardar = QtWidgets.QPushButton(self.frame_botones)
        self.boton_guardar.setMinimumSize(QtCore.QSize(150, 60))
        self.boton_guardar.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.boton_guardar.setObjectName("boton_guardar")
        self.horizontalLayout.addWidget(self.boton_guardar)
        
        self.boton_atras = QtWidgets.QPushButton(self.frame_botones)
        self.boton_atras.setMinimumSize(QtCore.QSize(150, 60))
        self.boton_atras.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.boton_atras.setObjectName("boton_atras")
        
        self.horizontalLayout.addWidget(self.boton_atras)
        self.gridLayout_3.addWidget(self.frame_botones, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 645, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 1, 1, 1)
        
        self.cuadro = QtWidgets.QFrame(self.marco)
        self.cuadro.setMinimumSize(QtCore.QSize(600, 250))
        self.cuadro.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.cuadro.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cuadro.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cuadro.setObjectName("cuadro")
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.cuadro)
        self.verticalLayout_3.setContentsMargins(9, 15, -1, 15)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        self.frame_texto = QtWidgets.QFrame(self.cuadro)
        self.frame_texto.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_texto.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_texto.setObjectName("frame_texto")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_texto)
        
        self.gridLayout.setObjectName("gridLayout")
        self.label_Ingrese = QtWidgets.QLabel(self.frame_texto)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_Ingrese.setFont(font)
        self.label_Ingrese.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Ingrese.setObjectName("label_Ingrese")
        self.gridLayout.addWidget(self.label_Ingrese, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_texto)
        self.frame_4 = QtWidgets.QFrame(self.cuadro)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.lineEdit_ID = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_ID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_ID.setMinimumSize(QtCore.QSize(0, 100))
        self.lineEdit_ID.setObjectName("lineEdit_ID")
        self.gridLayout_2.addWidget(self.lineEdit_ID, 0, 0, 1, 1)
        
        self.verticalLayout_3.addWidget(self.frame_4)
        self.gridLayout_3.addWidget(self.cuadro, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 1, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 2, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 2, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.marco)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "  ID del paciente"))
        self.boton_guardar.setText(_translate("MainWindow", "Guardar"))
        self.boton_atras.setText(_translate("MainWindow", "Atrás"))
        self.label_Ingrese.setText(_translate("MainWindow", "Ingrese ID del paciente:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AbrirVentanaPaciente()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
