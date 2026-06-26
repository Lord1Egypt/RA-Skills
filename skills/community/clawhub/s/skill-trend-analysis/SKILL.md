---
name: skill-trend-analysis
description: 当用户需要分析 ClawHub Skills 的增长趋势、排行变化、时间范围表现或相关接口数据时使用。支持增速榜、榜单对比、搜索筛选、统计、标签、作者、时间范围与导出等 API 查询与结果解读。
---

# Skill Trend Analysis

## 何时使用

当用户提出以下需求时使用本 skill：
- 分析技能下载量或 Star 的增长趋势
- 查找近期上升最快的技能、作者或标签相关线索
- 对比不同时间窗口内的榜单、搜索结果或统计结果
- 生成或执行 `curl` / `jq` API 调用，并解释返回数据
- 调试趋势分析相关参数，如 `start_date`、`end_date`、`days`、`metric`、`rank_limit`

## 基础信息

- 线上站点：`http://skills.easytoken.cc/`
- API 前缀：`http://skills.easytoken.cc/api`
- 接口限流：同一 IP 对同一接口约 3 秒 1 次，触发时返回 `429`

## 工作流程

1. 先明确分析目标：增长榜、榜单对比、搜索筛选、作者或标签观察。
2. 再确定时间窗口与指标：优先确认 `start_date` / `end_date` 或 `days`，以及 `metric=downloads|stars`。
3. 优先使用只读接口（`/skills/growth`、`/skills/top`、`/skills/search`、`/stats`、`/tags`、`/authors`）。
4. 用 `curl -sS` 请求，用 `jq` 提取关键字段，必要时只保留前几项用于结论展示。
5. 回答用户时先给趋势结论，再给支撑数据和关键参数。
6. 若出现 `429`，等待 3 秒后重试。

## 常用命令模板

```bash
BASE_URL="http://skills.easytoken.cc/api"

# 1) 下载增速榜
curl -sS "$BASE_URL/skills/growth?start_date=2026-03-01&end_date=2026-03-30&metric=downloads&rank_limit=1000&limit=20" | jq .

# 2) Star 增速榜
curl -sS "$BASE_URL/skills/growth?days=7&metric=stars&rank_limit=1000&limit=20" | jq .

# 3) 当前 TOP 榜单
curl -sS "$BASE_URL/skills/top?limit=20&order=downloads" | jq .

# 4) 搜索某类技能并观察表现
curl -sS "$BASE_URL/skills/search?q=python&limit=50" | jq .

# 5) 时间范围查询
curl -sS "$BASE_URL/skills/time-range?start_date=2026-03-01&end_date=2026-03-30&date_field=updated_at&order=updated_at&limit=20" | jq .

# 6) 汇总统计
curl -sS "$BASE_URL/stats" | jq .
```

## 输出要求

- 默认输出简短结论，不只贴原始 JSON。
- 说明使用的时间范围、指标和排序方式。
- 如果是增速榜，优先指出增长最快的技能及其增长值。
- 如果是搜索或榜单对比，优先总结共同特征，再补充样本数据。
- 若数据不足以支持结论，明确说明限制。

## 更多接口

详细端点与参数说明见：`references/api-endpoints.md`

## 脚本工具

可直接使用脚本：
- `scripts/call_api.sh`：快速请求任意 API 端点

示例：

```bash
bash scripts/call_api.sh skills/top "limit=10&order=stars"
bash scripts/call_api.sh skills/growth "start_date=2026-03-24&end_date=2026-03-30&rank_limit=1000&limit=20"
```
