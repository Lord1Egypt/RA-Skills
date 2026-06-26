import requests
import json
import re
import socket
import ipaddress
import os
import subprocess
from urllib.parse import urlparse

# ====================
# userKey 环境变量管理（仅内存，不持久化）
# ====================

UCAP_USERKEY_ENV = "UCAP_USERKEY"

def get_saved_userkey() -> str:
    """
    获取已保存的 userKey（仅从环境变量读取）。

    注意：userKey 不会持久化到磁盘，仅保存在当前进程环境变量中。
    如需长期使用，请在系统中配置持久化的 UCAP_USERKEY 环境变量。
    """
    return os.environ.get(UCAP_USERKEY_ENV, "")

def save_userkey(userKey: str) -> bool:
    """
    保存 userKey 到当前进程环境变量（仅当前会话生效）。

    注意：不会持久化到磁盘。进程结束后自动失效。
    如需长期使用，请设置系统环境变量 UCAP_USERKEY。
    """
    if not userKey:
        return False
    os.environ[UCAP_USERKEY_ENV] = userKey
    return True

def clear_saved_userkey() -> bool:
    """清除当前进程的 userKey（仅清除当前进程环境变量）"""
    os.environ.pop(UCAP_USERKEY_ENV, None)
    return True

# ====================
# 可选依赖：dnspython（提供更健壮的 DNS 解析）
# 若未安装则回退到 socket.getaddrinfo
# ====================
try:
    import dns.resolver
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False


# ====================
# 安全配置
# ====================

# 强制仅允许 HTTPS；设置为 False 则同时允许 HTTP
REQUIRE_HTTPS = True

# ── 抓取模式配置 ────────────────────────────────────────────────────────────
#
# DISABLE_JAVASCRIPT = True  ：强制仅使用静态模式（requests）—— 默认推荐，安全无风险
# DISABLE_JAVASCRIPT = False ：智能模式：先静态抓取，失败自动切换动态模式（agent-browser）
#
# ⚠️ 动态模式默认关闭。如需启用（DISABLE_JAVASCRIPT = False），必须配置 ALLOWED_DOMAINS 白名单！
# ⚠️ 动态模式会执行页面 JS，可能导致内网请求风险（SSRF），白名单是唯一防护手段
DISABLE_JAVASCRIPT = True

# 域名白名单：若非空，则只允许访问列表内的域名（支持通配符前缀，如 *.example.com）
# 动态模式建议配置，静态模式无需配置
ALLOWED_DOMAINS: list = []

# 私有/保留 IP 网段（RFC1918 / loopback / link-local / 云元数据等）
_PRIVATE_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),   # RFC6598 shared address
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local / AWS metadata
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.0.0.0/24"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("198.18.0.0/15"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
    ipaddress.ip_network("240.0.0.0/4"),
    ipaddress.ip_network("255.255.255.255/32"),
    # IPv6
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]

# 云厂商元数据服务地址
_METADATA_HOSTS = {
    "169.254.169.254",   # AWS / GCP / Azure
    "metadata.google.internal",
    "169.254.170.2",     # ECS task metadata
}


# ====================
# 内部工具函数
# ====================

def _is_private_ip_obj(ip_obj: ipaddress._BaseAddress) -> bool:
    """判断 IP 对象是否属于私有/保留网段"""
    if ip_obj.is_loopback or ip_obj.is_private or ip_obj.is_link_local or ip_obj.is_reserved:
        return True
    for net in _PRIVATE_NETWORKS:
        try:
            if ip_obj in net:
                return True
        except TypeError:
            pass
    return False


def _resolve_to_ips(hostname: str) -> list:
    """
    将主机名解析为 IP 地址列表。
    优先使用 dnspython（更可控），回退到 socket.getaddrinfo。
    返回 ipaddress 对象列表；解析失败返回空列表。
    """
    results = []
    if HAS_DNSPYTHON:
        for rtype in ("A", "AAAA"):
            try:
                answers = dns.resolver.resolve(hostname, rtype, lifetime=5)
                for rdata in answers:
                    try:
                        results.append(ipaddress.ip_address(str(rdata)))
                    except ValueError:
                        pass
            except Exception:
                pass
    else:
        try:
            infos = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC,
                                       socket.SOCK_STREAM, 0,
                                       socket.AI_ADDRCONFIG)
            for info in infos:
                addr = info[4][0]
                try:
                    results.append(ipaddress.ip_address(addr))
                except ValueError:
                    pass
        except Exception:
            pass
    return results


