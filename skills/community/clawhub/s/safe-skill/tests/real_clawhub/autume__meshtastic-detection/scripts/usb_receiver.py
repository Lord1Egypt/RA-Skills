#!/usr/bin/env python3
"""
Meshtastic USB Receiver Daemon

Continuously listens for DETECTION_SENSOR_APP messages from a Meshtastic device
via USB serial. Only detection sensor events (GPIO trigger) are captured and stored
as JSONL records. Other message types are ignored.

Run as a systemd service or directly:
    python usb_receiver.py
    python usb_receiver.py --port /dev/cu.usbmodem10B41DD29D981
    python usb_receiver.py --data-dir ./data
"""

import json
import time
import logging
import argparse
import signal
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("usb_receiver")

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

DEFAULT_SERIAL_PORT = os.environ.get(
    "MESH_SERIAL_PORT",
    "/dev/cu.usbmodem10B41DD29D981" if sys.platform == "darwin" else "/dev/ttyACM0",
)
DEFAULT_DATA_DIR = os.environ.get("MESH_DATA_DIR", str(Path(__file__).resolve().parent.parent / "data"))
RECONNECT_DELAY_SECONDS = 5
MAX_RECONNECT_DELAY_SECONDS = 60
MAX_JSONL_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB — rotate when exceeded
MAX_ARCHIVE_FILES = 2  # keep sensor_data.jsonl.1 and .2

# ═══════════════════════════════════════════════════════════════
# STORAGE
# ═══════════════════════════════════════════════════════════════


