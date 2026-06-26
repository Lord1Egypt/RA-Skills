---
name: campaign-tracker
description: 客户开发信追踪与分析 — 自动归档发送记录、匹配客户回复、生成效果分析报告、优化邮件模板
---

# campaign-tracker SKILL

> 客户开发信追踪与分析 — 完整闭环系统

## 用途

当需要以下操作时使用此 skill：
- 归档开发信发送记录
- 追踪客户回复状态
- 生成开发信效果分析报告（周报/月报）
- 优化开发信模板（A/B测试建议）

## 前置条件

1. task-001（`imap-smtp-email`）已配置并能正常发送邮件
2. task-002（`okki-email-sync`）已配置，OKKI 向量搜索可用
3. Node.js 环境可用

## 快速开始

```bash
# 切换到 skill 目录
cd <path-to-campaign-tracker>
# 或使用环境变量
cd $CAMPAIGN_TRACKER_ROOT
```

## 核心命令

### 归档已发送开发信
```bash
node scripts/archive-sent-records.js check --dry-run   # 预览
node scripts/archive-sent-records.js check             # 执行归档
```

### 匹配客户回复
```bash
node scripts/reply-matcher.js check --dry-run          # 预览
node scripts/reply-matcher.js check                    # 执行匹配
node scripts/reply-matcher.js unmatched                # 查看未匹配
```

### 生成分析报告
```bash
# 周报
node scripts/analytics-report.js weekly
node scripts/analytics-report.js weekly --obsidian     # 同时输出到 Obsidian

# 月报
node scripts/analytics-report.js monthly
node scripts/analytics-report.js monthly --last-month  # 上个月
```

### 模板优化建议
```bash
node scripts/template-optimizer.js analyze --dry-run   # 预览
node scripts/template-optimizer.js analyze             # 执行分析
node scripts/template-optimizer.js analyze --obsidian  # 输出到 Obsidian
```

## 文件说明

| 文件 | 用途 |
|------|------|
| `config/tracking-schema.json` | 数据模型配置（5模块） |
| `scripts/archive-sent-records.js` | 发送记录归档（512行） |
| `scripts/reply-matcher.js` | 回复匹配+状态更新（669行） |
| `scripts/analytics-report.js` | 效果分析报告（542行） |
| `scripts/template-optimizer.js` | 模板优化+A/B测试（625行） |

## 典型工作流

1. 每次发送开发信后 → 运行 `archive-sent-records.js check`
2. 每天检查新回复 → 运行 `reply-matcher.js check`
3. 每周一 → 运行 `analytics-report.js weekly --obsidian`
4. 每月初 → 运行 `analytics-report.js monthly --obsidian`
5. 每月优化模板 → 运行 `template-optimizer.js analyze --obsidian`

## 数据位置

```
<campaign-tracker-root>/
├── archive/          # 发送记录归档（JSONL）
├── reply-tracking/   # 回复状态数据（JSONL）
├── reports/          # 分析报告（Markdown+JSON）
└── logs/             # 运行日志

$OBSIDIAN_VAULT/开发信追踪/   # Obsidian 知识库输出
```

## 依赖集成

```javascript
// archive-sent-records.js 读取 smtp.js 发送日志
const emailSkillPath = process.env.EMAIL_SKILL_ROOT || '<path-to-imap-smtp-email>';

// reply-matcher.js 使用 IMAP 收件箱
const imapConfig = require(process.env.EMAIL_SKILL_ROOT + '/.env');

// 客户匹配使用 OKKI 向量搜索
const vectorSearch = process.env.OKKI_VECTOR_SEARCH || '<path-to-okki_vector_search_v3.py>';
```

## 注意事项

- 首次运行前确保 `archive/`、`reply-tracking/`、`reports/`、`logs/` 目录已存在（脚本会自动创建）
- 所有脚本支持 `--dry-run` 模式，建议首次运行时使用
- Obsidian 输出需要确认 vault 路径：`~/obsidian-vault/`
- A/B 测试配置存储在 `config/tracking-schema.json` 的 `ab_testing` 模块
