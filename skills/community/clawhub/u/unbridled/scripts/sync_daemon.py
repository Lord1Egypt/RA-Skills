#!/usr/bin/env python3
"""
Long-running Matrix sync for Beeper.

Purpose: accumulate Megolm group sessions for incoming messages, so the
collect_beeper_daily.py script (and on-demand reads) can decrypt chats
where Clawd wasn't the sender.

This daemon:
  - Loads the Olm store from ~/.local/share/clawd-matrix/
  - Runs `sync_forever` against the Beeper hungryserv
  - Automatically downloads and stores inbound room keys
  - Does NOT send messages — pure sync/read side

Meant to be supervised by systemd user:
  systemctl --user enable --now clawd-beeper-sync.service
"""
from __future__ import annotations

import asyncio
import logging
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Calm the logs before importing nio
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logging.getLogger("nio").setLevel(logging.WARNING)
logging.getLogger("nio.responses").setLevel(logging.ERROR)  # schema warnings
logging.getLogger("nio.rooms").setLevel(logging.ERROR)
logging.getLogger("nio.crypto").setLevel(logging.ERROR)
logging.getLogger("peewee").setLevel(logging.ERROR)

log = logging.getLogger("clawd-beeper-sync")
log.setLevel(logging.INFO)

from nio_client import make_client  # noqa: E402


async def run() -> int:
    log.info("starting Beeper sync daemon")
    client = await make_client()
    log.info(f"device: {client.device_id}  user: {client.user_id}")
    log.info(f"store:  ~/.local/share/clawd-matrix/ (e2ee enabled: {client.olm is not None})")

    stop = asyncio.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_event_loop().add_signal_handler(sig, stop.set)

    async def sync_loop():
        backoff = 2
        while not stop.is_set():
            try:
                # sync_forever handles its own loop internally; when it returns
                # (disconnect/error), we restart with backoff.
                await client.sync_forever(
                    timeout=30000,
                    loop_sleep_time=1000,
                    full_state=False,
                )
                backoff = 2  # reset after clean exit (unlikely)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                log.warning(f"sync_forever crashed: {e!r} — retry in {backoff}s")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 300)

    loop_task = asyncio.create_task(sync_loop())
    await stop.wait()
    log.info("stop signal received, shutting down")
    loop_task.cancel()
    try:
        await loop_task
    except asyncio.CancelledError:
        pass
    await client.close()
    log.info("bye")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
