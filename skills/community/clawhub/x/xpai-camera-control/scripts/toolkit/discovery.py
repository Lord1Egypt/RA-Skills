import socket
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

try:
    from . import camera_proto
except ImportError:
    import camera_proto

SUBTYPE_NAMES = {
    "1": "Bullet Camera",
    "2": "PTZ Camera",
    "3": "Dome Camera",
    "5": "PT Camera",
    "6": "Bullet-Dome Linkage",
}

@dataclass
class SkChannelInfo:
    chl: str = "0"
    name: str = ""
    stream: str = ""

@dataclass
class SkDiscoveredDevice:
    ip: str = ""
    sn: str = ""
    device_type: str = ""
    subtype: str = ""
    manufacturer: str = ""
    solution: str = ""
    name: str = ""
    dtype: str = ""
    model: str = ""
    hw_version: str = ""
    sw_version: str = ""
    did: str = ""
    channels: int = 1
    channel_list: List[SkChannelInfo] = field(default_factory=list)
    rtsp_port: int = 554
    web_port: int = 80
    udp_port: int = 9008
    net_type: str = "eth"
    ip_mode: str = "0"
    mask: str = ""
    gateway: str = ""
    mac: str = ""
    discovered_at: float = field(default_factory=time.time)

    @property
    def subtype_name(self) -> str:
        return SUBTYPE_NAMES.get(self.subtype, f"Unknown({self.subtype})")

    @property
    def rtsp_paths(self) -> List[str]:
        paths = []
        for ch in self.channel_list:
            if ch.stream:
                for s in ch.stream.split(","):
                    s = s.strip()
                    if s:
                        paths.append(s if s.startswith("/") else "/" + s)
        return paths

def _get_local_ip() -> Optional[str]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def _device_from_response(obj) -> Optional[SkDiscoveredDevice]:
    if not isinstance(obj, dict):
        return None

    try:

        src_ip = str(obj.get("_src", "") or "")
        ip = str(obj.get("ip", "") or "")
        if not ip and src_ip:
            ip = src_ip
        elif ip and src_ip and ip != src_ip:
            ip = src_ip

        channel_list = []
        for ch in obj.get("mode", []):
            channel_list.append(SkChannelInfo(
                chl=str(ch.get("chl", "")),
                name=str(ch.get("name", "")),
                stream=str(ch.get("stream", "")),
            ))

        return SkDiscoveredDevice(
            ip=ip,
            sn=obj.get("sn", ""),
            device_type=obj.get("type", ""),
            subtype=obj.get("subtype", ""),
            manufacturer=obj.get("mfr", ""),
            solution=obj.get("soln", ""),
            name=obj.get("name", ""),
            dtype=obj.get("dtype", ""),
            model=obj.get("model", ""),
            hw_version=obj.get("hwver", ""),
            sw_version=obj.get("swver", ""),
            did=obj.get("did", ""),
            channels=int(obj.get("chls", "1")),
            channel_list=channel_list,
            rtsp_port=int(obj.get("rtsp", "554")),
            web_port=int(obj.get("web", "80")),
            udp_port=int(obj.get("udp", "9008")),
            net_type=obj.get("net", "eth"),
            ip_mode=obj.get("ipmode", "0"),
            mask=obj.get("mask", ""),
            gateway=obj.get("gw", ""),
            mac=obj.get("mac", ""),
            discovered_at=time.time(),
        )
    except (TypeError, ValueError):
        return None

def discover_sky_devices(
    timeout: float = 5.0,
    target_sn: str = "",
) -> List[SkDiscoveredDevice]:
    local_ip = _get_local_ip()

    discovered: Dict[str, SkDiscoveredDevice] = {}

    try:
        responses = camera_proto.discovery_search(timeout=timeout, target_sn=target_sn)
    except Exception:
        responses = []

    for obj in responses:
        device = _device_from_response(obj)
        if device is None:
            continue

        device_ip = device.ip
        if not device_ip:
            continue

        if local_ip and device_ip == local_ip:
            continue
        device.ip = device_ip

        if device_ip in discovered:
            continue

        discovered[device_ip] = device

    return list(discovered.values())

class SkyDiscoveryListener:

    def __init__(
        self,
        interval: float = 30.0,
        timeout: float = 5.0,
        on_found: Optional[callable] = None,
    ):
        self._interval = interval
        self._timeout = timeout
        self._on_found = on_found
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._devices: Dict[str, SkDiscoveredDevice] = {}
        self._lock = threading.Lock()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="SkyDiscoveryListener",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=3)
            self._thread = None

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                devices = _silent_discover(
                    timeout=self._timeout,
                )
                with self._lock:
                    for dev in devices:
                        if dev.ip not in self._devices:
                            self._devices[dev.ip] = dev
                            if self._on_found:
                                try:
                                    self._on_found(dev)
                                except Exception:
                                    pass
            except Exception:
                pass

            self._stop_event.wait(self._interval)

    def get_devices(self) -> List[SkDiscoveredDevice]:
        with self._lock:
            return list(self._devices.values())

    def get_new_devices(self, known_ips: set) -> List[SkDiscoveredDevice]:
        with self._lock:
            return [d for ip, d in self._devices.items() if ip not in known_ips]

def _silent_discover(
    timeout: float = 5.0,
) -> List[SkDiscoveredDevice]:
    local_ip = _get_local_ip()
    discovered: Dict[str, SkDiscoveredDevice] = {}

    try:
        responses = camera_proto.discovery_search(timeout=timeout)
    except Exception:
        return []

    for obj in responses:
        device = _device_from_response(obj)
        if device is None or not device.ip:
            continue

        if local_ip and device.ip == local_ip:
            continue
        if device.ip not in discovered:
            discovered[device.ip] = device

    return list(discovered.values())

def probe_device_sn(
    ip: str,
    timeout: float = 3.0,
) -> str:
    try:
        return camera_proto.probe_device_sn(ip=ip, timeout=timeout)
    except Exception:
        return ""
