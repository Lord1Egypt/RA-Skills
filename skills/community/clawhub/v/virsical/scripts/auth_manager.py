"""
Virsical 认证管理模块。

负责 OAuth2 认证流程，包括：
- 登录（本地/远程模式）
- Token 存储与刷新
- Token 有效性检查
- 登出
"""

import hashlib
import http.server
import json
import os
import secrets
import sys
import time
import urllib.parse
import webbrowser
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from .config import get_config, VirsicalConfig

# 文件路径常量（与 auth_manager.py 同目录下的 data/ 子目录）
_SCRIPTS_DIR = Path(__file__).resolve().parent
DATA_DIR = _SCRIPTS_DIR / "data"
TOKEN_FILE = DATA_DIR / "token.json"
LOGIN_RESULT_FILE = DATA_DIR / "login_result.json"
OAUTH_STATE_FILE = DATA_DIR / "oauth_state.json"

# OAuth 常量
REDIRECT_URI = "http://127.0.0.1:1455/callback"
CALLBACK_PORT = 1455
STATE_BYTE_LENGTH = 32
STATE_EXPIRY_MINUTES = 10
TOKEN_REFRESH_BUFFER_SECONDS = 600  # 提前 10 分钟刷新

# CST 时区
CST = timezone(timedelta(hours=8))


def _now_cst() -> datetime:
    """返回当前 CST 时间。"""
    return datetime.now(CST)


def _format_cst(dt: datetime) -> str:
    """格式化 CST 时间为字符串。"""
    return dt.strftime("%Y/%m/%d %H:%M:%S")


