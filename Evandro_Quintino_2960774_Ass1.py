import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox, QCheckBox
from PyQt5 import QtGui
from decimal import Decimal

# Test  Evandro aqui eh um test


class StockTradeProfitCalculator(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Loading Database to TradeStock
        self.data = self.make_data()
        self.stocks = sorted(self.data.keys())

        # Labels
        self.stockPurched_label = QLabel("Stock Purchased:")
        self.qtyPurched_label = QLabel("Quantity Purchased:")
        self.purchaseDate_label = QLabel("Purchase Date:")
        self.purchaseTotal_label = QLabel("<b>Purchase Total:</b>")
        self.sellDate_label = QLabel("Sell Date")
        self.sellTotal_label = QLabel("<b>Sell Total:</b>")
        self.profitTotal_label = QLabel("<b>Profit Total:</b>")
        self.qtySold_label = QLabel("Quantity Sold:")
        self.checkbox = QCheckBox("Selling Full Qty")
        # Labels - Total values into String
        self.purchase_TotalValue_label = QLabel("")
        self.sell_TotalValue_label = QLabel("")
        self.profit_TotalValue_label = QLabel("")

        # ComboBox
        self.stock_selection_combobox = QComboBox()
        self.stock_selection_combobox.addItems(self.stocks)

        # CheckBox - Setting default value to True
        self.checkbox.setChecked(True)

        # SpinBox - Range and Default Value
        self.stock_qtyPurchase = QSpinBox()
        self.stock_qtyPurchase.setRange(0, 999)
        self.stock_qtyPurchase.setValue(1)

        # SpinBox - Default Value
        self.stock_qtySold = QSpinBox()
        self.stock_qtySold.setValue(1)

        # SpingBox Selling - Updating selling spinbox maximum range
        self.stock_qtySold.setRange(0, self.stock_qtyPurchase.value())

        # Calendars
        self.purchaseCalendar = QCalendarWidget()
        self.sellCalendar = QCalendarWidget()

        #Calendars - Configuration
        # Setting buying minimum range date
        self.purchaseCalendar.setMinimumDate(QDate(2013, 2, 8))
        self.sellCalendar.setMinimumDate(QDate(2013, 2, 8))

        # Setting buying maximum range date
        self.purchaseCalendar.setMaximumDate(QDate(2018, 2, 7))
        self.sellCalendar.setMaximumDate(QDate(2018, 2, 7))

        # Defining our layout
        grid = QGridLayout()

        # Window Title
        self.setWindowTitle(
            "Stock Trade Profit Calculator - Evandro - 2960774")

        # First Column
        grid.addWidget(self.stockPurched_label, 0, 0)
        grid.addWidget(self.qtyPurched_label, 1, 0)
        grid.addWidget(self.purchaseDate_label, 2, 0)
        grid.addWidget(self.purchaseTotal_label, 3, 0)
        grid.addWidget(self.sellDate_label, 4, 0)
        grid.addWidget(self.sellTotal_label, 5, 0)
        grid.addWidget(self.profitTotal_label, 6, 0)

        # Second Column
        grid.addWidget(self.stock_selection_combobox, 0, 1)
        grid.addWidget(self.stock_qtyPurchase, 1, 1)
        grid.addWidget(self.purchaseCalendar, 2, 1, 1, 3)
        grid.addWidget(self.purchase_TotalValue_label, 3, 1)

        grid.addWidget(self.sellCalendar, 4, 1, 1, 3)
        grid.addWidget(self.sell_TotalValue_label, 5, 1)
        grid.addWidget(self.profit_TotalValue_label, 6, 1)

        # Third Column
        grid.addWidget(self.qtySold_label, 1, 2)
        grid.addWidget(self.stock_qtySold, 1, 3)
        grid.addWidget(self.checkbox, 0, 3)

        self.setLayout(grid)

        # Connecting signals to slots to that a change in one control updates the UI
        self.stock_selection_combobox.currentIndexChanged.connect(
            self.updateUi)

        # Connecting Calendars - Selecting date will activate the UI
        self.purchaseCalendar.clicked.connect(self.updateUi)
        self.sellCalendar.clicked.connect(self.updateUi)

        # Connecting SpinBox - Changing Value affects total values
        self.stock_qtyPurchase.valueChanged.connect(self.updateUi)
        self.stock_qtySold.valueChanged.connect(self.updateUi)
        self.checkbox.toggled.connect(self.updateUi)

    def make_data(self):
        '''
        Loading data to the program
        '''
        # Loading data to the program
        # open a CSV file for reading https://docs.python.org/3/library/functions.html#open
        file = open("./all_stocks_5yr.csv", "r")
        data = {}         # empty data dictionary
        file_rows = []    # empty list of file rows
        # add rows to the file_rows list
        for row in file:
            # https://www.geeksforgeeks.org/python-string-strip-2/
            file_rows.append(row.strip())
        print("len(file_rows):" + str(len(file_rows)))

        # get the column headings of the CSV file
        row0 = file_rows[0]
        line = row0.split(",")
        column_headings = line
        # print(column_headings)

        # get the unique list of stocks from the CSV file
        non_unique_stocks = []
        file_rows_from_row1_to_end = file_rows[1:len(file_rows) - 1]
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            non_unique_stocks.append(line[6])
        stocks = self.unique(non_unique_stocks)
        #print("len(stocks):" + str(len(stocks)))
        #print("stocks:" + str(stocks))

        # build the base dictionary of stocks
        for stock in stocks:
            data[stock] = {}

        # build the dictionary of dictionaries
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            date = self.string_date_into_QDate(line[0])
            stock = line[6]
            close_price = line[4]
            # include error handeling code if close price is incorrect
            data[stock][date] = float(close_price)
        print("len(data):", len(data))
        return data

    def updateUi(self):
        '''
        Updates the Ui when control values are changed, should also be called when the app initializes
        '''
        try:
            # Getting selected dates from calendars
            purchase_date = self.purchaseCalendar.selectedDate()
            selling_date = self.sellCalendar.selectedDate()

            # Fixing Purchase on weekends - Moving selectedDay to Monday
            if self.purchaseCalendar.selectedDate().dayOfWeek() == 6:
                purchase_date = QDate(
                    self.purchaseCalendar.selectedDate()).addDays(2)

            elif self.purchaseCalendar.selectedDate().dayOfWeek() == 7:
                purchase_date = QDate(
                    self.purchaseCalendar.selectedDate()).addDays(1)

            # Fixing Selling on weekends - Moving selectedDay to Monday
            if self.sellCalendar.selectedDate().dayOfWeek() == 6:
                selling_date = QDate(
                    self.sellCalendar.selectedDate()).addDays(2)

            elif self.sellCalendar.selectedDate().dayOfWeek() == 7:
                selling_date = QDate(
                    self.sellCalendar.selectedDate()).addDays(1)

            # SeelingCalendar - Setting new minimum date range
            self.sellCalendar.setMinimumDate(
                self.purchaseCalendar.selectedDate())

            # SellingQty SpinBox - If True, keeps same value as per Purchase; else, user can edit value
            if self.checkbox.isChecked():
                self.stock_qtySold.setRange(self.stock_qtyPurchase.value(), 0)
            else:
                self.stock_qtySold.setRange(0, self.stock_qtyPurchase.value())

            # Getting spinBox value
            qnty_purchase = self.stock_qtyPurchase.value()
            qnty_sold = self.stock_qtySold.value()

            # Getting stock selection
            stock_selected = self.stock_selection_combobox.currentText()

            # Getting 'close' value and populating it in purchase and selling totals
            closeValue_purchase = self.data[stock_selected][purchase_date]
            self.purchase_TotalValue_label.setText(
                str(round(closeValue_purchase * qnty_purchase, 2)))

            closeValue_selling = self.data[stock_selected][selling_date]
            self.sell_TotalValue_label.setText(
                str(round(closeValue_selling * qnty_sold, 2)))

            # ProfitTotal - Getting total profit
            totalValue = round(
                (closeValue_selling - closeValue_purchase) * qnty_sold, 2)

            # ProfitTotal - Setting color, depending on result
            if totalValue > 0:
                self.profit_TotalValue_label.setText(str(totalValue))
                self.profit_TotalValue_label.setStyleSheet('color:green')
            else:
                self.profit_TotalValue_label.setText(str(totalValue))
                self.profit_TotalValue_label.setStyleSheet('color:red')

        except Exception as e:
            print(e)

    def string_date_into_QDate(self, date_String):
        '''
        Converts a data in a string format like that in a CSV file to QDate Objects for use with QCalendarWidget
        : param date_String: data in a string format
        : return:
        '''

        date_list = date_String.split("-")
        date_QDate = QDate(int(date_list[0]), int(
            date_list[1]), int(date_list[2]))
        return date_QDate

    def unique(self, non_unique_list):
        '''
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        '''
        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list


if __name__ == '__main__':
    # Calling the app Window
    app = QApplication(sys.argv)
    stock_trader = StockTradeProfitCalculator()
    stock_trader.show()
    sys.exit(app.exec_())
