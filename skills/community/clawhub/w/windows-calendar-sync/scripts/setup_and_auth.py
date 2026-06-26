"""
setup_and_auth.py — Windows 日历同步·首次配置向导
=======================================================
第一次运行时自动引导用户完成：
  Step 1: 注册 Azure AD 应用（获取 Client ID）
  Step 2: 设备代码流认证（OAuth 登录）
  Step 3: 保存 token，开始使用

全程约 3 分钟，无需手动操作 Azure 门户以外的任何地方。
"""
import json
import sys
import os
import webbrowser
import time
import urllib.request
import urllib.parse
import urllib.error

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE    = os.path.join(SKILL_DIR, "scripts", "token_store.json")
CLIENT_ID_FILE = os.path.join(SKILL_DIR, "scripts", "client_id.txt")
CONFIG_FILE   = os.path.join(SKILL_DIR, "scripts", "config.txt")

SCOPES = ["openid", "profile", "offline_access", "Calendars.ReadWrite"]

# 读写 TENANT_ID（持久化，不丢失）
def _load_tenant() -> str:
    if os.path.exists(CONFIG_FILE):
        for line in open(CONFIG_FILE, encoding="utf-8"):
            if line.startswith("TENANT_ID="):
                return line.split("=", 1)[1].strip()
    tenant = "fbc75ead-f917-4253-b911-84733c8c3e9c"
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(f"TENANT_ID={tenant}\n")
    return tenant

TENANT_ID = _load_tenant()
AUTH_URL  = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/devicecode"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
GRAPH_API = "https://graph.microsoft.com/v1.0"


# ──────────────────────────────────────────────
# Step 1: 注册 Azure AD 应用
# ──────────────────────────────────────────────
def register_azure_app():
    """打开 Azure 应用注册页面，引导用户创建应用"""
    portal_url = "https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade"
    print("""
╔══════════════════════════════════════════════════════════════╗
║         Step 1 · 注册 Azure AD 应用（免费，约 2 分钟）      ║
╠══════════════════════════════════════════════════════════════╣
║  1. 点击上方链接，打开 Azure 门户（需登录 Microsoft 账户）   ║
║  2. 点击 「新注册」                                           ║
║  3. 名称填写：QClaw Calendar Sync（任意）                   ║
║  4. 支持的账户类型：任意目录中的账户（多租户）              ║
║  5. 重定向 URI：选「公共客户端/移动」, 填 http://localhost   ║
║  6. 点击「注册」                                             ║
║  7. 复制「应用程序(客户端) ID」—— 粘贴到下方                 ║
╚══════════════════════════════════════════════════════════════╝
""")
    webbrowser.open(portal_url)
    client_id = input("请粘贴你的 Application (client) ID: ").strip()
    if not client_id or len(client_id) < 20:
        print("❌ Client ID 无效，请确保格式类似：3fa85f64-5717-45a8-a81e-...")
        sys.exit(1)
    with open(CLIENT_ID_FILE, "w", encoding="utf-8") as f:
        f.write(client_id)
    print(f"✅ Client ID 已保存: {client_id[:20]}...")
    return client_id


def get_client_id() -> str:
    if os.path.exists(CLIENT_ID_FILE):
        with open(CLIENT_ID_FILE, "r", encoding="utf-8") as f:
            cid = f.read().strip()
        if cid:
            return cid
    return register_azure_app()


# ──────────────────────────────────────────────
# Step 2: 设备代码流认证
# ──────────────────────────────────────────────
def get_device_code(client_id: str) -> dict:
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "scope": " ".join(SCOPES),
    }).encode()
    req = urllib.request.Request(AUTH_URL, data=data)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def poll_token(client_id: str, device_code: str, interval: int) -> dict:
    print("\n⏳ 等待你在浏览器中完成登录...\n")
    while True:
        time.sleep(interval)
        data = urllib.parse.urlencode({
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": client_id,
            "device_code": device_code,
        }).encode()
        req = urllib.request.Request(TOKEN_URL, data=data)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            err = json.loads(e.read().decode())
            error = err.get("error")
            if error == "authorization_pending":
                continue
            elif error == "authorization_declined":
                raise Exception("你拒绝了登录请求。请重新运行并同意授权。")
            elif error == "expired_token":
                raise Exception("验证码已过期（通常 15 分钟）。请重新运行脚本。")
            else:
                raise Exception(f"认证失败: {error} — {err.get('error_description', '')}")


