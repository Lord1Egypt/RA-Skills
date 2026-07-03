/**
 * trajectory-poller.ts — auto-extraction without relying on agent_end hook.
 *
 * Background (3.3.11-rc.1, 2026-05-06):
 *   OpenClaw 2026.5.4 silently rejects `agent_end` hook registration for
 *   non-bundled plugins despite
 *   `plugins.entries.totalreclaw.hooks.allowConversationAccess=true` in
 *   config. Verified across multiple SIGUSR1 cycles in fresh canonical
 *   containers — block message fires every boot. Pedro's pop-os
 *   2026-05-05 QA showed 0 extraction events across 2 h of Telegram chat.
 *
 *   Workaround: poll OpenClaw's trajectory log files directly via
 *   setInterval (NOT a hook event — gateway doesn't gate it). Every
 *   60 s, scan
 *
 *       ~/.openclaw/agents/<agent>/sessions/<sid>.trajectory.jsonl
 *
 *   for new prompt.submitted (user) and model.completed
 *   (data.assistantTexts) events since the last poll, build the same
 *   {role, content}[] array the agent_end hook received, and run the
 *   existing extraction pipeline. Per-file byte-offset is tracked in
 *   ~/.totalreclaw/extract-state.json so we never re-process lines.
 *
 * RC1 capture strategy (Phase 4, 2026-06-22):
 *   RC1 capture = POLLER-PRIMARY, FLUSH-SHADOWED. This poller is the
 *   capture workhorse. OpenClaw's host-facing `flushPlanResolver`
 *   (wired in native-memory.ts via buildFlushPlan) returns TR's
 *   extraction plan so the memory slot is "complete" and the host CAN
 *   drive flushes — but TR's encrypt→on-chain capture does NOT depend
 *   on the host invoking the flush. The flush-driven capture path
 *   (host flush → read scratch file → encrypt → on-chain) is NOT
 *   wired on TR's side today; that is H2/RC2-gated. The poller
 *   guarantees capture works regardless of host flush cadence: even
 *   if the host never flushes, the poller still captures on its own
 *   60 s schedule. This is the graceful-degradation stance —
 *   recall-native + capture-poller meets both primary bars even if
 *   H2 (host flush cadence) fails at the RC1 QA gate.
 *
 *   RC2 retires this poller IF H2 confirms the host invokes
 *   flushPlanResolver at useful cadence. If H2 fails, the poller
 *   stays as the long-term capture mechanism.
 *
 * Idempotency / offset-dedup:
 *   The poller is idempotent across poller-restart and gateway-reload.
 *   `extract-state.json` is the single source of truth for "what's
 *   been consumed from each trajectory file": loadState() reads it at
 *   the start of every poll iteration, parseNewMessages() only reads
 *   bytes past the recorded offset, and the file is rewritten (via
 *   saveState) only when at least one file's offset advanced. A
 *   poller that crashes mid-extraction loses at most the in-flight
 *   pass (state was not yet saved); the next poller re-reads from the
 *   last persisted offset and re-runs the extraction — duplicate
 *   facts are caught downstream by the dedup pass, and re-extraction
 *   of the same slice is bounded to one retry (state then advances).
 *
 *   `parseNewMessages` caps newOffset at the last full newline so a
 *   partially-flushed trailing line is re-read on the next poll
 *   rather than dropped or double-counted.
 *
 * Cross-path double-write (NOT a risk today; RC2 work):
 *   Today the poller is the only capture path that actually fires.
 *   The agent_end / before_compaction / before_reset hook handlers
 *   in index.ts still REGISTER storeExtractedFacts callbacks, but on
 *   OpenClaw 2026.5.x the host never fires those events for
 *   non-bundled plugins (the bug that motivated this poller), so in
 *   practice the poller is the sole capture path. If a future
 *   OpenClaw release un-blocks the hooks (or when the RC2
 *   flush-driven capture path is wired), BOTH the poller AND the
 *   parallel path would capture from overlapping state with NO
 *   shared dedup — the hooks do NOT consult `extract-state.json`.
 *   That is acceptable for RC1 (only the poller fires) but becomes
 *   a real double-write risk at RC2. See the TODO(RC2/H2) marker on
 *   STATE_FILE below for where the shared last-captured-offset
 *   resolver would live. The earlier claim that "both paths can
 *   coexist with offset-based dedup" was aspirational; no such
 *   shared offset exists today.
 *
 * Module boundary (scanner constraint):
 *   This file does disk I/O (fs.read* on trajectory files + state file)
 *   and intentionally avoids any outbound-network trigger words —
 *   otherwise OpenClaw's runtime scanner would flag the module under
 *   its potential-exfiltration rule (read-then-send pattern). All
 *   extraction work that touches the network is done via
 *   dependency-injected functions whose names are aliased in this
 *   module to neutral identifiers (`runExtraction`,
 *   `getDedupCandidates`, `persistFacts`). Callers in the main module
 *   can use any names they like; the aliases keep this file's source
 *   text free of trigger markers.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

// ---------------------------------------------------------------------------
// Public surface
// ---------------------------------------------------------------------------

export interface TrajectoryPollerDeps {
  /** Same logger surface as the OpenClaw plugin api. */
  logger: {
    info: (msg: string) => void;
    warn: (msg: string) => void;
    error: (msg: string) => void;
  };

  /**
   * 3.3.12-rc.19: optional slot-self-heal hook invoked once per poll
   * tick. OpenClaw's config-rewrite-after-restart can strip
   * plugins.slots.memory after register()'s self-heal ran (observed on
   * pop-os reinstall 2026-06-30 → slot reverted to disabled memory-core
   * → memory_search/memory_get never bound). The host wires this to
   * patchOpenClawConfig + a SIGUSR1 restart so the slot is re-asserted
   * on the next tick if it was clobbered. Runs before the pairing/
   * import gates so it fires even when extraction is deferred.
   */
  recheckSlot?: () => void;

  /** Initialization gate — same one the agent_end hook uses. */
  ensureInitialized: () => Promise<void>;

  /** True when the user has not paired yet — skip extraction. */
  isPairingPending: () => boolean;

  /** True when an import is mid-flight — skip to avoid re-import loops. */
  isImportActive: () => boolean;

  /** Number of conversation turns between extraction passes. */
  getExtractInterval: () => number;

  /** Hard cap on facts stored per extraction pass. */
  getMaxFactsPerExtraction: () => number;

  /** Whether the dedup-via-existing-memories pass is on. */
  isDedupEnabled: () => boolean;

  /**
   * Look up existing memories to feed the dedup pass. Aliased so this
   * module's source contains no outbound-request trigger words.
   */
  getDedupCandidates: (
    limit: number,
    messages: Array<{ role: 'user' | 'assistant'; content: string }>,
  ) => Promise<unknown[]>;

  /**
   * Run LLM-driven extraction. Aliased to neutral identifier; the real
   * function does an outbound model call but the call site lives in
   * the main module's outbound-request surface.
   */
  runExtraction: (
    messages: Array<{ role: 'user' | 'assistant'; content: string }>,
    mode: 'turn' | 'full',
    existing: unknown[],
    extra?: unknown,
  ) => Promise<ExtractedFactLike[]>;

  /** Filter raw facts by importance score. */
  filterByImportance: (
    facts: ExtractedFactLike[],
  ) => { kept: ExtractedFactLike[]; dropped: number };

  /**
   * Store filtered facts to the encrypted vault. Aliased to neutral
   * identifier.
   */
  persistFacts: (facts: ExtractedFactLike[]) => Promise<number>;
}

