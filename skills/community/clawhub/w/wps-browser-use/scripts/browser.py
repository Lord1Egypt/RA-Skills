"""
Browser Automation Library - Powered by nodriver (Chromium CDP)

本模块作为库使用，由 AI 生成代码后 import；**单例在包内创建**，直接调用模块级函数即可：

    import sys
    sys.path.insert(0, "skills/browser/scripts")
    import browser

    print(browser.navigate("https://www.baidu.com"))
    print(browser.click(1))
    print(browser.fill(0, "搜索内容"))

每次 navigate() 会销毁当前 Browser 封装单例（断开 CDP、停止后台事件循环线程）并重新创建实例；其它 API 仍复用当前单例。

所有公开方法均返回 str 快照报告，格式为：
    [操作摘要]
    ---
    Title: ...
    URL:   ...
    ---
    Interactive elements (index[:]info):
    0[:] input type="text" placeholder="搜索"
    1[:] button | 百度一下
    ...
    ---
    Page Text:
    ...页面可见文本...
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import nodriver as uc
from nodriver import cdp
from IPython.display import Image, display

logger = logging.getLogger(__name__)


_BRWS_REQ_PREFIX = "__BRWS_REQ__"

# navigate：在 wait_for / 快照前等待 DOMContentLoaded，避免与导航早期阶段叠在一起直至 wait_for 默认 10s 超时
_PAGE_DCL_PROMISE_JS = (
    "(() => {"
    " if (document.readyState === 'interactive' || document.readyState === 'complete') "
    "return Promise.resolve(null);"
    " return new Promise((resolve) => {"
    " document.addEventListener('DOMContentLoaded', () => resolve(null), { once: true });"
    " });"
    "})()"
)

# navigate 会拆除旧单例并新建；与 __new__ 的 _lock 配合，避免在持有 _lock 时再次 Browser() 死锁
_NAVIGATE_SWAP_LOCK = threading.Lock()


def _request_browser() -> str:
    """
    发送 input("__BRWS_REQ__<json>")，由 JupyterExecutor 截获并转发给前端。
    """
    try:
        response = input(f"{_BRWS_REQ_PREFIX}{{}}")
        browser_config = json.loads(response.strip())
        if browser_config.get("type") == "cdp" and browser_config.get("cdp_endpoint"):
            return browser_config.get("cdp_endpoint")
        return ""
    except EOFError:
        return ""


def _request_browser_failed() -> None:
    raise RuntimeError("浏览器启动失败")


def _parse_musa_cdp_endpoint(raw: str) -> tuple[str, int]:
    """解析 MUSA_CDP_ENDPOINT，例如 http://127.0.0.1:9222 → (host, port)。"""
    s = raw.strip()
    if not s:
        raise RuntimeError("MUSA_CDP_ENDPOINT 为空")
    if "://" not in s:
        s = "http://" + s
    u = urlparse(s)
    host = u.hostname
    if not host:
        raise RuntimeError(f"MUSA_CDP_ENDPOINT 无法解析主机名: {raw!r}")
    port = u.port if u.port is not None else 9222
    return host, port


