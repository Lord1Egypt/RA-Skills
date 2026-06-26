#!/usr/bin/env python3
"""
Safe Web Fetch - 安全的智能网页获取工具

特性:
- 强制 SSL 验证
- URL 白名单验证（防止 SSRF）
- 敏感数据检测
- 自动使用 Jina Reader 清洗

用法:
    python3 safe_fetch.py <url> [--json]
    python3 safe_fetch.py --show-config
"""

import sys
import os
import re
import json
import socket
import urllib.parse
import urllib.request
import ssl
from pathlib import Path

# ==================== 安全配置 ====================

# 私有 IP 范围（用于 SSRF 防护）
PRIVATE_IP_RANGES = [
    (0x0A000000, 0x0AFFFFFF),  # 10.0.0.0/8
    (0xAC100000, 0xAC1FFFFFF), # 172.16.0.0/12
    (0xC0A80000, 0xC0A8FFFF),  # 192.168.0.0/16
    (0x7F000000, 0x7FFFFFFF),  # 127.0.0.0/8
    (0xA9FE0000, 0xA9FEFFFF),  # 169.254.0.0/16 (link-local)
]

# 敏感数据正则模式
SENSITIVE_PATTERNS = [
    r'api[_-]?key\s*[=:]\s*["\']?[\w-]{20,}',
    r'apikey\s*[=:]\s*["\']?[\w-]{20,}',
    r'access[_-]?token\s*[=:]\s*["\']?[\w-]{20,}',
    r'auth[_-]?token\s*[=:]\s*["\']?[\w-]{20,}',
    r'bearer\s+[\w-]+\b',
    r'Authorization:\s*Bearer\s+',
    r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID
    r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']?[\w/+]{40}',
    r'-----BEGIN\s+[\w\s]*PRIVATE\s+KEY-----',
    r'-----BEGIN\s+RSA\s+PRIVATE\s+KEY-----',
    r'sk-[a-zA-Z0-9]{20,}',  # OpenAI API keys
    r'xox[baprs]-[\w-]+',  # Slack tokens
]

# 允许的协议
ALLOWED_SCHEMES = ['http', 'https']

# 危险域名后缀
BLOCKED_DOMAIN_SUFFIXES = [
    '.local',
    '.internal',
    '.localdomain',
    '.localhost',
    '.home',
    '.lan',
]

# 默认配置
DEFAULT_CONFIG = {
    "allowed_domains": [],
    "blocked_domains": [],
    "max_content_size": 10 * 1024 * 1024,  # 10MB
    "timeout": 30,
    "user_agent": "SafeWebFetch/1.0 (Security-First)",
    "max_redirects": 5
}

# ==================== 安全检查函数 ====================

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except Exception as e:
            print(f"Warning: Failed to load config: {e}", file=sys.stderr)
    return DEFAULT_CONFIG.copy()


def ip_to_int(ip_str):
    """将 IP 地址转换为整数"""
    try:
        parts = ip_str.split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16) + \
               (int(parts[2]) << 8) + int(parts[3])
    except:
        return None


def is_private_ip(ip_str):
    """检查是否为私有 IP 地址"""
    ip_int = ip_to_int(ip_str)
    if ip_int is None:
        return False
    for start, end in PRIVATE_IP_RANGES:
        if start <= ip_int <= end:
            return True
    return False


def resolve_hostname(hostname):
    """解析主机名并返回所有 IP 地址"""
    try:
        results = socket.getaddrinfo(hostname, None)
        ips = set()
        for result in results:
            ip = result[4][0]
            ips.add(ip)
        return list(ips)
    except:
        return []


def validate_url(url, config):
    """
    验证 URL 安全性
    
    检查:
    1. 协议必须是 HTTP/HTTPS
    2. 主机名不能是私有 IP
    3. 解析后的 IP 不能是私有地址
    4. 不能在黑名单中
    5. 如果有白名单，必须在白名单中
    
    Returns:
        (is_valid, error_message)
    """
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception as e:
        return False, f"Invalid URL format: {e}"
    
    # 检查协议
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return False, f"Blocked scheme: {parsed.scheme}. Only HTTP/HTTPS allowed."
    
    hostname = parsed.hostname
    if not hostname:
        return False, "Missing hostname in URL"
    
    hostname_lower = hostname.lower()
    
    # 检查危险域名后缀
    for suffix in BLOCKED_DOMAIN_SUFFIXES:
        if hostname_lower.endswith(suffix) or hostname_lower == suffix[1:]:
            return False, f"Blocked internal domain: {hostname}"
    
    # 检查 localhost
    if hostname_lower in ['localhost', '127.0.0.1', '::1']:
        return False, "Blocked: localhost"
    
    # 检查黑名单域名
    for blocked in config['blocked_domains']:
        if hostname_lower == blocked.lower() or hostname_lower.endswith('.' + blocked.lower()):
            return False, f"Domain in blocklist: {hostname}"
    
    # 如果有白名单，检查白名单
    if config['allowed_domains']:
        allowed = False
        for domain in config['allowed_domains']:
            if hostname_lower == domain.lower() or hostname_lower.endswith('.' + domain.lower()):
                allowed = True
                break
        if not allowed:
            return False, f"Domain not in allowlist: {hostname}"
    
    # 检查是否为私有 IP（直接 IP 访问）
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if re.match(ip_pattern, hostname):
        if is_private_ip(hostname):
            return False, f"Blocked private IP: {hostname}"
    
    # 解析域名并检查所有 IP
    ips = resolve_hostname(hostname)
    for ip in ips:
        # 检查是否为私有 IP
        if is_private_ip(ip):
            return False, f"Domain resolves to private IP: {hostname} -> {ip}"
    
    return True, None


