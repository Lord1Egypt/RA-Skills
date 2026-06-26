"""
scheduler.py
------------
APScheduler-based nightly pipeline for the superwise-drift-detection-skill.

Runs on a configurable cron schedule (default: 06:00 UTC daily).
  1. Fetches inference records from the model endpoint
  2. Ingests them into the Superwise inference dataset
  3. Checks drift via Superwise
  4. Sends a Telegram alert via skill.run()

Also exposes a Flask /run-check endpoint so OpenClaw can trigger a manual check
via HTTP GET (e.g., from a Telegram /drift_check command).

Deploy to Render (or any host) using render.yaml.
"""

import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask, jsonify

from skill import run as skill_run

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
scheduler = BackgroundScheduler()

CRON_HOUR = int(os.getenv("SCHEDULE_HOUR_UTC", "6"))
CRON_MINUTE = int(os.getenv("SCHEDULE_MINUTE_UTC", "0"))


def nightly_drift_check():
    """Scheduled job: run the full drift detection pipeline."""
    logger.info("[scheduler] Nightly drift check starting...")
    try:
        result = skill_run()
        logger.info(f"[scheduler] Done: {result}")
    except Exception as exc:
        logger.error(f"[scheduler] Pipeline failed: {exc}", exc_info=True)


@app.route("/run-check")
def run_check():
    """HTTP endpoint for OpenClaw to trigger a manual drift check."""
    logger.info("[scheduler] Manual /run-check triggered via HTTP")
    try:
        result = skill_run()
        return jsonify({"status": "ok", "result": result})
    except Exception as exc:
        logger.error(f"[scheduler] /run-check failed: {exc}", exc_info=True)
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    scheduler.add_job(
        nightly_drift_check,
        "cron",
        hour=CRON_HOUR,
        minute=CRON_MINUTE,
        id="drift_check",
    )
    scheduler.start()
    logger.info(
        f"[scheduler] Scheduled drift check at {CRON_HOUR:02d}:{CRON_MINUTE:02d} UTC daily"
    )

    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
