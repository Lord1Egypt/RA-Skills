#!/usr/bin/env python3
"""Read-only inventory; never prints profile contents or runtime logs."""
import argparse
import json
from pathlib import Path


def inspect(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be a directory")
    plugins = root / "plugins"
    profiles = root / "profiles"
    result = {
        "root": str(root),
        "activeHostConfirmed": False,
        "pluginsDirectoryExists": plugins.is_dir() and not plugins.is_symlink(),
        "profilesDirectoryExists": profiles.is_dir() and not profiles.is_symlink(),
        "selectionConfigExists": (root / "StreamDockConfig.ini").is_file(),
        "rootProfileCount": 0,
        "plugins": [],
        "warnings": [],
    }
    if result["profilesDirectoryExists"]:
        result["rootProfileCount"] = sum(
            p.is_dir() and not p.is_symlink() for p in profiles.glob("*.sdProfile")
        )
    if result["pluginsDirectoryExists"]:
        for folder in sorted(plugins.glob("*.sdPlugin")):
            manifest = folder / "manifest.json"
            if folder.is_symlink() or manifest.is_symlink():
                result["warnings"].append(f"Skipped symlink: {folder.name}")
                continue
            try:
                data = json.loads(manifest.read_text(encoding="utf-8-sig"))
                actions = data.get("Actions", [])
                result["plugins"].append({
                    "folder": folder.name,
                    "uuid": data.get("UUID"),
                    "version": data.get("Version"),
                    "sdkVersion": data.get("SDKVersion"),
                    "node": data.get("Nodejs"),
                    "actionCount": len(actions) if isinstance(actions, list) else None,
                })
            except (OSError, ValueError, AttributeError) as error:
                result["warnings"].append(f"Unreadable manifest: {folder.name} ({type(error).__name__})")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Data root confirmed by the host UI")
    args = parser.parse_args()
    try:
        result = inspect(args.root)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Inventory failed: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
