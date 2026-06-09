---
name: "Self-Governor"
description: "LLM 通用内部自裁决技能。在关键节点判断"当前这一层最优的下一步动作是什么"，再让主链继续执行。触发条件：(1) 路径分叉时——多个可行方案且无明显优先级；(2) 高代价动作前——搜索/生成/发布等消耗军费或不可逆操作；(3) 连续两步无明显增益时——进展停滞、输出质量未提升。禁止：改写主任务、输出并列动作、长..."
category: "other"
source: "ClawHub"
tags: []
platforms: []
author: ""
version: ""
license: ""
installCmd: "hermes skills install clawhub/self-governor"
sourceUrl: "https://clawhub.ai/skills/self-governor"
---

# Self-Governor

> LLM 通用内部自裁决技能。在关键节点判断"当前这一层最优的下一步动作是什么"，再让主链继续执行。触发条件：(1) 路径分叉时——多个可行方案且无明显优先级；(2) 高代价动作前——搜索/生成/发布等消耗军费或不可逆操作；(3) 连续两步无明显增益时——进展停滞、输出质量未提升。禁止：改写主任务、输出并列动作、长...

- **Category:** Other
- **Source:** ClawHub
- **Author:** 
- **Version:** 
- **License:** 
- **Platforms:** All
- **Install Command:** `hermes skills install clawhub/self-governor`
- **Source URL:** [https://clawhub.ai/skills/self-governor](https://clawhub.ai/skills/self-governor)

## Overview


## Installation
To install this skill, run the following command in your terminal:
```bash
hermes skills install clawhub/self-governor
```
