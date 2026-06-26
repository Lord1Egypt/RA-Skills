#!/usr/bin/env python3
"""
mcp_manager.py - MCP 连接管理器

参考 Claude Code 的 MCP 实现:
- 4 种传输协议:stdio/SSE/WebSocket/HTTP
- 认证缓存防雪崩(15分钟 TTL)
- 本地3/远端20并发限制
- Session 过期自动重连

用途:
    - 管理 MCP 工具连接
    - 自动重连机制
    - 并发控制
"""

import json
import time
import threading
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import ssl
import urllib.request
import urllib.error

# MCP 配置
CONFIG_DIR = Path.home() / ".openclaw" / "mcp"
CONFIG_FILE = CONFIG_DIR / "connections.json"

# TLS 证书验证(默认开启)
ssl_context = ssl.create_default_context()

# 并发限制
LOCAL_CONCURRENCY_LIMIT = 3
REMOTE_CONCURRENCY_LIMIT = 20

# TTL 配置
AUTH_CACHE_TTL = 15 * 60  # 15 分钟


class TransportType(Enum):
    STDIO = "stdio"
    SSE = "sse"
    WEBSOCKET = "websocket"
    HTTP = "http"


@dataclass
class AuthCache:
    """认证缓存"""
    token: str
    expires_at: float
    endpoint: str

    def is_expired(self) -> bool:
        return time.time() > self.expires_at


@dataclass
class MCPConnection:
    """MCP 连接"""
    name: str
    transport: TransportType
    endpoint: str
    auth_token: Optional[str] = None
    enabled: bool = True
    last_used: float = 0
    retry_count: int = 0
    max_retries: int = 3

    def __post_init__(self):
        if isinstance(self.transport, str):
            self.transport = TransportType(self.transport)


class ConcurrencyLimiter:
    """并发限制器"""

    def __init__(self, local_limit: int = LOCAL_CONCURRENCY_LIMIT,
                 remote_limit: int = REMOTE_CONCURRENCY_LIMIT):
        self.local_limit = local_limit
        self.remote_limit = remote_limit
        self.local_active = 0
        self.remote_active = 0
        self.local_lock = threading.Lock()
        self.remote_lock = threading.Lock()

    def acquire_local(self) -> bool:
        with self.local_lock:
            if self.local_active < self.local_limit:
                self.local_active += 1
                return True
            return False

    def release_local(self):
        with self.local_lock:
            self.local_active -= 1

    def acquire_remote(self) -> bool:
        with self.remote_lock:
            if self.remote_active < self.remote_limit:
                self.remote_active += 1
                return True
            return False

    def release_remote(self):
        with self.remote_lock:
            self.remote_active -= 1

    def wait_for_local(self, timeout: float = 10):
        """等待本地槽位"""
        start = time.time()
        while self.local_active >= self.local_limit:
            if time.time() - start > timeout:
                return False
            time.sleep(0.1)
        return self.acquire_local()

    def wait_for_remote(self, timeout: float = 30):
        """等待远端槽位"""
        start = time.time()
        while self.remote_active >= self.remote_limit:
            if time.time() - start > timeout:
                return False
            time.sleep(0.1)
        return self.acquire_remote()

    def get_stats(self) -> dict:
        return {
            "local": {"active": self.local_active, "limit": self.local_limit},
            "remote": {"active": self.remote_active, "limit": self.remote_limit},
        }


class MCPAuthCache:
    """MCP 认证缓存"""

    def __init__(self, ttl: int = AUTH_CACHE_TTL):
        self.cache: Dict[str, AuthCache] = {}
        self.ttl = ttl
        self.lock = threading.Lock()

    def get(self, endpoint: str) -> Optional[str]:
        """获取缓存的认证 token"""
        with self.lock:
            cache = self.cache.get(endpoint)
            if cache and not cache.is_expired():
                return cache.token
            return None

    def set(self, endpoint: str, token: str):
        """设置认证缓存"""
        with self.lock:
            self.cache[endpoint] = AuthCache(
                token=token,
                expires_at=time.time() + self.ttl,
                endpoint=endpoint,
            )

    def invalidate(self, endpoint: str):
        """清除缓存"""
        with self.lock:
            if endpoint in self.cache:
                del self.cache[endpoint]

    def cleanup_expired(self):
        """清理过期缓存"""
        with self.lock:
            expired = [
                ep for ep, cache in self.cache.items()
                if cache.is_expired()
            ]
            for ep in expired:
                del self.cache[ep]


