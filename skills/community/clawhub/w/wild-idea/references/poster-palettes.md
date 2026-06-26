# WildIdea 海报配色方案库

每个 round 对应一个不同的配色方案，避免连续轮次视觉重复。

| 轮次/主题 | BADGE_COLOR | BADGE_ACCENT | GRADIENT | CARD_BORDER (0→5) | INSIGHT_BG | INSIGHT_BORDER | INSIGHT_HEADING |
|-----------|-------------|-------------|----------|-------------------|------------|----------------|-----------------|
| R1 新能源汽车 | #f59e0b | #fbbf24 | `135deg, #a78bfa, #60a5fa, #34d399` | `#6366f1,#8b5cf6 / #f59e0b,#f97316 / #10b981,#34d399 / #ef4444,#f43f5e / #3b82f6,#60a5fa / #8b5cf6,#a78bfa` | `#2a1a44, #1a2436` | `#6d28d944` | `#c4b5fd` |
| R2 竞争优势 | #f59e0b | #fbbf24 | `135deg, #a78bfa, #60a5fa, #34d399` | 同R1 | `#2a1a44, #1a2436` | `#6d28d944` | `#c4b5fd` |
| R3 造手机 | #06b6d4 | #22d3ee | `135deg, #38bdf8, #a78bfa, #f472b6` | `#6366f1,#06b6d4 / #f59e0b,#f97316 / #10b981,#34d399 / #ef4444,#fb7185 / #3b82f6,#818cf8 / #8b5cf6,#d946ef` | `#1a2444, #1a1a36` | `#6366f144` | `#a5b4fc` |
| R4 vivo影像 | #8b5cf6 | #a78bfa | `135deg, #a78bfa, #60a5fa, #34d399` | 同R1 | `#1a1a36, #1a2436` | `#6366f144` | `#a5b4fc` |
| R5 vivo第二次迭代 | #f43f5e | #fb7185 | `135deg, #fb7185, #f59e0b, #34d399` | `#f43f5e,#fb7185 / #f59e0b,#fbbf24 / #10b981,#34d399 / #ef4444,#dc2626 / #3b82f6,#60a5fa / #8b5cf6,#a78bfa` | `#2a1a1a, #1a2436` | `#f43f5e44` | `#fb7185` |

## 快速选色规则

- **首次轮次** → 紫色/琥珀（#f59e0b / #a78bfa）
- **二次迭代（前轮已ban）** → 警告红/玫瑰（#f43f5e / #fb7185）
- **手机/科技主题** → 青色/蓝（#06b6d4 / #22d3ee）
- **学术/研究主题** → 紫色/紫罗兰（#8b5cf6 / #a78bfa）
- 每轮卡片顶部分别用6组渐变色（card-N），顺序不可重复使用

## 卡片 border 渐变色通用排列（6色循环）

按 N=0..5 顺序分配，每个 round 微调首色以制造差异感：

```
card-0: purple/indigo → blue/cyan
card-1: amber → orange
card-2: emerald → jade
card-3: red → rose
card-4: blue → indigo
card-5: violet → magenta
```

第二轮迭代时可整体向右shift一个色系（如首色从紫蓝改为玫瑰红）以视觉区分两轮产出。
