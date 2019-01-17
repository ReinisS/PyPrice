# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from PyPriceSpider.spiders.amazon import AmazonSpider
import json
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import random

uiFile = os.path.join(os.getcwd(), 'UI', 'PyPrice.ui') 
form, base = uic.loadUiType(uiFile)

class MainWindow(base, form):
    def __init__(self):
        super().__init__()

        self.getUrlList()

        self.setupUi(self)
        #self.resize(1000, 500) # initial size
        self.move(50, 50)
        self.loadLinkList()
        self.loadCurrentData()
        self.updateMode()
        #self.loadGraph()
        self.startSpiderButton.clicked.connect(self.startSpider)
        self.addLinkButton.clicked.connect(self.addLink)
        self.exitButton.clicked.connect(self.exitFunction)
        self.graphRadio1.toggled.connect(self.updateMode)
        self.graphRadio2.toggled.connect(self.updateMode)

    def updateMode(self):
        if self.graphRadio1.isChecked():
            self.relativeMode = True
            self.absoluteMode = False
        else:
            self.relativeMode = False
            self.absoluteMode = True
        self.loadGraph()

    def getUrlList(self):
        try:
            with open('item_links.json', 'r') as file:
                self.urlList = json.load(file)
        except:
            self.urlList = []
    
    def addLink(self):
        try:
            url = self.addLinkBox.toPlainText()
            self.urlList.append(url)
            
            with open('item_links.json', 'w') as file:
                json.dump(
                    self.urlList,
                    file,
                    sort_keys = True,
                    indent = 4,
                    ensure_ascii = False
                )
            
            self.addLinkBox.clear()
            self.loadLinkList()
        except:
            pass
        
    def loadLinkList(self):
        self.linkListWidget.clear()
        self.linkListWidget.addItems(self.urlList)
    
    def loadCurrentData(self):
        try:
            with open('data.json', 'r') as file:
                self.CurrentData = json.load(file)
        except:
            self.CurrentData = []

    def loadGraph(self):
        self.loadCurrentData()
        try:
            self.MplWidget.canvas.axes.clear()
            maxCount = 0

            for item in self.CurrentData:
                name = item['Name']
                shortName = name[:20] + '...'
                priceCount = len(item['Prices'])

                if priceCount > maxCount:
                    maxCount = priceCount

                x = range(1, priceCount + 1)

                if self.relativeMode:
                    y = [float(i) / float(item['Prices'][0]) * 100 for i in item['Prices']]
                else:
                    y = [float(i) for i in item['Prices']]
                self.MplWidget.canvas.axes.plot(x, y, label=shortName, marker='o')

            if self.relativeMode:
                self.MplWidget.canvas.axes.set_title('Relative price (1st price = 100%)')
                self.MplWidget.canvas.axes.set_ylabel("Price, %")
            else:
                self.MplWidget.canvas.axes.set_title('Absolute price')
                self.MplWidget.canvas.axes.set_ylabel("Price, $")

            self.MplWidget.canvas.axes.set_xticks(range(1, maxCount + 1, 1))
            self.MplWidget.canvas.axes.legend(prop={'size': 5})

            self.MplWidget.canvas.draw()
        except:
            pass

    def startSpider(self):
        if len(self.urlList) > 0:
            self.startSpiderButton.setEnabled(False)
            process = CrawlerProcess(get_project_settings())
            self.statusLabel.setText("Getting data from the Web...")
            self.progressBar.setValue(10)
            process.crawl(AmazonSpider, start_urls=self.urlList)
            process.start()
            self.progressBar.setValue(90)
            self.statusLabel.setText("Updating current data...")
            self.loadGraph()
            self.progressBar.setValue(100)
            self.statusLabel.setText("Done!")
        else:
            self.statusLabel.setText("No items provided!")

    def exitFunction(self):
        print('Stopping application')
        sys.exit(app.exec_())

if __name__ == '__main__':
    print('Starting application')
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())