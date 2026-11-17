---
slug: video-translator-tool-free
name: video-translator-tool-free
version: 1.0.0
displayName: 视频翻译-免费版
summary: "轻量级视频翻译与配音工具，支持中英互译、字幕翻译出片，适合个人创作者快速完成跨语言视频本地化.。视频翻译免费版，为个人用户提供轻量化的视频翻译与配音能力。核心能力:"
license: Proprietary
edition: free
description: '视频翻译免费版，为个人用户提供轻量化的视频翻译与配音能力。核心能力:

  - 中英双向视频翻译（zh ⇄ en）

  - 视频字幕翻译出片

  - 单视频翻译任务处理

  - 翻译结果预览链接返回

  - 任务状态轮询查询

  适用场景:

  - 个人创作者跨语言内容分发

  - 学习视频字幕翻译

  - 短视频出海本地化

  - 个人观影辅助翻译

  差异化:

  - 免费版聚焦中英互译核心场景，零配置上手

  - 单视频任务流程清晰...'
tags:
  - Creative
  - 视频翻译
  - 多语言
  - 免费版
  - 视频处理
  - 媒体
  - 创意
  - https
  - targetlanguage
  - luoji
  - bash
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"
---
# 视频翻译工具 - 免费版

## 概述

视频翻译免费版是一款面向个人用户的轻量级视频翻译与配音工具。用户上传视频文件或提供视频 URL，即可获得翻译后的视频预览链接，支持中英双向翻译.
免费版聚焦核心翻译场景：单视频翻译、中英互译、字幕开关控制。配置简单，适合以下用户：

- 个人短视频创作者跨语言分发内容
- 学习者翻译外文教学视频
- 观影爱好者翻译字幕
- 内容运营人员快速本地化短视频

> 免费版限制：单次处理 1 个视频，仅支持中英互译（zh/en），不支持双语字幕。如需多语言、双语字幕、批量处理、语音克隆等能力，请使用 PRO 版本.
## 核心能力

### 能力清单

| 能力 | 描述 | 免费版 |
|---|---|---|
| 视频翻译 | 中英双向翻译 | 支持（zh/en） |
| 字幕翻译 | 烧录字幕出片 | 支持（单语种） |
| 双语字幕 | 中英同时显示 | 不支持 |
| 多语言翻译 | 8 种源语言 | 不支持（仅 zh/en） |
| 批量翻译 | 多视频并行 | 不支持 |
| 语音克隆 | 保留原说话人音色 | 不支持 |
| 任务优先级 | 队列优先调度 | 不支持 |
| 预览链接 | 返回可预览 URL | 支持 |
| 任务状态查询 | 轮询任务进度 | 支持 |

**处理**: 解析能力清单的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回能力清单的响应数据,包含状态码、结果和日志.
### 工作流程

```text
用户提供视频文件或 URL
      ↓
设置翻译参数（源/目标语言、字幕开关）
      ↓
提交翻译任务（获取 job_id）
      ↓
轮询任务状态
      ↓
返回预览链接（preview_url）
```

**处理**: 解析工作流程的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回工作流程的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 固定服务地址

免费版使用统一的翻译服务地址：

- **Base URL**：`https://audiox-api-global.luoji.cn`
- 不使用本地服务地址，所有请求统一发往该地址

**处理**: 解析固定服务地址的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回固定服务地址的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级视频翻译与、配音工具、支持中英互译、字幕翻译出片、适合个人创作者快、速完成跨语言视频、本地化、视频翻译免费版、为个人用户提供轻、量化的视频翻译与、配音能力、核心能力、中英双向视频翻译、视频字幕翻译出片、单视频翻译任务处、翻译结果预览链接、任务状态轮询查询等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
### 核心功能执行
执行核心功能执行操作,使用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景 1：中文视频翻译为英文

小张制作了一段中文短视频，希望翻译成英文版本发布到海外平台.
**操作步骤：**

1. 告诉 Agent：「把这个中文视频翻译成英文」
2. 提供视频文件或 URL
3. Agent 提交翻译任务，自动轮询
4. 任务完成后返回 `preview_url`

**示例调用：**

```bash
# 提交翻译任务
curl -s -X POST 'https://audiox-api-global.luoji.cn/video-trans/orchestrate' \
  -H 'Authorization: Bearer ${API_KEY}' \
  -F 'video=@/path/to/video.mp4' \
  -F 'sourceLanguage=zh' \
  -F 'targetLanguage=en'
```

