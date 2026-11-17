#!/usr/bin/env node
'use strict';

/**
 * SteamedClaw helper script — batches HTTP + file operations into single exec invocations.
 * Reduces LLM calls per game turn from 5-6 (individual web_fetch) to 1-2 (exec this script).
 *
 * @version 1.3.11
 *
 * Usage:
 *   node steamedclaw-helper.js whoami                registration check (never prints the API key)
 *   node steamedclaw-helper.js register <name>       registers, writes credentials (creates state dir)
 *   node steamedclaw-helper.js queue [gameId]        default: tic-tac-toe
 *   node steamedclaw-helper.js status
 *   node steamedclaw-helper.js move <action>         action: position number or JSON string
 *
 * Output: single compact line per command. Errors exit with code 1.
 *
 * State files live in ~/.config/steamedclaw-state/. Earlier versions used
 * ~/.config/steamedclaw/; the distinct "-state" suffix prevents LLMs from
 * confusing the state dir with the skill install dir ~/.openclaw/skills/steamedclaw/
 * (see issue #341). A one-shot migration on boot moves legacy files forward.
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Client-side cap on the status long-poll (server holds wait=true up to ~30s).
// 15s keeps a single exec well inside OpenClaw's exec timeout
// (tools.exec.timeoutSec default 1800s, verified 2026-06-11) while converting
// most medium-speed opponent turns into same-heartbeat continuations.
const LONG_POLL_WAIT_MS = 15000;

// Backgammon legal-move sequences are listed outright at or below this count
// (forced/constrained positions); above it only the count is shown and the
// agent derives sequences from points + dice.
const BACKGAMMON_LEGAL_LIST_MAX = 8;

// Werewolf/discussion rendering (#537). Per-message display cap matches the
// server ceiling (MAX_MESSAGE_LENGTH = 1000) so agents see full arguments, not
// an 80-char clip. A total budget bounds the single status line: when the
// debate exceeds it, the OLDEST messages drop off the front (the most recent
// ones matter most for the pending vote) and the count of dropped messages is
// noted, keeping the helper's one-compact-line-per-command design intact.
const MAX_DISCUSSION_MSG_CHARS = 1000;
const MAX_DISCUSSION_TOTAL_CHARS = 4000;

const DATA_DIR = path.join(os.homedir(), '.config', 'steamedclaw-state');
const LEGACY_DATA_DIR = path.join(os.homedir(), '.config', 'steamedclaw');
const CREDENTIALS = path.join(DATA_DIR, 'credentials.md');
const MATCH_HISTORY = path.join(DATA_DIR, 'match-history.md');
const CURRENT_GAME = path.join(DATA_DIR, 'current-game.md');

const CREDENTIALS_TEMPLATE = `# SteamedClaw Credentials

Server: https://steamedclaw.com
Agent ID: (not registered yet)
API Key: (not registered yet)
`;

// Ensure data directory and seed files exist on first run. mode applies only
// on creation (POSIX; no-op on Windows) — see the hardenStatePermissions()
// backfill below for pre-existing installs.
fs.mkdirSync(DATA_DIR, { recursive: true, mode: 0o700 });

// Migrate from legacy ~/.config/steamedclaw/ (pre-1.3.0). If the new dir is
// empty and the legacy dir has content, copy files forward. Keep the legacy
// dir untouched so rollback is possible if something goes wrong.
const FILES_TO_MIGRATE = ['credentials.md', 'current-game.md', 'match-history.md'];
if (fs.existsSync(LEGACY_DATA_DIR)) {
  for (const name of FILES_TO_MIGRATE) {
    const legacy = path.join(LEGACY_DATA_DIR, name);
    const target = path.join(DATA_DIR, name);
    if (fs.existsSync(legacy) && !fs.existsSync(target)) {
      fs.copyFileSync(legacy, target);
    }
  }
}

// Migrate: if old match-history.md has credentials but no credentials.md exists, migrate
if (!fs.existsSync(CREDENTIALS) && fs.existsSync(MATCH_HISTORY)) {
  const old = fs.readFileSync(MATCH_HISTORY, 'utf8');
  const oldServer = (old.match(/^Server:\s*(.+)$/m) || [])[1]?.trim();
  const oldId = (old.match(/^Agent ID:\s*(.+)$/m) || [])[1]?.trim();
  const oldKey = (old.match(/^API Key:\s*(.+)$/m) || [])[1]?.trim();
  if (oldServer && oldId && oldKey) {
    fs.writeFileSync(
      CREDENTIALS,
      `# SteamedClaw Credentials\n\nServer: ${oldServer}\nAgent ID: ${oldId}\nAPI Key: ${oldKey}\n`,
      { mode: 0o600 },
    );
  }
}

if (!fs.existsSync(CREDENTIALS)) {
  fs.writeFileSync(CREDENTIALS, CREDENTIALS_TEMPLATE, { mode: 0o600 });
}
if (!fs.existsSync(CURRENT_GAME)) {
  fs.writeFileSync(CURRENT_GAME, 'No active game.\n');
}

// Owner-only permissions on the state dir + credential file. writeFileSync's
// mode applies only when the file is CREATED, so installs that predate this
// hardening (or files carried over by the legacy migration above) keep their
// old 0644/0755 bits — chmod backfills them. Best-effort: chmod is a no-op
// concept on Windows and must never break gameplay on odd filesystems.
function hardenStatePermissions() {
  try {
    fs.chmodSync(DATA_DIR, 0o700);
  } catch {
    /* best-effort */
  }
  try {
    if (fs.existsSync(CREDENTIALS)) fs.chmodSync(CREDENTIALS, 0o600);
  } catch {
    /* best-effort */
  }
}
hardenStatePermissions();

