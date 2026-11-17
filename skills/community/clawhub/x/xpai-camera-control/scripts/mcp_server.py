import sys
import os
import json
import asyncio
import argparse
import threading

import anyio
from anyio.to_thread import current_default_thread_limiter, run_sync as run_in_thread
from typing import Any, Dict, Optional, Tuple

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from scripts._paths import get_skill_root
_skill_root = str(get_skill_root())
if _skill_root not in sys.path:
    sys.path.insert(0, _skill_root)

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

TOOLS = [

    Tool(
        name="get_registered_cameras",
        description="Read all registered camera configs (including credentials) from config.yaml without scanning the network. Call this first when a session starts.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="register_camera",
        description="Persist camera credentials to config.yaml. Automatically replaces old entries matched by IP/SN (rename).",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Unique camera name"},
                "ip": {"type": "string", "description": "IP address"},
                "port": {"type": "integer", "description": "ONVIF port (pass only verified real ports; omit if unknown — connect_device probes it and writes it back automatically)"},
                "username": {"type": "string", "description": "Login username", "default": "admin"},
                "password": {"type": "string", "description": "Login password"},
                "rtsp_port": {"type": "integer", "description": "RTSP port", "default": 554},
                "rtsp_path": {"type": "string", "description": "Main stream path", "default": "/stream1"},
                "device_class": {"type": "string", "description": "Device class: password_required / direct_connect"},
                "connection_type": {"type": "string", "description": "Connection type: onvif", "default": "onvif"},
                "sn_code": {"type": "string", "description": "Serial number"},
                "pkdk": {"type": "string", "description": "Device public key identifier"},
                "rtsp_sub_path": {"type": "string", "description": "Sub stream path", "default": "/stream2"},
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="search_devices",
        description="Scan the LAN to discover available cameras. When multiple devices are found, ALL of them must be shown to the user; never omit any.",
        inputSchema={
            "type": "object",
            "properties": {
                "timeout": {
                    "type": "number",
                    "description": "Timeout in seconds",
                    "default": 15.0,
                },
            },
        },
    ),
    Tool(
        name="connect_device",
        description="Connect to a camera. Handles credential caching, cloud authorization, and password requests automatically. Returns a status field: success / needs_password / auth_rejected / cloud_pwd_failed.",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {"type": "string", "description": "Camera name"},
                "password": {"type": "string", "description": "User password (optional)"},
                "ip": {"type": "string", "description": "Device IP"},
                "port": {"type": "integer", "description": "ONVIF port"},
                "rtsp_port": {"type": "integer", "description": "RTSP port"},
                "rtsp_path": {"type": "string", "description": "RTSP path"},
                "username": {"type": "string", "description": "Login username"},
                "sn_code": {"type": "string", "description": "Device SN (obtained during discovery; required for cloud authorization)"},
                "device_class": {"type": "string", "description": "Device class: password_required / direct_connect (determined during discovery)"},
                "protocol_type": {"type": "string", "description": "Device protocol type: S=SK private / J=JCP / O=third-party ONVIF fallback (usually leave empty; authoritatively probed during connection; auto-probed when omitted)"},
            },
            "required": ["camera_name"],
        },
    ),
    Tool(
        name="disconnect_device",
        description="Disconnect the camera and release all resources.",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {"type": "string", "description": "Camera name"},
            },
            "required": ["camera_name"],
        },
    ),

    Tool(
        name="get_audio_video_stream",
        description="Get the RTSP stream URL and metadata (codec, resolution, frame rate) without capturing frames.",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {"type": "string", "description": "Camera name"},
                "sub_stream": {
                    "type": "boolean",
                    "description": "Use the sub stream (lower quality)",
                    "default": False,
                },
                "timeout_seconds": {
                    "type": "number",
                    "description": "Max wait seconds (default 20, cap 120)"
                },
            },
            "required": ["camera_name"],
        },
    ),
    Tool(
        name="capture_video_screenshot",
        description="Capture one frame from the RTSP stream and save it as JPEG, defaulting to the snapshots/ directory.",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {"type": "string", "description": "Camera name"},
                "save_path": {"type": "string", "description": "Save directory"},
                "timeout_seconds": {
                    "type": "number",
                    "description": "Max wait seconds (default 20, cap 120)"
                },
            },
            "required": ["camera_name"],
        },
    ),
    Tool(
        name="toggle_recording",
        description="Start, stop, or query local MP4 recording, defaulting to the video/ directory.",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {"type": "string", "description": "Camera name"},
                "action": {
                    "type": "string",
                    "enum": ["start", "stop", "status"],
                    "description": "start / stop / status",
                },
                "save_path": {"type": "string", "description": "Recording save directory"},
                "duration": {
                    "type": "number",
                    "description": "Recording duration (seconds); only valid for start; recording stops automatically when reached"
                },
            },
            "required": ["camera_name", "action"],
        },
    ),
    Tool(
        name="control_ptz",
        description="Control PTZ pan/tilt in four directions. Specify the movement via duration_seconds or degrees (choose one).",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {"type": "string", "description": "Camera name"},
                "direction": {
                    "type": "string",
                    "enum": ["up", "down", "left", "right"],
                    "description": "Movement direction (up/down/left/right)"
                },
                "speed": {
                    "type": "number",
                    "description": "Speed 0.0-1.0",
                    "default": 0.5,
                },
                "duration_seconds": {
                    "type": "number",
                    "description": "Movement duration (seconds); mutually exclusive with degrees"
                },
                "degrees": {
                    "type": "number",
                    "description": "Movement angle in degrees; mutually exclusive with duration_seconds"
                },
            },
            "required": ["camera_name", "direction"],
        },
    ),
    Tool(
        name="stop_ptz",
        description="Stop ongoing PTZ pan/tilt movement immediately.",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {"type": "string", "description": "Camera name"},
            },
            "required": ["camera_name"],
        },
    ),

    Tool(
        name="manage_camera_events",
        description="Camera alarm event management: start a listener / stop / poll events / wait for new events.",
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["start", "stop", "poll", "wait"],
                    "description": "Working mode"
                },
                "camera_name": {
                    "type": "string",
                    "description": "Camera name (required for start/stop)"
                },
                "debounce_seconds": {
                    "type": "number",
                    "description": "Deduplication window (seconds, start only)",
                    "default": 5.0,
                },
                "limit": {
                    "type": "integer",
                    "description": "Max events returned per call (poll only)",
                    "default": 100,
                },
                "timeout_seconds": {
                    "type": "number",
                    "description": "Blocking timeout (seconds, cap 60, wait only)",
                    "default": 60,
                },
            },
            "required": ["action"],
        },
    ),

    Tool(
        name="start_webrtc_stream",
        description="Start a WebRTC live preview and return the browser URL. Optionally set video_codec to switch the device codec to H264 (use when the preview stutters in Edge and similar browsers).",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {"type": "string", "description": "Camera name"},
                "sub_stream": {
                    "type": "boolean",
                    "description": "Use the sub stream (lower quality)",
                    "default": False,
                },
                "video_codec": {
                    "type": "string",
                    "enum": ["h264", "h265"],
                    "description": "Optional: switch the device video codec before starting the preview. Edge does not support H265 WebRTC; switch to h264 when the preview stutters or shows a black screen. This is a device-level global setting (main and sub streams change together) and briefly interrupts all RTSP sessions of the device; omit to keep the current codec."
                },
                "port": {
                    "type": "integer",
                    "description": "Web UI port",
                    "default": 1984,
                },
            },
            "required": ["camera_name"],
        },
    ),
    Tool(
        name="stop_webrtc_stream",
        description="Stop the WebRTC live preview and shut down the stream relay process.",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),

    Tool(
        name="manage_illumination",
        description="Query or set fill-light and night-vision modes (daynightmode / filllightmode).",
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get", "set"],
                    "description": "Working mode"
                },
                "camera_name": {
                    "type": "string",
                    "description": "Camera name",
                },
                "daynightmode": {
                    "description": "0=Day mode / 1=Night mode / 2=Auto mode / 3=Schedule mode / 4=Smart mode"
                },
                "filllightmode": {
                    "description": "0=Full-color mode / 1=Infrared mode / 2=Smart night-vision mode"
                },
            },
            "required": ["action", "camera_name"],
        },
    ),

    Tool(
        name="manage_image_settings",
        description="Query or set image parameters: brightness, contrast, saturation, sharpness, and image flip.",
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get", "set"],
                    "description": "Working mode"
                },
                "camera_name": {
                    "type": "string",
                    "description": "Camera name",
                },
                "brightness": {
                    "type": "integer",
                    "description": "Brightness",
                },
                "contrast": {
                    "type": "integer",
                    "description": "Contrast",
                },
                "saturation": {
                    "type": "integer",
                    "description": "Saturation",
                },
                "sharpness": {
                    "type": "integer",
                    "description": "Sharpness",
                },
                "flip": {
                    "type": "integer",
                    "enum": [0, 1, 2, 3],
                    "description": "0=Normal / 1=Diagonal flip / 2=Horizontal flip / 3=Vertical flip"
                },
            },
            "required": ["action", "camera_name"],
        },
    ),

    Tool(
        name="query_tracking_capabilities",
        description="Query smart-detection and tracking capabilities (human/vehicle/area/motion/line-crossing).",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {
                    "type": "string",
                    "description": "Camera name",
                },
                "detect_type": {
                    "type": "string",
                    "description": "human / vehicle / area / motion / line / all",
                    "default": "all",
                },
            },
            "required": ["camera_name"],
        },
    ),
    Tool(
        name="set_tracking",
        description="Enable or disable smart-detection and tracking features; pass only the parameters to change.",
        inputSchema={
            "type": "object",
            "properties": {
                "camera_name": {
                    "type": "string",
                    "description": "Camera name",
                },
                "detect_type": {
                    "type": "string",
                    "description": "human / vehicle / area / motion / line",
                },
                "enable": {
                    "type": "boolean",
                    "description": "Whether to enable this detection feature"
                },
                "tracking": {
                    "type": "boolean",
                    "description": "Whether to enable tracking"
                },
                "sensitivity_level": {
                    "type": "integer",
                    "description": "Sensitivity 0-3",
                },
            },
            "required": ["camera_name", "detect_type"],
        },
    ),
]

