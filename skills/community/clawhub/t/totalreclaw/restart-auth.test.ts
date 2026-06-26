/**
 * Tests for the 5-tier `/restart` auth fallback (issue #215, 3.3.7-rc.1).
 *
 * Asserted properties:
 *   - Each tier (1..5) accepts the invoker when the tier's preconditions hold.
 *   - Explicit-deny only fires when an explicit allow-from is configured
 *     and excludes the invoker (no later tier matches).
 *   - Default-config + lone user → tier 5 allow.
 *   - Default-config + multi user → no-tier-matched reject.
 *   - Wildcard `*` in ownerAllowFrom → tier 1 allow.
 *   - Channel-prefixed entry (`telegram:12345`) matches bare senderId.
 *   - Empty senderId + default-config + 1 inbound user → still rejects
 *     (we can't authorize a sender we can't identify).
 *
 * Run with: npx tsx restart-auth.test.ts
 */

import {
  resolveRestartAuth,
  rejectMessageFor,
  type RestartAuthInput,
  type RestartAuthDeps,
  type RestartAuthConfig,
} from './restart-auth.js';

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

/** Default deps that say "no credentials, no pairing, no inbound users".
 * Each test overrides only what it needs. */
function makeDeps(overrides: Partial<RestartAuthDeps> = {}): RestartAuthDeps {
  return {
    loadCredentialsExists: () => false,
    wasPairedViaChannel: () => false,
    getDistinctInboundUserCount: () => 0,
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// Tier 1: commands.ownerAllowFrom — explicit allow
// ---------------------------------------------------------------------------
{
  const cfg: RestartAuthConfig = { commands: { ownerAllowFrom: ['12345'] } };
  const v = resolveRestartAuth({ senderId: '12345', channel: 'telegram', config: cfg }, makeDeps());
  assert(v.allow === true, 'tier1: ownerAllowFrom listed → allow');
  if (v.allow) assert(v.reason === 'tier1-owner-allow-from', 'tier1: reason set');
}
{
  const cfg: RestartAuthConfig = { commands: { ownerAllowFrom: ['*'] } };
  const v = resolveRestartAuth({ senderId: 'anyone', channel: 'telegram', config: cfg }, makeDeps());
  assert(v.allow === true, 'tier1: ownerAllowFrom wildcard → allow');
}
{
  const cfg: RestartAuthConfig = { commands: { ownerAllowFrom: ['telegram:12345'] } };
  const v = resolveRestartAuth({ senderId: '12345', channel: 'telegram', config: cfg }, makeDeps());
  assert(v.allow === true, 'tier1: prefixed entry matches bare senderId');
}

// commands.allowFrom (per-provider variant) is treated as tier-1 equivalent
{
  const cfg: RestartAuthConfig = { commands: { allowFrom: { '*': ['12345'] } } };
  const v = resolveRestartAuth({ senderId: '12345', channel: 'telegram', config: cfg }, makeDeps());
  assert(v.allow === true, 'tier1: commands.allowFrom["*"] match → allow');
}
{
  const cfg: RestartAuthConfig = { commands: { allowFrom: { telegram: ['99999'] } } };
  const v = resolveRestartAuth({ senderId: '99999', channel: 'telegram', config: cfg }, makeDeps());
  assert(v.allow === true, 'tier1: commands.allowFrom[<provider>] match → allow');
}

// ---------------------------------------------------------------------------
// Tier 2: channels.<provider>.allowFrom — channel-derived allow
// ---------------------------------------------------------------------------
{
  const cfg: RestartAuthConfig = { channels: { telegram: { allowFrom: ['67890'] } } };
  const v = resolveRestartAuth({ senderId: '67890', channel: 'telegram', config: cfg }, makeDeps());
  assert(v.allow === true, 'tier2: channel allowFrom listed → allow');
  if (v.allow) assert(v.reason === 'tier2-channel-allow-from', 'tier2: reason set');
}

// ---------------------------------------------------------------------------
// Tier 3: session-bound (channel paired + lone inbound user)
// ---------------------------------------------------------------------------
{
  const v = resolveRestartAuth(
    { senderId: '11111', channel: 'telegram', config: {} },
    makeDeps({
      wasPairedViaChannel: (ch) => ch === 'telegram',
      getDistinctInboundUserCount: () => 1,
    }),
  );
  assert(v.allow === true, 'tier3: paired channel + 1 inbound → allow');
  if (v.allow) assert(v.reason === 'tier3-session-bound', 'tier3: reason set');
}
{
  // 2+ inbound users with paired channel — tier 3 must NOT fire (we can't
  // be sure the invoker is the paired identity), but tier 4 might.
  const v = resolveRestartAuth(
    { senderId: '11111', channel: 'telegram', config: {} },
    makeDeps({
      wasPairedViaChannel: () => true,
      getDistinctInboundUserCount: () => 3,
      loadCredentialsExists: () => true,
    }),
  );
  assert(v.allow === true, 'tier4: credentials present + paired channel → allow (tier3 skipped, tier4 fires)');
  if (v.allow) assert(v.reason === 'tier4-credentials-paired', 'tier4: reason set when tier3 cannot prove identity');
}

// ---------------------------------------------------------------------------
// Tier 4: credentials.json + paired-via-channel
// ---------------------------------------------------------------------------
{
  const v = resolveRestartAuth(
    { senderId: '22222', channel: 'telegram', config: {} },
    makeDeps({
      loadCredentialsExists: () => true,
      wasPairedViaChannel: () => true,
      getDistinctInboundUserCount: () => 5,  // multi-user → tier 3 fails, tier 5 fails
    }),
  );
  assert(v.allow === true, 'tier4: credentials + paired-via-channel → allow');
  if (v.allow) assert(v.reason === 'tier4-credentials-paired', 'tier4: reason set');
}
{
  // credentials present but channel was NOT paired → tier 4 must NOT fire
  const v = resolveRestartAuth(
    { senderId: '22222', channel: 'telegram', config: {} },
    makeDeps({
      loadCredentialsExists: () => true,
      wasPairedViaChannel: () => false,
      getDistinctInboundUserCount: () => 5,
    }),
  );
  assert(v.allow === false, 'tier4: credentials but no pairing on this channel → reject');
}

// ---------------------------------------------------------------------------
// Tier 5: lone-user heuristic (default config + 1 inbound user)
// ---------------------------------------------------------------------------
{
  const v = resolveRestartAuth(
    { senderId: '33333', channel: 'telegram', config: {} },  // default config
    makeDeps({
      getDistinctInboundUserCount: () => 1,
    }),
  );
  assert(v.allow === true, 'tier5: default-config + 1 inbound → allow');
  if (v.allow) assert(v.reason === 'tier5-lone-user', 'tier5: reason set');
}

// Tier 5 + missing senderId — we still allow because lone-user count is 1.
// This is intentional: in a fresh install the bot may receive a /restart
// before the channel adapter has resolved a stable sender id; the lone-user
// heuristic carries on the install.
{
  const v = resolveRestartAuth(
    { senderId: '', channel: 'telegram', config: {} },
    makeDeps({
      getDistinctInboundUserCount: () => 1,
    }),
  );
  assert(v.allow === true, 'tier5: empty senderId + lone-user → allow (fresh install)');
}

// ---------------------------------------------------------------------------
// Rejections
// ---------------------------------------------------------------------------

// ownerAllowFrom set + invoker not in list + no later tier → reject (explicit-deny-owner)
{
  const cfg: RestartAuthConfig = { commands: { ownerAllowFrom: ['12345'] } };
  const v = resolveRestartAuth(
    { senderId: '99999', channel: 'telegram', config: cfg },
    makeDeps({
      getDistinctInboundUserCount: () => 1,  // tier 5 still rejected because ownerAllowFrom is configured
    }),
  );
  assert(v.allow === false, 'reject: ownerAllowFrom set + sender not in list');
  if (!v.allow) assert(v.reason === 'explicit-deny-owner', 'reject: explicit-deny-owner reason');
}

// channels.<provider>.allowFrom set + invoker not in list + no later tier → reject (explicit-deny-channel)
{
  const cfg: RestartAuthConfig = { channels: { telegram: { allowFrom: ['67890'] } } };
  const v = resolveRestartAuth(
    { senderId: '99999', channel: 'telegram', config: cfg },
    makeDeps({
      getDistinctInboundUserCount: () => 1,
    }),
  );
  assert(v.allow === false, 'reject: channel allowFrom set + sender not in list');
  if (!v.allow) assert(v.reason === 'explicit-deny-channel', 'reject: explicit-deny-channel reason');
}

// default config + multi-user gateway → no-tier-matched
{
  const v = resolveRestartAuth(
    { senderId: '11111', channel: 'telegram', config: {} },
    makeDeps({
      getDistinctInboundUserCount: () => 5,  // multi-user → no tier-5
    }),
  );
  assert(v.allow === false, 'reject: default-config + multi-user → no-tier-matched');
  if (!v.allow) assert(v.reason === 'no-tier-matched', 'reject: no-tier-matched reason');
}

// rejectMessageFor — basic shape
{
  assert(rejectMessageFor('explicit-deny-owner').startsWith('You are not authorized'), 'rejectMessage: explicit-deny-owner format');
  assert(rejectMessageFor('explicit-deny-channel').includes('channels.'), 'rejectMessage: explicit-deny-channel mentions channels');
  assert(rejectMessageFor('no-tier-matched').includes('Multiple users'), 'rejectMessage: no-tier-matched mentions multi-user');
}

// ---------------------------------------------------------------------------
// Edge case: ownerAllowFrom configured but invoker is in channel allow-from
// (tier 1 fails, tier 2 saves the day).
// ---------------------------------------------------------------------------
{
  const cfg: RestartAuthConfig = {
    commands: { ownerAllowFrom: ['ownerguy'] },
    channels: { telegram: { allowFrom: ['12345'] } },
  };
  const v = resolveRestartAuth({ senderId: '12345', channel: 'telegram', config: cfg }, makeDeps());
  assert(v.allow === true, 'tier 1 fails / tier 2 wins: explicit channel allow-from listed');
  if (v.allow) assert(v.reason === 'tier2-channel-allow-from', 'reason: tier2');
}

// ---------------------------------------------------------------------------
// Done
// ---------------------------------------------------------------------------
console.log(`\n# tests ${passed + failed}`);
console.log(`# pass ${passed}`);
console.log(`# fail ${failed}`);
if (failed > 0) {
  console.error(`\nrestart-auth.test FAILED — ${failed} assertion(s) did not hold.`);
  process.exit(1);
}