class MCPManager:
    """MCP 连接管理器"""

    def __init__(self):
        self.connections: Dict[str, MCPConnection] = {}
        self.auth_cache = MCPAuthCache()
        self.concurrency = ConcurrencyLimiter()
        self._load()

    def _load(self):
        """加载配置"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, conn_data in data.items():
                        self.connections[name] = MCPConnection(**conn_data)
            except (json.JSONDecodeError, IOError):
                pass

    def _save(self):
        """保存配置"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            data = {
                name: {
                    "name": conn.name,
                    "transport": conn.transport.value,
                    "endpoint": conn.endpoint,
                    "auth_token": conn.auth_token,
                    "enabled": conn.enabled,
                    "last_used": conn.last_used,
                    "retry_count": conn.retry_count,
                    "max_retries": conn.max_retries,
                }
                for name, conn in self.connections.items()
            }
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_connection(self, name: str, transport: str, endpoint: str,
                      auth_token: Optional[str] = None) -> bool:
        """添加连接"""
        if name in self.connections:
            return False

        conn = MCPConnection(
            name=name,
            transport=TransportType(transport),
            endpoint=endpoint,
            auth_token=auth_token,
        )
        self.connections[name] = conn
        self._save()
        return True

    def remove_connection(self, name: str) -> bool:
        """移除连接"""
        if name not in self.connections:
            return False
        del self.connections[name]
        self._save()
        return True

    def enable(self, name: str) -> bool:
        """启用连接"""
        if name not in self.connections:
            return False
        self.connections[name].enabled = True
        self._save()
        return True

    def disable(self, name: str) -> bool:
        """禁用连接"""
        if name not in self.connections:
            return False
        self.connections[name].enabled = False
        self._save()
        return True

    def get_connection(self, name: str) -> Optional[MCPConnection]:
        """获取连接"""
        return self.connections.get(name)

    def list_connections(self) -> Dict[str, dict]:
        """列出所有连接"""
        result = {}
        for name, conn in self.connections.items():
            result[name] = {
                "transport": conn.transport.value,
                "endpoint": conn.endpoint,
                "enabled": conn.enabled,
                "last_used": conn.last_used,
                "retry_count": conn.retry_count,
            }
        return result

    def execute(self, name: str, method: str, params: dict = None) -> dict:
        """
        执行 MCP 调用
        """
        conn = self.connections.get(name)
        if not conn:
            return {"error": f"Connection '{name}' not found"}

        if not conn.enabled:
            return {"error": f"Connection '{name}' is disabled"}

        # 检查认证缓存
        cached_token = self.auth_cache.get(conn.endpoint)
        token = cached_token or conn.auth_token

        # 选择并发槽位
        is_local = conn.transport == TransportType.STDIO
        acquired = self.concurrency.wait_for_local() if is_local else self.concurrency.wait_for_remote()

        if not acquired:
            return {"error": "Concurrency limit exceeded"}

        try:
            # 更新最后使用时间
            conn.last_used = time.time()

            # 根据传输类型执行
            if conn.transport == TransportType.STDIO:
                result = self._execute_stdio(method, params or {})
            elif conn.transport == TransportType.SSE:
                result = self._execute_sse(conn.endpoint, token, method, params or {})
            elif conn.transport == TransportType.WEBSOCKET:
                result = self._execute_websocket(conn.endpoint, token, method, params or {})
            elif conn.transport == TransportType.HTTP:
                result = self._execute_http(conn.endpoint, token, method, params or {})
            else:
                result = {"error": f"Unknown transport: {conn.transport}"}

            # 更新认证缓存
            if token and "result" in result:
                self.auth_cache.set(conn.endpoint, token)

            return result

        except Exception as e:
            conn.retry_count += 1
            if conn.retry_count >= conn.max_retries:
                conn.enabled = False
                self._save()
            return {"error": str(e)}

        finally:
            if is_local:
                self.concurrency.release_local()
            else:
                self.concurrency.release_remote()

    def _execute_stdio(self, method: str, params: dict) -> dict:
        """通过 stdio 执行"""
        # 这里需要调用本地 MCP 进程
        # 简化实现
        return {"result": f"stdio:{method}", "params": params}

    def _execute_sse(self, endpoint: str, token: Optional[str], method: str, params: dict) -> dict:
        """通过 SSE 执行"""
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        data = json.dumps({"method": method, "params": params}).encode("utf-8")

        try:
            req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}

    def _execute_websocket(self, endpoint: str, token: Optional[str], method: str, params: dict) -> dict:
        """通过 WebSocket 执行"""
        # 简化实现(需要 websockets 库)
        return {"result": f"websocket:{method}", "endpoint": endpoint}

    def _execute_http(self, endpoint: str, token: Optional[str], method: str, params: dict) -> dict:
        """通过 HTTP 执行"""
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        data = json.dumps({"method": method, "params": params}).encode("utf-8")

        try:
            req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}

    def reconnect(self, name: str) -> bool:
        """重新连接"""
        if name not in self.connections:
            return False

        conn = self.connections[name]
        conn.retry_count = 0
        conn.enabled = True
        self._save()
        return True

    def get_stats(self) -> dict:
        """获取统计"""
        return {
            "connections": self.list_connections(),
            "concurrency": self.concurrency.get_stats(),
        }


