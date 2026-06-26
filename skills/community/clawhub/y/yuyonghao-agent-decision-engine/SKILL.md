# Agent Decision Engine

Autonomous decision engine for AI agents with multi-objective optimization, risk assessment, decision trees, and reinforcement learning capabilities.

## Features

- **Multi-Objective Optimization**: Pareto optimization with configurable weights and constraints
- **Risk Assessment**: Probability evaluation, impact analysis, and risk matrices
- **Decision Trees**: Build, evaluate, prune, and visualize decision paths
- **Reinforcement Learning**: Q-Learning with customizable reward functions

## Usage

```javascript
import { DecisionEngine } from './src/index.js';

const engine = new DecisionEngine();

// Multi-objective optimization
const result = engine.optimize([
  { name: 'cost', value: 100, weight: 0.4, minimize: true },
  { name: 'quality', value: 85, weight: 0.6, minimize: false }
]);

// Risk assessment
const risk = engine.assessRisk({
  probability: 0.3,
  impact: 0.8,
  mitigation: ['backup plan', 'monitoring']
});

// Decision tree
const tree = engine.buildDecisionTree({
  options: ['A', 'B', 'C'],
  outcomes: [0.7, 0.5, 0.9]
});

// Q-Learning
const action = engine.qLearn({
  state: [1, 0, 1],
  actions: ['move', 'stay', 'attack'],
  reward: 10
});
```

## API

### DecisionEngine

Main class combining all decision-making capabilities.

#### optimize(objectives, constraints)
Multi-objective optimization with Pareto front.

#### assessRisk(riskConfig)
Evaluate and score risks.

#### buildDecisionTree(config)
Build and evaluate decision trees.

#### qLearn(config)
Q-Learning for sequential decision making.

## License

MIT