class Browser:
    """
    nodriver（Chromium CDP）浏览器自动化封装，专为纯文本 agent 设计。

    架构：专用后台线程运行 asyncio 事件循环，对外通过 run_coroutine_threadsafe 提交协程，
    避免与 Jupyter 主线程事件循环冲突。
    """

    MAX_TEXT_LEN = 10000
    MAX_ELEMENTS = 100

    _instance: Browser | None = None
    _lock = threading.Lock()

    def __new__(cls) -> Browser:
        with cls._lock:
            if cls._instance is not None and cls._instance._worker_thread.is_alive():
                return cls._instance
            self = super().__new__(cls)
            cls._instance = self
            return self

    @classmethod
    def _clear_singleton_and_teardown_old(cls) -> None:
        """将类级单例置空，并停止旧实例的 CDP 与后台事件循环线程。"""
        with cls._lock:
            old = cls._instance
            cls._instance = None
        if old is None:
            return
        try:
            loop = old._loop
            if loop is not None and not loop.is_closed():
                fut = asyncio.run_coroutine_threadsafe(old._async_do_stop(), loop)
                fut.result(timeout=30)
        except Exception:
            logger.debug("navigate 重置：停止 CDP 失败", exc_info=True)
        try:
            loop = old._loop
            if loop is not None and loop.is_running():
                loop.call_soon_threadsafe(loop.stop)
        except Exception:
            pass
        try:
            old._worker_thread.join(timeout=30)
        except Exception:
            pass

    def __init__(self):
        if getattr(self, "_singleton_initialized", False):
            return
        self._singleton_initialized = True

        self._loop: asyncio.AbstractEventLoop | None = None
        self._loop_ready = threading.Event()
        self._browser = None
        self._tab = None

        self._last_raw_elements: list = []

        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
        self._loop_ready.wait(timeout=30)
        if not self._loop:
            raise RuntimeError("浏览器后台事件循环未能启动")

    # ── 后台线程：专用 asyncio 循环 ──────────────────────────

    def _worker_loop(self):
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        def _exception_handler(loop: asyncio.AbstractEventLoop, context: dict) -> None:
            # nodriver 在 CDP 连接关闭后仍有 fire-and-forget 的 send() / update_targets() Task 在排队，
            # 连接正常关闭（code 1000）时这些 Task 会抛 ConnectionClosedOK；
            # 浏览器/远端 CDP 已退出时，未 await 的 Task 会抛 ConnectionRefusedError（WinError 1225 等），
            # 同样属于收尾噪声，不应污染 Jupyter 日志。
            exc = context.get("exception")
            msg = str(context.get("message") or "")
            if exc is not None:
                try:
                    from websockets.exceptions import ConnectionClosed, ConnectionClosedOK

                    if isinstance(exc, ConnectionClosedOK):
                        return
                    if msg.startswith("Task exception was never retrieved") and isinstance(exc, ConnectionClosed):
                        return
                except ImportError:
                    pass
                if msg.startswith("Task exception was never retrieved") and isinstance(
                    exc, (ConnectionRefusedError, ConnectionResetError, BrokenPipeError)
                ):
                    return
            loop.default_exception_handler(context)

        loop.set_exception_handler(_exception_handler)
        self._loop = loop

        def _mark_ready():
            self._loop_ready.set()

        loop.call_soon(_mark_ready)
        try:
            loop.run_forever()
        finally:
            # stop() 之后若仍留有 nodriver Connection._listener 等 Task，不取消并 drain 就 close，
            # 协程在 GC 阶段收尾会触发「Event loop is closed」（Jupyter 报 Exception ignored in coroutine）。
            try:
                if not loop.is_closed():
                    pending = [t for t in asyncio.all_tasks(loop) if not t.done()]
                    for t in pending:
                        t.cancel()
                    if pending:
                        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception:
                logger.debug("[Browser] worker 退出：取消残余 asyncio 任务失败", exc_info=True)
            try:
                if not loop.is_closed():
                    loop.close()
            except Exception:
                logger.debug("[Browser] worker 退出：关闭事件循环失败", exc_info=True)

    def _async_run(self, coro: Any) -> Any:
        if self._loop is None:
            raise RuntimeError("事件循环未就绪")
        fut = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return fut.result(timeout=60)

    # -- nodriver init --

    async def _async_ensure_page_tab(self) -> None:
        """
        连接已有 CDP 时，若 targets 为空则 main_tab 会 IndexError。
        有 page 型 tab 则直接返回；targets 为空时不等待，立即 create_target(about:blank)，再短轮询直至可见。
        """
        br = self._browser
        if br is None:
            raise RuntimeError("浏览器未初始化")

        await br.update_targets()
        if br.tabs:
            return
        if br.targets:
            return

        conn = getattr(br, "connection", None)
        if conn is None or conn.closed:
            raise RuntimeError("CDP 连接不可用，无法创建页签")

        try:
            await conn.send(
                cdp.target.create_target(
                    "about:blank",
                    enable_begin_frame_control=True,
                )
            )
        except Exception as e:
            logger.debug("create_target(about:blank) 失败", exc_info=True)
            raise RuntimeError(
                "浏览器暂无可用页签且无法自动新建，请在前端打开浏览器窗口或保留至少一个标签页后重试。"
            ) from e

        for _ in range(10):
            await br.update_targets()
            if br.tabs:
                return
            await asyncio.sleep(0.1)

        raise RuntimeError("已请求新建页签，但未在 CDP 中发现 page 目标，请重试。")

    def _page_tab_target_ids(self) -> set[Any]:
        br = self._browser
        if br is None:
            return set()
        out: set[Any] = set()
        for t in br.tabs:
            tid = getattr(t, "target_id", None)
            if tid is not None:
                out.add(tid)
        return out

    async def _async_adopt_new_tab_if_opened(self, before_ids: set[Any]) -> None:
        """若出现新的 page 目标（如新标签页），将 self._tab 切到该页（取最后一个新目标）。"""
        br = self._browser
        if br is None:
            return
        for _ in range(30):
            await br.update_targets()
            new_tabs = [
                t
                for t in br.tabs
                if getattr(t, "target_id", None) is not None and getattr(t, "target_id", None) not in before_ids
            ]
            if new_tabs:
                chosen = new_tabs[-1]
                self._tab = chosen
                logger.debug("[Browser] 已切换到新开标签 target_id=%s", getattr(chosen, "target_id", "?"))
                try:
                    await self._tab
                except Exception:
                    pass
                return
            await asyncio.sleep(0.1)

    async def _async_do_start(self, cdp_endpoint: str):
        host, port = _parse_musa_cdp_endpoint(cdp_endpoint)
        # host + port 同时传入时 nodriver 仅连接已有 CDP，不启动本进程浏览器
        self._browser = await uc.start(
            host=host, port=port, browser_executable_path=os.environ.get("MUSA_BROWSER_EXECUTABLE_PATH", "").strip()
        )
        await self._async_ensure_page_tab()
        self._tab = self._browser.main_tab
        _anti_notify = (
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
            "(() => {"
            "  const deny = () => Promise.resolve('denied');"
            "  if (typeof Notification !== 'undefined') {"
            "    try {"
            "      Object.defineProperty(Notification, 'permission', { get: () => 'denied' });"
            "    } catch (e) {}"
            "    Notification.requestPermission = deny;"
            "  }"
            "})();"
        )
        await self._tab.send(cdp.page.add_script_to_evaluate_on_new_document(source=_anti_notify))
        await self._tab

    async def _async_do_stop(self):
        self._last_raw_elements = []
        tab, br = self._tab, self._browser
        self._tab = None
        self._browser = None
        if br is None:
            return

        try:
            if tab is not None and not tab.closed:
                try:
                    await tab.send(cdp.page.close())
                except Exception:
                    logger.debug("cdp.page.close 失败", exc_info=True)
                try:
                    await tab.disconnect()
                except Exception:
                    logger.debug("tab.disconnect 失败", exc_info=True)

            conn = getattr(br, "connection", None)
            if conn is not None and not conn.closed:
                try:
                    await conn.disconnect()
                except Exception:
                    logger.debug("browser.connection.disconnect 失败", exc_info=True)
        except Exception:
            logger.debug("关闭当前页签/连接时异常", exc_info=True)

        try:
            uc.core.util.get_registered_instances().discard(br)
        except Exception:
            pass

    # ── 小工具 ────────────────────────────────

    @staticmethod
    def _eval_error_payload(result: Any) -> str | None:
        if result is None:
            return None
        try:
            from nodriver.cdp.runtime import ExceptionDetails
        except ImportError:
            ExceptionDetails = ()  # type: ignore[misc, assignment]
        if ExceptionDetails and isinstance(result, ExceptionDetails):
            return str(result)
        return None

    async def _tab_eval(self, expression: str) -> Any:
        r = await self._tab.evaluate(expression, return_by_value=True)
        err = self._eval_error_payload(r)
        if err:
            raise RuntimeError(err)
        return r

    async def _wait_dom_content_loaded(self, timeout: float) -> None:
        """当前页在 DOMContentLoaded 之后再继续（wait_for / 快照依赖可执行的 document）。"""
        if self._tab is None:
            raise RuntimeError("tab 未就绪")

        async def _run() -> None:
            r = await self._tab.evaluate(
                _PAGE_DCL_PROMISE_JS,
                await_promise=True,
                return_by_value=True,
            )
            err = self._eval_error_payload(r)
            if err:
                raise RuntimeError(err)

        await asyncio.wait_for(_run(), timeout=timeout)

    async def _element_visible(self, el) -> bool:
        try:
            v = await el.apply(
                """(e) => {
  const r = e.getBoundingClientRect();
  const s = window.getComputedStyle(e);
  return r.width > 0 && r.height > 0 && s.visibility !== 'hidden'
    && s.display !== 'none' && parseFloat(s.opacity || '1') > 0;
}""",
                return_by_value=True,
            )
            return bool(v)
        except Exception:
            return False

    async def _attr(self, el, name: str) -> str:
        try:
            # 用 JSON 编码属性名，避免 name 中含引号、反斜杠、控制字符时破坏 JS 或注入
            js_name = json.dumps(name)
            v = await el.apply(f"(e) => e.getAttribute && e.getAttribute({js_name})", return_by_value=True)
            return (v or "") if isinstance(v, str) else ""
        except Exception:
            return ""

    async def _inner_text(self, el) -> str:
        try:
            t = await el.apply("(e) => (e.innerText || '').trim()", return_by_value=True)
            return str(t or "")[:60]
        except Exception:
            return ""

    # ── 快照 ──────────────────────────────────

    async def _extract_page_text(self) -> str:
        try:
            raw = await self._tab_eval("(function(){ return document.body ? document.body.innerText : ''; })()")
            raw = raw or ""
        except Exception:
            return ""
        result = []
        for line in str(raw).splitlines():
            s = line.strip()
            if not s or len(s) > 1000:
                continue
            alnum = sum(1 for c in s if c.isalnum() or "\u4e00" <= c <= "\u9fff")
            if alnum >= len(s) * 0.3:
                result.append(s)
        return "\n".join(result)

    async def _extract_elements(self) -> tuple[list, list[dict]]:
        try:
            all_els = await self._tab.query_selector_all("a, button, input, select, textarea")
        except Exception:
            return [], []
        if not all_els:
            return [], []

        raw, info = [], []
        idx = 0
        for el in all_els:
            try:
                await el.update()
                if not await self._element_visible(el):
                    continue
                tag = (el.tag or "").lower()
                el_type = (await self._attr(el, "type")).lower()
                el_name = await self._attr(el, "name")
                el_ph = await self._attr(el, "placeholder")
                el_val = await self._attr(el, "value")
                el_href = await self._attr(el, "href")
                el_text = await self._inner_text(el)

                if tag == "input" and el_type == "hidden":
                    continue

                parts = [tag]
                if el_type and el_type != tag:
                    parts.append(f'type="{el_type}"')
                if el_name:
                    parts.append(f'name="{el_name}"')
                if el_ph:
                    parts.append(f'placeholder="{el_ph[:40]}"')
                if el_href:
                    parts.append(f'href="{el_href[:60]}"')

                if tag == "select":
                    try:
                        options = await el.apply(
                            "(e) => Array.from(e.options).map(o => o.text.trim())",
                            return_by_value=True,
                        )
                        selected = await el.apply(
                            "(e) => e.options[e.selectedIndex] ? e.options[e.selectedIndex].text.trim() : ''",
                            return_by_value=True,
                        )
                        options = options or []
                        opts_str = " / ".join(str(x) for x in list(options)[:10])
                        if len(options) > 10:
                            opts_str += f" … (+{len(options)-10})"
                        display = f'selected="{selected}" options=[{opts_str}]'
                    except Exception:
                        display = el_text
                else:
                    display = el_val[:40] if tag == "input" and el_val else el_text

                desc = " ".join(parts)
                if display:
                    desc += f" | {display}"

                raw.append(el)
                info.append({"index": idx, "info": desc})
                idx += 1
            except Exception:
                continue

        return raw, info

    def _save_text(self, text: str, prefix: str) -> str:
        workspace_dir = os.environ.get("workspace_dir", "/tmp")
        filename = f"{prefix}_{int(time.time())}.txt"
        path = os.path.join(workspace_dir, filename)
        try:
            os.makedirs(workspace_dir, exist_ok=True)
            Path(path).write_text(text, encoding="utf-8")
        except Exception:
            path = os.path.join("/tmp", filename)
            Path(path).write_text(text, encoding="utf-8")
        return path

    async def _page_title_url(self) -> tuple[str, str]:
        try:
            await self._tab
            title = await self._tab_eval("document.title")
            url = getattr(self._tab, "url", None) or getattr(self._tab.target, "url", "") or ""
            return str(title or ""), str(url or "")
        except Exception:
            return "", ""

    async def _snapshot(self, op_summary: str) -> str:
        page_text = await self._extract_page_text()
        r, inf = await self._extract_elements()
        self._last_raw_elements = r

        text_note = ""
        if len(page_text) > self.MAX_TEXT_LEN:
            saved = self._save_text(page_text, "page_text")
            text_note = (
                f"\n[文本共 {len(page_text)} 字符，此处显示前 {self.MAX_TEXT_LEN} 字符。"
                f"完整内容已保存至：{saved}，可用 jupyter_cell_exec工具 读取。]"
            )
            page_text = page_text[: self.MAX_TEXT_LEN]

        elements_note = ""
        if len(inf) > self.MAX_ELEMENTS:
            all_text = "\n".join(f"{el['index']}[:]{el['info']}" for el in inf)
            saved = self._save_text(all_text, "page_elements")
            elements_note = (
                f"\n[可交互元素共 {len(inf)} 个，此处显示前 {self.MAX_ELEMENTS} 个。"
                f"完整列表已保存至：{saved}，可用 jupyter_cell_exec工具 读取。]"
            )
            inf = inf[: self.MAX_ELEMENTS]

        title, url = await self._page_title_url()

        lines = [
            op_summary,
            "---",
            f"Title: {title}",
            f"URL:   {url}",
            "---",
            "Interactive elements (index[:]info):",
            *[f"{el['index']}[:]{el['info']}" for el in inf],
            *([elements_note] if elements_note else []),
            "---",
            "Page Text:",
            page_text,
            *([text_note] if text_note else []),
        ]
        return "\n".join(lines)

    async def _write_temp_screenshot(self) -> str | None:
        try:
            if self._tab is None:
                return None
            fd, path = tempfile.mkstemp(suffix=".png", prefix="browser_")
            os.close(fd)
            await self._tab.save_screenshot(filename=path, format="png", full_page=False)
            return path
        except Exception:
            return None

    @staticmethod
    def _display_screenshot_path(path: str | None, *, remove_after: bool = True) -> None:
        if not path:
            return
        try:
            data = Path(path).read_bytes()
            display(Image(data=data))
        except Exception:
            pass
        finally:
            if remove_after:
                try:
                    os.unlink(path)
                except OSError:
                    pass

    def _get_target(self, element_index: int):
        if element_index < 0 or element_index >= len(self._last_raw_elements):
            raise IndexError(
                f"element_index={element_index} 超出范围，"
                f"当前缓存共 {len(self._last_raw_elements)} 个可交互元素。"
                f"请先调用 navigate() 或 get_interactive_elements() 刷新列表。"
            )
        return self._last_raw_elements[element_index]

    # ── 公开 API ──────────────────────────────

    async def _async_navigate(self, url: str, wait_for: str | None) -> tuple[str, str | None]:
        try:
            self._tab = await self._browser.get(url)
            await self._wait_dom_content_loaded(timeout=10)
            if wait_for:
                await self._tab.wait_for(selector=wait_for, timeout=15)
            report = await self._snapshot(f"[navigate] 成功 → {url}")
        except Exception as e:
            report = f"[navigate] 失败 → {url}\n  Error: {e}"
        shot = await self._write_temp_screenshot()
        return report, shot

    def _ensure_connected(self) -> None:
        cdp_endpoint = _request_browser()
        if not cdp_endpoint:
            _request_browser_failed()
        self._async_run(self._async_do_start(cdp_endpoint))

    def navigate(self, url: str, wait_for: str | None = None) -> str:
        self._ensure_connected()
        report, shot_path = self._async_run(self._async_navigate(url, wait_for))
        self._display_screenshot_path(shot_path)
        return report

    async def _async_click(self, element_index: int) -> tuple[str, str | None]:
        try:
            target = self._get_target(element_index)
            await target.scroll_into_view()
            await asyncio.sleep(0.3)
            tab_ids_before = self._page_tab_target_ids()
            await target.click()
            await asyncio.sleep(1.5)
            await self._async_adopt_new_tab_if_opened(tab_ids_before)
            await self._tab
            report = await self._snapshot(f"[click] 成功 → index={element_index}")
        except Exception as e:
            report = f"[click] 失败 → index={element_index}\n  Error: {e}"
        return report, await self._write_temp_screenshot()

    def click(self, element_index: int) -> str:
        report, shot_path = self._async_run(self._async_click(element_index))
        self._display_screenshot_path(shot_path)
        return report

    async def _async_fill(self, element_index: int, text: str, press_enter: bool) -> tuple[str, str | None]:
        try:
            tab_ids_before = self._page_tab_target_ids()
            target = self._get_target(element_index)
            await target.scroll_into_view()
            await asyncio.sleep(0.2)
            await target.click()
            await asyncio.sleep(0.5)
            await target.clear_input()
            await target.send_keys(text)
            if press_enter:
                await asyncio.sleep(0.2)
                await target.send_keys("\r")
                await asyncio.sleep(1.5)
            else:
                await asyncio.sleep(0.8)
            await self._async_adopt_new_tab_if_opened(tab_ids_before)
            await self._tab
            report = await self._snapshot(
                f"[fill] 成功 → index={element_index}, text='{text}', press_enter={press_enter}"
            )
        except Exception as e:
            report = f"[fill] 失败 → index={element_index}\n  Error: {e}"
        return report, await self._write_temp_screenshot()

    def fill(self, element_index: int, text: str, press_enter: bool = False) -> str:
        report, shot_path = self._async_run(self._async_fill(element_index, text, press_enter))
        self._display_screenshot_path(shot_path)
        return report

    async def _async_select_option(
        self,
        element_index: int,
        option_text: str | None,
        option_value: str | None,
        option_index: int | None,
    ) -> tuple[str, str | None]:
        if option_text is None and option_value is None and option_index is None:
            raise ValueError("必须提供 option_text、option_value 或 option_index 之一。")
        target = self._get_target(element_index)
        try:
            tab_ids_before = self._page_tab_target_ids()
            await target.scroll_into_view()
            await asyncio.sleep(0.2)
            label_j = json.dumps(option_text)
            val_j = json.dumps(option_value)
            idx_j = json.dumps(option_index)
            ok = await target.apply(
                f"""(sel) => {{
  const opts = Array.from(sel.options);
  let idx = -1;
  const label = {label_j};
  const val = {val_j};
  const i = {idx_j};
  if (label !== null) {{
    idx = opts.findIndex(o => (o.text || '').trim() === label);
  }} else if (val !== null) {{
    idx = opts.findIndex(o => o.value === val);
  }} else if (i !== null && i !== undefined) {{
    idx = i;
  }}
  if (idx < 0 || idx >= opts.length) return false;
  sel.selectedIndex = idx;
  sel.dispatchEvent(new Event('input', {{ bubbles: true }}));
  sel.dispatchEvent(new Event('change', {{ bubbles: true }}));
  return true;
}}""",
                return_by_value=True,
            )
            if not ok:
                raise RuntimeError("未找到匹配的 option 或索引无效")
            await asyncio.sleep(0.8)
            await self._async_adopt_new_tab_if_opened(tab_ids_before)
            await self._tab
            chosen = option_text or option_value or str(option_index)
            report = await self._snapshot(f"[select_option] 成功 → index={element_index}, option='{chosen}'")
        except Exception as e:
            report = f"[select_option] 失败 → index={element_index}\n  Error: {e}"
        return report, await self._write_temp_screenshot()

    def select_option(
        self,
        element_index: int,
        option_text: str | None = None,
        option_value: str | None = None,
        option_index: int | None = None,
    ) -> str:
        report, shot_path = self._async_run(
            self._async_select_option(element_index, option_text, option_value, option_index)
        )
        self._display_screenshot_path(shot_path)
        return report

    def get_interactive_elements(self) -> str:
        return self._async_run(self._snapshot("[get_interactive_elements] 已刷新元素列表"))

    @staticmethod
    def _prepare_evaluate_script(script: str) -> str:
        return f"(function() {{\n{script}\n}})()"

    async def _async_execute_script(self, script: str) -> str:
        try:
            js = self._prepare_evaluate_script(script)
            result = await self._tab.evaluate(js, return_by_value=True)
            err = Browser._eval_error_payload(result)
            if err:
                raise RuntimeError(err)
            result_str = "" if result is None else str(result)
            return await self._snapshot(f"[execute_script] 成功\n  Result: {result_str}")
        except Exception as e:
            return f"[execute_script] 失败\n  Error: {e}"

    def execute_script(self, script: str) -> str:
        return self._async_run(self._async_execute_script(script))

    async def _async_screenshot(self, output: str, full_page: bool) -> tuple[str, str | None]:
        try:
            output_path = str(Path(output).resolve())
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            await self._tab.save_screenshot(filename=output_path, format="png", full_page=full_page)
            report = await self._snapshot(f"[screenshot] 已保存 → {output_path}")
            return report, output_path
        except Exception as e:
            return f"[screenshot] 失败\n  Error: {e}", None

    def screenshot(self, output: str = "screenshot.png", full_page: bool = False) -> str:
        report, shot_path = self._async_run(self._async_screenshot(output, full_page))
        self._display_screenshot_path(shot_path, remove_after=False)
        return report


