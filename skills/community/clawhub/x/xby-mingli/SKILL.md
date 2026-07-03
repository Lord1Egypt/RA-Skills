---
name: 命理分析服务
description: 一个支持多种命理系统（紫微斗数、八字等）的MCP协议服务器，为AI工具提供命理分析与运势查询功能。
version: 1.0.0
---

# 命理分析服务

一个支持多种命理系统（紫微斗数、八字等）的MCP协议服务器，为AI工具提供命理分析与运势查询功能。

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
| 获取紫微斗数排盘信息，包含命盘十二宫、主星、辅星、四化等详细信息 | `scripts.tools.get_ziwei_chart` |
| 获取紫微斗数运势信息，包含大限、流年、流月、流日、流时的运势详情 | `scripts.tools.get_ziwei_fortune` |
| 分析紫微斗数特定宫位的详细信息 | `scripts.tools.analyze_ziwei_palace` |
| 列出所有可用的命理系统（紫微斗数、八字、占星等） | `scripts.tools.list_fortune_systems` |
| 获取八字（四柱）排盘信息，包含年月日时四柱、十神、五行、地支藏干等详细信息 | `scripts.tools.get_bazi_chart` |
| 获取八字运势信息，包含大运、流年等详情 | `scripts.tools.get_bazi_fortune` |
| 分析八字五行强弱，包含五行分数、平衡度、缺失五行等 | `scripts.tools.analyze_bazi_element` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_ziwei_chart
工具描述：获取紫微斗数排盘信息，包含命盘十二宫、主星、辅星、四化等详细信息
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|true| |出生日期，格式：YYYY-MM-DD，例如：2000-08-16|
|time_index|integer|true| |出生时辰序号（0-12）|
|gender|string|true| |性别：男 或 女|
|calendar|string|false|"solar"|历法类型：solar(阳历) 或 lunar(农历)|
|is_leap_month|boolean|false|false|是否为闰月（仅当calendar=lunar时有效）|
|format|string|false|"markdown"|null|
|language|string|false|"zh-CN"|null|
|longitude|number|false| |出生地经度，用于真太阳时修正|
|latitude|number|false| |出生地纬度|
|use_solar_time|boolean|false|false|是否启用真太阳时修正|
|birth_hour|integer|false| |精确出生小时（0-23）|
|birth_minute|integer|false| |精确出生分钟（0-59）|

---

## scripts.tools.get_ziwei_fortune
工具描述：获取紫微斗数运势信息，包含大限、流年、流月、流日、流时的运势详情
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|birth_date|string|true| |出生日期，格式：YYYY-MM-DD|
|time_index|integer|true| |出生时辰序号（0-12）|
|gender|string|true| |性别：男 或 女|
|calendar|string|false|"solar"|null|
|is_leap_month|boolean|false|false|null|
|query_date|string|false| |查询运势的日期，格式：YYYY-MM-DD|
|format|string|false|"markdown"|null|
|language|string|false|"zh-CN"|null|

---

## scripts.tools.analyze_ziwei_palace
工具描述：分析紫微斗数特定宫位的详细信息
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|birth_date|string|true| |出生日期，格式：YYYY-MM-DD|
|time_index|integer|true| |出生时辰序号（0-12）|
|gender|string|true| |null|
|palace_name|string|true| |要分析的宫位名称|
|calendar|string|false|"solar"|null|
|is_leap_month|boolean|false|false|null|
|format|string|false|"markdown"|null|
|language|string|false|"zh-CN"|null|

---

## scripts.tools.list_fortune_systems
工具描述：列出所有可用的命理系统（紫微斗数、八字、占星等）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|detailed|boolean|false|false|是否输出更详细信息|

---

## scripts.tools.get_bazi_chart
工具描述：获取八字（四柱）排盘信息，包含年月日时四柱、十神、五行、地支藏干等详细信息
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|true| |出生日期，格式：YYYY-MM-DD|
|time_index|integer|true| |出生时辰序号（0-12）|
|gender|string|true| |null|
|calendar|string|false|"solar"|null|
|is_leap_month|boolean|false|false|null|
|format|string|false|"markdown"|null|
|language|string|false|"zh-CN"|null|

---

## scripts.tools.get_bazi_fortune
工具描述：获取八字运势信息，包含大运、流年等详情
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|birth_date|string|true| |出生日期，格式：YYYY-MM-DD|
|time_index|integer|true| |出生时辰序号（0-12）|
|gender|string|true| |null|
|calendar|string|false|"solar"|null|
|is_leap_month|boolean|false|false|null|
|query_date|string|false| |查询运势的日期，格式：YYYY-MM-DD|
|format|string|false|"markdown"|null|
|language|string|false|"zh-CN"|null|

---

## scripts.tools.analyze_bazi_element
工具描述：分析八字五行强弱，包含五行分数、平衡度、缺失五行等
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|birth_date|string|true| |出生日期，格式：YYYY-MM-DD|
|time_index|integer|true| |出生时辰序号（0-12）|
|gender|string|true| |null|
|calendar|string|false|"solar"|null|
|is_leap_month|boolean|false|false|null|
|format|string|false|"markdown"|null|
|language|string|false|"zh-CN"|null|

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