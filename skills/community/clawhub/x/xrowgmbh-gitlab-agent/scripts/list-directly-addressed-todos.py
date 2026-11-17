#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""List pending GitLab to-dos directly addressed by the configured owner."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


PER_PAGE = 100


def api_json(endpoint: str) -> object:
    result = subprocess.run(
        ["glab", "api", endpoint], check=True, text=True, stdout=subprocess.PIPE
    )
    return json.loads(result.stdout)


def configured_owner() -> str:
    """Require the owner in the active OpenClaw skill configuration."""
    from pathlib import Path
    import re

    configured_path = os.environ.get("OPENCLAW_CONFIG_PATH")
    config_path = (Path(configured_path).expanduser() if configured_path
                   else Path.home() / ".openclaw" / "openclaw.json")
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    for key in ("skills", "entries", "gitlab-agent", "config"):
        if not isinstance(payload, dict):
            raise ValueError("GitLab agent owner configuration must contain objects")
        payload = payload.get(key)
    owner = payload.get("owner") if isinstance(payload, dict) else None
    if not isinstance(owner, str) or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", owner.strip()):
        raise ValueError("Set skills.entries.gitlab-agent.config.owner to a GitLab username")
    return owner.strip()


def owner_identity(username: str) -> tuple[int, str]:
    from urllib.parse import urlencode

    users = api_json(f"users?{urlencode({'username': username})}")
    if not isinstance(users, list):
        raise ValueError("GitLab owner lookup returned an invalid response")
    matches = [user for user in users if isinstance(user, dict)
               and str(user.get("username", "")).casefold() == username.casefold()
               and type(user.get("id")) is int and user["id"] > 0]
    if len(matches) != 1:
        raise ValueError("GitLab owner lookup did not identify one exact user")
    return matches[0]["id"], matches[0]["username"]


def pending_owner_todos(owner_id: int, owner_username: str) -> list[dict[str, object]]:
    from urllib.parse import urlencode

    todos: list[dict[str, object]] = []
    page = 1
    while True:
        query = urlencode({
            "action": "directly_addressed", "author_id": owner_id,
            "state": "pending", "per_page": PER_PAGE, "page": page,
        })
        payload = api_json(f"todos?{query}")
        if not isinstance(payload, list):
            raise ValueError("GitLab to-do lookup returned a non-list page")
        for todo in payload:
            if not isinstance(todo, dict):
                raise ValueError("GitLab to-do lookup returned an invalid entry")
            author = todo.get("author")
            if (type(todo.get("id")) is int and todo["id"] > 0
                    and todo.get("action_name") == "directly_addressed"
                    and todo.get("state") == "pending"
                    and isinstance(author, dict) and author.get("id") == owner_id
                    and author.get("username") == owner_username):
                todos.append(todo)
        if len(payload) < PER_PAGE:
            break
        page += 1
    return todos


def main() -> int:
    try:
        owner_id, owner_username = owner_identity(configured_owner())
        print(json.dumps(pending_owner_todos(owner_id, owner_username), ensure_ascii=False, indent=2))
        return 0
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError) as failure:
        print(f"Unable to list owner-addressed GitLab to-dos: {failure}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