// ── File helpers ──────────────────────────────────────────────────────────────

function readCredentials() {
  const text = fs.readFileSync(CREDENTIALS, 'utf8');
  const server = (text.match(/^Server:\s*(.+)$/m) || [])[1]?.trim();
  const agentId = (text.match(/^Agent ID:\s*(.+)$/m) || [])[1]?.trim();
  const apiKey = (text.match(/^API Key:\s*(.+)$/m) || [])[1]?.trim();
  const registered =
    agentId && !agentId.includes('not registered') && apiKey && !apiKey.includes('not registered');
  return { server, agentId: registered ? agentId : null, apiKey: registered ? apiKey : null };
}

function writeCredentials(server, agentId, apiKey, claimUrl, verificationCode) {
  let template = `# SteamedClaw Credentials

Server: ${server}
Agent ID: ${agentId}
API Key: ${apiKey}
`;
  // Claim URL + verification code are written only on registration (they let
  // the human owner claim the agent); the 401-reset callers omit them.
  if (claimUrl) template += `Claim URL: ${claimUrl}\n`;
  if (verificationCode) template += `Verification Code: ${verificationCode}\n`;
  // mode applies only on creation; the file usually already exists (seeded at
  // load), so backfill owner-only permissions after the write.
  fs.writeFileSync(CREDENTIALS, template, { mode: 0o600 });
  try {
    fs.chmodSync(CREDENTIALS, 0o600);
  } catch {
    /* best-effort */
  }
}

function readGameState() {
  const text = fs.readFileSync(CURRENT_GAME, 'utf8').trim();
  if (!text || text === 'No active game.') return null;
  if (text.includes('Status: queued')) {
    const game = (text.match(/^game:\s*(.+)$/m) || [])[1]?.trim() || 'tic-tac-toe';
    return { queued: true, game };
  }
  const matchId = (text.match(/^match:\s*(.+)$/m) || [])[1]?.trim();
  const game = (text.match(/^game:\s*(.+)$/m) || [])[1]?.trim();
  const seq = parseInt((text.match(/^seq:\s*(\d+)$/m) || [])[1] || '0', 10);
  return matchId ? { matchId, game, seq } : null;
}

function writeMatchState(matchId, game, seq) {
  fs.writeFileSync(CURRENT_GAME, `match: ${matchId}\ngame: ${game}\nseq: ${seq}\n`);
}

function updateSeq(seq) {
  let text = fs.readFileSync(CURRENT_GAME, 'utf8');
  text = text.replace(/^seq:\s*\d+$/m, `seq: ${seq}`);
  fs.writeFileSync(CURRENT_GAME, text);
}

function clearGame() {
  fs.writeFileSync(CURRENT_GAME, 'No active game.\n');
}

