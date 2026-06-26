import sys, json, urllib.request, socket, base64, os, struct, urllib.parse, re, time
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)
DEBUG_PORT = os.environ.get("_WANGDA_DEBUG_PORT")
DOC_DUMP_DIR = os.environ.get("_WANGDA_DOC_DUMP_DIR")
import subprocess


class NeedLoginError(Exception):
    """需要登录的异常"""

    pass


def read_ws_frame(sock):
    header = sock.recv(2)
    if not header:
        return None
    opcode = header[0] & 0x0F
    payload_len = header[1] & 0x7F

    if payload_len == 126:
        payload_len = struct.unpack("!H", sock.recv(2))[0]
    elif payload_len == 127:
        payload_len = struct.unpack("!Q", sock.recv(8))[0]

    payload = b""
    while len(payload) < payload_len:
        chunk = sock.recv(min(4096, payload_len - len(payload)))
        if not chunk:
            break
        payload += chunk

    return opcode, payload


def send_cdp_message(ws_url, method, params, wait_for_response=False):
    url_parts = urllib.parse.urlparse(ws_url)
    host, port, path = url_parts.hostname, url_parts.port, url_parts.path
    if not path:
        path = "/"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    key = base64.b64encode(os.urandom(16)).decode("utf-8")
    handshake = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    sock.sendall(handshake.encode("utf-8"))

    resp = sock.recv(4096)
    if b"101 " not in resp:
        raise Exception("WebSocket handshake failed")

    msg = json.dumps({"id": 1, "method": method, "params": params}).encode("utf-8")
    header = bytearray([0x81])
    if len(msg) <= 125:
        header.append(len(msg) | 0x80)
    else:
        header.append(126 | 0x80)
        header.extend(struct.pack("!H", len(msg)))

    mask = os.urandom(4)
    header.extend(mask)

    masked_msg = bytearray(msg)
    for i in range(len(msg)):
        masked_msg[i] ^= mask[i % 4]

    sock.sendall(header + masked_msg)

    if not wait_for_response:
        time.sleep(0.1)
        sock.close()
        return None

    while True:
        frame = read_ws_frame(sock)
        if not frame:
            break
        opcode, payload = frame
        if opcode == 1:
            try:
                data = json.loads(payload.decode("utf-8"))
                if data.get("id") == 1:
                    sock.close()
                    return data
            except:
                pass
    sock.close()
    return None


def get_ws_url(port, tab_idx=0):
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/json") as response:
            pages = json.loads(response.read().decode())
        pages = [p for p in pages if p.get("type") == "page"]
        if not pages or tab_idx < 0 or tab_idx >= len(pages):
            return None
        return pages[tab_idx].get("webSocketDebuggerUrl")
    except Exception as e:
        print(f"Error fetching pages: {e}")
        return None


