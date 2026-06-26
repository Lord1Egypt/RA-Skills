---
name: shipping-booking
description: 海运托书（Booking Note / Shipping Instruction）智能提取工具。从 PDF、图片、扫描件、Word、Excel、RTF 等格式的托书文件中提取结构化信息，输出标准 JSON。当用户明确提到"托书"、"booking"、"shipping instruction"、"帮我提取"、"解析托书"等关键词并上传文件时触发。不处理与托书无关的文件。
metadata: {"openclaw":{"emoji":"🚢","requires":{"anyEnv":["ANTHROPIC_API_KEY","OPENAI_API_KEY"]},"primaryEnv":"ANTHROPIC_API_KEY","network":["api.anthropic.com","api.openai.com","api.deepseek.com","dashscope.aliyuncs.com","api.moonshot.cn","open.bigmodel.cn"]}}
---

# Shipping Booking Extractor

从各种格式的海运托书文件中提取结构化数据，输出标准 JSON。

---

## 🚀 快速开始（首次安装）

**第一步：安装 skill**

```bash
clawhub install shipping-booking
```

**第二步：安装依赖（只需一次）**

```bash
pip install -r ~/.openclaw/skills/shipping-booking/requirements.txt
```

**第二步：配置 AI 模型（任选一种，无需全部配置）**

| 方式 | 说明 |
|------|------|
| ✅ 推荐 | 在 OpenClaw 中已配置 AI 账号，**自动读取，无需任何操作** |
| Anthropic Claude | `export ANTHROPIC_API_KEY=your_key` |
| DeepSeek | `export OPENAI_API_KEY=your_key` `export OPENAI_BASE_URL=https://api.deepseek.com/v1` |
| 通义千问 | `export OPENAI_API_KEY=your_key` `export OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Kimi | `export OPENAI_API_KEY=your_key` `export OPENAI_BASE_URL=https://api.moonshot.cn/v1` |
| 智谱 GLM | `export OPENAI_API_KEY=your_key` `export OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4` |
| 自定义文本模型 | `export SHIPPING_MODEL=your_model_name` |
| 自定义视觉模型 | `export SHIPPING_VISION_MODEL=your_vision_model`（用于图片/PDF） |

> 💡 只要在 OpenClaw 里配置过任意一个 AI 账号，装完即用，不需要手动设置环境变量。

**第三步：直接使用，把托书文件发给我即可！**

---

## 支持格式

| 格式 | 支持情况 |
|------|---------|
| PDF | ✅ 全平台 |
| 图片（JPG/PNG/TIFF/BMP/WebP） | ✅ 全平台 |
| Excel（.xlsx / .xls） | ✅ 全平台 |
| Word（.docx） | ✅ 全平台 |
| RTF（.rtf） | ✅ 全平台 |
| Word（.doc） | ✅ macOS 自动处理；其他平台需安装 LibreOffice 或另存为 .docx |

---

## 触发条件

**必须同时满足：**
1. 用户上传了文件
2. 用户提到以下任意关键词：
   - 中文：托书、提单、订舱、帮我提取、解析、识别
   - 英文：booking、shipping instruction、SI、extract

---

## 执行流程

### Step 1：确认文件类型，运行提取脚本

```bash
python3 ~/.openclaw/skills/shipping-booking/scripts/extract.py <文件路径>
```

### Step 2：验证并输出结果

- 提取成功 → 将 JSON 以代码块形式呈现，不要暴露终端命令
- `low_confidence_fields` 不为空 → 在 JSON 下方附加提醒：
  > ⚠️ 以下字段置信度较低，建议人工核查：字段1、字段2
- 不像托书文件 → 提示：
  > ❌ 这不像是托书文件，请确认上传的文件是否正确

---

## 🔒 数据安全说明

- 托书文件内容（文本/图片）会发送给你配置的 AI 模型 API 进行分析
- 支持的 API 端点：Anthropic Claude、OpenAI、DeepSeek、通义千问、Kimi、智谱 GLM
- **文件本身不会上传到任何第三方存储**，仅作为 API 请求内容临时传输
- API Key 从本地 OpenClaw 配置读取，不会泄露到其他地方

## 字段定义

详见 `references/schema.md`
