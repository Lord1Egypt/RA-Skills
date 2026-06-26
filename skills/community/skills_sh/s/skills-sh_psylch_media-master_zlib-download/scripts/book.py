#!/usr/bin/env python3
"""
book.py - Unified CLI for searching and downloading books.

Backends:
  - zlib:  Z-Library via vendored Zlibrary.py (EAPI)
  - annas: Anna's Archive via annas-mcp binary

All output is JSON to stdout. Errors go to stderr with non-zero exit.
Config stored at ~/.claude/book-tools/config.json
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_DIR = Path.home() / ".claude" / "book-tools"
CONFIG_FILE = CONFIG_DIR / "config.json"
ENV_FILE = CONFIG_DIR / ".env"
DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads"


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def _load_env() -> dict:
    """Load key=value pairs from .env file."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def load_config() -> dict:
    cfg = {}
    if CONFIG_FILE.exists():
        cfg = json.loads(CONFIG_FILE.read_text())

    # Merge .env values (env file overrides config.json)
    env = _load_env()
    if env.get("ZLIB_EMAIL") or env.get("ZLIB_PASSWORD"):
        cfg.setdefault("zlib", {})
        if env.get("ZLIB_EMAIL"):
            cfg["zlib"]["email"] = env["ZLIB_EMAIL"]
        if env.get("ZLIB_PASSWORD"):
            cfg["zlib"]["password"] = env["ZLIB_PASSWORD"]
    if env.get("ANNAS_SECRET_KEY"):
        cfg.setdefault("annas", {})
        cfg["annas"]["secret_key"] = env["ANNAS_SECRET_KEY"]

    return cfg


def save_config(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))


