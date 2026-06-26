#!/usr/bin/env python3
"""共享工具函数：session 管理、浏览器初始化、登录检测、状态文件读写、日志配置。"""

import os
import json
import asyncio
import logging
import random
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field
from agentbay import (
    AsyncAgentBay, CreateSessionParams, BrowserContext,
    BrowserOption, BrowserFingerprint, BrowserProxy, ExtractOptions,
)
from agentbay import AgentBayLogger
from playwright.async_api import async_playwright

# ── 路径常量 ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config.json"
STATUS_PATH = BASE_DIR / "status.md"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

# 模块级 logger，所有脚本共享同一实例
_log = logging.getLogger("xhs")


# ── 日志配置 ────────────────────────────────────────────────────
_LOG_MAX_TOTAL_BYTES = 10 * 1024 * 1024  # 10 MB


def _cleanup_old_logs(max_bytes: int = _LOG_MAX_TOTAL_BYTES) -> None:
    """若 logs/ 目录总大小超过 max_bytes，按修改时间从旧到新删除，直到低于限制。"""
    log_files = sorted(LOG_DIR.glob("*.log"), key=lambda f: f.stat().st_mtime)
    total = sum(f.stat().st_size for f in log_files)
    deleted = []
    for f in log_files:
        if total <= max_bytes:
            break
        total -= f.stat().st_size
        f.unlink()
        deleted.append(f.name)
    if deleted:
        print(f"[log cleanup] 已删除旧日志: {', '.join(deleted)}")


def setup_logging(script_name: str) -> logging.Logger:
    """初始化日志：脚本日志 + AgentBay SDK 日志统一写入同一个文件。
    日志路径：logs/{script_name}_{timestamp}.log
    各脚本在 main() 最开始调用一次，返回配置好的 logger。
    创建新文件前若 logs/ 总大小超过 10 MB，自动删除最旧的日志。
    """
    LOG_DIR.mkdir(exist_ok=True)
    _cleanup_old_logs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"{script_name}_{timestamp}.log"

    # ── 脚本自身日志（Python logging 模块） ──────────────────────
    _log.setLevel(logging.DEBUG)
    _log.handlers.clear()  # 避免多次调用时重复 handler

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    _log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    _log.addHandler(ch)

    # ── AgentBay SDK 日志（loguru）重定向到同一文件 ──────────────
    # AgentBayLogger.setup 会清除旧 handler 并重新注册，
    # force_reinit=True 确保每次脚本启动都以新文件路径生效。
    AgentBayLogger.setup(
        level="INFO",
        log_file=log_path,
        enable_console=True,   # 保持控制台输出
        enable_file=True,
        force_reinit=True,
    )

    _log.info(f"=== {script_name} 启动 ===")
    _log.info(f"日志文件: {log_path}")
    return _log


# ── 配置读写 ────────────────────────────────────────────────────
def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def save_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


