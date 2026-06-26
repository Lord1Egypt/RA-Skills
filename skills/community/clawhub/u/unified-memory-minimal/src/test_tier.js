/**
 * test_tier.js - v2.7.0 Tier Migration Tests
 * Run: node --experimental-vm-modules src/test_tier.js
 * Or simply: node src/test_tier.js
 */
import {
  TIER_CONFIG,
  assignTiers,
  partitionByTier,
  compressColdTier,
  getTierStats,
  autoMigrateTiers,
} from './tier.js';

const DAY_MS = 86400000;
let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✅ ${message}`);
    passed++;
  } else {
    console.log(`  ❌ ${message}`);
    failed++;
  }
}

function makeMemory(id, daysAgo, importance, lastAccessDaysAgo = null) {
  const now = Date.now();
  return {
    id: String(id),
    text: `Memory ${id}`,
    category: 'general',
    importance: importance ?? 0.5,
    created_at: now - daysAgo * DAY_MS,
    timestamp: now - daysAgo * DAY_MS,
    last_access: now - (lastAccessDaysAgo ?? daysAgo) * DAY_MS,
    lastAccess: now - (lastAccessDaysAgo ?? daysAgo) * DAY_MS,
  };
}

console.log('\n=== TIER CONFIG ===');
console.log(TIER_CONFIG);

console.log('\n=== Test: getTier() via assignTiers() ===');
// getTier is not exported; test via assignTiers instead
assert(assignTiers([makeMemory('1', 3, 0.5)])[0].tier === 'HOT', '3-day old memory → HOT');
assert(assignTiers([makeMemory('2', 10, 0.5)])[0].tier === 'WARM', '10-day old memory → WARM');
assert(assignTiers([makeMemory('3', 40, 0.5)])[0].tier === 'COLD', '40-day old memory → COLD');
assert(assignTiers([makeMemory('4', 0, 0.5)])[0].tier === 'HOT', '0-day old memory → HOT');

console.log('\n=== Test: assignTiers() ===');
const mems = [
  makeMemory('a', 3, 0.5),
  makeMemory('b', 10, 0.5),
  makeMemory('c', 40, 0.5),
];
const assigned = assignTiers(mems);
assert(assigned[0].tier === 'HOT', 'assigned[0] is HOT');
assert(assigned[1].tier === 'WARM', 'assigned[1] is WARM');
assert(assigned[2].tier === 'COLD', 'assigned[2] is COLD');

console.log('\n=== Test: partitionByTier() ===');
const partitioned = partitionByTier(mems);
assert(partitioned.HOT.length === 1, 'partitioned: 1 HOT');
assert(partitioned.WARM.length === 1, 'partitioned: 1 WARM');
assert(partitioned.COLD.length === 1, 'partitioned: 1 COLD');

console.log('\n=== Test: getTierStats() ===');
const stats = getTierStats(mems);
assert(stats.HOT === 1 && stats.WARM === 1 && stats.COLD === 1 && stats.total === 3,
  'stats: HOT=1 WARM=1 COLD=1 total=3');

console.log('\n=== Test: compressColdTier() ===');
const coldMems = [
  { id: 'c1', text: 'A'.repeat(500), category: 'fact', importance: 0.6, created_at: Date.now() - 60 * DAY_MS },
  { id: 'c2', text: 'B'.repeat(100), category: 'preference', importance: 0.3, created_at: Date.now() - 50 * DAY_MS, compressed: false },
  { id: 'c3', text: 'C'.repeat(300), category: 'decision', importance: 0.8, created_at: Date.now() - 45 * DAY_MS, compressed: true },
];
const compressed = compressColdTier(coldMems);
assert(compressed[0].compressed === true, 'compressed[0].compressed = true');
assert(compressed[0].text.length === 200, 'compressed[0].text truncated to 200');
assert(compressed[0].original_length === 500, 'compressed[0].original_length = 500');
assert(compressed[1].compressed === true, 'compressed[1].compressed = true');
assert(compressed[2].compressed === true, 'compressed[2] already compressed → unchanged');
assert(compressed[2].text.length === 300, 'compressed[2] unchanged text length = 300');

console.log('\n=== Test: autoMigrateTiers() — HOT → WARM demotion ===');
// HOT: not accessed in 3+ days + importance < 0.5 → demote to WARM
const hotMem1 = makeMemory('hm1', 1, 0.4, 5); // created 1d ago, last accessed 5d ago
const mig1 = autoMigrateTiers([hotMem1], { dryRun: true });
assert(mig1.changes.some(c => c.id === 'hm1' && c.toTier === 'WARM'),
  'HOT 5d-no-access + importance 0.4 → demote to WARM');

console.log('\n=== Test: autoMigrateTiers() — HOT → COLD demotion ===');
// HOT: not accessed in 7+ days + importance < 0.3 → demote to COLD
const hotMem2 = makeMemory('hm2', 1, 0.2, 8); // created 1d ago, last accessed 8d ago
const mig2 = autoMigrateTiers([hotMem2], { dryRun: true });
assert(mig2.changes.some(c => c.id === 'hm2' && c.toTier === 'COLD'),
  'HOT 8d-no-access + importance 0.2 → demote to COLD');

console.log('\n=== Test: autoMigrateTiers() — COLD → HOT promotion ===');
// COLD: accessed in last 2 days + importance >= 0.7 → promote to HOT
const coldMem1 = makeMemory('cm1', 60, 0.8, 1); // created 60d ago, accessed 1d ago
const mig3 = autoMigrateTiers([coldMem1], { dryRun: true });
assert(mig3.changes.some(c => c.id === 'cm1' && c.toTier === 'HOT'),
  'COLD accessed 1d ago + importance 0.8 → promote to HOT');

console.log('\n=== Test: autoMigrateTiers() — COLD → WARM promotion ===');
// COLD: accessed in last 7 days + importance >= 0.4 → promote to WARM
const coldMem2 = makeMemory('cm2', 60, 0.5, 5); // created 60d ago, accessed 5d ago
const mig4 = autoMigrateTiers([coldMem2], { dryRun: true });
assert(mig4.changes.some(c => c.id === 'cm2' && c.toTier === 'WARM'),
  'COLD accessed 5d ago + importance 0.5 → promote to WARM');

console.log('\n=== Test: autoMigrateTiers() — WARM → HOT promotion ===');
// WARM: accessed in last 2 days + importance >= 0.5 → promote to HOT
const warmMem1 = makeMemory('wm1', 15, 0.6, 1); // created 15d ago, accessed 1d ago
const mig5 = autoMigrateTiers([warmMem1], { dryRun: true });
assert(mig5.changes.some(c => c.id === 'wm1' && c.toTier === 'HOT'),
  'WARM accessed 1d ago + importance 0.6 → promote to HOT');

console.log('\n=== Test: autoMigrateTiers() — WARM → COLD demotion ===');
// WARM: not accessed in 14+ days → demote to COLD
const warmMem2 = makeMemory('wm2', 15, 0.3, 16); // created 15d ago, accessed 16d ago
const mig6 = autoMigrateTiers([warmMem2], { dryRun: true });
assert(mig6.changes.some(c => c.id === 'wm2' && c.toTier === 'COLD'),
  'WARM not accessed 16d → demote to COLD');

console.log('\n=== Test: autoMigrateTiers() — no change when stable ===');
// HOT memory recently accessed → stays HOT
const hotMem3 = makeMemory('hm3', 5, 0.6, 1); // created 5d ago, accessed 1d ago
const mig7 = autoMigrateTiers([hotMem3], { dryRun: true });
assert(mig7.changes.length === 0, 'Recent-access HOT memory stays HOT (no changes)');

console.log('\n=== Test: autoMigrateTiers() — dryRun=true modifies returned copy only ===');
const original = makeMemory('orig', 1, 0.4, 5);
// The returned memories are a copy; verify HOT→WARM change was made on the copy
const migOrig = autoMigrateTiers([original], { dryRun: true });
assert(migOrig.changes.length === 1, 'dryRun: changes detected');
assert(migOrig.changes[0].toTier === 'WARM', 'dryRun: detected HOT→WARM change');
assert(migOrig.memories[0].tier === 'WARM', 'dryRun: returned memories[0].tier set to WARM');
// Note: we can't easily verify original wasn't modified since the returned array IS a copy
// The key behavior is: changes are computed and returned, but saveMemories is only called externally

console.log('\n=== Test: tier_tools import & smoke test ===');
try {
  const { memoryTierStatusTool, memoryTierMigrateTool, memoryTierCompressTool } = await import('./tier_tools.js');
  assert(true, 'tier_tools.js imports successfully');
  // Smoke test: dry-run mode (no actual storage access)
  const statusResult = memoryTierStatusTool();
  assert(statusResult.content && statusResult.content[0], 'memoryTierStatusTool returns content');
  const migrateResult = memoryTierMigrateTool({ apply: false });
  assert(migrateResult.content && migrateResult.content[0], 'memoryTierMigrateTool returns content');
  const compressResult = memoryTierCompressTool({ apply: false });
  assert(compressResult.content && compressResult.content[0], 'memoryTierCompressTool returns content');
} catch (e) {
  assert(false, `tier_tools.js failed: ${e.message}`);
}

console.log('\n=== SUMMARY ===');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total:  ${passed + failed}`);

if (failed > 0) {
  process.exit(1);
} else {
  console.log('\n🎉 All tests passed!\n');
}
