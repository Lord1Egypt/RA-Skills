"""
基于影刀录制的选择器，转换的 Playwright 脚本。
优化后拆分为明确步骤函数，并统一关键点击、等待、下载和错误记录逻辑。
"""
from __future__ import annotations

import argparse
import json
import platform
import random
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app_errors import DownloadError, LoginStateError, RpaStepError
from playwright.sync_api import FrameLocator, Page, sync_playwright


DEFAULT_STORAGE_STATE_FILE = Path(__file__).parent / "yingdao_storage_state.json"
DEFAULT_DOWNLOAD_DIR = Path(__file__).parent / "downloads"
DEFAULT_RUN_LOG_DIR = DEFAULT_DOWNLOAD_DIR / "run_logs"

CONFIG = {
    "download_dir": str(DEFAULT_DOWNLOAD_DIR),
    "run_log_dir": str(DEFAULT_RUN_LOG_DIR),
    "storage_state_file": str(DEFAULT_STORAGE_STATE_FILE),
    "headless": False,
    "timeout": 30000,
    "report_name": f"生意参谋报表_{datetime.now().strftime('%Y%m%d')}",
    "report_name_goods": f"生意参谋报表_商品_{datetime.now().strftime('%Y%m%d')}",
    "max_retries": 2,
    "strict_mode": True,
    "download_timeout_ms": 120000,
    "use_storage_state": True,
}


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def human_sleep(min_sec: float, max_sec: float) -> None:
    time.sleep(random.uniform(min_sec, max_sec))


def human_click(target: Page | FrameLocator, selector: str, offset_range: int = 5) -> None:
    locator = target.locator(selector).first
    locator.wait_for(state="visible", timeout=5000)
    try:
        box = locator.bounding_box(timeout=5000)
        if box:
            locator.click(
                position={
                    "x": box["width"] / 2 + random.uniform(-offset_range, offset_range),
                    "y": box["height"] / 2 + random.uniform(-offset_range, offset_range),
                },
                timeout=5000,
            )
            return
    except Exception:
        pass
    locator.click(timeout=5000)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="淘宝生意参谋 RPA")
    parser.add_argument("--safe-mode", action="store_true", help="一键稳妥配置")
    parser.add_argument("--headless", action="store_true", help="无头模式运行")
    parser.add_argument("--timeout-ms", type=int, default=30000, help="页面默认超时毫秒")
    parser.add_argument("--download-timeout-ms", type=int, default=120000, help="下载等待超时毫秒")
    parser.add_argument("--max-retries", type=int, default=2, help="关键步骤最大重试次数")
    parser.add_argument("--strict", action="store_true", help="关键步骤失败即终止")
    parser.add_argument("--no-storage-state", action="store_true", help="不复用本地登录态")
    parser.add_argument("--downloads-dir", default="", help="下载目录")
    parser.add_argument("--run-log-dir", default="", help="运行日志目录")
    parser.add_argument("--storage-state-file", default="", help="登录态文件路径")
    return parser.parse_args()


def apply_cli_overrides(args: argparse.Namespace) -> None:
    if args.safe_mode:
        CONFIG["strict_mode"] = True
        CONFIG["use_storage_state"] = False
        CONFIG["max_retries"] = 3
        CONFIG["download_timeout_ms"] = 180000
    else:
        CONFIG["strict_mode"] = bool(args.strict)
        CONFIG["use_storage_state"] = not bool(args.no_storage_state)
        CONFIG["max_retries"] = max(1, int(args.max_retries))
        CONFIG["download_timeout_ms"] = int(args.download_timeout_ms)
    CONFIG["headless"] = bool(args.headless)
    CONFIG["timeout"] = int(args.timeout_ms)
    if args.downloads_dir:
        CONFIG["download_dir"] = str(Path(args.downloads_dir).resolve())
    if args.run_log_dir:
        CONFIG["run_log_dir"] = str(Path(args.run_log_dir).resolve())
    if args.storage_state_file:
        CONFIG["storage_state_file"] = str(Path(args.storage_state_file).resolve())


def ensure_output_dirs() -> None:
    Path(CONFIG["download_dir"]).mkdir(parents=True, exist_ok=True)
    Path(CONFIG["run_log_dir"]).mkdir(parents=True, exist_ok=True)
    Path(CONFIG["storage_state_file"]).parent.mkdir(parents=True, exist_ok=True)


def page_state(page: Page) -> dict[str, str]:
    try:
        title = page.title()
    except Exception:
        title = ""
    return {"url": page.url, "title": title}


def record_step(step_results: list[dict], step_no: int, step_name: str, ok: bool, detail: str = "", extra: dict | str | None = None) -> None:
    item = {
        "ts": datetime.now().isoformat(),
        "step_no": step_no,
        "step_name": step_name,
        "ok": bool(ok),
        "detail": detail,
    }
    if extra is not None:
        item["extra"] = extra
    step_results.append(item)


