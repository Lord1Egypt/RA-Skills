---
name: tencentcloud-aigc-recog-video
description: 腾讯云 AI 生成视频识别 (TencentCloud Video AIGC Detection) 技能。适用于 AI 生成视频检测、视频真伪鉴别、AI 合成视频检测、Deepfake 视频检测等场景。TencentCloud Video AIGC Detection is an AI-generated content detection service by Tencent Cloud, supporting aigc detection, AI-generated video identification, and video authenticity review.
---

# 腾讯云 AI 生成视频识别 Skill

## 功能描述

本技能用于识别视频是否为 AI 工具生成，覆盖 Veo3、Hunyuan、Jimeng、Hailuo等数十种主流模型生成的视频。

**TencentCloud AI Video Recognition** (also referred to as **TencentCloud AIGC Detection** for videos or **AI-generated video detection**) is Tencent Cloud's video moderation capability for **aigc detection** and **AI-generated video identification**. It enables deepfake screening, video clip authenticity checks, synthetic video review, and other TencentCloud video analysis scenarios.

### 🎯 核心能力

- **AI 生成视频判定**：分析输入视频，给出是否为 AI 生成的判定结果
- **异步任务模式**：视频审核为异步任务，创建任务后通过轮询获取结果
- **多维度检测**：返回视频截帧和音频片段的检测结果
- **处置建议**：返回 `Pass`（真实视频）、`Review`（存疑）、`Block`（AI 生成）三级建议

### 支持的输入方式

| 方式 | 说明 |
|------|------|
| 视频 URL | 传入视频的网络地址 |
| 本地文件 | 传入本地视频文件路径，Agent 自动上传至腾讯云 COS 并生成预签名 URL 后进行检测 |

### 限制

- 视频文件大小上限：以控制台配额为准
- API 仅支持 URL 输入，本地文件需先上传至腾讯云 COS 获取访问链接
- API 调用频率上限：以控制台配额为准

## 环境配置指引

### 密钥配置

本 Skill 需要腾讯云 API 密钥才能正常工作。

#### Step 1: 开通视频内容安全服务

