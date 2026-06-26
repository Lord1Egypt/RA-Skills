#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys


REQUIRED_PACKAGES = [
    ("requests", "requests"),
    ("playwright", "playwright"),
    ("imageio_ffmpeg", "imageio-ffmpeg"),
    ("sherpa_onnx", "sherpa-onnx"),
    ("docx", "python-docx"),
    ("numpy", "numpy"),
]


def missing_packages() -> list[str]:
    missing: list[str] = []
    for module_name, package_name in REQUIRED_PACKAGES:
        if importlib.util.find_spec(module_name) is None:
            missing.append(package_name)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Python packages required by the skill.")
    parser.add_argument(
        "--install-playwright-browser",
        action="store_true",
        help="Also run `python -m playwright install chromium`.",
    )
    args = parser.parse_args()

    missing = missing_packages()
    if missing:
        subprocess.run([sys.executable, "-m", "pip", "install", *missing], check=True)
    else:
        print("All required Python packages are already installed.")

    if args.install_playwright_browser:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)

    print("Environment bootstrap complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
