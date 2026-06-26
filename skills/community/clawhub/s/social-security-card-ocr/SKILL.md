---
name: social_security_card_ocr
description: 将图片中的文字、社保卡信息识别并提取出来。本技能应在用户需要 OCR 识别图片中的文字，或识别社保卡时使用。
version: 1.0.3
author: SCNet
license: MIT
tags:
  - OCR
  - 证件识别
  - 发票识别
  - 文字提取
required_env_vars:
  - SCNET_API_KEY
optional_env_vars:
  - SCNET_API_BASE
primary_credential: SCNET_API_KEY
dependencies:
  - python3
  - requests
input:
  - ocrType : 识别类型，可选值见下文
  - filePath : 待识别图片的本地路径
output: 结构化的 JSON 数据，包含识别结果和置信度
---
# Sugon-Scnet 社保卡识别 OCR 技能

本技能封装了社保卡识别的 OCR 服务，通过单一接口即可调用 1 种识别能力，高效提取社保卡核心信息。

## 功能特性

- **社保卡识别**：支持识别社保卡，自动提取证件核心信息。


## 前置配置

> **⚠️ 重要**：使用前需要申请 Scnet API Token

### 申请 API Token

1. 访问 [Scnet 官网](https://www.scnet.cn) 注册/登录
2. 在控制台申请 API 密钥（格式：`sc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
3. 复制密钥备用

### 配置 Token

**手动配置（推荐）**
1. 在技能目录下创建 `config/.env` 文件，内容如下：
```ini
# =====  Sugon-Scnet OCR API 配置 =====
# 申请地址：https://www.scnet.cn
SCNET_API_KEY=your_scnet_api_key_here

# API 基础地址（一般无需修改）
SCNET_API_BASE=https://api.scnet.cn/api/llm/v1
```
2. 添加：`SCNET_API_KEY=你的密钥`
3. 设置文件权限为 600（仅所有者可读写）
**⚠️ 安全警告**：切勿将 API Key 直接粘贴到聊天对话中，否则可能被记录或泄露。

### Token 更新

Token 过期后调用会返回 401 或 403 错误。更新方法：重新申请 Token 并替换 config/.env 中的 SCNET_API_KEY。

### 依赖安装

本技能需要 Python 3.6+ 和 requests 库。请运行以下命令：

```bash
   pip install requests
```
---
### 使用方法

### 参数说明

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| ocrType | string | 是 | 识别类型枚举。必须为以下之一：<br>• SOCIAL_SECURITY_CARD（社保卡） |
| filePath | string | 是 | 待识别图片的本地绝对路径。支持 jpg、png、pdf 等常见格式。 |

### 命令行调用示例

```bash
   python .claude/skills/social_security_card_ocr/scripts/main.py SOCIAL_SECURITY_CARD /path/to/invoice.jpg
```

### 在 AI 对话中使用

用户可以说：

- “帮我识别这张社保卡的信息，图片在 /Users/name/Downloads/id.jpg”

AI 会根据 description 中的关键词自动触发本技能。

### AI 调用建议
为避免触发 API 速率限制（10 QPS），请串行调用本技能，即等待前一个识别完成后再发起下一个请求。
如果使用 OpenClaw 的 exec 工具，建议设置 timeout 或 yieldMs 参数，让命令同步执行，避免多个命令同时运行导致并发。

### 配置选项

编辑 `config/.env` 文件：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| SCNET_API_KEY | 必需 | Scnet API 密钥 |
| SCNET_API_BASE | https://api.scnet.cn/api/llm/v1 | API 基础地址（一般无需修改） |

### 输出

- 标准输出：识别结果的 JSON 数据，结构与 API 文档一致，位于 `data` 字段内。
- 识别结果位于 data[0].result[0].elements 中，具体字段取决于 ocrType。
- 错误信息：如果发生错误，会输出以 `错误:` 开头的友好提示。

### 注意事项

- 本技能调用的 OCR API 有 10 QPS 的速率限制。
- 如果遇到 429 错误，请等待 2-3 秒后重试，不要连续发起请求。
- 建议在调用前确保图片已准备就绪，避免因网络问题导致重复调用。

### 故障排除

| 问题 | 解决方案 |
|------|----------|
| 配置文件不存在 | 创建 config/.env 并填入 Token（参考前置配置） |
| API Key 无效/过期 | 重新申请 Token 并更新 `.env` 文件 |
| 文件不存在 | 检查提供的文件路径是否正确 |
| 网络连接失败 | 检查网络连接或防火墙设置 |
| 不支持的文件类型 | 确保文件扩展名为允许的类型（参考 API 文档） |
| 401/403/Unauthorized | Token 无效或过期，重新申请并配置 |
| 429 Too Many Requests | 请求过于频繁，技能会自动等待并重试（最多 3 次）。若持续失败，请降低调用频率或联系服务方提高限额。 |


