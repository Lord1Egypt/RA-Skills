# Changelog

## v1.0.1 (2026-08-17) — README 隐私强化

- README.md 隐私清理示例改用抽象占位符（避免任何真实值片段）

## v1.0.0 (2026-08-17) — 首次发布

### 核心功能
- 6 大数据源抓取（头条 / 微博 / B站 / 抖音 / 知乎 / 36氪）
- 6 大类 119 词关键词库（财经 / 房产 / 政策 / AI / 大模型公司）
- LLM 钩子 + 公众号标题 + 数据点生成
- 36h 时间窗口过滤（36氪 RSS 修复）
- 禁用词后处理（sanitizeForbiddenWords）
- 飞书 webhook 推送 + 限流 fallback
- 3 次重试机制 + send_alert 告警
- archive_unused 归档未选用

### 脚本
- generate_topics.js (1170 行) — 主程序
- notify_feishu.js (407 行) — 飞书推送
- archive_unused.js (306 行) — 归档
- run_daily.sh (153 行) — Shell wrapper