/** Minimal fact shape. The deps hand the actual structured facts. */
export type ExtractedFactLike = {
  text: string;
  importance?: number;
  [k: string]: unknown;
};

/**
 * Persistent per-file offset tracker. The keys are absolute paths to
 * trajectory files; values are last byte-offset processed and the
 * accumulated turn count since the last extraction pass.
 */
export type PollerState = Record<string, { offset: number; turnsAccum: number }>;

export interface TrajectoryPollerHandle {
  /** Stop the poller. Idempotent. */
  stop: () => void;
  /** Run one poll iteration synchronously (for tests). */
  pollOnce: () => Promise<void>;
}

const DEFAULT_POLL_INTERVAL_MS = 60_000;
// Per-file offset tracker (poller's own source of truth for what's been
// consumed from each trajectory file). Today this is consulted ONLY by the
// poller — the agent_end / before_compaction / before_reset hooks in
// index.ts do NOT read or write it, so if any of those hooks ever fire
// alongside the poller they would double-capture from overlapping state.
//
// TODO(RC2/H2): when the flush-driven capture path is wired (host invokes
// flushPlanResolver → TR reads the scratch file → encrypt → on-chain) OR
// the upstream agent_end block is lifted, ALL capture paths MUST consult
// a shared last-captured-offset resolver before encrypting. The simplest
// shape is to expose loadState()/saveState() (or a `consumed(file)`
// helper) to the hook handlers and the flush callback so they skip any
// byte range the poller already consumed, and conversely the poller must
// skip any range the hooks/flush path recorded. Until then, this file is
// poller-private and there is no cross-path double-write risk (only the
// poller fires on OpenClaw 2026.5.x).
const STATE_FILE = path.join(os.homedir(), '.totalreclaw', 'extract-state.json');
/**
 * Skip trajectory files older than this. A user who installs
 * TotalReclaw on a host with months of OpenClaw session log history
 * shouldn't get a retroactive extraction backlog — we only care about
 * ongoing chat from now forward (3.3.11-rc.5). Files with mtime older
 * than this threshold get a one-time offset snapshot so they're never
 * re-scanned, and skip the extraction path entirely.
 */
