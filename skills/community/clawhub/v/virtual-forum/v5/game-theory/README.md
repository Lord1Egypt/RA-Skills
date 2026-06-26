# 博弈论分析模块 v5.0

> 独立的博弈论分析工具，可配合辩论使用

## 目录结构

```
game-theory/
├── advanced-game-theory.js   # 高级博弈论（信号博弈、重复博弈、信息设计、议价、联盟）
├── game-theory-v2.js         # v3.7 博弈论引擎（Nash均衡、贝叶斯更新）
├── game-theory-arena.js      # 博弈论竞技场
├── behavioral-arena.js       # 行为经济学竞技场
├── advanced/                 # 高级模块
│   ├── signaling.js          # 信号博弈
│   ├── repeated-games.js    # 重复博弈
│   ├── mechanism-design.js  # 机制设计
│   ├── evolutionary.js      # 演化博弈
│   └── bargaining.js        # 议价博弈
├── core/                    # 核心算法
│   ├── strategic-game.js    # 策略博弈
│   ├── bayesian-game.js     # 贝叶斯博弈
│   ├── game-theory-engine.js # 博弈论引擎
│   └── game-recognizer.js   # 博弈识别器
├── behavioral/             # 行为经济学
│   ├── prospect-theory.js   # 前景理论
│   ├── bounded-rationality.js # 有限理性
│   └── nudge-theory.js      # 助推理论
└── extensions/              # 扩展
    ├── visualization.js     # 可视化
    ├── sequential-equilibrium.js # 序列均衡
    └── extensive-form.js    # 扩展式博弈
```

## 理论依据

| 模块 | 理论依据 |
|------|---------|
| 信号博弈 | Spence (1973), Cho & Kreps (1987) |
| 重复博弈 | Folk Theorem, Fudenberg & Tirole (1991) |
| 议价博弈 | Rubinstein (1982), Nash (1950) |
| 联盟博弈 | Shapley (1953), Bondareva (1963) |
| 行为经济学 | Kahneman & Tversky (1979), Thaler (1980) |

## 使用示例

```javascript
const { SignalingGame } = require('./game-theory/advanced/signaling');

const signaling = new SignalingGame();
const result = signaling.assessSignalCredibility(
    "伊朗核计划是为了和平目的",
    "strategic",
    0.5
);
console.log(result);
```

## 与辩论的结合

博弈论模块可用于分析辩论中的策略：

1. **信号博弈** - 评估各方发言的可信度
2. **联盟博弈** - 分析各方可能的联盟
3. **议价博弈** - 计算均衡份额
4. **行为经济学** - 分析认知偏差对决策的影响
