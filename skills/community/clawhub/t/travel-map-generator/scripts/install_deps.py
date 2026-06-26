#!/usr/bin/env python3
"""Install required dependencies for travel-map-generator skill."""

import subprocess
import sys


def check_and_install():
    """Check if Pillow is available, install if missing."""
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
        print(f"✓ Pillow is already installed (version {Image.__version__})")
        return 0
    except ImportError:
        print("→ Pillow not found. Installing...")

    # Try installation methods in order of preference
    install_methods = [
        [sys.executable, "-m", "pip", "install", "--user", "Pillow"],
        [sys.executable, "-m", "pip", "install", "Pillow"],
        [sys.executable, "-m", "pip3", "install", "Pillow"],
    ]

    for i, cmd in enumerate(install_methods):
        try:
            print(f"  Attempt {i+1}/{len(install_methods)}: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode == 0:
                break
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"    Failed: {e}")
            continue
    else:
        print("✗ All installation attempts failed.", file=sys.stderr)
        print("  Please install manually: pip3 install Pillow", file=sys.stderr)
        return 1

    # Verify installation
    try:
        from PIL import Image
        print(f"✓ Pillow installed successfully (version {Image.__version__})")
        return 0
    except ImportError as e:
        print(f"✗ Pillow installation could not be verified: {e}", file=sys.stderr)
        print("  Please install manually: pip3 install Pillow", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(check_and_install())