class TokenManager:
    """Token 管理器。

    负责 token 的加载、保存、刷新和有效性检查。
    """

    def __init__(self, config: VirsicalConfig):
        self.config = config
        self._token: Optional[dict] = None

    def load_token(self) -> Optional[dict]:
        """从文件加载 token。

        Returns:
            Token 字典，如果不存在返回 None
        """
        if not TOKEN_FILE.exists():
            return None
        try:
            data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
            self._token = data.get("virsical:default")
            return self._token
        except (json.JSONDecodeError, KeyError):
            return None

    def save_token(self, token_data: dict):
        """保存 token 到文件。

        Args:
            token_data: Token 数据字典
        """
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        existing = {}
        if TOKEN_FILE.exists():
            try:
                existing = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass

        # 如果存在旧 token，保留 loginTime 字段
        old = existing.get("virsical:default", {})
        if old.get("loginTime"):
            token_data["loginTime"] = old["loginTime"]

        existing["virsical:default"] = token_data
        TOKEN_FILE.write_text(
            json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        try:
            os.chmod(TOKEN_FILE, 0o600)
        except Exception:
            pass
        self._token = token_data

    def clear_token(self):
        """清除本地 token。"""
        if TOKEN_FILE.exists():
            data = {}
            try:
                data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
            data.pop("virsical:default", None)
            TOKEN_FILE.write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        self._token = None

    def get_access_token(self) -> Optional[str]:
        """获取当前有效的 access token。

        如果 token 即将过期，会自动尝试刷新。

        Returns:
            Access token 字符串，如果无效返回 None
        """
        token = self._token or self.load_token()
        if not token:
            return None

        access = token.get("access", "")
        expires = token.get("expires", 0)
        now_ts = time.time()

        # 如果即将过期（10分钟内），尝试刷新
        if expires and (expires - now_ts) < TOKEN_REFRESH_BUFFER_SECONDS:
            refreshed = self._refresh()
            if refreshed:
                return refreshed.get("access", access)

        return access

    def get_refresh_token(self) -> Optional[str]:
        """获取 refresh token。"""
        token = self._token or self.load_token()
        if not token:
            return None
        return token.get("refresh", "")

    def is_token_valid(self) -> bool:
        """检查 token 是否有效（未过期）。

        Returns:
            True 如果 token 存在且未过期
        """
        token = self._token or self.load_token()
        if not token:
            return False
        expires = token.get("expires", 0)
        return expires > time.time()

    def need_refresh(self) -> bool:
        """检查是否需要刷新 token（即将过期）。

        Returns:
            True 如果 token 在 10 分钟内过期
        """
        token = self._token or self.load_token()
        if not token:
            return False
        expires = token.get("expires", 0)
        return 0 < (expires - time.time()) < TOKEN_REFRESH_BUFFER_SECONDS

    def set_token(self, access: str, refresh: str, expires_in: int,
                  username: str = "", user_id: str = "", tenant_id: str = "",
                  realname: str = ""):
        """设置 token 数据。

        Args:
            access: Access token
            refresh: Refresh token
            expires_in: 过期时间（秒）
            username: 用户名
            user_id: 用户 ID
            tenant_id: 租户 ID
            realname: 用户真实姓名（用于生成默认会议标题）
        """
        now = _now_cst()
        token_data = {
            "access": access,
            "refresh": refresh,
            "expires": time.time() + expires_in,
            "username": username,
            "userId": user_id,
            "tenantId": tenant_id,
            "realname": realname,
            "loginTime": _format_cst(now),
            "refreshTime": _format_cst(now),
        }
        self.save_token(token_data)

    def _refresh(self) -> Optional[dict]:
        """尝试刷新 access token。

        Returns:
            刷新后的 token 数据，失败返回 None
        """
        refresh_token = self.get_refresh_token()
        if not refresh_token:
            return None

        try:
            credentials = "bG9naW4tYWdlbnQ6QWdlbnQjMjAyNg=="

            body = urllib.parse.urlencode({
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }).encode()

            req = Request(
                f"{self.config.base_url}/vsk/virsical-auth/oauth/token",
                data=body,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {credentials}",
                },
                method="POST",
            )

            with urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())

            access_token = result.get("access_token", "")
            new_refresh = result.get("refresh_token", "")
            expires_in = result.get("expires_in", 0)

            if access_token:
                token = self._token or {}
                token["access"] = access_token
                if new_refresh:
                    token["refresh"] = new_refresh
                token["expires"] = time.time() + expires_in
                token["refreshTime"] = _format_cst(_now_cst())
                self.save_token(token)

                self._log_result({
                    "action": "refresh",
                    "status": "success",
                    "refreshTime": _format_cst(_now_cst()),
                })
                return token
        except HTTPError as e:
            self._log_result({
                "action": "refresh",
                "status": "error",
                "message": f"Token 刷新失败 (HTTP {e.code})",
                "refreshTime": _format_cst(_now_cst()),
            })
        except URLError as e:
            self._log_result({
                "action": "refresh",
                "status": "error",
                "message": f"无法连接到 Virsical 服务: {e.reason}",
                "refreshTime": _format_cst(_now_cst()),
            })
        except TimeoutError:
            self._log_result({
                "action": "refresh",
                "status": "error",
                "message": "Token 刷新超时",
                "refreshTime": _format_cst(_now_cst()),
            })
        except Exception as e:
            self._log_result({
                "action": "refresh",
                "status": "error",
                "message": f"Token 刷新失败: {e}",
                "refreshTime": _format_cst(_now_cst()),
            })

        return None

    def check_token_server(self) -> dict:
        """通过服务器检查 token 有效性。

        Returns:
            {"valid": bool, "message": str, "username": str}
        """
        token = self._token or self.load_token()
        if not token:
            return {"valid": False, "message": "No token found", "username": ""}

        access = token.get("access", "")
        if not access:
            return {"valid": False, "message": "No valid", "username": ""}

        try:
            credentials = "bG9naW4tYWdlbnQ6QWdlbnQjMjAyNg=="

            body = urllib.parse.urlencode({"token": access}).encode()
            req = Request(
                f"{self.config.base_url}/vsk/virsical-auth/oauth/check_token",
                data=body,
                headers={
                    "Authorization": f"Basic {credentials}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                method="POST",
            )

            with urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())

            if result.get("active") or result.get("user_id"):
                username = result.get("username", result.get("user_id", ""))
                return {"valid": True, "message": "Token is valid", "username": username}
            else:
                return {"valid": False, "message": "Token is invalid", "username": ""}

        except HTTPError as e:
            return {"valid": False, "message": f"Server error: {e.code}", "username": ""}
        except Exception as e:
            return {"valid": False, "message": f"Check failed: {e}", "username": ""}

    def logout(self) -> bool:
        """登出：调用服务端登出接口并清除本地 token。

        Returns:
            是否成功
        """
        token = self._token or self.load_token()
        if not token:
            return True

        access = token.get("access", "")
        try:
            data = json.dumps({"access_token": access}).encode()
            req = Request(
                f"{self.config.base_url}/vsk/virsical-auth/token/logout",
                data=data,
                headers={
                    "Authorization": f"Bearer {access}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            urlopen(req, timeout=30)
        except Exception:
            pass  # 服务端登出失败不阻塞本地清除

        self.clear_token()
        self._log_result({
            "action": "logout",
            "status": "success",
            "logoutTime": _format_cst(_now_cst()),
        })
        return True

    def _log_result(self, record: dict):
        """记录登录/刷新/登出结果。"""
        LOGIN_RESULT_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {"records": []}
        if LOGIN_RESULT_FILE.exists():
            try:
                data = json.loads(LOGIN_RESULT_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        data.setdefault("records", []).append(record)
        LOGIN_RESULT_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def exchange_code_for_token(code: str, config: VirsicalConfig) -> dict:
    """使用授权码换取 token。

    Args:
        code: 授权码
        config: 配置对象

    Returns:
        Token 响应数据

    Raises:
        Exception: 分类后的中文错误信息
    """
    credentials = "bG9naW4tYWdlbnQ6QWdlbnQjMjAyNg=="

    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }).encode()

    DEFAULT_TIMEOUT = 30

    try:
        req = Request(
            f"{config.base_url}/vsk/virsical-auth/oauth/token",
            data=body,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {credentials}",
            },
            method="POST",
        )

        with urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            result = json.loads(resp.read().decode())

        if "error" in result:
            raise Exception(
                f"授权码换取 token 失败: {result.get('error_description', result.get('error', '未知错误'))}"
            )

        # 校验必要字段
        if not result.get("access_token") or not result.get("refresh_token"):
            raise Exception(f"Token 响应格式异常，缺少 access_token 或 refresh_token")

        return {
            "access_token": result.get("access_token", ""),
            "refresh_token": result.get("refresh_token", ""),
            "expires_in": result.get("expires_in", 0),
            "user_id": result.get("user_id", ""),
            "tenant_id": result.get("tenant_id", ""),
            "username": result.get("username", ""),
        }
    except HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode()[:200]
        except Exception:
            pass
        raise Exception(
            f"授权码换取 token 失败 (HTTP {e.code}): {body_text}"
        )
    except URLError as e:
        raise Exception(
            f"无法连接到 Virsical 服务 ({config.base_url}): {e.reason}。"
            f"请检查网络连接和服务地址。"
        )
    except json.JSONDecodeError:
        raise Exception("Virsical 服务返回了无效的响应格式，请稍后重试")
    except TimeoutError:
        raise Exception(
            f"授权码换取 token 超时 ({DEFAULT_TIMEOUT}秒): Virsical 服务响应超时，请稍后重试"
        )