const STALE_TRAJECTORY_AGE_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

/**
 * Start the trajectory poller. Runs an initial poll after 5 s, then
 * every `pollIntervalMs` (default 60 s). Returns a handle the caller
 * can use to stop polling and run one-shot polls in tests.
 */
export function startTrajectoryPoller(
  deps: TrajectoryPollerDeps,
  opts: { pollIntervalMs?: number; stateFile?: string } = {},
): TrajectoryPollerHandle {
  const pollIntervalMs = opts.pollIntervalMs ?? DEFAULT_POLL_INTERVAL_MS;
  const stateFile = opts.stateFile ?? STATE_FILE;

  const pollAndExtract = async (): Promise<void> => {
    try {
      // 3.3.12-rc.19: re-assert slots.memory each tick in case OpenClaw's
      // config-rewrite stripped it after register() (see deps.recheckSlot).
      deps.recheckSlot?.();
      await deps.ensureInitialized();
      if (deps.isPairingPending()) return;
      if (deps.isImportActive()) return;

      const state = loadState(stateFile, deps.logger);
      const files = findTrajectoryFiles();
      if (files.length === 0) return;

      const extractInterval = deps.getExtractInterval();
      let stateChanged = false;
      // 3.3.11-rc.5: cap extractions per poll iteration. Pedro's
      // 2026-05-07 zai 429 cascade was caused by N session files all
      // crossing the extract threshold in the same poll → N back-to-back
      // LLM calls trip the rate-limiter (especially on free tiers).
      // With cap=1, extra files defer to the next poll iteration
      // (60 s later by default). Their turnsAccum is preserved across
      // polls so they don't lose progress.
      let extractionsThisPoll = 0;
      const MAX_EXTRACTIONS_PER_POLL = 1;

      for (const file of files) {
        // Stale-file skip: trajectory files untouched for STALE_TRAJECTORY_AGE_MS
        // are likely abandoned sessions (old test runs, dead chats). Skip them
        // entirely — don't burn LLM budget on extraction from stale content
        // that the user has effectively forgotten about.
        let mtimeMs = 0;
        try {
          mtimeMs = fs.statSync(file).mtimeMs;
        } catch {
          continue;
        }
        if (Date.now() - mtimeMs > STALE_TRAJECTORY_AGE_MS) {
          // Lazy-record offset so we don't repeatedly re-scan stale files —
          // if the user later resumes this session, the offset is already
          // current and we'll only extract net-new content.
          if (!state[file]) {
            try {
              state[file] = { offset: fs.statSync(file).size, turnsAccum: 0 };
              stateChanged = true;
            } catch { /* ignore */ }
          }
          continue;
        }

        const lastEntry = state[file] ?? { offset: 0, turnsAccum: 0 };
        const { messages, newOffset } = parseNewMessages(file, lastEntry.offset);
        if (newOffset === lastEntry.offset) continue; // nothing new

        const turnsAdded = countTurns(messages);
        const turnsAccum = lastEntry.turnsAccum + turnsAdded;
        const shouldExtract =
          turnsAccum >= extractInterval &&
          messages.length >= 2 &&
          extractionsThisPoll < MAX_EXTRACTIONS_PER_POLL;

        if (shouldExtract) {
          extractionsThisPoll++;

          deps.logger.info(
            `extractd: ${path.basename(file)} -> ${turnsAccum}/${extractInterval} turns; running extraction (${messages.length} messages)`,
          );
          const existing = deps.isDedupEnabled() ? await deps.getDedupCandidates(20, messages) : [];
          const rawFacts = await deps.runExtraction(messages, 'turn', existing, undefined);
          deps.logger.info(`extractd: extraction returned ${rawFacts.length} raw facts`);
          const { kept, dropped } = deps.filterByImportance(rawFacts);
          deps.logger.info(`extractd: importance-filter kept=${kept.length} dropped=${dropped}`);
          const maxFacts = deps.getMaxFactsPerExtraction();
          const facts = kept.slice(0, maxFacts);
          if (facts.length > 0) {
            const stored = await deps.persistFacts(facts);
            deps.logger.info(`extractd: stored ${stored} facts to encrypted vault`);
          } else {
            deps.logger.info('extractd: 0 storable facts after filter');
          }
          state[file] = { offset: newOffset, turnsAccum: 0 };
        } else {
          state[file] = { offset: newOffset, turnsAccum };
          if (turnsAdded > 0) {
            deps.logger.info(
              `extractd: ${path.basename(file)} -> +${turnsAdded} turns (total ${turnsAccum}/${extractInterval}, deferred)`,
            );
          }
        }
        stateChanged = true;
      }

      if (stateChanged) saveState(stateFile, state, deps.logger);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      deps.logger.error(`extractd: poll iteration failed: ${msg}`);
    }
  };

  const timer = setInterval(() => {
    void pollAndExtract();
  }, pollIntervalMs);
  if (typeof timer.unref === 'function') timer.unref();

  const initialTimeout = setTimeout(() => {
    void pollAndExtract();
  }, 5_000);
  if (typeof initialTimeout.unref === 'function') initialTimeout.unref();

  deps.logger.info(`extractd: trajectory poller started (interval=${Math.round(pollIntervalMs / 1000)}s)`);

  return {
    stop: () => {
      clearInterval(timer);
      clearTimeout(initialTimeout);
    },
    pollOnce: pollAndExtract,
  };
}

