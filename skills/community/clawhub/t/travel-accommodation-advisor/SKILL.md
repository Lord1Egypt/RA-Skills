---
name: travel-accommodation-advisor
description: 围绕已知地标通过 POI 锚定和半径筛选查找并对比附近酒店。适用于用户明确景点、商圈、交通枢纽或会展中心，并希望按距离与质量排序获得可预订住宿。
compatibility: 需要 flyai-cli、Node 运行环境，以及访问 FlyAI/Fliggy 数据端点的网络能力。
homepage: https://open.fly.ai/
metadata:
  version: 1.0.0
---

# 住宿顾问

## 何时使用
- 用户已明确目标地标（景点、商圈、车站、机场或会展中心）。
- 用户对当地地理不熟悉，希望以地标为锚点快速圈定住宿范围。
- 目标是输出可比较、可预订的酒店候选，而不是泛化的旅行建议。

## 输入/输出约定
- **最小输入**：`city`、`landmark keyword`、`check-in date`、`check-out date`。
- **增强输入**：`radius`、`budget`、`hotel stars`、`sorting preference`。
- **最小输出**：推荐结论、对比表、酒店图片行、预订链接行。
- **链接约束**：酒店预订链接必须使用 `detailUrl` 字段。

## 快速开始

1. **安装 CLI**：`npm i -g @fly-ai/flyai-cli`
2. **验证环境**：执行 `flyai fliggy-fast-search --query "三亚有什么可玩"` 并确认输出 JSON。
3. **查看命令**：执行 `flyai --help`。
4. **查看参数说明**：阅读 **`references/`** 中文档，确认必填/选填参数与字段映射。

## 配置说明
该工具可在无 API Key 情况下试用。若需要增强效果，可配置可选密钥：

```
flyai config set FLYAI_API_KEY "your-key"
```

## 核心流程（最小可执行路径）
1. 确认地标锚点（POI）：
   - `flyai search-poi --city-name "<city>" --keyword "<landmark>"`
2. 拉取地标周边酒店：
   - `flyai search-hotels --dest-name "<city>" --poi-name "<landmark>" --check-in-date <yyyy-mm-dd> --check-out-date <yyyy-mm-dd> --sort <distance_asc|rate_desc> --max-price <budget>`
3. 执行半径筛选：
   - 若有经纬度：按 `distanceKm <= radiusKm` 计算并过滤
   - 若无经纬度：保留 `distance_asc` 排序，并标注“近似半径”

## 输出规则（强约束）
- 使用 Markdown 标题、要点和对比表。
- 若存在图片字段，先输出图片行：`![]({mainPic|picUrl})`
- 然后输出预订链接行：
  - `search-hotels` -> `[Click to book]({detailUrl})`
  - 其他 -> `[Click to book]({jumpUrl})`

## 详细参考
- 场景化方案与参数速查：`references/playbooks.md`
- 问询清单、参数模板与输出模板：`references/templates.md`
- 失败兜底与重试策略：`references/fallbacks.md`
- 执行日志模板：`references/runbook.md`
