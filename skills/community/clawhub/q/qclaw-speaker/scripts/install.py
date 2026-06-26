#!/usr/bin/env python3
"""QClaw Speaker — 一键安装四引擎 TTS

Installs dependencies for all engines:
  - edge-tts  (online, premium, 0MB)
  - pyttsx3   (offline, native, 0MB)
  - sherpa-onnx (offline, ONNX, 13MB model, optional)

Usage:
  python install.py                    # All engines (excl. sherpa model)
  python install.py --edge-only        # Edge TTS only
  python install.py --win-only         # Windows SAPI only
  python install.py --sherpa xiao_ya   # Download specific model
  python install.py --check            # Check installed engines
"""

import os, sys, subprocess, tarfile, urllib.request, argparse, shutil, time
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
MODELS_DIR = SKILL_DIR / "models"

SHERPA_MODELS = {
    "xiao_ya": {
        "name": "vits-piper-zh_CN-xiao_ya-medium-int8",
        "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-zh_CN-xiao_ya-medium-int8.tar.bz2",
        "mirror": "https://www.modelscope.cn/models/manyeyes/sherpa-onnx-piper-zh/resolve/master/vits-piper-zh_CN-xiao_ya-medium-int8.tar.bz2",
        "size_mb": 13.4,
    },
    "chaowen": {
        "name": "vits-piper-zh_CN-chaowen-medium-int8",
        "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-zh_CN-chaowen-medium-int8.tar.bz2",
        "mirror": "https://www.modelscope.cn/models/manyeyes/sherpa-onnx-piper-zh/resolve/master/vits-piper-zh_CN-chaowen-medium-int8.tar.bz2",
        "size_mb": 13.4,
    },
    "huayan": {
        "name": "vits-piper-zh_CN-huayan-medium",
        "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-zh_CN-huayan-medium.tar.bz2",
        "mirror": "",
        "size_mb": 64.1,
    },
}


def pip_install(pkg: str):
    print(f"  pip install {pkg}...", end=" ", flush=True)
    r = subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"],
                       capture_output=True, text=True, timeout=120)
    print("✅" if r.returncode == 0 else f"❌ {r.stderr.strip()[-80:]}")
    return r.returncode == 0


def check_engine(name: str) -> bool:
    checks = {"edge": "edge_tts", "win": "pyttsx3", "sherpa": "sherpa_onnx"}
    try:
        __import__(checks.get(name, name))
        return True
    except ImportError:
        return False


def fix_ort_dll():
    """Override sherpa-onnx's bundled ORT DLL with system ORT."""
    try:
        import sherpa_onnx, onnxruntime
        sherpa_dir = Path(sherpa_onnx.__file__).parent
        ort_dir = Path(onnxruntime.__file__).parent
        # Find system ORT DLL
        for candidate in [ort_dir / "capi" / "onnxruntime.dll",
                          ort_dir / "onnxruntime.dll"]:
            if candidate.exists():
                target = sherpa_dir / "lib" / "onnxruntime.dll"
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists() or candidate.stat().st_size != target.stat().st_size:
                    shutil.copy2(str(candidate), str(target))
                    shutil.copy2(str(candidate), str(sherpa_dir / "onnxruntime.dll"))
                    print(f"  ORT fix: system {onnxruntime.__version__} → sherpa-onnx dir")
                return True
    except (ImportError, FileNotFoundError):
        pass
    return False


def install_edge():
    print("\n📡 [1/4] Edge TTS (online, Microsoft Neural)")
    if check_engine("edge"):
        print("   ✅ Already installed")
        return True
    return pip_install("edge-tts")


def install_win():
    print("\n💻 [2/4] Windows SAPI (offline, native)")
    if check_engine("win"):
        print("   ✅ Already installed")
        return True
    return pip_install("pyttsx3")


def install_sherpa_core():
    print("\n🤖 [3/4] sherpa-onnx + dependencies")
    ok = True
    if not check_engine("sherpa"):
        ok &= pip_install("sherpa-onnx")
    ok &= pip_install("soundfile")
    if check_engine("sherpa") and not fix_ort_dll():
        print("   ⚠️  ORT DLL fix not applied (may not be needed)")
    return ok


def install_sherpa_model(voice_name: str = "xiao_ya"):
    model_info = SHERPA_MODELS.get(voice_name, SHERPA_MODELS["xiao_ya"])
    model_dir = MODELS_DIR / model_info["name"]
    print(f"\n📥 [4/4] Model: {model_info['name']} ({model_info['size_mb']}MB)")

    if list(model_dir.rglob("*.onnx")):
        print(f"   ✅ Already downloaded")
        return True

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    tarball = MODELS_DIR / f"{model_info['name']}.tar.bz2"
    urls = [u for u in [model_info.get("mirror",""), model_info["url"]] if u]

    for url in urls:
        try:
            print(f"   Downloading from {url.split('/')[2]}...")
            urllib.request.urlretrieve(url, tarball)
            with tarfile.open(tarball, "r:bz2") as tf:
                tf.extractall(path=MODELS_DIR)
            tarball.unlink()

            # Flatten if tar created nested dir
            for child in model_dir.iterdir():
                if child.is_dir() and (child / "tokens.txt").exists():
                    for f in child.iterdir():
                        shutil.move(str(f), str(model_dir / f.name))
                    child.rmdir()

            print(f"   ✅ Model ready → {model_dir}")
            return True
        except Exception as e:
            print(f"   ⚠️  Failed: {e}")
            if tarball.exists():
                tarball.unlink()
    print(f"   ❌ All download URLs failed. Download manually to: {model_dir}")
    return False


def check_all():
    print("\n🔍 QClaw Speaker — Engine Status\n")
    engines = [
        ("edge", "Edge TTS", "Online, Microsoft Neural, best quality"),
        ("win", "Windows SAPI", "Offline native, zero config, instant"),
        ("sherpa", "sherpa-onnx", "Offline ONNX, 13MB Piper model"),
    ]
    for key, name, desc in engines:
        ok = check_engine(key)
        print(f"  {'✅' if ok else '❌'} {name:<18} {desc}")
    print(f"\n  Available: {sum(1 for k,_,_ in engines if check_engine(k))}/3")


def main():
    parser = argparse.ArgumentParser(description="QClaw Speaker Installer")
    parser.add_argument("--edge-only", action="store_true")
    parser.add_argument("--win-only", action="store_true")
    parser.add_argument("--sherpa", nargs="?", const="xiao_ya",
                        choices=list(SHERPA_MODELS.keys()),
                        help="Download sherpa-onnx model")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    print("🎙️  QClaw Speaker — Installer v1.1\n")

    if args.check:
        return check_all()
    if args.edge_only:
        install_edge()
    elif args.win_only:
        install_win()
    elif args.sherpa:
        install_sherpa_core()
        install_sherpa_model(args.sherpa)
    else:
        install_edge()
        install_win()
        install_sherpa_core()
        # Don't auto-download sherpa model (13MB, optional)

    print(f"\n📝 'python scripts/speak.py --list-voices' — 查看音色")
    print(f"📝 'python scripts/speak.py \"你好\"' — 测试播报\n")


if __name__ == "__main__":
    main()