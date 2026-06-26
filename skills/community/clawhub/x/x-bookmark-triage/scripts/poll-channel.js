#!/usr/bin/env node
/**
 * knowledge-intake/poll-channel.js
 * 
 * Polls #knowledge-intake for new messages containing URLs.
 * Runs as a cron every 1-2 minutes. Tracks last-seen message ID
 * to avoid reprocessing. Calls intake-listener.js for each new message.
 * 
 * Usage: node poll-channel.js
 */

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.resolve(__dirname, '../../..');
const CHANNEL_ID = process.env.KNOWLEDGE_INTAKE_CHANNEL_ID || '1481057788590297302'; // #knowledge-intake
const STATE_FILE = path.join(WORKSPACE, 'data/knowledge-intake-poll-state.json');
const BOT_TOKEN = process.env.DISCORD_BOT_TOKEN;

if (!BOT_TOKEN) {
  console.error('[poll-channel] Missing DISCORD_BOT_TOKEN');
  process.exit(1);
}

// ── State ────────────────────────────────────────────────────────────────────

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { last_message_id: null };
  }
}

function saveState(state) {
  fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// ── Discord fetch ────────────────────────────────────────────────────────────

function fetchMessages(after) {
  const params = new URLSearchParams({ limit: '20' });
  if (after) params.set('after', after);

  const url = `https://discord.com/api/v10/channels/${CHANNEL_ID}/messages?${params}`;
  const res = spawnSync('curl', [
    '-s', '--max-time', '10',
    '-H', `Authorization: Bot ${BOT_TOKEN}`,
    url
  ]);

  try {
    return JSON.parse(res.stdout.toString());
  } catch {
    console.error('[poll-channel] Failed to parse Discord response');
    return [];
  }
}

// ── URL extraction ───────────────────────────────────────────────────────────

function extractUrls(text) {
  const urlRegex = /https?:\/\/[^\s<>"{}|\\^`[\]]+/g;
  // Also strip Discord URL embed brackets: <https://...>
  const cleaned = text.replace(/<(https?:\/\/[^>]+)>/g, '$1');
  return [...new Set(cleaned.match(urlRegex) || [])];
}

// ── Main ─────────────────────────────────────────────────────────────────────

(async () => {
  const state = loadState();
  const messages = fetchMessages(state.last_message_id);

  if (!Array.isArray(messages) || messages.length === 0) {
    // No new messages
    process.exit(0);
  }

  // Discord returns newest first; process oldest first
  const sorted = messages.sort((a, b) => BigInt(a.id) < BigInt(b.id) ? -1 : 1);
  
  // Update last_message_id to the newest we've seen
  const newLastId = sorted[sorted.length - 1].id;

  let processed = 0;
  for (const msg of sorted) {
    // Only process messages from users (not bot's own triage cards)
    if (msg.author?.bot) continue;

    const urls = extractUrls(msg.content || '');
    if (urls.length === 0) continue;

    console.log(`[poll-channel] Message ${msg.id} from ${msg.author?.username}: ${urls.length} URL(s)`);

    for (const url of urls) {
      console.log(`[poll-channel] Triaging: ${url}`);
      const result = spawnSync('node', [
        path.join(__dirname, 'triage-url.js'),
        url,
        '--source', 'manual drop'
      ], {
        env: process.env,
        timeout: 90000,
        stdio: 'inherit'
      });

      if (result.status !== 0) {
        console.error(`[poll-channel] Triage failed for ${url}`);
      }
      processed++;
    }
  }

  // Save updated state
  saveState({ last_message_id: newLastId, last_run: new Date().toISOString() });

  if (processed > 0) {
    console.log(`[poll-channel] Processed ${processed} URL(s)`);
  }
})();
