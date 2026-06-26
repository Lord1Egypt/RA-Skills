# trump_tracker.history.md 修改记录

## [2026-03-27 19:30] 初始版本发布 (Python)
- 新增川普追踪技能 `trump-tracker`。
- 引入 `feedparser` + `TextBlob` 架构。
- **动态抓取器 (TrumpMonitor)**: 支持获取主流全球 RSS 实时新闻。
- **不靠谱预测模型 (TrumpUnreliableModel)**:
  - 实现基于经典川普关键词的关键词权重算法。
  - 集成情感分析极端性检测。
  - 自动输出：不靠谱指数、预测执行率、模型人性化点评。
- 全程采用 Python 编写。
