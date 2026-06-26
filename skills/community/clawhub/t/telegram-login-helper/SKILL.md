---
name: telegram-login-helper
description: Consolidate practical Telegram personal-account login workflows for tdl/TDLib: reuse an existing namespace, complete QR login, batch-login multiple namespaces, copy working TDLib state, and escalate honestly when human auth or API credentials are required. Use when Telegram personal-account access is blocked at login or when another agent needs a clean local login runbook.
metadata:
  {
    "openclaw":
      {
        "version": "1.0.0",
        "author": "Stevewu422",
        "license": "MIT",
        "tags": ["telegram", "tdl", "tdlib", "login", "qr", "mtproto"],
        "category": "communications"
      }
  }
---

# Telegram Login Helper

这个 skill 专门处理 **Telegram 个人账号登录**，不是 bot token。

适用场景：
- `tdl` / TDLib 登录卡住
- QR 扫码登录做不完
- 需要复用已有 namespace
- 需要一次性登录多个人号 namespace
- 另一个 agent 需要一份清晰的本地登录 runbook

## 核心路线

永远优先走 **personal account** 路线：
- `tdl`
- `TDLib`
- `MTProto`

不要因为 QR 登录不顺就切去 Bot API。

## 已确认的本地现实

- 已有可复用 namespace：`steve`
- TDLib 数据目录：`/home/stevewu/.tdl/data`
- 单 namespace 复用脚本：`/home/stevewu/.openclaw/workspace/skills/telegram-login-helper/scripts/reuse_namespace.sh`
- 多 namespace QR 登录脚本：`/home/stevewu/.openclaw/workspace/skills/telegram-login-helper/scripts/login_10_namespaces.sh`
- 参考 runbook：`/home/stevewu/.openclaw/workspace/skills/telegram-login-helper/references/runbook.md`

## 推荐处理顺序

### 1. 先复用已有 namespace
先别急着重新登录，先测旧登录态还活不活：

```bash
bash /home/stevewu/.openclaw/workspace/skills/telegram-login-helper/scripts/reuse_namespace.sh steve 5
```

或直接：

```bash
tdl chat ls -n steve --limit 5
```

### 2. 需要新 namespace 时，走 QR 登录
单账号：

```bash
tdl login -n tg1 -T qr
```

多账号批量：

```bash
bash /home/stevewu/.openclaw/workspace/skills/telegram-login-helper/scripts/login_10_namespaces.sh
```

### 3. 如果 QR 不可用，复制已有 TDLib state
如果另一台机器已经登录成功，优先复制对应 namespace 的 TDLib state，而不是反复扫码。

已知目录：

```bash
/home/stevewu/.tdl/data
```

复制后立即验证：

```bash
tdl chat ls -n <namespace> --limit 5
```

### 4. 再不行，走 MTProto / code login
这一步需要：
- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`

如果这两个没有，就别假装能闭环。

### 5. 最后才升级为人工一次性登录
如果：
- 没有可复用 namespace
- 没有可复制 session
- 没有 API credentials
- 又扫不了 QR

那就老老实实承认：**必须人工辅助一次登录**。

## 登录后怎么验活

先测 namespace：

```bash
tdl chat ls -n steve --limit 10
```

再测 personal reader/export 路线：

```bash
python3 /home/stevewu/.openclaw/workspace/skills/telegram-personal-ops/scripts/tg_personal_ops.py read_chats --limit 5
python3 /home/stevewu/.openclaw/workspace/skills/telegram-personal-ops/scripts/tg_personal_ops.py read_history --chat 777000 --limit 20
```

## 不要做的事

- 不要把 personal-account 登录问题误切到 bot tooling
- 不要明明缺 `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` 还假装 MTProto 已可用
- 不要在已有 namespace 可用时重复登录
- 不要让另一个 agent 因为扫不了二维码就误判“Telegram 读不了”

## 相关技能

- `telegram-personal-ops`：登录成功后做聊天读取与导出
- `telegram-multi-account-monitor`：多个 personal account 登录完成后做只读监控
- `telegram-reader-login-helper`：更偏向“QR 登录失败时如何救火”的窄场景版

## 一句话总结

Telegram 登录问题的正确解法是：**先复用，再转移 session，再补 fallback，最后才麻烦人类**。
