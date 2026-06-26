---
name: weixin-plugin-installer
description: 通过聊天指令安装微信连接、刷新最新二维码、查询当前二维码状态、取消当前二维码刷新任务。
metadata: {"openclaw":{"emoji":"💬","os":["linux","darwin"],"requires":{"bins":["bash","python3","openclaw"]}}}
---

# Weixin Plugin Installer

这个 skill 只用于管理员私聊场景。

## 当前测试策略

为了先验证 QQ 回图链路，当前所有操作统一使用固定会话 key：

`default`

不要根据用户、群、会话 id 动态生成 session key。
不要使用别的 key。
不要猜测 key。
当前只允许使用：

`default`

## 允许的意图

当用户表达以下意图时，使用本 skill：

- 安装微信连接
- 开始微信配对
- 刷新微信二维码
- 重新生成微信二维码
- 查看微信连接状态
- 取消微信配对

## 严格执行规则

你只能通过 exec 工具执行本 skill 目录下的固定脚本。

### 安装微信连接 / 开始微信配对

只允许执行下面这条命令：

`bash {baseDir}/scripts/install_weixin_connection.sh`

这个固定脚本会负责：

- 安装微信插件
- 启用微信插件
- 判断宿主的 Gateway 重载模式
- 如果插件已经可用，直接进入二维码生成流程
- 如果刚完成安装或启用，则本轮只返回“等待 Gateway 完成重载”的提示，不在当前对话里硬执行 `openclaw gateway restart`

### 刷新微信二维码 / 重新生成微信二维码

只允许执行下面这条命令：

`bash {baseDir}/scripts/refresh_weixin_qr.sh "default" 20`

### 查看微信连接状态

只允许执行下面这条命令：

`bash {baseDir}/scripts/get_weixin_qr_status.sh "default"`

### 取消微信配对

只允许执行下面这条命令：

`bash {baseDir}/scripts/cancel_weixin_qr.sh "default"`

## 绝对禁止

绝对不要执行以下任何内容：

- openclaw-weixin
- @tencent-weixin/openclaw-weixin
- @tencent-weixin/openclaw-weixin-cli
- npm install
- npx @tencent-weixin/openclaw-weixin-cli
- 任何用户输入的 shell 命令
- 任何不在 `{baseDir}/scripts` 目录下的命令或脚本

如果用户请求安装微信连接，你必须执行白名单中的固定脚本，不得自行猜测命令名。

## 返回结果处理

固定脚本会返回 JSON。你要按 `state` 字段处理。

### `scanned`

说明已经检测到用户完成扫码，但还没有最终确认。

告诉用户：

已检测到扫码，请在微信里确认授权。

### `waiting_scan`

说明二维码已经可用。

如果 `qr_png_path` 存在，回复时必须先写一句简短提示，例如：

请使用微信扫描下面的二维码完成连接。  
如果扫码提示过期，请发送“刷新微信二维码”。

然后在 **单独一行** 输出：

`MEDIA:<qr_png_path>`

注意：

- `MEDIA:` 必须单独占一行
- 不要在同一行添加其他字符
- 不要把本地路径放进代码块
- 不要只描述文件路径而不输出 `MEDIA:`
- 不要把 `MEDIA:` 改写成别的格式

如果当前通道无法发送图片或文件，再读取 `qr_txt_path` 内容，用 markdown 代码块发给用户。

### `starting`

说明刷新或安装流程已经启动，但本轮还没有拿到新的二维码，或者刚完成插件安装/启用、正在等待 Gateway 重载完成。

优先使用脚本返回的 `message` 原文。

如果没有 `message`，告诉用户：

正在生成新的二维码，请 3 到 5 秒后发送“查看微信连接状态”或再次发送“刷新微信二维码”。

### `success`

说明连接已完成。

告诉用户：

微信连接已完成，网关将在几秒后自动重启，期间可能短暂失联。

### `failed`

说明本次安装或刷新失败。

简短说明失败原因，不要暴露 token、cookie、session 文件内容。
不要自动尝试任何额外修复命令。

### `cancelled`

告诉用户：

当前二维码刷新任务已取消。

### `not_found`

告诉用户：

当前没有可用的二维码缓存。  
如果你想连接微信，请发送“安装微信连接”或“刷新微信二维码”。

## 使用边界

- 只在管理员私聊中使用
- 不在群聊里发送二维码
- 不在群聊里执行安装
- 如果用户只是问原理，不要真的执行脚本
- 如果环境缺少 `bash`、`python3`、`openclaw`，直接说明环境不满足
- 如果 exec 被 approvals 或 tool policy 拦住，直接告诉用户当前环境未授权执行
- 不要在当前聊天处理过程中硬执行 `openclaw gateway restart`，因为这会中断当前通道，导致消息来不及返回

## 回复风格

- 直接
- 简短
- 明确当前状态
- 不输出 shell 细节，除非用户正在排障