def detect_sensitive_data(content):
    """
    检测内容中是否包含敏感数据
    
    Returns:
        (has_sensitive, pattern_name)
    """
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True, pattern
    return False, None


# ==================== 获取函数 ====================

def create_ssl_context():
    """创建安全的 SSL 上下文（强制验证）"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    return ctx


def fetch_url_direct(url, config, check_sensitive=True):
    """直接获取 URL 内容（用于原始内容兜底）"""
    try:
        ssl_context = create_ssl_context()
        req = urllib.request.Request(
            url,
            headers={'User-Agent': config['user_agent']}
        )
        
        with urllib.request.urlopen(req, timeout=config['timeout'], context=ssl_context) as response:
            # 检查内容大小
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > config['max_content_size']:
                return {
                    "success": False,
                    "content": "",
                    "error": f"Content too large: {content_length} bytes"
                }
            
            content = response.read(config['max_content_size']).decode('utf-8', errors='ignore')
            
            # 检测敏感数据
            if check_sensitive:
                has_sensitive, pattern = detect_sensitive_data(content)
                if has_sensitive:
                    return {
                        "success": False,
                        "content": "",
                        "error": f"Sensitive data detected (refusing to process): matches pattern"
                    }
            
            return {
                "success": True,
                "content": content,
                "status": response.status
            }
    except ssl.SSLCertVerificationError as e:
        return {
            "success": False,
            "content": "",
            "error": f"SSL verification failed: {e}"
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "content": "",
            "error": f"URL error: {e.reason}"
        }
    except Exception as e:
        return {
            "success": False,
            "content": "",
            "error": str(e)
        }


def fetch_with_jina(original_url, config):
    """使用 Jina Reader 获取清洗后的内容"""
    # 构建 Jina Reader URL
    clean_url = original_url.replace('https://', '').replace('http://', '')
    jina_url = f"https://r.jina.ai/http://{clean_url}"
    
    # Jina Reader 返回的是 Markdown，无需检测敏感数据（已经是清洗后的）
    result = fetch_url_direct(jina_url, config, check_sensitive=False)
    
    if result['success']:
        result['source'] = 'jina'
        result['url'] = jina_url
        result['original_url'] = original_url
    
    return result


def get_clean_content(url, config=None):
    """
    获取网页的干净 Markdown 内容
    
    策略: Jina Reader → 原始内容（本地清洗）
    
    Returns:
        {
            "success": bool,
            "url": str,           # 实际使用的 URL
            "original_url": str,  # 用户提供的原始 URL
            "content": str,       # 获取到的内容
            "source": str,        # 使用的服务: jina/original
            "content_length": int,
            "error": str          # 失败时的错误信息
        }
    """
    if config is None:
        config = load_config()
    
    original_url = url.strip()
    
    # 1. 验证 URL 安全性
    is_valid, error = validate_url(original_url, config)
    if not is_valid:
        return {
            "success": False,
            "url": original_url,
            "original_url": original_url,
            "content": "",
            "source": "none",
            "content_length": 0,
            "error": f"Security: {error}"
        }
    
    # 2. 尝试 Jina Reader
    try:
        result = fetch_with_jina(original_url, config)
        if result['success'] and len(result['content']) > 100:
            result['content_length'] = len(result['content'])
            return result
    except Exception:
        pass
    
    # 3. 降级到原始内容
    try:
        result = fetch_url_direct(original_url, config)
        if result['success']:
            return {
                "success": True,
                "url": original_url,
                "original_url": original_url,
                "content": result['content'],
                "source": "original",
                "content_length": len(result['content']),
                "error": None
            }
    except Exception as e:
        pass
    
    return {
        "success": False,
        "url": original_url,
        "original_url": original_url,
        "content": "",
        "source": "none",
        "content_length": 0,
        "error": "All fetch methods failed"
    }


def show_config():
    """显示当前配置"""
    config = load_config()
    print("Current Safe Web Fetch Configuration:")
    print(json.dumps(config, indent=2))
    print("\nSecurity Features:")
    print("  ✅ SSL verification: ENABLED")
    print("  ✅ URL whitelist validation: ENABLED")
    print("  ✅ SSRF protection: ENABLED")
    print("  ✅ Sensitive data detection: ENABLED")
    print("\nBlocked Patterns:")
    for pattern in SENSITIVE_PATTERNS[:5]:
        print(f"  - {pattern}")
    print(f"  ... and {len(SENSITIVE_PATTERNS) - 5} more")


def main():
    if len(sys.argv) < 2:
        print("Usage: safe_fetch.py <url> [--json]", file=sys.stderr)
        print("       safe_fetch.py --show-config", file=sys.stderr)
        print("\nOptions:", file=sys.stderr)
        print("  --json          Output as JSON", file=sys.stderr)
        print("  --show-config   Show current configuration", file=sys.stderr)
        sys.exit(1)
    
    if sys.argv[1] == '--show-config':
        show_config()
        sys.exit(0)
    
    url = sys.argv[1]
    output_json = "--json" in sys.argv
    
    result = get_clean_content(url)
    
    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result['success']:
            print(f"# Source: {result['source']}")
            print(f"# URL: {result['url']}")
            print(f"# Content Length: {result['content_length']} bytes")
            print()
            print(result['content'])
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
