from tkinter import *
from service import *
import requests
from App.Scenes import *


def scene(func):
    def decorator(*args):
        if args[0].scene is not None:
            args[0].scene.close()
        return func(*args)

    return decorator


class StartApp(Tk):
    def __init__(self):
        super().__init__()

        # Init service with API requests
        self.service = Service()

        self.title('Analiza danych - kursy danych')
        self.init_menu()

        # Start window
        self.scene = None
        self.mainloop()

    @scene
    def set_gold_last_week_scene(self):
        self.scene = gold_last_week.GoldLastWeekScene(self)

    @scene
    def set_one_currency_scene(self, table_type):
        self.scene = one_currency.OneCurrencyScene(self, table_type)

    def init_menu(self):
        menu = Menu(self)

        self.config(menu=menu)

        currency_tables_menu = Menu(menu)
        currency_tables_menu.add_command(
            label="Zwykłe",
            command=lambda: self.set_one_currency_scene("common")
        )
        currency_tables_menu.add_command(
            label="Nietypowe",
            command=lambda: self.set_one_currency_scene("uncommon")
        )
        currency_tables_menu.add_command(
            label="Kupno/Sprzedaż",
            command=lambda: self.set_one_currency_scene("buy-sell")
        )

        # currencies_tables_menu = Menu(currencies_menu)
        # currencies_tables_menu.add_command(
        #     label="Zwykłe"
        # )
        # currencies_tables_menu.add_command(
        #     label="Nietypowe"
        # )
        # currencies_tables_menu.add_command(
        #     label="Kupno/Sprzedaż"
        # )
        # currencies_menu.add_cascade(
        #     label="Wszystkie waluty",
        #     menu=currencies_tables_menu
        # )

        menu.add_cascade(
            label="Waluty",
            menu=currency_tables_menu
        )


        menu.add_command(
            label="Złoto",
            command=self.set_gold_last_week_scene
        )