# ── Agent 授权码认证 ─────────────────────────────────────────────

# Agent 认证接口路径
AGENT_CREATE_AUTH_CODE_PATH = "/vsk/virsical-auth/agent/createAgentAuthCode"
AGENT_GET_TOKEN_PATH = "/vsk/virsical-auth/agent/getAgentToken"

# 错误码含义
AGENT_ERROR_CODES = {
    "101100": "Agent 授权码不存在或已过期，请重新登录威思客系统并获取新的授权码。",
}


def create_agent_auth_code(config: VirsicalConfig) -> dict:
    """调用服务端接口生成 agent 授权码（authCode），供 WorkBuddy Skill 换取 token。

    该接口需要 agent_auth_token（在 virsical.env 中配置为 VIRSICAL_AGENT_AUTH_TOKEN）。
    返回的 data 字段即为 32 位 authCode。

    Args:
        config: 配置对象

    Returns:
        {"success": bool, "auth_code": str, "message": str}
    """
    if not config.agent_auth_token:
        return {
            "success": False,
            "auth_code": "",
            "message": "Agent 授权令牌未配置。请先在 virsical.env 中设置 VIRSICAL_AGENT_AUTH_TOKEN。",
        }

    url = f"{config.agent_auth_base_url}{AGENT_CREATE_AUTH_CODE_PATH}"
    headers = {
        "Authorization": f"bearer {config.agent_auth_token}",
        "Content-Type": "application/json",
    }

    try:
        req = Request(url, data=b"{}", headers=headers, method="POST")
        with urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())

        code = result.get("code", -1)
        if code == 0:
            auth_code = result.get("data", "")
            if auth_code:
                return {
                    "success": True,
                    "auth_code": auth_code,
                    "message": f"Agent 授权码已生成: {auth_code}",
                }
            return {
                "success": False,
                "auth_code": "",
                "message": "获取授权码成功但返回数据为空，请重试。",
            }

        msg = result.get("msg", str(code))
        return {
            "success": False,
            "auth_code": "",
            "message": f"获取 Agent 授权码失败 (code={code}): {msg}",
        }
    except HTTPError as e:
        try:
            body = json.loads(e.read().decode())
            err_code = str(body.get("code", ""))
            msg = AGENT_ERROR_CODES.get(err_code, body.get("msg", e.reason))
        except Exception:
            msg = str(e.reason)
        return {
            "success": False,
            "auth_code": "",
            "message": f"获取 Agent 授权码失败 (HTTP {e.code}): {msg}",
        }
    except URLError as e:
        return {
            "success": False,
            "auth_code": "",
            "message": f"无法连接到 Agent 认证服务 ({config.agent_auth_base_url}): {e.reason}。请检查网络连接。",
        }
    except Exception as e:
        return {
            "success": False,
            "auth_code": "",
            "message": f"获取 Agent 授权码异常: {e}",
        }


