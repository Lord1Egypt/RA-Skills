import os
import signal
import threading
import time
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
import json
import shutil
import subprocess

try:
    from ._argnorm import coerce_str
except ImportError:
    from _argnorm import coerce_str

class RecordingAction(str, Enum):
    START = "start"
    STOP = "stop"
    STATUS = "status"

@dataclass
class StreamResult:
    success: bool
    stream_url: str = ""
    codec: str = ""
    resolution: str = ""
    fps: float = 0.0
    bitrate: int = 0
    error_message: str = ""

@dataclass
class ScreenshotResult:
    success: bool
    file_path: str = ""
    width: int = 0
    height: int = 0
    error_message: str = ""

@dataclass
class RecordingResult:
    success: bool
    is_recording: bool = False
    file_path: str = ""
    duration_seconds: float = 0.0
    auto_stop: bool = False
    error_message: str = ""

def _rtsp_transport_selectable() -> bool:

    import cv2
    return getattr(cv2, "CAP_PROP_OPENCV_FFMPEG_CAPTURE_OPTIONS", None) is not None

def _rtsp_transport_plan() -> Tuple[str, ...]:

    return ("tcp", "udp") if _rtsp_transport_selectable() else ("tcp",)

def _open_rtsp_capture(rtsp_url: str, transport: str = "tcp"):
    import cv2
    prop = getattr(cv2, "CAP_PROP_OPENCV_FFMPEG_CAPTURE_OPTIONS", None)
    if prop is not None:
        try:
            return cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG, [
                cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 8000,
                cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000,
                prop, f"rtsp_transport;{transport}",
            ])
        except (TypeError, AttributeError, cv2.error):
            pass

    try:
        return cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG, [
            cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 8000,
            cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000,
        ])
    except (TypeError, AttributeError):
        return cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

def _open_rtsp_capture_with_fallback(rtsp_url: str):

    cap = _open_rtsp_capture(rtsp_url, "tcp")
    if cap.isOpened():
        return cap
    cap.release()
    if not _rtsp_transport_selectable():
        return cap
    return _open_rtsp_capture(rtsp_url, "udp")

def _read_last_frame(cap, attempts: int = 6):

    frame = None
    for _ in range(attempts):
        ret, f = cap.read()
        if ret and f is not None:
            frame = f
    return frame

def get_audio_video_stream(
    camera_name: str,
    sub_stream: bool = False,
) -> StreamResult:
    camera_name = coerce_str(camera_name)

    from .device_mgmt import _connected_devices, _find_cached_camera
    conn_info = _connected_devices.get(camera_name)
    if not conn_info:

        cached = _find_cached_camera(camera_name)
        if cached and cached.ip:
            conn_info = {
                "ip": cached.ip,
                "rtsp_port": cached.rtsp_port,
                "rtsp_path": cached.rtsp_path if not sub_stream else cached.rtsp_sub_path,
                "rtsp_sub_path": cached.rtsp_sub_path,
                "username": cached.username,
                "password": cached.password,
                "connection_type": cached.connection_type,
            }
        else:
            return StreamResult(
                success=False,
                error_message=f"Device {camera_name} is not connected; call connect_device() first",
            )

    ip = conn_info.get("ip", "")
    rtsp_port = conn_info.get("rtsp_port", 554)
    username = conn_info.get("username", "")
    password = conn_info.get("password", "")

    if sub_stream:
        rtsp_path = conn_info.get("rtsp_sub_path") or "/md0_1"
    else:
        rtsp_path = conn_info.get("rtsp_path") or "/md0_0"

    from .device_mgmt import _build_rtsp_url
    rtsp_url = _build_rtsp_url(ip, rtsp_port, rtsp_path, username, password)

    try:
        import cv2
    except ImportError:

        from .device_mgmt import _probe_stream_access
        access = _probe_stream_access(ip, rtsp_port, rtsp_path, username, password)
        if access == "open":
            return StreamResult(
                success=True,
                stream_url=rtsp_url,
                codec="H.264",
                resolution="",
                fps=0.0,
                bitrate=0,
            )
        elif access == "auth_required":
            return StreamResult(
                success=False,
                error_message=f"Device {camera_name} requires password authentication; provide the correct password",
            )
        else:
            return StreamResult(
                success=False,
                error_message=f"Device {camera_name}({ip}) stream unavailable (RTSP unreachable)",
            )

    cap = _open_rtsp_capture_with_fallback(rtsp_url)
    if not cap.isOpened():

        cap.release()
        alt_path = (conn_info.get("rtsp_path") or "/md0_0") if sub_stream \
            else (conn_info.get("rtsp_sub_path") or "/md0_1")
        if alt_path != rtsp_path:
            rtsp_url = _build_rtsp_url(ip, rtsp_port, alt_path, username, password)
            cap = _open_rtsp_capture_with_fallback(rtsp_url)
        if not cap.isOpened():
            cap.release()
            return StreamResult(
                success=False,
                error_message=f"Cannot get video stream from {ip}:{rtsp_port}; check the RTSP path and credentials",
            )

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
    codec_map = {
        0x31637661: "H.264",
        0x31637668: "H.265",
        1196444237: "MJPEG",
    }
    codec = codec_map.get(fourcc_int, f"0x{fourcc_int:08x}")

    cap.release()

    return StreamResult(
        success=True,
        stream_url=rtsp_url,
        codec=codec,
        resolution=f"{width}x{height}" if width and height else "",
        fps=round(fps, 1) if fps > 0 else 0.0,
        bitrate=0,
    )