class DataStore:
    """Handles JSONL append and latest.json maintenance."""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.jsonl_path = self.data_dir / "sensor_data.jsonl"
        self.latest_path = self.data_dir / "latest.json"
        self._latest_cache: dict = self._load_latest()

    def _load_latest(self) -> dict:
        try:
            if self.latest_path.exists():
                return json.loads(self.latest_path.read_text())
        except Exception as e:
            log.warning(f"Could not load latest.json: {e}")
        return {}

    def append(self, record: dict) -> None:
        """Append a detection record to the JSONL file and update latest.json."""
        self._rotate_if_needed()

        try:
            with open(self.jsonl_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            log.error(f"Failed to write JSONL: {e}")
            return

        detection_type = record.get("data", {}).get("type", "unknown")
        self._latest_cache[detection_type] = {
            "received_at": record.get("received_at"),
            "sender": record.get("sender"),
            "data": record.get("data"),
        }
        try:
            self.latest_path.write_text(
                json.dumps(self._latest_cache, indent=2, ensure_ascii=False)
            )
        except Exception as e:
            log.error(f"Failed to write latest.json: {e}")

    def _rotate_if_needed(self) -> None:
        """Rotate sensor_data.jsonl when it exceeds MAX_JSONL_SIZE_BYTES.

        Archives: sensor_data.jsonl -> .1 -> .2 (oldest dropped).
        Resets event_monitor state so it re-reads from offset 0.
        """
        try:
            if not self.jsonl_path.exists():
                return
            if self.jsonl_path.stat().st_size < MAX_JSONL_SIZE_BYTES:
                return
        except OSError:
            return

        log.info(
            f"Rotating {self.jsonl_path.name} "
            f"(size: {self.jsonl_path.stat().st_size / 1024 / 1024:.1f} MB)"
        )

        for i in range(MAX_ARCHIVE_FILES, 0, -1):
            src = self.jsonl_path.with_suffix(f".jsonl.{i}" if i > 0 else ".jsonl")
            if i == MAX_ARCHIVE_FILES:
                src = self.jsonl_path.with_suffix(f".jsonl.{i}")
                if src.exists():
                    src.unlink()
            else:
                src = self.jsonl_path.with_suffix(f".jsonl.{i}")
                dst = self.jsonl_path.with_suffix(f".jsonl.{i + 1}")
                if src.exists():
                    src.rename(dst)

        self.jsonl_path.rename(self.jsonl_path.with_suffix(".jsonl.1"))

        # Reset event_monitor state so it starts from offset 0 on the new file
        monitor_state = self.data_dir / "monitor_state.json"
        if monitor_state.exists():
            try:
                monitor_state.write_text('{"last_offset": 0, "seen_hashes": []}')
                log.info("Reset monitor_state.json after rotation")
            except OSError:
                pass

    def record_count(self) -> int:
        try:
            if self.jsonl_path.exists():
                with open(self.jsonl_path, "r") as f:
                    return sum(1 for _ in f)
        except Exception:
            pass
        return 0


# ═══════════════════════════════════════════════════════════════
# RECEIVER
# ═══════════════════════════════════════════════════════════════


class MeshReceiver:
    """Connects to Meshtastic USB device, receives and stores detection data."""

    def __init__(self, serial_port: str, data_store: DataStore):
        self.serial_port = serial_port
        self.store = data_store
        self.interface = None
        self._running = True
        self._message_count = 0

    ACCEPTED_PORTNUMS = {
        "DETECTION_SENSOR_APP",
    }

    def on_receive(self, packet, interface):
        """Callback for incoming Meshtastic messages."""
        try:
            decoded = packet.get("decoded", {})
            portnum = decoded.get("portnum", "")
            sender = packet.get("fromId", "unknown")
            channel = packet.get("channel", 0)

            log.debug(
                f"Packet from {sender} ch{channel} portnum={portnum} "
                f"keys={list(decoded.keys())}"
            )

            if portnum not in self.ACCEPTED_PORTNUMS:
                return

            text = decoded.get("text", "") or decoded.get("payload", b"").decode(
                "utf-8", errors="replace"
            )
            if not text:
                log.debug(f"Empty payload from {sender} portnum={portnum}, skipping")
                return

            log.info(f"[{portnum}] from {sender} (ch{channel}): {text[:120]}")

            record = self._parse_message(text, sender, channel, portnum)
            if record:
                self.store.append(record)
                self._message_count += 1
                log.info(
                    f"Stored: type={record['data'].get('type', '?')}, "
                    f"portnum={portnum} (total: {self._message_count})"
                )

        except Exception as e:
            log.error(f"Error processing packet: {e}", exc_info=True)

    def _parse_message(
        self, text: str, sender: str, channel: int, portnum: str
    ) -> dict | None:
        """Parse a text message into a detection record.

        Tries to parse as JSON first. If that fails, stores the raw text
        with the portnum so no data is lost.
        """
        received_at = datetime.now(timezone.utc).isoformat()

        try:
            data = json.loads(text)
            if isinstance(data, dict):
                return {
                    "received_at": received_at,
                    "sender": sender,
                    "channel": f"ch{channel}",
                    "portnum": portnum,
                    "data": data,
                }
        except (json.JSONDecodeError, TypeError):
            pass

        return {
            "received_at": received_at,
            "sender": sender,
            "channel": f"ch{channel}",
            "portnum": portnum,
            "data": {
                "type": "detection",
                "text": text,
            },
        }

    def connect(self) -> bool:
        """Connect to the Meshtastic device via USB serial."""
        try:
            import meshtastic
            import meshtastic.serial_interface
            from pubsub import pub

            log.info(f"Connecting to {self.serial_port}...")
            self.interface = meshtastic.serial_interface.SerialInterface(
                devPath=self.serial_port
            )
            pub.subscribe(self.on_receive, "meshtastic.receive")

            my_info = self.interface.getMyNodeInfo()
            user = my_info.get("user", {}) if my_info else {}
            log.info(
                f"Connected: {user.get('longName', 'unknown')} "
                f"({user.get('id', '?')})"
            )
            return True

        except Exception as e:
            log.error(f"Connection failed: {e}")
            self.interface = None
            return False

    def disconnect(self):
        """Close the Meshtastic interface."""
        if self.interface:
            try:
                self.interface.close()
            except Exception:
                pass
            self.interface = None

    def run(self):
        """Main loop with auto-reconnection."""
        delay = RECONNECT_DELAY_SECONDS

        while self._running:
            if self.connect():
                delay = RECONNECT_DELAY_SECONDS
                log.info(
                    f"Receiver running. Data dir: {self.store.data_dir} | "
                    f"Existing records: {self.store.record_count()}"
                )
                try:
                    while self._running:
                        time.sleep(1)
                except KeyboardInterrupt:
                    break
                finally:
                    self.disconnect()
            else:
                log.warning(f"Retrying in {delay}s...")
                time.sleep(delay)
                delay = min(delay * 2, MAX_RECONNECT_DELAY_SECONDS)

    def stop(self):
        self._running = False
        self.disconnect()


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="Meshtastic USB Receiver Daemon")
    parser.add_argument(
        "--port", default=DEFAULT_SERIAL_PORT, help="Serial port path"
    )
    parser.add_argument(
        "--data-dir", default=DEFAULT_DATA_DIR, help="Data storage directory"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging (show all packets)"
    )
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    store = DataStore(args.data_dir)
    receiver = MeshReceiver(args.port, store)

    def shutdown(signum, frame):
        log.info("Shutdown signal received")
        receiver.stop()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    log.info("=" * 50)
    log.info("Meshtastic USB Receiver")
    log.info(f"  Serial port: {args.port}")
    log.info(f"  Data dir:    {args.data_dir}")
    log.info("=" * 50)

    receiver.run()
    log.info("Receiver stopped.")


if __name__ == "__main__":
    main()
