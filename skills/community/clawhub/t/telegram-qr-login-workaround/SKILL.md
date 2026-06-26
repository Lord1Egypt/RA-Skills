---
name: telegram-qr-login-workaround
description: Telegram新设备登录 — 绕过PHONE_CODE_EXPIRED错误，用QR码扫描代替验证码，附脚本和完整流程
triggers:
  - telegram 登录 验证码 过期
  - PHONE_CODE_EXPIRED
  - telegram 新设备 登录失败
  - telethon qr_login
---

# Telegram QR Login — 绕过"PHONE_CODE_EXPIRED"的终极方案

## 问题症状

用 Pyrogram/Telethon 通过手机号+验证码登录 Telegram 时：
- 验证码明明刚收到，立即写入文件
- 仍然报 `PHONE_CODE_EXPIRED`
- Telegram 官方邮件说"Device not approved"

## 根本原因

Telegram 的新设备登录安全机制：
1. 检测到来自新设备（IP/设备指纹）
2. 要求在**手机 App**上手动批准（设置 → 设备 → 批准新设备）
3. 验证码本身没问题，但设备未被批准 = 直接过期

**注意**：`PHONE_CODE_EXPIRED` 在这里是误导性错误，真实原因是"设备未批准"，而非5分钟超时。

## 解决方案：QR码登录（100%有效）

用 Telethon 的 `qr_login()` 方法，让用户直接扫QR，设备自动加入可信列表。

### 环境准备

```bash
# 创建独立 Python 环境（推荐3.12）
python3 -m venv /tmp/tg_env
source /tmp/tg_env/bin/activate
pip install telethon qrcode pillow
```

### 完整脚本

```python
import asyncio, os, qrcode
from telethon import TelegramClient

API_ID = "你的api_id"        # https://my.telegram.org
API_HASH = "你的api_hash"    # 同上
SESSION_PATH = "/path/to/session"  # session文件路径

OUT_PNG = "/tmp/tg_qr.png"

async def main():
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

    print("Connecting...", flush=True)
    await client.connect()
    print("Connected. Generating QR...", flush=True)

    # 获取QR码
    qr_login = await client.qr_login()
    url = qr_login.url
    print(f"QR URL: {url}", flush=True)

    # 生成PNG图片
    img = qrcode.make(url)
    img.save(OUT_PNG)
    print(f"QR saved: {OUT_PNG}", flush=True)

    # 等待扫码完成
    print("Waiting for scan...", flush=True)
    await qr_login.wait()
    print("Scanned!", flush=True)

    me = await client.get_me()
    print(f"OK: {me.first_name} @{me.username} ID={me.id}", flush=True)
    await client.disconnect()

asyncio.run(main())
```

### 使用流程

1. 运行脚本 → 生成 `/tmp/tg_qr.png`
2. 用户手机 Telegram → 设置 → 设备 → 扫描QR码
3. 扫完即登录成功，session文件自动保存
4. 以后复用这个session，无需再验证码

### 推送QR码给用户（示例）

```python
# 发送图片给Telegram用户
with open("/tmp/tg_qr.png", "rb") as f:
    await client.send_file("telegram_chat_id", f)
```

## 常见坑

| 错误 | 原因 | 解决 |
|------|------|------|
| `PHONE_CODE_EXPIRED` | 设备未批准，被误判为超时 | 用QR码登录 |
| `PHONE_NUMBER_INVALID` | 短时间内请求次数过多被封 | 等2分钟再试 |
| `PeerUser not found` (删私聊时) | 对话已不存在 | 跳过，无需处理 |
| QR扫描后立即过期 | 网络问题或IP不稳定 | 换个网络重试 |

## 关键发现

1. **验证码过期 ≠ 真的过期**：Telegram 的错误信息有误导性
2. **QR码绕过所有验证**：扫描即入可信设备列表，不需要手机号验证
3. **Session 格式**：Telethon 和 Pyrogram 的 session 文件格式**互不兼容**，选一个一直用
4. **独立 venv**：避免系统 Python 包冲突

## 批量清理对话

清理可疑频道/陌生私聊：见 `references/telegram-cleanup-workflow.md`（含脚本 + 失败处理）

## 发布到 GitHub / ClawHub

### GitHub Gist（最快，1分钟搞定）

用户去 https://github.com/settings/tokens/new 创建 PAT（勾 `gist` scope），发给你后用 curl 直接调用 GitHub API：

```bash
curl -s -X POST "https://api.github.com/gists" \
  -H "Authorization: token <PAT>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "<标题>",
    "public": true,
    "files": {
      "telegram-qr-login.md": {"content": "..."}
    }
  }'
```

返回 `html_url` 即为发布链接。无需 `gh` CLI，无需登录。

### ClawHub

ClawHub 需要独立的 GitHub OAuth 登录（`Sign in with GitHub`），不支持 GitHub PAT。
流程：
1. `npm i -g clawhub`（已装）
2. 用户在 https://clawhub.ai/login 用 GitHub OAuth 登录
3. 登录后用 `clawhub login --token <token>` 或浏览器交互方式认证
4. `clawhub skill publish <path> --slug <slug>`

注意：ClawHub skill 存储在 Convex 数据库，GitHub 仓库 openclaw/clawhub 的 skills/ 目录是模板，非实际发布路径。

## 适用场景

- 新设备首次登录 Telegram
- 账号因频繁验证请求被临时封禁
- 自动化脚本需要无感知的长期登录
