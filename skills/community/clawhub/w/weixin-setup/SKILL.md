---
name: openclaw-weixin-setup
description: "Install and connect the WeChat ClawBot (微信ClawBot) channel plugin for OpenClaw. Patches qrcode-terminal to output scannable image URLs instead of ASCII QR codes, which break in non-monospace surfaces like webchat, Discord, Feishu. Use when the user asks to set up WeChat, connect WeChat, install the WeChat plugin, scan WeChat QR code, link WeChat to OpenClaw, or says 微信ClawBot, 微信插件, 连接微信, 微信扫码. Triggers on phrases like connect WeChat, install WeChat plugin, 微信, 微信扫码登录."
---

# 微信 ClawBot 插件安装与连接

English: Install, connect, and troubleshoot the WeChat ClawBot channel plugin for OpenClaw.

## 前置条件

- OpenClaw 已安装并运行（`openclaw` CLI 可用）
- 手机上有微信账号，用于扫码
- Node.js / npm（用于 patch）

## 流程

### 第 1 步：安装插件

```bash
npx -y @tencent-weixin/openclaw-weixin-cli@latest install
```

### 第 2 步：Patch qrcode-terminal（webchat/Discord/Feishu 必需）

插件使用 `qrcode-terminal` 输出 ASCII 二维码，在等宽终端里正常，但在 webchat、Discord、Feishu 等界面里**无法扫描**。

需要 patch 为图片 URL 输出：

```bash
QR_MAIN=$(find /home/node/.openclaw/extensions/openclaw-weixin/node_modules/qrcode-terminal/lib/main.js -type f 2>/dev/null | head -1)

if [ -f "$QR_MAIN" ]; then
  sed -i '/var qrcode = new QRCode(-1, this.error);/c\
        // Patched: output image URL instead of ASCII\
        var encoded = encodeURIComponent(input);\
        var imageUrl = "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=" + encoded;\
        var output = "\\n📷 扫码链接（复制到浏览器打开或微信扫一扫）:\\n" + imageUrl + "\\n";\
        if (cb) cb(output); else console.log(output);\
        return;\n' "$QR_MAIN"
  echo "✅ 已 patch $QR_MAIN"
else
  echo "ERROR: qrcode-terminal 未找到，请先安装微信插件"
fi
```

⚠️ **重要：** 插件更新后 patch 会丢失，需要重新执行。

### 第 3 步：登录扫码

```bash
openclaw channels login --channel openclaw-weixin --verbose
```

会输出一个 QR 图片链接。在浏览器打开，用微信扫码完成连接。

### 第 4 步：验证连接

```bash
openclaw status 2>&1 | grep -i "openclaw-weixin"
```

期望输出：`openclaw-weixin │ ON │ OK`

### 第 5 步：⚠️ 修复 accountId 不匹配（常见问题）

扫码登录成功后，插件注册的 accountId 和 config 里的可能不一致，**导致收不到消息**。

排查方法：

1. 查看 config：`openclaw config get channels.openclaw-weixin`
2. 查看实际注册：`cat /home/node/.openclaw/state/openclaw-weixin/accounts.json`
3. 如果不一致，更新 config 并 reload：

```bash
# 把 NEW_ACCOUNT_ID 替换为 accounts.json 里的值
openclaw config set channels.openclaw-weixin.accountId "NEW_ACCOUNT_ID"

# Reload gateway
kill -USR1 $(pgrep -f openclaw-gateway)
```

## 添加更多微信账号

```bash
openclaw channels login --channel openclaw-weixin
```

每次扫码创建一个新账号，可同时在线多个。

## 会话隔离（可选）

按微信账号隔离会话上下文：

```bash
openclaw config set agents.mode per-channel-per-peer
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 二维码在聊天中无法扫描 | 执行 patch（第 2 步）或用真实终端 |
| 二维码过期 | 重新运行 `openclaw channels login --channel openclaw-weixin` |
| 插件未加载 | 检查 `openclaw status`，确认已启用 |
| 发消息没回复 | ⚠️ 检查 accountId 不匹配（第 5 步） |
| 连接断开 | 重新运行登录命令重新认证 |
| 插件更新后 patch 失效 | 重新执行 qrcode-terminal patch（第 2 步） |