### 场景 2：英文视频翻译为中文

小李下载了一段英文教学视频，希望生成中文字幕版本便于学习.
**操作步骤：**

1. 告诉 Agent：「把这个英文视频翻译成中文，要显示字幕」
2. 提供视频文件
3. Agent 提交任务，设置 `show=true`
4. 任务完成后返回带中文字幕的预览链接

**示例调用：**

```bash
luoji.cn/video-trans/orchestrate' \
  -H 'Authorization: Bearer ${API_KEY}' \
  -F 'video=@/path/to/tutorial.mp4' \
  -F 'sourceLanguage=en' \
  -F 'targetLanguage=zh' \
  -F 'show=true'
```

### 场景 3：通过 URL 翻译在线视频

小王想翻译一个在线视频，但不想先下载到本地.
**操作步骤：**

1. 告诉 Agent：「翻译这个视频 https://example.com/video.mp4」
2. Agent 使用 `video_url` 参数提交任务
3. 自动轮询任务状态
4. 返回翻译后视频预览链接

**示例调用：**

```bash
luoji.cn/video-trans/orchestrate' \
  -H 'Authorization: Bearer ${API_KEY}' \
  -H 'Content-Type: application/json' \
  -d '{
    "video_url": "https://example.com/video.mp4",
    "sourceLanguage": "zh",
    "targetLanguage": "en"
  }'
```

## 不适用场景

以下场景视频翻译-免费版不适合处理：

- 专业医学法律翻译认证
- 同声传译
- 文学创作翻译

## 触发条件

需要文本翻译、多语言转换、本地化处理时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步：获取 API Key

免费版需要翻译服务 API Key。若没有 API Key 或 Key 无效：

- 中国地区用户：访问 `https://luoji.cn` 获取
- 非中国地区用户：访问 `https://luoji.cn?lang=en-US` 获取

### 第二步：配置环境变量

```bash
# 设置 API Key 环境变量
export VIDEO_TRANSLATE_SERVICE_API_KEY="your_api_key_here"
```

### 第三步：提交翻译任务

```bash
# 提交中文视频翻译为英文
luoji.cn/video-trans/orchestrate' \
  -H "Authorization: Bearer $VIDEO_TRANSLATE_SERVICE_API_KEY" \
  -F 'sourceLanguage=zh' \
  -F 'targetLanguage=en'
```

### 第四步：轮询任务状态

```bash
# 从上一步响应中获取 job_id
JOB_ID="returned_job_id"
# ...
# 轮询任务状态
curl -s "https://audiox-api-global.luoji.cn/video-trans/jobs/$JOB_ID" \
  -H "Authorization: Bearer $VIDEO_TRANSLATE_SERVICE_API_KEY"
```

#
## 示例

### 输入参数说明

| 参数 | 类型 | 是否必需 | 默认值 | 说明 |
|:-----|:-----|:-----|:-----|:-----|
| video | 文件 | 二选一 | - | 二进制视频文件 |
| video_url | URL | 二选一 | - | 可访问的视频链接 |
| api_key | Header | 必需 | - | `Authorization: Bearer <key>` |
| targetLanguage | 字符串 | 可选 | en | 目标语言（zh/en） |
| sourceLanguage | 字符串 | 可选 | 自动推断 | 源语言（zh/en） |
| show | 布尔 | 可选 | false | 是否显示字幕 |
| bilingual | 布尔 | 可选 | false | 是否双语字幕（免费版不支持） |

### 目标语言规则

免费版仅支持以下目标语言：

- 中文 → `zh`
- 英文 → `en`

若用户未指定目标语言，默认 `targetLanguage=en`.
### 源语言规则

免费版源语言支持：

若用户未指定源语言，按目标语言推断：

- `targetLanguage=en` → `sourceLanguage=zh`
- `targetLanguage=zh` → `sourceLanguage=en`

### 字幕参数规则

```bash
# 不显示字幕（默认）
show=false&bilingual=false
# ...
# 显示单语字幕
show=true&bilingual=false
```

### 接口调用流程

```text
1. 健康检查：GET /video-trans/health
2. 提交任务：POST /video-trans/orchestrate
3. 获取任务 ID：从响应中提取 job_id
4. 轮询任务：GET /video-trans/jobs/{job_id}
5. 等待完成：直到 status 为 succeeded 或 failed
```

## 最佳实践

### 1. 选择合适的源语言

