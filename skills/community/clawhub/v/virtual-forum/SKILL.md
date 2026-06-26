---
name: virtual-forum
description: |
  虚拟论坛：让蒸馏的人物Skill就特定话题展开讨论。
  v5.0使用Claude Code CLI实现真正的多agent并行辩论。
  内置博弈论分析模块（信号博弈、议价博弈、联盟博弈、行为经济学）。
  触发词：「虚拟论坛」「发起讨论」「圆桌会议」「辩论」「主持讨论」「让XX YY讨论」
version: 5.0.2
---

# 🎭 虚拟论坛 Virtual Forum v5.0

> "让思想碰撞，让智慧涌现。"

## v5.0 架构

**v5.0** 使用外部CLI实现真正的多agent并行辩论：
- `v5/debate_parallel.sh` - Claude Code并行辩论脚本
- `v5/game-theory/` - 博弈论分析模块（可独立使用）

**不再维护**：v3.x 和 v4.0 已废弃（代码已移除）

## ⚠️ 安全警告

v5.0 会读取本地Skill文件并发送到外部API。请注意：

1. **Skill内容外传**：脚本读取 `SKILL.md` 文件内容，通过 `claude --print` 发送到外部
2. **敏感信息**：确保Skill文件中不包含密码、API密钥或其他私密信息
3. **路径配置**：使用环境变量 `SKILLS_DIR` 和 `OUTPUT_DIR` 避免硬编码路径
4. **网络传输**：所有Skill内容会通过HTTPS发送到Claude API

## 核心理念

虚拟论坛是一个**多角色讨论框架**，让蒸馏的人物Skill就特定话题展开有意义的对话。

不是简单的问答，而是**结构化的思想交锋**。

---

## 核心概念

### 两种讨论模式

| 模式 | 目标 | 适合场景 |
|------|------|---------|
| **探索性讨论** | 多角度剖析 → 发展 → 结论 | 复杂问题、需要综合视角 |
| **对抗性讨论** | 争辩 → 交锋 → 胜负/共识 | 决策分歧、需要明确方向 |
| **决策型讨论** | 多专家投票 → 加权评分 → 行动 | 需要拍板、有明确选项 |

### 可配置参数

```
轮次: 10 / 20 / 50 轮
主持人: 总主持 + 技术主持（可选）+ 魔鬼代言（可选）
参与者: 2-N 人
发言限时: 3分钟 / 5分钟 / 不限时
胜负判定: 点数制 / 投票制 / 让步制
输出格式: 对话流 / 报告流 / 决策流
```

---

## 执行流程

### Phase 1: 配置讨论

**收集用户配置**：

| 参数 | 选项 | 说明 |
|------|------|------|
| 话题 | 用户输入 | 要讨论的问题 |
| 模式 | 探索性/对抗性/决策型 | 讨论目标 |
| 轮次 | 10/20/50 | 讨论深度 |
| 参与者 | 2-N人 | 已蒸馏的Skill |
| 主持人风格 | 理性/犀利/整合 | 见下方 |
| 输出格式 | 对话流/报告流 | 结果展示 |

**主持人风格**：

| 风格 | 特点 | 适用场景 |
|------|------|---------|
| **理性主持人** | 客观中立，善于引导 | 学习型讨论 |
| **犀利主持人** | 追问到底，挑战每个观点 | 深度分析 |
| **整合主持人** | 归纳推动，形成共识 | 决策讨论 |

### Phase 2: 初始化讨论

1. **加载参与者Skill**
   - 读取每个参与者的SKILL.md
   - 提取心智模型、表达DNA、核心观点

2. **生成开场白**
   - 主持人自我介绍
   - 介绍话题和参与者
   - 说明讨论规则

3. **分配角色**（如有需要）
   - 技术主持：追问技术细节
   - 魔鬼代言：故意唱反调

### Phase 3: 执行讨论

**每轮结构**：

```
┌─────────────────────────────────────────┐
│ 第N轮                                    │
├─────────────────────────────────────────┤
│ 1️⃣ 轮流陈述   每人阐述观点 (限时)        │
│ 2️⃣ 交叉提问   可以点名某人提问           │
│ 3️⃣ 回应追问   被点名者回应              │
│ 4️⃣ 自由交锋   随机或点名辩论            │
│ 5️⃣ 回合总结   主持人简要归纳             │
└─────────────────────────────────────────┘
```

**不同模式的轮次差异**：

| 模式 | 第1-2轮 | 第3-N-2轮 | 最后2轮 |
|------|---------|-----------|---------|
| **探索性** | 开场陈述 | 深入探讨 | 综合结论 |
| **对抗性** | 立论 | 质疑反驳 | 胜负判定 |
| **决策型** | 各方立场 | 利弊分析 | 投票表决 |

### Phase 4: 追踪论点

