/**
 * pair-cli-default-mode.test.ts (3.3.4-rc.1)
 *
 * Asserts the 3.3.4-rc.1 invariant: the `openclaw totalreclaw pair`
 * CLI defaults to relay-mode. Without `--local`, the action picks the
 * relay runner. With `--local`, it picks the legacy local flow.
 *
 * QA on 3.3.3-rc.1 (Pedro 2026-04-30) found the CLI fallback emitted
 * `http://localhost:18789/...` — unreachable from a remote browser on
 * Docker deployments. This test pins the fix (relay default) so a
 * future refactor doesn't silently regress.
 *
 * Two layers of coverage:
 *
 *   1. `shouldUseRelayMode` (pure decision function): canonical truth
 *      table for the relay-vs-local selection.
 *
 *   2. The wired `registerPairCli` action: when the relay runner is
 *      wired AND no `--local` flag is set, the action invokes
 *      `runRelayPairCli` BEFORE attempting any local-flow surface.
 *      Asserted by counting calls to the stub relay runner — the test
 *      stub returns `'completed'` so the action exits cleanly without
 *      touching the local flow.
 */

import {
  registerPairCli,
  shouldUseRelayMode,
  type PairCliOutcome,
} from './pair-cli.js';

let passed = 0;
let failed = 0;
function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) { console.log(`ok ${n} - ${name}`); passed++; }
  else { console.log(`not ok ${n} - ${name}`); failed++; }
}

// ---------------------------------------------------------------------------
// shouldUseRelayMode — pure truth-table.
// ---------------------------------------------------------------------------

assert(
  shouldUseRelayMode({ hasRelayRunner: true }) === true,
  'shouldUseRelayMode: no flags + relay runner wired -> relay (3.3.4-rc.1 default)',
);
assert(
  shouldUseRelayMode({ local: true, hasRelayRunner: true }) === false,
  'shouldUseRelayMode: --local + relay runner wired -> local (explicit opt-in)',
);
assert(
  shouldUseRelayMode({ hasRelayRunner: false }) === false,
  'shouldUseRelayMode: no flags + no relay runner wired -> local (back-compat)',
);
assert(
  shouldUseRelayMode({ local: true, hasRelayRunner: false }) === false,
  'shouldUseRelayMode: --local + no relay runner -> local',
);

// ---------------------------------------------------------------------------
// registerPairCli wired action — relay runner invoked in default-mode.
// ---------------------------------------------------------------------------

interface MockCommand {
  _name: string;
  _action: ((...args: unknown[]) => Promise<void> | void) | null;
  commands: MockCommand[];
  name(): string;
  command(name: string): MockCommand;
  description(text: string): MockCommand;
  option(flags: string, description: string, defaultValue?: unknown): MockCommand;
  action(fn: (...args: unknown[]) => Promise<void> | void): MockCommand;
}

function mkMockCommand(name: string): MockCommand {
  const cmd: MockCommand = {
    _name: name,
    _action: null,
    commands: [],
    name() { return this._name; },
    command(n: string) {
      const child = mkMockCommand(n);
      this.commands.push(child);
      return child;
    },
    description() { return this; },
    option() { return this; },
    action(fn) { this._action = fn; return this; },
  };
  return cmd;
}

function findPairCommand(program: MockCommand): MockCommand | null {
  const tr = program.commands.find((c) => c.name() === 'totalreclaw');
  if (!tr) return null;
  return tr.commands.find((c) => c.name().startsWith('pair')) ?? null;
}

interface RelayCall {
  mode: string;
  outputMode?: string;
}

async function runActionDefaultMode(opts: {
  flags: { json?: boolean; urlPinOnly?: boolean };
}): Promise<RelayCall[]> {
  const relayCalls: RelayCall[] = [];

  const program = mkMockCommand('openclaw');

  registerPairCli(program as unknown as Parameters<typeof registerPairCli>[0], {
    sessionsPath: '/tmp/__never_used__',
    renderPairingUrl: () => '__never_used__',
    logger: { info: () => {}, warn: () => {}, error: () => {} },
    runRelayPairCli: async (mode, runOpts): Promise<PairCliOutcome> => {
      relayCalls.push({ mode, outputMode: runOpts.outputMode });
      // 'completed' status means the action does NOT call process.exit.
      return { status: 'completed', sid: 'relay-stub-token' };
    },
  });

  const pairCmd = findPairCommand(program);
  if (!pairCmd || !pairCmd._action) throw new Error('pair command not registered');
  await pairCmd._action('generate', opts.flags, pairCmd);
  return relayCalls;
}

// Default flags -> relay runner invoked exactly once.
{
  const calls = await runActionDefaultMode({ flags: {} });
  assert(
    calls.length === 1,
    'action: default flags + relay runner wired -> relay runner invoked once',
  );
  assert(
    calls[0]?.mode === 'generate',
    'action: pair mode "generate" forwarded to relay runner',
  );
}

// --json flag -> relay runner invoked, outputMode='json'.
{
  const calls = await runActionDefaultMode({ flags: { json: true } });
  assert(
    calls.length === 1 && calls[0]?.outputMode === 'json',
    'action: --json flag forwarded as outputMode="json" to relay runner',
  );
}

// --url-pin-only flag -> outputMode='url-pin' (subset of --json).
{
  const calls = await runActionDefaultMode({ flags: { urlPinOnly: true } });
  assert(
    calls.length === 1 && calls[0]?.outputMode === 'url-pin',
    'action: --url-pin-only flag forwarded as outputMode="url-pin" to relay runner',
  );
}

// --url-pin-only + --json -> --url-pin-only wins (it's the tighter surface).
{
  const calls = await runActionDefaultMode({ flags: { json: true, urlPinOnly: true } });
  assert(
    calls.length === 1 && calls[0]?.outputMode === 'url-pin',
    'action: --url-pin-only beats --json when both passed (tighter surface wins)',
  );
}

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
}
console.log('\nALL TESTS PASSED');