def capture_video_screenshot(
    camera_name: str,
    save_path: Optional[str] = None,
) -> ScreenshotResult:
    camera_name = coerce_str(camera_name)

    import os
    import time

    if save_path is None:
        snapshot_dir = os.path.join(os.path.dirname(__file__), "..", "..", "snapshots")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(snapshot_dir, f"{camera_name}_{timestamp}.jpg")
    elif save_path.lower().endswith((".jpg", ".jpeg")):
        file_path = save_path
        snapshot_dir = os.path.dirname(os.path.abspath(save_path))
    else:
        snapshot_dir = save_path
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(snapshot_dir, f"{camera_name}_{timestamp}.jpg")

    os.makedirs(snapshot_dir, exist_ok=True)

    from .device_mgmt import _connected_devices, _find_cached_camera
    conn_info = _connected_devices.get(camera_name)
    if not conn_info:
        cached = _find_cached_camera(camera_name)
        if cached and cached.ip:
            conn_info = {
                "ip": cached.ip,
                "rtsp_port": cached.rtsp_port,
                "rtsp_path": cached.rtsp_path,
                "rtsp_sub_path": cached.rtsp_sub_path,
                "username": cached.username,
                "password": cached.password,
                "connection_type": cached.connection_type,
            }
        else:
            return ScreenshotResult(
                success=False,
                file_path=file_path,
                error_message=f"Device {camera_name} is not connected; call connect_device() first",
            )

    try:
        import cv2
    except ImportError:
        return ScreenshotResult(
            success=False,
            file_path=file_path,
            error_message="opencv-python is missing; install it with: pip install opencv-python",
        )

    def _attempt_capture():
        frame = None
        ip = conn_info.get("ip", "")
        rtsp_port = conn_info.get("rtsp_port", 554)
        username = conn_info.get("username", "")
        password = conn_info.get("password", "")

        from .device_mgmt import _build_rtsp_url

        paths = []
        for p in (conn_info.get("rtsp_path") or "/md0_0",
                  conn_info.get("rtsp_sub_path") or "/md0_1"):
            if p and p not in paths:
                paths.append(p)

        opened_any = False
        transport_plan = _rtsp_transport_plan()
        for transport in transport_plan:
            for rtsp_path in paths:
                rtsp_url = _build_rtsp_url(ip, rtsp_port, rtsp_path, username, password)
                cap = _open_rtsp_capture(rtsp_url, transport)
                if not cap.isOpened():
                    cap.release()
                    continue
                opened_any = True
                frame = _read_last_frame(cap)
                cap.release()
                if frame is not None:
                    break
            if frame is not None:
                break

        if frame is None:
            if opened_any:
                return ScreenshotResult(
                    success=False,
                    file_path=file_path,
                    error_message="Cannot read frame data from the stream",
                )
            return ScreenshotResult(
                success=False,
                file_path=file_path,
                error_message=f"Cannot open video stream from {ip}:{rtsp_port}"
                              f" (tried {', '.join(paths)} × {'/'.join(transport_plan)}); "
                              f"check the RTSP path and credentials",
            )

        height, width = frame.shape[:2]
        try:
            import numpy as np
            success_enc, encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            if success_enc:
                encoded.tofile(file_path)
            else:
                raise RuntimeError("imencode failed")
        except Exception as e:
            return ScreenshotResult(
                success=False,
                file_path=file_path,
                error_message=f"Failed to save screenshot: {e}",
            )

        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return ScreenshotResult(
                success=False,
                file_path=file_path,
                error_message="Screenshot file write failed or is empty",
            )

        return ScreenshotResult(
            success=True,
            file_path=file_path,
            width=width,
            height=height,
        )

    result = _attempt_capture()
    if not result.success:
        time.sleep(1.0)
        result = _attempt_capture()
    return result

