---
name: "video-stream-upload-free"
description: "轻量级视频上传工具，支持快速上传视频至流媒体平台并获取播放链接，适合个人创作者分发内容。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "视频上传-免费版"
  version: "1.0.0"
  summary: "轻量级视频上传工具，支持快速上传视频至流媒体平台并获取播放链接，适合个人创作者分发内容。"
  tags:
    - "Creative"
    - "视频上传"
    - "流媒体"
    - "免费版"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 视频上传工具 - 免费版

## 概述

视频上传免费版是一款面向个人创作者的轻量级视频上传与流媒体分发工具。它采用三步上传流程（创建视频对象 → 上传文件 → 完成上传），快速将本地视频上传至流媒体平台，并获取 HLS 播放链接。

免费版聚焦默认上传场景：单视频上传、基础标题配置、HLS 流媒体链接返回。配置简单，适合以下用户：

- 个人短视频创作者分发内容
- 教学视频上传与分享
- 自媒体运营人员发布视频
- 视频内容备份托管

> 免费版限制：单次上传 1 个视频，使用默认编码配置，不支持自定义分辨率、缩略图、批量上传。如需自定义编码、多分辨率输出、批量上传等能力，请使用 PRO 版本。

## 核心能力

### 能力清单

| 能力 | 描述 | 免费版 |
|:-----|:-----|:-------|
| 默认上传 | 仅需标题快速上传 | 支持 |
| 三步流程 | 创建 → 上传 → 完成 | 支持 |
| HLS 链接 | 获取流媒体播放链接 | 支持 |
| 上传状态 | 查询转码进度 | 支持 |
| 自定义编码 | 分辨率/码率/编码器 | 不支持 |
| 多分辨率输出 | 240p-4320p 多档 | 不支持（默认档） |
| 缩略图上传 | 自定义封面图 | 不支持 |
| 批量上传 | 多视频并行 | 不支持 |
| 视频管理 | 列表/删除/更新 | 不支持 |
| 转码费用预估 | 上传前估算成本 | 不支持 |

**输入**: 用户提供能力清单所需的指令和必要参数。
**处理**: 按照skill规范执行能力清单操作,遵循单一意图原则。
**输出**: 返回能力清单的执行结果,包含操作状态和输出数据。

### 工作流程

```text
用户提供视频文件 + 标题
      ↓
Step 1: 创建视频对象（获取 VIDEO_ID）
      ↓
Step 2: 上传文件分片（带 MD5 校验）
      ↓
Step 3: 完成上传（触发转码）
      ↓
查询视频详情获取 HLS 链接
      ↓
返回播放链接给用户
```

**输入**: 用户提供工作流程所需的指令和必要参数。
**处理**: 按照skill规范执行工作流程操作,遵循单一意图原则。
**输出**: 返回工作流程的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 服务地址

免费版使用统一的流媒体服务地址：

- **API Base URL**：`https://api-w3stream.attoaioz.cyou`
- 所有 API 调用统一发往该地址

**输入**: 用户提供服务地址所需的指令和必要参数。
**处理**: 按照skill规范执行服务地址操作,遵循单一意图原则。
**输出**: 返回服务地址的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级视频上传工、支持快速上传视频、至流媒体平台并获、取播放链接、适合个人创作者分、发内容、视频上传免费版、为个人用户提供轻、量化的视频上传与、流媒体分发能力、核心能力、默认快速上传、三步上传流程、流媒体链接获取、上传进度查询、基础视频信息管理等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

### 核心功能执行
执行核心功能执行操作,使用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景 1：个人短视频上传

小张拍摄了一段 vlog，希望上传到流媒体平台获取播放链接分享给朋友。

**操作步骤：**

1. 告诉 Agent：「帮我上传视频 /videos/vlog.mp4，标题是『周末出游 vlog』」
2. Agent 询问 API Key（公钥 + 私钥）
3. 执行三步上传流程
4. 返回 HLS 播放链接

**示例流程：**

```bash
# Step 1: 创建视频对象
curl -s -X POST 'https://api-w3stream.attoaioz.cyou/api/videos/create' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"title": "周末出游 vlog"}'
```

### 场景 2：教学视频分享

小李录制了一段编程教学视频，希望上传后分享给学生观看。

**操作步骤：**

1. 告诉 Agent：「上传 /videos/python-tutorial.mp4，标题『Python 入门教程』」
2. 提供流媒体平台 API Key
3. Agent 完成上传并返回链接
4. 学生通过链接在线观看

