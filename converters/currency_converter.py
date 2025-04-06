class CurrencyConverter:
    def __init__(self, rate_service):
        self.rate_service = rate_service

    def convert(self, amount, currency_code):
        rates = self.rate_service.rates
        if rates is None:
            raise Exception("Курсы обмена недоступны")
        try:
            rate = rates[currency_code.upper()]
        except KeyError:
            raise ValueError(f"Валюта {currency_code} не поддерживается")
        return amount * rate