_RECORDING_STARTUP_COMPENSATION = 1.5

_VALID_RTSP_TRANSPORTS = frozenset({"tcp", "udp"})

def _resolve_binary(name: str) -> Optional[str]:
    path = shutil.which(name)
    if path:
        return path
    ffmpeg_dir = os.environ.get("FFMPEG_DIR", "")
    if ffmpeg_dir:
        candidate = os.path.join(ffmpeg_dir, name + (".exe" if os.name == "nt" else ""))
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None

def _resolve_transport_plan(rtsp_transport: Optional[Any]) -> List[str]:
    if rtsp_transport is None:
        return ["tcp", "udp"]
    if isinstance(rtsp_transport, str):
        plan = [rtsp_transport]
    else:
        plan = list(rtsp_transport)
    if not plan:
        raise ValueError("rtsp_transport must not be empty")
    bad = [t for t in plan if t not in _VALID_RTSP_TRANSPORTS]
    if bad:
        raise ValueError(f"Unsupported rtsp_transport: {bad}; valid: {sorted(_VALID_RTSP_TRANSPORTS)}")
    return plan

def _probe_dimensions(rtsp_url: str, transport_plan: List[str], timeout: int = 15) -> Tuple[int, int]:
    ffprobe_path = _resolve_binary("ffprobe")
    if not ffprobe_path:
        return 0, 0
    for transport in transport_plan:
        try:
            probe = subprocess.run(
                [
                    ffprobe_path,
                    "-rtsp_transport", transport,
                    "-timeout", "5000000",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_entries", "stream=width,height",
                    "-select_streams", "v:0",
                    rtsp_url,
                ],
                capture_output=True, text=True, timeout=timeout,
            )
            probe_data = json.loads(probe.stdout)
            streams = probe_data.get("streams", [])
            if streams:
                return int(streams[0].get("width", 0)), int(streams[0].get("height", 0))
        except Exception:
            continue
    return 0, 0

_IS_WINDOWS = os.name == "nt"

def _send_ffmpeg_interrupt(proc: subprocess.Popen) -> None:
    try:
        if _IS_WINDOWS:
            os.kill(proc.pid, signal.CTRL_BREAK_EVENT)
        else:
            proc.send_signal(signal.SIGINT)
    except (OSError, ValueError):
        pass

@dataclass
class _CameraRecState:
    process: Optional[subprocess.Popen] = None
    start_time: Optional[float] = None
    file_path: str = ""
    transport: str = ""
    timer: Optional[threading.Timer] = None
    log_handle: Any = None

_recording_states: Dict[str, _CameraRecState] = {}

_VIDEO_DIR = Path(__file__).resolve().parent.parent.parent / "video"
_REC_STATE_FILE = _VIDEO_DIR / "recording_state.json"