def _serialize(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, (list, tuple)):
        return [_serialize(i) for i in obj]
    if isinstance(obj, dict):
        return {str(k): _serialize(v) for k, v in obj.items()}
    if hasattr(obj, "__dataclass_fields__"):
        return {f.name: _serialize(getattr(obj, f.name)) for f in obj.__dataclass_fields__.values()}
    if hasattr(obj, "_value_"):
        return obj.value
    return str(obj)

_TOOL_TIMEOUTS: Dict[str, float] = {
    "capture_video_screenshot": 45.0,
    "get_audio_video_stream": 45.0,
    "toggle_recording": 90.0,
    "connect_device": 360.0,
    "start_webrtc_stream": 90.0,
}
_DEFAULT_TOOL_TIMEOUT = 60.0
_STREAM_TIMEOUT_ARG_MAX = 120.0
_STREAM_TIMEOUT_ARG_MARGIN = 25.0

def _resolve_tool_budget(name: str, args: Dict[str, Any]) -> float:
    if name in ("capture_video_screenshot", "get_audio_video_stream"):
        ts = args.get("timeout_seconds")
        if isinstance(ts, (int, float)) and not isinstance(ts, bool) and ts > 0:
            inner = min(float(ts), _STREAM_TIMEOUT_ARG_MAX)
            return inner + _STREAM_TIMEOUT_ARG_MARGIN
        return _TOOL_TIMEOUTS[name]
    if name == "search_devices":
        ts = args.get("timeout")
        base = float(ts) if isinstance(ts, (int, float)) and ts > 0 else 15.0
        return base + 30.0
    return _TOOL_TIMEOUTS.get(name, _DEFAULT_TOOL_TIMEOUT)

