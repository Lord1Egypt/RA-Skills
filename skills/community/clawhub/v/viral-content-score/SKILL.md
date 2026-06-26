# Viral Content Score — 内容病毒传播力评分

AI驱动的内容传播潜力预测引擎。输入标题/文案，即可获得跨平台（TikTok、Twitter/X、YouTube、Instagram）的病毒传播评分 + 优化建议。

## 核心能力

- **多维度评分**：情绪钩子、好奇心缺口、可分享性、趋势对齐度、平台匹配度
- **跨平台预测**：预估各平台曝光量区间
- **优化建议**：基于平台算法的具体文案调整策略
- **趋势风向标**：当前热门病毒传播模式识别

## 使用方式

```
GET http://8.145.54.67:3000/skill/viral-content-score?title=你的标题&platform=tiktok&language=zh
```

### 可选参数

| 参数 | 说明 | 示例 |
|------|------|------|
| title | 待评分标题/文案 | `?title=AI Agent 将取代所有SaaS` |
| platform | 目标平台 | `?platform=tiktok` |
| language | 语言 | `?language=zh` |

支持平台：`tiktok` / `twitter_x` / `youtube_shorts` / `instagram` / `all`

## 定价

¥0.50 / 次（AI收自动结算）

## 评分维度说明

| 维度 | 权重 | 说明 |
|------|------|------|
| Emotional Hook | 25% | 标题的情绪冲击力 |
| Curiosity Gap | 25% | 信息缺口引发的好奇心 |
| Shareability | 20% | 用户主动分享的意愿 |
| Trend Alignment | 15% | 与当前热点的契合度 |
| Platform Fit | 15% | 对特定平台算法的适配 |

## 适用场景

- 社交媒体运营团队内容策略
- 自媒体创作者标题优化
- 广告投放A/B测试前的预判
- 品牌营销内容策划