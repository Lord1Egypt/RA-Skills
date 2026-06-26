#!/usr/bin/env node
/**
 * Multi-Agent System - Real World Complex Test
 * Tests with actual tool execution and ReAct integration
 */

const { MultiAgentOrchestrator } = require('../src/orchestrator');
const { ToolsRegistry } = require('../../react-agent/src/tools-registry');
const { ReActEngine } = require('../../react-agent/src/react-engine');

async function runComplexTest() {
  console.log('\n🦞 Multi-Agent Complex Real-World Test');
  console.log('='.repeat(70));
  
  // Initialize with full tool support
  const orchestrator = new MultiAgentOrchestrator({ verbose: true, maxRetries: 2 });
  const tools = new ToolsRegistry(process.cwd());
  const reactEngine = new ReActEngine({ verbose: false, maxIterations: 5 });
  
  // Register all tools
  for (const [name, tool] of tools.tools) {
    reactEngine.registerTool(name, tool.handler, tool.description);
  }
  
  orchestrator.initializeAgents(['planner', 'executor', 'reviewer'], {
    toolsRegistry: tools,
    reactEngine
  });

  // Complex task: Multi-step project analysis
  const task = 'Analyze the project: 1) List directory contents, 2) Read package.json, 3) Count total files, 4) Create a summary report';
  
  console.log(`\n📝 Task: ${task}`);
  console.log('='.repeat(70));

  const startTime = Date.now();
  
  // Execute with collaborative mode
  const result = await orchestrator.executeTask(task, {
    mode: 'collaborative',
    context: {
      toolsRegistry: tools,
      reactEngine,
      qualityCriteria: ['success', 'complete', 'fast']
    }
  });

  const duration = Date.now() - startTime;

  // Detailed output
  console.log('\n' + '='.repeat(70));
  console.log('📊 DETAILED RESULTS');
  console.log('='.repeat(70));
  
  console.log(`\n✅ Overall Success: ${result.success}`);
  console.log(`⏱️  Total Duration: ${duration}ms`);
  console.log(`🎯 Mode: ${result.mode}`);

  // Planning phase
  if (result.planning) {
    console.log('\n📋 PLANNING PHASE:');
    console.log(`  Status: ${result.planning.success ? '✅ Success' : '❌ Failed'}`);
    
    if (result.planning.result?.plan) {
      const plan = result.planning.result.plan;
      console.log(`  Complexity: ${plan.complexity.level} (Score: ${plan.complexity.score})`);
      console.log(`  Estimated Duration: ${plan.estimatedDuration}ms`);
      console.log(`  Subtasks: ${plan.subtasks.length}`);
      
      plan.subtasks.forEach((subtask, i) => {
        console.log(`    ${i + 1}. [${subtask.role}] ${subtask.description.substring(0, 60)}...`);
      });
    }
  }

  // Execution phase
  if (result.execution && result.execution.length > 0) {
    console.log('\n🛠️  EXECUTION PHASE:');
    const successCount = result.execution.filter(e => e.success).length;
    console.log(`  Success Rate: ${successCount}/${result.execution.length} (${Math.round(successCount/result.execution.length*100)}%)`);
    
    result.execution.forEach((exec, i) => {
      console.log(`\n  Task ${i + 1}:`);
      console.log(`    Description: ${exec.task.substring(0, 60)}...`);
      console.log(`    Status: ${exec.success ? '✅' : '❌'}`);
      if (exec.result) {
        const resultPreview = JSON.stringify(exec.result).substring(0, 100);
        console.log(`    Result Preview: ${resultPreview}...`);
      }
      if (exec.error) {
        console.log(`    Error: ${exec.error}`);
      }
    });
  }

  // Review phase
  if (result.review) {
    console.log('\n🔍 REVIEW PHASE:');
    console.log(`  Status: ${result.review.success ? '✅' : '❌'}`);
    
    // Fix: Handle both number and object review results
    const reviewScore = typeof result.review.overallScore === 'number' 
      ? result.review.overallScore 
      : (result.review.result?.review?.overallScore || 0);
    
    console.log(`  Overall Score: ${Math.round((reviewScore || 0) * 100)}%`);
    console.log(`  Approved: ${result.review.approved ? '✅ Yes' : '❌ No'}`);
    
    if (result.review.result?.review?.checks) {
      console.log('  Quality Checks:');
      result.review.result.review.checks.forEach(check => {
        console.log(`    - ${check.name}: ${check.passed ? '✅' : '❌'} ${check.details || ''}`);
      });
    }
    
    if (result.review.result?.review?.recommendations) {
      console.log('  Recommendations:');
      result.review.result.review.recommendations.forEach(rec => {
        console.log(`    - ${rec}`);
      });
    }
  }

  // Statistics
  const stats = orchestrator.getStats();
  console.log('\n📈 PERFORMANCE STATISTICS:');
  console.log(`  Total Agents: ${stats.totalAgents}`);
  console.log(`  Tasks Completed: ${stats.completedTasks}/${stats.totalTasks}`);
  console.log(`  Success Rate: ${Math.round(stats.successRate * 100)}%`);
  
  console.log('\n🤖 Individual Agent Performance:');
  stats.agents.forEach(agent => {
    console.log(`  ${agent.role}:`);
    console.log(`    - Tasks: ${agent.totalTasks}`);
    console.log(`    - Success Rate: ${Math.round(agent.successRate * 100)}%`);
    console.log(`    - Avg Duration: ${Math.round(agent.avgDuration)}ms`);
  });

  console.log('\n' + '='.repeat(70));
  console.log('🏆 TEST COMPLETE');
  console.log('='.repeat(70) + '\n');

  return {
    success: result.success,
    duration,
    planning: result.planning,
    execution: result.execution,
    review: result.review,
    stats
  };
}

// Run the test
runComplexTest()
  .then(result => {
    console.log('Test completed successfully!');
    process.exit(0);
  })
  .catch(error => {
    console.error('Test failed:', error);
    process.exit(1);
  });
