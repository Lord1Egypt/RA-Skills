"""Setup script for local Whisper service."""
import os
import sys
from pathlib import Path


WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")


def download_model():
    """Download and cache whisper model (so server starts instantly)."""
    print(f"Downloading whisper model: {WHISPER_MODEL} ...")
    
    # Set proxy for download
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        print(f"Using proxy: {proxy}")
    
    from faster_whisper import WhisperModel
    # This downloads to huggingface cache (~/.cache/huggingface/hub)
    # Server uses the same path, so no re-download
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    print("✅ Model downloaded and cached!")
    return model


def update_env():
    """Update .env with local whisper config."""
    env_path = Path(__file__).parent.parent / ".env"
    
    config = {
        "WHISPER_API_KEY": "local",
        "WHISPER_BASE_URL": "http://127.0.0.1:8765/v1",
        "WHISPER_MODEL": WHISPER_MODEL,
    }
    
    lines = []
    if env_path.exists():
        lines = env_path.read_text().splitlines()
    
    # Update existing or append
    existing_keys = set()
    for i, line in enumerate(lines):
        for key, value in config.items():
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}"
                existing_keys.add(key)
    
    for key, value in config.items():
        if key not in existing_keys:
            lines.append(f"{key}={value}")
    
    env_path.write_text("\n".join(lines) + "\n")
    print(f"✅ Updated {env_path}")


def install_launchd():
    """Install launchd plist for auto-start (macOS)."""
    plist_src = Path(__file__).parent.parent / "scripts" / "videoarm-whisper.plist"
    plist_dst = Path.home() / "Library" / "LaunchAgents" / "videoarm-whisper.plist"
    
    if not plist_src.exists():
        print("⚠️  launchd plist not found, skipping auto-start setup")
        return
    
    if sys.platform != "darwin":
        print("ℹ️  Not macOS, skipping launchd setup")
        return
    
    import shutil
    plist_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(plist_src, plist_dst)
    os.system(f"launchctl load {plist_dst}")
    print(f"✅ Installed launchd service: {plist_dst}")


def main():
    print("🔧 Setting up local Whisper service...\n")
    
    # Step 1: Download model
    download_model()
    
    # Step 2: Update .env
    update_env()
    
    # Step 3: Install launchd (macOS auto-start)
    install_launchd()
    
    print("\n✅ Setup complete!")
    print("Whisper service will auto-start on boot.")
    print("To start now: python -m videoarm_local_whisper.server")


if __name__ == "__main__":
    main()
