---
name: 八字计算器
description: 八字 MCP 是一款基于 AI 的八字计算器，提供精准的八字排盘数据，用于性格分析和命运预测。
version: 1.0.0
---

# 八字计算器

八字 MCP 是一款基于 AI 的八字计算器，提供精准的八字排盘数据，用于性格分析和命运预测。

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
| 根据时间（公历或农历）、性别来获取八字信息。solarDatetime和lunarDatetime必须传且只传其中一个。 | `scripts.tools.getBaziDetail` |
| 根据八字获取公历时间列表。返回的时间格式为：YYYY-MM-DD hh:mm:ss。例如时间1998年7月31日下午2点整表示为：1998-07-31 14:00:00 | `scripts.tools.getSolarTimes` |
| 获取指定公历时间（默认今天）的黄历信息。 | `scripts.tools.getChineseCalendar` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.getBaziDetail
工具描述：根据时间（公历或农历）、性别来获取八字信息。solarDatetime和lunarDatetime必须传且只传其中一个。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|solarDatetime|string|false| |用ISO时间格式表示的公历时间. 例如：`2008-03-01T13:00:00+08:00`。|
|lunarDatetime|string|false| |农历时间。例如农历2000年5月初五中午12点整表示为：`2000-5-5 12:00:00`。|
|gender|number|true| |传0表示女性，传1表示男性。|
|eightCharProviderSect|number|false|2.0|早晚子时配置。传1表示23:00-23:59日干支为明天，传2表示23:00-23:59日干支为当天。|

---

## scripts.tools.getSolarTimes
工具描述：根据八字获取公历时间列表。返回的时间格式为：YYYY-MM-DD hh:mm:ss。例如时间1998年7月31日下午2点整表示为：1998-07-31 14:00:00
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|bazi|string|true| |八字，按年柱、月柱、日柱、时柱顺序，用空格隔开。例如：戊寅 己未 己卯 辛未|

---

## scripts.tools.getChineseCalendar
工具描述：获取指定公历时间（默认今天）的黄历信息。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|solarDatetime|string|false| |用ISO时间格式表示的公历时间. 例如：`2008-03-01T13:00:00+08:00`。|

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