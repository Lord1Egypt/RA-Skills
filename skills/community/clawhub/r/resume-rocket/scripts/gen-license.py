#!/usr/bin/env python
"""激活码生成器（管理员用）

用法:
    python scripts/gen-license.py {S|M|P} YYYYMMDD

例:
    python scripts/gen-license.py M 20261231
    -> M-20261231-a81cb97e
"""
import hashlib
import os
import sys


def gen(tier: str, expire: str, secret: str = None) -> str:
    secret = secret or os.getenv("RR_LICENSE_SECRET", "openclaw-resume-rocket-2026")
    if tier not in ("S", "M", "P"):
        raise ValueError(f"tier must be S/M/P, got {tier}")
    if len(expire) != 8 or not expire.isdigit():
        raise ValueError(f"expire must be YYYYMMDD, got {expire}")
    h = hashlib.sha256(f"{secret}|{tier}|{expire}".encode()).hexdigest()[:8]
    return f"{tier}-{expire}-{h}"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    print(gen(sys.argv[1], sys.argv[2]))
