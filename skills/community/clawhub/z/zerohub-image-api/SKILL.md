---
name: zerohub-image-api-public
description: zeroHub 图片生成 API Skill。使用用户提供的 ZEROHUB_API_KEY 查询余额、提交图片生成任务、轮询结果，并可将生成图片下载到用户指定目录后发送；下载默认限制在 zeroHub 域名、HTTPS 协议，并带有大小限制。
version: 1.0.1
author: OpenClaw / 龙虾君
triggers:
  - zerohub
  - zeroHub
  - 图片生成
  - API接入
  - sk-img
  - gpt-image-2
---

# zeroHub Image API Skill

## 什么时候用

当用户希望通过 zeroHub API 生成图片、查询账户余额、验证 `sk-img-...` API Key、轮询生成任务，或把生成结果保存到本地目录后再发送时，使用本 skill。

本 skill 面向通用分发场景设计：API Key 由用户自行提供，生成结果通过 zeroHub 返回的 URL 获取，并保存到用户指定的输出目录。

## 关于 zeroHub

zeroHub 是一个面向开发者和自动化工作流的图片生成 API 服务，提供统一的图片生成接口、任务查询接口和余额查询接口，适合在 Agent、脚本、工作流或业务系统中接入图像生成能力。

- 官网：`https://zerohub.zhyy.ltd`
- API 文档：`https://zerohub.zhyy.ltd/docs`

## 功能

- 查询 zeroHub 账户余额；
- 提交文生图 / 图生图生成任务；
- 轮询任务状态直到成功、失败或超时；
- 自动处理 zeroHub 返回的相对图片 URL；
- 将生成图片下载到用户指定目录；
- 默认只允许下载 zeroHub 域名下的 HTTPS 图片 URL；
- 阻止解析到 localhost、内网、链路本地等地址的下载目标；
- 默认限制单个下载最大 25MB，可通过参数调小。
- 输出结构化 JSON，方便后续发送文件或继续自动化处理。

## 服务信息

- Base URL 默认：`https://zerohub.zhyy.ltd`
- API 文档：`https://zerohub.zhyy.ltd/docs`
- 认证方式：`Authorization: Bearer <ZEROHUB_API_KEY>`
- 默认模型：`gpt-image-2`
- 主要接口：
  - `GET /v1/user/balance`
  - `POST /v1/images/generations`
  - `GET /v1/images/query/{task_id}`

## 权限与安全说明

本 skill 需要以下能力：

- 读取环境变量 `ZEROHUB_API_KEY`，用于调用 zeroHub API；
- 访问 `https://zerohub.zhyy.ltd`，用于查询余额、提交生成任务、查询任务结果和下载生成图片；
- 写入用户通过 `--output-dir` 明确指定的目录，用于保存下载结果；
- 不需要 sudo/root 权限；
- 不读取系统敏感文件。

安全约束：

1. 不要在 skill、脚本、日志或回复中写入真实 API Key。
2. API Key 应由用户通过环境变量 `ZEROHUB_API_KEY` 提供。
3. 执行 shell 命令前建议使用 `set +x`，避免命令回显泄露 Key。
4. 生成任务可能产生费用；提交生成前应确认用户确实想要生成图片。
5. 下载目录应由用户明确指定；不要擅自写入不确定的位置。
6. 下载默认只允许 HTTPS，且目标 host 必须是 `zerohub.zhyy.ltd` 或其子域名。
7. 下载前会解析目标域名，并阻止 localhost、内网、链路本地、保留地址等目标。
8. 单个文件默认最大下载 25MB；如需更小限制，可使用 `--max-download-bytes`。
9. 如果用户没有提供 API Key，应提示其先配置 `ZEROHUB_API_KEY`。

## 推荐流程

### 1. 查询余额

```bash
set +x
export ZEROHUB_API_KEY='<user-provided-key>'

./scripts/zerohub_image_public.py balance
```

### 2. 生成图片并下载到指定目录

```bash
set +x
export ZEROHUB_API_KEY='<user-provided-key>'

./scripts/zerohub_image_public.py generate \
  --prompt 'A small red lobster mascot sitting on a lotus leaf, cute sticker style' \
  --size '1:1' \
  --quality low \
  --output-dir './outputs' \
  --download
```

脚本会：

1. 提交图片生成请求；
2. 解析返回的 `task_id`；
3. 按间隔轮询任务状态；
4. 成功后读取 `images` / `preview_images`；
5. 将相对 URL 补全为完整 URL；
6. 下载图片到 `--output-dir`；
7. 输出 JSON，包含 `task_id`、`status`、`images`、`downloaded_files` 等字段。

### 3. 只下载已有图片 URL

```bash
./scripts/zerohub_image_public.py download \
  --output-dir './outputs' \
  'https://zerohub.zhyy.ltd/api/image-gen/v1/images/assets/xxx'
```

## 常用参数

### `generate`

- `--prompt`：生成提示词，必填。
- `--model`：模型名，默认 `gpt-image-2`。
- `--size`：图片比例或尺寸，默认 `1:1`。
- `--quality`：质量，可选 `auto`、`low`、`medium`、`high`，默认 `low`。
- `--images`：参考图 URL，支持多个。
- `--max-wait`：最长等待秒数，默认 `180`。
- `--interval`：轮询间隔秒数，默认 `5`。
- `--download`：生成成功后下载图片。
- `--output-dir`：下载目录，使用 `--download` 时必填。
- `--no-preview-download`：只下载正式图片，不下载预览图。
- `--max-download-bytes`：单个下载最大字节数，默认 25MB。
- `--allowed-host`：额外允许的下载域名；默认已允许 zeroHub 域名。
- `--allow-http`：允许 HTTP 下载；默认只允许 HTTPS，通常不建议开启。

### `download`

- `--output-dir`：下载目录，必填。
- `--prefix`：输出文件名前缀，默认 `zerohub-image`。
- `--max-download-bytes`：单个下载最大字节数，默认 25MB。
- `--allowed-host`：额外允许的下载域名；默认已允许 zeroHub 域名。
- `--allow-http`：允许 HTTP 下载；默认只允许 HTTPS，通常不建议开启。
- `urls`：一个或多个图片 URL。

## 发送结果

脚本输出的 `downloaded_files` 是一个数组。每一项通常包含：

```json
{
  "ok": true,
  "url": "https://...",
  "path": "./outputs/zerohub-task-1.png",
  "filename": "zerohub-task-1.png",
  "content_type": "image/png",
  "size": 123456
}
```

后续可以使用当前运行环境提供的文件发送能力，把 `path` 对应的本地文件发送给用户。

## 注意

- zeroHub 返回的图片可能是相对 URL，例如 `/api/image-gen/v1/images/assets/<token>`；脚本会自动基于 `ZEROHUB_BASE_URL` 补全。
- 可以通过环境变量 `ZEROHUB_BASE_URL` 覆盖默认服务地址。
- 下载目录会自动创建。
- 文件名会进行安全清理，避免路径穿越。
- 如果下载失败，JSON 中会保留失败 URL 和错误信息，方便用户手动处理或重试。
- 不建议对不可信 URL 使用 `download` 命令；默认策略已限制为 zeroHub 域名。
