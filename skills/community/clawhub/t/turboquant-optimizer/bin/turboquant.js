#!/usr/bin/env node
/**
 * TurboQuant Optimizer CLI
 * 
 * Command-line interface for the TurboQuant Optimizer skill
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { TurboQuantOptimizer } = require('../lib/turboquant-optimizer');
const { TokenBudgetManager } = require('../lib/token-budget-manager');

const COMMAND = process.argv[2];
const ARGS = process.argv.slice(3);

const HELP_TEXT = `
🚀 TurboQuant Optimizer CLI

Usage: turboquant <command> [options]

Commands:
  analyze <session-file>     Analyze a session for optimization potential
  optimize <session-file>    Optimize a specific session
  stats                      Show optimization statistics
  budget                     Show token budget allocation
  benchmark                  Run performance benchmarks
  visualize                  Show token budget visualization
  help                       Show this help message

Options:
  --session <id>             Specify session ID
  --format <json|markdown>   Output format (default: markdown)
  --max-tokens <number>      Set max token limit (default: 8000)
  --threshold <0-1>          Set compression threshold (default: 0.7)

Examples:
  turboquant analyze
  turboquant optimize --session abc123
  turboquant stats --format json
`;

async function main() {
  switch (COMMAND) {
    case 'analyze':
      await analyzeCommand();
      break;
    case 'optimize':
      await optimizeCommand();
      break;
    case 'stats':
      await statsCommand();
      break;
    case 'budget':
      await budgetCommand();
      break;
    case 'benchmark':
      await benchmarkCommand();
      break;
    case 'visualize':
      await visualizeCommand();
      break;
    case 'help':
    default:
      console.log(HELP_TEXT);
      process.exit(COMMAND === 'help' ? 0 : 1);
  }
}

async function analyzeCommand() {
  const sessionFile = ARGS[0];
  const format = getArg('--format') || 'markdown';
  
  console.log('🔍 Analyzing optimization potential...\n');
  
  let messages;
  
  if (sessionFile) {
    messages = loadSession(sessionFile);
  } else {
    // Analyze current session
    const sessionsDir = path.join(os.homedir(), '.openclaw/agents/main/sessions');
    const latestSession = getLatestSession(sessionsDir);
    if (!latestSession) {
      console.error('❌ No sessions found');
      process.exit(1);
    }
    messages = loadSession(latestSession);
  }
  
  const optimizer = new TurboQuantOptimizer();
  const originalTokens = optimizer.estimateTokens(messages);
  
  // Run optimization
  const result = await optimizer.optimize(messages);
  
  if (format === 'json') {
    console.log(JSON.stringify(result.metadata, null, 2));
  } else {
    console.log('📊 Analysis Results');
    console.log('='.repeat(50));
    console.log(`Messages: ${messages.length}`);
    console.log(`Original tokens: ${result.metadata.originalTokens.toLocaleString()}`);
    console.log(`Optimized tokens: ${result.metadata.finalTokens.toLocaleString()}`);
    console.log(`Tokens saved: ${result.metadata.tokensSaved.toLocaleString()}`);
    console.log(`Savings: ${result.metadata.savingsPercent}%`);
    console.log(`Compression ratio: ${result.metadata.compressionRatio.toFixed(3)}`);
    console.log(`Duration: ${result.metadata.duration}ms`);
    
    if (result.metadata.stages.length > 0) {
      console.log('\n📋 Optimization Stages:');
      result.metadata.stages.forEach((stage, i) => {
        console.log(`  ${i + 1}. ${stage.name}`);
        if (stage.tokensSaved) {
          console.log(`     Saved: ${stage.tokensSaved} tokens`);
        }
      });
    }
  }
}

async function optimizeCommand() {
  const sessionId = getArg('--session');
  const maxTokens = parseInt(getArg('--max-tokens')) || 8000;
  
  console.log('⚡ Optimizing session...\n');
  
  const sessionsDir = path.join(os.homedir(), '.openclaw/agents/main/sessions');
  let sessionFile;
  
  if (sessionId) {
    sessionFile = path.join(sessionsDir, `${sessionId}.jsonl`);
  } else {
    sessionFile = getLatestSession(sessionsDir);
  }
  
  if (!sessionFile || !fs.existsSync(sessionFile)) {
    console.error('❌ Session not found');
    process.exit(1);
  }
  
  const messages = loadSession(sessionFile);
  
  const optimizer = new TurboQuantOptimizer({ maxTokens });
  const result = await optimizer.optimize(messages);
  
  console.log('✅ Optimization complete!');
  console.log(`Saved ${result.metadata.tokensSaved.toLocaleString()} tokens (${result.metadata.savingsPercent}%)`);
}

async function statsCommand() {
  const format = getArg('--format') || 'markdown';
  
  console.log('📈 TurboQuant Optimizer Statistics\n');
  
  const optimizer = new TurboQuantOptimizer();
  const stats = optimizer.getDetailedStats();
  
  if (format === 'json') {
    console.log(JSON.stringify(stats, null, 2));
  } else {
    console.log('Overall Performance:');
    console.log(`  Total optimizations: ${stats.totalOptimizations}`);
    console.log(`  Total tokens saved: ${stats.totalTokensSaved.toLocaleString()}`);
    console.log(`  Compression ratio: ${(stats.compressionRatio * 100).toFixed(2)}%`);
    console.log(`  Efficiency score: ${stats.efficiencyScore}/100`);
    console.log(`  Cache hits: ${stats.cacheHits}`);
    console.log(`  Deduplication hits: ${stats.deduplicationHits}`);
    console.log(`  Checkpoints: ${stats.checkpointCount}`);
    console.log(`  Avg response time: ${stats.avgResponseTime.toFixed(2)}ms`);
  }
}

async function budgetCommand() {
  console.log('💰 Token Budget Allocation\n');
  
  const manager = new TokenBudgetManager();
  const stats = manager.getStats();
  
  console.log(JSON.stringify(stats, null, 2));
}

async function benchmarkCommand() {
  console.log('🏃 Running benchmarks...\n');
  
  const optimizer = new TurboQuantOptimizer();
  
  // Generate test data
  const testSizes = [10, 50, 100, 200];
  const results = [];
  
  for (const size of testSizes) {
    const messages = generateTestMessages(size);
    const start = Date.now();
    const result = await optimizer.optimize(messages);
    const duration = Date.now() - start;
    
    results.push({
      size,
      originalTokens: result.metadata.originalTokens,
      finalTokens: result.metadata.finalTokens,
      savings: result.metadata.savingsPercent,
      duration
    });
  }
  
  console.log('Benchmark Results:');
  console.log('Size | Original | Final | Savings | Time');
  console.log('-'.repeat(60));
  results.forEach(r => {
    console.log(`${r.size.toString().padStart(4)} | ${r.originalTokens.toString().padStart(8)} | ${r.finalTokens.toString().padStart(5)} | ${r.savings.padStart(6)}% | ${r.duration}ms`);
  });
}

async function visualizeCommand() {
  console.log('📊 Token Budget Visualization\n');
  
  const optimizer = new TurboQuantOptimizer();
  const sessionsDir = path.join(os.homedir(), '.openclaw/agents/main/sessions');
  const latestSession = getLatestSession(sessionsDir);
  
  if (!latestSession) {
    console.log('No sessions found');
    return;
  }
  
  const messages = loadSession(latestSession);
  const tokens = optimizer.estimateTokens(messages);
  const maxTokens = 8000;
  const usedPercent = Math.min(100, (tokens / maxTokens) * 100);
  const barWidth = 40;
  const filled = Math.floor((usedPercent / 100) * barWidth);
  const empty = barWidth - filled;
  const bar = '█'.repeat(Math.max(0, filled)) + '░'.repeat(Math.max(0, empty));
  
  console.log(`Session: ${path.basename(latestSession)}`);
  console.log(`┌${'─'.repeat(42)}┐`);
  console.log(`│ Context Budget: ${maxTokens.toLocaleString().padStart(5)} tokens     │`);
  console.log(`│ Used: ${tokens.toLocaleString().padStart(5)} tokens (${usedPercent.toFixed(1).padStart(5)}%)     │`);
  console.log(`│ ${bar} │`);
  console.log(`│                                         │`);
  console.log(`│ Remaining: ${(maxTokens - tokens).toLocaleString().padStart(5)} tokens              │`);
  console.log(`└${'─'.repeat(42)}┘`);
}

// Helper functions
function getArg(flag) {
  const index = ARGS.indexOf(flag);
  return index !== -1 && ARGS[index + 1] ? ARGS[index + 1] : null;
}

function getLatestSession(sessionsDir) {
  if (!fs.existsSync(sessionsDir)) return null;
  
  const files = fs.readdirSync(sessionsDir)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => ({
      name: f,
      path: path.join(sessionsDir, f),
      mtime: fs.statSync(path.join(sessionsDir, f)).mtime
    }))
    .sort((a, b) => b.mtime - a.mtime);
  
  return files.length > 0 ? files[0].path : null;
}

function loadSession(sessionPath) {
  const content = fs.readFileSync(sessionPath, 'utf8');
  const lines = content.trim().split('\n');
  
  return lines
    .map(line => {
      try {
        const entry = JSON.parse(line);
        if (entry.type === 'message' && entry.message?.role) {
          return entry.message;
        }
      } catch (e) {}
      return null;
    })
    .filter(Boolean);
}

function generateTestMessages(count) {
  return Array(count).fill(null).map((_, i) => ({
    role: i % 2 === 0 ? 'user' : 'assistant',
    content: `This is test message ${i} with enough text content to make it realistic for token estimation purposes. It contains multiple sentences to simulate real conversation content.`
  }));
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