def _call_tool(name: str, args: Dict[str, Any]) -> Any:
    import scripts.toolkit as tk
    from scripts.toolkit.stream import RecordingAction
    from scripts.toolkit.ptz import PTZDirection
    from scripts.toolkit.events import EventAction
    from scripts.toolkit.illumination import IlluminationAction
    from scripts.toolkit.image_settings import ImageAction
    from scripts.toolkit.tracking import TrackingAction

    if name == "get_registered_cameras":
        return _serialize(tk.get_registered_cameras())
    elif name == "register_camera":
        return _serialize(tk.register_camera(**args))
    elif name == "search_devices":
        result = _serialize(tk.search_devices(**args))
        if isinstance(result, dict):
            count = len(result.get("devices", []))
            result["device_count"] = count
            if count > 0:
                result["_display_instruction"] = (
                    f"Discovered {count} devices; ALL {count} devices above must be shown to the user in full; omission is not allowed"
                )
        return result
    elif name == "connect_device":
        return _serialize(tk.connect_device(**args))
    elif name == "disconnect_device":
        return _serialize(tk.disconnect_device(**args))

    elif name in ("get_audio_video_stream", "capture_video_screenshot"):

        args = {k: v for k, v in args.items() if k != "timeout_seconds"}
        if name == "get_audio_video_stream":
            return _serialize(tk.get_audio_video_stream(**args))
        return _serialize(tk.capture_video_screenshot(**args))
    elif name == "toggle_recording":
        args = dict(args)
        if "action" in args:
            args["action"] = RecordingAction(args["action"])
        return _serialize(tk.toggle_recording(**args))
    elif name == "control_ptz":
        args = dict(args)
        if "direction" in args:
            args["direction"] = PTZDirection(args["direction"])
        return _serialize(tk.control_ptz(**args))
    elif name == "stop_ptz":
        return _serialize(tk.stop_ptz(**args))

    elif name == "manage_camera_events":
        args = dict(args)
        args.pop("protocols", None)
        args["action"] = EventAction(args["action"])
        return _serialize(tk.manage_camera_events(**args))

    elif name == "start_webrtc_stream":
        return _serialize(tk.start_webrtc_stream(**args))
    elif name == "stop_webrtc_stream":
        return _serialize(tk.stop_webrtc_stream())

    elif name == "manage_illumination":
        args = dict(args)
        args["action"] = IlluminationAction(args["action"])
        return _serialize(tk.manage_illumination(**args))

    elif name == "manage_image_settings":
        args = dict(args)
        if "action" in args:
            args["action"] = ImageAction(args["action"])
        return _serialize(tk.manage_image_settings(**args))

    elif name == "query_tracking_capabilities":
        return _serialize(tk.manage_tracking(action=TrackingAction.QUERY, **args))
    elif name == "set_tracking":
        return _serialize(tk.manage_tracking(action=TrackingAction.SET, **args))

    else:
        raise ValueError(f"Unknown tool: {name}")

