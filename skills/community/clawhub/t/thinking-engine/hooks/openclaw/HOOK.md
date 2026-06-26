# OpenClaw Hook — multi-angle-thinking

Automatically reminds the agent to use the full analysis pipeline when deep thinking is requested.

## Install

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/multi-angle-thinking
openclaw hooks enable multi-angle-thinking
```

## What It Does

Monitors each user prompt for trigger phrases (in English and Arabic). When detected, injects a brief reminder of the 5-step pipeline into the agent context (~80 token overhead).

## Trigger Phrases Monitored

English: `analyze`, `simulate`, `think deeply`, `multiple angles`, `challenge my thinking`, `what am I missing`, `hidden risks`, `what would happen`

Arabic: `فكر معي`, `حلل`, `زوايا`, `نتائج غير متوقعة`, `ماذا سيحدث`

## Disable

```bash
openclaw hooks disable multi-angle-thinking
```
