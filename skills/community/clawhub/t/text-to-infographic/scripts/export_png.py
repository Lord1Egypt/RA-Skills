#!/usr/bin/env python3
"""export_png.py — 把渲染器产出的自包含 HTML 截成 PNG（可选能力）。

设计边界（与「安全渲染」契约一致）：
- **不安装任何东西**：只使用机器上已存在的 Chrome / Chromium / Edge，找不到就明确报错退出；
- **不改产物**：HTML 依旧是零 JS、零外链；测量高度由 Python 侧读像素完成，不往页面注入脚本；
- **纯标准库**：zlib + struct 手写 PNG 解码，仅用于测高；
- 失败不影响 HTML 主路径：调用方可以先拿到 HTML，再决定要不要图。

流程（两遍截图）：
  ① 用探测高度（默认 6000px）截一张 → 解码找出「最后一行有内容的 y」；
  ② 用测出的真实高度再截一张 → 得到无多余留白的成品。

用法:
    python3 export_png.py in.html out.png [--width 852] [--scale 2] [--chrome PATH]
    python3 export_png.py in.html out.png --height 1600    # 跳过测高，直接指定
"""
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib

# 页面宽度：.ig max-width 820 + body 左右 padding 16*2
DEFAULT_WIDTH = 852
DEFAULT_SCALE = 2
PROBE_HEIGHT = 2400          # 探测高度：绝大多数信息图 < 1200 CSS px
PROBE_HEIGHT_MAX = 9000      # 撑满时加高重探一次
MIN_HEIGHT = 240

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Arc.app/Contents/MacOS/Arc",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/microsoft-edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


class ChromeMissing(RuntimeError):
    pass


class ScreenshotFailed(RuntimeError):
    pass


def find_chrome(explicit=None):
    """按「显式参数 → 环境变量 → 常见安装路径 → PATH」顺序找浏览器，找不到抛 ChromeMissing。"""
    if explicit:
        if os.path.exists(explicit):
            return explicit
        raise ChromeMissing(f"--chrome 指定的路径不存在：{explicit}")
    env = os.environ.get("CHROME_PATH") or os.environ.get("CHROME_BIN")
    if env and os.path.exists(env):
        return env
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    raise ChromeMissing(
        "没找到可用的浏览器（Chrome / Chromium / Edge 都没装）。\n"
        "PNG 导出是可选的、且不会替你安装任何东西：\n"
        "  1) 装一个 Chrome，或\n"
        "  2) 用 --chrome /path/to/chrome 指定，或\n"
        "  3) 设环境变量 CHROME_PATH\n"
        "只要 HTML 的话，删掉 --png 即可，HTML 已经生成好了。")


# ---------------------------------------------------------------- PNG 解码（只为测高）
def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def decode_png(path):
    """解码 8-bit RGB/RGBA 非隔行 PNG，返回 (width, height, channels, 像素字节串)。"""
    data = open(path, "rb").read()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("不是 PNG 文件")
    pos, idat, width = 8, b"", None
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, depth, color, comp, filt, interlace = struct.unpack(">IIBBBBB", body)
            if depth != 8 or interlace != 0 or color not in (2, 6):
                raise ValueError(f"不支持的 PNG 格式 depth={depth} color={color} interlace={interlace}")
            channels = 3 if color == 2 else 4
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
    raw = zlib.decompress(idat)
    stride = width * channels
    out = bytearray(stride * height)
    prev = bytearray(stride)
    src = 0
    for y in range(height):
        ft = raw[src]
        src += 1
        line = bytearray(raw[src:src + stride])
        src += stride
        if ft == 0:
            pass
        elif ft == 1:                                  # Sub
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif ft == 2:                                  # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ft == 3:                                  # Average
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
        elif ft == 4:                                  # Paeth
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                c = prev[i - channels] if i >= channels else 0
                line[i] = (line[i] + _paeth(a, prev[i], c)) & 0xFF
        else:
            raise ValueError(
                f"未知 PNG 行过滤类型：{ft}（y={y}，raw前16字节={raw[:16].hex()}，"
                f"声明尺寸={width}x{height}，raw长度={len(raw)}，预期={height*(stride+1)}）")
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return width, height, channels, out