server = Server("xpai-camera-control", version="1.5.6")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return TOOLS

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any] | None) -> list[TextContent]:
    args = arguments or {}
    if name not in _LOCK_EXEMPT_TOOLS:
        lock_error = await run_in_thread(_ensure_camera_lock)
        if lock_error is not None:
            return [TextContent(
                type="text",
                text=json.dumps(lock_error, ensure_ascii=False, indent=2),
            )]
    budget = _resolve_tool_budget(name, args)
    try:

        with anyio.fail_after(budget):
            result = await run_in_thread(
                _call_tool, name, args, abandon_on_cancel=True,
            )
        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2),
        )]
    except TimeoutError:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error_code": "timeout",
                "error_message": f"Tool {name} timed out after {budget:.0f}s and was abandoned. Retry with a larger timeout_seconds.",
            }, ensure_ascii=False, indent=2),
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e),
            }, ensure_ascii=False, indent=2),
        )]

def _resume_event_monitors_async() -> None:
    def _worker():
        try:
            from scripts.toolkit.events import resume_persisted_monitors
            resume_persisted_monitors()
        except Exception:
            pass

    threading.Thread(target=_worker, name="EventMonitorResume", daemon=True).start()

_instance_lock_socket = None
_lease_file = os.path.join(_skill_root, ".instance_lease.json")
_lock_mutex = threading.Lock()
_lock_held = False
_LOCK_EXEMPT_TOOLS = {"get_registered_cameras", "register_camera", "search_devices"}

def _write_lease(pid: int, port: int) -> None:
    import time
    tmp = _lease_file + ".tmp"
    content = json.dumps({"pid": pid, "port": port, "ts": time.time()})
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, _lease_file)

def _get_lock_port() -> int:
    import zlib
    return 40000 + (
        zlib.crc32(_skill_root.lower().replace("\\", "/").encode("utf-8")) % 20000
    )

def _find_pid_on_port(port: int) -> Optional[int]:
    import subprocess
    try:
        if sys.platform == "win32":
            out = subprocess.check_output(
                ["netstat", "-ano", "-p", "TCP"],
                timeout=3, stderr=subprocess.DEVNULL, text=True,
            )
            target = f":{port} "
            for line in out.splitlines():
                if target in line and "LISTENING" in line:
                    parts = line.split()
                    if parts:
                        try:
                            return int(parts[-1])
                        except ValueError:
                            pass
        elif sys.platform == "darwin":
            out = subprocess.check_output(
                ["lsof", "-i", f":{port}", "-sTCP:LISTEN", "-Fn"],
                timeout=3, stderr=subprocess.DEVNULL, text=True,
            )
            for line in out.splitlines():
                if line.startswith("n") and "pid" in line.lower():
                    continue
                if line.startswith("p"):
                    try:
                        return int(line[1:])
                    except ValueError:
                        pass
        else:
            out = subprocess.check_output(
                ["ss", "-tlnp", f"sport = :{port}"],
                timeout=3, stderr=subprocess.DEVNULL, text=True,
            )
            for line in out.splitlines():
                if "users:" in line:
                    import re
                    m = re.search(r'pid=(\d+)', line)
                    if m:
                        return int(m.group(1))
    except Exception:
        pass
    return None

