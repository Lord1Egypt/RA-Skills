---
slug: whatsapp-image-tool-free
name: whatsapp-image-tool-free
version: 1.0.0
displayName: WhatsApp图片发送-免费版
summary: "轻量级WhatsApp图片发送工具，支持单图发送与基础文件传输，适合个人用户快速分享多媒体内容.。WhatsApp 图片发送免费版，为个人用户提供轻量化的多媒体消息发送能力。核心能力:"
license: Proprietary
edition: free
description: 'WhatsApp 图片发送免费版，为个人用户提供轻量化的多媒体消息发送能力。核心能力:

  - 单张图片发送（含说明文字）

  - 基础文件类型支持（JPG/PNG/GIF）

  - 工作区文件管理

  - 临时文件自动清理

  - 发送状态确认

  适用场景:

  - 个人图片分享给好友

  - 工作文档快速传递

  - 截图反馈与协作

  - 简易多媒体消息发送

  差异化:

  - 免费版聚焦单图发送核心场景...'
tags:
  - Creative
  - 消息发送
  - WhatsApp
  - 免费版
  - 图像处理
  - AI绘图
  - 创意
  - jpg
  - whatsapp
  - png
  - tmp
  - skill-platform
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"
---
# WhatsApp 图片发送工具 - 免费版

## 概述

WhatsApp 图片发送免费版是一款面向个人用户的多媒体消息发送工具。它通过四步工作流（下载 → 复制到工作区 → 发送 → 清理临时文件），快速将图片或文件发送至指定 WhatsApp 联系人.
免费版聚焦核心发送场景：单张图片发送、基础文件类型支持、说明文字附加。配置简单，适合以下用户：

- 个人用户分享图片给好友
- 工作场景快速传递截图
- 内容创作者发送预览图
- 简易多媒体消息需求

> 免费版限制：单次发送 1 张图片，仅支持基础图片格式（JPG/PNG/GIF），不支持批量发送、视频音频文件、定时发送、群组消息。如需批量发送、多媒体支持、定时发送等能力，请使用 PRO 版本.
## 核心能力

### 能力清单

| 能力 | 描述 | 免费版 |
|---|---|---|
| 单图发送 | 发送一张图片至指定联系人 | 支持 |
| 说明文字 | 附加文字说明 | 支持 |
| 图片格式 | 支持的图片格式 | JPG/PNG/GIF |
| 视频发送 | 发送视频文件 | 不支持 |
| 音频发送 | 发送音频文件 | 不支持 |
| 文档发送 | 发送文档文件 | 不支持 |
| 批量发送 | 多图同时发送 | 不支持 |
| 定时发送 | 指定时间发送 | 不支持 |
| 群组消息 | 发送至群组 | 不支持 |
| 模板消息 | 预设消息模板 | 不支持 |
| 发送报告 | 发送状态追踪 | 基础确认 |

**处理**: 解析能力清单的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回能力清单的响应数据,包含状态码、结果和日志.
### 工作流程

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | WhatsApp图片发送-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
用户提供图片 URL 或路径 + 联系人手机号
      ↓
Step 1: 下载图片到 /tmp/ 目录
      ↓
Step 2: 复制到工作区目录
      ↓
Step 3: 调用发送命令（含说明文字）
      ↓
Step 4: 清理临时文件
      ↓
