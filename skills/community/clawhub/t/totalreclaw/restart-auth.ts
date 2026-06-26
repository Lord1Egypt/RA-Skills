/**
 * /totalreclaw-restart slash command — 5-tier auth fallback (issue #215)
 *
 * Architectural fix shipped 3.3.7-rc.1 after 3.3.6-rc.1 QA found that
 * default-config users (no `commands.ownerAllowFrom`, no
 * `channels.<provider>.allowFrom`) hit "You are not authorized to use
 * this command." when they typed `/restart` to recover from the plugin
 * tool-binding race (the dominant first-run install path).
 *
 * 3.3.7-rc.2 (2026-05-04) renamed the plugin command from `restart` to
 * `totalreclaw-restart` after Pedro caught — in rc.1 manual integration
 * testing — that OpenClaw's plugin registry hard-rejects names on
 * `RESERVED_COMMANDS` (gateway log: `Command name "restart" is reserved
 * by a built-in command`). The 5-tier matrix below is unchanged from
 * rc.1; only the command name attached to it changed. SKILL.md /
 * setup-guide both tell the agent to issue the namespaced form, so
 * end-users never type `restart` directly. An upstream FR is open
 * asking for a plugin-override-precedence flag.
 *
 * Plugin handles `/totalreclaw-restart` (validation passes — hyphenated
 * names are allowed and the name is unique). With `requireAuth: false`
 * the channel-layer auth check is skipped, and this module's
 * `resolveRestartAuth` decides allow-vs-reject using a five-tier
 * fallback. If the result is `allow`, the caller fires
 * `process.kill(process.pid, 'SIGUSR1')` — which the gateway accepts
 * iff `commands.restart=true` (the default; the SIGUSR1 policy keys on
 * the gateway-level config flag, NOT on the plugin command name).
 *
 * Tier order (highest priority first):
 *   1. `commands.ownerAllowFrom` explicitly lists invoker → allow
 *   2. `channels.<provider>.allowFrom` explicitly lists invoker → allow
 *   3. Invoker is the same identity this channel session is bound to → allow
 *   4. `credentials.json` exists AND was paired via this same channel → allow
 *   5. BOTH allow-from configs are unset (default) AND only one user
 *      has ever messaged this gateway → allow (lone-user heuristic)
 *
 * Rejection ONLY when explicit config exists and excludes the invoker
 * (i.e. tier 1 or tier 2 was configured but did not match), and no
 * later tier matched.
 *
 * Intentionally pure (no fs/process side effects) so the matrix can be
 * exhaustively tested in `restart-auth.test.ts`. Filesystem / process
 * lookups are passed in via `RestartAuthDeps`.
 */

/** Minimal config shape this module reads. Avoids importing OpenClaw's
 * full OpenClawConfig type so the file stays self-contained for testing. */
export interface RestartAuthConfig {
  commands?: {
    ownerAllowFrom?: ReadonlyArray<string | number>;
    allowFrom?: Record<string, ReadonlyArray<string | number>>;
  };
  channels?: Record<
    string,
    {
      allowFrom?: ReadonlyArray<string | number>;
    } | undefined
  >;
}

/** Verdict returned to the caller. */
export type RestartAuthVerdict =
  | { allow: true; reason: 'tier1-owner-allow-from' | 'tier2-channel-allow-from' | 'tier3-session-bound' | 'tier4-credentials-paired' | 'tier5-lone-user' }
  | { allow: false; reason: 'explicit-deny-owner' | 'explicit-deny-channel' | 'no-tier-matched' };

/** Helper: normalize an allow-from entry for case-insensitive comparison.
 * Accepts string | number (Telegram chat IDs are numeric, Discord uses
 * `discord:<id>` strings, etc.). Mirrors OpenClaw's `normalizeStringEntries`
 * + lowercasing dance — we keep this local so the plugin doesn't depend on
 * OpenClaw's internal symbol layout. */
function normalizeEntry(value: string | number): string {
  return String(value).trim().toLowerCase();
}

