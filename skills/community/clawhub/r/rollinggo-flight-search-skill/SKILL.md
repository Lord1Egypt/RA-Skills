---
name: rollinggo-searchflight
description: 使用 RollingGo Flight CLI 查询机场代码和机票结果。当用户需要搜索机票、查询机场三字码、按出发地 / 到达地 / 日期 / 舱位 / 往返类型筛选航班，或围绕飞行出行做结构化查询时触发本技能。触发短语——"查机票"、"搜索机票"、"查航班"、"查机场代码"、"北京到上海机票"、"往返商务舱"、"rollinggo-flight"。
homepage: https://rollinggo.store
metadata:
  {
    "openclaw": {
      "emoji": "✈️",
      "skillKey": "rollinggo-searchflight",
      "primaryEnv": "ROLLINGGO_API_KEY",
      "requires": {
        "anyBins": ["rollinggo-flight", "npx", "node", "uvx", "uv"],
        "env": ["ROLLINGGO_API_KEY"]
      },
      "install": [
        {
          "id": "node",
          "kind": "node",
          "package": "rollinggo-flight@latest",
          "bins": ["rollinggo-flight"],
          "label": "Install rollinggo-flight (npm)"
        }
      ]
    }
  }
---

# RollingGo 机票 CLI

## 适用范围

✅ **在以下情况使用本技能：**
- **查询机场代码：** 用户需要确认城市对应的机场代码，或根据机场名 / 城市名 / 三字码查询机场信息（例如：“杭州机场代码是什么？”）。
- **搜索机票：** 用户要查询两个城市或机场之间的航班，并指定日期、舱位、人数等条件。
- **单程或往返查询：** 用户需要按 `ONE_WAY` 或 `ROUND_TRIP` 查询结构化航班结果。
- **行前规划：** 用户给出自然语言出行需求，需要先解析成机场代码，再继续搜索机票。

❌ **以下情况不适用：**
- 用户询问酒店、火车票、接送机或租车等非机票类业务。
- 用户需要值机、选座或支付下单闭环；本技能只负责搜索结果查询。

## API Key

解析顺序：`--api-key` 参数 → `ROLLINGGO_API_KEY` 环境变量。

还没有 Key？前往申请：https://rollinggo.store/apply

## 运行环境

默认加载 [references/rollinggo-flight-npx.md](references/rollinggo-flight-npx.md)；用户明确使用 `uv`/`uvx`/Python 时改加载 [references/rollinggo-flight-uvx.md](references/rollinggo-flight-uvx.md)。如果当前环境没有 Node.js 或 Python，可改用独立二进制安装方式。更完整的分步场景教程见 [references/flight-workflows.md](references/flight-workflows.md)。API Key 持久化配置见 [references/claw-host-env.md](references/claw-host-env.md)。

## 版本新鲜度（始终使用最新版）

本技能默认策略：每次执行都使用最新发布版本。

- **npm/npx：** `npx --yes rollinggo-flight@latest ...`
- **uvx：** `uvx --refresh --from rollinggo-flight@latest rollinggo-flight ...`

## 主要工作流

除非用户已经明确处在后续步骤，否则按顺序执行：

1. 明确需求：出发城市 / 机场、到达城市 / 机场、出发日期、是否往返、返程日期（若往返）、人数、舱位
2. 如果城市码或机场码不明确 → 先执行 `search-airports` 解析机场 / 城市代码
3. 执行 `search-flights` 搜索航班
4. 如果没有结果 → 放宽筛选条件后重试

## 常用命令速查

```bash
# 查询机场 / 城市代码
rollinggo-flight search-airports --api-key <key> --keyword "Hangzhou"

# 搜索机票（最少必填参数）
rollinggo-flight search-flights \
  --api-key <key> \
  --from-city <code> \
  --to-city <code> \
  --from-date YYYY-MM-DD \
  --trip-type ONE_WAY \
  --adult-number 1 \
  --child-number 0 \
  --cabin-grade ECONOMY

# 查看所有可用参数
rollinggo-flight search-airports --help
rollinggo-flight search-flights --help
```

## 关键规则

- `--trip-type` 必须是精确值：`ONE_WAY` 或 `ROUND_TRIP`
- 当 `--trip-type` 为 `ROUND_TRIP` 时，`--ret-date` 为必填
- `--cabin-grade` 只能是：`ECONOMY`、`PREMIUM_ECONOMY`、`BUSINESS`、`FIRST`
- 出发地使用 `--from-city` 或 `--from-airport` 二选一；到达地同理
- `--from-city` / `--to-city` 接收城市代码（如 `BJS`、`SHA`）；`--from-airport` / `--to-airport` 接收机场三字码（如 `PEK`、`PVG`）
- `--adult-number` 必须 ≥ 1；`--child-number` 必须 ≥ 0
- 日期格式必须为 `YYYY-MM-DD`

## 输出说明

- stdout → 结果数据（默认 JSON）
- stderr → 仅错误信息
- 退出码 `0` 成功 · `1` HTTP/网络失败 · `2` CLI 参数校验失败

## 无结果时的放宽策略

按顺序尝试：改用同城其他机场 → 尝试相邻日期 → 降低或调整舱位要求 → 改用城市代码而不是机场代码
