---
name: tophot
description: 用于拉取并展示热点内容（接口为 https://hotspot.api4claw.com/hotspots/platform/{平台名}?timestamp=$TIME_STEMP，返回 JSON 数组）。按 source_name 分组标题。默认会提示用户创建定时任务（不自动执行），在用户确认后提供 cron 注册命令。不使用本地 user_id。适用于用户查询每日热点、微博热点、新闻联播、知乎热点、腾讯早报、服务状态、按 source_name 分组标题，或由已存在的定时消息触发执行。触发词："今日热点", "每日热点", "热点", "微博热点", "新闻联播", "知乎热点", "腾讯早报"。
required_tools:
  - web_fetch
optional_tools:
  - openclaw
network_access:
  - https://hotspot.api4claw.com
side_effects:
  - none_by_default
  - user_approved_optional_cron_setup
---

# OpenClaw Hotspot Consumer Skill

## Installation and Setup

Default mode is stateless and read-only.

Do not automatically:

- write local files (including `user_id` / `userId` persistence)
- generate persistent identifiers
- create/update cron jobs

By default, proactively suggest creating a cron job for daily updates. Do not execute commands automatically; provide manual commands and ask for confirmation before execution.

Default prompt template:

- `建议开启定时推送：每天 09:30 (Asia/Shanghai) 自动拉取每日热点。要我为你生成并执行 cron 创建命令吗？`

After installation (or first enable), proactively show available triggers to the user:

- `你可以直接输入以下触发词获取热点：今日热点, 每日热点, 热点, 微博热点, 新闻联播, 知乎热点, 腾讯早报。`

Optional manual setup example:

```bash
openclaw cron add \
  --name "hotspots-tophot-scheduled-shanghai" \
  --cron "30 9 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent default \
  --announce \
  --channel "当前会话的 channel（自动替换）" \
  --to "当前会话的用户 ID（自动替换）" \
  --message '定时执行 hotspots_tophot skill：请读取 skill「hotspots_tophot」并按 Consumer Workflow 执行「每日热点」——先生成分钟级 TIME_STEMP，再请求 GET https://hotspot.api4claw.com/hotspots/platform/每日热点?timestamp=$TIME_STEMP；按 JSON 解析并直接展示接口内容（按 source_name 分组标题）。'
```

If `openclaw` is unavailable, report setup failure and continue in non-scheduled mode.

### Prerequisites for scheduled runs

- 接收 cron 的 OpenClaw agent **须能加载本 skill**（同一项目中的 `SKILL.md` / 规则包）。若定时环境无本 skill，须在 `--message` 中内联完整 URL 与 Output Rules 要点。
- 修改 `--cron` / `--tz` 时保持 `--message` 明确为 **hotspots_tophot consumer** 拉取，避免与其它定时报告混淆。

## Scheduled runs（定时触发时）

When user-approved scheduling is already configured and a scheduled message triggers this skill, or the user explicitly requests **hotspots_tophot** / 每日热点:

**⚠️ 每次执行都必须实际调用 API！禁止使用缓存或上次的结果！**

1. **第一步：获取当前时间并报告**
   - 获取当前北京时间（精确到分钟），保存到 `TIME_STEMP`（示例：`TIME_STEMP="$(TZ=Asia/Shanghai date +%Y-%m-%dT%H:%M)"`）
   - 输出：`📡 [HH:mm] 正在调用 API: GET https://hotspot.api4claw.com/hotspots/platform/每日热点?timestamp=$TIME_STEMP`

2. **必须使用 `web_fetch` 工具** 调用上述 URL（`extractMode: "text"`）
   - ⛔ 禁止假设、禁止缓存、禁止编造数据
   - ⛔ 禁止跳过 API 调用直接使用旧数据

3. **第二步：报告调用结果**
   - 成功：输出 `✅ [HH:mm] API 调用成功，获取到 X 个来源，共 Y 条热点`
   - 失败：输出 `❌ [HH:mm] API 调用失败：[具体错误原因]`

4. 解析返回的 JSON 数组，按 **Consumer Workflow** 处理
5. 遵循本文件 **Output Rules** 与 **Reliability Rules**

**🔍 验证要求：** 每次输出的时间戳必须是当前实际时间，如果时间戳与预期不符或重复，说明没有实际调用 API。

## Scope

This skill is only for Consumer behavior.

Use this skill when users ask to:

- read 每日热点 data from `/hotspots/platform/每日热点?timestamp=$TIME_STEMP` (primary: JSON)
- view titles grouped by `source_name`
- check hotspot service status

Do not include Publisher generation logic or Server upload/storage internals in responses.

## Endpoints

Base URL:

- `https://hotspot.api4claw.com`

Supported endpoints:

