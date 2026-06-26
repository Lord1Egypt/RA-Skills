/**
 * Tests for 3.3.1 pair-cli JSON mode + 3.3.1-rc.15 url-pin mode (issue #87).
 *
 * Covers:
 *   - outputMode: 'json' emits a single line of valid JSON to stdout
 *   - JSON payload contains sid, url, pin, qr_ascii, expires_at_ms
 *   - JSON mode never prints the human-readable intro / security warning
 *   - ttlSeconds is propagated to the pair session's expiresAtMs
 *   - test_issue_87_url_pin_only_emits_slim_payload: url-pin mode emits
 *     ONLY {v,url,pin,expires_at_ms}, skips QR rendering, stays silent
 *     on status transitions, and has no phrase-adjacent material.
 *
 * Run with: npx tsx pair-cli-json.test.ts
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  transitionPairSession,
  getPairSession,
} from './pair-session-store.js';
import { runPairCli, type PairCliIo, type PairCliJsonPayload, type PairCliUrlPinPayload } from './pair-cli.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) { console.log(`ok ${n} - ${name}`); passed++; }
  else { console.log(`not ok ${n} - ${name}`); failed++; }
}

function mkTmp(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-json-'));
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
// JSON mode emits a single well-formed JSON line
// ---------------------------------------------------------------------------

{
  const sessionsPath = path.join(mkTmp(), 'pair-sessions.json');
  const t = buildTestIo();

  // Start the CLI + immediately drive the session to 'completed' so it
  // terminates deterministically.
  const runPromise = runPairCli('generate', {
    sessionsPath,
    renderPairingUrl: (s) => `http://test/pair/finish?sid=${s.sid}#pk=${s.pkGatewayB64}`,
    renderQr: mkFakeQrRenderer(),
    pollIntervalMs: 50,
    io: t.io,
    outputMode: 'json',
    ttlSeconds: 600,
  });

  // The first emitted line should be JSON with the payload. Wait a tick,
  // then mark the session completed so the poll loop returns.
  await new Promise<void>((r) => setTimeout(r, 100));

  // Parse the first stdout chunk as JSON (the payload line).
  const firstOutput = t.stdout.text().split('\n')[0];
  let payload: PairCliJsonPayload | null = null;
  try {
    payload = JSON.parse(firstOutput) as PairCliJsonPayload;
  } catch {
    /* payload stays null */
  }
  assert(payload !== null, 'json: first stdout chunk parses as JSON');
  assert(payload?.v === 1, 'json: payload.v === 1');
  assert(typeof payload?.sid === 'string' && /^[0-9a-f]{32}$/.test(payload.sid), 'json: sid is 32-hex');
  assert(
    typeof payload?.url === 'string' && payload.url.startsWith('http://test/pair/finish?sid='),
    'json: url is the rendered pairing URL',
  );
  assert(typeof payload?.pin === 'string' && /^\d{6}$/.test(payload.pin), 'json: pin is 6 digits');
  assert(typeof payload?.expires_at_ms === 'number' && payload.expires_at_ms > Date.now(), 'json: expires_at_ms in future');
  assert(typeof payload?.qr_ascii === 'string' && payload.qr_ascii.includes('[QR:'), 'json: qr_ascii populated');
  assert(payload?.mode === 'generate', 'json: mode echoed');

  // ttlSeconds=600 means expiresAtMs - now() should be close to 600_000.
  const delta = (payload?.expires_at_ms ?? 0) - Date.now();
  assert(delta > 590_000 && delta < 610_000, `json: ttlSeconds=600 honoured (delta=${delta}ms)`);

  // Verify human-readable copy is NOT on stdout.
  assert(
    !t.stdout.text().includes('TotalReclaw — Remote pairing'),
    'json: no human-readable intro leaked to stdout',
  );
  assert(
    !t.stdout.text().includes('Security:'),
    'json: no security warning copy leaked to stdout',
  );

  // Drive the session to completed so runPairCli can return.
  await transitionPairSession(sessionsPath, payload!.sid, 'device_connected', Date.now);
  await transitionPairSession(sessionsPath, payload!.sid, 'consumed', Date.now);
  await transitionPairSession(sessionsPath, payload!.sid, 'completed', Date.now);

  const outcome = await runPromise;
  assert(outcome.status === 'completed', 'json: runPairCli returns completed');
}

