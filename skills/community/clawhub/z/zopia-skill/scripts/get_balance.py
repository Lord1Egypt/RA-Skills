#!/usr/bin/env python3
"""查询 Zopia 账户余额。

用法:
    python get_balance.py

返回:
    {accounts: [...], summary: {totalBalance, totalHeld, totalAvailable}}
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import get_balance, print_json


def main() -> None:
    result = get_balance()
    print_json(result)


if __name__ == "__main__":
    main()
