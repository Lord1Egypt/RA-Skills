# wei-devils-advocate 配置指南

[English Version](README.md)

本文档说明如何配置 `config.json` 以使用不同的模型提供商和部署环境。

---

## 配置文件概述

项目提供以下示例配置文件，可根据你的网络环境和 API 访问情况选择：

| 配置文件 | 适用场景 | 说明 |
|---------|---------|------|
| `config_global_example.json` | **默认推荐** | 支持 OpenRouter 全球访问，包含最丰富的模型选择 |
| `config_cn_example.json` | 中国用户 | 优化 OpenRouter 中国访问，去除中国受限模型 |
| `config_dashscope_example.json` | 阿里云用户 | 仅使用阿里云 DashScope/Bailian 模型，无需 OpenRouter |

---

## 快速开始

### 1. 选择配置文件

根据你的网络环境和 API 访问情况，复制对应的示例文件为 `config.json`：

```bash
# 默认配置（全球访问，推荐）
cp config_global_example.json config.json

# 中国优化配置（去除受限模型）
cp config_cn_example.json config.json

# 阿里云 DashScope 配置（无需 OpenRouter）
cp config_dashscope_example.json config.json
```

### 2. 配置环境变量

根据所选配置，设置相应的 API 密钥：

#### 使用 OpenRouter 配置（global/cn）

```bash
# 必需：OpenRouter API 密钥（用于回答模型）
export OPENROUTER_API_KEY=your_openrouter_api_key

# 可选：DashScope API 密钥（用于 judge 模型，如果使用 bailian 的 judge）
export DASHSCOPE_API_KEY=your_dashscope_api_key
```

或在项目根目录创建 `.env` 文件：

```bash
OPENROUTER_API_KEY=your_openrouter_api_key
DASHSCOPE_API_KEY=your_dashscope_api_key
```

#### 使用 DashScope 配置

```bash
# 必需：DashScope API 密钥
export DASHSCOPE_API_KEY=your_dashscope_api_key
```

或在 `.env` 文件中：

```bash
DASHSCOPE_API_KEY=your_dashscope_api_key
```

### 3. 验证配置

运行测试命令验证配置是否正确：

```bash
bun run scripts/index.ts "测试配置是否生效"
```

---

## 配置文件详解

### config_global_example.json（默认配置）

**适用场景**：全球访问，拥有 OpenRouter API 密钥

**特点**：
- 使用 OpenRouter 作为模型提供商
- 包含丰富的模型选择：GPT-5.4、Grok-4.1、Kimi、GLM-5、MiniMax、Qwen 等
- Judge 模型通过 OpenRouter 访问
- `region` 设置为 `"global"`

**模型列表**：
- `glm-5` - 通用、检索、分析
- `minimax-m2.5` - 推理、创意、综合
- `kimi-k2.5` - 长上下文、检索、时事
- `gpt-5.4` - 通用、检索、平衡
- `grok-4.1` - 社交、情感、趋势（X 平台数据）
- `qwen3.5` - 结构化、编码、技术
- `glm-5-judge` / `qwen3.5-judge` - Judge 模型

**路由配置**：
- `financial`: kimi-k2.5, gpt-5.4, qwen3.5
- `technical`: qwen3.5, gpt-5.4, kimi-k2.5
- `social`: grok-4.1, kimi-k2.5, minimax-m2.5
- `current_events`: kimi-k2.5, grok-4.1, gpt-5.4

---

### config_cn_example.json（中国优化）

**适用场景**：中国网络环境，OpenRouter 访问受限

**特点**：
- 使用 OpenRouter 作为模型提供商
- **去除**中国受限模型：GPT-5.4、Grok-4.1
- **添加**中国可用模型：DeepSeek-V3.2
- Judge 模型通过 OpenRouter 访问
- `region` 设置为 `"cn"`

**模型列表**：
- `glm-5` - 通用、检索、分析
- `minimax-m2.5` - 推理、创意、综合
- `qwen3.5` - 结构化、编码、技术
- `kimi-k2.5` - 长上下文、检索、时事
- `deepseek-v3.2` - 编码、技术、推理（替代 GPT）
- `glm-5-judge` / `qwen3.5-judge` - Judge 模型

**路由配置**：
- `financial`: kimi-k2.5, qwen3.5, glm-5
- `technical`: qwen3.5, deepseek-v3.2, kimi-k2.5
- `social`: kimi-k2.5, minimax-m2.5（去除 grok-4.1）
- `current_events`: kimi-k2.5, glm-5, qwen3.5

---

### config_dashscope_example.json（阿里云）

**适用场景**：无法访问 OpenRouter，但拥有阿里云 DashScope API 密钥