function entryMatches(allowFrom: ReadonlyArray<string | number>, senderId: string): boolean {
  if (!senderId) return false;
  const needle = senderId.trim().toLowerCase();
  if (!needle) return false;
  for (const raw of allowFrom) {
    const normalized = normalizeEntry(raw);
    if (!normalized) continue;
    // wildcard: match any sender
    if (normalized === '*') return true;
    if (normalized === needle) return true;
    // Channel-prefixed entries: `telegram:12345`, `discord:user:12345`, etc.
    // The senderId is bare (e.g. `12345`); treat the suffix after the LAST
    // colon as the bare id and compare. This mirrors how OpenClaw parses
    // chat-allow-target prefixes in the upstream allow-from helper.
    const lastColon = normalized.lastIndexOf(':');
    if (lastColon >= 0) {
      const tail = normalized.slice(lastColon + 1);
      if (tail === needle) return true;
    }
  }
  return false;
}

/**
 * Pure dependencies for the auth resolver. Tests inject mocks; production
 * passes real fs / runtime functions.
 *
 * `loadCredentialsExists` returns true if the plugin's own `credentials.json`
 * is present on disk (does NOT load the contents — we never need the
 * mnemonic for this check). The plugin already exposes `loadCredentialsJson`
 * for this; the wrapper just maps `null → false`.
 *
 * `wasPairedViaChannel` is the tier-4 hint: returns true if the active
 * channel is the same one the credentials were paired through. Production
 * persists the pair-channel into the channel-allow-from store at
 * pair-finish (see `pair-session-store.ts` 3.3.0 path) — so the check
 * collapses to "any allow-from store entry exists for this provider".
 *
 * `getDistinctInboundUserCount` returns how many distinct sender IDs have
 * messaged this gateway on the active channel. Tier-5 only fires when this
 * is exactly 1 (the lone-user heuristic — first-run install path).
 */
export interface RestartAuthDeps {
  loadCredentialsExists: () => boolean;
  wasPairedViaChannel: (channel: string) => boolean;
  getDistinctInboundUserCount: (channel: string) => number;
}

export interface RestartAuthInput {
  /** The invoker (Telegram chat id, Discord user id, etc). May be empty if the channel adapter couldn't resolve it. */
  senderId: string | undefined | null;
  /** Channel slug (e.g. `telegram`, `discord`, `slack`). May be undefined for in-process / CLI invocations. */
  channel: string | undefined | null;
  /** OpenClaw config object (the plugin command handler receives this). */
  config: RestartAuthConfig | undefined | null;
}

/**
 * Resolve whether the given invoker may run `/totalreclaw-restart`.
 *
 * Tier order: see file header.
 *
 * Edge cases:
 *  - `senderId` empty / undefined → tier 1+2 cannot match (entryMatches
 *    returns false on empty), tier 3 also cannot match. Tier 4 still
 *    works (it's not sender-keyed). Tier 5 still works (it's a count, not
 *    sender-keyed). Default-config + 0 inbound users → 'no-tier-matched'.
 *  - `channel` empty → tier 2/3/4/5 cannot resolve (they're channel-
 *    scoped); only tier 1 can save the day.
 *  - `config` null/undefined → treated as default-config (no allowFrom
 *    set anywhere) → tiers 4 + 5 still apply.
 */
