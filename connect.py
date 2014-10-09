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


from PyQt4 import QtSql


class QDatabase(object):
    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("database/etecsa.db")

    def check_opened_db(self):
        return self.db.open()

    def execute_query(self, params):
        query = QtSql.QSqlQuery(self.db)
        query.exec_(params)
        return query


class QModel(QtSql.QSqlQueryModel):
    def __init__(self, parent=None):
        super(QModel, self).__init__(parent)
