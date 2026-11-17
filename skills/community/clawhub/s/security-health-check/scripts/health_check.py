#!/usr/bin/env python3
"""
security-health-check: 本地安全健康检查工具
- HIBP 密码泄露检测（k-匿名，密码不离开本地）
- 本地密码强度分析
- SSL 证书检查
- 综合安全评分
"""

import argparse
import hashlib
import math
import re
import socket
import ssl
import sys
from datetime import datetime
from typing import Optional

try:
    import requests
except ImportError:
    print("❌ 请先安装依赖: pip3 install requests")
    sys.exit(1)

try:
    import OpenSSL
    _HAS_OPENSSL = True
except ImportError:
    _HAS_OPENSSL = False


# ═══════════════════════════════════════════════
# 1. HIBP 密码泄露检测（k-匿名）
# ═══════════════════════════════════════════════

def check_hibp(password: str) -> dict:
    """
    使用 k-匿名检测密码是否在 HIBP 泄露库中。
    密码永不离开本地，只发送 SHA-1 前5位。
    
    ⚠️ 已知限制：HIBP /range/ 接口不返回 breached count（需 API Key）。
    本实现通过密码存在性检测泄露，返回 {"leaked": true/false}。
    如需完整 count，需购买 HIBP API Key。
    """
    if not password:
        return {"leaked": False, "count": 0, "suffix": "", "error": "空密码"}
    
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    
    try:
        r = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={"Add-Padding": "true"},
            timeout=15
        )
        r.raise_for_status()
        
        # HIBP API 返回格式：SUFFIX:COUNT\n...
        hashes = r.text.strip().split("\n")
        for line in hashes:
            if ":" not in line:
                continue
            h_suffix, count = line.split(":")
            if h_suffix.strip() == suffix:
                return {
                    "leaked": True,
                    "count": int(count.strip()),
                    "suffix": suffix,
                    "sha1_prefix": prefix
                }
        
        return {
            "leaked": False,
            "count": 0,
            "suffix": suffix,
            "sha1_prefix": prefix
        }
        
    except requests.RequestException as e:
        return {
            "leaked": False,
            "count": 0,
            "suffix": suffix,
            "error": str(e)
        }


# ═══════════════════════════════════════════════
# 2. 本地密码强度分析
# ═══════════════════════════════════════════════

def analyze_password_strength(password: str) -> dict:
    """
    分析本地密码强度（熵值 + 评分 + 破解时间估算）。
    不发送任何数据到外部。
    """
    if not password:
        return {
            "score": 0,
            "level": "空密码",
            "entropy_bits": 0,
            "crack_time": "瞬间",
            "pool_size": 0,
            "length": 0
        }
    
    # 计算字符池大小
    pool = 0
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~!@#$%^&*()_+]', password))
    
    if has_lower: pool += 26
    if has_upper: pool += 26
    if has_digit: pool += 10
    if has_special: pool += 32
    
    # 熵值计算
    entropy = math.log2(pool ** len(password)) if pool > 0 else 0
    
    # 评分 0-100
    score = min(100, int(entropy / 80 * 100))
    
    if score < 20:
        level = "极弱"
    elif score < 40:
        level = "弱"
    elif score < 60:
        level = "中等"
    elif score < 80:
        level = "强"
    else:
        level = "极强"
    
    # 破解时间估算（假设 10^10 次/秒，GPU 集群）
    seconds_to_crack = (pool ** len(password)) / 2 / 10**10
    crack_time = _format_crack_time(seconds_to_crack)
    
    return {
        "score": score,
        "level": level,
        "entropy_bits": round(entropy, 2),
        "crack_time": crack_time,
        "pool_size": pool,
        "length": len(password),
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_special": has_special
    }


def _format_crack_time(seconds: float) -> str:
    """格式化破解时间"""
    if seconds < 1:
        return "瞬间"
    units = [
        ("秒", 60),
        ("分钟", 60),
        ("小时", 24),
        ("天", 365),
        ("年", 100),
        ("世纪", 1000)
    ]
    val = seconds
    for name, div in units:
        if val < div:
            return f"{val:.1f} {name}"
        val /= div
    return f"{val:.1e} 年"


