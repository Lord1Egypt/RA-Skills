#!/usr/bin/env python3
"""
Dual-backend activity logger.
Supports SiYuan Note API and local markdown file backend.
"""

import json
import subprocess
import sys
import os
from datetime import datetime

# ==================== Configuration ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "../config.json")
LOCAL_STATE_FILE = os.path.expanduser("~/.openclaw/scripts/daily-docs.json")

# =============================================================


def load_config():
    """Load configuration from config.json."""
    config = {
        "backend": "local",
        "local": {"output_dir": "~/screen-activity", "keep_days": 7},
        "siyuan": {"url": "http://127.0.0.1:6806", "token": "", "notebook_id": ""},
        "mlx_url": "",
        "analysis_mode": "simple",
        "analysis_prompt": "",
        "interval_minutes": 5,
        "idle_detection": True,
        "app_blacklist": [],
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                user = json.load(f)
            # Merge top-level keys
            for k, v in user.items():
                if k in config and isinstance(config[k], dict) and isinstance(v, dict):
                    config[k].update(v)
                else:
                    config[k] = v
        except (json.JSONDecodeError, IOError):
            pass
    return config


# ==================== SiYuan API ====================

def siyuan_post(endpoint, data=None, files=None, config=None):
    """Generic SiYuan API POST request."""
    if config is None:
        config = load_config()
    siyuan = config.get("siyuan", {})

    cmd = [
        "curl", "-s", "--connect-timeout", "10", "--max-time", "15",
        "-X", "POST",
        "-H", f"Authorization: Token {siyuan.get('token', '')}",
    ]
    if files:
        for key, val in files.items():
            cmd.extend(["-F", f"{key}={val}"])
    else:
        cmd.extend(["-H", "Content-Type: application/json"])
        if data:
            cmd.extend(["-d", json.dumps(data, ensure_ascii=False)])
    cmd.append(f"{siyuan.get('url', 'http://127.0.0.1:6806')}{endpoint}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.stdout:
            return json.loads(result.stdout)
        return {}
    except (json.JSONDecodeError, subprocess.TimeoutExpired):
        return {}


def siyuan_load_state():
    if os.path.exists(LOCAL_STATE_FILE):
        try:
            with open(LOCAL_STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def siyuan_save_state(state):
    os.makedirs(os.path.dirname(LOCAL_STATE_FILE), exist_ok=True)
    with open(LOCAL_STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False)


def siyuan_ensure_daily_docs(date_str, config=None):
    """Ensure today's SiYuan docs exist. Returns (daily_doc_id, image_doc_id)."""
    state = siyuan_load_state()
    if state.get("date") == date_str and state.get("daily_doc") and state.get("image_doc"):
        return state["daily_doc"], state["image_doc"]

    if config is None:
        config = load_config()
    siyuan = config.get("siyuan", {})

    daily_title = f"{date_str} 操作记录"
    image_title = f"{date_str} 截图存档"

    # Create daily doc
    resp = siyuan_post(
        "/api/filetree/createDocWithMd",
        {"notebook": siyuan.get("notebook_id", ""),
         "path": f"/{daily_title}",
         "markdown": f"# {daily_title}\n\n记录 {date_str} 的屏幕活动。\n\n"},
        config=config,
    )
    daily_doc = resp.get("data") if resp.get("code") == 0 else None
    if not daily_doc:
        ts = datetime.now().strftime("%H%M%S")
        resp = siyuan_post(
            "/api/filetree/createDocWithMd",
            {"notebook": siyuan.get("notebook_id", ""),
             "path": f"/{daily_title}-{ts}",
             "markdown": f"# {daily_title}\n\n记录 {date_str} 的屏幕活动。\n\n"},
            config=config,
        )
        daily_doc = resp.get("data") if resp.get("code") == 0 else None

    # Create image doc
    resp = siyuan_post(
        "/api/filetree/createDocWithMd",
        {"notebook": siyuan.get("notebook_id", ""),
         "path": f"/{image_title}",
         "markdown": f"# {image_title}\n\n{date_str} 的截图存档。\n\n"},
        config=config,
    )
    image_doc = resp.get("data") if resp.get("code") == 0 else None
    if not image_doc:
        ts = datetime.now().strftime("%H%M%S")
        resp = siyuan_post(
            "/api/filetree/createDocWithMd",
            {"notebook": siyuan.get("notebook_id", ""),
             "path": f"/{image_title}-{ts}",
             "markdown": f"# {image_title}\n\n{date_str} 的截图存档。\n\n"},
            config=config,
        )
        image_doc = resp.get("data") if resp.get("code") == 0 else None

    state = {"date": date_str, "daily_doc": daily_doc, "image_doc": image_doc}
    siyuan_save_state(state)
    return daily_doc, image_doc


# ==================== Local Backend ====================

def local_ensure_md_file(date_str, config=None):
    """Ensure today's markdown file exists. Returns file path."""
    if config is None:
        config = load_config()
    output_dir = os.path.expanduser(config.get("local", {}).get("output_dir", "~/screen-activity"))
    os.makedirs(output_dir, exist_ok=True)

    md_path = os.path.join(output_dir, f"{date_str}.md")
    if not os.path.exists(md_path):
        with open(md_path, "w") as f:
            f.write(f"# {date_str} 操作记录\n\n")
    return md_path


def local_cleanup(config=None):
    """Clean up old screenshots based on keep_days config."""
    if config is None:
        config = load_config()
    output_dir = os.path.expanduser(config.get("local", {}).get("output_dir", "~/screen-activity"))
    keep_days = config.get("local", {}).get("keep_days", 7)

    if keep_days > 0:
        ss_dir = os.path.join(output_dir, "screenshots")
        if os.path.exists(ss_dir):
            try:
                subprocess.run(
                    ["find", ss_dir, "-type", "d", "-mtime", f"+{keep_days}", "-exec", "rm", "-rf", "{}", "+"],
                    capture_output=True, timeout=30,
                )
            except (subprocess.TimeoutExpired, OSError):
                pass


# ==================== Main Log Function ====================

def log_activity(screenshot_path, date_str, time_str, summary, config=None):
    """Log activity to configured backend."""
    if config is None:
        config = load_config()

    backend = config.get("backend", "local")

    if backend == "siyuan":
        return _log_siyuan(screenshot_path, date_str, time_str, summary, config)
    else:
        return _log_local(screenshot_path, date_str, time_str, summary, config)


def _log_siyuan(screenshot_path, date_str, time_str, summary, config):
    """Log to SiYuan Note."""
    siyuan = config.get("siyuan", {})
    daily_doc, image_doc = siyuan_ensure_daily_docs(date_str, config)

    if not screenshot_path or not os.path.exists(screenshot_path):
        resp = siyuan_post(
            "/api/block/appendBlock",
            {"dataType": "markdown", "data": f"- **{time_str}** {summary}\n", "parentID": daily_doc},
            config=config,
        )
        print(f"TEXT-ONLY | {date_str} {time_str} | {summary}")
        return resp.get("code") == 0

    # Upload screenshot
    upload_resp = siyuan_post(
        "/api/asset/upload",
        files={"assetsDirPath": "/assets/", "file[]": f"@{screenshot_path}"},
        config=config,
    )

    asset_path = ""
    try:
        asset_path = list(upload_resp["data"]["succMap"].values())[0]
    except (KeyError, TypeError, IndexError, AttributeError):
        print(f"WARN: Upload failed", file=sys.stderr)
        resp = siyuan_post(
            "/api/block/appendBlock",
            {"dataType": "markdown", "data": f"- **{time_str}** {summary} （截图上传失败）\n", "parentID": daily_doc},
            config=config,
        )
        return resp.get("code") == 0

    # Insert into image doc
    img_md = f"## {time_str}\n\n![{time_str} 截图]({asset_path})\n\n> {summary}\n\n---\n"
    img_resp = siyuan_post(
        "/api/block/appendBlock",
        {"dataType": "markdown", "data": img_md, "parentID": image_doc},
        config=config,
    )

    img_block_id = ""
    try:
        for op in img_resp["data"][0]["doOperations"]:
            if op.get("action") == "insert":
                img_block_id = op["id"]
                break
    except (KeyError, TypeError, IndexError, AttributeError):
        pass

    # Append link to daily doc
    if img_block_id:
        entry = f'- **{time_str}** {summary} [查看截图](siyuan://blocks/{img_block_id})\n'
    else:
        entry = f'- **{time_str}** {summary}\n'

    resp = siyuan_post(
        "/api/block/appendBlock",
        {"dataType": "markdown", "data": entry, "parentID": daily_doc},
        config=config,
    )

    ok = resp.get("code") == 0
    print(f"{'OK' if ok else 'FAIL'} | {date_str} {time_str} | {summary} | {asset_path}")
    return ok


def _log_local(screenshot_path, date_str, time_str, summary, config):
    """Log to local markdown file."""
    cfg = config or load_config()
    output_dir = os.path.expanduser(cfg.get("local", {}).get("output_dir", "~/screen-activity"))
    ss_dir = os.path.join(output_dir, "screenshots", date_str)
    md_path = local_ensure_md_file(date_str, cfg)

    if not screenshot_path or not os.path.exists(screenshot_path):
        with open(md_path, "a") as f:
            f.write(f"- **{time_str}** {summary}\n")
        print(f"TEXT-ONLY | {date_str} {time_str} | {summary}")
        return True

    # Ensure screenshot is in the right place (already saved by screen-activity.sh)
    rel_path = f"screenshots/{date_str}/{os.path.basename(screenshot_path)}"

    with open(md_path, "a") as f:
        f.write(f"- **{time_str}** {summary} ![{rel_path}]({rel_path})\n")

    print(f"OK | {date_str} {time_str} | {summary} | local:{rel_path}")
    local_cleanup(cfg)
    return True


# ==================== CLI ====================
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(f"Usage: {sys.argv[0]} <screenshot_path|NONE> <date> <time> <summary>", file=sys.stderr)
        sys.exit(1)

    screenshot = sys.argv[1]
    date = sys.argv[2]
    time = sys.argv[3]
    summary = sys.argv[4]

    if screenshot == "NONE" or not os.path.exists(screenshot):
        screenshot = ""

    try:
        success = log_activity(screenshot, date, time, summary)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
