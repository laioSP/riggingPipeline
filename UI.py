from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QSizePolicy, QWidget, QGridLayout, QPushButton,QCheckBox, QSpinBox, QComboBox, QDoubleSpinBox
from PySide2.QtGui import QPainter, QPainterPath, QColor, QPen
import sys
import os
import pymel.core as pm
import folderManager

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.builtLayouts = {}
        self.loadedSelection = []

        self.project = folderManager.projectManager()

        self.setWindowTitle("asset manager")

        mainLayout = QGridLayout()
        layoutInputs = {'switchStatusLayout' : {}, 'statusLayout' : {}} 

        self.chainLayout(layoutInputs, mainLayout)

        self.position = self.button("position state")
        self.build = self.button("build state")
        self.publish = self.button("publish")
        self.publish.clicked.connect(lambda : cube())       

        self.assetList = QComboBox()
        self.assetList.currentIndexChanged.connect(lambda : self.selectedAsset())

        self.showList = QComboBox()
        self.showList.addItems(self.project.getShowList())
        self.showList.currentIndexChanged.connect(lambda : self.selectedShow())

        self.version =  QLabel()
        self.logo = QPainter()

        self.selectedShow()
        self.selectedAsset()

        self.save = self.button("save")
        self.save.clicked.connect(lambda : self.project.save())

        self.asset = self.button("load asset")
        self.asset.clicked.connect(lambda : self.project.setProject())   

        self.builtLayouts['switchStatusLayout'].addWidget(self.position,0,0)
        self.builtLayouts['switchStatusLayout'].addWidget(self.build,1,0)
        self.builtLayouts['switchStatusLayout'].addWidget(self.publish,2,0)

        self.builtLayouts['statusLayout'].addWidget(self.showList,0,0)
        self.builtLayouts['statusLayout'].addWidget(self.assetList,1,0)
        self.builtLayouts['statusLayout'].addWidget(self.version,2,0)
        self.builtLayouts['statusLayout'].addWidget(self.save,3,0)
        self.builtLayouts['statusLayout'].addWidget(self.asset,4,0)

        widget = QWidget()
        widget.setLayout( mainLayout )
        self.setCentralWidget(widget)

    @staticmethod
    def button(name):
        pushButton=QPushButton(name)
        pushButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
  
        return pushButton
    
    @staticmethod
    def checkBox(name, checked = True):
        check = QCheckBox(name)
        check.setChecked(checked)
        check.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return check
    
    @staticmethod
    def numberBox(defaultValue, max='noLimit', min = -100000000):
        box = QDoubleSpinBox()
        box.setDecimals(2)
        if max == 'noLimit':
            box.setMaximum(100000000)  
        else:
            box.setMaximum(max)  

        box.setMinimum(min)
        box.setValue(defaultValue)

        return box
      
    def chainLayout(self, layoutDictionary, parent):
        counter=0

        for layoutName in layoutDictionary:
            grid = QGridLayout()
            self.builtLayouts[layoutName] = grid
            parent.addLayout(grid, 0, counter)
            counter+=1    
            
            if layoutDictionary[layoutName]:

                for child in layoutDictionary[layoutName]:   
                    childLayout = self.chainLayout(layoutDictionary[layoutName], grid)
                    self.builtLayouts[child] = childLayout
        
        return grid

    def selectedShow(self):
        self.assetList.clear()
        self.assetList.addItems(self.project.getAssetList(self.showList.currentText()))

    def selectedAsset(self):
        self.project.getVersionList(self.assetList.currentText())
        self.version.setText(self.project.version)
        return self.project.version
    
def cube():
    pm.polyCube()

window = MainWindow()
window.show()







