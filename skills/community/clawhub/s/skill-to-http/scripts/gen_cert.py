#!/usr/bin/env python3
"""gen_cert.py — 为 skill-to-http 生成/管理自签 TLS 证书

特性：
- 支持 SAN（Subject Alternative Names）配置，可同时签多个 IP/域名
- 证书路径由 tls_auth.detect_http_root() 决定（默认 <workspace>/.http/certs/）
- 默认有效期 825 天（macOS 信任链上限）
- 子命令：generate（默认）/ info / renew / import
- 生成后打印客户端信任配置方法

用法：
    python3 gen_cert.py                                  # 交互式生成
    python3 gen_cert.py --san 10.40.1.2,myserver.local   # 直接指定 SAN
    python3 gen_cert.py --san auto                       # 自动嗅探本机 IP
    python3 gen_cert.py --force                          # 覆盖已有证书
    python3 gen_cert.py info                             # 查看当前证书状态
    python3 gen_cert.py renew --san auto                 # 强制续期
    python3 gen_cert.py import --cert <path> --key <path>  # 导入现有证书
"""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
from pathlib import Path

# 路径统一从 tls_auth 拿（workspace 内 .http/ 持久化）
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from tls_auth import CERT_DIR  # noqa: E402

CERT_PATH = CERT_DIR / "server.crt"
KEY_PATH = CERT_DIR / "server.key"
CSR_CONF = CERT_DIR / "openssl.cnf"

DEFAULT_DAYS = 825  # macOS Catalina+ 信任链上限
DEFAULT_CN = "skill-to-http"


def detect_local_ips() -> list[str]:
    """嗅探本机所有非 lo 的 IPv4。"""
    ips: list[str] = []
    try:
        # 通用方法：连接外网（不会真发包，只是让内核选源 IP）
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            primary = s.getsockname()[0]
            if primary and primary != "127.0.0.1":
                ips.append(primary)
    except Exception:
        pass

    try:
        # hostname -I 兜底，能拿到多个内网 IP
        result = subprocess.run(
            ["hostname", "-I"], capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            for ip in result.stdout.strip().split():
                if ip and ip != "127.0.0.1" and ip not in ips:
                    ips.append(ip)
    except Exception:
        pass

    return ips


def write_openssl_conf(cn: str, san_entries: list[str]) -> None:
    """生成 openssl 配置文件（含 SAN 扩展）。"""
    san_lines = []
    ip_idx = 1
    dns_idx = 1
    for entry in san_entries:
        # 简单判断 IP vs 域名
        parts = entry.split(".")
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            san_lines.append(f"IP.{ip_idx} = {entry}")
            ip_idx += 1
        else:
            san_lines.append(f"DNS.{dns_idx} = {entry}")
            dns_idx += 1

    # 总是把 localhost 和 127.0.0.1 加进去
    if "127.0.0.1" not in san_entries:
        san_lines.append(f"IP.{ip_idx} = 127.0.0.1")
    if "localhost" not in san_entries:
        san_lines.append(f"DNS.{dns_idx} = localhost")

    conf = f"""[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = CN
ST = Shanghai
L = Shanghai
O = OpenClaw
OU = HTTP Services
CN = {cn}

[v3_req]
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
{chr(10).join(san_lines)}
"""
    CSR_CONF.write_text(conf)


def generate_cert(cn: str, san_entries: list[str], days: int = DEFAULT_DAYS) -> None:
    """调用 openssl 生成自签证书。

    Raises:
        RuntimeError: openssl 命令失败时抛出友好错误（含原始 stderr 摘要）
        FileNotFoundError: openssl 未安装时抛出
    """
    write_openssl_conf(cn, san_entries)

    # 1. 生成私钥
    try:
        subprocess.run(
            ["openssl", "genrsa", "-out", str(KEY_PATH), "2048"],
            check=True, capture_output=True,
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            "openssl 命令未找到。请安装：apt-get install openssl / brew install openssl"
        )
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or b"").decode(errors="replace").strip()
        raise RuntimeError(f"openssl genrsa 失败（生成私钥）：{stderr[:500]}") from e

    try:
        os.chmod(KEY_PATH, 0o600)
    except OSError as e:
        # 私钥权限设置失败不致命，但要告警
        import logging as _logging
        _logging.getLogger("skill-to-http.cert").warning(
            f"无法设置私钥权限 0600：{e}（建议手动 chmod）"
        )

    # 2. 生成自签证书（一步到位）
    try:
        subprocess.run(
            [
                "openssl", "req", "-x509", "-new", "-nodes",
                "-key", str(KEY_PATH),
                "-sha256",
                "-days", str(days),
                "-out", str(CERT_PATH),
                "-config", str(CSR_CONF),
                "-extensions", "v3_req",
            ],
            check=True, capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or b"").decode(errors="replace").strip()
        raise RuntimeError(
            f"openssl req 失败（生成自签证书）：{stderr[:500]}\n"
            f"  配置文件：{CSR_CONF}\n"
            f"  CN={cn} SAN={san_entries}"
        ) from e

    try:
        os.chmod(CERT_PATH, 0o644)
    except OSError:
        pass  # 证书权限不致命