def save_token(token_data: dict):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)


def authenticate(client_id: str) -> dict:
    print("""
╔══════════════════════════════════════════════════════════════╗
║              Step 2 · 使用 Microsoft 账户登录               ║
╠══════════════════════════════════════════════════════════════╣
║  脚本将自动打开浏览器进行设备代码登录。                      ║
║  如果浏览器没有自动打开，手动访问：                          ║
║    https://microsoft.com/devicelogin                        ║
║  并输入下方显示的验证码。                                    ║
╚══════════════════════════════════════════════════════════════╝
""")
    dc = get_device_code(client_id)
    user_code = dc.get("user_code")
    verification_url = dc.get("verification_url", "https://microsoft.com/devicelogin")
    interval = dc.get("interval", 5)
    message = dc.get("message", "")

    print(f"  🔗 打开浏览器: {verification_url}")
    print(f"  🔑 验证码: {user_code}")
    if message:
        print(f"  📋 {message}")
    print()
    webbrowser.open(verification_url)

    input("\n  按 Enter 继续（如果已在浏览器完成登录，直接回车）... ")

    token = poll_token(client_id, dc["device_code"], interval)
    import time
    token["_expires_at"] = time.time() + token.get("expires_in", 3600)
    save_token(token)
    return token


# ──────────────────────────────────────────────
# Step 3: 验证 token 是否可用
# ──────────────────────────────────────────────
def verify_token(token: str) -> dict:
    req = urllib.request.Request(f"{GRAPH_API}/me/calendar")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🗓️  Windows 日历同步 · 首次配置向导                      ║
║     将提醒同步到 Microsoft Outlook / Windows 日历            ║
╚══════════════════════════════════════════════════════════════╝
""")

    # 检查是否已认证
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            import time
            if saved.get("access_token") and saved.get("_expires_at"):
                if time.time() < saved["_expires_at"] - 60:
                    print("✅ 已存在有效 token，直接验证...")
                    verify_token(saved["access_token"])
                    print("✅ token 有效！日历同步已就绪。")
                    print(f"   Token 位置: {TOKEN_FILE}")
                    return
                else:
                    print("⏳ token 已过期，正在尝试刷新...")
                    # 尝试刷新
                    client_id = get_client_id()
                    data = urllib.parse.urlencode({
                        "grant_type": "refresh_token",
                        "refresh_token": saved.get("refresh_token", ""),
                        "client_id": client_id,
                        "scope": " ".join(SCOPES),
                    }).encode()
                    req = urllib.request.Request(TOKEN_URL, data=data)
                    try:
                        with urllib.request.urlopen(req) as resp:
                            new_token = json.loads(resp.read().decode())
                            new_token["_expires_at"] = time.time() + new_token.get("expires_in", 3600)
                            save_token(new_token)
                            print("✅ token 刷新成功！日历同步已就绪。")
                            return
                    except Exception as e:
                        print(f"⚠️ 刷新失败（{e}），需要重新认证")
        except Exception as e:
            print(f"⚠️ 读取已有 token 失败: {e}")

    # 完整流程
    client_id = get_client_id()
    token = authenticate(client_id)
    print("\n✅ 认证完成！正在验证访问权限...")

    try:
        calendar = verify_token(token["access_token"])
        print(f"✅ 日历访问正常！日历名称: {calendar.get('name', '默认日历')}")
    except Exception as e:
        print(f"⚠️ 验证时出错（不影响使用）: {e}")

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  ✅ 配置完成！                              ║
╠══════════════════════════════════════════════════════════════╣
║  日历同步已就绪。以后只需说「提醒我...」                     ║
║  我就会自动把事件写入你的 Windows 日历。                    ║
║                                                               ║
║  文件位置:                                                    ║
║    {TOKEN_FILE}
║  Token 有效期: ~90 天（会自动刷新）                         ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消。")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)