def _domain_in_whitelist(hostname: str, require_configured: bool = False) -> bool:
    """
    检查主机名是否在白名单内（支持 *.example.com 通配符）

    :param hostname: 待检查的主机名
    :param require_configured: True 时表示动态模式必须配置白名单（空列表视为未配置）
    """
    if not ALLOWED_DOMAINS:
        if require_configured:
            return False  # 动态模式要求必须配置白名单
        return True  # 静态模式未配置时默认通过

    hostname_lower = hostname.lower()
    for pattern in ALLOWED_DOMAINS:
        pattern_lower = pattern.lower()
        if pattern_lower.startswith("*."):
            suffix = pattern_lower[1:]  # ".example.com"
            if hostname_lower == suffix[1:] or hostname_lower.endswith(suffix):
                return True
        else:
            if hostname_lower == pattern_lower:
                return True
    return False


# ====================
# 对外安全校验接口
# ====================

def validate_url_security(url: str) -> tuple:
    """
    验证 URL 是否符合安全要求：
    1. 协议校验（强制 HTTPS，可配置）
    2. 域名白名单校验（可配置）
    3. 云元数据地址屏蔽
    4. DNS 解析后逐 IP 检查私有网段（防 DNS 重绑定 / SSRF）
    5. 直接 IP 写入时的私有网段检查

    :param url: 待验证的 URL
    :return: (是否安全, 错误信息)
    """
    if not url:
        return False, "URL 不能为空"

    try:
        parsed = urlparse(url)
        scheme = (parsed.scheme or "").lower()
        hostname = parsed.hostname

        if not hostname:
            return False, "无法解析主机名"

        # ── 1. 协议校验 ──────────────────────────────────────────────
        if REQUIRE_HTTPS and scheme != "https":
            return False, f"仅允许 HTTPS 协议，当前协议: {scheme or '(空)'}"

        if scheme not in ("http", "https"):
            return False, f"不支持的协议: {scheme}"

        # ── 2. 云元数据地址屏蔽 ───────────────────────────────────────
        if hostname.lower() in _METADATA_HOSTS:
            return False, f"不允许访问云元数据服务地址: {hostname}"

        # ── 3. 域名白名单校验（静态模式：未配置则默认通过）────────────
        # 注意：动态模式需调用 _fetch_browser_content 内部额外检查
        if not _domain_in_whitelist(hostname, require_configured=False):
            return False, f"域名不在白名单中: {hostname}"

        # ── 4. 若主机名本身是 IP，直接检查 ───────────────────────────
        try:
            ip_obj = ipaddress.ip_address(hostname)
            if _is_private_ip_obj(ip_obj):
                return False, f"不允许访问私有/保留 IP 地址: {hostname}"
            # 直接 IP 无需 DNS 解析，校验通过
            return True, ""
        except ValueError:
            pass  # 不是 IP，继续做 DNS 解析

        # ── 5. DNS 解析后逐 IP 检查（防 SSRF / DNS 重绑定） ──────────
        resolved_ips = _resolve_to_ips(hostname)
        if not resolved_ips:
            return False, f"无法解析域名: {hostname}"

        for ip_obj in resolved_ips:
            if _is_private_ip_obj(ip_obj):
                return False, (
                    f"域名 {hostname} 解析到私有/保留 IP 地址 {ip_obj}，"
                    "拒绝访问（SSRF 防护）"
                )

        return True, ""

    except Exception as e:
        return False, f"URL 解析错误: {str(e)}"


# ====================
# URL 格式判断
# ====================

def is_url(text: str) -> bool:
    """
    判断输入文本是否为有效的 URL
    :param text: 待判断的文本
    :return: 是 URL 返回 True，否则返回 False
    """
    if not text or not isinstance(text, str):
        return False

    text = text.strip()
    url_pattern = re.compile(
        r'^(https?:\/\/)?'
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
        r'(\/[^\s]*)?$'
    )
    return bool(url_pattern.match(text))


# ====================
# 网页内容获取（使用 agent-browser）
# ====================

def _require_browser_mode_allowed() -> dict:
    """
    检查动态模式是否可用。

    ⚠️ 强制要求：动态模式必须配置 ALLOWED_DOMAINS 白名单！
    未配置白名单时直接拒绝使用动态模式，防止 SSRF/内网请求风险。

    :return: 如果不允许使用动态模式，返回错误 dict；否则返回 None
    """
    if not ALLOWED_DOMAINS:
        return {
            "code": -100,
            "message": (
                "动态模式（浏览器渲染）需要配置 ALLOWED_DOMAINS 白名单才能使用。"
                "请在代码中设置 ALLOWED_DOMAINS = ['your-trusted-domain.com', ...]"
            ),
            "data": None
        }
    return None


