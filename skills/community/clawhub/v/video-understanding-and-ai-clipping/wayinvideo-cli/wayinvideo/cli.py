"""WayinVideo CLI - unified entry-point.

Examples
--------
    wayinvideo upload  --file-path video.mp4
    wayinvideo submit  clip     --url <url> --export --ratio RATIO_9_16
    wayinvideo submit  search   --url <url> --query "funny cat"
    wayinvideo poll    --type clip --id <id>
    wayinvideo config  show
    wayinvideo config  set defaults.clip.top_k 5
"""

import os
import sys
import json
import copy
import time
import argparse
import textwrap
import subprocess
from datetime import datetime, timedelta, timezone

from wayinvideo import __version__
from wayinvideo import constants
from wayinvideo.constants import (
    TASK_TYPES,
    INCREMENTAL_TASKS,
    TERMINAL_STATUSES,
    SUBMIT_ENDPOINTS,
    DURATION_CHOICES,
    RATIO_CHOICES,
    RESOLUTION_CHOICES,
    CAPTION_DISPLAY_CHOICES,
    AI_HOOK_SCRIPT_STYLE_CHOICES,
    AI_HOOK_POSITION_CHOICES,
    SUPPORTED_LANGUAGES,
    CONFIG_KEYS_DOC,
)
from wayinvideo import config as cfg
from wayinvideo import client


# ══════════════════════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _resolve(cli_val, config_key, fallback=None):
    """Priority chain: explicit CLI arg  ▸  config file  ▸  hardcoded fallback."""
    if cli_val is not None:
        return cli_val
    v = cfg.get_value(config_key)
    if v is not None:
        if isinstance(v, str) and v.startswith("~"):
            return os.path.expanduser(v)
        return v
    return fallback


def _resolve_flag(args, attr, config_key, fallback):
    """Resolve a --flag / --no-flag pair (True / False / None in namespace)."""
    val = getattr(args, attr, None)
    if val is not None:
        return val
    return _resolve(None, config_key, fallback)


def _send_event(text):
    """Fire an openclaw system event (best-effort, never raises)."""
    # Only send if event_enabled = True and event_enabled > 0, which is False and 0 by default.
    try:
        subprocess.run([
            "openclaw", "system", "event",
            "--text", text,
            "--mode", "now"
        ], check=True, capture_output=True, text=True)
    except Exception:
        pass


