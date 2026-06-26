#!/usr/bin/env python3
"""API Data Loader - REST API with retry, pagination, timeout."""

import json
import time
import logging
import argparse
from typing import Optional
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 30
_DEFAULT_MAX_RETRIES = 3


class APILoader:
    def __init__(self, base_url='', timeout=_DEFAULT_TIMEOUT, max_retries=_DEFAULT_MAX_RETRIES, headers=None):
        import requests
        self.session = requests.Session()
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        if headers:
            self.session.headers.update(headers)

    def set_auth_token(self, token, scheme='Bearer'):
        self.session.headers['Authorization'] = f'{scheme} {token}'

    def _request(self, method, url, **kwargs):
        import requests
        full_url = f"{self.base_url}/{url.lstrip('/')}" if self.base_url else url
        kwargs.setdefault('timeout', self.timeout)
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self.session.request(method, full_url, **kwargs)
                resp.raise_for_status()
                ct = resp.headers.get('Content-Type', '')
                if 'json' in ct:
                    return resp.json()
                if 'csv' in ct or 'text' in ct:
                    return resp.text
                return resp.content
            except requests.exceptions.RequestException as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
        raise RuntimeError(f"API request failed after {self.max_retries} retries") from last_exc

    def get(self, url, params=None):
        return self._request('GET', url, params=params)

    def fetch_json_to_df(self, url, params=None, data_key=None):
        raw = self.get(url, params=params)
        if data_key and isinstance(raw, dict):
            raw = raw[data_key]
        if isinstance(raw, list):
            return pd.DataFrame(raw)
        if isinstance(raw, dict):
            return pd.json_normalize(raw)
        raise ValueError(f"Cannot convert to DataFrame: {type(raw)}")

    def fetch_paginated(self, url, page_param='page', per_page_param='per_page', per_page=100, data_key='data', max_pages=100):
        all_frames = []
        for page in range(1, max_pages + 1):
            params = {page_param: page, per_page_param: per_page}
            raw = self.get(url, params=params)
            items = raw.get(data_key, []) if isinstance(raw, dict) else raw
            if not items:
                break
            all_frames.append(pd.DataFrame(items))
            if isinstance(raw, dict) and len(items) < per_page:
                break
        return pd.concat(all_frames, ignore_index=True) if all_frames else pd.DataFrame()

    def close(self):
        self.session.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--data-key', default=None)
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    loader = APILoader()
    try:
        df = loader.fetch_json_to_df(args.url, data_key=args.data_key)
        if args.output:
            df.to_csv(args.output, index=False, encoding='utf-8-sig')
        else:
            print(df.to_string(max_rows=30))
    finally:
        loader.close()


if __name__ == "__main__":
    main()
