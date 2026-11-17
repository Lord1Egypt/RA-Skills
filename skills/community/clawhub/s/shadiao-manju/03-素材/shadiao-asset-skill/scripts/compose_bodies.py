#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 8 张表情预合成到整身图上，生成 8 张完整角色图（full_*.png）

为什么：
  直接在 app 里「身体 + 表情头」叠两层，近看会有双描边/贴纸边。
  预合成后，工程里只切整身图（symbol 的 8 个 material），没有叠层接缝。

用法：
  python3 compose_bodies.py --season-dir 99-项目/<剧名>/第01季
  python3 compose_bodies.py --char-dir 99-项目/<剧名>/第01季/03-素材/角色/阿强

输入：body.png、exp_*.png、face.json
输出：full_平静.png … full_崩溃.png
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFilter
except ImportError:
    sys.exit("缺少 Pillow：pip install Pillow")

# 复用 white_to_alpha 的「填回被轮廓包住的白色」，防止表情图白脸被抠成透明后
# 预合成出半透明的头（近景会整颗头发灰）
try:
    from white_to_alpha import fill_enclosed_white
except Exception:  # noqa: BLE001
    fill_enclosed_white = None

EXPRESSIONS = ["平静", "开心", "愤怒", "悲伤", "惊讶", "无语", "得意", "崩溃"]


def alpha_bbox(img):
    a = img.getchannel("A")
    return a.getbbox()


def make_mask(size, center, rx, ry, feather=6):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([center[0] - rx, center[1] - ry, center[0] + rx, center[1] + ry], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(feather))


def compose(char_dir: Path):
    body_path = char_dir / "body.png"
    face_path = char_dir / "face.json"
    if not body_path.is_file() or not face_path.is_file():
        print(f"  ! 跳过 {char_dir.name}：缺 body.png 或 face.json", file=sys.stderr)
        return 0

    face = json.loads(face_path.read_text(encoding="utf-8-sig"))
    body = Image.open(body_path).convert("RGBA")
    # v0.9：换物种/换头型时，身体图里自带的旧头要先擦掉，
    # 否则新头套在旧头外面（熊猫耳朵会露在狼头两侧）。
    # face.json 里写 eraseHead: [{x,y,r}]，x/y 为归一化坐标，r 为像素（按 body 宽度算）
    for disc in face.get("eraseHead") or []:
        cx = float(disc["x"]) * body.width
        cy = float(disc["y"]) * body.height
        r = float(disc["r"]) * body.width
        alpha = Image.new("L", body.size, 0)
        ImageDraw.Draw(alpha).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        hole = Image.new("RGBA", body.size, (0, 0, 0, 0))
        body = Image.composite(hole, body, alpha)
    scale = float(face.get("scale", 1.0))

    ref_path = char_dir / "exp_平静.png"
    if not ref_path.is_file():
        print(f"  ! 跳过 {char_dir.name}：缺 exp_平静.png", file=sys.stderr)
        return 0
    ref = Image.open(ref_path).convert("RGBA")
    bbox = alpha_bbox(ref)
    if not bbox:
        print(f"  ! 跳过 {char_dir.name}：表情图为空", file=sys.stderr)
        return 0

    x0, y0, x1, y1 = bbox
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx = (x1 - x0) * 0.56
    ry = (y1 - y0) * 0.56
    # v0.7：羽化改成 1px（几乎硬边）。原来 5px 的软边在近景会留下一圈半透明椭圆，
    # 叠在背景上就是「双层描边」。脸是同色块，硬边反而看不出来。
    base_mask = make_mask(ref.size, (cx, cy), rx, ry, feather=1)

    # 除了标准 8 个表情，还支持额外姿势（说话 / 摸鱼 …）：只要 exp_<名>.png 存在就一起合成
    extra = sorted(
        f.stem[4:] for f in char_dir.glob("exp_*.png") if f.stem[4:] not in EXPRESSIONS
    )
    made = 0
    for emo in EXPRESSIONS + extra:
        p = char_dir / f"exp_{emo}.png"
        if not p.is_file():
            print(f"  ! {char_dir.name} 缺 exp_{emo}.png，跳过", file=sys.stderr)
            continue
        expr = Image.open(p).convert("RGBA")
        ew, eh = max(1, int(expr.width * scale)), max(1, int(expr.height * scale))
        expr_r = expr.resize((ew, eh), Image.LANCZOS)
        mask_r = base_mask.resize((ew, eh), Image.LANCZOS)

        px = int(round(face.get("x", 0.5) * body.width - ew / 2))
        py = int(round(face.get("y", 0.5) * body.height - eh / 2))

        out = body.copy()
        # v0.7：mask 要和表情图自身的 alpha 取交集，否则表情图的透明区会把身体
        # 「擦」出洞（白脸被抠过的表情图会让整颗头变透明）
        paste_mask = ImageChops.multiply(mask_r, expr_r.getchannel("A"))
        # v0.8：把粘贴区往内收一点，剪掉表情图自带的那圈描边（否则头上出现第二圈线，
        # 呆毛也会被贴成两根）。脸的内部特征离边缘很远，内收不影响五官。
        erode = max(1, int(ew * 0.045) | 1)
        paste_mask = paste_mask.filter(ImageFilter.MinFilter(erode))
        out.paste(expr_r, (px, py), paste_mask)
        # 注意：不要在这里再跑 fill_enclosed_white。
        # 形态学闭运算会让「填充区」比轮廓略微外扩，在头边上留一圈不透明白边
        # （近景就是「白色月牙 + 第二圈描边」）。白脸的不透明由 exp 图本身保证。
        out.save(char_dir / f"full_{emo}.png", "PNG", optimize=True)
        made += 1

    print(f"  ✓ {char_dir.name}：{made} 张完整角色图")
    return made


def main():
    ap = argparse.ArgumentParser(description="表情预合成到整身图")
    ap.add_argument("--season-dir", help="季目录（自动扫描 03-素材/角色/*）")
    ap.add_argument("--char-dir", help="只处理某个角色目录")
    args = ap.parse_args()

    if args.char_dir:
        compose(Path(args.char_dir))
        return

    if not args.season_dir:
        sys.exit("给 --season-dir 或 --char-dir")
    root = Path(args.season_dir) / "03-素材" / "角色"
    if not root.is_dir():
        sys.exit(f"找不到角色目录：{root}")
    total = 0
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        total += compose(d)
    print(f"完成：{total} 张")


if __name__ == "__main__":
    main()