def exchange_agent_code_for_token(
    auth_code: str, config: VirsicalConfig, token_manager: TokenManager
) -> dict:
    """使用用户粘贴的 Agent 授权码换取 token，并保存到本地。

    Args:
        auth_code: 用户从威思客系统复制粘贴的授权码
        config: 配置对象
        token_manager: Token 管理器（用于保存 token）

    Returns:
        {"success": bool, "message": str, "username": str}
    """
    auth_code = (auth_code or "").strip()
    if not auth_code:
        return {"success": False, "message": "授权码不能为空。", "username": ""}

    url = f"{config.agent_auth_base_url}{AGENT_GET_TOKEN_PATH}"
    form_data = urllib.parse.urlencode({"authCode": auth_code}).encode()

    try:
        req = Request(
            url,
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())

        code = result.get("code", -1)
        if code != 0:
            err_code_str = str(code)
            msg = result.get("msg", f"错误码: {code}")
            msg = AGENT_ERROR_CODES.get(err_code_str, msg)
            return {"success": False, "message": msg, "username": ""}

        data = result.get("data", {})
        access_token = data.get("access_token", "")
        refresh_token = data.get("refresh_token", "")
        expires_in = int(data.get("expires_in", 0) or 0)
        username = data.get("username", "")
        user_id = str(data.get("user_id", ""))
        tenant_id = str(data.get("tenant_id", ""))
        realname = data.get("realname", "")

        if not access_token:
            return {
                "success": False,
                "message": "Token 换取成功但返回数据缺少 access_token。",
                "username": "",
            }

        token_manager.set_token(
            access=access_token,
            refresh=refresh_token,
            expires_in=expires_in,
            username=username,
            user_id=user_id,
            tenant_id=tenant_id,
            realname=realname,
        )

        token_manager._log_result({
            "action": "agent_login",
            "status": "success",
            "username": username,
            "loginTime": _format_cst(_now_cst()),
            "expires": _format_cst(_now_cst() + timedelta(seconds=expires_in)),
        })

        return {
            "success": True,
            "message": f"登录成功！欢迎，{username or 'Virsical 用户'}。",
            "username": username,
        }
    except HTTPError as e:
        try:
            body = json.loads(e.read().decode())
            err_code = str(body.get("code", ""))
            msg = AGENT_ERROR_CODES.get(err_code, body.get("msg", e.reason))
        except Exception:
            msg = str(e.reason)
        return {
            "success": False,
            "message": f"Agent Token 换取失败 (HTTP {e.code}): {msg}",
            "username": "",
        }
    except URLError as e:
        return {
            "success": False,
            "message": f"无法连接到 Agent 认证服务 ({config.agent_auth_base_url}): {e.reason}。请检查网络连接。",
            "username": "",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Agent Token 换取异常: {e}",
            "username": "",
        }


def build_authorize_url(config: VirsicalConfig, state: str) -> str:
    """构建 OAuth 授权 URL。

    Args:
        config: 配置对象
        state: CSRF 状态值

    Returns:
        完整的授权 URL
    """
    params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": "login-agent",
        "scope": "server",
        "redirect_uri": REDIRECT_URI,
        "state": state,
    })
    return f"{config.base_url}/vsk/virsical-auth/oauth2/authorize?{params}"


