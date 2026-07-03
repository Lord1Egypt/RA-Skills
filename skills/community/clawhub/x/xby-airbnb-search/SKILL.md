---
name: Airbnb搜索扩展
description: 一个提供高级筛选功能和详细房源信息的Airbnb搜索桌面扩展，适用于旅行规划和房源研究。
version: 1.0.0
---

# Airbnb搜索扩展

一个提供高级筛选功能和详细房源信息的Airbnb搜索桌面扩展，适用于旅行规划和房源研究。

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
| Search for Airbnb listings with various filters and pagination. Provide direct links to the user | `scripts.tools.airbnb_search` |
| Get detailed information about a specific Airbnb listing. Provide direct links to the user | `scripts.tools.airbnb_listing_details` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.airbnb_search
工具描述：Search for Airbnb listings with various filters and pagination. Provide direct links to the user
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|location|string|true| |Location to search for (city, state, etc.)|
|placeId|string|false| |Google Maps Place ID (overrides the location parameter)|
|checkin|string|false| |Check-in date (YYYY-MM-DD)|
|checkout|string|false| |Check-out date (YYYY-MM-DD)|
|adults|number|false| |Number of adults|
|children|number|false| |Number of children|
|infants|number|false| |Number of infants|
|pets|number|false| |Number of pets|
|minPrice|number|false| |Minimum price for the stay|
|maxPrice|number|false| |Maximum price for the stay|
|cursor|string|false| |Base64-encoded string used for Pagination|
|ignoreRobotsText|boolean|false| |Ignore robots.txt rules for this request|

---

## scripts.tools.airbnb_listing_details
工具描述：Get detailed information about a specific Airbnb listing. Provide direct links to the user
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|id|string|true| |The Airbnb listing ID|
|checkin|string|false| |Check-in date (YYYY-MM-DD)|
|checkout|string|false| |Check-out date (YYYY-MM-DD)|
|adults|number|false| |Number of adults|
|children|number|false| |Number of children|
|infants|number|false| |Number of infants|
|pets|number|false| |Number of pets|
|ignoreRobotsText|boolean|false| |Ignore robots.txt rules for this request|

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