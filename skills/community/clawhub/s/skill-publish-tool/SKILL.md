---
name: skill-publish-tool
version: 1.0.0
description: 自动更新 GitHub 仓库并发布 Skill 到 ClawHub。当用户需要发布 skill 更新时使用此技能。支持自动版本号递增、更新日志管理、Git 提交推送、ClawHub 发布。
---

# skill-publish-tool

自动化发布 OpenClaw Skill 到 GitHub 和 ClawHub 的工具。

## 功能特性

- 📦 **自动版本管理** - 支持 major/minor/patch 版本号递增
- 📝 **更新日志管理** - 自动更新 README.md 的更新日志部分
- 🔄 **Git 自动化** - 自动提交并推送到 GitHub
- 🚀 **ClawHub 发布** - 一键发布到 ClawHub 市场
- 📋 **多文件同步** - 同时更新 package.json 和 _meta.json

## 使用方式

### 基础用法

```bash
python3 scripts/publish_skill.py <skill 目录> --slug <slug> --changelog "<更新日志>"
```

### 完整参数

```bash
python3 scripts/publish_skill.py <skill 目录> \
  --slug <slug> \
  --name "<display name>" \
  --bump <major|minor|patch> \
  --changelog "<更新日志>" \
  [--skip-git] \
  [--skip-clawhub]
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `path` | ✅ | Skill 目录路径 |
| `--slug` | ✅ | ClawHub 上的 skill slug |
| `--name` | ❌ | Display name（可选） |
| `--bump` | ❌ | 版本号递增类型，默认 `patch` |
| `--changelog` | ✅ | 更新日志内容 |
| `--skip-git` | ❌ | 跳过 Git 操作 |
| `--skip-clawhub` | ❌ | 跳过 ClawHub 发布 |

## 使用示例

### 示例 1: 发布补丁版本

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/cn-stock-volume \
  --slug cn-stock-volume \
  --changelog "新增创业板数据，修复合计计算逻辑"
```

### 示例 2: 发布小版本更新

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/my-skill \
  --slug my-skill \
  --bump minor \
  --changelog "新增 XX 功能，优化 XX 性能"
```

### 示例 3: 仅更新本地文件（不发布）

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/my-skill \
  --slug my-skill \
  --changelog "本地测试更新" \
  --skip-clawhub
```

### 示例 4: 仅发布到 ClawHub（不推送到 GitHub）

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/my-skill \
  --slug my-skill \
  --changelog "仅发布到 ClawHub" \
  --skip-git
```

## 输出示例

```
============================================================
  📦 Skill Publisher
  路径：/Users/xxx/skills/cn-stock-volume
  Slug: cn-stock-volume
============================================================

📋 当前版本：v1.0.0
📋 新版本：v1.0.1

━━━ 步骤 1: 更新版本号 ━━━
✅ 已更新：package.json → v1.0.1
✅ 已更新：_meta.json → v1.0.1

━━━ 步骤 2: 更新 README.md ━━━
✅ 已更新 README.md 更新日志 → v1.0.1

━━━ 步骤 3: Git 提交和推送 ━━━
🔧 执行：git add -A
🔧 执行：git commit -m "v1.0.1: 新增创业板数据"
🔧 执行：git push
✅ Git 推送成功

━━━ 步骤 4: 发布到 ClawHub ━━━
🚀 发布到 ClawHub: cn-stock-volume@1.0.1
✅ ClawHub 发布成功!
📦 Skill ID: k974z4a6pc4bv3gverd92c935s83anr6
🔗 链接：https://clawhub.ai/k974z4a6pc4bv3gverd92c935s83anr6/cn-stock-volume

============================================================
  ✅ 发布完成!
  版本：v1.0.1
============================================================
```

## 前置要求

1. **Node.js + npm** - 用于运行 `npx clawhub` 命令
2. **Git** - 用于版本控制和推送
3. **ClawHub 账号** - 需要先登录 ClawHub

## 注意事项

1. **Git 认证** - 确保已配置 Git 凭证或 SSH 密钥
2. **ClawHub 登录** - 首次使用需要先登录 ClawHub
3. **版本号规则** - 遵循语义化版本（Semantic Versioning）
   - `major`: 不兼容的 API 更改
   - `minor`: 向后兼容的功能新增
   - `patch`: 向后兼容的问题修复

## 文件结构

```
skill-publisher/
├── SKILL.md
├── package.json
├── _meta.json
├── README.md
└── scripts/
    └── publish_skill.py
```

## 更新日志

### v1.0.0 (2026-03-21)
- 🎉 初始版本发布
- 支持自动版本号递增
- 支持 Git 自动提交推送
- 支持 ClawHub 自动发布
- 支持更新日志自动管理