# ═══════════════════════════════════════════════
# 3. 综合安全评分（0-100）
# ═══════════════════════════════════════════════

def calculate_security_score(password_strength: dict, hibp_result: dict) -> dict:
    """
    综合安全评分算法：
    - HIBP 泄露：直接判 0
    - 无泄露：密码强度分 * 0.4 + 60（基础分）
    """
    if hibp_result.get("leaked"):
        return {
            "score": 0,
            "level": "极度危险",
            "details": [
                "❌ 密码已在公开泄露库中出现",
                f"   相同密码已被使用 {hibp_result.get('count', '?')} 次",
                "⚠️ 请立即更换密码"
            ]
        }
    
    strength_score = password_strength["score"]
    base_score = 60
    final_score = strength_score * 0.4 + base_score
    final_score = max(0, min(100, int(final_score)))
    
    if final_score >= 90:
        level = "优秀"
    elif final_score >= 75:
        level = "良好"
    elif final_score >= 50:
        level = "一般"
    elif final_score >= 25:
        level = "较差"
    else:
        level = "危险"
    
    details = []
    if password_strength["score"] >= 80:
        details.append("✅ 密码强度良好")
    elif password_strength["score"] >= 50:
        details.append("⚠️ 密码强度一般，建议增强")
    else:
        details.append("❌ 密码强度不足，请使用更复杂的密码")
    
    details.append("✅ 未在公开泄露库中发现（HIBP）")
    
    if password_strength["length"] < 12:
        details.append("💡 建议：密码长度至少 12 位")
    if not password_strength["has_special"]:
        details.append("💡 建议：加入特殊字符增强安全性")
    
    return {
        "score": final_score,
        "level": level,
        "details": details,
        "strength_contribution": strength_score * 0.4,
        "base_contribution": base_score
    }


# ═══════════════════════════════════════════════
# 4. SSL 证书检查
# ═══════════════════════════════════════════════

