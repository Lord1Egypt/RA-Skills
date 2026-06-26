---
name: soyoung-clinic-tools
slug: soyoung-clinic-tools
version: 2.2.2
description: >
  新氧青春诊所工具集，包含预约、项目查询百科、医生信息及医生排班查询等能力 | Soyoung clinic tools
  OpenClaw skill for the Soyoung (soyoung) clinic chain: appointment booking, store lookup, doctor info,
  schedules, project knowledge and pricing. Keywords: Soyoung, soyoung, clinic, appointment, doctor,
  schedule, medical aesthetic.
tags: [Soyoung, soyoung, clinic, appointment, doctor, schedule, medical, beauty, healthcare, 新氧, 诊所, 预约, 医生, 排班, 医美, 整形, hospital]
license: MIT
---

# 新氧青春诊所工具集 Soyoung Clinic Tools — 技能集规格

**Name**: soyoung-clinic-tools  
**Version**: 2.2.2  
**License**: MIT

## Description

新氧青春诊所工具集，包含预约、项目查询百科、医生信息及医生排班查询等能力 | Soyoung clinic tools

OpenClaw skill for the Soyoung (soyoung) clinic chain: appointment booking, store lookup, doctor info, schedules, project knowledge and pricing. Keywords: Soyoung, soyoung, clinic, appointment, doctor, schedule, medical aesthetic.

> 本文件作为技能集主说明；子技能配置与规则见各目录 `SKILL.md`。

## 功能总览

### 📅 预约与门店（appointment）
- 配置文件：`skills/appointment/SKILL.md`
- 能力：门店查询、预约切片、预约创建/修改/取消/查询、审批流

### 💉 项目与商品（project）
- 配置文件：`skills/project/SKILL.md`
- 能力：项目知识检索、商品价格检索

### 👨‍⚕️ 医生与排班（doctor）
- 配置文件：`skills/doctor/SKILL.md`
- 能力：医生信息检索、门店医生检索、排班查询

## 共享配置（Setup）

### 🔐 apikey
- 配置文件：`setup/apikey/SKILL.md`
- 作用：API Key 主人绑定与管理、位置保存与读取
- 依赖关系：`appointment`、`project`、`doctor` 均依赖该 setup

## Requirements

- `python3`（3.8+，必需）
- `bash`（入口兼容壳依赖）
- API Key：打开浏览器访问 `https://www.soyoung.com/loginOpenClaw`，登录后复制 API Key

## Workspace State

| 文件 | 说明 |
|------|------|
| `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/api_key.txt` | 当前 workspace 的 API Key，权限 600 |
| `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/binding.json` | 主人 Open ID、主人名、绑定时间等元信息 |
| `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/location.json` | 主人位置 |
| `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/pending/*.json` | 群聊预约审批单 |

## Security Model

- API Key 只能在与主人私聊中发送和配置
- 非主人群聊发起高风险预约操作时，必须先 `@主人`
- 高风险预约动作只包括：查询我的预约、提交预约、修改预约、取消预约
- 主人确认格式：`确认 #审批单号`
- 主人拒绝格式：`拒绝 #审批单号`

## Uninstall

```bash
# 1. 由主人在私聊中删除当前 workspace 的 API Key
bash ~/.openclaw/skills/soyoung-clinic-tools/setup/apikey/scripts/main.sh --delete-key --confirm --workspace-key <workspace_key> --chat-type direct --chat-id <chat_id> --sender-open-id <owner_open_id>

# 2. 禁用并移除 bootstrap hook
openclaw hooks disable soyoung-clinic-tools
rm -rf ~/.openclaw/hooks/soyoung-clinic-tools/

# 3. 删除 skill 目录
rm -rf ~/.openclaw/skills/soyoung-clinic-tools/
```

## Documentation

- 用户指南：[使用说明.md](使用说明.md)
- 版本历史：[CHANGELOG.md](CHANGELOG.md)
- 后端接口规范：[references/api-spec.md](references/api-spec.md)