def generate_state() -> str:
    """生成随机 state 值用于 CSRF 防护。

    Returns:
        32 字节随机十六进制字符串
    """
    return secrets.token_hex(STATE_BYTE_LENGTH)


def save_oauth_state(state: str):
    """保存 OAuth state 到文件（用于远程登录模式）。

    Args:
        state: CSRF 状态值
    """
    OAUTH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {"states": []}
    if OAUTH_STATE_FILE.exists():
        try:
            data = json.loads(OAUTH_STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    # 清理过期 state
    now = time.time()
    data["states"] = [
        s for s in data.get("states", [])
        if now - s.get("created_at", 0) < STATE_EXPIRY_MINUTES * 60
    ]

    data["states"].append({
        "value": state,
        "created_at": now,
    })

    OAUTH_STATE_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def validate_oauth_state(state: str) -> bool:
    """验证 OAuth state 是否有效。

    Args:
        state: 要验证的状态值

    Returns:
        True 如果 state 有效
    """
    if not OAUTH_STATE_FILE.exists():
        return False
    try:
        data = json.loads(OAUTH_STATE_FILE.read_text(encoding="utf-8"))
        now = time.time()
        for s in data.get("states", []):
            if s.get("value") == state:
                if now - s.get("created_at", 0) < STATE_EXPIRY_MINUTES * 60:
                    return True
        return False
    except json.JSONDecodeError:
        return False


def consume_oauth_state(state: str):
    """消费（删除）已使用的 OAuth state。

    Args:
        state: 已使用的状态值
    """
    if not OAUTH_STATE_FILE.exists():
        return
    try:
        data = json.loads(OAUTH_STATE_FILE.read_text(encoding="utf-8"))
        data["states"] = [
            s for s in data.get("states", [])
            if s.get("value") != state
        ]
        OAUTH_STATE_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except json.JSONDecodeError:
        pass


def validate_and_consume_state(state: str) -> bool:
    """验证并消费 OAuth state（用于远程登录模式防重放攻击）。

    一次性使用：验证通过后立即删除 state，防止同一 state 被重复使用。

    Args:
        state: 要验证的状态值

    Returns:
        True 如果 state 有效且消费成功
    """
    if validate_oauth_state(state):
        consume_oauth_state(state)
        return True
    return False


def check_token_before_login(token_manager) -> dict:
    """在登录前智能检查 token 状态。

    先本地检查，再通过服务端 check_token API 验证。

    Returns:
        {
            "should_login": bool,
            "message": str,
            "username": str,
            "token_valid": bool,
        }
    """
    token = token_manager.load_token()
    if not token:
        return {
            "should_login": True,
            "message": "尚未登录 Virsical，需要登录",
            "username": "",
            "token_valid": False,
        }

    access = token.get("access", "")
    if not access:
        return {
            "should_login": True,
            "message": "Token 数据不完整，需要重新登录",
            "username": token.get("username", ""),
            "token_valid": False,
        }

    # 如果本地判断未过期且距离过期 > 10 分钟，视为有效
    expires = token.get("expires", 0)
    if expires and (expires - time.time()) > TOKEN_REFRESH_BUFFER_SECONDS:
        return {
            "should_login": False,
            "message": f"已登录 Virsical，用户: {token.get('username', '未知')}",
            "username": token.get("username", ""),
            "token_valid": True,
        }

    # Token 即将过期或已过期，尝试通过服务端验证
    server_result = token_manager.check_token_server()
    if server_result.get("valid"):
        return {
            "should_login": False,
            "message": f"已登录 Virsical (服务端验证)，用户: {server_result.get('username', '未知')}",
            "username": server_result.get("username", ""),
            "token_valid": True,
        }

    return {
        "should_login": True,
        "message": f"Token 已失效，用户: {token.get('username', '未知')}，需要重新登录",
        "username": token.get("username", ""),
        "token_valid": False,
    }


def local_login(
    config: VirsicalConfig,
    token_manager: TokenManager,
    wait: bool = True,
    timeout_seconds: int = STATE_EXPIRY_MINUTES * 60,
) -> dict:
    """执行本地登录流程。

    启动本地 HTTP 回调服务器，尝试自动打开浏览器完成 OAuth 授权。
    默认同步等待回调完成（最多 10 分钟），确保 token 已写入后再返回。

    当 wait=False 时退化为非阻塞模式（仅启动服务并返回授权链接），
    仅用于需要自定义等待逻辑的场景。

    Args:
        config: 配置对象
        token_manager: Token 管理器
        wait: 是否阻塞等待登录完成，默认 True
        timeout_seconds: 等待超时秒数，默认 600（10 分钟）

    Returns:
        {
            "success": bool,
            "message": str,
            "username": str,
            "authorize_url": str,     # 仅非阻塞模式返回
            "mode": "local",
            "state": str,             # 仅非阻塞模式返回
        }
    """
    import threading

    state = generate_state()
    auth_url = build_authorize_url(config, state)

    result_container = {"done": False, "result": None, "server_error": None}

    class _ReuseHTTPServer(http.server.HTTPServer):
        """设置 SO_REUSEADDR 的 HTTPServer，避免端口 TIME_WAIT 导致的绑定失败。"""
        allow_reuse_address = True

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            if parsed.path != "/callback":
                self.send_error(404)
                return

            code = params.get("code", [None])[0]
            returned_state = params.get("state", [None])[0]

            if not code or returned_state != state:
                content = _error_html("授权验证失败：state 不匹配或缺少 code 参数")
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode())
                result_container["result"] = {
                    "success": False,
                    "message": "State 不匹配或缺少授权码",
                    "username": "",
                }
                result_container["done"] = True
                return

            try:
                token_data = exchange_code_for_token(code, config)
                token_manager.set_token(
                    access=token_data["access_token"],
                    refresh=token_data["refresh_token"],
                    expires_in=token_data["expires_in"],
                    username=token_data["username"],
                    user_id=token_data["user_id"],
                    tenant_id=token_data["tenant_id"],
                )

                expires_date = _format_cst(_now_cst() + timedelta(seconds=token_data["expires_in"]))
                token_manager._log_result({
                    "action": "login",
                    "status": "success",
                    "username": token_data["username"],
                    "loginTime": _format_cst(_now_cst()),
                    "expires": expires_date,
                })

                content = _success_html(token_data.get("username", "用户"))
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode())

                result_container["result"] = {
                    "success": True,
                    "message": "登录成功",
                    "username": token_data["username"],
                }
            except Exception as e:
                content = _error_html(f"授权失败：{e}")
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode())

                result_container["result"] = {
                    "success": False,
                    "message": str(e),
                    "username": "",
                }
            result_container["done"] = True

        def log_message(self, format, *args):
            pass  # 静默日志

    # 创建服务器（带 SO_REUSEADDR，避免 TIME_WAIT 端口占用）
    server = _ReuseHTTPServer(("127.0.0.1", CALLBACK_PORT), CallbackHandler)
    server.timeout = 1

    def _run_server():
        deadline = time.time() + STATE_EXPIRY_MINUTES * 60
        while not result_container["done"] and time.time() < deadline:
            try:
                server.handle_request()
            except Exception as e:
                result_container["server_error"] = str(e)
                break
        try:
            server.server_close()
        except Exception:
            pass
        if not result_container["done"] and not result_container["server_error"]:
            token_manager._log_result({
                "action": "login",
                "status": "timeout",
                "message": "等待授权超时",
                "loginTime": _format_cst(_now_cst()),
            })

    t = threading.Thread(target=_run_server, daemon=False)
    t.start()

    # 短暂延迟确保服务器完全就绪后再打开浏览器
    time.sleep(0.3)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    # 非阻塞模式：立即返回授权链接
    if not wait:
        return {
            "success": True,
            "message": "本地登录回调服务已启动，请在 10 分钟内完成授权",
            "authorize_url": auth_url,
            "mode": "local",
            "state": state,
        }

    # 阻塞等待回调完成
    t.join(timeout=timeout_seconds)

    # 服务器启动阶段就出错了
    if result_container.get("server_error"):
        server.server_close()
        return {
            "success": False,
            "message": f"登录服务启动失败: {result_container['server_error']}",
            "username": "",
            "mode": "local",
        }

    if result_container["result"]:
        return {
            **result_container["result"],
            "mode": "local",
        }

    # 超时
    server.server_close()
    return {
        "success": False,
        "message": "登录超时：未在 10 分钟内完成授权，请重试",
        "username": "",
        "mode": "local",
    }


