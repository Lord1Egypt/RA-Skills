#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DISCORD_ME_URL = "https://discord.com/api/v10/users/@me"


def sanitize_filename(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip())
    s = s.strip("-.")
    return s or "discord-bot"


def build_static_avatar_url(bot_id: str, avatar_hash: str) -> str:
    return f"https://cdn.discordapp.com/avatars/{bot_id}/{avatar_hash}.png"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def http_get_json(url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)


def list_discord_channel_candidates(config: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    candidates: List[Tuple[str, Dict[str, Any]]] = []

    def visit(obj: Any, path: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                next_path = f"{path}.{key}" if path else key
                if isinstance(value, dict):
                    lower_path = next_path.lower()
                    has_token = isinstance(value.get("token"), str) and bool(value.get("token", "").strip())
                    enabled = value.get("enabled")
                    if "discord" in lower_path and has_token and enabled is not False:
                        candidates.append((next_path, value))
                    visit(value, next_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                visit(item, f"{path}[{i}]")

    visit(config)
    return candidates


def choose_discord_channel(config: Dict[str, Any], channel_name: Optional[str]) -> Tuple[str, Dict[str, Any]]:
    candidates = list_discord_channel_candidates(config)
    if not candidates:
        raise RuntimeError("Could not find an enabled Discord channel with a token in openclaw.json.")

    if channel_name:
        channel_name = channel_name.strip().lower()
        for path, channel in candidates:
            tail = path.split(".")[-1].lower()
            if tail == channel_name or path.lower().endswith("." + channel_name):
                return path, channel
        raise RuntimeError(f"Could not find Discord channel '{channel_name}' in openclaw.json.")

    if len(candidates) == 1:
        return candidates[0]

    enabled = [(path, channel) for path, channel in candidates if channel.get("enabled") is True]
    if len(enabled) == 1:
        return enabled[0]

    names = ", ".join(path for path, _ in candidates)
    raise RuntimeError(
        "Found multiple Discord channels in openclaw.json. "
        f"Use --channel to choose one. Candidates: {names}"
    )


def ensure_discord_block_lines(data: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    for key in ("username", "locale", "email", "bio"):
        value = data.get(key)
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        lines.append(f"  - {key}: {value}")
    return ["- **Discord:**", *lines] if lines else []


def find_field_line(lines: List[str], field_name: str) -> Optional[int]:
    pat = re.compile(rf"^\s*[-*]\s*\*\*{re.escape(field_name)}:\*\*")
    for i, line in enumerate(lines):
        if pat.search(line):
            return i
    return None


def find_discord_block(lines: List[str]) -> Optional[Tuple[int, int]]:
    start = find_field_line(lines, "Discord")
    if start is None:
        return None
    end = start + 1
    while end < len(lines):
        if re.match(r"^\s*[-*]\s*\*\*[^*]+:\*\*", lines[end]):
            break
        end += 1
    return start, end


def upsert_avatar(lines: List[str], avatar_url: str, force_avatar: bool) -> List[str]:
    idx = find_field_line(lines, "Avatar")
    new_line = f"- **Avatar:** {avatar_url}"
    if idx is None:
        insert_at = 1 if lines and lines[0].startswith("#") else 0
        while insert_at < len(lines) and not lines[insert_at].strip():
            insert_at += 1
        lines.insert(insert_at, new_line)
        return lines

    existing = lines[idx].strip()
    if existing == new_line:
        return lines
    if not force_avatar:
        raise RuntimeError(
            f"IDENTITY.md already has a different Avatar field:\n  existing: {existing}\n  desired:  {new_line}\nUse --force-avatar to replace it."
        )
    lines[idx] = new_line
    return lines


def upsert_discord_block(lines: List[str], discord_lines: List[str]) -> List[str]:
    if not discord_lines:
        return lines
    block = find_discord_block(lines)
    if block is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(discord_lines)
        return lines
    start, end = block
    lines[start:end] = discord_lines
    return lines


def ensure_identity_lines(identity_path: Path) -> List[str]:
    if identity_path.exists():
        return identity_path.read_text(encoding="utf-8").splitlines()
    return ["# IDENTITY", ""]


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Discord bot metadata into OpenClaw IDENTITY.md")
    parser.add_argument("--workspace", required=True, help="Path to the current OpenClaw workspace")
    parser.add_argument("--config", help="Path to openclaw.json (default: <workspace>/openclaw.json)")
    parser.add_argument("--identity", help="Path to IDENTITY.md (default: <workspace>/IDENTITY.md)")
    parser.add_argument("--channel", help="Discord channel name to use when multiple Discord channels exist")
    parser.add_argument("--force-avatar", action="store_true", help="Replace an existing different Avatar field")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    config_path = Path(args.config).expanduser().resolve() if args.config else workspace / "openclaw.json"
    identity_path = Path(args.identity).expanduser().resolve() if args.identity else workspace / "IDENTITY.md"

    if not config_path.exists():
        print(f"Missing config: {config_path}", file=sys.stderr)
        return 2

    config = load_json(config_path)
    channel_path, channel = choose_discord_channel(config, args.channel)
    token = str(channel.get("token") or "").strip()
    if not token:
        print(f"Discord channel token is empty: {channel_path}", file=sys.stderr)
        return 2

    profile = http_get_json(DISCORD_ME_URL, {"Authorization": f"Bot {token}"})
    bot_id = str(profile.get("id") or "").strip()
    avatar_hash = str(profile.get("avatar") or "").strip()
    username = str(profile.get("username") or bot_id or "discord-bot").strip()

    if not bot_id or not avatar_hash:
        print("Discord profile is missing id or avatar.", file=sys.stderr)
        return 2

    avatar_url = build_static_avatar_url(bot_id, avatar_hash)
    avatar_dest = workspace / "avatars" / f"discord-{sanitize_filename(username)}.png"
    download_file(avatar_url, avatar_dest)

    lines = ensure_identity_lines(identity_path)
    backup_path: Optional[Path] = None
    if identity_path.exists():
        backup_path = identity_path.with_suffix(identity_path.suffix + ".bak")
        shutil.copy2(identity_path, backup_path)

    lines = upsert_avatar(lines, avatar_url, args.force_avatar)
    lines = upsert_discord_block(lines, ensure_discord_block_lines(profile))

    identity_path.parent.mkdir(parents=True, exist_ok=True)
    identity_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"workspace:    {workspace}")
    print(f"config:       {config_path}")
    print(f"channel:      {channel_path}")
    print(f"identity:     {identity_path}")
    print(f"avatar local: {avatar_dest}")
    print(f"avatar url:   {avatar_url}")
    if backup_path:
        print(f"backup:       {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
