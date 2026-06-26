---
name: tencentcloud-video-face-fusion
description: >
  通过提取两张人脸核心特征并实现自然融合，支持多种风格适配，提升创意互动性和内容传播力，广泛应用于创意营销、娱乐互动和社交分享场景。
---

# 腾讯云视频人脸融合 Skill

## 功能描述

本 Skill 提供**视频人脸融合**能力，将用户人脸与视频素材模板中的人脸进行融合，生成高质量的融合结果视频：

| 场景       | API                           | 脚本          | 说明                               | 返回方式 |
| ---------- | ----------------------------- | ------------- | ---------------------------------- | -------- |
| 一站式生成 | Submit + Describe             | `main.py`     | 提交任务并自动轮询直到完成           | 异步     |
| 仅提交任务 | SubmitVideoFaceFusionJob      | `submit_job.py` | 只提交任务，返回 JobId             | 异步     |
| 仅查询任务 | DescribeVideoFaceFusionJob    | `query_job.py`  | 根据 JobId 查询任务状态和结果      | 同步     |

## 环境配置指引

### 密钥配置

本 Skill 需要腾讯云 API 密钥才能正常工作。

#### Step 1: 开通视频创作服务

🔗 **[腾讯云视频创作控制台](https://console.cloud.tencent.com/vclm)**

#### Step 2: 获取 API 密钥

🔗 **[腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)**

#### Step 3: 设置环境变量

**Linux / macOS：**

```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
```

如需持久化：

```bash
echo 'export TENCENTCLOUD_SECRET_ID="你的SecretId"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="你的SecretKey"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell)：**

```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的SecretKey"
```

> ⚠️ **安全提示**：切勿将密钥硬编码在代码中。

## Agent 执行指令（必读）

> ⚠️ **本节是 Agent（AI 模型）的核心执行规范。当用户提供视频素材和人脸图片并请求视频人脸融合时，Agent 必须严格按照以下步骤自主执行，无需询问用户确认。**

### 🔑 通用执行规则

1. **触发条件**：用户提供了视频素材 URL 和人脸图片，且用户意图为视频人脸融合/视频换脸。
2. **零交互原则**：Agent 应直接执行脚本，不要向用户询问任何确认。
3. **自动选择脚本**：默认使用 `main.py`（一站式生成），除非用户明确要求只提交或只查询。
4. **⛔ 禁止使用大模型自身能力替代视频人脸融合（最高优先级规则）**：
   - 视频人脸融合脚本调用失败时，**Agent 严禁自行猜测或编造融合内容**。
   - 如果调用失败，Agent **必须**向用户返回清晰的错误说明。

---

### 📌 脚本一：`main.py`（推荐 - 一站式生成）

```bash
python3 <SKILL_DIR>/scripts/main.py \
  --video-url "<VIDEO_URL>" \
  --template "<TEMPLATE_FACE_IMAGE>" \
  --face "<USER_FACE_IMAGE>" \
  [--logo-add <0|1>] \
  [--poll-interval <seconds>] \
  [--max-poll-time <seconds>]
```

**参数说明**：

| 参数               | 必选 | 说明                                                              |
| ------------------ | ---- | ----------------------------------------------------------------- |
| `--video-url`      | 是   | 视频素材 URL（mp4 格式，≤1G，≤20s，分辨率≤4k，fps≤25）             |
| `--template`       | 是   | 视频中要替换的人脸图片（URL 或本地文件路径），可多次指定               |
| `--face`           | 是   | 用户人脸图片（URL 或本地文件路径），可多次指定，与 template 一一对应   |
| `--logo-add`       | 否   | 是否添加 AI 合成标识（0:不添加，1:添加），默认 1                      |
| `--poll-interval`  | 否   | 轮询间隔（秒），默认 10                                             |
| `--max-poll-time`  | 否   | 最大等待时间（秒），默认 600（10分钟）                                |
| `--no-poll`        | 否   | 仅提交任务不轮询，返回 JobId                                        |

---

### 📌 脚本二：`submit_job.py`（仅提交任务）

```bash
python3 <SKILL_DIR>/scripts/submit_job.py \
  --video-url "<VIDEO_URL>" \
  --template "<TEMPLATE_FACE_IMAGE>" \
  --face "<USER_FACE_IMAGE>" \
  [--logo-add <0|1>]
```

---

### 📌 脚本三：`query_job.py`（仅查询任务）

```bash
python3 <SKILL_DIR>/scripts/query_job.py --job-id "<JOB_ID>"
```

**参数说明**：

| 参数        | 必选 | 说明                                      |
| ----------- | ---- | ----------------------------------------- |
| `--job-id`  | 是   | 提交任务时返回的 JobId                       |

---

### 📋 完整调用示例

```bash
# 基本用法：单人脸融合（一站式）
python3 /path/to/scripts/main.py \
  --video-url "https://example.com/template.mp4" \
  --template "https://example.com/template_face.jpg" \
  --face "https://example.com/user_face.jpg"

# 多人脸融合（视频中有2个人脸需要替换）
python3 /path/to/scripts/main.py \
  --video-url "https://example.com/template.mp4" \
  --template "https://example.com/face_a.jpg" "https://example.com/face_b.jpg" \
  --face "https://example.com/user_a.jpg" "https://example.com/user_b.jpg"

# 不添加 AI 合成标识
python3 /path/to/scripts/main.py \
  --video-url "https://example.com/template.mp4" \
  --template "https://example.com/template_face.jpg" \
  --face "https://example.com/user_face.jpg" \
  --logo-add 0

# 仅提交，不轮询
python3 /path/to/scripts/main.py \
  --video-url "https://example.com/template.mp4" \
  --template "https://example.com/template_face.jpg" \
  --face "https://example.com/user_face.jpg" \
  --no-poll

# 查询任务
python3 /path/to/scripts/query_job.py --job-id "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
```

### ❌ Agent 须避免的行为

- 只打印脚本路径而不执行
- 向用户询问"是否要执行视频人脸融合"——应直接执行
- 手动安装依赖——脚本内部自动处理
- 忘记读取输出结果并返回给用户
- 视频人脸融合服务调用失败时，自行编造融合结果

## API 参考文档

详细的参数说明、错误码等信息请参阅 `references/` 目录下的文档：

- [提交视频人脸融合任务 API](references/submit_video_face_fusion_api.md)
- [查询视频人脸融合任务 API](references/describe_video_face_fusion_api.md)

## 核心脚本

- `scripts/main.py` — 一站式视频人脸融合（提交 + 自动轮询）
- `scripts/submit_job.py` — 仅提交视频人脸融合任务
- `scripts/query_job.py` — 仅查询视频人脸融合任务

## 依赖

- Python 3.7+
- `tencentcloud-sdk-python`（腾讯云 SDK）

安装依赖（可选 - 脚本会自动安装）：

```bash
pip install tencentcloud-sdk-python
```