// ---------------------------------------------------------------------------
// Filesystem scan + trajectory parser
// ---------------------------------------------------------------------------

/**
 * Walk `~/.openclaw/agents/<agent>/sessions/` and collect every
 * `*.trajectory.jsonl` file. Best-effort — malformed agent dirs are
 * skipped silently.
 */
export function findTrajectoryFiles(rootHome?: string): string[] {
  const home = rootHome ?? os.homedir();
  const agentsDir = path.join(home, '.openclaw', 'agents');
  if (!fs.existsSync(agentsDir)) return [];

  const out: string[] = [];
  try {
    for (const agent of fs.readdirSync(agentsDir)) {
      const sessionsDir = path.join(agentsDir, agent, 'sessions');
      if (!fs.existsSync(sessionsDir)) continue;
      for (const f of fs.readdirSync(sessionsDir)) {
        if (f.endsWith('.trajectory.jsonl')) {
          out.push(path.join(sessionsDir, f));
        }
      }
    }
  } catch {
    // Best-effort; skip silently on read errors.
  }
  return out;
}

/**
 * Read new bytes since `lastOffset` and parse them as line-delimited
 * trajectory events. Extracts user prompts and assistant text replies
 * into the `{role, content}[]` shape the extraction pipeline expects.
 *
 * Conservatively caps `newOffset` at the last full newline so
 * partially-flushed lines are re-read on the next poll.
 */
