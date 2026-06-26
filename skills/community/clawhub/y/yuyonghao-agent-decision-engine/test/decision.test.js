/**
 * Agent Decision Engine Test Suite
 */

import DecisionTree from '../src/decision-tree.js';
import RiskAssessor from '../src/risk-assessor.js';
import MultiObjectiveOptimizer from '../src/multi-objective.js';
import ReinforcementLearner from '../src/reinforcement-learner.js';

class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('\n🧪 Running Decision Engine Tests\n');
    console.log('=' .repeat(50));
    
    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✅ PASS: ${name}`);
        this.passed++;
      } catch (error) {
        console.log(`❌ FAIL: ${name}`);
        console.log(`   Error: ${error.message}`);
        this.failed++;
      }
    }
    
    console.log('=' .repeat(50));
    console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
    console.log(`Success Rate: ${((this.passed / this.tests.length) * 100).toFixed(1)}%\n`);
    
    return this.failed === 0;
  }

  assert(condition, message) {
    if (!condition) throw new Error(message || 'Assertion failed');
  }
}

const runner = new TestRunner();

// Test 1: DecisionTree Creation
runner.test('DecisionTree should be created', () => {
  const tree = new DecisionTree({ root: 'start' });
  runner.assert(tree, 'Tree should be created');
});

// Test 2: RiskAssessor Creation
runner.test('RiskAssessor should be created', () => {
  const assessor = new RiskAssessor();
  runner.assert(assessor, 'Assessor should be created');
});

// Test 3: MultiObjective Creation
runner.test('MultiObjective should be created', () => {
  const mo = new MultiObjectiveOptimizer({ objectives: ['speed', 'quality'] });
  runner.assert(mo, 'MO should be created');
});

// Test 4: ReinforcementLearner Creation
runner.test('ReinforcementLearner should be created', () => {
  const learner = new ReinforcementLearner({ states: 5, actions: 3 });
  runner.assert(learner, 'Learner should be created');
});

// Test 5: Decision Tree Build
runner.test('DecisionTree should build tree', () => {
  const tree = new DecisionTree();
  tree.build({
    condition: 'x > 5',
    trueBranch: { action: 'A' },
    falseBranch: { action: 'B' }
  });
  runner.assert(tree.root, 'Should have root');
});

// Test 6: Risk Assessment
runner.test('RiskAssessor should assess risk', () => {
  const assessor = new RiskAssessor();
  const risk = assessor.assessRisk({ id: 'r1', probability: 0.3, impact: 0.8 });
  runner.assert(typeof risk === 'object', 'Should return risk object');
});

// Test 7: Calculate Risk Score
runner.test('RiskAssessor should calculate risk score', () => {
  const assessor = new RiskAssessor();
  const score = assessor.calculateRiskScore(0.5, 0.6);
  runner.assert(typeof score === 'number', 'Should return score');
});

// Test 8: RL Learn
runner.test('ReinforcementLearner should learn', () => {
  const learner = new ReinforcementLearner({ states: 3, actions: 2 });
  learner.learn(0, 1, 1, 1);
  runner.assert(learner.qTable, 'Should have Q-table');
});

// Test 9: Decision Tree Evaluate
runner.test('DecisionTree should evaluate', () => {
  const tree = new DecisionTree();
  tree.build({ condition: 'x > 5', trueBranch: { action: 'A' }, falseBranch: { action: 'B' } });
  const result = tree.evaluate({ x: 10 });
  runner.assert(result, 'Should return result');
});

// Test 10: Risk Matrix
runner.test('RiskAssessor should generate risk matrix', () => {
  const assessor = new RiskAssessor();
  const matrix = assessor.buildRiskMatrix();
  runner.assert(typeof matrix === 'object', 'Should return matrix');
});

// Test 11: Get Risk Rating
runner.test('RiskAssessor should get risk rating', () => {
  const assessor = new RiskAssessor();
  const rating = assessor.getRiskRating(0.5);
  runner.assert(rating, 'Should return rating');
});

// Test 12: RL Select Action
runner.test('ReinforcementLearner should select action', () => {
  const learner = new ReinforcementLearner({ states: 2, actions: 2 });
  const action = learner.selectAction(0);
  runner.assert(typeof action === 'number', 'Should return action');
});

// Run tests
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
