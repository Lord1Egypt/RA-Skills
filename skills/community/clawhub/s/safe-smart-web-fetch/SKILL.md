---
name: "Safe Smart Web Fetch"
description: "安全网页抓取技能。获取网页内容时，默认先判断 URL 是否可能包含 token、是否为内网/本地域名、是否为私密链接；这三类一律不走第三方清洗服务，只走直接抓取。其余公开网页可按顺序尝试 Jina Reader、markdown.new、defuddle.md 获取干净 Markdown，失败再回退原始抓取。"
category: "other"
source: "ClawHub"
tags: []
platforms: []
author: ""
version: ""
license: ""
installCmd: "hermes skills install clawhub/safe-smart-web-fetch"
sourceUrl: "https://clawhub.ai/skills/safe-smart-web-fetch"
---

# Safe Smart Web Fetch

> 安全网页抓取技能。获取网页内容时，默认先判断 URL 是否可能包含 token、是否为内网/本地域名、是否为私密链接；这三类一律不走第三方清洗服务，只走直接抓取。其余公开网页可按顺序尝试 Jina Reader、markdown.new、defuddle.md 获取干净 Markdown，失败再回退原始抓取。

- **Category:** Other
- **Source:** ClawHub
- **Author:** 
- **Version:** 
- **License:** 
- **Platforms:** All
- **Install Command:** `hermes skills install clawhub/safe-smart-web-fetch`
- **Source URL:** [https://clawhub.ai/skills/safe-smart-web-fetch](https://clawhub.ai/skills/safe-smart-web-fetch)

## Overview


## Installation
To install this skill, run the following command in your terminal:
```bash
hermes skills install clawhub/safe-smart-web-fetch
```
