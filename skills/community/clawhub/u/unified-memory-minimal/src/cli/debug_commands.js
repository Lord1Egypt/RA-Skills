/**
 * CLI Debug Commands - Memory Replay Debugger (Feature #8)
 * 
 * Commands:
 *   memory debug --replay <query-id>
 *   memory debug --blame <memory-id>
 *   memory debug --diff <query1> <query2>
 *   memory debug --analyze
 */

import { getAllTraces, getTraceById, getMemoryRetrievalHistory, clearAllTraces, getMemoryIndexStats, searchTraces } from '../retrieval_tracer.js';
import { replayQuery, replayMemory, diffQueries, explainMemoryRetrieval } from '../memory_replay.js';
import { attributeMemoryScore, getAttributionPieChart } from '../memory_attribution.js';
import { analyzeRetrievalPatterns, getRetrievalQualityScore } from '../trace_analyzer.js';

/**
 * Handle debug CLI commands
 * @param {object} args - parsed CLI args
 */
export async function cmdDebug(args) {
  const subcommand = args._ ? args._[0] : null;
  
  if (args.replay) {
    return await cmdReplay(args.replay);
  }
  
  if (args.blame) {
    return await cmdBlame(args.blame);
  }
  
  if (args.diff) {
    const ids = args._ || [];
    if (ids.length < 2) {
      console.log('Usage: memory debug --diff <queryId1> <queryId2>');
      return;
    }
    return await cmdDiff(ids[0], ids[1]);
  }
  
  if (args.analyze) {
    return await cmdAnalyze();
  }
  
  // Default: show usage
  console.log(`
Memory Replay Debugger - Debug retrieval pipeline

Usage:
  memory debug --replay <query-id>   Replay a historical query's retrieval trace
  memory debug --blame <memory-id>   Show all queries that retrieved this memory
  memory debug --diff <q1> <q2>      Compare two query retrieval paths
  memory debug --analyze             Analyze retrieval patterns and quality

Examples:
  memory debug --replay qt-abc123
  memory debug --blame mem_12345
  memory debug --diff qt-abc123 qt-def456
  memory debug --analyze

To find query IDs:
  memory debug --list                List recent traces
  `);
}

/**
 * Replay a historical query
 */
async function cmdReplay(queryId) {
  console.log(`\n🔄 Replaying query: ${queryId}\n`);
  
  const result = await replayQuery(queryId);
  
  if (!result.success) {
    console.log(`❌ ${result.error}`);
    if (result.hint) console.log(`💡 ${result.hint}`);
    return;
  }
  
  console.log(`Query: "${result.query}"`);
  console.log(`Historical: ${result.historical.timestamp} (${result.historical.durationMs}ms)`);
  console.log(`Current:    ${result.current.timestamp} (${result.current.durationMs}ms)`);
  console.log(`\n📊 Pipeline Steps:`);
  
  for (const step of result.historical.pipelineSteps) {
    const icon = step.score ? '✅' : '⚠️';
    console.log(`  ${icon} ${step.stepName}: score=${step.score?.toFixed(3) || 'N/A'}`);
    console.log(`     ${step.reasoning}`);
  }
  
  console.log(`\n📋 Final Ranking:`);
  for (const r of result.historical.finalRanking.slice(0, 5)) {
    console.log(`  #${r.rank} [${r.score?.toFixed(3)}] ${r.text?.slice(0, 60)}...`);
  }
  
  if (result.comparison.rankingChanges.length > 0) {
    console.log(`\n🔄 Comparison with current results:`);
    for (const c of result.comparison.rankingChanges.slice(0, 5)) {
      const change = typeof c.change === 'number' 
        ? (c.change > 0 ? `↑${c.change}` : c.change < 0 ? `↓${Math.abs(c.change)}` : '→')
        : c.change;
      console.log(`  Rank ${c.rank}: ${change}`);
    }
  }
}

/**
 * Show retrieval history for a memory
 */
