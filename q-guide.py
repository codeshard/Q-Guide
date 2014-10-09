# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Q-Guide - Another frontend to ETECSA Sqlite DB
#   Copyright 2014 Ozkar L. Garcell <ozkar.garcell@gmail.com>

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sip

sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui, QtSql

from connect import QDatabase, QModel
import qguide_rc

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class QGuide(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QGuide, self).__init__(parent)

        self.connection = QDatabase()

        if not self.connection.check_opened_db():
            QtGui.QMessageBox.critical(self,
                                       'Error', 'Base de Datos no encontrada')

        self.resize(340, 450)

        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred,
            QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(340, 450))
        self.setMaximumSize(QtCore.QSize(340, 450))

        self.centralwidget = QtGui.QWidget(self)

        self.create_input_form()

        self.create_table()

        self.fix_layouts()

        self.verticalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.setCentralWidget(self.centralwidget)

        self.create_statusbar()

        self.createActions()

        self.createTrayIcon()

        self.trayIcon.show()
        self.trayIcon.setIcon(QtGui.QIcon(':/images/q-guide.png'))

        self.setWindowIcon(QtGui.QIcon(':/images/q-guide.png'))

    def create_input_form(self):
        self.numberLabel = QtGui.QLabel(self.centralwidget)
        self.numberLabel.setText(_translate(None, "Número:", None))
        self.spacerItem = QtGui.QSpacerItem(
            40,
            20,
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
        self.numberLine = QtGui.QLineEdit(self.centralwidget)
        self.numberLine.setMinimumSize(QtCore.QSize(250, 0))

        self.nameLabel = QtGui.QLabel(self.centralwidget)
        self.nameLabel.setText(_translate(None, "Nombre:", None))
        self.spacerItem1 = QtGui.QSpacerItem(
            40,
            20,
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
        self.nameLine = QtGui.QLineEdit(self.centralwidget)
        self.nameLine.setMinimumSize(QtCore.QSize(250, 0))

        self.addressLabel = QtGui.QLabel(self.centralwidget)
        self.addressLabel.setText(_translate(None, "Dirección':", None))
        self.spacerItem2 = QtGui.QSpacerItem(
            40,
            20,
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
        self.addressLine = QtGui.QLineEdit(self.centralwidget)
        self.addressLine.setMinimumSize(QtCore.QSize(250, 0))

        self.pushButtonFix = QtGui.QPushButton(self.centralwidget)
        self.pushButtonFix.setText(_translate(None, "Fijo", None))
        self.pushButtonMovil = QtGui.QPushButton(self.centralwidget)
        self.pushButtonMovil.setText(_translate(None, "Movil", None))

        self.pushButtonMovil.clicked.connect(self.search_movil)
        self.pushButtonFix.clicked.connect(self.search_fix)

    def create_table(self):
        self.tableWidget = QtGui.QTableView(self.centralwidget)

        self.tableWidget.setItemDelegate(
            QtSql.QSqlRelationalDelegate(self.tableWidget))
        self.tableWidget.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.model = QModel(self)
        self.tableWidget.setModel(self.model)

    def fix_layouts(self):
        self.numberHorizontalLayout = QtGui.QHBoxLayout()
        self.numberHorizontalLayout.addWidget(self.numberLabel)
        self.numberHorizontalLayout.addItem(self.spacerItem)
        self.numberHorizontalLayout.addWidget(self.numberLine)

        self.nameHorizontalLayout = QtGui.QHBoxLayout()
        self.nameHorizontalLayout.addWidget(self.nameLabel)
        self.nameHorizontalLayout.addItem(self.spacerItem1)
        self.nameHorizontalLayout.addWidget(self.nameLine)

        self.addressHorizontalLayout = QtGui.QHBoxLayout()
        self.addressHorizontalLayout.addWidget(self.addressLabel)
        self.addressHorizontalLayout.addItem(self.spacerItem2)
        self.addressHorizontalLayout.addWidget(self.addressLine)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.addLayout(self.numberHorizontalLayout)
        self.verticalLayout.addLayout(self.nameHorizontalLayout)
        self.verticalLayout.addLayout(self.addressHorizontalLayout)

        self.buttonsHorizontalLayout = QtGui.QHBoxLayout()
        self.buttonsHorizontalLayout.addWidget(self.pushButtonFix)
        self.buttonsHorizontalLayout.addWidget(self.pushButtonMovil)

        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.addLayout(self.buttonsHorizontalLayout)

    def create_statusbar(self):
        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def createActions(self):
        self.minimizeAction = QtGui.QAction(QtGui.QIcon(':/images/minimize.png'),
                "Mi&nimizar",
                self,
                triggered=self.hide)

        self.restoreAction = QtGui.QAction(QtGui.QIcon(':/images/restore.png'),
                "&Restaurar",
                self,
                triggered=self.showNormal)

        self.aboutAction = QtGui.QAction(QtGui.QIcon(':/images/about.png'),
                "&Acerca de",
                self,
                triggered=self.about)

        self.quitAction = QtGui.QAction(QtGui.QIcon(':/images/quit.png'),
                "&Cerrar",
                self,
                triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
         self.trayIconMenu = QtGui.QMenu(self)
         self.trayIconMenu.addAction(self.minimizeAction)
         self.trayIconMenu.addAction(self.restoreAction)
         self.trayIconMenu.addAction(self.aboutAction)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)

         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setContextMenu(self.trayIconMenu)

    def search_movil(self):
        nmbr = self.numberLine.text()
        nam = self.nameLine.text()
        addr = self.addressLine.text()
        if nmbr == "" and nam == "" and addr == "":
            QtGui.QMessageBox.critical(
                self,
                'Error',
                'No se pueden realizar consultas sobre campos vacios')
        else:
            query = ("SELECT number, name, address FROM 'main'.'movil' WHERE number LIKE '%{nmbr}%' AND name LIKE '%{nam}%' AND address LIKE '%{addr}%';").format(nmbr=nmbr, nam=nam, addr=addr)
            model_query = self.model.setQuery(query)
            print model_query
            self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Nombre")
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Numero")
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Direccion")

    def search_fix(self):
        nmbr = self.numberLine.text()
        nam = self.nameLine.text()
        addr = self.addressLine.text()
        if nmbr == "" and nam == "" and addr == "":
            QtGui.QMessageBox.critical(
                self,
                'Error',
                'No se pueden realizar consultas sobre campos vacios')
        else:
            query = ("SELECT number, name, address FROM 'main'.'fix' WHERE number LIKE '%{nmbr}%' AND name LIKE '%{nam}%' AND address LIKE '%{addr}%';").format(nmbr=nmbr, nam=nam, addr=addr)
            self.model.setQuery(query)
            self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Nombre")
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Numero")
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Direccion")

    def about(self):
        QtGui.QMessageBox.about(
                self,
                'Q-Guide',
                '<p>Q-Guide es un front-end para la base de datos de ETECSA</p>'
                '<p>Copyright &copy; 2014 <a href=mailto:"ozkar.garcell@gmail.com">Ozkar L. Garcell</a></p>')


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)
    qguide = QGuide()
    qguide.show()
    sys.exit(app.exec_())
