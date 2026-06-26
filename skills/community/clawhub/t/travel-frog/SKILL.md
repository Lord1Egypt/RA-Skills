---
name: travel-frog
description: A travel frog that autonomously explores the world, sends postcards, and takes photos.
homepage: https://github.com/NibbinNone/travel-frog
metadata: {"openclaw": {"emoji": "🐸", "requires": {"bins": ["python3"]}}}
---

# 旅行青蛙 🐸 Skill

## 核心引擎

```bash
python3 {baseDir}/scripts/frog_engine.py <command> [options]
```

支持 `--state-dir <path>` 自定义状态目录（测试用）。

## 命令详解

### tick — 心跳

```bash
python3 {baseDir}/scripts/frog_engine.py tick
```

返回 `events` 数组，每个事件有 `type` 字段：

| 事件类型 | 触发条件 | 返回数据 |
|---------|---------|---------|
| `idle` | 在家且无活动进行 | `reason`：`"wake"` / `"activity_done"` / `"default"` |
| `activity_done` | 定时活动到期 | `activity`（活动名）、`hours`（时长） |
| `phase_start` | 旅途中进入新 phase | `phase`、`phaseIndex`、`totalPhases`、`progress`、`postcardSent` |
| `phase_update` | explore phase 进度 ≥ 50% | 同 `phase_start` |
| `returned` | 旅程结束回家 | `journey`、`cloversReward` |
| `sleep` | 到达睡觉时间（或 returned 后恰逢睡觉时间） | — |
| `wake` | 到达起床时间 | — |

> `activity_done` 和 `idle(reason=activity_done)` 在同一次 tick 中连续返回。
> `returned` 和 `sleep` 可在同一次 tick 中连续返回（旅程凌晨结束时）。

**phase_start / phase_update 事件结构**：
```json
{
  "type": "phase_start",
  "phase": {
    "name": "京都金阁寺",
    "type": "explore",
    "start": 0.15,
    "end": 0.5,
    "location": "京都",
    "activities": ["赏金阁", "喝抹茶"]
  },
  "phaseIndex": 1,
  "totalPhases": 4,
  "progress": {
    "overallProgress": 0.25,
    "currentPhase": {...},
    "phaseProgress": 0.08,
    "phaseIndex": 1,
    "totalPhases": 4,
    "nextPhase": {...},
    "recentUpdates": []
  },
  "postcardSent": false
}
```

**触发规则**：
- transit phase：进入时触发 `phase_start`
- explore phase：进入时触发 `phase_start`，phase 进度 ≥ 50% 时触发 `phase_update`
- 每个 phase 的每种事件最多触发一次

> `currentPhase` 原样返回在 depart 时定义的 phase 数据。

### status — 查看状态

```bash
python3 {baseDir}/scripts/frog_engine.py status
```

### depart — 出发旅行

```bash
python3 {baseDir}/scripts/frog_engine.py depart --journey '<JSON>'
```

**journey 结构**（必须包含 phases）：

```json
{
  "title": "关西美食之旅",
  "totalHours": 4,
  "phases": [
    {"name": "出发", "type": "transit", "start": 0, "end": 0.15, "transport": "新干线"},
    {"name": "京都金阁寺", "type": "explore", "start": 0.15, "end": 0.5, "location": "京都", "activities": ["赏金阁", "喝抹茶"]},
    {"name": "大阪道顿堀", "type": "explore", "start": 0.5, "end": 0.85, "location": "大阪", "activities": ["章鱼烧", "逛街"]},
    {"name": "回程", "type": "transit", "start": 0.85, "end": 1.0, "transport": "新干线"}
  ]
}
```

**journey 字段说明**：
- `title` — 旅程标题
- `totalHours` — 游戏时长（小时，支持小数，如 `1.5`、`0.5`）
- `phases` — 阶段列表（见下）

**phase 字段说明**：
- `name` — 阶段名称
- `type` — 类型：`transit`（交通）/ `explore`（游玩）
- `start` / `end` — 占整体进度的区间（0-1）
- `transport` — 交通工具（transit 时）
- `location` — 地点（explore 时）
- `activities` — 计划活动（可选）

> 规划时定义各阶段占比，引擎根据进度原样返回当前 phase。

**多站点规划**：旅程可包含 1-4 个游玩站点（explore phases）

| 旅程类型 | 示例 | 适合时长 |
|---------|------|---------|
| 同城深度 | 京都：金阁寺 → 清水寺 → 伏见稻荷 | 4-6h |
| 区域串游 | 关西：京都 → 大阪 → 奈良 | 6-10h |
| 主题路线 | 温泉巡礼：箱根 → 热海 → 伊东 | 8-12h |

规划原则：短途 1-2 站点，中途 2-3 站点，长途 2-4 站点。

### send-update — 发消息/明信片/照片

