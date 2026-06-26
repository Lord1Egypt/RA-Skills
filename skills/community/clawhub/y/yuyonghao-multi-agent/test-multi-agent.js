#!/usr/bin/env node
/**
 * Multi-Agent System - Practical Test
 * Tests real-world scenarios
 */

const { MultiAgentOrchestrator } = require('./src/orchestrator');
const { ToolsRegistry } = require('../react-agent/src/tools-registry');
const { ReActEngine } = require('../react-agent/src/react-engine');

async function runTest(testName, task, mode = 'collaborative') {
  console.log('\n' + '='.repeat(70));
  console.log(`🧪 TEST: ${testName}`);
  console.log('='.repeat(70));
  console.log(`Task: ${task}`);
  console.log(`Mode: ${mode}`);
  console.log('='.repeat(70));

  const startTime = Date.now();

  // Initialize orchestrator
  const orchestrator = new MultiAgentOrchestrator({ verbose: false });
  
  // Initialize agents with tools
  const tools = new ToolsRegistry(process.cwd());
  const reactEngine = new ReActEngine({ verbose: false, maxIterations: 5 });
  
  for (const [name, tool] of tools.tools) {
    reactEngine.registerTool(name, tool.handler, tool.description);
  }
  
  orchestrator.initializeAgents(['planner', 'executor', 'reviewer'], {
    toolsRegistry: tools,
    reactEngine
  });

  // Execute task
  const result = await orchestrator.executeTask(task, {
    mode,
    context: { toolsRegistry: tools, reactEngine }
  });

  const duration = Date.now() - startTime;

  // Output results
  console.log('\n📊 RESULTS:');
  console.log(`  Success: ${result.success ? '✅' : '❌'}`);
  console.log(`  Duration: ${duration}ms`);
  console.log(`  Mode: ${result.mode}`);

  if (result.planning) {
    console.log(`  Planning: ${result.planning.success ? '✅' : '❌'}`);
    if (result.planning.result?.plan) {
      const plan = result.planning.result.plan;
      console.log(`    - Complexity: ${plan.complexity.level} (score: ${plan.complexity.score})`);
      console.log(`    - Subtasks: ${plan.subtasks.length}`);
    }
  }

  if (result.execution && result.execution.length > 0) {
    console.log(`  Execution: ${result.execution.filter(e => e.success).length}/${result.execution.length} successful`);
    result.execution.forEach((exec, i) => {
      console.log(`    ${i + 1}. ${exec.success ? '✅' : '❌'} ${exec.task.substring(0, 40)}...`);
    });
  }

  if (result.review) {
    console.log(`  Review: ${result.review.success ? '✅' : '❌'} (Score: ${Math.round(result.review.overallScore * 100)}%)`);
    console.log(`    - Approved: ${result.review.approved ? '✅' : '❌'}`);
  }

  const stats = orchestrator.getStats();
  console.log(`\n📈 Agent Performance:`);
  stats.agents.forEach(agent => {
    console.log(`  ${agent.role}: ${agent.totalTasks} tasks, ${Math.round(agent.successRate * 100)}% success, ${Math.round(agent.avgDuration)}ms avg`);
  });

  console.log('='.repeat(70));

  return {
    testName,
    success: result.success,
    duration,
    planning: result.planning?.success,
    execution: result.execution?.filter(e => e.success).length || 0,
    totalExecution: result.execution?.length || 0,
    review: result.review?.success,
    reviewScore: result.review?.overallScore || 0
  };
}

async function main() {
  console.log('\n🦞 Multi-Agent System - Practical Test Suite');
  console.log('Testing real-world scenarios...\n');

  const tests = [
    {
      name: 'Project Analysis',
      task: 'Analyze this project structure and list main components',
      mode: 'collaborative'
    },
    {
      name: 'File Operations',
      task: 'Read package.json and extract project name and version',
      mode: 'collaborative'
    },
    {
      name: 'Directory Listing',
      task: 'List all markdown files in current directory',
      mode: 'sequential'
    },
    {
      name: 'Complex Task',
      task: 'Analyze project, count files, and create a summary',
      mode: 'collaborative'
    }
  ];

  const results = [];

  for (const test of tests) {
    try {
      const result = await runTest(test.name, test.task, test.mode);
      results.push(result);
      
      // Wait between tests
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error(`❌ Test failed: ${test.name}`);
      console.error(error.message);
      results.push({
        testName: test.name,
        success: false,
        error: error.message
      });
    }
  }

  // Summary
  console.log('\n\n' + '='.repeat(70));
  console.log('📊 TEST SUMMARY');
  console.log('='.repeat(70));

  const totalTests = results.length;
  const successfulTests = results.filter(r => r.success).length;
  const successRate = (successfulTests / totalTests * 100).toFixed(1);
  const avgDuration = results.reduce((sum, r) => sum + (r.duration || 0), 0) / totalTests;

  console.log(`\nTotal Tests: ${totalTests}`);
  console.log(`Successful: ${successfulTests}/${totalTests} (${successRate}%)`);
  console.log(`Average Duration: ${Math.round(avgDuration)}ms`);

  console.log('\nDetailed Results:');
  results.forEach((result, i) => {
    const icon = result.success ? '✅' : '❌';
    console.log(`  ${i + 1}. ${icon} ${result.testName} (${result.duration}ms)`);
  });

  console.log('\n' + '='.repeat(70));
  console.log(`🏆 Overall: ${successRate >= 75 ? 'EXCELLENT' : successRate >= 50 ? 'GOOD' : 'NEEDS IMPROVEMENT'}`);
  console.log('='.repeat(70) + '\n');

  return results;
}

// Run tests
main().catch(console.error);
