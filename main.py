#!/usr/bin/python

import sys, os
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import parameters, ecu

class Main_widget(gui.QMainWindow):
    def __init__(self, parent = None):
        super(Main_widget, self).__init__(parent)
        print "Scanning ECUs..."
        self.ecu_scan = ecu.Ecu_scanner()
        self.ecu_scan.scan()
        print "Done"
        self.initUI()
        
    def initUI(self):
        self.scrollview = gui.QScrollArea()
        self.scrollview.setWidgetResizable(False)
        self.setCentralWidget(self.scrollview)
        
        self.treedock_params = gui.QDockWidget(self)
        self.treeview_params = gui.QTreeWidget(self.treedock_params)
        self.treedock_params.setWidget(self.treeview_params)
        self.treeview_params.doubleClicked.connect(self.changeScreen)
        
        self.treedock_ecu = gui.QDockWidget(self)
        self.treeview_ecu = gui.QTreeWidget(self.treedock_ecu)
        self.treedock_ecu.setWidget(self.treeview_ecu)
        self.treeview_ecu.doubleClicked.connect(self.changeECU)
        
        i = 0
        for ecu in self.ecu_scan.ecus:
            item = gui.QTreeWidgetItem(self.treeview_ecu, [ecu.name])
            item.setData(0, core.Qt.UserRole, str(i))
            i += 1
        
        self.addDockWidget(core.Qt.LeftDockWidgetArea, self.treedock_ecu)
        self.addDockWidget(core.Qt.LeftDockWidgetArea, self.treedock_params)
        
        menu = self.menuBar()
        diagmenu = menu.addMenu("Diagnostic")
        dtcaction = diagmenu.addAction("Lire DTC")
        dtcaction.triggered.connect(self.readDTC)
        
        
    def readDTC(self):
        print "DTC"
        
    def changeScreen(self, index):
        item = self.treeview_params.model().itemData(index)
        screen = unicode(item[0].toPyObject().toUtf8(), encoding="UTF-8")
        self.paramview.init(screen)
    
    def changeECU(self, index):
        item = self.treeview_params.model().itemData(index)
        ecu_from_index = item[core.Qt.UserRole].toInt()
        
        if ecu_from_index[1] == False:
            print "Changement ECU impossible"
            return

        self.treeview_params.clear()
            
        ecu = self.ecu_scan.ecus[ecu_from_index[0]]
        ecu_file = "ecus/" + ecu.href
        self.paramview = parameters.Param_widget(self.scrollview, ecu_file)
        self.scrollview.setWidget(self.paramview)
        
        screens = self.paramview.categories.keys()
        for screen in screens:
            item = gui.QTreeWidgetItem(self.treeview_params, [screen])
            for param in self.paramview.categories[screen]:
                param_item = gui.QTreeWidgetItem(item, [param])
                param_item.setData(0, core.Qt.UserRole, param)
        
if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    w = Main_widget()
    w.show()
    app.exec_()