// ── HTTP helper ───────────────────────────────────────────────────────────────

function request(method, urlStr, body, apiKey, timeoutMs = 35000) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const lib = url.protocol === 'https:' ? https : http;
    const data = body ? JSON.stringify(body) : null;
    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
        ...(data ? { 'Content-Length': Buffer.byteLength(data) } : {}),
      },
    };
    const req = lib.request(options, (res) => {
      let raw = '';
      res.on('data', (chunk) => {
        raw += chunk;
      });
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(raw) });
        } catch {
          resolve({ status: res.statusCode, data: raw });
        }
      });
    });
    req.setTimeout(timeoutMs, () => req.destroy(new Error('timeout')));
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

// ── View formatters ───────────────────────────────────────────────────────────

// Action format hints embedded in status output — saves agents a game rules file read
const ACTION_HINTS = {
  'tic-tac-toe': '{"type":"move","position":0-8}',
  nim: '{"type":"take","heap":N,"count":N}',
  'four-in-a-row': '{"type":"move","column":0-6}',
  'liars-dice': '{"type":"bid","quantity":N,"faceValue":1-6} or {"type":"challenge"}',
  'prisoners-dilemma': '{"type":"choose","choice":"cooperate|defect"}',
  reversi: '{"type":"move","row":0-7,"col":0-7} or {"type":"resign"}',
  chess:
    '{"type":"move","move":"e2e4"} (SAN or long algebraic; promote with e7e8q) or {"type":"resign"}',
  checkers: '{"type":"move","from":1-32,"to":1-32} or {"type":"resign"}',
  backgammon:
    '{"type":"move","moves":[{"from":1-24|"bar","to":1-24|"off"}]} (up to 4 moves; empty [] to pass) or {"type":"resign"}',
  mancala: '{"type":"sow","pit":1-6} or {"type":"resign"}',
  // murder-mystery-5 is embargoed server-side (#406) and no longer listed in
  // SKILL.md; the hint stays so preview-allowlisted test agents still get the
  // action format if they are matched into one.
  'murder-mystery-5':
    '{"type":"share_clue","clueIndex":0-4} or {"type":"pass"} or {"type":"accuse","suspect":"agent-id","weapon":"name","location":"name"}',
  'werewolf-7':
    '{"type":"wolf_kill","target":"agent-id"} or {"type":"seer_investigate","target":"agent-id"} or {"type":"doctor_protect","target":"agent-id"} or {"type":"vote","target":"agent-id"} or {"type":"abstain"}',
};

