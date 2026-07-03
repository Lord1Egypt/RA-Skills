#!/usr/bin/env python3
"""
token-slim: tiktoken installer (opensource edition)

Install strategy (in order, with automatic fallback):
  1. PyPI official (pypi.org)            — 2 retries
  2. Tsinghua mirror                     — China users acceleration
  3. Aliyun mirror                       — China users acceleration
  4. Skip tiktoken, use heuristic estimate (CJK/ASCII split, ~40-60% error)

BPE vocabulary (cl100k_base.tiktoken) is fetched on first use by tiktoken
itself from OpenAI's public blob (openaipublic.blob.core.windows.net),
cached under TIKTOKEN_CACHE_DIR (default: <workspace>/.cache/tiktoken).

Usage:
    python3 install_tiktoken.py            # install + verify
    python3 install_tiktoken.py --check    # only check current state
    python3 install_tiktoken.py --workspace /path/to/ws  # custom workspace
"""

import argparse
import os
import sys
import subprocess
import urllib.request
import urllib.error
import shutil
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

PYPI_OFFICIAL  = "https://pypi.org/simple/"
TSINGHUA_INDEX = "https://pypi.tuna.tsinghua.edu.cn/simple"
ALIYUN_INDEX   = "https://mirrors.aliyun.com/pypi/simple/"

# Each entry: (display_name, index_url, retries)
INSTALL_SOURCES = [
    ("PyPI (official)",         PYPI_OFFICIAL,  2),
    ("Tsinghua mirror (China)", TSINGHUA_INDEX, 1),
    ("Aliyun mirror (China)",   ALIYUN_INDEX,   1),
]

# BPE vocabulary public blob (tiktoken fetches this automatically on first encode)
BPE_BLOB_URL  = "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken"
BPE_CACHE_KEY = "9b5ad71b2ce5302211f9c61530b329a4922fc6a4"

PIP_TIMEOUT = 60  # seconds per pip attempt

# ── Helpers ───────────────────────────────────────────────────────────────────

def _run(cmd, **kwargs):
    try:
        return subprocess.run(cmd, **kwargs)
    except (OSError, subprocess.SubprocessError) as e:
        result = subprocess.CompletedProcess(cmd, returncode=1)
        result.stdout = ""
        result.stderr = str(e)
        return result


def _tiktoken_importable():
    try:
        import importlib.util
        return importlib.util.find_spec("tiktoken") is not None
    except Exception:
        return False


def _default_cache_dir(workspace=None):
    """
    Default tiktoken cache directory.

    Priority:
      1. TIKTOKEN_CACHE_DIR env var (respected by tiktoken natively)
      2. <workspace>/.cache/tiktoken (user-supplied workspace)
      3. <CWD>/.cache/tiktoken (page-root persistent on most VMs)

    NOTE: We avoid ~/.cache/tiktoken (default tiktoken behaviour) because some
    container / VM environments mount only the working directory persistently
    while $HOME may be wiped between sessions.
    """
    env_dir = os.environ.get("TIKTOKEN_CACHE_DIR", "").strip()
    if env_dir:
        return Path(env_dir).expanduser()

    if workspace:
        return Path(workspace).expanduser().resolve() / ".cache" / "tiktoken"

    return Path.cwd().resolve() / ".cache" / "tiktoken"


def _bpe_cache_exists(cache_dir):
    cache_path = Path(cache_dir) / BPE_CACHE_KEY
    return cache_path.exists() and cache_path.stat().st_size > 0


# ── Step 1: Install tiktoken via pip with multi-source fallback ─────────────

def _pip_install(index_url, attempt_label):
    """Single pip attempt against a given index URL."""
    cmd = [
        sys.executable, "-m", "pip", "install",
        "--user", "--break-system-packages",
        "-i", index_url,
        "tiktoken",
    ]
    print(f"  → {attempt_label} ({index_url}) ...")
    result = _run(cmd, capture_output=True, text=True, timeout=PIP_TIMEOUT)
    if result.returncode == 0:
        return True, ""
    err_tail = (result.stderr or result.stdout or "").strip()[-200:]
    return False, err_tail


def install_wheels():
    """Try each install source with retries; return True if tiktoken installs."""
    print("📦 Installing tiktoken ...")

    for source_name, index_url, retries in INSTALL_SOURCES:
        for attempt in range(1, retries + 1):
            label = f"Try {source_name}"
            if retries > 1:
                label += f" [attempt {attempt}/{retries}]"
            ok, err = _pip_install(index_url, label)
            if ok:
                print(f"  ✅ Installed via {source_name}")
                return True
            print(f"  ⚠️  Failed: {err}")

    print("  ❌ All install sources exhausted. tiktoken unavailable.")
    print("     scan_workspace.py will fall back to heuristic estimation.")
    return False


# ── Step 2: Pre-warm BPE vocabulary cache ───────────────────────────────────

