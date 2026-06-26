#!/usr/bin/env python3
"""Check baseline prerequisites for a local workspace retrieval setup.

This script is intentionally lightweight and cross-platform:
- no network calls
- no package installation
- no mutation outside stdout
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
from typing import Any


def run(cmd: list[str]) -> tuple[bool, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        out = (proc.stdout or proc.stderr).strip()
        return proc.returncode == 0, out
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def parse_major_minor(text: str) -> tuple[int, int] | None:
    import re

    m = re.search(r"(\d+)\.(\d+)", text)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def check_python() -> dict[str, Any]:
    v = sys.version_info
    ok = (v.major, v.minor) >= (3, 10)
    return {
        "name": "python",
        "ok": ok,
        "version": f"{v.major}.{v.minor}.{v.micro}",
        "required": ">=3.10",
        "details": sys.executable,
    }


def check_node() -> dict[str, Any]:
    path = shutil.which("node")
    if not path:
        return {"name": "node", "ok": False, "required": ">=20", "details": "not found"}
    ok, out = run([path, "--version"])
    ver = out.strip()
    parsed = parse_major_minor(ver)
    return {
        "name": "node",
        "ok": ok and parsed is not None and parsed[0] >= 20,
        "version": ver,
        "required": ">=20",
        "details": path,
    }


def check_sqlite_cli() -> dict[str, Any]:
    path = shutil.which("sqlite3")
    if not path:
        return {"name": "sqlite3-cli", "ok": False, "required": "recommended", "details": "not found"}
    ok, out = run([path, "--version"])
    return {
        "name": "sqlite3-cli",
        "ok": ok,
        "version": out.split()[0] if out else None,
        "required": "recommended",
        "details": path,
    }


def check_python_sqlite() -> dict[str, Any]:
    version = sqlite3.sqlite_version
    con = sqlite3.connect(":memory:")
    fts5 = False
    try:
        con.execute("CREATE VIRTUAL TABLE t USING fts5(content)")
        fts5 = True
    except Exception:
        fts5 = False
    finally:
        con.close()
    parsed = parse_major_minor(version)
    ok = parsed is not None and parsed >= (3, 40) and fts5
    return {
        "name": "python-sqlite",
        "ok": ok,
        "version": version,
        "required": "SQLite >=3.40 with FTS5 preferred",
        "details": {"fts5": fts5},
    }


def check_ollama() -> dict[str, Any]:
    path = shutil.which("ollama")
    if not path:
        return {"name": "ollama", "ok": False, "required": "optional", "details": "not found"}
    ok, out = run([path, "--version"])
    return {
        "name": "ollama",
        "ok": ok,
        "version": out.splitlines()[0] if out else None,
        "required": "optional",
        "details": path,
    }


def recommendations(results: list[dict[str, Any]]) -> list[str]:
    by = {r["name"]: r for r in results}
    recs: list[str] = []
    if not by["python"]["ok"]:
        recs.append("Install Python 3.10+.")
    if not by["node"]["ok"]:
        recs.append("Install Node.js 20+ for agent-facing wrapper scripts.")
    if not by["python-sqlite"]["ok"]:
        recs.append("Use a newer SQLite build with FTS5 support, or a Python build linked against one.")
    if not by["sqlite3-cli"]["ok"]:
        recs.append("Install sqlite3 CLI for easier local inspection and debugging.")
    if not by["ollama"]["ok"]:
        recs.append("If you want fully local semantic retrieval, install Ollama or configure another local embedding service.")
    return recs


def main() -> None:
    parser = argparse.ArgumentParser(description="Check prerequisites for workspace-local-retrieval.")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    results = [
        check_python(),
        check_node(),
        check_sqlite_cli(),
        check_python_sqlite(),
        check_ollama(),
    ]
    payload = {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "results": results,
        "recommendations": recommendations(results),
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(f"Platform: {payload['platform']['system']} {payload['platform']['release']} ({payload['platform']['machine']})")
    for r in results:
        status = "OK" if r.get("ok") else "MISSING/WEAK"
        version = f" [{r['version']}]" if r.get("version") else ""
        print(f"- {r['name']}: {status}{version} :: required={r['required']} :: {r['details']}")
    if payload["recommendations"]:
        print("Recommendations:")
        for rec in payload["recommendations"]:
            print(f"- {rec}")


if __name__ == "__main__":
    main()
