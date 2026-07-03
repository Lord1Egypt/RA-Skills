---
name: 农历日历服务
description: 一个基于Python 3.12和lunar-python的中国传统农历日历功能服务器，提供八字计算、日历转换、黄历查询等功能。
version: 1.0.0
---

# 农历日历服务

一个基于Python 3.12和lunar-python的中国传统农历日历功能服务器，提供八字计算、日历转换、黄历查询等功能。

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
| 
Calculate BaZi (Eight Characters) for fortune telling / 计算生辰八字用于算命

Args:
    birth_date: Birth date in YYYY-MM-DD format / 出生日期，格式YYYY-MM-DD
    birth_time: Birth time in HH:MM format / 出生时间，格式HH:MM

Returns:
    Detailed BaZi calculation result / 详细的八字计算结果
 | `scripts.tools.bazi_calculate` |
| 
Convert between solar and lunar calendar / 公历农历互转

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD
    convert_to: Convert to "lunar" or "solar" / 转换为"lunar"或"solar"
    is_leap: Is leap month (only for lunar to solar conversion) / 是否闰月（仅用于农历转公历）

Returns:
    Calendar conversion result / 历法转换结果
 | `scripts.tools.calendar_convert` |
| 
Query Chinese almanac (Huangli) for a specific date / 查询指定日期的黄历信息

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD

Returns:
    Detailed almanac information / 详细的黄历信息
 | `scripts.tools.huangli_query` |
| 
Get daily fortune and recommendations / 获取每日运势和建议

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD

Returns:
    Daily fortune analysis / 每日运势分析
 | `scripts.tools.fortune_daily` |
| 
Query 24 solar terms (Jie Qi) for a year / 查询一年的二十四节气

Args:
    year: Year to query / 查询的年份

Returns:
    List of solar terms for the year / 该年的节气列表
 | `scripts.tools.jieqi_query` |
| 
Analyze Wu Xing (Five Elements) from birth info / 根据出生信息分析五行

Args:
    birth_date: Birth date in YYYY-MM-DD format / 出生日期，格式YYYY-MM-DD
    birth_time: Birth time in HH:MM format / 出生时间，格式HH:MM

Returns:
    Wu Xing analysis result / 五行分析结果
 | `scripts.tools.wuxing_analyze` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.bazi_calculate
工具描述：
Calculate BaZi (Eight Characters) for fortune telling / 计算生辰八字用于算命

Args:
    birth_date: Birth date in YYYY-MM-DD format / 出生日期，格式YYYY-MM-DD
    birth_time: Birth time in HH:MM format / 出生时间，格式HH:MM

Returns:
    Detailed BaZi calculation result / 详细的八字计算结果

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|birth_date|string|true| |null|
|birth_time|string|true| |null|

---

## scripts.tools.calendar_convert
工具描述：
Convert between solar and lunar calendar / 公历农历互转

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD
    convert_to: Convert to "lunar" or "solar" / 转换为"lunar"或"solar"
    is_leap: Is leap month (only for lunar to solar conversion) / 是否闰月（仅用于农历转公历）

Returns:
    Calendar conversion result / 历法转换结果

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|true| |null|
|convert_to|string|true| |null|
|is_leap|boolean|false|false|null|

---

## scripts.tools.huangli_query
工具描述：
Query Chinese almanac (Huangli) for a specific date / 查询指定日期的黄历信息

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD

Returns:
    Detailed almanac information / 详细的黄历信息

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|true| |null|

---

## scripts.tools.fortune_daily
工具描述：
Get daily fortune and recommendations / 获取每日运势和建议

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD

Returns:
    Daily fortune analysis / 每日运势分析

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|true| |null|

---

## scripts.tools.jieqi_query
工具描述：
Query 24 solar terms (Jie Qi) for a year / 查询一年的二十四节气

Args:
    year: Year to query / 查询的年份

Returns:
    List of solar terms for the year / 该年的节气列表

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|year|integer|true| |null|

---

## scripts.tools.wuxing_analyze
工具描述：
Analyze Wu Xing (Five Elements) from birth info / 根据出生信息分析五行

Args:
    birth_date: Birth date in YYYY-MM-DD format / 出生日期，格式YYYY-MM-DD
    birth_time: Birth time in HH:MM format / 出生时间，格式HH:MM

Returns:
    Wu Xing analysis result / 五行分析结果

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|birth_date|string|true| |null|
|birth_time|string|true| |null|

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