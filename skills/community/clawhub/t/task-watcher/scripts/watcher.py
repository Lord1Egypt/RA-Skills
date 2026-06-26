#!/usr/bin/env python3
"""
Task Watcher — Cron Entry Point

Checks all active tasks for state changes and sends notifications.

Usage (standalone):
    python3 watcher.py --once

Cron setup (every 3 minutes):
    */3 * * * * cd /path/to/task-watcher-skill && python3 scripts/watcher.py --once >> watcher.log 2>&1
"""

import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from bus import create_default_bus


def setup_logging():
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('watcher')


def run_watcher(once=False):
    logger = setup_logging()

    logger.info("=" * 50)
    logger.info("Task Watcher Starting")
    logger.info(f"Time: {datetime.now().isoformat()}")
    logger.info("=" * 50)

    try:
        bus = create_default_bus()

        health = bus.get_health()
        logger.info(f"Health: {health['status']}")
        logger.info(f"Active tasks: {health['active_tasks']}")

        stats = bus.run_cycle()
        logger.info(f"Cycle complete: {stats}")

        if stats['errors'] > 0:
            logger.error(f"Encountered {stats['errors']} errors during cycle")
        if stats['tasks_escalated'] > 0:
            logger.warning(f"{stats['tasks_escalated']} tasks escalated")

        return 0 if stats['errors'] == 0 else 1

    except Exception as e:
        logger.exception(f"Watcher failed: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Task Watcher")
    parser.add_argument("--once", action="store_true", help="Run once and exit (for cron)")
    args = parser.parse_args()
    return run_watcher(once=args.once)


if __name__ == "__main__":
    sys.exit(main())
