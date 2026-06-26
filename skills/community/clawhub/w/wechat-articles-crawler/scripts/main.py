#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown
from PIL import Image, ImageOps
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

APP_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = APP_ROOT / "config.json"
PROFILE_DIR = Path(os.environ.get("WECHAT_FETCHER_PROFILE_DIR", APP_ROOT / ".playwright-profile"))
LOGIN_ARTIFACTS_DIR = Path(
    os.environ.get("WECHAT_FETCHER_LOGIN_ARTIFACTS_DIR", APP_ROOT / "login_artifacts")
)
DEFAULT_OUTPUT_FOLDER_NAME = "输出文章"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)
MP_HOME_URL = "https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN"
MP_LOGIN_URL = "https://mp.weixin.qq.com/"
ARTICLE_LIST_PAGE_SIZE = 20
KNOWN_COMMANDS = {"fetch", "ensure-login", "login-status", "clear-login"}
ACTIVE_QR_VIEWER: Any | None = None


@dataclass
class AppConfig:
    output_parent: str
    output_folder_name: str = DEFAULT_OUTPUT_FOLDER_NAME
    article_limit: int = 20
    concurrency: int = 6
    display_mode: str = "auto"

    @property
    def output_root(self) -> Path:
        return Path(self.output_parent).expanduser().resolve() / self.output_folder_name


