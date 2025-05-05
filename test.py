
import unittest
import hashlib
import datetime

import api  # предполагается, что api.py содержит метод method_handler


def cases(cases_list):
    def decorator(func):
        def wrapper(self):
            for i, case in enumerate(cases_list, 1):
                with self.subTest(case=case):
                    try:
                        func(self, case)
                    except Exception as e:
                        raise AssertionError(f"Case #{i} failed: {case}") from e
        return wrapper
    return decorator


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store = None

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    def test_empty_request(self):
        response, code = self.get_response({})
        self.assertEqual(api.INVALID_REQUEST, code)

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "", "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "badtoken", "arguments": {}},
        {"account": "horns&hoofs", "login": "admin", "method": "online_score", "token": "", "arguments": {}},
    ])
    def test_bad_auth(self, request):
        response, code = self.get_response(request)
        self.assertEqual(api.FORBIDDEN, code)

    def test_valid_auth_regular(self):
        login = "h&f"
        account = "horns&hoofs"
        token = hashlib.sha512((account + login + api.SALT).encode("utf-8")).hexdigest()
        request = {
            "account": account,
            "login": login,
            "token": token,
            "method": "online_score",
            "arguments": {}
        }
        _, code = self.get_response(request)
        self.assertNotEqual(code, api.FORBIDDEN)

    def test_valid_auth_admin(self):
        login = "admin"
        token = hashlib.sha512((datetime.datetime.now().strftime("%Y%m%d%H") + api.ADMIN_SALT).encode("utf-8")).hexdigest()
        request = {
            "account": "",
            "login": login,
            "token": token,
            "method": "online_score",
            "arguments": {}
        }
        _, code = self.get_response(request)
        self.assertNotEqual(code, api.FORBIDDEN)


if __name__ == "__main__":
    unittest.main()
