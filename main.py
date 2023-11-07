import h5py
from pyqtgraph import PlotWidget, mkPen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout

from nplogic import generating_random_data, resizing_2d_array_randomly, refilling_2d_array_randomly


# class for customizing table model
class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        print(self._data)

    def data(self, index, role):
        # the values in numpy.ndarray are stored in a special format (np.int8, np.int16, etc.)
        # so it need to be converted to a string representation to display it correct
        if role == Qt.DisplayRole:
            value = self._data[index.row(), index.column()]
            return str(value)

        # values alignment in the cell
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter + Qt.AlignRight

        # filling the cells of the first column with color depending on the value
        elif role == Qt.BackgroundRole and index.column() == 0:
            value = self._data[index.row(), index.column()]
            if value < 0:
                return QtGui.QColor('red')
            elif value > 0:
                return QtGui.QColor('green')


    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]


# class for customizing a dependency graph
class PlotGraph(PlotWidget):
    def __init__(self):
        super(PlotGraph, self).__init__()
        self.setTitle('Зависимость второго выбранного столбца от первого')
        self.setLabel('bottom', 'Значения из первого выбранного столбца')
        self.setLabel('left', 'Значения из второго выбранного столбца')
        self.setBackground('w')


# class for customizing main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Test app for NIPI')

        # setting up table view
        self.table = QtWidgets.QTableView()
        # setting Resize Mode to Stretch to exclude empty spaces around table view
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # generating random 2d array at the start of the application
        self.data = generating_random_data()

        # setting up 2d array to the model and setting up this model to table view
        self.model = TableModel(self.data)
        self.table.setModel(self.model)

        # setting up graph
        self.plot_graph = PlotGraph()
        # customizing a pen for graph
        self.pen = mkPen(width=2, color='b')
        # setting up the plot for graph
        self.plot_graph.plot(self.data[:, 0], self.data[:, 1], pen=self.pen)

        # setting up button for loading array from file
        load_array_button = QPushButton('Load array')
        load_array_button.clicked.connect(self.loading_array_from_file)
        load_array_button.setGeometry(20, 20, 50, 20)

        # setting up button for saving array to file
        save_array_button = QPushButton('Save array')
        save_array_button.clicked.connect(self.saving_array_to_file)
        save_array_button.setGeometry(20, 50, 50, 20)

        # setting up button for resizing array
        resize_array_button = QPushButton('Resize array')
        resize_array_button.clicked.connect(self.resizing_array)
        resize_array_button.setGeometry(20, 80, 50, 20)

        # setting up button for refilling array
        refill_array_button = QPushButton('Refill array')
        refill_array_button.clicked.connect(self.refilling_array)
        refill_array_button.setGeometry(20, 80, 50, 20)

        # setting up layout for buttons
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(load_array_button)
        layout_buttons.addWidget(save_array_button)
        layout_buttons.addWidget(resize_array_button)
        layout_buttons.addWidget(refill_array_button)

        # setting up the main window layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.table)
        layout_main.addWidget(self.plot_graph)
        layout_main.addLayout(layout_buttons)

        # setting up spacing for content and window borders
        layout_main.setContentsMargins(5, 5, 5, 5)
        layout_main.setSpacing(5)

        # setting up the main widget to display in the app window
        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)


    # updating instances after changed 2d array
    def updating_instance(self):
        self.model._data = self.data
        self.model.layoutChanged.emit()
        self.plot_graph.clear()
        self.plot_graph.plot(self.data[:, 0], self.data[:, 1], pen=self.pen)


    # loading 2d array from h5py dataset stored in the file
    def loading_array_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load from file')
        if file_path:
            with h5py.File(file_path, mode='r') as file:
                self.data = file['default'][:]
                self.updating_instance()


    # saving 2d array to h5py dataset in the file
    def saving_array_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save to file')
        if file_path:
            with h5py.File(file_path, mode='w') as file:
                file.create_dataset(name='default', data=self.data)


    def resizing_array(self):
        self.data = resizing_2d_array_randomly(self.data)
        self.updating_instance()


    def refilling_array(self):
        self.data = refilling_2d_array_randomly(self.data)
        self.updating_instance()


# this app doesn't accept command line arguments
app = QApplication([])
# setting up window
window = MainWindow()
# making window visible
window.show()
app.exec()
