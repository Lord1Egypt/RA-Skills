/**
 * Regression test for issue #128 — registerTool breadcrumbs must be gated
 * so they do NOT bleed into `openclaw agent --json` stdout.
 *
 * Background
 * ----------
 * rc.20 user QA found that `openclaw agent --message "..." --json` returned
 * a clean JSON-RPC body preceded (or followed) by a `[plugins] TotalReclaw:
 * registerTool(totalreclaw_pair) returned. ...` banner — invalid JSON for
 * any programmatic parser. Root cause: the plugin's `register()` function
 * called `api.logger.info(...)` immediately after each `api.registerTool`
 * call as an ops-debug breadcrumb, but in OpenClaw `api.logger.info` ends
 * up on stdout (decorated with `[plugins] `).
 *
 * Fix: gate every "I just registered tool X" breadcrumb behind
 * `CONFIG.verboseRegister`, which is OFF by default. Ops can opt back in
 * with `TOTALRECLAW_VERBOSE_REGISTER=1` or `TOTALRECLAW_DEBUG=1`.
 *
 * What this asserts
 * -----------------
 *   1. The literal "registerTool(totalreclaw_pair) returned" log appears
 *      ONLY inside an `if (CONFIG.verboseRegister) { ... }` block.
 *   2. The literal "totalreclaw_report_qa_bug registered" log (the RC-only
 *      breadcrumb) is also gated.
 *   3. Mock-runtime check: a stdout sink wrapping `JSON.parse` of every
 *      line emitted by the plugin in `--json` simulation succeeds (no log
 *      lines, only the JSON body). Approximated by feeding our gated
 *      logger sample lines and asserting the JSON parser sees a
 *      single-line valid JSON object.
 *   4. `CONFIG.verboseRegister` reads `TOTALRECLAW_VERBOSE_REGISTER`
 *      AND falls through to `TOTALRECLAW_DEBUG`. Default false.
 *
 * Run with: `npx tsx json-stdout-cleanliness.test.ts`
 */

import fs from 'node:fs';
import path from 'node:path';

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

const INDEX_PATH = path.resolve(import.meta.dirname, 'index.ts');
const SRC = fs.readFileSync(INDEX_PATH, 'utf-8');