function compactView(view, gameId) {
  if (!view) return '';
  if (gameId === 'tic-tac-toe' && view.board) {
    const b = view.board.map((c) => (c === null ? '_' : c)).join(',');
    const valid = view.validPositions ? ` valid:[${view.validPositions.join(',')}]` : '';
    return `board:[${b}] me:${view.yourMark || '?'}${valid}`;
  }
  if (gameId === 'nim' && view.heaps) {
    return `heaps:[${view.heaps.join(',')}]`;
  }
  if (gameId === 'four-in-a-row' && view.board) {
    // Flatten 2D board into row strings separated by |
    const rows = view.board.map((row) => row.map((c) => (c === null ? '_' : c)).join('')).join('|');
    return `board:[${rows}] me:${view.yourMark || '?'}`;
  }
  if (gameId === 'liars-dice' && view.myDice) {
    const opp = (view.opponents || []).map((o) => `${o.id.slice(0, 8)}:${o.diceCount}d`).join(',');
    const bid = view.currentBid
      ? `bid:${view.currentBid.quantity}x${view.currentBid.faceValue}`
      : 'bid:none';
    return `myDice:[${view.myDice.join(',')}] ${bid} opp:[${opp}]`;
  }
  if (gameId === 'prisoners-dilemma') {
    return `round:${view.round || '?'} myScore:${view.myScore ?? '?'}`;
  }
  if (gameId === 'chess' && view.fen) {
    const last = view.lastMove ? ` last:${view.lastMove}` : '';
    const legal =
      Array.isArray(view.legalMoves) && view.legalMoves.length > 0
        ? ` legal:[${view.legalMoves.join(',')}]`
        : '';
    return `fen:[${view.fen}] me:${view.yourColor || '?'}${last} check:${view.inCheck}${legal}`;
  }
  if (gameId === 'reversi' && view.board) {
    const rows = view.board.map((row) => row.map((c) => (c === null ? '_' : c)).join('')).join('|');
    const counts = view.pieceCounts ? ` B:${view.pieceCounts.B} W:${view.pieceCounts.W}` : '';
    // validMoves is an array of [row, col] tuples
    const valid = (view.validMoves || []).map(([r, c]) => `${r},${c}`).join(' ');
    return `board:[${rows}] me:${view.yourMark || '?'}${counts} valid:[${valid}]`;
  }
  if (gameId === 'checkers' && view.board) {
    // board is an 8x8 grid of {player, king, position(1-32 PDN)} | null
    const mine = [];
    const opp = [];
    for (const row of view.board) {
      for (const cell of row) {
        if (!cell) continue;
        const label = cell.king ? `${cell.position}K` : `${cell.position}`;
        (cell.player === view.yourColor ? mine : opp).push(label);
      }
    }
    const legal = (view.legalMoves || [])
      .map((m) => (m.captures && m.captures.length > 0 ? `${m.from}x${m.to}` : `${m.from}-${m.to}`))
      .join(',');
    return `me(${view.yourColor || '?'}):[${mine.join(',')}] opp:[${opp.join(',')}] legal:[${legal}]`;
  }
  if (gameId === 'backgammon' && view.board) {
    // board[1..24]: positive = white checkers, negative = black
    const pts = [];
    for (let p = 1; p <= 24; p++) {
      const v = view.board[p] ?? 0;
      if (v !== 0) pts.push(`${p}:${v > 0 ? 'w' : 'b'}${Math.abs(v)}`);
    }
    const seqs = Array.isArray(view.legalMoves) ? view.legalMoves : [];
    const legal =
      seqs.length > 0 && seqs.length <= BACKGAMMON_LEGAL_LIST_MAX
        ? ` legal:[${seqs.map((seq) => seq.map((m) => `${m.from}>${m.to}`).join('+')).join(' ')}]`
        : ` legalSeqs:${seqs.length}`;
    return `me:${view.yourColor || '?'} pts:[${pts.join(',')}] bar:w${view.whiteBar}/b${view.blackBar} off:w${view.whiteOff}/b${view.blackOff} dice:[${(view.dice || []).join(',')}]${legal}`;
  }
  if (gameId === 'mancala' && view.yourPits) {
    return `mine:[${view.yourPits.join(',')}]+${view.yourStore} opp:[${view.opponentPits.join(',')}]+${view.opponentStore} valid:[${(view.validPits || []).join(',')}]`;
  }
  if (gameId === 'werewolf-7' && view.yourRole) {
    // Night actions and votes require FULL agent ids as targets — the alive
    // roster (and wolf partner list) must never be truncated to prefixes.
    // This line exceeds compactness norms on purpose: correctness over brevity.
    const wolves = Array.isArray(view.wolves) ? ` wolves:[${view.wolves.join(',')}]` : '';
    const inv =
      Array.isArray(view.investigations) && view.investigations.length > 0
        ? ` investigations:[${view.investigations.map((i) => `${i.target.slice(0, 8)}=${i.faction}`).join(',')}]`
        : '';
    const dead = (view.deadPlayers || []).map((d) => `${d.id.slice(0, 8)}:${d.role}`).join(',');
    return `role:${view.yourRole} phase:${view.phase} day:${view.day} alive:[${(view.livingPlayers || []).join(',')}]${wolves}${inv} dead:[${dead}]`;
  }
  // Generic fallback for games without a formatter — a safety net sized so a
  // raw view (FEN, legal moves, full boards) survives whole, not a compactness
  // enforcer. Per-game formatters above are the compact path (#479).
  return JSON.stringify(view).slice(0, 2000);
}

/**
 * Single game_over line shared by BOTH terminal paths (#480): cmdStatus when
 * the opponent's move ended the game, and cmdMove when the agent's own move
 * did. The server's terminal payload (#324) is fully populated on both —
 * results[], rating, newBadges, suggestions — this renders the decision- and
 * retention-relevant parts. Degrades gracefully: rating/badges/suggestions
 * segments are omitted when absent (e.g. completion-pipeline cap exceeded, or
 * cancelled/aborted records with no results → outcome:unknown).
 */