def _save_json(data, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def _load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def _ms_to_iso(ms_timestamp):
    return datetime.fromtimestamp(ms_timestamp / 1000, tz=timezone.utc).isoformat()


# ══════════════════════════════════════════════════════════════════════════════
#  Command: upload
# ══════════════════════════════════════════════════════════════════════════════

def _cmd_upload(args):
    print(f"Uploading {args.file_path} …", file=sys.stderr)
    try:
        identity = client.upload_file(args.file_path)
    except Exception as e:
        print(f"Upload failed: {e}", file=sys.stderr)
        sys.exit(1)
    print("Upload complete.", file=sys.stderr)
    print(json.dumps({"identity": identity}))


# ══════════════════════════════════════════════════════════════════════════════
#  Command: submit
# ══════════════════════════════════════════════════════════════════════════════

def _cmd_submit(args):
    task_type = args.task_type
    if not task_type:
        print(
            "Error: task type is required.\n"
            "  wayinvideo submit {clip,search,summarize,transcribe,export} -h",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── Build common payload ──
    if task_type == "export":
        payload = {"project_id": args.id}
    else:
        payload = {"video_url": args.url}
    
    target_lang = _resolve(args.target, "defaults.target", None)
    if target_lang:
        payload["target_lang"] = target_lang

    # ── Task-specific fields ──
    if task_type == "clip":
        _apply_clipping(payload, args)
    elif task_type == "search":
        _apply_moments(payload, args)
    elif task_type == "export":
        _apply_export(payload, args)

    # ── Submit ──
    try:
        project_id = client.submit_task(task_type, payload)
    except Exception as e:
        print(f"Submit failed: {e}", file=sys.stderr)
        sys.exit(1)
    
    id_label = "export_task_id" if task_type == "export" else "id"
    print(f"Submitted {task_type} task - {id_label}={project_id}", file=sys.stderr)

    # ── Decide whether to persist initial state ──
    if args.no_save:
        should_save = False
    elif args.save_dir:
        should_save = True
    else:
        should_save = _resolve(None, "save_results", True)

    output = {id_label: project_id}
    if should_save:
        save_dir = args.save_dir or _resolve(None, "save_dir", os.path.expanduser("~/.wayinvideo/cache"))
        if save_dir.startswith("~"):
            save_dir = os.path.expanduser(save_dir)
        path = _init_result_file(task_type, project_id, payload, save_dir)
        output["save_file"] = path
        print(f"Result file: {path}", file=sys.stderr)

    print(json.dumps(output))


# ── Payload builders ─────────────────────────────────────────────────────────

def _apply_export(payload, args):
    """Build payload for the standalone export API."""
    dk = "defaults.export"
    # clip_indices (comma-separated string to int list)
    if args.clip_indices:
        try:
            payload["clip_indices"] = [int(i.strip()) for i in args.clip_indices.split(",")]
        except ValueError:
            print("Error: --clip-indices must be comma-separated integers.", file=sys.stderr)
            sys.exit(1)

    # resolution
    res = _resolve(args.resolution, f"{dk}.resolution", "FHD_1080")
    if res:
        payload["resolution"] = res

    # ── Caption settings (logic inherited from clipping/moments) ──
    caption_display = _resolve(args.caption_display, f"{dk}.caption_display", None)
    if caption_display == "none":
        enable_caption = False
        caption_display = None
    elif caption_display:
        enable_caption = True
    else:
        # Default to True for export as well, matching clip/search logic
        enable_caption = True
        caption_display = "translation" if payload.get("target_lang") else "original"
    
    payload["enable_caption"] = enable_caption
    if enable_caption:
        payload["caption_display"] = caption_display
        
        # Default caption style logic
        cc_style_tpl = _resolve(args.cc_style_tpl, f"{dk}.cc_style_tpl", None)
        if cc_style_tpl is None:
            cc_style_tpl = "temp-static-2" if caption_display == "both" else "word-focus"

        if caption_display == "both" and not (cc_style_tpl and cc_style_tpl.startswith("temp-static-")):
            print(f"ERROR: `--cc-style-tpl` can only be `temp-static-...` when `--caption-display both`", file=sys.stderr)
            sys.exit(1)

        payload["cc_style_tpl"] = cc_style_tpl

    # AI hook
    enable_ai_hook = _resolve_flag(args, "ai_hook_flag", f"{dk}.ai_hook", True)
    payload["enable_ai_hook"] = enable_ai_hook
    if enable_ai_hook:
        payload["ai_hook_script_style"] = _resolve(args.ai_hook_style, f"{dk}.ai_hook_style", "serious")
        payload["ai_hook_position"]     = _resolve(args.ai_hook_pos, f"{dk}.ai_hook_pos", "beginning")
        if args.ai_hook_keywords:
            payload["ai_hook_keywords"] = args.ai_hook_keywords
        if args.ai_hook_text_duration:
            payload["ai_hook_text_duration"] = args.ai_hook_text_duration

    # AI reframe
    ratio = _resolve(args.ratio, f"{dk}.ratio", "RATIO_9_16")
    if ratio:
        payload["enable_ai_reframe"] = True
        payload["ratio"] = ratio
    else:
        # If explicitly set to None in config or somehow resolved to None,
        # we respect the API default (keeping original aspect ratio)
        payload["enable_ai_reframe"] = False


def _apply_clipping(payload, args):
    dk = "defaults.clip"
    
    export_enabled = _resolve_flag(args, "export_flag", f"{dk}.export", True)
    payload["enable_export"] = export_enabled
    
    # Determine caption setting
    caption_display = _resolve(args.caption_display, f"{dk}.caption_display", None)
    if caption_display == "none":
        enable_caption = False
        caption_display = None
    elif caption_display:
        enable_caption = True
    else:
        enable_caption = True
        caption_display = "translation" if payload.get("target_lang") else "original"
    
    payload["enable_caption"] = enable_caption
    
    # Resolve ratio first to determine AI reframe status
    ratio = _resolve(args.ratio, f"{dk}.ratio", "RATIO_9_16")
    if export_enabled:
        payload["enable_ai_reframe"] = ratio is not None
    else:
        payload["enable_ai_reframe"] = False

    duration = _resolve(getattr(args, "duration", None), f"{dk}.duration")
    if duration:
        payload["target_duration"] = duration

    top_k = _resolve(args.top_k, f"{dk}.top_k", 10)
    if top_k != -1:
        payload["limit"] = top_k

    if export_enabled:
        payload["ratio"]           = ratio
        payload["resolution"]      = _resolve(args.resolution, f"{dk}.resolution", "FHD_1080")
        payload["caption_display"] = caption_display
        
        # Default caption style logic
        cc_style_tpl = _resolve(args.cc_style_tpl, f"{dk}.cc_style_tpl", None)
        if cc_style_tpl is None:
            cc_style_tpl = "temp-static-2" if caption_display == "both" else "word-focus"

        if caption_display == "both" and not (cc_style_tpl and cc_style_tpl.startswith("temp-static-")):
            print(f"ERROR: `--cc-style-tpl` can only be `temp-static-...` when `--caption-display both`", file=sys.stderr)
            sys.exit(1)

        payload["cc_style_tpl"] = cc_style_tpl

        # AI Hook settings (only relevant when export is enabled)
        ai_hook_enabled = _resolve_flag(args, "ai_hook_flag", f"{dk}.ai_hook", False)
        payload["enable_ai_hook"] = ai_hook_enabled
        if ai_hook_enabled:
            payload["ai_hook_script_style"] = _resolve(args.ai_hook_style, f"{dk}.ai_hook_style", "serious")
            payload["ai_hook_position"]     = _resolve(args.ai_hook_pos, f"{dk}.ai_hook_pos", "beginning")


def _apply_moments(payload, args):
    if not args.query:
        print("Error: --query is required for 'search' task.", file=sys.stderr)
        sys.exit(1)

    dk = "defaults.search"
    payload["query"] = args.query
    
    export_enabled = _resolve_flag(args, "export_flag", f"{dk}.export", True)
    payload["enable_export"] = export_enabled
    
    # Determine caption setting
    caption_display = _resolve(args.caption_display, f"{dk}.caption_display", None)
    if caption_display == "none":
        enable_caption = False
        caption_display = None
    elif caption_display:
        enable_caption = True
    else:
        enable_caption = True
        caption_display = "translation" if payload.get("target_lang") else "original"
    
    payload["enable_caption"] = enable_caption
    
    # Resolve ratio first to determine AI reframe status
    ratio = _resolve(args.ratio, f"{dk}.ratio", "RATIO_9_16")
    if export_enabled:
        payload["enable_ai_reframe"] = ratio is not None
    else:
        payload["enable_ai_reframe"] = False

    top_k = _resolve(args.top_k, f"{dk}.top_k", 10)
    if top_k != -1:
        payload["limit"] = top_k

    if export_enabled:
        payload["ratio"]           = ratio
        payload["resolution"]      = _resolve(args.resolution, f"{dk}.resolution", "FHD_1080")
        payload["caption_display"] = caption_display
        
        # Default caption style logic
        cc_style_tpl = _resolve(args.cc_style_tpl, f"{dk}.cc_style_tpl", None)
        if cc_style_tpl is None:
            cc_style_tpl = "temp-static-2" if caption_display == "both" else "word-focus"

        if caption_display == "both" and not (cc_style_tpl and cc_style_tpl.startswith("temp-static-")):
            print(f"ERROR: `--cc-style-tpl` can only be `temp-static-...` when `--caption-display both`", file=sys.stderr)
            sys.exit(1)

        payload["cc_style_tpl"] = cc_style_tpl


def _build_export(args, dk):
    """Build the ``export_settings`` object."""
    return {
        "video_ratio":       _resolve(args.ratio, f"{dk}.ratio", "RATIO_9_16"),
        "video_res":         _resolve(args.resolution, f"{dk}.resolution", "FHD_1080"),
        "caption_display":   _resolve(args.caption_display, f"{dk}.caption_display", "original"),
        "cc_style_tpl":      _resolve(args.cc_style_tpl, f"{dk}.cc_style_tpl", "word-focus"),
        "enable_ai_reframe": args.ratio is not None,
    }


def _init_result_file(task_type, project_id, payload, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{task_type}_{project_id}.json"
    path = os.path.abspath(os.path.join(save_dir, name))
    now  = datetime.now().isoformat()

    # Non-sensitive data will be persisted for debugging; sensitive data such as API keys in environment variables will not be persisted.
    data = {
        "_metadata": {
            "id":                     project_id,
            "task_type":              task_type,
            "submit_payload":         payload,
            "api_endpoint":           SUBMIT_ENDPOINTS[task_type],
            "task_submitted_at":      now,
            "status":                 "ONGOING",
            "updated_at":             now,
            "task_finished_at":       None,
            "task_expires_at":        None,
            "export_links_expire_at": None,
        },
        "api_response": None,
    }
    _save_json(data, path)
    return path


def _update_metadata(meta, api_data):
    meta["status"]     = api_data.get("status", meta.get("status", "UNKNOWN"))
    meta["updated_at"] = datetime.now().isoformat()

    # ── expire_at: Unix timestamp → ISO ──
    raw_expire = api_data.get("expire_at")
    if raw_expire is not None:
        meta["task_expires_at"] = _ms_to_iso(raw_expire)

    # ── Terminal status ──
    if meta["status"] in TERMINAL_STATUSES:
        now = datetime.now()

        if not meta.get("task_finished_at"):
            meta["task_finished_at"] = now.isoformat()

        # export_links_expire_a: clip/search only, local now + 24h
        if (
            meta.get("task_type") in INCREMENTAL_TASKS
            and not meta.get("export_links_expire_at")
        ):
            meta["export_links_expire_at"] = (now + timedelta(hours=24)).isoformat()


# ══════════════════════════════════════════════════════════════════════════════
#  Command: poll
# ══════════════════════════════════════════════════════════════════════════════

def _cmd_poll(args):
    task_type  = args.type
    project_id = args.id

    timeout  = _resolve(args.timeout, "poll_timeout", 3600)
    interval = _resolve(args.interval, "poll_interval", 10)

    # ── Event interval resolution ──
    if args.event_interval is not None:
        event_interval = args.event_interval
    else:
        if cfg.get_value("event_enabled"):
            ei = cfg.get_value("event_interval")
            event_interval = ei if ei and ei > 0 else 60
        else:
            event_interval = 0

    # ── Save-file resolution ──
    save_file = None
    if not args.no_save:
        save_file = args.save_file
        if not save_file:
            sd = _resolve(None, "save_dir", os.path.expanduser("~/.wayinvideo/cache"))
            if sd.startswith("~"):
                sd = os.path.expanduser(sd)
            os.makedirs(sd, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_file = os.path.abspath(
                os.path.join(sd, f"{task_type}_{project_id}.json")
            )

    _poll_loop(task_type, project_id, save_file, timeout, interval, event_interval)


def _poll_loop(task_type, project_id, save_file, timeout, interval, event_interval):
    """Core blocking poll loop.

    * *save_file* = None  →  no-save mode (full JSON printed on completion).
    * Incremental tasks update the save file every cycle.
    * Final-only tasks update it once on SUCCEEDED.

    Save file structure:
        {
            "_metadata":    { id, task_type, submit_payload, status, ... },
            "api_response": { <raw API return> }
        }
    """
    start      = time.time()
    last_event = start
    state      = _load_json(save_file) if save_file else {}

    # ── Ensure _metadata exists (poll may start without a prior submit file) ──
    if "_metadata" not in state:
        state["_metadata"] = {
            "id":                     project_id,
            "task_type":              task_type,
            "api_endpoint":           SUBMIT_ENDPOINTS[task_type],
            "task_submitted_at":      None,
            "status":                 "ONGOING",
            "updated_at":             datetime.now().isoformat(),
            "task_finished_at":       None,
            "task_expires_at":        None,
            "export_links_expire_at": None,
        }
    if "api_response" not in state:
        state["api_response"] = None

    meta = state["_metadata"]

    while True:
        # ── timeout guard ──
        if time.time() - start > timeout:
            msg = f"⚠️ [{task_type}] {project_id} polling timeout ({timeout}s)"
            print(f"TIMEOUT: {msg}", file=sys.stderr)
            if event_interval > 0:
                _send_event(msg)
            sys.exit(2)

        # ── fetch ──
        try:
            data = client.fetch_results(task_type, project_id)
        except Exception as e:
            print(f"Poll error: {e} (retry in {interval}s)", file=sys.stderr)
            time.sleep(interval)
            continue

        status = data.get("status", "UNKNOWN")
        now    = time.time()

        # ── update metadata ──
        _update_metadata(meta, data)

        is_terminal = status in TERMINAL_STATUSES

        # ── incremental tasks (clip / search) ──
        if task_type in INCREMENTAL_TASKS:
            clips     = data.get("clips", [])
            old_resp  = state.get("api_response") or {}
            old_count = len(old_resp.get("clips", []))
            new_count = len(clips) - old_count

            # Always replace the full API response
            state["api_response"] = data

            if save_file:
                _save_json(state, save_file)

            if (
                new_count > 0
                and event_interval > 0
                and (now - last_event) >= event_interval
            ):
                emsg = f"🔔 [{task_type}] {project_id} +{new_count} (total {len(clips)})"
                if save_file:
                    emsg += f" → {os.path.abspath(save_file)}"
                _send_event(emsg)
                last_event = now

            print(
                f"[{task_type}] status={status}  clips={len(clips)}",
                file=sys.stderr,
            )

        # ── final-only tasks (summarize / transcribe) ──
        else:
            print(f"[{task_type}] status={status}", file=sys.stderr)

            if is_terminal:
                state["api_response"] = data
                if save_file:
                    _save_json(state, save_file)
            else:
                # Even before completion, persist metadata progress
                if save_file:
                    _save_json(state, save_file)

                if (
                    event_interval > 0
                    and (now - last_event) >= event_interval
                ):
                    _send_event(f"🔄 [{task_type}] {project_id} processing…")
                    last_event = now

        # ── terminal states ──
        if is_terminal:
            if event_interval > 0:
                emoji = "✅" if status != "FAILED" else "❌"
                emsg  = f"{emoji} [{task_type}] {project_id} {status.lower()}"
                if save_file:
                    emsg += f" → {os.path.abspath(save_file)}"
                _send_event(emsg)

            if save_file:
                print(json.dumps({
                    "status":    status,
                    "save_file": os.path.abspath(save_file),
                }))
            else:
                # no-save mode: print the full structured result
                print(json.dumps(state, ensure_ascii=False, indent=2))

            if status == "FAILED":
                sys.exit(1)
            return

        time.sleep(interval)


# ══════════════════════════════════════════════════════════════════════════════
#  Command: config
# ══════════════════════════════════════════════════════════════════════════════

def _cmd_config(args):
    action = args.action
    if not action:
        print(
            "Error: action required.\n"
            "  wayinvideo config {show|get|set|reset|path|keys}\n"
            "  wayinvideo config -h  for details",
            file=sys.stderr,
        )
        sys.exit(1)

    if action == "show":
        for line in cfg.format_tree(cfg.load_config()):
            print(line)

    elif action == "get":
        if not args.key:
            print("Error: 'get' requires a KEY argument.", file=sys.stderr)
            sys.exit(1)
        config = cfg.load_config()
        if not cfg.key_exists(config, args.key):
            print(f"Key not found: {args.key}", file=sys.stderr)
            sys.exit(1)
        val = cfg.get_nested(config, args.key)
        if isinstance(val, dict):
            for line in cfg.format_tree(val):
                print(line)
        else:
            print(json.dumps(val))

    elif action == "set":
        if not args.key or args.value is None:
            print("Error: 'set' requires KEY and VALUE.", file=sys.stderr)
            sys.exit(1)
        config = cfg.load_config()
        parsed = cfg.parse_value(args.value)
        cfg.set_nested(config, args.key, parsed)
        cfg.save_config(config)
        print(f"{args.key} = {json.dumps(parsed)}")

    elif action == "reset":
        cfg.save_config(copy.deepcopy(constants.DEFAULT_CONFIG))
        print("Configuration reset to defaults.")

    elif action == "path":
        print(cfg.CONFIG_FILE)

    elif action == "keys":
        for key, desc in sorted(CONFIG_KEYS_DOC.items()):
            print(f"  {key:45s}  {desc}")


# ══════════════════════════════════════════════════════════════════════════════
#  Argument parser
# ══════════════════════════════════════════════════════════════════════════════

def _build_parser():
    # ── top level ────────────────────────────────────────────────────────────
    top = argparse.ArgumentParser(
        prog="wayinvideo",
        description=textwrap.dedent("""\
            WayinVideo CLI - unified interface for WayinVideo APIs.

            Commands:
              upload    Upload a local video and obtain an identity token
              submit    Submit a processing task (ai-clipping / find-moments / video-summarization / video-transcription / export)
              poll      Poll for task results (supports incremental & final-only modes)
              config    View and manage persistent CLI settings

            Environment:
              WAYIN_API_KEY   Your WayinVideo API key (required for upload / submit / poll)
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    top.add_argument(
        "-v", "--version", action="version",
        version=f"wayinvideo {__version__}",
    )
    subs = top.add_subparsers(dest="command")

    # ── upload ───────────────────────────────────────────────────────────────
    p_up = subs.add_parser(
        "upload",
        help="Upload a local video file",
        description=textwrap.dedent("""\
            Upload a local video file to WayinVideo and receive a one-time
            identity token that can be used as --url in 'wayinvideo submit'.

            Constraints:
              • Max size : 5 GB
              • Formats  : MP4, AVI, MOV, WEBM

            stdout (JSON): {"identity": "<token>"}
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_up.add_argument(
        "--file-path", required=True, metavar="PATH",
        help="Path to the local video file",
    )
    p_up.set_defaults(func=_cmd_upload)

    # ── submit ───────────────────────────────────────────────────────────────
    p_sm = subs.add_parser(
        "submit",
        help="Submit a video processing task",
        description=textwrap.dedent("""\
            Submit a video processing task to WayinVideo.

            Choose a task type as a sub-command:
              clip           AI Clipping - auto-generate highlight clips
              search         Find Moments - natural-language scene search
              summarize      Summarisation - structured video summary
              transcribe     Transcription - audio-to-text
              export         Export - standalone rendering for clip/search results

            stdout (JSON): {"project_id": "…"[, "save_file": "…"]}
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sm_sub = p_sm.add_subparsers(dest="task_type", metavar="TASK_TYPE")

    # -- shared arg builders --

    def _common(p):
        """Add arguments shared across all task types."""
        p.add_argument(
            "--url", required=True, metavar="URL",
            help="Video URL or identity token from 'wayinvideo upload'",
        )
        p.add_argument(
            "--target", metavar="LANG", choices=SUPPORTED_LANGUAGES,
            help="Target language code, e.g. en, zh, ja",
        )
        sg = p.add_mutually_exclusive_group()
        sg.add_argument(
            "--save-dir", metavar="DIR",
            help="Directory for the result JSON file (overrides config save_dir)",
        )
        sg.add_argument(
            "--no-save", action="store_true",
            help="Do not persist result to file",
        )

    def _export(p):
        """Add export / rendering arguments (clipping & moments only)."""
        eg = p.add_mutually_exclusive_group()
        eg.add_argument(
            "--export", dest="export_flag",
            action="store_const", const=True, default=None,
            help="Enable video rendering / export",
        )
        eg.add_argument(
            "--no-export", dest="export_flag",
            action="store_const", const=False,
            help="Disable rendering (overrides config default)",
        )
        p.add_argument(
            "--top-k", type=int, metavar="N",
            help="Number of results to return (default: config or 10)",
        )
        p.add_argument(
            "--ratio", choices=RATIO_CHOICES, metavar="RATIO",
            help="Aspect ratio for export. Values: "
                 + ", ".join(RATIO_CHOICES),
        )
        p.add_argument(
            "--resolution", choices=RESOLUTION_CHOICES, metavar="RES",
            help="Video resolution for export. Values: "
                 + ", ".join(RESOLUTION_CHOICES),
        )
        p.add_argument(
            "--caption-display", choices=CAPTION_DISPLAY_CHOICES, metavar="MODE",
            help="Caption display mode. Values: "
                 + ", ".join(CAPTION_DISPLAY_CHOICES),
        )
        p.add_argument(
            "--cc-style-tpl", metavar="ID",
            help="Caption style template ID (default: config or word-focus)",
        )

    def _ai_hook(p):
        """Add AI hook arguments (clipping only)."""
        ag = p.add_mutually_exclusive_group()
        ag.add_argument(
            "--ai-hook", dest="ai_hook_flag",
            action="store_const", const=True, default=None,
            help="Enable automatically generated text hooks",
        )
        ag.add_argument(
            "--no-ai-hook", dest="ai_hook_flag",
            action="store_const", const=False,
            help="Disable text hooks (overrides config default)",
        )
        p.add_argument(
            "--ai-hook-style", dest="ai_hook_style",
            choices=AI_HOOK_SCRIPT_STYLE_CHOICES, metavar="STYLE",
            help="Style of the generated hook text. Values: "
                 + ", ".join(AI_HOOK_SCRIPT_STYLE_CHOICES),
        )
        p.add_argument(
            "--ai-hook-pos", dest="ai_hook_pos",
            choices=AI_HOOK_POSITION_CHOICES, metavar="POS",
            help="Position of the generated hook text. Values: "
                 + ", ".join(AI_HOOK_POSITION_CHOICES),
        )

    # -- clip --
    p_cl = sm_sub.add_parser(
        "clip",
        help="AI Clipping - auto-generate highlight clips",
        description=textwrap.dedent("""\
            Submit an AI Clipping task.

            Analyses the video and produces highlight clips ranked by
            relevance and virality.  When --export is enabled, clips are
            rendered with the specified ratio / resolution / captions.

            Configurable defaults (wayinvideo config set defaults.clip.<key> <value>):
              top_k, duration, export, ratio, resolution, caption_display, cc_style_tpl
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _common(p_cl)
    _export(p_cl)
    _ai_hook(p_cl)
    p_cl.add_argument(
        "--duration", choices=DURATION_CHOICES, metavar="DUR",
        help="Target clip duration range. Values: "
             + ", ".join(DURATION_CHOICES),
    )
    p_cl.set_defaults(func=_cmd_submit)

    # -- search --
    p_mo = sm_sub.add_parser(
        "search",
        help="Find Moments - natural-language scene search",
        description=textwrap.dedent("""\
            Submit a Find Moments task.

            Searches the video for segments matching a natural-language query.
            --query is required.

            When --export is enabled, matched moments are rendered with the
            specified video settings.

            Configurable defaults (wayinvideo config set defaults.search.<key> <value>):
              top_k, export, ratio, resolution, caption_display, cc_style_tpl
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _common(p_mo)
    _export(p_mo)
    p_mo.add_argument(
        "--query", required=True, metavar="TEXT",
        help="Natural-language search query (required)",
    )
    p_mo.set_defaults(func=_cmd_submit)

    # -- summarize --
    p_su = sm_sub.add_parser(
        "summarize",
        help="Summarisation - structured video summary",
        description=textwrap.dedent("""\
            Submit a Video Summarisation task.

            Generates a structured summary of the video contents.
            Results are only available upon task SUCCEEDED (no incremental updates).
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _common(p_su)
    p_su.set_defaults(func=_cmd_submit)

    # -- transcribe --
    p_tr = sm_sub.add_parser(
        "transcribe",
        help="Transcription - audio to text",
        description=textwrap.dedent("""\
            Submit a Video Transcription task.

            Transcribes the audio track of the video to text.
            Results are only available upon task SUCCEEDED (no incremental updates).
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _common(p_tr)
    p_tr.set_defaults(func=_cmd_submit)

    # -- export --
    p_ex = sm_sub.add_parser(
        "export",
        help="Export - standalone rendering for clip/search results",
        description=textwrap.dedent("""\
            Submit an export task to render or re-export clips from an existing task.
            Required: --id from a prior clip or search task.

            Allows changing aspect ratio, resolution, captions, and AI hooks.
            Results are delivered incrementally via 'poll --type export'.

            Example:
              wayinvideo submit export --id <id> --clip-indices 0,2 --ratio RATIO_9_16
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_ex.add_argument(
        "--id", required=True, metavar="ID",
        help="The original AI Clipping or Find Moments task ID",
    )
    p_ex.add_argument(
        "--clip-indices", metavar="LIST",
        help="Comma-separated clip indices to export (default: all)",
    )
    p_ex.add_argument(
        "--target", metavar="LANG", choices=SUPPORTED_LANGUAGES,
        help="Target language code for output subtitles",
    )
    _export(p_ex)
    _ai_hook(p_ex)
    p_ex.add_argument(
        "--ai-hook-keywords", metavar="TEXT",
        help="Keywords to steer AI hook generation",
    )
    p_ex.add_argument(
        "--ai-hook-text-duration", type=int, metavar="MS",
        help="Duration of the AI hook text overlay in milliseconds",
    )
    sg_ex = p_ex.add_mutually_exclusive_group()
    sg_ex.add_argument(
        "--save-dir", metavar="DIR",
        help="Directory for the result JSON file",
    )
    sg_ex.add_argument(
        "--no-save", action="store_true",
        help="Do not persist result to file",
    )
    p_ex.set_defaults(func=_cmd_submit)

    # ── poll ─────────────────────────────────────────────────────────────────
    p_po = subs.add_parser(
        "poll",
        help="Poll for task results",
        description=textwrap.dedent("""\
            Poll WayinVideo for the results of a submitted task.

            Behaviour by task type:
              • clip / search / export  Results arrive incrementally while
                                        ONGOING. The save file is updated
                                        every poll cycle.
              • summarize / transcribe  Results appear only on SUCCEEDED.
                                        The save file is written once.

            The command blocks until SUCCEEDED / FAILED or --timeout, then exits.

            stdout on completion:
              Save mode   : {"status": "…", "save_file": "…"}
              --no-save   : full result JSON
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_po.add_argument(
        "--type", required=True, choices=TASK_TYPES,
        help="Task type",
    )
    p_po.add_argument(
        "--id", required=True, metavar="ID",
        help="The task ID returned by submit",
    )
    pg = p_po.add_mutually_exclusive_group()
    pg.add_argument(
        "--save-file", metavar="PATH",
        help="Result JSON file to read/write (auto-generated if omitted)",
    )
    pg.add_argument(
        "--no-save", action="store_true",
        help="Do not save to file; print full result JSON to stdout",
    )
    p_po.add_argument(
        "--timeout", type=int, metavar="SEC",
        help="Max polling duration in seconds (default: config or 3600)",
    )
    p_po.add_argument(
        "--interval", type=int, metavar="SEC",
        help="Seconds between API requests (default: config or 10)",
    )
    p_po.add_argument(
        "--event-interval", type=int, metavar="SEC",
        help="Min seconds between system event notifications; 0 disables (default: config)",
    )
    p_po.set_defaults(func=_cmd_poll)

    # ── config ───────────────────────────────────────────────────────────────
    p_cf = subs.add_parser(
        "config",
        help="View and manage CLI configuration",
        description=textwrap.dedent("""\
            View and manage persistent WayinVideo CLI settings.

            Actions:
              show             Display all current settings
              get  <key>       Display a single setting
              set  <key> <v>   Write a setting (type auto-detected: bool/int/str)
              reset            Restore every setting to built-in defaults
              path             Print config file location
              keys             List all recognised config keys with descriptions

            Keys use dot-notation for nested values:
              wayinvideo config set defaults.clipping.top_k 5
              wayinvideo config get poll_timeout

            Config file: ~/.wayinvideo/config.json
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_cf.add_argument(
        "action", nargs="?",
        choices=["show", "get", "set", "reset", "path", "keys"],
        help="Config action to perform",
    )
    p_cf.add_argument("key",   nargs="?", metavar="KEY",   help="Config key (dot notation)")
    p_cf.add_argument("value", nargs="?", metavar="VALUE", help="New value (for 'set')")
    p_cf.set_defaults(func=_cmd_config)

    return top


# ══════════════════════════════════════════════════════════════════════════════
#  Entry-point
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = _build_parser()
    args   = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    func = getattr(args, "func", None)
    if func:
        func(args)
    else:
        # e.g. `wayinvideo submit` with no task type → show submit help
        parser.parse_args([args.command, "-h"])