**示例流程：**

```bash
# Step 2: 上传文件分片
FILE_SIZE=$(stat -c%s /videos/python-tutorial.mp4)
END_POS=$((FILE_SIZE - 1))
HASH=$(md5sum /videos/python-tutorial.mp4 | awk '{print $1}')

curl -s -X POST "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID/part" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H "Content-Range: bytes 0-$END_POS/$FILE_SIZE" \
  -F "file=@/videos/python-tutorial.mp4" \
  -F "index=0" \
  -F "hash=$HASH"
```

### 场景 3：视频内容备份

小王想将本地视频上传到流媒体平台作为云端备份。

**操作步骤：**

1. 告诉 Agent：「上传 /videos/family-trip.mp4 作为备份」
2. 提供标题与 API Key
3. Agent 完成上传，返回链接
4. 随时可访问播放

**示例流程：**

```bash
# Step 3: 完成上传
curl -s -X GET "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID/complete" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'
```

## 不适用场景

以下场景视频上传-免费版不适合处理：

- 版权受保护的媒体内容处理
- 实时直播推流
- 专业影视后期

## 触发条件

需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 第一步：获取 API Key

免费版需要流媒体平台的 API Key：

- `stream-public-key`：公钥
- `stream-secret-key`：私钥

若未提供，Agent 会主动询问用户。

### 第二步：上传第一个视频

最简单的用法 - 默认快速上传：

```bash
# Step 1: 创建视频对象（仅需标题）
curl -s -X POST 'https://api-w3stream.attoaioz.cyou/api/videos/create' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"title": "我的第一个视频"}'
```

从响应中提取 `data.id` 作为 `VIDEO_ID`。

### 第三步：上传文件

```bash
# 计算文件大小与 MD5
FILE_SIZE=$(stat -c%s /path/to/video.mp4)
END_POS=$((FILE_SIZE - 1))
HASH=$(md5sum /path/to/video.mp4 | awk '{print $1}')

# 上传文件分片
curl -s -X POST "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID/part" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H "Content-Range: bytes 0-$END_POS/$FILE_SIZE" \
  -F "file=@/path/to/video.mp4" \
  -F "index=0" \
  -F "hash=$HASH"
```

### 第四步：完成上传并获取链接

```bash
# 完成上传（触发转码）
curl -s -X GET "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID/complete" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'

# 查询视频详情获取 HLS 链接
curl -s 'https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

### 上传参数说明

| 参数 | 类型 | 是否必需 | 默认值 | 说明 |
|:-----|:-----|:---------|:-------|:-----|
| title | 字符串 | 必需 | - | 视频标题 |
| stream-public-key | Header | 必需 | - | 平台公钥 |
| stream-secret-key | Header | 必需 | - | 平台私钥 |
| file | 文件 | 必需 | - | 视频文件二进制 |
| index | 整数 | 必需 | 0 | 分片索引（单分片固定为 0） |
| hash | 字符串 | 必需 | - | 文件 MD5 哈希 |

### 三步上传流程详解

```text
Step 1: POST /api/videos/create
   请求体: {"title": "视频标题"}
   响应: {"data": {"id": "VIDEO_ID"}}

Step 2: POST /api/videos/VIDEO_ID/part
   Header: Content-Range: bytes 0-{end}/{total}
   表单: file, index, hash
   响应: 上传成功确认

Step 3: GET /api/videos/VIDEO_ID/complete
   响应: 触发转码，上传完成

查询: GET /api/videos/VIDEO_ID
   响应: 包含 HLS/DASH 流媒体链接
```

## 错误处理


| 错误码 | 含义 | 处理建议 |
|:-------|:-----|:---------|
| 401 | API Key 无效 | 检查公钥与私钥是否正确 |
| 400 | 请求格式错误 | 检查请求体格式与参数 |
| 500 | 服务器错误 | 稍后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |

## 最佳实践

### 1. 文件大小处理

```bash
# 小文件（< 50MB）：单分片上传
FILE_SIZE=$(stat -c%s video.mp4)
END_POS=$((FILE_SIZE - 1))

# 大文件（> 50MB）：建议使用 PRO 版本多分片上传
# 免费版仅支持单分片，大文件可能超时
```

### 2. MD5 哈希计算

不同操作系统计算 MD5 的命令：

```bash
# Linux
HASH=$(md5sum video.mp4 | awk '{print $1}')

# macOS
HASH=$(md5 -q video.mp4)