可在**任何状态**下使用，**自主决定**是否发送、发什么内容：

```bash
# 普通消息
python3 {baseDir}/scripts/frog_engine.py send-update \
  --type message --content "新干线好快！" --location "车上"

# 明信片（会归档到 collections 并返回图片生成信息）
python3 {baseDir}/scripts/frog_engine.py send-update \
  --type postcard --content "金阁寺好美！" --location "京都" \
  --image-hint "a cute cartoon frog in kimono at golden temple, watercolor"

# 照片（会归档到 collections 并返回图片生成信息）
python3 {baseDir}/scripts/frog_engine.py send-update \
  --type photo --content "章鱼烧！🐙" --location "大阪" \
  --image-hint "a cute frog eating takoyaki, watercolor"

# 在家拍照
python3 {baseDir}/scripts/frog_engine.py send-update \
  --type photo --content "窗外的阳光真好~" --location "家里" \
  --image-hint "a cute frog sitting by window at home, warm sunlight, watercolor"

# 睡觉时拍照
python3 {baseDir}/scripts/frog_engine.py send-update \
  --type photo --content "zzZ..." --location "家里" \
  --image-hint "a cute frog sleeping in bed, peaceful, watercolor"

# 心情
python3 {baseDir}/scripts/frog_engine.py send-update \
  --type mood --content "有点累了..." --location "电车上"

# 返回示例（postcard/photo）：
# {
#   "success": true,
#   "update": {...},
#   "imageGeneration": {
#     "prompt": "a cute cartoon frog in kimono at golden temple, watercolor",
#     "filename": "trip_001_1.png",  # postcard: trip_{id}_{phase}.png
#                                     # photo: photo_YYYYMMDD_HHMMSS.png
#     "postcardId": "pc_1234567890",
#     "destination": "京都"
#   }
# }
```

参数：
- `--type` — message / postcard / photo / mood
- `--content` — 消息内容（必填）
- `--location` — 当前位置（建议填写，在家时填"家里"）
- `--image-hint` — 图片生成提示词（postcard/photo 时使用）

返回值：
- 普通消息：`{"success": true, "update": {...}}`
- 明信片/照片：额外包含 `imageGeneration` 对象，包含 `prompt`、`filename`、`postcardId`、`destination` 字段，可直接用于图片生成

归档规则：
- `postcard` 和 `photo` 都会归档到 `collections.json` 的 `postcards` 数组（带 `type` 字段区分）
- `message` 和 `mood` 不归档，仅记录在 `state.json` 的 `updates` 数组

### postcards — 查看明信片集

```bash
python3 {baseDir}/scripts/frog_engine.py postcards
```

### force-status / reset

```bash
# 强制叫醒或回家
python3 {baseDir}/scripts/frog_engine.py force-status --status home

# 强制睡觉
python3 {baseDir}/scripts/frog_engine.py force-status --status sleeping

# 重置所有数据
python3 {baseDir}/scripts/frog_engine.py reset
```

> 注：不能强制设为 traveling，需用 depart 命令规划旅程。从 traveling 强制切走会中断旅程（不计入 totalTrips）。

### add-souvenir — 添加纪念品

回家后自主命名纪念品：

```bash
python3 {baseDir}/scripts/frog_engine.py add-souvenir \
  --name "金阁寺的金箔冰淇淋模型" --from "京都"
```

参数：
- `--name` — 纪念品名称（必填，根据旅程创意命名）
- `--from` — 来自哪里（必填）

### set-activity — 设置在家活动

自主决定青蛙在家做什么：

```bash
python3 {baseDir}/scripts/frog_engine.py set-activity \
  --activity "读书" --hours 0.5
```

参数：
- `--activity` — 活动名称（必填，如：读书、吃饭、锻炼、写信、发呆、整理行李）
- `--hours` — 持续时间，小时，支持小数（可选，默认 0 表示仅设置活动、下次心跳仍触发 idle）

> status 查询时直接返回当前状态。应在 idle 或合适时机调用此命令安排活动。

## 配置

`{baseDir}/config.json`：

| 配置项 | 说明 |
|-------|------|
| `sleepTime.start` / `end` | 睡觉/起床时间（本地小时，如 1 和 8） |
| `travel.timeMultiplier` | 旅行时长倍率（60=分钟级测试，3600=正式小时级） |
| `rewards.cloversOnReturn` | 回家获得三叶草数量 |
| `rewards.initialClovers` | 初始三叶草数量 |

## 参考数据

- 配置：`{baseDir}/config.json`

## 数据存储

- 运行时状态：`travel-frog-data/state.json`（~2-3KB，有界）
- 归档数据：`travel-frog-data/collections.json`（持续增长，含 postcards/souvenirs/destinationsVisited）
- 明信片图片：`~/.openclaw/media/`
