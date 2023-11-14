from tkinter import *
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class OneCurrencyScene:
    def __init__(self, app, table_type):
        self.app = app
        self.table_type = table_type

        self.currency_input = Entry(app)
        self.currency_input.pack()
        self.currency_input.bind('<KeyRelease>', self.filter_currencies)

        self.currencies_list = Listbox(app)
        self.currencies_list.bind("<<ListboxSelect>>", self.pick_currency)
        self.currencies_list.pack()
        self.filter_currencies()

        self.week_btn = Button(app, command=lambda: self.set_range(7), text="Ostatne 7 dni")
        self.week_btn.pack()
        self.month_btn = Button(app, command=lambda: self.set_range(31), text="Ostatnie 31 dni")
        self.month_btn.pack()
        self.hundred_btn = Button(app, command=lambda: self.set_range(100), text="Ostatnie 100 dni")
        self.hundred_btn.pack()

        self.figure_canvas = None
        self.toolbar = None

        self.picked_code = None
        self.picked_range = 7

    def set_range(self, days_range):
        self.picked_range = days_range
        self.print_chart()

    def pick_currency(self, event):
        index = event.widget.curselection()[0]
        self.picked_code = event.widget.get(index).split(" - ")
        self.print_chart()

    def print_chart(self):
        if self.picked_code is None:
            return
        name, code = self.picked_code
        try:
            raw_data = self.app.service.get_data("currency", table=self.table_type, count="single", currency=code, days_range=self.picked_range)
        except Exception as err:
            print(err)
            return

        data = {}

        for currency in raw_data['rates']:
            if self.table_type != "buy-sell":
                data[currency['effectiveDate']] = currency['mid']
            else:
                data[currency['effectiveDate']] = [currency['bid'], currency['ask']]
        date = data.keys()
        price = data.values()

        if self.figure_canvas is not None:
            self.toolbar.destroy()
            self.figure_canvas.get_tk_widget().destroy()

        figure = Figure(dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(figure, self.app)
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self.app)
        axes = figure.add_subplot()
        axes.plot(date, price, marker="o")
        if self.picked_range == 100:
            axes.set_xticks(list(range(0, 100, 10)))
        elif self.picked_range == 31:
            axes.set_xticks(list(range(0, 31, 3)))
        axes.set_title(f'Kurs {name} z ostatnich {self.picked_range} dni')
        axes.set_ylabel(f'Cena {name} względem złotówki')
        self.figure_canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
    def filter_currencies(self, event=None):
        if event is None:
            value = ""
        else:
            value = event.widget.get()

        data = []
        try:
            currencies = self.app.service.get_currency_codes(self.table_type)
        except Exception as err:
            print(err)
            return

        for currency in currencies:
            text = f"{currency} - {currencies[currency]}"
            if value.lower() in text.lower() or value == '':
                data.append(text)

        self.update_currencies_list(data)

    def update_currencies_list(self, data):
        self.currencies_list.delete(0, 'end')
        for currency in data:
            self.currencies_list.insert("end", currency)

    def close(self):
        self.toolbar.destroy()
        self.figure_canvas.get_tk_widget().destroy()

        self.week_btn.destroy()
        self.month_btn.destroy()
        self.hundred_btn.destroy()

        self.currencies_list.destroy()
        self.currency_input.destroy()