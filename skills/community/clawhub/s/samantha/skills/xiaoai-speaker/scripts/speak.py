#!/usr/bin/env python3
"""
Samantha → 小爱音箱 TTS
Usage: python3 speak.py "你到家了呀"
"""

import asyncio
import json
import os
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "data" / "xiaoai_config.json"


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {
        "mi_user": os.environ.get("MI_USER", ""),
        "mi_pass": os.environ.get("MI_PASS", ""),
        "device_name": os.environ.get("MI_DEVICE", "小爱音箱"),
        "use_command": False,
    }


async def get_device_id(mina_service, device_name):
    devices = await mina_service.device_list()
    for d in devices:
        if device_name in d.get("name", "") or device_name in d.get("alias", ""):
            return d["deviceID"]
    # fallback: return first device
    if devices:
        print(f"Device '{device_name}' not found, using: {devices[0].get('name')}")
        return devices[0]["deviceID"]
    raise ValueError("No Xiaomi speaker devices found")


async def xiaoai_speak(text: str, config: dict = None):
    try:
        from miservice import MiAccount, MiNAService
    except ImportError:
        print("miservice not installed. Run: pip install miservice")
        sys.exit(1)

    if config is None:
        config = load_config()

    if not config.get("mi_user") or not config.get("mi_pass"):
        print("Error: MI_USER and MI_PASS required in config or environment")
        sys.exit(1)

    account = MiAccount(
        session=None,
        username=config["mi_user"],
        password=config["mi_pass"],
        token_path=str(Path(__file__).parent.parent / "data" / ".mi_token"),
    )

    mina_service = MiNAService(account)

    device_id = config.get("device_id") or await get_device_id(
        mina_service, config.get("device_name", "小爱音箱")
    )

    if config.get("use_command") and config.get("mi_did"):
        from miservice import MiIOService, miio_command
        miio_service = MiIOService(account)
        cmd = config.get("tts_command", "5-1")
        await miio_command(miio_service, config["mi_did"], f"{cmd} {text}")
    else:
        await mina_service.text_to_speech(device_id, text)

    print(f"✓ 小爱说: {text}")


async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 speak.py '<text>'")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    await xiaoai_speak(text)


if __name__ == "__main__":
    asyncio.run(main())