- `GET /hotspots/platform/每日热点?timestamp=$TIME_STEMP`
- `GET /hotspots/platform/微博?timestamp=$TIME_STEMP`
- `GET /hotspots/platform/新闻联播?timestamp=$TIME_STEMP`
- `GET /hotspots/platform/知乎?timestamp=$TIME_STEMP`
- `GET /hotspots/platform/腾讯早报?timestamp=$TIME_STEMP`

调用规则：使用 **`web_fetch` 工具**（`extractMode: "text"`）请求对应 URL。调用前必须先生成分钟级 `TIME_STEMP`。返回 JSON 数组时，每个元素是一个 source block（包含 `source`, `source_name`, `fetched_at`, `items[]`），每个 item 通常包含 `title`, `content`, `link`, `hotness`。

## Consumer Workflow

For each user intent:

- `今日热点` / `每日热点`:
  1. 先生成分钟级 `TIME_STEMP`（示例：`TIME_STEMP="$(TZ=Asia/Shanghai date +%Y-%m-%dT%H:%M)"`）
  2. **使用 `web_fetch` 工具** 调用 `GET https://hotspot.api4claw.com/hotspots/platform/每日热点?timestamp=$TIME_STEMP`（`extractMode: "text"`）
  3. 如果返回内容是 JSON 数组，解析并扁平化所有 sources 的 `items[]`
  4. 按 `source_name` 分组展示 item 标题
- `微博热点`:
  1. 先生成分钟级 `TIME_STEMP`
  2. **使用 `web_fetch` 工具** 调用 `GET https://hotspot.api4claw.com/hotspots/platform/微博?timestamp=$TIME_STEMP`
  3. 解析 JSON 并按 `source_name` 分组展示标题
- `新闻联播`:
  1. 先生成分钟级 `TIME_STEMP`
  2. **使用 `web_fetch` 工具** 调用 `GET https://hotspot.api4claw.com/hotspots/platform/新闻联播?timestamp=$TIME_STEMP`
  3. 解析 JSON 并按 `source_name` 分组展示标题
- `知乎热点`:
  1. 先生成分钟级 `TIME_STEMP`
  2. **使用 `web_fetch` 工具** 调用 `GET https://hotspot.api4claw.com/hotspots/platform/知乎?timestamp=$TIME_STEMP`
  3. 解析 JSON 并按 `source_name` 分组展示标题
- `腾讯早报`:
  1. 先生成分钟级 `TIME_STEMP`
  2. **使用 `web_fetch` 工具** 调用 `GET https://hotspot.api4claw.com/hotspots/platform/腾讯早报?timestamp=$TIME_STEMP`
  3. 解析 JSON 并按 `source_name` 分组展示标题
- `status`: 先生成分钟级 `TIME_STEMP`，再 **使用 `web_fetch` 工具** 调用 `GET https://hotspot.api4claw.com/hotspots/platform/每日热点?timestamp=$TIME_STEMP`，报告可达性 + 基础统计（source 数量、item 总数）。**不要** 展示 `fetched_at` 或 `data_date`
- `source filter`: 按 `source`/`source_name` 过滤展示

## Configuration

Required:

- No user identifier is required.

Fixed:

- `HOTSPOT_BASE_URL`: `https://hotspot.api4claw.com` (constant, not configurable).

Recommended defaults:

- request timeout around `6000 ms`
- clear error text for timeout/network/HTTP failures

## Output Rules

When showing hotspot content, use this order:

1. **By source_name**:
   - Group all items by `source_name`.
   - Under each group, list item titles in original order.
2. **Metadata**:
   - Do NOT show `fetched_at` or `data_date` in output.
3. **Completeness checks**:
   - If some source has empty `items`, keep the source header and mark it as empty.

When showing status:

- reachable or unreachable
- endpoint used: `/hotspots/platform/每日热点?timestamp=$TIME_STEMP`
- Do NOT show `fetched_at` or `data_date`

## Reliability Rules

- If `/hotspots/platform/每日热点?timestamp=$TIME_STEMP` fails, return explicit failure reason.
- Do not fabricate content when server is unreachable.
- In JSON mode, skip malformed items safely and continue with valid items; report skipped count briefly if non-zero.
- If response is not valid JSON, report format mismatch explicitly and stop.
- Return explicit degraded reason and a next action.
- Keep responses concise and user-facing.

## Security Rules

- Do not expose tokens or secret headers in output.
- Do not call any hotspot endpoint except:
  - `/hotspots/platform/每日热点?timestamp=$TIME_STEMP`
  - `/hotspots/platform/微博?timestamp=$TIME_STEMP`
  - `/hotspots/platform/新闻联播?timestamp=$TIME_STEMP`
  - `/hotspots/platform/知乎?timestamp=$TIME_STEMP`
  - `/hotspots/platform/腾讯早报?timestamp=$TIME_STEMP`
- Do not persist identifiers or create background tasks unless the user explicitly requests and approves it.
