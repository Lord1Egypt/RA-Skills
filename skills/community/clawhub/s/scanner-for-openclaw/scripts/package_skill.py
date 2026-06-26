#!/usr/bin/env python3
"""
Package OpenClaw Security Scanner skill for distribution.
Creates a tarball suitable for ClawHub publishing.

Usage:
    python3 package_skill.py
"""

import tarfile
import json
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent
OUTPUT_DIR = Path("/tmp/skill-packages")
OUTPUT_DIR.mkdir(exist_ok=True)

def get_version():
    """Get skill version from clawhub.json"""
    clawhub_json = SKILL_DIR / "clawhub.json"
    if clawhub_json.exists():
        with open(clawhub_json, 'r') as f:
            data = json.load(f)
            return data.get('version', '1.0.0')
    return '1.0.0'

def get_files():
    """Get list of files to include"""
    files = []
    for pattern in [
        "SKILL.md",
        "README.md",
        "clawhub.json",
        "scripts/*.py",
        "references/*.md",
        "LICENSE"
    ]:
        files.extend(SKILL_DIR.glob(pattern))
    return [f for f in files if f.exists()]

def package():
    """Create tarball package"""
    version = get_version()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"openclaw-security-scanner-{version}"
    tarball_path = OUTPUT_DIR / f"{package_name}.tar.gz"
    
    files = get_files()
    
    with tarfile.open(tarball_path, "w:gz") as tar:
        for file in files:
            arcname = f"{package_name}/{file.relative_to(SKILL_DIR)}"
            tar.add(file, arcname=arcname)
            print(f"Added: {arcname}")
    
    # Create manifest
    manifest = {
        "name": "openclaw-security-scanner",
        "version": version,
        "package": str(tarball_path),
        "files": [str(f.relative_to(SKILL_DIR)) for f in files],
        "created": datetime.now().isoformat(),
        "checksum": None  # Would calculate in production
    }
    
    manifest_path = OUTPUT_DIR / f"{package_name}.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✅ Package created: {tarball_path}")
    print(f"📋 Manifest: {manifest_path}")
    print(f"📦 Files: {len(files)}")
    
    return tarball_path, manifest_path

if __name__ == "__main__":
    package()
