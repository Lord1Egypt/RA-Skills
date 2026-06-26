# AI Creator Briefing - Cron Task

## Task Configuration

**Task ID**: 7fcf083a-77d0-41ce-8863-8701027bcea9
**Name**: AI Creator Briefing
**Schedule**: 每天 8:00 (0 8 * * *)
**Status**: ✅ Enabled

## Next Run

**下次执行时间**: 2026-03-28 08:00:00 (GMT+8)

## Task Payload

```json
{
  "kind": "systemEvent",
  "text": "run-briefing"
}
```

## Setup Complete

定时任务已成功创建！明天早上8点将自动执行AI博主简报生成流程。

## What Happens at 8:00 AM

1. 抓取18位AI博主近10天推文
2. 清洗、去重、评分
3. 生成结构化简报
4. 提炼英文推文
5. 自动发布到X
6. 归档保存

## Manual Execution (Optional)

如果你想立即测试，可以手动执行：

```bash
cd /Users/youke/.openclaw/workspace/skills/zeelin-x-creator-briefing
./scripts/run-briefing.sh
```

## Monitor Task

查看任务状态：
```bash
openclaw cron status
```

查看任务历史：
```bash
openclaw cron runs
```

## Disable Task (If Needed)

如需禁用任务：
```bash
openclaw cron disable "AI Creator Briefing"
```

删除任务：
```bash
openclaw cron rm "AI Creator Briefing"
```

---

*任务创建时间: 2026-03-27 22:26*
*下次执行: 2026-03-28 08:00*
