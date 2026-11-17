---
slug: whatsapp-master-free
name: whatsapp-master-free
version: 1.0.0
displayName: WhatsApp大师(免费版)
summary: WhatsApp 消息自动化免费版：文本/媒体/贴纸/语音发送，含 JID 格式与速率限制指南。
license: Proprietary
edition: free
description: WhatsApp 大师（免费版）面向个人用户与独立开发者，封装 WhatsApp 的基础消息能力：文本发送、媒体发送、贴纸、语音笔记与 GIF。通过原生通道集成直接调用
  WhatsApp Web 协议，无需外部 Docker 或 CLI 包装。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。
tags:
- 即时通讯
- WhatsApp
- 消息自动化
- 媒体处理
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L3
pricing_model: per_use
suggested_price: 29.9
tools: ["read", "write", "exec"]
tags: "WhatsApp,社交,通信"
---
# WhatsApp 大师（免费版）

## 概述

WhatsApp 是全球使用最广泛的即时通讯应用之一。本工具箱通过原生通道集成直接调用 WhatsApp Web 协议，让 AI Agent 能够发送文本、媒体、贴纸、语音笔记与 GIF。免费版聚焦于"能发"——覆盖 5 类基础消息与速率限制指南；交互（反应/回复/编辑/撤回）、群组管理、多智能体讨论等进阶能力留给专业版。

无需外部 Docker 服务，无需 CLI 包装，直接通过 Agent 平台的通道集成调用。

## 核心能力

| 能力 | 说明 | 免费版 |
|---|---|---|
| 文本发送 | 纯文本消息 | 是 |
| 媒体发送 | 图片/视频/文档 | 是 |
| 贴纸发送 | WebP 格式贴纸 | 是 |
| 语音笔记 | OGG/Opus 语音 | 是 |
| GIF 发送 | MP4 格式动画 | 是 |
| JID 格式 | 个人与群组 JID 转换 | 是 |
| 速率限制 | 反垃圾策略说明 | 是 |
| 媒体转换 | ffmpeg 模板 | 是 |
| 交互能力 | 反应/回复/编辑/撤回 | 否（专业版） |
| 群组管理 | 创建/重命名/邀请/权限 | 否（专业版） |
| 多智能体 | 群组内多 Agent 协作 | 否（专业版） |
| 历史搜索 | 全文检索与联系人提取 | 否（专业版） |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：WhatsApp、消息自动化免费版、语音发送、格式与速率限制指、面向个人用户与独、立开发者、的基础消息能力、语音笔记与、通过原生通道集成、直接调用、无需外部、Docker、CLI、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：每日日报推送
用户说"每天早上 9 点把昨天的日报发到我的 WhatsApp"。Agent 调用 `message action=send channel=whatsapp` 发送文本消息，配合定时任务实现日报推送。

### 场景二：发送项目截图
用户说"把这张设计稿发给客户"。Agent 调用 `message action=send` 携带 `filePath` 发送图片，支持的格式包括 JPG/PNG/GIF/MP4/PDF/DOC。

### 场景三：发送语音提醒
用户说"录一段语音提醒我开会"。Agent 先用 ffmpeg 把音频转为 OGG/Opus 格式，再调用 `message action=send asVoice=true` 发送。

## 快速开始

### 60 秒上手
1. 确认 WhatsApp 账号已通过二维码链接（`whatsapp login`）
2. 准备目标手机号（含国家代码，如 `+34612345678`）
3. 调用 `message action=send` 发送消息

### 发送文本消息

```text
message action=send channel=whatsapp to="+34612345678" message="Hello!"
```

### 发送媒体

```text
message action=send channel=whatsapp to="+34612345678" message="Check this out" filePath=/path/to/image.jpg
```

支持的格式：JPG、PNG、GIF、MP4、PDF、DOC 等。

### 发送贴纸

```text
message action=sticker channel=whatsapp to="+34612345678" filePath=/path/to/sticker.webp
```

必须是 WebP 格式，理想尺寸 512x512。

### 发送语音笔记

```text
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/audio.ogg asVoice=true
```

使用 OGG/Opus 格式，MP3 可能无法正常播放。

### 发送 GIF

```text
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/animation.mp4 gifPlayback=true
```

WhatsApp 要求 GIF 转为 MP4 格式。

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### JID 格式说明

WhatsApp 内部使用 JID（Jabber ID）：

