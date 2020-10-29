import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
import Ping


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

TIMER_TIMEOUT = 5000

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(100, 600)

        self.table = QtWidgets.QTableView()

        self.data = [[]]
        # self.data = [['192.168.178.1', 0], ['192.168.178.24', 71]]

        self.model = TableModel(self.data)

        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.main)
        self.timer.start(TIMER_TIMEOUT)


    def main(self):
        IPs = Ping.get_IPs()
        results = Ping.loop(IPs)
        self.data = [result.result() for result in results]
        print(self.data)


        newTable = TableModel(self.data)
        self.table.setModel(newTable)


        self.timer.start(TIMER_TIMEOUT)


app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()

