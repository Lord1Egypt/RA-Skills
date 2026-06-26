# Changelog - Virtual Forum

All notable changes to the Virtual Forum skill will be documented in this file.

## [5.0.3] - 2026-04-18

### Note
- ClawHub发布问题修复（重试发布）

## [5.0.2] - 2026-04-18

### Breaking Change
- **移除**: v3/ 和 v4/ 目录（已废弃代码已删除）

### Reorganized
- **移动**: 博弈论模块移至 `v5/game-theory/`
  - advanced-game-theory.js
  - game-theory-v2.js
  - game-theory-arena.js
  - behavioral-arena.js
  - advanced/, core/, behavioral/, extensions/ 子目录
- **新增**: `v5/game-theory/README.md` 博弈论模块文档

### Updated
- README.md 目录结构已更新
- SKILL.md 描述已更新

## [5.0.1] - 2026-04-18

### Fixed
- **P0**: `v3/game-theory-v2.js` 第574行模板字符串语法错误
  - 修复：`${(x).toFixed(0)%}` → `${((x).toFixed(0))}%`
- **Shell脚本加固**:
  - 添加 `trap` 处理异常退出（临时文件清理）
  - 添加超时控制（每轮5分钟）
  - 添加API重试机制（最多3次）
  - 改进进程等待逻辑

### Improved
- 错误处理更健壮
- 临时文件管理更安全

## [5.0.0] - 2026-04-18

### Breaking Change
- **废弃**: v3.x 顺序调用方案
- **废弃**: v4.0 sessions_spawn 子代理方案

### Added
- **v5.0 Claude Code并行方案** (v5/debate_parallel.sh)
  - 使用 bash + `claude --print` 调用外部Claude Code CLI
  - 5个进程真正并行运行
  - 完全绕过OpenClaw sessions限制

### Architecture Comparison

| 版本 | 协调方式 | 状态 | 推荐 |
|------|---------|------|------|
| **v3.x** | 顺序调用 | 废弃 | ❌ |
| **v4.0** | sessions_spawn | 废弃 | ❌ |
| **v5.0** | Claude Code并行 | ✅ 推荐 | ✅ |

### Technical Details

**v5.0 工作原理**:
```bash
# 并行启动5个参与者
(echo "$USER_MSG" | claude --print --system-prompt "$TRUMP_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$NETANYAHU_PROMPT") &
# ... 5个并行进程
wait
```

### Why v5.0 Works
- Claude Code CLI 是独立进程，不受OpenClaw sessions限制
- 每个进程独立调用MiniMax API
- 无需管理session状态
- 无上下文膨胀问题

### Limitations
- 需要安装 Claude Code CLI
- 每个进程消耗独立API配额

### Verified
- ✅ 10轮辩论成功完成
- ✅ 60次Claude Code调用
- ✅ 294KB输出文件

## [3.9.2] - 2026-04-18

### Fixed
- **P0**: `_grimTriggerDecision()` 逻辑错误 - 检查对手是否背叛，而非自己
- **P2**: `_checkIncentivesToDefect()` 未使用参数 `totalCoalitionShapley`
- **P2**: `generateBargainingReport()` 硬编码 P1/P2 → 支持通用玩家名

## [3.9.1] - 2026-04-18

### Fixed
- **P0**: 除零错误 - `calculateEquilibrium()` 当 δ₁=1 且 δ₂=1 时
- **P0**: 除零错误 - `calculateEquilibriumShares()` 同样问题
- **P0**: 语法错误 - `generateOffer建议()` 函数名包含中文字符
- **P0**: 溢出风险 - `_factorial(25)` 超过 `Number.MAX_SAFE_INTEGER`
- **P1**: 议价逻辑 - `evaluateOffer()` 的 `futureValueIfReject` 公式错误
- **Low**: Emoji乱码 - `� coalition` → `🛡 联盟博弈`

### Documentation
- Added `CODE_REVIEW_v3.9.md` - 详细的问题报告和修复说明

## [3.9.0] - 2026-04-18

### Added
- **议价博弈 (BargainingGame)** [P1]
  - Rubinstein (1982) 轮流议价均衡
  - `calculateEquilibrium()`: 计算均衡份额
  - `generateOffer()`: 生成出价建议
  - `evaluateOffer()`: 评估是否接受出价
  - `getBargainingPhase()`: 议价阶段分析

- **联盟博弈 (CoalitionGame)** [P1]
  - Shapley (1953) 联盟价值分配
  - `calculateShapleyValues()`: Shapley值计算
  - `calculateAllCoalitions()`: 所有联盟及价值
  - `checkCoreStability()`: 核心稳定性检测
  - `predictOptimalCoalition()`: 最优联盟预测

### Documentation
- Updated SKILL.md with v3.9 section
- Added BargainingGame theory and examples
- Added CoalitionGame theory and examples
- Comparison table: v3.8 vs v3.9

### Technical Details

**Rubinstein均衡**:
```
p1_share = (1 - δ₂) / (1 - δ₁δ₂)
```

**Shapley公式**:
```
φ_i(v) = Σ_{S⊆N\{i}} [|S|!(n-|S|-1)!/n!] × [v(S∪{i}) - v(S)]
```

## [3.8.0] - 2026-04-18

### Added
- **AdvancedGameTheoryArena** (v3/advanced-game-theory.js): 高级博弈论模块