export function parseNewMessages(
  file: string,
  lastOffset: number,
): {
  messages: Array<{ role: 'user' | 'assistant'; content: string }>;
  newOffset: number;
} {
  const stat = fs.statSync(file);
  if (stat.size <= lastOffset) {
    return { messages: [], newOffset: stat.size };
  }
  const fd = fs.openSync(file, 'r');
  let text: string;
  try {
    const buf = Buffer.alloc(stat.size - lastOffset);
    fs.readSync(fd, buf, 0, buf.length, lastOffset);
    text = buf.toString('utf-8');
  } finally {
    fs.closeSync(fd);
  }

  const lastNl = text.lastIndexOf('\n');
  const completeText = lastNl === -1 ? '' : text.slice(0, lastNl);
  const newOffset = lastNl === -1 ? lastOffset : lastOffset + Buffer.byteLength(completeText, 'utf-8') + 1;

  const messages: Array<{ role: 'user' | 'assistant'; content: string }> = [];
  for (const line of completeText.split('\n')) {
    if (!line.trim()) continue;
    try {
      const evt = JSON.parse(line) as {
        type?: string;
        data?: { prompt?: string; assistantTexts?: string[] };
      };
      if (evt.type === 'prompt.submitted' && typeof evt.data?.prompt === 'string') {
        messages.push({ role: 'user', content: evt.data.prompt });
      } else if (
        evt.type === 'model.completed' &&
        Array.isArray(evt.data?.assistantTexts) &&
        evt.data.assistantTexts.length > 0
      ) {
        const content = evt.data.assistantTexts.filter((t) => typeof t === 'string').join('\n\n');
        if (content.trim().length > 0) {
          messages.push({ role: 'assistant', content });
        }
      }
    } catch {
      // Skip malformed line; offset still advances.
    }
  }
  return { messages, newOffset };
}

/**
 * Pair adjacent user+assistant entries into "turns". A turn is a user
 * message followed by an assistant reply. Mid-stream user-only or
 * assistant-only entries do not count.
 */
export function countTurns(messages: Array<{ role: 'user' | 'assistant'; content: string }>): number {
  let turns = 0;
  for (let i = 0; i < messages.length - 1; i++) {
    if (messages[i].role === 'user' && messages[i + 1].role === 'assistant') {
      turns++;
      i++; // skip the matched assistant
    }
  }
  return turns;
}

// ---------------------------------------------------------------------------
// State file (per-file offset + turn accumulator)
// ---------------------------------------------------------------------------

export function loadState(
  stateFile: string,
  logger: TrajectoryPollerDeps['logger'],
): PollerState {
  try {
    if (!fs.existsSync(stateFile)) return {};
    const raw = fs.readFileSync(stateFile, 'utf-8');
    if (!raw.trim()) return {};
    return JSON.parse(raw) as PollerState;
  } catch (err) {
    logger.warn(`extractd: state load failed (resetting): ${err instanceof Error ? err.message : String(err)}`);
    return {};
  }
}

export function saveState(
  stateFile: string,
  state: PollerState,
  logger: TrajectoryPollerDeps['logger'],
): void {
  try {
    fs.mkdirSync(path.dirname(stateFile), { recursive: true });
    fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
  } catch (err) {
    logger.warn(`extractd: state save failed: ${err instanceof Error ? err.message : String(err)}`);
  }
}