def _get_process_cmdline(pid: int) -> str:
    import subprocess
    try:
        if sys.platform == "win32":
            cmd = [
                "powershell", "-NoProfile", "-Command",
                f"Get-CimInstance Win32_Process -Filter 'ProcessId={pid}' | Select -Expand CommandLine",
            ]
            out = subprocess.check_output(cmd, timeout=5, stderr=subprocess.DEVNULL, text=True)
            return out.strip()
        elif sys.platform == "darwin":
            out = subprocess.check_output(
                ["ps", "-p", str(pid), "-o", "command="],
                timeout=3, stderr=subprocess.DEVNULL, text=True,
            )
            return out.strip()
        else:
            with open(f"/proc/{pid}/cmdline", "r", encoding="utf-8", errors="replace") as f:
                return f.read().replace("\0", " ")
    except Exception:
        return ""

def _is_our_server(cmdline: str, pid: Optional[int] = None) -> bool:
    norm = os.path.normcase(cmdline).replace("\\", "/")
    if "mcp_server.py" not in norm:
        return False
    if os.path.normcase(_skill_root).replace("\\", "/") in norm:
        return True
    # No absolute path in cmdline (e.g. relative-path registration): fall back to the lease pid.
    if pid is None:
        return False
    try:
        with open(_lease_file, "r", encoding="utf-8") as f:
            return json.load(f).get("pid") == pid
    except Exception:
        return False

def _kill_pid(pid: int) -> bool:
    import subprocess
    try:
        if sys.platform == "win32":
            subprocess.check_call(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                timeout=5, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            )
        else:
            import signal
            os.kill(pid, signal.SIGKILL)
        return True
    except Exception:
        return False

def _acquire_instance_lock() -> Tuple[Optional[int], str]:
    global _instance_lock_socket
    import socket

    port = _get_lock_port()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except OSError:
        s.close()
        return _try_recover_lock(port)
    s.listen(1)  # visible in netstat/ss/lsof, required by _find_pid_on_port
    _instance_lock_socket = s
    return port, ""

def _try_recover_lock(port: int) -> Tuple[Optional[int], str]:
    global _instance_lock_socket
    import socket
    import time

    pid = _find_pid_on_port(port)
    if pid is None:
        return None, f"Lock port {port} is occupied, but the listening process could not be identified; retry later"

    cmdline = _get_process_cmdline(pid)
    if not _is_our_server(cmdline, pid):
        return None, f"Lock port {port} is occupied by another program (PID {pid}); close it and retry"

    killed = _kill_pid(pid)  # a concurrent starter may have killed it already
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for _ in range(10):
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            time.sleep(0.5)
            continue
        s.listen(1)  # visible in netstat/ss/lsof, required by _find_pid_on_port
        _instance_lock_socket = s
        if killed:
            print(f"[instance-lock] took over from PID {pid}", file=sys.stderr, flush=True)
        return port, ""
    s.close()
    if killed:
        return None, f"Killed the previous instance (PID {pid}), but lock port {port} was not released within 5 seconds; retry"
    return None, f"Failed to kill the previous instance (PID {pid}); lock port {port} is still occupied"

def _ensure_camera_lock() -> Optional[dict]:
    """Take the instance lock on first use; returns None on success, else an error payload."""
    global _lock_held
    if _lock_held:
        return None
    with _lock_mutex:
        if _lock_held:
            return None
        port, fail_reason = _acquire_instance_lock()
        if port is None:
            print(f"[instance-lock] conflict: {fail_reason}", file=sys.stderr, flush=True)
            return {
                "success": False,
                "error_code": "instance_lock_conflict",
                "error_message": fail_reason,
                "lock_port": _get_lock_port(),
            }
        _lock_held = True
        try:
            _write_lease(os.getpid(), port)
        except Exception:
            pass
        _resume_event_monitors_async()
    return None

async def main():
    parser = argparse.ArgumentParser(description="XPAI Camera Control MCP Server")
    parser.add_argument("--transport", default="stdio", choices=["stdio"],
                        help="Transport to use (default: stdio)")
    args = parser.parse_args()

    try:
        import cv2
    except Exception:
        pass

    current_default_thread_limiter().total_tokens = 16

    async with stdio_server() as (read_stream, write_stream):

        sys.stdout = sys.stderr
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)

    os._exit(70)

if __name__ == "__main__":
    asyncio.run(main())