# ── 状态文件写入 ────────────────────────────────────────────────
def write_status(status: str, extra: dict | None = None) -> None:
    """写入 status.md，记录当前运行状态供大模型 / 调用方读取。"""
    lines = [
        "# 小红书采集状态",
        "",
        f"**状态**: {status}",
        f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    if extra:
        for k, v in extra.items():
            lines.append(f"**{k}**: {v}")
        lines.append("")
    STATUS_PATH.write_text("\n".join(lines), encoding="utf-8")
    _log.info(f"[status] {status}")


def read_status_value() -> str:
    """读取 status.md 中的当前状态值；不存在或无法解析时返回空字符串。"""
    if not STATUS_PATH.exists():
        return ""

    for line in STATUS_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("**状态**:"):
            return line.split(":", 1)[1].strip()
    return ""


def clear_error_status() -> None:
    """仅在 status.md 当前为 error 时删除它，避免旧错误状态干扰后续步骤。"""
    if read_status_value() != "error":
        return
    STATUS_PATH.unlink(missing_ok=True)
    _log.info("[status] cleared stale error")


# ── AgentBay 环境变量 ───────────────────────────────────────────
_AGENTBAY_CONFIG_KEYS = [
    "agentbay_api_key",
    "agentbay_region_id",
    "agentbay_endpoint",
    "agentbay_timeout_ms",
]


def setup_env(cfg: dict) -> None:
    """将 config.json 中的配置写入环境变量。
    
    优先级规则：
    1. agentbay_api_key: config.json > 环境变量 AGENTBAY_API_KEY
       - config 有值则始终覆盖（方便多项目切换）
       - 如果 config 和环境变量都为空，则环境配置失败
    
    2. 其他配置 (region_id, endpoint, timeout_ms): config.json > 环境变量
       - 不设置默认值，优先使用 config.json 中的配置
       - 如果 config 未配置，则使用环境变量中的值
       - 如果都没有，则设置为空字符串
    """
    # 处理 agentbay_api_key
    api_key = cfg.get("agentbay_api_key") or os.getenv("AGENTBAY_API_KEY", "")
    if api_key:
        os.environ["AGENTBAY_API_KEY"] = api_key
    
    # 处理其他配置项
    config_mapping = {
        "agentbay_region_id": "AGENTBAY_REGION_ID",
        "agentbay_endpoint": "AGENTBAY_ENDPOINT",
        "agentbay_timeout_ms": "AGENTBAY_TIMEOUT_MS",
    }
    
    for cfg_key, env_key in config_mapping.items():
        val = cfg.get(cfg_key)
        if val:
            os.environ[env_key] = str(val)
        else:
            # 使用环境变量中的值，如果没有则设为空字符串
            os.environ[env_key] = os.getenv(env_key, "")


def validate_agentbay_env(cfg: dict) -> tuple[bool, str]:
    """前置环境检查，脚本启动最早期调用。返回 (ok, error_message)。
    
    检查项：
    1. agentbay_api_key: 必须提供（config.json 或环境变量均可）
       - 如果缺失，写入 error 状态并返回 False
    
    失败时调用方应写 status.md 并以退出码 1 结束。
    """
    api_key = cfg.get("agentbay_api_key") or os.getenv("AGENTBAY_API_KEY", "")
    if not api_key:
        return False, (
            "缺少 AgentBay API Key，当前无法执行小红书搜索 skill。\n"
            "解决方法（二选一）：\n"
            "  1. 在 config.json 的 agentbay_api_key 字段填写密钥（推荐）\n"
            "  2. 设置环境变量：export AGENTBAY_API_KEY=<your-key>\n"
            "\n"
            "如需开通 AgentBay 服务，请访问：https://www.aliyun.com/product/agentbay"
        )
    return True, ""




# ── Session 管理 ────────────────────────────────────────────────
async def get_or_create_browser_context(agent_bay, context_name: str) -> BrowserContext:
    result = await agent_bay.context.get(name=context_name, create=True)
    if not result.success or not result.context:
        raise RuntimeError(f"Failed to get/create context '{context_name}': {result.error_message}")
    ctx_id = result.context_id or result.context.id
    _log.info(f"Browser context: {context_name} (id={ctx_id})")
    return BrowserContext(context_id=ctx_id, auto_upload=True)


async def create_or_reuse_session(cfg: dict):
    """返回 (agent_bay, session, is_reused)。"""
    api_key = os.environ["AGENTBAY_API_KEY"]
    agent_bay = AsyncAgentBay(api_key=api_key)
    session_id = cfg.get("session_id", "")
    _log.info(f"session_id: {session_id}, api_key:{api_key}")
    if session_id:
        try:
            result = await agent_bay.get(session_id)
            if result.success and result.session:
                _log.info(f"✅ 复用 session: {session_id}")
                return agent_bay, result.session, True
            _log.warning(f"session {session_id} 获取失败，尝试创建session")
        except Exception as e:
            _log.warning(f"session 获取异常: {e}，新建")

    browser_context = None
    context_name = cfg.get("context_name", "")
    if context_name:
        browser_context = await get_or_create_browser_context(agent_bay, context_name)

    params = CreateSessionParams(
        image_id=cfg.get("image_id", "linux_latest"),
        browser_context=browser_context,
    )
    result = await agent_bay.create(params)
    if not result.success:
        raise RuntimeError(f"Create session failed: {result.error_message}")
    _log.info(f"✅ 新建 session: {result.session.session_id}")
    return agent_bay, result.session, False


def _build_proxies(cfg: dict) -> list[BrowserProxy]:
    """根据 config.json 的 proxy.server 构建代理列表，server 为空则不使用代理。"""
    proxy_cfg = cfg.get("proxy") or {}
    server = proxy_cfg.get("server", "")
    if not server:
        return []
    kwargs: dict = {"proxy_type": "custom", "server": server}
    if proxy_cfg.get("username"):
        kwargs["username"] = proxy_cfg["username"]
    if proxy_cfg.get("password"):
        kwargs["password"] = proxy_cfg["password"]
    return [BrowserProxy(**kwargs)]


async def initialize_browser(session, cfg: dict | None = None) -> str:
    """初始化浏览器，返回 cdp_url。"""
    proxies = _build_proxies(cfg or {})
    opt = BrowserOption(
        use_stealth=True,
        solve_captchas=True,
        fingerprint=BrowserFingerprint(
            devices=["desktop"],
            operating_systems=["windows"],
            locales=["zh-CN"],
        ),
        proxies=proxies if proxies else None,
    )
    if not await session.browser.initialize(opt):
        await session.delete()
        raise RuntimeError("Browser initialize failed")
    cdp_url = await session.browser.get_endpoint_url()
    _log.info(f"CDP: {cdp_url[:80]}...")
    await asyncio.sleep(2)
    try:
        info = await session.info()
        if info.success and info.data:
            _log.info(f"Resource URL: {info.data.resource_url}")
    except Exception:
        pass
    return cdp_url


async def get_cdp_url(session, is_reused: bool, cfg: dict | None = None) -> str:
    return await initialize_browser(session, cfg)


# ── 登录检测 ────────────────────────────────────────────────────
class LoginStatus(BaseModel):
    is_logged_in: bool = Field(description="当前页面是否已经登录")


async def check_login_status(agent, page) -> bool:
    try:
        ok, data = await agent.extract(
            options=ExtractOptions[LoginStatus](
                instruction="检查当前页面是否已经登录，有用户头像、昵称、个人中心等则为已登录",
                schema=LoginStatus,
                use_text_extract=True,
            ),
            page=page,
        )
        if not ok or data is None:
            return False
        _log.info(f"登录状态: {'已登录' if data.is_logged_in else '未登录'}")
        return data.is_logged_in
    except Exception as e:
        _log.warning(f"登录检测异常: {e}")
        return False


# ── 拟人滚动 ────────────────────────────────────────────────────
async def _human_scroll(page, total_delta: int) -> None:
    num_steps = random.randint(2, 4)
    step = max(total_delta // num_steps, 20)
    for _ in range(num_steps):
        await page.mouse.wheel(0, step + random.randint(-30, 30))
        await asyncio.sleep(random.uniform(0.1, 0.3))


async def scroll_comment_area(page, scroll_rounds: int = 10) -> None:
    bottom = await page.query_selector('.bottom-container')
    if bottom:
        await bottom.click()
        await asyncio.sleep(random.uniform(0.3, 0.6))
    viewport_h = (page.viewport_size or {}).get("height") or await page.evaluate("window.innerHeight")
    for i in range(scroll_rounds):
        delta = max(int(viewport_h * random.uniform(1.0, 1.2)), 200)
        await _human_scroll(page, delta)
        pause = random.uniform(0.8, 1.2)
        _log.info(f"  滚动 {i + 1}/{scroll_rounds}，delta={delta}，停顿 {pause:.1f}s")
        await asyncio.sleep(pause)
        # comment-end
        end = await page.query_selector('.end-container')
        if end and await end.is_visible():
            _log.info(f"  评论底部（第 {i + 1} 次）")
            return
        # class_name = "no-comments"
        no_comments = await page.query_selector('.no-comments')
        if no_comments and await no_comments.is_visible():
            _log.info(f"  无评论（第 {i + 1} 次）")
            return

    _log.info(f"  完成 {scroll_rounds} 次滚动")


# ── 清理 ────────────────────────────────────────────────────────
async def cleanup(agent_bay, session, browser=None) -> None:
    try:
        if browser:
            await browser.close()
        if session:
            r = await agent_bay.delete(session, sync_context=True)
            if r.success:
                _log.info("✅ session 删除成功")
            else:
                _log.error(f"❌ session 删除失败: {r.error_message}")
    except Exception as e:
        _log.warning(f"清理异常: {e}")
