/**
 * Tests for the per-channel inbound-user tracker (issue #215, 3.3.7-rc.1).
 *
 * Asserted:
 *   - Empty state → count = 0
 *   - Single user recorded → count = 1
 *   - Same user recorded twice → still count = 1 (idempotent)
 *   - Two distinct users → count = 2
 *   - Per-channel isolation (telegram count != discord count)
 *   - Persistence: write + re-read returns same count
 *   - Survives module-cache reset (re-reads from disk)
 *
 * Run with: npx tsx inbound-user-tracker.test.ts
 */

import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import {
  recordInboundUser,
  getDistinctInboundUserCount,
  resolveTrackerPath,
  __resetForTesting,
} from './inbound-user-tracker.js';

let passed = 0;
let failed = 0;

function assert(condition: boolean, name: string): void {
  const n = passed + failed + 1;
  if (condition) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-tracker-'));
const credentialsPath = path.join(tmpDir, 'credentials.json');
const trackerPath = resolveTrackerPath(credentialsPath);

// Clean slate each test run.
function resetStorage(): void {
  __resetForTesting();
  if (fs.existsSync(trackerPath)) fs.unlinkSync(trackerPath);
}

// ---------------------------------------------------------------------------
// Empty state
// ---------------------------------------------------------------------------
resetStorage();
assert(getDistinctInboundUserCount(trackerPath, 'telegram') === 0, 'empty: count = 0');

// ---------------------------------------------------------------------------
// Single user recorded
// ---------------------------------------------------------------------------
resetStorage();
recordInboundUser(trackerPath, 'telegram', '12345');
assert(getDistinctInboundUserCount(trackerPath, 'telegram') === 1, 'single user: count = 1');

// ---------------------------------------------------------------------------
// Idempotent (same user twice)
// ---------------------------------------------------------------------------
resetStorage();
recordInboundUser(trackerPath, 'telegram', '12345');
recordInboundUser(trackerPath, 'telegram', '12345');
recordInboundUser(trackerPath, 'telegram', '12345');
assert(getDistinctInboundUserCount(trackerPath, 'telegram') === 1, 'idempotent: same user twice → count = 1');

// ---------------------------------------------------------------------------
// Two distinct users
// ---------------------------------------------------------------------------
resetStorage();
recordInboundUser(trackerPath, 'telegram', '12345');
recordInboundUser(trackerPath, 'telegram', '67890');
assert(getDistinctInboundUserCount(trackerPath, 'telegram') === 2, 'two users: count = 2');

// ---------------------------------------------------------------------------
// Per-channel isolation
// ---------------------------------------------------------------------------
resetStorage();
recordInboundUser(trackerPath, 'telegram', '12345');
recordInboundUser(trackerPath, 'discord', 'abcdef');
recordInboundUser(trackerPath, 'discord', 'ghijkl');
assert(getDistinctInboundUserCount(trackerPath, 'telegram') === 1, 'telegram isolation: count = 1');
assert(getDistinctInboundUserCount(trackerPath, 'discord') === 2, 'discord isolation: count = 2');
assert(getDistinctInboundUserCount(trackerPath, 'slack') === 0, 'unmessaged channel: count = 0');

// ---------------------------------------------------------------------------
// Persistence: simulate module reload
// ---------------------------------------------------------------------------
resetStorage();
recordInboundUser(trackerPath, 'telegram', '12345');
recordInboundUser(trackerPath, 'telegram', '67890');
__resetForTesting();  // wipe in-memory cache
assert(getDistinctInboundUserCount(trackerPath, 'telegram') === 2, 'persistence: re-read after cache reset → count = 2');

// File is mode 0o600?
{
  const stat = fs.statSync(trackerPath);
  // On macOS / linux mode includes file-type bits; mask down to perms.
  assert((stat.mode & 0o777) === 0o600, 'file mode = 0o600');
}

// ---------------------------------------------------------------------------
// Channel slug normalization (lowercase + trim)
// ---------------------------------------------------------------------------
resetStorage();
recordInboundUser(trackerPath, '  Telegram  ', '12345');
assert(getDistinctInboundUserCount(trackerPath, 'telegram') === 1, 'channel slug lowercased + trimmed');
assert(getDistinctInboundUserCount(trackerPath, 'TELEGRAM') === 1, 'channel slug case-insensitive on read');

// Empty channel/sender id → no-op
resetStorage();
assert(recordInboundUser(trackerPath, '', '12345') === false, 'empty channel → false (no record)');
assert(recordInboundUser(trackerPath, 'telegram', '') === false, 'empty senderId → false (no record)');
assert(getDistinctInboundUserCount(trackerPath, 'telegram') === 0, 'after no-op records → count = 0');

// Cleanup
fs.rmSync(tmpDir, { recursive: true, force: true });

// ---------------------------------------------------------------------------
// Done
// ---------------------------------------------------------------------------
console.log(`\n# tests ${passed + failed}`);
console.log(`# pass ${passed}`);
console.log(`# fail ${failed}`);
if (failed > 0) {
  console.error(`\ninbound-user-tracker.test FAILED — ${failed} assertion(s) did not hold.`);
  process.exit(1);
}