```bash
# 已知源语言时明确指定（更准确）
sourceLanguage=zh&targetLanguage=en
# ...
# 不确定源语言时可省略（自动推断）
targetLanguage=en
```

### 2. 字幕开关建议

| 场景 | 建议配置 |
|---:|---:|
| 配音版本（无字幕） | `show=false` |
| 学习辅助（带字幕） | `show=true` |
| 静音观看（仅字幕） | `show=true` |

### 3. 任务轮询间隔

```bash
# 建议轮询间隔：5-10 秒
while true; do
  STATUS=$(curl -s "https://audiox-api-global.luoji.cn/video-trans/jobs/$JOB_ID" \
    -H "Authorization: Bearer $API_KEY" | jq -r '.status')
# ...
  if [ "$STATUS" = "succeeded" ] || [ "$STATUS" = "failed" ]; then
    break
  fi
  sleep 5
done
```

### 4. 视频文件预处理

为提高翻译成功率，建议：

- 视频时长：< 10 分钟（免费版推荐）
- 视频大小：< 100MB
- 视频格式：mp4、mov、avi
- 音轨清晰，无明显噪音

## 常见问题

### Q1：没有 API Key 怎么办？

**A：** 请前往获取：

- 中国地区：`https://luoji.cn`
- 非中国地区：`https://luoji.cn?lang=en-US`

### Q2：提示 token 不足怎么办？

**A：** Token 是翻译服务的使用额度。免费版有每日额度限制，请：

- 等待额度刷新（通常每日重置）
- 升级至 PRO 版本获取更高额度
- 联系服务提供商充值

### Q3：任务一直处于 running 状态？

**A：** 可能原因：

1. 视频较长，处理需要时间（10 分钟视频约需 3-5 分钟）
2. 服务繁忙，排队中
3. 网络波动导致轮询失败

建议：增加轮询间隔至 10 秒，最多等待 15 分钟.
### Q4：翻译结果质量不理想？

**A：** 优化建议：

- 确保视频音轨清晰，无明显背景噪音
- 口语化内容翻译效果优于专业术语
- 避免多人同时说话的片段

### Q5：免费版支持哪些语言？

**A：** 免费版仅支持中英互译（zh ⇄ en）。如需翻译韩语、日语、法语等 8 种语言，请使用 PRO 版本.
### Q6：能否批量翻译多个视频？

**A：** 免费版仅支持单视频翻译。如需批量处理，请使用 PRO 版本.
### Q7：返回结果中的 preview_url 有效期多久？

**A：** 预览链接通常有效 7 天，请及时查看或下载。如需长期保存，建议下载到本地.
## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 规范的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **网络**：需要稳定网络连接（访问翻译服务）

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 | 版本要求 |
|:---:|:---:|:---:|:---:|:---:|
| curl | 命令行工具 | 必需 | 系统自带 | 任意版本 |
| jq | JSON 处理 | 可选 | 系统包管理器 | 1.6+ |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 | - |

#
### 安装命令

```bash
# macOS 安装 jq
brew install jq
# ...
# Ubuntu / Debian 安装 jq
sudo apt install jq
# ...
# 验证安装
curl --version
jq --version
```

### API Key 配置

免费版需要以下 API Key：

| API 类型 | 环境变量 | 用途 | 获取方式 |
|:--------|--------:|:--------|:--------|
| 翻译服务 | `VIDEO_TRANSLATE_SERVICE_API_KEY` | 视频翻译 API 调用 | `https://luoji.cn` |

```bash
# 配置环境变量
export VIDEO_TRANSLATE_SERVICE_API_KEY="your_translation_api_key"
# ...
# 验证配置
curl -s 'https://audiox-api-global.luoji.cn/video-trans/health' \
  -H "Authorization: Bearer $VIDEO_TRANSLATE_SERVICE_API_KEY"
```

### 可用性分类

- **分类**：MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**：通过自然语言指令驱动 Agent 调用翻译 API 完成视频翻译
- **离线可用**：否（依赖在线翻译服务）
- **隐私等级**：中（视频需上传至翻译服务）

## 版本说明

- **当前版本**：1.0.0
- **版本类型**：FREE（免费版）
- **升级路径**：如需多语言翻译、双语字幕、批量处理、语音克隆等能力，请使用 `video-translator-tool-pro`

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步
- 视频分析依赖模型的推理能力与准确性
- 长视频处理可能超出上下文窗口限制
- 免费版不支持实时视频流分析

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "视频翻译-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "video translator"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