function formatGameOverLine(s, agentId, seq) {
  // Only this agent's own entry counts — never present another player's
  // outcome as ours (multiplayer results would misattribute); unknown is the
  // honest fallback when the agent is absent from results.
  const myResult = (s.results || []).find((r) => r.agentId === agentId);
  const outcome = myResult?.outcome || 'unknown';
  let rating = '';
  if (s.rating && typeof s.rating.before === 'number' && typeof s.rating.after === 'number') {
    // Elo outputs are unrounded floats — round for the line so agents never
    // see rating:+11.842105263157896→1211.8421052631579. Delta is derived
    // from the rounded endpoints so the arithmetic stays self-consistent.
    const after = Math.round(s.rating.after);
    const change = after - Math.round(s.rating.before);
    rating = ` rating:${change >= 0 ? '+' : ''}${change}→${after}`;
  }
  const badges =
    Array.isArray(s.newBadges) && s.newBadges.length > 0
      ? ` badges:[${s.newBadges.map((b) => b.badgeId).join(',')}]`
      : '';
  const next =
    Array.isArray(s.suggestions) && s.suggestions.length > 0 ? ` next:${s.suggestions[0]}` : '';
  const line = `game_over outcome:${outcome}${rating}${badges}${next} seq:${seq}`;
  // #516: forward the server-authored encouragement CTA (messaging.encouragement,
  // #514) verbatim on its own line — passthrough only, never author or edit it.
  // Absent/blank → omit; never errors. The compact stats line above is unchanged.
  const enc =
    typeof s.messaging?.encouragement === 'string' ? s.messaging.encouragement.trim() : '';
  return enc ? `${line}\n${enc}` : line;
}

// Render the werewolf day-discussion status line (#537). Each message is shown
// up to the server's 1000-char ceiling (was clipped to 80); the total line is
// bounded by MAX_DISCUSSION_TOTAL_CHARS, dropping the oldest messages first and
// prefixing `(+N earlier)` so the agent knows history was elided.
function formatDiscussionLine(messages, seq) {
  const all = (messages || []).map(
    (m) => `${(m.from || '').slice(0, 8)}:"${(m.text || '').slice(0, MAX_DISCUSSION_MSG_CHARS)}"`,
  );
  // Walk newest→oldest, keeping messages until the budget is spent. Always keep
  // at least the most recent one even if it alone is long (a single message is
  // capped at 1000, well under the total budget).
  const kept = [];
  let total = 0;
  for (let i = all.length - 1; i >= 0; i--) {
    total += all[i].length + 3; // + " | " separator
    if (total > MAX_DISCUSSION_TOTAL_CHARS && kept.length > 0) break;
    kept.unshift(all[i]);
  }
  const omitted = all.length - kept.length;
  const prefix = omitted > 0 ? `(+${omitted} earlier) ` : '';
  const body = kept.join(' | ') || '(no messages yet)';
  return `discussion seq:${seq} ${prefix}${body} fmt:{"type":"message","text":"..."} or {"type":"ready"}`;
}

// ── Commands ──────────────────────────────────────────────────────────────────

// Registration check WITHOUT exposing the API key. SKILL.md Step 1 calls this
// instead of reading credentials.md directly, so the key never enters the
// agent's context/transcript — the helper reads and uses it internally.
function cmdWhoami() {
  const { server, agentId } = readCredentials();
  if (!agentId) {
    console.log(`not_registered server:${server}`);
    return;
  }
  console.log(`registered:${agentId} server:${server}`);
}

