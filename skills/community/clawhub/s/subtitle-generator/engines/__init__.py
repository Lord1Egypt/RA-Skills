"""ASR Engine factory - auto-detects the best available engine."""
import sys
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING


def _get_venv_site_packages(venv_path: Path) -> Path | None:
    """Dynamically find the actual Python version's site-packages in the venv."""
    lib_dir = venv_path / "lib"
    if not lib_dir.exists():
        return None
    for p in lib_dir.iterdir():
        if p.is_dir() and p.name.startswith("python"):
            site = p / "site-packages"
            if site.exists():
                return site
    return None


# Add whisper venv to sys.path (dynamic Python version)
_WHISPER_VENV_PATH = Path.home() / ".whisper-venv"
_WHISPER_VENV_SITE = _get_venv_site_packages(_WHISPER_VENV_PATH)
if _WHISPER_VENV_SITE is not None:
    sys.path.insert(0, str(_WHISPER_VENV_SITE))

from engines.base import ASREngine

# Import engines
try:
    from engines.faster_whisper_engine import FasterWhisperEngine
    _HAS_FASTER_WHISPER = True
except ImportError:
    _HAS_FASTER_WHISPER = False

try:
    from engines.openai_whisper_engine import OpenAIWhisperEngine
    _HAS_OPENAI_WHISPER = True
except ImportError:
    _HAS_OPENAI_WHISPER = False


def _check_venv_packages(pip_path: Path) -> bool:
    """Check if the venv has packages installed by running pip list."""
    try:
        result = subprocess.run(
            [str(pip_path), "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            # If we can parse JSON and get non-empty list, packages are installed
            import json
            packages = json.loads(result.stdout)
            return len(packages) > 0
    except Exception:
        pass
    return False


def ensure_whisper_venv() -> bool:
    """Ensure the whisper venv is set up with required packages.

    1. Checks if ~/.whisper-venv exists and has packages installed
    2. If not, creates it (platform-aware: python3 on macOS/Linux, python on Windows)
    3. Installs packages from requirements.txt
    4. GPU acceleration handled by CTranslate2 (faster-whisper), no PyTorch needed
    5. Returns True on success
    """
    venv_path = Path.home() / ".whisper-venv"
    pip_path = venv_path / "bin" / "pip"
    requirements_path = Path(__file__).parent.parent / "requirements.txt"

    # Step 1: Check if venv exists and has packages
    if venv_path.exists() and pip_path.exists():
        if _check_venv_packages(pip_path):
            print("[Setup] whisper-venv already ready")
            return True
        else:
            print("[Setup] whisper-venv exists but is empty, rebuilding...")

    # Step 2: Create venv — prefer python3 on macOS/Linux, python on Windows
    print("[Setup] Creating venv...")
    try:
        import shutil
        import platform
        system = platform.system()
        # macOS/Linux: python3 first; Windows: python first (py launcher)
        if system == "Windows":
            python_cmd = shutil.which("python") or shutil.which("python3") or "python3"
        else:
            python_cmd = shutil.which("python3") or shutil.which("python") or "python3"
        result = subprocess.run(
            [python_cmd, "-m", "venv", str(venv_path)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create venv: {result.stderr}")
        print(f"[Setup] venv created ({python_cmd}, {system})")
    except Exception as e:
        raise RuntimeError(f"[Setup] Failed to create venv: {e}")

    # Step 3: Install requirements.txt
    print("[Setup] Installing dependencies...")
    try:
        result = subprocess.run(
            [str(pip_path), "install", "-r", str(requirements_path)],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to install requirements: {result.stderr}")
        print("[Setup] Dependencies installed")
    except Exception as e:
        raise RuntimeError(f"[Setup] Failed to install dependencies: {e}")

    # Step 4: faster-whisper uses CTranslate2 (not PyTorch), no GPU CUDA install needed.
    # GPU acceleration is handled automatically by CTranslate2 at runtime.
    print("[Setup] Skipping PyTorch CUDA install (CTranslate2 handles GPU acceleration)")

    # Step 5: Re-import engines to pick up newly installed packages
    print("[Setup] Reloading engine modules...")
    # Remove previously imported engine modules from sys.modules so they re-import
    modules_to_remove = [
        key for key in sys.modules
        if key.startswith("engines.")
    ]
    for mod in modules_to_remove:
        del sys.modules[mod]

    # Re-add venv site-packages to sys.path (dynamic Python version)
    venv_site = _get_venv_site_packages(venv_path)
    if venv_site is not None and str(venv_site) not in sys.path:
        sys.path.insert(0, str(venv_site))

    # Re-execute the imports
    from engines.base import ASREngine  # noqa: re-import

    global _HAS_FASTER_WHISPER, _HAS_OPENAI_WHISPER
    _HAS_FASTER_WHISPER = False
    _HAS_OPENAI_WHISPER = False

    try:
        from engines.faster_whisper_engine import FasterWhisperEngine
        _HAS_FASTER_WHISPER = True
    except ImportError:
        pass

    try:
        from engines.openai_whisper_engine import OpenAIWhisperEngine
        _HAS_OPENAI_WHISPER = True
    except ImportError:
        pass

    print("[Setup] Engine modules reloaded")
    return True


def create_engine() -> ASREngine:
    """Factory function that auto-detects and returns the best available ASR engine.

    Priority:
        1. faster-whisper (faster, preferred)
        2. openai-whisper (fallback)
        3. Auto-setup whisper-venv and retry if no engine found
    """
    if _HAS_FASTER_WHISPER:
        print("[Engine] Using: Faster-Whisper (preferred)")
        return FasterWhisperEngine()

    if _HAS_OPENAI_WHISPER:
        print("[Engine] Using: OpenAI Whisper (fallback)")
        return OpenAIWhisperEngine()

    # No engine found — try auto-setup
    setup_error = None
    try:
        ensure_whisper_venv()
    except RuntimeError as e:
        setup_error = str(e)

    # Re-check after setup attempt
    if _HAS_FASTER_WHISPER:
        print("[Engine] Using: Faster-Whisper (preferred)")
        return FasterWhisperEngine()

    if _HAS_OPENAI_WHISPER:
        print("[Engine] Using: OpenAI Whisper (fallback)")
        return OpenAIWhisperEngine()

    # Still no engine — raise with setup error details
    base_msg = (
        "No ASR engine available. Install one of:\n"
        "  pip install faster-whisper  (preferred, faster)\n"
        "  pip install openai-whisper  (fallback)"
    )
    if setup_error:
        raise RuntimeError(f"{base_msg}\n\n[Setup] Auto-setup failed:\n{setup_error}")
    raise RuntimeError(base_msg)
