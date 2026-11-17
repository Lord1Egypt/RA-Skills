# weixinclaw-proactive-push

通过 WorkBuddy 已连接的 **ClawBot 微信 bot 通道**（`weixinClawBot` / ilink bot，**非微信客服号**）主动向老板微信推送 **文本 / 图片 / 文件 / 视频**。

协议严格对齐腾讯官方插件 `@tencent-weixin/openclaw-weixin@2.4.6`（`src/api` + `src/messaging` + `src/cdn`）。

> 本 skill 源码即本仓库：clone 后放入 `~/.workbuddy/skills/weixinclaw-proactive-push/` 即可使用。

## 文件说明

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 完整使用文档（通道原理、token 获取、推送、排错） |
| `send.js` | 推送主脚本：文本 / 图片 / 文件 / 视频 |

## 核心机制（2026-07-09 定稿）

| 推送类型 | `context_token` | 是否需要激活 |
|----------|------------------|--------------|
| **文本** | 默认**空串**，长期有效 | ❌ 不需要 |
| **媒体**（图片 / 文件 / 视频）| **必须**带 → 读 `claw-state/weixin/<ACCOUNT_ID>_im.bot.cursor.json` 的 `get_updates_buf`（原样，零变换） | 读不到 / 被拒才激活 |
| **任意类型被拒 `ret:-2`** | — | ✅ 都要激活（文本被拒通常是底层 bot id 轮换，同样需激活） |

- **文本免激活的原因**：空 `context_token` 对文本长期有效，因此闲置十几小时仍能推文字。
- **媒体必须带 token**：图片 / 文件 / 视频接口强制要求非空 `context_token`，从宿主刷新的 cursor 游标文件读取。
- **唯一需要激活的时刻 = 实际被拒（`ret:-2`）**：先到微信给 ClawBot 发一条任意消息激活，再重跑 `send.js` 自动读最新游标重发。

### 协议常量（官方 `@tencent-weixin/openclaw-weixin@2.4.6`）

- `Authorization: Bearer <完整 botToken，含 accountId: 前缀>`
- 6 个请求头：`Content-Type`、`AuthorizationType: ilink_bot_token`、`X-WECHAT-UIN`、`Authorization`、`iLink-App-Id: bot`、`iLink-App-ClientVersion: 132102`
- `base_info`：`{ channel_version: "2.4.6", bot_agent: "OpenClaw" }`
- 发送接口：`POST {baseUrl}/ilink/bot/sendmessage`，`baseUrl = https://ilinkai.weixin.qq.com`

### 🔴 隐私红线

- `claw-state/weixin/<ACCOUNT_ID>_im.bot.cursor.json` 内含 bot 凭证镜像，**禁止随仓库提交 / 分享**。
- 本 skill 仅**只读**本机凭据（从 `settings.json` 与本地 cursor 文件读取），不向任何文件写入密钥。
- 日志只打印 token 长度，绝不打印明文。

## 快速开始

```bash
# 0. 依赖：Node 18+（推荐 WorkBuddy managed node 22）
# 1. 确保 settings.json 已配置 weixinClawBot 通道（凭据自动读取，无需手填）

# 2. 推送文本（context_token 默认空，免激活）
node send.js "你好，老板 🦐"

# 3. 推送图片 / 文件 / 视频（自动读 cursor 游标当 context_token）
node send.js --image ./pic.png
node send.js --file  ./report.pdf
node send.js --video ./clip.mp4

# 4. 显式覆盖 context_token（一般情况不需要）
node send.js "文本" --context "<token>"
```

详见 `SKILL.md`。
