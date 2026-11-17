#!/usr/bin/env python3
"""lib_vibo.py — thin Python client for the ViBo CLI (vibo_use.py).

The vibo-selfdeed skill uses ONLY this client to talk to memory:
add / find / usage / link / stats. The core (vibo/*.so) is not duplicated.

Notes (from acceptance review):
- vibo_use.py lookup: VIBO_CLI env → PATH → next to the skill → walk up (3 levels)
- interpreter: python3.11 (core .so) → python3
- find parses the real CLI output: "• [L1] label: content"

Usage:
    from lib_vibo import ViBo
    v = ViBo()
    v.find("project architecture")
    v.add("lesson", "do not use Y")
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


class ViBoError(RuntimeError):
    """Error while talking to the ViBo CLI."""


def _find_cli() -> str:
    """Find vibo_use.py: VIBO_CLI → PATH → next to the skill → walk up 3 levels.

    Security: VIBO_CLI is accepted only if it is an existing .py file
    (not an executable script/binary) — protects against path substitution.
    """
    env = os.environ.get("VIBO_CLI")
    if env:
        p = Path(env).expanduser()
        if p.is_file() and p.suffix == ".py":
            return str(p.resolve())
        raise ViBoError(
            f"VIBO_CLI must point to a .py file: {env!r} — rejected."
        )
    w = shutil.which("vibo_use.py")
    if w:
        return w
    here = Path(__file__).resolve().parent
    # next to the skill and walk up to 3 levels
    for depth in range(4):
        cand = here / "vibo_use.py"
        if cand.is_file():
            return str(cand.resolve())
        here = here.parent
    raise ViBoError(
        "vibo_use.py not found.\n"
        "→ Get ViBo (free tier: 500 facts forever, no card): https://wwwvibo.com/download/skill\n"
        "→ or 2-day trial: https://wwwvibo.com/download/trial\n"
        "Then set: export VIBO_CLI=/path/to/vibo_use.py"
    )


def _find_python() -> str:
    """python3.11 (core .so) → python3."""
    for name in ("python3.11", "python3"):
        p = shutil.which(name)
        if p:
            return p
    return sys.executable


class MiniMemory:
    """Built-in DEMO memory (no ViBo CLI required).

    Lets the client feel the convenience right after installing the skill:
    facts are saved and found by words, up to DEMO_LIMIT facts. No semantic
    embeddings, no encryption, no L3 — the full engine needs the ViBo package.
    """

    DEMO_LIMIT = 100
    DEMO_URL = "https://wwwvibo.com/download/skill"

    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else Path(__file__).resolve().parent / "demo_memory.json"
        self._facts: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        try:
            if self.path.exists():
                self._facts = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            self._facts = {}

    def _save(self) -> None:
        try:
            if not getattr(self, "_warned", False):
                self._warned = True
                print("⚠️ DEMO mode: facts are written locally to "
                      f"{self.path} — local-only, no telemetry.", file=sys.stderr)
            self.path.write_text(json.dumps(self._facts, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception:
            pass

    def add(self, label: str, content: str = "", level: str = "L1", tags: list[str] | None = None) -> dict:
        if level != "L1" or (tags and "secret" in [t.lower() for t in tags]):
            return {"ok": False, "nodes": len(self._facts), "exit": 1,
                    "raw": "⛔ DEMO mode: L2/L3 and secrets need the full ViBo (https://wwwvibo.com/download/skill)."}
        used = len(self._facts)
        if used >= self.DEMO_LIMIT:
            return {"ok": False, "nodes": self.DEMO_LIMIT, "exit": 1,
                    "raw": (f"⛔ DEMO limit reached ({self.DEMO_LIMIT} facts) — you liked it, time to go full.\n"
                            f"With a subscription ($5/mo · $30/yr · $60 lifetime): unlimited memory, semantic search, "
                            f"L1/L2/L3 encryption, 96% web savings, living archive, privacy layer.\n"
                            f"Your facts are KEPT — enter a key and the limit is gone.\n"
                            f"Get a key: https://wwwvibo.com/pricing or @ViBomemorybot")}
        self._facts[label[:60]] = content
        self._save()
        added = len(self._facts)
        if added >= self.DEMO_LIMIT * 0.8:
            return {"ok": True, "nodes": added, "exit": 0,
                    "raw": (f"✅ Added: {label[:60]} ({added}/{self.DEMO_LIMIT} DEMO facts)\n"
                            f"⚡ {self.DEMO_LIMIT - added} facts left in DEMO — full memory (500 facts free) is one download away: {self.DEMO_URL}")}
        return {"ok": True, "nodes": added, "exit": 0,
                "raw": f"✅ Added: {label[:60]} ({added}/{self.DEMO_LIMIT} DEMO facts) — full memory: {self.DEMO_URL}"}

    def find(self, query: str, limit: int = 5) -> list[dict]:
        q = set(w.lower() for w in query.split() if len(w) > 2)
        scored = []
        for label, content in self._facts.items():
            text = f"{label} {content}".lower()
            score = sum(1 for w in q if w in text)
            if score > 0:
                scored.append((score, label, content))
        scored.sort(key=lambda x: -x[0])
        out = [{"label": l, "content": c, "level": "L1"} for _, l, c in scored[:limit]]
        return out

    def stats(self) -> dict:
        used = len(self._facts)
        warn = ""
        if used >= self.DEMO_LIMIT * 0.8:
            warn = (f"\n⚡ {self.DEMO_LIMIT - used} facts left in DEMO — full memory (500 facts free): {self.DEMO_URL}"
                    f"\n💰 Upgrade: $5/mo · $30/yr · $60 lifetime → https://wwwvibo.com/pricing")
        return {"nodes": used, "edges": 0,
                "raw": f"Nodes: {used}/{self.DEMO_LIMIT} (DEMO) — semantic search, encryption and 500 facts need the full ViBo: {self.DEMO_URL}{warn}"}

    def usage(self) -> dict:
        return {"ok": True, "raw": "💾 ViBo DEMO mode: no real token savings until the full ViBo is installed (https://wwwvibo.com/download/skill)."}


class ViBo:
    """Thin wrapper over vibo_use.py (subprocess, no core import)."""

    def __init__(self, cli: str | Path | None = None, env: dict | None = None):
        self.demo = False
        explicit_cli = bool(cli) or bool(os.environ.get("VIBO_CLI"))
        try:
            self.cli = str(cli) if cli else _find_cli()
        except ViBoError as e:
            if explicit_cli:
                # An explicit VIBO_CLI that is invalid must fail loud — the
                # operator expects the real memory, not a silent DEMO fallback.
                raise
            # No ViBo CLI at all → built-in DEMO mode (100 facts) so the client
            # can try the convenience right away; full engine is one download.
            self.demo = True
            self.cli = ""
            self._demo = MiniMemory()
        self.python = _find_python()
        # Pass ONLY a safe minimum (whitelist) to the child process,
        # not the whole os.environ — env secrets never reach subprocess.
        self.env = {k: os.environ.get(k) for k in ("PATH", "HOME", "LANG", "LC_ALL")}
        self.env["VIBO_MEM_FILE"] = os.environ.get("VIBO_MEM_FILE", "memory.web")
        self.env["VIBO_USAGE_LOG"] = os.environ.get("VIBO_USAGE_LOG", "vibo_usage.jsonl")
        self.env = {k: v for k, v in self.env.items() if v is not None}
        if env:
            # allowlist only: caller-supplied env may not inject arbitrary
            # variables (audit 31.08 — weakens the whitelist otherwise)
            _allowed = {"VIBO_MEM_FILE", "VIBO_USAGE_LOG", "PATH", "HOME", "LANG", "LC_ALL"}
            for k, v in env.items():
                if k in _allowed and v is not None:
                    self.env[k] = v

    def _run(self, args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
        try:
            # vibo_use.py keeps memory.web relative to CWD — run the CLI
            # from its folder so it sees its own memory (acceptance fix v3).
            return subprocess.run(
                [self.python, self.cli, *args],
                capture_output=True, text=True, timeout=timeout, env=self.env,
                cwd=os.path.dirname(os.path.abspath(self.cli)),
            )
        except subprocess.TimeoutExpired as e:
            raise ViBoError(f"ViBo CLI timeout ({timeout}s)") from e

    # ── commands ────────────────────────────────────────────────────────

    def add(self, label: str, content: str = "", level: str = "L1", tags: list[str] | None = None) -> dict:
        """Save a fact. level: L1/L2/L3. Returns {'ok': bool, 'nodes': int, 'raw': str}."""
        if self.demo:
            return self._demo.add(label, content, level, tags)
        args = ["add", label[:60]]
        if content:
            args += [content]
        if level != "L1":
            args += ["--level", level]
        for t in tags or []:
            args += ["--tag", t]
        r = self._run(args)
        out = (r.stdout or "").strip()
        m = re.search(r"\((\d+) nodes\)", out)
        return {"ok": r.returncode == 0, "nodes": int(m.group(1)) if m else 0,
                "raw": out, "exit": r.returncode}

    def find(self, query: str, limit: int = 5) -> list[dict]:
        """Semantic search. Real CLI format:
        In DEMO mode: simple word match.
        """
        if self.demo:
            return self._demo.find(query, limit)
        r = self._run(["find", query, "--limit", str(limit)])
        facts: list[dict] = []
        line_re = re.compile(r"^\s*[•\-*]\s*\[([A-Z0-9]+)\]\s*([^:]+):\s?(.*)$")
        for line in (r.stdout or "").splitlines():
            m = line_re.match(line)
            if m:
                facts.append({"label": m.group(2).strip(),
                              "content": m.group(3).strip(),
                              "level": m.group(1)})
            if len(facts) >= limit:
                break
        return facts

    def usage(self) -> dict:
        """Real savings. Returns {'ok': bool, 'raw': str}."""
        if self.demo:
            return self._demo.usage()
        r = self._run(["usage"])
        return {"ok": r.returncode == 0, "raw": (r.stdout or "").strip()}

    def link(self, a: str, b: str, rel: str = "related") -> dict:
        """Link two facts (by label)."""
        r = self._run(["link", a, b, "--rel", rel])
        return {"ok": r.returncode == 0, "raw": (r.stdout or "").strip(), "exit": r.returncode}

    def stats(self) -> dict:
        """Memory stats."""
        if self.demo:
            return self._demo.stats()
        r = self._run(["stats"])
        raw = (r.stdout or "").strip()
        m = re.search(r"Nodes:\s*(\d+)/(\d+)", raw) or re.search(r"Nodes:\s*(\d+)", raw)
        nodes = int(m.group(1)) if m else 0
        return {"ok": r.returncode == 0, "nodes": nodes, "raw": raw}


if __name__ == "__main__":
    # CLI mode: python3 lib_vibo.py find "test" | stats | add ... | usage
    v = ViBo()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "stats":
        print(json.dumps(v.stats(), ensure_ascii=False))
    elif cmd == "find":
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        print(json.dumps(v.find(q), ensure_ascii=False, indent=1))
    elif cmd == "add":
        label = sys.argv[2] if len(sys.argv) > 2 else "test"
        content = sys.argv[3] if len(sys.argv) > 3 else ""
        print(json.dumps(v.add(label, content), ensure_ascii=False))
    elif cmd == "usage":
        print(json.dumps(v.usage(), ensure_ascii=False))
    else:
        print(__doc__)