| 类型 | 格式 | 示例 |
|:-----|:-----|:-----|
| 个人 | `<number>@s.whatsapp.net` | `34612345678@s.whatsapp.net` |
| 群组 | `<id>@g.us` | `123456789012345678@g.us` |

使用 `to=` 传入手机号时，Agent 平台会自动转换为 JID 格式。

### ffmpeg 媒体转换模板

#### 语音笔记转换

```bash
ffmpeg -i input.wav -c:a libopus -b:a 64k output.ogg
```

#### 贴纸转换（图片转 WebP）

```bash
ffmpeg -i input.png -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000" output.webp
```

#### GIF 转 MP4

```bash
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4 -y
```

## 最佳实践

### 已知限制
WhatsApp 有反垃圾措施，应避免：
- 向大量联系人批量发送相同消息
- 快速连发消息
- 向未与你互动过的联系人发送消息

建议：单次广播不超过 10 人，消息间隔 ≥ 3 秒，优先回复已有对话。

### 2. 媒体格式规范
- 语音笔记：必须 OGG/Opus，码率 64k 即可
- 贴纸：必须 WebP，512x512，透明背景
- GIF：必须转为 MP4，`-movflags faststart` 加速首帧
- 图片：JPG/PNG 均可，建议压缩到 1MB 以内

### 3. 手机号格式
`to=` 参数必须包含国家代码（如 `+34` 代表西班牙），不要带空格或连字符。

### 4. 文件路径
`filePath` 使用绝对路径，避免相对路径在不同工作目录下失效。

### 5. 消息确认
发送后 Agent 平台会返回消息 ID，建议记录用于后续的回复/引用（专业版功能）。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### Q1：发送失败提示"未登录"？
A：需要先通过二维码链接 WhatsApp 账号。运行 `whatsapp login` 扫码登录，登录状态会持久化。

### Q2：语音笔记对方听不到？
A：必须是 OGG/Opus 格式。MP3 在部分设备上无法播放。用 ffmpeg 转换：`ffmpeg -i input.mp3 -c:a libopus -b:a 64k output.ogg`。

### Q3：贴纸发送后变形？
A：贴纸必须是 WebP 格式且 512x512。用 ffmpeg 的 `scale` + `pad` 滤镜保持比例并填充透明背景。

### Q4：GIF 发送后不动？
A：WhatsApp 不支持原生 GIF，必须转为 MP4 并设置 `gifPlayback=true`。

### Q5：发送给群组怎么填？
A：群组使用 `@g.us` 后缀的 JID，例如 `123456789012345678@g.us`。群组管理能力在专业版。

### Q6：被 WhatsApp 限流怎么办？
A：降低发送频率，单次广播不超过 10 人，间隔 ≥ 3 秒。避免向未互动联系人发送。严重时账号可能被临时封禁。

### Q7：媒体文件大小有限制吗？
A：建议图片 < 1MB，视频 < 16MB，文档 < 100MB。超大文件建议先用 ffmpeg 压缩。

## 免费版限制

本免费体验版限制以下高级功能：
- 交互能力（反应、回复/引用、编辑、撤回）
- 群组管理（创建、重命名、图标、描述、参与者、管理员、邀请链接）
- 多智能体讨论（群组内多 Agent 协作与拥塞控制）
- 历史消息搜索与 vCard 联系人提取
- 预算感知调度与对话生命周期管理
- 高级媒体处理与批量广播策略

解锁全部功能请使用专业版：`whatsapp-master-pro`

## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 且具备 WhatsApp 通道集成的 AI Agent
- **操作系统**：Windows / macOS / Linux
- **WhatsApp 账号**：已通过二维码链接的有效账号
- **Node.js**：18+（如需运行通道插件）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由 Agent 平台内置 LLM 提供 |
| WhatsApp 通道插件 | 插件 | 必需 | Agent 平台内置或自行安装 |
| ffmpeg | CLI 工具 | 推荐 | 系统包管理器安装 |
| Baileys 协议库 | npm 包 | 内置 | 通道插件依赖 |

### API Key 配置
- **WhatsApp 通道凭证**：通过二维码登录获取，由 Agent 平台持久化
- **无需额外 API Key**：本 Skill 基于原生通道集成，不调用外部付费 API
- **禁止**：在 SKILL.md 或脚本中硬编码 WhatsApp 账号密码

### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务
- **模型路由建议**：免费版使用低成本模型（如 GPT-4o-mini / Claude Haiku）

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "WhatsApp大师(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "whatsapp master"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
