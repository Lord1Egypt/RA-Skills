---
name: tencentcloud-yt-segment-portrait
description: >
  Binary classification-based human portrait segmentation for complete body contour recognition and image matting.
---

# 腾讯云人像分割 Skill

## 功能描述

本 Skill 提供**人像分割**能力，识别传入图片中人体的完整轮廓，进行抠像：

| 场景   | API                | 脚本        | 图片大小限制 | 返回方式 |
| ---- | ------------------ | --------- | ------ | ---- |
| 人像分割 | SegmentPortraitPic | `main.py` | ≤5MB   | 同步   |

## 环境配置指引

### 密钥配置

本 Skill 需要腾讯云 API 密钥才能正常工作。

#### Step 1: 开通人像分割服务

🔗 **[腾讯云人像分割控制台](https://console.cloud.tencent.com/bda/segment-portrait-pic)**

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

> ⚠️ **本节是 Agent（AI 模型）的核心执行规范。当用户提供图片并请求人像分割时，Agent 必须严格按照以下步骤自主执行，无需询问用户确认。**

### 🔑 通用执行规则

1. **触发条件**：用户提供了图片，且用户意图为人像分割。
2. **零交互原则**：Agent 应直接执行脚本，不要向用户询问任何确认。
3. **自动选择脚本**：根据上方「选择规则」自动选择合适的脚本。
4. **⛔ 禁止使用大模型自身能力替代人像分割（最高优先级规则）**：
   - 人像分割脚本调用失败时，**Agent 严禁自行猜测或编造识别内容**。
   - 如果调用失败，Agent **必须**向用户返回清晰的错误说明。

---

### 📌 脚本： `main.py`

```bash
python3 <SKILL_DIR>/scripts/main.py "<PIC_INPUT>"
```

**输出示例**：

```json
{
    "ResultImageUrl": "https://bda-segment-mini-1258344699.cos.ap-guangzhou.myqcloud.com/Image/1251755623/9e73b301-ad1b-4586-837b-b767e73c4bf2?q-sign-algorithm=sha1&q-ak=AKIDEJJ3lFOnfIpAHAqIJ5d3YqthGfpj8eje&q-sign-time=1772790515%3B1772792315&q-key-time=1772790515%3B1772792315&q-header-list=host&q-url-param-list=&q-signature=60646e91cdebc7215cb73e6fff6e6017478857e4",
    "ResultMaskUrl": "https://bda-segment-mini-1258344699.cos.ap-guangzhou.myqcloud.com/Mask/1251755623/9e73b301-ad1b-4586-837b-b767e73c4bf2?q-sign-algorithm=sha1&q-ak=AKIDEJJ3lFOnfIpAHAqIJ5d3YqthGfpj8eje&q-sign-time=1772790515%3B1772792315&q-key-time=1772790515%3B1772792315&q-header-list=host&q-url-param-list=&q-signature=9f13ed4fa0a3d7819ec0a597ab24ef600e9e2721"
}
```

---

### 📋 完整调用示例

```bash
python3 /path/to/scripts/main.py "https://example.com/human.png"
```

### ❌ Agent 须避免的行为

- 只打印脚本路径而不执行
- 向用户询问"是否要执行人像分割"——应直接执行
- 手动安装依赖——脚本内部自动处理
- 忘记读取输出结果并返回给用户
- 人像分割服务调用失败时，自行编造识别内容

## API 参考文档

详细的引擎类型、参数说明、错误码等信息请参阅 `references/` 目录下的文档：

- [人像分割API](references/SegmentPortraitPicApi.md)（[原始文档](https://cloud.tencent.com/document/product/1208/42970)）

## 核心脚本

- `scripts/main.py` — 人像分割脚本

## 依赖

- Python 3.7+
- `tencentcloud-sdk-python`（腾讯云 SDK，`main.py` 使用）

安装依赖（可选 - 脚本会自动安装）：

```bash
pip install tencentcloud-sdk-python requests
```