#### 1. 信号博弈 (SignalingGame)
  - 分离均衡/混同均衡检测
  - 贝叶斯可信度评估 P(H|E) = P(E|H)P(H)/P(E)
  - 信号成本分析 (strong_claim, evidence_backed, weak_claim, assertion)
  - 似然比计算
  - 互信息计算

#### 2. 重复博弈 (RepeatedGameEngine)
  - Folk Theorem实现
  - 四种策略: Grim Trigger, Tit-for-Tat, Generous TFT, Suspicious TFT
  - 合作率追踪
  - 阶段分析 (COOPERATION, TRANSITION, CONFLICT)
  - 惩罚/原谅机制

#### 3. 信息设计 (InformationDesigner)
  - Kamenica & Mandler 2012贝叶斯说服理论
  - 三种披露模式: FULL, STRATEGIC, CONDITIONAL
  - 问题诊断: OVERCONFIDENT_DOMINANT, BELIEF_DIVERGENCE, INFORMATION_ASYMMETRY
  - 最优信号设计

### Documentation
- Updated SKILL.md with v3.8 section
- Complete theory explanations with formulas
- Comparison table: v3.7 vs v3.8
- Usage recommendations

### Technical Details

**信号博弈 - 分离均衡条件**:
```
P(真|信号) > P(真) 且 信号成本 > 阈值
```

**重复博弈 - Folk Theorem**:
```
背叛条件: T < R / (1-δ)
其中 T=背叛诱惑, R=合作奖励, δ=贴现因子
```

**信息设计 - 策略选择**:
```
IF 过度自信 > 50%: STRATEGIC披露
ELIF 信念分歧 > 0.3: 聚焦共同知识
ELIF 信息不对称: CONDITIONAL披露
ELSE: FULL披露
```

## [3.7.0] - 2026-04-18

### Added
- **GameTheoryArena** (v3/game-theory-v2.js): True game theory implementation
  - `GameStructure` class: Explicit payoff matrix and Nash equilibrium calculation
  - `BayesianBeliefSystem` class: Real Bayesian updates (not hardcoded multipliers)
  - `GameStateTracker` class: Game state tracking
  - 2x2 game analytical solution (Myerson 1991)
  - Fictitious Play approximation for N-player games
  - Nash equilibrium calculation with confidence score

### Added
- **GameTheoryArena** (v3/game-theory-v2.js): True game theory implementation
  - `GameStructure` class: Explicit payoff matrix and Nash equilibrium calculation
  - `BayesianBeliefSystem` class: Real Bayesian updates (not hardcoded multipliers)
  - `GameStateTracker` class: Game state tracking
  - 2x2 game analytical solution (Myerson 1991)
  - Fictitious Play approximation for N-player games
  - Nash equilibrium calculation with confidence score

### Enhanced
- **博弈论实现**: No longer "game theory themed decoration"
  - True Nash equilibrium computation
  - Explicit payoff matrix structure
  - Dominant strategy checking
  - Bayesian belief updates with proper formulas

### Documentation
- Added v3.7 section to SKILL.md
- Complete theory explanation with formulas
- Comparison table: v3.5 vs v3.7
- Code examples for new API

### Technical Details

**Nash Equilibrium (2x2 game)**:
```
p = (d - c) / (a + d - b - c)
where:
  a = A强硬B强硬收益
  b = A强硬B让步收益
  c = A让步B强硬收益
  d = A让步B让步收益
```

**Bayesian Update Formula**:
```
P(H|E) = P(E|H) × P(H) / P(E)
```

## [3.6.4] - 2026-04-17

### Fixed
- behavioral-arena.js: Added missing `strategyAdvice` initialization
- behavioral-arena.js: Added `analyzeRound()` and `generateReport()` stub methods
- behavioral-arena.js: Safe access in `generateBehavioralAdviceForAll()`

### Enhanced
- API timeout protection (30s default)
- Token compression with MAX_CONTEXT_CHARS = 16000
- Graceful shutdown with SIGINT/SIGTERM handling

## [3.6.3] - 2026-04-17

### Fixed
- shared-config.js: `maxRounds = 100` to prevent resource exhaustion
- shared-config.js: `apiBaseDelay` increased from 2000ms to 5000ms
- shared-config.js: `validateConfig` now checks rounds upper bound
- shared-config.js: `loadSkill` path traversal protection

### Enhanced
- Error handling: Throws when all Skills fail to load
- Partial load warnings when some Skills fail

## [3.6.2] - 2026-04-17

### Fixed
- context-manager.js: Added MAX_CONTEXT_CHARS = 16000 token limit
- context-manager.js: Force compression when context exceeds limit
- subagent-arena.js: Added `generateSummary()` fallback implementation

## [3.6.1] - 2026-04-12

### Added
- Behavioral Economics Enhanced mode
  - Prospect Theory engine (Kahneman & Tversky, 1979)
  - Bounded Rationality engine (Simon & Jones, 1999)
  - Nudge Theory engine (Thaler & Sunstein, 2008)

### Features
- `launchBehavioralEconomicsArena()` method
- Behavioral bias detection
- Strategy advice with behavioral considerations

## [3.5.0] - 2026-04

### Added
- Game Theory Enhanced mode
  - Discount factors and BATNA (outside options)
  - Bayesian belief updates based on observed actions

## [3.0.0] - 2026-03

### Added
- Subagent Arena mode
- Context Manager for token optimization
- Argument Tracker

## [1.0.0] - 2026-02

### Added
- Initial release
- Basic forum simulation
- Three discussion modes (exploratory, adversarial, decision)

---

*Generated by AI Assistant - 2026-04-18*