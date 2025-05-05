
import redis
import logging
import time


class StoreException(Exception):
    pass


class Store:
    def __init__(self, host="localhost", port=6379, db=0, retries=3, retry_delay=0.1, timeout=0.5):
        self.host = host
        self.port = port
        self.db = db
        self.retries = retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self._client = None
        self._connect()

    def _connect(self):
        try:
            self._client = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.db,
                socket_connect_timeout=self.timeout,
                socket_timeout=self.timeout,
                decode_responses=True,
            )
            self._client.ping()
        except Exception as e:
            logging.error("Store connection failed: %s", e)
            self._client = None

    def _ensure_connection(self):
        if self._client is None:
            self._connect()

    def get(self, key):
        for attempt in range(self.retries):
            try:
                self._ensure_connection()
                if not self._client:
                    raise StoreException("No connection")
                return self._client.get(key)
            except Exception as e:
                logging.warning("Store.get failed (attempt %s): %s", attempt + 1, e)
                time.sleep(self.retry_delay)
        raise StoreException("Store.get failed after retries")

    def cache_get(self, key):
        try:
            self._ensure_connection()
            if not self._client:
                return None
            return self._client.get(key)
        except Exception as e:
            logging.warning("Store.cache_get failed: %s", e)
            return None

    def set(self, key, value, ex=None):
        try:
            self._ensure_connection()
            if not self._client:
                return
            self._client.set(key, value, ex=ex)
        except Exception as e:
            logging.warning("Store.set failed: %s", e)