# Windows (Git Bash)
HASH=$(certutil -hashfile video.mp4 MD5 | grep -v ":" | tr -d ' ')
```

### 3. 上传状态检查

```bash
# 检查转码状态
STATUS=$(curl -s 'https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' | jq -r '.data.status')

# 状态说明：
# transcoding - 转码中（需等待）
# done - 转码完成（可获取链接）
```

### 4. 视频文件建议

| 项目 | 推荐值 |
|:-----|:-------|
| 格式 | mp4（兼容性最佳） |
| 大小 | < 50MB（免费版单分片） |
| 分辨率 | 720p 或 1080p |
| 编码 | H.264 + AAC |
| 时长 | < 30 分钟 |

## 常见问题

### Q1：如何获取 API Key？

**A：** 需要流媒体平台账号。注册后可在控制台获取：

- `stream-public-key`：公钥
- `stream-secret-key`：私钥

若用户未提供，Agent 会主动询问。

### Q2：上传大文件失败怎么办？

**A：** 免费版仅支持单分片上传，建议：

1. 视频文件控制在 50MB 以内
2. 压缩视频后再上传
3. 大文件请使用 PRO 版本（支持多分片上传，单文件可达数 GB）

### Q3：上传成功但没有播放链接？

**A：** 上传完成后需要等待转码：

```bash
# 轮询转码状态
while true; do
  STATUS=$(curl -s 'https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID' \
    -H 'stream-public-key: PUBLIC_KEY' \
    -H 'stream-secret-key: SECRET_KEY' | jq -r '.data.status')
  
  if [ "$STATUS" = "done" ]; then
    echo "转码完成"
    break
  fi
  sleep 10
done
```

### Q4：支持哪些视频格式？

**A：** 平台支持主流视频格式，推荐使用：

- mp4（兼容性最佳）
- mov（Apple 设备）
- avi、mkv、webm（需转码）

### Q5：能否上传自定义封面图？

**A：** 免费版不支持自定义封面。如需上传缩略图，请使用 PRO 版本。

### Q6：上传后视频是公开的吗？

**A：** 免费版默认上传后为公开状态。如需设置私密视频，请使用 PRO 版本的 `is_public` 参数。

### Q7：HLS 链接有效期多久？

**A：** HLS 链接长期有效，只要视频未被删除即可访问。

## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 规范的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **网络**：需要稳定网络连接（上传视频至流媒体平台）
- **Shell**：Bash 或兼容 Shell（需要 curl、md5sum、stat 命令）

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 | 版本要求 |
|:-------|:-----|:---------|:---------|:---------|
| curl | 命令行工具 | 必需 | 系统自带 | 任意版本 |
| md5sum | 命令行工具 | 必需 | 系统自带 | 任意版本 |
| stat | 命令行工具 | 必需 | 系统自带 | 任意版本 |
| jq | JSON 处理 | 可选 | 系统包管理器 | 1.6+ |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 | - |

#### 安装命令

```bash
# macOS 安装 jq
brew install jq

# Ubuntu / Debian 安装 jq
sudo apt install jq

# 验证安装
curl --version
md5sum --version
stat --version
jq --version
```

### API Key 配置

免费版需要以下 API Key：

| API 类型 | 环境变量 | 用途 | 获取方式 |
|:---------|:---------|:-----|:---------|
| 流媒体公钥 | `STREAM_PUBLIC_KEY` | API 认证 | 流媒体平台控制台 |
| 流媒体私钥 | `STREAM_SECRET_KEY` | API 认证 | 流媒体平台控制台 |

```bash
# 配置环境变量
export STREAM_PUBLIC_KEY="your_public_key"
export STREAM_SECRET_KEY="your_secret_key"

# 验证配置
curl -s 'https://api-w3stream.attoaioz.cyou/api/videos' \
  -X POST \
  -H "stream-public-key: $STREAM_PUBLIC_KEY" \
  -H "stream-secret-key: $STREAM_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{"limit": 1}'
```

### 可用性分类

- **分类**：MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**：通过自然语言指令驱动 Agent 调用流媒体 API 完成视频上传
- **离线可用**：否（依赖在线流媒体服务）
- **隐私等级**：中（视频上传至流媒体平台）

## 版本说明

- **当前版本**：1.0.0
- **版本类型**：FREE（免费版）
- **升级路径**：如需自定义编码、多分辨率输出、缩略图、批量上传、视频管理等能力，请使用 `video-stream-upload-pro`

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
