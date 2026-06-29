---
name: x-skill-updater
description: 检查并更新 OpenClaw skills。触发词：「检查skill更新」「更新skill」「skill更新检查」。支持定时自动检查（每周一 09:00）和手动触发，有更新时通知后确认再升级。
author: "B站_少年李迟迟"
version: v1.2
---

# x-skill-updater — Skill 更新检查与升级管理

> `<OPENCLAW_HOME>` 是你的 OpenClaw 配置根目录，通常为 `~/.openclaw`。以下路径均需替换为实际安装路径。

## 何时使用

| 场景 | 触发方式 |
|------|---------|
| 用户主动要求检查 | 说「检查skill更新」「更新skill」「skill更新」等 |
| 每周定时检查 | cron 自动触发（每周一 09:00） |

## 核心规则

1. **不降级**：本地版本 > 官频版本 → 视为定制版，跳过（不降级）
2. **全量字段核对**：`_meta.json`（ownerId / slug / version / publishedAt）+ `SKILL.md`（author / slug / homepage / metadata）全部纳入核对
3. **征得同意再升级**：检查结果通知用户，用户回复「更新」后才执行
4. **分来源检查**：
   - **skillhub** → COS bucket index
   - **clawhub** → clawhub.ai API
   - **custom** → 跳过，仅记录说明

## 检查流程

### Step 1 — 运行检查脚本

```bash
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/check.py
```

### Step 2 — 分析输出

- **有可升级**（exit code=1）：生成报告发给用户，等回复「更新」
- **无更新**（exit code=0）：生成报告存档，无需通知

### Step 3 — 执行升级（如用户同意）

```bash
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/upgrade.py <slug>
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/upgrade.py --all
```

## 新 skill 来源确认

检查报告发现来源不明的 skill 时，用户只需回复格式即可：

```bash
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/reply.py "skill名 → clawhub"
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/reply.py "skill名 → skillhub"
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/reply.py "skill名 → custom"
```

## 数据文件

- `data/skill-sources.json` — 所有 skill 的来源配置（需根据实际安装补充）
- `data/last-report.md` — 上次检查报告存档
- `data/pending-sources.json` — 来源不明的 skill 列表（由 check.py 自动维护）

## skill-sources.json 字段说明

```json
{
  "<skill-name>": {
    "source":    "skillhub | clawhub | custom",
    "slug":      "registry 上的 slug（默认等于 skill 目录名）",
    "ownerId":   "clawhub 作者 handle，用于作者一致性校验",
    "check_mode":"auto | manual",
    "note":      "来源说明"
  }
}
```

## 本地文件字段说明（全部纳入核对）

**`_meta.json`**（skillhub + clawhub 共用）：
- `version` — 版本号（主要数据源）
- `slug` — registry 上的 slug
- `ownerId` — 作者系统 ID
- `publishedAt` — 发布时间（毫秒时间戳）

**`SKILL.md` frontmatter**：
- `version` — 版本号（_meta.json 的备用）
- `author` — 作者名称
- `slug` — slug 决策链兜底
- `homepage` — clawhub 特征（包含 clawic.com）
- `metadata` — clawhub 专属标记（metadata.clawdbot）

## 来源说明符号

| 符号 | 含义 |
|------|------|
| 🆕 可升级 | 有新版本，征得同意后更新 |
| ✅ 已是最新 | 本地版本等于或高于官频 |
| 🟡 定制版 | 本地版本更高，不降级 |
| ⚠️ 需关注 | 版本信息不完整或字段不一致 |
| 🔧 手动 | custom 来源，需手动查看 |
| ❓ 来源不明 | 未在 skill-sources.json 登记 |

## 安装路径说明

脚本通过自身所在位置自动向上定位 OpenClaw 根目录，不依赖硬编码路径，安装在任何位置均可正常工作。

## 扫描范围

自动扫描 `<OPENCLAW_HOME>/skills/` 和 `<OPENCLAW_HOME>/workspace-*/skills/` 下所有 skill。