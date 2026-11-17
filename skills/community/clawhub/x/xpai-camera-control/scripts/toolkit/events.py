import json
import re
import socket
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from . import camera_proto
except ImportError:
    import camera_proto

try:
    from ._argnorm import coerce_str
except ImportError:
    from _argnorm import coerce_str

_SKILL_ROOT = Path(__file__).resolve().parents[2]
EVENTS_DIR = _SKILL_ROOT / "events"
EVENT_STORE_PATH = EVENTS_DIR / "camera_events.txt"
EVENT_CURSOR_PATH = EVENTS_DIR / "events_cursor.json"
MONITOR_STATE_PATH = EVENTS_DIR / "monitor_state.json"

EVENT_SCHEMA_VERSION = "1.0"

DEFAULT_DEBOUNCE_SECONDS = 5.0
_SNAPSHOT_MIN_INTERVAL = 30.0
WAIT_TIMEOUT_CAP = 60.0
_STORE_MAX_READ = 10000
_RESUME_RETRY_SECONDS = 60.0

EVENT_SEVERITY_MAP = {
    "motion": "warning",
    "human": "warning",
    "vehicle": "warning",
    "tamper": "critical",
    "region_intrusion": "critical",
    "line_crossing": "critical",
    "high_temp": "critical",
    "low_temp": "critical",
}

_EVENT_TEXT_MAP = {
    "motion": ("Motion detected", "detected movement in the frame"),
    "human": ("Person detected", "detected a person in the frame"),
    "vehicle": ("Vehicle detected", "detected a vehicle in the frame"),
    "tamper": ("Lens blocked", "detected lens obstruction"),
    "region_intrusion": ("Region intrusion alarm", "detected a target entering the guard region"),
    "line_crossing": ("Line crossing alarm", "detected a target crossing the guard line"),
    "high_temp": ("High temperature alarm", "detected abnormally high temperature"),
    "low_temp": ("Low temperature alarm", "detected abnormally low temperature"),
}

_SUBTYPE_LABEL_MAP = {
    "person": "person",
    "human": "person",
    "salooncar": "car",
    "car": "car",
    "truck": "truck",
    "bus": "bus",
    "motorcycle": "motorcycle",
    "bicycle": "bicycle",
}

class EventAction(Enum):
    START = "start"
    STOP = "stop"
    POLL = "poll"
    WAIT = "wait"

@dataclass
class CameraEvent:
    schema_version: str = EVENT_SCHEMA_VERSION
    event_id: str = ""
    event_type: str = ""
    camera_id: str = ""
    camera_name: str = ""
    timestamp: str = ""
    severity: str = ""
    title: str = ""
    message: str = ""
    label: Optional[str] = None
    confidence: Optional[float] = None
    snapshot_path: str = ""
    tags: List[str] = field(default_factory=lambda: ["guardian"])

@dataclass
class EventMonitorResult:
    success: bool
    camera_name: str = ""
    running: bool = False
    active_channels: List[str] = field(default_factory=list)
    error_message: str = ""

@dataclass
class PendingEventsResult:
    success: bool
    events: List[CameraEvent] = field(default_factory=list)
    remaining: int = 0
    monitors: Dict[str, Any] = field(default_factory=dict)
    error_message: str = ""

_store_lock = threading.Lock()
_event_arrived = threading.Condition(_store_lock)

def _ensure_events_dir() -> None:
    EVENTS_DIR.mkdir(parents=True, exist_ok=True)

