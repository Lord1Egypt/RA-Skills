# 能力矩阵 · 完整版

> ⚠️ 全部13个模块已迁移为独立子技能。主skill负责路由 + fallback 降级。
> 此文件记录完整能力目录，与路由表一一对应。

---

## 子技能一览

| # | 领域 | 子技能 | 核心职责 |
|---|------|--------|---------|
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

## Fallback 内容库

| 模块 | 文件 | 对应子技能 |
|------|------|-----------|
| 天气 | `modules/天气.md` | `xiao-chuang-you-weather` |
| 宠物 | `modules/宠物.md` | `xiao-chuang-you-pet` |
| 饮食 | `modules/饮食.md` | `xiao-chuang-you-health` |
| 作息 | `modules/作息.md` | `xiao-chuang-you-health` |
| 养生 | `modules/养生.md` | `xiao-chuang-you-health` |
| 音乐 | `modules/音乐.md` | `xiao-chuang-you-music` |
| 文学 | `modules/文学.md` | `xiao-chuang-you-literature` |
| 穿搭 | `modules/穿搭.md` | `xiao-chuang-you-fashion` |
| 手工 | `modules/手工.md` | `xiao-chuang-you-handcraft` |
| 摄影 | `modules/摄影.md` | `xiao-chuang-you-photography` |
| 园艺 | `modules/园艺.md` | `xiao-chuang-you-garden` |
| 器物 | `modules/器物.md` | `xiao-chuang-you-objects` |
| 岁时 | `modules/岁时.md` | `xiao-chuang-you-season` |
| 人文地理 | `modules/人文地理.md` | `xiao-chuang-you-geography` |
| 情绪 | `modules/情绪.md` | `xiao-chuang-you-emotion` |

> **Fallback 说明**：子技能未安装时，主skill自动降级至 `references/modules/` 对应文件读取内容，保证用户问题不被遗漏。

---

## 完整架构

```
xiao-chuang-you（主skill）
└── 13个子技能（一一对应）
    xiao-chuang-you-weather（天气）
    xiao-chuang-you-pet（宠物）
    xiao-chuang-you-health（健康养生）
    xiao-chuang-you-music（音乐）
    xiao-chuang-you-literature（文学）
    xiao-chuang-you-fashion（穿搭）
    xiao-chuang-you-handcraft（手工）
    xiao-chuang-you-photography（摄影）
    xiao-chuang-you-garden（园艺）
    xiao-chuang-you-objects（器物）
    xiao-chuang-you-season（岁时）
    xiao-chuang-you-geography（人文地理）
    xiao-chuang-you-emotion（情绪）
```
