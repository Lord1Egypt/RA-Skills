#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""微信 GUI 批量下载：盲点开查看器 → 方向键翻页 → 关闭 → 滚一层（循环）
macOS + 微信桌面版 + 已开「辅助功能/屏幕录制」权限。
用法:
  python3 wx_download.py --hash <会话hash> --month 2026-10 --wxid wxid_xxx_yyy \
      [--key 124] [--rounds 30] [--max-rounds 60] [--interval 0.5] [--dry]
说明:
  --key 124 = 右(更晚) 适合图片；--key 123 = 左(更早) **视频只能用123**
  --dry     = 只打印计划不发事件
停止: 越界哨兵(邻月目录增长) / 连续3轮零增长 / 开不了查看器
"""
import os, sys, glob, time, argparse, subprocess
import Quartz
from Quartz import (CGEventPost, CGEventCreateKeyboardEvent,
                    CGEventCreateMouseEvent, CGEventCreateScrollWheelEvent,
                    CGPointMake, kCGHIDEventTap, kCGScrollEventUnitPixel,
                    kCGEventLeftMouseDown, kCGEventLeftMouseUp,
                    kCGEventMouseMoved, kCGMouseButtonLeft)

BASE = os.path.expanduser("~/Library/Containers/com.tencent.xinWeChat/"
                          "Data/Documents/xwechat_files")


def asy(s, timeout=25):
    r = subprocess.run(["osascript", "-e", s], capture_output=True, text=True, timeout=timeout)
    return (r.stdout + r.stderr).strip()


def viewer_open():
    return "图片和视频" in asy(
        'tell application "System Events" to tell process "WeChat" to get name of every window')


def raise_viewer():
    asy("""
    tell application "System Events" to tell process "WeChat"
      set hit to 0
      set i to 0
      repeat with w in windows
        set i to i + 1
        if (name of w) is "图片和视频" then set hit to i
      end repeat
      if hit > 0 then
        perform action "AXRaise" of (window hit)
        set frontmost to true
      end if
    end tell
    """)


def close_viewer():
    """ESC(53) 无效！必须走菜单 文件→关闭"""
    asy("""
    tell application "System Events" to tell process "WeChat"
      if exists menu item "关闭" of menu "文件" of menu bar 1 then
        click menu item "关闭" of menu "文件" of menu bar 1
      end if
    end tell
    """)


def main_window_frame():
    """主窗口 (x,y,w,h) pt，排除查看器；动态测量不硬编码"""
    out = asy("""
    tell application "System Events" to tell process "WeChat"
      set out to ""
      repeat with w in windows
        if (name of w) is not "图片和视频" then
          set p to position of w
          set s to size of w
          set out to out & (item 1 of p) & "," & (item 2 of p) & "," & \\
                 (item 1 of s) & "," & (item 2 of s) & ";"
        end if
      end repeat
      return out
    end tell
    """)
    best, area = None, 0
    for seg in out.split(";"):
        seg = seg.strip()
        if not seg:
            continue
        try:
            x, y, w, h = [int(v) for v in seg.split(",")]
        except ValueError:
            continue
        if w * h > area:
            best, area = (x, y, w, h), w * h
    return best


def key(code):
    for d in (True, False):
        CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, code, d))
        time.sleep(0.03)


def click(x, y):
    p = CGPointMake(float(x), float(y))
    for _ in range(3):
        CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventMouseMoved, p, 0))
        time.sleep(0.05)
    CGEventPost(kCGHIDEventTap,
                CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, p, kCGMouseButtonLeft))
    time.sleep(0.07)
    CGEventPost(kCGHIDEventTap,
                CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, p, kCGMouseButtonLeft))


def scroll(px):
    """负=更早。必须 pixel 单位——line 单位对微信 0% 有效"""
    CGEventPost(kCGHIDEventTap,
                CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitPixel, 1, int(px)))


def home_bottom():
    """Cmd+↓ 回底 + 正向滚动兜底，防止滚过头"""
    for d in (True, False):
        ev = CGEventCreateKeyboardEvent(None, 121, d)
        if d:
            ev.setFlags_(0x100000)      # cmdKey
        CGEventPost(kCGHIDEventTap, ev)
        time.sleep(0.04)
    scroll(6000)
    time.sleep(0.6)


def counts(img_dir, vid_dir, prev_dir):
    imgs = glob.glob(os.path.join(img_dir, "*.dat"))
    full = len([p for p in imgs if not p.endswith("_t.dat")])
    mp4 = len(glob.glob(os.path.join(vid_dir, "*.mp4")))
    guard = len(glob.glob(os.path.join(prev_dir, "*.dat"))) if prev_dir else 0
    return full, len(imgs), mp4, guard


def blind_spots(frame):
    """盲点网格（相对窗口比例）：窗口900x700 时 = x420/460/500/540, y200..620 步长70"""
    x, y, w, h = frame
    pts = []
    for i in range(7):
        fy = 0.126 + i * 0.100
        for fx in (0.397, 0.441, 0.486, 0.530):
            pts.append((round(x + fx * w), round(y + fy * h)))
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", required=True, help="会话 hash")
    ap.add_argument("--month", required=True, help="目标月份 YYYY-MM")
    ap.add_argument("--wxid", required=True, help="账号目录名 wxid_xxx_yyy")
    ap.add_argument("--key", type=int, default=124, choices=[123, 124],
                    help="124=右(图片) 123=左(视频唯一有效)")
    ap.add_argument("--rounds", type=int, default=30, help="每轮按方向键次数")
    ap.add_argument("--max-rounds", type=int, default=60)
    ap.add_argument("--interval", type=float, default=0.5, help="图片≥0.42 视频≥0.9")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    base = os.path.join(BASE, a.wxid)
    img_dir = os.path.join(base, "msg", "attach", a.hash, a.month, "Img")
    if not os.path.isdir(img_dir):
        raise SystemExit(f"目录不存在: {img_dir}\n先跑 wx_locate.py 确认 hash/month")
    vid_dir = os.path.join(base, "msg", "video", a.month)
    # 越界哨兵：上月目录（点到更早的图会写进去 → 立即停）
    y, m = a.month.split("-")
    prev_m = f"{y}-{int(m) - 1:02d}" if int(m) > 1 else f"{int(y) - 1}-12"
    prev_dir = os.path.join(base, "msg", "attach", a.hash, prev_m, "Img")
    if not os.path.isdir(prev_dir):
        prev_dir = None

    frame = main_window_frame()
    if not frame:
        raise SystemExit("找不到微信主窗口（先打开微信并切到目标会话）")
    print(f"窗口 frame={frame}  目标={a.month}  方向键={a.key}", flush=True)
    f0 = counts(img_dir, vid_dir, prev_dir)
    print(f"起点: full={f0[0]} dat={f0[1]} mp4={f0[2]} 哨兵={f0[3]}", flush=True)

    if a.dry:
        print("盲点网格样例:", blind_spots(frame)[:6])
        return

    stale = 0
    for rnd in range(a.max_rounds):
        if not viewer_open():
            for (px, py) in blind_spots(frame):
                click(px, py)
                time.sleep(0.42)
                if viewer_open():
                    print(f"  查看器已开 @({px},{py})", flush=True)
                    break
        if not viewer_open():
            print("  开不了查看器 → 回底重试", flush=True)
            home_bottom()
            stale += 1
            if stale >= 3:
                print("*** 连续3轮开不了，停止 ***", flush=True)
                break
            continue

        raise_viewer()
        time.sleep(0.8)
        for i in range(a.rounds):
            key(a.key)
            time.sleep(a.interval)
        close_viewer()
        time.sleep(0.8)

        f1 = counts(img_dir, vid_dir, prev_dir)
        d = tuple(f1[j] - f0[j] for j in range(4))
        print(f"第{rnd + 1}轮: full={f1[0]}(+{d[0]}) dat={f1[1]}(+{d[1]}) "
              f"mp4={f1[2]}(+{d[2]}) 哨兵={f1[3]}(+{d[3]})", flush=True)
        if prev_dir and d[3] > 0:
            print("*** 哨兵增长=越过月份边界，停止 ***", flush=True)
            break
        if sum(d[:3]) == 0:
            stale += 1
            if stale >= 3:
                print("*** 连续3轮零增长，停止 ***", flush=True)
                break
        else:
            stale = 0
        f0 = f1
        home_bottom()
        scroll(-900)
        time.sleep(1.0)

    f2 = counts(img_dir, vid_dir, prev_dir)
    print(f"结束: full {f0[0]}->{f2[0]}  mp4 {f0[2]}->{f2[2]}", flush=True)
    print("下一步: wx_decrypt.py 解密 → wx_verify.py 验收", flush=True)


if __name__ == "__main__":
    main()
