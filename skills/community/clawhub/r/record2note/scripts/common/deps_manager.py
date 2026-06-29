#!/usr/bin/env python3
"""Dependency manager for record2note. Handles detection, download, and mirror switching."""
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
import urllib.error
import zipfile

WHISPER_RELEASE_BASE = "https://github.com/ggml-org/whisper.cpp/releases/download/v1.8.4"

WHISPER_BINARIES = {
    "macos-arm64": {
        "method": "brew_or_build",
        "formula": "whisper-cpp",
        "build_repo": "ggerganov/whisper.cpp",
        "build_tag": "v1.8.4",
        "name": "whisper-cli",
    },
    "macos-x86_64": {
        "method": "brew_or_build",
        "formula": "whisper-cpp",
        "build_repo": "ggerganov/whisper.cpp",
        "build_tag": "v1.8.4",
        "name": "whisper-cli",
    },
    "windows-amd64": {
        "method": "download",
        "zip_url": f"{WHISPER_RELEASE_BASE}/whisper-bin-x64.zip",
        "zip_name": "whisper-bin-x64.zip",
        "binary_in_zip": "Release/whisper-cli.exe",
        "name": "whisper-cli.exe",
    },
}

WHISPER_MODELS = {
    "ggml-base.bin": {
        "url": "ggerganov/whisper.cpp/resolve/main/ggml-base.bin",
        "size_hint": "148MB",
    },
    "ggml-medium.bin": {
        "url": "ggerganov/whisper.cpp/resolve/main/ggml-medium.bin",
        "size_hint": "1.5GB",
    },
    "ggml-large-v3.bin": {
        "url": "ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin",
        "size_hint": "3GB",
    },
}

SILERO_VAD = {
    "url": "ggerganov/whisper-vad/resolve/main/ggml-silero-v6.2.0.bin",
    "size_hint": "864KB",
}

MIRRORS = {
    "intl": {
        "huggingface": "https://huggingface.co",
        "github": "https://github.com",
    },
    "cn": {
        "huggingface": "https://hf-mirror.com",
        "github": "https://ghfast.top",
    },
}

BIN_DIR = os.path.expanduser("~/.config/record2note/bin")

EXTRA_PATHS = [BIN_DIR, "/opt/local/bin", "/opt/homebrew/bin", "/usr/local/bin"]