def fetch_url_content(url: str, wait_time: int = 5, force_mode: str = None) -> dict:
    """
    获取 URL 指定的网页内容。

    行为由全局配置 DISABLE_JAVASCRIPT 决定：
    - DISABLE_JAVASCRIPT = True  （默认）：静态模式，安全高效
    - DISABLE_JAVASCRIPT = False ：智能模式：先静态抓取，失败后自动切换动态模式

    force_mode 参数可覆盖全局配置：
    - force_mode="static"：强制使用静态模式（无需白名单）
    - force_mode="browser"：强制使用动态模式（需要白名单）

    ⚠️ 动态模式默认关闭。如需启用，必须设置 DISABLE_JAVASCRIPT = False 并配置 ALLOWED_DOMAINS 白名单。

    :param url: 目标网址
    :param wait_time: 等待页面加载的额外时间（秒），默认5秒（仅动态模式）
    :param force_mode: 覆盖全局配置，"static" 或 "browser"，默认 None（跟随全局配置）
    :return: 包含状态码和内容的字典
    """
    # 确保 URL 带有协议前缀
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # ── 安全验证（包含 DNS 解析 IP 检查）──────────────────────────────
    is_safe, error_msg = validate_url_security(url)
    if not is_safe:
        return {"code": -100, "message": f"URL 安全检查未通过：{error_msg}", "data": None}
    # ──────────────────────────────────────────────────────────────────

    # 强制静态模式（无需白名单）
    if force_mode == "static":
        return _fetch_static_content(url)

    # ── 强制动态模式：必须配置白名单 ──────────────────────────────────
    if force_mode == "browser":
        check_result = _require_browser_mode_allowed()
        if check_result:
            return check_result
        return _fetch_browser_content(url, wait_time)
    # ──────────────────────────────────────────────────────────────────

    # ── 跟随全局配置 ──────────────────────────────────────────────────
    if DISABLE_JAVASCRIPT:
        # 静态模式（默认）
        return _fetch_static_content(url)

    # ── 智能模式：先静态，失败则切换动态（仅在已配置白名单时）───────
    # 尝试静态抓取
    result = _fetch_static_content(url)

    # 静态抓取成功，返回结果
    if result["code"] == 0:
        return result

    # 静态抓取失败，尝试动态模式（仅在已配置白名单时）
    # 检测是否为空内容（可能是 SPA/JS 渲染页面）
    is_empty = (
        result["code"] == 0 and
        result.get("data", {}).get("content", "").strip() == ""
    ) or (
        result["code"] == 0 and
        len(result.get("data", {}).get("content", "")) < 100  # 内容过少，可能是未渲染的 HTML
    )

    if is_empty or result["code"] != 0:
        # ── 智能切换前检查：必须配置白名单才能使用动态模式 ──────────────
        check_result = _require_browser_mode_allowed()
        if check_result:
            # 白名单未配置时，返回静态模式失败结果（不切换到动态模式）
            return {
                "code": result["code"],
                "message": result["message"] + "（动态模式需要配置 ALLOWED_DOMAINS 白名单，请参考文档）",
                "data": result["data"]
            }
        # ─────────────────────────────────────────────────────────────────

        browser_result = _fetch_browser_content(url, wait_time)
        # 返回动态模式结果（不论成功与否）
        if browser_result["code"] == 0:
            browser_result["message"] = browser_result["message"] + "（静态模式内容为空，自动切换）"
            browser_result["data"]["fallback"] = True
        return browser_result

    return result


