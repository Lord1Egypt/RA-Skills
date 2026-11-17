# -*- coding: utf-8 -*-
"""图片诊断/对照 CLI（纯标准库，不需要 Pillow）。

子命令
------
stats   <图...>                 平均色/亮度、主色、相邻像素跳变（锐度代理）
lift    <图> [--gamma 0.62]     模拟「显示端把暗部提一档」，看色带是否暴露
compare <图A> <图B> [--width 900] 并排/上下拼一张对照图（白底留边）
bbox    <图> [--thresh 235]     非白区域外接框（从截图里裁出目标图）
resize  <图> --width 900 -o out 缩放并另存
sheet   <图...> --cols 5 --width 300 -o out   联系表（批量目检）
crop    <图> --box x0,y0,x1,y1 -o out

为什么不用 Pillow：很多交付环境（本机、CI、客户机）装不上或不该装三方库；
PNG 是公开格式，zlib 解码 + 手写滤镜还原就能读，写 PNG 更是几十行。
"""
import argparse
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import imgtool as I                                              # noqa: E402


def cmd_stats(args):
    print("%-46s %6s %6s %8s %8s" % ("图", "尺寸", "亮度", "主色数", "跳变"))
    for p in args.files:
        try:
            w, h, px = I.load_rgb(p)
        except Exception as e:                                   # noqa: BLE001
            print("%-46s 失败: %s" % (p, e))
            continue
        step = max(1, w // 400)
        n = sr = sg = sb = 0
        hist = {}
        jump = 0
        jn = 0
        for y in range(0, h, step):
            for x in range(0, w, step):
                o = (y * w + x) * 3
                r, g, b = px[o], px[o + 1], px[o + 2]
                sr += r
                sg += g
                sb += b
                n += 1
                k = (r >> 4, g >> 4, b >> 4)
                hist[k] = hist.get(k, 0) + 1
                if x + step < w:
                    o2 = (y * w + x + step) * 3
                    jump += abs(px[o2] - r) + abs(px[o2 + 1] - g)
                    jn += 1
        lum = (0.299 * sr + 0.587 * sg + 0.114 * sb) / n
        top = sorted(hist.items(), key=lambda kv: -kv[1])[:3]
        print("%-46s %4dx%-4d %6.1f %8d %8.2f  | %s"
              % (os.path.basename(p)[:46], w, h, lum, len(hist),
                 jump / max(1, jn),
                 " ".join("RGB(%d,%d,%d):%.0f%%"
                          % (k[0] * 16 + 8, k[1] * 16 + 8, k[2] * 16 + 8,
                             100.0 * v / n) for k, v in top)))
    print("\n读法：亮度 <40/255 说明整图挤在近黑区，任何显示端的暗部提升都会把"
          "量化台阶放大成可见色带；跳变低而主色数少 = 平滑区域已经块状化。")


def cmd_lift(args):
    table = [min(255, int(round(255.0 * ((i / 255.0) ** args.gamma))))
             for i in range(256)]
    w, h, px = I.load_rgb(args.file)
    out = bytes(table[v] for v in px)
    I.write_png(args.out, w, h, out)
    print("提亮后 %s (%dx%d, gamma=%.2f)" % (args.out, w, h, args.gamma))


def cmd_compare(args):
    items = []
    for p in args.files:
        w, h, px = I.load_rgb(p)
        if args.width and w != args.width:
            nh = max(1, int(round(h * args.width / w)))
            px = I.resize(w, h, px, args.width, nh)
            w, h = args.width, nh
        items.append((w, h, px))
    tw, th, out = I.vstack(items, pad=args.pad)
    I.write_png(args.out, tw, th, out)
    print("对照图 %s (%dx%d, %d 张)" % (args.out, tw, th, len(items)))


def cmd_bbox(args):
    x0, y0, x1, y1 = I.bbox_nonwhite(args.file, args.thresh)
    print("非白外接框: %d,%d,%d,%d  ->  %dx%d"
          % (x0, y0, x1, y1, x1 - x0, y1 - y0))


def cmd_resize(args):
    w, h, px = I.load_rgb(args.file)
    nh = max(1, int(round(h * args.width / w)))
    I.write_png(args.out, args.width, nh, I.resize(w, h, px, args.width, nh))
    print("%s -> %s (%dx%d)" % (args.file, args.out, args.width, nh))


def cmd_crop(args):
    w, h, px = I.load_rgb(args.file)
    x0, y0, x1, y1 = [int(v) for v in args.box.split(",")]
    I.write_png(args.out, x1 - x0, y1 - y0, I.crop(w, h, px, x0, y0, x1 - x0, y1 - y0))
    print("%s -> %s (%dx%d)" % (args.file, args.out, x1 - x0, y1 - y0))


def cmd_sheet(args):
    cols, cw = args.cols, args.width
    cells = []
    for p in args.files:
        w, h, px = I.load_rgb(p)
        nh = max(1, int(round(h * cw / w)))
        cells.append((cw, nh, I.resize(w, h, px, cw, nh)))
    rows = (len(cells) + cols - 1) // cols
    ch = max(c[1] for c in cells)
    gap = args.pad
    tw = cols * cw + (cols + 1) * gap
    th = rows * ch + (rows + 1) * gap
    canvas = bytearray(bytes((235, 235, 235)) * (tw * th))
    for n, (w, h, px) in enumerate(cells):
        r, c = divmod(n, cols)
        ox = gap + c * (cw + gap)
        oy = gap + r * (ch + gap)
        for j in range(h):
            src = j * w * 3
            dst = ((oy + j) * tw + ox) * 3
            canvas[dst:dst + w * 3] = px[src:src + w * 3]
    I.write_png(args.out, tw, th, bytes(canvas))
    print("联系表 %s (%dx%d, %d 张)" % (args.out, tw, th, len(cells)))


def main():
    ap = argparse.ArgumentParser(description="零依赖图片诊断/对照工具")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("stats", help="统计亮度/主色/跳变")
    p.add_argument("files", nargs="+")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("lift", help="模拟暗部提亮")
    p.add_argument("file")
    p.add_argument("--gamma", type=float, default=0.62)
    p.add_argument("-o", "--out", default="lifted.png")
    p.set_defaults(func=cmd_lift)

    p = sub.add_parser("compare", help="上下拼接对照")
    p.add_argument("files", nargs="+")
    p.add_argument("--width", type=int, default=900)
    p.add_argument("--pad", type=int, default=12)
    p.add_argument("-o", "--out", default="compare.png")
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("bbox", help="非白区域外接框")
    p.add_argument("file")
    p.add_argument("--thresh", type=int, default=235)
    p.set_defaults(func=cmd_bbox)

    p = sub.add_parser("resize", help="缩放另存")
    p.add_argument("file")
    p.add_argument("--width", type=int, required=True)
    p.add_argument("-o", "--out", default="resized.png")
    p.set_defaults(func=cmd_resize)

    p = sub.add_parser("crop", help="裁切另存")
    p.add_argument("file")
    p.add_argument("--box", required=True, help="x0,y0,x1,y1")
    p.add_argument("-o", "--out", default="cropped.png")
    p.set_defaults(func=cmd_crop)

    p = sub.add_parser("sheet", help="联系表")
    p.add_argument("files", nargs="+")
    p.add_argument("--cols", type=int, default=5)
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--pad", type=int, default=10)
    p.add_argument("-o", "--out", default="sheet.png")
    p.set_defaults(func=cmd_sheet)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
