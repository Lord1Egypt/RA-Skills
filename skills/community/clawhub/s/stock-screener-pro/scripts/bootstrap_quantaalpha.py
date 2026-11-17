#!/usr/bin/env python3
"""Install the optional QuantaAlpha backend and its public research data.

This script is intentionally manual. The MCP server never installs packages,
downloads datasets, or changes environments while handling a tool request.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path


REPOSITORY = "https://github.com/QuantaAlpha/QuantaAlpha.git"
PINNED_COMMIT = "b7ceb27b1001261d7a95b209a963664ae1f8ab23"
DATASET_BASE = "https://huggingface.co/datasets/QuantaAlpha/qlib_csi300/resolve/main"


def run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    printable = " ".join(command)
    print(f"+ {printable}", flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and destination.stat().st_size > 0:
        print(f"Using existing {destination}")
        return
    partial = destination.with_suffix(destination.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "stock-screener-pro/3.8.1"})
    with urllib.request.urlopen(request, timeout=60) as response, partial.open("wb") as output:
        total = int(response.headers.get("Content-Length", "0"))
        copied = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)
            copied += len(chunk)
            if total and copied % (64 * 1024 * 1024) < len(chunk):
                print(f"  downloaded {copied / 1024 / 1024:.0f}/{total / 1024 / 1024:.0f} MiB", flush=True)
    partial.replace(destination)


def extract_qlib(archive: Path, destination: Path) -> Path:
    expected = destination / "cn_data"
    if all((expected / name).is_dir() for name in ("calendars", "features", "instruments")):
        return expected
    destination.mkdir(parents=True, exist_ok=True)
    destination_root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for item in bundle.infolist():
            target = (destination / item.filename).resolve()
            if os.path.commonpath([str(destination_root), str(target)]) != str(destination_root):
                raise RuntimeError(f"Unsafe path in cn_data.zip: {item.filename}")
        bundle.extractall(destination)
    candidates = [
        path
        for path in destination.rglob("*")
        if path.is_dir() and all((path / name).is_dir() for name in ("calendars", "features", "instruments"))
    ]
    if not candidates:
        raise RuntimeError("cn_data.zip did not contain a valid Qlib data directory")
    source = min(candidates, key=lambda path: len(path.parts))
    if source != expected:
        if expected.exists():
            raise RuntimeError(f"Unexpected existing Qlib destination: {expected}")
        source.rename(expected)
    return expected


def install_repository(repo_dir: Path, venv_dir: Path) -> Path:
    if not repo_dir.exists():
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--filter=blob:none", REPOSITORY, str(repo_dir)])
    if not (repo_dir / ".git").is_dir():
        raise RuntimeError(f"Existing path is not a Git checkout: {repo_dir}")
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True, check=True
    ).stdout.strip()
    if status:
        raise RuntimeError(f"QuantaAlpha checkout has local changes; refusing to replace them: {repo_dir}")
    run(["git", "fetch", "origin", PINNED_COMMIT], cwd=repo_dir)
    run(["git", "checkout", "--detach", PINNED_COMMIT], cwd=repo_dir)

    venv_python = venv_dir / "bin" / "python"
    if not venv_python.exists():
        run([sys.executable, "-m", "venv", str(venv_dir)])
    install_env = dict(os.environ)
    install_env["SETUPTOOLS_SCM_PRETEND_VERSION"] = "0.1.0"
    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], env=install_env)
    run([str(venv_python), "-m", "pip", "install", "-e", str(repo_dir)], env=install_env)
    run([str(venv_python), "-c", "import quantaalpha; print('QuantaAlpha import OK')"])
    return venv_python


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the isolated QuantaAlpha backend for stock-screener-pro")
    parser.add_argument(
        "--data",
        choices=("none", "debug", "full"),
        default="none",
        help="none installs code only; debug adds Qlib plus the small HDF5 sample; full adds all published data",
    )
    args = parser.parse_args()
    if not ((3, 10) <= sys.version_info[:2] <= (3, 11)):
        print("QuantaAlpha requires Python 3.10 or 3.11; rerun this script with a supported interpreter.", file=sys.stderr)
        return 2
    if not shutil.which("git"):
        print("git is required.", file=sys.stderr)
        return 2

    state_dir = Path(
        os.environ.get(
            "STOCK_SCREENER_STATE_DIR",
            str(Path.home() / ".local" / "share" / "stock-screener-pro"),
        )
    ).expanduser().resolve()
    backend_dir = state_dir / "quant-backends" / "quantaalpha"
    repo_dir = backend_dir / "repo"
    venv_dir = backend_dir / "venv"
    data_dir = backend_dir / "data"
    venv_python = install_repository(repo_dir, venv_dir)

    if args.data in {"debug", "full"}:
        archive = data_dir / "downloads" / "cn_data.zip"
        download(f"{DATASET_BASE}/cn_data.zip?download=true", archive)
        qlib_dir = extract_qlib(archive, data_dir / "qlib")
        debug_path = data_dir / "factor_source_debug" / "daily_pv.h5"
        download(f"{DATASET_BASE}/daily_pv_debug.h5?download=true", debug_path)
        print(f"Qlib data ready at {qlib_dir}")
    if args.data == "full":
        full_path = data_dir / "factor_source" / "daily_pv.h5"
        download(f"{DATASET_BASE}/daily_pv.h5?download=true", full_path)
        print(f"Full factor source ready at {full_path}")

    installed_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_dir, capture_output=True, text=True, check=True
    ).stdout.strip()
    print(f"QuantaAlpha ready: python={venv_python}")
    print(f"Pinned commit: {installed_commit}")
    if args.data == "none":
        print("Code-only install complete. Run again with --data full before factor mining/backtesting.")
    elif args.data == "debug":
        print("Debug data is for environment validation only. Use --data full for factor mining.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
