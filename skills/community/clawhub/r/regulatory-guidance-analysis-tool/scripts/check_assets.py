"""校验 assets/ 下文件是否齐全

Usage: python check_assets.py <assets_dir> --type <pptx|pdf>
"""
import sys
from pathlib import Path

COMMON = [
    "fonts.css",
    "base.css",
    "themes/midcentury.css",
    "runtime.js",
    "animations/animations.css",
    "animations/fx-runtime.js",
    "animations/fx/_util.js",
    "animations/fx/chain-react.js",
    "animations/fx/confetti-cannon.js",
    "animations/fx/constellation.js",
    "animations/fx/counter-explosion.js",
]

ONLY = {
    "pptx": ["pptx-model.css"],
    "pdf":  ["pdf-model.css"],
}

def main():
    if len(sys.argv) < 4 or sys.argv[2] != "--type":
        print("Usage: python check_assets.py <assets_dir> --type <pptx|pdf>")
        sys.exit(1)

    assets_dir = Path(sys.argv[1])
    fmt = sys.argv[3]

    if fmt not in ONLY:
        print(f"不支持的类型: {fmt}，仅支持 pptx 或 pdf")
        sys.exit(1)

    checklist = COMMON + ONLY[fmt]
    missing = []

    for f in checklist:
        p = assets_dir / f
        if not p.exists():
            missing.append(f)
            print(f"  MISS {f}")
        else:
            print(f"  OK   {f}")

    if missing:
        print(f"\n共 {len(missing)} 个文件缺失：")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)
    else:
        print(f"\n全部 {len(checklist)} 个文件就位 OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
