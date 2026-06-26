---
name: web-data-monitor-claw
description: |
  全网数据探测虾 — 监控竞品官网或特定站点的页面变动，自动巡查并在关键内容变化时发送通知。
  适用场景：竞品价格监控、法规更新监控、招聘信息监控、新闻舆情监控、技术文档更新监控。
  触发关键词：监控 爬虫 网页变动 竞品监控 价格监控 法规更新 舆情监控 数据采集 网站监控 页面变化 自动抓取 web-data-monitor
  Use when the user wants to: monitor a website for changes, track competitor prices, watch for regulatory updates, scrape web data periodically, or get notified when specific page content changes.
---

# 全网数据探测虾 (web-data-monitor-claw)

监控竞品官网或特定站点的页面变动，7×24 小时自动巡查，第一时间捕获关键变化。

## 核心工作流

### 步骤 1：接收监控任务

从用户输入中提取：
- 目标网址（必填）
- 监控频率（每小时/每天/每周，默认每天）
- 监控内容（价格/标题/全文/特定 CSS 选择器）
- 变动阈值（如价格变动 >5%）
- 通知方式（飞书/邮件/webhook）

支持两种输入格式：
1. **结构化**：Excel/CSV 文件，含监控任务清单
2. **自然语言**：如"监控 XX 公司官网的产品价格，每天检查一次"

### 步骤 2：首次快照

使用 `scripts/web-monitor.sh` 执行首次抓取：
```bash
./scripts/web-monitor.sh add-task \
  --url "https://example.com/products" \
  --frequency "daily" \
  --selector ".price" \
  --notify "feishu"

./scripts/web-monitor.sh run-check --task-id "task-001"
```

首次抓取生成基准版本（Baseline），存储为 JSON 快照。

### 步骤 3：定期巡查

按设定频率自动访问目标网页，与基准版本对比，识别：
- 文本变化（新增/删除/修改）
- 数值变化（价格/数量/百分比）
- 结构变化（新增/删除页面元素）

### 步骤 4：变动分析与通知

判断变动是否达到通知阈值：
- **重要变动** → 立即推送飞书消息
- **一般变动** → 汇总到日报/周报
- **微小变动** → 仅记录日志

通知内容包含：变动前/变动后/变动幅度/原始链接。

### 步骤 5：数据归档

将抓取的原始数据归档至数据仓库，供其他数字员工使用（数据分析虾、报告生成虾等）。

## 关键设计原则

- **原始采矿**：抓取第一手原始数据，不做主观加工
- **高频巡查**：支持分钟级监控，确保信息实时性
- **智能过滤**：自动过滤广告、噪音、无关变动
- **反爬虫对抗**：模拟真实浏览器行为，避免被封禁

## 依赖工具

- `curl`、`jq`、`pup`（HTML 解析）、`diff`
- 安装 pup：`brew install pup` 或 `go install github.com/ericchiang/pup@latest`

## 参考文件

- **监控规则**：`references/monitoring-rules.md` — 不同类型网站的监控策略
- **提取模板**：`references/extraction-templates.md` — 常见网站结构的数据提取模板
- **反爬虫策略**：`references/anti-detection.md` — 应对网站反爬虫机制的策略库

## 与其他虾的协作

| 上下游 | 虾名 | 数据流向 |
|--------|------|---------|
| 下游 | data-cleaning-claw | 原始数据 → 清洗后提供给分析类员工 |
| 下游 | compliance-archive-claw | 监控到新法规时自动归档 |
| 下游 | cross-platform-messenger-claw | 变动通知推送到多个平台 |
| 下游 | auto-data-analysis-claw | 抓取的竞品数据用于分析 |

## 已知限制

- 仅支持公开可访问的网页，无法监控需要登录的内容
- 动态加载（JavaScript 渲染）的页面需使用浏览器模式（较慢）
- 部分网站有严格的反爬虫机制，可能被封禁 IP
- 不支持监控移动 App 内的内容