**论点追踪表**：

```
┌──────────┬─────────┬─────────┬─────────┬─────────┐
│ 参与者   │ 核心论点 │ 被追问  │ 有效反驳│ 得分    │
├──────────┼─────────┼─────────┼─────────┼─────────┤
│ 巴菲特   │ 3个     │ 2次     │ 1次     │ +5      │
│ 芒格     │ 4个     │ 3次     │ 2次     │ +8      │
└──────────┴─────────┴─────────┴─────────┴─────────┘
```

**得分规则**：
- 提出有效论点：+2分
- 成功反驳对方：+3分
- 被有效反驳：-1分
- 回避问题：-2分

### Phase 5: 判定结果

| 判定方式 | 说明 |
|---------|------|
| **点数制** | 轮次结束统计点数，高分者胜 |
| **投票制** | 主持人/观众投票 |
| **让步制** | 一方主动承认对方更合理 |
| **无胜负** | 达成"保留分歧的共识" |

### Phase 6: 生成输出

**对话流格式**：
```
🎙️ 主持人：开场
💬 A：观点
💬 B：回应
⚔️ A vs B：交锋
📋 主持人：总结
```

**报告流格式**：
```
# 讨论报告

## 话题
...

## 参与者
...

## 核心论点
### A方
...
### B方
...

## 共识
...

## 分歧
...

## 结果
...
```

**决策流格式**：
```
# 决策建议

## 问题
...

## 方案A | 方案B | 方案C
...

## 投票结果
...

## 建议行动
1. ...
2. ...
```

---

## 使用示例

```
# 启动虚拟论坛
发起讨论：巴菲特 vs 芒格，当前市场该激进还是保守？

# 指定配置
虚拟论坛
模式：对抗性
轮次：20
参与者：巴菲特、芒格、马斯克
主持人：犀利主持人
输出：对话流

# 快速启动
让乔布斯和马斯克讨论：电动车行业未来
```

---

## 技术实现

### 核心模块

```
virtual-forum/
├── forum-engine.js       # 主讨论引擎
├── moderator.js          # 主持人逻辑
├── argument-tracker.js   # 论点追踪
├── verdict-calculator.js # 胜负判定
└── output-formatter.js   # 输出格式化
```

### 关键功能

1. **Skill加载器**：读取已蒸馏的Skill
2. **观点生成器**：基于Skill的思维框架生成观点
3. **论点追踪器**：记录每轮交锋
4. **判定引擎**：计算最终结果
5. **格式化器**：生成可读输出

---

## 与女娲的关系

女娲蒸馏人物，虚拟论坛让蒸馏的人物"活"起来。

- **女娲** → 造人：提取思维框架
- **虚拟论坛** → 用人：让框架互动

---

## 诚实边界

- 虚拟论坛的观点是基于Skill中记录的思维框架"模拟"生成
- 不是真正的人物在思考
- 结果应作为参考，不是真理
- 胜负判定是游戏化的，帮助结构化思考

## v3.6 行为经济学增强版 (2026-04-12)

基于三本经典著作实现的行为经济学模块：
- **前景理论** (Kahneman & Tversky, 1979) - 风险决策分析
- **有限理性模型** (Simon & Jones, 1999) - 认知限制与决策
- **助推理论** (Thaler & Sunstein, 2008) - 选择架构设计

### 新增核心模块

```javascript
const { BehavioralEconomicsSubagentArena } = require('./v3/behavioral-arena');

const arena = new BehavioralEconomicsSubagentArena();
await arena.initArenaWithBehavioralEconomics({
  topic: "气候变化政策",
  participants: [
    { name: "环保主义者", position: "激进减排" },
    { name: "经济学家", position: "成本效益平衡" }
  ],
  rounds: 5
});
```

---

## v3.7 博弈论增强版 (2026-04-18)

实现真正的博弈论计算，不再是"博弈论主题装饰"。基于：
- **Myerson (1991)** - Nash均衡计算公式
- **Fudenberg & Tirole (1991)** - 博弈论经典教材
- **Brown (1951)** - Fictitious Play学习动态

### 核心新增模块

```javascript
// 真正的博弈论框架
const { GameTheoryArena, GameStructure, BayesianBeliefSystem } = require('./v3/game-theory-v2');

const arena = new GameTheoryArena();
await arena.initArenaWithGameTheory({
  topic: "NVDA估值是否合理",
  participants: [
    { name: "巴菲特", skillName: "buffett" },
    { name: "木头姐", skillName: "cathie-wood" }
  ],
  discountFactors: { '巴菲特': 0.95, '木头姐': 0.85 },
  outsideOptions: { '巴菲特': 15, '木头姐': 5 }
});

// 计算Nash均衡
const eq = arena.calculateNashEquilibrium();
// 输出: { type: 'mixed', player1: {prob: 0.7}, player2: {prob: 0.6}, confidence: 0.9 }

// 获取博弈论报告
console.log(arena.getGameTheoryReport());
```