**特点**：
- 使用阿里云 **DashScope/Bailian** 作为唯一模型提供商
- 所有模型通过 `dashscope.aliyuncs.com` 访问
- 仅需 `DASHSCOPE_API_KEY`，无需 OpenRouter
- `region` 设置为 `"cn"`

**模型列表**：
- `minimax-m2.5` - 推理、创意、综合
- `qwen3.5` - 结构化、编码、技术
- `kimi-k2.5` - 长上下文、检索、时事
- `deepseek-v3.2` - 编码、技术、推理
- `glm-5-judge` / `qwen3.5-judge` - Judge 模型

**注意**：DashScope 提供的模型可能略有不同，实际可用模型请参考阿里云官方文档。

---

## 配置参数说明

### 顶层参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| `region` | string | 区域标识，`"global"` 或 `"cn"` |
| `judge_model` | string | Judge 模型名称，用于综合评估 |
| `max_models` | number | 默认使用的回答模型数量（1-3） |
| `depth` | string | 默认深度模式，`"simple"` 或 `"tree"` |
| `max_tokens` | number | 回答模型的最大 token 数 |
| `max_tokens_judge` | number | Judge 模型的最大 token 数 |

### 模型配置（`models`）

每个模型包含以下字段：

| 字段 | 类型 | 说明 |
|-----|------|------|
| `provider` | string | 提供商：`"openrouter"`、`"bailian"` 或 `"openai_compliant"` |
| `model_id` | string | 模型在提供商处的 ID |
| `api_base` | string | API 基础 URL |
| `api_key_env` | string | 环境变量名，用于获取 API 密钥 |
| `timeout` | number | 请求超时时间（秒） |
| `roles` | array | 模型能力标签，用于路由选择 |

### 路由配置（`routing`）

根据 `queryType` 选择模型的规则：

| queryType | 适用场景 |
|-----------|---------|
| `financial` | 金融、投资、宏观经济 |
| `technical` | 编程、系统、工程 |
| `social` | 社交媒体、公众舆论 |
| `current_events` | 时事新闻、实时信息 |
| `scientific` | 科学知识、理论研究 |
| `creative` | 创意写作、设计 |
| `general` | 通用默认 |

---

## 自定义配置

### 添加新模型

在 `config.json` 的 `models` 部分添加：

```json
{
  "models": {
    "my-custom-model": {
      "provider": "openrouter",
      "model_id": "provider/model-name:online",
      "api_base": "https://openrouter.ai/api/v1",
      "api_key_env": "OPENROUTER_API_KEY",
      "timeout": 60,
      "roles": ["general", "retrieval"]
    }
  }
}
```

### 修改路由

在 `routing` 部分添加或修改：

```json
{
  "routing": {
    "my-domain": {
      "models": ["model-1", "model-2"],
      "judge_prompt": "custom_judge"
    }
  }
}
```

### 使用其他 OpenAI 兼容服务

支持任何 OpenAI 兼容 API：

```json
{
  "my-model": {
    "provider": "openai_compliant",
    "model_id": "model-name",
    "api_base": "https://your-api-endpoint.com/v1",
    "api_key_env": "YOUR_API_KEY_ENV",
    "timeout": 60,
    "roles": ["general"]
  }
}
```

---

## 故障排除

### OpenRouter 连接问题

**症状**：HTTP 404 错误或连接超时

**解决**：
1. 检查 `OPENROUTER_API_KEY` 是否正确设置
2. 尝试切换为 `config_cn_example.json`
3. 检查网络是否能访问 `https://openrouter.ai`

### DashScope 连接问题

**症状**：模型返回错误或超时

**解决**：
1. 确认使用 `config_dashscope_example.json`
2. 检查 `DASHSCOPE_API_KEY` 是否有效
3. 查看阿里云控制台确认模型是否已开通

### 模型不存在错误

**症状**：`The model 'xxx' does not exist`

**解决**：
- 该模型可能在你的地区不可用
- 切换到其他配置或修改 `config.json` 移除该模型

---

## 参考链接

- [OpenRouter 文档](https://openrouter.ai/docs)
- [阿里云 DashScope 文档](https://help.aliyun.com/document_detail/611411.html)
- [Bun 运行时](https://bun.sh/docs)

---

## 示例对比

| 特性 | Global | CN | DashScope |
|------|--------|-----|-----------|
| 主要提供商 | OpenRouter | OpenRouter | 阿里云 |
| GPT-5.4 | ✅ | ❌ | ❌ |
| Grok-4.1 | ✅ | ❌ | ❌ |
| 需要 OPENROUTER_API_KEY | ✅ | ✅ | ❌ |
| 需要 DASHSCOPE_API_KEY | 可选 | 可选 | ✅ |
| 中国访问 | 可能受限 | 优化 | 良好 |