def kill_chrome():
    user_data_dir = os.environ.get("_WANGDA_USER_DATA_DIR")
    print("Closing existing Chrome instance (if any)...")
    subprocess.run(
        ["pkill", "-if", f"chrome.*user-data-dir={user_data_dir}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)


def start(url="https://wangda.chinamobile.com/#/home"):

    user_data_dir = os.environ.get("_WANGDA_USER_DATA_DIR")
    chrome_path = os.environ.get("_WANGDA_CHROME_PATH")
    if not user_data_dir or not DEBUG_PORT:
        print(
            "Error: Missing _WANGDA_USER_DATA_DIR or _WANGDA_DEBUG_PORT environment variables."
        )
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    ext_dir = os.path.join(script_dir, "stealth-extension")

    kill_chrome()

    # 使用open命令启动Chrome（macOS）
    cmd_args = [
        "open",
        "-na",
        chrome_path or "Google Chrome",
        "--args",
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={user_data_dir}",
        "--disable-blink-features=AutomationControlled",
        "--exclude-switches=enable-automation",
        f"--load-extension={ext_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        url,
    ]

    print(f"Starting Google Chrome (Port: {DEBUG_PORT}) ...")
    subprocess.run(cmd_args)
    print("Chrome started.")


def navi(url, tab_idx=0, wait_for_response=True, auto_start=True):
    """
    导航到指定url

    Args:
        url: 要导航到的URL
        tab_idx: tab索引，默认0
        wait_for_response: 是否等待响应，默认True
        auto_start: 如果Chrome未启动是否自动启动，默认True

    Returns:
        如果wait_for_response为True，返回响应数据；否则返回None

    Raises:
        NeedLoginError: 如果导航后需要登录
    """
    if not DEBUG_PORT:
        print("Error: _WANGDA_DEBUG_PORT environment variable is not set.")
        sys.exit(1)

    ws_url = get_ws_url(DEBUG_PORT, tab_idx)

    # 如果Chrome未启动且允许自动启动，则启动Chrome
    if not ws_url and auto_start:
        print("Chrome 未启动，正在启动...")
        start(url=url)
        # 等待Chrome完全启动
        for i in range(10):
            time.sleep(1)
            ws_url = get_ws_url(DEBUG_PORT, tab_idx)
            if ws_url:
                print("Chrome 启动成功。")
                break
        else:
            print("Error: Chrome 启动超时。")
            raise Exception("Chrome 启动超时。")

    if not ws_url:
        print(f"Error: Could not find webSocketDebuggerUrl for tab {tab_idx}")
        raise Exception(f"Could not find webSocketDebuggerUrl for tab {tab_idx}")

    try:
        response = send_cdp_message(
            ws_url, "Page.navigate", {"url": url}, wait_for_response=wait_for_response
        )

        if wait_for_response:
            if response is None:
                print("Error: No response received from Chrome.")
                sys.exit(1)

            if "error" in response:
                print(f"Navigation failed: {response['error']}")
                sys.exit(1)

            if "result" in response:
                print(f"Navigation started successfully.")

                # 等待页面加载完成，然后检查是否需要登录
                time.sleep(2)  # 等待页面跳转完成
                current_url = _get_current_url_silent(tab_idx)
                if current_url and current_url.startswith(
                    "https://wangda.chinamobile.com/oauth/#login"
                ):
                    print("检测到需要登录")
                    raise NeedLoginError("导航到需要登录的页面，请先登录")

                return response["result"]

        print("Navigation command sent successfully.")
        return True

    except Exception as e:
        print(f"Navigation failed: {e}")
        raise e


def _get_current_url_silent(tab_idx=0):
    """静默获取当前tab的URL（不打印输出）"""
    if not DEBUG_PORT:
        return None

    try:
        with urllib.request.urlopen(f"http://localhost:{DEBUG_PORT}/json") as response:
            pages = json.loads(response.read().decode())
        pages = [p for p in pages if p.get("type") == "page"]
        if not pages or tab_idx < 0 or tab_idx >= len(pages):
            return None
        return pages[tab_idx].get("url")
    except Exception:
        return None


def get_url(tab_idx=0):
    """获取当前tab的url"""
    if not DEBUG_PORT:
        print("Error: _WANGDA_DEBUG_PORT environment variable is not set.")
        sys.exit(1)

    try:
        with urllib.request.urlopen(f"http://localhost:{DEBUG_PORT}/json") as response:
            pages = json.loads(response.read().decode())
        pages = [p for p in pages if p.get("type") == "page"]
        if not pages or tab_idx < 0 or tab_idx >= len(pages):
            print(
                f"Error: Tab index {tab_idx} out of range (total pages: {len(pages)})"
            )
            sys.exit(1)
        url = pages[tab_idx].get("url")
        print(url)
        return url
    except Exception as e:
        print(f"Error fetching tab url: {e}")
        sys.exit(1)


def is_need_login(tab_idx=0):
    """判断是否需要登录"""
    url = get_url(tab_idx)
    if url.startswith("https://wangda.chinamobile.com/oauth/#login"):
        print("true")
        return True
    print("false")
    return False


def dump_page(tab_idx=0):
    """dump当前页面内容(json格式)"""
    if not DEBUG_PORT:
        print("Error: _WANGDA_DEBUG_PORT environment variable is not set.")
        sys.exit(1)

    ws_url = get_ws_url(DEBUG_PORT, tab_idx)
    if not ws_url:
        print(f"Error: Could not find webSocketDebuggerUrl for tab {tab_idx}")
        sys.exit(1)

    response = send_cdp_message(
        ws_url, "DOM.getDocument", {"depth": -1}, wait_for_response=True
    )
    if response:
        print("Document retrieved successfully.")

        doc_dump_dir = os.environ.get("_WANGDA_DOC_DUMP_DIR")
        if not doc_dump_dir:
            print("Error: _WANGDA_DOC_DUMP_DIR environment variable is not set.")
            sys.exit(1)

        os.makedirs(doc_dump_dir, exist_ok=True)
        dump_path = os.path.join(doc_dump_dir, f"document_tab{tab_idx}.json")

        with open(dump_path, "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=2)

        print(dump_path)
        return dump_path
    else:
        print("Failed to get document.")
        sys.exit(1)


def close_pop_window(tab_idx=0):
    """
    关闭页面上的弹窗（如学习报告弹窗、推广弹窗等）

    使用多种策略尝试关闭弹窗，兼容性高：
    1. 点击带 close 相关 class/id 的元素
    2. 点击遮罩层（overlay/mask）
    3. 匹配关闭文本（"关闭"、"×" 等）
    4. 按 Escape 键兜底

    Args:
        tab_idx: tab索引，默认0

    Returns:
        True 如果成功关闭弹窗，False 如果没有检测到弹窗
    """
    if not DEBUG_PORT:
        print("Error: _WANGDA_DEBUG_PORT environment variable is not set.")
        sys.exit(1)

    ws_url = get_ws_url(DEBUG_PORT, tab_idx)
    if not ws_url:
        print(f"Error: Could not find webSocketDebuggerUrl for tab {tab_idx}")
        sys.exit(1)

    # 使用一段 JS 尝试多种策略关闭弹窗，返回关闭结果
    close_expr = """
    (() => {
        // 辅助：判断元素是否可见
        const isVisible = (el) => {
            if (!el) return false;
            const style = window.getComputedStyle(el);
            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0;
        };

        // 策略1: 查找带 close 相关 class/id 的可见元素并点击
        const closeSelectors = [
            '.close .icon-close',
            '.close .iconfont',
            'i.icon-close',
            'i[class*="close"]',
            '.close',
            '[class*="close-btn"]',
            '[class*="close-icon"]',
            '[class*="btn-close"]',
            '.countdown-close',
            '#D183close',
            '[id*="close"]',
            '[class*="dialog"] [class*="close"]',
            '[class*="popup"] [class*="close"]',
            '[class*="modal"] [class*="close"]',
            '[class*="report"] [class*="close"]',
        ];

        for (const selector of closeSelectors) {
            try {
                const elements = document.querySelectorAll(selector);
                for (const el of elements) {
                    if (isVisible(el)) {
                        el.click();
                        return {success: true, method: 'selector', selector: selector};
                    }
                }
            } catch(e) {}
        }

        // 策略2: 查找包含关闭相关文本的可点击小元素
        const closeTexts = ['关闭', '×', '✕', '✖', 'X', '╳'];
        const allElements = Array.from(document.body.querySelectorAll('*'));
        for (const el of allElements) {
            if (!isVisible(el)) continue;
            const text = (el.textContent || '').trim();
            if (closeTexts.includes(text) && el.children.length <= 1) {
                const rect = el.getBoundingClientRect();
                // 关闭按钮通常较小
                if (rect.width < 200 && rect.height < 100) {
                    el.click();
                    return {success: true, method: 'text', text: text};
                }
            }
        }

        // 策略3: 查找并点击遮罩层（overlay/mask）
        const overlaySelectors = [
            '.dialog-overlay:not(.hidden)',
            '[class*="overlay"]:not(.hidden):not([class*="hidden"])',
            '[class*="mask"]:not(.hidden):not([class*="hidden"])',
            '[class*="backdrop"]:not(.hidden):not([class*="hidden"])',
        ];
        for (const selector of overlaySelectors) {
            try {
                const elements = document.querySelectorAll(selector);
                for (const el of elements) {
                    if (isVisible(el)) {
                        el.click();
                        return {success: true, method: 'overlay', selector: selector};
                    }
                }
            } catch(e) {}
        }

        // 策略4: 查找弹窗容器并隐藏（最后的兜底，直接操作DOM）
        const popupSelectors = [
            '[class*="report-popup"]',
            '[class*="promotion-popup"]:not([class*="hide"])',
            '[class*="popup"]:not([class*="hide"])',
            '[class*="modal"]:not([class*="hidden"])',
        ];
        for (const selector of popupSelectors) {
            try {
                const elements = document.querySelectorAll(selector);
                for (const el of elements) {
                    if (isVisible(el)) {
                        el.style.display = 'none';
                        return {success: true, method: 'hide', selector: selector};
                    }
                }
            } catch(e) {}
        }

        return {success: false, method: 'none'};
    })()
    """

    result = send_cdp_message(
        ws_url,
        "Runtime.evaluate",
        {"expression": close_expr, "returnByValue": True},
        wait_for_response=True,
    )

    closed = False
    method = "none"
    if result and "result" in result:
        value = result["result"].get("result", {}).get("value")
        if value and isinstance(value, dict):
            closed = value.get("success", False)
            method = value.get("method", "none")

    if closed:
        print(f"弹窗已关闭 (方式: {method})")
    else:
        # 最后兜底：按 Escape 键
        send_cdp_message(
            ws_url,
            "Input.dispatchKeyEvent",
            {
                "type": "rawKeyDown",
                "windowsVirtualKeyCode": 27,
                "key": "Escape",
                "code": "Escape",
            },
            wait_for_response=True,
        )
        time.sleep(0.05)
        send_cdp_message(
            ws_url,
            "Input.dispatchKeyEvent",
            {
                "type": "keyUp",
                "windowsVirtualKeyCode": 27,
                "key": "Escape",
                "code": "Escape",
            },
            wait_for_response=True,
        )
        print("未检测到弹窗，已发送 Escape 键尝试关闭")

    return closed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Chrome CDP Tools")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # start command
    parser_start = subparsers.add_parser("start", help="启动chrome浏览器")
    parser_start.add_argument(
        "--url",
        type=str,
        default="https://wangda.chinamobile.com",
        help="The initial URL to open",
    )

    # navi command
    parser_navi = subparsers.add_parser("navi", help="导航到指定url")
    parser_navi.add_argument("url", type=str, help="The URL to navigate to")

    # get-url command
    subparsers.add_parser("get-url", help="获取当前tab的url")

    # is-need-login command
    subparsers.add_parser("is-need-login", help="判断是否需要登录")

    # dump-page command
    parser_dump = subparsers.add_parser("dump-page", help="dump当前页面内容(json格式)")
    parser_dump.add_argument(
        "--tab-idx", type=int, default=0, help="The tab index to inspect (default: 0)"
    )

    # close-pop-window command
    subparsers.add_parser("close-pop-window", help="关闭页面弹窗")

    args = parser.parse_args()

    if args.command == "start":
        start(args.url)
    elif args.command == "navi":
        navi(args.url)
    elif args.command == "get-url":
        get_url()
    elif args.command == "is-need-login":
        is_need_login()
    elif args.command == "dump-page":
        dump_page(args.tab_idx)
    elif args.command == "close-pop-window":
        close_pop_window()
    else:
        parser.print_help()
