"""
TuyaDeviceMQClient — Python client for Tuya device message subscription.

The WebSocket URI is auto-detected from the API key prefix (same key as
TUYA_API_KEY used by tuya_api.py), matching all 7 data centers.

Usage:
    import os, sys
    sys.path.insert(0, "<baseDir>/scripts")
    from tuya_device_mq_client import TuyaDeviceMQClient

    client = TuyaDeviceMQClient(api_key=os.environ["TUYA_API_KEY"])

    @client.on_property_change
    async def handle_property(device_id, properties):
        for prop in properties:
            print(f"{device_id}: {prop['code']} = {prop['value']}")

    @client.on_online_status
    async def handle_status(device_id, status, timestamp):
        print(f"{device_id} is now {status}")

    await client.connect()

Dependencies:
    pip install websockets
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Callable, Coroutine, Optional

try:
    import websockets
except ImportError:
    raise ImportError("'websockets' package is required. Install with: pip install websockets")

logger = logging.getLogger("tuya-mq-client")

# Type aliases
PropertyChangeHandler = Callable[[str, list[dict[str, Any]]], Coroutine]
OnlineStatusHandler = Callable[[str, str, int], Coroutine]
RawMessageHandler = Callable[[dict[str, Any]], Coroutine]

_FATAL_CLOSE_CODES = {1002, 1003, 1008, 1011}

# API key prefix → WebSocket URI mapping
_PREFIX_TO_WS_URI = {
    "AY": "wss://wsmsgs.tuyacn.com",       # China Data Center
    "AZ": "wss://wsmsgs.iot-wus.com",      # US West Data Center
    "EU": "wss://wsmsgs.iot-eu.com",       # Central Europe Data Center
    "IN": "wss://wsmsgs.iot-ap.com",       # India Data Center
    "UE": "wss://wsmsgs.iot-eus.com",      # US East Data Center
    "WE": "wss://wsmsgs.iot-weu.com",      # Western Europe Data Center
    "SG": "wss://wsmsgs.iot-sea.com",      # Singapore Data Center
}


def _resolve_ws_uri(api_key: str) -> str:
    """Resolve WebSocket URI from the API key prefix.

    API key format: sk-<PREFIX><rest>
    Example: sk-AY12c7ee31ae19... → prefix AY → China
    """
    key = api_key
    if key.startswith("sk-"):
        key = key[3:]
    prefix = key[:2].upper()
    if prefix in _PREFIX_TO_WS_URI:
        return _PREFIX_TO_WS_URI[prefix]
    raise ValueError(
        f"WebSocket message subscription is not yet supported for API key "
        f"prefix '{prefix}'. Currently supported: "
        f"{', '.join(sorted(_PREFIX_TO_WS_URI.keys()))} (China). "
        f"You can pass uri explicitly to override."
    )


class TuyaDeviceMQClient:
    """
    WebSocket client for subscribing to Tuya device events.

    Supports two event types:
      - devicePropertyChange: device dp property updates
      - onlineStatusChange: device online/offline transitions

    Args:
        api_key:    API Key for authentication (same TUYA_API_KEY used by TuyaAPI).
                    Defaults to the TUYA_API_KEY environment variable.
        uri:        WebSocket server URI. Auto-detected from the API key prefix
                    if not provided. Pass explicitly to override.
        device_ids: Optional list of device IDs to filter; None means all devices.
    """

    def __init__(self, api_key: str = None, uri: str = None,
                 device_ids: Optional[list[str]] = None):
        if api_key is None:
            api_key = os.environ.get("TUYA_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing API key. Set environment variable TUYA_API_KEY, "
                "or pass api_key argument."
            )
        if uri is None:
            uri = _resolve_ws_uri(api_key)
        self._uri = uri
        self._api_key = api_key
        self._device_ids = set(device_ids) if device_ids else None
        self._property_handlers: list[PropertyChangeHandler] = []
        self._online_status_handlers: list[OnlineStatusHandler] = []
        self._raw_handlers: list[RawMessageHandler] = []
        self._running = False

    # -- Decorator-style handler registration --

    def on_property_change(self, func: PropertyChangeHandler) -> PropertyChangeHandler:
        """Register a handler for devicePropertyChange events.

        The handler receives (device_id: str, properties: list[dict]).
        Each property dict has keys: code, value, time.
        """
        self._property_handlers.append(func)
        return func

    def on_online_status(self, func: OnlineStatusHandler) -> OnlineStatusHandler:
        """Register a handler for onlineStatusChange events.

        The handler receives (device_id: str, status: str, timestamp_ms: int).
        status is "online" or "offline".
        """
        self._online_status_handlers.append(func)
        return func

    def on_raw_message(self, func: RawMessageHandler) -> RawMessageHandler:
        """Register a handler for all raw messages (before filtering)."""
        self._raw_handlers.append(func)
        return func

    # -- Connection --

    async def connect(self):
        """Connect to the WebSocket and start listening for events.

        Automatically reconnects on transient failures.
        Stops on fatal close codes or server error messages.
        """
        headers = {"Authorization": self._api_key}
        self._running = True
        logger.info("Connecting to %s ...", self._uri)

        try:
            async for websocket in websockets.connect(self._uri, additional_headers=headers):
                if not self._running:
                    break
                try:
                    logger.info("Connected — listening for device events")
                    async for message in websocket:
                        if not self._running:
                            await websocket.close(1000, "Client stopped")
                            return

                        try:
                            data = json.loads(message)
                        except json.JSONDecodeError:
                            logger.warning("Non-JSON message: %s", message)
                            continue

                        if self._is_error(data):
                            logger.error("Server error: %s", data)
                            await websocket.close(1000, "Received error")
                            return

                        await self._dispatch(data)

                except websockets.ConnectionClosedError as e:
                    if e.rcvd and e.rcvd.code in _FATAL_CLOSE_CODES:
                        logger.error("Fatal close (code=%d, reason=%s). Stopping.",
                                     e.rcvd.code, e.rcvd.reason or "unknown")
                        return
                    logger.warning("Connection lost: %s. Reconnecting...", e)
                    continue
                except websockets.ConnectionClosedOK:
                    logger.info("Connection closed normally.")
                    return

        except websockets.InvalidStatusCode as e:
            logger.error("HTTP %s from server. Stopping.", e.status_code)
        except OSError as e:
            logger.error("Cannot reach server: %s. Stopping.", e)
        finally:
            self._running = False

    def stop(self):
        """Signal the client to disconnect gracefully."""
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    # -- Internal helpers --

    async def _dispatch(self, data: dict):
        """Route a parsed message to the appropriate handlers."""
        # Fire raw handlers first
        for handler in self._raw_handlers:
            await handler(data)

        event_type = data.get("eventType")
        event_data = data.get("data", {})
        dev_id = event_data.get("devId")

        # Apply device filter
        if self._device_ids and dev_id not in self._device_ids:
            return

        if event_type == "devicePropertyChange":
            status_list = event_data.get("status", [])
            for handler in self._property_handlers:
                await handler(dev_id, status_list)

        elif event_type == "onlineStatusChange":
            status = event_data.get("status", "unknown")
            timestamp = event_data.get("time", 0)
            for handler in self._online_status_handlers:
                await handler(dev_id, status, timestamp)

    @staticmethod
    def _is_error(data: dict) -> bool:
        if data.get("error"):
            return True
        if data.get("errorCode") and data.get("errorCode") != "SUCCESS":
            return True
        if data.get("errorMsg"):
            return True
        if data.get("success") is False:
            return True
        return False

    @staticmethod
    def format_timestamp(ts_ms: int) -> str:
        """Convert a millisecond timestamp to a readable datetime string."""
        try:
            return datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, OSError):
            return str(ts_ms)