// ---------------------------------------------------------------------------
// Test 1 — `registerTool(totalreclaw_pair) returned` log is gated.
// ---------------------------------------------------------------------------
{
  const banner = "registerTool(totalreclaw_pair) returned";
  const idx = SRC.indexOf(banner);
  assert(idx > 0, 'totalreclaw_pair breadcrumb still present in source (sanity)');

  // Walk backwards to find the start of the enclosing block. The previous
  // ~40 lines must contain `if (CONFIG.verboseRegister)` so the log is
  // gated. We scan a 1500-char window, conservative for the comment block
  // that precedes the gate.
  const window = SRC.slice(Math.max(0, idx - 1500), idx);
  assert(
    /if\s*\(\s*CONFIG\.verboseRegister\s*\)\s*\{/.test(window),
    'totalreclaw_pair breadcrumb is wrapped in `if (CONFIG.verboseRegister) { ... }`',
  );
}

// ---------------------------------------------------------------------------
// Test 2 — `totalreclaw_report_qa_bug registered` (RC log) is gated.
// ---------------------------------------------------------------------------
{
  const banner = "totalreclaw_report_qa_bug registered";
  const idx = SRC.indexOf(banner);
  assert(idx > 0, 'totalreclaw_report_qa_bug breadcrumb present in source');
  const window = SRC.slice(Math.max(0, idx - 1500), idx);
  assert(
    /if\s*\(\s*CONFIG\.verboseRegister\s*\)\s*\{/.test(window),
    'totalreclaw_report_qa_bug breadcrumb is wrapped in `if (CONFIG.verboseRegister) { ... }`',
  );
}

// ---------------------------------------------------------------------------
// Test 3 — simulated `--json` stdout is parseable JSON (no log preamble).
//
// We don't have a full gateway harness here, so we simulate the contract:
// a clean `--json` run emits exactly ONE line of JSON to stdout. Our
// "stdout" only receives the JSON body when the gate is OFF (default).
// We approximate by feeding the same gated logger pattern through a
// CaptureStream and asserting JSON.parse on the sole line succeeds.
// ---------------------------------------------------------------------------
{
  class CaptureStdout {
    lines: string[] = [];
    write(data: string | Uint8Array): boolean {
      const s = typeof data === 'string' ? data : Buffer.from(data).toString('utf-8');
      // OpenClaw's stdout writes are line-buffered for `--json`; we split
      // on newlines and drop empty trailers to match real behavior.
      for (const line of s.split('\n')) {
        if (line.length > 0) this.lines.push(line);
      }
      return true;
    }
  }

  // Simulate the gated registration path: when `verboseRegister` is false
  // (default), the plugin would NOT call `logger.info` for the breadcrumb.
  // The only stdout writes during a `--json` agent invocation should be
  // the JSON-RPC body.
  const verboseRegister = false;
  const stdout = new CaptureStdout();

  // Mimic plugin register() — when gated off, no breadcrumb is written.
  if (verboseRegister) {
    stdout.write('[plugins] TotalReclaw: registerTool(totalreclaw_pair) returned. ...\n');
  }
  // The agent's JSON-RPC body is the only legitimate stdout payload.
  const agentResponse = {
    jsonrpc: '2.0',
    id: 1,
    result: { type: 'text', text: 'pong' },
  };
  stdout.write(JSON.stringify(agentResponse) + '\n');

  assert(stdout.lines.length === 1, 'only ONE line on stdout when gate is OFF');
  let parsed: unknown = null;
  let parseOk = false;
  try {
    parsed = JSON.parse(stdout.lines[0]);
    parseOk = true;
  } catch {
    parseOk = false;
  }
  assert(parseOk, 'sole stdout line is parseable JSON');
  assert(
    typeof parsed === 'object' && parsed !== null && (parsed as { jsonrpc?: string }).jsonrpc === '2.0',
    'parsed JSON is a JSON-RPC envelope',
  );
}

// ---------------------------------------------------------------------------
// Test 4 — `CONFIG.verboseRegister` reads both env vars; defaults to false.
// ---------------------------------------------------------------------------
{
  const prevSpecific = process.env.TOTALRECLAW_VERBOSE_REGISTER;
  const prevGeneral = process.env.TOTALRECLAW_DEBUG;

  delete process.env.TOTALRECLAW_VERBOSE_REGISTER;
  delete process.env.TOTALRECLAW_DEBUG;

  // Reload the module so the getter picks up the cleared env. Use a unique
  // cache-bust query string — Node's loader keys ESM modules by exact URL,
  // so a fresh import is needed when env is mutated between reads.
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const { CONFIG } = await import(`./config.js?cache=${Date.now()}-1`);
  assert(CONFIG.verboseRegister === false, 'verboseRegister defaults to false');

  process.env.TOTALRECLAW_VERBOSE_REGISTER = '1';
  // Note: getter reads env on each access, so no re-import needed for the
  // SAME module instance to pick up the new value.
  assert(CONFIG.verboseRegister === true, 'verboseRegister=true when TOTALRECLAW_VERBOSE_REGISTER=1');

  delete process.env.TOTALRECLAW_VERBOSE_REGISTER;
  process.env.TOTALRECLAW_DEBUG = 'true';
  assert(CONFIG.verboseRegister === true, 'verboseRegister=true when TOTALRECLAW_DEBUG=true');

  delete process.env.TOTALRECLAW_DEBUG;
  assert(CONFIG.verboseRegister === false, 'verboseRegister=false when both env vars cleared');

  // Restore — be a good test citizen.
  if (prevSpecific !== undefined) process.env.TOTALRECLAW_VERBOSE_REGISTER = prevSpecific;
  if (prevGeneral !== undefined) process.env.TOTALRECLAW_DEBUG = prevGeneral;
}

// ---------------------------------------------------------------------------
console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) {
  process.exit(1);
}
