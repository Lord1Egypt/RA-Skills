"""
yumnb delivery dispatcher — send generated note outputs to chat/IM surfaces.

This is intentionally separate from webhook-style notify:
- notify = fire a JSON payload to some webhook receiver
- deliver = send user-facing messages/files to an IM/channel layer

Providers:
  - none                : do nothing
  - openclaw / hermes   : shell out to `openclaw message send`, which can
                          target Telegram, Discord, Slack, Microsoft Teams,
                          and other channels supported by the local OpenClaw /
                          Hermes bridge.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_FILES = ["talkshow.mp3", "deck.pptx"]
LABEL_MAP = {
    "talkshow.mp3": "🎧 Listen",
    "deck.pptx": "📊 Slides",
    "summary.md": "📝 Summary",
}


def _run(cmd: List[str], timeout: int = 300) -> Tuple[int, str, str]:
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except FileNotFoundError as e:
        return 127, "", f"binary not found: {e}"
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s: {' '.join(cmd)}"
    except Exception as e:  # noqa: BLE001
        return 1, "", f"{type(e).__name__}: {e}"


def _public_links_only(links: Dict[str, str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for label, url in (links or {}).items():
        if not url:
            continue
        low = url.lower()
        if low.startswith("http://") or low.startswith("https://"):
            out[label] = url
    return out


def _build_text(title: str, summary: str, links: Dict[str, str]) -> str:
    parts = [f"📓 {title}"]
    if summary:
        parts.append(summary)
    pub = _public_links_only(links)
    if pub:
        parts.append("\n".join(f"{label}: {url}" for label, url in pub.items()))
    return "\n\n".join(p for p in parts if p).strip()


def _openclaw_send(subcfg: Dict, message: str = "", media: Optional[Path] = None) -> Dict:
    binary = subcfg.get("binary") or "openclaw"
    channel = subcfg.get("channel") or ""
    target = subcfg.get("target") or ""
    if not channel or not target:
        return {
            "ok": False,
            "rc": 2,
            "error": "deliver.openclaw.channel and deliver.openclaw.target are required",
        }

    cmd = [binary, "message", "send", "--channel", str(channel), "--target", str(target), "--json"]
    account = subcfg.get("account") or subcfg.get("account_id") or ""
    if account:
        cmd += ["--account", str(account)]
    reply_to = subcfg.get("reply_to") or ""
    if reply_to:
        cmd += ["--reply-to", str(reply_to)]
    thread_id = subcfg.get("thread_id") or ""
    if thread_id:
        cmd += ["--thread-id", str(thread_id)]
    if subcfg.get("silent"):
        cmd.append("--silent")
    if subcfg.get("force_document"):
        cmd.append("--force-document")
    if subcfg.get("dry_run"):
        cmd.append("--dry-run")
    if media is not None:
        cmd += ["--media", str(media)]
    if message:
        cmd += ["--message", message]

    rc, out, err = _run(cmd, timeout=int(subcfg.get("timeout_seconds") or 120))
    payload = None
    if out:
        try:
            payload = json.loads(out)
        except json.JSONDecodeError:
            payload = None
    return {
        "ok": rc == 0,
        "rc": rc,
        "stdout": out,
        "stderr": err,
        "payload": payload,
        "command": cmd,
    }


def _deliver_openclaw(folder: Path, cfg: Dict, title: str, summary: str, links: Dict[str, str]) -> List[Dict]:
    subcfg = (cfg.get("openclaw") or cfg.get("hermes") or {}).copy()
    results: List[Dict] = []

    send_text = bool(subcfg.get("send_text", True))
    send_files = bool(subcfg.get("send_files", True))
    text = _build_text(title, summary, links)

    if send_text and text:
        res = _openclaw_send(subcfg, message=text)
        res["kind"] = "text"
        results.append(res)
        print(f"deliver [openclaw text] rc={res['rc']}")

    if send_files:
        files = cfg.get("files") or DEFAULT_FILES
        for fname in files:
            fp = folder / fname
            if not fp.exists():
                continue
            caption = ""
            if subcfg.get("captions", True):
                caption = f"{title} — {LABEL_MAP.get(fname, fname)}"
            res = _openclaw_send(subcfg, message=caption, media=fp)
            res["kind"] = "media"
            res["file"] = fname
            results.append(res)
            print(f"deliver [openclaw {fname}] rc={res['rc']}")

    return results


def deliver_folder(folder: Path, cfg: Dict, title: str, summary: str, links: Dict[str, str]) -> List[Dict]:
    provider = ((cfg or {}).get("provider") or "none").strip().lower()
    if provider in ("", "none"):
        return []
    if provider in ("openclaw", "hermes"):
        return _deliver_openclaw(folder, cfg, title, summary, links)
    print(f"deliver [{provider}] SKIP — unknown provider")
    return []
