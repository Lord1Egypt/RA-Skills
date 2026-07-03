---
name: 随机数生成服务
description: 一款符合MCP协议的加密安全随机数生成服务器，适用于AI应用、LLM及其他需要高质量随机数的系统。
version: 1.0.0
---

# 随机数生成服务

一款符合MCP协议的加密安全随机数生成服务器，适用于AI应用、LLM及其他需要高质量随机数的系统。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Generate cryptographically secure random integers within a specified range | `scripts.tools.generate_random_integer` |
| Generate cryptographically secure random floating-point numbers | `scripts.tools.generate_random_float` |
| Generate cryptographically secure random bytes | `scripts.tools.generate_random_bytes` |
| Generate a cryptographically secure UUID (v4) | `scripts.tools.generate_uuid` |
| Generate a cryptographically secure random string | `scripts.tools.generate_random_string` |
| Randomly select items from a given list using cryptographically secure randomness | `scripts.tools.generate_random_choice` |
| Generate cryptographically secure random boolean values | `scripts.tools.generate_random_boolean` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.generate_random_integer
工具描述：Generate cryptographically secure random integers within a specified range
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|min|integer|false|0.0|Minimum value (inclusive)|
|max|integer|false|100.0|Maximum value (inclusive)|
|count|integer|false|1.0|Number of random integers to generate|

---

## scripts.tools.generate_random_float
工具描述：Generate cryptographically secure random floating-point numbers
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|min|number|false|0.0|Minimum value (inclusive)|
|max|number|false|1.0|Maximum value (exclusive)|
|count|integer|false|1.0|Number of random floats to generate|
|precision|integer|false|6.0|Number of decimal places to round to|

---

## scripts.tools.generate_random_bytes
工具描述：Generate cryptographically secure random bytes
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|length|integer|false|32.0|Number of random bytes to generate|
|encoding|string|false|"hex"|Output encoding format|

---

## scripts.tools.generate_uuid
工具描述：Generate a cryptographically secure UUID (v4)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|count|integer|false|1.0|Number of UUIDs to generate|
|format|string|false|"standard"|UUID format|

---

## scripts.tools.generate_random_string
工具描述：Generate a cryptographically secure random string
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|length|integer|false|16.0|Length of the random string|
|charset|string|false|"alphanumeric"|Character set to use|
|count|integer|false|1.0|Number of random strings to generate|

---

## scripts.tools.generate_random_choice
工具描述：Randomly select items from a given list using cryptographically secure randomness
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|choices|array|true| |Array of items to choose from|
|count|integer|false|1.0|Number of items to select|
|allow_duplicates|boolean|false|true|Whether to allow duplicate selections|

---

## scripts.tools.generate_random_boolean
工具描述：Generate cryptographically secure random boolean values
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|count|integer|false|1.0|Number of random booleans to generate|
|probability|number|false|0.5|Probability of true (0.0 to 1.0)|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据