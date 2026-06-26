#!/usr/bin/env python3
"""
Initiate SAS key verification from Clawd → Beeper Desktop.

Workaround: Beeper's hungryserv returns sync responses with a partial
shape that nio's jsonschema validator doesn't like (floods warnings).
So we avoid sync_forever and poll manually with short syncs.

Usage:
    ~/.venvs/beeper/bin/python verify_interactive.py [--device-id XXX]
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Silence nio's schema warnings BEFORE importing nio
logging.basicConfig(level=logging.ERROR)
logging.getLogger("nio").setLevel(logging.ERROR)
logging.getLogger("nio.responses").setLevel(logging.ERROR)

from nio import (
    KeyVerificationCancel,
    KeyVerificationEvent,
    KeyVerificationKey,
    KeyVerificationMac,
    KeyVerificationStart,
    ToDeviceError,
)
from nio_client import make_client


async def pick_target_device(client, override):
    if override:
        return override
    resp = await client.devices()
    if not hasattr(resp, "devices"):
        print(f"Could not list devices: {resp}", file=sys.stderr)
        return None
    others = [d for d in resp.devices if d.id != client.device_id]
    if not others:
        print("No other device found.", file=sys.stderr)
        return None
    beeper = [d for d in others if "beeper desktop" in (d.display_name or "").lower()]
    target = beeper[0] if beeper else others[0]
    print(f"Target device: {target.id}  ({target.display_name!r})")
    return target.id


async def handle_event(client, event, state):
    if isinstance(event, KeyVerificationStart):
        print(f"▶ Got KeyVerificationStart from {event.sender} ({event.from_device})")
        if "emoji" not in event.short_authentication_string:
            print("  ⚠ No emoji SAS support on other side.")
            await client.cancel_key_verification(event.transaction_id, reject=True)
            return
        r = await client.accept_key_verification(event.transaction_id)
        if isinstance(r, ToDeviceError):
            print(f"  ❌ accept: {r}")

    elif isinstance(event, KeyVerificationKey):
        sas = client.key_verifications.get(event.transaction_id)
        if sas is None:
            return
        emoji = sas.get_emoji()
        print("\n" + "=" * 60)
        print("COMPARE THESE EMOJIS with those on Beeper Desktop:")
        for e, name in emoji:
            print(f"   {e}  {name}")
        print("=" * 60)
        state["emoji_shown"] = True

    elif isinstance(event, KeyVerificationMac):
        sas = client.key_verifications.get(event.transaction_id)
        if sas is None:
            return
        try:
            mac_msg = sas.get_mac()
        except Exception as e:
            print(f"❌ get_mac failed: {e}")
            return
        await client.to_device(mac_msg)
        print("\n🎉 VERIFICATION COMPLETE — our device is now TRUSTED.")
        state["done"] = True

    elif isinstance(event, KeyVerificationCancel):
        print(f"✗ Cancelled by other side: {event.reason}")
        state["done"] = True


async def main(args) -> int:
    client = await make_client()
    await client.sync(timeout=6000, full_state=False)
    if client.should_query_keys:
        await client.keys_query()

    target_id = await pick_target_device(client, args.device_id)
    if target_id is None:
        await client.close()
        return 1

    our_user = client.user_id

    # Ensure we have device keys for target
    try:
        target_device = client.device_store[our_user][target_id]
    except KeyError:
        print(f"Device {target_id} not in device_store. Querying keys…")
        await client.keys_query()
        target_device = client.device_store[our_user][target_id]

    print(f"\nSending verification request to {our_user}:{target_id}…")
    resp = await client.start_key_verification(target_device)
    if isinstance(resp, ToDeviceError):
        print(f"❌ start_key_verification failed: {resp}")
        await client.close()
        return 1

    print("✓ Sent. A prompt should appear on Beeper Desktop — accept it.")
    print("  (polling for events…)\n")

    state = {"done": False, "emoji_shown": False, "confirmed": False}
    client.add_to_device_callback(
        lambda ev: asyncio.create_task(handle_event(client, ev, state)),
        (KeyVerificationEvent,),
    )

    # Poll loop — short syncs
    try:
        while not state["done"]:
            try:
                await client.sync(timeout=3000, full_state=False)
            except Exception as e:
                print(f"(sync warning: {e})", file=sys.stderr)

            # Once emojis are shown, prompt for confirmation (only once)
            if state["emoji_shown"] and not state["confirmed"]:
                loop = asyncio.get_event_loop()
                ans = await loop.run_in_executor(
                    None, input, "Do the emojis match on Beeper Desktop? [yes/no] "
                )
                if ans.strip().lower().startswith("y"):
                    # Find the active tx
                    for tx_id in list(client.key_verifications.keys()):
                        r = await client.confirm_short_auth_string(tx_id)
                        if isinstance(r, ToDeviceError):
                            print(f"❌ confirm: {r}")
                        else:
                            print("✓ Confirmed on our side. Waiting for MAC…")
                else:
                    for tx_id in list(client.key_verifications.keys()):
                        await client.cancel_key_verification(tx_id, reject=True)
                    print("✗ Cancelled.")
                    state["done"] = True
                state["confirmed"] = True
    except KeyboardInterrupt:
        print("\nCancelled.")
    finally:
        await client.close()
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--device-id")
    args = p.parse_args()
    sys.exit(asyncio.run(main(args)))
