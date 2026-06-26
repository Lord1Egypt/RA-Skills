#!/usr/bin/env python3
"""OpenClaw Quark Drive CLI.

This CLI is the executable surface for the quark-netdisk skill.

- Uses system Python (dependencies via apt on this host)
- Supports API QR login, upload, and share/save workflows
- Enforces allowlists from references/config.json (or config.example.json)

Commands implemented:
- login: generate QR url+png, wait for scan, save session cookies
- login-prepare: generate QR png+url and persist token (for Telegram flow)
- login-wait: poll login using persisted token; save session cookies
- mkdir: ensure /OpenClaw exists
- upload: upload a local file into /OpenClaw
- ls: list folder (by id)
- search: global search
- rename: rename a remote item (within allowlist)
- mv: move a remote item to another remote folder (within allowlist)
- rm: soft-delete a remote item by moving it into /OpenClaw/.trash (requires confirm)
- purge-trash: hard-delete trash entries older than retention days (requires confirm)

NOTE: This is a first operational slice to enable scheduled backups later.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from quark_api import (
    QuarkSession,
    create_share,
    ensure_remote_dir,
    enforce_remote_allowlist,
    get_share_detail,
    get_share_token,
    list_folder,
    parse_share_url,
    purge_trash,
    rename_file,
    resolve_fid_path,
    resolve_remote_fid,
    save_png_qr,
    save_share_to_my_drive,
    search,
    soft_delete_to_trash,
    split_remote_path,
)


ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"

# Machine-readable interaction exit codes (for OpenClaw agent orchestration)
EXIT_NEED_LOGIN = 10
EXIT_NEED_PICK = 11
EXIT_NEED_CONFIRM = 12

# Privacy default: restrict searches to /OpenClaw unless user explicitly allows broader scope.
DEFAULT_SEARCH_ROOT = "/OpenClaw"


def _print_json(obj: dict[str, Any]) -> None:
    print(json.dumps(obj, ensure_ascii=False)[:2000])


def load_config() -> dict[str, Any]:
    cfg_path = REF / "config.json"
    if not cfg_path.exists():
        cfg_path = REF / "config.example.json"
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def save_session(login: dict[str, Any]) -> Path:
    out = REF / "session_api.json"
    out.write_text(json.dumps(login, ensure_ascii=False, indent=2), encoding="utf-8")

    # Also persist QuarkPan-compatible cookies.json for portability/debugging.
    # Format aligns with external/QuarkPan/config/cookies.json.
    try:
        cookies = login.get("cookies") if isinstance(login, dict) else None
        if isinstance(cookies, list):
            import time

            # compute expires_at as min positive expires
            expires_at = None
            for c in cookies:
                try:
                    exp = c.get("expires")
                    if isinstance(exp, int) and exp > 0:
                        expires_at = exp if expires_at is None else min(expires_at, exp)
                except Exception:
                    pass
            if expires_at is None:
                expires_at = int(time.time()) + 7 * 24 * 3600

            qp = {
                "cookies": [
                    {"name": c.get("name"), "value": c.get("value"), "domain": c.get("domain", ".quark.cn"), "path": c.get("path", "/")}
                    for c in cookies
                    if isinstance(c, dict) and c.get("name") and c.get("value")
                ],
                "timestamp": int(time.time()),
                "expires_at": expires_at,
            }
            (REF / "cookies.json").write_text(json.dumps(qp, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

    return out


def save_login_token(data: dict[str, Any]) -> Path:
    out = REF / "login_token.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def load_login_token() -> dict[str, Any]:
    p = REF / "login_token.json"
    if not p.exists():
        raise FileNotFoundError("未找到 login_token.json，请先运行 login-prepare")
    return json.loads(p.read_text(encoding="utf-8"))


def cmd_login(_args: argparse.Namespace) -> int:
    cfg = load_config()
    timeout = int(cfg.get("loginTimeoutSeconds", 300))

    qr_png = REF / "qr_code.png"

    with QuarkSession(timeout_s=60) as s:
        token = s.get_qr_token()
        qr_url = s.build_qr_url(token)
        save_png_qr(qr_url, qr_png)

        # Best-effort: open QR PNG locally for immediate scanning.
        try:
            import subprocess
            subprocess.Popen(["xdg-open", str(qr_png)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

        print("二维码已生成（已尝试在本机打开图片）：")
        print(f"- PNG: {qr_png}")
        print(f"- URL: {qr_url}")
        print("用夸克 App 扫码确认后，我会继续轮询登录状态...")

        st = s.poll_service_ticket(token, timeout_s=timeout, poll_interval_s=5.0)
        s.exchange_ticket_for_cookies(st)
        lr = s.export_cookies()

        out = save_session(
            {
                "source": "api-qr",
                "service_ticket": st,
                "cookieString": lr.cookie_string,
                "cookies": lr.cookies_json,
            }
        )
        print(f"登录成功，cookie 已保存到: {out}")

    return 0


def load_cookie_string() -> str:
    # Allow overriding cookie via env for debugging / browser-exported cookies.
    cs_env = os.environ.get("QUARK_COOKIE")
    if cs_env:
        return cs_env

    p = REF / "session_api.json"
    if not p.exists():
        raise FileNotFoundError("未找到 session_api.json，请先运行 login")
    data = json.loads(p.read_text(encoding="utf-8"))
    cs = data.get("cookieString")
    if not cs:
        raise ValueError("session_api.json 缺少 cookieString")
    return cs


def load_cookies_json() -> list[dict[str, Any]]:
    # Prefer structured cookies (domain/path-aware) when available.
    p = REF / "session_api.json"
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    cookies = data.get("cookies")
    if isinstance(cookies, list):
        return cookies
    return []


def open_authed_session(timeout_s: int = 60) -> QuarkSession:
    """Open an authenticated QuarkSession from stored cookies.

    Centralizes cookie loading so commands don't re-implement it.
    """
    cs = load_cookie_string()
    cookies_json = load_cookies_json()
    return QuarkSession(timeout_s=timeout_s, cookie_string=cs, cookies_json=cookies_json)


def remote_allowlist(cfg: dict[str, Any] | None = None) -> list[str]:
    if cfg is None:
        cfg = load_config()
    return list(cfg.get("remoteAllowlist", []) or [])


def _index_path() -> Path:
    # Privacy default: treat index as sensitive; keep it ephemeral unless explicitly requested.
    return REF / "index.json"


def _build_index(
    *,
    session: QuarkSession,
    root_path: str,
    remote_allow: list[str],
    max_items: int = 5000,
    write_file: bool = False,
) -> dict[str, Any]:
    """Build a local index of files/folders under a remote root.

    WARNING:
    - This may issue many API calls; keep max_items bounded.
    - The index contains private filenames/paths. By default we do NOT write it to disk.
    """
    enforce_remote_allowlist(root_path, remote_allow)
    root_fid = resolve_remote_fid(session, root_path)

    items: list[dict[str, Any]] = []
    q: list[tuple[str, str]] = [(root_fid, root_path)]  # (fid, path)

    while q and len(items) < max_items:
        fid, cur_path = q.pop(0)
        lst = list_folder(session, parent_id=fid, size=200)
        for it in lst:
            name = it.get("file_name") or ""
            if not name:
                continue
            child_path = (cur_path.rstrip("/") + "/" + name) if cur_path != "/" else "/" + name
            try:
                enforce_remote_allowlist(child_path, remote_allow)
            except Exception:
                continue

            child_fid = str(it.get("fid"))
            is_dir = bool(it.get("dir"))
            items.append(
                {
                    "fid": child_fid,
                    "path": child_path,
                    "name": name,
                    "is_dir": is_dir,
                    "size": it.get("size"),
                    "updated_at": it.get("updated_at"),
                }
            )
            if is_dir and child_fid and len(items) < max_items:
                q.append((child_fid, child_path))
            if len(items) >= max_items:
                break

    idx = {
        "version": 1,
        "generated_at": int(time.time()),
        "root": root_path,
        "count": len(items),
        "max_items": max_items,
        "items": items,
    }
    if write_file:
        _index_path().write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
    return idx


def _load_index() -> dict[str, Any] | None:
    p = _index_path()
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _fuzzy_score(q: str, s: str) -> float:
    q = (q or "").lower()
    s = (s or "").lower()
    if not q or not s:
        return 0.0
    return SequenceMatcher(None, q, s).ratio()


def _search_local_index(idx: dict[str, Any], keyword: str, top: int = 20) -> list[dict[str, Any]]:
    items = idx.get("items") if isinstance(idx, dict) else None
    if not isinstance(items, list):
        return []
    scored = []
    for it in items:
        if not isinstance(it, dict):
            continue
        name = it.get("name") or ""
        path = it.get("path") or ""
        score = max(_fuzzy_score(keyword, name), _fuzzy_score(keyword, path))
        if score <= 0:
            continue
        out = dict(it)
        out["score"] = round(score, 4)
        scored.append(out)
    scored.sort(key=lambda x: x.get("score", 0), reverse=True)
    return scored[: max(1, int(top))]


def cmd_mkdir(args: argparse.Namespace) -> int:
    cfg = load_config()
    remote_allow = cfg.get("remoteAllowlist", [])

    path = args.path
    enforce_remote_allowlist(path, remote_allow)

    with open_authed_session(timeout_s=60) as s:
        fid = ensure_remote_dir(s, path)
        print(json.dumps({"folder": path, "fid": fid}, ensure_ascii=False))
    return 0


def ensure_logged_in(
    *,
    timeout: int,
    progress_mode: str,
    send_qr_telegram: bool = False,
    telegram_chat: str | None = None,
) -> None:
    """Ensure session_api.json exists and is valid; otherwise run login.

    progress_mode:
      - "terminal": print progress every ~30s
      - "telegram": (TODO) send progress messages

    For now, Telegram send is best-effort (requires manual wiring in main agent).
    """

    def is_ok() -> bool:
        try:
            cs = load_cookie_string()
        except Exception:
            return False
        try:
            with open_authed_session(timeout_s=15) as s:
                _ = list_folder(s, parent_id="0", size=1)
            return True
        except Exception:
            return False

    if is_ok():
        return

    # run login
    qr_png = REF / "qr_code.png"
    with QuarkSession(timeout_s=60) as s:
        token = s.get_qr_token()
        qr_url = s.build_qr_url(token)
        save_png_qr(qr_url, qr_png)

        # terminal: open image
        if progress_mode == "terminal":
            try:
                import subprocess
                subprocess.Popen(["xdg-open", str(qr_png)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
            print("需要登录夸克网盘，二维码已生成并尝试打开：")
            print(f"- PNG: {qr_png}")
            print(f"- URL: {qr_url}")

        # telegram: send image (requires main agent call with message tool; leave stub here)
        if send_qr_telegram and telegram_chat:
            # We cannot call OpenClaw message tool from this CLI directly.
            # Main agent should send REF/qr_code.png to telegram_chat.
            pass

        def progress_cb(remaining: int, msg: str):
            if progress_mode == "terminal":
                print(f"[login] {msg}，剩余 {remaining}s")

        st = s.poll_service_ticket(token, timeout_s=timeout, progress_cb=progress_cb, progress_interval_s=30, poll_interval_s=5.0)
        s.exchange_ticket_for_cookies(st)
        lr = s.export_cookies()
        save_session({"source": "api-qr", "service_ticket": st, "cookieString": lr.cookie_string, "cookies": lr.cookies_json})

    return


def cmd_upload(args: argparse.Namespace) -> int:
    cfg = load_config()
    local_allow = cfg.get("localAllowlist", [])
    remote_allow = cfg.get("remoteAllowlist", [])

    # auto-login if needed
    ensure_logged_in(timeout=int(cfg.get("loginTimeoutSeconds", 300)), progress_mode="terminal")

    # simple checks
    src = Path(args.file).expanduser().resolve()
    if not any(str(src).startswith(str(Path(a).expanduser().resolve())) for a in local_allow):
        raise PermissionError(f"本地路径不在 allowlist: {src}")
    if "/OpenClaw" not in remote_allow:
        raise PermissionError("远端 allowlist 未包含 /OpenClaw")

    cs = load_cookie_string()
    cookies_json = load_cookies_json()

    def prog(p: int, msg: str):
        print(f"[{p:3d}%] {msg}")

    # Use QuarkPan uploader for upload stability.
    from quarkpan_uploader import QuarkPanAPIClient, QuarkPanUploader

    api = QuarkPanAPIClient(cookie_string=cs, timeout_s=60.0)
    up = QuarkPanUploader(api)

    # Ensure /OpenClaw exists and upload into it.
    with QuarkSession(timeout_s=60, cookie_string=cs, cookies_json=cookies_json) as s:
        openclaw_fid = ensure_remote_dir(s, "/OpenClaw")

    res = up.upload(file_path=src, parent_folder_id=openclaw_fid, progress=prog)
    print(json.dumps({"uploaded": src.name, "target": "/OpenClaw", "result": res.__dict__}, ensure_ascii=False)[:2000])

    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("login")
    pprep = sub.add_parser("login-prepare")
    pprep.add_argument("--no-open", action="store_true", help="Do not xdg-open the QR image (useful for Telegram flow)")
    sub.add_parser("login-wait")

    pmkd = sub.add_parser("mkdir")
    pmkd.add_argument("path", nargs="?", default="/OpenClaw")

    pls = sub.add_parser("ls")
    pls.add_argument("path", nargs="?", default="/")
    pls.add_argument("--folder-id", default=None)
    pls.add_argument("--json", action="store_true", help="Output raw JSON (debug) instead of pretty list")
    pls.add_argument("--allow-root", action="store_true", help="Allow listing '/' (privacy: disabled by default)")

    ps = sub.add_parser("search")
    ps.add_argument("keyword")
    ps.add_argument(
        "--allow-outside-openclaw",
        action="store_true",
        help="Allow returning results outside /OpenClaw (privacy: off by default)",
    )

    sub.add_parser("auth-status")

    psc = sub.add_parser("share-create")
    psc.add_argument("path", help="Remote file/folder path (within allowlist)")
    psc.add_argument("--title", default="", help="Share title")
    psc.add_argument("--days", type=int, default=0, help="Expire days, 0=permanent")
    psc.add_argument("--passcode", default=None, help="Optional extraction code (default: none)")

    psa = sub.add_parser("share-create-auto")
    psa.add_argument("keyword", help="Search keyword (agent will resolve a candidate under allowlist)")
    psa.add_argument("--pick", type=int, default=None, help="Pick 1-based index when multiple candidates are found")
    psa.add_argument("--days", type=int, default=0, help="Expire days: 1|7|30 or 0=permanent")
    psa.add_argument("--passcode", default=None, help="Optional extraction code; omit for none")
    psa.add_argument("--local", action="store_true", help="Use client-side fuzzy search via ephemeral local index (not persisted) instead of server search")
    psa.add_argument(
        "--allow-outside-openclaw",
        action="store_true",
        help="Allow searching candidates outside /OpenClaw (privacy: off by default)",
    )

    pib = sub.add_parser("index-build")
    pib.add_argument("--root", default="/OpenClaw", help="Remote root path to index (must be within allowlist)")
    pib.add_argument("--max-items", type=int, default=5000, help="Safety limit for indexed items")
    pib.add_argument("--write", action="store_true", help="Write index.json to disk (privacy sensitive; off by default)")
    pib.add_argument("--json", action="store_true", help="Output index summary as JSON")

    psl = sub.add_parser("search-local")
    psl.add_argument("keyword")
    psl.add_argument("--top", type=int, default=20)

    pss = sub.add_parser("share-save")
    pss.add_argument("share", help="Share URL or text containing https://pan.quark.cn/s/<id>")
    pss.add_argument("--passcode", default=None, help="Optional extraction code; if omitted, try parse from text")
    pss.add_argument("--to", default="/OpenClaw/FromShares", help="Target remote dir to save into (within allowlist)")
    pss.add_argument("--no-wait", action="store_true", help="Do not wait for save task completion")

    # Generic interactive orchestration helper (works for any OpenClaw channel).
    # Keep telegram-run for backward compatibility.
    pcg = sub.add_parser("channel-run")
    pcg.add_argument("op", help="Underlying quark-netdisk command to run after ensuring login")
    pcg.add_argument("op_args", nargs=argparse.REMAINDER, help="Args for the underlying command")

    ptg = sub.add_parser("telegram-run")
    ptg.add_argument("op", help="Alias of channel-run (back-compat)")
    ptg.add_argument("op_args", nargs=argparse.REMAINDER, help="Args for the underlying command")

    pu = sub.add_parser("upload")
    pu.add_argument("file")

    prn = sub.add_parser("rename")
    prn.add_argument("src")
    prn.add_argument("new_name")

    pmv = sub.add_parser("mv")
    pmv.add_argument("src")
    pmv.add_argument("dst_dir")

    prm = sub.add_parser("rm")
    prm.add_argument("src")
    prm.add_argument("--confirm", action="store_true")

    ppt = sub.add_parser("purge-trash")
    ppt.add_argument("--days", type=int, default=30)
    ppt.add_argument("--confirm", action="store_true")

    args = p.parse_args(argv)
    cfg = load_config()
    # Commands that may run without auto-login.
    # - login/login-prepare/login-wait: explicit login flows
    # - auth-status: just checks whether a stored cookie is usable
    # - channel-run/telegram-run: orchestration helper that should emit a machine-readable
    #   "need_login" payload instead of blocking on terminal polling.
    if args.cmd not in ("login", "login-prepare", "login-wait", "auth-status", "channel-run", "telegram-run"):
        ensure_logged_in(timeout=int(cfg.get("loginTimeoutSeconds", 300)), progress_mode="terminal")

    if args.cmd == "login":
        return cmd_login(args)

    if args.cmd == "login-prepare":
        timeout = int(cfg.get("loginTimeoutSeconds", 300))
        qr_png = REF / "qr_code.png"
        with QuarkSession(timeout_s=60) as s:
            token = s.get_qr_token()
            qr_url = s.build_qr_url(token)
            save_png_qr(qr_url, qr_png)
            if not args.no_open:
                try:
                    import subprocess
                    subprocess.Popen(["xdg-open", str(qr_png)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass
            out = save_login_token({"token": token, "qr_url": qr_url, "timeout": timeout})
            print(json.dumps({"qr_png": str(qr_png), "qr_url": qr_url, "token_file": str(out)}, ensure_ascii=False))
        return 0

    if args.cmd == "login-wait":
        tok = load_login_token()
        token = tok["token"]
        timeout = int(tok.get("timeout", cfg.get("loginTimeoutSeconds", 300)))
        with QuarkSession(timeout_s=60) as s:
            def progress_cb(remaining: int, msg: str):
                print(f"[login] {msg}，剩余 {remaining}s")
            st = s.poll_service_ticket(token, timeout_s=timeout, progress_cb=progress_cb, progress_interval_s=30, poll_interval_s=5.0)
            s.exchange_ticket_for_cookies(st)
            # Trigger drive-pc to set additional cookies required by upload/auth (e.g. __puus)
            try:
                # Use current cookies jar export as seed cookie string for hydration
                seed = s.export_cookies().cookie_string
                s.hydrate_drive_pc_cookies(seed)
            except Exception:
                pass

            lr = s.export_cookies()
            out = save_session({"source": "api-qr", "service_ticket": st, "cookieString": lr.cookie_string, "cookies": lr.cookies_json})
            print(json.dumps({"ok": True, "session": str(out)}, ensure_ascii=False))
        return 0
    if args.cmd in ("channel-run", "telegram-run"):
        # Orchestration helper for OpenClaw channels: if not logged in, prepare QR and exit with a machine-readable payload.
        # Expected caller behavior:
        #   1) Run `channel-run <op> ...`
        #   2) If exit code == 10, read JSON, send qr_png to *the current channel/chat*,
        #      then run `login-wait` and forward progress every 30s, then re-run channel-run.
        st_code = main(["auth-status"])
        if st_code != 0:
            timeout = int(cfg.get("loginTimeoutSeconds", 300))
            qr_png = REF / "qr_code.png"
            with QuarkSession(timeout_s=60) as s:
                token = s.get_qr_token()
                qr_url = s.build_qr_url(token)
                save_png_qr(qr_url, qr_png)
                out = save_login_token({"token": token, "qr_url": qr_url, "timeout": timeout})
            _print_json(
                {
                    "need_login": True,
                    "qr_png": str(qr_png),
                    "qr_url": qr_url,
                    "token_file": str(out),
                    "hint": "Send qr_png to user on current channel, then run login-wait; re-run channel-run afterwards.",
                }
            )
            return EXIT_NEED_LOGIN

        op = args.op
        op_args = list(args.op_args or [])
        if op.startswith("-"):
            raise SystemExit("op must be a command name")
        return main([op] + op_args)

    if args.cmd == "mkdir":
        return cmd_mkdir(args)
    if args.cmd == "ls":
        cfg = load_config()
        remote_allow = remote_allowlist(cfg)
        with open_authed_session(timeout_s=60) as s:
            if args.folder_id is not None:
                folder_id = str(args.folder_id)
                lst = list_folder(s, parent_id=folder_id, size=200)
                if args.json:
                    print(json.dumps({"folder_id": folder_id, "count": len(lst), "list": lst[:50]}, ensure_ascii=False)[:2000])
                else:
                    # pretty output: — for folders, • for files
                    items = sorted(lst, key=lambda it: (0 if it.get('dir') else 1, it.get('file_name','')))
                    for it in items:
                        name = it.get('file_name','')
                        print(f"— {name}" if it.get('dir') else f"• {name}")
                return 0

            # path mode (preferred)
            path = args.path
            # Privacy default: do not allow listing '/' unless explicitly requested.
            if path == "/" and not args.allow_root:
                _print_json({
                    "ok": False,
                    "need_confirm": True,
                    "op": "ls",
                    "path": "/",
                    "reason": "Listing '/' may expose private top-level folder names. Re-run with --allow-root if you really want it.",
                    "how_to_confirm": "Re-run with: ls / --allow-root",
                })
                return EXIT_NEED_CONFIRM

            if path != "/":
                enforce_remote_allowlist(path, remote_allow)
            folder_id = resolve_remote_fid(s, path)
            lst = list_folder(s, parent_id=folder_id, size=200)
            if args.json:
                print(json.dumps({"path": path, "folder_id": folder_id, "count": len(lst), "list": lst[:50]}, ensure_ascii=False)[:2000])
            else:
                items = sorted(lst, key=lambda it: (0 if it.get('dir') else 1, it.get('file_name','')))
                for it in items:
                    name = it.get('file_name','')
                    print(f"— {name}" if it.get('dir') else f"• {name}")
        return 0
    if args.cmd == "search":
        with open_authed_session(timeout_s=60) as s:
            res = search(s, args.keyword, page=1, size=50)

            if not bool(args.allow_outside_openclaw):
                # Filter results to /OpenClaw/** by resolving fid -> path.
                lst = (res.get("data") or {}).get("list") or []
                kept = []
                for it in lst:
                    try:
                        fid = str(it.get("fid"))
                        if not fid:
                            continue
                        full_path = resolve_fid_path(s, fid)
                        if full_path == DEFAULT_SEARCH_ROOT or full_path.startswith(DEFAULT_SEARCH_ROOT + "/"):
                            kept.append(it)
                    except Exception:
                        continue
                # Mutate response minimally
                res = dict(res)
                res["data"] = dict(res.get("data") or {})
                res["data"]["list"] = kept
                res["metadata"] = dict(res.get("metadata") or {})
                res["metadata"]["scoped_root"] = DEFAULT_SEARCH_ROOT

            print(json.dumps(res, ensure_ascii=False)[:2000])
        return 0

    if args.cmd == "auth-status":
        try:
            _ = load_cookie_string()
        except Exception as e:
            print(json.dumps({"ok": False, "reason": f"no-session: {e}", "action": "run login"}, ensure_ascii=False))
            return 1

        with open_authed_session(timeout_s=30) as s:
            try:
                # smallest auth check: list root
                res = list_folder(s, parent_id="0", size=1)
                _ = res
                print(json.dumps({"ok": True, "message": "cookie valid for drive-pc", "action": "none"}, ensure_ascii=False))
                return 0
            except Exception as e:
                print(json.dumps({"ok": False, "reason": str(e), "action": "run login"}, ensure_ascii=False)[:2000])
                return 2

    if args.cmd == "share-create":
        cfg = load_config()
        remote_allow = remote_allowlist(cfg)
        enforce_remote_allowlist(args.path, remote_allow)

        with open_authed_session(timeout_s=60) as s:
            fid = resolve_remote_fid(s, args.path)
            info = create_share(
                s,
                [fid],
                title=args.title or "",
                expire_days=int(args.days or 0),
                passcode=args.passcode,
            )
            # best-effort extract
            out = {
                "ok": True,
                "path": args.path,
                "fid": fid,
                "share": info,
                "share_url": info.get("share_url") or info.get("url"),
                "share_id": info.get("pwd_id") or info.get("share_id"),
                "passcode": args.passcode,
                "expire_days": int(args.days or 0),
            }
            print(json.dumps(out, ensure_ascii=False)[:2000])
        return 0

    if args.cmd == "share-save":
        cfg = load_config()
        remote_allow = remote_allowlist(cfg)
        target_dir = args.to
        enforce_remote_allowlist(target_dir, remote_allow)

        share_id, parsed_pass = parse_share_url(args.share)
        passcode = args.passcode or parsed_pass

        with open_authed_session(timeout_s=60) as s:
            stoken = get_share_token(s, share_id, passcode)
            # optional: fetch detail to show file count/title
            detail = get_share_detail(s, share_id, stoken)

            to_fid = ensure_remote_dir(s, target_dir)
            res = save_share_to_my_drive(
                s,
                share_id=share_id,
                stoken=stoken,
                to_pdir_fid=to_fid,
                save_all=True,
                wait=not bool(args.no_wait),
            )
            print(
                json.dumps(
                    {
                        "ok": True,
                        "share_id": share_id,
                        "to": target_dir,
                        "to_fid": to_fid,
                        "share_detail": (detail.get("data") if isinstance(detail, dict) else None),
                        "result": res,
                    },
                    ensure_ascii=False,
                )[:2000]
            )
        return 0

    if args.cmd == "index-build":
        cfg = load_config()
        remote_allow = remote_allowlist(cfg)
        root = args.root
        with open_authed_session(timeout_s=60) as s:
            idx = _build_index(
                session=s,
                root_path=root,
                remote_allow=remote_allow,
                max_items=int(args.max_items),
                write_file=bool(args.write),
            )
        if args.json:
            _print_json({"ok": True, "index": {k: idx.get(k) for k in ("root", "count", "max_items", "generated_at")}, "written": bool(args.write)})
        else:
            if args.write:
                print(f"index built+written: root={idx.get('root')} count={idx.get('count')} -> {_index_path()}")
            else:
                print(f"index built (ephemeral): root={idx.get('root')} count={idx.get('count')} (not written)")
        return 0

    if args.cmd == "search-local":
        # Privacy default: build ephemeral index on demand and do NOT persist.
        cfg = load_config()
        remote_allow = remote_allowlist(cfg)
        with open_authed_session(timeout_s=60) as s:
            idx = _build_index(session=s, root_path="/OpenClaw", remote_allow=remote_allow, max_items=5000, write_file=False)
            hits = _search_local_index(idx, args.keyword, top=int(args.top))
        _print_json({"ok": True, "keyword": args.keyword, "count": len(hits), "hits": hits, "ephemeral": True})
        return 0

    if args.cmd == "share-create-auto":
        cfg = load_config()
        remote_allow = remote_allowlist(cfg)
        # enforce days option set
        if int(args.days) not in (0, 1, 7, 30):
            raise ValueError("--days must be one of 0,1,7,30")

        with open_authed_session(timeout_s=60) as s:
            cands: list[dict[str, Any]] = []

            scope_root = DEFAULT_SEARCH_ROOT
            if bool(args.allow_outside_openclaw):
                scope_root = "/"  # still constrained by remoteAllowlist

            if args.local:
                # Privacy default: build ephemeral index in-memory; do NOT write index.json.
                idx = _build_index(session=s, root_path=DEFAULT_SEARCH_ROOT, remote_allow=remote_allow, max_items=5000, write_file=False)
                hits = _search_local_index(idx, args.keyword, top=50)
                cands = [{"path": h.get("path"), "fid": h.get("fid"), "name": h.get("name"), "is_dir": bool(h.get("is_dir")), "score": h.get("score")} for h in hits]
            else:
                res = search(s, args.keyword, page=1, size=50)
                lst = (res.get("data") or {}).get("list") or []
                for it in lst:
                    try:
                        fid = str(it.get("fid"))
                        if not fid:
                            continue
                        full_path = resolve_fid_path(s, fid)
                        enforce_remote_allowlist(full_path, remote_allow)
                        # Default privacy scope: /OpenClaw only
                        if scope_root != "/" and not (full_path == scope_root or full_path.startswith(scope_root + "/")):
                            continue
                        cands.append({"path": full_path, "fid": fid, "name": it.get("file_name"), "is_dir": bool(it.get("dir"))})
                    except Exception:
                        continue

            if not cands:
                _print_json({"ok": False, "reason": "no-candidate-under-allowlist", "keyword": args.keyword})
                return 4

            if len(cands) > 1 and args.pick is None:
                _print_json({"ok": False, "need_pick": True, "keyword": args.keyword, "candidates": cands[:20]})
                return EXIT_NEED_PICK

            pick = int(args.pick or 1)
            if pick < 1 or pick > len(cands):
                raise ValueError(f"--pick out of range: 1..{len(cands)}")
            chosen = cands[pick - 1]
            info = create_share(
                s,
                [chosen["fid"]],
                title=chosen.get("name") or "",
                expire_days=int(args.days or 0),
                passcode=args.passcode,
            )
            out = {
                "ok": True,
                "keyword": args.keyword,
                "chosen": chosen,
                "share": info,
                "share_url": info.get("share_url") or info.get("url"),
                "share_id": info.get("pwd_id") or info.get("share_id"),
                "passcode": args.passcode,
                "expire_days": int(args.days or 0),
            }
            _print_json(out)
        return 0

    if args.cmd == "upload":
        return cmd_upload(args)

    cfg = load_config()
    remote_allow = remote_allowlist(cfg)

    if args.cmd == "rename":
        enforce_remote_allowlist(args.src, remote_allow)
        with open_authed_session(timeout_s=60) as s:
            fid = resolve_remote_fid(s, args.src)
            res = rename_file(s, fid, args.new_name)
            print(json.dumps({"op": "rename", "src": args.src, "new_name": args.new_name, "result": res}, ensure_ascii=False)[:2000])
        return 0

    if args.cmd == "mv":
        enforce_remote_allowlist(args.src, remote_allow)
        enforce_remote_allowlist(args.dst_dir, remote_allow)
        with open_authed_session(timeout_s=60) as s:
            src_fid = resolve_remote_fid(s, args.src)
            dst_fid = ensure_remote_dir(s, args.dst_dir)
            # API expects `filelist` (and rejects unknown `fid`).
            # Some backends reject providing both current_dir_fid and filelist, so we only send filelist.
            res = s.api_post(
                "file/move",
                json_data={"filelist": [src_fid], "to_pdir_fid": dst_fid},
            )
            print(json.dumps({"op": "mv", "src": args.src, "dst_dir": args.dst_dir, "result": res}, ensure_ascii=False)[:2000])
        return 0

    if args.cmd == "rm":
        if not args.confirm:
            _print_json({
                "ok": False,
                "need_confirm": True,
                "op": "rm",
                "src": args.src,
                "how_to_confirm": "Re-run with: rm <src> --confirm",
            })
            return EXIT_NEED_CONFIRM
        enforce_remote_allowlist(args.src, remote_allow)
        with open_authed_session(timeout_s=60) as s:
            res = soft_delete_to_trash(s, args.src)
            _print_json({"ok": True, "op": "rm", "src": args.src, "result": res})
        return 0

    if args.cmd == "purge-trash":
        if not args.confirm:
            _print_json({
                "ok": False,
                "need_confirm": True,
                "op": "purge-trash",
                "days": args.days,
                "how_to_confirm": "Re-run with: purge-trash --days <n> --confirm",
            })
            return EXIT_NEED_CONFIRM
        # purge only operates inside /OpenClaw/.trash
        enforce_remote_allowlist("/OpenClaw/.trash", remote_allow)
        with open_authed_session(timeout_s=60) as s:
            res = purge_trash(s, trash_root="/OpenClaw/.trash", retention_days=int(args.days))
            _print_json({"ok": True, "op": "purge-trash", "days": args.days, "result": res})
        return 0

    raise SystemExit(2)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
