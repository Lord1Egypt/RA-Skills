---
name: wechat-group-operator
description: WeChat group operations automation for Windows desktop WeChat. Use when the user wants to run recurring group engagement workflows such as morning questions, afternoon follow-ups, and evening case posts in specified微信群, with content pools, posting history, and OpenClaw cron scheduling. Best for群运营、私域活跃、课程群维护、社群节奏 automation. Not for朋友圈 scraping or broad WeChat data extraction.
---

# wechat-group-operator

Use this skill to operate designated WeChat groups on a recurring schedule.

## What this skill provides

- group whitelist config
- content pools for questions / followups / cases
- post history to reduce repeats
- execution script for one action at a time
- compatibility with OpenClaw cron jobs

## Files

Core files:

- `scripts/wechat_group_operator.py`
- `assets/groups.json`
- `assets/post_history.json`
- `assets/content/questions.json`
- `assets/content/followups.json`
- `assets/content/cases.json`

## Supported actions

- `morning_question`
- `afternoon_followup`
- `evening_case`

## Quick start

### Dry run

```bash
python scripts/wechat_group_operator.py --action morning_question --dry-run
python scripts/wechat_group_operator.py --action evening_case --group "Core突击龙虾🦞" --dry-run
```

### Real send

```bash
python scripts/wechat_group_operator.py --action morning_question
python scripts/wechat_group_operator.py --action afternoon_followup
python scripts/wechat_group_operator.py --action evening_case
```

## Recommended workflow

1. Edit `assets/groups.json` to maintain target group whitelist
2. Edit content pools under `assets/content/`
3. Dry run first
4. Run real send manually
5. Attach to OpenClaw cron when stable

## OpenClaw routing guidance

Map user intent like this:

- “上午往群里抛一个问题” → `morning_question`
- “下午追问一下群里讨论” → `afternoon_followup`
- “晚上发一个案例到群里” → `evening_case`
- “给指定群先预演一下今天会发什么” → add `--dry-run`

## Boundaries

Current MVP assumes:

- groups are manually whitelisted
- content comes from maintained pools
- one action runs at a time
- sending uses existing desktop WeChat sender capability

Do not claim support yet for:

- automatic discovery of groups where the user is owner
- automatic web research and content generation inside this skill
- advanced WeChat content forwarding/media posting

## Read more when needed

- `references/config.md`
- `references/actions.md`
- `references/cron-setup.md`
