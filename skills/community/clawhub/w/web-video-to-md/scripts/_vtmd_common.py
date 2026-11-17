"""Shared helpers for the web-video-to-md skill.

Keeps yt-dlp / ffmpeg discovery, version staleness checks and subprocess
wrapping in one place so both entry scripts behave identically.
"""

from __future__ import annotations

import datetime as _dt
import glob as _glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

MEDIA_SUFFIXES = {
    ".mp4", ".m4a", ".mp3", ".webm", ".mkv", ".opus", ".ogg",
    ".flac", ".mov", ".avi", ".wav", ".aac", ".ts",
}
PARTIAL_SUFFIXES = (".part", ".ytdl")
SUBTITLE_SUFFIXES = {".srt", ".vtt", ".ass", ".ssa", ".lrc"}

_VERSION_RE = re.compile(r"^(\d{4})\.(\d{2})\.(\d{2})$")
_RETRYABLE_MARKERS = (
    "412",
    "precondition failed",
    "sign in to confirm",
    "unable to extract",
    "unable to download api page",
    "http error 403",
    "http error 429",
)


def log(message: str, stream=sys.stderr) -> None:
    try:
        print(message, file=stream)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode("ascii"), file=stream)


def child_env():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run(cmd, timeout=None, cwd=None):
    """Run a command and return (returncode, stdout, stderr). Never raises."""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=cwd,
            shell=False,
            env=child_env(),
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        return 124, (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""), "timeout"
    except OSError as exc:
        return 127, "", str(exc)


def parse_json_blob(text):
    """Extract the first JSON object from yt-dlp output that mixes in log lines."""
    import json
    text = text or ""
    start = text.find("{")
    if start < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
        return obj
    except ValueError:
        return None


def parse_version_date(text):
    text = (text or "").strip().splitlines()[-1].strip() if text else ""
    match = _VERSION_RE.match(text)
    if not match:
        return None
    try:
        return _dt.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def version_age_days(version):
    date = parse_version_date(version)
    if date is None:
        return None
    return (_dt.date.today() - date).days


def looks_retryable(output):
    lowered = (output or "").lower()
    return any(marker in lowered for marker in _RETRYABLE_MARKERS)


def origin_of(url):
    parts = urlparse(url)
    if parts.scheme and parts.netloc:
        return "%s://%s/" % (parts.scheme, parts.netloc)
    return None


def human_bytes(size):
    size = float(size or 0)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return "%.1f%s" % (size, unit) if unit != "B" else "%dB" % int(size)
        size /= 1024


# ---------------------------------------------------------------------------
# Python / yt-dlp / ffmpeg discovery
# ---------------------------------------------------------------------------

def _unique(seq):
    out = []
    for item in seq:
        if item and item not in out:
            out.append(item)
    return out


def python_candidates(explicit=None):
    """Return a list of python command prefixes ([exe] or [exe, '-m'])."""
    candidates = []
    for exe in _unique([
        explicit,
        os.environ.get("VTMD_PYTHON"),
        sys.executable,
        shutil.which("python3"),
        shutil.which("python"),
    ]):
        candidates.append([exe])
    home = Path.home()
    for path in sorted(_glob.glob(str(home / "AppData/Roaming/Python/Python3*/python.exe")), reverse=True):
        candidates.append([path])
    if shutil.which("py"):
        candidates.append(["py", "-3"])
    # Deduplicate by the joined command.
    seen = set()
    result = []
    for cmd in candidates:
        key = " ".join(cmd)
        if key in seen:
            continue
        seen.add(key)
        result.append(cmd)
    return result


def _module_version(python_cmd):
    code = "import yt_dlp; print(yt_dlp.version.__version__)"
    rc, out, _ = run([*python_cmd, "-c", code], timeout=40)
    if rc != 0:
        return None
    value = out.strip().splitlines()[-1].strip() if out.strip() else ""
    return value or None


class YtDlpTool:
    """A resolved way to invoke yt-dlp plus its update channel."""

    def __init__(self, base, kind, version=None, update_cmd=None, source=""):
        self.base = list(base)
        self.kind = kind              # "exe" | "module"
        self.version = version or ""
        self.update_cmd = list(update_cmd) if update_cmd else None
        self.source = source
        self.updated = False

    def __call__(self, *args, **kwargs):
        return run([*self.base, *args], **kwargs)

    def refresh_version(self):
        _, out, _ = run([*self.base, "--version"], timeout=60)
        value = out.strip()
        if value:
            self.version = value
        return self.version

    def update(self):
        if not self.update_cmd:
            return False, "no update channel for %s" % self.source
        rc, out, err = run(self.update_cmd, timeout=600)
        if rc != 0:
            return False, (err or out).strip()[:800]
        self.refresh_version()
        self.updated = True
        return True, self.version


