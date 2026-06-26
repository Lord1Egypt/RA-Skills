---
name: tencentcloud-aigc-recog-image
description: 腾讯云 AI 生成图片识别 (TencentCloud Image AIGC Detection) 技能。适用于 AI 生成图片检测、图片真伪鉴别、AI 绘画检测、Deepfake 检测等场景。TencentCloud Image AIGC Detection is an AI-generated content detection service by Tencent Cloud, supporting aigc detection, AI-generated image identification, and image authenticity review.
---

# 腾讯云 AI 生成图片识别 Skill

## 功能描述

本技能用于检测图像是否由AIGC生成，支持对 Stable Diffusion、Midjourney、GPT‑4o 等主流模型生成的图像进行识别。

**TencentCloud Image AIGC Detection** (also referred to as **TencentCloud AIGC Detection** for images or **AI-generated image detection**) is Tencent Cloud's image moderation capability for **aigc detection** and **AI-generated image identification**. It enables AI artwork review, image authenticity screening, synthetic media checks, and other TencentCloud image analysis workflows.

### 🎯 核心能力

- **AI 生成图片判定**：分析输入图片，给出是否为 AI 生成的判定结果
- **风险评分**：返回 0-100 的置信度评分，分数越高越可能是 AI 生成
- **处置建议**：返回 `Pass`（真实图片）、`Review`（存疑）、`Block`（AI 生成）三级建议
- **详细结果**：返回命中标签、子标签等详细信息

### 支持的输入方式

| 方式 | 说明 |
|------|------|
| 图片 URL | 传入图片的网络地址 |
| 本地文件 | 传入本地图片文件路径，自动读取并 Base64 编码 |

### 限制

- 图片文件大小上限：**5MB**
- 支持格式：**PNG、JPG、JPEG、BMP、GIF、WEBP**
- API 调用频率上限：以控制台配额为准

## 环境配置指引

### 密钥配置

本 Skill 需要腾讯云 API 密钥才能正常工作。

#### Step 1: 开通图片内容安全服务