def verify_cert() -> dict:
    """读取已生成证书的关键信息。"""
    if not CERT_PATH.exists():
        return {}
    try:
        out = subprocess.check_output(
            ["openssl", "x509", "-in", str(CERT_PATH), "-noout", "-text"],
            text=True,
        )
        info = {"path": str(CERT_PATH)}
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Not After"):
                info["expires"] = line.split(":", 1)[1].strip()
            elif line.startswith("Subject:"):
                info["subject"] = line.split(":", 1)[1].strip()
            elif "DNS:" in line or "IP Address:" in line:
                info["san"] = line.strip()
        return info
    except Exception as e:
        return {"error": str(e)}


def import_cert(src_cert: str, src_key: str) -> None:
    """导入现有证书 + 私钥到 ~/.http/certs/。

    复制时校验：
    - 文件存在且可读
    - cert 是合法 X.509 PEM
    - key 是合法 PEM 私钥
    """
    import shutil
    src_cert_p = Path(src_cert).expanduser().resolve()
    src_key_p = Path(src_key).expanduser().resolve()
    if not src_cert_p.exists():
        raise FileNotFoundError(f"证书文件不存在: {src_cert_p}")
    if not src_key_p.exists():
        raise FileNotFoundError(f"私钥文件不存在: {src_key_p}")

    # 校验是 PEM 格式
    cert_content = src_cert_p.read_text(errors="replace")
    if "-----BEGIN CERTIFICATE-----" not in cert_content:
        raise ValueError(f"证书文件不是合法 PEM 格式: {src_cert_p}")
    key_content = src_key_p.read_text(errors="replace")
    if "-----BEGIN" not in key_content or "PRIVATE KEY" not in key_content:
        raise ValueError(f"私钥文件不是合法 PEM 格式: {src_key_p}")

    # 用 openssl 校验证书可被解析
    try:
        subprocess.run(
            ["openssl", "x509", "-in", str(src_cert_p), "-noout"],
            check=True, capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(f"证书无法被 openssl 解析: {e.stderr.decode() if e.stderr else e}")

    # 复制到目标位置
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_cert_p, CERT_PATH)
    shutil.copy2(src_key_p, KEY_PATH)
    os.chmod(CERT_PATH, 0o644)
    os.chmod(KEY_PATH, 0o600)


def get_cert_status() -> dict:
    """返回证书状态字典，用于 doctor / cert info 命令。

    字段：
    - exists: bool
    - expires_at: str (ISO 8601) or None
    - days_until_expiry: int or None
    - san: list[str]
    - subject: str
    - needs_renewal: bool (30 天内过期)
    - san_mismatch: bool (本机 IP 不在 SAN 中)
    """
    status: dict = {
        "exists": CERT_PATH.exists() and KEY_PATH.exists(),
        "cert_path": str(CERT_PATH),
        "key_path": str(KEY_PATH),
        "expires_at": None,
        "days_until_expiry": None,
        "san": [],
        "subject": "",
        "needs_renewal": False,
        "san_mismatch": False,
    }
    if not status["exists"]:
        return status

    try:
        import datetime
        # 取到期时间（machine readable）
        out = subprocess.check_output(
            ["openssl", "x509", "-in", str(CERT_PATH), "-noout", "-enddate", "-subject", "-ext", "subjectAltName"],
            text=True,
        )
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("notAfter="):
                # notAfter=Aug 25 06:00:00 2027 GMT
                date_str = line.split("=", 1)[1].strip()
                try:
                    dt = datetime.datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z")
                    dt = dt.replace(tzinfo=datetime.timezone.utc)
                    status["expires_at"] = dt.isoformat()
                    days = (dt - datetime.datetime.now(datetime.timezone.utc)).days
                    status["days_until_expiry"] = days
                    status["needs_renewal"] = days <= 30
                except ValueError:
                    pass
            elif line.startswith("subject="):
                status["subject"] = line.split("=", 1)[1].strip()
            elif "DNS:" in line or "IP Address:" in line:
                # X509v3 Subject Alternative Name: DNS:localhost, IP Address:127.0.0.1
                parts = [p.strip() for p in line.split(",")]
                sans = []
                for p in parts:
                    if "DNS:" in p:
                        sans.append(p.split("DNS:", 1)[1].strip())
                    elif "IP Address:" in p:
                        sans.append(p.split("IP Address:", 1)[1].strip())
                status["san"] = sans

        # 检测本机 IP 是否都在 SAN 中
        local_ips = detect_local_ips()
        san_set = set(status["san"])
        for ip in local_ips:
            if ip not in san_set:
                status["san_mismatch"] = True
                break
    except Exception as e:
        status["error"] = str(e)

    return status