### 理论实现

#### 1. 博弈结构 (GameStructure)

显式定义支付矩阵和策略空间：
- **策略空间**: 每个参与者可选择"强硬"或"让步"
- **支付矩阵**: 博弈收益的完整映射
- **Nash均衡计算**: 2x2博弈使用解析公式，更复杂博弈使用Fictitious Play近似

#### 2. Nash均衡计算

**2x2博弈解析解** (Myerson 1991):

```
p = (d - c) / (a + d - b - c)
其中:
a = A强硬B强硬的收益
b = A强硬B让步的收益
c = A让步B强硬的收益
d = A让步B让步的收益
```

**N人博弈**: 使用Fictitious Play迭代逼近均衡

#### 3. 贝叶斯信念更新 (BayesianBeliefSystem)

真正的贝叶斯更新，非硬编码乘数：

```
P(H|E) = P(E|H) × P(H) / P(E)

// 例如：观察到攻击性行为 → 更新对手类型信念
posterior = bayesianUpdate('对手', 'aggressive')
// 返回: { prior, posterior, updateStrength }
```

### 博弈论功能

#### 均衡分析
```javascript
const eq = arena.calculateNashEquilibrium();
// { type: 'mixed', confidence: 0.95, equilibriumPayoff: 45.2 }
```

#### 策略建议
```javascript
// 基于均衡分析生成策略建议
const advice = arena.getStrategyAdvice('巴菲特');
// 返回: { shouldConcede: false, utility: 38.5, reason: '...' }
```

#### 贝叶斯预测
```javascript
const prediction = arena.beliefSystem.predict('木头姐');
// 返回: { type: 'growth', confidence: 0.78 }
```

### 对比: v3.5 vs v3.7

| 功能 | v3.5 | v3.7 |
|------|------|------|
| 折扣因子 | ✅ | ✅ |
| BATNA外部选项 | ✅ | ✅ |
| 贝叶斯更新 | ⚠️ 硬编码乘数 | ✅ 真正的贝叶斯 |
| Nash均衡 | ❌ | ✅ 解析解+Fictitious Play |
| 支付矩阵 | ⚠️ 隐式 | ✅ 显式定义 |
| 占优策略检验 | ❌ | ✅ |
| 博弈树/逆向归纳 | ❌ | 🔜 后续版本 |

### 文件结构

```
v3/
├── behavioral/               # 行为经济学模块
├── behavioral-arena.js      # v3.6 行为经济学竞技场
├── game-theory-arena.js     # v3.5 博弈论竞技场（基础版）
└── game-theory-v2.js        # v3.7 博弈论竞技场（真正实现）🆕
```

**使用建议**：
- 简单辩论使用 `SubagentArena` (v3.4)
- 博弈论分析使用 `GameTheoryArena` (v3.7) ← 推荐
- 行为经济学 + 博弈论使用 `BehavioralEconomicsSubagentArena` (v3.6)

### 行为经济学功能

#### 1. 前景理论引擎
- **价值函数**: 收益凹函数(风险厌恶) vs 损失凸函数(风险寻求)
- **概率加权**: 高估小概率，低估中高概率
- **四折模式**: 解释彩票偏好、保险购买、确定性效应
- **框架效应**: 增益框架 vs 损失框架的偏好逆转
- **损失厌恶**: λ ≈ 2.25，损失影响是收益的2.25倍

#### 2. 有限理性引擎
- **满意化决策**: 寻找足够好的方案而非最优
- **可得性启发**: 基于记忆可提取性判断概率
- **代表性启发**: 基于相似性判断，忽视基础概率
- **锚定调整**: 从初始值出发，调整不足
- **双系统理论**: 系统1(快速直觉) vs 系统2(慢速理性)
- **注意力模型**: 注意力作为稀缺资源的分配

#### 3. 助推理论引擎
- **选择架构**: 默认选项、排序效应、简化选择
- **社会规范**: 利用从众心理和社会证明
- **框架设计**: 增益/损失/社会框架的应用
- **反馈机制**: 即时反馈、社会比较、游戏化
- **承诺机制**: 软承诺到硬承诺的设计

### 辩论中的应用

#### 偏差检测
```javascript
const insights = arena.analyzeRoundBehavior(roundData);
// 检测：损失厌恶、确定性效应、可得性偏差、锚定效应等
```

#### 策略建议
```javascript
const advice = arena.generateBehavioralAdvice(agentName, {
  position: "支持",
  opponentPosition: "反对",
  topic: "议题",
  audienceProfile: { riskAverse: true }
});
```

#### 综合报告
```javascript
const report = arena.generateBehavioralReport();
// 包含：博弈论分析 + 行为经济学洞察 + 综合策略建议
```

