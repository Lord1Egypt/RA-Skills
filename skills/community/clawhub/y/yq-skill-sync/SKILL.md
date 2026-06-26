---
name: yq-skill-sync
description: ClaWHub 技能同步与自动更新。关键词：技能更新、更新技能、同步技能、检测技能更新、自动更新所有技能、技能版本状态
version: 1.0.0
---

## 触发词（任意一个即可激活）

- 「技能更新」
- 「更新技能」
- 「同步技能」
- 「检测技能更新」
- 「自动更新所有技能」
- 「技能版本状态」
- 定时触发（cron 每日 06:37）

## 技能概述

- **版本**: 1.0.1
- **类型**: utility（工具型）
- **功能**: 自动检测 + 更新 workspace/skills 本地技能，支持版本比对、clawhub sync 批量发布、定时提醒

## 内部配置（自动读取，无需修改）

- **Token 文件:** `/root/.config/clawhub/config.json`
- **clawhub CLI:** `/root/.npm/_npx/ce38bf0ef4fd88c6/node_modules/.bin/clawhub`
- **workspace:** `/workspace`
- **账号:** tianheihei002

## 核心逻辑

### 执行流程

1. 读取 `/root/.config/clawhub/config.json` 确认 token 有效
2. 执行 `clawhub whoami` 验证登录状态
3. 扫描 `/workspace/skills/` 下所有 SKILL.md，提取 version
4. 对有版本 API 的技能（如 mxai）调 API 检测
5. 执行 `clawhub sync --workdir /workspace` 同步线上
6. 输出完整差异报告

### 更新策略

| 类型 | 来源 | 更新方式 |
|------|------|----------|
| ClaWHub 官方技能 | `clawhub install` | `clawhub update --all` |
| 有版本 API | mxai 等 | GET version_url 对比 |
| 纯本地技能 | 手动创建 | 发布到 ClaWHub 建立机制 |

### cron 配置建议

```json
{
  "name": "每日技能同步检测",
  "schedule": { "kind": "cron", "expr": "37 6 * * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "执行 skill-sync，检测所有技能更新并输出报告" },
  "sessionTarget": "isolated",
  "enabled": true
}
```

## Skill Vetter 安全审核

**安装任意技能前**，必须先经过 skill-vetter 审核：

| 决策 | 标注 | 说明 |
|------|------|------|
| ✅ 通过 | `verified: true` | 无风险或轻微风险可忽略 |
| ⚠️ 需审阅 | `needs_review: true` | 有潜在风险，用户确认后安装 |
| ❌ 拒绝 | `blocked: true` | 高危风险，直接拒绝 |

## 版本

- **Skill 版本**: 1.0.1
- **兼容**: OpenClaw + ClaWHub CLI v0.9.0+

## 更新日志

- 1.0.1（2026-04-07）：触发词优化，新增「技能更新」「更新技能」
- 1.0.0（2026-04-07）：首次创建
