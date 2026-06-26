# campaign-tracker

> 客户开发信追踪与分析系统 — 完整闭环：发送 → 追踪 → 分析 → 优化

## 概述

campaign-tracker 是 Farreach 开发信营销闭环系统，集成邮件发送记录归档、回复状态追踪、效果分析报告和模板优化建议四大功能模块。

## 依赖

- **task-001** (`imap-smtp-email`)：邮件发送系统，提供已发送邮件数据
- **task-002** (`okki-email-sync`)：OKKI CRM 同步，客户匹配数据

## 目录结构

```
campaign-tracker/
├── config/
│   └── tracking-schema.json      # 数据模型配置（5个核心模块）
├── scripts/
│   ├── archive-sent-records.js   # 发送记录自动归档
│   ├── reply-matcher.js          # 回复匹配与状态更新
│   ├── analytics-report.js       # 效果分析报告（周报/月报）
│   └── template-optimizer.js     # 模板优化建议（A/B测试）
├── archive/                      # 归档数据目录（JSONL格式）
├── reply-tracking/               # 回复追踪数据
├── reports/                      # 分析报告输出
├── logs/                         # 运行日志
├── README.md
└── SKILL.md
```

## 核心模块

### 1. 数据模型 (`tracking-schema.json`)
5个核心数据模块：
- `sent_records`：12字段发送记录（recipient、template、campaign_id、subject等）
- `reply_tracking`：11字段回复追踪（含AI意图分类）
- `conversion_funnel`：6阶段转化漏斗
- `metrics`：多维度指标（campaign/template/sales_owner）
- `ab_testing`：A/B测试配置

### 2. 发送记录归档 (`archive-sent-records.js`)
```bash
# 检查已发送邮件并归档
node scripts/archive-sent-records.js check

# 干跑模式（预览，不写入）
node scripts/archive-sent-records.js check --dry-run

# 手动归档指定邮件
node scripts/archive-sent-records.js archive --uid <UID>
```

### 3. 回复匹配 (`reply-matcher.js`)
```bash
# 检查收件箱并匹配回复
node scripts/reply-matcher.js check

# 干跑模式
node scripts/reply-matcher.js check --dry-run

# 查看未匹配回复
node scripts/reply-matcher.js unmatched
```

**匹配策略：**
- 邮件地址精确匹配
- Subject 关键词模糊匹配
- 时间窗口过滤（30天内）
- AI意图分类（interested/not_interested/need_info/pricing/sample_request/no_reply）

### 4. 效果分析报告 (`analytics-report.js`)
```bash
# 生成本周周报
node scripts/analytics-report.js weekly

# 生成上月月报
node scripts/analytics-report.js monthly --last-month

# 输出到 Obsidian 知识库
node scripts/analytics-report.js weekly --obsidian
```

**报告内容：**
- 发送总量、回复率、转化率
- 转化漏斗分析
- 模板对比分析
- 智能洞察建议

### 5. 模板优化 (`template-optimizer.js`)
```bash
# 分析并生成优化建议
node scripts/template-optimizer.js analyze

# 干跑模式
node scripts/template-optimizer.js analyze --dry-run

# 输出到 Obsidian
node scripts/template-optimizer.js analyze --obsidian
```

**优化逻辑：**
- 识别高效模板（回复率 Top 30%）
- 识别低效模板（回复率 Bottom 30%）
- 生成改进建议
- 推荐 A/B 测试计划

## 工作流程

```
发送开发信（task-001）
       ↓
archive-sent-records.js → archive/ JSONL 归档
       ↓
reply-matcher.js → 匹配回复，更新状态
       ↓
analytics-report.js → 生成周报/月报
       ↓
template-optimizer.js → 优化建议 + A/B测试计划
       ↓
Obsidian 知识库归档
```

## 数据存储

| 数据类型 | 位置 | 格式 |
|---------|------|------|
| 发送记录 | `archive/sent-{campaign_id}.jsonl` | JSONL |
| 回复追踪 | `reply-tracking/replies-{date}.jsonl` | JSONL |
| 分析报告 | `reports/` | Markdown + JSON |
| 优化建议 | `reports/optimization-{date}.md` | Markdown |
| Obsidian | `~/obsidian-vault/开发信追踪/` | Markdown |

## 集成说明

### 与 task-001（imap-smtp-email）集成
archive-sent-records.js 读取 smtp.js 发送后的日志，自动提取发送记录字段。

### 与 task-002（okki-email-sync）集成
客户匹配使用 okki-email-sync 的向量检索能力，将发送记录关联到 OKKI 客户ID。

### Obsidian 输出
报告自动输出到 `~/obsidian-vault/开发信追踪/` 目录，与知识库无缝集成。

## 开发信息

- **版本：** 1.0.0
- **状态：** 生产就绪
- **构建时间：** 2026-03-24
- **task_id：** task-004
