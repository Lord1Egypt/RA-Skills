import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import psutil
import pyperclip
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError

try:
    from PIL import ImageGrab
except Exception:  # optional dependency
    ImageGrab = None

try:
    import pytesseract
except Exception:  # optional dependency
    pytesseract = None

WECHAT_PATHS = [
    r"C:\Program Files\Tencent\WeChat\WeChat.exe",
    r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
]

DEFAULT_TARGET_CHAT = "文件传输助手"
DEFAULT_MESSAGE = "你好"
DEFAULT_LOG_DIR = Path(__file__).resolve().parent.parent / "wechat_automation_logs"


def parse_args():
    parser = argparse.ArgumentParser(description="打开微信、定位聊天并发送消息")
    parser.add_argument("--to", default=DEFAULT_TARGET_CHAT, help="目标聊天名称")
    parser.add_argument("--message", default=DEFAULT_MESSAGE, help="要发送的消息")
    parser.add_argument("--delay", type=float, default=1.5, help="UI 操作后的等待秒数")
    parser.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR), help="日志与截图输出目录")
    parser.add_argument("--dump-tree", action="store_true", help="打印并保存微信控件树")
    parser.add_argument("--no-screenshot", action="store_true", help="禁用失败截图")
    parser.add_argument("--verify-title", action="store_true", help="校验窗口标题里是否包含聊天名")
    parser.add_argument("--ocr-verify", action="store_true", help="发送后追加 OCR 校验（需安装 pytesseract）")
    return parser.parse_args()


def setup_logging(log_dir: Path):
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = log_dir / f"wechat-send-{ts}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )
    return log_file


def find_wechat_exe():
    for path in WECHAT_PATHS:
        if os.path.exists(path):
            return path
    return None


def is_wechat_running():
    for p in psutil.process_iter(["name", "exe"]):
        try:
            name = p.info["name"] or ""
            exe = p.info["exe"] or ""
            if "WeChat.exe" in name or exe.endswith("WeChat.exe"):
                return True
        except Exception:
            pass
    return False


def start_wechat():
    exe = find_wechat_exe()
    if not exe:
        raise FileNotFoundError("没找到 WeChat.exe，请手动修改 WECHAT_PATHS")
    subprocess.Popen([exe])
    logging.info("已启动微信，等待加载...")
    time.sleep(6)


def ensure_wechat():
    if not is_wechat_running():
        start_wechat()
    else:
        logging.info("微信已在运行")


def connect_wechat_window():
    for _ in range(12):
        try:
            app = Application(backend="uia").connect(path="WeChat.exe")
            win = app.top_window()
            win.set_focus()
            time.sleep(1)
            logging.info("已连接微信主窗口: %s", win.window_text())
            return win
        except Exception:
            time.sleep(1)
    raise RuntimeError("连接微信窗口失败，请确认微信已登录并显示主界面")


def dump_control_tree(win, log_dir: Path):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    tree_file = log_dir / f"wechat-control-tree-{ts}.txt"
    with tree_file.open("w", encoding="utf-8") as f:
        old_stdout = sys.stdout
        try:
            sys.stdout = f
            win.print_control_identifiers()
        finally:
            sys.stdout = old_stdout
    logging.info("已保存控件树: %s", tree_file)
    return tree_file


def save_screenshot(log_dir: Path, prefix: str):
    if ImageGrab is None:
        logging.warning("Pillow 未安装，无法截图")
        return None
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    img_path = log_dir / f"{prefix}-{ts}.png"
    try:
        img = ImageGrab.grab()
        img.save(img_path)
        logging.info("已保存截图: %s", img_path)
        return img_path
    except Exception as e:
        logging.warning("截图失败: %s", e)
        return None


def verify_message_sent_ocr(log_dir: Path, text: str):
    if ImageGrab is None:
        logging.warning("OCR 校验跳过：Pillow 未安装")
        return False, None, None
    if pytesseract is None:
        logging.warning("OCR 校验跳过：pytesseract 未安装")
        return False, None, None

    img_path = save_screenshot(log_dir, "wechat-send-ocr-check")
    if not img_path:
        return False, None, None

    try:
        img = ImageGrab.grab()
        ocr_text = pytesseract.image_to_string(img, lang="chi_sim+eng")
        matched = (text or "").strip() in (ocr_text or "")
        if matched:
            logging.info("OCR 校验通过：截图文本中检测到消息内容")
        else:
            logging.warning("OCR 校验未命中消息内容")
        return matched, img_path, ocr_text
    except Exception as e:
        logging.warning("OCR 校验失败: %s", e)
        return False, img_path, None


