#!/usr/bin/env python3
# Security Manifest
# - Env: TAPO_CAMERA_USERNAME, TAPO_CAMERA_PASSWORD, KASA_CREDENTIALS_HASH
# - Endpoints: https://{camera-host} via python-kasa, rtsp://{camera-host}:554/{stream}
# - Reads: none
# - Writes: user-selected output image path only

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a local Tapo camera and optionally capture one still frame."
    )
    parser.add_argument("--host", required=True, help="Camera hostname or IP")
    parser.add_argument(
        "--stream",
        choices=["hd", "sd"],
        default="hd",
        help="RTSP stream to use when capturing (default: hd)",
    )
    parser.add_argument(
        "--output",
        help="Local path for a captured image. If omitted, only a capability summary is printed.",
    )
    parser.add_argument(
        "--show-rtsp",
        action="store_true",
        help="Print the full RTSP URL. This exposes credentials and should be used sparingly.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable output.",
    )
    parser.add_argument(
        "--rtsp-transport",
        choices=["tcp", "udp"],
        default="tcp",
        help="Transport passed to ffmpeg for RTSP capture (default: tcp).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Camera connection timeout in seconds (default: 10).",
    )
    return parser.parse_args()


def build_config(host: str, timeout: int) -> DeviceConfig:
    try:
        from kasa import DeviceConfig, DeviceConnectionParameters
        from kasa import DeviceEncryptionType, DeviceFamily
        from kasa.credentials import Credentials
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "python-kasa is required. Install it with `python3 -m pip install python-kasa`."
        ) from exc

    username = os.getenv("TAPO_CAMERA_USERNAME")
    password = os.getenv("TAPO_CAMERA_PASSWORD")
    credentials_hash = os.getenv("KASA_CREDENTIALS_HASH")

    if credentials_hash and (username or password):
        raise SystemExit(
            "Use either TAPO_CAMERA_USERNAME/TAPO_CAMERA_PASSWORD or KASA_CREDENTIALS_HASH, not both."
        )

    if username or password:
        if not username or not password:
            raise SystemExit(
                "Both TAPO_CAMERA_USERNAME and TAPO_CAMERA_PASSWORD are required together."
            )
        credentials = Credentials(username=username, password=password)
    else:
        credentials = None

    if not credentials and not credentials_hash:
        raise SystemExit(
            "Set TAPO_CAMERA_USERNAME/TAPO_CAMERA_PASSWORD or KASA_CREDENTIALS_HASH before running."
        )

    camera_connection = DeviceConnectionParameters(
        DeviceFamily("SMART.IPCAMERA"),
        DeviceEncryptionType("AES"),
        2,
        True,
    )

    return DeviceConfig(
        host=host,
        timeout=timeout,
        credentials=credentials,
        credentials_hash=credentials_hash,
        connection_type=camera_connection,
    )


def redact_rtsp_url(url: str | None) -> str | None:
    if not url:
        return None
    parsed = urlsplit(url)
    host = parsed.hostname or "<unknown-host>"
    stream = parsed.path.lstrip("/")
    return f"rtsp://<redacted>@{host}:{parsed.port or 554}/{stream}"


async def inspect_camera(args: argparse.Namespace) -> dict[str, object]:
    try:
        from kasa import Device, Module, StreamResolution
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "python-kasa is required. Install it with `python3 -m pip install python-kasa`."
        ) from exc

    config = build_config(args.host, args.timeout)
    dev = await Device.connect(config=config)
    try:
        await dev.update()
        camera = dev.modules.get(Module.Camera)
        if not camera or camera.disabled:
            raise SystemExit(
                "Camera module unavailable. Check model support, privacy mode, or whether this is a hub child."
            )

        resolution = StreamResolution.HD if args.stream == "hd" else StreamResolution.SD
        rtsp_url = camera.stream_rtsp_url(stream_resolution=resolution)
        onvif_url = camera.onvif_url()

        result: dict[str, object] = {
            "host": dev.host,
            "alias": dev.alias,
            "model": dev.model,
            "firmware": dev.device_info.firmware_version,
            "stream": args.stream,
            "rtsp_available": bool(rtsp_url),
            "rtsp_url_redacted": redact_rtsp_url(rtsp_url),
            "onvif_url": onvif_url,
            "capture_path": None,
        }

        if args.output:
            if not rtsp_url:
                raise SystemExit(
                    "No RTSP URL available for this device. Check third-party compatibility or use the fallback playbook."
                )
            capture_path = capture_frame(
                rtsp_url=rtsp_url,
                output=Path(args.output).expanduser(),
                transport=args.rtsp_transport,
            )
            result["capture_path"] = str(capture_path)

        if args.show_rtsp:
            result["rtsp_url"] = rtsp_url

        return result
    finally:
        await dev.disconnect()


def capture_frame(rtsp_url: str, output: Path, transport: str) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is required for capture but was not found in PATH.")

    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg,
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-rtsp_transport",
        transport,
        "-i",
        rtsp_url,
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output),
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"ffmpeg capture failed with exit code {exc.returncode}.") from exc
    return output


def render_text(result: dict[str, object]) -> str:
    lines = [
        "Tapo camera summary",
        f"Host: {result['host']}",
        f"Alias: {result['alias']}",
        f"Model: {result['model']}",
        f"Firmware: {result['firmware']}",
        f"Stream: {result['stream']}",
        f"RTSP available: {result['rtsp_available']}",
        f"RTSP: {result['rtsp_url'] if 'rtsp_url' in result else result['rtsp_url_redacted']}",
        f"ONVIF: {result['onvif_url'] or 'not available'}",
    ]
    if result.get("capture_path"):
        lines.append(f"Capture: {result['capture_path']}")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    result = asyncio.run(inspect_camera(args))
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render_text(result))


if __name__ == "__main__":
    main()
