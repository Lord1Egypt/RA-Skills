#!/usr/bin/env python3
"""Transactional current-session browser remote desktop helper.

Architecture:
- GNOME Remote Desktop VNC against the current live GNOME/Wayland session only.
- Apache Guacamole + guacd in short-lived Podman containers.
- Cloudflare Quick Tunnel container exposes only Guacamole over an outbound tunnel.

Hard requirement: current live desktop session. No headless/fresh desktop fallback.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import secrets
import shutil
import socket
import string
import subprocess
import time
import urllib.parse
import urllib.request
import xml.sax.saxutils as saxutils
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

STATE_DIR = Path.home() / ".openclaw" / "remote-support"
CONFIG_DIR = STATE_DIR / "guacamole"
STATE_FILE = STATE_DIR / "session.json"
LOG_FILE = STATE_DIR / "remote-support.log"
OWNED_PREFIX = "openclaw-remote-support"
GUACD_CONTAINER = f"{OWNED_PREFIX}-guacd"
GUAC_CONTAINER = f"{OWNED_PREFIX}-guacamole"
TUNNEL_CONTAINER = f"{OWNED_PREFIX}-tunnel"
NETWORK = f"{OWNED_PREFIX}-net"
GUACD_IMAGE = "docker.io/guacamole/guacd:latest"
GUAC_IMAGE = "docker.io/guacamole/guacamole:latest"
CLOUDFLARED_IMAGE = "docker.io/cloudflare/cloudflared:latest"
GUAC_LOCAL_PORT = 18080
VNC_PORT = 1024
RELEVANT_PORTS = [1024, 3389, 5900, 5901, 6080, 8080, 8081, GUAC_LOCAL_PORT]
TTL_RE = re.compile(r"^([1-9][0-9]*)(m|h)$")
URL_RE = re.compile(r"https://[-a-zA-Z0-9.]+\.trycloudflare\.com")
IDLE_DELAY_KEY = ("org.gnome.desktop.session", "idle-delay")
LOCK_ENABLED_KEY = ("org.gnome.desktop.screensaver", "lock-enabled")
IDLE_ACTIVATION_KEY = ("org.gnome.desktop.screensaver", "idle-activation-enabled")


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    required: bool = False


def log(event: str, *, create_dir: bool = True, **fields: Any) -> None:
    if create_dir:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
    elif not STATE_DIR.exists():
        return
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "event": event, **fields}
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


def run(cmd: list[str], timeout: int = 10) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError as e:
        return 127, "", str(e)
    except subprocess.TimeoutExpired as e:
        return 124, e.stdout or "", e.stderr or f"timeout after {timeout}s"


def which(bin_name: str) -> str | None:
    return shutil.which(bin_name)


def podman(*args: str, timeout: int = 30) -> tuple[int, str, str]:
    return run(["podman", *args], timeout=timeout)


def port_open(host: str, port: int, timeout: float = 0.2) -> bool:
    family = socket.AF_INET6 if ":" in host else socket.AF_INET
    with socket.socket(family, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        target = (host, port, 0, 0) if family == socket.AF_INET6 else (host, port)
        return s.connect_ex(target) == 0


def ss_lines_for_ports() -> list[str]:
    code, out, _ = run(["ss", "-ltnp"], timeout=5)
    if code != 0 or not out:
        return []
    return [line for line in out.splitlines() if any(f":{p}" in line for p in RELEVANT_PORTS)]


def listeners() -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for port in RELEVANT_PORTS:
        if port_open("127.0.0.1", port):
            found.append({"host": "127.0.0.1", "port": port})
    for line in ss_lines_for_ports():
        found.append({"ss": line})
    return found


def container_rows() -> list[str]:
    if not which("podman"):
        return []
    code, out, err = podman("ps", "-a", "--format", "{{.Names}} {{.Image}} {{.Status}}", timeout=10)
    if code != 0:
        return [f"podman error: {err or out}"]
    return [row for row in out.splitlines() if row.startswith(OWNED_PREFIX)]


def load_state() -> dict[str, Any] | None:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        return {"corrupt": True, "error": str(e), "path": str(STATE_FILE)}


def ensure_state_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(STATE_DIR, 0o700)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # Guacamole's container entrypoint must be able to read/copy this mounted directory.
    os.chmod(CONFIG_DIR, 0o755)


def save_state(obj: dict[str, Any]) -> None:
    ensure_state_dirs()
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(STATE_FILE)
    os.chmod(STATE_FILE, 0o600)


def public_state(state: dict[str, Any] | None) -> dict[str, Any] | None:
    if state is None:
        return None
    redacted = dict(state)
    if redacted.get("password"):
        redacted["password"] = "***"
    if redacted.get("one_click_url"):
        redacted["one_click_url"] = "***"
    return redacted


def write_json(obj: Any) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True))


def random_password(n: int = 24) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))


def random_vnc_password() -> str:
    # GNOME Remote Desktop VNC rejects long passwords; VNC password semantics are historically 8-byte limited.
    return random_password(8)


def random_guac_password() -> str:
    # Human handoff is one-click-token-first; keep the underlying Guacamole password high entropy.
    return random_password(32)


def ttl_seconds(ttl: str) -> int:
    m = TTL_RE.match(ttl)
    if not m:
        raise ValueError("invalid TTL")
    return int(m.group(1)) * (60 if m.group(2) == "m" else 3600)


def ttl_valid(ttl: str) -> bool:
    return TTL_RE.match(ttl) is not None


def gsettings_get(schema: str, key: str) -> str | None:
    code, out, _ = run(["gsettings", "get", schema, key], timeout=10)
    return out if code == 0 else None


def gsettings_set(schema: str, key: str, value: str) -> None:
    code, out, err = run(["gsettings", "set", schema, key, value], timeout=10)
    if code != 0:
        raise RuntimeError(f"gsettings set {schema} {key} failed: {err or out}")


def get_vnc_encryption() -> str:
    return gsettings_get("org.gnome.desktop.remote-desktop.vnc", "encryption") or "['tls-anon']"


def set_vnc_encryption(value: str) -> None:
    if which("gsettings"):
        gsettings_set("org.gnome.desktop.remote-desktop.vnc", "encryption", value)


def disable_idle_lock_temporarily() -> dict[str, str | None]:
    previous = {
        "idle_delay": gsettings_get(*IDLE_DELAY_KEY),
        "lock_enabled": gsettings_get(*LOCK_ENABLED_KEY),
        "idle_activation_enabled": gsettings_get(*IDLE_ACTIVATION_KEY),
    }
    gsettings_set(*IDLE_DELAY_KEY, "0")
    gsettings_set(*LOCK_ENABLED_KEY, "false")
    gsettings_set(*IDLE_ACTIVATION_KEY, "false")
    return previous


def restore_idle_lock(previous: dict[str, str | None] | None) -> None:
    if not previous:
        return
    for key, setting in [
        ("idle_delay", IDLE_DELAY_KEY),
        ("lock_enabled", LOCK_ENABLED_KEY),
        ("idle_activation_enabled", IDLE_ACTIVATION_KEY),
    ]:
        value = previous.get(key)
        if value is not None:
            run(["gsettings", "set", *setting, value], timeout=10)


def current_session_id() -> str:
    code, out, err = run(["loginctl", "list-sessions", "--no-legend"], timeout=10)
    if code != 0:
        raise RuntimeError(f"cannot list login sessions: {err or out}")
    candidates: list[str] = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[2] == os.environ.get("USER", "riclewis") and parts[3] == "seat0":
            candidates.append(parts[0])
    if not candidates:
        raise RuntimeError("no active seat0 GNOME session found for current user; refusing headless/fresh fallback")
    return candidates[0]


def session_props(session_id: str) -> dict[str, str]:
    fields = ["Id", "Name", "User", "Type", "Class", "Active", "State", "Remote", "Service", "Seat", "LockedHint", "IdleHint"]
    # Build command this way for compatibility with loginctl's repeated -p flags.
    cmd = ["loginctl", "show-session", session_id]
    for f in fields:
        cmd.extend(["-p", f])
    code, out, err = run(cmd, timeout=10)
    if code != 0:
        raise RuntimeError(f"cannot inspect session {session_id}: {err or out}")
    props: dict[str, str] = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            props[k] = v
    return props


def session_locked(session_id: str | None = None) -> tuple[bool, str]:
    sid = session_id or current_session_id()
    props = session_props(sid)
    return props.get("LockedHint") == "yes", "; ".join(f"{k}={v}" for k, v in sorted(props.items()))


def assert_current_live_session_ready(*, allow_unlock: bool) -> dict[str, Any]:
    sid = current_session_id()
    props = session_props(sid)
    if props.get("Type") != "wayland" or props.get("Active") != "yes" or props.get("Seat") != "seat0":
        raise RuntimeError(f"session {sid} is not the active live Wayland seat0 session: {props}")
    if props.get("LockedHint") == "yes":
        if not allow_unlock:
            raise RuntimeError("current GNOME session is locked; rerun with --unlock-current-session if Ric explicitly approves unlocking")
        code, out, err = run(["loginctl", "unlock-session", sid], timeout=10)
        if code != 0:
            raise RuntimeError(f"current GNOME session is locked and unlock failed: {err or out}")
        time.sleep(1)
        props = session_props(sid)
        if props.get("LockedHint") == "yes":
            raise RuntimeError("current GNOME session remained locked after unlock-session; refusing to expose broken remote desktop")
        return {"session_id": sid, "was_locked": True, "props": props}
    return {"session_id": sid, "was_locked": False, "props": props}


def grd_status() -> tuple[bool, str]:
    if not which("grdctl"):
        return False, "grdctl missing"
    code, out, err = run(["grdctl", "status"], timeout=8)
    return code == 0, (out or err)[:2000]


def firewall_cmd_available() -> bool:
    return which("firewall-cmd") is not None and run(["firewall-cmd", "--state"], timeout=5)[0] == 0


def vnc_port_allowed_by_firewalld() -> bool:
    if not firewall_cmd_available():
        return False
    code, out, _ = run(["firewall-cmd", "--query-port", f"{VNC_PORT}/tcp"], timeout=10)
    return code == 0 and out.strip() == "yes"


def preflight(args: argparse.Namespace) -> int:
    checks: list[Check] = []
    for b in ["python3", "podman", "grdctl", "curl", "firewall-cmd", "loginctl", "gsettings"]:
        checks.append(Check(f"bin:{b}", which(b) is not None, which(b) or "missing", required=True))
    checks.append(Check("session:wayland", os.environ.get("XDG_SESSION_TYPE") == "wayland", f"XDG_SESSION_TYPE={os.environ.get('XDG_SESSION_TYPE','')}", required=False))
    ok, detail = grd_status()
    checks.append(Check("gnome-remote-desktop:status", ok, detail, required=True))
    try:
        locked, lock_detail = session_locked()
        checks.append(Check("current-session:present", True, f"locked={locked}; {lock_detail}", required=True))
    except Exception as e:
        checks.append(Check("current-session:present", False, str(e), required=True))
    if which("podman"):
        for img in [GUACD_IMAGE, GUAC_IMAGE, CLOUDFLARED_IMAGE]:
            code, out, err = podman("manifest", "inspect", img, timeout=35)
            checks.append(Check(f"image:{img}", code == 0, "available" if code == 0 else (err or out)[:500], required=False))
    report = {
        "ok": all(c.ok for c in checks if c.required),
        "state_dir": str(STATE_DIR),
        "checks": [asdict(c) for c in checks],
        "listeners": listeners(),
        "owned_containers": container_rows(),
        "firewalld_active": firewall_cmd_available(),
        "vnc_port_allowed_by_firewalld": vnc_port_allowed_by_firewalld(),
        "notes": [
            "Current live GNOME session is mandatory; headless/fresh desktop is not an acceptable fallback.",
            "Current-session sharing fails while GNOME is locked; open refuses unless --unlock-current-session is explicitly passed.",
            "VNC uses port 1024 because FedoraWorkstation opens 1025-65535/tcp by default.",
        ],
    }
    write_json(report)
    log("preflight", ok=report["ok"])
    return 0 if report["ok"] else 2


def status(args: argparse.Namespace) -> int:
    report = {
        "active_state": public_state(load_state()),
        "state_file": str(STATE_FILE),
        "listeners": listeners(),
        "owned_containers": container_rows(),
        "firewalld_active": firewall_cmd_available(),
        "vnc_port_allowed_by_firewalld": vnc_port_allowed_by_firewalld(),
        "log_file": str(LOG_FILE),
    }
    write_json(report)
    return 0


def ensure_network() -> None:
    code, _, _ = podman("network", "exists", NETWORK, timeout=10)
    if code != 0:
        code, out, err = podman("network", "create", NETWORK, timeout=20)
        if code != 0:
            raise RuntimeError(f"podman network create failed: {err or out}")


def install(args: argparse.Namespace) -> int:
    plan = {
        "dry_run": args.dry_run,
        "create_dirs": [str(STATE_DIR), str(CONFIG_DIR)],
        "pull_images": [GUACD_IMAGE, GUAC_IMAGE, CLOUDFLARED_IMAGE],
        "create_network": NETWORK,
        "no_auto_start": True,
    }
    if args.dry_run:
        write_json(plan)
        log("install_dry_run")
        return 0
    ensure_state_dirs()
    pulled: list[str] = []
    for img in [GUACD_IMAGE, GUAC_IMAGE, CLOUDFLARED_IMAGE]:
        code, out, err = podman("pull", img, timeout=300)
        if code != 0:
            write_json({"ok": False, "error": f"failed to pull {img}", "detail": err or out, "pulled": pulled})
            return 5
        pulled.append(img)
    ensure_network()
    (STATE_DIR / "README.txt").write_text("OpenClaw remote-support skill runtime state. Safe to remove after close/uninstall.\n", encoding="utf-8")
    write_json({**plan, "ok": True, "pulled": pulled})
    log("install", pulled=pulled)
    return 0


def xml_attr(value: str) -> str:
    return saxutils.escape(value, {'"': '&quot;'})


def write_guacamole_config(guac_user: str, guac_pass: str, vnc_pass: str, mode: str) -> None:
    ensure_state_dirs()
    (CONFIG_DIR / "guacamole.properties").write_text(
        f"guacd-hostname: {GUACD_CONTAINER}\nguacd-port: 4822\napi-session-timeout: 10\n",
        encoding="utf-8",
    )
    read_only = "true" if mode == "view-only" else "false"
    xml = f"""<user-mapping>
  <authorize username=\"{xml_attr(guac_user)}\" password=\"{xml_attr(guac_pass)}\">
    <connection name=\"Tommy Current Desktop ({xml_attr(mode)})\">
      <protocol>vnc</protocol>
      <param name=\"hostname\">host.containers.internal</param>
      <param name=\"port\">{VNC_PORT}</param>
      <param name=\"password\">{xml_attr(vnc_pass)}</param>
      <param name=\"read-only\">{read_only}</param>
    </connection>
  </authorize>
