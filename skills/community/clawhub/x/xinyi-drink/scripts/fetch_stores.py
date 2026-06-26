#!/usr/bin/env python3
from __future__ import annotations

import sys

from build_response import render_store_query_unavailable, render_stores_section
from skill_config import load_config
from skill_http import SkillHttpError, build_url, fetch_json, make_debug_logger


debug_log = make_debug_logger("fetch_stores")


def main() -> int:
    debug_enabled = "--debug" in sys.argv[1:]
    config = load_config()
    url = build_url(config["apiBaseUrl"], "/skill/xinyi/stores")
    debug_log(debug_enabled, f"fetching stores from {url}")

    try:
        payload = fetch_json(url, config["timeoutSeconds"])
    except SkillHttpError as exc:
        sys.stdout.write(render_store_query_unavailable(exc))
        return 0

    sys.stdout.write(render_stores_section(payload.get("data", {}).get("stores", [])))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
