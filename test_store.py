
import unittest
from unittest.mock import MagicMock, patch
from store import Store, StoreException


class StoreTests(unittest.TestCase):

    @patch("store.redis.StrictRedis")
    def test_store_get_success(self, mock_redis_cls):
        mock_redis = MagicMock()
        mock_redis.get.return_value = "value"
        mock_redis.ping.return_value = True
        mock_redis_cls.return_value = mock_redis

        store = Store()
        result = store.get("key")
        self.assertEqual(result, "value")

    @patch("store.redis.StrictRedis")
    def test_store_get_fails_after_retries(self, mock_redis_cls):
        mock_redis_cls.side_effect = Exception("connection error")
        store = Store(retries=2, retry_delay=0.01)
        with self.assertRaises(StoreException):
            store.get("key")

    @patch("store.redis.StrictRedis")
    def test_store_cache_get_does_not_raise(self, mock_redis_cls):
        mock_redis_cls.side_effect = Exception("boom")
        store = Store()
        result = store.cache_get("key")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
