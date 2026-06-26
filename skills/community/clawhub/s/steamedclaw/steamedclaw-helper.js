#!/usr/bin/env node
'use strict';

/**
 * SteamedClaw helper script — batches HTTP + file operations into single exec invocations.
 * Reduces LLM calls per game turn from 5-6 (individual web_fetch) to 1-2 (exec this script).
 *
 * @version 1.3.4
 *
 * Usage:
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

// Ensure data directory and seed files exist on first run
fs.mkdirSync(DATA_DIR, { recursive: true });

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
    );
  }
}

if (!fs.existsSync(CREDENTIALS)) {
  fs.writeFileSync(CREDENTIALS, CREDENTIALS_TEMPLATE);
}
if (!fs.existsSync(CURRENT_GAME)) {
  fs.writeFileSync(CURRENT_GAME, 'No active game.\n');
}

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

function writeCredentials(server, agentId, apiKey) {
  const template = `# SteamedClaw Credentials

Server: ${server}
Agent ID: ${agentId}
API Key: ${apiKey}
`;
  fs.writeFileSync(CREDENTIALS, template);
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
  mancala: '{"type":"sow","pit":0-5} or {"type":"resign"}',
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
  // Generic fallback — truncate to keep output compact
  return JSON.stringify(view).slice(0, 200);
}

// ── Commands ──────────────────────────────────────────────────────────────────

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

  // Poll with wait=false only — afterSequence is ignored by the server in this mode.
  // Sequence tracking is only needed for the action endpoint's optimistic concurrency.
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

  const s = res.data;
  const seq = s.sequence ?? state.seq;

  if (s.status === 'game_over') {
    clearGame();
    const myResult = (s.results || []).find((r) => r.agentId === agentId) || (s.results || [])[0]; // fallback if agentId not in results
    const outcome = myResult?.outcome || 'unknown';
    let rating = '';
    if (s.rating && typeof s.rating.before === 'number' && typeof s.rating.after === 'number') {
      const change = s.rating.after - s.rating.before;
      rating = ` rating:${change >= 0 ? '+' : ''}${change}→${s.rating.after}`;
    }
    console.log(`game_over outcome:${outcome}${rating} seq:${seq}`);
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
    const msgs = (s.messages || [])
      .map((m) => `${m.from.slice(0, 8)}:"${m.text.slice(0, 80)}"`)
      .join(' | ');
    console.log(
      `discussion seq:${seq} ${msgs || '(no messages yet)'} fmt:{"type":"message","text":"..."} or {"type":"ready"}`,
    );
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
    clearGame();
    console.log(`game_over seq:${newSeq}`);
    return;
  }
  console.log(`ok seq:${newSeq} status:${newState.status}`);
}

// ── Main ──────────────────────────────────────────────────────────────────────

const [, , cmd, ...args] = process.argv;

(async () => {
  try {
    if (cmd === 'queue') await cmdQueue(args[0]);
    else if (cmd === 'status') await cmdStatus();
    else if (cmd === 'move') await cmdMove(args.join(' '));
    else {
      console.error(`err: unknown command: ${cmd || '(none)'}`);
      console.error('Usage: node steamedclaw-helper.js queue|status|move');
      process.exit(1);
    }
  } catch (e) {
    // OpenClaw exec merges both stdout and stderr into a single output visible to the LLM.
    console.error(`err: ${e.message}`);
    process.exit(1);
  }
})();
