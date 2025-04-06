from converters.exchange_rate_service import ExchangeRateService
from converters.currency_converter import CurrencyConverter
from converters.constants import SUPPORTED_CURRENCIES

def main():
    try:
        amount = float(input("Введите значение в USD: "))
    except ValueError:
        print("Неверное значение. Ожидается число.")
        return

    service = ExchangeRateService()
    converter = CurrencyConverter(service)
    
    for currency in SUPPORTED_CURRENCIES:
        try:
            result = converter.convert(amount, currency)
            print(f"{amount} USD to {currency}: {result}")
        except Exception as e:
            print(f"Ошибка конвертации для {currency}: {e}")

if __name__ == "__main__":
    main()