def print_trust_instructions() -> None:
    """打印各端如何信任自签证书的指引。"""
    print()
    print("=" * 60)
    print("  📋 客户端如何信任此自签证书")
    print("=" * 60)
    print()
    print(f"证书路径：{CERT_PATH}")
    print()
    print("【curl】")
    print(f"  curl --cacert {CERT_PATH} https://your-host:port/health")
    print("  # 或临时跳过验证：curl -k https://...")
    print()
    print("【Python requests】")
    print("  requests.get('https://...', verify='" + str(CERT_PATH) + "')")
    print()
    print("【浏览器】")
    print("  macOS: 双击证书 → 钥匙串访问 → 改信任为「始终信任」")
    print("  Windows: 双击证书 → 安装到「受信任的根证书颁发机构」")
    print("  Linux: cp 到 /usr/local/share/ca-certificates/ && update-ca-certificates")
    print()
    print("【验证证书有效性】")
    print(f"  openssl s_client -connect your-host:port -CAfile {CERT_PATH}")
    print()


def _cmd_info():
    """显示当前证书状态。"""
    status = get_cert_status()
    if not status["exists"]:
        print(f"❌ 证书不存在：{CERT_PATH}")
        print(f"   生成方法：python3 gen_cert.py --san auto")
        return
    print("=" * 60)
    print(f"  🔐 当前证书状态")
    print("=" * 60)
    print(f"  证书路径    : {status['cert_path']}")
    print(f"  私钥路径    : {status['key_path']}")
    print(f"  Subject     : {status.get('subject', '?')}")
    print(f"  SAN         : {', '.join(status.get('san', [])) or '(无)'}")
    print(f"  到期时间    : {status.get('expires_at', '?')}")
    days = status.get("days_until_expiry")
    if days is not None:
        if days <= 0:
            print(f"  剩余天数    : ❌ 已过期 {-days} 天")
        elif days <= 30:
            print(f"  剩余天数    : ⚠️  {days} 天（建议续期）")
        else:
            print(f"  剩余天数    : ✅ {days} 天")
    if status.get("san_mismatch"):
        local = detect_local_ips()
        print(f"  ⚠️  本机 IP {local} 部分不在 SAN 中，外部访问可能失败")
        print(f"     建议：python3 gen_cert.py --san auto --force")
    print("=" * 60)


def _cmd_import(args):
    """导入现有证书。"""
    if not args.cert or not args.key:
        print("❌ import 模式需要 --cert <path> --key <path>")
        sys.exit(1)
    try:
        import_cert(args.cert, args.key)
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        sys.exit(1)
    print(f"✅ 证书已导入到：")
    print(f"   {CERT_PATH}")
    print(f"   {KEY_PATH}")
    _cmd_info()