def _which(name):
    paths = os.environ.get("PATH", "").split(os.pathsep)
    paths = paths + EXTRA_PATHS
    for d in paths:
        candidate = os.path.join(d, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return shutil.which(name)


def _which_any(names):
    for name in names:
        found = _which(name)
        if found:
            return found
    return None


def get_progress_mode():
    if os.environ.get("RECORD2NOTE_PROGRESS") in ("agent", "markdown"):
        return "agent"
    if sys.stdout.isatty():
        return "terminal"
    return "agent"


def format_bar(pct, width=20):
    filled = int(width * pct / 100)
    return f"[{'█' * filled}{'░' * (width - filled)}]"


def get_platform_key():
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "darwin":
        if machine == "arm64":
            return "macos-arm64"
        return "macos-x86_64"
    elif system == "windows":
        return "windows-amd64"
    return "linux-amd64"


def get_config_path():
    skill_dir = os.environ.get(
        "SKILL_DIR",
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    return os.path.join(skill_dir, "config.json")


def load_config():
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config):
    config_path = get_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def resolve_mirror(config):
    mirror_pref = config.get("mirror", "auto")
    if mirror_pref in ("cn", "intl"):
        return MIRRORS[mirror_pref]

    try:
        req = urllib.request.Request("https://huggingface.co", method="HEAD")
        urllib.request.urlopen(req, timeout=5)
        return MIRRORS["intl"]
    except Exception:
        return MIRRORS["cn"]


def build_hf_url(model_path, mirror_config):
    base = mirror_config["huggingface"].rstrip("/")
    return f"{base}/{model_path}"


def build_github_url(url, mirror_config):
    base = mirror_config["github"]
    if "ghfast.top" in base:
        return f"{base}/{url}"
    return url


def download_with_progress(url, dest_path, desc=None):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if desc is None:
        desc = os.path.basename(dest_path)

    progress_mode = get_progress_mode()

    existing_size = 0
    if os.path.exists(dest_path):
        existing_size = os.path.getsize(dest_path)

    headers = {}
    if existing_size > 0:
        headers["Range"] = f"bytes={existing_size}-"

    req = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(req, timeout=300)
    except urllib.error.HTTPError as e:
        if e.code == 416:
            print(f"[record2note] Already fully downloaded: {desc}")
            return True
        if e.code == 404:
            print(f"[record2note] Error: Download not found (404): {url}", file=sys.stderr)
            return False
        raise

    total = response.headers.get("Content-Length")
    if total:
        total = int(total) + existing_size
    mode = "ab" if existing_size > 0 and response.status == 206 else "wb"
    if response.status == 200 and existing_size > 0:
        mode = "wb"
        existing_size = 0

    downloaded = existing_size
    chunk_size = 65536

    if progress_mode == "agent":
        if existing_size > 0 and total:
            resume_pct = existing_size * 100 // total
            mb_existing = existing_size / (1024 * 1024)
            print(f"[record2note] Resuming {desc} from {mb_existing:.1f}MB ({resume_pct}% already downloaded)")
        last_pct = -5
        with open(dest_path, mode) as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    if pct - last_pct >= 5 or pct == 100:
                        mb_done = downloaded / (1024 * 1024)
                        mb_total = total / (1024 * 1024)
                        bar = format_bar(pct)
                        print(f"[record2note] Downloading {desc}: {bar} {pct}% ({mb_done:.1f}/{mb_total:.1f}MB)", flush=True)
                        last_pct = pct
                else:
                    mb_done = downloaded / (1024 * 1024)
                    if downloaded - (downloaded - len(chunk)) >= 5 * 1024 * 1024 or downloaded == 0:
                        print(f"[record2note] Downloading {desc}: {mb_done:.1f}MB downloaded", flush=True)
        if total:
            mb_done = downloaded / (1024 * 1024)
            mb_total = total / (1024 * 1024)
            pct = downloaded * 100 // total
            if pct - last_pct < 5:
                bar = format_bar(pct)
                print(f"[record2note] Downloading {desc}: {bar} {pct}% ({mb_done:.1f}/{mb_total:.1f}MB)", flush=True)
    else:
        with open(dest_path, mode) as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    mb_done = downloaded / (1024 * 1024)
                    mb_total = total / (1024 * 1024)
                    print(f"\r[record2note] Downloading {desc}: {pct}% ({mb_done:.1f}/{mb_total:.1f}MB)", end="", flush=True)
                else:
                    mb_done = downloaded / (1024 * 1024)
                    print(f"\r[record2note] Downloading {desc}: {mb_done:.1f}MB", end="", flush=True)
        print()

    return True


def cmd_check():
    config = load_config()
    mirror_config = resolve_mirror(config)
    plat = get_platform_key()
    issues = []

    whisper_bin = config.get("whisper_binary", "whisper-cli")
    whisper_model_path = os.path.expanduser(config.get("whisper_model_path", "/usr/local/share/whisper-models"))
    whisper_model = config.get("whisper_model", "ggml-base.bin")

    if _which(whisper_bin):
        print(f"  [OK] whisper binary: {_which(whisper_bin)}")
    elif os.path.exists(os.path.join(BIN_DIR, WHISPER_BINARIES.get(plat, {}).get("name", "whisper-cli"))):
        print(f"  [OK] whisper binary (local): {BIN_DIR}")
    else:
        print(f"  [MISSING] whisper binary: {whisper_bin}")
        issues.append("whisper binary")

    model_file = os.path.join(whisper_model_path, whisper_model)
    if os.path.exists(model_file):
        size_mb = os.path.getsize(model_file) / (1024 * 1024)
        print(f"  [OK] whisper model: {model_file} ({size_mb:.1f}MB)")
    else:
        size_hint = WHISPER_MODELS.get(whisper_model, {}).get("size_hint", "?")
        print(f"  [MISSING] whisper model: {model_file} ({size_hint})")
        issues.append(f"whisper model ({size_hint})")

    if _which("ffmpeg") and _which("ffprobe"):
        print("  [OK] ffmpeg + ffprobe")
    elif _which_any([f"ffmpeg{v}" for v in range(10, 0, -1)]) and _which_any([f"ffprobe{v}" for v in range(10, 0, -1)]):
        ff_ver = _which_any([f"ffmpeg{v}" for v in range(10, 0, -1)])
        fp_ver = _which_any([f"ffprobe{v}" for v in range(10, 0, -1)])
        print(f"  [OK] ffmpeg + ffprobe (versioned: {os.path.basename(ff_ver)}, {os.path.basename(fp_ver)})")
        print("  [INFO] Run 'deps_manager.py ensure L1' to create ffmpeg/ffprobe symlinks")
    else:
        print("  [MISSING] ffmpeg or ffprobe")
        issues.append("ffmpeg")

    if _which("python3") or _which("python"):
        print("  [OK] python3")
    else:
        print("  [MISSING] python3")
        issues.append("python3")

    if config.get("vad", False):
        vad_path = os.path.expanduser(
            config.get("vad_model_path", os.path.join(whisper_model_path, "ggml-silero-v6.2.0.bin"))
        )
        if os.path.exists(vad_path):
            print(f"  [OK] Silero-VAD model: {vad_path}")
        else:
            print(f"  [MISSING] Silero-VAD model ({SILERO_VAD['size_hint']})")
            issues.append("vad model")

    if config.get("diarization", True):
        try:
            subprocess.run(
                ["python3", "-c", "import pyannote.audio"],
                capture_output=True, check=True, timeout=10
            )
            print("  [OK] pyannote-audio")
        except Exception:
            print("  [MISSING] pyannote-audio (pip install pyannote-audio torch)")
            issues.append("pyannote-audio")

    if platform.system() == "Darwin":
        if _which("fswatch"):
            print("  [OK] fswatch")
        else:
            print("  [MISSING] fswatch (brew install fswatch)")
            issues.append("fswatch")

    mirror_name = "CN mirror" if "hf-mirror" in mirror_config["huggingface"] else "International"
    print(f"\n  Mirror: {mirror_name} ({mirror_config['huggingface']})")

    if issues:
        print(f"\n  Missing dependencies: {', '.join(issues)}")
        return 1
    print("\n  All dependencies satisfied.")
    return 0


def _find_pkg_manager():
    for cmd, path in [("brew", "/opt/homebrew/bin/brew"), ("port", "/opt/local/bin/port")]:
        found = _which(cmd)
        if found:
            return cmd, found
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return cmd, path
    return None, None


def _install_whisper_brew(formula, bin_name, config):
    brew = _which("brew") or "/opt/homebrew/bin/brew"
    if not os.path.isfile(brew):
        return False
    print(f"[record2note] Installing {formula} via Homebrew...")
    print("[record2note] (This may take several minutes on first install)")
    result = subprocess.run([brew, "install", formula], check=False,
                           timeout=600)
    if result.returncode != 0:
        print(f"[record2note] brew install {formula} failed.", file=sys.stderr)
        return False
    found = _which(bin_name)
    if found:
        config["whisper_binary"] = found
        save_config(config)
        print(f"[record2note] {bin_name} installed: {found}")
        return True
    return False


def _install_whisper_build(repo, tag, bin_name, config):
    print(f"[record2note] Building whisper.cpp from source ({tag})...")
    print("[record2note] (Requires git, cmake, and a C/C++ compiler)")

    mirror_config = resolve_mirror(config)
    git_binary = _which("git")
    cmake_binary = _which("cmake")
    if _which("cc") or _which("gcc"):
        pass
    elif _which("clang"):
        pass
    else:
        print("[record2note] Error: No C compiler found.", file=sys.stderr)
        return False

    if not git_binary:
        print("[record2note] Error: git not found. Install git to build from source.", file=sys.stderr)
        return False

    if not cmake_binary:
        print("[record2note] cmake not found, installing via pip...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "cmake"],
            check=False, timeout=120
        )
        cmake_binary = _which("cmake")
        if not cmake_binary:
            cmake_binary = os.path.join(
                os.path.dirname(sys.executable), "cmake"
            )
        if result.returncode != 0 and not os.path.exists(cmake_binary):
            print("[record2note] Error: Failed to install cmake.", file=sys.stderr)
            return False

    import tempfile
    build_dir = tempfile.mkdtemp(prefix="whisper-build-")
    try:
        repo_url = build_github_url(f"https://github.com/{repo}", mirror_config)
        print(f"[record2note] Cloning {repo}...")
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", tag, repo_url, build_dir],
            check=False, timeout=300
        )
        if result.returncode != 0:
            print("[record2note] Error: git clone failed.", file=sys.stderr)
            return False

        cmake_build_dir = os.path.join(build_dir, "build")
        os.makedirs(cmake_build_dir, exist_ok=True)
        print("[record2note] Configuring build...")
        result = subprocess.run(
            [cmake_binary, "..", "-DCMAKE_BUILD_TYPE=Release",
             "-DWHISPER_BUILD_EXAMPLES=ON"],
            cwd=cmake_build_dir, check=False, timeout=120
        )
        if result.returncode != 0:
            print("[record2note] Error: cmake configuration failed.", file=sys.stderr)
            return False

        print("[record2note] Building whisper-cli (this may take a few minutes)...")
        cpu_count = os.cpu_count() or 2
        result = subprocess.run(
            ["make", f"-j{cpu_count}", "whisper-cli"],
            cwd=cmake_build_dir, check=False, timeout=600
        )
        if result.returncode != 0:
            print("[record2note] Error: Build failed.", file=sys.stderr)
            return False

        possible = [
            os.path.join(cmake_build_dir, "bin", bin_name),
            os.path.join(cmake_build_dir, bin_name),
        ]
        built = None
        for p in possible:
            if os.path.exists(p):
                built = p
                break
        if not built:
            print(f"[record2note] Error: Built binary not found.", file=sys.stderr)
            return False

        os.makedirs(BIN_DIR, exist_ok=True)
        dest = os.path.join(BIN_DIR, bin_name)
        shutil.copy2(built, dest)
        os.chmod(dest, 0o755)
        config["whisper_binary"] = dest
        save_config(config)
        print(f"[record2note] whisper-cli built and installed to {dest}")
        return True
    except subprocess.TimeoutExpired:
        print("[record2note] Error: Build timed out.", file=sys.stderr)
        return False
    finally:
        shutil.rmtree(build_dir, ignore_errors=True)


