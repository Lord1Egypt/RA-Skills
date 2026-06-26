#!/usr/bin/env python3
"""上传永久素材到微信"""
import argparse, json, sys
from wechat_client import upload_permanent_material

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--type", default="thumb", choices=["image", "voice", "video", "thumb"])
    args = parser.parse_args()
    try:
        result = upload_permanent_material(args.file, material_type=args.type)
        json.dump({"ok": True, "step": "upload_material", "file": args.file, "material_type": args.type, "media_id": result.get("media_id"), "url": result.get("url"), "result": result}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except Exception as e:
        json.dump({"ok": False, "step": "upload_material", "file": args.file, "message": str(e)}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