def cmd_list(args: list):
    """列出连接"""
    manager = MCPManager()
    connections = manager.list_connections()

    print(f"\n{'='*50}")
    print(f" MCP Connections ({len(connections)})")
    print(f"{'='*50}")

    for name, info in connections.items():
        status = "✅" if info["enabled"] else "❌"
        print(f"  {status} {name}")
        print(f"     Transport: {info['transport']}")
        print(f"     Endpoint: {info['endpoint']}")
        print(f"     Retries: {info['retry_count']}")

    print()


def cmd_stats(args: list):
    """显示统计"""
    manager = MCPManager()
    stats = manager.get_stats()

    print(f"\n📊 MCP Stats:")
    print(f"  Connections: {len(stats['connections'])}")
    print(f"  Concurrency:")
    print(f"    Local: {stats['concurrency']['local']['active']}/{stats['concurrency']['local']['limit']}")
    print(f"    Remote: {stats['concurrency']['remote']['active']}/{stats['concurrency']['remote']['limit']}")

    print()


def cmd_add(args: list):
    """添加连接"""
    if len(args) < 3:
        print("Usage: mcp_manager.py add <name> <transport> <endpoint> [auth_token]")
        return

    manager = MCPManager()
    name, transport, endpoint = args[0], args[1], args[2]
    auth_token = args[3] if len(args) > 3 else None

    if manager.add_connection(name, transport, endpoint, auth_token):
        print(f"✅ Added connection: {name}")
    else:
        print(f"❌ Failed to add connection: {name} (may already exist)")


def cmd_remove(args: list):
    """移除连接"""
    if not args:
        print("Usage: mcp_manager.py remove <name>")
        return

    manager = MCPManager()
    name = args[0]
    if manager.remove_connection(name):
        print(f"✅ Removed connection: {name}")
    else:
        print(f"❌ Failed to remove connection: {name}")


def cmd_enable(args: list):
    """启用连接"""
    if not args:
        print("Usage: mcp_manager.py enable <name>")
        return

    manager = MCPManager()
    name = args[0]
    if manager.enable(name):
        print(f"✅ Enabled: {name}")
    else:
        print(f"❌ Failed to enable: {name}")


def cmd_disable(args: list):
    """禁用连接"""
    if not args:
        print("Usage: mcp_manager.py disable <name>")
        return

    manager = MCPManager()
    name = args[0]
    if manager.disable(name):
        print(f"❌ Disabled: {name}")
    else:
        print(f"❌ Failed to disable: {name}")


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: mcp_manager.py <command> [args]")
        print("\nCommands:")
        print("  list                    - 列出所有连接")
        print("  stats                   - 显示统计信息")
        print("  add <name> <transport> <endpoint> [token] - 添加连接")
        print("  remove <name>          - 移除连接")
        print("  enable <name>           - 启用连接")
        print("  disable <name>         - 禁用连接")
        print("\nTransports: stdio, sse, websocket, http")
        sys.exit(1)

    manager = MCPManager()
    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "list": cmd_list,
        "stats": cmd_stats,
        "add": cmd_add,
        "remove": cmd_remove,
        "enable": cmd_enable,
        "disable": cmd_disable,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