def check_ssl(url_or_host: str) -> dict:
    """
    检查目标网站的 SSL 证书有效性。
    支持 OpenSSL（详细）和内置 ssl（基础）两种模式。
    """
    # 解析主机
    host = url_or_host
    if host.startswith("http"):
        from urllib.parse import urlparse
        parsed = urlparse(url_or_host if url_or_host.startswith("http") else f"https://{url_or_host}")
        host = parsed.hostname or url_or_host
    
    try:
        port = 443
        
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        with socket.create_connection((host, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                
                # OpenSSL 模式：详细证书信息
                if _HAS_OPENSSL:
                    x509 = OpenSSL.crypto.load_certificate(
                        OpenSSL.crypto.FILETYPE_ASN1, cert
                    )
                    not_before = datetime.strptime(
                        x509.get_notBefore().decode(), "%Y%m%d%H%M%SZ"
                    )
                    not_after = datetime.strptime(
                        x509.get_notAfter().decode(), "%Y%m%d%H%M%SZ"
                    )
                    issuer_components = dict(x509.get_issuer().get_components())
                    issuer_cn = issuer_components.get(b'CN', b'Unknown').decode()
                    issuer_org = issuer_components.get(b'O', b'').decode()
                else:
                    # 内置 ssl 模式：基础信息
                    cert_dict = ssock.getpeercert()
                    not_before_str = cert_dict.get('notBefore', '')
                    not_after_str = cert_dict.get('notAfter', '')
                    issuer = dict(cert_dict.get('issuer', []))
                    issuer_cn = ''
                    issuer_org = ''
                    for key in issuer:
                        if key[0][1] == 'commonName':
                            issuer_cn = key[1]
                        if key[0][1] == 'organizationName':
                            issuer_org = key[1]
                    not_before = datetime.fromisoformat(
                        not_before_str[0:10]
                    ) if not_before_str else datetime.now()
                    not_after = datetime.fromisoformat(
                        not_after_str[0:10]
                    ) if not_after_str else datetime.now()
                
                days_left = (not_after - datetime.utcnow()).days
                
                return {
                    "valid": True,
                    "host": host,
                    "issuer_cn": issuer_cn or "Unknown",
                    "issuer_org": issuer_org,
                    "not_before": not_before.isoformat(),
                    "not_after": not_after.isoformat(),
                    "days_left": days_left,
                    "detailed": _HAS_OPENSSL
                }
                
    except ssl.SSLCertVerificationError as e:
        return {"valid": False, "host": host, "error": f"证书验证失败: {str(e)}"}
    except socket.timeout:
        return {"valid": False, "host": host, "error": "连接超时"}
    except socket.gaierror:
        return {"valid": False, "host": host, "error": "无法解析域名"}
    except Exception as e:
        return {"valid": False, "host": host, "error": str(e)}


# ═══════════════════════════════════════════════
# 5. 输出格式化
# ═══════════════════════════════════════════════

def print_report(password: str = None, ssl_host: str = None, full: bool = False):
    """打印安全报告"""
    print("\n🔐 安全健康检查报告")
    print("━" * 40)
    
    if password:
        print("\n📌 密码强度分析")
        print("─" * 20)
        strength = analyze_password_strength(password)
        print(f"  评分：{strength['score']}分 ({strength['level']})")
        print(f"  熵值：{strength['entropy_bits']} bits")
        print(f"  预计破解时间：{strength['crack_time']}")
        print(f"  长度：{strength['length']} 位")
        chars = []
        if strength['has_lower']: chars.append("小写字母")
        if strength['has_upper']: chars.append("大写字母")
        if strength['has_digit']: chars.append("数字")
        if strength['has_special']: chars.append("特殊字符")
        print(f"  字符类型：{', '.join(chars)}")
        
        print("\n📌 HIBP 泄露检测")
        print("─" * 20)
        hibp = check_hibp(password)
        if "error" in hibp:
            print(f"  ⚠️ 检测失败：{hibp['error']}")
        elif hibp["leaked"]:
            print(f"  ❌ 已泄露！相同密码已被使用 {hibp['count']} 次")
            print(f"     （k-匿名：仅发送哈希前5位，密码未离开本地）")
        else:
            print(f"  ✅ 未发现泄露")
            print(f"     （k-匿名：仅发送哈希前5位，密码未离开本地）")
        
        print("\n📌 综合安全评分")
        print("─" * 20)
        final = calculate_security_score(strength, hibp)
        print(f"  {final['score']} / 100 ({final['level']})")
        for d in final["details"]:
            print(f"  {d}")
    
    if ssl_host:
        print(f"\n📌 SSL 证书检查: {ssl_host}")
        print("─" * 20)
        ssl_result = check_ssl(ssl_host)
        if ssl_result["valid"]:
            print(f"  ✅ 证书有效")
            print(f"  颁发者：{ssl_result['issuer_org']} ({ssl_result['issuer_cn']})")
            print(f"  有效期至：{ssl_result['not_after']}")
            print(f"  剩余：{ssl_result['days_left']} 天")
            if ssl_result["days_left"] < 30:
                print(f"  ⚠️ 证书即将过期，请续期！")
        else:
            print(f"  ❌ 证书检查失败")
            print(f"  原因：{ssl_result.get('error', '未知错误')}")
    
    if full and not password and not ssl_host:
        print("\n📌 综合安全报告")
        print("─" * 20)
        print("  使用 -p <密码> 检查密码安全")
        print("  使用 -s <域名> 检查 SSL 证书")
        print("  使用 -a 检查全部")
    
    print()


# ═══════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🔐 安全健康检查工具 - HIBP 密码泄露检测 + 密码强度分析 + SSL 证书检查",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 health_check.py -p mypassword123        # 检查密码
  python3 health_check.py -s example.com          # 检查 SSL 证书
  python3 health_check.py -a                       # 完整报告
  python3 health_check.py -p mypassword -s google.com  # 同时检查
        """
    )
    parser.add_argument("-p", "--password", help="要检查的密码（仅本地分析）")
    parser.add_argument("-s", "--ssl", help="检查网站的 SSL 证书")
    parser.add_argument("-a", "--all", action="store_true", help="完整报告模式")
    
    args = parser.parse_args()
    
    if not args.password and not args.ssl and not args.all:
        parser.print_help()
        print("\n💡 提示：密码仅在本地计算熵值，不会上传到任何服务器")
        sys.exit(0)
    
    print_report(password=args.password, ssl_host=args.ssl, full=args.all)


if __name__ == "__main__":
    main()
