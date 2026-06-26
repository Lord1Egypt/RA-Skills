/**
 * Tests for first-run.ts — 3.3.0-rc.2 welcome detection + copy.
 *
 * Run with: npx tsx first-run.test.ts
 *
 * Verifies:
 *   - detectFirstRun returns true when file missing / empty / invalid JSON /
 *     parses but has no usable mnemonic.
 *   - detectFirstRun returns false when a valid credentials.json has either
 *     `mnemonic` or the legacy `recovery_phrase` alias.
 *   - buildWelcomePrepend emits the canonical copy with the correct
 *     mode-specific instructions.
 *   - The copy constants exactly match the canonical strings so the
 *     onboarding-cli + pair-page + first-run banner all speak the same
 *     language.
 *
 * TAP-style output, no jest dependency.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  detectFirstRun,
  buildWelcomePrepend,
  COPY,
  WELCOME,
  BRANCH_QUESTION,
  LOCAL_MODE_INSTRUCTIONS,
  REMOTE_MODE_INSTRUCTIONS,
  STORAGE_GUIDANCE,
  RESTORE_PROMPT,
  GENERATED_CONFIRMATION,
} from './first-run.js';

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
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-first-run-'));
}

// ---------------------------------------------------------------------------
// detectFirstRun
// ---------------------------------------------------------------------------

// Missing file → first run
{
  const dir = mkTmp();
  const credsPath = path.join(dir, 'credentials.json');
  const isFirst = await detectFirstRun(credsPath);
  assert(isFirst === true, 'detectFirstRun: returns true when file missing');
}

// Empty file → first run (invalid JSON)
{
  const dir = mkTmp();
  const credsPath = path.join(dir, 'credentials.json');
  fs.writeFileSync(credsPath, '');
  const isFirst = await detectFirstRun(credsPath);
  assert(isFirst === true, 'detectFirstRun: returns true when file is empty');
}

// Invalid JSON → first run
{
  const dir = mkTmp();
  const credsPath = path.join(dir, 'credentials.json');
  fs.writeFileSync(credsPath, '{ not valid json');
  const isFirst = await detectFirstRun(credsPath);
  assert(isFirst === true, 'detectFirstRun: returns true on invalid JSON');
}

// Valid JSON but no mnemonic → first run
{
  const dir = mkTmp();
  const credsPath = path.join(dir, 'credentials.json');
  fs.writeFileSync(credsPath, JSON.stringify({ userId: 'abc' }));
  const isFirst = await detectFirstRun(credsPath);
  assert(
    isFirst === true,
    'detectFirstRun: returns true when parsed JSON lacks mnemonic/recovery_phrase',
  );
}

// Valid JSON with empty mnemonic string → first run
{
  const dir = mkTmp();
  const credsPath = path.join(dir, 'credentials.json');
  fs.writeFileSync(credsPath, JSON.stringify({ mnemonic: '   ' }));
  const isFirst = await detectFirstRun(credsPath);
  assert(
    isFirst === true,
    'detectFirstRun: returns true when mnemonic field is whitespace-only',
  );
}

// Valid credentials (canonical `mnemonic` field) → NOT first run
{
  const dir = mkTmp();
  const credsPath = path.join(dir, 'credentials.json');
  fs.writeFileSync(
    credsPath,
    JSON.stringify({
      mnemonic: 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art',
    }),
  );
  const isFirst = await detectFirstRun(credsPath);
  assert(isFirst === false, 'detectFirstRun: returns false when canonical mnemonic present');
}

// Valid credentials (legacy `recovery_phrase` alias) → NOT first run
{
  const dir = mkTmp();
  const credsPath = path.join(dir, 'credentials.json');
  fs.writeFileSync(
    credsPath,
    JSON.stringify({
      recovery_phrase: 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art',
    }),
  );
  const isFirst = await detectFirstRun(credsPath);
  assert(
    isFirst === false,
    'detectFirstRun: returns false when legacy recovery_phrase alias present',
  );
}

// ---------------------------------------------------------------------------
// buildWelcomePrepend — mode=local
// ---------------------------------------------------------------------------

{
  const out = buildWelcomePrepend('local');
  assert(out.includes('## Welcome to TotalReclaw'), 'buildWelcomePrepend: includes section heading');
  assert(out.includes('Welcome to TotalReclaw — encrypted, agent-portable memory.'), 'buildWelcomePrepend: includes brand WELCOME line');
  assert(out.includes('OpenClaw, Hermes, or NanoClaw'), 'buildWelcomePrepend: mentions portable clients');
  assert(out.includes("Let's set up your account."), 'buildWelcomePrepend: includes BRANCH_QUESTION');
  assert(out.includes('openclaw plugin totalreclaw onboard restore'), 'buildWelcomePrepend local: restore command');
  assert(out.includes('openclaw plugin totalreclaw onboard generate'), 'buildWelcomePrepend local: generate command');
  assert(!out.includes('pair start'), 'buildWelcomePrepend local: does NOT include remote pair command');
  assert(out.includes('Your recovery phrase is 12 words.'), 'buildWelcomePrepend: includes STORAGE_GUIDANCE');
}

// ---------------------------------------------------------------------------
// buildWelcomePrepend — mode=remote
// ---------------------------------------------------------------------------

{
  const out = buildWelcomePrepend('remote');
  assert(out.includes('## Welcome to TotalReclaw'), 'buildWelcomePrepend remote: includes section heading');
  assert(out.includes('openclaw plugin totalreclaw pair start'), 'buildWelcomePrepend remote: pair command');
  assert(
    out.includes('browser page with a QR code'),
    'buildWelcomePrepend remote: explains QR flow',
  );
  assert(!out.includes('openclaw plugin totalreclaw onboard restore'), 'buildWelcomePrepend remote: does NOT include local restore command');
  assert(!out.includes('openclaw plugin totalreclaw onboard generate'), 'buildWelcomePrepend remote: does NOT include local generate command');
  assert(out.includes('Your recovery phrase is 12 words.'), 'buildWelcomePrepend remote: includes STORAGE_GUIDANCE');
}

// ---------------------------------------------------------------------------
// Canonical copy — exact-match substrings for cross-surface parity
// ---------------------------------------------------------------------------

{
  // These exact strings MUST match the canonical copy from the 3.3.0-rc.2 UX
  // spec. Any drift here means the CLI wizard, the browser page, and the
  // first-run banner have diverged — users will see inconsistent language.
  assert(
    WELCOME === COPY.WELCOME,
    'copy parity: WELCOME constant matches COPY.WELCOME',
  );
  assert(
    BRANCH_QUESTION === "Let's set up your account. Do you already have a recovery phrase, or should we generate a new one?",
    'copy parity: BRANCH_QUESTION canonical text',
  );
  assert(
    LOCAL_MODE_INSTRUCTIONS ===
      'If you have one, run: openclaw plugin totalreclaw onboard restore\n' +
      'If you need a new one, run: openclaw plugin totalreclaw onboard generate',
    'copy parity: LOCAL_MODE_INSTRUCTIONS canonical text',
  );
  assert(
    REMOTE_MODE_INSTRUCTIONS.startsWith('Run: openclaw plugin totalreclaw pair start\n'),
    'copy parity: REMOTE_MODE_INSTRUCTIONS starts with pair-start command',
  );
  assert(
    REMOTE_MODE_INSTRUCTIONS.includes('your recovery phrase never passes through the chat.'),
    'copy parity: REMOTE_MODE_INSTRUCTIONS ends with safety note',
  );
  assert(
    STORAGE_GUIDANCE ===
      'Your recovery phrase is 12 words. Store it somewhere safe — a password manager works well. Use it only for TotalReclaw. Don\'t reuse it anywhere else. Don\'t put funds on it.',
    'copy parity: STORAGE_GUIDANCE canonical text',
  );
  assert(
    RESTORE_PROMPT === 'Enter your 12-word recovery phrase to restore your account.',
    'copy parity: RESTORE_PROMPT canonical text',
  );
  assert(
    GENERATED_CONFIRMATION ===
      'A new recovery phrase has been generated. Write it down now, somewhere safe. This is the only way to restore your account later.',
    'copy parity: GENERATED_CONFIRMATION canonical text',
  );
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log(`# ${failed} FAILED`);
  process.exit(1);
}
console.log('\nALL TESTS PASSED');
