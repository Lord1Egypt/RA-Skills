#!/usr/bin/env python3
import json
from pathlib import Path


def main() -> None:
    skill_dir = Path(__file__).resolve().parent.parent
    theme_pack_path = skill_dir / "assets" / "theme-pack.json"
    theme_pack = json.loads(theme_pack_path.read_text(encoding="utf-8"))
    for theme in theme_pack["themes"]:
        print(f"{theme['id']} {theme['name']} - {theme['description']}")


if __name__ == "__main__":
    main()
