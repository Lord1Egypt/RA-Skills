#!/usr/bin/env python3
"""
RealBrowser by Ceki — Python quickstart.

Rent a real Chrome from the marketplace, navigate, capture screenshot, stop.

Requirements:
    pip install ceki-sdk

Env:
    CEKI_API_KEY — your API key from https://ceki.me dashboard
"""

import asyncio
import os
from pathlib import Path

from ceki_sdk import connect, ConnectOptions


async def main():
    token = os.environ.get("CEKI_API_KEY")
    if not token:
        raise SystemExit("Set CEKI_API_KEY env var (get one at https://ceki.me)")

    opts = ConnectOptions(
        relay_url="wss://browser.ceki.me/ws/agent",
        api_url="https://api.ceki.me",
        chat_url="https://chat.ceki.me/api/chat",
    )
    client = await connect(token, opts)

    # discover available marketplace browsers
    options = await client.search({})
    if not options:
        print("No browsers online. Try again in a moment.")
        await client.close()
        return

    schedule_id = options[0].schedule_id
    print(f"Renting browser schedule_id={schedule_id}...")

    browser = await client.rent(schedule_id, human="natural")
    try:
        await browser.navigate("https://example.com")

        png = await browser.screenshot(format="png")
        out = Path("/tmp/ceki_quickstart.png")
        out.write_bytes(png)
        print(f"Screenshot saved: {out}")

        snap = await browser.snapshot()
        print(f"Snapshot ts: {snap.ts}, chat messages: {len(snap.chat)}")

    finally:
        await browser.close()  # release rental, settle billing
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