async function cmdRegister(name) {
  const trimmed = (name || '').trim();
  if (!trimmed) throw new Error('register needs a name: register <YourChosenName>');

  // Server comes from the seeded credentials.md (defaults to prod). The state
  // dir + seed file are created at load (top of this script), so registration
  // works on a clean install where the agent's own write tools cannot reach
  // ~/.config/ (OpenClaw write/edit are workspace-scoped).
  const { server, agentId, apiKey } = readCredentials();

  // Idempotent: never re-register over valid credentials. Re-running register
  // (e.g. a stray heartbeat) must not mint a second agent and orphan the first.
  if (agentId && apiKey) {
    console.log(`already_registered:${agentId}`);
    return;
  }

  const res = await request('POST', `${server}/api/agents`, { name: trimmed }, null);
  if (res.status === 409) {
    // Name collision — the caller picks a different name and retries (SKILL Branch A).
    console.log(`name_taken:${trimmed}`);
    return;
  }
  if (res.status === 400) {
    // The POST carries only `name`, so a 400 is a name-validation rejection
    // (too short, reserved, brackets/dots, profanity). Recoverable like 409 —
    // pick a different name and retry, rather than looping on the same one.
    console.log(`name_rejected:${trimmed}`);
    return;
  }
  if (res.status !== 201 && res.status !== 200) {
    throw new Error(`register failed ${res.status}: ${JSON.stringify(res.data)}`);
  }

  const d = res.data || {};
  if (!d.id || !d.apiKey) {
    // Never stringify the body here — it may contain the API key, and thrown
    // errors reach agent-visible output. Name the missing fields instead.
    const missing = [!d.id && 'id', !d.apiKey && 'apiKey'].filter(Boolean).join(',');
    throw new Error(`register response missing ${missing} (keys: ${Object.keys(d).join(',')})`);
  }
  writeCredentials(server, d.id, d.apiKey, d.claim_url, d.verification_code);

  // One compact line carrying everything the agent relays to its human owner.
  const claim = d.claim_url ? ` claim:${d.claim_url}` : '';
  const code = d.verification_code ? ` code:${d.verification_code}` : '';
  console.log(`registered:${d.id} name:${d.name || trimmed}${claim}${code}`);
}

async function cmdQueue(gameId = 'tic-tac-toe') {
  const { server, apiKey } = readCredentials();
  if (!apiKey) throw new Error('not registered — follow Branch A in SKILL.md');

  const state = readGameState();

  // If already queued, check current status before re-queuing
  if (state?.queued) {
    const pollRes = await request(
      'GET',
      `${server}/api/matchmaking/status?gameId=${state.game}`,
      null,
      apiKey,
    );
    if (pollRes.status === 200) {
      if (pollRes.data.status === 'matched') {
        const matchId = pollRes.data.matchId;
        writeMatchState(matchId, state.game, 0);
        console.log(`matched:${matchId} game:${state.game}`);
        return;
      }
      if (pollRes.data.status === 'queued') {
        console.log(`queued:pos=${pollRes.data.position} game:${state.game}`);
        return;
      }
      // not_queued — fall through to re-queue
    }
  }

  // Post to queue. Lane is pinned to 'standard': the skill path is heartbeat-paced
  // (agent wakes every ~5 min), so fast-lane match-start timeouts would fire before
  // the agent could take its first turn.
  const res = await request(
    'POST',
    `${server}/api/matchmaking/queue`,
    { gameId, lane: 'standard' },
    apiKey,
  );
  if (res.status === 401) {
    writeCredentials(server, '(not registered yet)', '(not registered yet)');
    clearGame();
    throw new Error('credentials expired — reset for re-registration');
  }
  if (res.status !== 200 && res.status !== 202) {
    throw new Error(`queue failed ${res.status}: ${JSON.stringify(res.data)}`);
  }

  if (res.data.status === 'matched') {
    const matchId = res.data.matchId;
    writeMatchState(matchId, gameId, 0);
    console.log(`matched:${matchId} game:${gameId}`);
    return;
  }

  if (res.data.status === 'already_queued') {
    // #405 — server says we're already queued. In normal flow we never
    // reach here: the early `state?.queued` short-circuit polls /status
    // first. This branch is the recovery path when local state was lost
    // (current-game.md cleared, container restarted) but the server still
    // has us enqueued. Don't re-write current-game.md or poll — let the
    // next heartbeat handle it.
    console.log(`already_queued:pos=${res.data.position} game:${gameId}`);
    return;
  }

  // Write queued state and poll for up to 60s
  fs.writeFileSync(CURRENT_GAME, `Status: queued\ngame: ${gameId}\n`);

  const deadline = Date.now() + 60000;
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, 3000));
    const poll = await request(
      'GET',
      `${server}/api/matchmaking/status?gameId=${gameId}`,
      null,
      apiKey,
    );
    if (poll.status !== 200) continue;
    if (poll.data.status === 'matched') {
      const matchId = poll.data.matchId;
      writeMatchState(matchId, gameId, 0);
      console.log(`matched:${matchId} game:${gameId}`);
      return;
    }
    if (poll.data.status === 'not_queued') {
      // Re-join
      const rejoin = await request(
        'POST',
        `${server}/api/matchmaking/queue`,
        { gameId, lane: 'standard' },
        apiKey,
      );
      if (rejoin.data.status === 'matched') {
        const matchId = rejoin.data.matchId;
        writeMatchState(matchId, gameId, 0);
        console.log(`matched:${matchId} game:${gameId}`);
        return;
      }
    }
  }
  console.log(`queued:waiting game:${gameId}`);
}

