"""videoarm-doctor: Check all VideoARM dependencies and environment."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def _check_python() -> dict:
    v = sys.version_info
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    ok = (v.major, v.minor) >= (3, 10)
    result = {"name": "Python", "version": version_str, "ok": ok}
    if not ok:
        result["hint"] = f"Python 3.10+ required, found {version_str}"
    return result


def _check_ffmpeg() -> dict:
    try:
        proc = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True, text=True, timeout=10,
        )
        # First line: "ffmpeg version X.Y.Z ..."
        first_line = proc.stdout.splitlines()[0] if proc.stdout else ""
        parts = first_line.split()
        version_str = parts[2] if len(parts) >= 3 else "unknown"
        return {"name": "ffmpeg", "version": version_str, "ok": True}
    except FileNotFoundError:
        return {
            "name": "ffmpeg",
            "version": None,
            "ok": False,
            "hint": "ffmpeg not found. Install: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)",
        }
    except Exception as e:
        return {"name": "ffmpeg", "version": None, "ok": False, "hint": str(e)}


def _check_ytdlp() -> dict:
    try:
        proc = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        version_str = proc.stdout.strip()
        return {"name": "yt-dlp", "version": version_str, "ok": True, "optional": True}
    except FileNotFoundError:
        return {
            "name": "yt-dlp",
            "version": None,
            "ok": False,
            "optional": True,
            "hint": "yt-dlp not found (optional, needed for YouTube download). Install: pip install yt-dlp",
        }
    except Exception as e:
        return {"name": "yt-dlp", "version": None, "ok": False, "optional": True, "hint": str(e)}


def _check_python_package(import_name: str, display_name: str, install_hint: str) -> dict:
    try:
        mod = __import__(import_name)
        version_str = getattr(mod, "__version__", "installed")
        return {"name": display_name, "version": version_str, "ok": True}
    except ImportError:
        return {
            "name": display_name,
            "version": None,
            "ok": False,
            "hint": f"{display_name} not found. Install: {install_hint}",
        }


def _check_whisper_model() -> dict:
    """Check if any faster-whisper model has been downloaded."""
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    model_name = os.environ.get("WHISPER_MODEL", "base")

    # faster-whisper models are stored as Systran/faster-whisper-* directories
    if cache_dir.exists():
        candidates = list(cache_dir.glob("models--Systran--faster-whisper-*"))
        if candidates:
            # Find the specific model if possible
            target = f"models--Systran--faster-whisper-{model_name}"
            matched = [c for c in candidates if c.name == target]
            model_dir = matched[0] if matched else candidates[0]
            found_name = model_dir.name.replace("models--Systran--faster-whisper-", "")
            return {
                "name": "Whisper model",
                "version": found_name,
                "ok": True,
            }

    return {
        "name": "Whisper model",
        "version": None,
        "ok": False,
        "optional": True,
        "hint": "Whisper model not downloaded (run: videoarm-setup-whisper)",
    }


def run_checks() -> list:
    checks = [
        _check_python(),
        _check_ffmpeg(),
        _check_ytdlp(),
        _check_python_package("cv2", "opencv-python", "pip install opencv-python"),
        _check_python_package("faster_whisper", "faster-whisper", "pip install faster-whisper"),
        _check_python_package("numpy", "numpy", "pip install numpy"),
        _check_whisper_model(),
    ]
    return checks


def _format_human(checks: list) -> str:
    lines = ["VideoARM Doctor 🩺", "──────────────────"]
    passed = 0
    total = len(checks)

    for c in checks:
        icon = "✅" if c["ok"] else ("⚠️ " if c.get("optional") else "❌")
        name = c["name"]
        version = c.get("version")
        if c["ok"] and version:
            lines.append(f"{icon} {name} {version}")
        elif c["ok"]:
            lines.append(f"{icon} {name}")
        else:
            hint = c.get("hint", f"{name} not found")
            lines.append(f"{icon} {hint}")

        if c["ok"]:
            passed += 1

    lines.append("")
    # Count only required checks (non-optional) for the summary
    required = [c for c in checks if not c.get("optional")]
    required_passed = sum(1 for c in required if c["ok"])
    optional_failed = [c for c in checks if c.get("optional") and not c["ok"]]

    if required_passed == len(required):
        if optional_failed:
            lines.append(f"All required checks passed ({required_passed}/{len(required)}), "
                         f"{len(optional_failed)} optional item(s) missing")
        else:
            lines.append(f"All checks passed ({passed}/{total})")
    else:
        lines.append(f"Some checks failed ({passed}/{total} passed)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check VideoARM dependencies")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    checks = run_checks()

    if args.json:
        passed = sum(1 for c in checks if c["ok"])
        output = {
            "checks": checks,
            "summary": {
                "total": len(checks),
                "passed": passed,
                "failed": len(checks) - passed,
                "all_required_ok": all(c["ok"] for c in checks if not c.get("optional")),
            },
        }
        json.dump(output, sys.stdout, indent=2)
        print()
    else:
        print(_format_human(checks))

    # Exit non-zero if any required check failed
    if not all(c["ok"] for c in checks if not c.get("optional")):
        sys.exit(1)


if __name__ == "__main__":
    main()