def content_height(png_path, bg_tolerance=6):
    """返回「最后一行含内容」的像素 y（0 起算，含）。用页面左上角像素作背景参考色。"""
    width, height, ch, px = decode_png(png_path)

    def rgb(x, y):
        i = (y * width + x) * ch
        return px[i], px[i + 1], px[i + 2]

    bg = rgb(0, 0)
    step = max(1, width // 220)                        # 抽样列，够用且快
    xs = list(range(0, width, step))
    for y in range(height - 1, -1, -1):
        row = y * width * ch
        for x in xs:
            i = row + x * ch
            if (abs(px[i] - bg[0]) > bg_tolerance or
                    abs(px[i + 1] - bg[1]) > bg_tolerance or
                    abs(px[i + 2] - bg[2]) > bg_tolerance):
                return y
    return height - 1


# ---------------------------------------------------------------- 截图
def _shoot(chrome, html_path, out_png, width, height, scale, no_sandbox=False):
    url = "file://" + os.path.abspath(html_path)
    cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--disable-extensions", "--no-first-run", "--no-default-browser-check",
           "--disable-background-networking", f"--force-device-scale-factor={scale}",
           f"--window-size={width},{height}", "--virtual-time-budget=800",
           f"--screenshot={out_png}", url]
    if no_sandbox:
        cmd.insert(2, "--no-sandbox")
    if os.path.exists(out_png):
        os.remove(out_png)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
    if not os.path.exists(out_png) or os.path.getsize(out_png) == 0:
        raise ScreenshotFailed(
            f"截图失败（退出码 {proc.returncode}）：\n"
            + proc.stderr.decode("utf-8", "ignore").strip()[-600:])


def export(html_path, out_png, width=DEFAULT_WIDTH, scale=DEFAULT_SCALE,
           chrome=None, height=None, verbose=True):
    chrome = find_chrome(chrome)
    tmpdir = tempfile.mkdtemp(prefix="ig-png-")
    probe = os.path.join(tmpdir, "probe.png")
    no_sandbox = False

    def shoot(target, h, s, note=""):
        """截图，失败时降级 --no-sandbox 重试一次（容器/CI 里 Chrome 常起不来）。
        一旦降级成功，本次运行后续截图都直接带 --no-sandbox，不再重复试错。"""
        nonlocal no_sandbox
        try:
            _shoot(chrome, html_path, target, width, h, s, no_sandbox=no_sandbox)
        except ScreenshotFailed:
            if no_sandbox:
                raise
            if verbose:
                print(f"… {note}首次截图失败，用 --no-sandbox 重试", file=sys.stderr)
            _shoot(chrome, html_path, target, width, h, s, no_sandbox=True)
            no_sandbox = True                       # 本次运行记住，后续不再试错

    try:
        if height:                                     # 手动指定高度：一次成型
            shoot(out_png, height, scale)
            return out_png, height, chrome

        # ① 探测高度：用 1x 缩放，图小、解码快（测量结果直接就是 CSS px）
        probe_h = PROBE_HEIGHT
        shoot(probe, probe_h, 1, "测高")
        try:
            bottom = content_height(probe)
        except Exception as e:                         # 解码失败不该阻断出图
            if verbose:
                print(f"… 自动测高失败（{e}），按探测高度输出", file=sys.stderr)
            shoot(out_png, probe_h, scale)
            return out_png, probe_h, chrome

        if bottom >= probe_h - 2:                      # 撑满了，加高再探一次
            probe_h = PROBE_HEIGHT_MAX
            shoot(probe, probe_h, 1, "加高测高")
            bottom = content_height(probe)
            if bottom >= probe_h - 2:                  # 真的到顶了，就用探测高度
                shoot(out_png, probe_h, scale)
                return out_png, probe_h, chrome

        need = max(MIN_HEIGHT, bottom + 3)             # +3px 留底边余量
        # ② 按真实高度、按目标缩放重截
        shoot(out_png, need, scale)
        return out_png, need, chrome
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    positional = [a for a in args if not a.startswith("--")]
    opts = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            opts[args[i]] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else True
        i += 1
    if len(positional) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    html_path, out_png = positional[0], positional[1]
    try:
        path, h, _ = export(
            html_path, out_png,
            width=int(opts.get("--width", DEFAULT_WIDTH)),
            scale=int(opts.get("--scale", DEFAULT_SCALE)),
            chrome=opts.get("--chrome") if isinstance(opts.get("--chrome"), str) else None,
            height=int(opts["--height"]) if "--height" in opts else None)
    except (ChromeMissing, ScreenshotFailed) as e:
        print(str(e), file=sys.stderr)
        sys.exit(3)
    print(f"OK -> {path}  ({h * int(opts.get('--scale', DEFAULT_SCALE))}px 高)")


if __name__ == "__main__":
    main()
