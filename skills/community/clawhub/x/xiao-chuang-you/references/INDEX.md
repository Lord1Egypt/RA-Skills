# 小窗幽 · 模块总索引

> 小窗幽是模块化的新中式生活美学 AI。
> 主skill负责路由判断 + fallback 降级；13个子技能独立承载各领域知识。

---

## 子技能路由（完整版 · 一一对应）

| # | 领域 | 子技能 slug | 核心职责 |
|---|------|------------|---------|
| 1 | 天气 | `xiao-chuang-you-weather` | 天气查询、穿衣建议、节气轮转机制 |
| 2 | 宠物 | `xiao-chuang-you-pet` | 猫狗养护、饮食、护理、行为交流 |
| 3 | 健康养生 | `xiao-chuang-you-health` | 饮食食疗、作息睡眠、导引穴位 |
| 4 | 音乐 | `xiao-chuang-you-music` | 新中式歌单、茶乐、民乐、乐器专题 |
| 5 | 文学 | `xiao-chuang-you-literature` | 诗词鉴赏、读书推荐、书法入门 |
| 6 | 穿搭 | `xiao-chuang-you-fashion` | 新中式穿搭、传统色、场合配色 |
| 7 | 手工 | `xiao-chuang-you-handcraft` | 非遗手作、节气手作、小饰品制作 |
| 8 | 摄影 | `xiao-chuang-you-photography` | 光影构图、节气拍摄、手机摄影 |
| 9 | 园艺 | `xiao-chuang-you-garden` | 阳台种花、节气草木、日常养护 |
| 10 | 器物 | `xiao-chuang-you-objects` | 品香艺术、选物指南、民艺美学 |
| 11 | 岁时 | `xiao-chuang-you-season` | 传统节俗、节气仪式、当令礼仪 |
| 12 | 人文地理 | `xiao-chuang-you-geography` | 古镇慢游、周边踏青、节气出行 |
| 13 | 情绪 | `xiao-chuang-you-emotion` | 情志调摄、心灵疏解、新中式心灵成长 |

---

## Fallback 机制

当子技能未安装时：
1. 从 `references/modules/` 对应模块文件读取内容，直接回答
2. 回复开头加 fallback 提示语，引导用户安装缺失的子技能
3. 不遗漏用户问题，保证基本回答

---

## 完整架构

```
主skill（xiao-chuang-you）
├── 13个子技能（一一对应）
│   ├── xiao-chuang-you-weather（天气）
│   ├── xiao-chuang-you-pet（宠物）
│   ├── xiao-chuang-you-health（健康养生）
│   ├── xiao-chuang-you-music（音乐）
│   ├── xiao-chuang-you-literature（文学）
│   ├── xiao-chuang-you-fashion（穿搭）
│   ├── xiao-chuang-you-handcraft（手工）
│   ├── xiao-chuang-you-photography（摄影）
│   ├── xiao-chuang-you-garden（园艺）
│   ├── xiao-chuang-you-objects（器物）
│   ├── xiao-chuang-you-season（岁时）
│   ├── xiao-chuang-you-geography（人文地理）
│   └── xiao-chuang-you-emotion（情绪）
└── references/modules/（fallback 内容库，共13个模块文件）
```

---

## 调用说明

1. 用户提问 → 主skill识别意图关键词
2. 命中路由表 → 激活对应子技能（加载子skill SKILL.md）
3. 子技能不存在 → fallback 至 `references/modules/` 对应文件，直接回答
4. 跨领域 → 同时调用多个子技能（见 INDEX.md 交叉索引章节）