def cmd_install_whisper():
    config = load_config()
    plat = get_platform_key()

    if plat not in WHISPER_BINARIES:
        print(f"[record2note] Error: No pre-compiled whisper binary for platform '{plat}'.", file=sys.stderr)
        print("[record2note] Please install whisper.cpp manually: https://github.com/ggerganov/whisper.cpp", file=sys.stderr)
        return 1

    info = WHISPER_BINARIES[plat]
    method = info.get("method", "download")
    bin_name = info["name"]

    existing = _which(bin_name)
    if existing:
        print(f"[record2note] {bin_name} already installed: {existing}")
        config["whisper_binary"] = existing
        save_config(config)
        return 0

    local_bin = os.path.join(BIN_DIR, bin_name)
    if os.path.exists(local_bin):
        print(f"[record2note] {bin_name} already installed: {local_bin}")
        config["whisper_binary"] = local_bin
        save_config(config)
        return 0

    if method == "brew_or_build":
        if _install_whisper_brew(info["formula"], bin_name, config):
            return 0
        print("[record2note] brew install failed or unavailable, trying build from source...")
        if _install_whisper_build(info["build_repo"], info["build_tag"], bin_name, config):
            return 0
        print("[record2note] All installation methods failed.", file=sys.stderr)
        print("[record2note] Please install whisper.cpp manually: https://github.com/ggerganov/whisper.cpp", file=sys.stderr)
        return 1

    if method == "brew":
        if _install_whisper_brew(info["formula"], bin_name, config):
            return 0
        print(f"[record2note] Error: brew install {info['formula']} failed.", file=sys.stderr)
        print("[record2note] You can try building from source: https://github.com/ggerganov/whisper.cpp", file=sys.stderr)
        return 1

    mirror_config = resolve_mirror(config)
    dest = os.path.join(BIN_DIR, info["name"])

    print(f"[record2note] Downloading whisper binary for {plat}...")
    print(f"[record2note] Estimated size: ~4MB (compressed)")
    zip_url = build_github_url(info["zip_url"], mirror_config)
    zip_path = os.path.join(BIN_DIR, info["zip_name"])
    if not download_with_progress(zip_url, zip_path):
        print("[record2note] Failed to download whisper binary.", file=sys.stderr)
        return 1
    print(f"[record2note] Extracting whisper binary from {info['zip_name']}...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            candidates = [n for n in zf.namelist() if n.endswith(info["name"])]
            if not candidates:
                all_names = zf.namelist()
                print(f"[record2note] Error: '{info['name']}' not found in zip. Contents:", file=sys.stderr)
                for n in all_names[:20]:
                    print(f"  {n}", file=sys.stderr)
                os.remove(zip_path)
                return 1
            extracted = candidates[0]
            with zf.open(extracted) as src, open(dest, "wb") as dst:
                shutil.copyfileobj(src, dst)
    except zipfile.BadZipFile:
        print("[record2note] Error: Downloaded file is not a valid zip.", file=sys.stderr)
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return 1
    os.remove(zip_path)
    os.chmod(dest, 0o755)

    config["whisper_binary"] = dest
    save_config(config)
    print(f"[record2note] whisper binary installed to {dest}")
    print("[record2note] Config updated.")
    return 0


def cmd_download_model(model_name=None):
    config = load_config()
    mirror_config = resolve_mirror(config)
    whisper_model_path = os.path.expanduser(
        config.get("whisper_model_path", "/usr/local/share/whisper-models")
    )

    if model_name is None:
        model_name = config.get("whisper_model", "ggml-base.bin")

    if model_name not in WHISPER_MODELS:
        print(f"[record2note] Error: Unknown model '{model_name}'.", file=sys.stderr)
        print(f"[record2note] Available models: {', '.join(WHISPER_MODELS.keys())}", file=sys.stderr)
        return 1

    info = WHISPER_MODELS[model_name]
    dest = os.path.join(whisper_model_path, model_name)
    url = build_hf_url(info["url"], mirror_config)

    if os.path.exists(dest):
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"[record2note] Model already exists: {dest} ({size_mb:.1f}MB)")
        print("[record2note] Delete it and re-run to re-download.")
        return 0

    print(f"[record2note] Downloading {model_name} (~{info['size_hint']})...")
    print(f"[record2note] Estimated time: varies by network speed")
    if not download_with_progress(url, dest):
        print(f"[record2note] Failed to download {model_name}.", file=sys.stderr)
        return 1

    print(f"[record2note] Model downloaded to {dest}")
    return 0


