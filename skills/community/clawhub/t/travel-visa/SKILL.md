---
name: travel-visa
description: 面向出境旅行的签证办理咨询与行前核验顾问。适用于用户已知目的国家/地区，希望快速获得签证要求、办理地点与行程衔接建议。
compatibility: 需要 flyai-cli、Node 运行环境，以及访问 FlyAI/Fliggy 数据端点的网络能力。
homepage: https://open.fly.ai/
metadata:
  version: 1.0.0
---

# 旅行签证顾问

## 何时使用
- 用户准备出境旅行，但不确定签证是否需要、办理材料或办理地点。
- 用户已确定目的地，想把签证办理与机票/住宿安排联动决策。
- 目标是输出可执行的签证办理与行前准备清单，而不是泛化旅行建议。

## 输入/输出约定
- **最小输入**：`departure country/region`、`destination country/region`、`passport nationality`、`planned departure date`。
- **增强输入**：`stay duration`、`entry count`、`first arrival city`、`preferred processing city`。
- **最小输出**：结论摘要、办理路径、材料清单、时间线建议、领馆/签证中心信息。
- **链接约束**：酒店预订链接必须使用 `detailUrl`，其他场景链接使用 `jumpUrl`。

## 快速开始
1. **安装 CLI**：`npm i -g @fly-ai/flyai-cli`
2. **验证环境**：执行 `flyai fliggy-fast-search --query "中国护照去日本旅游签证要求"` 并确认输出 JSON。
3. **查看命令**：执行 `flyai --help`。
4. **查看参数说明**：阅读 **`references/`** 中文档，确认问询模板、命令模板与兜底策略。

## 配置说明
该工具可在无 API Key 情况下试用。若需要增强效果，可配置可选密钥：

```
flyai config set FLYAI_API_KEY "your-key"
```

## 核心流程（最小可执行路径）
1. 核验签证政策与办理要求（自然语言检索）：
   - `flyai fliggy-fast-search --query "<国籍> 护照去 <目的地> 旅游签证要求 材料 办理时效"`
2. 锚定办理地点（领馆/签证中心 POI）：
   - `flyai search-poi --city-name "<办理城市>" --keyword "<目的地国家> 签证中心"`
3. 如需联动行程成本，补充住宿搜索：
   - `flyai search-hotels --dest-name "<办理城市>" --poi-name "<签证中心或领馆>" --check-in-date <yyyy-mm-dd> --check-out-date <yyyy-mm-dd> --sort distance_asc --max-price <budget>`

## 输出规则（强约束）
- 使用 Markdown 标题、要点、检查清单和对比表。
- 若存在图片字段，先输出图片行：`![]({mainPic|picUrl})`
- 然后输出预订/跳转链接行：
  - `search-hotels` -> `[Click to book]({detailUrl})`
  - 其他 -> `[Click to book]({jumpUrl})`

## 详细参考
- 场景化方案与参数速查：`references/playbooks.md`
- 问询清单、参数模板与输出模板：`references/templates.md`
- 失败兜底与重试策略：`references/fallbacks.md`
- 执行日志模板：`references/runbook.md`
