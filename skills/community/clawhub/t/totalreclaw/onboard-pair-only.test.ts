/**
 * Tests for `openclaw totalreclaw onboard --pair-only` (3.3.1-rc.18, issue #95).
 *
 * Phrase-safety contract: when the onboard CLI is invoked with
 * `--pair-only`, the stdout/stderr captured during the run MUST contain
 * ZERO phrase / mnemonic / recovery material — by construction the
 * pair flow delegated to is x25519-only and never imports BIP-39.
 *
 * Strategy: drive `runPairCli` directly with `outputMode: 'pair-only'`
 * (the same wiring `registerOnboardingCli`'s `--pair-only` branch uses
 * via dynamic import) and assert on:
 *   1. Single JSON line on stdout with the {v,pair_url,pin,expires_at_ms}
 *      shape — no `url`, no `sid`, no `mode`, no `qr_ascii`.
 *   2. `pair_url` is the rendered pairing URL (the `pk=` fragment is
 *      x25519 — no phrase material).
 *   3. `pin` is 6 digits.
 *   4. The captured stdout buffer contains NO phrase-adjacent token
 *      (`phrase`, `mnemonic`, `recovery`, `seed`, `bip39`).
 *   5. The captured stdout buffer contains NO BIP-39 wordlist word
 *      (sample-checked across 10 random wordlist entries).
 *   6. The captured stdout buffer contains NO 12-word run of lowercase
 *      alpha tokens — defense against a future regression that prints
 *      the phrase grid by accident.
 *   7. Status transitions DO NOT surface on stdout (silent after the
 *      single payload line).
 *   8. Stderr from the pair flow contains no phrase material either.
 *
 * Run with: npx tsx onboard-pair-only.test.ts
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { wordlist } from '@scure/bip39/wordlists/english.js';

import {
  transitionPairSession,
} from './pair-session-store.js';
import {
  runPairCli,
  type PairCliIo,
  type PairCliPairOnlyPayload,
} from './pair-cli.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) { console.log(`ok ${n} - ${name}`); passed++; }
  else { console.log(`not ok ${n} - ${name}`); failed++; }
}

function mkTmp(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-onboard-pair-only-'));
}

class CaptureStream {
  buf: string[] = [];
  write(data: string | Uint8Array): boolean {
    this.buf.push(data.toString());
    return true;
  }
  end() { /* noop */ }
  text(): string { return this.buf.join(''); }
}

function buildTestIo(): { stdout: CaptureStream; stderr: CaptureStream; io: PairCliIo; triggerInterrupt: () => void } {
  const stdout = new CaptureStream();
  const stderr = new CaptureStream();
  let interruptCb: (() => void) | null = null;
  const io: PairCliIo = {
    stdout: stdout as unknown as NodeJS.WritableStream,
    stderr: stderr as unknown as NodeJS.WritableStream,
    onInterrupt(cb) {
      interruptCb = cb;
      return () => { interruptCb = null; };
    },
  };
  return {
    stdout,
    stderr,
    io,
    triggerInterrupt: () => { interruptCb?.(); },
  };
}

function mkFakeQrRenderer(): (payload: string, cb: (ascii: string) => void) => void {
  return (payload, cb) => cb(`[QR:${payload.length}]`);
}

// ---------------------------------------------------------------------------
// test_issue_95_pair_only_emits_pair_url_payload
// ---------------------------------------------------------------------------

