# 值得练 — train-priority 设计文档

## 命令

```
/pvp 值得练
/pvp 值得练 <联盟>
```

## 用途

自动找当前库存里最值得投入星尘/糖果/XL糖/精英学习器的宝可梦，按培养紧迫度排序。

## 数据来源

- `data/my_pokemon.json` — 用户库存
- `cache/rankings-{league}.json` — PvPokeTW 排名
- `data/elite_moves.json` — 精英招式

## 排序算法

### 加权公式

| 因子 | 权重 | 说明 |
|------|------|------|
| PvPokeTW 物种排名 | 40% | 该联盟下排名分，排名越靠前越高 |
| IV 排名 | 25% | 与最佳 IV 对比，进入前 50 按排名计分，未进入计 0 |
| 已培养状态 | 15% | 未培养直接加分，已培养降权 |
| 缺推荐配招 | 10% | 推荐配招 vs 实际配招，缺失越多分越高 |
| 常见配队需求 | 10% | 是否在配队推荐 / 热门环境中是核心组件 |

### 分数计算（伪代码）

```
score = 0

// 物种排名分（0~40）
speciesScore = max(0, mapRankToScore(pvpokeRank))  // rank #1=40, #50=20, #100=0
score += speciesScore

// IV排名分（0~25）
if ivRank <= 50:
  ivScore = max(0, 25 - ivRank * 0.5)  // #1=24.5, #50=0
  score += ivScore

// 已培养状态（-15~15）
if !built:
  score += 15
else:
  score -= 10

// 缺配招（0~10）
missing = count(recommendedMoves - actualMoves)
score += min(10, missing * 3)

// 配队需求（0~10）
if inRecommendedTeam:
  score += 10
```

## 输出卡片格式

```
🔥 值得练｜{联盟名}

1. {宝可梦名}
   PvPokeTW：#{rank}
   IV：{a}/{d}/{s}（#{ivRank}）
   状态：未培养 / 已培养
   推荐配招：
   小招：{fastMove}
   充能1：{charged1}
   充能2：{charged2}
   建议：{priority}

2. {宝可梦名}
   ...
```

### 建议文案

| 条件 | 建议 |
|------|------|
| 未培养 + 排名前10 + IV前10 | ⭐ 优先培养 |
| 未培养 + (排名前30 或 IV前30) | 推荐培养 |
| 未培养 | 值得培养 |
| 已培养 + 缺配招 | 更新配招 |
| 已培养 | 可用 ✓ |

## 不做

- 不输出 product / 百分比 / 接近度
- 不编数据（IV 排名仅当真实存在时输出）
- 不做跨联盟合并排序
- 不涉及 XL 糖数量评估（仅为展示，不读取实际库存）

## 实现位置

- `src/train.ts` — `/pvp 值得练` 命令逻辑
- `src/index.ts` — 新增路由
