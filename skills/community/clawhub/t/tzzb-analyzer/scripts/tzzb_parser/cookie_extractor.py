import os
import sys
import time
import subprocess
import re
import json
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urlparse
from contextlib import contextmanager
from dotenv import load_dotenv

os.environ.setdefault("NODE_NO_WARNINGS", "1")
os.environ.setdefault("NODE_OPTIONS", "--no-deprecation")

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

load_dotenv()

CHROME_DEBUG_URL = os.getenv("CHROME_DEBUG_URL", "http://127.0.0.1:9222")
TARGET_URL = "https://tzzb.10jqka.com.cn/"
COOKIE_DOMAINS = [".10jqka.com.cn", ".10jqka.com"]

def _cdp_base_url() -> str:
    return CHROME_DEBUG_URL.rstrip("/")


def _cdp_version_url() -> str:
    return f"{_cdp_base_url()}/json/version"


def _is_cdp_running(timeout_s: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen(_cdp_version_url(), timeout=timeout_s) as resp:
            raw = resp.read()
        data = json.loads(raw.decode("utf-8", errors="ignore") or "{}")
        return bool(data.get("webSocketDebuggerUrl") or data.get("Browser"))
    except Exception:
        return False


def _parse_debug_port(debug_url: str) -> int:
    parsed = urlparse(debug_url)
    if parsed.port:
        return int(parsed.port)
    if parsed.scheme in ("http", "https") and parsed.netloc and ":" in parsed.netloc:
        return int(parsed.netloc.rsplit(":", 1)[-1])
    return 9222


def _default_user_data_dir() -> str:
    env_dir = os.getenv("CHROME_USER_DATA_DIR", "").strip()
    if env_dir:
        return str(Path(env_dir).expanduser())
    base = Path((os.getenv("TEMP") or os.getenv("TMP") or "")).expanduser()
    if str(base).strip():
        return str(base / "tzzb_parser_chrome")
    return str(Path.cwd() / "tzzb_parser_chrome")


def _find_chrome_executable() -> str:
    env_path = os.getenv("CHROME_PATH", "").strip()
    if env_path and Path(env_path).exists():
        return env_path

    candidates: list[str] = []
    if sys.platform.startswith("win"):
        candidates.extend(
            [
                os.path.join(os.getenv("PROGRAMFILES", r"C:\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(os.getenv("PROGRAMFILES(X86)", r"C:\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(os.getenv("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
            ]
        )
    elif sys.platform == "darwin":
        candidates.append("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    else:
        candidates.extend(["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"])

    for p in candidates:
        if Path(p).exists() or p in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
            return p
    return "chrome"


def _start_chrome_remote_debug() -> tuple[subprocess.Popen | None, str]:
    exe = _find_chrome_executable()
    port = _parse_debug_port(CHROME_DEBUG_URL)
    user_data_dir = _default_user_data_dir()
    Path(user_data_dir).mkdir(parents=True, exist_ok=True)

    parsed = urlparse(CHROME_DEBUG_URL)
    host = (parsed.hostname or "").lower()
    if host not in ("127.0.0.1", "localhost", ""):
        return None, f"debug url host is not local: {host}"

    if sys.platform.startswith("win") and os.getenv("CHROME_KILL_EXISTING", "").strip() in ("1", "true", "yes"):
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
        time.sleep(1.5)

    args = [
        exe,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--remote-allow-origins=*",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank",
    ]

    try:
        if sys.platform.startswith("win"):
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
            proc = subprocess.Popen(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                creationflags=creationflags,
            )
        else:
            proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)

        time.sleep(0.5)
        if proc.poll() is not None:
            return None, f"chrome exited early (code={proc.returncode})"

        deadline = time.time() + 15.0
        while time.time() < deadline:
            if _is_cdp_running(timeout_s=2.0):
                return proc, ""
            if proc.poll() is not None:
                return None, f"chrome exited early (code={proc.returncode})"
            time.sleep(1.0)

        return None, "cdp did not become ready in 15s"
    except Exception as e:
        return None, str(e)


def _cdp_guide(error: Exception) -> str:
    return (
        f"无法连接到 Chrome 远程调试地址 {CHROME_DEBUG_URL}。"
        "程序会尝试自动启动 Chrome 并连接该地址；若自动启动失败，可手动以远程调试模式启动 Chrome 后重试。"
        "若你使用了不同端口/地址，请设置环境变量 CHROME_DEBUG_URL。"
        "也可设置 CHROME_PATH / CHROME_USER_DATA_DIR 来辅助自动启动。"
        f" 原始错误：{error}"
    )


def _connect_browser(p):
    try:
        return p.chromium.connect_over_cdp(CHROME_DEBUG_URL)
    except Exception as e:
        if _is_cdp_running(timeout_s=2.0):
            try:
                return p.chromium.connect_over_cdp(CHROME_DEBUG_URL)
            except Exception:
                pass

        proc, start_err = _start_chrome_remote_debug()
        if proc:
            deadline = time.time() + 20.0
            while time.time() < deadline:
                try:
                    return p.chromium.connect_over_cdp(CHROME_DEBUG_URL)
                except Exception:
                    if proc.poll() is not None:
                        break
                    time.sleep(0.4)
        if start_err:
            raise RuntimeError(f"{_cdp_guide(e)} 自动启动失败：{start_err}")
        raise RuntimeError(f"{_cdp_guide(e)} 已尝试自动启动 Chrome 但仍无法连接")


def _get_automation_page(context):
    try:
        pages = list(context.pages)
    except Exception:
        pages = []

    if len(pages) == 1:
        url = ""
        try:
            url = pages[0].url or ""
        except Exception:
            url = ""
        if url == "about:blank":
            return pages[0]

    return context.new_page()


@contextmanager
def cdp_session():
    with sync_playwright() as p:
        browser = _connect_browser(p)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = _get_automation_page(context)
        try:
            yield context, page
        finally:
            try:
                page.close()
            except Exception:
                pass


def _click_first(locator) -> bool:
    try:
        target = locator.first
        target.scroll_into_view_if_needed(timeout=2000)
        target.click(timeout=8000)
        return True
    except Exception:
        return False


def _open_trade_records_tab(page) -> None:
    candidates = [
        page.get_by_role("tab", name=re.compile(r"(交易记录|成交记录)")),
        page.get_by_text("交易记录", exact=True),
        page.get_by_text("成交记录", exact=True),
        page.locator("text=交易记录"),
        page.locator("text=成交记录"),
    ]
    for locator in candidates:
        if _click_first(locator):
            return

    try:
        clicked = page.evaluate(
            """
            () => {
              const targets = new Set(["交易记录", "成交记录"]);
              const els = document.querySelectorAll("*");
              for (const el of els) {
                const t = (el.innerText || "").trim();
                if (targets.has(t) && el.offsetParent !== null) {
                  el.click();
                  return true;
                }
              }
              return false;
            }
            """
        )
        if clicked:
            return
    except Exception:
        pass
    raise RuntimeError("未找到“交易记录/成交记录”入口，请确认已进入账户详情页并处于登录态")


def _login_guide() -> str:
    return (
        "未检测到登录态：请在已开启远程调试的 Chrome 中打开并登录 "
        "https://tzzb.10jqka.com.cn/ ，然后重试。若使用 --user-data-dir，"
        "请确保登录发生在该目录对应的 Chrome 中。"
    )


def _get_userid(context, page) -> str:
    urls = [TARGET_URL, f"{TARGET_URL}pc/index.html"]
    try:
        cookies = context.cookies(urls)
    except Exception:
        cookies = context.cookies()

    for cookie in cookies:
        if cookie.get("name") == "userid":
            return cookie.get("value", "")

    page.goto(f"{TARGET_URL}pc/index.html", wait_until="networkidle")
    page.wait_for_timeout(1500)

    try:
        cookies = context.cookies(urls)
    except Exception:
        cookies = context.cookies()

    for cookie in cookies:
        if cookie.get("name") == "userid":
            return cookie.get("value", "")

    return ""


def get_userid(context, page) -> str:
    return _get_userid(context, page)


def _get_stock_watchlist_in_session(context, page) -> dict:
    page.goto(TARGET_URL, wait_until="networkidle")
    page.wait_for_timeout(3000)

    userid = _get_userid(context, page)

    if not userid:
        return {"error_code": "-1", "error_msg": _login_guide()}

    return page.evaluate(
        """
        async function(userid) {
            function safeJson(text) {
                try {
                    return JSON.parse(text);
                } catch (e) {
                    return {
                        error_code: "-1",
                        error_msg: String(text || "").slice(0, 500)
                    };
                }
            }

            const formData = new URLSearchParams();
            formData.append('terminal', '1');
            formData.append('version', '0.0.0');
            formData.append('userid', userid);
            formData.append('user_id', userid);
            formData.append('sort_rule', '');
            formData.append('sort_order', '1');

            const response = await fetch('/caishen_httpserver/tzzb/caishen_fund/pc/optional/v1/sort_list', {
                method: 'POST',
                body: formData,
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': 'https://tzzb.10jqka.com.cn/',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const text = await response.text();
            const json = safeJson(text);
            if (typeof json === "object" && json !== null && !("status" in json)) {
                json.status = response.status;
            }
            return json;
        }
        """,
        userid,
    )


def extract_cookies() -> dict[str, str]:
    """通过 Playwright CDP 连接 Chrome，提取认证 Cookie"""
    cookies_dict: dict[str, str] = {}

    with sync_playwright() as p:
        browser = _connect_browser(p)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = _get_automation_page(context)

        page.goto(TARGET_URL, wait_until="networkidle")
        page.wait_for_timeout(2000)

        urls = [TARGET_URL, f"{TARGET_URL}pc/index.html"]
        try:
            all_cookies = context.cookies(urls)
        except Exception:
            all_cookies = context.cookies()
        for cookie in all_cookies:
            domain = cookie.get("domain", "")
            if any(d in domain for d in COOKIE_DOMAINS):
                cookies_dict[cookie["name"]] = cookie["value"]

        page.close()

    return cookies_dict


def get_stock_watchlist_via_browser(context=None, page=None) -> dict:
    """通过浏览器上下文调用自选股 API，返回原始响应 dict"""
    if context is not None and page is not None:
        return _get_stock_watchlist_in_session(context, page)

    try:
        with cdp_session() as (ctx, pg):
            return _get_stock_watchlist_in_session(ctx, pg)
    except RuntimeError as e:
        return {"error_code": "-1", "error_msg": str(e)}


def _get_stock_positions_in_session(context, page) -> dict:
    page.goto(TARGET_URL, wait_until="networkidle")
    page.wait_for_timeout(3000)

    userid = _get_userid(context, page)

    if not userid:
        return {"error_code": "-1", "error_msg": _login_guide()}

    account_result = page.evaluate(
        """
        async function(userid) {
            function safeJson(text) {
                try {
                    return JSON.parse(text);
                } catch (e) {
                    return {
                        error_code: "-1",
                        error_msg: String(text || "").slice(0, 500)
                    };
                }
            }

            const formData = new URLSearchParams();
            formData.append("terminal", "1");
            formData.append("version", "0.0.0");
            formData.append("userid", userid);
            formData.append("user_id", userid);

            const response = await fetch("/caishen_httpserver/tzzb/caishen_fund/pc/account/v1/account_list", {
                method: "POST",
                body: formData,
                credentials: "include",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "https://tzzb.10jqka.com.cn/pc/index.html",
                    "X-Requested-With": "XMLHttpRequest"
                }
            });
            const text = await response.text();
            const json = safeJson(text);
            if (typeof json === "object" && json !== null && !("status" in json)) {
                json.status = response.status;
            }
            return json;
        }
        """,
        userid,
    )

    fund_key = ""
    common_accounts = account_result.get("ex_data", {}).get("common", [])
    if common_accounts:
        fund_key = common_accounts[0].get("fund_key", "")

    if not fund_key:
        return {"error_code": "-1", "error_msg": "missing fund_key"}

    return page.evaluate(
        """
        async function(args) {
            function safeJson(text) {
                try {
                    return JSON.parse(text);
                } catch (e) {
                    return {
                        error_code: "-1",
                        error_msg: String(text || "").slice(0, 500)
                    };
                }
            }

            const formData = new URLSearchParams();
            formData.append("terminal", "1");
            formData.append("version", "0.0.0");
            formData.append("userid", args.userid);
            formData.append("user_id", args.userid);
            formData.append("manual_id", "");
            formData.append("fund_key", args.fund_key);
            formData.append("rzrq_fund_key", "");

            const response = await fetch("/caishen_httpserver/tzzb/caishen_fund/pc/asset/v1/stock_position", {
                method: "POST",
                body: formData,
                credentials: "include",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "https://tzzb.10jqka.com.cn/pc/index.html",
                    "X-Requested-With": "XMLHttpRequest"
                }
            });
            const text = await response.text();
            const json = safeJson(text);
            if (typeof json === "object" && json !== null && !("status" in json)) {
                json.status = response.status;
            }
            return json;
        }
        """,
        {"userid": userid, "fund_key": fund_key},
    )


def get_stock_positions_via_browser(context=None, page=None) -> dict:
    """通过浏览器上下文调用持仓 API，返回原始响应 dict"""
    if context is not None and page is not None:
        return _get_stock_positions_in_session(context, page)

    try:
        with cdp_session() as (ctx, pg):
            return _get_stock_positions_in_session(ctx, pg)
    except RuntimeError as e:
        return {"error_code": "-1", "error_msg": str(e)}


def _get_trade_records_in_session(context, page) -> list[dict]:
    records: list[dict] = []

    page.goto(TARGET_URL, wait_until="networkidle")
    page.wait_for_timeout(3000)

    userid = _get_userid(context, page)

    if not userid:
        return records

    account_result = page.evaluate(
        """
        async function(userid) {
            function safeJson(text) {
                try {
                    return JSON.parse(text);
                } catch (e) {
                    return {
                        error_code: "-1",
                        error_msg: String(text || "").slice(0, 500)
                    };
                }
            }

            const formData = new URLSearchParams();
            formData.append("terminal", "1");
            formData.append("version", "0.0.0");
            formData.append("userid", userid);
            formData.append("user_id", userid);

            const response = await fetch("/caishen_httpserver/tzzb/caishen_fund/pc/account/v1/account_list", {
                method: "POST",
                body: formData,
                credentials: "include",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "https://tzzb.10jqka.com.cn/pc/index.html",
                    "X-Requested-With": "XMLHttpRequest"
                }
            });
            const text = await response.text();
            const json = safeJson(text);
            if (typeof json === "object" && json !== null && !("status" in json)) {
                json.status = response.status;
            }
            return json;
        }
        """,
        userid,
    )

    account_key = ""
    stock_accounts = account_result.get("ex_data", {}).get("stock", [])
    if stock_accounts:
        account_key = stock_accounts[0].get("fund_key", "")

    if not account_key:
        common_accounts = account_result.get("ex_data", {}).get("common", [])
        if common_accounts:
            account_key = common_accounts[0].get("fund_key", "")

    if not account_key:
        return records

    page.goto(f"https://tzzb.10jqka.com.cn/pc/index.html#/myAccount/a/{account_key}", wait_until="networkidle")
    page.wait_for_timeout(2000)

    try:
        _open_trade_records_tab(page)
    except PlaywrightTimeoutError as e:
        raise RuntimeError(f"打开交易记录失败：{e}")

    page.wait_for_timeout(1500)

    result = page.evaluate(
        """
        () => {
            const rows = document.querySelectorAll("table tr");
            const data = [];
            rows.forEach(row => {
                const text = row.innerText;
                if (text && !text.includes("成交日期") && text.length > 10) {
                    const parts = text.split("\\n").map(p => p.trim()).filter(p => p);
                    if (parts.length >= 8) {
                        data.push(parts);
                    }
                }
            });
            return data;
        }
        """
    )

    for row in result:
        if len(row) >= 8:
            records.append(
                {
                    "trade_date": row[0],
                    "stock_code": row[1],
                    "stock_name": row[2],
                    "trade_type": row[3],
                    "price": row[4],
                    "quantity": row[5],
                    "amount": row[6],
                    "fee": row[7],
                    "note": row[8] if len(row) > 8 else "",
                }
            )

    return records


def get_trade_records_via_browser(context=None, page=None) -> list[dict]:
    """通过 Playwright CDP 连接 Chrome，从 DOM 提取交易记录"""
    if context is not None and page is not None:
        return _get_trade_records_in_session(context, page)

    with cdp_session() as (ctx, pg):
        return _get_trade_records_in_session(ctx, pg)