def save_run_summary(step_results: list[dict], downloads: list[str], fatal_error: str | None = None) -> None:
    summary = {
        "timestamp": datetime.now().isoformat(),
        "ok": fatal_error is None and all(s["ok"] for s in step_results),
        "total_steps": len(step_results),
        "success_steps": sum(1 for s in step_results if s["ok"]),
        "failed_steps": [s for s in step_results if not s["ok"]],
        "downloads": downloads,
        "fatal_error": fatal_error,
    }
    out = Path(CONFIG["run_log_dir"]) / f"run_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"运行摘要: {out}")


def write_diagnostics() -> None:
    info = {
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "storage_state_path": CONFIG["storage_state_file"],
        "storage_state_exists": Path(CONFIG["storage_state_file"]).exists(),
        "config": CONFIG,
    }
    out = Path(CONFIG["run_log_dir"]) / f"diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"启动诊断: {out}")


def save_error_screenshot(page: Page, step_name: str) -> None:
    try:
        error_dir = Path(CONFIG["download_dir"]) / "errors"
        error_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = error_dir / f"error_{step_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=str(screenshot_path))
        log(f"错误截图已保存: {screenshot_path}")
    except Exception as exc:
        log(f"截图失败: {exc}")


def ensure_step(ok: bool, step_name: str) -> None:
    if ok:
        return
    if CONFIG["strict_mode"]:
        raise RpaStepError(f"{step_name} 失败，严格模式已中止执行")


def build_download_filename(prefix: str, suggested_filename: str | None) -> str:
    suffix = ".xlsx"
    if suggested_filename and Path(suggested_filename).suffix:
        suffix = Path(suggested_filename).suffix
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{suffix}"


def retry_action(action, step_name: str, retries: int | None = None) -> bool:
    attempts = retries if retries is not None else CONFIG["max_retries"]
    last_err = None
    for _ in range(attempts):
        try:
            action()
            return True
        except Exception as exc:
            last_err = exc
            human_sleep(0.3, 0.8)
    if last_err:
        log(f"{step_name} 重试失败: {last_err}")
    return False


def click_first(frame: FrameLocator | Page, selectors: list[str], step_name: str, *, exact_text: str | None = None) -> None:
    def action() -> None:
        if exact_text:
            frame.get_by_text(exact_text, exact=True).first.click(timeout=5000)
            return
        for selector in selectors:
            human_click(frame, selector)
            return
        raise RpaStepError(f"{step_name} missing selectors")
    ok = retry_action(action, step_name)
    ensure_step(ok, step_name)


def fill_first(frame: FrameLocator, selectors: list[str], value: str, step_name: str) -> None:
    def action() -> None:
        last_exc = None
        for selector in selectors:
            try:
                frame.locator(selector).first.fill(value, timeout=5000)
                return
            except Exception as exc:
                last_exc = exc
        raise RpaStepError(f"{step_name} failed: {last_exc}")
    ok = retry_action(action, step_name)
    ensure_step(ok, step_name)


def click_radio(frame: FrameLocator, label_text: str) -> None:
    def action() -> None:
        try:
            frame.get_by_label(label_text, exact=True).locator('input[type="radio"]').click(timeout=5000)
            return
        except Exception:
            pass
        selectors = [
            f'xpath=.//label[normalize-space(.)="{label_text}"]/span[@class="dt-oui-radio"]/input[@type="radio"]',
            f'xpath=.//label[normalize-space(.)="{label_text}"]/span/input[@type="radio"]',
            f'xpath=.//label[normalize-space(.)="{label_text}"]/input[@type="radio"]',
        ]
        for selector in selectors:
            try:
                human_click(frame, selector, offset_range=3)
                return
            except Exception:
                pass
        raise RpaStepError(f"无法选中单选项: {label_text}")
    ok = retry_action(action, f"选择单选项 {label_text}")
    ensure_step(ok, f"选择单选项 {label_text}")


def wait_for_login(page: Page, step_results: list[dict]) -> None:
    login_success = False
    for attempt in range(3):
        try:
            page.wait_for_selector('ul li a span:has-text("自助分析")', timeout=5000)
            login_success = True
            break
        except Exception:
            if "login" in page.url.lower() or page.url == "https://sycm.taobao.com/":
                log(f"检测到未登录（尝试 {attempt + 1}/3），请扫码登录。")
                human_sleep(5, 8)
    if not login_success:
        record_step(step_results, 1, "登录检测", False, "登录失败", page_state(page))
        raise LoginStateError("登录失败，请确认已成功扫码登录后重试。")
    record_step(step_results, 1, "登录检测", True, "已登录", page_state(page))


