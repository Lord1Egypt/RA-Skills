---
name: "Skill Router — 智能技能路由引擎"
description: "两阶段路由：embedding粗筛之后LLM精排，977技能里挑top5。中文query自动翻成英文再匹配，外加三重拒选防线，纯信息类查询直接踢到L0工具，别浪费LLM token。"
version: "2.1.2"
author: "炎哥"
homepage: https://github.com/awoo129/wangyan
source: https://github.com/awoo129/wangyan/tree/main/experiments/skill-router-p0
tags: ["tool-selection", "skill-router", "routing", "intent-classification", "embedding"]
---

# Skill Router

skill库大到977个以后，让LLM一条条翻着看太傻也太贵。这个router用两段路由解决：先embedding粗筛，再LLM精排。

## 怎么用

```python
from skill_router import SkillRouter

router = SkillRouter()
result = router.route("做一篇新生儿低血糖的系统综述")
# → top1: literature-search (96%)

print(router.route_formatted("帮我画个森林图"))
```

## 干了什么

```
Query → BM25 + 翻译桥(双通道embedding) → RRF融合 → top5候选 → 拒选防线 → LLM精排
                                                                  ↓
                                                          拒选的走L0工具
```

### 四个块

- **BM25关键词匹配** — 对英文skill名/描述做关键词硬匹配
- **中英翻译桥** — 中文query先翻成英文，0.3zh + 0.7en加权揉一起
- **RRF排序** — 加权Reciprocal Rank Fusion，BM25×0.5 + Embed×2.0
- **三重拒选** — 信息查询/任务重叠/分数阈值，三道坎

### 拒选规则

三道防线：

1. **信息查询** — query里只有"天气"/"百科"/"用药"这类词，没有强技能关键词 → 不走LLM，直接L0工具
2. **任务重叠** — 根本看不出要干什么 → 打回噪声
3. **分数阈值** — RRF top1 < 0.008 或 gap < 0.06 → 太模糊，拒了

## 什么时候用

skill超过50个以后，传统一条条审查的方案token成本就扛不住了。特别是中英文混着用的场景——用户说中文但skill库全是英文名。还有就是明确不想让LLM碰的信息查询类请求，路由器帮你拦外面。

## 要求

- Python 3.10+
- sentence-transformers (all-MiniLM-L6-v2)
- numpy
- 第一次跑要联网下embedding模型，大概80MB

## 隐私

路由引擎本身全本地跑：skill索引存在本地，embedding模型本地加载，query不走外部API。

L0工具层（技能全拒后的保底）可能调用外部API：PubMed、Semantic Scholar、TinyFish等。
这些工具的API key通过环境变量注入，详见tool_catalog.json中的`${VAR_NAME}`占位符。

拒选防线保证纯查询类请求不会进LLM上下文。
