#!/usr/bin/env python3
"""
截图守护进程 — 核心后台服务
功能: 定时截屏 → 检测变化 → 获取窗口信息 → OCR 提取文字 → 写入结构化日志
"""

import os
import sys
import time
import json
import signal
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, DATA_DIR, PID_FILE, PAUSE_FILE
from ocr_processor import extract_text

# ── 全局状态 ──────────────────────────────────────────────

running = True


def _on_signal(sig, frame):
    global running
    running = False


signal.signal(signal.SIGTERM, _on_signal)
signal.signal(signal.SIGINT, _on_signal)

# ── 截图 ──────────────────────────────────────────────────


def take_screenshot(output_path: str) -> bool:
    """调用 macOS screencapture 截取全屏，保存为 JPEG"""
    try:
        subprocess.run(
            ["screencapture", "-x", "-t", "jpg", output_path],
            capture_output=True, timeout=10,
        )
        return os.path.exists(output_path)
    except Exception:
        return False


# ── 活跃窗口检测 ──────────────────────────────────────────


def get_active_window() -> tuple:
    """
    通过 AppleScript 获取当前前台应用名 + 窗口标题
    返回 (app_name, window_title)
    """
    script = '''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    tell application frontApp
        try
            set winTitle to name of front window
        on error
            set winTitle to ""
        end try
    end tell
    return frontApp & "|||" & winTitle
    '''
    try:
        r = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0:
            parts = r.stdout.strip().split("|||", 1)
            return (parts[0], parts[1] if len(parts) > 1 else "")
    except Exception:
        pass
    return ("Unknown", "")


# ── 变化检测 ──────────────────────────────────────────────


def _image_hash(path: str):
    """把图片缩到 16×16 灰度图，算出 256 位感知哈希"""
    try:
        from PIL import Image
        img = Image.open(path).resize((16, 16)).convert("L")
        pixels = list(img.getdata())
        avg = sum(pixels) / len(pixels)
        return tuple(1 if p > avg else 0 for p in pixels)
    except Exception:
        return None


def is_similar(h1, h2, threshold: float) -> bool:
    """比较两个哈希的相似度，threshold 是"相同比例"阈值（0~1）"""
    if h1 is None or h2 is None or len(h1) != len(h2):
        return False
    same = sum(a == b for a, b in zip(h1, h2))
    return (same / len(h1)) >= threshold


# ── 日志写入 ──────────────────────────────────────────────


def append_log(date_str: str, entry: dict):
    log_dir = os.path.join(DATA_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, f"{date_str}.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── 主循环 ────────────────────────────────────────────────


def main():
    config = load_config()
    interval = config["capture"]["interval_seconds"]
    smart = config["capture"]["smart_detect"]
    change_pct = config["capture"]["change_threshold"]
    blacklist = config["privacy"]["blacklist_apps"]
    ocr_on = config["ocr"]["enabled"]
    max_txt = config["ocr"]["max_text_length"]

    # 写 PID 文件供 service_manager 使用
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    prev_hash = None
    sim_threshold = 1.0 - (change_pct / 100.0)

    print(f"[screen-reviewer] 守护进程启动  PID={os.getpid()}  间隔={interval}s")

    while running:
        loop_start = time.time()
        try:
            # 1. 暂停检查
            if os.path.exists(PAUSE_FILE):
                time.sleep(interval)
                continue

            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H-%M-%S")

            # 2. 获取前台窗口
            app_name, win_title = get_active_window()

            # 3. 黑名单过滤
            if any(b.lower() in app_name.lower() for b in blacklist):
                time.sleep(interval)
                continue

            # 4. 截图
            shot_dir = os.path.join(DATA_DIR, "screenshots", date_str)
            os.makedirs(shot_dir, exist_ok=True)
            shot_path = os.path.join(shot_dir, f"{time_str}.jpg")

            if not take_screenshot(shot_path):
                time.sleep(interval)
                continue

            # 5. 智能变化检测：跳过几乎没变的帧
            if smart:
                cur_hash = _image_hash(shot_path)
                if is_similar(prev_hash, cur_hash, sim_threshold):
                    os.remove(shot_path)
                    time.sleep(interval)
                    continue
                prev_hash = cur_hash

            # 6. OCR 文字提取
            ocr_text = ""
            if ocr_on:
                ocr_text = extract_text(shot_path)
                if len(ocr_text) > max_txt:
                    ocr_text = ocr_text[:max_txt] + "..."

            # 7. 写日志
            entry = {
                "timestamp": now.isoformat(),
                "app": app_name,
                "window_title": win_title,
                "screenshot": f"screenshots/{date_str}/{time_str}.jpg",
                "ocr_text": ocr_text,
            }
            append_log(date_str, entry)

        except Exception as e:
            print(f"[screen-reviewer] 循环异常: {e}", file=sys.stderr)

        # 保证间隔稳定（扣除本次循环耗时）
        elapsed = time.time() - loop_start
        sleep_time = max(0, interval - elapsed)
        time.sleep(sleep_time)

    # 清理 PID 文件
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    print("[screen-reviewer] 守护进程已停止")


if __name__ == "__main__":
    main()