def _exe_update_channel(exe_path):
    """If the exe belongs to a pip install, upgrade through that python."""
    exe = Path(exe_path)
    scripts_dir = exe.parent
    owner = None
    if scripts_dir.name.lower() == "scripts":
        candidate = scripts_dir.parent / "python.exe"
        if candidate.exists():
            owner = str(candidate)
    if owner is None:
        # Python313-style layout: Roaming/Python/Python313/Scripts/yt-dlp.exe
        for candidate in sorted(_glob.glob(str(scripts_dir.parent / "python*.exe"))):
            owner = candidate
            break
    if owner:
        return [owner, "-m", "pip", "install", "-U", "yt-dlp"]
    return [str(exe), "-U"]


def resolve_ytdlp(explicit_exe=None, explicit_python=None):
    """Locate a usable yt-dlp invocation. Returns YtDlpTool or None."""
    # 1. Explicit executable.
    for exe in _unique([explicit_exe, os.environ.get("VTMD_YTDLP"), os.environ.get("YTDLP")]):
        if os.path.isfile(exe):
            version = ""
            rc, out, _ = run([exe, "--version"], timeout=60)
            if rc == 0:
                version = out.strip()
            return YtDlpTool([exe], "exe", version, _exe_update_channel(exe), exe)

    # 2. On PATH.
    for name in ("yt-dlp", "yt-dlp.exe"):
        found = shutil.which(name)
        if found:
            rc, out, _ = run([found, "--version"], timeout=60)
            version = out.strip() if rc == 0 else ""
            return YtDlpTool([found], "exe", version, _exe_update_channel(found), found)

    # 3. pip console scripts under the user roaming python dirs.
    home = Path.home()
    matches = sorted(_glob.glob(str(home / "AppData/Roaming/Python/Python3*/Scripts/yt-dlp.exe")), reverse=True)
    if matches:
        exe = matches[0]
        rc, out, _ = run([exe, "--version"], timeout=60)
        version = out.strip() if rc == 0 else ""
        return YtDlpTool([exe], "exe", version, _exe_update_channel(exe), exe)

    # 4. Importable module in some python.
    for python_cmd in python_candidates(explicit_python):
        version = _module_version(python_cmd)
        if version:
            return YtDlpTool(
                [*python_cmd, "-m", "yt_dlp"],
                "module",
                version,
                [*python_cmd, "-m", "pip", "install", "-U", "yt-dlp"],
                " ".join(python_cmd) + " -m yt_dlp",
            )
    return None


def find_ffmpeg_dir(explicit=None):
    """Return a directory containing ffmpeg, or None."""
    for candidate in _unique([explicit, os.environ.get("VTMD_FFMPEG")]):
        if candidate and Path(candidate).is_dir():
            return candidate
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).parent)
    found = shutil.which("ffmpeg")
    if found:
        return str(Path(found).parent)
    patterns = [
        str(Path.home() / "AppData/Local/Microsoft/WinGet/Packages/*FFmpeg*/ffmpeg-*_full_build/bin"),
        str(Path.home() / "AppData/Local/Microsoft/WinGet/Packages/*FFmpeg*/ffmpeg-*-full_build/bin"),
        "C:/ffmpeg/bin",
        "C:/Program Files/ffmpeg/bin",
        "C:/Program Files/Gyan.FFmpeg/bin",
        "/usr/bin",
        "/usr/local/bin",
    ]
    for pattern in patterns:
        for path in sorted(_glob.glob(pattern), reverse=True):
            if os.path.isfile(os.path.join(path, "ffmpeg.exe")) or os.path.isfile(os.path.join(path, "ffmpeg")):
                return path
    return None


def ensure_ffmpeg(explicit=None, allow_missing=True):
    path = find_ffmpeg_dir(explicit)
    if path is None and not allow_missing:
        raise SystemExit("ffmpeg not found; install ffmpeg or pass --ffmpeg-location")
    return path


# ---------------------------------------------------------------------------
# Receipt helpers
# ---------------------------------------------------------------------------

def scan_media(root):
    """Map of path -> size for media files under root (recursive)."""
    result = {}
    root_path = Path(root)
    if not root_path.exists():
        return result
    for path in root_path.rglob("*"):
        if not path.is_file():
            continue
        if path.name.startswith((".", "_")):
            continue
        if path.suffix.lower() in MEDIA_SUFFIXES:
            try:
                result[str(path)] = path.stat().st_size
            except OSError:
                continue
    return result


def scan_partials(root):
    root_path = Path(root)
    found = []
    if not root_path.exists():
        return found
    for path in root_path.rglob("*"):
        if path.is_file() and path.name.lower().endswith(PARTIAL_SUFFIXES):
            found.append(str(path))
    return found


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        __import__("json").dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(tmp, path)
    return str(path)


def read_json(path):
    import json
    return json.loads(Path(path).read_text(encoding="utf-8"))