def _fetch_static_content(url: str) -> dict:
    """
    使用 requests 抓取静态 HTML（禁用 JavaScript）。

    适用场景：追求安全的静态内容抓取，可避免 JS 发起内网请求的风险。
    不足：无法抓取 SPA/React/Vue 等需要 JS 渲染的页面。
    """
    import time as _time
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,*/*",
        }
        response = requests.get(url, headers=headers, timeout=15, verify=True, allow_redirects=True)
        response.raise_for_status()

        # 重定向后二次校验
        final_url = response.url
        if final_url != url:
            is_safe2, err2 = validate_url_security(final_url)
            if not is_safe2:
                return {"code": -100, "message": f"页面重定向后安全检查未通过：{err2}", "data": None}

        # 尝试提取 <title> 和正文
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
        except ImportError:
            title = ""
            soup = None

        return {
            "code": 0,
            "message": "获取成功（静态模式）",
            "data": {
                "content": response.text,
                "url": final_url,
                "title": title,
                "mode": "static"
            }
        }
    except requests.exceptions.SSLError as e:
        return {"code": -8, "message": f"SSL 证书验证失败：{str(e)}", "data": None}
    except requests.exceptions.Timeout:
        return {"code": -101, "message": f"访问超时：无法在规定时间内加载页面（{url}）", "data": None}
    except requests.exceptions.HTTPError as e:
        return {"code": -4, "message": f"页面返回错误：{str(e)}", "data": None}
    except requests.exceptions.ConnectionError as e:
        return {"code": -5, "message": f"网络连接失败：{str(e)}", "data": None}
    except requests.exceptions.RequestException as e:
        return {"code": -104, "message": f"访问失败：{str(e)}（{url}）", "data": None}
    except Exception as e:
        return {"code": -104, "message": f"访问失败：{str(e)}（{url}）", "data": None}


def _fetch_browser_content(url: str, wait_time: int = 5) -> dict:
    """
    使用 agent-browser 获取动态渲染后的页面内容。

    ⚠️ 前提条件：调用方必须已通过 _require_browser_mode_allowed() 检查。
    此函数不再重复检查白名单（已在 fetch_url_content() 入口处检查）。
    """
    import time as _time

    # ── 防御性检查：双重保障 ──────────────────────────────────────────
    # 注意：此检查是防御性的，实际调用链已确保已检查白名单
    if not ALLOWED_DOMAINS:
        return {
            "code": -100,
            "message": "动态模式需要配置 ALLOWED_DOMAINS 白名单才能使用。",
            "data": None
        }
    # ─────────────────────────────────────────────────────────────────

    browser_opened = False
    try:
        # 1. 启动浏览器
        result = subprocess.run(
            ["agent-browser", "launch"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return {
                "code": -103,
                "message": f"无法启动浏览器：{result.stderr.strip()}。请确保已安装 agent-browser（npm install -g agent-browser）",
                "data": None
            }
        browser_opened = True

        # 2. 打开目标 URL
        result = subprocess.run(
            ["agent-browser", "open", url],
            capture_output=True,
            text=True,
            timeout=35
        )
        if result.returncode != 0:
            return {
                "code": -101,
                "message": f"打开页面失败：{result.stderr.strip()}",
                "data": None
            }

        # 3. 等待页面加载
        _time.sleep(wait_time)

        # 4. 获取页面内容
        result = subprocess.run(
            ["agent-browser", "snapshot"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return {
                "code": -104,
                "message": f"获取页面内容失败：{result.stderr.strip()}",
                "data": None
            }

        content = result.stdout
        final_url = url  # agent-browser snapshot 不返回最终 URL，这里简化处理

        # ── 二次检查：页面重定向后的最终 URL ──────────────────────────
        result = subprocess.run(
            ["agent-browser", "evaluate", "window.location.href"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            final_url = result.stdout.strip()
            if final_url != url:
                is_safe2, err2 = validate_url_security(final_url)
                if not is_safe2:
                    return {
                        "code": -100,
                        "message": f"页面重定向后安全检查未通过：{err2}",
                        "data": None
                    }
        # ─────────────────────────────────────────────────────────────

        return {
            "code": 0,
            "message": "获取成功（浏览器模式）",
            "data": {
                "content": content,
                "url": final_url,
                "title": "",  # agent-browser snapshot 不返回标题
                "mode": "browser"
            }
        }

    except subprocess.TimeoutExpired:
        return {"code": -101, "message": f"访问超时：无法在规定时间内加载页面（{url}）", "data": None}
    except FileNotFoundError:
        return {
            "code": -103,
            "message": "agent-browser 命令未找到。请先安装：npm install -g agent-browser",
            "data": None
        }
    except Exception as e:
        return {"code": -104, "message": f"访问失败：{str(e)}（{url}）", "data": None}
    finally:
        if browser_opened:
            try:
                subprocess.run(
                    ["agent-browser", "close"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            except Exception:
                pass


# ====================
# UCAP 敏感信息检测
# ====================

def check_sensitive(content: str, userKey: str = None, sensitive_code_list: list = None) -> dict:
    """
    错敏信息检测核心函数

    :param content: 待检测文本内容（必传）
    :param userKey: 接口调用密钥（可选，不传则自动从环境变量读取）
    :param sensitive_code_list: 检测类型列表（可选，不传则检测所有类型）
    :return: 标准化检测结果
    """
    if not content:
        return {"code": -1, "message": "待检测文本不能为空", "data": None}

    # ── userKey 优先级：参数 > 环境变量 ───────────────────────────────
    # 如果传入了新的 userKey，则保存到环境变量供后续使用
    if userKey:
        save_userkey(userKey)
    else:
        # 未传入时，尝试从环境变量读取已保存的 userKey
        userKey = get_saved_userkey()
    # ──────────────────────────────────────────────────────────────────

    request_data = {"content": content}
    if sensitive_code_list is not None and len(sensitive_code_list) > 0:
        request_data["sensitiveCodeList"] = sensitive_code_list

    try:
        url = "https://safeguard.ucap.com.cn/safe-apiinterface/open/skill/skillSensitiveCheck"
        headers = {"Content-Type": "application/json"}
        if userKey:
            headers["userKey"] = userKey

        response = requests.post(
            url=url,
            headers=headers,
            json=request_data,
            timeout=15,
            verify=True
        )
        response.raise_for_status()

        return {
            "code": 0,
            "message": "检测成功",
            "data": response.json()
        }

    except requests.exceptions.SSLError as e:
        return {"code": -8, "message": f"SSL 证书验证失败：{str(e)}", "data": None}
    except requests.exceptions.Timeout:
        return {"code": -3, "message": "接口调用超时（15秒）", "data": None}
    except requests.exceptions.HTTPError as e:
        return {"code": -4, "message": f"接口返回错误：{str(e)}",
                "data": response.text if 'response' in locals() else None}
    except requests.exceptions.ConnectionError as e:
        return {"code": -5, "message": f"网络连接失败：{str(e)}", "data": None}
    except requests.exceptions.RequestException as e:
        return {"code": -6, "message": f"接口调用失败：{str(e)}", "data": None}
    except json.JSONDecodeError:
        return {"code": -7, "message": "接口返回非 JSON 格式数据",
                "data": response.text if 'response' in locals() else None}


# ====================
# OpenClaw 标准入口
# ====================

def run(params: dict) -> dict:
    """
    OpenClaw 对话调用的标准入口
    :param params: OpenClaw 传入的参数字典
    :return: 检测结果
    """
    content = params.get("content", "")

    if is_url(content):
        fetch_result = fetch_url_content(content)
        if fetch_result["code"] != 0:
            return fetch_result

        actual_content = fetch_result["data"]["content"]
        source_url = fetch_result["data"]["url"]

        check_result = check_sensitive(
            content=actual_content,
            userKey=params.get("userKey"),
            sensitive_code_list=params.get("sensitive_code_list")
        )

        if check_result.get("code") == 0:
            check_result["source_url"] = source_url
            check_result["source_type"] = "url"

        return check_result
    else:
        check_result = check_sensitive(
            content=content,
            userKey=params.get("userKey"),
            sensitive_code_list=params.get("sensitive_code_list")
        )

        if check_result.get("code") == 0:
            check_result["source_type"] = "text"

        return check_result


# ====================
# 本地测试
# ====================
if __name__ == "__main__":
    # 测试1：SSRF 防护（应被拦截）
    print("=" * 50)
    print("测试1：SSRF 防护 - 内网 IP（应被拦截）")
    print("=" * 50)
    print(json.dumps(validate_url_security("http://192.168.1.1/admin"), ensure_ascii=False, indent=2))

    # 测试2：SSRF 防护（域名解析到私有 IP）
    print("\n" + "=" * 50)
    print("测试2：SSRF 防护 - localhost（应被拦截）")
    print("=" * 50)
    print(json.dumps(validate_url_security("https://localhost/secret"), ensure_ascii=False, indent=2))

    # 测试3：合法 URL
    print("\n" + "=" * 50)
    print("测试3：合法 URL（应通过）")
    print("=" * 50)
    print(json.dumps(validate_url_security("https://example.com"), ensure_ascii=False, indent=2))

    # 测试4：URL 抓取
    print("\n" + "=" * 50)
    print("测试4：URL 抓取")
    print("=" * 50)
    result = fetch_url_content("https://example.com")
    if result["code"] == 0:
        print("抓取成功，标题：", result["data"]["title"])
    else:
        print("抓取失败：", result["message"])

    # 测试5：直接检测文本
    print("\n" + "=" * 50)
    print("测试5：直接检测文本")
    print("=" * 50)
    test_result = run({
        "content": "这是一段待检测的文本内容",
        "userKey": "your_user_key_here"
    })
    print(json.dumps(test_result, ensure_ascii=False, indent=2))
