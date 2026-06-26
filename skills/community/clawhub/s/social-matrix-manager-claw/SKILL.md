---
name: social-matrix-manager-claw
description: |
  自媒体矩阵管家虾 — 多账号自媒体矩阵的统一调度中心。监控数据、分析互动、检测异常、生成日报。

  **当以下情况时使用此 Skill**：
  (1) 需要汇总多个自媒体账号（抖音/小红书/视频号/B站/微博）的运营数据
  (2) 需要生成矩阵日报，标出异常账号
  (3) 需要检测爆款内容（播放量超均值N倍）并推送预警
  (4) 需要监控账号健康状态（限流、封禁、数据下滑）
  (5) 需要分析评论区舆情（负面词汇、投诉预警）
  (6) 需要生成内容排期建议或跨账号复用建议
  (7) 用户提到"矩阵数据"、"账号汇总"、"多账号"、"自媒体监控"、"粉丝互动"、"爆款预警"、"账号健康"、"内容排期"、"矩阵日报"、"平台数据"、"涨粉分析"、"评论监控"、"限流检测"、"矩阵运营"
---

# 自媒体矩阵管家虾

多账号自媒体矩阵的统一调度中心。核心定位：**看数据、报异常、给建议**，不负责内容创作和发布。

## 输入格式

### 结构化输入（推荐）

用户提供 CSV/Excel 文件，必填字段：

| 字段名 | 说明 |
|--------|------|
| `account_name` | 账号名称 |
| `platform` | 平台（douyin/xiaohongshu/shipinhao/bilibili/weibo） |
| `account_id` | 账号 ID |
| `plays` | 昨日播放量 |
| `likes` | 昨日点赞数 |
| `comments` | 昨日评论数 |
| `shares` | 昨日分享数 |
| `new_fans` | 昨日涨粉数 |
| `total_fans` | 当前总粉丝数 |
| `avg_plays_30d` | 近30日日均播放量 |

可选字段：`consecutive_decline_days`（连续下滑天数）、`risk_signal`（风险信号描述）、`owner`（负责人）

### 自然语言输入

直接描述需求，引导用户提供数据文件或手动输入关键数据。

## 核心工作流

### 1. 数据分析（有数据文件时）

将用户提供的数据文件保存到 workspace，运行分析脚本：

```bash
python3 scripts/analyze_matrix.py <数据文件.csv> [--viral-threshold 3.0] [--decline-days 3] [--output report.md]
```

脚本输出包含：矩阵总览、异常预警、账号明细表格。

### 2. 异常检测逻辑

- **爆款预警**：`viral_score = 当日播放 / 30日均值 ≥ 3x`（可调）
- **数据下滑**：连续 ≥3 天下降
- **账号风险**：`risk_signal` 字段非空（限流/封禁等）
- **负面舆情**：评论数据中负面词占比 > 10%（参考 `references/sentiment-keywords.md`）

### 3. 报告生成与推送

分析完成后：
1. 将报告内容整理为飞书友好格式（Markdown）
2. 用 `feishu_create_doc` 创建云文档，或直接在对话中输出
3. 如需推送到群聊，配合 `message` 工具发送

### 4. 内容排期建议

当用户要求排期时：
- 询问各账号历史最佳发布时间（或从数据中推断）
- 结合内容类型标签（参考 `references/content-taxonomy.md`）
- 生成本周发布计划表格

## 参考资料

- **指标定义与健康基准值** → `references/platform-metrics.md`（异常阈值配置也在此）
- **内容分类与爆款特征** → `references/content-taxonomy.md`
- **舆情关键词库** → `references/sentiment-keywords.md`

## 与其他 Skill 的协作

| 场景 | 配合的 Skill |
|------|-------------|
| 爆款内容二次创作 | `video-script-writer-claw` |
| 预警推送到多渠道 | `cross-platform-messenger-claw` |
| 深度月度复盘 | `auto-data-analysis-claw` |
| 生成正式报告文件 | `financial-report-render-claw` |

## 注意事项

- 平台 API 数据通常 T+1，实时数据需用户手动导出
- 账号数量 > 50 时建议分批处理，避免脚本超时
- 情感分析基于关键词，复杂语境可能误判，仅供参考
- 不支持直接操作账号（发布/删除内容）
