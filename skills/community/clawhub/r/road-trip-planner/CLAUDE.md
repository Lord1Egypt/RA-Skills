# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Claude Code skill 仓库 — 基于高德地图 API 规划多日自驾游路线（仅限中国大陆）。
Skill 定义在 `SKILL.md`，依赖 [@lbs-amap/personal-map](https://clawhub.ai/lbs-amap/personal-map) skill 和 `AMAP_API_KEY` 环境变量。
本仓库不含脚本代码，API 客户端完全由外部 skill 提供。

## 架构

| 文件 | 职责 | 何时修改 |
|------|------|---------|
| `SKILL.md` | 权威 skill 定义：触发条件、完整工作流、约束表、输出模板 | 修改工作流、约束、模板 |
| `examples.md` | 完整案例（蒙东 8 日、青甘 9 日、川西 5 日） | 修改或新增示例 |
| `README.md` / `README_CN.md` | 中英文项目说明，面向用户的功能介绍 | 功能变化时同步更新 |

修改原则：`SKILL.md` 是唯一的权威定义源。`CLAUDE.md` 是本文件 — 开发者快速参考，不重复 `SKILL.md` 的细节。

## 工作流速查

详见 `SKILL.md` 的 Workflow 章节。快速记忆：

1. 确认行程框架 → 2. 按天拆分节点（≤6h/天）→ 3. 高德 API（geo→search→验证→sleep，含补给搜索）→ 4. 跨天里程补全 → 5. 去重→精简至≤16→生成二维码 → 6. 输出 Markdown 行程表

## 关键约束速查

- **依赖检查**：API 调用前必须验证 `personal-map` skill + `AMAP_API_KEY`，缺失则 fail fast。安装命令：`openclaw skills install personal-map`
- **API 错误模式**：所有 API 方法失败时返回 `{"error": ..., "message": ...}`，不抛异常。每次调用后检查 `"error"` key
- **无本地脚本**：`AMapPersonalMapClient` 由外部 `personal-map` skill 提供，canonical import 路径为 `scripts.amap_personal_map_client`
- **客户端构造**：`AMapPersonalMapClient()` 自动读取 `AMAP_API_KEY` 环境变量；也可显式传入 `AMapPersonalMapClient(api_key="...")`
- **≤16 节点**：高德个人地图限制，超限按优先级精简（详见 SKILL.md Step 5.3）
- **poiId 策略**：`maps_text_search` → 城市名重试 → 占位符 `B000000000`
- **QPS**：调用间隔 ≥ 0.3s，超限时 wait 1s 重试一次
- **每日驾驶 ≤ 6h**：高原/山区进一步压缩至 4–5h

## 常见问题（开发时参考）

- **ImportError / AMapPersonalMapClient 找不到**：检查 personal-map skill 是否安装 (`openclaw skills install personal-map`)，canonical import 路径为 `from scripts.amap_personal_map_client import AMapPersonalMapClient`
- **API 返回错误**：所有方法失败返回 dict 而非抛异常，始终检查 `"error"` key。常见错误：`CUQPS_HAS_EXCEEDED_THE_LIMIT`（等 1s 重试）、`API Key 缺失`（检查环境变量）
- **某天里程为 0**：检查跨天补全（Step 4 — 前一天终点未插入当天头部）
- **坐标跨城误匹配**：`maps_text_search` 结果与 `maps_geo` 坐标做距离验证（<30km）
- **环线不闭合**：去重时保留首尾同名终点（Step 5.2），否则路线末尾缺失
- **节点超过 16 个**：按 Step 5.3 优先级表精简，优先保留首尾锚点和用户指定景点
- **示例数据不一致**：修改 examples.md 后需同步更新设计思路中的总里程范围和节点数
- **新增功能**：先在 SKILL.md 设计工作流/约束，再修改 examples.md 补充案例，最后更新 README
