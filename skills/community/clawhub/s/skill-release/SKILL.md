---
name: clawhub-deploy
description: Publish and manage Claude Code skills on ClawHub (clawhub.ai). Use when user wants to "publish skill", "update skill version", "release to clawhub", "clawhub publish", "clawhub update", or manage skill versions on the ClawHub registry.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - CLAWHUB_TOKEN
      bins:
        - clawhub
        - node
        - npm
---

# ClawHub Publish - Skill 发布助手

帮助用户将 Claude Code skills 发布到 ClawHub (clawhub.ai) 并管理版本更新。

## 核心能力

- **发布新 Skill**: 首次发布到 ClawHub
- **更新版本**: 发布新版本（自动递增版本号、生成 changelog）
- **检查状态**: 验证 CLI 安装、登录状态、已发布技能列表
- **规范校验**: 检查 SKILL.md 是否符合 ClawHub 要求

## 前置检查

执行任何命令前，自动检查：
1. **clawhub CLI 安装**: `clawhub --version`
2. **登录状态**: `clawhub whoami`
3. **SKILL.md 存在**: 目标目录是否有 SKILL.md
4. **frontmatter 完整**: name / description / version 是否齐全

缺少时自动引导修复。

## 常用命令

| 命令 | 说明 |
|------|------|
| `/clawhub-publish status` | 检查 CLI、登录状态、已发布技能 |
| `/clawhub-publish publish <path>` | 发布新 skill |
| `/clawhub-publish update <path>` | 更新已有 skill 版本 |
| `/clawhub-publish check <path>` | 检查 skill 是否符合规范 |

## 工作流程

### 首次发布
```
1. 检查 CLI & 登录状态
2. 检查 SKILL.md 规范
3. 询问版本号（默认 1.0.0）
4. 询问 changelog
5. 执行 clawhub publish
6. 返回发布链接
```

### 版本更新
```
1. 检查当前已发布版本
2. 建议新版本号（自动递增 patch）
3. 询问 changelog（自动生成 diff 摘要辅助）
4. 更新 SKILL.md 中的 version
5. 执行 clawhub publish
6. 返回更新链接
```

## ClawHub 规范要求

### SKILL.md 必须包含
- **frontmatter**: `name`, `description`, `version`
- **metadata** (推荐): `openclaw.requires.env`, `openclaw.requires.bins`
- **description**: 决定触发时机，需清晰全面

### 目录结构
```
skill-name/
├── SKILL.md          # 必须
├── README.md         # 推荐
├── scripts/          # 可选
├── prompts/          # 可选
├── references/       # 可选
├── templates/        # 可选
└── requirements.txt  # Python 依赖
```

## 安装依赖

```bash
npm i -g clawhub
clawhub login
```
