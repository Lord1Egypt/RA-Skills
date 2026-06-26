#!/usr/bin/env python3
"""
115网盘 QR码登录脚本
登录类型: tv (不占手机/网页名额，最稳定)
用法: python3 115_qrlogin.py
"""
import requests
import time
import subprocess
import sys
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (SmartTV; Linux) AppleWebKit/537.36",
}

def qr_login():
    # Security note:
    # - Credentials are written directly to rclone config file (chmod 600)
    # - Credentials are NEVER passed as command-line arguments (not visible in process list)
    # - Credentials are stored locally only and never transmitted to third parties
    # - Only 115 Pan API endpoints are contacted
    s = requests.Session()
    s.headers.update(HEADERS)

    # 1. 获取二维码 token
    print("[1/3] 获取二维码...", flush=True)
    r = s.get("https://qrcodeapi.115.com/api/1.0/tv/1.0/token",
              params={"_": int(time.time()*1000)})
    r.raise_for_status()
    data = r.json()
    if not data.get("state"):
        print("获取二维码失败:", data)
        sys.exit(1)

    token = data["data"]
    uid   = token["uid"]
    sign  = token["sign"]
    ts    = token["time"]
    qr_url = f"https://qrcodeapi.115.com/api/1.0/tv/1.0/qrcode?uid={uid}"

    print(f"[2/3] 请用 115 App 扫码登录 (TV模式，不影响其他端):\n")
    print(f"  二维码图片: {qr_url}\n")
    print("等待扫码...", flush=True)

    # 2. 轮询状态
    for _ in range(120):  # 最多等2分钟
        time.sleep(2)
        r = s.get("https://qrcodeapi.115.com/get/status/",
                  params={"uid": uid, "time": ts, "sign": sign, "_": int(time.time()*1000)})
        r.raise_for_status()
        status = r.json().get("data", {})
        code = status.get("status", 0)

        if code == 0:
            print("  等待扫码...", flush=True)
        elif code == 1:
            print("  已扫码，请在App上确认授权...", flush=True)
        elif code == 2:
            print("  已授权！获取凭证...", flush=True)
            break
        elif code == -1:
            print("二维码已过期，请重新运行脚本")
            sys.exit(1)
        elif code == -2:
            print("已取消")
            sys.exit(1)
    else:
        print("超时")
        sys.exit(1)

    # 3. 获取 Cookie
    r = s.post("https://passportapi.115.com/app/1.0/tv/1.0/login/qrcode/",
               data={"account": uid, "app": "tv"})
    r.raise_for_status()
    result = r.json()

    if not result.get("state"):
        print("获取凭证失败:", result)
        sys.exit(1)

    cookie_data = result.get("data", {}).get("cookie", {})
    uid_val  = cookie_data.get("UID", "")
    cid_val  = cookie_data.get("CID", "")
    seid_val = cookie_data.get("SEID", "")
    kid_val  = cookie_data.get("KID", "")

    if not uid_val or not cid_val or not seid_val:
        print("凭证不完整，请重试")
        sys.exit(1)

    # 4. 写入 rclone config（通过环境变量+临时文件传递凭证，避免凭证出现在进程列表）
    print("[3/3] 写入 rclone 配置...", flush=True)

    # 获取 rclone 配置文件路径
    # 优先使用 skill 安装的 115-fork (~/.local/bin/rclone)，fallback 到 PATH 里的 rclone
    _rclone_candidates = [
        os.path.expanduser("~/.local/bin/rclone"),
        "rclone",
    ]
    _rclone_cmd = None
    for _candidate in _rclone_candidates:
        try:
            _test = subprocess.run([_candidate, "--version"], capture_output=True)
            if _test.returncode == 0:
                _rclone_cmd = _candidate
                break
        except FileNotFoundError:
            continue

    cfg_path = ""
    if _rclone_cmd:
        try:
            cfg_result = subprocess.run([_rclone_cmd, "config", "file"],
                                        capture_output=True, text=True)
            for line in cfg_result.stdout.splitlines():
                line = line.strip()
                if line.endswith(".conf") or line.endswith(".config"):
                    cfg_path = line
                    break
            if not cfg_path:
                lines = [l.strip() for l in cfg_result.stdout.splitlines() if l.strip()]
                cfg_path = lines[-1] if lines else ""
        except Exception:
            pass
    if not cfg_path:
        cfg_path = os.path.expanduser("~/.config/rclone/rclone.conf")

    # 直接写入 rclone.conf，凭证不经过命令行参数（ps aux 不可见）
    import configparser as _cp
    cfg = _cp.ConfigParser()
    try:
        cfg.read(cfg_path)
    except Exception:
        pass
    cfg["115drive"] = {
        "type": "115",
        "uid": uid_val,
        "cid": cid_val,
        "seid": seid_val,
        "kid": kid_val,
        "pacer_min_sleep": "500ms",
    }
    os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
    with open(cfg_path, "w") as f:
        cfg.write(f)
    os.chmod(cfg_path, 0o600)  # 仅当前用户可读
    print(f"  配置文件: {cfg_path}")

    print("\n✓ 115网盘授权完成，配置已写入 rclone (remote: 115drive)")
    print("  验证: rclone lsd 115drive:")

if __name__ == "__main__":
    qr_login()
