# 行为经济学模块 (Behavioral Economics Module)

## 版本: v3.6.1

基于三本经典学术著作实现的行为经济学分析引擎。

## 理论基础

### 1. 前景理论 (Prospect Theory)
**Kahneman, D., & Tversky, A. (1979).** Prospect Theory: An Analysis of Decision under Risk. *Econometrica*, 47(2), 263-291.

**核心概念:**
- **价值函数**: v(x) = x^α (收益) 或 -λ(-x)^β (损失)
- **概率加权**: w(p) = exp(-(-ln(p))^γ)
- **损失厌恶**: λ ≈ 2.25 (损失影响是收益的2.25倍)
- **四折模式**: 解释彩票偏好、保险购买、确定性效应

**数学实现:**
```javascript
const engine = new ProspectTheoryEngine({
  alpha: 0.88,  // 收益凹度
  beta: 0.88,   // 损失凸度
  lambda: 2.25, // 损失厌恶系数
  gamma: 0.61,  // 收益概率加权
  delta: 0.69   // 损失概率加权
});
```

### 2. 有限理性 (Bounded Rationality)
**Jones, B. D. (1999).** Bounded Rationality. *Annual Review of Political Science*, 2, 297-321.

**核心概念:**
- **满意化决策**: 寻找足够好的方案而非最优
- **可得性启发**: 基于记忆可提取性判断概率
- **代表性启发**: 基于相似性判断，忽视基础概率
- **双系统理论**: 系统1(快速直觉) vs 系统2(慢速理性)
- **注意力模型**: 注意力作为稀缺资源

**认知参数:**
```javascript
const engine = new BoundedRationalityEngine({
  attentionCapacity: 7,     // 工作记忆容量 (Miller, 1956)
  processingSpeed: 1.0,     // 信息处理速度
  aspirationLevel: 0.7,     // 满意化阈值
  searchDepth: 5            // 搜索深度限制
});
```

### 3. 助推理论 (Nudge Theory)
**Thaler, R. H., & Sunstein, C. R. (2008).** Nudge: Improving Decisions About Health, Wealth, and Happiness. Yale University Press.

**核心概念:**
- **选择架构**: 通过环境设计影响决策
- **默认选项**: 利用现状偏见
- **社会规范**: 利用从众心理
- **框架效应**: 增益/损失框架
- **反馈机制**: 即时反馈促进改变

**架构配置:**
```javascript
const engine = new NudgeTheoryEngine({
  defaultOptions: { ... },
  architectureConfig: {
    orderEffects: true,
    framing: 'neutral',
    socialProof: true,
    feedbackLoops: true
  },
  nudgeIntensity: 0.5
});
```

## 使用示例

### 基础用法

```javascript
const { BehavioralEconomicsArena } = require('./behavioral');

const arena = new BehavioralEconomicsArena();

// 初始化辩论
await arena.initBehavioralDebate(
  "气候变化政策",
  [
    { name: "环保主义者", position: "激进减排" },
    { name: "经济学家", position: "成本效益平衡" }
  ]
);

// 分析回合
const insights = arena.analyzeRoundBehavior(roundData);

// 生成策略建议
const advice = arena.generateBehavioralAdvice(agentName, context);
```

### 前景理论示例

```javascript
const { ProspectTheoryEngine } = require('./behavioral/prospect-theory');

const pt = new ProspectTheoryEngine();

// 计算前景价值
const value = pt.calculateProspectValue([
  { probability: 0.3, outcome: 1000, referencePoint: 0 },
  { probability: 0.7, outcome: -500, referencePoint: 0 }
]);

// 四折模式分析
const pattern = pt.fourFoldPattern(0.05, 10000); // 小概率高收益
// 结果: { behavior: 'risk_seeking', explanation: '彩票偏好' }
```

### 有限理性示例

```javascript
const { BoundedRationalityEngine } = require('./behavioral/bounded-rationality');

const br = new BoundedRationalityEngine();

// 满意化决策
const result = br.satisficingDecision(
  alternatives,
  (alt) => evaluate(alt),
  0.8 // 阈值
);

// 双系统决策
const decision = br.dualSystemDecision(
  { complexity: 0.6, familiarity: 0.7 },
  { timePressure: 0.5, cognitiveLoad: 0.4 }
);
// 结果: { system: 1, mechanism: 'heuristic', speed: 'fast' }
```

