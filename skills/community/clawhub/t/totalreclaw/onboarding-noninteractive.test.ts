/**
 * Tests for `runNonInteractiveOnboard` (3.3.1 agent-driven onboarding).
 *
 * Covers:
 *   - mode=generate creates credentials.json + state.json with mode 0600
 *   - mode=generate JSON result omits the phrase by default
 *   - emitPhrase=true includes phrase (deprecation path)
 *   - mode=restore with a valid 12-word phrase writes credentials
 *   - mode=restore with an invalid phrase returns error=invalid-phrase
 *   - mode=restore without a phrase returns error=missing-phrase
 *   - Existing credentials.json short-circuits with error=already-active
 *
 * Run with: npx tsx onboarding-noninteractive.test.ts
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { runNonInteractiveOnboard } from './onboarding-cli.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function assertEq<T>(actual: T, expected: T, name: string): void {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  if (!ok) {
    console.log(`  actual:   ${JSON.stringify(actual)}`);
    console.log(`  expected: ${JSON.stringify(expected)}`);
  }
  assert(ok, name);
}

function mkTmp(): { credentialsPath: string; statePath: string; dir: string } {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-ni-'));
  return {
    dir,
    credentialsPath: path.join(dir, 'credentials.json'),
    statePath: path.join(dir, 'state.json'),
  };
}

// A canonical valid 12-word mnemonic for import/restore tests
const VALID_PHRASE =
  'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about';
const INVALID_PHRASE_BAD_CHECKSUM =
  'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon';

// ---------------------------------------------------------------------------
// mode=generate happy path
// ---------------------------------------------------------------------------

{
  const t = mkTmp();
  const result = await runNonInteractiveOnboard({
    credentialsPath: t.credentialsPath,
    statePath: t.statePath,
    mode: 'generate',
  });
  assert(result.ok === true, 'generate: ok=true');
  assertEq(result.action, 'generate', 'generate: action echoed');
  assert(result.mnemonic === undefined, 'generate: phrase NOT included in payload by default');
  assertEq(result.credentials_path, t.credentialsPath, 'generate: credentials_path echoed');

  // Credentials written
  const creds = JSON.parse(fs.readFileSync(t.credentialsPath, 'utf-8')) as { mnemonic?: string };
  assert(
    typeof creds.mnemonic === 'string' && creds.mnemonic.trim().split(/\s+/).length === 12,
    'generate: credentials.json contains a 12-word phrase',
  );

  // Mode 0600 — skip on non-Unix (Windows treats mode differently)
  if (process.platform !== 'win32') {
    const st = fs.statSync(t.credentialsPath);
    const mode = st.mode & 0o777;
    assert(mode === 0o600, `generate: credentials.json mode is 0600 (got 0o${mode.toString(8)})`);
  }

  // State written
  const state = JSON.parse(fs.readFileSync(t.statePath, 'utf-8')) as {
    onboardingState?: string;
    createdBy?: string;
  };
  assertEq(state.onboardingState, 'active', 'generate: state.onboardingState === active');
  assertEq(state.createdBy, 'generate', 'generate: state.createdBy === generate');
}

// ---------------------------------------------------------------------------
// emitPhrase=true returns the phrase
// ---------------------------------------------------------------------------

{
  const t = mkTmp();
  const result = await runNonInteractiveOnboard({
    credentialsPath: t.credentialsPath,
    statePath: t.statePath,
    mode: 'generate',
    emitPhrase: true,
  });
  assert(result.ok === true, 'emit-phrase: ok=true');
  assert(
    typeof result.mnemonic === 'string' && result.mnemonic.trim().split(/\s+/).length === 12,
    'emit-phrase: mnemonic included in payload',
  );
}

// ---------------------------------------------------------------------------
// mode=restore with valid phrase
// ---------------------------------------------------------------------------

{
  const t = mkTmp();
  const result = await runNonInteractiveOnboard({
    credentialsPath: t.credentialsPath,
    statePath: t.statePath,
    mode: 'restore',
    phrase: VALID_PHRASE,
  });
  assert(result.ok === true, 'restore: ok=true with valid phrase');
  assertEq(result.action, 'restore', 'restore: action echoed');

  const creds = JSON.parse(fs.readFileSync(t.credentialsPath, 'utf-8')) as { mnemonic?: string };
  assertEq(creds.mnemonic, VALID_PHRASE, 'restore: credentials.json stores the exact phrase');

  const state = JSON.parse(fs.readFileSync(t.statePath, 'utf-8')) as { createdBy?: string };
  assertEq(state.createdBy, 'import', 'restore: state.createdBy === import');
}

// ---------------------------------------------------------------------------
// mode=restore with invalid phrase
// ---------------------------------------------------------------------------

{
  const t = mkTmp();
  const result = await runNonInteractiveOnboard({
    credentialsPath: t.credentialsPath,
    statePath: t.statePath,
    mode: 'restore',
    phrase: INVALID_PHRASE_BAD_CHECKSUM,
  });
  assert(result.ok === false, 'restore: ok=false with invalid phrase');
  assertEq(result.error, 'invalid-phrase', 'restore: error === invalid-phrase');
  assert(!fs.existsSync(t.credentialsPath), 'restore: no credentials written on invalid phrase');
}

// ---------------------------------------------------------------------------
// mode=restore without a phrase
// ---------------------------------------------------------------------------

{
  const t = mkTmp();
  const result = await runNonInteractiveOnboard({
    credentialsPath: t.credentialsPath,
    statePath: t.statePath,
    mode: 'restore',
  });
  assert(result.ok === false, 'restore: ok=false without --phrase');
  assertEq(result.error, 'missing-phrase', 'restore: error === missing-phrase');
}

// ---------------------------------------------------------------------------
// Already-active short-circuit
// ---------------------------------------------------------------------------

{
  const t = mkTmp();
  fs.writeFileSync(t.credentialsPath, JSON.stringify({ mnemonic: VALID_PHRASE }), { mode: 0o600 });
  const result = await runNonInteractiveOnboard({
    credentialsPath: t.credentialsPath,
    statePath: t.statePath,
    mode: 'generate',
  });
  assert(result.ok === false, 'already-active: ok=false');
  assertEq(result.error, 'already-active', 'already-active: error === already-active');
}

// ---------------------------------------------------------------------------
// deriveScopeAddress is plumbed through
// ---------------------------------------------------------------------------

{
  const t = mkTmp();
  const result = await runNonInteractiveOnboard({
    credentialsPath: t.credentialsPath,
    statePath: t.statePath,
    mode: 'generate',
    deriveScopeAddress: async () => '0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef',
  });
  assertEq(
    result.scope_address,
    '0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef',
    'scope_address: derived when helper provided',
  );
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