// ---------------------------------------------------------------------------
// Human mode still emits the banner (regression guard — do not break pre-3.3.1 UX)
// ---------------------------------------------------------------------------

{
  const sessionsPath = path.join(mkTmp(), 'pair-sessions.json');
  const t = buildTestIo();
  const runPromise = runPairCli('generate', {
    sessionsPath,
    renderPairingUrl: (s) => `http://test/pair/finish?sid=${s.sid}`,
    renderQr: mkFakeQrRenderer(),
    pollIntervalMs: 50,
    io: t.io,
    outputMode: 'human',
  });
  await new Promise<void>((r) => setTimeout(r, 100));

  const text = t.stdout.text();
  assert(text.includes('TotalReclaw — Remote pairing'), 'human: intro copy present');
  assert(text.includes('Secondary code (type this into the browser):'), 'human: code label present');
  assert(text.includes('Security:'), 'human: security warning present');

  // Find session by reading sessions file.
  const raw = fs.readFileSync(sessionsPath, 'utf-8');
  const parsed = JSON.parse(raw) as { sessions?: Array<{ sid: string }> };
  const sid = parsed.sessions?.[0]?.sid;
  assert(typeof sid === 'string', 'human: session exists in store');

  // Cancel via Ctrl+C to terminate the poll loop.
  t.triggerInterrupt();
  await new Promise<void>((r) => setTimeout(r, 200));
  const outcome = await runPromise;
  assert(outcome.status === 'canceled', 'human: canceled outcome on interrupt');
}

// ---------------------------------------------------------------------------
// test_issue_87_url_pin_only_emits_slim_payload
//
// Headless container-agent fallback: when `totalreclaw_pair` tool is
// missing from the agent's tool list (OpenClaw gateway-to-container
// tool-injection gap), the agent shells out to
// `openclaw totalreclaw pair generate --url-pin-only`. This mode MUST:
//   - Emit ONLY {v,url,pin,expires_at_ms} on stdout — no qr_ascii,
//     no sid, no mode echo, no banner, no spinner.
//   - Skip QR rendering entirely (no CPU cost, no qrcode-terminal load).
//   - Stay silent on status transitions (device_connected, completed).
//   - Carry zero phrase-adjacent material on stdout (defense-in-depth
//     check — pair-crypto is x25519-only and never imports BIP-39).
// ---------------------------------------------------------------------------

