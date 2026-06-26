---
name: skill-search-create
slug: skill-search-create
version: 1.0.1
description: 在 ClawHub 上搜索现有技能，当找不到匹配时自动创建新的 OpenClaw 技能。
user-invocable: true
metadata:
  author: "蒋斌 (本地开发)"
  homepage: "https://clawhub.com"
  openclaw:
    requires:
      bins: ["clawhub"]
    install:
      - id: node
        kind: node
        package: clawhub
        bins: ["clawhub"]
        label: "Install ClawHub CLI (npm)"
---

# Skill Search & Create

> Version: 1.0.1

_Find skills on ClawHub or create new ones when needed._

## 功能

- **搜索**: 在 ClawHub 上搜索现有技能
- **创建**: 找不到合适的时，自动创建新技能
- **发布**: 创建后可直接发布到 ClawHub

## 命令

### 搜索技能

```bash
clawhub search <关键词>
```

### 创建技能

```bash
# 通过 CLI（需先登录）
clawhub create <skill-name>

# 或手动创建目录结构:
# skill-name/
#   ├── SKILL.md (必须)
#   ├── scripts/
#   ├── references/
#   └── assets/
```

### 发布技能

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --changelog "Initial release"
```

> 发布前需先登录: `clawhub login`

## 推荐工作流

当用户请求某个技能时：
1. `clawhub search <关键词>` 搜索
2. 找到 → 报告结果（名称、描述、作者）
3. 没找到 → 询问是否创建
4. 用户确认 → 初始化技能结构
5. 用户想发布 → `clawhub publish`

## 使用示例

| 用户请求 | 操作 |
|----------|------|
| "找天气预报的 skill" | `clawhub search weather` |
| "没有就创建一个" | 初始化新 weather 技能 |
| "找一个做表格的" | `clawhub search spreadsheet` |
| "把这个 skill 发布上去" | `clawhub publish ./xxx --slug xxx ...` |

## 备注

- 依赖 `clawhub` CLI（通过 npm 全局安装）
- CLI 不可用时回退到手动创建
- 遵循 OpenClaw 技能结构规范
