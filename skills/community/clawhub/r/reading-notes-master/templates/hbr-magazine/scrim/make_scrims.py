#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HBR 杂志遮罩 PNG 生成器（reading-notes-master v2.7 · templates/hbr-magazine/scrim/）

为什么必须用 PNG 而不是 CSS linear-gradient：
Chrome headless 打印 PDF 时，linear-gradient 叠在背景照片上会把照片
光栅化进平铺 Pattern（未压缩位图，体积暴涨 2.4 倍）。预渲染成带 alpha 的
PNG（8×1024，约 280B）后照片保持直连 JPEG XObject，Pattern 归零。

四类遮罩的渐变曲线（与 mag.css 的 .mc/.md/.mp/.mq-scrim 对应）：
  mc 封面   .62 → .18 → .30 → .88   （顶暗压刊名，中段透，底暗压封面条）
  md 章隔页 .55 → .06 → .10 → .90   （上浅显巨号，底暗压标题）
  mp 照片页 .30 →   0  →      .78   （仅底段压说明文字）
  mq 金句页 平铺 .66                （整页压暗保居中金句可读）

改曲线只改 STOPS 字典；RGB 底色同步改 TINT。
运行：python3 make_scrims.py  （纯标准库 + PIL，无其他依赖）
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

# 遮罩底色（接近 HBR 墨色的深黑，略带暖）
TINT = (10, 8, 12)

# 四类遮罩的 alpha 曲线：[(位置 0~1, alpha 0~1), ...] 线性插值
STOPS = {
    "mc": [(0.00, 0.62), (0.34, 0.18), (0.62, 0.30), (1.00, 0.88)],
    "md": [(0.00, 0.55), (0.30, 0.06), (0.55, 0.10), (1.00, 0.90)],
    "mp": [(0.00, 0.30), (0.40, 0.00), (1.00, 0.78)],
    # mq 用平铺：单点 alpha（见 FLAT）
}
FLAT = {"mq": 0.66}

W, H = 8, 1024  # 竖向渐变；横向拉伸由 CSS background-size:100% 100% 完成


def alpha_at(stops, t):
    for i in range(len(stops) - 1):
        t0, a0 = stops[i]
        t1, a1 = stops[i + 1]
        if t0 <= t <= t1:
            if t1 == t0:
                return a1
            return a0 + (a1 - a0) * (t - t0) / (t1 - t0)
    return stops[-1][1] if t > stops[-1][0] else stops[0][1]


def main():
    for name, stops in STOPS.items():
        img = Image.new("RGBA", (W, H))
        px = img.load()
        for y in range(H):
            v = int(round(alpha_at(stops, y / (H - 1)) * 255))
            for x in range(W):
                px[x, y] = (TINT[0], TINT[1], TINT[2], v)
        p = os.path.join(HERE, "scrim_%s.png" % name)
        img.save(p, "PNG", optimize=True)
        print("%s -> %s (%dB)" % (name, p, os.path.getsize(p)))
    for name, a in FLAT.items():
        img = Image.new("RGBA", (1, 1), (TINT[0], TINT[1], TINT[2], int(round(a * 255))))
        p = os.path.join(HERE, "scrim_%s.png" % name)
        img.save(p, "PNG", optimize=True)
        print("%s -> %s (%dB)" % (name, p, os.path.getsize(p)))


if __name__ == "__main__":
    main()
