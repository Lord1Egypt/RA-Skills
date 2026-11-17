"""Offline review regressions; no OA business traffic or credentials."""
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import oa_utils as api

class ReviewHardeningTests(unittest.TestCase):
    def test_details_redirect_never_reaches_cross_origin_adapter(self):
        import requests
        class Adapter(requests.adapters.BaseAdapter):
            def __init__(self): self.seen = []
            def send(self, request, **kwargs):
                self.seen.append(request)
                response = requests.Response()
                response.status_code = 302
                response.headers['Location'] = 'https://collector.invalid/steal'
                response._content = b'{}'
                response.request = request
                return response
            def close(self): pass
        session = requests.Session()
        session.trust_env = False
        session.headers['Admin-OA-Token'] = 'synthetic-only'
        adapter = Adapter()
        session.mount('https://', adapter)
        try:
            api.get_time_entry_details(session, 'https://oa.invalid', '123')
        except (ValueError, requests.exceptions.TooManyRedirects):
            pass
        else:
            self.fail('redirect must be rejected')
        self.assertEqual(len(adapter.seen), 1)
        self.assertEqual(adapter.seen[0].url, 'https://oa.invalid/sn/timeEntry/details/123')

if __name__ == '__main__': unittest.main()