### 助推理论示例

```javascript
const { NudgeTheoryEngine } = require('./behavioral/nudge-theory');

const nudge = new NudgeTheoryEngine();

// 设计选择架构
const architecture = nudge.designChoiceArchitecture(options, {
  defaultOption: 'option_a',
  orderBy: 'popularity',
  frame: 'gain',
  highlight: ['option_a', 'option_b']
});

// 应用社会规范
const withSocialNorm = nudge.applySocialNorm(options, 0.75, 'increasing');
```

## API参考

### ProspectTheoryEngine

| 方法 | 描述 | 返回值 |
|-----|------|-------|
| `valueFunction(x, rp)` | 计算价值 | number |
| `probabilityWeight(p, isGain)` | 概率加权 | number |
| `calculateProspectValue(prospects)` | 累积前景价值 | number |
| `fourFoldPattern(p, m)` | 四折模式分析 | object |
| `analyzeFramingEffect(opts, frame)` | 框架效应分析 | array |
| `endowmentEffect(value, duration, attachment)` | 禀赋效应 | number |
| `generateDebiasingAdvice(context)` | 生成去偏差建议 | array |
| `generateDebateStrategy(pos, opp, topic)` | 辩论策略 | array |

### BoundedRationalityEngine

| 方法 | 描述 | 返回值 |
|-----|------|-------|
| `satisficingDecision(alts, fn, threshold)` | 满意化决策 | object |
| `availabilityJudgment(event, examples, vivid)` | 可得性判断 | object |
| `representativenessJudgment(target, proto, base)` | 代表性判断 | object |
| `anchoringAdjustment(anchor, target, range)` | 锚定调整 | object |
| `dualSystemDecision(problem, context)` | 双系统决策 | object |
| `attentionAllocation(topics, salience)` | 注意力分配 | object |
| `emotionalInfluence(decision, emotions)` | 情感影响 | object |
| `detectCognitiveBiases(argument)` | 偏差检测 | array |

### NudgeTheoryEngine

| 方法 | 描述 | 返回值 |
|-----|------|-------|
| `designChoiceArchitecture(opts, config)` | 选择架构设计 | object |
| `applyDefaultEffect(opts, defaultId, optOut)` | 默认选项效应 | array |
| `applySocialNorm(opts, rate, trend)` | 社会规范助推 | array |
| `applyFraming(opts, frameType)` | 框架效应 | array |
| `designFeedback(current, target, config)` | 反馈机制 | object |
| `designCommitmentDevice(behavior, level)` | 承诺机制 | object |
| `simplifyChoice(opts, strategy)` | 简化选择 | array/object |
| `generateDebateNudges(position, profile)` | 辩论助推 | array |
| `detectDarkNudges(argument)` | 检测不良助推 | array |

## 版本历史

- **v3.6.1** (2026-04-12): 添加完整文档和README
- **v3.6** (2026-04-12): 初始实现三大行为经济学理论

## 参考资料

1. Kahneman, D., & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. *Econometrica*, 47(2), 263-291.

2. Tversky, A., & Kahneman, D. (1992). Advances in Prospect Theory: Cumulative Representation of Uncertainty. *Journal of Risk and Uncertainty*, 5(4), 297-323.

3. Simon, H. A. (1955). A Behavioral Model of Rational Choice. *The Quarterly Journal of Economics*, 69(1), 99-118.

4. Simon, H. A. (1997). *Administrative Behavior* (4th ed.). Free Press.

5. Jones, B. D. (1999). Bounded Rationality. *Annual Review of Political Science*, 2, 297-321.

6. Thaler, R. H., & Sunstein, C. R. (2008). *Nudge: Improving Decisions About Health, Wealth, and Happiness*. Yale University Press.

7. Thaler, R. H. (2015). *Misbehaving: The Making of Behavioral Economics*. W.W. Norton.

