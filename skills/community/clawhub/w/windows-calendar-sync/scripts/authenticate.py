"""
authenticate.py — Microsoft Graph 设备代码流认证
从同目录 client_id.txt 读取 Client ID，从 config.txt 读取 Tenant ID
"""
import json, os, sys, time, webbrowser, urllib.request, urllib.parse, urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE  = os.path.join(SCRIPT_DIR, "token_store.json")
CLIENT_FILE = os.path.join(SCRIPT_DIR, "client_id.txt")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.txt")   # 存 TENANT_ID

SCOPES = ["openid", "profile", "offline_access", "Calendars.ReadWrite"]


def _load_config():
    """从 config.txt 读取 TENANT_ID，不存在则创建"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("TENANT_ID="):
                    return line.split("=", 1)[1].strip()
    # 自动创建，写入已知有效值
    tenant = "fbc75ead-f917-4253-b911-84733c8c3e9c"
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(f"TENANT_ID={tenant}\n")
    return tenant


def _client_id() -> str:
    if os.path.exists(CLIENT_FILE):
        cid = open(CLIENT_FILE, encoding="utf-8").read().strip()
        if cid:
            return cid
    cid = open(CLIENT_FILE, encoding="utf-8").read().strip()
    if cid:
        return cid
    raise RuntimeError(
        "未找到 Client ID。请先运行 setup_and_auth.py 完成首次配置。"
    )


TENANT_ID = _load_config()
CLIENT_ID = _client_id()
AUTH_URL  = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/devicecode"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"


# ── 设备代码获取 ────────────────────────────────────────────────
def _device_code() -> dict:
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "scope": " ".join(SCOPES),
    }).encode()
    req = urllib.request.Request(AUTH_URL, data=data)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        raise RuntimeError(
            f"获取设备代码失败 (HTTP {e.code}):\n"
            f"  error={body.get('error')}\n"
            f"  description={body.get('error_description','')}\n\n"
            f"请确认：\n"
            f"  1. Client ID ({CLIENT_ID}) 正确\n"
            f"  2. Azure 应用「支持的账户类型」包含你的账户\n"
            f"  3. Tenant ID ({TENANT_ID}) 正确"
        )


# ── 轮询 token ─────────────────────────────────────────────────
def _poll(device_code: str, interval: int, user_code: str):
    print(f"\n  🔗 打开浏览器: https://microsoft.com/devicelogin")
    print(f"  🔑 输入验证码: {user_code}")
    print(f"  ⏳ 等待你在浏览器完成登录...\n")

    while True:
        time.sleep(interval)
        data = urllib.parse.urlencode({
            "grant_type":  "urn:ietf:params:oauth:grant-type:device_code",
            "client_id":   CLIENT_ID,
            "device_code": device_code,
        }).encode()
        req = urllib.request.Request(TOKEN_URL, data=data)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            err = json.loads(e.read().decode())
            err_code = err.get("error")
            if err_code == "authorization_pending":
                continue
            elif err_code == "authorization_declined":
                raise RuntimeError("你拒绝了登录请求。")
            elif err_code == "expired_token":
                raise RuntimeError("验证码已过期（15分钟），请重新运行脚本。")
            else:
                raise RuntimeError(
                    f"Token 获取失败: {err_code}\n{err.get('error_description','')}"
                )


# ── token 文件读写 ──────────────────────────────────────────────
def _save(token_data: dict):
    token_data["_expires_at"] = time.time() + token_data.get("expires_in", 3600)
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2, ensure_ascii=False)


def _load() -> dict | None:
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None


# ── 主入口 ──────────────────────────────────────────────────────
def get_access_token() -> str:
    """
    返回有效 access_token。
    优先使用缓存 token，必要时自动刷新或重新认证。
    """
    token_data = _load()

    if token_data:
        # 提前5分钟刷新
        if time.time() < token_data.get("_expires_at", 0) - 300:
            return token_data["access_token"]
        # 尝试用 refresh_token 刷新
        if "refresh_token" in token_data:
            data = urllib.parse.urlencode({
                "grant_type":    "refresh_token",
                "refresh_token": token_data["refresh_token"],
                "client_id":     CLIENT_ID,
                "scope":         " ".join(SCOPES),
            }).encode()
            req = urllib.request.Request(TOKEN_URL, data=data)
            try:
                with urllib.request.urlopen(req) as resp:
                    new = json.loads(resp.read().decode())
                    _save(new)
                    return new["access_token"]
            except Exception:
                pass  # refresh_token 也过期了，走重新认证

    # ── 重新认证 ──
    print("\n[Windows Calendar Sync] 正在进行 Microsoft 账户认证...")
    dc = _device_code()
    token_data = _poll(
        dc["device_code"],
        dc.get("interval", 5),
        dc["user_code"],
    )
    _save(token_data)
    print("[Windows Calendar Sync] ✅ 认证完成！Token 已保存。\n")
    return token_data["access_token"]


# ── 单独运行脚本 ────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        token = get_access_token()
        print(f"\n✅ access_token 获取成功 (长度: {len(token)})")
        print(f"   文件: {TOKEN_FILE}")
    except Exception as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)