def open_business_report_page(page: Page, step_results: list[dict]) -> FrameLocator:
    log("Step 1: 打开生意参谋...")
    page.goto("https://sycm.taobao.com/mc/ci/shop/overview", timeout=30000)
    human_sleep(2, 3)
    record_step(step_results, 1, "打开生意参谋", True, extra=page_state(page))
    wait_for_login(page, step_results)
    page.context.storage_state(path=CONFIG["storage_state_file"])
    log("登录状态已保存")

    log("Step 2: 点击自助分析...")
    click_first(page, ['ul li a span:has-text("自助分析")'], "点击自助分析")
    record_step(step_results, 2, "点击自助分析", True)
    human_sleep(0.8, 1.8)

    log("Step 3: 点击取数报表...")
    click_first(page, ['ul li ul li div:has-text("取数报表")'], "点击取数报表")
    record_step(step_results, 3, "点击取数报表", True)
    human_sleep(1.5, 3)

    log("Step 4: 进入 iframe...")
    page.wait_for_selector("#jycm-insert-iframe", timeout=10000)
    frame = page.frame_locator("#jycm-insert-iframe")
    record_step(step_results, 4, "进入iframe", True)
    return frame


def wait_for_report_ready(frame: FrameLocator) -> None:
    frame.get_by_text("下载报表", exact=False).first.wait_for(timeout=CONFIG["download_timeout_ms"])


def select_recent_30_days(frame: FrameLocator, step_name: str) -> None:
    click_first(
        frame,
        [
            'xpath=.//div[@id="autoUpdateCycle"]//span[@class="dt-oui-radio"]/input[@type="radio"]',
            'xpath=.//div[@id="autoUpdateCycle"]//input[@type="radio"]',
        ],
        step_name,
    )


def download_report(page: Page, frame: FrameLocator, prefix: str, step_no: int, step_name: str, step_results: list[dict], downloaded_files: list[str]) -> None:
    log(f"Step {step_no}: {step_name}...")
    errors: list[str] = []
    for selector in [
        'xpath=.//button/span[normalize-space(.)="下载报表"]',
        'xpath=.//button[normalize-space(.)="下载报表"]',
    ]:
        try:
            wait_for_report_ready(frame)
            with page.expect_download(timeout=CONFIG["download_timeout_ms"]) as dl_info:
                human_click(frame, selector)
            download = dl_info.value
            save_path = Path(CONFIG["download_dir"]) / build_download_filename(prefix, download.suggested_filename)
            download.save_as(str(save_path))
            downloaded_files.append(str(save_path))
            record_step(step_results, step_no, step_name, True, str(save_path))
            log(f"下载成功: {save_path}")
            return
        except Exception as exc:
            errors.append(str(exc))
    record_step(step_results, step_no, step_name, False, "; ".join(errors))
    raise DownloadError(f"{step_name} 失败: {'; '.join(errors)}")


def generate_shop_report(frame: FrameLocator, step_results: list[dict]) -> None:
    log("Step 5: 选择自动更新...")
    click_radio(frame, "自动更新")
    record_step(step_results, 5, "选择自动更新", True)
    human_sleep(0.5, 1)

    log("Step 6: 选择最近30天...")
    select_recent_30_days(frame, "选择最近30天")
    record_step(step_results, 6, "选择最近30天", True)
    human_sleep(0.5, 1)

    log("Step 7: 填写报表名称...")
    fill_first(frame, ["input#reportName", 'input[type="text"]#reportName', 'xpath=//input[@id="reportName"]'], CONFIG["report_name"], "填写报表名称")
    record_step(step_results, 7, "填写报表名称", True, CONFIG["report_name"])

    log("Step 8: 点击生成报表...")
    click_first(
        frame,
        ['xpath=.//form//button[normalize-space(.)="生成报表"]', 'xpath=.//button[normalize-space(.)="生成报表"]'],
        "点击生成报表",
    )
    record_step(step_results, 8, "点击生成报表", True)
    human_sleep(6, 10)


def return_to_report_list(frame: FrameLocator, step_results: list[dict]) -> None:
    log("Step 10: 点击返回...")
    ok = retry_action(
        lambda: (
            frame.get_by_text("返回 |", exact=True).first.click(timeout=5000)
        ),
        "点击返回",
        retries=1,
    )
    if not ok:
        ok = retry_action(lambda: frame.locator(".report-generation-sycm-title-back").first.click(timeout=5000), "点击返回")
    if not ok:
        ok = retry_action(lambda: frame.get_by_text("返回", exact=False).first.click(timeout=5000), "点击返回")
    ensure_step(ok, "点击返回")
    record_step(step_results, 10, "点击返回", True)
    human_sleep(2, 4)


