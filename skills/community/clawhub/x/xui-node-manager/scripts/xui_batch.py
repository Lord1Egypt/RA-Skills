#!/usr/bin/env python3
"""
3x-ui 批量 VLESS 节点管理工具
──────────────────────────────────────────
多面板登录 → 创建 VLESS+Reality+TCP 节点
→ 绑定 SOCKS5 出口 → 输出 QR 码

用法: python xui_batch.py
环境: pip install -r requirements.txt
"""

import json
import sys
import uuid
import base64
import secrets
import subprocess
import re
import os
import urllib3
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import yaml
import requests
import qrcode
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

urllib3.disable_warnings()

# ============================================================
# 工具函数
# ============================================================

def load_config(path: Path) -> dict:
    if not path.exists():
        print(f"❌ 配置文件不存在: {path}")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def find_xray_bin() -> Optional[str]:
    """查找本地 xray 二进制"""
    paths = [
        os.path.expanduser("~/Library/Application Support/v2rayN/bin/xray/xray"),
        "/usr/local/bin/xray",
        "/usr/bin/xray",
    ]
    for p in paths:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return shutil.which("xray")
import shutil


def generate_reality_keys(session: requests.Session, panel: dict) -> tuple[str, str]:
    """生成 x25519 密钥对，优先使用面板 API（含公钥），失败则回退本地"""
    # 方式 1: 面板 API — 直接返回私钥+公钥
    try:
        resp = session.get(f"{panel['url']}/panel/api/server/getNewX25519Cert", timeout=15)
        data = resp.json()
        if data.get("success") and data.get("obj"):
            obj = data["obj"]
            if obj.get("privateKey") and obj.get("publicKey"):
                return obj["privateKey"], obj["publicKey"]
    except Exception:
        pass

    # 方式 2: 本地 xray 二进制
    xray_bin = find_xray_bin()
    if xray_bin:
        try:
            out = subprocess.run([xray_bin, "x25519"], capture_output=True, text=True, timeout=10)
            priv = re.search(r'PrivateKey:\s*(\S+)', out.stdout).group(1)
            pub = re.search(r'PublicKey\):\s*(\S+)', out.stdout).group(1)
            return priv, pub
        except Exception:
            pass

    # 方式 3: cryptography 库
    priv = X25519PrivateKey.generate()
    pub = priv.public_key()
    priv_b64 = base64.urlsafe_b64encode(
        priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    ).decode().rstrip("=")
    pub_b64 = base64.urlsafe_b64encode(
        pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    ).decode().rstrip("=")
    return priv_b64, pub_b64


def derive_public_key(private_key_b64: str) -> str:
    """从 private key 推导 public key（urlsafe base64 格式）"""
    # 补齐 base64 填充
    padding = 4 - len(private_key_b64) % 4
    if padding != 4:
        private_key_b64 += "=" * padding
    priv_bytes = base64.urlsafe_b64decode(private_key_b64)
    priv = X25519PrivateKey.from_private_bytes(priv_bytes)
    pub_bytes = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return base64.urlsafe_b64encode(pub_bytes).decode().rstrip("=")


def generate_short_id() -> str:
    return secrets.token_hex(4)


# ============================================================
# 3x-ui API 操作
# ============================================================

def api_login(session: requests.Session, panel: dict) -> bool:
    url = f"{panel['url']}/login"
    try:
        resp = session.post(url, json={
            "username": panel["username"],
            "password": panel["password"]
        }, timeout=30)
        data = resp.json()
        if data.get("success"):
            print(f"  ✅ 登录成功: {panel['name']}")
            return True
        print(f"  ❌ 登录失败: {panel['name']} — {data.get('msg', resp.text[:200])}")
        return False
    except Exception as e:
        print(f"  ❌ 连接失败: {panel['name']} — {e}")
        return False


