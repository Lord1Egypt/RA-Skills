#!/usr/bin/env python3
"""Webhook receiver for WHOOP real-time event notifications."""

import json
import os
import sys
import time
from flask import Flask, request, jsonify

from whoop_client import WhoopClient, DailyLimitExceeded
from formatters import format_recovery, format_sleep, format_workout

app = Flask(__name__)
client = None

CONFIG_PATH = os.path.expanduser("~/.whoop/config.json")
WEBHOOK_HEARTBEAT_PATH = os.path.expanduser("~/.whoop/webhook_heartbeat")


def _load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def _touch_heartbeat():
    """Update heartbeat file so auto_sync knows webhook is alive."""
    os.makedirs(os.path.dirname(WEBHOOK_HEARTBEAT_PATH), exist_ok=True)
    with open(WEBHOOK_HEARTBEAT_PATH, "w") as f:
        f.write(str(time.time()))


def get_client():
    global client
    if client is None:
        client = WhoopClient()
    return client


@app.route("/whoop/webhook", methods=["POST"])
def webhook():
    """Handle WHOOP webhook events.

    WHOOP sends event notifications (not full data).
    On receipt, we fetch the complete data via the API.
    Respects push_* config flags and updates heartbeat.
    """
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "invalid payload"}), 400

    event_type = payload.get("type", "")
    user_id = payload.get("user_id")
    resource_id = payload.get("id")
    trace_id = payload.get("trace_id")

    log_prefix = f"[webhook] {event_type} trace={trace_id}"
    _touch_heartbeat()

    config = _load_config()

    try:
        c = get_client()

        if event_type == "recovery.updated":
            data = c.get_recovery_for_cycle(resource_id)
            if config.get("push_recovery", True):
                output = format_recovery(data)
                print(output, flush=True)
            else:
                print(f"{log_prefix} received (push_recovery=off, stored only)", flush=True)

        elif event_type == "sleep.updated":
            data = c.get_sleep_by_id(resource_id)
            if config.get("push_sleep", True):
                output = format_sleep(data)
                print(output, flush=True)
            else:
                print(f"{log_prefix} received (push_sleep=off, stored only)", flush=True)

        elif event_type == "workout.updated":
            data = c.get_workout_by_id(resource_id)
            if config.get("push_workout", True):
                output = format_workout(data)
                print(output, flush=True)
            else:
                print(f"{log_prefix} received (push_workout=off, stored only)", flush=True)

        elif event_type in ("recovery.deleted", "sleep.deleted", "workout.deleted"):
            print(f"{log_prefix} resource_id={resource_id} — deleted", flush=True)

        else:
            print(f"{log_prefix} unknown event type, ignoring", flush=True)

    except DailyLimitExceeded as e:
        print(f"{log_prefix} {e}", flush=True)
        return jsonify({"error": "daily API limit reached"}), 429
    except Exception as e:
        print(f"{log_prefix} error: {e}", flush=True)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


def main():
    port = 9876
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--port" and i + 1 < len(args):
            port = int(args[i + 1])

    # Load config port if not overridden
    config_path = os.path.expanduser("~/.whoop/config.json")
    if port == 9876 and os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
        port = config.get("webhook_port", 9876)

    print(f"WHOOP webhook server starting on port {port}")
    print(f"Endpoint: http://localhost:{port}/whoop/webhook")
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
