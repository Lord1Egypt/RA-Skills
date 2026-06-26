#!/usr/bin/env node
/**
 * Multi-Agent System - Main Entry Point
 * Usage: node src/index.js [task] [--mode collaborative|sequential|parallel]
 */

const { MultiAgentOrchestrator } = require('./orchestrator');
const { ToolsRegistry } = require('../../react-agent/src/tools-registry');
const { ReActEngine } = require('../../react-agent/src/react-engine');

async function main() {
  // Parse arguments
  const args = process.argv.slice(2);
  const modeIndex = args.indexOf('--mode');
  const mode = modeIndex > -1 ? args[modeIndex + 1] : 'collaborative';
  const task = args.filter(arg => !arg.startsWith('--')).join(' ') || 'Analyze this project structure';
  
  console.log('🦞 Multi-Agent System v0.1.0');
  console.log('=' .repeat(60));
  console.log(`Task: ${task}`);
  console.log(`Mode: ${mode}`);
  console.log('=' .repeat(60));

  // Initialize orchestrator
  const orchestrator = new MultiAgentOrchestrator({ verbose: true, maxRetries: 2 });
  
  // Initialize agents
  const tools = new ToolsRegistry(process.cwd());
  const reactEngine = new ReActEngine({ verbose: false, maxIterations: 5 });
  
  // Register tools with executor
  for (const [name, tool] of tools.tools) {
    reactEngine.registerTool(name, tool.handler, tool.description);
  }
  
  orchestrator.initializeAgents(['planner', 'executor', 'reviewer'], {
    toolsRegistry: tools,
    reactEngine
  });

  console.log(`\n📦 Initialized ${orchestrator.agents.length} agents:`);
  orchestrator.agents.forEach(agent => {
    console.log(`   - ${agent.role.name}: ${agent.role.description.substring(0, 60)}...`);
  });

  console.log('\n🚀 Starting multi-agent execution...\n');

  // Execute task
  const result = await orchestrator.executeTask(task, {
    mode,
    context: {
      toolsRegistry: tools,
      reactEngine
    }
  });

  // Output results
  console.log('\n' + '=' .repeat(60));
  console.log('📊 RESULTS');
  console.log('=' .repeat(60));
  console.log(`Success: ${result.success ? '✅' : '❌'}`);
  console.log(`Mode: ${result.mode}`);
  console.log(`Duration: ${result.duration}ms`);
  
  if (result.planning) {
    console.log('\n📋 Planning Phase:');
    console.log(`  Status: ${result.planning.success ? '✅' : '❌'}`);
    if (result.planning.result?.plan) {
      const plan = result.planning.result.plan;
      console.log(`  Complexity: ${plan.complexity.level} (${plan.complexity.score})`);
      console.log(`  Subtasks: ${plan.subtasks.length}`);
    }
  }
  
  if (result.execution && result.execution.length > 0) {
    console.log('\n🛠️  Execution Phase:');
    result.execution.forEach((exec, i) => {
      console.log(`  ${i + 1}. ${exec.task.substring(0, 50)}...`);
      console.log(`     Status: ${exec.success ? '✅' : '❌'}`);
    });
  }
  
  if (result.review) {
    console.log('\n🔍 Review Phase:');
    console.log(`  Status: ${result.review.success ? '✅' : '❌'}`);
    console.log(`  Score: ${Math.round(result.review.overallScore * 100)}%`);
    console.log(`  Approved: ${result.review.approved ? '✅' : '❌'}`);
    
    if (result.review.result?.review?.checks) {
      console.log('  Checks:');
      result.review.result.review.checks.forEach(check => {
        console.log(`    - ${check.name}: ${check.passed ? '✅' : '❌'}`);
      });
    }
  }

  // Show statistics
  const stats = orchestrator.getStats();
  console.log('\n📈 Statistics:');
  console.log(`  Total agents: ${stats.totalAgents}`);
  console.log(`  Tasks completed: ${stats.completedTasks}/${stats.totalTasks}`);
  console.log(`  Success rate: ${Math.round(stats.successRate * 100)}%`);
  
  console.log('\n🤖 Agent Stats:');
  stats.agents.forEach(agent => {
    console.log(`  ${agent.role}: ${agent.totalTasks} tasks, ${Math.round(agent.successRate * 100)}% success`);
  });

  return result;
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { main, MultiAgentOrchestrator };
