---
name: tmeet-conflict-check
description: "Check the current account's Tencent Meeting list for hard overlaps, short transition gaps, and three-or-more concurrent meetings, or configure a deterministic weekday office-hours watcher that wakes the Agent only for new conflicts. Use for requests such as checking today/tomorrow/this week's meeting conflicts, detecting conflicts caused by new invitations, changing the monitoring schedule, or deploying the watcher on macOS, Linux, or Windows x64."
---

# 腾讯会议冲突检查

独立执行即时冲突查询和低成本被动监测。调用 `tmeet` 时同时遵守官方 `tmeet-skill` 的认证、分页、隐私和安全规则。

## 命令子树

```text
tmeet
├── auth
│   ├── login
│   └── status
└── meeting
    ├── list
    └── search
```

## 通用规则

1. 先运行 `tmeet auth status`。未登录时让用户在前台运行 `tmeet auth login`。
2. 时间使用带时区的 ISO 8601；未提供时区时使用用户当前时区并说明。
3. 仅检查当前账号可见的腾讯会议，不代表完整日历，不覆盖线下会议或其他会议平台。
4. 面向用户只显示会议主题、会议号和时间；不显示内部会议 ID 或 Token。
5. 不替用户取消会议或决定参加哪场。

## 用户主动查询

用户说“现在查一下”、“我明天是否撞会”时立即执行，不受办公时间或定时槽位限制。无冲突也要当场返回结果。

```bash
tmeet meeting list \
  --start "<ISO_START>" \
  --end "<ISO_END>" \
  --show-all-sub 1 \
  --compact
```

用户同时给出主题、会议号、创建人或备注等关键词时使用 `meeting search`。未给时间范围时默认检查当天 00:00–23:59:59 并说明。

“是否有冲突”必须遍历指定范围内全部会议，按 `next_page_token` 继续取数。连续超过 5 页或累计超过 200 条时，先告知数据量并询问是否继续。

## 冲突判定

按开始时间排列，用活动集合保留所有“结束时间晚于当前会议开始时间”的会议，不要只比较相邻会议。

```text
overlap_start = max(A.start, B.start)
overlap_end   = min(A.end, B.end)
硬冲突       = overlap_start < overlap_end
软冲突       = 无重叠且 0 <= B.start - A.end < 15 分钟
多场冲突     = 同一时间点至少 3 场会议同时进行
```

缺少开始或结束时间的会议标记“无法判断”，不补默认时长。输出查询范围、总体结论、冲突会议及重叠/间隔分钟数。

无冲突时写：“在上述范围内，未发现当前账号腾讯会议之间的时间冲突。”

## 脚本被动监测

用户要求主动提醒时，先完整读取 [references/conflict-watcher-protocol.md](references/conflict-watcher-protocol.md)，再使用 [scripts/watch_meeting_conflicts.py](scripts/watch_meeting_conflicts.py)。不让模型定时调用 `meeting list`。

- 默认仅在当前时区工作日 09:00–18:00（含 18:00）的整点和半点检查。
- 工作时间外、非计划槽位或没有新冲突时标准输出为空；宿主不得创建 Agent 回合或发用户消息。
- 只有 `meeting.conflict.detected` NDJSON 才唤醒 Agent，且直接使用事件结果，不重新拉取列表。
- 用户可自定义时区、工作日、办公时段、每小时分钟点或具体时间。
- 用户要求启用监测却没给时间时，直接使用默认值，不追问。
- 本方式是脚本轮询，不是腾讯会议服务端实时邀请事件。

## 平台适配

- macOS/Linux 使用 `tmeet` 和 `python3`。
- Windows x64 使用 `tmeet.cmd` 和 `py -3`。部署、调度或验收前完整读取 [references/windows-execution.md](references/windows-execution.md)。
- 不声称支持 Windows ARM64 原生 CLI。

## 用户可见的时间说明

每次用户可见结果末尾都说明检查时间可自定义：

- 监测已启用：回显当前实际配置。
- 未自定义：说明默认工作日 09:00–18:00 整点/半点由脚本检查，只有新冲突才提醒并唤醒 Agent。
- 只做即时查询且监测未启用：写“可启用冲突监测”，不虚假声称后台正在运行。

不把“定时检查”说成“定时必定提醒”。