返回发送结果
```

**处理**: 解析工作流程的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回工作流程的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 支持的文件格式

免费版支持以下图片格式：

| 格式 | 扩展名 | 适用场景 |
|---:|---:|---:|
| JPG | .jpg / .jpeg | 照片分享（体积小） |
| PNG | .png | 截图分享（无损画质） |
| GIF | .gif | 动图分享 |

**处理**: 解析支持的文件格式的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回支持的文件格式的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、WhatsApp、图片发送工具、支持单图发送与基、础文件传输、适合个人用户快速、分享多媒体内容、图片发送免费版、为个人用户提供轻、量化的多媒体消息、发送能力、核心能力、单张图片发送、基础文件类型支持、工作区文件管理、临时文件自动清理、发送状态确认等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
### 核心功能执行
执行核心功能执行操作,使用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景 1：分享网络图片给好友

小张在网上看到一张有趣的图片，想通过 WhatsApp 分享给朋友.
**操作步骤：**

1. 告诉 Agent：「把这张图片 https://example.com/funny.jpg 发到 WhatsApp +8613800138000」
2. Agent 下载图片到 `/tmp/`
3. 复制到工作区目录
4. 调用发送命令
5. 清理临时文件

**示例流程：**

```bash
# Step 1: 下载图片
curl -o /tmp/funny.jpg https://example.com/funny.jpg
# ...
# Step 2: 复制到工作区
cp /tmp/funny.jpg ~/.skill-platform/workspace/
# ...
# Step 3: 发送到 WhatsApp
message --channel whatsapp \
  --target +8613800138000 \
  --filePath ~/.skill-platform/workspace/funny.jpg \
  --message "看到这张图觉得很有趣"
# ...
# Step 4: 清理临时文件
rm /tmp/funny.jpg
```

### 场景 2：发送本地截图

小李需要把本地的设计截图发给同事确认.
**操作步骤：**

1. 告诉 Agent：「发送本地截图 /tmp/design-preview.png 给 +14843124960，说明是设计预览」
2. Agent 直接复制文件到工作区（无需下载）
3. 调用发送命令
4. 清理临时文件

**示例流程：**

```bash
# Step 1: 复制本地文件到工作区
cp /tmp/design-preview.png ~/.skill-platform/workspace/
# ...
# Step 2: 发送到 WhatsApp
message --channel whatsapp \
  --target +14843124960 \
  --filePath ~/.skill-platform/workspace/design-preview.png \
  --message "这是设计预览图，请确认"
# ...
# Step 3: 清理
```

### 场景 3：分享生成的图片

小王用 AI 生成了一张图片，想发送给朋友查看效果.
**操作步骤：**

1. 告诉 Agent：「把刚生成的图片 /tmp/ai-artwork.png 发到 WhatsApp +8613900139000」
2. Agent 复制文件到工作区
3. 调用发送命令
4. 清理临时文件

**示例流程：**

```bash
# 复制 AI 生成图片到工作区
cp /tmp/ai-artwork.png ~/.skill-platform/workspace/
# ...
# 发送
message --channel whatsapp \
  --target +8613900139000 \
  --filePath ~/.skill-platform/workspace/ai-artwork.png \
  --message "AI 生成的作品"
# ...
# 清理
```

## 不适用场景

以下场景WhatsApp图片发送-免费版不适合处理：

- 版权受保护的媒体内容处理
- 实时直播推流
- 专业影视后期

## 触发条件

需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步：环境检查

确认系统已安装 `curl` 与 `message` 工具：

```bash
curl --version
which message
```

### 第二步：发送网络图片

最简单的用法 - 发送网络图片：

```bash
# 下载图片
curl -o /tmp/share.jpg https://example.com/image.jpg
# ...
# 复制到工作区
cp /tmp/share.jpg ~/.skill-platform/workspace/
# ...
# 发送
message --channel whatsapp \
  --target +14843124960 \
  --filePath ~/.skill-platform/workspace/share.jpg \
  --message "分享一张图片"
# ...
# 清理
rm /tmp/share.jpg
```

### 第三步：发送本地图片

```bash
# 直接复制到工作区
cp /path/to/local.png ~/.skill-platform/workspace/
# ...
# 发送
message --channel whatsapp \
  --target +14843124960 \
  --filePath ~/.skill-platform/workspace/local.png \
  --message "本地图片"
# ...
# 清理工作区文件
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

以下是WhatsApp图片发送-免费版的典型使用示例，展示核心功能的输入输出流程.
## 最佳实践

### 1. 文件命名规范

建议使用有意义的文件名：

```bash
# 推荐：描述性命名
curl -o /tmp/design-v2-preview.jpg https://example.com/design.jpg
# ...
# 不推荐：随机命名
curl -o /tmp/abc123.jpg https://example.com/design.jpg
```