def generate_goods_report(frame: FrameLocator, step_results: list[dict]) -> None:
    log("Step 11: 选择商品维度...")
    click_first(
        frame,
        [
            'xpath=.//label[normalize-space(.)="商品"]/span/input[@type="radio"][@value="商品"]',
            'xpath=.//label[normalize-space(.)="商品"]/span/input[@type="radio"]',
        ],
        "选择商品维度",
    )
    record_step(step_results, 11, "选择商品维度", True)
    human_sleep(1, 2)

    log("Step 12: 选择自动更新（第二轮）...")
    click_radio(frame, "自动更新")
    record_step(step_results, 12, "选择自动更新(第二轮)", True)

    log("Step 13: 选择最近30天（第二轮）...")
    select_recent_30_days(frame, "选择最近30天(第二轮)")
    record_step(step_results, 13, "选择最近30天(第二轮)", True)

    log("Step 14: 搜索商品（留空=全店）...")
    click_first(
        frame,
        [
            'xpath=.//form//span/input[@type="text"][@placeholder="请输入商品关键字或商品id"]',
            'xpath=.//input[@placeholder="请输入商品关键字或商品id"]',
        ],
        "搜索商品(留空)",
    )
    record_step(step_results, 14, "搜索商品(留空)", True)
    human_sleep(0.3, 0.8)

    log("Step 15: 一键全选...")
    click_first(
        frame,
        ['xpath=.//form//ul/li//button[normalize-space(.)="一键全选"]', 'xpath=.//button[normalize-space(.)="一键全选"]'],
        "一键全选",
    )
    record_step(step_results, 15, "一键全选", True)
    human_sleep(1, 2)

    log("Step 16: 填写报表名称（第二轮）...")
    fill_first(frame, ["input#reportName", 'input[type="text"]#reportName', 'xpath=//input[@id="reportName"]'], CONFIG["report_name_goods"], "填写报表名称(第二轮)")
    record_step(step_results, 16, "填写报表名称(第二轮)", True, CONFIG["report_name_goods"])

    log("Step 17: 点击生成报表（第二轮）...")
    click_first(
        frame,
        ['xpath=.//form//button[normalize-space(.)="生成报表"]', 'xpath=.//button[normalize-space(.)="生成报表"]'],
        "点击生成报表(第二轮)",
    )
    record_step(step_results, 17, "点击生成报表(第二轮)", True)
    human_sleep(6, 10)


def capture_diagnostics(step_results: list[dict], downloaded_files: list[str]) -> None:
    log("Step 19: 校验下载结果...")
    if not downloaded_files:
        record_step(step_results, 19, "校验下载结果", False, "no downloads")
        ensure_step(False, "校验下载结果")
        return
    record_step(step_results, 19, "校验下载结果", True, f"count={len(downloaded_files)}")
    for path in downloaded_files:
        log(f"已下载: {path}")


def run() -> None:
    args = parse_args()
    apply_cli_overrides(args)
    ensure_output_dirs()
    write_diagnostics()

    step_results: list[dict] = []
    downloaded_files: list[str] = []
    fatal_error = None

    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(
                headless=CONFIG["headless"],
                args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-setuid-sandbox"],
            )
        except Exception as exc:
            raise RpaStepError(
                f"Chromium 启动失败: {exc}。请先运行: python -m playwright install chromium"
            ) from exc

        storage_state_path = Path(CONFIG["storage_state_file"])
        storage_state = str(storage_state_path) if CONFIG["use_storage_state"] and storage_state_path.exists() else None
        log("发现保存的登录状态，尝试自动登录..." if storage_state else "未找到登录状态，将进行扫码登录...")

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            accept_downloads=True,
            storage_state=storage_state,
        )
        page = context.new_page()
        page.set_default_timeout(CONFIG["timeout"])

        try:
            frame = open_business_report_page(page, step_results)
            generate_shop_report(frame, step_results)
            download_report(page, frame, "shop", 9, "下载报表(第一轮)", step_results, downloaded_files)
            human_sleep(3, 5)
            return_to_report_list(frame, step_results)
            generate_goods_report(frame, step_results)
            download_report(page, frame, "goods", 18, "下载报表(第二轮)", step_results, downloaded_files)
            human_sleep(3, 5)
            capture_diagnostics(step_results, downloaded_files)
            log("全部流程执行完成")
        except Exception as exc:
            fatal_error = str(exc)
            log(f"执行异常: {exc}")
            save_error_screenshot(page, "fatal_error")
            raise
        finally:
            save_run_summary(step_results, downloaded_files, fatal_error=fatal_error)
            context.close()
            browser.close()


if __name__ == "__main__":
    run()