def main():
    parser = argparse.ArgumentParser(description="为 skill-to-http 生成/管理自签 TLS 证书")
    parser.add_argument("--san", default=None,
                        help="逗号分隔的 SAN 列表（IP/域名），或 'auto' 自动嗅探")
    parser.add_argument("--cn", default=DEFAULT_CN, help="证书 Common Name")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="有效期（天）")
    parser.add_argument("--force", action="store_true", help="覆盖已有证书")
    # 子命令模式
    parser.add_argument("command", nargs="?", default="generate",
                        choices=["generate", "info", "renew", "import"],
                        help="generate=生成（默认）, info=查看, renew=强制续期, import=导入现有证书")
    parser.add_argument("--cert", help="import 模式：源证书路径")
    parser.add_argument("--key", help="import 模式：源私钥路径")
    args = parser.parse_args()

    # 子命令分发
    if args.command == "info":
        _cmd_info()
        return
    if args.command == "renew":
        args.force = True
        # 续期默认用 auto SAN
        if not args.san:
            args.san = "auto"
        # 落入 generate 流程
    if args.command == "import":
        _cmd_import(args)
        return

    # 检查 openssl 可用
    try:
        subprocess.run(["openssl", "version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ 未找到 openssl 命令，请先安装：apt-get install openssl / brew install openssl")
        sys.exit(1)

    CERT_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(CERT_DIR.parent, 0o700)

    # 检查是否已有证书
    if CERT_PATH.exists() and not args.force:
        info = verify_cert()
        print(f"⚠️  证书已存在：{CERT_PATH}")
        if info.get("expires"):
            print(f"   到期时间：{info['expires']}")
        if info.get("san"):
            print(f"   SAN：{info['san']}")
        print()
        print("如需重新生成，加 --force")
        return

    # 收集 SAN
    san_entries: list[str] = []
    if args.san == "auto":
        san_entries = detect_local_ips()
        print(f"🔍 自动嗅探到的本机 IP：{san_entries or '(无)'}")
    elif args.san:
        san_entries = [s.strip() for s in args.san.split(",") if s.strip()]
    else:
        # 交互式
        detected = detect_local_ips()
        print(f"🔍 检测到本机 IP：{detected or '(无)'}")
        prompt = "请输入证书要绑定的 IP/域名（逗号分隔，回车=用检测到的）: "
        user_input = input(prompt).strip()
        if user_input:
            san_entries = [s.strip() for s in user_input.split(",") if s.strip()]
        else:
            san_entries = detected

    if not san_entries:
        print("⚠️  未配置任何 SAN，仅 127.0.0.1 和 localhost 可访问")

    # 生成
    print()
    print(f"📝 生成证书 CN={args.cn} SAN={san_entries + ['127.0.0.1', 'localhost']}")
    try:
        generate_cert(args.cn, san_entries, args.days)
    except subprocess.CalledProcessError as e:
        print(f"❌ openssl 失败：{e.stderr.decode() if e.stderr else e}")
        sys.exit(1)

    print(f"✅ 证书已生成")
    print(f"   证书：{CERT_PATH}")
    print(f"   私钥：{KEY_PATH}")
    info = verify_cert()
    if info.get("expires"):
        print(f"   到期：{info['expires']}")

    print_trust_instructions()


if __name__ == "__main__":
    main()


def _cert_needs_regeneration(cert_path, key_path) -> bool:
    """判断是否需要重新生成证书。

    返回 True（需要重生）的条件：
    1. 证书或私钥文件不存在
    2. 证书已过期或 30 天内过期（临近续期）
    3. 本机 IP 不在证书 SAN 中（IP 发生变化）

    返回 False 表示已有证书仍可用，跳过生成。
    """
    cert_p = Path(cert_path).expanduser()
    key_p = Path(key_path).expanduser()

    # 1. 文件不存在
    if not cert_p.exists() or not key_p.exists():
        return True

    # 2. 检查过期（用 openssl 解析，有效期内且 >30 天剩余才跳过）
    try:
        out = subprocess.check_output(
            ["openssl", "x509", "-in", str(cert_p), "-noout", "-enddate"],
            text=True, stderr=subprocess.DEVNULL,
        )
        # 格式: notAfter=May 26 16:03:16 2028 GMT
        date_str = out.strip().split("=", 1)[1]
        from datetime import datetime, timezone
        expire_dt = datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        days_left = (expire_dt - datetime.now(timezone.utc)).days
        if days_left < 30:
            logger.info(f"Certificate expires in {days_left} days, will regenerate")
            return True
    except Exception:
        # openssl 不可用或格式异常，保守重生
        return True

    # 3. 检查本机 IP 是否在 SAN 里（IP 漂移时重生）
    try:
        san_out = subprocess.check_output(
            ["openssl", "x509", "-in", str(cert_p), "-noout", "-ext", "subjectAltName"],
            text=True, stderr=subprocess.DEVNULL,
        )
        local_ips = detect_local_ips()
        # san_out 中 IP Address 格式: IP Address:10.40.69.146
        san_ips = set()
        for token in san_out.replace(",", "\n").split():
            if token.startswith("IP"):
                ip = token.split(":", 1)[-1].strip()
                san_ips.add(ip)
        # 至少本机一个非 127 IP 在 SAN 中即可（127.0.0.1 已在 generate_cert 写死）
        non_lo = [ip for ip in local_ips if ip != "127.0.0.1"]
        if non_lo and not any(ip in san_ips for ip in non_lo):
            logger.info(f"Local IPs {non_lo} not in cert SAN {san_ips}, will regenerate")
            return True
    except Exception:
        # SAN 检查失败视为兼容，不强制重生
        pass

    return False
