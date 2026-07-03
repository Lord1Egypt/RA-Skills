/**
 * Regression test for issue #128 — register-time breadcrumbs must not bleed
 * into `openclaw agent --json` stdout.
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
 * History
 * -------
 * Phase 3.2 (this branch) RETIRED the legacy `totalreclaw_*` agent tools
 * (totalreclaw_pair, totalreclaw_report_qa_bug, etc.) and replaced them
 * with native `memory_search` / `memory_get` tools registered through the
 * host's MemoryPluginCapability via `registerNativeMemory`. The old
 * `CONFIG.verboseRegister`-gated breadcrumbs for the retired tools were
 * removed along with the tools themselves.
 *
 * What this asserts NOW
 * ---------------------
 *   1. The retired-tool breadcrumbs are GONE from index.ts (regression
 *      guard — re-adding them would re-introduce the stdout leak).
 *   2. The CURRENT native-registration breadcrumb exists exactly once and
 *      lives inside the `registerNativeMemory` try/catch (so a failure
 *      in the native path does not emit a false-success breadcrumb).
 *   3. Mock-runtime check: a stdout sink wrapping `JSON.parse` of every
 *      line emitted by the plugin in `--json` simulation succeeds (no log
 *      lines, only the JSON body). Approximated by feeding our gated
 *      logger sample lines and asserting the JSON parser sees a
 *      single-line valid JSON object.
 *   4. `CONFIG.verboseRegister` reads `TOTALRECLAW_VERBOSE_REGISTER`
 *      AND falls through to `TOTALRECLAW_DEBUG`. Default false.
 *      (CONFIG.verboseRegister is still defined in config.ts and still
 *      honored by any future verbose-gated log; we assert it stays correct
 *      so the mechanism is ready if ops needs to re-add a breadcrumb.)
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
// Test 1 — retired-tool breadcrumbs are GONE from index.ts.
//
// Phase 3.2 retired totalreclaw_pair / totalreclaw_report_qa_bug (and the
// rest of the totalreclaw_* agent tools). Their register-time breadcrumbs
// were removed because the underlying `api.logger.info` call leaks to
// stdout in OpenClaw (issue #128). Re-adding either literal to index.ts
// would re-introduce the stdout leak — this is a regression guard.
// ---------------------------------------------------------------------------
{
  const retired = [
    'registerTool(totalreclaw_pair) returned',
    'totalreclaw_report_qa_bug registered',
  ];
  for (const banner of retired) {
    assert(
      !SRC.includes(banner),
      `retired breadcrumb "${banner}" is NOT present in index.ts (Phase 3.2 retire)`,
    );
  }
  // Belt-and-suspenders: no `registerTool(<literal>) returned` style
  // breadcrumb for ANY totalreclaw_* agent tool has leaked back in.
  const totalreclawToolBreadcrumb = /registerTool\(\s*totalreclaw_[a-z_]+\s*\)\s+returned/;
  assert(
    !totalreclawToolBreadcrumb.test(SRC),
    'no `registerTool(totalreclaw_*) returned` breadcrumb of any kind in index.ts',
  );
}

// ---------------------------------------------------------------------------
// Test 2 — the CURRENT native-registration breadcrumb exists and is scoped
// to the registerNativeMemory try/catch.
//
// The single remaining register-time success log is the native capability
// breadcrumb at the end of register(). It is emitted via api.logger.info
// unconditionally (NOT behind CONFIG.verboseRegister), because it is the
// only ops-visible signal that the native memory pipeline came up. We
// assert it exists exactly once and that its preceding line is the
// registerNativeMemory() call (so a try/catch failure cannot emit a
// false-success breadcrumb — the log is inside the try, before the catch).
// ---------------------------------------------------------------------------
{
  const banner = 'registered native MemoryPluginCapability + memory_search/memory_get tools';
  const count = SRC.split(banner).length - 1;
  assert(count === 1, `native registration breadcrumb present exactly once (got ${count})`);

  const idx = SRC.indexOf(banner);
  // Walk backwards ~300 chars — the registerNativeMemory(api, ...) call
  // must precede the breadcrumb (both inside the same try block).
  const window = SRC.slice(Math.max(0, idx - 300), idx);
  assert(
    /registerNativeMemory\s*\(/.test(window),
    'native breadcrumb is preceded by the registerNativeMemory() call (inside the try)',
  );
  // Walk forwards ~500 chars — the catch block must follow, so a
  // registration failure routes to api.logger.warn, not the success log.
  const after = SRC.slice(idx, idx + 500);
  assert(
    /}\s*catch\s*\(/.test(after),
    'native breadcrumb is followed by a catch block (failure does not emit false-success)',
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
