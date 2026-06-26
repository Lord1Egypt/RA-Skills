import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import ImageGrab
from rapidocr_onnxruntime import RapidOCR
import uiautomation as auto
import win32api
import win32clipboard
import win32con
from pywinauto import Desktop
from pywinauto.keyboard import send_keys


WECHAT_TITLE_KEYWORDS = ("\u5fae\u4fe1", "Weixin")
SEARCH_BOX_NAMES = (
    "\u641c\u7d22",
    "\u641c\u7d22\uff1a\u8054\u7cfb\u4eba\u3001\u7fa4\u804a\u3001\u4f01\u4e1a",
)
DEFAULT_CONTACT = "\u6587\u4ef6\u4f20\u8f93\u52a9\u624b"
DEFAULT_SYSTEM_PROMPT = (
    "You are replying to a WeChat friend in Chinese. "
    "Keep the reply short, warm, natural, and context-aware. "
    "Do not mention being an AI. "
    "If the latest visible content mentions an image or video placeholder, "
    "respond honestly based only on the placeholder and the surrounding text."
)
DEFAULT_PREVIEW_SHOT = "wechat_latest_image_preview.png"
OCR_ENGINE = None


def configure_stdio():
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def raise_if_escape_pressed():
    if win32api.GetAsyncKeyState(win32con.VK_ESCAPE) & 0x8000:
        raise KeyboardInterrupt("ESC pressed")


def sleep_with_abort(seconds: float, step: float = 0.05):
    deadline = time.time() + max(0.0, seconds)
    while time.time() < deadline:
        raise_if_escape_pressed()
        time.sleep(min(step, max(0.0, deadline - time.time())))


def get_ocr_engine():
    global OCR_ENGINE
    if OCR_ENGINE is None:
        OCR_ENGINE = RapidOCR()
    return OCR_ENGINE


def launch_wechat(exe_path: str):
    subprocess.Popen([exe_path])


def iter_wechat_window_handles():
    seen = set()
    for backend in ("uia", "win32"):
        for win in Desktop(backend=backend).windows():
            title = (win.window_text() or "").strip()
            if not title:
                continue
            if not any(keyword in title for keyword in WECHAT_TITLE_KEYWORDS):
                continue
            handle = win.handle
            if handle in seen:
                continue
            seen.add(handle)
            yield handle, title


def is_usable_wechat_window(handle: int, title: str) -> bool:
    window = auto.ControlFromHandle(handle)
    if not window:
        return False

    if "WxTrayIconMessageWindow" in title:
        return False

    rect = window.BoundingRectangle
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    if width < 500 or height < 500:
        return False
    return True


