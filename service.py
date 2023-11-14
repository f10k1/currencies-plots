from enum import Enum
import requests

class Service:
    def __init__(self):
        self.base_url = "https://api.nbp.pl/api"

        self.__api_types = {
            "currency": "exchangerates",
            "gold": "cenyzlota"
        }

        self.__currency_count = {
            "multiple": "tables",
            "single": "rates"
        }

        self.__currency_tables = {
            "common": "A",
            "uncommon": "B",
            "buy-sell": "C"
        }

        self.__currency_codes = {
            "common": {},
            "uncommon": {},
            "buy-sell": {}
        }

    def get_currency_codes(self, table):
        if not self.__currency_codes[table]:
            try:
                request = requests.get(f"{self.base_url}/{self.__api_types['currency']}/{self.__currency_count['multiple']}/{self.__currency_tables[table]}/")
                print(request)
                request.raise_for_status()

                json = request.json()

                for row in json:
                    for currency in row['rates']:
                        self.__currency_codes[table][currency["currency"]] = currency["code"]

            except requests.exceptions.RequestException:
                raise Exception("Coś poszło nie tak podczas pobierania kodów walut")
        return self.__currency_codes[table]

    def get_data(self, api_type, table='common', count='multiple', currency=None, days_range=7):
        url = f"{self.base_url}/{self.__api_types[api_type]}/"
        if api_type == "currency":
            url += f"{self.__currency_count[count]}/{self.__currency_tables[table]}/"

            if count == "single":
                if currency is None:
                    return Exception("Musisz podać kod waluty")
                else:
                    url += currency+"/"
        url += f"last/{days_range}/"
        try:
            request = requests.get(url)

            request.raise_for_status()

            json = request.json()

            return json

        except requests.exceptions.RequestException:
            raise Exception("Coś poszło nie tak podczas pobierania statystyk")
