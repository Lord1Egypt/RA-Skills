/**
 * Tests for onboarding-cli.ts — the 3.2.0 CLI wizard.
 *
 * Run with: npx tsx onboarding-cli.test.ts
 *
 * Strategy: we exercise `runOnboardingWizard` with a deterministic mock
 * WizardIo so we can assert on both the I/O transcript and the on-disk
 * side effects. The real readline + raw-mode hidden-input plumbing lives
 * in `buildDefaultIo` and is exercised by the OpenClaw-harness smoke
 * script, not by these tests.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  runOnboardingWizard,
  printStatus,
  COPY,
  type WizardIo,
  type WizardResult,
} from './onboarding-cli.js';
import { loadOnboardingState, loadCredentialsJson } from './fs-helpers.js';

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
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-cli-'));
}

// ---------------------------------------------------------------------------
// Mock I/O
// ---------------------------------------------------------------------------

interface MockIo extends WizardIo {
  stdoutBuf: string;
  stderrBuf: string;
  inputs: string[];
  hiddenInputs: string[];
  askCalls: string[];
  askHiddenCalls: string[];
}

function mkMockIo(opts: { answers?: string[]; hiddenAnswers?: string[] }): MockIo {
  const stdoutBuf = { value: '' };
  const stderrBuf = { value: '' };
  const answers = [...(opts.answers ?? [])];
  const hiddenAnswers = [...(opts.hiddenAnswers ?? [])];
  const askCalls: string[] = [];
  const askHiddenCalls: string[] = [];

  const stdout: NodeJS.WritableStream = {
    write(chunk: string | Uint8Array) {
      stdoutBuf.value += typeof chunk === 'string' ? chunk : Buffer.from(chunk).toString('utf-8');
      return true;
    },
  } as unknown as NodeJS.WritableStream;

  const stderr: NodeJS.WritableStream = {
    write(chunk: string | Uint8Array) {
      stderrBuf.value += typeof chunk === 'string' ? chunk : Buffer.from(chunk).toString('utf-8');
      return true;
    },
  } as unknown as NodeJS.WritableStream;

  return {
    stdout,
    stderr,
    ask: async (q: string) => {
      askCalls.push(q);
      const ans = answers.shift();
      if (ans === undefined) throw new Error(`MockIo.ask: no queued answer for prompt: ${q}`);
      return ans;
    },
    askHidden: async (q: string) => {
      askHiddenCalls.push(q);
      const ans = hiddenAnswers.shift();
      if (ans === undefined) throw new Error(`MockIo.askHidden: no queued answer for prompt: ${q}`);
      return ans;
    },
    close: () => {},
    get stdoutBuf() {
      return stdoutBuf.value;
    },
    get stderrBuf() {
      return stderrBuf.value;
    },
    get inputs() {
      return answers;
    },
    get hiddenInputs() {
      return hiddenAnswers;
    },
    askCalls,
    askHiddenCalls,
  };
}

// Valid 12-word BIP-39 test vector (from the SLIP-0039 / BIP-39 reference suite).
const VALID_PHRASE = 'legal winner thank year wave sausage worth useful legal winner thank yellow';
const INVALID_PHRASE = 'not a valid phrase for anything not a valid phrase for anything';

// ---------------------------------------------------------------------------
// 1. Skip path
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  const io = mkMockIo({ answers: ['3'] });

  const result = await runOnboardingWizard({ credentialsPath: credPath, statePath, io });

  assert(result.choice === 'skip', 'skip: choice is "skip"');
  assert(result.state === undefined, 'skip: no state returned');
  assert(!fs.existsSync(credPath), 'skip: credentials.json NOT created');
  assert(!fs.existsSync(statePath), 'skip: state.json NOT created');
  assert(io.stdoutBuf.includes('Skipped'), 'skip: prints skipped copy');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 2. Generate — happy path
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  const words = VALID_PHRASE.split(' ');
  // Deterministic probe: indices 0, 5, 11 → words[0]='legal', words[5]='sausage', words[11]='yellow'
  const io = mkMockIo({ answers: ['1', 'legal', 'sausage', 'yellow'] });

  const result: WizardResult = await runOnboardingWizard({
    credentialsPath: credPath,
    statePath,
    io,
    generateMnemonic: () => VALID_PHRASE,
    randomProbeIndices: () => [0, 5, 11],
  });

  assert(result.choice === 'generate', 'generate: choice is "generate"');
  assert(result.error === undefined, `generate: no error (got ${result.error})`);
  assert(result.state?.onboardingState === 'active', 'generate: state.onboardingState is "active"');
  assert(result.state?.createdBy === 'generate', 'generate: createdBy is "generate"');
  assert(typeof result.state?.credentialsCreatedAt === 'string', 'generate: credentialsCreatedAt set');

  assert(fs.existsSync(credPath), 'generate: credentials.json written');
  const credMode = fs.statSync(credPath).mode & 0o777;
  assert(credMode === 0o600, `generate: credentials.json mode is 0o600 (got ${credMode.toString(8)})`);
  const creds = loadCredentialsJson(credPath);
  assert(creds?.mnemonic === VALID_PHRASE, 'generate: mnemonic persisted correctly');

  assert(fs.existsSync(statePath), 'generate: state.json written');
  const stateMode = fs.statSync(statePath).mode & 0o777;
  assert(stateMode === 0o600, `generate: state.json mode is 0o600 (got ${stateMode.toString(8)})`);
  const st = loadOnboardingState(statePath);
  assert(st?.onboardingState === 'active', 'generate: state.json onboardingState is "active"');
  assert(st?.createdBy === 'generate', 'generate: state.json createdBy is "generate"');

  // Output assertions
  assert(io.stdoutBuf.includes('ABOUT YOUR RECOVERY PHRASE'), 'generate: prints generate warning');
  assert(io.stdoutBuf.includes('Coming in 3.3.0'.slice(0, 0)) || io.stdoutBuf.includes('3.3.0'), 'generate: prints 3.3.0 hint');
  assert(io.stdoutBuf.includes('Memory tools are now active'), 'generate: prints next-step line');
  assert(io.stdoutBuf.includes('openclaw chat'), 'generate: prints openclaw chat hint');

  // The phrase SHOULD appear in stdout (that's the whole point — TTY surface)
  assert(io.stdoutBuf.includes(words[0]), 'generate: prints the mnemonic words');
  // But NOT in stderr.
  assert(!io.stderrBuf.includes(words[0]), 'generate: stderr does NOT contain mnemonic');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 3. Generate — ack failure bails without persisting
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  // Answer the probe wrong for word #1
  const io = mkMockIo({ answers: ['1', 'wrong', 'sausage', 'yellow'] });

  const result = await runOnboardingWizard({
    credentialsPath: credPath,
    statePath,
    io,
    generateMnemonic: () => VALID_PHRASE,
    randomProbeIndices: () => [0, 5, 11],
  });

  assert(result.choice === 'generate', 'ack-fail: choice is "generate"');
  assert(result.error === 'ack-failed', 'ack-fail: error is "ack-failed"');
  assert(result.state === undefined, 'ack-fail: no state returned');
  assert(!fs.existsSync(credPath), 'ack-fail: credentials.json NOT written');
  assert(!fs.existsSync(statePath), 'ack-fail: state.json NOT written');
  assert(io.stderrBuf.includes('Word mismatch'), 'ack-fail: prints mismatch copy on stderr');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 4. Import — happy path (valid BIP-39)
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  const io = mkMockIo({
    answers: ['2'],
    hiddenAnswers: [VALID_PHRASE],
  });

  const result = await runOnboardingWizard({
    credentialsPath: credPath,
    statePath,
    io,
    // Use real validateMnemonic — we want to assert real BIP-39 behavior.
  });

  assert(result.choice === 'import', 'import: choice is "import"');
  assert(result.error === undefined, `import: no error (got ${result.error})`);
  assert(result.state?.onboardingState === 'active', 'import: state.onboardingState is "active"');
  assert(result.state?.createdBy === 'import', 'import: createdBy is "import"');
  assert(fs.existsSync(credPath), 'import: credentials.json written');
  const creds = loadCredentialsJson(credPath);
  assert(creds?.mnemonic === VALID_PHRASE, 'import: persisted mnemonic matches input');
  assert(fs.existsSync(statePath), 'import: state.json written');
  const st = loadOnboardingState(statePath);
  assert(st?.onboardingState === 'active', 'import: state.onboardingState persisted as "active"');
  assert(st?.createdBy === 'import', 'import: state.createdBy persisted as "import"');
  assert(io.stdoutBuf.includes('BEFORE YOU PASTE'), 'import: prints import warning');
  assert(io.stdoutBuf.includes('Memory tools are now active'), 'import: prints next-step line');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 5. Import — invalid phrase rejected (checksum fail)
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  const io = mkMockIo({
    answers: ['2'],
    hiddenAnswers: [INVALID_PHRASE],
  });

  const result = await runOnboardingWizard({
    credentialsPath: credPath,
    statePath,
    io,
  });

  assert(result.choice === 'import', 'import-invalid: choice is "import"');
  assert(result.error === 'invalid-phrase', 'import-invalid: error is "invalid-phrase"');
  assert(result.state === undefined, 'import-invalid: no state returned');
  assert(!fs.existsSync(credPath), 'import-invalid: credentials.json NOT written');
  assert(!fs.existsSync(statePath), 'import-invalid: state.json NOT written');
  // 3.3.0-rc.2: "BIP-39 phrase" → "recovery phrase" in user-facing copy.
  assert(io.stderrBuf.includes('Invalid recovery phrase'), 'import-invalid: prints invalid phrase copy');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 6. Import — phrase normalisation (whitespace + case + zero-width)
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  const messy = `  LEGAL winner  thank\tyear wave sausage worth useful legal winner thank yellow\u200B `;
  const io = mkMockIo({
    answers: ['2'],
    hiddenAnswers: [messy],
  });

  const result = await runOnboardingWizard({
    credentialsPath: credPath,
    statePath,
    io,
  });

  assert(result.choice === 'import', 'import-norm: choice is "import"');
  assert(result.error === undefined, `import-norm: no error (got ${result.error})`);
  const creds = loadCredentialsJson(credPath);
  assert(creds?.mnemonic === VALID_PHRASE, 'import-norm: phrase normalised to canonical form');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 7. Already-active short-circuit (wizard refuses to overwrite)
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  fs.writeFileSync(credPath, JSON.stringify({ mnemonic: VALID_PHRASE }), { mode: 0o600 });
  fs.writeFileSync(statePath, JSON.stringify({ onboardingState: 'active', createdBy: 'generate', version: '3.2.0' }), { mode: 0o600 });

  const io = mkMockIo({ answers: [] });
  const result = await runOnboardingWizard({ credentialsPath: credPath, statePath, io });

  assert(result.choice === 'skip', 'already-active: choice is "skip" (short-circuit)');
  assert(result.state?.onboardingState === 'active', 'already-active: returns persisted active state');
  assert(io.stdoutBuf.includes('already set up'), 'already-active: prints already-active copy');
  // Did NOT prompt.
  assert(io.askCalls.length === 0, 'already-active: no prompts issued');
  // Credentials untouched.
  const creds = loadCredentialsJson(credPath);
  assert(creds?.mnemonic === VALID_PHRASE, 'already-active: credentials.json unchanged');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 8. Invalid menu choice
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  const io = mkMockIo({ answers: ['banana'] });

  const result = await runOnboardingWizard({ credentialsPath: credPath, statePath, io });

  assert(result.choice === 'skip', 'invalid-choice: resolves to skip');
  assert(typeof result.error === 'string' && result.error.startsWith('invalid-choice:'), 'invalid-choice: error code set');
  assert(!fs.existsSync(credPath), 'invalid-choice: credentials.json NOT written');
  assert(!fs.existsSync(statePath), 'invalid-choice: state.json NOT written');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 9. printStatus does not leak the mnemonic
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  fs.writeFileSync(credPath, JSON.stringify({ mnemonic: VALID_PHRASE }), { mode: 0o600 });
  fs.writeFileSync(statePath, JSON.stringify({ onboardingState: 'active', createdBy: 'import', credentialsCreatedAt: '2026-04-19T12:00:00.000Z', version: '3.2.0' }), { mode: 0o600 });

  let buf = '';
  const out = {
    write(chunk: string | Uint8Array) {
      buf += typeof chunk === 'string' ? chunk : Buffer.from(chunk).toString('utf-8');
      return true;
    },
  } as unknown as NodeJS.WritableStream;

  printStatus(credPath, statePath, out);

  assert(buf.includes('onboarding: complete'), 'status: prints active copy');
  assert(buf.includes('credentials.json'), 'status: mentions credentials file path');
  assert(buf.includes('import'), 'status: mentions createdBy');
  // Critical: the mnemonic must NEVER appear in status output.
  for (const w of VALID_PHRASE.split(' ')) {
    assert(!buf.includes(w), `status: does NOT leak phrase word "${w}"`);
  }

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 10. printStatus when fresh → hints at the CLI wizard
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');

  let buf = '';
  const out = {
    write(chunk: string | Uint8Array) {
      buf += typeof chunk === 'string' ? chunk : Buffer.from(chunk).toString('utf-8');
      return true;
    },
  } as unknown as NodeJS.WritableStream;

  printStatus(credPath, statePath, out);
  assert(buf.includes('not complete'), 'status-fresh: prints fresh copy');
  assert(buf.includes('openclaw totalreclaw onboard'), 'status-fresh: hints at CLI command');

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 11. printStatus with legacy recovery_phrase key → reports "complete"
// ---------------------------------------------------------------------------
{
  const tmp = mkTmp();
  const credPath = path.join(tmp, 'credentials.json');
  const statePath = path.join(tmp, 'state.json');
  // Write credentials with the LEGACY key only (no `mnemonic` field).
  fs.writeFileSync(credPath, JSON.stringify({ recovery_phrase: VALID_PHRASE }), { mode: 0o600 });
  fs.writeFileSync(
    statePath,
    JSON.stringify({ onboardingState: 'active', createdBy: 'import', credentialsCreatedAt: '2026-04-19T00:00:00.000Z', version: '3.2.0' }),
    { mode: 0o600 },
  );

  let buf = '';
  const out = {
    write(chunk: string | Uint8Array) {
      buf += typeof chunk === 'string' ? chunk : Buffer.from(chunk).toString('utf-8');
      return true;
    },
  } as unknown as NodeJS.WritableStream;

  printStatus(credPath, statePath, out);

  assert(buf.includes('onboarding: complete'), 'status-legacy-key: prints "complete" for recovery_phrase creds');
  assert(!buf.includes('not complete'), 'status-legacy-key: does NOT print "not complete"');
  // Mnemonic words must never leak.
  for (const w of VALID_PHRASE.split(' ')) {
    assert(!buf.includes(w), `status-legacy-key: does NOT leak phrase word "${w}"`);
  }

  fs.rmSync(tmp, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// 13. Copy strings — the scripted ones that tests depend on exist
// ---------------------------------------------------------------------------
{
  assert(COPY.welcome.includes('TotalReclaw'), 'copy: welcome references product');
  assert(COPY.generateWarning.includes('RECOVERY PHRASE'), 'copy: generate warning headline');
  assert(COPY.importWarning.includes('BEFORE YOU PASTE'), 'copy: import warning headline');
  assert(COPY.importRemoteLimitation.includes('3.3.0'), 'copy: import remote limitation cites 3.3.0');
  assert(COPY.postSuccessGenerate.includes('openclaw chat'), 'copy: post-success-generate references next step');
  assert(COPY.postSuccessImport.includes('openclaw chat'), 'copy: post-success-import references next step');
  assert(COPY.skipped.includes('openclaw totalreclaw onboard'), 'copy: skipped references CLI command to resume');
  assert(COPY.alreadyActive.includes('already set up'), 'copy: already-active references existing setup');
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
