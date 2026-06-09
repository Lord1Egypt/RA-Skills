---
name: "skill-c-fetch-minutes"
description: "【会后纪要抓取与issue草稿生成】每10分钟由 OpenClaw cron 触发一次。负责在会议结束后从腾讯会议拉取转录与AI智能纪要，由 OpenClaw 做两阶段issue抽取，生成 draft_issue.md 等四个文件并提交到 Gitea，最后通知组织者审核。不处理会议创建、会前简报、issue落地等场景。"
category: "other"
source: "ClawHub"
tags: []
platforms: []
author: ""
version: ""
license: ""
installCmd: "hermes skills install clawhub/skill-c-fetch-minutes"
sourceUrl: "https://clawhub.ai/skills/skill-c-fetch-minutes"
---

# skill-c-fetch-minutes

> 【会后纪要抓取与issue草稿生成】每10分钟由 OpenClaw cron 触发一次。负责在会议结束后从腾讯会议拉取转录与AI智能纪要，由 OpenClaw 做两阶段issue抽取，生成 draft_issue.md 等四个文件并提交到 Gitea，最后通知组织者审核。不处理会议创建、会前简报、issue落地等场景。

- **Category:** Other
- **Source:** ClawHub
- **Author:** 
- **Version:** 
- **License:** 
- **Platforms:** All
- **Install Command:** `hermes skills install clawhub/skill-c-fetch-minutes`
- **Source URL:** [https://clawhub.ai/skills/skill-c-fetch-minutes](https://clawhub.ai/skills/skill-c-fetch-minutes)

## Overview


## Installation
To install this skill, run the following command in your terminal:
```bash
hermes skills install clawhub/skill-c-fetch-minutes
```
