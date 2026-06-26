"""
浏览器引擎：SeleniumBase UC Mode + XHR 拦截
核心思路：注入 JS 拦截 fetch/XHR，捕获小红书真实 API 响应 JSON
不需要逆向签名算法，直接从浏览器内存中读取已签名的响应
"""
import json
import time
import os
from seleniumbase import SB


# 注入到页面的 JS 拦截器
_INTERCEPT_JS = """
(function() {
    if (window.__xhs_interceptor_installed) return;
    window.__xhs_interceptor_installed = true;
    window.__xhs_api_cache = {};

    // 拦截 fetch
    const _fetch = window.fetch;
    window.fetch = async function(...args) {
        const url = typeof args[0] === 'string' ? args[0] : args[0]?.url || '';
        const res = await _fetch.apply(this, args);
        if (url.includes('/api/sns/') || url.includes('edith.xiaohongshu')) {
            try {
                const clone = res.clone();
                clone.json().then(data => {
                    window.__xhs_api_cache[url] = data;
                }).catch(() => {});
            } catch(e) {}
        }
        return res;
    };

    // 拦截 XHR
    const _open = XMLHttpRequest.prototype.open;
    const _send = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function(method, url) {
        this.__url = url;
        return _open.apply(this, arguments);
    };
    XMLHttpRequest.prototype.send = function() {
        this.addEventListener('load', function() {
            if (this.__url && (this.__url.includes('/api/sns/') || this.__url.includes('edith.xiaohongshu'))) {
                try {
                    window.__xhs_api_cache[this.__url] = JSON.parse(this.responseText);
                } catch(e) {}
            }
        });
        return _send.apply(this, arguments);
    };
})();
"""


class BrowserSession:
    def __init__(self, cookies_file: str, headless: bool = False):
        self.cookies_file = cookies_file
        self.headless = headless
        self._sb = None
        self._ctx = None

    def __enter__(self):
        self._ctx = SB(uc=True, headless2=self.headless)
        self._sb = self._ctx.__enter__()
        self._init()
        return self

    def __exit__(self, *args):
        if self._ctx:
            self._ctx.__exit__(*args)

    def _init(self):
        self._sb.uc_open_with_reconnect("https://www.xiaohongshu.com", 4)
        time.sleep(2)
        self._inject_cookies()
        # Register CDP script BEFORE refresh so it runs on reload
        self._register_cdp_interceptor()
        self._sb.refresh()
        time.sleep(2)
        self._sb.execute_script(_INTERCEPT_JS)

    def _inject_cookies(self):
        if not os.path.exists(self.cookies_file):
            raise FileNotFoundError(f"Cookie 文件不存在: {self.cookies_file}\n请先运行 xhs_login.py")
        with open(self.cookies_file, encoding="utf-8") as f:
            cookies = json.load(f)
        for c in cookies:
            c.pop("sameSite", None)
            c.pop("httpOnly", None)
            try:
                self._sb.driver.add_cookie(c)
            except Exception:
                pass

    def _register_cdp_interceptor(self):
        """注册 CDP onNewDocument 脚本，每次页面加载前执行（捕获 page-load API）"""
        try:
            self._sb.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": _INTERCEPT_JS
            })
        except Exception:
            pass

    def _install_interceptor(self):
        self._sb.execute_script(_INTERCEPT_JS)

    def navigate(self, url: str, wait: float = 3.0):
        """导航到页面：用 driver.get 保留 CDP 会话（使拦截器在 page-load 前运行）"""
        # Re-register in case CDP session was reset
        self._register_cdp_interceptor()
        # Use driver.get to keep CDP alive (interceptor runs before page JS)
        self._sb.driver.get(url)
        time.sleep(wait)
        # Also inject immediately for any late-arriving race conditions
        self._install_interceptor()

    def scroll_and_collect(self, times: int = 3, gap: float = 2.0):
        """滚动页面触发懒加载 API"""
        for _ in range(times):
            self._sb.execute_script("window.scrollBy(0, 1500)")
            time.sleep(gap)

    def get_api_cache(self) -> dict:
        """读取所有已拦截的 API 响应"""
        try:
            return self._sb.execute_script("return window.__xhs_api_cache || {}") or {}
        except Exception:
            return {}

    def clear_cache(self):
        self._sb.execute_script("window.__xhs_api_cache = {}")

    def get_page_source(self) -> str:
        return self._sb.get_page_source()

    def find_elements(self, selector: str):
        return self._sb.find_elements(selector)

    def execute_script(self, script: str):
        return self._sb.execute_script(script)

    @property
    def driver(self):
        return self._sb.driver