def api_add_inbound(session: requests.Session, panel: dict, cfg: dict, socks5: dict,
                    priv_key: str, pub_key: str, short_id: str) -> Optional[dict]:
    """创建 VLESS+Reality+TCP inbound，返回含 id/tag/port/uid 的 dict"""
    from datetime import datetime
    import random
    defaults = cfg.get("defaults", {})

    # 端口：random 则随机，否则用固定值
    port_cfg = defaults.get("port", "random")
    if port_cfg == "random" or str(port_cfg).lower() == "random":
        lo, hi = defaults.get("port_range", [10000, 60000])
        port = random.randint(lo, hi)
    else:
        port = int(port_cfg)

    # 客户端标识：出口 IP 最后两段
    ip_parts = socks5["address"].split(".")
    ip_suffix = ".".join(ip_parts[-2:]) if len(ip_parts) >= 2 else socks5["address"]

    # 备注：创建日期-IP末两段
    remark = f"{datetime.now().strftime('%Y-%m-%d')}-{ip_suffix}"
    client_tag = f"{ip_suffix}-{remark}"

    uid = str(uuid.uuid4())

    settings = json.dumps({
        "clients": [{
            "id": uid,
            "flow": "",
            "email": f"{client_tag}",
            "enable": True,
            "limitIp": 0,
            "totalGB": 0,
            "expiryTime": 0,
            "tgId": 0,
            "subId": ""
        }],
        "decryption": "none",
        "encryption": "none",
        "fallbacks": []
    })

    stream = json.dumps({
        "network": defaults.get("network", "tcp"),
        "security": "reality",
        "externalProxy": [],
        "realitySettings": {
            "show": False,
            "xver": 0,
            "target": defaults.get("dest", "1.1.1.1:443"),
            "serverNames": defaults.get("server_names", ["www.microsoft.com"]),
            "privateKey": priv_key,
            "minClientVer": "",
            "maxClientVer": "",
            "maxTimediff": 0,
            "shortIds": [short_id],
            "mldsa65Seed": "",
            "settings": {
                "publicKey": pub_key,
                "fingerprint": defaults.get("fingerprint", "chrome"),
                "serverName": "",
                "spiderX": "/",
                "mldsa65Verify": ""
            }
        },
        "tcpSettings": {
            "acceptProxyProtocol": False,
            "header": {"type": "none"}
        }
    })

    sniffing = json.dumps({
        "enabled": False,
        "destOverride": ["http", "tls", "quic", "fakedns"],
        "metadataOnly": False,
        "routeOnly": False
    })

    payload = {
        "up": 0, "down": 0, "total": 0,
        "remark": remark,
        "enable": True,
        "expiryTime": 0,
        "listen": "",
        "port": port,
        "protocol": "vless",
        "settings": settings,
        "streamSettings": stream,
        "sniffing": sniffing
    }

    url = f"{panel['url']}/panel/api/inbounds/add"
    try:
        resp = session.post(url, json=payload, timeout=45)
        data = resp.json()
        if data.get("success"):
            obj = data["obj"]
            tag = obj.get("tag", f"inbound-{port}")
            print(f"  ✅ 节点创建: {remark} (端口 {port}, tag={tag})")
            return {
                "uid": uid,
                "port": port,
                "remark": remark,
                "tag": tag,
                "public_key": pub_key,
                "short_id": short_id,
                "inbound_id": obj.get("id")
            }
        print(f"  ❌ 创建失败: {data.get('msg', resp.text[:200])}")
        return None
    except Exception as e:
        print(f"  ❌ API 异常: {e}")
        return None


def api_get_xray_setting(session: requests.Session, panel: dict) -> Optional[dict]:
    """获取 xray config 设置，返回 {xraySetting, inboundTags, outboundTestUrl}"""
    try:
        resp = session.post(f"{panel['url']}/panel/xray/", timeout=30)
        data = resp.json()
        if data.get("success"):
            obj = data["obj"]
            return json.loads(obj) if isinstance(obj, str) else obj
        return None
    except Exception as e:
        print(f"  ⚠️  获取 xray 设置失败: {e}")
        return None


def api_save_xray_setting(session: requests.Session, panel: dict,
                           xray_setting: dict, outbound_test_url: str) -> bool:
    """保存 xray config 设置（必须用 form-encoded data）"""
    try:
        resp = session.post(
            f"{panel['url']}/panel/xray/update",
            data={
                "xraySetting": json.dumps(xray_setting),
                "outboundTestUrl": outbound_test_url
            },
            timeout=45
        )
        data = resp.json()
        if data.get("success"):
            print(f"  ✅ Xray 配置已保存")
            return True
        print(f"  ⚠️  保存失败: {data.get('msg', resp.text[:100])}")
        return False
    except Exception as e:
        print(f"  ⚠️  保存异常: {e}")
        return False


# ============================================================
# SOCKS5 绑定
# ============================================================

def bind_socks5_outbound(session: requests.Session, panel: dict,
                          socks5: dict, inbound_tag: str) -> bool:
    """在 Xray 设置中添加 SOCKS5 outbound 并创建路由规则"""
    setting = api_get_xray_setting(session, panel)
    if not setting:
        return False

    xs = setting["xraySetting"]
    outbound_test_url = setting.get("outboundTestUrl", "https://www.google.com/generate_204")

    tag = f"socks5-{socks5['address']}"
    xs.setdefault("outbounds", [])

    # 添加 SOCKS5 outbound（去重）
    if not any(o.get("tag") == tag for o in xs["outbounds"]):
        xs["outbounds"].append({
            "protocol": "socks",
            "tag": tag,
            "settings": {
                "servers": [{
                    "address": socks5["address"],
                    "port": socks5["port"],
                    "users": [{
                        "user": socks5["username"],
                        "pass": socks5["password"]
                    }]
                }]
            }
        })
        print(f"  ✅ 已添加 SOCKS5 outbound: {tag}")
    else:
        print(f"  ℹ️  SOCKS5 outbound 已存在")

    # 添加路由规则（去重）
    xs.setdefault("routing", {}).setdefault("rules", [])
    rules = xs["routing"]["rules"]

    updated = False
    for rule in rules:
        if inbound_tag in rule.get("inboundTag", []):
            rule["outboundTag"] = tag
            updated = True
            break

    if not updated:
        rules.append({
            "type": "field",
            "inboundTag": [inbound_tag],
            "outboundTag": tag
        })

    print(f"  ✅ 路由规则: {inbound_tag} → {tag}")
    return api_save_xray_setting(session, panel, xs, outbound_test_url)


