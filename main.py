import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            [description[0] for description in cur.description])
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j == 2:
                    val = cur.execute(f"""SELECT * FROM degreesOfRoasting
WHERE id = (
SELECT degreeOfRoasting FROM coffee
WHERE id = {elem[0]})""").fetchall()[0][1]
                elif j == 3:
                    val = cur.execute(f"""SELECT * FROM types
WHERE id = (
SELECT type FROM coffee
WHERE id = {elem[0]})""").fetchall()[0][1]
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def item_changed(self, item):
        pass

    def save_results(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
