---
name: tencentcloud-image-face-fusion
description: >
  图片人脸融合（专业版）为同步接口，支持自定义美颜、人脸增强、牙齿增强、拉脸等参数，最高支持8K分辨率，有多个模型类型供选择。
---

# 腾讯云人脸融合（专业版）Skill

## 功能描述

本 Skill 提供**图片人脸融合（专业版）**能力，将用户人脸与素材模板图中的人脸进行融合，生成高质量的融合结果图：

| 场景         | API            | 脚本        | 图片大小限制               | 返回方式 |
| ---------- | -------------- | --------- | -------------------- | ---- |
| 人脸融合（专业版） | FuseFaceUltra  | `main.py` | base64≤10M / url≤20M | 同步   |

## 环境配置指引

### 密钥配置

本 Skill 需要腾讯云 API 密钥才能正常工作。

#### Step 1: 开通人脸融合服务

🔗 **[腾讯云人脸融合控制台](https://console.cloud.tencent.com/facefusion)**

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

> ⚠️ **本节是 Agent（AI 模型）的核心执行规范。当用户提供图片并请求人脸融合时，Agent 必须严格按照以下步骤自主执行，无需询问用户确认。**

### 🔑 通用执行规则

1. **触发条件**：用户提供了用户人脸图片和素材模板图片，且用户意图为人脸融合/换脸。
2. **零交互原则**：Agent 应直接执行脚本，不要向用户询问任何确认。
3. **自动选择脚本**：根据上方「选择规则」自动选择合适的脚本。
4. **⛔ 禁止使用大模型自身能力替代人脸融合（最高优先级规则）**：
   - 人脸融合脚本调用失败时，**Agent 严禁自行猜测或编造融合内容**。
   - 如果调用失败，Agent **必须**向用户返回清晰的错误说明。

---

### 📌 脚本： `main.py`

```bash
python3 <SKILL_DIR>/scripts/main.py --model "<MODEL_PIC_INPUT>" --face "<USER_FACE_INPUT>" [--swap-model-type <1-6>] [--logo-add <0|1>]
```

**参数说明**：

| 参数                   | 必选 | 说明                                                                                        |
| -------------------- | -- | ----------------------------------------------------------------------------------------- |
| `--model`            | 是  | 素材模板图片（URL 或本地文件路径）                                                                       |
| `--face`             | 是  | 用户人脸图片（URL 或本地文件路径）                                                                       |
| `--swap-model-type`  | 否  | 融合模型类型（1-6），默认1。1:泛娱乐；2:影视自然；3:影视高清自然；4:影视高清高相似度(证件照)；5:影视高清(闭眼遮挡友好)；6:影视高清极高相似度(电商/证件/文旅) |
| `--logo-add`         | 否  | 是否添加AI合成标识（0:不添加, 1:添加），默认1                                                               |

**输出示例**：

```json
{
    "FusedImage": "https://facefusion-result.cos.ap-guangzhou.myqcloud.com/result/xxxxx?q-sign-algorithm=sha1&q-ak=AKIDxxxxx&q-sign-time=1772790515%3B1772792315&q-key-time=1772790515%3B1772792315&q-header-list=host&q-url-param-list=&q-signature=xxxxx"
}
```

---

### 📋 完整调用示例

```bash
# 基本用法：提供素材模板图和用户人脸图
python3 /path/to/scripts/main.py --model "https://example.com/template.png" --face "https://example.com/user_face.png"

# 指定融合模型类型为影视级高清（证件照场景）
python3 /path/to/scripts/main.py --model "/path/to/template.jpg" --face "/path/to/face.jpg" --swap-model-type 4

# 不添加AI合成标识
python3 /path/to/scripts/main.py --model "https://example.com/template.png" --face "https://example.com/face.png" --logo-add 0
```

### ❌ Agent 须避免的行为

- 只打印脚本路径而不执行
- 向用户询问"是否要执行人脸融合"——应直接执行
- 手动安装依赖——脚本内部自动处理
- 忘记读取输出结果并返回给用户
- 人脸融合服务调用失败时，自行编造融合结果

## API 参考文档

详细的参数说明、错误码等信息请参阅 `references/` 目录下的文档：

- [图片人脸融合（专业版）API](references/FuseFaceUltraApi.md)（[原始文档](https://cloud.tencent.com/document/product/670/106891)）

## 核心脚本

- `scripts/main.py` — 人脸融合（专业版）脚本

## 依赖

- Python 3.7+
- `tencentcloud-sdk-python`（腾讯云 SDK，`main.py` 使用）

安装依赖（可选 - 脚本会自动安装）：

```bash
pip install tencentcloud-sdk-python
```
