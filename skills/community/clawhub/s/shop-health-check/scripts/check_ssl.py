#!/usr/bin/env python3
"""
check_ssl.py - SSL 证书健康度检查
自实现，不依赖第三方 skill
"""
import sys
import ssl
import socket
import datetime
import re
import configparser

try:
    import certifi
    HAS_CERTIFI = True
except ImportError:
    HAS_CERTIFI = False


def extract_cn(lst):
    """从嵌套元组格式提取 commonName"""
    for item in lst:
        if isinstance(item, tuple) and len(item) == 2:
            k, v = item
            if k == "commonName":
                return v
        elif isinstance(item, (list, tuple)):
            cn = extract_cn(item)
            if cn != "N/A":
                return cn
    return "N/A"


def parse_expiry_time(time_str):
    """解析 SSL 证书时间字符串"""
    formats = [
        "%b %d %H:%M:%S %Y %Z",
        "%b %d %H:%M:%S %Y GMT",
        "%Y-%m-%d %H:%M:%S %Z",
        "%Y-%m-%d %H:%M:%SZ",
    ]
    # 移除可能的曜日 "Mon, 15 Apr 2024..."
    cleaned = re.sub(r"^[A-Z][a-z]{2},\s+", "", time_str.strip())
    for fmt in formats:
        try:
            return datetime.datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    return None


def check_ssl(domain, port=443, warning_days=14):
    """检查单个域名的 SSL 证书状态"""
    result = {
        "domain": domain, "port": port,
        "issuer": None, "subject": None,
        "not_before": None, "not_after": None,
        "days_remaining": None,
        "status": "unknown", "error": None
    }
    try:
        ctx = ssl.create_default_context(cafile=certifi.where()) if HAS_CERTIFI else ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=8) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert(binary_form=False)
                if not cert:
                    result.update({"error": "无法获取证书", "status": "error"})
                    return result

                not_after = cert.get("notAfter")
                not_before = cert.get("notBefore")
                result["subject"] = extract_cn(cert.get("subject", []))
                result["issuer"] = extract_cn(cert.get("issuer", []))
                result["not_before"] = not_before
                result["not_after"] = not_after

                if not_after:
                    expiry = parse_expiry_time(not_after)
                    if expiry:
                        days = (expiry - datetime.datetime.utcnow()).days
                        result["days_remaining"] = days
                        result["status"] = "expired" if days < 0 else ("warning" if days <= warning_days else "valid")
                    else:
                        result.update({"status": "unknown", "error": f"无法解析过期时间: {not_after}"})
                else:
                    result.update({"status": "unknown", "error": "证书无过期时间"})
    except socket.timeout:
        result.update({"error": "连接超时", "status": "error"})
    except socket.gaierror:
        result.update({"error": "DNS解析失败", "status": "error"})
    except ConnectionRefusedError:
        result.update({"error": "连接被拒绝", "status": "error"})
    except Exception as e:
        result.update({"error": str(e)[:80], "status": "error"})
    return result


def check_all_shops(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    results = {}
    for shop in config.sections():
        if shop == "DEFAULT":
            continue
        domain = config.get(shop, "domain")
        warning_days = int(config.get(shop, "ssl_warning_days", fallback=14))
        r = check_ssl(domain, 443, warning_days)
        r["shop"] = shop
        results[shop] = r
    return results


def main():
    cfg_path = __file__.replace("scripts/check_ssl.py", "config/shops.conf")
    results = check_all_shops(cfg_path)
    for shop, r in results.items():
        icon = {"valid": "✅", "warning": "⚠️", "expired": "❌", "error": "❌"}.get(r["status"], "?")
        days = r.get("days_remaining")
        if r["status"] == "valid":
            print(f"  {icon} {r['domain']}: 正常（剩余 {days} 天）")
        elif r["status"] == "warning":
            print(f"  {icon} {r['domain']}: ⚠️ 剩余 {days} 天，请尽快续期")
        elif r["status"] == "expired":
            print(f"  {icon} {r['domain']}: ❌ 证书已过期！")
        else:
            print(f"  {icon} {r['domain']}: 错误 - {r.get('error', 'unknown')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())