def find_wechat_window(timeout: float = 8.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        raise_if_escape_pressed()
        for handle, title in iter_wechat_window_handles():
            window = auto.ControlFromHandle(handle)
            if not window:
                continue
            if is_usable_wechat_window(handle, title):
                return window
        sleep_with_abort(0.5)
    raise RuntimeError("WeChat main window was not found.")


def find_search_box(window):
    for name in SEARCH_BOX_NAMES:
        candidate = window.EditControl(Name=name)
        if candidate.Exists(0, 0):
            return candidate

    candidate = window.EditControl(AutomationId="SearchBox")
    if candidate.Exists(0, 0):
        return candidate

    for child in window.GetChildren():
        if child.ControlTypeName == "EditControl":
            return child
    raise RuntimeError("Unable to locate the WeChat search box.")


def open_clipboard_with_retry(retries: int = 10, delay: float = 0.1):
    last_error = None
    for _ in range(retries):
        try:
            win32clipboard.OpenClipboard()
            return
        except OSError as exc:
            last_error = exc
            time.sleep(delay)
    raise last_error or RuntimeError("Unable to open clipboard.")


def set_clipboard_text(text: str):
    open_clipboard_with_retry()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    finally:
        win32clipboard.CloseClipboard()


def get_clipboard_text() -> str:
    open_clipboard_with_retry()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
            return win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        return ""
    finally:
        win32clipboard.CloseClipboard()


def build_dropfiles_payload(paths):
    normalized = [os.path.abspath(path) for path in paths]
    payload = ("\0".join(normalized) + "\0\0").encode("utf-16le")
    header = struct.pack("IiiII", 20, 0, 0, 0, 1)
    return header + payload


def set_clipboard_files(paths):
    open_clipboard_with_retry()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(
            win32con.CF_HDROP,
            build_dropfiles_payload(paths),
        )
    finally:
        win32clipboard.CloseClipboard()


def open_chat(window, contact_name: str):
    raise_if_escape_pressed()
    if is_current_chat(window, contact_name):
        return
    try:
        search_box = find_search_box(window)
        search_box.Click(simulateMove=False)
        sleep_with_abort(0.3)
        search_box.SendKeys("{Ctrl}a{Del}", waitTime=0.1)
        sleep_with_abort(0.2)
        search_box.SendKeys(contact_name, interval=0.05, waitTime=0.1)
    except RuntimeError:
        send_keys("^f", pause=0.05)
        sleep_with_abort(0.6)
        send_keys("^a{DEL}", pause=0.05)
        sleep_with_abort(0.2)
        set_clipboard_text(contact_name)
        send_keys("^v", pause=0.05)
    sleep_with_abort(1.0)
    send_keys("{ENTER}", pause=0.05)
    sleep_with_abort(1.0)


def get_window_box(window):
    rect = window.BoundingRectangle
    return rect.left, rect.top, rect.right, rect.bottom


def get_relative_point(window, x_ratio: float, y_ratio: float):
    left, top, right, bottom = get_window_box(window)
    width = right - left
    height = bottom - top
    return (
        left + int(width * x_ratio),
        top + int(height * y_ratio),
    )


def get_history_capture_box(window):
    left, top, right, bottom = get_window_box(window)
    width = right - left
    height = bottom - top
    return (
        left + int(width * 0.33),
        top + int(height * 0.12),
        left + int(width * 0.96),
        top + int(height * 0.78),
    )


def get_chat_header_ocr_box(window):
    left, top, right, bottom = get_window_box(window)
    width = right - left
    height = bottom - top
    return (
        left + int(width * 0.36),
        top + int(height * 0.02),
        left + int(width * 0.86),
        top + int(height * 0.11),
    )


def get_recent_chat_ocr_box(window):
    left, top, right, bottom = get_window_box(window)
    width = right - left
    height = bottom - top
    return (
        left + int(width * 0.34),
        top + int(height * 0.48),
        left + int(width * 0.96),
        top + int(height * 0.82),
    )


def grab_image(box, retries: int = 3, delay: float = 0.2):
    last_error = None
    for _ in range(retries):
        raise_if_escape_pressed()
        try:
            return ImageGrab.grab(box)
        except OSError as exc:
            last_error = exc
            sleep_with_abort(delay)
    raise last_error or RuntimeError("Unable to capture the screen region.")


def capture_box_sha1(box) -> str:
    return hashlib.sha1(grab_image(box).tobytes()).hexdigest()


def capture_window(window, output_path: str):
    image = grab_image(get_window_box(window))
    image.save(output_path)
    return output_path


def find_message_box(window):
    edit_controls = []
    for child in window.GetChildren():
        if child.ControlTypeName == "EditControl":
            edit_controls.append(child)

    if not edit_controls:
        raise RuntimeError("Unable to locate the WeChat message input box.")

    for control in reversed(edit_controls):
        name = (getattr(control, "Name", "") or "").strip()
        if "\u641c\u7d22" not in name:
            return control
    return edit_controls[-1]


def focus_message_box(window):
    try:
        message_box = find_message_box(window)
        message_box.Click(simulateMove=False)
        sleep_with_abort(0.2)
        return
    except RuntimeError:
        pass

    x, y = get_relative_point(window, 0.68, 0.92)
    auto.Click(x, y)
    sleep_with_abort(0.3)


def focus_chat_history(window):
    x, y = get_relative_point(window, 0.72, 0.42)
    auto.Click(x, y)
    sleep_with_abort(0.3)


def ensure_chat_scrolled_to_bottom(window, max_passes: int = 6) -> bool:
    focus_chat_history(window)
    history_box = get_history_capture_box(window)
    track_x, drag_start_y = get_relative_point(window, 0.985, 0.36)
    _, drag_end_y = get_relative_point(window, 0.985, 0.90)

    previous_hash = capture_box_sha1(history_box)
    raise_if_escape_pressed()
    auto.DragDrop(
        track_x,
        drag_start_y,
        track_x,
        drag_end_y,
        moveSpeed=0.25,
        waitTime=0.25,
    )
    sleep_with_abort(0.25)

    for _ in range(max_passes):
        raise_if_escape_pressed()
        auto.SetCursorPos(track_x, drag_end_y)
        auto.WheelDown(2)
        sleep_with_abort(0.2)
        current_hash = capture_box_sha1(history_box)
        if current_hash == previous_hash:
            return True
        previous_hash = current_hash

    return False


def send_message(window, message: str):
    message = (message or "").strip()
    if not message:
        return

    raise_if_escape_pressed()
    focus_message_box(window)
    set_clipboard_text(message)
    send_keys("^v", pause=0.05)
    sleep_with_abort(0.2)
    send_keys("{ENTER}", pause=0.05)


def send_files(window, file_paths):
    if not file_paths:
        return

    raise_if_escape_pressed()
    focus_message_box(window)
    set_clipboard_files(file_paths)
    send_keys("^v", pause=0.05)
    sleep_with_abort(1.2)
    send_keys("{ENTER}", pause=0.05)
    sleep_with_abort(1.0)


def clean_chat_lines(chat_text: str, max_lines: int) -> str:
    cleaned = []
    for raw_line in chat_text.splitlines():
        line = raw_line.replace("\ufeff", "").strip()
        if line and is_high_signal_line(line):
            cleaned.append(line)
    if max_lines > 0:
        cleaned = cleaned[-max_lines:]
    return "\n".join(cleaned)


def is_high_signal_line(line: str) -> bool:
    signal_count = sum(
        ch.isalnum() or ("\u4e00" <= ch <= "\u9fff")
        for ch in line
    )
    if line and signal_count == 0 and len(line) > 3:
        return False
    return bool(line)


def is_probably_time_line(line: str) -> bool:
    value = (line or "").strip()
    if not value:
        return False
    patterns = (
        r"^\d{1,2}:\d{2}$",
        r"^(昨天|今天|星期.)\s*\d{1,2}:\d{2}$",
        r"^(上午|下午|晚上|凌晨)?\s*\d{1,2}:\d{2}$",
    )
    return any(re.fullmatch(pattern, value) for pattern in patterns)


def extract_latest_message(chat_text: str) -> str:
    lines = [line.strip() for line in chat_text.splitlines() if line.strip()]
    latest = []
    for line in reversed(lines):
        if is_probably_time_line(line):
            if latest:
                break
            continue
        if latest:
            latest.append(line)
            continue
        latest.append(line)

    latest.reverse()
    if len(latest) > 1 and latest[0] in {"你好", "在吗", "哈喽", "hello", "Hello"}:
        latest = latest[1:]
    return "\n".join(latest).strip()


def extract_latest_incoming_message_by_ocr(window) -> str:
    entries, image_width = read_recent_chat_entries_by_ocr(window)
    if not entries:
        return ""

    side_boundary = image_width * 0.58
    latest = []
    collecting = False

    for entry in reversed(entries):
        text = entry["text"].strip()
        if not text:
            continue
        if is_probably_time_line(text):
            if collecting:
                break
            continue

        is_incoming = entry["x"] < side_boundary
        if not collecting:
            if not is_incoming:
                continue
            collecting = True
            latest.append(text)
            continue

        if not is_incoming:
            break
        latest.append(text)

    latest.reverse()
    if len(latest) > 1 and latest[0] in {"你好", "在吗", "哈喽", "hello", "Hello"}:
        latest = latest[1:]
    return "\n".join(latest).strip()


def read_latest_incoming_message(window, attempts: int = 2) -> str:
    for _ in range(attempts):
        raise_if_escape_pressed()
        latest = extract_latest_incoming_message_by_ocr(window)
        if latest:
            return latest
        sleep_with_abort(0.15)
    return ""


def merge_ocr_line_entries(ocr_result, y_threshold: float = 24.0):
    lines = []
    items = []
    for quad, text, score in ocr_result or []:
        text = (text or "").strip()
        if not text:
            continue
        center_x = sum(point[0] for point in quad) / 4.0
        center_y = sum(point[1] for point in quad) / 4.0
        items.append((center_y, center_x, text, score))

    items.sort()
    for center_y, center_x, text, score in items:
        if not lines or abs(center_y - lines[-1]["y"]) > y_threshold:
            lines.append({"y": center_y, "parts": [(center_x, text)], "score": score})
            continue
        lines[-1]["parts"].append((center_x, text))
        lines[-1]["score"] = min(lines[-1]["score"], score)

    merged = []
    for line in lines:
        ordered_parts = sorted(line["parts"])
        text = " ".join(part for _, part in ordered_parts).strip()
        x_positions = [position for position, _ in ordered_parts]
        merged.append(
            {
                "text": text,
                "x": min(x_positions) if x_positions else 0.0,
                "y": line["y"],
            }
        )
    return merged


def read_recent_chat_entries_by_ocr(window, screenshot_path: str | None = None):
    ensure_chat_scrolled_to_bottom(window)
    box = get_recent_chat_ocr_box(window)
    image = grab_image(box)
    if screenshot_path:
        image.save(screenshot_path)

    ocr_result, _ = get_ocr_engine()(image)
    entries = [
        entry
        for entry in merge_ocr_line_entries(ocr_result)
        if is_high_signal_line(entry["text"])
    ]
    return entries, image.width


def read_recent_chat_by_ocr(window, max_lines: int = 12, screenshot_path: str | None = None) -> str:
    entries, _ = read_recent_chat_entries_by_ocr(window, screenshot_path=screenshot_path)
    merged_lines = [entry["text"] for entry in entries]
    return clean_chat_lines("\n".join(merged_lines), max_lines)


def read_chat_header_by_ocr(window) -> str:
    image = grab_image(get_chat_header_ocr_box(window))
    ocr_result, _ = get_ocr_engine()(image)
    merged_lines = merge_ocr_line_entries(ocr_result, y_threshold=18.0)
    return " ".join(part["text"].strip() for part in merged_lines if part["text"].strip()).strip()


def is_current_chat(window, contact_name: str) -> bool:
    header_text = read_chat_header_by_ocr(window)
    if not header_text:
        return False
    return contact_name.casefold() in header_text.casefold()


def read_recent_chat(window, max_lines: int = 12, attempts: int = 3) -> str:
    for _ in range(attempts):
        raise_if_escape_pressed()
        chat_text = read_recent_chat_by_ocr(window, max_lines=max_lines)
        if chat_text:
            return chat_text
        sleep_with_abort(0.2)
    return ""


def infer_latest_image_side(chat_text: str, contact_name: str) -> str:
    lines = [line.strip() for line in chat_text.splitlines() if line.strip()]
    for line in reversed(lines):
        if "[图片]" not in line:
            continue
        if line.startswith(f"{contact_name}:"):
            return "incoming"
        if line.startswith("我:") or line.startswith("Me:"):
            return "outgoing"
    return "incoming"


def detect_preview_opened(window, baseline_bytes: bytes, threshold: int = 200000) -> bool:
    current_bytes = grab_image(get_window_box(window)).tobytes()
    delta = sum(left != right for left, right in zip(baseline_bytes, current_bytes))
    return delta >= threshold


def open_latest_image_preview(window, side: str = "incoming") -> bool:
    baseline = grab_image(get_window_box(window)).tobytes()
    candidate_sets = {
        "incoming": [
            (0.48, 0.58),
            (0.54, 0.58),
            (0.43, 0.64),
            (0.48, 0.64),
            (0.54, 0.64),
            (0.48, 0.70),
        ],
        "outgoing": [
            (0.72, 0.58),
            (0.78, 0.58),
            (0.84, 0.58),
            (0.72, 0.64),
            (0.78, 0.64),
            (0.84, 0.64),
        ],
    }

    for x_ratio, y_ratio in candidate_sets.get(side, candidate_sets["incoming"]):
        raise_if_escape_pressed()
        x, y = get_relative_point(window, x_ratio, y_ratio)
        auto.Click(x, y, waitTime=0.1)
        sleep_with_abort(0.15)
        auto.Click(x, y, waitTime=0.1)
        sleep_with_abort(0.6)
        if detect_preview_opened(window, baseline):
            return True
        send_keys("{ESC}", pause=0.05)
        sleep_with_abort(0.25)

    return False


def capture_latest_image_preview(window, contact_name: str, output_path: str, chat_text: str = "") -> str:
    ensure_chat_scrolled_to_bottom(window)
    chat_text = chat_text or read_recent_chat(window, max_lines=20)
    side = infer_latest_image_side(chat_text, contact_name)
    if not open_latest_image_preview(window, side=side):
        raise RuntimeError("Unable to open the latest image preview.")

    sleep_with_abort(0.5)
    capture_window(window, output_path)
    send_keys("{ESC}", pause=0.05)
    sleep_with_abort(0.3)
    return output_path


def resolve_output_path(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        raw = DEFAULT_PREVIEW_SHOT
    return str(Path(raw).expanduser().resolve())


def read_text_file(path_value: str) -> str:
    path = Path(path_value).expanduser().resolve()
    return path.read_text(encoding="utf-8").strip()


def compute_signature(text: str) -> str:
    if not text:
        return ""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def normalize_endpoint(base_url: str) -> str:
    base = (base_url or "").strip()
    if not base:
        base = "https://api.openai.com/v1"
    base = base.rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    if not base.endswith("/v1"):
        base = base + "/v1"
    return base + "/chat/completions"


def extract_response_text(payload) -> str:
    choices = payload.get("choices") or []
    if not choices:
        return ""

    message = choices[0].get("message") or {}
    content = message.get("content", "")
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append((item.get("text") or "").strip())
        return "\n".join(part for part in parts if part).strip()

    return ""


def request_llm_reply(
    transcript: str,
    contact: str,
    api_key: str,
    api_base: str,
    model: str,
    system_prompt: str,
) -> str:
    if not api_key:
        raise RuntimeError("Missing API key. Set OPENAI_API_KEY or pass --api-key.")
    if not model:
        raise RuntimeError("Missing model name. Set OPENAI_MODEL or pass --model.")

    prompt = (
        f"Contact: {contact}\n"
        "Recent visible WeChat transcript:\n"
        f"{transcript}\n\n"
        "Write the next reply message only. "
        "Do not add quotes, prefixes, or explanations."
    )
    body = {
        "model": model,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }

    request = urllib.request.Request(
        normalize_endpoint(api_base),
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM request failed: {exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    reply = extract_response_text(payload).strip()
    if not reply:
        raise RuntimeError("LLM returned an empty reply.")
    return reply


def collect_file_paths(values):
    file_paths = []
    for value in values:
        if not value:
            continue
        full_path = os.path.abspath(value)
        if not os.path.exists(full_path):
            raise FileNotFoundError(full_path)
        file_paths.append(full_path)
    return file_paths


def smart_reply_loop(window, args):
    api_key = args.api_key or os.getenv("OPENAI_API_KEY", "")
    api_base = args.api_base or os.getenv("OPENAI_BASE_URL", "")
    model = args.model or os.getenv("OPENAI_MODEL", "")

    last_snapshot = read_recent_chat(window, args.history_lines)
    last_signature = compute_signature(last_snapshot)
    print(
        f'Watching "{args.contact}" every {args.poll_seconds:.1f}s. '
        "Press Ctrl+C to stop.",
        flush=True,
    )

    while True:
        sleep_with_abort(args.poll_seconds)
        current_snapshot = read_recent_chat(window, args.history_lines)
        current_signature = compute_signature(current_snapshot)
        if not current_signature or current_signature == last_signature:
            continue

        reply = request_llm_reply(
            transcript=current_snapshot,
            contact=args.contact,
            api_key=api_key,
            api_base=api_base,
            model=model,
            system_prompt=args.system_prompt,
        )
        send_message(window, reply)
        print(f'AUTO_REPLY: contact="{args.contact}" reply="{reply}"', flush=True)

        sleep_with_abort(1.0)
        refreshed_snapshot = read_recent_chat(window, args.history_lines)
        last_signature = compute_signature(refreshed_snapshot) or current_signature


def build_parser():
    parser = argparse.ArgumentParser(
        description="Send WeChat text/media and optionally auto-reply to a friend.",
    )
    parser.add_argument("--contact", default=DEFAULT_CONTACT, help="Contact or chat name.")
    parser.add_argument("--message", default="", help="Text message to send.")
    parser.add_argument(
        "--message-file",
        help="UTF-8 text file containing the message to send. Overrides --message.",
    )
    parser.add_argument("--image", action="append", default=[], help="Image path to send.")
    parser.add_argument("--video", action="append", default=[], help="Video path to send.")
    parser.add_argument("--file", action="append", default=[], help="Generic file path to send.")
    parser.add_argument(
        "--smart-reply",
        action="store_true",
        help="Watch the current chat and auto-reply with an LLM.",
    )
    parser.add_argument(
        "--read-chat",
        action="store_true",
        help="Print the recent visible chat text and exit unless --smart-reply is also set.",
    )
    parser.add_argument(
        "--read-latest",
        action="store_true",
        help="Print only the latest extracted message block from OCR.",
    )
    parser.add_argument(
        "--read-latest-incoming",
        action="store_true",
        help="Print only the latest incoming message block from OCR.",
    )
    parser.add_argument(
        "--capture-latest-image",
        action="store_true",
        help="Open the latest visible image in chat, capture the preview, then close it.",
    )
    parser.add_argument(
        "--preview-output",
        default=DEFAULT_PREVIEW_SHOT,
        help="Output path used by --capture-latest-image.",
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=5.0,
        help="Polling interval used by --smart-reply.",
    )
    parser.add_argument(
        "--history-lines",
        type=int,
        default=12,
        help="Visible chat lines passed to the LLM.",
    )
    parser.add_argument(
        "--system-prompt",
        default=DEFAULT_SYSTEM_PROMPT,
        help="System prompt used for --smart-reply.",
    )
    parser.add_argument("--api-key", help="LLM API key. Defaults to OPENAI_API_KEY.")
    parser.add_argument(
        "--api-base",
        help="LLM base URL. Defaults to OPENAI_BASE_URL or https://api.openai.com/v1.",
    )
    parser.add_argument("--model", help="LLM model name. Defaults to OPENAI_MODEL.")
    parser.add_argument(
        "--exe",
        help="Path to WeChat.exe. Used only if the window is not already open.",
    )
    return parser


def main():
    configure_stdio()
    parser = build_parser()
    args = parser.parse_args()

    outbound_message = read_text_file(args.message_file) if args.message_file else args.message
    outbound_files = collect_file_paths(args.image + args.video + args.file)
    auto.SetGlobalSearchTimeout(3)

    try:
        try:
            window = find_wechat_window()
        except RuntimeError:
            if not args.exe:
                raise
            launch_wechat(args.exe)
            sleep_with_abort(3.0)
            window = find_wechat_window(timeout=15.0)

        window.SetActive()
        sleep_with_abort(0.8)
        open_chat(window, args.contact)
        latest_chat_text = ""

        if args.read_chat or args.read_latest:
            latest_chat_text = read_recent_chat(window, args.history_lines)
            if args.read_chat:
                print(f'CHAT: contact="{args.contact}"\n{latest_chat_text}')
            if args.read_latest:
                latest_message = extract_latest_message(latest_chat_text)
                print(f'LATEST: contact="{args.contact}"\n{latest_message}')
            if (
                not args.smart_reply
                and not outbound_message
                and not outbound_files
                and not args.capture_latest_image
                and not args.read_latest_incoming
            ):
                return 0

        if args.read_latest_incoming:
            latest_incoming = read_latest_incoming_message(window)
            print(f'LATEST_INCOMING: contact="{args.contact}"\n{latest_incoming}')
            if (
                not args.smart_reply
                and not outbound_message
                and not outbound_files
                and not args.capture_latest_image
            ):
                return 0

        if args.capture_latest_image:
            preview_path = resolve_output_path(args.preview_output)
            capture_latest_image_preview(
                window,
                contact_name=args.contact,
                output_path=preview_path,
                chat_text=latest_chat_text,
            )
            print(f'IMAGE_PREVIEW: contact="{args.contact}" path="{preview_path}"')
            if not args.smart_reply and not outbound_message and not outbound_files:
                return 0

        if outbound_message:
            send_message(window, outbound_message)

        if outbound_files:
            send_files(window, outbound_files)

        if args.smart_reply:
            smart_reply_loop(window, args)

    except KeyboardInterrupt:
        print("Stopped by user.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        f'SENT: contact="{args.contact}" '
        f'message={"yes" if bool(outbound_message) else "no"} '
        f'files={len(outbound_files)}'
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
