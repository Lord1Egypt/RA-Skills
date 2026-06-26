# -*- coding: utf-8 -*-
"""
CDP (Chrome DevTools Protocol) 客户端封装
支持 Edge/Chrome 的 DevTools WebSocket 连接
"""
import json
import time
import asyncio
import websockets
import subprocess
from typing import Optional, Dict, Any


class CdpClient:
    """
    CDP WebSocket 客户端
    
    使用方式:
        cdp = CdpClient()
        cdp.connect("E7C2FA5DB0FB60DDD01D97EFAB45BCD8")
        cdp.execute(tab_id, "document.title")
        cdp.disconnect()
    """
    
    def __init__(self):
        self.ws: Optional[websockets.client.WebSocketClientProtocol] = None
        self.tab_id: Optional[str] = None
        self._msg_id = 0
        self._pending: Dict[int, asyncio.Future] = {}
    
    def connect(self, tab_id: str, host: str = "127.0.0.1", port: int = 9222) -> bool:
        """
        连接到指定 Tab 的 DevTools WebSocket
        """
        try:
            # 获取正确的 WebSocket URL
            ws_url = self._get_ws_url(tab_id, host, port)
            if not ws_url:
                print(f"无法获取 Tab {tab_id} 的 WebSocket URL，尝试直接连接...")
                ws_url = f"ws://{host}:{port}/devtools/page/{tab_id}"
            
            self.ws = asyncio.get_event_loop().run_until_complete(
                websockets.connect(ws_url, ping_interval=None)
            )
            self.tab_id = tab_id
            print(f"WebSocket 连接成功: {ws_url}")
            return True
        except Exception as e:
            print(f"WebSocket 连接失败: {e}")
            return False
    
    def _get_ws_url(self, tab_id: str, host: str = "127.0.0.1", port: int = 9222) -> Optional[str]:
        """通过 JSON API 获取 Tab 的 WebSocket URL"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', f'(Invoke-RestMethod http://{host}:{port}/json).webSocketDebuggerUrl'],
                capture_output=True, text=True, timeout=5
            )
            urls = result.stdout.strip().split('\n')
            for url in urls:
                if tab_id in url:
                    return url
            # 返回第一个可用 URL
            if urls:
                return urls[0]
            return None
        except Exception:
            return None
    
    async def _async_send(self, method: str, params: Optional[dict] = None) -> Any:
        """异步发送 CDP 命令"""
        if not self.ws:
            raise RuntimeError("Not connected. Call connect() first.")
        
        self._msg_id += 1
        msg = {"id": self._msg_id, "method": method}
        if params:
            msg["params"] = params
        
        future = asyncio.get_event_loop().create_future()
        self._pending[self._msg_id] = future
        
        await self.ws.send(json.dumps(msg))
        
        try:
            response = await asyncio.wait_for(future, timeout=30)
            return response.get("result")
        except asyncio.TimeoutError:
            del self._pending[self._msg_id]
            raise TimeoutError(f"CDP command '{method}' timed out")
    
    def _recv_sync(self) -> Optional[dict]:
        """同步接收消息（用于简单场景）"""
        if not self.ws:
            return None
        try:
            import socket
            # 注意：websockets 不支持同步 recv，这里只是占位
            # 实际使用中请用异步方法
            return None
        except Exception:
            return None
    
    def execute(self, tab_id: str, script: str, timeout: int = 30) -> Any:
        """
        在指定 Tab 执行 JavaScript 代码
        """
        async def _exec():
            result = await self._async_send("Runtime.evaluate", {
                "expression": script,
                "returnByValue": True,
                "awaitPromise": True,
                "timeout": timeout * 1000
            })
            return result
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(_exec())
    
    def click_js(self, tab_id: str, selector: str, text_contains: Optional[str] = None) -> Any:
        """
        用 JS 点击元素（比 click_by_ref 更可靠）
        
        Args:
            tab_id: Tab ID
            selector: CSS 选择器，如 'button'
            text_contains: 可选，匹配按钮文字
        """
        if text_contains:
            script = f"""
            (function() {{
                const els = Array.from(document.querySelectorAll('{selector}'));
                const target = els.find(el => el.innerText.includes('{text_contains}'));
                if (target) {{
                    target.click();
                    return 'OK:' + target.innerText.trim();
                }} else {{
                    return 'NOT_FOUND: ' + els.map(e => e.innerText.trim()).join('|');
                }}
            }})();
            """
        else:
            script = f"""
            (function() {{
                const el = document.querySelector('{selector}');
                if (el) {{ el.click(); return 'OK'; }}
                return 'NOT_FOUND';
            }})();
            """
        return self.execute(tab_id, script)
    
    def enable_target(self, tab_id: str) -> Any:
        """启用 Target 相关域"""
        return self.execute(tab_id, "// enable Target domain")
    
    def disconnect(self):
        """关闭 WebSocket 连接"""
        if self.ws:
            try:
                asyncio.get_event_loop().run_until_complete(self.ws.close())
            except Exception:
                pass
            self.ws = None
            self.tab_id = None


def get_doubao_tab_id(host: str = "127.0.0.1", port: int = 9222) -> Optional[str]:
    """
    自动发现豆包PC版的 Tab ID
    
    策略：查找标题包含"豆包"或 URL 包含"doubao"的 Tab
    """
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Invoke-RestMethod http://127.0.0.1:9222/json -TimeoutSec 3 | ConvertTo-Json -Depth 3'],
            capture_output=True, text=True, timeout=10
        )
        tabs = json.loads(result.stdout)
        if not isinstance(tabs, list):
            tabs = [tabs]
        
        for tab in tabs:
            title = tab.get("title", "")
            url = tab.get("url", "")
            tab_id = tab.get("id", "")
            print(f"Tab: [{tab_id}] {title} - {url[:60]}")
            
            if "doubao" in url.lower() or "豆包" in title:
                print(f">>> 找到豆包 Tab: {tab_id}")
                return tab_id
        
        # 返回第一个可用的 Tab
        if tabs:
            first_id = tabs[0].get("id")
            print(f"未找到豆包 Tab，使用第一个: {first_id}")
            return first_id
        return None
    except Exception as e:
        print(f"获取 Tab 列表失败: {e}")
        return None


if __name__ == "__main__":
    # 测试：列出所有可用 Tab
    print("=== 可用浏览器 Tab ===")
    tab_id = get_doubao_tab_id()
    if tab_id:
        print(f"\n推荐使用 Tab: {tab_id}")
    else:
        print("未找到任何 Tab，请确认浏览器已开启 DevTools (--remote-debugging-port=9222)")