def cmd_download_vad():
    config = load_config()
    mirror_config = resolve_mirror(config)
    whisper_model_path = os.path.expanduser(
        config.get("whisper_model_path", "/usr/local/share/whisper-models")
    )
    vad_path = os.path.expanduser(
        config.get("vad_model_path", os.path.join(whisper_model_path, "ggml-silero-v6.2.0.bin"))
    )

    if os.path.exists(vad_path):
        print(f"[record2note] VAD model already exists: {vad_path}")
        return 0

    url = build_hf_url(SILERO_VAD["url"], mirror_config)
    print(f"[record2note] Downloading Silero-VAD model (~{SILERO_VAD['size_hint']})...")
    if not download_with_progress(url, vad_path):
        print("[record2note] Failed to download VAD model.", file=sys.stderr)
        return 1

    print(f"[record2note] VAD model downloaded to {vad_path}")
    return 0


def _install_ffmpeg_port(port_path):
    print("[record2note] Installing ffmpeg via MacPorts...")
    print("[record2note] (This may require sudo and take several minutes)")
    result = subprocess.run([port_path, "install", "ffmpeg"], check=False, timeout=600)
    if result.returncode != 0:
        print("[record2note] Error: port install ffmpeg failed.", file=sys.stderr)
        return 1
    ff = _which("ffmpeg")
    fp = _which("ffprobe")
    if ff and fp:
        print("[record2note] ffmpeg + ffprobe installed successfully.")
        return 0
    print("[record2note] Error: ffmpeg not found after port install.", file=sys.stderr)
    return 1