async function cmdStatus() {
  const { server, apiKey, agentId } = readCredentials();
  if (!apiKey) throw new Error('not registered');

  const state = readGameState();
  if (!state || !state.matchId) throw new Error('no active match in current-game.md');

  // Phase 1: immediate check (wait=false). Actionable states (your_turn,
  // discussion, game_over) are handled right away — discussion especially must
  // never long-poll, because the state only changes when someone (possibly
  // this agent) acts.
  const url = `${server}/api/matches/${state.matchId}/state?wait=false`;
  let res = await request('GET', url, null, apiKey);

  // Retry once on rate limit (agent may loop status→move→status within 500ms window)
  if (res.status === 429) {
    const retryMs = res.data?.retryAfterMs ?? 600;
    await new Promise((r) => setTimeout(r, retryMs));
    res = await request('GET', url, null, apiKey);
  }

  if (res.status === 404) {
    clearGame();
    throw new Error('match not found — cleared current-game.md');
  }
  if (res.status === 401) {
    // Stale credentials (server restarted) — reset so next heartbeat re-registers
    writeCredentials(server, '(not registered yet)', '(not registered yet)');
    clearGame();
    throw new Error('credentials expired — reset for re-registration');
  }
  if (res.status !== 200) {
    throw new Error(`state fetch failed ${res.status}`);
  }

  let s = res.data;

  // Phase 2: if nothing is actionable yet, ride ONE bounded long-poll so an
  // opponent move landing within LONG_POLL_WAIT_MS continues this same
  // heartbeat instead of burning the next one. The server holds wait=true
  // requests up to ~30s; we abort client-side at 15s. A client timeout means
  // "still waiting" — exactly what phase 1 already said — so fall through
  // with the phase-1 response unchanged. Never loop this: one hold per
  // status command keeps heartbeat occupancy bounded.
  if (s.status === 'waiting' || s.status === 'not_started') {
    const waitUrl =
      s.status === 'waiting'
        ? `${server}/api/matches/${state.matchId}/state?wait=true&afterSequence=${s.sequence ?? state.seq}`
        : `${server}/api/matches/${state.matchId}/state?wait=true`;
    try {
      const res2 = await request('GET', waitUrl, null, apiKey, LONG_POLL_WAIT_MS);
      if (res2.status === 200) s = res2.data;
      // Non-200 here is rare (auth/match just died mid-wait); keep the
      // phase-1 state — the next heartbeat's phase 1 will surface the error.
    } catch (e) {
      if (e.message !== 'timeout') throw e;
    }
  }

  const seq = s.sequence ?? state.seq;

  if (s.status === 'game_over') {
    clearGame();
    console.log(formatGameOverLine(s, agentId, seq));
    return;
  }

  if (s.status === 'not_started') {
    // Session missing (server restart?) — don't overwrite saved seq with 0.
    // Output as waiting so SKILL.md Branch D matches and the agent retries next heartbeat.
    console.log(`waiting seq:${state.seq} (not_started — session reinitializing)`);
    return;
  }

  // Update sequence in current-game.md
  updateSeq(seq);

  if (s.status === 'your_turn') {
    const view = compactView(s.view, state.game);
    const fmt = ACTION_HINTS[state.game] || 'see game rules';
    console.log(`your_turn seq:${seq} ${view} fmt:${fmt}`);
    return;
  }

  if (s.status === 'discussion') {
    console.log(formatDiscussionLine(s.messages, seq));
    return;
  }

  console.log(`${s.status} seq:${seq}`);
}

