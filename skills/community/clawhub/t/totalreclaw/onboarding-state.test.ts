/**
 * Tests for the 3.2.0 onboarding state machine (fs-helpers.ts — state surface).
 *
 * State model (simplest possible, per user's clean-slate ratification 2026-04-19):
 *   - `fresh`  → no usable credentials; memory tools gated.
 *   - `active` → credentials.json has a valid mnemonic; tools unblocked.
 *
 * Coverage targets:
 *   1. defaultFreshState shape.
 *   2. writeOnboardingState is atomic (temp + rename), sets 0600.
 *   3. loadOnboardingState rejects non-{fresh,active} values with `null`.
 *   4. deriveStateFromCredentials: missing file → fresh.
 *   5. deriveStateFromCredentials: valid mnemonic → active.
 *   6. deriveStateFromCredentials: empty / non-string mnemonic → fresh.
 *   7. deriveStateFromCredentials: recovery_phrase alias → active.
 *   8. resolveOnboardingState: no persisted state + missing creds → fresh (persisted).
 *   9. resolveOnboardingState: no persisted state + valid creds → active (persisted).
 *   10. resolveOnboardingState: persisted matches implied → returned as-is.
 *   11. resolveOnboardingState: persisted disagrees with creds → recomputes + writes.
 *   12. resolveOnboardingState preserves createdBy when recomputing.
 *
 * Run with: npx tsx onboarding-state.test.ts
 *
 * TAP-style, no jest dependency — matches credentials-bootstrap.test.ts style.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  defaultFreshState,
  loadOnboardingState,
  writeOnboardingState,
  deriveStateFromCredentials,
  resolveOnboardingState,
  type OnboardingState,
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
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-state-'));
}

// ---------------------------------------------------------------------------
// 1. defaultFreshState shape
// ---------------------------------------------------------------------------
{
  const s = defaultFreshState();
  assert(s.onboardingState === 'fresh', 'default: state is "fresh"');
  assert(s.version === '3.2.0', 'default: version pinned to "3.2.0"');
  assert(s.credentialsCreatedAt === undefined, 'default: no createdAt');
  assert(s.createdBy === undefined, 'default: no createdBy');
}

// ---------------------------------------------------------------------------
// 2. writeOnboardingState — atomic, 0600
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const statePath = path.join(tmp, 'state.json');
  const state: OnboardingState = {
    onboardingState: 'active',
    createdBy: 'generate',
    credentialsCreatedAt: '2026-04-19T10:00:00.000Z',
    version: '3.2.0',
  };

  assert(writeOnboardingState(statePath, state) === true, 'write: returns true on success');
  assert(fs.existsSync(statePath), 'write: state.json written to disk');

  const mode = fs.statSync(statePath).mode & 0o777;
  assert(mode === 0o600, `write: mode is 0o600 (got ${mode.toString(8)})`);

  const on = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
  assert(on.onboardingState === 'active', 'write: onboardingState persisted');
  assert(on.createdBy === 'generate', 'write: createdBy persisted');

  // No leftover temp files in the directory.
  const leftovers = fs.readdirSync(tmp).filter((f) => f.startsWith('state.json.tmp-'));
  assert(leftovers.length === 0, `write: no leftover temp files (got ${leftovers.join(',')})`);

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 3. loadOnboardingState — rejects unknown values with null
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const statePath = path.join(tmp, 'state.json');

  fs.writeFileSync(statePath, JSON.stringify({ onboardingState: 'awaiting', version: '3.0.0' }));
  assert(loadOnboardingState(statePath) === null, 'load: rejects non-{fresh,active} onboardingState');

  fs.writeFileSync(statePath, 'not json');
  assert(loadOnboardingState(statePath) === null, 'load: returns null on invalid JSON');

  fs.writeFileSync(statePath, JSON.stringify({}));
  assert(loadOnboardingState(statePath) === null, 'load: returns null on empty object');

  fs.writeFileSync(statePath, JSON.stringify({ onboardingState: 'fresh' }));
  const ok = loadOnboardingState(statePath);
  assert(ok?.onboardingState === 'fresh', 'load: accepts well-formed "fresh"');

  fs.writeFileSync(statePath, JSON.stringify({ onboardingState: 'active', createdBy: 'import' }));
  const act = loadOnboardingState(statePath);
  assert(act?.onboardingState === 'active', 'load: accepts well-formed "active"');
  assert(act?.createdBy === 'import', 'load: preserves createdBy="import"');

  // Malformed createdBy → sanitised to undefined.
  fs.writeFileSync(statePath, JSON.stringify({ onboardingState: 'active', createdBy: 'hax' }));
  const san = loadOnboardingState(statePath);
  assert(san?.createdBy === undefined, 'load: sanitises unknown createdBy to undefined');

  // Missing file
  fs.rmSync(statePath);
  assert(loadOnboardingState(statePath) === null, 'load: returns null for missing file');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 4-7. deriveStateFromCredentials
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');

  // 4. Missing file → fresh
  assert(deriveStateFromCredentials(credPath) === 'fresh', 'derive: missing creds → fresh');

  // 5. Valid mnemonic → active
  fs.writeFileSync(
    credPath,
    JSON.stringify({ mnemonic: 'one two three four five six seven eight nine ten eleven twelve' }),
  );
  assert(deriveStateFromCredentials(credPath) === 'active', 'derive: valid mnemonic → active');

  // 6. Empty mnemonic → fresh
  fs.writeFileSync(credPath, JSON.stringify({ mnemonic: '' }));
  assert(deriveStateFromCredentials(credPath) === 'fresh', 'derive: empty mnemonic → fresh');

  // 6b. Non-string mnemonic → fresh
  fs.writeFileSync(credPath, JSON.stringify({ mnemonic: 12345 }));
  assert(deriveStateFromCredentials(credPath) === 'fresh', 'derive: non-string mnemonic → fresh');

  // 6c. Whitespace mnemonic → fresh
  fs.writeFileSync(credPath, JSON.stringify({ mnemonic: '   ' }));
  assert(deriveStateFromCredentials(credPath) === 'fresh', 'derive: whitespace mnemonic → fresh');

  // 7. recovery_phrase alias → active
  fs.writeFileSync(
    credPath,
    JSON.stringify({ recovery_phrase: 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu' }),
  );
  assert(
    deriveStateFromCredentials(credPath) === 'active',
    'derive: recovery_phrase alias → active',
  );

  // Corrupt JSON → fresh (load returns null, mnemonic extract returns null)
  fs.writeFileSync(credPath, '{invalid json');
  assert(deriveStateFromCredentials(credPath) === 'fresh', 'derive: corrupt JSON → fresh');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 8. resolveOnboardingState — no persisted + missing creds → fresh (persisted)
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');

  const s = resolveOnboardingState(credPath, statePath);
  assert(s.onboardingState === 'fresh', 'resolve: fresh case returns fresh');
  assert(fs.existsSync(statePath), 'resolve: state.json written even for fresh');
  const on = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
  assert(on.onboardingState === 'fresh', 'resolve: persisted state is fresh');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 9. resolveOnboardingState — no persisted + valid creds → active (persisted)
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');

  fs.writeFileSync(
    credPath,
    JSON.stringify({ mnemonic: 'one two three four five six seven eight nine ten eleven twelve' }),
  );

  const s = resolveOnboardingState(credPath, statePath);
  assert(s.onboardingState === 'active', 'resolve: active case returns active');
  const on = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
  assert(on.onboardingState === 'active', 'resolve: persisted state is active');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 10. resolveOnboardingState — persisted matches implied → returned as-is
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');

  fs.writeFileSync(
    credPath,
    JSON.stringify({ mnemonic: 'one two three four five six seven eight nine ten eleven twelve' }),
  );
  const persisted: OnboardingState = {
    onboardingState: 'active',
    createdBy: 'generate',
    credentialsCreatedAt: '2026-04-19T08:00:00.000Z',
    version: '3.2.0',
  };
  fs.writeFileSync(statePath, JSON.stringify(persisted), { mode: 0o600 });
  const beforeMtime = fs.statSync(statePath).mtimeMs;

  // Wait a tick to make mtime comparison meaningful (fs mtime resolution is 1ms on some FS).
  const s = resolveOnboardingState(credPath, statePath);
  assert(s.onboardingState === 'active', 'resolve-match: returns active');
  assert(s.createdBy === 'generate', 'resolve-match: preserves createdBy=generate');
  assert(s.credentialsCreatedAt === '2026-04-19T08:00:00.000Z', 'resolve-match: preserves createdAt');

  // No rewrite — file should not have been touched. mtime check is best-effort
  // since some filesystems coalesce writes. Compare content instead.
  const after = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
  assert(after.createdBy === 'generate', 'resolve-match: on-disk createdBy unchanged');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 11. resolveOnboardingState — persisted disagrees → recomputes + writes
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');

  // Persisted says "active" but credentials.json is missing.
  fs.writeFileSync(statePath, JSON.stringify({ onboardingState: 'active', createdBy: 'import', version: '3.2.0' }));

  const s = resolveOnboardingState(credPath, statePath);
  assert(s.onboardingState === 'fresh', 'resolve-disagree: creds missing → flips to fresh');

  const on = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
  assert(on.onboardingState === 'fresh', 'resolve-disagree: persisted flipped to fresh on disk');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 12. resolveOnboardingState preserves createdBy even when flipping fresh→active
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');

  // Stale state file says "fresh" but creds were dropped in (e.g. user ran CLI
  // wizard in parallel and state file hasn't been updated yet).
  fs.writeFileSync(statePath, JSON.stringify({ onboardingState: 'fresh', createdBy: 'import', version: '3.2.0' }));
  fs.writeFileSync(
    credPath,
    JSON.stringify({ mnemonic: 'one two three four five six seven eight nine ten eleven twelve' }),
  );

  const s = resolveOnboardingState(credPath, statePath);
  assert(s.onboardingState === 'active', 'resolve-preserve: flips to active');
  assert(s.createdBy === 'import', 'resolve-preserve: preserves prior createdBy=import');

  const on = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
  assert(on.createdBy === 'import', 'resolve-preserve: on-disk createdBy preserved');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------
console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