def cmd_install_ffmpeg():
    system = platform.system()
    if system == "Darwin":
        pkg_mgr, pkg_path = _find_pkg_manager()
        if pkg_mgr == "brew":
            print("[record2note] Installing ffmpeg via Homebrew...")
            print("[record2note] (This may take several minutes on first install)")
            result = subprocess.run([pkg_path, "install", "ffmpeg"], check=False, timeout=600)
            if result.returncode != 0:
                print("[record2note] brew install ffmpeg failed, trying MacPorts...", file=sys.stderr)
                port_path = _which("port") or "/opt/local/bin/port"
                if os.path.isfile(port_path):
                    return _install_ffmpeg_port(port_path)
                print("[record2note] Error: All package managers failed.", file=sys.stderr)
                print("[record2note] Install manually: brew install ffmpeg or sudo port install ffmpeg", file=sys.stderr)
                return 1
        elif pkg_mgr == "port":
            return _install_ffmpeg_port(pkg_path)
        else:
            print("[record2note] No package manager found (Homebrew or MacPorts).", file=sys.stderr)
            print("[record2note] Install Homebrew: https://brew.sh", file=sys.stderr)
            print("[record2note] Or MacPorts: https://macports.org", file=sys.stderr)
            return 1

        if _which("ffmpeg") and _which("ffprobe"):
            print("[record2note] ffmpeg + ffprobe installed successfully.")
            return 0
        print("[record2note] Error: ffmpeg not found after install.", file=sys.stderr)
        return 1
    elif system == "Windows":
        choco = _which("choco")
        if choco:
            print("[record2note] Installing ffmpeg via Chocolatey...")
            result = subprocess.run([choco, "install", "ffmpeg", "-y"], check=False, timeout=600)
            if result.returncode == 0 and _which("ffmpeg"):
                print("[record2note] ffmpeg installed successfully.")
                return 0
        print("[record2note] Error: Could not auto-install ffmpeg.", file=sys.stderr)
        print("[record2note] Install manually: choco install ffmpeg (or download from https://ffmpeg.org)", file=sys.stderr)
        return 1
    else:
        print("[record2note] Error: Auto-install not supported on Linux.", file=sys.stderr)
        print("[record2note] Install via your package manager, e.g.: sudo apt install ffmpeg", file=sys.stderr)
        return 1


