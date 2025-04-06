import requests
import time
import json
import os
import logging
from .constants import API_URL, CACHE_FILE, CACHE_EXPIRY, MAX_RETRIES, RETRY_DELAY

class ExchangeRateService:
    def __init__(self, api_url=API_URL, cache_file=CACHE_FILE, cache_expiry=CACHE_EXPIRY,
                 max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY):
        self.api_url = api_url
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = self._setup_logger()
        self.rates = self.get_rates()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            ch = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger

    def _load_from_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    data = json.load(f)
                    if time.time() - data["timestamp"] < self.cache_expiry:
                        return data["rates"]
            except (json.JSONDecodeError, KeyError):
                self.logger.info("Неверный формат кэша, получение новых данных.")
        return None

    def _save_to_cache(self, rates):
        try:
            data = {"timestamp": time.time(), "rates": rates}
            with open(self.cache_file, "w") as f:
                json.dump(data, f)
        except IOError as e:
            self.logger.error("Ошибка сохранения кэша: %s", e)

    def get_rates(self):
        rates = self._load_from_cache()
        if rates:
            return rates

        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.api_url, timeout=10)
                response.raise_for_status()
                data = response.json()
                rates = data["rates"]
                self._save_to_cache(rates)
                return rates
            except requests.exceptions.RequestException as e:
                self.logger.error("Попытка %d: %s", attempt + 1, e)
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error("Ошибка обработки данных: %s", e)
                break
        return None