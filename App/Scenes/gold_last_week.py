from tkinter import *
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


class GoldLastWeekScene:
    def __init__(self, app):
        self.app = app

        self.week_btn = Button(app, command=lambda: self.set_range(7), text="Ostatne 7 dni")
        self.week_btn.pack()
        self.month_btn = Button(app, command=lambda: self.set_range(31), text="Ostatnie 31 dni")
        self.month_btn.pack()
        self.hundred_btn = Button(app, command=lambda: self.set_range(100), text="Ostatnie 100 dni")
        self.hundred_btn.pack()

        self.days_range = 7

        self.figure_canvas = None
        self.toolbar = None

        self.print_chart()


    def print_chart(self):
        try:
            raw_data = self.app.service.get_data("gold", days_range=self.days_range)
        except Exception as err:
            print(err)
            return

        data = {}

        for item in raw_data:
            data[item['data']] = item['cena']

        date = data.keys()
        price = data.values()

        if self.figure_canvas:
            self.toolbar.destroy()
            self.figure_canvas.get_tk_widget().destroy()

        figure = Figure(figsize=(10, 3), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(figure, self.app)
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self.app)
        axes = figure.add_subplot()
        axes.plot(date, price, marker="o")
        if self.days_range == 100:
            axes.set_xticks(list(range(0, 100, 10)))
        elif self.days_range == 31:
            axes.set_xticks(list(range(0, 31, 3)))
        axes.set_title(f'Kurs złota z ostatnich {self.days_range} dni')
        axes.set_ylabel('Cena złota w zł/g')
        self.figure_canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)

    def set_range(self, days_range):
        self.days_range = days_range
        self.print_chart()

    def close(self):
        self.toolbar.destroy()
        self.figure_canvas.get_tk_widget().destroy()
        self.week_btn.destroy()
        self.month_btn.destroy()
        self.hundred_btn.destroy()