def output(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def die(msg: str, hint: str = "", code: int = 1, recoverable: bool = True):
    print(json.dumps({"error": msg, "hint": hint or msg, "recoverable": recoverable}), file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# Z-Library backend
# ---------------------------------------------------------------------------

def _get_zlib():
    """Return an authenticated Zlibrary instance.

    Token refresh strategy (see best_practices.md § Error Recovery):
      1. Try cached remix tokens → if logged in, return immediately
      2. If not logged in AND email/password available → fresh login
      3. On fresh login success → update cached tokens in config
      4. If nothing works → die with actionable hint
    """
    cfg = load_config()
    zlib_cfg = cfg.get("zlib", {})

    sys.path.insert(0, str(SCRIPT_DIR))
    from Zlibrary import Zlibrary

    remix_userid = zlib_cfg.get("remix_userid")
    remix_userkey = zlib_cfg.get("remix_userkey")
    email = zlib_cfg.get("email")
    password = zlib_cfg.get("password")

    # Step 1: Try cached tokens
    if remix_userid and remix_userkey:
        z = Zlibrary(remix_userid=remix_userid, remix_userkey=remix_userkey)
        if z.isLoggedIn():
            return z
        # Cached tokens expired — fall through to fresh login

    # Step 2: Try fresh login with email/password
    if email and password:
        z = Zlibrary(email=email, password=password)
        if z.isLoggedIn():
            # Cache tokens for next time
            profile = z.getProfile()
            if profile and profile.get("success"):
                user = profile["user"]
                cfg.setdefault("zlib", {})
                cfg["zlib"]["remix_userid"] = str(user["id"])
                cfg["zlib"]["remix_userkey"] = user["remix_userkey"]
                save_config(cfg)
            return z

    # Step 3: No valid credentials
    if not email and not password and not remix_userid:
        die("Z-Library not configured. Edit ~/.claude/book-tools/.env with your ZLIB_EMAIL and ZLIB_PASSWORD.")
    else:
        die("Z-Library login failed. Check credentials in ~/.claude/book-tools/.env")


def zlib_search(args):
    z = _get_zlib()
    params = {"message": args.query}
    if args.limit:
        params["limit"] = args.limit
    if args.lang:
        params["languages"] = args.lang
    if args.ext:
        params["extensions"] = args.ext
    if args.year_from:
        params["yearFrom"] = args.year_from
    if args.year_to:
        params["yearTo"] = args.year_to

    result = z.search(**params)
    if not result or not result.get("success"):
        die(f"Z-Library search failed: {result}")

    books = []
    for b in result.get("books", []):
        books.append({
            "source": "zlib",
            "id": b.get("id"),
            "hash": b.get("hash"),
            "title": b.get("title", ""),
            "author": b.get("author", ""),
            "publisher": b.get("publisher", ""),
            "year": b.get("year", ""),
            "language": b.get("language", ""),
            "extension": b.get("extension", ""),
            "filesize": b.get("filesizeString", ""),
            "cover": b.get("cover", ""),
        })
    output({"source": "zlib", "count": len(books), "books": books})


def zlib_info(args):
    z = _get_zlib()
    result = z.getBookInfo(args.id, args.hash)
    if not result or not result.get("success"):
        die(f"Z-Library info failed: {result}")
    result["source"] = "zlib"
    output(result)


def zlib_download(args):
    z = _get_zlib()
    out_dir = Path(args.output) if args.output else DEFAULT_DOWNLOAD_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    result = z._Zlibrary__getBookFile(args.id, args.hash)
    if result is None:
        die("Z-Library download failed: no file returned")

    filename, content = result
    # Sanitize filename
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filepath = out_dir / filename
    filepath.write_bytes(content)
    output({"source": "zlib", "status": "ok", "path": str(filepath), "size": len(content)})


# ---------------------------------------------------------------------------
# Anna's Archive backend
# ---------------------------------------------------------------------------

def _find_annas_binary() -> str:
    """Find annas-mcp binary."""
    cfg = load_config()
    custom = cfg.get("annas", {}).get("binary_path")
    if custom and Path(custom).exists():
        return custom

    # Check PATH
    for p in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(p) / "annas-mcp"
        if candidate.exists():
            return str(candidate)

    # Check common locations
    for loc in [
        Path.home() / ".local" / "bin" / "annas-mcp",
        Path("/usr/local/bin/annas-mcp"),
    ]:
        if loc.exists():
            return str(loc)

    die(
        "annas-mcp binary not found",
        hint="Install it:\n"
        "  1. Run: bash ${SKILL_PATH}/scripts/setup.sh install-annas\n"
        "  2. Or manually: download from https://github.com/iosifache/annas-mcp/releases, "
        "extract and move to ~/.local/bin/annas-mcp",
    )


def _annas_env() -> dict:
    """Build env dict for annas-mcp subprocess."""
    cfg = load_config()
    annas_cfg = cfg.get("annas", {})
    env = os.environ.copy()
    if annas_cfg.get("secret_key"):
        env["ANNAS_SECRET_KEY"] = annas_cfg["secret_key"]
    download_path = annas_cfg.get("download_path", str(DEFAULT_DOWNLOAD_DIR))
    env["ANNAS_DOWNLOAD_PATH"] = download_path
    if annas_cfg.get("base_url"):
        env["ANNAS_BASE_URL"] = annas_cfg["base_url"]
    return env


def _parse_annas_search_output(text: str) -> list[dict]:
    """Parse annas-mcp search plain-text output into structured dicts."""
    books = []
    current = {}

    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            if current:
                books.append(current)
                current = {}
            continue

        if line.startswith("Title:"):
            if current:
                books.append(current)
            current = {"source": "annas", "title": line[6:].strip()}
        elif line.startswith("Authors:"):
            current["author"] = line[8:].strip()
        elif line.startswith("Publisher:"):
            current["publisher"] = line[10:].strip()
        elif line.startswith("Language:"):
            current["language"] = line[9:].strip()
        elif line.startswith("Format:"):
            current["extension"] = line[7:].strip()
        elif line.startswith("Size:"):
            current["filesize"] = line[5:].strip()
        elif line.startswith("URL:"):
            current["url"] = line[4:].strip()
        elif line.startswith("Hash:"):
            current["hash"] = line[5:].strip()

    if current:
        books.append(current)
    return books


def _extract_annas_error(stderr: str) -> str:
    """Extract the useful error message from annas-mcp verbose output."""
    # Look for the last ERROR line with a human-readable message
    for line in reversed(stderr.strip().splitlines()):
        line = line.strip()
        if line.startswith("Failed to"):
            return line
        if "ERROR" in line and "environment variables must be set" in line:
            return "ANNAS_SECRET_KEY and ANNAS_DOWNLOAD_PATH must be set"
    # Fallback: last non-empty line
    lines = [l.strip() for l in stderr.strip().splitlines() if l.strip()]
    return lines[-1] if lines else "Unknown error"


def annas_search(args):
    binary = _find_annas_binary()
    cfg = load_config()

    if not cfg.get("annas", {}).get("secret_key"):
        die("Anna's Archive API key not configured. Add ANNAS_SECRET_KEY to ~/.claude/book-tools/.env\n"
            "Get a key by donating to Anna's Archive.")

    env = _annas_env()

    try:
        result = subprocess.run(
            [binary, "search", args.query],
            capture_output=True, text=True, env=env, timeout=30,
        )
    except subprocess.TimeoutExpired:
        die("annas-mcp search timed out after 30s")

    if result.returncode != 0:
        die(f"annas-mcp search failed: {_extract_annas_error(result.stderr)}")

    if "No books found" in result.stdout:
        output({"source": "annas", "count": 0, "books": []})
        return

    books = _parse_annas_search_output(result.stdout)
    output({"source": "annas", "count": len(books), "books": books})


def annas_download(args):
    binary = _find_annas_binary()
    env = _annas_env()
    cfg = load_config()

    if not cfg.get("annas", {}).get("secret_key"):
        die("Anna's Archive API key not configured. Add ANNAS_SECRET_KEY to ~/.claude/book-tools/.env")

    filename = args.filename
    if not filename:
        filename = f"book_{args.hash[:8]}.pdf"

    if args.output:
        env["ANNAS_DOWNLOAD_PATH"] = str(Path(args.output).resolve())
        Path(args.output).mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [binary, "download", args.hash, filename],
            capture_output=True, text=True, env=env, timeout=120,
        )
    except subprocess.TimeoutExpired:
        die("annas-mcp download timed out after 120s")

    if result.returncode != 0:
        die(f"annas-mcp download failed: {_extract_annas_error(result.stderr)}")

    download_path = env.get("ANNAS_DOWNLOAD_PATH", str(DEFAULT_DOWNLOAD_DIR))
    filepath = Path(download_path) / filename
    output({"source": "annas", "status": "ok", "path": str(filepath), "message": result.stdout.strip()})


# ---------------------------------------------------------------------------
# Unified commands
# ---------------------------------------------------------------------------

def cmd_search(args):
    source = args.source
    if source == "zlib":
        zlib_search(args)
    elif source == "annas":
        annas_search(args)
    elif source == "auto":
        # Try Z-Library first, fall back to Anna's Archive
        cfg = load_config()
        errors = []
        if cfg.get("zlib", {}).get("email") or cfg.get("zlib", {}).get("remix_userid"):
            try:
                zlib_search(args)
                return
            except SystemExit:
                errors.append("zlib: login failed or service unavailable")
        else:
            errors.append("zlib: not configured")

        if cfg.get("annas", {}).get("secret_key"):
            try:
                annas_search(args)
                return
            except SystemExit:
                errors.append("annas: search failed")
        else:
            errors.append("annas: not configured")

        die("No backend available. Configure at least one in ~/.claude/book-tools/.env:\n"
            "  Z-Library: set ZLIB_EMAIL and ZLIB_PASSWORD\n"
            "  Anna's Archive: set ANNAS_SECRET_KEY\n"
            f"Details: {'; '.join(errors)}")


def cmd_download(args):
    if args.source == "zlib":
        zlib_download(args)
    elif args.source == "annas":
        annas_download(args)
    else:
        die("Download requires --source (zlib or annas)")


def cmd_info(args):
    if args.source == "zlib":
        zlib_info(args)
    else:
        die("Info command currently only supports --source zlib")


def cmd_config(args):
    if args.config_action == "show":
        cfg = load_config()
        # Mask sensitive values
        display = json.loads(json.dumps(cfg))
        if "zlib" in display:
            if "password" in display["zlib"]:
                display["zlib"]["password"] = "***"
            if "remix_userkey" in display["zlib"]:
                display["zlib"]["remix_userkey"] = display["zlib"]["remix_userkey"][:8] + "..."
        if "annas" in display:
            if "secret_key" in display["annas"]:
                display["annas"]["secret_key"] = display["annas"]["secret_key"][:8] + "..."
        output(display)

    elif args.config_action == "set":
        cfg = load_config()

        if args.annas_binary:
            cfg.setdefault("annas", {})
            cfg["annas"]["binary_path"] = args.annas_binary

        if args.annas_download_path:
            cfg.setdefault("annas", {})
            cfg["annas"]["download_path"] = args.annas_download_path

        if args.annas_mirror:
            cfg.setdefault("annas", {})
            cfg["annas"]["base_url"] = args.annas_mirror

        if args.download_dir:
            cfg["default_download_dir"] = args.download_dir

        save_config(cfg)
        output({"status": "ok", "message": "Config updated"})

    elif args.config_action == "reset":
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        output({"status": "ok", "message": "Config reset"})


def cmd_setup(args):
    """Check dependencies and report status."""
    status = {"zlib": {}, "annas": {}}
    cfg = load_config()

    # Check Python requests
    try:
        import requests
        status["zlib"]["requests_installed"] = True
        status["zlib"]["requests_version"] = requests.__version__
    except ImportError:
        status["zlib"]["requests_installed"] = False

    # Check Z-Library credentials
    zlib_cfg = cfg.get("zlib", {})
    status["zlib"]["configured"] = bool(
        zlib_cfg.get("email") or zlib_cfg.get("remix_userid")
    )

    # Check annas-mcp binary
    status["annas"]["binary_found"] = _has_annas_binary()
    if status["annas"]["binary_found"]:
        status["annas"]["binary_path"] = _find_annas_binary_silent()

    # Check Anna's Archive API key
    status["annas"]["api_key_configured"] = bool(cfg.get("annas", {}).get("secret_key"))

    output(status)


def _has_annas_binary() -> bool:
    try:
        _find_annas_binary_silent()
        return True
    except:
        return False


def _find_annas_binary_silent() -> str:
    cfg = load_config()
    custom = cfg.get("annas", {}).get("binary_path")
    if custom and Path(custom).exists():
        return custom
    for p in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(p) / "annas-mcp"
        if candidate.exists():
            return str(candidate)
    for loc in [
        Path.home() / ".local" / "bin" / "annas-mcp",
        Path("/usr/local/bin/annas-mcp"),
    ]:
        if loc.exists():
            return str(loc)
    raise FileNotFoundError("annas-mcp not found")


def cmd_preflight(args):
    """Standardized preflight check with JSON output."""
    cfg = load_config()
    ready = False

    # Check requests library
    requests_ok = False
    try:
        import requests as _req
        requests_ok = True
    except ImportError:
        pass

    # Check Z-Library credentials with live validation
    zlib_cfg = cfg.get("zlib", {})
    zlib_has_tokens = bool(zlib_cfg.get("remix_userid") and zlib_cfg.get("remix_userkey"))
    zlib_has_email = bool(zlib_cfg.get("email") and zlib_cfg.get("password"))
    zlib_status = "not_configured"
    zlib_hint = "Edit ~/.claude/book-tools/.env with ZLIB_EMAIL and ZLIB_PASSWORD"

    if requests_ok and (zlib_has_tokens or zlib_has_email):
        # Attempt live validation with cached tokens
        if zlib_has_tokens:
            try:
                sys.path.insert(0, str(SCRIPT_DIR))
                from Zlibrary import Zlibrary
                z = Zlibrary(
                    remix_userid=zlib_cfg["remix_userid"],
                    remix_userkey=zlib_cfg["remix_userkey"],
                )
                if z.isLoggedIn():
                    zlib_status = "valid"
                    zlib_hint = "Z-Library tokens are valid"
                elif zlib_has_email:
                    # Tokens expired but email/password available for re-login
                    zlib_status = "configured"
                    zlib_hint = "Cached tokens expired; will re-login with email/password on next use"
                else:
                    zlib_status = "expired"
                    zlib_hint = "Cached tokens expired and no email/password available. Edit ~/.claude/book-tools/.env"
            except Exception:
                if zlib_has_email:
                    zlib_status = "configured"
                    zlib_hint = "Token validation failed; will attempt email/password login on next use"
                else:
                    zlib_status = "configured"
                    zlib_hint = "Token validation could not be performed"
        else:
            # Only email/password, no cached tokens yet — can attempt login on use
            zlib_status = "configured"
            zlib_hint = "Email/password set; will login on first use"

    # Check Anna's Archive
    annas_binary = _has_annas_binary()
    annas_key = bool(cfg.get("annas", {}).get("secret_key"))

    # Ready if at least one backend is usable
    if requests_ok and zlib_status in ("valid", "configured"):
        ready = True
    if annas_binary and annas_key:
        ready = True

    result = {
        "ready": ready,
        "dependencies": {
            "python3": {"status": "ok", "hint": "Python 3 is running"},
            "requests": {
                "status": "ok" if requests_ok else "missing",
                "hint": "Run: bash ${SKILL_PATH}/scripts/setup.sh install-deps (or: pip3 install requests)",
            },
        },
        "credentials": {
            "zlib": {
                "status": zlib_status,
                "required": False,
                "hint": zlib_hint,
            },
            "annas_api_key": {
                "status": "configured" if annas_key else "not_configured",
                "required": False,
                "hint": "Donate at Anna's Archive for API key, add ANNAS_SECRET_KEY to ~/.claude/book-tools/.env",
            },
        },
        "services": {
            "annas_binary": {
                "status": "ok" if annas_binary else "missing",
                "hint": "Run: bash ${SKILL_PATH}/scripts/setup.sh install-annas (or manually download from https://github.com/iosifache/annas-mcp/releases)",
            },
        },
        "hint": "Ready — at least one backend configured" if ready else "No backend fully configured. Set up Z-Library or Anna's Archive credentials in ~/.claude/book-tools/.env",
    }
    output(result)
    if not ready:
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="book.py",
        description="Unified CLI for book search and download (Z-Library + Anna's Archive)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- search --
    p_search = sub.add_parser("search", help="Search for books")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--source", choices=["zlib", "annas", "auto"], default="auto",
                          help="Backend to use (default: auto)")
    p_search.add_argument("--limit", type=int, help="Max results")
    p_search.add_argument("--lang", help="Language filter (e.g. english, chinese)")
    p_search.add_argument("--ext", help="File extension filter (e.g. pdf, epub)")
    p_search.add_argument("--year-from", type=int, help="Publication year from")
    p_search.add_argument("--year-to", type=int, help="Publication year to")
    p_search.set_defaults(func=cmd_search)

    # -- download --
    p_dl = sub.add_parser("download", help="Download a book")
    p_dl.add_argument("--source", choices=["zlib", "annas"], required=True,
                      help="Backend to use")
    p_dl.add_argument("--id", help="Book ID (zlib)")
    p_dl.add_argument("--hash", required=True, help="Book hash (zlib hash or annas MD5)")
    p_dl.add_argument("--filename", help="Output filename (annas)")
    p_dl.add_argument("--output", "-o", help="Output directory")
    p_dl.set_defaults(func=cmd_download)

    # -- info --
    p_info = sub.add_parser("info", help="Get book details")
    p_info.add_argument("--source", choices=["zlib", "annas"], default="zlib")
    p_info.add_argument("--id", required=True, help="Book ID")
    p_info.add_argument("--hash", required=True, help="Book hash")
    p_info.set_defaults(func=cmd_info)

    # -- config --
    p_cfg = sub.add_parser("config", help="Manage configuration")
    cfg_sub = p_cfg.add_subparsers(dest="config_action", required=True)

    cfg_show = cfg_sub.add_parser("show", help="Show current config")
    cfg_show.set_defaults(func=cmd_config)

    cfg_set = cfg_sub.add_parser("set", help="Set non-sensitive config values (for credentials, edit ~/.claude/book-tools/.env)")
    cfg_set.add_argument("--annas-binary", help="Path to annas-mcp binary")
    cfg_set.add_argument("--annas-download-path", help="Anna's Archive download directory")
    cfg_set.add_argument("--annas-mirror", help="Anna's Archive mirror URL")
    cfg_set.add_argument("--download-dir", help="Default download directory for all backends")
    cfg_set.set_defaults(func=cmd_config)

    cfg_reset = cfg_sub.add_parser("reset", help="Reset all config")
    cfg_reset.set_defaults(func=cmd_config)

    # -- setup --
    p_setup = sub.add_parser("setup", help="Check dependencies and backend status")
    p_setup.set_defaults(func=cmd_setup)

    # -- preflight --
    p_preflight = sub.add_parser("preflight", help="Standardized environment readiness check")
    p_preflight.set_defaults(func=cmd_preflight)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