def ensure_bpe_cache(cache_dir):
    """
    Pre-warm BPE vocab by invoking tiktoken once.
    tiktoken downloads cl100k_base.tiktoken from the public OpenAI blob on
    first use and caches it under TIKTOKEN_CACHE_DIR (or ~/.cache/tiktoken).
    """
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    if _bpe_cache_exists(cache_dir):
        print(f"  ✅ BPE vocab already cached at {cache_dir / BPE_CACHE_KEY}")
        return True

    print(f"  → Fetching BPE vocab via tiktoken (cache → {cache_dir}) ...")

    env = os.environ.copy()
    env["TIKTOKEN_CACHE_DIR"] = str(cache_dir)

    code = (
        "import tiktoken; "
        "enc = tiktoken.get_encoding('cl100k_base'); "
        "_ = enc.encode('warmup')"
    )
    result = _run(
        [sys.executable, "-c", code],
        capture_output=True, text=True, env=env, timeout=60,
    )

    if result.returncode == 0 and _bpe_cache_exists(cache_dir):
        print("  ✅ BPE vocab cached successfully")
        return True

    err = (result.stderr or "").strip()[-300:]
    print(f"  ❌ Failed to cache BPE vocab: {err}")
    print(f"     (likely no network to {BPE_BLOB_URL})")
    return False


# ── Step 3: End-to-end verification ─────────────────────────────────────────

def verify(cache_dir):
    """Verify tiktoken can encode a known sample."""
    env = os.environ.copy()
    env["TIKTOKEN_CACHE_DIR"] = str(cache_dir)

    test_text = "hello 你好世界"
    expected = 8  # cl100k_base
    code = (
        f"import tiktoken; enc = tiktoken.get_encoding('cl100k_base'); "
        f"n = len(enc.encode({test_text!r})); print('tokens:', n); "
        f"assert n == {expected}, f'expected {expected} got {{n}}'"
    )
    result = _run(
        [sys.executable, "-c", code],
        capture_output=True, text=True, env=env, timeout=10,
    )

    if result.returncode == 0:
        print(f"  ✅ Verified: {result.stdout.strip()}")
        return True

    err = (result.stderr or "").strip()[-200:]
    print(f"  ❌ Verification failed: {err}")
    return False


# ── Status / Main ───────────────────────────────────────────────────────────

def check_status(cache_dir):
    installed = _tiktoken_importable()
    cache_ok  = _bpe_cache_exists(cache_dir)
    print(f"tiktoken importable : {'✅' if installed else '❌'}")
    print(f"BPE cache present   : {'✅' if cache_ok else '❌'} ({cache_dir / BPE_CACHE_KEY})")
    if installed and cache_ok:
        print("Status: ready (precise tiktoken counting)")
    elif installed and not cache_ok:
        print("Status: tiktoken installed but BPE vocab missing → run install_tiktoken.py")
    else:
        print("Status: not installed → falls back to CJK/ASCII heuristic (~40-60% error)")


def parse_args():
    p = argparse.ArgumentParser(
        description="Install tiktoken for token-slim (multi-source fallback)."
    )
    p.add_argument(
        "--check", action="store_true",
        help="Only report current install/cache status; do not install.",
    )
    p.add_argument(
        "--workspace", default=None,
        help="Workspace path; tiktoken cache goes to <workspace>/.cache/tiktoken. "
             "Defaults to CWD. Honoured only if TIKTOKEN_CACHE_DIR is unset.",
    )
    return p.parse_args()


def main():
    args = parse_args()
    cache_dir = _default_cache_dir(args.workspace)

    if args.check:
        check_status(cache_dir)
        return

    print("🚀 token-slim: tiktoken installer")
    print("=" * 50)
    print(f"Cache directory: {cache_dir}")
    print()

    # Step 1: install tiktoken
    if _tiktoken_importable():
        print("📦 tiktoken already importable, skipping pip step")
        wheel_ok = True
    else:
        wheel_ok = install_wheels()

    if not wheel_ok:
        print("\n⚠️  tiktoken not installed; scan_workspace.py will use heuristic mode.")
        print("    To retry later: python3 install_tiktoken.py")
        sys.exit(1)

    # Step 2: prewarm BPE vocab
    print("\n📥 Caching BPE vocabulary ...")
    bpe_ok = ensure_bpe_cache(cache_dir)
    if not bpe_ok:
        print("\n⚠️  BPE vocab unavailable; scan_workspace.py will use heuristic mode.")
        sys.exit(1)

    # Step 3: verify end-to-end
    print("\n🔍 Verifying ...")
    if verify(cache_dir):
        print(f"\n✅ tiktoken ready!")
        print(f"   Cache: {cache_dir}")
        print(f"   scan_workspace.py will pick it up automatically.")
    else:
        print("\n❌ Verification failed. Please re-check your environment.")
        sys.exit(1)


if __name__ == "__main__":
    main()