def _load_rec_state_file() -> Dict[str, dict]:
    try:
        with open(_REC_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}

def _write_rec_state_file(states: Dict[str, dict]) -> None:
    try:
        os.makedirs(_VIDEO_DIR, exist_ok=True)
        with open(_REC_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(states, f, ensure_ascii=False, indent=2)
    except OSError:
        pass

def _persist_rec_start(camera_name: str, pid: int, file_path: str,
                       stop_at: Optional[float]) -> None:
    states = _load_rec_state_file()
    states[camera_name] = {
        "pid": pid,
        "file_path": file_path,
        "start_time": time.time(),
        "stop_at": stop_at,
    }
    _write_rec_state_file(states)

def _persist_rec_remove(camera_name: str) -> None:
    states = _load_rec_state_file()
    if camera_name in states:
        states.pop(camera_name)
        _write_rec_state_file(states)

def _rec_pid_alive(pid: int) -> bool:
    try:
        import psutil
        proc = psutil.Process(pid)
        return proc.is_running() and "ffmpeg" in proc.name().lower()
    except Exception:
        return False

def _get_live_persisted_recording(camera_name: str) -> Optional[dict]:
    states = _load_rec_state_file()
    entry = states.get(camera_name)
    if not entry:
        return None
    pid = entry.get("pid", 0)
    if isinstance(pid, int) and pid > 0 and _rec_pid_alive(pid):
        return entry

    states.pop(camera_name, None)
    _write_rec_state_file(states)
    return None

def _stop_orphan_recording(camera_name: str, entry: dict) -> "RecordingResult":
    pid = entry["pid"]
    file_path = entry.get("file_path", "")
    start_time = entry.get("start_time") or time.time()

    try:
        if _IS_WINDOWS:
            os.kill(pid, signal.CTRL_BREAK_EVENT)
        else:
            os.kill(pid, signal.SIGINT)
    except OSError:
        pass

    deadline = time.time() + 15
    while time.time() < deadline and _rec_pid_alive(pid):
        time.sleep(0.5)
    if _rec_pid_alive(pid):
        try:
            import psutil
            psutil.Process(pid).kill()
        except Exception:
            pass

    _persist_rec_remove(camera_name)

    actual_duration = _get_video_duration(file_path) if file_path else None
    elapsed = time.time() - start_time
    reported_duration = actual_duration if actual_duration is not None else round(elapsed, 2)

    if not file_path or not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        return RecordingResult(
            success=False, is_recording=False,
            duration_seconds=reported_duration,
            error_message="Recording file is empty or missing; recording may not have started",
        )

    _remove_log_if_empty(file_path)
    return RecordingResult(
        success=True, is_recording=False,
        file_path=file_path,
        duration_seconds=reported_duration,
    )

def _read_log_tail(log_path: str, n: int = 300) -> str:
    try:
        with open(log_path, "rb") as f:
            data = f.read()
        return data[-n:].decode(errors="replace")
    except OSError:
        return ""

def _remove_log_if_empty(video_path: str) -> None:
    log_path = os.path.splitext(video_path)[0] + ".log"
    try:
        if os.path.isfile(log_path) and os.path.getsize(log_path) == 0:
            os.remove(log_path)
    except OSError:
        pass

def _get_video_duration(file_path: str) -> Optional[float]:
    ffprobe_path = _resolve_binary("ffprobe")
    if not ffprobe_path:
        return None
    try:
        probe = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_entries", "format=duration",
                file_path,
            ],
            capture_output=True, text=True, timeout=10,
        )
        data = json.loads(probe.stdout)
        dur = data.get("format", {}).get("duration")
        if dur is not None:
            return round(float(dur), 2)
    except Exception:
        pass
    return None