def remote_login(config: VirsicalConfig) -> dict:
    """执行远程登录流程。

    生成授权 URL 和 state，保存 state 到文件，用户手动完成授权后
    需要调用 exchange_code 完成 token 交换。

    Args:
        config: 配置对象

    Returns:
        {"authorize_url": str, "state": str}
    """
    state = generate_state()
    save_oauth_state(state)
    auth_url = build_authorize_url(config, state)
    return {"authorize_url": auth_url, "state": state}


def exchange_code(code: str, state: str, config: VirsicalConfig,
                  token_manager: TokenManager) -> dict:
    """远程登录模式下的 code 交换。

    强制验证 state 参数防 CSRF 攻击，验证通过后立即消费（防重放）。

    Args:
        code: 授权码
        state: CSRF 状态值（必填）
        config: 配置对象
        token_manager: Token 管理器

    Returns:
        {"success": bool, "message": str, "username": str}
    """
    if not state:
        return {
            "success": False,
            "message": "缺少 state 参数，远程登录必须提供 state 以确保安全。请重新发起登录",
            "username": "",
        }

    if not validate_and_consume_state(state):
        return {
            "success": False,
            "message": "state 参数验证失败或已过期（10 分钟）。请重新发起登录",
            "username": "",
        }

    try:
        token_data = exchange_code_for_token(code, config)

        token_manager.set_token(
            access=token_data["access_token"],
            refresh=token_data["refresh_token"],
            expires_in=token_data["expires_in"],
            username=token_data["username"],
            user_id=token_data["user_id"],
            tenant_id=token_data["tenant_id"],
        )
        token_manager._log_result({
            "action": "login",
            "status": "success",
            "username": token_data["username"],
            "loginTime": _format_cst(_now_cst()),
            "expires": _format_cst(_now_cst() + timedelta(seconds=token_data["expires_in"])),
        })
        return {
            "success": True,
            "message": f"登录成功，用户: {token_data['username']}",
            "username": token_data["username"],
        }
    except Exception as e:
        return {"success": False, "message": str(e), "username": ""}


