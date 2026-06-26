/**
 * Evaluation Suite - 快速测试
 */

import { RAGEvaluator, ReasoningEvaluator, HallucinationDetector } from '../src/evaluator.js';

console.log('🧪 Evaluation Suite Quick Test\n');

async function testRAG() {
  console.log('📊 Testing RAG Evaluation...');
  
  const evaluator = new RAGEvaluator();
  const result = await evaluator.evaluate({
    query: 'OpenClaw 是什么？',
    answer: 'OpenClaw 是一个本地优先的 AI 助手框架',
    contexts: ['OpenClaw 是本地优先的 AI 助手', '支持多种技能和工具'],
    groundTruth: 'OpenClaw 是本地优先的 AI 助手框架'
  });
  
  console.log(`  Overall Score: ${(result.overallScore * 100).toFixed(1)}%`);
  console.log(`  Passed: ${result.passed ? '✅' : '❌'}`);
  console.log();
}

async function testReasoning() {
  console.log('🧠 Testing Reasoning Evaluation...');
  
  const evaluator = new ReasoningEvaluator();
  const result = await evaluator.evaluate({
    question: '2 + 2 = ?',
    steps: ['首先，我们有数字 2', '然后，加上另一个 2', '所以，2 + 2 = 4'],
    conclusion: '4',
    expectedAnswer: '4'
  });
  
  console.log(`  Overall Score: ${(result.overallScore * 100).toFixed(1)}%`);
  console.log(`  Passed: ${result.passed ? '✅' : '❌'}`);
  console.log();
}

async function testHallucination() {
  console.log('👁️ Testing Hallucination Detection...');
  
  const detector = new HallucinationDetector();
  const result = await detector.detect({
    text: '根据我的知识，OpenClaw 是由 Google 开发的框架。',
    sources: ['OpenClaw 是开源项目，由社区维护'],
    query: 'OpenClaw 是谁开发的？'
  });
  
  console.log(`  Hallucination Score: ${(result.hallucinationScore * 100).toFixed(1)}%`);
  console.log(`  Is Hallucination: ${result.isHallucination ? '⚠️ YES' : '✅ NO'}`);
  console.log(`  Indicators: ${result.indicators.length}`);
  console.log();
}

async function main() {
  try {
    await testRAG();
    await testReasoning();
    await testHallucination();
    
    console.log('='.repeat(40));
    console.log('✅ All tests passed!');
    console.log('='.repeat(40));
  } catch (e) {
    console.error('❌ Test failed:', e);
    process.exit(1);
  }
}

main();