def _ensure_ffmpeg_symlinks():
    ffmpeg_path = _which("ffmpeg")
    ffprobe_path = _which("ffprobe")
    os.makedirs(BIN_DIR, exist_ok=True)
    linked = []

    if not ffmpeg_path:
        versioned = _which_any([f"ffmpeg{v}" for v in range(10, 0, -1)])
        if versioned:
            link = os.path.join(BIN_DIR, "ffmpeg")
            if not os.path.exists(link):
                os.symlink(versioned, link)
                linked.append(f"ffmpeg -> {versioned}")
            ffmpeg_path = link

    if not ffprobe_path:
        versioned = _which_any([f"ffprobe{v}" for v in range(10, 0, -1)])
        if versioned:
            link = os.path.join(BIN_DIR, "ffprobe")
            if not os.path.exists(link):
                os.symlink(versioned, link)
                linked.append(f"ffprobe -> {versioned}")
            ffprobe_path = link

    if linked:
        print(f"[record2note] Created symlinks: {', '.join(linked)}")

    return ffmpeg_path is not None and ffprobe_path is not None


def cmd_ensure(tier):
    config = load_config()
    errors = []

    if tier in ("L1", "1"):
        whisper_bin = config.get("whisper_binary", "whisper-cli")
        if not _which(whisper_bin):
            bin_name = WHISPER_BINARIES.get(get_platform_key(), {}).get("name", "whisper-cli")
            local_bin = os.path.join(BIN_DIR, bin_name)
            if os.path.exists(local_bin):
                config["whisper_binary"] = local_bin
                save_config(config)
                print(f"[record2note] Using local whisper binary: {local_bin}")
            else:
                print("[record2note] whisper binary not found, downloading...")
                ret = cmd_install_whisper()
                if ret != 0:
                    errors.append("whisper binary")
                    config = load_config()

        whisper_model_path = os.path.expanduser(
            config.get("whisper_model_path", "/usr/local/share/whisper-models")
        )
        whisper_model = config.get("whisper_model", "ggml-base.bin")
        model_file = os.path.join(whisper_model_path, whisper_model)
        if not os.path.exists(model_file):
            print(f"[record2note] Model not found: {model_file}, downloading...")
            ret = cmd_download_model(whisper_model)
            if ret != 0:
                errors.append(f"whisper model ({whisper_model})")

        if not _which("ffmpeg") or not _which("ffprobe"):
            if not _ensure_ffmpeg_symlinks():
                print("[record2note] ffmpeg not found, attempting auto-install...")
                ret = cmd_install_ffmpeg()
                if ret != 0:
                    _ensure_ffmpeg_symlinks()
                    if not _which("ffmpeg") or not _which("ffprobe"):
                        errors.append("ffmpeg")

        if platform.system() == "Darwin" and not _which("fswatch"):
            errors.append("fswatch")

    if tier in ("L3", "3"):
        try:
            subprocess.run(
                ["python3", "-c", "import pyannote.audio"],
                capture_output=True, check=True, timeout=10
            )
        except Exception:
            print("[record2note] pyannote-audio not found. Installing...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pyannote-audio", "torch"],
                check=False
            )
            try:
                subprocess.run(
                    ["python3", "-c", "import pyannote.audio"],
                    capture_output=True, check=True, timeout=10
                )
            except Exception:
                errors.append("pyannote-audio")
                print("[record2note] Warning: pyannote installation failed.", file=sys.stderr)
                print("[record2note] You may need: pip install pyannote-audio torch", file=sys.stderr)
                print("[record2note] And: huggingface-cli login", file=sys.stderr)

    if config.get("vad", False) and tier in ("L1", "1"):
        cmd_download_vad()

    if errors:
        print(f"[record2note] Missing dependencies: {', '.join(errors)}", file=sys.stderr)
        return 1
    print("[record2note] All required dependencies are ready.")
    return 0