def _append_event_to_store(event: Dict[str, Any]) -> None:
    with _event_arrived:
        _ensure_events_dir()
        with open(EVENT_STORE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        _event_arrived.notify_all()

def _read_store_lines() -> List[Dict[str, Any]]:
    if not EVENT_STORE_PATH.exists():
        return []
    events = []
    try:
        with open(EVENT_STORE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
                if len(events) >= _STORE_MAX_READ:
                    break
    except OSError:
        return []
    return events

def _load_cursor() -> Dict[str, int]:
    if not EVENT_CURSOR_PATH.exists():
        return {}
    try:
        with open(EVENT_CURSOR_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {str(k): int(v) for k, v in data.items()} if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}

def _save_cursor(cursor: Dict[str, int]) -> None:
    _ensure_events_dir()
    with open(EVENT_CURSOR_PATH, "w", encoding="utf-8") as f:
        json.dump(cursor, f, ensure_ascii=False, indent=2)

def _collect_pending(
    camera_name: Optional[str],
    limit: int,
    advance: bool,
) -> Tuple[List[Dict[str, Any]], int]:
    with _store_lock:
        lines = _read_store_lines()
        cursor = _load_cursor()
        new_cursor = dict(cursor)
        pending: List[Dict[str, Any]] = []

        for idx, evt in enumerate(lines):
            cam = str(evt.get("camera_id", ""))
            if camera_name and cam != camera_name:
                continue
            if idx < cursor.get(cam, 0):
                continue
            if len(pending) >= limit:
                break
            pending.append(evt)
            new_cursor[cam] = idx + 1

        remaining = 0
        for idx, evt in enumerate(lines):
            cam = str(evt.get("camera_id", ""))
            if camera_name and cam != camera_name:
                continue
            if idx >= new_cursor.get(cam, 0):
                remaining += 1

        if advance and pending:
            _save_cursor(new_cursor)

    return pending, remaining

def _dict_to_camera_event(d: Dict[str, Any]) -> CameraEvent:
    return CameraEvent(
        schema_version=str(d.get("schema_version", EVENT_SCHEMA_VERSION)),
        event_id=str(d.get("event_id", "")),
        event_type=str(d.get("event_type", "")),
        camera_id=str(d.get("camera_id", "")),
        camera_name=str(d.get("camera_name", "")),
        timestamp=str(d.get("timestamp", "")),
        severity=str(d.get("severity", "")),
        title=str(d.get("title", "")),
        message=str(d.get("message", "")),
        label=d.get("label"),
        confidence=d.get("confidence"),
        snapshot_path=str(d.get("snapshot_path", "")),
        tags=d.get("tags", []) if isinstance(d.get("tags"), list) else [],
    )

def _parse_private_data_field(data: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for part in (data or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            result[k.strip().upper()] = v.strip()
    return result

def _extract_label_confidence(
    event_type: str,
    source: str,
    detail: Dict[str, Any],
) -> Tuple[Optional[str], Optional[float]]:
    label: Optional[str] = None
    confidence: Optional[float] = None

    if source == "private":
        kv = _parse_private_data_field(str(detail.get("data", "")))
        subtype = kv.get("SUBTYPE", "")
        if subtype:
            label = _SUBTYPE_LABEL_MAP.get(subtype.lower(), subtype.lower())
        for key in ("CONFIDENCE", "CONF", "PROB"):
            if key in kv:
                try:
                    val = float(kv[key])
                    confidence = round(val / 100.0 if val > 1.0 else val, 4)
                except ValueError:
                    pass
                break

    if label is None and event_type == "human":
        label = "person"
    elif label is None and event_type == "vehicle":
        label = "vehicle"
    return label, confidence

def _process_event_message(
    camera_id: str,
    event_type: str,
    source: str,
    detail: Optional[Dict[str, Any]],
    snapshot_path: str,
    display_name: str = "",
) -> Dict[str, Any]:
    dt = datetime.now().astimezone()
    name = display_name or camera_id
    title_phrase, message_phrase = _EVENT_TEXT_MAP.get(
        event_type, (f"{event_type} alarm", f"reported a {event_type} event")
    )
    label, confidence = _extract_label_confidence(event_type, source, detail or {})
    suffix = ", snapshot taken." if snapshot_path else "."

    return {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event_id": f"{dt.strftime('%Y%m%d_%H%M%S')}_{camera_id}_{event_type}",
        "event_type": event_type,
        "camera_id": camera_id,
        "camera_name": name,
        "timestamp": dt.isoformat(timespec="seconds"),
        "severity": EVENT_SEVERITY_MAP.get(event_type, "info"),
        "title": f"{name} {title_phrase}",
        "message": f"{name} camera at {dt.strftime('%H:%M:%S')} {message_phrase}{suffix}",
        "label": label,
        "confidence": confidence,
        "snapshot_path": snapshot_path,
        "tags": ["guardian"],
    }

class _CameraEventMonitor:

    def __init__(
        self,
        camera_name: str,
        ip: str,
        rtsp_port: int,
        rtsp_path: str,
        username: str,
        password: str,
        debounce_seconds: float = DEFAULT_DEBOUNCE_SECONDS,
    ):
        self.camera_name = camera_name
        self.ip = ip
        self.rtsp_port = rtsp_port
        self.rtsp_path = rtsp_path or "/md0_0"
        self.username = username
        self.password = password
        self.debounce = max(0.5, float(debounce_seconds))

        self._stop_event = threading.Event()
        self._threads: List[threading.Thread] = []
        self._channels: Dict[str, bool] = {}
        self._rtsp_session_id: str = ""
        self._rtsp_cseq: int = 0
        self._rtsp_auth_ctx: Tuple[str, str, bool] = ("", "", False)
        self._last_error: str = ""
        self._last_emit: Dict[Tuple[str, str], float] = {}
        self._last_snapshot: float = 0.0
        self._suppressed_count = 0
        self._emitted_count = 0
        self._lock = threading.Lock()

    @property
    def running(self) -> bool:
        return any(t.is_alive() for t in self._threads)

    def status(self) -> Dict[str, Any]:
        return {
            "running": self.running,
            "channels": dict(self._channels),
            "rtsp_session": bool(self._rtsp_session_id),
            "last_error": self._last_error,
            "emitted": self._emitted_count,
            "suppressed": self._suppressed_count,
            "debounce_seconds": self.debounce,
        }

    def start(self) -> List[str]:
        active: List[str] = []
        if self._probe_tcp(self.ip, self.rtsp_port):
            t = threading.Thread(
                target=self._private_rtsp_alarm_loop,
                name=f"EventMonitor-private-{self.camera_name}",
                daemon=True,
            )
            t.start()
            self._threads.append(t)
            active.append("private")
        else:
            self._channels["private"] = False
            self._last_error = f"RTSP port {self.rtsp_port} unreachable over TCP"
        return active

    def stop(self) -> None:
        self._stop_event.set()
        for t in self._threads:
            t.join(timeout=3)
        self._threads = []
        self._channels = {k: False for k in self._channels}

    @staticmethod
    def _probe_tcp(ip: str, port: int, timeout: float = 3.0) -> bool:
        try:
            sock = socket.create_connection((ip, port), timeout=timeout)
            sock.close()
            return True
        except OSError:
            return False

    def _emit(
        self,
        topic: str,
        source: str,
        detail: Optional[Dict[str, Any]] = None,
    ) -> None:
        now = time.time()
        key = (self.camera_name, topic)

        with self._lock:

            if now - self._last_emit.get(key, 0.0) < self.debounce:
                self._suppressed_count += 1
                return
            self._last_emit[key] = now

            take_snapshot = (now - self._last_snapshot) >= _SNAPSHOT_MIN_INTERVAL
            if take_snapshot:
                self._last_snapshot = now

        snapshot_path = ""
        if take_snapshot:
            snapshot_path = self._schedule_snapshot()

        event = _process_event_message(
            camera_id=self.camera_name,
            event_type=topic,
            source=source,
            detail=detail,
            snapshot_path=snapshot_path,
        )
        _append_event_to_store(event)
        with self._lock:
            self._emitted_count += 1

    def _schedule_snapshot(self) -> str:
        import os
        snapshot_dir = os.path.join(os.path.dirname(__file__), "..", "..", "snapshots")
        ts = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(snapshot_dir, f"{self.camera_name}_{ts}.jpg")

        def _worker() -> None:
            try:
                from .stream import capture_video_screenshot
                capture_video_screenshot(self.camera_name, save_path=file_path)
            except Exception:
                pass

        t = threading.Thread(
            target=_worker, name=f"EventSnapshot-{self.camera_name}", daemon=True
        )
        t.start()
        return file_path

    def _private_rtsp_alarm_loop(self) -> None:
        backoff = 2.0
        while not self._stop_event.is_set():
            sock = None
            session_start = 0.0
            try:
                sock = self._open_rtsp_alarm_session()
                self._channels["private"] = True
                self._last_error = ""
                session_start = time.time()
                self._read_alarm_stream(sock)
            except Exception as e:
                self._last_error = f"{type(e).__name__}: {e}"
            finally:
                if sock is not None:
                    self._send_rtsp_teardown(sock)
                self._rtsp_session_id = ""
                self._rtsp_auth_ctx = ("", "", False)
                if sock is not None:
                    try:
                        sock.close()
                    except OSError:
                        pass

            if self._stop_event.is_set():
                return
            self._channels["private"] = False

            if session_start and time.time() - session_start > 30.0:
                backoff = 2.0
            if self._stop_event.wait(backoff):
                return
            backoff = min(backoff * 2, 30.0)

    def _send_rtsp_teardown(self, sock: socket.socket) -> None:

        try:
            session_id = self._rtsp_session_id
            if not session_id:
                return
            import base64
            import hashlib

            base_url = f"rtsp://{self.ip}:{self.rtsp_port}{self.rtsp_path}"
            realm, nonce, use_basic = self._rtsp_auth_ctx
            auth = ""
            if self.username:
                if nonce:
                    ha1 = hashlib.md5(
                        f"{self.username}:{realm}:{self.password}".encode()
                    ).hexdigest()
                    ha2 = hashlib.md5(f"TEARDOWN:{base_url}".encode()).hexdigest()
                    resp = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()
                    auth = (
                        f'Authorization: Digest username="{self.username}", '
                        f'realm="{realm}", nonce="{nonce}", '
                        f'uri="{base_url}", response="{resp}"\r\n'
                    )
                elif use_basic:
                    token = base64.b64encode(
                        f"{self.username}:{self.password}".encode()
                    ).decode()
                    auth = f"Authorization: Basic {token}\r\n"
            req = (
                f"TEARDOWN {base_url} RTSP/1.0\r\n"
                f"CSeq: {self._rtsp_cseq + 1}\r\n"
                f"User-Agent: {camera_proto.rtsp_ua()}\r\n"
                f"Session: {session_id}\r\n"
                f"{auth}\r\n"
            )
            sock.settimeout(1.0)
            sock.sendall(req.encode("utf-8"))
        except Exception:
            pass

    def _open_rtsp_alarm_session(self) -> socket.socket:
        import base64
        import hashlib

        sock = socket.create_connection((self.ip, self.rtsp_port), timeout=5.0)
        sock.settimeout(1.0)

        base_url = f"rtsp://{self.ip}:{self.rtsp_port}{self.rtsp_path}"

        digest_realm = ""
        digest_nonce = ""
        use_basic = False

        def build_auth(method: str, url: str) -> str:
            if not self.username:
                return ""
            if digest_nonce:
                ha1 = hashlib.md5(
                    f"{self.username}:{digest_realm}:{self.password}".encode()
                ).hexdigest()
                ha2 = hashlib.md5(f"{method}:{url}".encode()).hexdigest()
                resp = hashlib.md5(f"{ha1}:{digest_nonce}:{ha2}".encode()).hexdigest()
                return (
                    f'Authorization: Digest username="{self.username}", '
                    f'realm="{digest_realm}", nonce="{digest_nonce}", '
                    f'uri="{url}", response="{resp}"\r\n'
                )
            if use_basic:
                token = base64.b64encode(
                    f"{self.username}:{self.password}".encode()
                ).decode()
                return f"Authorization: Basic {token}\r\n"
            return ""

        cseq_counter = [0]

        def send_req(method: str, url: str, extra: str = "") -> str:
            cseq_counter[0] += 1
            req = (
                f"{method} {url} RTSP/1.0\r\n"
                f"CSeq: {cseq_counter[0]}\r\n"
                f"User-Agent: {camera_proto.rtsp_ua()}\r\n"
                f"{build_auth(method, url)}{extra}\r\n"
            )
            sock.sendall(req.encode("utf-8"))
            resp = b""
            deadline = time.time() + 5.0
            while time.time() < deadline:
                try:
                    chunk = sock.recv(4096)
                except socket.timeout:
                    continue
                if not chunk:
                    break
                resp += chunk
                if b"\r\n\r\n" in resp:
                    break
            return resp.decode("utf-8", errors="ignore")

        describe = send_req("DESCRIBE", base_url, "Accept: application/sdp\r\n")
        retried = False
        if describe and "401" in describe.splitlines()[0] and self.username:
            rm = re.search(r'realm="([^"]+)"', describe)
            nm = re.search(r'nonce="([^"]+)"', describe)
            if "Digest" in describe and rm and nm:
                digest_realm, digest_nonce = rm.group(1), nm.group(1)
            else:
                use_basic = True
            retried = True
            describe = send_req("DESCRIBE", base_url, "Accept: application/sdp\r\n")
        describe_ok = bool(describe) and "200" in describe.splitlines()[0]
        if not describe_ok:
            status_line = describe.splitlines()[0] if describe else "no response"
            raise RuntimeError(f"DESCRIBE {base_url} failed: {status_line}")

        track_urls: List[str] = []
        sdp_base_url = base_url
        current_control = ""
        for line in describe.split("\r\n"):
            if line.startswith("a=control:"):
                ctrl = line.split(":", 1)[1].strip()
                if ctrl and ctrl != "*":
                    current_control = ctrl
            if line.startswith("m=") and current_control:
                if current_control.lower().startswith("rtsp://"):
                    track_urls.append(current_control)
                else:
                    track_urls.append(
                        f"{sdp_base_url.rstrip('/')}/{current_control}"
                    )
                current_control = ""
        if not track_urls:

            controls = [c.strip() for c in re.findall(r"a=control:(\S+)", describe)]
            control = next((c for c in controls if c != "*"), "")
            if control:
                if control.lower().startswith("rtsp://"):
                    track_urls.append(control)
                else:
                    track_urls.append(base_url.rstrip("/") + "/" + control.lstrip("/"))
            else:
                track_urls.append(base_url)

        session_id = ""
        interleaved_base = 0
        for track_url in track_urls:
            transport = (
                f"Transport: RTP/AVP/TCP;interleaved={interleaved_base}"
                f"-{interleaved_base + 1}\r\n"
            )
            setup = send_req("SETUP", track_url, transport)
            setup_status = setup.splitlines()[0] if setup else ""

            if "401" in setup_status:
                rm = re.search(r'realm="([^"]+)"', setup)
                nm = re.search(r'nonce="([^"]+)"', setup)
                if "Digest" in setup and rm and nm:
                    digest_realm, digest_nonce = rm.group(1), nm.group(1)
                else:
                    use_basic = True
                setup = send_req("SETUP", track_url, transport)
                setup_status = setup.splitlines()[0] if setup else ""

            sm = re.search(r"Session:\s*([^;\r\n]+)", setup)
            if sm and "200" in setup_status:
                sid = sm.group(1).strip()
                if not session_id:
                    session_id = sid
                interleaved_base += 2

        if not session_id:
            raise RuntimeError("SETUP established no session (missing Session header or non-200 status)")

        play_target = track_urls[0] if track_urls else base_url
        play = send_req(
            "PLAY", play_target,
            f"Session: {session_id}\r\nRange: npt=0.000-\r\n",
        )
        play_status = play.splitlines()[0] if play else "no response"
        if "200" not in play_status:
            raise RuntimeError(f"PLAY {play_target} failed: {play_status}")
        self._rtsp_session_id = session_id
        self._rtsp_cseq = cseq_counter[0]
        self._rtsp_auth_ctx = (digest_realm, digest_nonce, use_basic)

        return sock

    def _read_alarm_stream(self, sock: socket.socket) -> None:
        parser = camera_proto.AlarmParser()
        last_keepalive = time.time()
        cseq = 10
        base_url = f"rtsp://{self.ip}:{self.rtsp_port}{self.rtsp_path}"

        try:
            while not self._stop_event.is_set():

                if time.time() - last_keepalive > 25.0:
                    last_keepalive = time.time()
                    cseq += 1
                    session_hdr = ""
                    if getattr(self, "_rtsp_session_id", ""):
                        session_hdr = f"Session: {self._rtsp_session_id}\r\n"
                    try:
                        sock.sendall(
                            f"OPTIONS {base_url} RTSP/1.0\r\nCSeq: {cseq}\r\n"
                            f"User-Agent: {camera_proto.rtsp_ua()}\r\n{session_hdr}\r\n".encode()
                        )
                    except OSError:
                        return

                try:
                    chunk = sock.recv(8192)
                except socket.timeout:
                    continue
                except OSError:
                    return
                if not chunk:
                    return

                try:
                    events = parser.feed(chunk)
                except Exception:
                    events = []
                for ev in events:
                    self._handle_alarm_event(ev)
        finally:

            parser.close()

    def _handle_alarm_event(self, ev: Dict[str, Any]) -> None:
        self._emit(
            topic=ev.get("topic", ""),
            source="private",
            detail=ev.get("detail") or {},
        )

_monitors: Dict[str, _CameraEventMonitor] = {}
_monitors_lock = threading.Lock()

_resume_last_attempt: Dict[str, float] = {}
_resume_lock = threading.Lock()

def _monitor_status_summary() -> Dict[str, Any]:
    with _monitors_lock:
        return {name: m.status() for name, m in _monitors.items()}

def _load_monitor_state() -> Dict[str, Dict[str, Any]]:
    if not MONITOR_STATE_PATH.exists():
        return {}
    try:
        with open(MONITOR_STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {str(k): v for k, v in data.items() if isinstance(v, dict)} \
            if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}

def _save_monitor_state(state: Dict[str, Dict[str, Any]]) -> None:
    _ensure_events_dir()
    with open(MONITOR_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def _record_monitor_intent(camera_name: str, debounce_seconds: float) -> None:
    state = _load_monitor_state()
    state[camera_name] = {
        "debounce_seconds": debounce_seconds,
        "enabled_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    _save_monitor_state(state)

def _clear_monitor_intent(camera_name: str) -> None:
    state = _load_monitor_state()
    if camera_name in state:
        state.pop(camera_name)
        _save_monitor_state(state)
    _resume_last_attempt.pop(camera_name, None)

def resume_persisted_monitors() -> Dict[str, str]:

    if not _resume_lock.acquire(blocking=False):
        return {}
    try:
        outcome: Dict[str, str] = {}
        for camera_name, spec in _load_monitor_state().items():
            with _monitors_lock:
                existing = _monitors.get(camera_name)
                if existing and existing.running:
                    outcome[camera_name] = "already_running"
                    continue

            now = time.time()
            if now - _resume_last_attempt.get(camera_name, 0.0) < _RESUME_RETRY_SECONDS:
                outcome[camera_name] = "cooldown"
                continue

            if camera_name not in _load_monitor_state():
                outcome[camera_name] = "cancelled"
                continue

            result = start_event_monitor(
                camera_name,
                debounce_seconds=float(spec.get("debounce_seconds", DEFAULT_DEBOUNCE_SECONDS)),
                _resuming=True,
            )
            if result.success:
                _resume_last_attempt.pop(camera_name, None)
                outcome[camera_name] = "resumed"
            else:
                _resume_last_attempt[camera_name] = now
                outcome[camera_name] = f"failed: {result.error_message}"
        return outcome
    finally:
        _resume_lock.release()

def start_event_monitor(
    camera_name: str,
    debounce_seconds: float = DEFAULT_DEBOUNCE_SECONDS,
    _resuming: bool = False,
) -> EventMonitorResult:
    camera_name = coerce_str(camera_name)

    with _monitors_lock:
        existing = _monitors.get(camera_name)
        if existing and existing.running:
            return EventMonitorResult(
                success=True, camera_name=camera_name, running=True,
                active_channels=[k for k, v in existing._channels.items() if v],
                error_message="Monitor already running; no need to start it again",
            )

    from .device_mgmt import _connected_devices, _find_cached_camera
    conn = _connected_devices.get(camera_name)
    cached = _find_cached_camera(camera_name)
    if conn:
        ip = conn.get("ip", "")
        rtsp_port = int(conn.get("rtsp_port", 554) or 554)
        username = conn.get("username", "admin")
        password = conn.get("password", "")
    elif cached and cached.ip:
        ip = cached.ip
        rtsp_port = cached.rtsp_port
        username = cached.username
        password = cached.password
    else:
        return EventMonitorResult(
            success=False, camera_name=camera_name,
            error_message=f"Device {camera_name} is not connected and has no config.yaml record; "
                          f"call connect_device() first",
        )

    if cached and cached.rtsp_path:
        rtsp_path = cached.rtsp_path
    elif conn:
        rtsp_path = conn.get("rtsp_path", "") or "/md0_0"
    else:
        rtsp_path = "/md0_0"

    monitor = _CameraEventMonitor(
        camera_name=camera_name,
        ip=ip,
        rtsp_port=rtsp_port,
        rtsp_path=rtsp_path,
        username=username,
        password=password,
        debounce_seconds=debounce_seconds,
    )
    active = monitor.start()

    if not active:
        return EventMonitorResult(
            success=False, camera_name=camera_name,
            error_message=f"Private-protocol monitor failed to start (RTSP {ip}:{rtsp_port} TCP unreachable)",
        )

    with _monitors_lock:
        _monitors[camera_name] = monitor

    if not _resuming:
        _record_monitor_intent(camera_name, debounce_seconds)

    return EventMonitorResult(
        success=True, camera_name=camera_name,
        running=True, active_channels=active,
    )

def stop_event_monitor(
    camera_name: str,
) -> EventMonitorResult:
    camera_name = coerce_str(camera_name)

    _clear_monitor_intent(camera_name)

    with _monitors_lock:
        monitor = _monitors.pop(camera_name, None)

    if monitor is None:
        return EventMonitorResult(
            success=True, camera_name=camera_name, running=False,
            error_message="No running event monitor for this camera",
        )

    monitor.stop()
    return EventMonitorResult(success=True, camera_name=camera_name, running=False)

def get_pending_events(
    camera_name: Optional[str] = None,
    limit: int = 100,
) -> PendingEventsResult:
    camera_name = coerce_str(camera_name)

    try:
        resume_persisted_monitors()
    except Exception:
        pass

    try:
        pending, remaining = _collect_pending(camera_name, max(1, int(limit)), advance=True)
    except Exception as e:
        return PendingEventsResult(success=False, error_message=f"Failed to read event store: {e}")

    return PendingEventsResult(
        success=True,
        events=[_dict_to_camera_event(d) for d in pending],
        remaining=remaining,
        monitors=_monitor_status_summary(),
    )

def wait_for_events(
    camera_name: Optional[str] = None,
    timeout_seconds: float = 60.0,
) -> PendingEventsResult:
    camera_name = coerce_str(camera_name)

    try:
        resume_persisted_monitors()
    except Exception:
        pass

    timeout = min(max(1.0, float(timeout_seconds)), WAIT_TIMEOUT_CAP)
    deadline = time.time() + timeout

    while True:
        try:
            pending, remaining = _collect_pending(camera_name, limit=100, advance=True)
        except Exception as e:
            return PendingEventsResult(success=False, error_message=f"Failed to read event store: {e}")

        if pending:
            return PendingEventsResult(
                success=True,
                events=[_dict_to_camera_event(d) for d in pending],
                remaining=remaining,
                monitors=_monitor_status_summary(),
            )

        wait_left = deadline - time.time()
        if wait_left <= 0:
            return PendingEventsResult(
                success=True, events=[], remaining=0,
                monitors=_monitor_status_summary(),
            )

        with _event_arrived:
            _event_arrived.wait(timeout=min(2.0, wait_left))

def manage_camera_events(
    action: "EventAction",
    camera_name: Optional[str] = None,
    debounce_seconds: float = DEFAULT_DEBOUNCE_SECONDS,
    limit: int = 100,
    timeout_seconds: float = 60.0,
):
    camera_name = coerce_str(camera_name)

    if camera_name:
        try:
            from .device_mgmt import _is_non_sk_camera, _unsupported_protocol_message
        except ImportError:
            from device_mgmt import _is_non_sk_camera, _unsupported_protocol_message
        if _is_non_sk_camera(camera_name):
            msg = _unsupported_protocol_message(camera_name, "alarm event monitoring")
            if action in (EventAction.START, EventAction.STOP):
                return EventMonitorResult(success=False, error_message=msg)
            return PendingEventsResult(success=False, error_message=msg)

    if action in (EventAction.START, EventAction.STOP):
        if not camera_name:
            return EventMonitorResult(
                success=False,
                error_message=f"action={action.value} requires the camera_name parameter",
            )
        if action == EventAction.START:
            return start_event_monitor(camera_name, debounce_seconds)
        return stop_event_monitor(camera_name)

    if action == EventAction.POLL:
        return get_pending_events(camera_name, limit)

    if action == EventAction.WAIT:
        return wait_for_events(camera_name, timeout_seconds)

    return PendingEventsResult(
        success=False,
        error_message=f"Unknown action: {action} (options: start/stop/poll/wait)",
    )
