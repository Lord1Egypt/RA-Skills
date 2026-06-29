#!/usr/bin/env python3
"""
skill-sediment installer / operator -- deploy the OpenClaw auto-sediment plugin
to any OpenClaw pod.

Subcommands:
  install    Full install (deploy plugin to convention dir -> auto-load when allow
             is empty, append whitelist when non-empty -> restart prompt)
  config     Print current plugins.allow state and recommended action
  doctor     Diagnose: plugin files / config / version / whether plugin loaded /
             sediment_skills directory
  heal       Self-repair: detect and fix whitelist/file loss, supplement missing
             validAgentId, auto-restart gateway
  recover    Restore after pod restart (plugin present -> OK; PVC volume swapped
             -> redeploy)
  status     Inspect sediment pool (pending incubations / activated promotions)
  uninstall  Remove plugin dir (+ optionally clean openclaw.json whitelist entries)

Design constraints:
  - Plugin is extracted to the workspace convention directory
    <workspace>/.openclaw/extensions/skill-sediment/
    (OpenClaw auto-discovers this dir; when plugins.allow is empty, no
     openclaw.json change is needed)
  - All paths use env var overrides with universal fallbacks (multi-pod friendly)
  - Managed pods (Lobi/Apollo) are auto-detected via env signals; writes still go
    to local openclaw.json, with a note that pod rebuild may require re-install
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants & paths (all env-overridable, multi-pod friendly)
# ---------------------------------------------------------------------------

PLUGIN_NAME = "skill-sediment"

# Plugin source bundle CDN (optional fallback).
# Normal distribution: the plugin tarball is bundled inside this skill's assets/
# directory and used directly (offline install). This URL is only consulted if
# the bundled tarball is missing.
CDN_PLUGIN_TARGZ = os.environ.get("SKILL_SEDIMENT_CDN", "").strip()
# Optional sha256 checksum for the downloaded bundle (recommended when the user
# supplies a custom CDN URL).
EXPECTED_SHA256 = os.environ.get("SKILL_SEDIMENT_SHA256", "").strip()

# Resolve HOME via $HOME env var (fallback to expanduser) so we honour the
# real user's home even when running under sudo/su. Avoids hardcoding /home/node.
HOME = Path(os.environ.get("HOME") or os.path.expanduser("~"))
WORKSPACE = Path(
    os.environ.get("OPENCLAW_WORKSPACE", str(HOME / ".openclaw" / "workspace"))
)

# Plugin convention directory (auto-discovered by OpenClaw):
#   <workspace>/.openclaw/extensions/<plugin-name>/
# When plugins.allow is empty, the plugin auto-loads from here -- no openclaw.json
# change required. The directory sits inside the workspace (typically PVC-mounted),
# surviving container restart / PVC volume swap.
EXTENSION_DIR = WORKSPACE / ".openclaw" / "extensions" / PLUGIN_NAME

# openclaw.json path (only needed when plugins.allow is non-empty and we must
# append our plugin name to the whitelist).
OPENCLAW_JSON = Path(
    os.environ.get("OPENCLAW_CONFIG", str(HOME / ".openclaw" / "openclaw.json"))
)

# Verified OpenClaw baseline version (used by install for compatibility check)
BASELINE_VERSION = "2026.3.8"
# OpenClaw core package.json (read to determine the target's version)
CORE_PACKAGE_JSON = Path(os.environ.get("OPENCLAW_CORE_PKG", "/app/package.json"))
# plugin-sdk presence check
PLUGIN_SDK_DIR = Path(os.environ.get("OPENCLAW_PLUGIN_SDK", "/app/dist/plugin-sdk"))

# The 6 plugin hook events (used in doctor diagnostics output)
REQUIRED_HOOKS = [
    "llm_input",
    "llm_output",
    "session_end",
    "before_reset",
    "agent_end",
    "subagent_ended",
]

ENTRY_FILE = "index.ts"  # Entry file expected after extraction

# Managed-environment signals: when any of these is set, the platform is likely
# to overwrite local openclaw.json from a remote config source. Examples:
#  - Lobi (clawbot* / LOBI_SYNC_ENABLED) syncs from a remote control plane
#  - Apollo (config-guard-service) periodically reconciles ~16s after gateway start
# Pure "write-then-read-back" detection cannot catch these reliably, so we
# pre-detect via env vars before deciding whether to write the local file.
MANAGED_ENV_FLAGS = [
    "LOBI_SYNC_ENABLED",  # Lobi platform sync switch
    "APOLLO_META",        # Apollo config center
    "APOLLO_APP_ID",
]


def detect_managed_env():
    """Return (is_managed, reason). When managed signals are detected, writing
    local openclaw.json is unreliable -- prefer the remote config plane."""
    # 1. Explicit sync switch
    val = os.environ.get("LOBI_SYNC_ENABLED", "").strip().lower()
    if val in ("1", "true", "yes"):
        return (True, f"Lobi-managed (LOBI_SYNC_ENABLED={val})")
    # 2. Lobi clawbot* APPID
    appid = os.environ.get("APPID", "").strip()
    if appid.startswith("clawbot"):
        return (True, f"Lobi-managed (APPID={appid})")
    # 3. Apollo signals
    for f in ("APOLLO_META", "APOLLO_APP_ID"):
        if os.environ.get(f, "").strip():
            return (True, f"Apollo-managed ({f} is set)")
    return (False, "")


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def log(msg):
    print(f"▶ {msg}")


def ok(msg):
    print(f"✅ {msg}")


def warn(msg):
    print(f"⚠️  {msg}")


def err(msg):
    print(f"❌ {msg}", file=sys.stderr)


def hr():
    print("═" * 50)


# ---------------------------------------------------------------------------
# Version check
# ---------------------------------------------------------------------------

def parse_version(v):
    """'2026.3.8' -> (2026, 3, 8); returns None on parse failure"""
    try:
        return tuple(int(x) for x in str(v).strip().split("."))
    except Exception:
        return None


def get_core_version():
    try:
        d = json.loads(CORE_PACKAGE_JSON.read_text())
        return d.get("version")
    except Exception:
        return None


def check_version():
    """Return (level, version, message); level in {'ok','higher','lower','unknown'}"""
    v = get_core_version()
    if not v:
        return ("unknown", None, "Cannot read OpenClaw version (/app/package.json unreadable)")
    cur = parse_version(v)
    base = parse_version(BASELINE_VERSION)
    if cur is None or base is None:
        return ("unknown", v, f"Cannot parse version: {v}")
    if cur == base:
        return ("ok", v, f"Version {v} matches the verified baseline -- best compatibility")
    if cur > base:
        return (
            "higher",
            v,
            f"Version {v} is above baseline {BASELINE_VERSION} -- likely compatible; smoke test will run after install",
        )
    return (
        "lower",
        v,
        f"Version {v} is below baseline {BASELINE_VERSION} -- may lack required APIs; install not recommended",
    )


def check_plugin_sdk():
    return PLUGIN_SDK_DIR.exists()


# ---------------------------------------------------------------------------
# Download & extract
# ---------------------------------------------------------------------------

def is_placeholder(url):
    return (not url) or url.startswith("PLACEHOLDER")


def download_plugin(dest_targz):
    if is_placeholder(CDN_PLUGIN_TARGZ):
        err(
            "Plugin file missing; bundled assets/ tarball unavailable and no CDN fallback configured.\n"
            "   Normally the plugin tarball sits at <skill>/assets/skill-sediment-ext.tar.gz.\n"
            "   If the bundled tarball is lost, set SKILL_SEDIMENT_CDN=<URL> to point at a fallback download."
        )
        return False
    log(f"Downloading plugin bundle from CDN... ({CDN_PLUGIN_TARGZ[:60]}...)")
    try:
        req = urllib.request.Request(
            CDN_PLUGIN_TARGZ, headers={"User-Agent": "skill-sediment-installer"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp, open(
            dest_targz, "wb"
        ) as f:
            shutil.copyfileobj(resp, f)
    except Exception as e:
        err(f"Download failed: {e}")
        return False

    if EXPECTED_SHA256:
        import hashlib

        h = hashlib.sha256(Path(dest_targz).read_bytes()).hexdigest()
        if h != EXPECTED_SHA256:
            err(f"sha256 mismatch: expected {EXPECTED_SHA256}, got {h}")
            return False
        ok("sha256 verified")
    ok(f"Plugin bundle downloaded: {dest_targz}")
    return True


def extract_plugin(targz):
    log(f"Extracting plugin to {EXTENSION_DIR} ...")
    EXTENSION_DIR.mkdir(parents=True, exist_ok=True)
    # Safe extraction: reject path traversal
    with tarfile.open(targz, "r:gz") as tar:
        for member in tar.getmembers():
            target = (EXTENSION_DIR / member.name).resolve()
            if not str(target).startswith(str(EXTENSION_DIR.resolve())):
                err(f"Refused traversal extraction: {member.name}")
                return False
        tar.extractall(EXTENSION_DIR)
    if not (EXTENSION_DIR / ENTRY_FILE).exists():
        err(f"Entry file {ENTRY_FILE} missing after extraction -- bundle structure looks wrong")
        return False
    ok(f"Plugin extracted (entry {ENTRY_FILE} present)")
    return True


def local_bundled_plugin_dir():
    """Prefer the skill's bundled `assets/plugin-source/` directory (flat-file
    distribution, friendly to hubs that whitelist file types and reject .tar.gz).
    Returns the directory path if it contains the entry file, else None."""
    here = Path(__file__).resolve().parent.parent
    src_dir = here / "assets" / "plugin-source"
    if src_dir.is_dir() and (src_dir / ENTRY_FILE).exists():
        return src_dir
    return None


def local_bundled_plugin_tarball():
    """Legacy fallback: bundled tarball form (`assets/skill-sediment-ext.tar.gz`).
    Older builds shipped this; new open-source builds prefer the flat directory."""
    here = Path(__file__).resolve().parent.parent
    bundled = here / "assets" / "skill-sediment-ext.tar.gz"
    return bundled if bundled.exists() else None


def copy_plugin_dir(src_dir):
    """Copy plugin source from a flat directory into EXTENSION_DIR. Returns bool."""
    log(f"Copying plugin source from {src_dir} → {EXTENSION_DIR}")
    try:
        # Remove existing dir to avoid stale files mixing
        if EXTENSION_DIR.exists():
            shutil.rmtree(EXTENSION_DIR)
        shutil.copytree(src_dir, EXTENSION_DIR)
    except Exception as e:
        err(f"Failed to copy plugin source: {e}")
        return False
    if not (EXTENSION_DIR / ENTRY_FILE).exists():
        err(f"Entry file {ENTRY_FILE} missing after copy -- source dir may be incomplete")
        return False
    ok(f"Plugin source copied (entry {ENTRY_FILE} present)")
    return True


def ensure_plugin_files():
    """Ensure plugin files are in place. Order of preference:
      1. Already present in EXTENSION_DIR → skip
      2. Bundled flat dir `assets/plugin-source/` (recommended; hub-friendly)
      3. Legacy bundled tarball `assets/skill-sediment-ext.tar.gz`
      4. CDN fallback (only if SKILL_SEDIMENT_CDN is set)
    """
    if (EXTENSION_DIR / ENTRY_FILE).exists():
        ok("Plugin files already present; skipping download")
        return True
    EXTENSION_DIR.parent.mkdir(parents=True, exist_ok=True)

    # Path 2: flat directory (preferred)
    bundled_dir = local_bundled_plugin_dir()
    if bundled_dir:
        return copy_plugin_dir(bundled_dir)

    # Path 3: legacy tarball (older bundles)
    bundled_targz = local_bundled_plugin_tarball()
    tmp_dir = EXTENSION_DIR.parent
    tmp_dir.mkdir(parents=True, exist_ok=True)
    targz = tmp_dir / "skill-sediment-ext.tar.gz"
    if bundled_targz:
        log(f"Using legacy bundled tarball: {bundled_targz}")
        shutil.copy(bundled_targz, targz)
        EXTENSION_DIR.mkdir(parents=True, exist_ok=True)
        return extract_plugin(targz)

    # Path 4: CDN
    EXTENSION_DIR.mkdir(parents=True, exist_ok=True)
    if not download_plugin(targz):
        return False
    return extract_plugin(targz)


# ---------------------------------------------------------------------------
# openclaw.json config patching
# ---------------------------------------------------------------------------

def build_config_patch(valid_agent_id):
    """Return the 3 config fragments to append (used by both apply and diff)."""
    return {
        "allow_add": PLUGIN_NAME,
        "load_path_add": str(EXTENSION_DIR),
        "entry": {
            PLUGIN_NAME: {
                "enabled": True,
                "config": {"validAgentId": valid_agent_id},
            }
        },
    }


def read_config():
    try:
        return json.loads(OPENCLAW_JSON.read_text())
    except FileNotFoundError:
        # Quiet: callers handle the None return; doctor/config/etc print their own message
        return None
    except Exception as e:
        err(f"Failed to read {OPENCLAW_JSON}: {e}")
        return None


def apply_config(cfg, patch):
    """Idempotently append the 3 fragments; return whether anything actually changed."""
    plugins = cfg.setdefault("plugins", {})
    changed = False

    allow = plugins.setdefault("allow", [])
    if patch["allow_add"] not in allow:
        allow.append(patch["allow_add"])
        changed = True

    load = plugins.setdefault("load", {})
    paths = load.setdefault("paths", [])
    if patch["load_path_add"] not in paths:
        paths.append(patch["load_path_add"])
        changed = True

    entries = plugins.setdefault("entries", {})
    if entries.get(PLUGIN_NAME) != patch["entry"][PLUGIN_NAME]:
        entries[PLUGIN_NAME] = patch["entry"][PLUGIN_NAME]
        changed = True

    return changed


def config_already_applied(cfg, patch):
    plugins = cfg.get("plugins", {})
    allow = plugins.get("allow", [])
    paths = plugins.get("load", {}).get("paths", [])
    entries = plugins.get("entries", {})
    return (
        patch["allow_add"] in allow
        and patch["load_path_add"] in paths
        and entries.get(PLUGIN_NAME, {}).get("enabled") is True
    )


# clawconfig source file paths (sync-config-fields.sh uses these as the source
# of truth when the gateway restarts)
CLAWCONFIG_SOURCES = [
    Path("/app/clawconfig/openclaw.json"),
    Path("/app/k8s-config/clawconfig/openclaw.json"),
]
# Sync only these three sub-fields -- do not replace `plugins` wholesale,
# to preserve other fields in clawconfig (slots/installs/etc.)
CLAWCONFIG_SYNC_KEYS = ["allow", "load", "entries"]


def sync_plugins_to_clawconfig(runtime_cfg):
    """Sync the runtime openclaw.json `plugins.allow/load/entries` into the
    clawconfig source files. Only those three sub-fields are touched -- the
    rest of `plugins` (slots/installs/etc.) is preserved.
    """
    rt_plugins = runtime_cfg.get("plugins", {})
    for src in CLAWCONFIG_SOURCES:
        if not src.exists():
            continue
        try:
            src_cfg = json.loads(src.read_text())
            src_plugins = src_cfg.setdefault("plugins", {})
            for k in CLAWCONFIG_SYNC_KEYS:
                if k in rt_plugins:
                    src_plugins[k] = rt_plugins[k]
            src.write_text(json.dumps(src_cfg, indent=2, ensure_ascii=False) + "\n")
            ok(f"Synced plugins to {src.name}")
        except Exception as e:
            warn(f"Sync to {src} failed: {e}")


def ensure_clawconfig_allow():
    """Append PLUGIN_NAME directly to plugins.allow in both clawconfig files.
    Does not depend on runtime state, preventing loss when the ConfigMap is
    re-pushed by the platform and the gateway restarts.
    """
    for src in CLAWCONFIG_SOURCES:
        if not src.exists():
            continue
        try:
            src_cfg = json.loads(src.read_text())
            allow = src_cfg.setdefault("plugins", {}).setdefault("allow", [])
            if PLUGIN_NAME not in allow:
                allow.append(PLUGIN_NAME)
                src.write_text(json.dumps(src_cfg, indent=2, ensure_ascii=False) + "\n")
                log(f"Ensured {src.name} allow contains {PLUGIN_NAME}")  # Print only when changed
        except Exception as e:
            warn(f"ensure_clawconfig_allow {src} failed: {e}")




def remove_clawconfig_allow():
    """Remove PLUGIN_NAME from plugins.allow in both clawconfig files (called by uninstall)."""  # L3
    for src in CLAWCONFIG_SOURCES:
        if not src.exists():
            continue
        try:
            src_cfg = json.loads(src.read_text())
            allow = src_cfg.get("plugins", {}).get("allow", [])
            if PLUGIN_NAME in allow:
                allow.remove(PLUGIN_NAME)
                src.write_text(json.dumps(src_cfg, indent=2, ensure_ascii=False) + "\n")
                log(f"Removed {PLUGIN_NAME} from {src.name} allow")
        except Exception as e:
            warn(f"remove_clawconfig_allow {src} failed: {e}")


def print_config_guide(patch, managed_reason=""):
    """Print reference config to sync into the remote control plane for managed
    setups (purely informational; install has already written local)."""
    hr()
    print("📋 Plugin config reference (sync to a remote control plane for permanent persistence):\n")
    print("[1] Append to the plugins.allow array:")
    print(f'    "{patch["allow_add"]}"\n')
    print("[2] Append to the plugins.load.paths array:")
    print(f'    "{patch["load_path_add"]}"\n')
    print("[3] Append a config block to plugins.entries:")
    print(json.dumps(patch["entry"], indent=4, ensure_ascii=False))
    hr()
    if managed_reason:
        print(f"i️  This pod is a managed environment: {managed_reason}")
    print(
        "💡 install has written to local openclaw.json; restart the gateway to take effect.\n"
        "   On pod rebuild the remote config will overwrite local; re-run install after rebuild.\n"
        "   For permanent persistence, sync the configuration above to your remote control plane (Lobi / Apollo / etc.)."
    )


# Read-back detection window (seconds). Lobi can overwrite up to ~16s after
# write, so we extend to 20s as a fallback; but the primary judgement is via
# detect_managed_env() up-front -- read-back only catches unknown managed setups.
APOLLO_DETECT_WAIT_S = int(os.environ.get("SKILL_SEDIMENT_DETECT_WAIT", "20"))


def write_config_with_apollo_detect(cfg, patch):
    """Write the config file and detect whether a managed system overwrites it.
    Returns 'written' / 'overwritten' / 'failed'.

    Strategy:
      - Known managed env (Lobi/Apollo): write directly, skip read-back
        (the user is informed that pod rebuild will lose the change)
      - Unknown env: write then poll read-back to catch unknown managed setups
    """
    is_managed, reason = detect_managed_env()
    if is_managed:
        warn(f"Managed environment detected: {reason}")
        warn("Writing to local openclaw.json (pod rebuild will overwrite; re-run install after rebuild)")

    # Actually write to disk
    try:
        if OPENCLAW_JSON.exists():
            # Don't accumulate backups in managed envs; only back up in unmanaged envs
            if not is_managed:
                bak = OPENCLAW_JSON.with_suffix(f".json.bak.{int(time.time())}")
                shutil.copy(OPENCLAW_JSON, bak)
                log(f"Backed up original config → {bak.name}")
        OPENCLAW_JSON.write_text(
            json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"
        )
        ok("openclaw.json written")
    except Exception as e:
        err(f"Write failed: {e}")
        return "failed"

    # Known managed env: skip read-back, return 'written' directly
    if is_managed:
        return "written"

    # Unknown env: poll read-back as fallback (covers unknown managed systems + ~16s overwrite window)
    log(f"Watching to see if a remote system overwrites the config (max {APOLLO_DETECT_WAIT_S}s)...")
    waited = 0
    interval = 4
    while waited < APOLLO_DETECT_WAIT_S:
        time.sleep(interval)
        waited += interval
        recheck = read_config()
        if recheck is None:
            continue
        if not config_already_applied(recheck, patch):
            warn(f"At t={waited}s the config was cleared → detected as managed pod (remote overwrite)")
            return "overwritten"
    ok(f"Config still present after {APOLLO_DETECT_WAIT_S}s (unmanaged, or no overwrite triggered)")
    return "written"


# ---------------------------------------------------------------------------
# Subcommand implementations
# ---------------------------------------------------------------------------

def get_allow_list():
    """Return the current plugins.allow list from openclaw.json, or None on read failure."""
    cfg = read_config()
    if cfg is None:
        return None
    return cfg.get("plugins", {}).get("allow", [])


def ensure_allow_contains(plugin_name, valid_agent_id):
    """
    When plugins.allow is non-empty and does not contain plugin_name, append it and write back.
    Returns one of: 'empty' (allow is empty -- convention-dir auto-load, no change needed) /
                    'already' (already in whitelist) / 'added' (appended) /
                    'managed' (managed env -- local write unreliable) / 'failed'.
    """
    cfg = read_config()
    if cfg is None:
        return "failed"
    allow = cfg.get("plugins", {}).get("allow", [])
    if not allow:
        return "empty"
    if plugin_name in allow:
        return "already"

    # allow is non-empty but missing this plugin → append it
    patch = build_config_patch(valid_agent_id)
    apply_config(cfg, patch)
    result = write_config_with_apollo_detect(cfg, patch)
    if result == "overwritten":
        return "managed"
    if result == "failed":
        return "failed"
    return "added"


def _prompt_valid_agent_id(default_value):
    """Interactively prompt the user to pick which agent ids should enable sediment.

    - List all local agents via `openclaw agents list`, skipping non-human
      agents (stt-runner, etc.)
    - Show the list; accept space/comma-separated input, or Enter for default
    - Return the final agent id string (comma-separated, e.g. "main" or "main,zhima")
    """
    # Fetch the local agent list
    SKIP_AGENTS = {"stt-runner"}   # Non-human agents -- skip sediment for these
    agents = []
    try:
        # Use `proc` to avoid shadowing the local `result`
        proc = subprocess.run(
            ["openclaw", "agents", "list"],
            capture_output=True, text=True, timeout=10
        )
        for line in proc.stdout.splitlines():
            line = line.strip()
            if line.startswith("- ") and "(" in line:
                agent_id = line[2:].split("(")[0].strip()
                # Real agent ids only contain lowercase letters, digits, and hyphens
                # Filter out config-warning noise like '- plugins.allow: ...'
                if agent_id and re.match(r'^[a-z0-9][a-z0-9\-]*$', agent_id) and agent_id not in SKIP_AGENTS:
                    agents.append(agent_id)
    except Exception:
        pass

    # When we cannot read the agent list, fall back to default (don't block)
    if not agents:
        warn("Cannot read local agent list -- falling back to default: main")
        return default_value

    hr()
    print("🤖 Pick which agents should enable skill auto-sediment:")
    print()
    for i, a in enumerate(agents, 1):
        marker = "  [default]" if a == "main" else ""
        print(f"  {i}. {a}{marker}")
    print()
    print(f"  Enter → main only (recommended)")
    print(f"  Enter numbers or agent ids; separate multiples with space or comma (e.g. 1 3 or main,zhima)")
    print()
    try:
        raw = input("  Your choice: ").strip()
    except (EOFError, KeyboardInterrupt):
        raw = ""

    if not raw:
        ok(f"Using default: main")
        return "main"

    # Parse input: accept both numbers (1 2 3) and ids (main,zhima), mixed
    chosen = []
    for token in raw.replace(",", " ").split():
        token = token.strip()
        if token.isdigit():
            idx = int(token) - 1
            if 0 <= idx < len(agents):
                chosen.append(agents[idx])
            else:
                warn(f"Number {token} out of range -- skipping")
        elif token in agents:
            chosen.append(token)
        else:
            warn(f"Unknown agent '{token}' -- skipping")

    if not chosen:
        warn("No valid agent selected -- falling back to default: main")
        return "main"

    # Dedupe while preserving order
    seen = set()
    deduped = [a for a in chosen if not (a in seen or seen.add(a))]
    result_str = ",".join(deduped)
    ok(f"Selected: {result_str}")
    return result_str


def cmd_install(args):
    hr()
    print("🚀 skill-sediment install")
    hr()

    # 1. Environment self-check
    level, ver, msg = check_version()
    if level == "lower":
        err(msg)
        print("Pass --force-version to install anyway")
        if not args.force_version:
            return 1
    elif level == "higher":
        warn(msg)
    else:
        ok(msg)

    if not check_plugin_sdk():
        warn(
            f"plugin-sdk not found at {PLUGIN_SDK_DIR} -- the target may not be a standard OpenClaw image; the plugin may fail to load"
        )

    # 2. Deploy plugin file to the convention dir
    #    <workspace>/.openclaw/extensions/skill-sediment/
    log(f"Target directory: {EXTENSION_DIR}")
    if not ensure_plugin_files():
        return 1

    # 3. Interactively pick validAgentId (only when stdin is a TTY)
    #    - If --valid-agent-id was passed explicitly → use it, skip prompt
    #    - Otherwise → show the local agent list and prompt the user
    # Detect explicit user input via sentinel rather than default-value comparison.
    # argparse already set default to env/"main"; compare namespace against the
    # reconstructed default to be certain.
    _default_va = os.environ.get("SKILL_SEDIMENT_AGENTS", "main")
    explicitly_set = "--valid-agent-id" in sys.argv
    cfg_existing = read_config()
    current_va = (
        cfg_existing.get("plugins", {}).get("entries", {})
        .get(PLUGIN_NAME, {}).get("config", {}).get("validAgentId")
        if cfg_existing else None
    )

    if explicitly_set:
        # User passed --valid-agent-id explicitly -- use it
        valid_agent = args.valid_agent_id
        log(f"validAgentId (from --valid-agent-id): {valid_agent}")
    elif current_va:
        # Existing config detected → show it and ask whether to modify
        print(f"\n  Current validAgentId config: {current_va}")
        try:
            change = input("  Modify it? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            change = "n"
        if change == "y":
            valid_agent = _prompt_valid_agent_id("main")
        else:
            valid_agent = current_va
            ok(f"Keeping existing config: {valid_agent}")
    else:
        # Fresh install -- prompt the user to pick
        valid_agent = _prompt_valid_agent_id("main")

    # 4. Whitelist check
    #    - allow is empty → OpenClaw auto-loads from the convention dir, no openclaw.json change needed
    #    - allow is non-empty but missing this plugin → append it
    #    - Managed pod → direct user to add it via the remote console
    allow_result = ensure_allow_contains(PLUGIN_NAME, valid_agent)

    hr()
    if allow_result == "empty":
        ok(
            "plugins.allow is empty → OpenClaw auto-loads everything in the convention dir; "
            "no openclaw.json change needed ✨"
        )
        print(
            f"  Convention dir: {EXTENSION_DIR}\n"
            "  (When allow is empty, the convention dir auto-loads.)"
        )
    elif allow_result == "already":
        ok(f"plugins.allow already contains '{PLUGIN_NAME}' -- skipping")
    elif allow_result == "added":
        ok(f"Appended '{PLUGIN_NAME}' to plugins.allow")
    elif allow_result == "failed":  # Dead-code managed branch removed
        err("Failed to read/write openclaw.json -- please check file permissions")
        return 1

    # 5. Write validAgentId into plugins.entries.
    #    Regardless of whether allow is empty, the user-selected validAgentId must be
    #    written into entries, because the plugin reads its config from entries on load.
    #    Read cfg_now once and reuse across subsequent steps to avoid inconsistent state.
    cfg_now = read_config()
    if cfg_now is not None:
        existing_va = (
            cfg_now.get("plugins", {}).get("entries", {})
            .get(PLUGIN_NAME, {}).get("config", {}).get("validAgentId")
        )
        if existing_va == valid_agent:
            ok(f"validAgentId already at target value: {valid_agent}")
        else:
            entry_cfg = (
                cfg_now.setdefault("plugins", {})
                .setdefault("entries", {})
                .setdefault(PLUGIN_NAME, {})
            )
            entry_cfg.setdefault("enabled", True)
            entry_cfg.setdefault("config", {})["validAgentId"] = valid_agent
            try:
                OPENCLAW_JSON.write_text(
                    json.dumps(cfg_now, indent=2, ensure_ascii=False) + "\n"
                )
                ok(f"validAgentId written: {valid_agent}")
            except Exception as e:
                warn(f"Failed to write validAgentId: {e}")

    # 6. Sync to clawconfig source files so gateway-restart sync-config-fields.sh
    #    does not overwrite our changes.
    #    When allow is empty, only sync entries (not allow), so we don't touch
    #    unnecessary clawconfig fields.
    if allow_result in ("added", "already"):
        # allow is non-empty: sync allow + entries to clawconfig
        if cfg_now:
            sync_plugins_to_clawconfig(cfg_now)
        ensure_clawconfig_allow()
    elif allow_result == "empty":
        # allow is empty: only write entries (validAgentId), don't touch clawconfig allow
        if cfg_now:
            rt_plugins = cfg_now.get("plugins", {})
            for src in CLAWCONFIG_SOURCES:
                if not src.exists():
                    continue
                try:
                    src_cfg = json.loads(src.read_text())
                    src_entries = src_cfg.setdefault("plugins", {}).setdefault("entries", {})
                    if PLUGIN_NAME in rt_plugins.get("entries", {}):
                        src_entries[PLUGIN_NAME] = rt_plugins["entries"][PLUGIN_NAME]
                        src.write_text(json.dumps(src_cfg, indent=2, ensure_ascii=False) + "\n")
                except Exception as e:
                    warn(f"Failed to sync entries to {src.name}: {e}")


    # 7. Restart prompt
    hr()
    if args.auto_restart:
        log("Triggering gateway restart...")
        try:
            subprocess.run(["openclaw", "gateway", "restart"], timeout=60)
            ok("Restart triggered")
        except Exception as e:
            warn(f"Auto-restart failed: {e} -- please run `openclaw gateway restart` manually")
    else:
        print("⏭️  Next step: manually restart the gateway for the plugin to take effect:")
        print("    openclaw gateway restart")
    hr()
    print("After restart, run a self-check:")
    print(f"    python3 {Path(__file__).name} doctor")
    return 0


def cmd_config(args):
    hr()
    print("📋 skill-sediment config status")
    hr()
    print(f"Convention plugin dir: {EXTENSION_DIR}")
    print(f"Plugin file present:  {'✅' if (EXTENSION_DIR / ENTRY_FILE).exists() else '❌ missing (run install)'}")
    print()

    cfg = read_config()
    allow = cfg.get("plugins", {}).get("allow", []) if cfg else []
    print(f"plugins.allow current value: {allow if allow else '[] (empty)'}")
    print()

    if not allow:
        print(
            "✅ allow is empty → OpenClaw auto-loads from the convention dir; no config change needed.\n"
            "   The plugin file already occupies the path -- restart the gateway to take effect."
        )
    elif PLUGIN_NAME in allow:
        print(f"✅ plugins.allow already contains '{PLUGIN_NAME}'; config is healthy.")
    else:
        print(f"⚠️  plugins.allow is non-empty but missing '{PLUGIN_NAME}' -- needs appending.")
        patch = build_config_patch(args.valid_agent_id)
        print(f"Run `install` to auto-append to local openclaw.json, or manually add \"{PLUGIN_NAME}\" to plugins.allow.")

    # Current entries config
    if cfg:
        ents = cfg.get("plugins", {}).get("entries", {}).get(PLUGIN_NAME, {})
        if ents:
            print(f"\nplugins.entries.skill-sediment: {json.dumps(ents, ensure_ascii=False)}")
        else:
            print(f"\nplugins.entries.skill-sediment: not configured (plugin will use defaults)")
    return 0


def cmd_doctor(args):
    hr()
    print("🔍 skill-sediment diagnostics")
    hr()
    problems = []

    # Version
    level, ver, msg = check_version()
    {"ok": ok, "higher": warn, "lower": err, "unknown": warn}[level](msg)
    if level == "lower":
        problems.append("OpenClaw version is below the verified baseline")

    # Managed env (Lobi / Apollo) -- remote will overwrite local openclaw.json
    is_managed, reason = detect_managed_env()
    if is_managed:
        warn(f"Managed environment: {reason}")
        warn("On pod rebuild openclaw.json will be overwritten by the remote source -- re-run install after rebuild.")
    else:
        ok("Unmanaged environment (local openclaw.json takes effect directly)")

    # plugin-sdk
    if check_plugin_sdk():
        ok(f"plugin-sdk present: {PLUGIN_SDK_DIR}")
    else:
        warn(f"plugin-sdk missing: {PLUGIN_SDK_DIR}")
        problems.append("plugin-sdk missing")

    # Plugin file
    if (EXTENSION_DIR / ENTRY_FILE).exists():
        ok(f"Plugin file present: {EXTENSION_DIR}")
    else:
        err(f"Plugin file missing: {EXTENSION_DIR}/{ENTRY_FILE}")
        problems.append("Plugin file missing (run recover or install)")

    # Config: convention-dir loading; primarily check whether allow blocks us
    cfg = read_config()
    if cfg is None:
        # B2 fix: distinguish "openclaw.json missing" from "all checks passed"
        if OPENCLAW_JSON.exists():
            err(f"Cannot parse {OPENCLAW_JSON} -- file exists but JSON is invalid")
            problems.append(f"openclaw.json present but unparsable at {OPENCLAW_JSON}")
        else:
            warn(f"openclaw.json not found at {OPENCLAW_JSON} -- cannot verify allow/validAgentId")
            problems.append("openclaw.json not found (run install, or set OPENCLAW_CONFIG)")
    else:
        allow = cfg.get("plugins", {}).get("allow", [])
        if not allow:
            ok(f"plugins.allow is empty → convention-dir auto-load; no whitelist config needed")
        elif PLUGIN_NAME in allow:
            ok(f"plugins.allow is non-empty and contains '{PLUGIN_NAME}'; whitelist is healthy")
        else:
            err(
                f"plugins.allow is non-empty ({allow}) and missing '{PLUGIN_NAME}'!\n"
                f"   The plugin will be blocked by the whitelist and will not load.\n"
                f"   Run `install` to append, or add it manually."
            )
            problems.append(f"plugins.allow missing '{PLUGIN_NAME}' (will be blocked by whitelist)")
        ents = cfg.get("plugins", {}).get("entries", {}).get(PLUGIN_NAME, {})
        va = ents.get("config", {}).get("validAgentId", None)
        if va:
            ok(f"validAgentId config: {va}")
        else:
            warn("plugins.entries.skill-sediment has no validAgentId (plugin will use defaults; run install to fill in)")
            problems.append("validAgentId not configured (run install to fill in)")

    # sediment_skills directory
    sediment_dir = WORKSPACE / "sediment_skills"
    if sediment_dir.exists():
        n = len(list(sediment_dir.glob("*/__sediment_meta__.json")))
        ok(f"sediment_skills directory present ({n} pending incubations)")
    else:
        warn(
            "sediment_skills directory not created yet -- the plugin may not be loaded, "
            "or no sediment has been triggered. After a gateway restart, normal conversation "
            "for a while will auto-create this directory."
        )

    hr()
    if problems:
        print(f"Found {len(problems)} issue(s):")
        for p in problems:
            print(f"  • {p}")
        return 1
    ok("Files and config are ready ✨")
    print("\n⚠️  Files/config all green ≠ the plugin is actually running. Two final checks:")
    print("\n  1. Check gateway logs to confirm the plugin loaded (K8s container logs go to stdout):")
    print("     • Inside container: tail PID 1 stdout:")
    print('       grep -r "\\[skill-sediment\\]" /proc/1/fd/1 2>/dev/null | tail')
    print("     • Or OpenClaw's own logs (if present):")
    print('       ls ~/.openclaw/logs/ 2>/dev/null && grep "\\[skill-sediment\\]" ~/.openclaw/logs/*.log | tail')
    print("     • Or from outside K8s: kubectl logs <pod> | grep '[skill-sediment]'")
    print(f"     You should see plugin-load + 6 hooks: {', '.join(REQUIRED_HOOKS)}")
    print("\n  2. Live verification: after a normal conversation accumulates ~15 tool calls, run:")
    print(f"     python3 {Path(__file__).name} status")
    print("     New sediments appearing under sediment_skills/ = it's actually working.")
    return 0


def cmd_recover(args):
    """Restore after pod restart: plugin present → OK; PVC volume swapped → redeploy."""
    hr()
    print("🔧 skill-sediment recovery")
    hr()
    if (EXTENSION_DIR / ENTRY_FILE).exists():
        ok(f"Plugin file still present: {EXTENSION_DIR}")
    else:
        warn("Plugin file missing (likely PVC volume swap) -- redeploying...")
        if not ensure_plugin_files():
            return 1
        ok(f"Plugin redeployed: {EXTENSION_DIR}")

    # Refill allow / entries config (config may also have been overwritten by remote)
    valid_agent = getattr(args, "valid_agent_id", "main")
    allow_result = ensure_allow_contains(PLUGIN_NAME, valid_agent)
    if allow_result == "empty":
        ok("plugins.allow is empty -- convention dir auto-loads; no config change needed")
    elif allow_result in ("already", "added"):
        ok(f"plugins.allow contains '{PLUGIN_NAME}'" + (" (added this run)" if allow_result == "added" else ""))
    elif allow_result == "failed":
        warn("Reading/writing openclaw.json failed -- check file permissions (does not affect plugin file recovery)")

    print("\nIf anything changed, restart the gateway: openclaw gateway restart")
    return 0


def cmd_status(args):
    hr()
    print("📊 skill-sediment status")
    hr()
    sediment_dir = WORKSPACE / "sediment_skills"
    skills_dir = WORKSPACE / "skills"

    if not sediment_dir.exists():
        warn("sediment_skills directory does not exist -- the plugin may not be running")
        print("  → Next step: run `python3 manage.py doctor` to check plugin status")
        return 1

    pending = list(sediment_dir.glob("*/__sediment_meta__.json"))
    print(f"Pending incubations (sediment_skills/): {len(pending)}")
    for m in pending:
        try:
            d = json.loads(m.read_text())
            name = m.parent.name
            rev = d.get("revisionCount", "?")
            action = d.get("lastAction", "?")
            print(f"  • {name}  (rev {rev}, last={action})")
        except Exception:
            print(f"  • {m.parent.name}  (failed to read metadata)")

    # Already promoted (under skills/ with __sediment_meta__.json)
    if skills_dir.exists():
        promoted = list(skills_dir.glob("*/__sediment_meta__.json"))
        print(f"\nActivated sediments (skills/, post-promote): {len(promoted)}")
        for m in promoted:
            try:
                d = json.loads(m.read_text())
                if d.get("promotedAt"):
                    print(f"  • {m.parent.name}  (promoted {d.get('promotedAt','')[:10]})")
            except Exception:
                pass
    return 0


def cmd_heal(args):
    """Self-repair: doctor-style detection → fix whitelist / replace plugin files → restart gateway.

    Use cases:
      - Managed environments (Lobi/Apollo) where pod rebuild causes the remote
        source to overwrite openclaw.json and drop the whitelist entry
      - PVC volume swap where the plugin file is lost
    Exit codes: 0 = all green (including successful self-repair); 1 = unresolved issues
    """
    hr()
    print("🔧 skill-sediment self-repair")
    hr()

    # ── 0. Baseline environment check ──────────────────────────────────
    level, ver, msg = check_version()
    {"ok": ok, "higher": warn, "lower": err, "unknown": warn}[level](msg)
    if level == "lower" and not args.force_version:
        err("Version too low -- skipping self-repair (pass --force-version to continue)")
        return 1

    is_managed, reason = detect_managed_env()
    if is_managed:
        warn(f"Managed environment: {reason} (local openclaw.json will be overwritten on pod rebuild; re-run heal periodically to stay healthy)")
    else:
        ok("Unmanaged environment")

    issues = []   # issues we could not auto-fix
    fixed = []    # things repaired this run
    need_restart = False

    # ── 1. Plugin file ─────────────────────────────────────────────────
    if (EXTENSION_DIR / ENTRY_FILE).exists():
        ok(f"Plugin file present: {EXTENSION_DIR}")
    else:
        warn("Plugin file missing -- redeploying...")
        if ensure_plugin_files():
            fixed.append("Plugin file redeployed")
            need_restart = True
        else:
            issues.append("Plugin file deployment failed (assets bundle missing and no CDN fallback)")

    # ── 2. Whitelist check & repair ────────────────────────────────────
    valid_agent = args.valid_agent_id
    cfg = read_config()
    if cfg is None:
        issues.append("Cannot read openclaw.json")
    else:
        allow = cfg.get("plugins", {}).get("allow", [])
        entries = cfg.get("plugins", {}).get("entries", {})
        allow_ok = (not allow) or (PLUGIN_NAME in allow)

        # 2a. Whitelist repair
        if not allow_ok:
            warn(f"plugins.allow missing '{PLUGIN_NAME}' -- trying to append...")
            patch = build_config_patch(valid_agent)
            apply_config(cfg, patch)
            write_result = write_config_with_apollo_detect(cfg, patch)
            if write_result != "failed":
                # Also sync into clawconfig to survive gateway-restart sync
                sync_plugins_to_clawconfig(cfg)
                ensure_clawconfig_allow()
                fixed.append(f"plugins.allow appended with '{PLUGIN_NAME}'")
                need_restart = True
            else:
                issues.append("Failed to write openclaw.json")
        else:
            ok(f"plugins.allow state is healthy ({'empty=auto-load' if not allow else 'contains this plugin'})")

        # 2b. validAgentId backfill (only when missing; never overwrite user's value)
        current_va = entries.get(PLUGIN_NAME, {}).get("config", {}).get("validAgentId")
        if not current_va:
            log(f"validAgentId not configured -- filling in default: {valid_agent}")
            cfg_now = read_config() or cfg
            entry_cfg = cfg_now.setdefault("plugins", {}).setdefault("entries", {}).setdefault(PLUGIN_NAME, {})
            entry_cfg.setdefault("enabled", True)
            entry_cfg.setdefault("config", {})["validAgentId"] = valid_agent
            try:
                OPENCLAW_JSON.write_text(
                    json.dumps(cfg_now, indent=2, ensure_ascii=False) + "\n"
                )
                sync_plugins_to_clawconfig(cfg_now)
                fixed.append(f"validAgentId backfilled to '{valid_agent}'")
                need_restart = True
            except Exception as e:
                issues.append(f"Failed to write validAgentId: {e}")
        else:
            ok(f"validAgentId already configured: {current_va} (heal never overwrites existing values)")

    # ── 3. Restart gateway ─────────────────────────────────────────────
    if need_restart:
        if args.no_restart:
            warn("Restart needed but --no-restart was passed")
            warn("Please run manually: openclaw gateway restart")
        else:
            log("Triggering gateway restart...")
            try:
                subprocess.run(
                    ["openclaw", "gateway", "restart"],
                    timeout=60, check=True
                )
                ok("Gateway restarted")
                fixed.append("Gateway restarted")
            except Exception as e:
                issues.append(f"Gateway restart failed: {e} (run `openclaw gateway restart` manually)")
    else:
        ok("No restart needed")

    # ── 4. Summary ─────────────────────────────────────────────────────
    hr()
    if fixed:
        print(f"✅ Fixed {len(fixed)} item(s) this run:")
        for f in fixed:
            print(f"  • {f}")
    else:
        ok("All checks are healthy; nothing to fix")

    if issues:
        print(f"\n❌ {len(issues)} issue(s) could not be auto-fixed and need manual attention:")
        for i in issues:
            print(f"  • {i}")
        return 1

    return 0



def cmd_uninstall(args):
    hr()
    print("🗑️  skill-sediment uninstall")
    hr()

    # Clean allow entries and entries (if any) from openclaw.json
    cfg = read_config()
    if cfg:
        plugins = cfg.get("plugins", {})
        changed = False
        allow = plugins.get("allow", [])
        if PLUGIN_NAME in allow:
            allow.remove(PLUGIN_NAME)
            changed = True
            ok(f"Removed '{PLUGIN_NAME}' from plugins.allow")
        entries = plugins.get("entries", {})
        if PLUGIN_NAME in entries:
            del entries[PLUGIN_NAME]
            changed = True
            ok(f"Removed '{PLUGIN_NAME}' from plugins.entries")
        if changed:
            is_managed, _ = detect_managed_env()
            if not is_managed:
                shutil.copy(
                    OPENCLAW_JSON,
                    OPENCLAW_JSON.with_suffix(f".json.bak.{int(time.time())}"),
                )
            OPENCLAW_JSON.write_text(
                json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"
            )
            ok("openclaw.json updated")
            # Also sync to clawconfig source files (including allow removal) so
            # that a gateway restart sync does not re-introduce the entry.
            sync_plugins_to_clawconfig(cfg)
            remove_clawconfig_allow()
        else:
            ok("openclaw.json had no skill-sediment config (already clean)")
        allow_after = cfg.get("plugins", {}).get("allow", [])
        if not allow_after:
            warn(
                "⚠️  After uninstall, plugins.allow is still empty, so other plugins in the\n"
                "   convention dir will continue to auto-load. To block all non-built-in plugins,\n"
                "   set allow to an explicit whitelist manually."
            )

    # Delete plugin files
    if args.purge:
        if EXTENSION_DIR.exists():
            shutil.rmtree(EXTENSION_DIR)
            ok(f"Deleted plugin directory {EXTENSION_DIR}")
        else:
            ok(f"Plugin directory does not exist -- skipping")
        warn(
            "Note: --purge does NOT delete already-sedimented SKILL.md under sediment_skills/\n"
            "(those are your accumulated workflows). Remove them manually if you wish."
        )
    else:
        if EXTENSION_DIR.exists():
            print(f"Plugin files kept in {EXTENSION_DIR} (pass --purge to delete)")
            warn("⚠️  Plugin files are still in the convention dir; if allow is empty they will reload on next restart!")
        else:
            ok("Plugin directory already absent")

    print("\nRestart the gateway for uninstall to take effect: openclaw gateway restart")
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="skill-sediment installer / operator")
    sub = p.add_subparsers(dest="command", required=True)

    def add_agent_arg(sp):
        sp.add_argument(
            "--valid-agent-id",
            default=os.environ.get("SKILL_SEDIMENT_AGENTS", "main"),
            help="Comma-separated agent ids that enable sediment (e.g. main,debp). Default: main",
        )

    sp = sub.add_parser("install", help="Full install")
    add_agent_arg(sp)
    sp.add_argument("--auto-restart", action="store_true",
                    help="Restart the gateway automatically after install (not recommended in Apollo-managed envs)")
    sp.add_argument("--force-version", action="store_true",
                    help="Install even if the OpenClaw version is below the verified baseline")

    sp = sub.add_parser("config", help="Print current allow state and recommended action")
    add_agent_arg(sp)

    sp = sub.add_parser("doctor", help="Diagnose plugin files / config / version / sediment dir")
    add_agent_arg(sp)

    sp = sub.add_parser("recover", help="Restore after pod restart")
    add_agent_arg(sp)

    sub.add_parser("status", help="Inspect the sediment pool (pending / activated counts)")

    sp = sub.add_parser("heal", help="Self-repair: detect and fix whitelist/file loss, auto-restart gateway")
    add_agent_arg(sp)
    sp.add_argument("--no-restart", action="store_true",
                    help="Do not auto-restart gateway after applying fixes")
    sp.add_argument("--force-version", action="store_true",
                    help="Run even if the OpenClaw version is below the verified baseline")


    sp = sub.add_parser("uninstall", help="Uninstall (config entries only; add --purge to also delete the plugin dir)")
    sp.add_argument("--purge", action="store_true",
                    help="Also delete the plugin directory (does NOT delete already-sedimented SKILL.md files)")

    args = p.parse_args()

    cmd_map = {
        "install": cmd_install,
        "config": cmd_config,
        "doctor": cmd_doctor,
        "recover": cmd_recover,
        "status": cmd_status,
        "heal": cmd_heal,
        "uninstall": cmd_uninstall,
    }
    return cmd_map[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
