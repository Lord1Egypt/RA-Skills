#!/usr/bin/env python3
"""
One-click installer for Voice Recognition skill.
Creates a virtual environment and installs all dependencies.
"""
import subprocess
import sys
import os


def main():
    print("=" * 55)
    print("  🎤 Voice Recognition Skill — Installer")
    print("=" * 55)
    print()

    # Check Python version
    py_version = sys.version_info
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
        print("❌ Python 3.8+ required. Found:", sys.version)
        sys.exit(1)
    print(f"✓ Python {py_version.major}.{py_version.minor}.{py_version.micro}")

    # Create virtual environment
    venv_dir = os.path.join(os.path.dirname(__file__), '..', '.venv')
    if not os.path.exists(venv_dir):
        print(f"📦 Creating virtual environment...")
        try:
            import venv
            venv.main(['--without-pip', venv_dir])
            # Manually install pip
            subprocess.run(
                [sys.executable, '-m', 'ensurepip', '--upgrade', '--default-pip'],
                cwd=venv_dir, capture_output=True
            )
        except Exception:
            # Fallback: use --break-system-packages
            print("⚠️  Could not create venv. Falling back to system pip.")
            venv_dir = None
    else:
        print(f"✓ Virtual environment exists")

    if venv_dir:
        pip_path = os.path.join(venv_dir, 'bin', 'pip')
        python_path = os.path.join(venv_dir, 'bin', 'python')
    else:
        pip_path = 'pip3'
        python_path = 'python3'

    # Install dependencies
    print("📥 Installing dependencies (this may take a few minutes)...")
    print("   • openai-whisper (speech recognition)")
    print("   • torch (deep learning engine)")
    print("   • soundfile (audio processing)")
    print()

    packages = [
        'openai-whisper',
        'soundfile',
        'numpy',
    ]

    for pkg in packages:
        print(f"  → Installing {pkg}...")
        result = subprocess.run(
            [pip_path, 'install', pkg],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ⚠️  pip failed, trying with --break-system-packages...")
            result = subprocess.run(
                [pip_path, 'install', '--break-system-packages', pkg],
                capture_output=True, text=True
            )

    # Install PyTorch (CPU)
    print(f"  → Installing torch (CPU)...")
    result = subprocess.run(
        [pip_path, 'install', 'torch', '--index-url', 'https://download.pytorch.org/whl/cpu'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  Retrying torch install...")
        result = subprocess.run(
            [pip_path, 'install', '--break-system-packages', 'torch',
             '--index-url', 'https://download.pytorch.org/whl/cpu'],
            capture_output=True, text=True
        )

    print()
    print("=" * 55)
    print("  ✅ Installation complete!")
    print()
    if venv_dir:
        print(f"  Virtual environment: {venv_dir}")
        print(f"  Activate: source {venv_dir}/bin/activate")
    print()
    print("  Try it:")
    print(f"    {python_path} scripts/transcribe.py your_audio.ogg")
    print("=" * 55)


if __name__ == "__main__":
    main()