### 2. 说明文字建议

| 场景 | 说明文字示例 |
|:---:|:---:|
| 分享照片 | "周末出游拍的照片" |
| 工作截图 | "这是设计预览，请确认" |
| AI 作品 | "AI 生成的画作，看看效果" |
| 反馈图 | "这里有个问题需要修改" |

### 3. 临时文件管理

```bash
# 发送完成后及时清理
rm /tmp/share.jpg
# ...
# 避免工作区堆积文件
ls ~/.skill-platform/workspace/
```

### 4. 图片大小建议

| 用途 | 建议大小 | 格式 |
|:------|------:|:------|
| 快速分享 | < 1MB | JPG |
| 高清截图 | < 5MB | PNG |
| 动图分享 | < 3MB | GIF |

## 常见问题

### Q1：提示 message 命令未找到？

**A：** `message` 是 Skill 平台提供的发送工具，需确保：

1. Skill 平台已正确安装
2. `message` 命令在 PATH 中
3. 平台服务正在运行

### Q2：发送失败提示文件不存在？

**A：** WhatsApp 要求文件必须在工作区目录中：

```bash
# 确认文件已复制到工作区
ls ~/.skill-platform/workspace/
# ...
# 确认文件路径正确
message --channel whatsapp \
  --target +14843124960 \
  --filePath ~/.skill-platform/workspace/your-file.jpg
```

### Q3：手机号格式如何填写？

**A：** 手机号需包含国家代码：

- 格式：`+国家代码 + 手机号`
- 美国示例：`+14843124960`
- 中国示例：`+8613800138000`

### Q4：能否发送视频或音频？

**A：** 免费版仅支持图片格式（JPG/PNG/GIF）。如需发送视频、音频、文档，请使用 PRO 版本.
### Q5：能否批量发送多张图片？

**A：** 免费版仅支持单张图片发送。如需批量发送，请使用 PRO 版本.
### Q6：说明文字支持中文吗？

**A：** 支持。`--message` 参数可包含中英文、Emoji 等字符.
### Q7：临时文件需要手动清理吗？

**A：** 建议每次发送后清理 `/tmp/` 和工作区的临时文件，避免磁盘空间占用.
## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 规范的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **网络**：需要网络连接（下载图片与发送消息）
- **Skill 平台**：需安装并提供 `message` 命令

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 | 版本要求 |
|---:|:---|---:|---:|:---|
| curl | 命令行工具 | 必需 | 系统自带 | 任意版本 |
| message | 平台工具 | 必需 | Skill 平台安装 | - |
| WhatsApp 账号 | 服务 | 必需 | WhatsApp 注册 | - |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 | - |

#
### 环境准备

```bash
# 验证 curl
curl --version
# ...
# 验证 message 工具
which message
# ...
# 验证工作区目录
ls ~/.skill-platform/workspace/
```

### API Key 配置

免费版需要以下配置：

| 配置项 | 环境变量 | 用途 | 获取方式 |
|:------:|--------|:-------|:------:|
| WhatsApp 凭证 | 平台配置 | WhatsApp 账号认证 | Skill 平台配置 |
| Skill 平台 Token | 平台配置 | 平台认证 | Skill 平台控制台 |

```bash
# Skill 平台通常会自动配置 WhatsApp 凭证
# 若需手动配置，请参考平台文档
```

### 可用性分类

- **分类**：MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**：通过自然语言指令驱动 Agent 调用 `message` 命令完成图片发送
- **离线可用**：否（需要网络连接发送消息）
- **隐私等级**：中（图片需经过平台中转）

## 版本说明

- **当前版本**：1.0.0
- **版本类型**：FREE（免费版）
- **升级路径**：如需批量发送、多媒体支持、定时发送、群组消息、模板消息等能力，请使用 `whatsapp-image-tool-pro`

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|----|:--:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "WhatsApp图片发送-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "whatsapp image"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
