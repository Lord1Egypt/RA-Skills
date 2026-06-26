#!/usr/bin/env python3
"""Refresh local Swagger snapshot without third-party dependencies."""

from __future__ import annotations

import json
from pathlib import Path
import urllib.request

URL = "https://api.yuboto.com/swagger/v1/swagger.json"
OUT = Path(__file__).resolve().parents[1] / "references" / "swagger_v1.json"


def main() -> int:
    req = urllib.request.Request(URL, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()

    obj = json.loads(raw.decode("utf-8"))
    OUT.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {OUT}")
    print(f"[INFO] paths={len(obj.get('paths', {}))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
