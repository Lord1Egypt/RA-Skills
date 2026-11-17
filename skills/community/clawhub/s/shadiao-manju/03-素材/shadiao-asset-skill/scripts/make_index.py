#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 03-素材，生成 素材索引.json

用法：
  python3 make_index.py --season-dir 99-项目/周一打工人/第01季
  python3 make_index.py --season-dir . --assets-dir 03-素材

输出：<season>/03-素材/素材索引.json
"""

import argparse
import json
import sys
from pathlib import Path

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}
REQUIRED_EXP = ["平静", "开心", "愤怒", "悲伤", "惊讶", "无语", "得意", "崩溃"]


def list_images(directory):
    if not directory.is_dir():
        return []
    # *.orig.png / *.bak.png 是白底转透明留下的原图备份，不算素材
    skip = (".orig", ".bak")
    return sorted(
        p
        for p in directory.iterdir()
        if p.suffix.lower() in IMG_EXT and p.stem not in skip and not p.stem.endswith(skip)
    )


def main():
    ap = argparse.ArgumentParser(description="生成素材索引")
    ap.add_argument("--season-dir", default=".", help="季目录")
    ap.add_argument("--assets-dir", help="素材目录（默认 <season>/03-素材）")
    args = ap.parse_args()

    season = Path(args.season_dir).resolve()
    assets = Path(args.assets_dir).resolve() if args.assets_dir else season / "03-素材"
    if not assets.is_dir():
        sys.exit(f"素材目录不存在：{assets}")

    # 从剧本读性别 / 音色
    meta = {}
    script_path = season / "01-剧本" / "剧本.json"
    if script_path.is_file():
        try:
            script = json.loads(script_path.read_text(encoding="utf-8-sig"))
            for c in script.get("characters", []):
                meta[c.get("name", "")] = c
        except Exception as e:
            print(f"  ! 剧本读取失败（忽略）：{e}", file=sys.stderr)

    def rel(p):
        return str(p.relative_to(assets)).replace("\\", "/")

    characters = []
    char_root = assets / "角色"
    if char_root.is_dir():
        for d in sorted(p for p in char_root.iterdir() if p.is_dir()):
            body = None
            for ext in IMG_EXT:
                cand = d / f"body{ext}"
                if cand.is_file():
                    body = cand
                    break
            expressions = {}
            full_bodies = {}
            for p in list_images(d):
                if p.name.startswith("exp_"):
                    expressions[p.stem[4:]] = rel(p)
                elif p.name.startswith("full_"):
                    full_bodies[p.stem[5:]] = rel(p)
            info = meta.get(d.name, {})
            face = {"x": 0.5, "y": 0.197, "scale": 0.6}
            face_path = d / "face.json"
            if face_path.is_file():
                try:
                    face.update(json.loads(face_path.read_text(encoding="utf-8-sig")))
                except Exception as e:
                    print(f"  ! {d.name}/face.json 读取失败：{e}", file=sys.stderr)
            item = {
                "name": d.name,
                "gender": info.get("gender", "male"),
                "voice": info.get("voice", ""),
                "dir": rel(d),
                "body": rel(body) if body else "",
                "expressions": expressions,
                "fullBodies": full_bodies,
                "face": face,
            }
            if body is None:
                print(f"  ! {d.name} 缺 body.png", file=sys.stderr)
            missing = [e for e in REQUIRED_EXP if e not in expressions]
            if missing:
                print(f"  ! {d.name} 缺表情：{', '.join(missing)}", file=sys.stderr)
            characters.append(item)

    backgrounds = [{"name": p.stem, "file": rel(p)} for p in list_images(assets / "背景")]
    props = [{"name": p.stem, "file": rel(p)} for p in list_images(assets / "道具")]
    covers = list_images(assets / "封面")

    index = {
        "characters": characters,
        "backgrounds": backgrounds,
        "props": props,
        "cover": rel(covers[0]) if covers else "",
    }

    out = assets / "素材索引.json"
    out.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f">> 素材索引：{out}")
    print(f"   角色 {len(characters)} 个 / 背景 {len(backgrounds)} 张 / 道具 {len(props)} 个 / 封面 {len(covers)} 张")
    for c in characters:
        print(f"   - {c['name']}：body={'有' if c['body'] else '缺'}，表情 {len(c['expressions'])}/8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
