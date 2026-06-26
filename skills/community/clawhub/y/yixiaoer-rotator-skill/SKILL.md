---
name: yixiaoer-rotator-skill
description: 蚁小二账号轮询管理器 - 多账号矩阵自动轮询发布，支持按平台独立维护索引、状态持久化。使用场景：需要管理多个平台账号（如哔哩哔哩、头条号、百家号等），自动轮询发布避免重复使用同一账号。触发词：账号轮询、多账号管理、蚁小二发布、自动切换账号、矩阵发布。
---

# yixiaoer-rotator-skill - 账号轮询 Skill

## 快速开始

### 1. 配置环境变量

```bash
export YIXIAOER_API_KEY="你的蚁小二 API Key"
export YIXIAOER_MEMBER_ID="你的成员 ID"
```

详见 [`references/config.md`](references/config.md)

### 2. 同步账号

```bash
cd /root/.openclaw/workspace/skills/yixiaoer-rotator-skill
node scripts/account-rotator.js sync
```

### 3. 获取下一个账号

```bash
node scripts/account-rotator.js next 哔哩哔哩
# 输出：69c9e5cd398e5ae930212379
```

## 核心能力

| 功能 | 说明 |
|------|------|
| **自动同步账号** | 从蚁小二 API 获取所有已绑定账号 |
| **按平台独立轮询** | 哔哩哔哩、头条号、百家号等各自维护索引 |
| **状态持久化** | JSON 文件记录，重启不丢失 |
| **CLI 命令** | 方便的命令行工具，可集成到发布流程 |

## 使用示例

### 同步账号列表

```bash
node scripts/account-rotator.js sync
```

输出示例：
```
正在从蚁小二同步账号列表...
✅ 同步完成！共 23 个账号，分布在 5 个平台

平台分布:
  - 哔哩哔哩：16 个账号
  - 百家号：1 个账号
  - 头条号：1 个账号
  - 网易号：3 个账号
  - 搜狐号：2 个账号
```

### 获取下一个账号（发布前调用）

```bash
# 获取账号 ID
ACCOUNT_ID=$(node scripts/account-rotator.js next 哔哩哔哩)

# 使用账号 ID 发布
node ../yixiaoer-skill/scripts/api.ts --payload='{
  "action": "publish",
  "platforms": ["哔哩哔哩"],
  "accountForms": [{"platformAccountId": "'$ACCOUNT_ID'"}]
}'
```

### 查看当前状态

```bash
node scripts/account-rotator.js status
```

## 集成到发布流程

```bash
#!/bin/bash

# 1. 同步账号（可选，定期执行）
node scripts/account-rotator.js sync

# 2. 获取下一个账号
ACCOUNT_ID=$(node scripts/account-rotator.js next 头条号)

# 3. 发布文章
node ../yixiaoer-skill/scripts/api.ts --payload='{
  "action": "publish",
  "publishType": "article",
  "platforms": ["头条号"],
  "accountForms": [{"platformAccountId": "'$ACCOUNT_ID'"}]
}'
```

## 状态文件

- **位置**: `account-rotator-state.json`（技能目录下）
- **内容**: 账号列表和轮询索引（不含 API Key）
- **安全**: 可安全存储，不含敏感凭据

## 依赖

本技能依赖 `yixiaoer-skill`，请确保已安装：
```bash
clawhub install yixiaoer-skill
```

## 安全说明

- **yixiaoer-skill**: 蚁小二官方 API 封装，源码公开可审计
- **API Key**: 通过环境变量传递，不硬编码
- **建议**: 安装前查看源码，确认无恶意代码