export function resolveRestartAuth(
  input: RestartAuthInput,
  deps: RestartAuthDeps,
): RestartAuthVerdict {
  const senderId = (input.senderId ?? '').toString().trim();
  const channel = (input.channel ?? '').toString().trim().toLowerCase();
  const cfg = input.config ?? {};

  // ---------------------------------------------------------------
  // Tier 1: commands.ownerAllowFrom explicitly lists invoker.
  // ---------------------------------------------------------------
  const ownerAllowFrom = cfg.commands?.ownerAllowFrom;
  const ownerListConfigured = Array.isArray(ownerAllowFrom) && ownerAllowFrom.length > 0;
  if (ownerListConfigured && senderId && entryMatches(ownerAllowFrom!, senderId)) {
    return { allow: true, reason: 'tier1-owner-allow-from' };
  }

  // Note: also honor `commands.allowFrom` per-provider entries as a tier-1
  // equivalent — they are an alternative explicit owner allowlist surface.
  const cmdAllowFromGlobal = cfg.commands?.allowFrom?.['*'];
  const cmdAllowFromChannel = channel ? cfg.commands?.allowFrom?.[channel] : undefined;
  const cmdAllowFromConfigured = Array.isArray(cmdAllowFromGlobal) && cmdAllowFromGlobal.length > 0
    || Array.isArray(cmdAllowFromChannel) && cmdAllowFromChannel.length > 0;
  if (
    senderId
    && (
      (Array.isArray(cmdAllowFromGlobal) && entryMatches(cmdAllowFromGlobal, senderId))
      || (Array.isArray(cmdAllowFromChannel) && entryMatches(cmdAllowFromChannel, senderId))
    )
  ) {
    return { allow: true, reason: 'tier1-owner-allow-from' };
  }

  // ---------------------------------------------------------------
  // Tier 2: channels.<provider>.allowFrom explicitly lists invoker.
  // ---------------------------------------------------------------
  const channelAllowFrom = channel ? cfg.channels?.[channel]?.allowFrom : undefined;
  const channelListConfigured = Array.isArray(channelAllowFrom) && channelAllowFrom.length > 0;
  if (channelListConfigured && senderId && entryMatches(channelAllowFrom!, senderId)) {
    return { allow: true, reason: 'tier2-channel-allow-from' };
  }

  // ---------------------------------------------------------------
  // Tier 3: session-bound identity match.
  //
  // If the channel is paired (i.e. the channel-allow-from store has an
  // entry for this channel + matches this sender), treat that as
  // implicit owner-auth. This covers the case where the user paired
  // via QR earlier in the same install — the pairing wrote a store
  // entry for `<channel>:<senderId>` even though `commands.ownerAllowFrom`
  // is unset.
  //
  // Implementation: `wasPairedViaChannel` returns true if a store
  // entry exists for this channel; we additionally require that the
  // sender's id is one of the store entries (we can't query-by-sender
  // without exposing the store, so we approximate by checking whether
  // the channel has ANY pairing AND there's only one user — that's the
  // common case AND the failure mode the bug report describes; the
  // multi-user-paired case is rare in default-config and falls through
  // to tier 5 if the count is 1, otherwise to no-tier-matched).
  // ---------------------------------------------------------------
  if (channel && senderId && deps.wasPairedViaChannel(channel)) {
    // For tier 3 to fire safely we need either (a) only one paired user
    // on this channel, or (b) the sender is explicitly the paired user.
    // Without exposing the full store list (which would require an
    // upstream API change), we conservatively gate on a single inbound
    // user — same-shape as tier 5, but priority-ordered above it
    // because the pairing is a stronger signal than the lone-user
    // heuristic alone.
    if (deps.getDistinctInboundUserCount(channel) === 1) {
      return { allow: true, reason: 'tier3-session-bound' };
    }
  }

  // ---------------------------------------------------------------
  // Tier 4: credentials.json exists AND paired via this same channel.
  // ---------------------------------------------------------------
  if (channel && deps.loadCredentialsExists() && deps.wasPairedViaChannel(channel)) {
    return { allow: true, reason: 'tier4-credentials-paired' };
  }

  // ---------------------------------------------------------------
  // Tier 5: lone-user heuristic (default config + single inbound user).
  // Only applies when NEITHER explicit allow-from is set anywhere AND
  // exactly one user has messaged this gateway on this channel.
  // ---------------------------------------------------------------
  const anyExplicitConfig = ownerListConfigured || cmdAllowFromConfigured || channelListConfigured;
  if (!anyExplicitConfig && channel && deps.getDistinctInboundUserCount(channel) === 1) {
    return { allow: true, reason: 'tier5-lone-user' };
  }

  // ---------------------------------------------------------------
  // No tier matched — decide WHICH rejection reason to return.
  // ---------------------------------------------------------------
  if (ownerListConfigured || cmdAllowFromConfigured) return { allow: false, reason: 'explicit-deny-owner' };
  if (channelListConfigured) return { allow: false, reason: 'explicit-deny-channel' };
  return { allow: false, reason: 'no-tier-matched' };
}

/** Human-readable rejection text. Kept in this module so the
 * plugin handler doesn't have to duplicate the string. */
export function rejectMessageFor(reason: 'explicit-deny-owner' | 'explicit-deny-channel' | 'no-tier-matched'): string {
  if (reason === 'explicit-deny-owner') {
    return 'You are not authorized to use this command. Add your channel id to `commands.ownerAllowFrom` in your OpenClaw config to grant access.';
  }
  if (reason === 'explicit-deny-channel') {
    return 'You are not authorized to use this command. Add your channel id to `channels.<provider>.allowFrom` in your OpenClaw config to grant access.';
  }
  // 'no-tier-matched' — happens when default-config but multiple inbound
  // users (lone-user heuristic does not apply). Surface a clear pointer.
  return 'You are not authorized to use this command. Multiple users have messaged this gateway; configure `commands.ownerAllowFrom` to identify the owner.';
}
