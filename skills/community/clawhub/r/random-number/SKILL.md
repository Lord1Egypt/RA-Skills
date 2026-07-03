---
name: 随机数生成工具
description: 提供伪随机和加密安全的随机数生成功能，包括整数、浮点数、加权选择、列表洗牌和安全令牌生成。
version: 1.0.0
---

# 随机数生成工具

提供伪随机和加密安全的随机数生成功能，包括整数、浮点数、加权选择、列表洗牌和安全令牌生成。

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
| Generate a random integer between low and high (inclusive).

Args:
    low: Lower bound (inclusive)
    high: Upper bound (inclusive)

Returns:
    Random integer between low and high | `scripts.tools.random_int` |
| Generate a random float between low and high.

Args:
    low: Lower bound (default 0.0)
    high: Upper bound (default 1.0)

Returns:
    Random float between low and high | `scripts.tools.random_float` |
| Choose k items from population with replacement, optionally weighted.

Args:
    population: List of items to choose from
    k: Number of items to choose (default 1)
    weights: Optional weights for each item (default None for equal weights)

Returns:
    List of k chosen items | `scripts.tools.random_choices` |
| Return a new list with items in random order.

Args:
    items: List of items to shuffle

Returns:
    New list with items in random order | `scripts.tools.random_shuffle` |
| Choose k unique items from population without replacement.

Args:
    population: List of items to choose from
    k: Number of items to choose

Returns:
    List of k unique chosen items | `scripts.tools.random_sample` |
| Generate a secure random hex token.

Args:
    nbytes: Number of random bytes to generate (default 32)

Returns:
    Hex string containing 2*nbytes characters | `scripts.tools.secure_token_hex` |
| Generate a secure random integer below upper_bound.

Args:
    upper_bound: Upper bound (exclusive)

Returns:
    Random integer in range [0, upper_bound) | `scripts.tools.secure_random_int` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.random_int
工具描述：Generate a random integer between low and high (inclusive).

Args:
    low: Lower bound (inclusive)
    high: Upper bound (inclusive)

Returns:
    Random integer between low and high
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|low|integer|true| |null|
|high|integer|true| |null|

---

## scripts.tools.random_float
工具描述：Generate a random float between low and high.

Args:
    low: Lower bound (default 0.0)
    high: Upper bound (default 1.0)

Returns:
    Random float between low and high
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|low|number|false|0.0|null|
|high|number|false|1.0|null|

---

## scripts.tools.random_choices
工具描述：Choose k items from population with replacement, optionally weighted.

Args:
    population: List of items to choose from
    k: Number of items to choose (default 1)
    weights: Optional weights for each item (default None for equal weights)

Returns:
    List of k chosen items
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|population|array|true| |null|
|k|integer|false|1.0|null|
|weights|null|false| |null|

---

## scripts.tools.random_shuffle
工具描述：Return a new list with items in random order.

Args:
    items: List of items to shuffle

Returns:
    New list with items in random order
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|items|array|true| |null|

---

## scripts.tools.random_sample
工具描述：Choose k unique items from population without replacement.

Args:
    population: List of items to choose from
    k: Number of items to choose

Returns:
    List of k unique chosen items
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|population|array|true| |null|
|k|integer|true| |null|

---

## scripts.tools.secure_token_hex
工具描述：Generate a secure random hex token.

Args:
    nbytes: Number of random bytes to generate (default 32)

Returns:
    Hex string containing 2*nbytes characters
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|nbytes|integer|false|32.0|null|

---

## scripts.tools.secure_random_int
工具描述：Generate a secure random integer below upper_bound.

Args:
    upper_bound: Upper bound (exclusive)

Returns:
    Random integer in range [0, upper_bound)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|upper_bound|integer|true| |null|

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