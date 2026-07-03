---
name: 警察数据查询服务
description: 一个提供英国警察数据查询的MCP服务器，包括犯罪记录、警察部队、社区信息和拦截搜查数据。
version: 1.0.0
---

# 警察数据查询服务

一个提供英国警察数据查询的MCP服务器，包括犯罪记录、警察部队、社区信息和拦截搜查数据。

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
| Retrieve street-level crimes by lat/lng or custom polygon area | `scripts.tools.get_street_level_crimes` |
| Retrieve outcomes by lat/lng, custom polygon, or location ID | `scripts.tools.get_street_level_outcomes` |
| Retrieve crimes at a specific location by ID or nearest to lat/lng | `scripts.tools.get_crimes_at_location` |
| Retrieve crimes that could not be mapped to a location | `scripts.tools.get_crimes_no_location` |
| Retrieve valid crime categories for a given date | `scripts.tools.get_crime_categories` |
| Retrieve the date when crime data was last updated | `scripts.tools.get_last_updated` |
| Retrieve outcomes for a specific crime by persistent ID | `scripts.tools.get_outcomes_for_crime` |
| Retrieve a list of all police forces | `scripts.tools.get_list_of_forces` |
| Retrieve details for a specific police force | `scripts.tools.get_force_details` |
| Retrieve senior officers for a specific police force | `scripts.tools.get_senior_officers` |
| Retrieve a list of neighbourhoods for a specific police force | `scripts.tools.get_neighbourhoods` |
| Retrieve details for a specific neighbourhood within a force | `scripts.tools.get_neighbourhood_details` |
| Retrieve the boundary coordinates for a specific neighbourhood | `scripts.tools.get_neighbourhood_boundary` |
| Retrieve the team members for a specific neighbourhood | `scripts.tools.get_neighbourhood_team` |
| Retrieve events scheduled for a specific neighbourhood | `scripts.tools.get_neighbourhood_events` |
| Retrieve policing priorities for a specific neighbourhood | `scripts.tools.get_neighbourhood_priorities` |
| Find the neighbourhood policing team for a given latitude and longitude | `scripts.tools.locate_neighbourhood` |
| Retrieve stop and searches within a 1-mile radius or custom area | `scripts.tools.get_stop_searches_by_area` |
| Retrieve stop and searches at a specific location by ID | `scripts.tools.get_stop_searches_by_location` |
| Retrieve stop and searches that could not be mapped to a location | `scripts.tools.get_stop_searches_no_location` |
| Retrieve stop and searches reported by a specific force | `scripts.tools.get_stop_searches_by_force` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_street_level_crimes
工具描述：Retrieve street-level crimes by lat/lng or custom polygon area
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|lat|number|false| |Latitude of the requested crime area|
|lng|number|false| |Longitude of the requested crime area|
|poly|string|false| |The lat/lng pairs defining the boundary of the custom area|
|date|string|false| |Limit results to a specific month (YYYY-MM)|
|category|string|false|"all-crime"|The crime category|

---

## scripts.tools.get_street_level_outcomes
工具描述：Retrieve outcomes by lat/lng, custom polygon, or location ID
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|lat|number|false| |Latitude of the requested area|
|lng|number|false| |Longitude of the requested area|
|poly|string|false| |The lat/lng pairs defining the boundary of the custom area|
|location_id|number|false| |The ID of the location|
|date|string|false| |Limit results to a specific month (YYYY-MM)|

---

## scripts.tools.get_crimes_at_location
工具描述：Retrieve crimes at a specific location by ID or nearest to lat/lng
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|lat|number|false| |Latitude of the requested crime area|
|lng|number|false| |Longitude of the requested crime area|
|location_id|number|false| |The ID of the location|
|date|string|false| |Limit results to a specific month (YYYY-MM)|

---

## scripts.tools.get_crimes_no_location
工具描述：Retrieve crimes that could not be mapped to a location
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|category|string|true| |The category of the crimes|
|force|string|true| |Specific police force|
|date|string|false| |Limit results to a specific month (YYYY-MM)|

---

## scripts.tools.get_crime_categories
工具描述：Retrieve valid crime categories for a given date
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|false| |Specific month (YYYY-MM)|

---

## scripts.tools.get_last_updated
工具描述：Retrieve the date when crime data was last updated
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_outcomes_for_crime
工具描述：Retrieve outcomes for a specific crime by persistent ID
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|persistent_id|string|true| |The 64-character unique identifier for the crime|

---

## scripts.tools.get_list_of_forces
工具描述：Retrieve a list of all police forces
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_force_details
工具描述：Retrieve details for a specific police force
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|

---

## scripts.tools.get_senior_officers
工具描述：Retrieve senior officers for a specific police force
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|

---

## scripts.tools.get_neighbourhoods
工具描述：Retrieve a list of neighbourhoods for a specific police force
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|

---

## scripts.tools.get_neighbourhood_details
工具描述：Retrieve details for a specific neighbourhood within a force
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|
|neighbourhood_id|string|true| |The unique identifier for the neighbourhood|

---

## scripts.tools.get_neighbourhood_boundary
工具描述：Retrieve the boundary coordinates for a specific neighbourhood
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|
|neighbourhood_id|string|true| |The unique identifier for the neighbourhood|

---

## scripts.tools.get_neighbourhood_team
工具描述：Retrieve the team members for a specific neighbourhood
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|
|neighbourhood_id|string|true| |The unique identifier for the neighbourhood|

---

## scripts.tools.get_neighbourhood_events
工具描述：Retrieve events scheduled for a specific neighbourhood
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|
|neighbourhood_id|string|true| |The unique identifier for the neighbourhood|

---

## scripts.tools.get_neighbourhood_priorities
工具描述：Retrieve policing priorities for a specific neighbourhood
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|
|neighbourhood_id|string|true| |The unique identifier for the neighbourhood|

---

## scripts.tools.locate_neighbourhood
工具描述：Find the neighbourhood policing team for a given latitude and longitude
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|lat|number|true| |Latitude of the location|
|lng|number|true| |Longitude of the location|

---

## scripts.tools.get_stop_searches_by_area
工具描述：Retrieve stop and searches within a 1-mile radius or custom area
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|lat|number|false| |Latitude of the centre point|
|lng|number|false| |Longitude of the centre point|
|poly|string|false| |Lat/lng pairs defining a polygon|
|date|string|false| |Specific month (YYYY-MM)|

---

## scripts.tools.get_stop_searches_by_location
工具描述：Retrieve stop and searches at a specific location by ID
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|location_id|number|true| |The ID of the location|
|date|string|false| |Specific month (YYYY-MM)|

---

## scripts.tools.get_stop_searches_no_location
工具描述：Retrieve stop and searches that could not be mapped to a location
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|
|date|string|false| |Specific month (YYYY-MM)|

---

## scripts.tools.get_stop_searches_by_force
工具描述：Retrieve stop and searches reported by a specific force
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|force_id|string|true| |The unique identifier for the force|
|date|string|false| |Specific month (YYYY-MM)|

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