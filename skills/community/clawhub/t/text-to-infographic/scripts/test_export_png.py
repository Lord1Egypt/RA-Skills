#!/usr/bin/env python3
"""test_export_png.py — PNG 导出链路测试。

三块：
  1. 手写 PNG 的解码往返（合成图 → decode → 像素一致）；
  2. content_height 测高逻辑（合成图：背景行 + 内容行）；
  3. 真机截图冒烟（本机有 Chrome 才跑，没有则 SKIP——不安装任何东西）。

用法: python3 scripts/test_export_png.py
"""
import os
import struct
import sys
import tempfile
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import export_png as EP                          # noqa: E402

PASS = FAIL = 0


def ok(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"✅ {name}")
    else:
        FAIL += 1
        print(f"❌ {name}  {detail}")


def make_png(width, height, pixel_fn, path):
    """合成 RGBA PNG（filter 0），pixel_fn(x, y) -> (r, g, b, a)。"""
    rows = b""
    for y in range(height):
        rows += b"\x00" + b"".join(
            bytes(pixel_fn(x, y)) for x in range(width))

    def chunk(ctype, body):
        c = ctype + body
        return struct.pack(">I", len(body)) + c + struct.pack(
            ">I", zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(rows))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)


def test_decode_roundtrip(tmp):
    W, H = 6, 4
    expect = {}
    path = os.path.join(tmp, "rt.png")

    def px(x, y):
        v = (x * 40 % 256, y * 60 % 256, (x + y) * 30 % 256, 255)
        expect[(x, y)] = v
        return v

    make_png(W, H, px, path)
    w, h, ch, data = EP.decode_png(path)
    ok("解码: 尺寸/通道", (w, h, ch) == (W, H, 4), f"got {(w, h, ch)}")
    same = all(
        tuple(data[(y * w + x) * ch:(y * w + x) * ch + ch]) == expect[(x, y)]
        for x in range(W) for y in range(H))
    ok("解码: 像素往返一致", same)


def test_content_height(tmp):
    W, H, BG, FG = 10, 50, (250, 247, 242, 255), (201, 111, 74, 255)
    path = os.path.join(tmp, "ch.png")

    make_png(W, H, lambda x, y: FG if y == 30 else BG, path)
    ok("测高: 单行内容 → y=30", EP.content_height(path) == 30)

    make_png(W, H, lambda x, y: FG if 20 <= y <= 35 else BG, path)
    ok("测高: 区块内容 → y=35", EP.content_height(path) == 35)

    make_png(W, H, lambda x, y: BG, path)
    # 纯背景（识别不出内容）→ 保底不裁剪，返回最后一行，宁可多留白不误裁
    ok("测高: 纯背景 → 不裁剪（保底）", EP.content_height(path) == H - 1,
       f"got {EP.content_height(path)}")


def test_live_screenshot(tmp):
    try:
        chrome = EP.find_chrome()
    except EP.ChromeMissing as e:
        print(f"⏭  真机截图跳过：{e.splitlines()[0]}")
        return
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html = os.path.join(here, "examples", "dashboard-demo.json")
    import subprocess
    out_html = os.path.join(tmp, "dash.html")
    subprocess.run([sys.executable, os.path.join(here, "scripts",
                   "render_infographic_html.py"), html, out_html],
                   check=True, stdout=subprocess.DEVNULL)
    out_png = os.path.join(tmp, "dash.png")
    path, h, _ = EP.export(out_html, out_png, chrome=chrome, verbose=False)
    import struct as _s
    d = open(path, "rb").read(33)
    w_px, h_px = _s.unpack(">II", d[16:24])
    ok("真机截图: 文件生成", os.path.getsize(path) > 10_000,
       f"size={os.path.getsize(path)}")
    ok("真机截图: 2x 密度", w_px == 852 * 2 and h_px == h * 2,
       f"got {w_px}x{h_px}, expect {852*2}x{h*2}")
    ok("真机截图: 高度合理", 400 <= h <= 6000, f"h={h}")


def main():
    import tempfile
    with tempfile.TemporaryDirectory(prefix="t2i-png-test-") as tmp:
        test_decode_roundtrip(tmp)
        test_content_height(tmp)
        test_live_screenshot(tmp)
    print(f"—— 通过: {PASS}  未通过: {FAIL}")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