</user-mapping>
"""
    (CONFIG_DIR / "user-mapping.xml").write_text(xml, encoding="utf-8")
    os.chmod(CONFIG_DIR / "user-mapping.xml", 0o644)


def enable_vnc(vnc_pass: str, mode: str) -> None:
    if vnc_port_allowed_by_firewalld():
        raise RuntimeError(f"firewalld allows {VNC_PORT}/tcp; refusing to expose current-session VNC")
    set_vnc_encryption("['none']")
    cmds = [
        ["grdctl", "vnc", "set-port", str(VNC_PORT)],
        ["grdctl", "vnc", "set-auth-method", "password"],
        ["grdctl", "vnc", "set-password", vnc_pass],
        ["grdctl", "vnc", "enable-view-only"] if mode == "view-only" else ["grdctl", "vnc", "disable-view-only"],
        ["grdctl", "vnc", "enable"],
    ]
    for cmd in cmds:
        code, out, err = run(cmd, timeout=15)
        if code != 0:
            raise RuntimeError(f"{' '.join(cmd)} failed: {err or out}")
    for _ in range(20):
        if port_open("127.0.0.1", VNC_PORT):
            return
        time.sleep(0.25)
    raise RuntimeError(f"VNC did not start on localhost port {VNC_PORT}")


def disable_vnc() -> None:
    if which("grdctl"):
        run(["grdctl", "vnc", "disable"], timeout=15)
        run(["grdctl", "vnc", "clear-password"], timeout=15)
        run(["grdctl", "vnc", "enable-view-only"], timeout=15)


def start_guacamole() -> None:
    ensure_network()
    for name in [TUNNEL_CONTAINER, GUAC_CONTAINER, GUACD_CONTAINER]:
        podman("rm", "-f", name, timeout=30)
    code, out, err = podman("run", "-d", "--name", GUACD_CONTAINER, "--network", NETWORK, GUACD_IMAGE, timeout=60)
    if code != 0:
        raise RuntimeError(f"guacd start failed: {err or out}")
    code, out, err = podman(
        "run", "-d", "--name", GUAC_CONTAINER,
        "--network", NETWORK,
        "-p", f"127.0.0.1:{GUAC_LOCAL_PORT}:8080",
        "-e", "WEBAPP_CONTEXT=ROOT",
        "-v", f"{CONFIG_DIR}:/etc/guacamole:Z,ro",
        GUAC_IMAGE,
        timeout=90,
    )
    if code != 0:
        raise RuntimeError(f"guacamole start failed: {err or out}")
    for _ in range(100):
        if port_open("127.0.0.1", GUAC_LOCAL_PORT):
            code, out, _ = run(["curl", "-fsS", f"http://127.0.0.1:{GUAC_LOCAL_PORT}/"], timeout=5)
            if code == 0 and ("Guacamole" in out or "guacamole" in out):
                return
        time.sleep(0.5)
    _, logs, logs_err = podman("logs", GUAC_CONTAINER, timeout=10)
    raise RuntimeError(f"Guacamole did not become healthy; logs={(logs or logs_err)[-3000:]}")


def start_tunnel() -> tuple[str, str]:
    podman("rm", "-f", TUNNEL_CONTAINER, timeout=20)
    code, out, err = podman(
        "run", "-d", "--name", TUNNEL_CONTAINER,
        "--network", "host",
        CLOUDFLARED_IMAGE,
        "tunnel", "--no-autoupdate", "--url", f"http://127.0.0.1:{GUAC_LOCAL_PORT}",
        timeout=60,
    )
    if code != 0:
        raise RuntimeError(f"cloudflared tunnel start failed: {err or out}")
    for _ in range(60):
        _, logs, logs_err = podman("logs", TUNNEL_CONTAINER, timeout=10)
        text = logs + "\n" + logs_err
        m = URL_RE.search(text)
        if m:
            return m.group(0), text[-2000:]
        time.sleep(0.5)
    _, logs, logs_err = podman("logs", TUNNEL_CONTAINER, timeout=10)
    raise RuntimeError(f"tunnel URL not found in cloudflared logs: {(logs or logs_err)[-3000:]}")


def schedule_expiry(ttl: str) -> dict[str, Any]:
    sec = ttl_seconds(ttl)
    code, out, err = run([
        "systemd-run", "--user", "--collect", f"--unit={OWNED_PREFIX}-expiry", f"--on-active={sec}", "/usr/bin/python3", str(Path(__file__).resolve()), "close"
    ], timeout=15)
    if code == 0:
        return {"method": "systemd-run", "seconds": sec, "detail": out}
    return {"method": "none", "seconds": sec, "error": err or out}


def running_inside_expiry_unit() -> bool:
    try:
        text = Path("/proc/self/cgroup").read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False
    return f"{OWNED_PREFIX}-expiry.service" in text


def guacamole_one_click_url(state: dict[str, Any]) -> dict[str, Any]:
    base = f"http://127.0.0.1:{GUAC_LOCAL_PORT}"
    data = urllib.parse.urlencode({"username": state["username"], "password": state["password"]}).encode()
    req = urllib.request.Request(f"{base}/api/tokens", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=10) as r:
        token = json.load(r)["authToken"]
    tree_url = f"{base}/api/session/data/default/connectionGroups/ROOT/tree?token={urllib.parse.quote(token)}"
    with urllib.request.urlopen(tree_url, timeout=10) as r:
        tree = json.load(r)
    conns = tree.get("childConnections") or []
    if not conns:
        raise RuntimeError("no Guacamole connections found")
    identifier = conns[0]["identifier"]
    raw = (identifier + "\x00c\x00default").encode()
    encoded = base64.b64encode(raw).decode().rstrip("=").replace("+", "-").replace("/", "_")
    return {"connection": identifier, "url": state["public_url"].rstrip("/") + "/#/client/" + encoded + "?token=" + token}


def verify_local_auth(state: dict[str, Any]) -> dict[str, Any]:
    one_click = guacamole_one_click_url(state)
    return {"ok": True, "connection": one_click["connection"]}


def open_output(state: dict[str, Any], one_click: dict[str, Any], expiry: dict[str, Any], auth_check: dict[str, Any], *, one_click_only: bool) -> dict[str, Any]:
    base = {
        "ok": True,
        "one_click_url": one_click["url"],
        "warning": "one_click_url is password-equivalent until the session expires/closes",
        "connection": one_click["connection"],
        "ttl": state.get("ttl"),
        "mode": state.get("mode"),
        "expiry": expiry,
        "auth_check": auth_check,
    }
    if not one_click_only:
        base.update({
            "url": state.get("public_url"),
            "username": state.get("username"),
            "password": state.get("password"),
        })
    return base


def open_session(args: argparse.Namespace) -> int:
    if not ttl_valid(args.ttl):
        write_json({"ok": False, "error": "invalid TTL; use a positive integer followed by m or h, e.g. 10m or 1h", "ttl": args.ttl})
        return 2
    if load_state() and not args.force:
        write_json({"ok": False, "error": "active or stale state exists; run status/close first", "state_file": str(STATE_FILE)})
        return 3
    plan = {
        "dry_run": args.dry_run,
        "ttl": args.ttl,
        "mode": args.mode,
        "will_start": ["verify current live GNOME session", "optionally unlock only with --unlock-current-session", "disable idle lock temporarily", "GNOME current-session VNC", "Guacamole+guacd", "Cloudflare Quick Tunnel"],
        "local_url": f"http://127.0.0.1:{GUAC_LOCAL_PORT}/",
    }
    if args.dry_run:
        write_json({"ok": True, **plan})
        log("open_dry_run", ttl=args.ttl, mode=args.mode)
        return 0
    guac_user = "ric"
    guac_pass = random_guac_password()
    vnc_pass = random_vnc_password()
    started: list[str] = []
    try:
        ensure_state_dirs()
        previous_vnc_encryption = get_vnc_encryption()
        previous_lock_settings = {
            "idle_delay": gsettings_get(*IDLE_DELAY_KEY),
            "lock_enabled": gsettings_get(*LOCK_ENABLED_KEY),
            "idle_activation_enabled": gsettings_get(*IDLE_ACTIVATION_KEY),
        }
        provisional_state = {
            "status": "opening",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "ttl": args.ttl,
            "mode": args.mode,
            "previous_vnc_encryption": previous_vnc_encryption,
            "previous_lock_settings": previous_lock_settings,
        }
        save_state(provisional_state)
        unlock_info = assert_current_live_session_ready(allow_unlock=args.unlock_current_session)
        disable_idle_lock_temporarily()
        write_guacamole_config(guac_user, guac_pass, vnc_pass, args.mode)
        enable_vnc(vnc_pass, args.mode)
        started.append("current-session-vnc")
        start_guacamole()
        started.append("guacamole")
        public_url, _tunnel_log_tail = start_tunnel()
        started.append("tunnel")
        expiry = schedule_expiry(args.ttl)
        state = {
            "status": "open",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "ttl": args.ttl,
            "mode": args.mode,
            "public_url": public_url,
            "local_url": f"http://127.0.0.1:{GUAC_LOCAL_PORT}/",
            "username": guac_user,
            "password": guac_pass,
            "containers": [GUACD_CONTAINER, GUAC_CONTAINER, TUNNEL_CONTAINER],
            "expiry": expiry,
            "previous_vnc_encryption": previous_vnc_encryption,
            "previous_lock_settings": previous_lock_settings,
            "unlock_info": unlock_info,
        }
        save_state(state)
        auth_check = verify_local_auth(state)
        one_click = guacamole_one_click_url(state)
        write_json(open_output(state, one_click, expiry, auth_check, one_click_only=args.one_click_only))
        log("open", ttl=args.ttl, mode=args.mode, tunnel_started=True, expiry_method=expiry.get("method"))
        return 0
    except Exception as e:
        close(argparse.Namespace(dry_run=False))
        write_json({"ok": False, "error": str(e), "started_before_failure": started})
        log("open_failed", error=str(e), started=started)
        return 10


def link_session(args: argparse.Namespace) -> int:
    state = load_state()
    if not state:
        write_json({"ok": False, "error": "no active remote-support session"})
        return 2
    try:
        one_click = guacamole_one_click_url(state)
    except Exception as e:
        write_json({"ok": False, "error": str(e)})
        return 3
    write_json({"ok": True, "one_click_url": one_click["url"], "warning": "one_click_url is password-equivalent until the session expires/closes", "connection": one_click["connection"], "ttl": state.get("ttl"), "mode": state.get("mode")})
    return 0


def close(args: argparse.Namespace) -> int:
    actions: list[str] = []
    prior_state = load_state()
    if not args.dry_run:
        # When this function is invoked by the expiry service, stopping the service
        # itself kills the cleanup process before it reaches the container/VNC teardown.
        # Stop the timer, but never stop our own currently-running expiry service.
        run(["systemctl", "--user", "stop", f"{OWNED_PREFIX}-expiry.timer"], timeout=10)
        if not running_inside_expiry_unit():
            run(["systemctl", "--user", "stop", f"{OWNED_PREFIX}-expiry.service"], timeout=10)
    rows = [row for row in container_rows() if not row.startswith("podman error:")]
    for row in rows:
        name = row.split()[0]
        if args.dry_run:
            actions.append(f"would stop/rm container {name}")
        else:
            podman("rm", "-f", name, timeout=30)
            actions.append(f"stopped/removed container {name}")
    if args.dry_run:
        actions.append("would disable GNOME VNC and restore lock/VNC settings")
    else:
        disable_vnc()
        set_vnc_encryption((prior_state or {}).get("previous_vnc_encryption", "['tls-anon']"))
        restore_idle_lock((prior_state or {}).get("previous_lock_settings"))
        actions.append("disabled GNOME VNC, cleared credentials, and restored lock/VNC settings")
    if STATE_FILE.exists():
        if args.dry_run:
            actions.append(f"would remove {STATE_FILE}")
        else:
            STATE_FILE.unlink()
            actions.append(f"removed {STATE_FILE}")
    report = {"ok": True, "dry_run": args.dry_run, "actions": actions, "remaining_listeners": listeners(), "remaining_owned_containers": container_rows()}
    write_json(report)
    log("close", dry_run=args.dry_run, actions=actions)
    return 0


def uninstall(args: argparse.Namespace) -> int:
    if not args.purge and not args.dry_run:
        write_json({"ok": True, "message": "Runtime uninstall without --purge has no destructive action. Remove skill folder separately if desired.", "state_dir": str(STATE_DIR)})
        return 0
    if args.dry_run:
        write_json({"dry_run": True, "would_run_close": True, "would_remove_state_dir_if_purge": args.purge, "would_remove_network": NETWORK, "state_dir": str(STATE_DIR)})
        return 0
    close(argparse.Namespace(dry_run=False))
    podman("network", "rm", NETWORK, timeout=20)
    log("uninstall", purge=args.purge)
    if args.purge and STATE_DIR.exists():
        shutil.rmtree(STATE_DIR)
    write_json({"ok": True, "purged": args.purge, "state_dir_exists": STATE_DIR.exists()})
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Remote desktop support lifecycle helper")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("preflight").set_defaults(func=preflight)
    sub.add_parser("status").set_defaults(func=status)

    sp = sub.add_parser("install")
    sp.add_argument("--dry-run", action="store_true")
    sp.set_defaults(func=install)

    sp = sub.add_parser("open")
    sp.add_argument("--ttl", default="10m")
    sp.add_argument("--mode", choices=["view-only", "control"], default="view-only")
    sp.add_argument("--dry-run", action="store_true")
    sp.add_argument("--force", action="store_true")
    sp.add_argument("--unlock-current-session", action="store_true", help="explicitly unlock the live GNOME session if it is locked")
    sp.add_argument("--one-click-only", action="store_true", help="print only the one-click URL and non-secret metadata")
    sp.set_defaults(func=open_session)

    sub.add_parser("link").set_defaults(func=link_session)

    sp = sub.add_parser("close")
    sp.add_argument("--dry-run", action="store_true")
    sp.set_defaults(func=close)

    sp = sub.add_parser("uninstall")
    sp.add_argument("--dry-run", action="store_true")
    sp.add_argument("--purge", action="store_true")
    sp.set_defaults(func=uninstall)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