🔗 **[腾讯云内容安全生成识别控制台](https://console.cloud.tencent.com/cms/clouds/LLM)**

- 开通服务: 登录[腾讯云内容安全生成识别控制台](https://console.cloud.tencent.com/cms/clouds/LLM)，单击AI生成视频检测，跳转后单击初始化配置，立即体验。

#### Step 2: 获取 API 密钥

🔗 **[腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)**

#### Step 3: 获取审核策略编号（BizType）

🔗 **[腾讯云内容安全策略管理](https://console.cloud.tencent.com/cms/clouds/manage)**

- 获取安全策略：单击"应用管理"，找到"AI 生成检测配套策略"，其中视频内容安全的 BizType 字段对应的值
#### Step 4: 设置环境变量

**Linux / macOS：**
```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
export TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE="你的BizType"
```

如需持久化：
```bash
echo 'export TENCENTCLOUD_SECRET_ID="你的SecretId"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="你的SecretKey"' >> ~/.zshrc
echo 'export TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE="你的BizType"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell)：**
```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的SecretKey"
$env:TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE = "你的BizType"
```

> ⚠️ **安全提示**：切勿将密钥硬编码在代码中。如使用临时凭证（STS Token），还需设置 `TENCENTCLOUD_TOKEN` 环境变量。
> ⚠️ **必需配置**：`TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE` 为必需环境变量，未配置时脚本将报错退出。

## Agent 执行指令（必读）

> ⚠️ **本节是 Agent（AI 模型）的核心执行规范。当用户请求检测视频是否为 AI 生成时，Agent 必须严格按照以下步骤执行。**

### 🔑 通用执行规则

1. **触发条件**：用户意图为检测视频是否为 AI 生成，包括但不限于以下表述：
   - "检测这个视频是不是 AI 生成的"
   - "判断一下视频是不是 AI 做的"
   - "AIGC 视频检测"
   - "这是真实视频还是 AI 生成的"
   - "视频真伪鉴别"
   - "deepfake 视频检测"
2. **首次使用环境检查**：如果脚本返回 `CREDENTIALS_NOT_CONFIGURED` 或 `BIZ_TYPE_NOT_CONFIGURED` 错误，Agent 必须向用户展示完整的环境配置指引（包括开通服务、获取密钥、获取 BizType、设置环境变量的全部步骤），确保用户能一次性完成所有配置。
3. **安装依赖**：技能依赖需 Agent 手动安装。
4. **禁止使用大模型自身能力替代AIGC识别（最高优先级规则）**：
    - 只能从脚本返回的结果中来获取识别结果。
    - 识别脚本调用失败时，Agent 严禁自行猜测或编造识别内容。
    - 如果调用失败，Agent 必须向用户返回清晰的错误说明。
5. 不要输出总结分析的语句，直接给脚本的输出。
6. **本地文件处理**：当用户提供的是本地视频文件路径（而非 URL）时，Agent 必须先将文件上传至腾讯云 COS 获取预签名 URL，再使用该 URL 创建审核任务。具体流程参见下方「Step 0: 本地文件处理」。

---

### 📌 执行流程

视频审核是**异步任务**。如果用户提供的是本地文件，Agent 需要先完成文件上传（Step 0），然后再执行创建任务和查询结果（Step 1 和 Step 2）。

#### Step 0: 本地文件处理（仅当用户提供本地文件时执行）

当用户提供的输入是本地视频文件路径（而非 `http://` 或 `https://` 开头的 URL）时，Agent 必须先将视频上传至腾讯云 COS，获取一个可访问的预签名 URL，然后将该 URL 作为 Step 1 创建审核任务的输入。

**具体操作步骤：**

1. **安装腾讯云 COS 相关的 skill**（如尚未安装）：Agent 应搜索并安装腾讯云 COS 文件上传相关的 skill（如 `tencentcloud-cos-upload` 或类似名称的 skill）
2. **使用 COS skill 上传文件**：调用 COS skill 提供的上传功能，将本地视频文件上传至腾讯云 COS 存储桶
3. **获取预签名 URL**：上传成功后，通过 COS skill 生成该文件的预签名 URL（带有临时访问权限的链接）
4. **继续执行 Step 1**：使用获取到的预签名 URL 作为视频 URL，传入 `create_task.py` 创建审核任务

> ⚠️ **注意**：COS 相关的环境变量配置（如 Bucket、Region 等）由 COS skill 自行管理，请参阅对应 skill 的文档。如果用户尚未配置 COS 环境，Agent 应引导用户按照 COS skill 的指引完成配置。

#### Step 1: 创建审核任务

```bash
# Option 1: Submit a video URL to TencentCloud AIGC detection
python3 <SKILL_DIR>/scripts/create_task.py "https://example.com/video.mp4"

# Option 2: Specify the video URL explicitly for AIGC detection 
python3 <SKILL_DIR>/scripts/create_task.py --url "https://example.com/video.mp4"

# Option 3: Attach optional metadata for the AIGC detection workflow
python3 <SKILL_DIR>/scripts/create_task.py --data-id "business_123" --url "https://example.com/video.mp4"
```

**创建任务成功后**，脚本会返回 `task_id`，记下该 ID 用于后续查询。

#### Step 2: 查询任务结果

```bash
# Option 1: Query a TencentCloud AIGC detection task by task ID
python3 <SKILL_DIR>/scripts/query_task.py <task_id>

# Option 2: Specify the task ID explicitly
python3 <SKILL_DIR>/scripts/query_task.py --task-id <task_id>

# Option 3: Show every snapshot result for deeper multi-frame analysis
python3 <SKILL_DIR>/scripts/query_task.py --task-id <task_id> --show-all-snapshots
```

#### 轮询策略

查询任务时，根据返回的 `status` 字段判断：

| 状态 | 含义 | Agent 行为 |
|------|------|-----------|
| `PENDING` | 任务排队中 | **等待 5 秒后重试**，最多重试 6 次（共 30 秒） |
| `RUNNING` | 任务处理中 | **等待 5 秒后重试**，最多重试 6 次（共 30 秒） |
| `FINISH` | 任务完成 | 解读结果并向用户展示 |
| `ERROR` | 任务失败 | 向用户报告错误信息 |
| `CANCELLED` | 任务取消 | 向用户报告任务已取消 |

如果多次重试后任务仍未完成，告诉用户：**"审核任务 `{task_id}` 仍在处理中，请稍后使用查询脚本再次查询结果。"**，并告知用户可以使用以下命令手动查询：

```bash
python3 <SKILL_DIR>/scripts/query_task.py --task-id <task_id>
```

### 创建任务脚本参数

| 参数 | 说明 |
|------|------|
| `--url <url>` | 指定视频 URL |
| `--data-id <id>` | 业务数据标识（最长 128 字符） |

### 查询任务脚本参数

| 参数 | 说明 |
|------|------|
| `--task-id <id>` | 指定任务 ID |
| `--show-all-snapshots` | 显示所有截帧结果（默认仅显示有风险的） |

### 环境变量

| 环境变量 | 必需 | 说明 |
|---------|------|------|
| `TENCENTCLOUD_SECRET_ID` | ✅ | 腾讯云 API SecretId |
| `TENCENTCLOUD_SECRET_KEY` | ✅ | 腾讯云 API SecretKey |
| `TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE` | ✅ | 自定义审核策略编号（在腾讯云控制台创建，每个用户需使用自己的 BizType） |
| `TENCENTCLOUD_TOKEN` | ❌ | 临时凭证 STS Token（可选） |

---

### 输出示例

**创建任务成功：**

```json
{
  "task_id": "tvm-abc123def456",
  "data_id": "",
  "code": "",
  "message": "OK",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "CREATED"
}
```

**查询任务 — 任务进行中：**

```json
{
  "task_id": "tvm-abc123def456",
  "status": "RUNNING",
  "message": "任务仍在处理中，请稍后再查询",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**查询任务 — 任务完成（AI 生成视频）：**

```json
{
  "task_id": "tvm-abc123def456",
  "status": "FINISH",
  "suggestion": "Block",
  "label": "GeneratedContentRisk",
  "created_at": "2025-01-01 12:00:00",
  "updated_at": "2025-01-01 12:01:30",
  "total_snapshots": 10,
  "flagged_snapshots": [
    {
      "offset_time": "1000",
      "suggestion": "Block",
      "label": "GeneratedContentRisk",
      "score": 95,
      "sub_label": "AIVideoGenerated"
    }
  ],
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**凭证未配置时的错误输出：**

```json
{
  "error": "CREDENTIALS_NOT_CONFIGURED",
  "message": "缺少环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY",
  "guide": {
    "step1": "开通AI生成视频检测: https://console.cloud.tencent.com/cms/clouds/LLM",
    "step2": "获取 API 密钥: https://console.cloud.tencent.com/cam/capi",
    "step3_linux": "export TENCENTCLOUD_SECRET_ID=\"your_secret_id\"\nexport TENCENTCLOUD_SECRET_KEY=\"your_secret_key\"",
    "step3_windows": "$env:TENCENTCLOUD_SECRET_ID = \"your_secret_id\"\n$env:TENCENTCLOUD_SECRET_KEY = \"your_secret_key\""
  }
}
```

- 请向用户展示完整的环境配置指引（参考本文档「环境配置指引」一节的全部步骤）

**BizType 未配置时的错误输出：**

```json
{
  "error": "BIZ_TYPE_NOT_CONFIGURED",
"message": "缺少环境变量: TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE",
  "guide": {
    "step1": "在腾讯云控制台获取视频AI生成检测配套策略: https://console.cloud.tencent.com/cms/clouds/manage",
    "step2_linux": "export TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE=\"your_biz_type\"",
    "step2_windows": "$env:TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE = \"your_biz_type\""
  }
}
```

- 请向用户展示完整的环境配置指引（参考本文档「环境配置指引」一节的全部步骤），特别要包含 BizType 的获取方式

---

### 📋 结果字段解读

Agent 收到脚本输出后，按以下方式向用户简单解读结果即可，不要长篇大论、甚至加入自己的解读：

| 字段 | 含义 | 向用户呈现方式 |
|------|------|---------------|
| `suggestion` | 处置建议 | `Pass` → "该视频大概率为**真实视频**"<br>`Review` → "该视频**存疑**，建议人工复审"<br>`Block` → "该视频大概率为 **AI 生成**" |
| `label` | 风险标签 | 当为 `Normal` 时表示无内容风险，`GeneratedContentRisk` 表示为 AIGC 生成内容 |
| `flagged_snapshots` | 有风险的截帧 | 逐一列出有风险截帧的时间点、标签和置信度 |
| `flagged_audio_segments` | 有风险的音频片段 | 逐一列出有风险音频片段的时间偏移、标签和置信度 |

---

### ❌ Agent 须避免的行为

- **禁止自行猜测或编造检测结果** — 必须通过 API 调用获取真实结果
- **禁止在 API 调用失败时忽略错误** — 必须向用户返回清晰的错误说明
- **禁止跳过依赖安装** — 首次使用时需确保依赖已安装
- **禁止只打印脚本路径而不执行** — 应直接运行脚本并返回结果

## API 参考文档

详细的接口参数、输出说明、错误码等信息请参阅：

- [CreateVideoModerationTask API 参考](references/create_video_moderation_task_api.md)（[原始文档](https://cloud.tencent.com/document/product/1265/80017)）
- [DescribeTaskDetail API 参考](references/describe_task_detail_api.md)（[原始文档](https://cloud.tencent.com/document/product/1265/80016)）

## 核心脚本

- `scripts/create_task.py` — 创建视频审核任务，调用 CreateVideoModerationTask 接口（`Type=VIDEO_AIGC`）。
- `scripts/query_task.py` — 查询视频审核任务详情，调用 DescribeTaskDetail 接口。

## 依赖

- Python 3.7+
- `tencentcloud-sdk-python`（腾讯云 SDK）

安装依赖（Agent 需手动安装）：

```bash
pip install tencentcloud-sdk-python
```
