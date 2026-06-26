/**
 * Tests for autoBootstrapCredentials (bug #4 from 3.0.7-rc.1 QA).
 *
 * Regression: if credentials.json was missing OR had a mnemonic field but
 * no TOTALRECLAW_RECOVERY_PHRASE env var, the plugin asked the user to
 * explicitly call `totalreclaw_setup` on their first turn. That's a lousy
 * first-run UX — the user just installed a plugin, they shouldn't have
 * to babysit an init ceremony.
 *
 * Fix design:
 *   1. Probe credentials.json on plugin load (before `initialize()`).
 *   2. If valid shape (non-empty mnemonic or recovery_phrase) → no-op.
 *   3. If missing → generate a fresh BIP-39 mnemonic and write the file.
 *   4. If corrupt JSON or missing/empty mnemonic field → rename to
 *      credentials.json.broken-<ts> and generate a fresh mnemonic.
 *   5. Persist a `firstRunAnnouncementShown: false` flag so we can show
 *      the recovery phrase to the user EXACTLY ONCE (on their next
 *      before_agent_start turn), then flip to `true`.
 *
 * Also: read both `mnemonic` (plugin-native) AND `recovery_phrase`
 * (what some users / guides / older flows write manually) so either
 * spelling works. On write we always use `mnemonic` for compatibility
 * with the MCP server CLI.
 *
 * Run with: npx tsx credentials-bootstrap.test.ts
 *
 * TAP-style output, no jest dependency.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  autoBootstrapCredentials,
  markFirstRunAnnouncementShown,
  extractBootstrapMnemonic,
  type BootstrapOutcome,
} from './fs-helpers.js';

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

function mkTmp(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-bootstrap-'));
}

// A deterministic "mnemonic generator" for tests — real BIP-39 generator
// is injected by the caller in production code (keeps the fs-helpers
// module free of crypto imports).
function fakeMnemonic(tag: string): string {
  return `word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 ${tag}`;
}

// ---------------------------------------------------------------------------
// 1. Missing file → generate fresh mnemonic + write + announcement pending
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  assert(!fs.existsSync(credPath), 'precondition: credentials.json missing');

  const outcome: BootstrapOutcome = autoBootstrapCredentials(credPath, {
    generateMnemonic: () => fakeMnemonic('fresh'),
  });

  assert(outcome.status === 'fresh_generated', `missing: status is "fresh_generated" (got ${outcome.status})`);
  assert(outcome.mnemonic === fakeMnemonic('fresh'), 'missing: returned mnemonic is the generated one');
  assert(outcome.announcementPending === true, 'missing: announcementPending is true');
  assert(fs.existsSync(credPath), 'missing: credentials.json now exists on disk');

  const saved = JSON.parse(fs.readFileSync(credPath, 'utf-8'));
  assert(saved.mnemonic === fakeMnemonic('fresh'), 'missing: mnemonic persisted under "mnemonic" key');
  assert(saved.firstRunAnnouncementShown === false, 'missing: firstRunAnnouncementShown persisted as false');

  // File permissions: must be 0o600 (owner rw only). Stat mode masks off
  // file type; take the low 9 bits.
  const mode = fs.statSync(credPath).mode & 0o777;
  assert(mode === 0o600, `missing: credentials.json mode is 0o600 (got ${mode.toString(8)})`);

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 2. Valid existing mnemonic → no-op, no announcement
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const existing = {
    userId: 'user-abc',
    salt: 'deadbeef'.repeat(16), // 64-char hex
    mnemonic: 'one two three four five six seven eight nine ten eleven twelve',
    firstRunAnnouncementShown: true,
  };
  fs.writeFileSync(credPath, JSON.stringify(existing), { mode: 0o600 });
  const beforeContent = fs.readFileSync(credPath, 'utf-8');

  const outcome = autoBootstrapCredentials(credPath, {
    generateMnemonic: () => {
      throw new Error('generator should NOT be called for valid existing file');
    },
  });

  assert(outcome.status === 'existing_valid', `valid: status is "existing_valid" (got ${outcome.status})`);
  assert(outcome.mnemonic === existing.mnemonic, 'valid: outcome.mnemonic matches disk');
  assert(outcome.announcementPending === false, 'valid: announcementPending is false');
  assert(fs.readFileSync(credPath, 'utf-8') === beforeContent, 'valid: file contents unchanged');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 3. Existing file with `recovery_phrase` alias → treated as valid, migrated
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const existing = {
    userId: 'user-xyz',
    salt: 'cafecafe'.repeat(16),
    // User (or older CLI) wrote `recovery_phrase` instead of `mnemonic`.
    // This is the exact shape the 3.0.7-rc.1 QA flagged as "not auto-
    // triggered" — plugin ignored it and asked for setup anyway.
    recovery_phrase: 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu',
  };
  fs.writeFileSync(credPath, JSON.stringify(existing), { mode: 0o600 });

  const outcome = autoBootstrapCredentials(credPath, {
    generateMnemonic: () => {
      throw new Error('generator should NOT be called for valid recovery_phrase alias');
    },
  });

  assert(outcome.status === 'existing_valid', `alias: status is "existing_valid" (got ${outcome.status})`);
  assert(outcome.mnemonic === existing.recovery_phrase, 'alias: outcome.mnemonic read from recovery_phrase key');
  assert(outcome.announcementPending === false, 'alias: announcementPending is false');

  // After bootstrap, the canonical `mnemonic` key is populated for
  // downstream callers that only look for `mnemonic`.
  const saved = JSON.parse(fs.readFileSync(credPath, 'utf-8'));
  assert(saved.mnemonic === existing.recovery_phrase, 'alias: canonical "mnemonic" key now present');
  assert(saved.userId === existing.userId, 'alias: userId preserved');
  assert(saved.salt === existing.salt, 'alias: salt preserved');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 4. Corrupt JSON → rename to .broken-<ts>, generate fresh, pending
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  fs.writeFileSync(credPath, '{ this is not: valid json', { mode: 0o600 });

  const outcome = autoBootstrapCredentials(credPath, {
    generateMnemonic: () => fakeMnemonic('recovered'),
  });

  assert(outcome.status === 'recovered_from_corrupt', `corrupt: status is "recovered_from_corrupt" (got ${outcome.status})`);
  assert(outcome.mnemonic === fakeMnemonic('recovered'), 'corrupt: returned mnemonic is the generated one');
  assert(outcome.announcementPending === true, 'corrupt: announcementPending is true');
  assert(typeof outcome.backupPath === 'string' && outcome.backupPath!.includes('.broken-'), 'corrupt: backupPath exposes the renamed file');
  if (outcome.backupPath) {
    assert(fs.existsSync(outcome.backupPath), 'corrupt: renamed-backup file actually exists on disk');
  }
  assert(fs.existsSync(credPath), 'corrupt: new credentials.json exists');

  const saved = JSON.parse(fs.readFileSync(credPath, 'utf-8'));
  assert(saved.mnemonic === fakeMnemonic('recovered'), 'corrupt: new file has the fresh mnemonic');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 5. Existing file with no mnemonic / no recovery_phrase → treated as
//    malformed, renamed + regenerated
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  // Valid JSON but no mnemonic of any spelling — this is the exact
  // failure mode that a plugin-first-run-then-env-var-removed user would
  // land on: userId + salt but no mnemonic.
  fs.writeFileSync(credPath, JSON.stringify({ userId: 'orphan', salt: 'ffff' }), { mode: 0o600 });

  const outcome = autoBootstrapCredentials(credPath, {
    generateMnemonic: () => fakeMnemonic('orphaned'),
  });

  assert(outcome.status === 'recovered_from_corrupt', `no-mnemonic: status is "recovered_from_corrupt" (got ${outcome.status})`);
  assert(outcome.mnemonic === fakeMnemonic('orphaned'), 'no-mnemonic: returned the generated mnemonic');
  assert(typeof outcome.backupPath === 'string', 'no-mnemonic: backupPath is set');
  if (outcome.backupPath) {
    assert(fs.existsSync(outcome.backupPath), 'no-mnemonic: backup file exists');
    // The backup should have the old userId so the user could, in theory,
    // recover if they still have the mnemonic somewhere.
    const backup = JSON.parse(fs.readFileSync(outcome.backupPath, 'utf-8'));
    assert(backup.userId === 'orphan', 'no-mnemonic: backup preserves original userId');
  }

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 6. Empty-string mnemonic → treated as malformed
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  fs.writeFileSync(credPath, JSON.stringify({ mnemonic: '   ' }), { mode: 0o600 });

  const outcome = autoBootstrapCredentials(credPath, {
    generateMnemonic: () => fakeMnemonic('whitespace'),
  });

  assert(outcome.status === 'recovered_from_corrupt', 'whitespace: status is "recovered_from_corrupt"');
  assert(outcome.mnemonic === fakeMnemonic('whitespace'), 'whitespace: generated a fresh mnemonic');
}

// ---------------------------------------------------------------------------
// 7. markFirstRunAnnouncementShown — flips the flag on disk
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');

  // Bootstrap a fresh file first
  autoBootstrapCredentials(credPath, {
    generateMnemonic: () => fakeMnemonic('pre-ack'),
  });
  const beforeAck = JSON.parse(fs.readFileSync(credPath, 'utf-8'));
  assert(beforeAck.firstRunAnnouncementShown === false, 'ack: flag starts at false');

  const flipped = markFirstRunAnnouncementShown(credPath);
  assert(flipped === true, 'ack: markFirstRunAnnouncementShown returns true on success');

  const afterAck = JSON.parse(fs.readFileSync(credPath, 'utf-8'));
  assert(afterAck.firstRunAnnouncementShown === true, 'ack: flag is now true on disk');
  assert(afterAck.mnemonic === fakeMnemonic('pre-ack'), 'ack: mnemonic unchanged by flag flip');

  // Idempotent — flipping twice is safe.
  const flippedAgain = markFirstRunAnnouncementShown(credPath);
  assert(flippedAgain === true, 'ack: idempotent — second call also returns true');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 8. markFirstRunAnnouncementShown on missing file → returns false
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'nope.json');
  const result = markFirstRunAnnouncementShown(credPath);
  assert(result === false, 'ack: returns false when credentials.json is missing');
  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 9. extractBootstrapMnemonic — pure helper, accepts both field names
// ---------------------------------------------------------------------------
{
  assert(
    extractBootstrapMnemonic({ mnemonic: 'one two' }) === 'one two',
    'extract: prefers mnemonic field',
  );
  assert(
    extractBootstrapMnemonic({ recovery_phrase: 'alpha beta' }) === 'alpha beta',
    'extract: falls back to recovery_phrase',
  );
  assert(
    extractBootstrapMnemonic({ mnemonic: 'm1', recovery_phrase: 'm2' }) === 'm1',
    'extract: prefers mnemonic when both present',
  );
  assert(
    extractBootstrapMnemonic({}) === null,
    'extract: returns null for empty object',
  );
  assert(
    extractBootstrapMnemonic({ mnemonic: '   ' }) === null,
    'extract: treats whitespace-only as empty',
  );
  assert(
    extractBootstrapMnemonic({ mnemonic: 42 as unknown as string }) === null,
    'extract: rejects non-string values',
  );
  assert(
    extractBootstrapMnemonic(null) === null,
    'extract: rejects null',
  );
}

// ---------------------------------------------------------------------------
// 10. Atomic write — bootstrap failure partway through does not leave
//     a half-written credentials.json that would be re-bootstrapped next
//     startup.
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');

  // Throw from the generator — bootstrap must propagate the error without
  // leaving behind a partial file.
  let caught = false;
  try {
    autoBootstrapCredentials(credPath, {
      generateMnemonic: () => {
        throw new Error('entropy source unavailable');
      },
    });
  } catch (e) {
    caught = true;
    assert(e instanceof Error && /entropy/.test(e.message), 'atomic: the generator error propagates');
  }
  assert(caught, 'atomic: bootstrap throws when generator throws');
  assert(!fs.existsSync(credPath), 'atomic: no credentials.json left behind after generator failure');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------
console.log(`# fail: ${failed}`);
if (failed === 0) {
  console.log(`# ${passed}/${passed} passed`);
  console.log(`\nALL TESTS PASSED`);
  process.exit(0);
} else {
  console.log(`# ${passed}/${passed + failed} passed, ${failed} failed`);
  process.exit(1);
}
