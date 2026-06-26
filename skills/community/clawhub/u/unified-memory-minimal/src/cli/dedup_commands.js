/**
 * dedup_commands.js - CLI commands for semantic deduplication
 *
 * Commands:
 *   memory dedup --scan        → Full semantic scan of all memories
 *   memory dedup --auto        → Auto-merge mode (absorb >0.95, merge 0.85-0.95)
 *   memory dedup --report      → Show dedup log history
 *   memory dedup --dry-run      → Scan without applying changes
 *   memory dedup --threshold 0.9 → Set custom similarity threshold
 */

import { findAllDuplicatePairs, loadDedupLog } from '../semantic_dedup.js';
import { applyDedup } from '../dedup_merger.js';
import { getAllMemories, getMemory } from '../storage.js';

async function cmdDedupScan(args) {
  const threshold = args.threshold ?? args.t ?? 0.85;
  const dryRun = args.dryRun ?? false;
  const auto = args.auto ?? false;

  console.log(`\n🔍 Semantic Dedup Scan`);
  console.log(`   Threshold: ${threshold}`);
  console.log(`   Mode: ${auto ? 'auto-merge' : dryRun ? 'dry-run' : 'scan-only'}\n`);

  const result = await findAllDuplicatePairs({ threshold, maxPairs: 100 });

  if (result.pairs.length === 0) {
    console.log('✅ No duplicates found.\n');
    return;
  }

  const absorbPairs = result.pairs.filter(p => p.strategy === 'absorb');
  const mergePairs = result.pairs.filter(p => p.strategy === 'merge');
  const keepPairs = result.pairs.filter(p => p.strategy === 'keep_both');

  console.log(`📊 Found ${result.pairs.length} duplicate candidates:`);
  console.log(`   • Absorb candidates (>${(0.95 * 100).toFixed(0)}%): ${absorbPairs.length}`);
  console.log(`   • Merge candidates (${(threshold * 100).toFixed(0)}%-${(0.95 * 100).toFixed(0)}%): ${mergePairs.length}`);
  console.log(`   • Different aspects (<${(threshold * 100).toFixed(0)}%): ${keepPairs.length}\n`);

  if (!dryRun && !auto) {
    console.log('Pairs (showing top 10 by similarity):\n');
    for (const pair of result.pairs.slice(0, 10)) {
      console.log(`  [${(pair.similarity * 100).toFixed(1)}%] ${pair.strategy.toUpperCase()}`);
      console.log(`    A: "${pair.memoryA.text.slice(0, 60)}..." (${pair.memoryA.id})`);
      console.log(`    B: "${pair.memoryB.text.slice(0, 60)}..." (${pair.memoryB.id})`);
      console.log();
    }
    console.log('Run with --auto to apply merges automatically, or --dry-run with no args for scan-only.');
    return;
  }

  if (auto) {
    let applied = 0;
    for (const pair of result.pairs) {
      const memA = getMemory(pair.memoryA.id);
      const memB = getMemory(pair.memoryB.id);
      if (!memA || !memB) continue;

      const result2 = applyDedup(memA, memB, pair.similarity, true);
      if (result2.autoApplied) applied++;
    }
    console.log(`\n✅ Auto-merge complete. Applied ${applied} merge(s).\n`);
  }
}

async function cmdDedupReport() {
  console.log('\n📜 Dedup Merge Log\n');
  const log = loadDedupLog();

  console.log(`Total merges recorded: ${log.merges.length}`);
  console.log(`Total scans recorded: ${log.scans.length}\n`);

  if (log.merges.length > 0) {
    console.log('Recent merges:\n');
    for (const m of log.merges.slice(-10).reverse()) {
      console.log(`  [${new Date(m.timestamp).toLocaleString()}] ${m.strategy}`);
      console.log(`    Merged: ${m.mergedId || m.keptId} ← ${m.discardedId || m.absorbedId}`);
      console.log(`    Similarity: ${m.similarity}`);
      console.log(`    Reason: ${m.reason}`);
      console.log();
    }
  }
}

export async function cmdDedup(args) {
  if (args.scan || Object.keys(args).filter(k => !['_', 'scan'].includes(k)).length === 0) {
    return cmdDedupScan(args);
  }
  if (args.report) {
    return cmdDedupReport();
  }
  // Fallback: treat as scan
  return cmdDedupScan(args);
}

export default { cmdDedup };
