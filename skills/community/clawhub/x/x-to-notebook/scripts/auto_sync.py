"""Auto-sync X bookmark folders to matching NotebookLM notebooks.

Outputs a JSON report to stdout for the cron to parse and send via Telegram.
"""

import asyncio
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

from twikit import Client

COOKIES_PATH = Path.home() / ".openclaw" / "credentials" / "x-cookies.json"
PUSHED_PATH = Path.home() / ".openclaw" / "data" / "x-bookmarks-pushed.json"
MARK_PUSHED_SCRIPT = Path(__file__).parent / "mark_pushed.py"


def load_cookies(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return {item["name"]: item["value"] for item in data}
    return data


def load_pushed_ids() -> set:
    if not PUSHED_PATH.exists():
        return set()
    with open(PUSHED_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))


def mcporter_call(tool: str, **kwargs) -> dict:
    """Call an MCP tool via mcporter and return parsed JSON."""
    cmd = ["mcporter", "call", f"notebooklm.{tool}"]
    for k, v in kwargs.items():
        cmd.append(f"{k}={shlex.quote(str(v))}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"mcporter error: {result.stderr.strip()}")
    return json.loads(result.stdout)


EMOJI_RE = re.compile(
    r"[\U0001f600-\U0001f64f\U0001f300-\U0001f5ff\U0001f680-\U0001f6ff"
    r"\U0001f900-\U0001f9ff\U0001fa00-\U0001fa6f\U0001fa70-\U0001faff"
    r"\u2600-\u26ff\u2700-\u27bf\ufe0f]+",
)


FOLDER_SUFFIX_RE = re.compile(r"[- ]*(notebook|bookmarks?)$", re.IGNORECASE)


def normalize_name(name: str) -> str:
    """Strip emojis, folder suffixes (-notebook, -bookmarks), and extra whitespace."""
    name = EMOJI_RE.sub("", name).strip()
    name = FOLDER_SUFFIX_RE.sub("", name).strip()
    return name.lower()


def match_folder_to_notebook(folder_name: str, notebooks: list[dict]) -> dict | None:
    """Case-insensitive match of folder name to notebook title, ignoring emojis."""
    normalized = normalize_name(folder_name)
    for nb in notebooks:
        if normalize_name(nb.get("title", "")) == normalized:
            return nb
    return None


async def fetch_folder_bookmarks(
    client: Client, folder_id: str | None, pushed_ids: set
) -> list[dict]:
    """Fetch new bookmarks from a folder (or all if folder_id is None)."""
    bookmarks = await client.get_bookmarks(count=20, folder_id=folder_id)
    results = []
    for tweet in bookmarks:
        if tweet.id not in pushed_ids:
            results.append(
                {
                    "id": tweet.id,
                    "author": tweet.user.screen_name,
                    "text": tweet.full_text,
                    "url": f"https://x.com/{tweet.user.screen_name}/status/{tweet.id}",
                }
            )
    return results


def push_bookmark(notebook_id: str, bookmark: dict) -> tuple[bool, str]:
    """Push a bookmark as text source to a notebook. Returns (success, error_msg)."""
    text = f"@{bookmark['author']}: {bookmark['text']}\n\nSource: {bookmark['url']}"
    try:
        mcporter_call(
            "source_add",
            notebook_id=notebook_id,
            source_type="text",
            text=text,
        )
        return True, ""
    except RuntimeError as e:
        print(f"Failed to push {bookmark['url']}: {e}", file=sys.stderr)
        return False, str(e)


def mark_pushed(ids: list[str]):
    """Mark bookmark IDs as pushed by calling mark_pushed.py."""
    if not ids:
        return
    result = subprocess.run(
        [
            "uv",
            "run",
            "--project",
            str(Path.home() / ".openclaw"),
            str(MARK_PUSHED_SCRIPT),
        ]
        + ids,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Failed to mark pushed: {result.stderr.strip()}", file=sys.stderr)


async def main():
    if not COOKIES_PATH.exists():
        report = {"error": f"X cookies not found at {COOKIES_PATH}"}
        json.dump(report, sys.stdout)
        sys.exit(1)

    # Init twikit
    client = Client(language="en-US")
    client.set_cookies(load_cookies(COOKIES_PATH))
    pushed_ids = load_pushed_ids()

    # Fetch folders
    folders = await client.get_bookmark_folders()
    folder_list = [{"id": f.id, "name": f.name} for f in folders]
    # Add virtual "unfiled" entry (folder_id=None fetches all/unfiled)
    folder_list.append({"id": None, "name": "Unfiled"})

    # Fetch notebooks
    try:
        notebooks_raw = mcporter_call("notebook_list")
        notebooks = (
            notebooks_raw
            if isinstance(notebooks_raw, list)
            else notebooks_raw.get("notebooks", [])
        )
    except RuntimeError as e:
        report = {"error": str(e)}
        json.dump(report, sys.stdout)
        sys.exit(1)

    # Process each folder
    synced = []
    skipped = []

    for folder in folder_list:
        bookmarks = await fetch_folder_bookmarks(client, folder["id"], pushed_ids)
        if not bookmarks:
            continue

        notebook = match_folder_to_notebook(folder["name"], notebooks)
        if not notebook:
            skipped.append({"folder": folder["name"], "count": len(bookmarks)})
            continue

        pushed_count = 0
        folder_pushed_ids = []
        for bm in bookmarks:
            success, _ = push_bookmark(notebook["id"], bm)
            if success:
                pushed_count += 1
                folder_pushed_ids.append(bm["id"])

        if folder_pushed_ids:
            mark_pushed(folder_pushed_ids)
            synced.append(
                {
                    "notebook": notebook.get("title", folder["name"]),
                    "count": pushed_count,
                    "failed": len(bookmarks) - pushed_count,
                }
            )

    report = {"synced": synced, "skipped": skipped}
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    asyncio.run(main())
