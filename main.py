import sys
import random
import PySide6.QtCore as core
import PySide6.QtWidgets as widgets
import PySide6.QtGui as gui
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import requests
import re


class App(widgets.QWidget):
    def __init__(self):
        super().__init__()
        self.button = widgets.QPushButton('Request from webservice')
        self.text = widgets.QLabel('aiplayground', alignment=core.Qt.AlignCenter)
        self.layout = widgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)
        self.api_url = 'http://www.lennartberning.de/api/moods?'

    def createTable(self, data):
        #Not proud about the following, but it serves the purpose...
        data = data.strip('][').split(',')
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(data)/3)
        self.tableWidget.setHorizontalHeaderLabels(['Mood', 'Is-Positive', 'Timestamp'])
        p = 0
        for r, list in enumerate(data):
            for i in range(3):
                if p < len(data):
                    self.tableWidget.setItem(r, i, QTableWidgetItem(re.sub('[""]', '', data[p]).replace('[','').replace(']','')))
                p = p + 1
        self.tableWidget.show()

    @core.Slot()
    def magic(self):
        response = self.call_webservice(self.api_url, 'sentiment', 0)
        self.text.setText(str(response.status_code))
        self.createTable(response.text)

    @staticmethod
    def call_webservice(api_url, key, direction):
        url = '{0}{1}={2}'.format(api_url, key, direction)
        r = requests.get(url)
        if r.status_code == 200:
            return r
        else:
            return 'Error contacting webservice. Please check connectivity!'


if __name__ == '__main__':
    app = widgets.QApplication([])
    widget = App()
    widget.resize(300, 300)
    widget.show()
    sys.exit(app.exec_())