def cmd_mirror():
    config = load_config()
    mirror_config = resolve_mirror(config)
    if "hf-mirror" in mirror_config["huggingface"]:
        detected = "cn"
    else:
        detected = "intl"
    print(f"Detected: {detected}")
    print(f"huggingface: {mirror_config['huggingface']}")
    print(f"github: {mirror_config['github']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: deps_manager.py <command> [args]", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  check              Check all dependency status", file=sys.stderr)
        print("  ensure L1|L3        Ensure tier dependencies", file=sys.stderr)
        print("  install-whisper     Install whisper binary (brew/build/download)", file=sys.stderr)
        print("  install-ffmpeg      Install ffmpeg via package manager", file=sys.stderr)
        print("  download-model [n]  Download whisper model (default: from config)", file=sys.stderr)
        print("  download-vad        Download Silero-VAD model", file=sys.stderr)
        print("  mirror              Auto-detect best mirror", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "check":
        sys.exit(cmd_check())
    elif cmd == "ensure":
        tier = sys.argv[2] if len(sys.argv) > 2 else "L1"
        sys.exit(cmd_ensure(tier))
    elif cmd == "install-whisper":
        sys.exit(cmd_install_whisper())
    elif cmd == "install-ffmpeg":
        sys.exit(cmd_install_ffmpeg())
    elif cmd == "download-model":
        model = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(cmd_download_model(model))
    elif cmd == "download-vad":
        sys.exit(cmd_download_vad())
    elif cmd == "mirror":
        cmd_mirror()
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)