async function cmdBlame(memoryId) {
  console.log(`\n🔍 Retrieval history for: ${memoryId}\n`);
  
  const result = replayMemory(memoryId);
  
  if (!result.retrieved) {
    console.log(`❌ ${result.message}`);
    return;
  }
  
  console.log(`Total retrievals: ${result.totalRetrievals}`);
  console.log(`Top-rank (1-3): ${result.performance.topRankCount}`);
  console.log(`Mid-rank (4-10): ${result.performance.midRankCount}`);
  console.log(`Low-rank (10+): ${result.performance.lowRankCount}`);
  console.log(`Avg score: ${result.scoreStats.avgScore.toFixed(3)}`);
  
  console.log(`\n📋 Recent retrievals:`);
  for (const h of result.retrievalHistory.slice(0, 10)) {
    const rankIcon = h.rank <= 3 ? '🥇' : h.rank <= 10 ? '📋' : '📉';
    console.log(`  ${rankIcon} [Rank ${h.rank}] "${h.query.slice(0, 40)}..." (score: ${h.score?.toFixed(3)})`);
  }
}

/**
 * Compare two queries
 */
async function cmdDiff(queryId1, queryId2) {
  console.log(`\n⚖️ Comparing queries:\n`);
  
  const result = await diffQueries(queryId1, queryId2);
  
  if (!result.success) {
    console.log(`❌ ${result.error}`);
    return;
  }
  
  console.log(`Query 1: "${result.query1.query}" (${result.query1.durationMs}ms)`);
  console.log(`Query 2: "${result.query2.query}" (${result.query2.durationMs}ms)`);
  
  console.log(`\n📊 Step comparison:`);
  for (const s of result.stepComparison) {
    const diff = s.different ? '❌' : '✅';
    console.log(`  ${diff} Step ${s.index}: ${s.step1?.name || '-'} vs ${s.step2?.name || '-'}`);
  }
  
  console.log(`\n📋 Result comparison:`);
  console.log(`  Shared results: ${result.resultComparison.sharedCount}`);
  console.log(`  Only in query 1: ${result.resultComparison.onlyInQuery1Count}`);
  console.log(`  Only in query 2: ${result.resultComparison.onlyInQuery2Count}`);
}

/**
 * Analyze retrieval patterns
 */
async function cmdAnalyze() {
  console.log(`\n📈 Retrieval Quality Analysis\n`);
  
  const qualityScore = getRetrievalQualityScore();
  const result = analyzeRetrievalPatterns(200);
  
  console.log(`Quality Score: ${qualityScore}/100`);
  
  if (!result.stats) {
    console.log(result.message);
    return;
  }
  
  const { overview, biases, failingPatterns, suggestions } = result.stats;
  
  console.log(`\n📊 Overview:`);
  console.log(`  Total queries: ${overview.totalTraces}`);
  console.log(`  Avg duration: ${overview.avgDurationMs.toFixed(2)}ms`);
  console.log(`  Zero-result rate: ${overview.zeroResultRate}%`);
  console.log(`  Avg results/query: ${overview.avgResultsPerQuery.toFixed(2)}`);
  
  if (biases.length > 0) {
    console.log(`\n⚠️ Detected biases:`);
    for (const b of biases) {
      const icon = b.severity === 'high' ? '🔴' : '🟡';
      console.log(`  ${icon} ${b.description}`);
    }
  }
  
  if (failingPatterns.length > 0) {
    console.log(`\n❌ Failing patterns:`);
    for (const p of failingPatterns) {
      console.log(`  [${p.type}] ${p.description}`);
      console.log(`     Likely cause: ${p.likelyCause}`);
    }
  }
  
  if (suggestions.length > 0) {
    console.log(`\n💡 Tuning suggestions:`);
    for (const s of suggestions) {
      const priority = s.priority === 'high' ? '🔴' : s.priority === 'medium' ? '🟡' : '🟢';
      console.log(`  ${priority} ${s.parameter}: ${s.suggestion}`);
    }
  }
}

/**
 * List recent traces
 */
export function cmdListTraces(limit = 10) {
  console.log(`\n📋 Recent Traces\n`);
  
  const traces = getAllTraces(limit);
  
  if (traces.length === 0) {
    console.log('No traces found. Enable traceRetrieval in config.');
    return;
  }
  
  for (const t of traces) {
    const resultCount = t.finalRanking?.length || 0;
    const icon = resultCount > 0 ? '✅' : '❌';
    console.log(`${icon} ${t.queryId}: "${t.query.slice(0, 50)}..." (${resultCount} results, ${t.durationMs}ms)`);
  }
}