def main() -> int:
    args = parse_args()

    try:
        if args.command == "fetch":
            config = load_or_create_config(noninteractive=args.json or is_headless_environment())
            display_mode = args.display or config.display_mode
            payload = command_fetch(
                article_url=args.article_url,
                config=config,
                display_mode=display_mode,
                quiet=args.json,
            )
        elif args.command == "ensure-login":
            display_mode = args.display or load_or_create_config(
                noninteractive=args.json or is_headless_environment()
            ).display_mode
            payload = command_ensure_login(display_mode=display_mode, quiet=args.json)
        elif args.command == "login-status":
            payload = command_login_status()
        elif args.command == "clear-login":
            payload = command_clear_login()
        else:
            raise RuntimeError(f"不支持的命令：{args.command}")
    except Exception as exc:  # noqa: BLE001
        if args.json:
            print(
                json.dumps(
                    {
                        "status": "error",
                        "error": str(exc),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 1
        raise

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="本地版微信公众号文章抓取工具")
    parser.add_argument("primary", nargs="?", help="命令或文章链接")
    parser.add_argument("secondary", nargs="?", help="当命令需要时传入第二个位置参数")
    parser.add_argument(
        "--display",
        choices=["auto", "terminal", "image", "silent"],
        help="二维码展示模式，默认读取 config.json 的 display_mode",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="只输出 JSON，适合 agent / CLI 集成",
    )
    args = parser.parse_args()

    if args.primary in KNOWN_COMMANDS:
        args.command = args.primary
        args.article_url = args.secondary
    else:
        args.command = "fetch"
        args.article_url = args.primary

    if args.command in {"ensure-login", "login-status", "clear-login"} and args.secondary:
        parser.error(f"{args.command} 不接受额外的位置参数。")
    return args


def command_fetch(
    *,
    article_url: str | None,
    config: AppConfig,
    display_mode: str,
    quiet: bool,
) -> dict[str, Any]:
    article_url = get_article_url(article_url)

    log("正在检查公众号后台登录状态...", quiet=quiet)
    token, cookies = ensure_login(display_mode=display_mode, quiet=quiet)
    log("登录状态可用，开始解析文章来源...", quiet=quiet)

    seed = fetch_seed_article_info(article_url)
    if not seed.get("nickname") and not seed.get("alias"):
        raise RuntimeError("无法从这篇文章里识别公众号名称，换一篇该号文章再试。")

    with build_sync_client(cookies) as client:
        account, preview_articles = resolve_account(client, token, seed, config.article_limit)
        log(
            f"已锁定公众号：{account['nickname']}"
            + (f"（{account['alias']}）" if account.get("alias") else ""),
            quiet=quiet,
        )

        articles = preview_articles
        if len(articles) < config.article_limit:
            articles = fetch_account_articles(
                client=client,
                token=token,
                fakeid=account["fakeid"],
                limit=config.article_limit,
            )

    if not articles:
        raise RuntimeError("没有拿到可下载的文章列表。")

    output_dir = prepare_output_dir(config, account["nickname"])
    log(f"准备下载 {len(articles)} 篇文章到：{output_dir}", quiet=quiet)
    results = asyncio.run(
        download_articles(
            cookies=cookies,
            articles=articles[: config.article_limit],
            output_dir=output_dir,
            account=account,
            concurrency=config.concurrency,
        )
    )

    index_path = output_dir / "articles.json"
    index_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    success_count = sum(1 for item in results if item.get("status") == "ok")
    log(f"完成：成功 {success_count}/{len(results)} 篇。", quiet=quiet)
    log(f"输出目录：{output_dir}", quiet=quiet)
    log(f"索引文件：{index_path}", quiet=quiet)

    return {
        "status": "completed",
        "account_name": account["nickname"],
        "account_alias": account.get("alias") or "",
        "requested_limit": config.article_limit,
        "downloaded": success_count,
        "failed": len(results) - success_count,
        "output_dir": str(output_dir),
        "index_file": str(index_path),
        "profile_dir": str(PROFILE_DIR),
        "login_artifacts_dir": str(LOGIN_ARTIFACTS_DIR),
        "results": results,
    }


def command_ensure_login(*, display_mode: str, quiet: bool) -> dict[str, Any]:
    log("正在检查公众号后台登录状态...", quiet=quiet)
    token, _cookies = ensure_login(display_mode=display_mode, quiet=quiet)
    payload = command_login_status()
    payload.update(
        {
            "status": "authenticated",
            "token_present": bool(token),
        }
    )
    return payload


def command_login_status() -> dict[str, Any]:
    status_path = LOGIN_ARTIFACTS_DIR / "login_status.json"
    payload: dict[str, Any] = {
        "status": "missing",
        "status_file": str(status_path),
        "profile_dir": str(PROFILE_DIR),
        "profile_exists": PROFILE_DIR.exists(),
        "login_artifacts_dir": str(LOGIN_ARTIFACTS_DIR),
        "login_artifacts_exists": LOGIN_ARTIFACTS_DIR.exists(),
    }

    if status_path.exists():
        payload.update(json.loads(status_path.read_text(encoding="utf-8")))
        payload["status_file"] = str(status_path)
        payload["profile_dir"] = str(PROFILE_DIR)
        payload["profile_exists"] = PROFILE_DIR.exists()
        payload["login_artifacts_dir"] = str(LOGIN_ARTIFACTS_DIR)
        payload["login_artifacts_exists"] = LOGIN_ARTIFACTS_DIR.exists()
    return payload


def command_clear_login() -> dict[str, Any]:
    removed_paths: list[str] = []
    if PROFILE_DIR.exists():
        shutil.rmtree(PROFILE_DIR)
        removed_paths.append(str(PROFILE_DIR))
    if LOGIN_ARTIFACTS_DIR.exists():
        shutil.rmtree(LOGIN_ARTIFACTS_DIR)
        removed_paths.append(str(LOGIN_ARTIFACTS_DIR))

    return {
        "status": "cleared",
        "removed_paths": removed_paths,
        "profile_dir": str(PROFILE_DIR),
        "login_artifacts_dir": str(LOGIN_ARTIFACTS_DIR),
    }


def log(message: str, *, quiet: bool) -> None:
    if not quiet:
        print(message)


def load_or_create_config(*, noninteractive: bool) -> AppConfig:
    if CONFIG_PATH.exists():
        raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return AppConfig(**raw)

    if noninteractive:
        config = build_default_config()
        CONFIG_PATH.write_text(
            json.dumps(asdict(config), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return config

    output_parent, article_limit = prompt_first_run_config()
    config = AppConfig(output_parent=output_parent, article_limit=article_limit)
    CONFIG_PATH.write_text(
        json.dumps(asdict(config), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return config


def build_default_config() -> AppConfig:
    return AppConfig(
        output_parent=str(default_output_parent()),
        article_limit=20,
        concurrency=6,
        display_mode="silent" if is_headless_environment() else "auto",
    )


def default_output_parent() -> Path:
    # In the bundled skill package, keep output under the skill root so agents
    # can use the tool without asking the user for a separate output path.
    skill_root = APP_ROOT.parent
    if (skill_root / "SKILL.md").exists():
        return skill_root

    desktop_path = Path.home() / "Desktop"
    if desktop_path.exists():
        return desktop_path
    return Path.home()


def is_headless_environment() -> bool:
    if sys.platform == "darwin":
        return not sys.stdout.isatty()
    return not bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def prompt_first_run_config() -> tuple[str, int]:
    selected_dir = choose_directory_with_dialog()
    if not selected_dir:
        fallback = input("请输入输出父目录绝对路径：").strip()
        selected_dir = fallback

    if not selected_dir:
        raise SystemExit("未选择输出目录，程序已退出。")

    raw_limit = ask_text_with_dialog(
        message="请输入单次批量提取文章数：",
        default="20",
    )
    if not raw_limit:
        raw_limit = input("请输入单次批量提取文章数：").strip()

    try:
        article_limit = int(raw_limit)
    except ValueError as exc:
        raise SystemExit("单次抓取篇数不是有效数字。") from exc

    if article_limit < 1 or article_limit > 200:
        raise SystemExit("单次抓取篇数必须在 1 到 200 之间。")
    return selected_dir, article_limit


def choose_directory_with_dialog() -> str | None:
    script = """
    set chosenFolder to choose folder with prompt "请选择文章输出的父目录，程序会在里面自动新建“输出文章”文件夹"
    POSIX path of chosenFolder
    """
    return run_osascript(script)


def ask_text_with_dialog(*, message: str, default: str) -> str | None:
    escaped_message = message.replace('"', '\\"')
    escaped_default = default.replace('"', '\\"')
    script = f'''
    text returned of (display dialog "{escaped_message}" default answer "{escaped_default}" buttons {{"取消", "确定"}} default button "确定")
    '''
    return run_osascript(script)


def run_osascript(script: str) -> str | None:
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def get_article_url(article_url: str | None) -> str:
    if article_url and article_url.strip():
        return article_url.strip()

    article_url = input("请输入任意一篇公众号文章链接：").strip()
    if not article_url:
        raise SystemExit("未输入文章链接。")
    return article_url


def ensure_login(*, display_mode: str, quiet: bool) -> tuple[str, dict[str, str]]:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    LOGIN_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        token, cookies = try_get_session(playwright, headless=True, interactive=False)
        if token:
            write_login_status(
                status="authenticated",
                display_mode=display_mode,
                message="已复用本地登录态。",
            )
            return token, cookies

        log("常规会话检查未命中，正在进入登录页；如有需要会生成登录二维码...", quiet=quiet)
        token, cookies = login_with_qr(playwright, display_mode=display_mode, quiet=quiet)
        if token:
            return token, cookies

    write_login_status(
        status="timeout",
        display_mode=display_mode,
        message="登录超时，未拿到公众号后台 token。",
    )
    raise SystemExit("登录失败，未拿到公众号后台 token。")


def try_get_session(
    playwright: Any,
    *,
    headless: bool,
    interactive: bool,
) -> tuple[str | None, dict[str, str]]:
    context = launch_browser_context(playwright, headless=headless, user_data_dir=PROFILE_DIR)

    try:
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(MP_HOME_URL, wait_until="domcontentloaded", timeout=45000)

        token = wait_for_token(page, interactive=interactive)
        cookies = {
            item["name"]: item["value"]
            for item in context.cookies("https://mp.weixin.qq.com")
        }
        return token, cookies
    finally:
        context.close()


def launch_browser_context(playwright: Any, *, headless: bool, user_data_dir: Path) -> Any:
    browser_args = {
        "user_data_dir": str(user_data_dir),
        "headless": headless,
        "viewport": {"width": 1440, "height": 960},
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-default-browser-check",
        ],
    }

    last_error: Exception | None = None
    for channel in ("chrome", "msedge", None):
        try:
            if channel:
                return playwright.chromium.launch_persistent_context(
                    channel=channel,
                    **browser_args,
                )
            return playwright.chromium.launch_persistent_context(**browser_args)
        except Exception as exc:  # noqa: BLE001
            last_error = exc

    if last_error is not None:
        raise last_error
    raise RuntimeError("无法启动浏览器。")


def login_with_qr(
    playwright: Any,
    *,
    display_mode: str,
    quiet: bool,
) -> tuple[str | None, dict[str, str]]:
    context = launch_browser_context(playwright, headless=True, user_data_dir=PROFILE_DIR)
    qr_selector = "img.login__type__container__scan__qrcode"
    last_qr_signature: str | None = None
    last_refresh_at = time.time()

    try:
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(MP_LOGIN_URL, wait_until="domcontentloaded", timeout=45000)

        token = extract_token_from_url(page.url)
        if token:
            cookies = {
                item["name"]: item["value"]
                for item in context.cookies("https://mp.weixin.qq.com")
            }
            write_login_status(
                status="authenticated",
                display_mode=display_mode,
                message="已通过登录页复用本地登录态。",
            )
            return token, cookies

        wait_for_login_qr(page, qr_selector)

        deadline = time.time() + 300
        while time.time() < deadline:
            token = extract_token_from_url(page.url)
            if token:
                cookies = {
                    item["name"]: item["value"]
                    for item in context.cookies("https://mp.weixin.qq.com")
                }
                write_login_status(
                    status="authenticated",
                    display_mode=display_mode,
                    message="扫码登录成功。",
                )
                return token, cookies

            last_qr_signature = maybe_refresh_qr_artifacts(
                page=page,
                qr_selector=qr_selector,
                display_mode=display_mode,
                last_qr_signature=last_qr_signature,
                quiet=quiet,
            )

            if time.time() - last_refresh_at > 90:
                page.reload(wait_until="domcontentloaded", timeout=45000)
                token = extract_token_from_url(page.url)
                if token:
                    cookies = {
                        item["name"]: item["value"]
                        for item in context.cookies("https://mp.weixin.qq.com")
                    }
                    write_login_status(
                        status="authenticated",
                        display_mode=display_mode,
                        message="二维码刷新期间已复用本地登录态。",
                    )
                    return token, cookies
                wait_for_login_qr(page, qr_selector)
                last_refresh_at = time.time()

            try:
                page.wait_for_timeout(1000)
            except PlaywrightTimeoutError:
                pass
    finally:
        close_qr_viewer()
        context.close()

    return None, {}


def wait_for_login_qr(page: Any, qr_selector: str) -> None:
    locator = page.locator(qr_selector).first
    locator.wait_for(state="visible", timeout=45000)
    deadline = time.time() + 45
    while time.time() < deadline:
        info = locator.evaluate(
            "el => ({complete: el.complete, naturalWidth: el.naturalWidth, naturalHeight: el.naturalHeight})"
        )
        if info["complete"] and info["naturalWidth"] > 0 and info["naturalHeight"] > 0:
            return
        page.wait_for_timeout(250)
    raise RuntimeError("二维码图片未能在限定时间内加载完成。")


def maybe_refresh_qr_artifacts(
    *,
    page: Any,
    qr_selector: str,
    display_mode: str,
    last_qr_signature: str | None,
    quiet: bool,
) -> str | None:
    qr_image = page.locator(qr_selector).first

    try:
        qr_src = qr_image.get_attribute("src", timeout=3000) or ""
    except PlaywrightTimeoutError:
        return last_qr_signature

    try:
        body_text = page.locator("body").inner_text(timeout=3000)
    except PlaywrightTimeoutError:
        body_text = ""

    if body_text and "二维码已失效" in body_text:
        page.reload(wait_until="domcontentloaded", timeout=45000)
        wait_for_login_qr(page, qr_selector)
        qr_image = page.locator(qr_selector).first
        qr_src = qr_image.get_attribute("src") or ""

    if qr_src and qr_src != last_qr_signature:
        wait_for_login_qr(page, qr_selector)
        qr_image = page.locator(qr_selector).first
        png_bytes = qr_image.screenshot()
        return write_login_qr_artifacts(
            png_bytes=png_bytes,
            qr_signature=qr_src,
            display_mode=display_mode,
            quiet=quiet,
        )

    return last_qr_signature


def write_login_qr_artifacts(
    *,
    png_bytes: bytes,
    qr_signature: str,
    display_mode: str,
    quiet: bool,
) -> str:
    png_path = LOGIN_ARTIFACTS_DIR / "login_qr.png"
    txt_path = LOGIN_ARTIFACTS_DIR / "login_qr.txt"
    png_path.write_bytes(png_bytes)

    ascii_qr = render_qr_ascii(png_bytes)
    txt_path.write_text(ascii_qr + "\n", encoding="utf-8")

    write_login_status(
        status="waiting_scan",
        display_mode=display_mode,
        qr_signature=qr_signature,
        qr_png_path=str(png_path),
        qr_text_path=str(txt_path),
        message="请使用微信扫码登录公众号后台。",
    )

    log("登录二维码已生成：", quiet=quiet)
    log(f"- PNG：{png_path}", quiet=quiet)
    log(f"- 文本：{txt_path}", quiet=quiet)

    if should_print_qr_to_terminal(display_mode) and not quiet:
        print(ascii_qr)

    if should_open_qr_image(display_mode):
        open_file_in_viewer(png_path)

    return qr_signature


def render_qr_ascii(png_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(png_bytes)).convert("L")
    image = ImageOps.autocontrast(image)

    binary = image.point(lambda value: 255 if value > 180 else 0, mode="1")
    bbox = ImageOps.invert(binary.convert("L")).getbbox()
    if bbox:
        binary = binary.crop(bbox)

    padded = ImageOps.expand(binary, border=4, fill=1)
    max_side = 48
    padded = padded.resize((max_side, max_side), resample=Image.Resampling.NEAREST)

    lines = []
    for y in range(padded.height):
        row = []
        for x in range(padded.width):
            pixel = padded.getpixel((x, y))
            row.append("  " if pixel else "██")
        lines.append("".join(row).rstrip())
    return "\n".join(lines)


def should_print_qr_to_terminal(display_mode: str) -> bool:
    return display_mode in {"auto", "terminal"} and sys.stdout.isatty()


def should_open_qr_image(display_mode: str) -> bool:
    if display_mode not in {"auto", "image"}:
        return False
    if sys.platform == "darwin":
        return shutil.which("qlmanage") is not None
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")) and shutil.which(
        "xdg-open"
    ) is not None


def open_file_in_viewer(path: Path) -> None:
    global ACTIVE_QR_VIEWER
    close_qr_viewer()
    try:
        if sys.platform == "darwin":
            ACTIVE_QR_VIEWER = subprocess.Popen(
                ["qlmanage", "-p", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        if shutil.which("xdg-open"):
            ACTIVE_QR_VIEWER = subprocess.Popen(
                ["xdg-open", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except Exception:  # noqa: BLE001
        ACTIVE_QR_VIEWER = None
        return


def close_qr_viewer() -> None:
    global ACTIVE_QR_VIEWER
    if ACTIVE_QR_VIEWER is None:
        return
    try:
        if ACTIVE_QR_VIEWER.poll() is None:
            ACTIVE_QR_VIEWER.terminate()
            try:
                ACTIVE_QR_VIEWER.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ACTIVE_QR_VIEWER.kill()
    except Exception:  # noqa: BLE001
        pass
    ACTIVE_QR_VIEWER = None


def write_login_status(status: str, display_mode: str, **payload: Any) -> None:
    status_path = LOGIN_ARTIFACTS_DIR / "login_status.json"
    data = {
        "status": status,
        "display_mode": display_mode,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        **payload,
    }
    status_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def wait_for_token(page: Any, *, interactive: bool) -> str | None:
    deadline = time.time() + (300 if interactive else 5)
    if interactive:
        print("浏览器已打开。请在微信公众平台页面扫码并完成确认。")

    while time.time() < deadline:
        token = extract_token_from_url(page.url)
        if token:
            return token

        try:
            page.wait_for_timeout(1000)
        except PlaywrightTimeoutError:
            pass

    return None


def extract_token_from_url(url: str) -> str | None:
    parsed = urlparse(url)
    values = parse_qs(parsed.query).get("token")
    return values[0] if values else None


def build_sync_client(cookies: dict[str, str]) -> httpx.Client:
    return httpx.Client(
        headers=base_headers(),
        cookies=cookies,
        follow_redirects=True,
        timeout=httpx.Timeout(30.0, connect=30.0),
    )


def build_async_client(cookies: dict[str, str]) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        headers=base_headers(),
        cookies=cookies,
        follow_redirects=True,
        timeout=httpx.Timeout(30.0, connect=30.0),
    )


def base_headers() -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Referer": "https://mp.weixin.qq.com/",
        "Origin": "https://mp.weixin.qq.com",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "identity",
    }


def fetch_seed_article_info(article_url: str) -> dict[str, Any]:
    response = httpx.get(
        article_url,
        headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://mp.weixin.qq.com/",
        },
        follow_redirects=True,
        timeout=httpx.Timeout(30.0, connect=30.0),
    )
    response.raise_for_status()

    html_text = response.text
    soup = BeautifulSoup(html_text, "html.parser")
    parsed = urlparse(str(response.url))
    query = parse_qs(parsed.query)

    title = ""
    title_node = soup.select_one("#activity-name")
    if title_node:
        title = title_node.get_text(" ", strip=True)
    if not title:
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title:
            title = og_title.get("content", "").strip()

    seed = {
        "article_url": str(response.url),
        "title": title,
        "nickname": first_match(
            html_text,
            [
                r'var\s+nickname\s*=\s*htmlDecode\("([^"]+)"\);',
                r'window\.__INITIAL_STATE__.*?"nickname":"([^"]+)"',
            ],
        ),
        "alias": first_match(
            html_text,
            [
                r'var\s+user_name\s*=\s*"([^"]*)";',
                r'"user_name":"([^"]+)"',
            ],
        ),
        "biz": query.get("__biz", [None])[0]
        or first_match(html_text, [r'var\s+biz\s*=\s*"([^"]+)";']),
        "mid": query.get("mid", [None])[0],
        "idx": query.get("idx", [None])[0],
        "sn": query.get("sn", [None])[0],
    }
    return seed


def first_match(content: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return decode_js_string(match.group(1))
    return None


def decode_js_string(value: str) -> str:
    candidate = value.strip()
    try:
        candidate = json.loads(f'"{candidate}"')
    except json.JSONDecodeError:
        candidate = candidate.replace('\\"', '"').replace("\\/", "/")
    return html.unescape(candidate).strip()


def resolve_account(
    client: httpx.Client,
    token: str,
    seed: dict[str, Any],
    limit: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    queries = [seed.get("alias"), seed.get("nickname")]
    candidates: list[dict[str, Any]] = []
    seen_fakeids: set[str] = set()

    for query in queries:
        if not query:
            continue
        for account in search_accounts(client, token, query):
            fakeid = str(account.get("fakeid") or "")
            if fakeid and fakeid not in seen_fakeids:
                seen_fakeids.add(fakeid)
                candidates.append(account)

    if not candidates:
        raise SystemExit("没有找到公众号候选结果。该账号可能关闭了后台搜索。")

    ranked = sorted(candidates, key=lambda item: score_account(item, seed), reverse=True)
    preview_cache: dict[str, list[dict[str, Any]]] = {}

    for account in ranked[:5]:
        preview = fetch_account_articles(
            client=client,
            token=token,
            fakeid=account["fakeid"],
            limit=min(max(limit, 10), 20),
        )
        preview_cache[str(account["fakeid"])] = preview
        if any(is_same_article(article["link"], seed["article_url"]) for article in preview):
            return account, preview

    best = ranked[0]
    return best, preview_cache.get(str(best["fakeid"]), [])


def search_accounts(client: httpx.Client, token: str, query: str) -> list[dict[str, Any]]:
    response = client.get(
        "https://mp.weixin.qq.com/cgi-bin/searchbiz",
        params={
            "action": "search_biz",
            "query": query,
            "begin": 0,
            "count": 5,
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": 1,
        },
    )
    data = safe_json(response)
    return data.get("list") or []


def fetch_account_articles(
    *,
    client: httpx.Client,
    token: str,
    fakeid: str,
    limit: int,
) -> list[dict[str, Any]]:
    articles: list[dict[str, Any]] = []
    seen_links: set[str] = set()
    begin = 0

    while len(articles) < limit:
        response = client.get(
            "https://mp.weixin.qq.com/cgi-bin/appmsgpublish",
            params={
                "sub": "list",
                "begin": begin,
                "count": ARTICLE_LIST_PAGE_SIZE,
                "fakeid": fakeid,
                "type": "101_1",
                "free_publish_type": 1,
                "sub_action": "list_ex",
                "token": token,
                "lang": "zh_CN",
                "f": "json",
                "ajax": 1,
            },
        )
        data = safe_json(response)
        page_raw = data.get("publish_page")
        if not page_raw:
            break

        page_data = json.loads(page_raw) if isinstance(page_raw, str) else page_raw
        publish_list = page_data.get("publish_list") or []
        if not publish_list:
            break

        before_count = len(articles)
        for item in publish_list:
            publish_info = item.get("publish_info")
            publish_data = json.loads(publish_info) if isinstance(publish_info, str) else publish_info
            for appmsg in (publish_data or {}).get("appmsgex", []):
                link = normalize_article_url(appmsg.get("link") or "")
                if not link or link in seen_links:
                    continue
                seen_links.add(link)
                articles.append(
                    {
                        "title": appmsg.get("title") or "",
                        "digest": appmsg.get("digest") or "",
                        "link": link,
                        "cover": appmsg.get("cover") or "",
                        "update_time": appmsg.get("update_time"),
                        "create_time": appmsg.get("create_time"),
                    }
                )
                if len(articles) >= limit:
                    return articles

        if len(articles) == before_count:
            break

        begin += ARTICLE_LIST_PAGE_SIZE
        if len(publish_list) < ARTICLE_LIST_PAGE_SIZE:
            break

    return articles


def score_account(account: dict[str, Any], seed: dict[str, Any]) -> int:
    nickname = normalize_text(account.get("nickname"))
    alias = normalize_text(account.get("alias"))
    seed_nickname = normalize_text(seed.get("nickname"))
    seed_alias = normalize_text(seed.get("alias"))

    score = 0
    if seed_alias and alias == seed_alias:
        score += 100
    if seed_nickname and nickname == seed_nickname:
        score += 80
    if seed_alias and seed_alias in alias:
        score += 30
    if seed_nickname and seed_nickname in nickname:
        score += 20
    return score


def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", "", str(value or "")).strip().lower()


def normalize_article_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    important = []
    for key in ("__biz", "mid", "idx", "sn"):
        value = query.get(key, [None])[0]
        if value:
            important.append(f"{key}={value}")
    if important:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{'&'.join(important)}"
    return url


def is_same_article(left: str, right: str) -> bool:
    left_sig = article_signature(left)
    right_sig = article_signature(right)
    return bool(left_sig and right_sig and left_sig == right_sig)


def article_signature(url: str) -> tuple[str, str, str, str] | None:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    values = tuple(query.get(key, [""])[0] for key in ("__biz", "mid", "idx", "sn"))
    return values if any(values) else None


def prepare_output_dir(config: AppConfig, account_name: str) -> Path:
    config.output_root.mkdir(parents=True, exist_ok=True)
    run_name = f"{safe_name(account_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = config.output_root / run_name
    (output_dir / "markdown").mkdir(parents=True, exist_ok=True)
    (output_dir / "html").mkdir(parents=True, exist_ok=True)
    return output_dir


async def download_articles(
    *,
    cookies: dict[str, str],
    articles: list[dict[str, Any]],
    output_dir: Path,
    account: dict[str, Any],
    concurrency: int,
) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(max(concurrency, 1))
    async with build_async_client(cookies) as client:
        tasks = [
            download_single_article(
                client=client,
                semaphore=semaphore,
                index=index,
                article=article,
                output_dir=output_dir,
                account=account,
            )
            for index, article in enumerate(articles, start=1)
        ]
        return await asyncio.gather(*tasks)


async def download_single_article(
    *,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    index: int,
    article: dict[str, Any],
    output_dir: Path,
    account: dict[str, Any],
) -> dict[str, Any]:
    async with semaphore:
        try:
            response = await client.get(article["link"])
            response.raise_for_status()
            parsed = parse_article_content(response.text, article)

            base_name = f"{index:03d}_{safe_name(parsed['title'] or article['title'] or '未命名文章')}"
            markdown_path = output_dir / "markdown" / f"{base_name}.md"
            html_path = output_dir / "html" / f"{base_name}.html"

            markdown_path.write_text(
                build_markdown_document(parsed, article, account),
                encoding="utf-8",
            )
            html_path.write_text(response.text, encoding="utf-8")

            return {
                "status": "ok",
                "index": index,
                "title": parsed["title"] or article["title"],
                "url": article["link"],
                "markdown_file": str(markdown_path),
                "html_file": str(html_path),
                "publish_time": parsed.get("publish_time"),
            }
        except Exception as exc:  # noqa: BLE001
            return {
                "status": "error",
                "index": index,
                "title": article.get("title"),
                "url": article.get("link"),
                "error": str(exc),
            }


def parse_article_content(html_text: str, fallback: dict[str, Any]) -> dict[str, Any]:
    soup = BeautifulSoup(html_text, "html.parser")
    content_node = soup.select_one("#js_content") or soup.body
    title_node = soup.select_one("#activity-name")
    account_node = soup.select_one("#js_name")

    if content_node:
        for selector in [
            "script",
            "style",
            "#js_pc_qr_code",
            ".qr_code_pc_outer",
            ".original_primary_card",
            ".wx_profile_card_inner",
            ".discuss_container",
            "iframe",
        ]:
            for tag in content_node.select(selector):
                tag.decompose()
        for image in content_node.select("img"):
            data_src = image.get("data-src")
            if data_src:
                image["src"] = data_src

    title = title_node.get_text(" ", strip=True) if title_node else fallback.get("title") or ""
    account_name = account_node.get_text(" ", strip=True) if account_node else ""
    publish_time = parse_publish_time(html_text)
    content_html = str(content_node) if content_node else ""
    markdown = clean_markdown(html_to_markdown(content_html, heading_style="ATX"))

    return {
        "title": title,
        "account_name": account_name,
        "publish_time": publish_time,
        "markdown": markdown,
    }


def parse_publish_time(html_text: str) -> str | None:
    match = re.search(r'var\s+ct\s*=\s*"(\d+)";', html_text)
    if not match:
        match = re.search(r'"ct":(\d+)', html_text)
    if not match:
        return None

    timestamp = int(match.group(1))
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def clean_markdown(content: str) -> str:
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()


def build_markdown_document(
    parsed: dict[str, Any],
    article: dict[str, Any],
    account: dict[str, Any],
) -> str:
    lines = [
        f"# {parsed['title'] or article.get('title') or '未命名文章'}",
        "",
        f"- 公众号：{parsed.get('account_name') or account.get('nickname') or ''}",
        f"- 账号别名：{account.get('alias') or ''}",
        f"- 发布时间：{parsed.get('publish_time') or ''}",
        f"- 原文链接：{article.get('link') or ''}",
        "",
        "---",
        "",
        parsed.get("markdown") or "",
        "",
    ]
    return "\n".join(lines).strip() + "\n"


def safe_name(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', "_", value).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[:80] or "未命名"


def safe_json(response: httpx.Response) -> dict[str, Any]:
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(f"接口返回不是 JSON：{response.text[:200]}") from exc

    if isinstance(data, dict) and data.get("base_resp", {}).get("ret") not in (None, 0):
        raise RuntimeError(f"公众号后台接口报错：{data}")
    return data


if __name__ == "__main__":
    raise SystemExit(main())
