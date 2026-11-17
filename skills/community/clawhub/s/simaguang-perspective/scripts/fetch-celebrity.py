#!/usr/bin/env python3
"""Fetch the next public-figure image from Wikimedia Commons via image proxy.

Outputs `<state>/current.json` so the Simaguang analysis automation can use one
deterministic image per run. State dir = `$SIMAGUANG_STATE_DIR` or
`~/.cache/simaguang-celebrity/`（可丢弃缓存，不属于技能包，也不写入任何 Agent 全局配置目录）.
Images go through images.weserv.nl so no direct Commons hotlink is made.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
POOL = SKILL_DIR / "references" / "名人分析库.json"
_STATE_ROOT = (
    Path(os.environ["SIMAGUANG_STATE_DIR"]).expanduser()
    if os.environ.get("SIMAGUANG_STATE_DIR")
    else Path(os.environ.get("XDG_CACHE_HOME") or (Path.home() / ".cache"))
)
STATE_DIR = _STATE_ROOT / "simaguang-celebrity"
STATE = STATE_DIR / "state.json"
CURRENT = STATE_DIR / "current.json"


def load_pool():
    with POOL.open(encoding="utf-8") as f:
        return json.load(f)["people"]


def load_state():
    if STATE.exists():
        with STATE.open(encoding="utf-8") as f:
            return json.load(f)
    return {"used": []}


def save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with STATE.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def fetch(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": "CodexSkill/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    if not data:
        raise RuntimeError("empty response")
    out.write_bytes(data)


def main():
    people = load_pool()
    state = load_state()
    used = set(state["used"])
    person = next((p for p in people if p["name"] not in used), None)
    if person is None:
        used = set()
        person = people[0]
    if "--dry-run" in sys.argv:
        print(json.dumps({"next": person["name"], "used": sorted(used)}, ensure_ascii=False))
        return
    used.add(person["name"])
    state["used"] = sorted(used)
    save_state(state)

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    image_path = STATE_DIR / f"{slugify(person['name'])}.jpg"
    quoted = urllib.parse.quote(person["file"])
    url = (
        "https://images.weserv.nl/?url="
        f"commons.wikimedia.org/wiki/Special:FilePath/{quoted}&w=800"
    )
    fetch(url, image_path)

    current = {
        "name": person["name"],
        "image_path": str(image_path),
        "source_url": url,
        "commons_file": person["file"],
        "summary": person["summary"],
    }
    with CURRENT.open("w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    print(json.dumps(current, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
