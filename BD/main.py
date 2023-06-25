import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QCalendarWidget
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5 import QtCore
import sys
import csv

# функция для подключения к PostgreSQL
def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="1234"
        )
    except psycopg2.DatabaseError as e:
        print(f"Error while connecting to PostgreSQL: {e}")
    return conn

def write_csv_file(file_path, rows):
    with open(r'/BD/diagnosis.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)


def read_csv_file(file_path):
    rows = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            rows.append(row)
    return rows


def select_from_csv_file(file_path, select_columns=None, where_column=None, where_value=None):
    rows = read_csv_file(file_path)
    headers = rows[0]
    if not select_columns:
        select_columns = headers
    if where_column and where_value:
        where_index = headers.index(where_column)
        rows = [row for row in rows if row[where_index] == where_value]
    select_indexes = [headers.index(col) for col in select_columns]
    result = []
    for row in rows:
        result.append([row[i] for i in select_indexes])
    message_box = QMessageBox()
    message_box.setText(str(result))
    message_box.exec_()

def show_message_box(data):
    message_box = QMessageBox()
    message_box.setText(str(data))
    message_box.exec_()

def select_rows_with_date_and_columns(file_path, select_columns, date):
    rows = read_csv_file(file_path)
    headers = rows[0]
    date_index = headers.index('articles.publicationDate')
    where_column = 'articles.publicationDate'
    where_value = date
    select_indexes = [headers.index(col) for col in select_columns]
    result = []
    for row in rows[1:]:
        if row[date_index] > date:
            result.append([row[i] for i in select_indexes])
    return result

def insert_into_csv_file(file_path, values):
    rows = read_csv_file(r'/BD/diagnosis.csv')
    headers = rows[0]
    values.insert(0, str(len(rows)))
    rows.append(values)
    write_csv_file(file_path, rows)


def update_csv_file(file_path, set_column, set_value, where_column, where_value):
    rows = read_csv_file(r'/BD/diagnosis.csv')
    headers = rows[0]
    set_index = headers.index(set_column)
    where_index = headers.index(where_column)
    for i, row in enumerate(rows):
        if row[where_index] == where_value:
            rows[i][set_index] = set_value
    write_csv_file(file_path, rows)


def delete_from_csv_file(file_path, where_column, where_value):
    rows = read_csv_file(r'/BD/diagnosis.csv')
    headers = rows[0]
    where_index = headers.index(where_column)
    rows = [row for row in rows if row[where_index] != where_value]
    write_csv_file(file_path, rows)

def select_date_above(date):
    rows = read_csv_file('diagnosis.csv')
    headers = rows[0]
    date_index = headers.index('articles.publicationDate')
    result = []
    for row in rows[1:]:
        if row[date_index] > date:
            result.append(row)
    return result

# функция для выполнения SELECT запроса
def select_from_table(conn, results):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT * FROM client.results;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

# функция для выполнения INSERT запроса
def insert_into_table(conn, table_name, values):
    with conn.cursor() as cur:
        query = f"insert into client.results (dateResult, description) VALUES ('2021-05-01', 'Результат теста свидетельствует о высоком уровне стресса.');"
        cur.execute(query)
    conn.commit()

# функция для выполнения UPDATE запроса
def update_table(conn, table_name, column_name, condition, new_value):
    with conn.cursor() as cur:
        query = f"update client.results set description = 1 where idResults = 12;"
        cur.execute(query)
    conn.commit()

# функция для выполнения DELETE запроса
def delete_from_table(conn, table_name, condition):
    with conn.cursor() as cur:
        query = f"DELETE FROM client.results WHERE idResults = 12;"
        cur.execute(query)
    conn.commit()

# функция для выполнения SELECT запроса
def select_from_table2(conn, client):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT * FROM client.client;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

# функция для выполнения INSERT запроса
def insert_into_table2(conn, table_name, values):
    with conn.cursor() as cur:
        query = f"INSERT INTO client.client (nameclient, phone, email) VALUES ('Петров И.И.', '3545675', 'Client20@gmail.com');"
        cur.execute(query)
    conn.commit()

# функция для выполнения UPDATE запроса
def update_table2(conn, table_name, column_name, condition, new_value):
    with conn.cursor() as cur:
        query = f"update client.client set phone = 1 where idClient = 15;"
        cur.execute(query)
    conn.commit()

# функция для выполнения DELETE запроса
def delete_from_table2(conn, table_name, condition):
    with conn.cursor() as cur:
        query = f"DELETE FROM client.Client WHERE idClient = 15;"
        cur.execute(query)
    conn.commit()

# функция для выполнения SELECT запроса
def select_from_table2_2(conn, therapist):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT * FROM therapists.therapist;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

# функция для выполнения INSERT запроса
def insert_into_table2_2(conn, table_name, values):
    with conn.cursor() as cur:
        query = f"insert into therapists.therapist (nametherapist, email, phone, hospitalId, educationId,coursesId,experienceId,questionsId,costId) values ('Иванов А.','ivan@mail.ru','11111111111',1,1,1,1,1,1);"
        cur.execute(query)
    conn.commit()

# функция для выполнения UPDATE запроса
def update_table2_2(conn, table_name, column_name, condition, new_value):
    with conn.cursor() as cur:
        query = f"update therapists.therapist set phone = '1234567890' where idtherapist = 1;"
        cur.execute(query)
    conn.commit()

# функция для выполнения DELETE запроса
def delete_from_table2_2(conn, table_name, condition):
    with conn.cursor() as cur:
        query = f"delete from therapists.therapist where idtherapist  = 5;"
        cur.execute(query)
    conn.commit()

# функция для выполнения SELECT запроса
def select_from_table2_3(conn, hospital):
    res = []
    with conn.cursor() as cur:
        query = f"select * from therapists.hospital;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

# функция для выполнения INSERT запроса
def insert_into_table2_3(conn, table_name, values):
    with conn.cursor() as cur:
        query = f"insert into therapists.hospital (namehospital, address) values ('#1','Ленина,10');"
        cur.execute(query)
    conn.commit()

# функция для выполнения UPDATE запроса
def update_table2_3(conn, table_name, column_name, condition, new_value):
    with conn.cursor() as cur:
        query = f"update therapists.hospital set address = 'Ленина,5' where idhospital = 7;"
        cur.execute(query)
    conn.commit()

# функция для выполнения DELETE запроса
def delete_from_table2_3(conn, table_name, condition):
    with conn.cursor() as cur:
        query = f"delete from therapists.hospital where idhospital = 12;"
        cur.execute(query)
    conn.commit()

#def insert_into_table_for_review(conn, table_name, values):
#    with conn.cursor() as cur:
#        query = f"INSERT INTO review (description, idClient) VALUES (?, ?);"
#        cur.execute(query)
#    conn.commit()

def select_from_table_tests(conn, client):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT nameTest FROM client.tests;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

def select_from_table_dateC(conn, client):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT Client.nameClient, Client.idContract, Contract.dateFinish FROM client.Client JOIN client.Contract ON Client.idContract = Contract.idContract;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

def select_from_table_results(conn, results):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT tests.nametest, results.dateresult, results.description FROM client.tests JOIN client.results ON tests.idresults = results.idresults WHERE results.dateresult BETWEEN '2021-01-01' AND '2021-12-31';"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res


def select_from_table_hosp(conn, client):
    res = []
    with conn.cursor() as cur:
        query = f"select therapist.nametherapist, hospital.namehospital, hospital.address from therapists.therapist join therapists.hospital on therapist.hospitalId=hospital.idhospital;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

def select_from_table_price(conn, results):
    res = []
    with conn.cursor() as cur:
        query = f"select therapist.nametherapist, costs.price from therapists.therapist join therapists.costs on therapist.costId=costs.idCost where costs.price < 2000;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res


# функция для выполнения INSERT запроса
def insert_for_group(conn, table_name, values):
    with conn.cursor() as cur:
        query = f"insert into client.groupClient (visitDate, nameGroup, idClient) VALUES ('2023-04-11', 'Групповая терапия для преодоления социальной фобии', 1);"
        cur.execute(query)
    conn.commit()

# функция для выполнения UPDATE запроса
def update_for_group(conn, table_name, column_name, condition, new_value):
    with conn.cursor() as cur:
        query = f"update client.groupClient set idClient = 10 where idClient = 1;"
        cur.execute(query)
    conn.commit()



# функция для выполнения DELETE запроса
def delete_for_group(conn, table_name, condition):
    with conn.cursor() as cur:
        query = f"DELETE FROM client.groupClient WHERE idClient = 2;"
        cur.execute(query)
    conn.commit()


class GroupDialog(QDialog):
    def __init__(self):
        super().__init__()

        # здесь размещаем виджеты для групповой терапии, например, таблицу записей

        self.register_button = QPushButton("Записаться", self)
        self.register_button.clicked.connect(self.register_for_group)

        self.cancel_button = QPushButton("Отменить", self)
        self.cancel_button.clicked.connect(self.cancel_registration)

        self.reschedule_button = QPushButton("Перенести", self)
        self.reschedule_button.clicked.connect(self.reschedule_registration)

        hbox = QHBoxLayout()
        hbox.addWidget(self.register_button)
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.reschedule_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def register_for_group(self):
        # обработка нажатия кнопки "Записаться"
        conn = create_conn()
        if conn:
            values = ("'2023-04-11'", "'Групповая терапия для преодоления социальной фобии'", 1)
            insert_for_group(conn, 'table_name', values)
            QMessageBox.information(self, 'Insertion: ', 'Values inserted successfully!')
            conn.close()

    def cancel_registration(self):
        # обработка нажатия кнопки "Отменить"
        conn = create_conn()
        if conn:
            delete_for_group(conn, 'table_name', 'idClient = 2')
            QMessageBox.information(self, 'Delete: ', 'Values deleted successfully!')
            conn.close()

    def reschedule_registration(self):
        # обработка нажатия кнопки "Перенести"
        conn = create_conn()
        if conn:
            update_for_group(conn, 'table_name', 'column_name', 'idClient = 1', 1)
            QMessageBox.information(self, 'Update: ', 'Values updated successfully!')
            conn.close()

class ReviewDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оставить отзыв")
        self.setFixedSize(300, 200)

        self.review_label = QLabel("Введите отзыв:")
        self.review_text_edit = QTextEdit(self)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.add_review_to_db)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.review_label)
        vbox.addWidget(self.review_text_edit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def add_review_to_db(self):
        # вставляем отзыв в базу данных
        conn = create_conn()
        if conn:
            #description = self.review_text_edit.toPlainText()
            #cursor = conn.cursor()
            #cursor.execute("INSERT INTO client.review (date_review, description) VALUES ('2023-04-11', '" + description + "');)"
            #conn.commit()
            #QMessageBox.information(self, "Успех", "Отзыв успешно добавлен!")
            pass


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    #def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
    #    painter = QPainter(self)
    #    painter.setBrush(Qt.lightGray)
    #    painter.drawRect(self.rect())

    def setupUi(self):
        # Основное окно
        self.setWindowTitle("Психологическая помощь")
        #self.setGeometry(300, 300, 300, 300)
        self.resize(1900, 1000)
        self.setMinimumSize(QtCore.QSize(1000, 800))
        self.setMaximumSize(QtCore.QSize(1800, 1300))

        self.chat_button = QPushButton("Оставить отзыв", self)
        self.chat_button.clicked.connect(self.show_review)
        self.chat_button.setGeometry(QtCore.QRect(1250, 20, 500, 50))

        # Календарь
        self.calendar_label = QLabel("Ближайший сеанс:", self)
        self.calendar = QCalendarWidget(self)
        self.calendar_label.setGeometry(QtCore.QRect(1250, 80, 500, 50))
        self.calendar.setGeometry(QtCore.QRect(1250, 150, 500, 500))

        self.back_button = QPushButton("Выход", self)
        self.back_button.clicked.connect(self.show_exit)
        self.back_button.setGeometry(QtCore.QRect(50, 20, 200, 50))

        self.group_button = QPushButton("Групповая терапия", self)
        self.group_button.setGeometry(QtCore.QRect(1250, 700, 500, 50))
        self.group_button.clicked.connect(self.show_group)
        # Психологические тесты
        self.tests_button = QPushButton("Психологические тесты", self)
        self.tests_button.setGeometry(QtCore.QRect(1250, 770, 500, 50))
        self.tests_button.clicked.connect(self.show_tests)
        # Результаты
        self.results_button = QPushButton("Результаты", self)
        self.results_button.clicked.connect(self.show_result)
        self.results_button.setGeometry(QtCore.QRect(1250, 840, 500, 50))
        #--------------------------------------------------------------------------------------------------------------
        # Для моей базы данных
        self.client_label = QLabel("Запросы для таблицы Client:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 80, 200, 50))

        select_btn2 = QPushButton('Select for Client', self)
        select_btn2.setToolTip('Execute SELECT query')
        select_btn2.setGeometry(QtCore.QRect(50, 150, 200, 50))
        select_btn2.clicked.connect(self.select_button_clicked2)

        insert_btn2 = QPushButton('Insert for Client', self)
        insert_btn2.setToolTip('Execute INSERT query')
        insert_btn2.setGeometry(QtCore.QRect(50, 220, 200, 50))
        insert_btn2.clicked.connect(self.insert_button_clicked2)

        update_btn2 = QPushButton('Update for Client', self)
        update_btn2.setToolTip('Execute UPDATE query')
        update_btn2.setGeometry(QtCore.QRect(50, 290, 200, 50))
        update_btn2.clicked.connect(self.update_button_clicked2)

        delete_btn2 = QPushButton('Delete for Client', self)
        delete_btn2.setToolTip('Execute Delete query')
        delete_btn2.setGeometry(QtCore.QRect(50, 360, 200, 50))
        delete_btn2.clicked.connect(self.delete_button_clicked2)

        self.client_label = QLabel("Запросы для таблицы Results:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 430, 200, 50))

        select_btn = QPushButton('Select for Results', self)
        select_btn.setToolTip('Execute SELECT query')
        select_btn.setGeometry(QtCore.QRect(50, 500, 200, 50))
        select_btn.clicked.connect(self.select_button_clicked)

        insert_btn = QPushButton('Insert for Results', self)
        insert_btn.setToolTip('Execute INSERT query')
        insert_btn.setGeometry(QtCore.QRect(50, 570, 200, 50))
        insert_btn.clicked.connect(self.insert_button_clicked)

        update_btn = QPushButton('Update for Results', self)
        update_btn.setToolTip('Execute UPDATE query')
        update_btn.setGeometry(QtCore.QRect(50, 640, 200, 50))
        update_btn.clicked.connect(self.update_button_clicked)

        delete_btn = QPushButton('Delete for Results', self)
        delete_btn.setToolTip('Execute Delete query')
        delete_btn.setGeometry(QtCore.QRect(50, 710, 200, 50))
        delete_btn.clicked.connect(self.delete_button_clicked)

        self.client_label = QLabel("Запросы с join:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 770, 200, 50))

        select_btn_j1 = QPushButton('Select for DateFinish', self)
        select_btn_j1.setToolTip('Execute SELECT query')
        select_btn_j1.setGeometry(QtCore.QRect(50, 840, 200, 50))
        select_btn_j1.clicked.connect(self.select_button_clickedj1)

        select_btn_j2 = QPushButton('Select for DateResult', self)
        select_btn_j2.setToolTip('Execute SELECT query')
        select_btn_j2.setGeometry(QtCore.QRect(50, 910, 200, 50))
        select_btn_j2.clicked.connect(self.select_button_clickedj2)
        #--------------------------------------------------------------------------------------------------------------
        #Для базы данных Тани
        self.client_label = QLabel("Запросы для таблицы Therapist:", self)
        self.client_label.setGeometry(QtCore.QRect(305, 80, 200, 50))

        select_btn2_2 = QPushButton('Select for Therapist', self)
        select_btn2_2.setToolTip('Execute SELECT query')
        select_btn2_2.setGeometry(QtCore.QRect(300, 150, 200, 50))
        select_btn2_2.clicked.connect(self.select_button_clicked2_2)

        insert_btn2_2 = QPushButton('Insert for Therapist', self)
        insert_btn2_2.setToolTip('Execute INSERT query')
        insert_btn2_2.setGeometry(QtCore.QRect(300, 220, 200, 50))
        insert_btn2_2.clicked.connect(self.insert_button_clicked2_2)

        update_btn2_2 = QPushButton('Update for Therapist', self)
        update_btn2_2.setToolTip('Execute UPDATE query')
        update_btn2_2.setGeometry(QtCore.QRect(300, 290, 200, 50))
        update_btn2_2.clicked.connect(self.update_button_clicked2_2)

        delete_btn2_2 = QPushButton('Delete for Therapist', self)
        delete_btn2_2.setToolTip('Execute Delete query')
        delete_btn2_2.setGeometry(QtCore.QRect(300, 360, 200, 50))
        delete_btn2_2.clicked.connect(self.delete_button_clicked2_2)

        self.client_label = QLabel("Запросы для таблицы Hospital:", self)
        self.client_label.setGeometry(QtCore.QRect(305, 430, 200, 50))

        select_btn = QPushButton('Select for Hospital', self)
        select_btn.setToolTip('Execute SELECT query')
        select_btn.setGeometry(QtCore.QRect(300, 500, 200, 50))
        select_btn.clicked.connect(self.select_button_clicked2_3)

        insert_btn = QPushButton('Insert for Hospital', self)
        insert_btn.setToolTip('Execute INSERT query')
        insert_btn.setGeometry(QtCore.QRect(300, 570, 200, 50))
        insert_btn.clicked.connect(self.insert_button_clicked2_3)

        update_btn = QPushButton('Update for Hospital', self)
        update_btn.setToolTip('Execute UPDATE query')
        update_btn.setGeometry(QtCore.QRect(300, 640, 200, 50))
        update_btn.clicked.connect(self.update_button_clicked2_3)

        delete_btn = QPushButton('Delete for Hospital', self)
        delete_btn.setToolTip('Execute Delete query')
        delete_btn.setGeometry(QtCore.QRect(300, 710, 200, 50))
        delete_btn.clicked.connect(self.delete_button_clicked2_3)

        self.client_label = QLabel("Запросы с join:", self)
        self.client_label.setGeometry(QtCore.QRect(305, 770, 200, 50))

        select_btn_j1 = QPushButton('Select for Address', self)
        select_btn_j1.setToolTip('Execute SELECT query')
        select_btn_j1.setGeometry(QtCore.QRect(300, 840, 200, 50))
        select_btn_j1.clicked.connect(self.select_button_clickedj1_2)

        select_btn_j2 = QPushButton('Select for Price', self)
        select_btn_j2.setToolTip('Execute SELECT query')
        select_btn_j2.setGeometry(QtCore.QRect(300, 910, 200, 50))
        select_btn_j2.clicked.connect(self.select_button_clickedj2_2)
        # --------------------------------------------------------------------------------------------------------------
        # Для базы данных Кати
        self.client_label = QLabel("Запросы для таблицы Diagnosis:", self)
        self.client_label.setGeometry(QtCore.QRect(555, 80, 200, 50))

        select_btn2_2k = QPushButton('Select for Diagnosis', self)
        select_btn2_2k.setToolTip('Execute SELECT query')
        select_btn2_2k.setGeometry(QtCore.QRect(550, 150, 200, 50))
        select_btn2_2k.clicked.connect(self.select_button_clicked2_4)

        insert_btn2_2k = QPushButton('Insert for Diagnosis', self)
        insert_btn2_2k.setToolTip('Execute INSERT query')
        insert_btn2_2k.setGeometry(QtCore.QRect(550, 220, 200, 50))
        insert_btn2_2k.clicked.connect(self.insert_button_clicked2_4)

        update_btn2_2k = QPushButton('Update for Diagnosis', self)
        update_btn2_2k.setToolTip('Execute UPDATE query')
        update_btn2_2k.setGeometry(QtCore.QRect(550, 290, 200, 50))
        update_btn2_2k.clicked.connect(self.update_button_clicked2_4)

        delete_btn2_2k = QPushButton('Delete for Diagnosis', self)
        delete_btn2_2k.setToolTip('Execute Delete query')
        delete_btn2_2k.setGeometry(QtCore.QRect(550, 360, 200, 50))
        delete_btn2_2k.clicked.connect(self.delete_button_clicked2_4)

        self.client_label = QLabel("Сложные запросы:", self)
        self.client_label.setGeometry(QtCore.QRect(555, 770, 200, 50))

        select_btn_j12 = QPushButton('Select for PublicationDate', self)
        select_btn_j12.setToolTip('Execute SELECT query')
        select_btn_j12.setGeometry(QtCore.QRect(550, 840, 200, 50))
        select_btn_j12.clicked.connect(self.select_button_clicked2_5)

        select_btn_j22 = QPushButton('Select for Therapy', self)
        select_btn_j22.setToolTip('Execute SELECT query')
        select_btn_j22.setGeometry(QtCore.QRect(550, 910, 200, 50))
        select_btn_j22.clicked.connect(self.select_button_clicked2_6)

    def select_button_clicked2_4(self):
        result = select_from_csv_file(r'/BD/diagnosis.csv')
        show_message_box(result)

    def select_button_clicked2_5(self):
        result = select_date_above('2022-01-01')
        show_message_box(result)


    def select_button_clicked2_6(self):
        result = select_rows_with_date_and_columns('diagnosis.csv', ['method.therapy', 'name'], '2022-01-01')
        show_message_box(result)

    def insert_button_clicked2_4(self):
        values = ['Лукиных Н.Б.', 'Алкоголизм – это болезнь', 'https://zhivika.ru/article/alkogol', '2022-05-01', '',
                  'Борьба с алкоголизмом', 'Мотивационная терапия', '', 'Алкогольная зависимость']
        insert_into_csv_file('diagnosis.csv', values)
        QMessageBox.information(self, 'Insertion: ', 'Values inserted successfully!')


    def update_button_clicked2_4(self):
        update_csv_file('diagnosis.csv', set_column='articles.author', set_value='-', where_column='articles.author',
                        where_value='Лукиных Н.Б.')
        QMessageBox.information(self, 'Update: ', 'Values updated successfully!')

    def delete_button_clicked2_4(self):
        delete_from_csv_file('diagnosis.csv', where_column='_id', where_value='11')
        QMessageBox.information(self, 'Delete: ', 'Values deleted successfully!')

    def select_button_clicked(self):
        conn = create_conn()
        if conn:
            res = select_from_table(conn, 'results')
            QMessageBox.information(self, 'Results: ', str(res))
            conn.close()

    def insert_button_clicked(self):
        conn = create_conn()
        if conn:
            values = "(1, '2021-05-01', 'Результат теста свидетельствует о высоком уровне стресса.');"
            insert_into_table(conn, 'table_name', values)
            QMessageBox.information(self, 'Insertion: ', 'Values inserted successfully!')
            conn.close()

    def update_button_clicked(self):
        conn = create_conn()
        if conn:
            update_table(conn, 'table_name', 'column_name', 'idResults = 12', 1)
            QMessageBox.information(self, 'Update: ', 'Values updated successfully!')
            conn.close()

    def delete_button_clicked(self):
        conn = create_conn()
        if conn:
            delete_from_table(conn, 'table_name', 'idResults = 12')
            QMessageBox.information(self, 'Delete: ', 'Values deleted successfully!')
            conn.close()

    def select_button_clicked2(self):
        conn = create_conn()
        if conn:
            res = select_from_table2(conn, 'client')
            QMessageBox.information(self, 'Results: ', str(res))
            conn.close()

    def insert_button_clicked2(self):
        conn = create_conn()
        if conn:
            values = "(1, 'value')"
            insert_into_table2(conn, 'table_name', values)
            QMessageBox.information(self, 'Insertion: ', 'Values inserted successfully!')
            conn.close()

    def update_button_clicked2(self):
        conn = create_conn()
        if conn:
            update_table2(conn, 'table_name', 'column_name', 'idClient = 15', 1)
            QMessageBox.information(self, 'Update: ', 'Values updated successfully!')
            conn.close()

    def delete_button_clicked2(self):
        conn = create_conn()
        if conn:
            delete_from_table2(conn, 'table_name', 'idClient = 15')
            QMessageBox.information(self, 'Delete: ', 'Values deleted successfully!')
            conn.close()

    def select_button_clicked2_2(self):
        conn = create_conn()
        if conn:
            res = select_from_table2_2(conn, 'therapist')
            QMessageBox.information(self, 'Results: ', str(res))
            conn.close()

    def insert_button_clicked2_2(self):
        conn = create_conn()
        if conn:
            values = "(1, 'value')"
            insert_into_table2_2(conn, 'table_name', values)
            QMessageBox.information(self, 'Insertion: ', 'Values inserted successfully!')
            conn.close()

    def update_button_clicked2_2(self):
        conn = create_conn()
        if conn:
            update_table2_2(conn, 'table_name', 'column_name', 'idtherapist = 1', 1)
            QMessageBox.information(self, 'Update: ', 'Values updated successfully!')
            conn.close()

    def delete_button_clicked2_2(self):
        conn = create_conn()
        if conn:
            delete_from_table2_2(conn, 'table_name', 'idtherapist  = 5')
            QMessageBox.information(self, 'Delete: ', 'Values deleted successfully!')
            conn.close()

    def select_button_clicked2_3(self):
        conn = create_conn()
        if conn:
            res = select_from_table2_3(conn, 'hospital')
            QMessageBox.information(self, 'Results: ', str(res))
            conn.close()

    def insert_button_clicked2_3(self):
        conn = create_conn()
        if conn:
            values = "(1, 'value')"
            insert_into_table2_3(conn, 'table_name', values)
            QMessageBox.information(self, 'Insertion: ', 'Values inserted successfully!')
            conn.close()

    def update_button_clicked2_3(self):
        conn = create_conn()
        if conn:
            update_table2_3(conn, 'table_name', 'column_name', 'idhospital = 7')
            QMessageBox.information(self, 'Update: ', 'Values updated successfully!')
            conn.close()

    def delete_button_clicked2_3(self):
        conn = create_conn()
        if conn:
            delete_from_table2_3(conn, 'table_name', 'idhospital = 12')
            QMessageBox.information(self, 'Delete: ', 'Values deleted successfully!')
            conn.close()

    def show_review(self):
        dialog = ReviewDialog()
        dialog.exec_()

    def show_group(self):
        dialog = GroupDialog()
        dialog.exec_()

    def show_tests(self):
        conn = create_conn()
        if conn:
            res = select_from_table_tests(conn, 'tests')
            QMessageBox.information(self, 'Tests: ', str(res))
            conn.close()

    def show_result(self):
        conn = create_conn()
        if conn:
            res = select_from_table_results(conn, 'results')
            QMessageBox.information(self, 'Results: ', str(res))
            conn.close()

    def show_exit(self):
        reply = QMessageBox.question(self, "Подтверждение выхода", "Вы уверены, что хотите выйти?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def select_button_clickedj1(self):
        conn = create_conn()
        if conn:
            res = select_from_table_dateC(conn, 'contract')
            QMessageBox.information(self, 'Contracts: ', str(res))
            conn.close()

    def select_button_clickedj2(self):
        conn = create_conn()
        if conn:
            res = select_from_table_results(conn, 'results')
            QMessageBox.information(self, 'Results: ', str(res))
            conn.close()

    def select_button_clickedj1_2(self):
        conn = create_conn()
        if conn:
            res = select_from_table_hosp(conn, 'hospital')
            QMessageBox.information(self, 'Hospitals: ', str(res))
            conn.close()

    def select_button_clickedj2_2(self):
        conn = create_conn()
        if conn:
            res = select_from_table_price(conn, 'price')
            QMessageBox.information(self, 'Prices: ', str(res))
            conn.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec())

    window2 = GroupDialog()
    window2.show()

