#!/usr/bin/env python3
"""
Discover Xiaomi devices on your account.
Usage: python3 discover_devices.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "data" / "xiaoai_config.json"


async def main():
    try:
        from miservice import MiAccount, MiNAService
    except ImportError:
        print("miservice not installed. Run: pip install miservice")
        sys.exit(1)

    config = {}
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)

    mi_user = config.get("mi_user") or os.environ.get("MI_USER", "")
    mi_pass = config.get("mi_pass") or os.environ.get("MI_PASS", "")

    if not mi_user or not mi_pass:
        print("Set MI_USER and MI_PASS in data/xiaoai_config.json or environment")
        sys.exit(1)

    account = MiAccount(
        session=None,
        username=mi_user,
        password=mi_pass,
        token_path=str(Path(__file__).parent.parent / "data" / ".mi_token"),
    )

    mina_service = MiNAService(account)
    devices = await mina_service.device_list()

    print(f"\nFound {len(devices)} device(s):\n")
    for d in devices:
        print(f"  Name:     {d.get('name', 'unknown')}")
        print(f"  Alias:    {d.get('alias', '-')}")
        print(f"  DeviceID: {d.get('deviceID', '-')}")
        print(f"  Hardware: {d.get('hardware', '-')}")
        print()

    print("Copy the DeviceID of your 小爱音箱 into data/xiaoai_config.json")


if __name__ == "__main__":
    asyncio.run(main())