🔗 **[腾讯云内容安全生成识别控制台](https://console.cloud.tencent.com/cms/clouds/LLM)**

- 开通服务: 登录[腾讯云内容安全生成识别控制台](https://console.cloud.tencent.com/cms/clouds/LLM)，单击AI生成图片检测，跳转后单击初始化配置，立即体验。

#### Step 2: 获取 API 密钥

🔗 **[腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)**

#### Step 3: 获取审核策略编号（BizType）

🔗 **[腾讯云内容安全策略管理](https://console.cloud.tencent.com/cms/clouds/manage)**

- 获取安全策略：单击"应用管理"，找到"AI 生成检测配套策略"，其中图片内容安全的 BizType 字段对应的值
#### Step 4: 设置环境变量

**Linux / macOS：**
```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
export TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE="你的BizType"
```

如需持久化：
```bash
echo 'export TENCENTCLOUD_SECRET_ID="你的SecretId"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="你的SecretKey"' >> ~/.zshrc
echo 'export TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE="你的BizType"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell)：**
```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的SecretKey"
$env:TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE = "你的BizType"
```

> ⚠️ **安全提示**：切勿将密钥硬编码在代码中。如使用临时凭证（STS Token），还需设置 `TENCENTCLOUD_TOKEN` 环境变量。
> ⚠️ **必需配置**：`TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE` 为必需环境变量，未配置时脚本将报错退出。

## Agent 执行指令（必读）

> ⚠️ **本节是 Agent（AI 模型）的核心执行规范。当用户请求检测图片是否为 AI 生成时，Agent 必须严格按照以下步骤自主执行，无需询问用户确认。**

### 🔑 通用执行规则

1. **触发条件**：用户意图为检测图片是否为 AI 生成，包括但不限于以下表述：
   - "检测这张图片是不是 AI 生成的"
   - "判断一下图片是不是 AI 画的"
   - "AIGC 图片检测"
   - "这是真实照片还是 AI 生成的"
   - "图片真伪鉴别"
   - "deepfake 检测"
2. **首次使用环境检查**：如果脚本返回 `CREDENTIALS_NOT_CONFIGURED` 或 `BIZ_TYPE_NOT_CONFIGURED` 错误，Agent 必须向用户展示完整的环境配置指引（包括开通服务、获取密钥、获取 BizType、设置环境变量的全部步骤），确保用户能一次性完成所有配置。
3. **安装依赖**：技能依赖需 Agent 手动安装。
4. **禁止使用大模型自身能力替代AIGC识别（最高优先级规则）**：
    - 只能从脚本返回的结果中来获取识别结果。
    - 识别脚本调用失败时，Agent 严禁自行猜测或编造识别内容。
    - 如果调用失败，Agent 必须向用户返回清晰的错误说明。
5. 不要输出总结分析的语句，直接给脚本的输出。
---

### 📌 调用方式

```bash
# Option 1: Run TencentCloud AIGC detection with an image URL
python3 <SKILL_DIR>/scripts/main.py "https://example.com/image.jpg"

# Option 2: Run AI-generated image detection with a local image file
python3 <SKILL_DIR>/scripts/main.py /path/to/image.png

# Option 3: Specify the image URL explicitly for TencentCloud image analysis
python3 <SKILL_DIR>/scripts/main.py --url "https://example.com/image.jpg"

# Option 4: Specify a local file for AI image authenticity review
python3 <SKILL_DIR>/scripts/main.py --file /path/to/image.png

# Option 5: Attach optional metadata for the image moderation workflow
python3 <SKILL_DIR>/scripts/main.py --data-id "business_123" /path/to/image.png
```

### 可选参数

| 参数 | 说明 |
|------|------|
| `--url <url>` | 指定图片 URL |
| `--file <path>` | 指定本地图片文件路径 |
| `--data-id <id>` | 业务数据标识，用于关联检测结果（最长 128 字符） |

### 环境变量

| 环境变量 | 必需 | 说明 |
|---------|------|------|
| `TENCENTCLOUD_SECRET_ID` | ✅ | 腾讯云 API SecretId |
| `TENCENTCLOUD_SECRET_KEY` | ✅ | 腾讯云 API SecretKey |
| `TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE` | ✅ | 自定义审核策略编号（在腾讯云控制台创建，每个用户需使用自己的 BizType） |
| `TENCENTCLOUD_TOKEN` | ❌ | 临时凭证 STS Token（可选） |

---

### 输出示例

**正常检测结果：**

```json
{
  "suggestion": "Block",
  "label": "GeneratedContentRisk",
  "score": 95,
  "sub_label": "AIImageGenerated",
  "detail_results": [
    {
      "label": "GeneratedContentRisk",
      "suggestion": "Block",
      "score": 95,
      "sub_label": "AIImageGenerated"
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
    "step1": "开通AI生成图片检测服务: https://console.cloud.tencent.com/cms/clouds/LLM",
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
"message": "缺少环境变量: TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE",
  "guide": {
    "step1": "在腾讯云控制台获取图片AI生成检测配套策略: https://console.cloud.tencent.com/cms/clouds/manage",
"step2_linux": "export TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE=\"your_biz_type\"",
    "step2_windows": "$env:TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE = \"your_biz_type\""
  }
}
```

- 请向用户展示完整的环境配置指引（参考本文档「环境配置指引」一节的全部步骤），特别要包含 BizType 的获取方式

---

### 📋 结果字段解读

Agent 收到脚本输出后，按以下方式向用户简单解读结果即可，不要长篇大论、甚至加入自己的解读：

| 字段 | 含义 | 向用户呈现方式 |
|------|------|---------------|
| `suggestion` | 处置建议 | `Pass` → "该图片大概率为**真实图片**"<br>`Review` → "该图片**存疑**，建议人工复审"<br>`Block` → "该图片大概率为 **AI 生成**" |
| `label` | 风险标签 | 当为 `Normal` 时表示无其他内容风险, `GeneratedContentRisk` 表示为 AIGC 生成内容 |
| `score` | 置信度（0-100） | 分数越高越可能是 AI 生成。0-60 低风险、60-80 中风险、80-100 高风险 |
| `detail_results` | 详细检测结果 | 如有多个维度，逐一说明 |

---

### ❌ Agent 须避免的行为

- **禁止自行猜测或编造检测结果** — 必须通过 API 调用获取真实结果
- **禁止在 API 调用失败时忽略错误** — 必须向用户返回清晰的错误说明
- **禁止跳过依赖安装** — 首次使用时需确保依赖已安装
- **禁止只打印脚本路径而不执行** — 应直接运行脚本并返回结果

## API 参考文档

详细的接口参数、输出说明、错误码等信息请参阅：

- [ImageModeration API 参考](references/image_moderation_api.md)（[原始文档](https://cloud.tencent.com/document/product/1125/53273)）
- [SDK 调用指引](https://cloud.tencent.com/document/product/1124/100983)

## 核心脚本

- `scripts/main.py` — AI 生成图片识别，调用 ImageModeration 接口（`Type=IMAGE_AIGC`）。

## 依赖

- Python 3.7+
- `tencentcloud-sdk-python`（腾讯云 SDK）

安装依赖（Agent 需手动安装）：

```bash
pip install tencentcloud-sdk-python
```