---

## v3.9 高级博弈论完整版 (2026-04-18)

v3.8基础上新增P1级别模块：
- **Rubinstein议价博弈** - 轮流议价模型
- **Shapley联盟博弈** - 联盟价值分配与核心稳定性

理论依据：
- **Rubinstein (1982)** - 轮流议价均衡
- **Shapley (1953)** - 联盟博弈核心论文

### 核心新增模块

```javascript
const {
    SignalingGame,
    RepeatedGameEngine,
    InformationDesigner,
    BargainingGame,      // 🆕 议价博弈
    CoalitionGame,       // 🆕 联盟博弈
    AdvancedGameTheoryArena,
} = require('./v3/advanced-game-theory');
```

### 4. 议价博弈 (BargainingGame) [P1]

**核心问题**：蛋糕如何分配？谁先出价？耐心程度如何影响结果？

**Rubinstein均衡公式**：
```
p1_share = (1 - δ₂) / (1 - δ₁δ₂)  // P1先出价时
p2_share = δ₂(1 - δ₁) / (1 - δ₁δ₂)
```

**功能**：
| 函数 | 说明 |
|------|------|
| `calculateEquilibrium(delta1, delta2, firstMover)` | 计算均衡份额 |
| `generateOffer(player, myDelta, oppDelta, value)` | 生成出价建议 |
| `evaluateOffer(player, offeredShare, myDelta, oppDelta)` | 评估是否接受 |
| `getBargainingPhase()` | 获取议价阶段分析 |

**示例**：
```javascript
const bargaining = new BargainingGame();
const eq = bargaining.calculateEquilibrium(0.9, 0.85, 'player1');
// P1先出价: P1=57.9%, P2=42.1%

const offer = bargaining.generateOffer('巴菲特', 0.9, 0.85, 100);
// 返回出价建议和策略分析

const eval = bargaining.evaluateOffer('马斯克', 0.35, 0.9, 0.85);
// 返回是否应该接受当前出价
```

### 5. 联盟博弈 (CoalitionGame) [P1]

**核心问题**：谁和谁结盟？收益如何公平分配？联盟是否会崩溃？

**Shapley公式**：
```
φ_i(v) = Σ_{S⊆N\{i}} [|S|!(n-|S|-1)!/n!] × [v(S∪{i}) - v(S)]
```

**功能**：
| 函数 | 说明 |
|------|------|
| `calculateShapleyValues()` | 计算Shapley值 |
| `calculateAllCoalitions()` | 所有联盟及其价值 |
| `checkCoreStability(shapley)` | 核心稳定性检测 |
| `predictOptimalCoalition()` | 预测最优联盟 |

**示例**：
```javascript
const coalition = new CoalitionGame();
coalition.init(['巴菲特', '马斯克', '木头姐'], (S) => {
    if (S.length === 0) return 0;
    if (S.length === 1) return 1;
    if (S.length === 2) return 3;
    return 5;  // 三人联盟最大价值
});

const shapley = coalition.calculateShapleyValues();
// { '巴菲特': 2.33, '马斯克': 2.33, '木头姐': 2.33 }

const stability = coalition.checkCoreStability(shapley.shapleyValues);
// { isStable: true, stabilityScore: 100 }
```

### 对比: v3.8 vs v3.9

| 功能 | v3.8 | v3.9 |
|------|------|------|
| 信号博弈 | ✅ | ✅ |
| 重复博弈 | ✅ | ✅ |
| 信息设计 | ✅ | ✅ |
| **议价博弈** | ❌ | ✅ |
| **联盟博弈** | ❌ | ✅ |
| **Shapley值** | ❌ | ✅ |
| **核心稳定性** | ❌ | ✅ |

### 文件结构

```
v3/
├── behavioral/               # 行为经济学模块
├── behavioral-arena.js      # v3.6
├── game-theory-arena.js     # v3.5
├── game-theory-v2.js        # v3.7
├── advanced-game-theory.js  # v3.9 ⭐ 完整版
└── game-theory-v2.js       # v3.7
```

**使用建议**：
- 简单辩论: `SubagentArena` (v3.4)
- 博弈论分析: `GameTheoryArena` (v3.7)
- **深度辩论（推荐）**: `AdvancedGameTheoryArena` (v3.9)

### 理论来源

1. **Kahneman, D., & Tversky, A. (1979)**. Prospect Theory: An Analysis of Decision under Risk. *Econometrica*, 47(2), 263-291.

2. **Jones, B. D. (1999)**. Bounded Rationality. *Annual Review of Political Science*, 2, 297-321.

3. **Thaler, R. H., & Sunstein, C. R. (2008)**. Nudge: Improving Decisions About Health, Wealth, and Happiness. Yale University Press.

