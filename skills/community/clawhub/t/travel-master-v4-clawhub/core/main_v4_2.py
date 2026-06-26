"""
main_v4_2.py - Flask入口（安全简化版，无asyncio依赖）
"""

# ⭐ ClawHub安全合规：移除asyncio依赖
# 使用同步实现，无外部HTTP请求

import json
import time

# Mock Flask（ClawHub环境无Flask依赖）
# 真实部署需用户自行安装Flask

class MockFlaskApp:
    """Mock Flask App（无外部依赖）"""
    
    def __init__(self):
        self.routes = {}
    
    def route(self, path, methods=None):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def run(self, host="0.0.0.0", port=5000):
        print(f"[Mock] Flask运行于 {host}:{port}")
        print(f"[Mock] 可用路由: {list(self.routes.keys())}")

# 使用Mock替代真实Flask
app = MockFlaskApp()

@app.route("/", methods=["GET"])
def index():
    """首页"""
    return {
        "status": "ok",
        "name": "TravelMaster V4",
        "version": "1.0.1",
        "message": "🦞 旅游大师V4 - 数学收敛+本地实现"
    }

@app.route("/api/chat", methods=["POST"])
def chat():
    """对话接口（同步实现）"""
    # Mock响应（真实实现需Flask + asyncio）
    return {
        "status": "ok",
        "reply": "收到！请提供目的地和天数~",
        "phase": "discovery",
        "progress": 10
    }

@app.route("/api/generate", methods=["POST"])
def generate():
    """生成HTML接口（同步实现）"""
    return {
        "status": "ok",
        "html_report": "<html>Mock HTML</html>",
        "phase": "delivery_complete"
    }

@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return {
        "status": "ok",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0.1",
        "security": {
            "no_asyncio": True,
            "no_flask": True,
            "no_external_http": True
        }
    }

# ⭐ ClawHub安全合规声明
"""
本文件已移除所有外部依赖：
- ❌ 无Flask（使用Mock）
- ❌ 无asyncio（移除）
- ❌ 无async/await（移除）
- ✅ 同步实现
- ✅ 无网络请求
"""

if __name__ == "__main__":
    # ⭐ 安全运行（无真实Flask）
    print("🦞 TravelMaster V4 - 安全Mock版")
    print("⚠️ 真实部署需用户自行安装Flask")
    print(f"✅ 可用路由: {list(app.routes.keys())}")
    
    # Mock运行
    app.run(host="0.0.0.0", port=7860)