def toggle_recording(
    camera_name: str,
    action: RecordingAction,
    save_path: Optional[str] = None,
    rtsp_transport: Optional[Any] = None,
    duration: Optional[float] = None,
) -> RecordingResult:
    camera_name = coerce_str(camera_name)

    if action == RecordingAction.STATUS:
        state = _recording_states.get(camera_name)
        if state and state.process is not None and state.process.poll() is None:
            elapsed = time.time() - (state.start_time or time.time())
            return RecordingResult(
                success=True, is_recording=True,
                file_path=state.file_path,
                duration_seconds=round(elapsed, 2),
                auto_stop=state.timer is not None,
            )

        persisted = _get_live_persisted_recording(camera_name)
        if persisted:
            elapsed = time.time() - persisted.get("start_time", time.time())
            return RecordingResult(
                success=True, is_recording=True,
                file_path=persisted.get("file_path", ""),
                duration_seconds=round(elapsed, 2),
                auto_stop=persisted.get("stop_at") is not None,
            )
        return RecordingResult(
            success=True, is_recording=False,
            error_message="No recording in progress",
        )

    if action == RecordingAction.STOP:
        state = _recording_states.get(camera_name)
        if not state or state.process is None:

            persisted = _get_live_persisted_recording(camera_name)
            if persisted:
                return _stop_orphan_recording(camera_name, persisted)
            return RecordingResult(
                success=False, is_recording=False,
                error_message="No recording in progress",
            )

        if state.timer is not None:
            state.timer.cancel()
            state.timer = None

        proc = state.process
        start_time = state.start_time or time.time()
        file_path = state.file_path

        _send_ffmpeg_interrupt(proc)

        try:
            proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
                proc.wait(timeout=3)
            except Exception:
                pass

        if state.log_handle is not None:
            try:
                state.log_handle.close()
            except OSError:
                pass

        actual_duration = _get_video_duration(file_path)
        elapsed = time.time() - start_time
        reported_duration = actual_duration if actual_duration is not None else round(elapsed, 2)

        _recording_states.pop(camera_name, None)
        _persist_rec_remove(camera_name)

        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
            return RecordingResult(
                success=False, is_recording=False,
                duration_seconds=reported_duration,
                error_message="Recording file is empty or missing; recording may not have started",
            )

        _remove_log_if_empty(file_path)

        return RecordingResult(
            success=True, is_recording=False,
            file_path=file_path,
            duration_seconds=reported_duration,
        )

    if action == RecordingAction.START:

        existing = _recording_states.get(camera_name)
        if existing and existing.process is not None and existing.process.poll() is None:
            return RecordingResult(
                success=False, is_recording=True,
                error_message=f"Camera {camera_name} recording in progress (file: {existing.file_path}); stop it before starting a new recording",
            )

        if existing:
            if existing.timer is not None:
                existing.timer.cancel()
            _recording_states.pop(camera_name, None)

        persisted = _get_live_persisted_recording(camera_name)
        if persisted:
            return RecordingResult(
                success=False, is_recording=True,
                file_path=persisted.get("file_path", ""),
                error_message=f"Camera {camera_name} recording in progress (file: {persisted.get('file_path', '')}); "
                              f"if this is a retry, no need to start again; call stop first to re-record",
            )

        ffmpeg_path = _resolve_binary("ffmpeg")
        if not ffmpeg_path:
            return RecordingResult(
                success=False, is_recording=False,
                error_message="ffmpeg is not installed; recording unavailable",
            )

        from .device_mgmt import _connected_devices, _find_cached_camera, _build_rtsp_url
        conn_info = _connected_devices.get(camera_name)
        cached = _find_cached_camera(camera_name)
        if not conn_info and not cached:
            return RecordingResult(
                success=False, is_recording=False,
                error_message=f"Camera '{camera_name}' is not registered",
            )

        if cached:
            rtsp_url = _build_rtsp_url(
                cached.ip, cached.rtsp_port, cached.rtsp_path,
                cached.username, cached.password,
            )
        else:
            ip = conn_info.get("ip", "")
            rtsp_port = conn_info.get("rtsp_port", 554)
            rtsp_path = conn_info.get("rtsp_path", "/md0_0")
            username = conn_info.get("username", "")
            password = conn_info.get("password", "")
            rtsp_url = _build_rtsp_url(ip, rtsp_port, rtsp_path, username, password)

        recording_dir = save_path or str(
            Path(__file__).resolve().parent.parent.parent / "video"
        )
        try:
            os.makedirs(recording_dir, exist_ok=True)
        except OSError as e:
            return RecordingResult(
                success=False, is_recording=False,
                error_message=f"Failed to create recording directory: {e}",
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(recording_dir, f"recording_{camera_name}_{timestamp}.mp4")

        try:
            transport_plan = _resolve_transport_plan(rtsp_transport)
        except ValueError as e:
            return RecordingResult(
                success=False, is_recording=False,
                error_message=str(e),
            )

        working_transport = ""
        for transport in transport_plan:
            dims = _probe_dimensions(rtsp_url, [transport], timeout=10)
            if dims != (0, 0):
                working_transport = transport
                break

        if not working_transport:
            working_transport = transport_plan[0]

        ffmpeg_timeout = None
        if duration is not None and duration > 0:
            ffmpeg_timeout = duration + _RECORDING_STARTUP_COMPENSATION + 5.0

        last_error = ""
        for transport in ([working_transport] + [t for t in transport_plan if t != working_transport]):

            ffmpeg_cmd = [
                ffmpeg_path, "-y",
                "-loglevel", "error",
                "-nostats",
                "-rtsp_transport", transport,
                "-timeout", "5000000",
                "-i", rtsp_url,
                "-c:a", "aac",
                "-c:v", "copy",
                "-movflags", "+faststart",
            ]
            if ffmpeg_timeout is not None:
                ffmpeg_cmd += ["-t", str(ffmpeg_timeout)]
            ffmpeg_cmd.append(file_path)

            log_path = os.path.splitext(file_path)[0] + ".log"
            try:
                log_handle = open(log_path, "wb")
            except OSError:
                log_handle = None
            popen_kwargs = dict(
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=log_handle if log_handle is not None else subprocess.DEVNULL,
            )
            if _IS_WINDOWS:
                popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            try:
                proc = subprocess.Popen(ffmpeg_cmd, **popen_kwargs)
            except FileNotFoundError:
                if log_handle is not None:
                    log_handle.close()
                return RecordingResult(
                    success=False, is_recording=False,
                    error_message="ffmpeg is not installed",
                )

            popen_time = time.time()
            _recording_start_time = popen_time

            time.sleep(2)
            health_check_delay = time.time() - popen_time
            if proc.poll() is not None:

                if log_handle is not None:
                    log_handle.close()
                    log_handle = None
                last_error = _read_log_tail(log_path, 300)
                for p in (file_path, log_path):
                    try:
                        if os.path.exists(p):
                            os.remove(p)
                    except OSError:
                        pass
                continue

            if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
                state = _CameraRecState(
                    process=proc, start_time=_recording_start_time,
                    file_path=file_path, transport=transport,
                    log_handle=log_handle,
                )
                _recording_states[camera_name] = state

                stop_at = None
                if duration is not None and duration > 0:
                    compensated = max(
                        duration + _RECORDING_STARTUP_COMPENSATION - health_check_delay,
                        1.0,
                    )
                    state.timer = threading.Timer(
                        compensated,
                        lambda: toggle_recording(camera_name, RecordingAction.STOP),
                    )
                    state.timer.daemon = True
                    state.timer.start()
                    stop_at = time.time() + compensated

                _persist_rec_start(camera_name, proc.pid, file_path, stop_at)

                return RecordingResult(
                    success=True, is_recording=True,
                    file_path=file_path,
                    auto_stop=duration is not None and duration > 0,
                )

            time.sleep(8)
            if proc.poll() is None and os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
                state = _CameraRecState(
                    process=proc, start_time=_recording_start_time,
                    file_path=file_path, transport=transport,
                    log_handle=log_handle,
                )
                _recording_states[camera_name] = state

                stop_at = None
                if duration is not None and duration > 0:
                    health_check_delay = time.time() - popen_time
                    compensated = max(
                        duration + _RECORDING_STARTUP_COMPENSATION - health_check_delay,
                        1.0,
                    )
                    state.timer = threading.Timer(
                        compensated,
                        lambda: toggle_recording(camera_name, RecordingAction.STOP),
                    )
                    state.timer.daemon = True
                    state.timer.start()
                    stop_at = time.time() + compensated

                _persist_rec_start(camera_name, proc.pid, file_path, stop_at)

                return RecordingResult(
                    success=True, is_recording=True,
                    file_path=file_path,
                    auto_stop=duration is not None and duration > 0,
                )

            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                proc.kill()

            if log_handle is not None:
                log_handle.close()
                log_handle = None
            for p in (file_path, log_path):
                try:
                    if os.path.exists(p):
                        os.remove(p)
                except OSError:
                    pass
            last_error = f"transport={transport} produced no data after startup"

        return RecordingResult(
            success=False, is_recording=False,
            error_message=f"Recording failed to start (transports tried: {transport_plan}): {last_error}",
        )

    return RecordingResult(
        success=False, is_recording=False,
        error_message=f"Unknown action: {action}",
    )

import os as _os
import sys as _sys

_GO2RTC_IS_WIN = _sys.platform == "win32"
_GO2RTC_SKILL_DIR = _os.path.dirname(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
)

_go2rtc_process: Optional[Any] = None

@dataclass
class WebRTCResult:
    success: bool = False
    web_url: str = ""
    rtsp_url: str = ""
    video_codec: str = ""
    error_message: str = ""

def _ensure_go2rtc() -> str:
    import shutil
    path = shutil.which("go2rtc")
    if path:
        return path
    bin_name = "go2rtc.exe" if _GO2RTC_IS_WIN else "go2rtc"
    local_path = _os.path.join(_GO2RTC_SKILL_DIR, bin_name)
    if _os.path.isfile(local_path):
        return local_path
    return ""

_SK_VIDEO_PORT = 9010
_SK_VIDEO_TIMEOUT = 8.0

def _switch_video_codec(cam, codec: str) -> str:
    from . import camera_proto
    from .illumination import _envelope

    if not cam.sn_code:
        return f"Camera {cam.name} has no SN; cannot switch video codec; re-scan/register the device first"
    unreachable = f"Cannot connect to {cam.ip}:{_SK_VIDEO_PORT} (SK HTTP no response)"

    ok, resp, _status = _envelope(camera_proto.video_get_option(
        cam.ip, cam.sn_code, cam.username, cam.password, _SK_VIDEO_TIMEOUT))
    if not ok or not resp:
        return f"Failed to query video codec capabilities: {unreachable}"
    supported = set()
    for stream in resp.get("video") or []:
        if not isinstance(stream, dict):
            continue
        for spec in stream.get("specs") or []:
            if (isinstance(spec, dict) and spec.get("name") == "encode"
                    and isinstance(spec.get("specs"), list)):
                supported.update(str(item) for item in spec["specs"])
    if codec not in supported:
        return (f"Device does not support video codec {codec}"
                + (f" (supported: {', '.join(sorted(supported))})" if supported else "")
                + "; codec not switched")

    ok, resp, _status = _envelope(camera_proto.video_get(
        cam.ip, cam.sn_code, cam.username, cam.password, _SK_VIDEO_TIMEOUT))
    if not ok or not resp:
        return f"Failed to query current video config: {unreachable}"
    streams = resp.get("video")
    if not isinstance(streams, list) or not streams:
        return "Failed to query current video config: response missing 'video' field"
    if all(str(s.get("encode", "")).upper() == codec
           for s in streams if isinstance(s, dict)):
        return ""

    payload = {"video": [dict(s, encode=codec) for s in streams if isinstance(s, dict)]}
    ok, resp, _status = _envelope(camera_proto.video_set(
        cam.ip, cam.sn_code, cam.username, cam.password, payload, _SK_VIDEO_TIMEOUT))
    if not ok or not resp:
        return f"Failed to set video codec: {unreachable}"
    if not camera_proto.code_ok(resp.get("code", "")):
        return f"Device rejected the video codec set (code={resp.get('code')} msg={resp.get('msg')})"

    ok, resp, _status = _envelope(camera_proto.video_get(
        cam.ip, cam.sn_code, cam.username, cam.password, _SK_VIDEO_TIMEOUT))
    if not ok or not resp:
        return "Set command sent but read-back verification failed (SK HTTP no response)"
    streams = resp.get("video")
    if not isinstance(streams, list) or any(
            str(s.get("encode", "")).upper() != codec
            for s in streams if isinstance(s, dict)):
        return f"Read-back mismatch after set; codec is not {codec}"
    return ""

def start_webrtc_stream(
    camera_name: str,
    sub_stream: bool = False,
    video_codec: Optional[str] = None,
    go2rtc_path: Optional[str] = None,
    port: int = 1984,
) -> WebRTCResult:
    camera_name = coerce_str(camera_name)

    import subprocess

    global _go2rtc_process

    codec = ""
    if video_codec is not None and str(video_codec).strip():
        codec = str(video_codec).strip().upper()
        if codec not in ("H264", "H265"):
            return WebRTCResult(
                success=False,
                error_message=f"Unsupported codec: {video_codec}; video_codec only supports h264/h265; omit it to keep the device codec unchanged",
            )

    binary = go2rtc_path or _ensure_go2rtc()
    if not binary:
        return WebRTCResult(
            success=False,
            error_message=(
                f"go2rtc not detected (WebRTC relay tool, a single ~15MB file). "
                f"Follow the Obtaining go2rtc instructions in SKILL.md to get the binary for your platform, "
                f"place it in {_GO2RTC_SKILL_DIR} or add it to PATH, then retry."
            ),
        )

    from . import device_mgmt as dm
    cameras = dm.get_registered_cameras()
    target = next((c for c in cameras if c.name == camera_name), None)
    if target is None:
        return WebRTCResult(success=False, error_message=f"Camera not found: {camera_name}")

    if codec:
        if dm._is_non_sk_camera(camera_name):
            return WebRTCResult(
                success=False,
                error_message=dm._unsupported_protocol_message(camera_name, "video codec switching"),
            )
        switch_error = _switch_video_codec(target, codec)
        if switch_error:
            return WebRTCResult(success=False, error_message=switch_error)

    if _go2rtc_process is not None:
        stop_webrtc_stream()

    rtsp_path = target.rtsp_sub_path if sub_stream else target.rtsp_path
    rtsp_url = dm._build_rtsp_url(
        target.ip, target.rtsp_port, rtsp_path, target.username, target.password,
    )

    import yaml

    config_path = _os.path.join(_GO2RTC_SKILL_DIR, "go2rtc.yaml")
    stream_name = camera_name.replace(" ", "_")
    go2rtc_config = {
        "streams": {stream_name: rtsp_url},
        "api": {"listen": f":{port}"},
    }
    with open(config_path, "w") as f:
        yaml.dump(go2rtc_config, f, default_flow_style=False, allow_unicode=True)

    try:
        popen_kwargs = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
        }
        if _GO2RTC_IS_WIN:
            popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        _go2rtc_process = subprocess.Popen(
            [binary, "-config", config_path],
            **popen_kwargs,
        )
    except Exception as e:
        return WebRTCResult(
            success=False,
            rtsp_url=rtsp_url,
            error_message=f"go2rtc failed to start: {e}",
        )

    web_url = f"http://localhost:{port}"
    return WebRTCResult(success=True, web_url=web_url, rtsp_url=rtsp_url,
                        video_codec=codec)

def stop_webrtc_stream() -> bool:
    global _go2rtc_process

    if _go2rtc_process is None:
        return True

    try:
        _go2rtc_process.terminate()
        _go2rtc_process.wait(timeout=5)
    except Exception:
        try:
            _go2rtc_process.kill()
        except Exception:
            pass
    finally:
        _go2rtc_process = None

    return True