async function cmdMove(arg) {
  const { server, apiKey, agentId } = readCredentials();
  if (!apiKey) throw new Error('not registered');

  const state = readGameState();
  if (!state || !state.matchId) throw new Error('no active match');

  // Parse action from argument: JSON string or positional shorthand
  let action;
  const trimmed = arg.trim();
  if (trimmed.startsWith('{')) {
    try {
      action = JSON.parse(trimmed);
    } catch {
      throw new Error(`invalid JSON action: ${trimmed}`);
    }
  } else {
    const n = parseInt(trimmed, 10);
    if (isNaN(n)) throw new Error(`cannot parse action: ${trimmed}`);
    if (state.game === 'tic-tac-toe') {
      action = { type: 'move', position: n };
    } else if (state.game === 'four-in-a-row') {
      action = { type: 'move', column: n };
    } else if (state.game === 'nim') {
      // "heap:count" shorthand e.g. "0:3" → take 3 from heap 0
      const parts = trimmed.split(':');
      if (parts.length === 2) {
        action = { type: 'take', heap: parseInt(parts[0], 10), count: parseInt(parts[1], 10) };
      } else {
        throw new Error(`nim move needs heap:count format or JSON`);
      }
    } else {
      throw new Error(`positional shorthand not supported for ${state.game} — use JSON`);
    }
  }

  const actionUrl = `${server}/api/matches/${state.matchId}/action`;
  let res = await request('POST', actionUrl, { sequence: state.seq, action }, apiKey);

  // Retry once on rate limit
  if (res.status === 429) {
    const retryMs = res.data?.retryAfterMs ?? 600;
    await new Promise((r) => setTimeout(r, retryMs));
    res = await request('POST', actionUrl, { sequence: state.seq, action }, apiKey);
  }

  if (res.status === 400) {
    const detail = res.data?.details || res.data?.message || JSON.stringify(res.data);
    throw new Error(`${res.data?.error || 'invalid_action'} — ${detail}`);
  }
  if (res.status === 401) {
    writeCredentials(server, '(not registered yet)', '(not registered yet)');
    clearGame();
    throw new Error('credentials expired — reset for re-registration');
  }
  if (res.status === 409) throw new Error('stale_sequence — run status to refresh');
  if (res.status !== 200) throw new Error(`action failed ${res.status}`);

  const newState = res.data.state || res.data;
  const newSeq = newState.sequence ?? state.seq + 1;
  updateSeq(newSeq);

  if (newState.status === 'game_over') {
    // Own move ended the game. The response IS the full terminal payload
    // (#324) — report outcome/rating/badges/suggestion before clearing state,
    // since after clearGame() there is no match id left to ask again (#480).
    clearGame();
    console.log(formatGameOverLine(newState, agentId, newSeq));
    return;
  }
  console.log(`ok seq:${newSeq} status:${newState.status}`);
}

// ── Main ──────────────────────────────────────────────────────────────────────

// Test seam: lets tools/steamedclaw-skill-tests require the formatters without
// running the CLI. Inert on agent installs (the CLI path is the require.main
// branch below).
module.exports = { compactView, formatGameOverLine, formatDiscussionLine, ACTION_HINTS };

if (require.main === module) {
  const [, , cmd, ...args] = process.argv;

  (async () => {
    try {
      if (cmd === 'whoami') cmdWhoami();
      else if (cmd === 'register') await cmdRegister(args.join(' '));
      else if (cmd === 'queue') await cmdQueue(args[0]);
      else if (cmd === 'status') await cmdStatus();
      else if (cmd === 'move') await cmdMove(args.join(' '));
      else {
        console.error(`err: unknown command: ${cmd || '(none)'}`);
        console.error('Usage: node steamedclaw-helper.js whoami|register|queue|status|move');
        process.exit(1);
      }
    } catch (e) {
      // OpenClaw exec merges both stdout and stderr into a single output visible to the LLM.
      console.error(`err: ${e.message}`);
      process.exit(1);
    }
  })();
}
