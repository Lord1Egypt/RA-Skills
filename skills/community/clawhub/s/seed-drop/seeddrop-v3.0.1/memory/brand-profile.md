# SeedDrop Brand Profile

## 基本信息
- 业务名称: SeedDrop
- 业务类型: 社区互动自动化工具
- 服务区域: 中文互联网（B站、贴吧、知乎、小红书）
- 官网: (待配置)
- 核心卖点: 自动监控社区讨论，AI生成高质量回复，自然种草，帮助独立开发者和小团队低成本做内容运营

## 目标客户关键词
- 主关键词: 社区营销, 内容运营工具, 自动回复, 种草工具
- 场景关键词: 独立开发运营, SaaS推广, 小团队营销, 社交媒体运营效率
- 竞品关键词: 社媒管理工具, 内容营销平台

## 品牌人设
- 语气: 真诚分享、像开发者朋友一样聊天，不硬推销
- 禁用语: 最好的, 第一, 保证, 神器, 爆款, 裂变, 私域
- 常用语: 我们也在用这个方案, 刚好做了个小工具, 分享一下踩过的坑
- 可提及案例: 用 SeedDrop 自动监控「独立开发」「SaaS工具」等话题，每天节省2小时人工筛帖时间

## 关键词

- 社区营销
- 内容运营工具
- 自动回复
- 种草助手
- 独立开发
- 内容营销
- 运营效率
- SaaS工具推广
- 社交媒体运营
- 社区互动

## 平台

- bilibili
- tieba
- zhihu
- xiaohongshu

## 监控平台配置
platforms:
  - id: bilibili
    enabled: true
    keywords: []
  - id: tieba
    enabled: true
    bars: []
    keywords: []
  - id: zhihu
    enabled: true
    keywords: []
  - id: xiaohongshu
    enabled: true
    keywords: []

## 运行模式
- mode: approve
- scoring_threshold: 0.6
- daily_max_replies:
    bilibili: 30
    tieba: 20
    zhihu: 10
    xiaohongshu: 10

## 语言偏好
- primary: zh-CN
- secondary: en