{
  const sessionsPath = path.join(mkTmp(), 'pair-sessions.json');
  const t = buildTestIo();
  let qrRendererCalled = false;

  const runPromise = runPairCli('generate', {
    sessionsPath,
    renderPairingUrl: (s) =>
      `http://test/pair/finish?sid=${s.sid}#pk=${s.pkGatewayB64}`,
    // If url-pin mode accidentally invokes the QR renderer, flip this
    // and the test fails — url-pin mode MUST skip QR rendering.
    renderQr: (_, cb) => {
      qrRendererCalled = true;
      cb('[QR:should-not-appear]');
    },
    pollIntervalMs: 30,
    io: t.io,
    outputMode: 'url-pin',
  });

  await new Promise<void>((r) => setTimeout(r, 100));

  const firstOutput = t.stdout.text().split('\n')[0];
  let payload: PairCliUrlPinPayload | null = null;
  try {
    payload = JSON.parse(firstOutput) as PairCliUrlPinPayload;
  } catch {
    /* payload stays null */
  }
  assert(payload !== null, 'test_issue_87_url_pin_only: stdout parses as JSON');
  assert(payload?.v === 1, 'test_issue_87_url_pin_only: v=1');
  assert(typeof payload?.url === 'string' && payload.url.includes('#pk='), 'test_issue_87_url_pin_only: url has pk fragment');
  assert(typeof payload?.pin === 'string' && /^\d{6}$/.test(payload.pin), 'test_issue_87_url_pin_only: pin is 6 digits');
  assert(typeof payload?.expires_at_ms === 'number' && payload.expires_at_ms > Date.now(), 'test_issue_87_url_pin_only: expires_at_ms is future');

  // Slim payload shape: exactly these four keys, nothing more.
  const keys = Object.keys(payload as object).sort();
  assert(
    keys.length === 4 &&
      keys[0] === 'expires_at_ms' &&
      keys[1] === 'pin' &&
      keys[2] === 'url' &&
      keys[3] === 'v',
    `test_issue_87_url_pin_only: keys = [expires_at_ms,pin,url,v] (got [${keys.join(',')}])`,
  );
  // Forbidden fields from the json mode that must NOT appear here.
  const p2 = payload as unknown as Record<string, unknown>;
  assert(!('sid' in p2), 'test_issue_87_url_pin_only: no sid field');
  assert(!('mode' in p2), 'test_issue_87_url_pin_only: no mode field');
  assert(!('qr_ascii' in p2), 'test_issue_87_url_pin_only: no qr_ascii field');

  assert(!qrRendererCalled, 'test_issue_87_url_pin_only: QR renderer NOT invoked');

  // Drive the session through state transitions; in url-pin mode these
  // must NOT surface on stdout.
  const raw = fs.readFileSync(sessionsPath, 'utf-8');
  const parsed = JSON.parse(raw) as { sessions?: Array<{ sid: string }> };
  const sid = parsed.sessions?.[0]?.sid as string;
  await transitionPairSession(sessionsPath, sid, 'device_connected', Date.now);
  await new Promise<void>((r) => setTimeout(r, 80));
  await transitionPairSession(sessionsPath, sid, 'consumed', Date.now);
  await transitionPairSession(sessionsPath, sid, 'completed', Date.now);

  const outcome = await runPromise;
  assert(outcome.status === 'completed', 'test_issue_87_url_pin_only: outcome completed');

  const fullText = t.stdout.text();

  // Stdout must remain a single JSON line + trailing newline.
  const nonEmptyLines = fullText.split('\n').filter((l) => l.length > 0);
  assert(nonEmptyLines.length === 1, `test_issue_87_url_pin_only: single stdout line (got ${nonEmptyLines.length})`);

  // No human-readable banner / status copy at any point.
  assert(!fullText.includes('Remote pairing'), 'test_issue_87_url_pin_only: no intro copy leaked');
  assert(!fullText.includes('Browser connected'), 'test_issue_87_url_pin_only: no "Browser connected" copy');
  assert(!fullText.includes('Pairing complete'), 'test_issue_87_url_pin_only: no "Pairing complete" copy');
  assert(!fullText.includes('Security:'), 'test_issue_87_url_pin_only: no security warning copy');
  assert(!fullText.includes('[QR:'), 'test_issue_87_url_pin_only: no QR ASCII on stdout');

  // Defense-in-depth: phrase-adjacent tokens must never surface on
  // stdout — pair-cli does not import any mnemonic code, so these
  // assertions can only fail if a regression accidentally inlines them.
  assert(!/\bphrase\b/i.test(fullText), 'test_issue_87_url_pin_only: no "phrase" on stdout');
  assert(!/\bmnemonic\b/i.test(fullText), 'test_issue_87_url_pin_only: no "mnemonic" on stdout');
  assert(!/\brecovery\b/i.test(fullText), 'test_issue_87_url_pin_only: no "recovery" on stdout');
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
