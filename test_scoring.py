
import unittest
from unittest.mock import MagicMock
from scoring import get_score, get_interests
from store import StoreException


class ScoringTests(unittest.TestCase):
    def test_get_score_returns_cached(self):
        store = MagicMock()
        store.cache_get.return_value = "5.0"
        score = get_score(store, phone="79111234567", email="test@example.com")
        self.assertEqual(score, 5.0)

    def test_get_score_computes_and_caches(self):
        store = MagicMock()
        store.cache_get.return_value = None
        score = get_score(store, phone="79111234567", email="test@example.com")
        self.assertGreater(score, 0)
        store.set.assert_called_once()

    def test_get_score_works_without_store(self):
        score = get_score(None, phone="79111234567", email="test@example.com")
        self.assertGreater(score, 0)

    def test_get_interests_success(self):
        store = MagicMock()
        store.get.return_value = "books,hi-tech"
        result = get_interests(store, 42)
        self.assertEqual(result, ["books", "hi-tech"])

    def test_get_interests_raises_on_failure(self):
        store = MagicMock()
        store.get.side_effect = Exception("fail")
        with self.assertRaises(StoreException):
            get_interests(store, 123)

    def test_get_interests_no_store_raises(self):
        with self.assertRaises(StoreException):
            get_interests(None, 1)


if __name__ == "__main__":
    unittest.main()