def _success_html(username: str) -> str:
    """生成登录成功 HTML 页面。"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录成功 - Virsical</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .card {{
            background: white; border-radius: 16px; padding: 48px;
            text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            max-width: 400px; width: 90%;
        }}
        .icon {{ font-size: 64px; margin-bottom: 16px; }}
        h1 {{ color: #333; font-size: 24px; margin-bottom: 12px; }}
        p {{ color: #666; font-size: 16px; margin-bottom: 8px; }}
        .username {{ color: #667eea; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">✅</div>
        <h1>登录成功</h1>
        <p>欢迎，<span class="username">{username}</span></p>
        <p>您可以关闭此页面了</p>
    </div>
</body>
</html>"""


def _error_html(message: str) -> str:
    """生成登录失败 HTML 页面。"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录失败 - Virsical</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        .card {{
            background: white; border-radius: 16px; padding: 48px;
            text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            max-width: 400px; width: 90%;
        }}
        .icon {{ font-size: 64px; margin-bottom: 16px; }}
        h1 {{ color: #333; font-size: 24px; margin-bottom: 12px; }}
        p {{ color: #666; font-size: 16px; }}
        .error {{ color: #f5576c; font-size: 14px; margin-top: 16px; word-break: break-all; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">❌</div>
        <h1>登录失败</h1>
        <p>授权过程中出现问题</p>
        <div class="error">{message}</div>
    </div>
</body>
</html>"""


if __name__ == "__main__":
    cfg = get_config()
    if not cfg.is_configured:
        print("Error: Virsical is not configured. Please set environment variables or create ~/.virsical/virsical.env")
        sys.exit(1)

    tm = TokenManager(cfg)

    if len(sys.argv) > 1 and sys.argv[1] == "check":
        result = tm.check_token_server()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "status":
        token = tm.load_token()
        if token:
            valid = tm.is_token_valid()
            print(f"Token valid: {valid}")
            print(f"Username: {token.get('username', 'N/A')}")
            print(f"Expires: {datetime.fromtimestamp(token.get('expires', 0), CST).isoformat()}")
        else:
            print("No token found")
    elif len(sys.argv) > 1 and sys.argv[1] == "login":
        result = local_login(cfg, tm)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "logout":
        tm.logout()
        print("Logged out successfully")
    else:
        print("Usage: python auth_manager.py [check|status|login|logout]")
