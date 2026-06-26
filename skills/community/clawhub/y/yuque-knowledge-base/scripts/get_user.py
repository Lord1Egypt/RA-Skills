#!/usr/bin/env python3
"""Get current Yuque user info. Also useful for verifying API token.

Usage:
    python get_user.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    result = api_request("GET", "/api/v2/user")
    output_json(result)


if __name__ == "__main__":
    main()
