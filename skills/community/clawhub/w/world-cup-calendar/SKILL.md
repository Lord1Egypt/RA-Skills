---
name: world-cup-calendar
license: MIT-0
description: 将 2026 FIFA 世界杯赛程同步到飞书日历。用于用户想查看世界杯完整赛程、按北京时间创建飞书日程、把关注球队比赛提前提醒、设置日程私密且不占用忙闲状态，或维护世界杯赛程同步 Skill 时。
---

# World Cup Calendar

## 能力

使用 `scripts/world_cup_calendar.py` 读取内置赛程数据，并把比赛转换成飞书日程。

默认规则：
- 使用北京时间 `Asia/Shanghai`。
- 导入全部 104 场比赛，包含已经过去的比赛。
- 每场比赛默认 2 小时。
- 创建或使用名为 `world-cup-calendar` 的飞书日历。
- 日历权限为私密，日程 `visibility=private`。
- 日程忙闲状态为 `free`，不阻塞同事预约会议。
- 普通比赛不提醒。
- 关注球队默认 `ARG`，即阿根廷；关注球队比赛提前 1440 分钟提醒。

赛程数据在 `references/fwc2026-schedule.json`。来源为 FIFA 官方赛程 PDF，原始时间为 Eastern Time，脚本已换算为北京时间。FIFA 标注赛程可能调整，执行前如果用户要求最新信息，需要重新核对官方来源。

## 常用命令

先检查环境：

```bash
python3 scripts/world_cup_calendar.py doctor
```

如果没有安装飞书 CLI，可以让脚本尝试安装：

```bash
python3 scripts/world_cup_calendar.py doctor --install-cli
```

先预览赛程，不访问飞书：

```bash
python3 scripts/world_cup_calendar.py preview --focus-team ARG --limit 12
```

预览将写入飞书的日程内容，不真正创建：

```bash
python3 scripts/world_cup_calendar.py sync --focus-team ARG
```

确认无误后真正创建飞书日程：

```bash
python3 scripts/world_cup_calendar.py sync --focus-team ARG --execute
```

只同步关注球队比赛：

```bash
python3 scripts/world_cup_calendar.py sync --focus-team ARG --only-focus --execute
```

关注多个球队时用英文代码逗号分隔：

```bash
python3 scripts/world_cup_calendar.py sync --focus-team ARG,BRA,FRA --execute
```

## 删除日程

删除命令默认只预览，不真正删除。确认输出无误后，才加 `--execute`。

按比赛编号删除，例如删除阿根廷三场小组赛：

```bash
python3 scripts/world_cup_calendar.py delete --match-numbers 19,43,70
python3 scripts/world_cup_calendar.py delete --match-numbers 19,43,70 --execute
```

支持区间写法：

```bash
python3 scripts/world_cup_calendar.py delete --match-numbers 19-21
```

删除整套世界杯日程，也就是 104 场比赛：

```bash
python3 scripts/world_cup_calendar.py delete --all
python3 scripts/world_cup_calendar.py delete --all --execute
```

如果确定整个 `world-cup-calendar` 日历都不要了，可以删除日历本身：

```bash
python3 scripts/world_cup_calendar.py delete --delete-calendar
python3 scripts/world_cup_calendar.py delete --delete-calendar --execute
```

删除逻辑会先在目标日历中搜索“世界杯”，再匹配描述里的 `FWC2026-xxx` 比赛编号，只删除本 Skill 创建的世界杯日程。

## 飞书权限

执行 `--execute` 前，确认本机有 `lark-cli`，并使用用户身份授权日历权限。缺少权限时，脚本会输出 `lark-cli` 给出的中文提示或授权命令。

安装飞书 CLI：

```bash
npm install -g @larksuite/cli
```

如果用户没有 Node.js/npm，先安装 Node.js LTS：https://nodejs.org/

通常需要这些 scope：
- `calendar:calendar:read`
- `calendar:calendar:create`
- `calendar:calendar.event:create`
- `calendar:calendar.event:delete`
- `calendar:calendar:delete`（只有删除整个日历时需要）

授权示例：

```bash
lark-cli auth login --scope "calendar:calendar:create"
lark-cli auth login --scope "calendar:calendar.event:create"
```

## 隐私说明

本 Skill 同时处理两件不同的事：
- `visibility=private`：别人看不到日程详情。
- `free_busy_status=free`：这段时间不会显示为忙碌。

不要把 `free_busy_status` 改成 `busy`，除非用户明确希望世界杯比赛占用自己的工作忙闲时间。

## 淘汰赛占位

淘汰赛在官方赛程中会出现 `1J`、`2H`、`W85`、`3 EFGIJ` 等占位：
- `1J` 表示 J 组第 1 名。
- `2H` 表示 H 组第 2 名。
- `W85` 表示第 85 场胜者。
- `3 EFGIJ` 表示 E/F/G/I/J 组第三名之一。

小组赛结束后，如果用户想把占位更新成真实球队，需要先核对 FIFA 官方结果，再更新 `references/fwc2026-schedule.json` 或重新生成数据。