# ============================================================
# 节点链接 & QR
# ============================================================

def build_vless_uri(panel: dict, node: dict, cfg: dict) -> str:
    defaults = cfg.get("defaults", {})
    host = urlparse(panel["url"]).hostname or "127.0.0.1"

    params = [
        f"type={defaults.get('network', 'tcp')}",
        "encryption=none",
        "security=reality",
        f"pbk={node['public_key']}",
        f"fp={defaults.get('fingerprint', 'chrome')}",
        f"sni={defaults.get('server_names', ['www.microsoft.com'])[0]}",
        f"sid={node['short_id']}",
        "spx=%2F"
    ]
    param_str = "&".join(params)
    return f"vless://{node['uid']}@{host}:{node['port']}?{param_str}#{node['remark']}"


def show_qr(uri: str, remark: str, output_dir: Path):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10, border=2
    )
    qr.add_data(uri)
    qr.make(fit=True)

    # 终端 ASCII（非 TTY 环境会失败，忽略）
    try:
        qr.print_ascii(tty=True)
    except OSError:
        qr.print_ascii()

    # PNG
    png_path = output_dir / f"qr_{remark}.png"
    qr.make_image(fill_color="black", back_color="white").save(png_path)
    print(f"  QR_PNG: {png_path}")
    print(f"  {uri}")


# ============================================================
# 主流程
# ============================================================

def parse_socks5(raw: str) -> dict:
    """解析 socks5 字符串 ip:port:user:pass → dict"""
    parts = raw.strip().split(":")
    if len(parts) < 2:
        print(f"❌ SOCKS5 格式错误，需要 ip:port:user:pass，收到: {raw}")
        sys.exit(1)
    return {
        "address": parts[0],
        "port": int(parts[1]),
        "username": parts[2] if len(parts) > 2 else "",
        "password": parts[3] if len(parts) > 3 else ""
    }


def main():
    import argparse
    ap = argparse.ArgumentParser(description="3x-ui VLESS 节点管理")
    ap.add_argument("--server", required=True, help="目标服务器名 (对应 servers.yaml) 或 all")
    ap.add_argument("--socks5", required=True, help="SOCKS5 出口 (ip:port:user:pass)")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    config = load_config(script_dir / "servers.yaml")

    socks5 = parse_socks5(args.socks5)

    all_panels = config.get("servers", config.get("panels", []))
    if not all_panels:
        print("❌ servers.yaml 中无服务器")
        sys.exit(1)

    # 过滤目标服务器
    if args.server == "all":
        panels = all_panels
    else:
        panels = [p for p in all_panels if p.get("name") == args.server]
        if not panels:
            print(f"❌ 未找到服务器: {args.server}")
            print(f"   可用: {[p.get('name') for p in all_panels]}")
            sys.exit(1)

    # 代理配置
    proxy_url = config.get("proxy", "")
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    output_dir = script_dir.parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("=" * 56)
    print("  3x-ui VLESS 节点管理")
    print(f"  目标: {args.server} | SOCKS5: {socks5['address']}:{socks5['port']}")
    if proxies:
        print(f"  🔀 代理: {proxy_url}")
    print("=" * 56)

    ok = 0
    for panel in panels:
        print(f"\n── {panel['name']} ──")
        s = requests.Session()
        s.verify = False
        if proxies:
            s.proxies = proxies

        if not api_login(s, panel):
            continue

        priv_key, pub_key = generate_reality_keys(s, panel)
        short_id = generate_short_id()
        print(f"  🔑 密钥已生成")

        node = api_add_inbound(s, panel, config, socks5, priv_key, pub_key, short_id)
        if not node:
            continue

        bind_socks5_outbound(s, panel, socks5, node["tag"])

        # 重启 Xray 使路由规则生效
        try:
            r = s.post(f"{panel['url']}/panel/api/server/restartXrayService", timeout=30)
            if r.json().get("success"):
                print(f"  ✅ Xray 已重启")
        except Exception:
            print(f"  ⚠️  Xray 重启失败，请手动重启")

        uri = build_vless_uri(panel, node, config)
        print(f"\n  📡 节点链接:")
        show_qr(uri, node["remark"], output_dir)
        ok += 1

    print(f"\n{'=' * 56}")
    print(f"  完成: {ok}/{len(panels)} 成功")
    print(f"  输出: {output_dir}")
    print(f"{'=' * 56}")


if __name__ == "__main__":
    main()
