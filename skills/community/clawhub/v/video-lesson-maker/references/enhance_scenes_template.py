#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画面增强模板（复制本文件到视频目录后，按线稿布局改坐标即可）。

职责：在匀纸/裁剪后的线稿上，用 enhance_toolkit 的「手绘风图元」补充
必须在揭示区内的标题、标签牌、便签、印章。增强图的尺寸必须与
annotation.json 的 canvas 一致（本项目统一 1536×864）。

⚠️ 铁律：用 toolkit 画上去的每个文字块，都要落在对应 annotation region 框内，
否则渲染时不会显示（渲染器只在 region 内揭示墨迹）。

用法（在视频目录下）：
  <ENV_PY> enhance_scenes.py
"""
import sys
from pathlib import Path

# 把 skill 的 scripts 目录加进 import 路径，便于直接 `from enhance_toolkit import ...`
SKILL_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from enhance_toolkit import (  # noqa: E402
    Image, ImageDraw, f_kai, f_yahei, INK, RED, BLUE, ORANGE, PAPER_LIGHT,
    draw_title, draw_label_card, draw_note, draw_stamp, sketch_rect, sketch_line,
)

SRC = "scene-01-xxx-crop.png"   # ← 裁剪后的线稿（1536×864）
OUT = "scene-01-xxx-enh.png"    # ← 增强输出


def main():
    im = Image.open(SRC).convert("RGBA")
    d = ImageDraw.Draw(im)

    # 1) 大标题（居中 + 红色波浪下划线）
    draw_title(d, "本幕标题", cx=768, y=80, size=72, color=INK)

    # 2) 标签牌：手绘双线框 + 居中文字（每个牌对应一个 annotation region）
    draw_label_card(d, box=(120, 240, 620, 360), text="左侧要点", font=f_yahei(44))
    draw_label_card(d, box=(900, 240, 1400, 360), text="右侧要点", font=f_yahei(44))

    # 3) 便签条（带折角 + 胶带，适合放结论/警示）
    draw_note(d, im, box=(120, 620, 700, 800), text="一句话结论", font=f_kai(46))

    # 4) 完结印章（可选）
    draw_stamp(d, cx=1300, cy=720, r=70, text="判定")

    im.convert("RGB").save(OUT)
    print(f"增强完成 -> {OUT}  ({im.size})")


if __name__ == "__main__":
    main()
