#!/usr/bin/env python3
"""Create a tar/tar.gz archive and upload it to WebDAV."""

from __future__ import annotations

import argparse
import fnmatch
import os
import shlex
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.parse import quote
from zoneinfo import ZoneInfo

SUCCESS_MKCOL = {201, 301, 405}
SUCCESS_PUT = {200, 201, 204}


def parse_env_file(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def require_env(env: Dict[str, str], key: str) -> str:
    value = env.get(key)
    if not value:
        raise ValueError("Missing required env key: {}".format(key))
    return value


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ["B", "K", "M", "G", "T"]:
        if size < 1024.0 or unit == "T":
            if unit == "B":
                return "{}{}".format(int(size), unit)
            return "{:.0f}{}".format(size, unit)
        size /= 1024.0
    return "{}B".format(num_bytes)


def run_cmd(cmd: List[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    kwargs = {
        "stdout": subprocess.PIPE if capture else None,
        "stderr": subprocess.PIPE if capture else None,
        "text": True,
        "check": False,
    }
    result = subprocess.run(cmd, **kwargs)
    if check and result.returncode != 0:
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        raise RuntimeError(
            "Command failed ({}): {}\nstdout:\n{}\nstderr:\n{}".format(
                result.returncode,
                " ".join(shlex.quote(part) for part in cmd),
                stdout[-1000:],
                stderr[-1000:],
            )
        )
    return result


def should_exclude(name: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def tar_filter(patterns: List[str]):
    def _filter(tarinfo: tarfile.TarInfo):
        if should_exclude(tarinfo.name, patterns):
            return None
        return tarinfo

    return _filter


def build_archive_name(prefix: str, compression: str, timezone: str) -> str:
    stamp = datetime.now(ZoneInfo(timezone)).strftime("%Y-%m-%d-%H%M%S")
    if compression == "gz":
        return "{}-{}.tar.gz".format(prefix, stamp)
    return "{}-{}.tar".format(prefix, stamp)


def make_archive(archive_path: Path, sources: List[Path], patterns: List[str], compression: str) -> None:
    mode = "w:gz" if compression == "gz" else "w"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, mode) as tar:
        for source in sources:
            arcname = source.name
            tar.add(str(source), arcname=arcname, filter=tar_filter(patterns))


def curl_config_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")


def create_curl_auth_config(tmp_dir: Path, user: str, password: str) -> Path:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    fd, raw_path = tempfile.mkstemp(prefix="webdav-curl-auth-", suffix=".conf", dir=str(tmp_dir))
    os.close(fd)
    path = Path(raw_path)
    path.write_text(
        'user = "{}:{}"\n'.format(curl_config_escape(user), curl_config_escape(password)),
        encoding="utf-8",
    )
    path.chmod(0o600)
    return path


def ensure_remote_dir(base_url: str, remote_subdir: str, curl_bin: str, auth_config: Path) -> None:
    current = base_url.rstrip("/") + "/"
    pieces = [piece for piece in remote_subdir.strip("/").split("/") if piece]
    for piece in pieces:
        current = current + quote(piece) + "/"
        result = run_cmd([
            curl_bin,
            "--config",
            str(auth_config),
            "-sS",
            "-o",
            "/dev/null",
            "-w",
            "%{http_code}",
            "-X",
            "MKCOL",
            current,
            "--connect-timeout",
            "20",
            "--max-time",
            "60",
        ], check=False)
        try:
            status = int((result.stdout or "").strip() or "0")
        except ValueError:
            status = 0
        if status not in SUCCESS_MKCOL:
            raise RuntimeError("MKCOL failed for {} with HTTP {}".format(current, status))


def upload_file(base_url: str, remote_subdir: str, archive_name: str, archive_path: Path, curl_bin: str, auth_config: Path) -> int:
    remote_url = "{}/{}/{}".format(
        base_url.rstrip("/"),
        "/".join(quote(part) for part in remote_subdir.strip("/").split("/") if part),
        quote(archive_name),
    )
    result = run_cmd([
        curl_bin,
        "--config",
        str(auth_config),
        "-sS",
        "-o",
        "/dev/null",
        "-w",
        "%{http_code}",
        "-T",
        str(archive_path),
        remote_url,
        "--connect-timeout",
        "30",
        "--max-time",
        "1800",
    ], check=False)
    try:
        return int((result.stdout or "").strip() or "0")
    except ValueError:
        return 0


def send_notification(openclaw_bin: str, channel: str, target: str, message: str) -> None:
    if not channel or not target:
        return
    run_cmd([
        openclaw_bin,
        "message",
        "send",
        "--channel",
        channel,
        "--target",
        target,
        "--message",
        message,
    ], capture=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive local paths and upload to WebDAV.")
    parser.add_argument("--source", action="append", required=True, help="Local file or directory to archive. Repeatable.")
    parser.add_argument("--archive-prefix", default="backup", help="Archive filename prefix.")
    parser.add_argument("--remote-subdir", required=True, help="Subdirectory under WEBDAV_SITE for uploaded archives.")
    parser.add_argument("--env-file", default=".env", help="Env file containing WebDAV credentials.")
    parser.add_argument("--tmp-dir", default="/tmp/openclaw-webdav-sync", help="Temporary directory for archive creation.")
    parser.add_argument("--exclude", action="append", default=[], help="Archive exclude glob, matched against tar entry names.")
    parser.add_argument("--compression", choices=["gz", "none"], default="gz", help="Archive compression mode.")
    parser.add_argument("--timezone", default="Asia/Shanghai", help="Timezone used in archive timestamps.")
    parser.add_argument("--notify-channel", default="", help="Optional OpenClaw notification channel.")
    parser.add_argument("--notify-target", default="", help="Optional OpenClaw notification target.")
    parser.add_argument("--openclaw-bin", default="openclaw", help="Path to OpenClaw CLI.")
    parser.add_argument("--curl-bin", default="curl", help="Path to curl binary.")
    parser.add_argument("--keep-local", action="store_true", help="Keep local archive after upload.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.time()
    env_path = Path(args.env_file)
    if not env_path.exists():
        raise FileNotFoundError("Env file not found: {}".format(env_path))

    env = parse_env_file(env_path)
    base_url = require_env(env, "WEBDAV_SITE").rstrip("/")
    user = require_env(env, "WEBDAV_USERID")
    password = require_env(env, "WEBDAV_PWD")

    sources = [Path(item).expanduser().resolve() for item in args.source]
    missing = [str(path) for path in sources if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing source paths: {}".format(", ".join(missing)))

    tmp_dir = Path(args.tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    compression = args.compression
    archive_name = build_archive_name(args.archive_prefix, compression, args.timezone)
    archive_path = tmp_dir / archive_name
    auth_config = create_curl_auth_config(tmp_dir, user, password)

    try:
        print("[webdav-sync] creating archive {}".format(archive_path))
        make_archive(archive_path, sources, args.exclude, compression)
        archive_size = archive_path.stat().st_size
        archive_size_human = human_size(archive_size)
        print("[webdav-sync] archive ready {}".format(archive_size_human))

        ensure_remote_dir(base_url, args.remote_subdir, args.curl_bin, auth_config)
        print("[webdav-sync] remote directory ready")

        put_status = upload_file(base_url, args.remote_subdir, archive_name, archive_path, args.curl_bin, auth_config)
        if put_status not in SUCCESS_PUT:
            raise RuntimeError("PUT failed with HTTP {}".format(put_status))

        duration = int(time.time() - started)
        message = "✅ WebDAV 同步成功\n文件：{}\n大小：{} ({} bytes)\n耗时：{}s".format(
            archive_name,
            archive_size_human,
            archive_size,
            duration,
        )
        send_notification(args.openclaw_bin, args.notify_channel, args.notify_target, message)
        print("[webdav-sync] upload succeeded HTTP {}".format(put_status))

        if not args.keep_local and archive_path.exists():
            archive_path.unlink()
        return 0
    finally:
        if auth_config.exists():
            auth_config.unlink()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("[webdav-sync] error: {}".format(exc), file=sys.stderr)
        try:
            parsed = parse_args()
            send_notification(
                parsed.openclaw_bin,
                parsed.notify_channel,
                parsed.notify_target,
                "❌ WebDAV 同步失败：{}".format(exc),
            )
        except Exception:
            pass
        raise