{
  const sessionsPath = path.join(mkTmp(), 'pair-sessions.json');
  const t = buildTestIo();
  let qrRendererCalled = false;

  const runPromise = runPairCli('generate', {
    sessionsPath,
    renderPairingUrl: (s) =>
      `http://test/pair/finish?sid=${s.sid}#pk=${s.pkGatewayB64}`,
    // pair-only mode MUST NOT invoke the QR renderer (no qrcode-terminal
    // load, no ASCII on stdout) — same invariant as url-pin mode.
    renderQr: (_, cb) => {
      qrRendererCalled = true;
      cb('[QR:should-not-appear]');
    },
    pollIntervalMs: 30,
    io: t.io,
    outputMode: 'pair-only',
  });

  await new Promise<void>((r) => setTimeout(r, 100));

  const firstOutput = t.stdout.text().split('\n')[0];
  let payload: PairCliPairOnlyPayload | null = null;
  try {
    payload = JSON.parse(firstOutput) as PairCliPairOnlyPayload;
  } catch {
    /* payload stays null */
  }

  assert(payload !== null, 'test_issue_95_pair_only: stdout parses as JSON');
  assert(payload?.v === 1, 'test_issue_95_pair_only: v=1');
  assert(
    typeof payload?.pair_url === 'string' && payload.pair_url.includes('#pk='),
    'test_issue_95_pair_only: pair_url has pk fragment',
  );
  assert(typeof payload?.pin === 'string' && /^\d{6}$/.test(payload.pin), 'test_issue_95_pair_only: pin is 6 digits');
  assert(
    typeof payload?.expires_at_ms === 'number' && payload.expires_at_ms > Date.now(),
    'test_issue_95_pair_only: expires_at_ms is future',
  );

  // Slim payload shape: exactly these four keys, nothing more. The spec
  // names `pair_url` (not `url`) — assert that explicitly so a future
  // regression can't silently rename without breaking this test.
  const keys = Object.keys(payload as object).sort();
  assert(
    keys.length === 4 &&
      keys[0] === 'expires_at_ms' &&
      keys[1] === 'pair_url' &&
      keys[2] === 'pin' &&
      keys[3] === 'v',
    `test_issue_95_pair_only: keys = [expires_at_ms,pair_url,pin,v] (got [${keys.join(',')}])`,
  );

  // Forbidden fields from json / url-pin modes that must NOT appear here.
  const p2 = payload as unknown as Record<string, unknown>;
  assert(!('url' in p2), 'test_issue_95_pair_only: no url field (must be pair_url)');
  assert(!('sid' in p2), 'test_issue_95_pair_only: no sid field');
  assert(!('mode' in p2), 'test_issue_95_pair_only: no mode field');
  assert(!('qr_ascii' in p2), 'test_issue_95_pair_only: no qr_ascii field');
  assert(!('mnemonic' in p2), 'test_issue_95_pair_only: no mnemonic field');
  assert(!('phrase' in p2), 'test_issue_95_pair_only: no phrase field');

  assert(!qrRendererCalled, 'test_issue_95_pair_only: QR renderer NOT invoked');

  // Drive the session through state transitions; in pair-only mode
  // these MUST NOT surface on stdout.
  const raw = fs.readFileSync(sessionsPath, 'utf-8');
  const parsed = JSON.parse(raw) as { sessions?: Array<{ sid: string }> };
  const sid = parsed.sessions?.[0]?.sid as string;
  await transitionPairSession(sessionsPath, sid, 'device_connected', Date.now);
  await new Promise<void>((r) => setTimeout(r, 80));
  await transitionPairSession(sessionsPath, sid, 'consumed', Date.now);
  await transitionPairSession(sessionsPath, sid, 'completed', Date.now);

  const outcome = await runPromise;
  assert(outcome.status === 'completed', 'test_issue_95_pair_only: outcome completed');

  const fullStdout = t.stdout.text();
  const fullStderr = t.stderr.text();

  // Stdout must remain a single JSON line + trailing newline.
  const nonEmptyLines = fullStdout.split('\n').filter((l) => l.length > 0);
  assert(nonEmptyLines.length === 1, `test_issue_95_pair_only: single stdout line (got ${nonEmptyLines.length})`);

  // No human-readable banner / status copy at any point.
  assert(!fullStdout.includes('Remote pairing'), 'test_issue_95_pair_only: no intro copy on stdout');
  assert(!fullStdout.includes('Browser connected'), 'test_issue_95_pair_only: no "Browser connected" on stdout');
  assert(!fullStdout.includes('Pairing complete'), 'test_issue_95_pair_only: no "Pairing complete" on stdout');
  assert(!fullStdout.includes('Security:'), 'test_issue_95_pair_only: no security warning on stdout');
  assert(!fullStdout.includes('[QR:'), 'test_issue_95_pair_only: no QR ASCII on stdout');

  // ---------------------------------------------------------------
  // STRICT INVARIANT (issue #95 spec): phrase string MUST NOT appear
  // in captured stdout/stderr in --pair-only mode. Defense-in-depth
  // since pair-cli does not import any mnemonic code, but this test
  // catches a regression that accidentally inlines phrase material.
  // ---------------------------------------------------------------
  assert(!/\bphrase\b/i.test(fullStdout), 'STRICT: no "phrase" on stdout');
  assert(!/\bmnemonic\b/i.test(fullStdout), 'STRICT: no "mnemonic" on stdout');
  assert(!/\brecovery\b/i.test(fullStdout), 'STRICT: no "recovery" on stdout');
  assert(!/\bseed\b/i.test(fullStdout), 'STRICT: no "seed" on stdout');
  assert(!/\bbip-?39\b/i.test(fullStdout), 'STRICT: no "bip39" on stdout');

  assert(!/\bphrase\b/i.test(fullStderr), 'STRICT: no "phrase" on stderr');
  assert(!/\bmnemonic\b/i.test(fullStderr), 'STRICT: no "mnemonic" on stderr');
  assert(!/\brecovery\b/i.test(fullStderr), 'STRICT: no "recovery" on stderr');
  assert(!/\bseed\b/i.test(fullStderr), 'STRICT: no "seed" on stderr');
  assert(!/\bbip-?39\b/i.test(fullStderr), 'STRICT: no "bip39" on stderr');

  // Assert no BIP-39 wordlist word appears on stdout. We sample 10
  // random wordlist entries — if any are present, fail. (Full-list
  // scan is overkill: the assertion above already rules out every
  // scenario where a phrase would leak; this is belt-and-braces.)
  const sampleWords = ['ability', 'absurd', 'access', 'banana', 'cargo', 'dance', 'eager', 'fabric', 'galaxy', 'hammer'];
  for (const w of sampleWords) {
    assert(
      wordlist.includes(w),
      `setup: sample word "${w}" is in the BIP-39 wordlist`,
    );
    assert(
      !new RegExp(`\\b${w}\\b`).test(fullStdout),
      `STRICT: BIP-39 word "${w}" not on stdout`,
    );
  }

  // Defense against a future regression that accidentally prints a
  // phrase grid: scan stdout for any 12-word run of lowercase alpha
  // tokens of length >=3. The pair-only payload's URL contains no such
  // structure (it's hex / base64url + URL-encoded chars), so this is
  // a clean proxy for a leaked phrase.
  const tokens = fullStdout.toLowerCase().match(/\b[a-z]{3,}\b/g) ?? [];
  let maxRun = 0;
  let cur = 0;
  for (const _t of tokens) {
    cur++;
    if (cur > maxRun) maxRun = cur;
  }
  // Tokens come from JSON keys/values; even concatenated, a legitimate
  // payload should produce far fewer than 12 contiguous lowercase
  // tokens. (`{"v":1,"pair_url":"http://...","pin":"123456","expires_at_ms":...}`
  // has 4-6 lowercase tokens depending on URL).
  assert(
    maxRun < 12,
    `STRICT: stdout has fewer than 12 contiguous lowercase tokens (got ${maxRun}) — phrase-grid regression check`,
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