# ── 模块级 API ───────────────────────────────────────────────


def _singleton() -> Browser:
    return Browser()


def navigate(url: str, wait_for: str | None = None) -> str:
    with _NAVIGATE_SWAP_LOCK:
        Browser._clear_singleton_and_teardown_old()
        return Browser().navigate(url, wait_for=wait_for)


def click(element_index: int) -> str:
    return _singleton().click(element_index)


def fill(element_index: int, text: str, press_enter: bool = False) -> str:
    return _singleton().fill(element_index, text, press_enter=press_enter)


def select_option(
    element_index: int,
    option_text: str | None = None,
    option_value: str | None = None,
    option_index: int | None = None,
) -> str:
    return _singleton().select_option(
        element_index,
        option_text=option_text,
        option_value=option_value,
        option_index=option_index,
    )


def get_interactive_elements() -> str:
    return _singleton().get_interactive_elements()


def execute_script(script: str) -> str:
    return _singleton().execute_script(script)


def screenshot(output: str = "screenshot.png", full_page: bool = False) -> str:
    return _singleton().screenshot(output=output, full_page=full_page)


__all__ = [
    "Browser",
    "navigate",
    "click",
    "fill",
    "select_option",
    "get_interactive_elements",
    "execute_script",
    "screenshot",
]
