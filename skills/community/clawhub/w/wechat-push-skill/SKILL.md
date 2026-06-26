---
name: "wechat-push-skill"
description: "微信主动推送 — 让本地 Agent 主动推送消息到用户手机微信（绕过 24h 客服窗口限制）。当用户提到 微信主动推送、推微信消息、push 微信、给用户发微信、绕过 24h 限制、推送失败排查、推送假成功、ret=-2、errcode=-14、session timeout 时触发。涵盖：openclaw message send CLI 通道、4 个自动化 cron、bot 账号活跃度探测、5 跳链路自检、假成功/假活 6 种故障模式库。"
metadata: { "openclaw": { "emoji": "📲" } }
---

# 微信主动推送 skill

> 装上就能用：`wechat-push "消息"` → 用户手机微信收到

## 这是什么

一个让本地 Agent **主动**向用户手机微信推送消息的工程化方案。绕过微信官方的"24 小时客服窗口"限制（用户必须先发消息、Agent 才能在 24 小时内回复），实现真正的"主动告知"。

## 何时使用

### 用户表达需要
- "我想让 Agent 主动发微信"
- "微信主动推送怎么搞"
- "怎么推消息到用户微信"
- "绕过 24 小时窗口"

### 用户报告故障
- "推送失败 / 收不到"
- "脚本说 SUCCESS 但用户没收到"（假成功）
- "推消息 ret=-2 / errcode=-14"
- "session timeout"
- "换了账号还是推不出去"

## 核心原则（先记住这 3 条）

1. **必须走 OpenClaw 内部通道** `openclaw message send` —— 裸 curl ilink 在 macOS 上 99% 不通
2. **必须用活跃 bot 账号** —— 账号目录里可能有多个 `*@im.bot.json`，按 mtime 选最近的
3. **必须校验业务层响应** —— `Sent via` + `exit 0` 双条件 = 真成功；只看 HTTP 200 = 假成功

## 完整链路（5 跳）

```
① 触发层（cron / Agent / 健康检查 / 手动）
    ↓
② 推送脚本  wechat-push.py
    ↓
③ 通道选择  →  openclaw message send CLI
    ↓
④ OpenClaw 微信插件（node 进程，长连接常驻）
    ↓
⑤ ilink 服务端  →  POST /ilink/bot/sendmessage
    ↓
⑥ 用户手机微信
```

详见 `references/protocol-notes.md`。

## 装上即用

```bash
# 一键安装
bash ~/.openclaw/skills/wechat-push-skill/install.sh

# 安装过程中会：
#   1. 检查 openclaw CLI
#   2. 探测活跃 bot 账号
#   3. 引导配置 openid
#   4. 链接命令到 ~/.local/bin
#   5. 跑一次 verify 验证链路
```

## 用法（装完就能用）

```bash
# 推一条消息
wechat-push "你好"

# 推给指定 openid（临时覆盖配置）
wechat-push --to oXXXXXXXXXXXXXXXXX@im.wechat "你好"

# 静默推送（不响通知，用于探活）
wechat-push --silent "probe test"

# 预演：只打印将使用的 openid/account，不发送
wechat-push --dry-run "你好"

# 链路 5 跳自检
wechat-push-verify

# 故障排查
wechat-push-doctor
```

## 文件结构

```
wechat-push-skill/
├── SKILL.md              ← 你正在看
├── README.md             ← 公开说明（中英）
├── install.sh            ← 一键安装
├── bin/
│   ├── wechat-push       ← 主命令
│   ├── wechat-push-verify   ← 链路自检
│   └── wechat-push-doctor   ← 故障排查
├── lib/
│   ├── wechat_push.py    ← 推送核心
│   ├── ilink_probe.sh    ← 探活
│   └── (config 自动生成在 ~/.config/wechat-push/)
├── templates/
│   └── config.example    ← openid 配置模板
└── references/
    ├── protocol-notes.md ← ilink 协议关键点
    └── troubleshooting.md ← 6 种故障模式库
```

## 4 个自动化 cron（可选）

安装后可加这些 cron 自动化推送：

| cron | 频率 | 作用 |
|---|---|---|
| `wechat-monitor-5min` | 5m | 看 Mac mini 微信插件状态 |
| `ilink-probe-15min` | 15m | silent 探活，状态变 DOWN 时主动告警 |
| `daily-morning-briefing` | 0 8 * * * | 早报（C 档详细版） |
| `daily-evening-summary` | 0 21 * * * | 晚报 |

```bash
# 加探活 cron（最常用）
openclaw cron add ilink-probe-15min \
  --every "15m" --session main \
  --system-event "触发 ilink 探活，跑 wechat-push-skill 的 ilink_probe.sh"
```

## 6 种故障模式（速查表）

| 现象 | 根因 | 修法 |
|---|---|---|
| 脚本说 SUCCESS，用户没收到 | 假成功（只看 HTTP 200） | 用本 skill v2，校验 `Sent via` |
| `errcode=-14, "session timeout"` | bot session 被微信踢 | 换活跃账号 / 重新扫码 |
| `ret=-2 / HTTP 000` 裸 curl | 裸 ilink 网络层不通 | 必须走 `openclaw message send` |
| `getupdates` 有响应，`sendmessage` 推不出 | 半活状态 | plugin 内部状态不同步，重启 plugin |
| 推了 8 次后突然全失败 | bot session 静默被踢 | 等几小时自动恢复 / 重新扫码 |
| 推一次 silent 成功，推非 silent 失败 | openid 不对 | 确认 `--to` 是目标 openid |

详见 `references/troubleshooting.md`。

## 验证标准

装完跑 `wechat-push-verify`，**所有 5 跳都 ✅ OK** = 装成功。

推一条测试消息 `wechat-push "test from skill"`，**用户手机微信实际收到** = 真成功。脚本 exit 0 只能说明命令层通过，不能替代手机端确认。

## 局限

- ❌ 不支持多人 / 群发（每个用户单独 install）
- ❌ 不支持模板消息（卡片 / 图文）
- ❌ 不支持主动告警 cron（自己加）
- ❌ 不支持早报/晚报生成（自己写生成逻辑）
- ✅ 推消息（单条文本）= 唯一核心能力

## 引用

- 推送脚本核心：`lib/wechat_push.py`（~180 行）
- 探活脚本：`lib/ilink_probe.sh`
- 安装器：`install.sh`
- 公开说明：`README.md`
- 协议笔记：`references/protocol-notes.md`
- 故障库：`references/troubleshooting.md`