def try_find_search_box(win):
    candidates = [
        {"title_re": ".*搜索.*", "control_type": "Edit"},
        {"title_re": ".*Search.*", "control_type": "Edit"},
        {"control_type": "Edit", "found_index": 0},
        {"control_type": "Edit", "found_index": 1},
    ]

    for c in candidates:
        try:
            ctrl = win.child_window(**c)
            ctrl.wait("exists ready", timeout=2)
            logging.info("搜索框定位成功: %s", c)
            return ctrl
        except Exception:
            continue
    raise ElementNotFoundError("没找到搜索框")


def open_chat(win, chat_name: str, delay: float, verify_title: bool = False):
    search = try_find_search_box(win)
    search.click_input()
    time.sleep(0.5)
    search.type_keys("^a{BACKSPACE}", set_foreground=True)
    time.sleep(0.3)
    pyperclip.copy(chat_name)
    search.type_keys("^v", set_foreground=True)
    time.sleep(delay)
    search.type_keys("{ENTER}", set_foreground=True)
    time.sleep(delay)
    current_title = win.window_text()
    logging.info("已尝试打开聊天：%s；当前窗口标题：%s", chat_name, current_title)
    if verify_title and chat_name not in current_title:
        logging.warning("窗口标题未包含目标聊天名，可能需要进一步校验")


def try_find_input_box(win):
    candidates = [
        {"control_type": "Document"},
        {"control_type": "Edit", "found_index": 1},
        {"control_type": "Edit", "found_index": 2},
        {"control_type": "Pane", "found_index": 0},
    ]

    for c in candidates:
        try:
            ctrl = win.child_window(**c)
            ctrl.wait("exists ready", timeout=2)
            logging.info("消息输入框定位成功: %s", c)
            return ctrl
        except Exception:
            continue
    raise ElementNotFoundError("没找到消息输入框")


def collect_window_texts(win):
    texts = []
    try:
        for ctrl in win.descendants():
            try:
                text = (ctrl.window_text() or "").strip()
                if text:
                    texts.append(text)
            except Exception:
                continue
    except Exception:
        pass
    return texts


def verify_message_sent(win, text: str, attempts: int = 5, interval: float = 1.0):
    target = (text or "").strip()
    if not target:
        return False, []

    for idx in range(attempts):
        texts = collect_window_texts(win)
        if any(target in t for t in texts):
            logging.info("发送校验通过：在窗口文本中检测到消息内容")
            return True, texts
        logging.info("发送校验第 %s/%s 次未命中，继续等待...", idx + 1, attempts)
        time.sleep(interval)
    return False, texts if 'texts' in locals() else []


def send_message(win, text: str, delay: float):
    editor = try_find_input_box(win)
    editor.click_input()
    time.sleep(0.5)
    pyperclip.copy(text)
    editor.type_keys("^v", set_foreground=True)
    time.sleep(0.3)
    editor.type_keys("{ENTER}", set_foreground=True)
    time.sleep(delay)
    logging.info("已尝试发送消息：%s", text)
    return verify_message_sent(win, text)


def main():
    args = parse_args()
    log_dir = Path(args.log_dir)
    log_file = setup_logging(log_dir)
    logging.info("日志文件: %s", log_file)
    logging.info("运行参数: to=%s, message=%s", args.to, args.message)

    try:
        ensure_wechat()
        win = connect_wechat_window()

        if args.dump_tree:
            dump_control_tree(win, log_dir)

        open_chat(win, args.to, args.delay, args.verify_title)
        verified, texts = send_message(win, args.message, args.delay)
        ocr_verified = False
        if verified:
            logging.info("执行完成：消息已通过轻量校验")
        else:
            logging.warning("执行完成：消息已发送，但未通过聊天区文本校验")
            preview = " | ".join(texts[:20]) if texts else "<no texts captured>"
            logging.warning("当前窗口文本预览: %s", preview)

        if args.ocr_verify:
            ocr_verified, ocr_img, ocr_text = verify_message_sent_ocr(log_dir, args.message)
            if ocr_verified:
                logging.info("执行完成：OCR 校验也通过")
            else:
                logging.warning("执行完成：OCR 校验未通过")
                if ocr_img:
                    logging.warning("OCR 截图: %s", ocr_img)
                if ocr_text:
                    logging.warning("OCR 文本预览: %s", (ocr_text or "")[:300].replace("\n", " | "))

        logging.info("最终校验结果: text_verify=%s, ocr_verify=%s", verified, ocr_verified)
        logging.info("执行完成")
    except Exception as e:
        logging.exception("执行失败: %s", e)
        if not args.no_screenshot:
            save_screenshot(log_dir, "wechat-send-failed")
        raise


if __name__ == "__main__":
    main()
