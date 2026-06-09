---
name: "skill-h-meeting-sync"
description: "【会议状态同步后台守护任务】每25分钟由 OpenClaw cron 触发一次。负责同步腾讯会议与各 Gitea 仓库之间的会议状态一致性，处理会议取消、改期、新增三种场景，并定期归档过期会议目录。不处理会议创建（用 skill-a）、会前简报（用 skill-b）、会后纪要（用 skill-c）等场景。"
category: "other"
source: "ClawHub"
tags: []
platforms: []
author: ""
version: ""
license: ""
installCmd: "hermes skills install clawhub/skill-h-meeting-sync"
sourceUrl: "https://clawhub.ai/skills/skill-h-meeting-sync"
---

# skill-h-meeting-sync

> 【会议状态同步后台守护任务】每25分钟由 OpenClaw cron 触发一次。负责同步腾讯会议与各 Gitea 仓库之间的会议状态一致性，处理会议取消、改期、新增三种场景，并定期归档过期会议目录。不处理会议创建（用 skill-a）、会前简报（用 skill-b）、会后纪要（用 skill-c）等场景。

- **Category:** Other
- **Source:** ClawHub
- **Author:** 
- **Version:** 
- **License:** 
- **Platforms:** All
- **Install Command:** `hermes skills install clawhub/skill-h-meeting-sync`
- **Source URL:** [https://clawhub.ai/skills/skill-h-meeting-sync](https://clawhub.ai/skills/skill-h-meeting-sync)

## Overview


## Installation
To install this skill, run the following command in your terminal:
```bash
hermes skills install clawhub/skill-h-meeting-sync
```
