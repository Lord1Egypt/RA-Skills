#!/usr/bin/env node
/**
 * awareness.js — Quirk's Background Watcher (v2)
 *
 * v2 changes: ACTIVE gateway monitoring.
 * No longer waits to be told something broke.
 * Polls openclaw status every 60s, detects WhatsApp flapping,
 * and can auto-restart the gateway if flapping persists.
 *
 * Watches:
 * - WhatsApp gateway status (active poll every 60s)
 * - X/Twitter mentions (every 5 min)
 * - Scheduled reminders from awareness-schedule.json
 *
 * Design: no AI calls, no heavy compute. Watch + decide + act.
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

const WORKSPACE = '/home/ubuntu/.openclaw/workspace';
const ALERTS_FILE = path.join(WORKSPACE, 'memory/alerts.json');
const SCHEDULE_FILE = path.join(WORKSPACE, 'memory/awareness-schedule.json');
const STATE_FILE = path.join(WORKSPACE, 'memory/awareness-state.json');

// Tuning knobs
const MENTION_POLL_INTERVAL_MS = 5 * 60 * 1000;   // 5 minutes
const GATEWAY_POLL_INTERVAL_MS = 20 * 1000;         // 20 seconds — catches fast flaps
const FLAP_THRESHOLD = 3;                            // disconnects to call it flapping
const FLAP_WINDOW_MS = 5 * 60 * 1000;               // within this window
const AUTO_RESTART_AFTER_FLAPS = 6;                  // restart gateway after this many flaps (0 = disabled)
const AUTO_RESTART_COOLDOWN_MS = 10 * 60 * 1000;    // don't restart more than once per 10 min

// ─── Alert management ────────────────────────────────────────────────────────

function loadAlerts() {
  try { return JSON.parse(fs.readFileSync(ALERTS_FILE, 'utf8')); }
  catch { return { alerts: [], lastUpdated: null }; }
}

function saveAlerts(data) {
  data.lastUpdated = new Date().toISOString();
  fs.writeFileSync(ALERTS_FILE, JSON.stringify(data, null, 2));
}

function addAlert(type, message, priority = 'normal') {
  const data = loadAlerts();

  // Dedupe — don't add same alert twice within 30 min
  const cutoff = Date.now() - 30 * 60 * 1000;
  const duplicate = data.alerts.find(a =>
    a.type === type &&
    a.message === message &&
    new Date(a.timestamp).getTime() > cutoff
  );
  if (duplicate) return false;

  data.alerts.push({
    id: `${type}-${Date.now()}`,
    type,
    message,
    priority,
    timestamp: new Date().toISOString(),
    read: false,
  });

  data.alerts = data.alerts.slice(-50); // keep last 50
  saveAlerts(data);
  console.log(`[alert] ${priority.toUpperCase()} | ${type}: ${message}`);
  return true;
}

// ─── State management ────────────────────────────────────────────────────────

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); }
  catch {
    return {
      lastMentionId: null,
      gateway: {
        lastStatus: null,       // 'linked' | 'disconnected' | 'unknown'
        disconnectTimes: [],    // timestamps of recent disconnects
        flapCount: 0,           // total flaps detected this session
        lastRestartAt: null,    // timestamp of last auto-restart
        flapAlertSent: false,   // did we already alert this flap cycle?
      },
      lastScheduleCheck: null,
    };
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// ─── Gateway monitor (ACTIVE) ────────────────────────────────────────────────

function checkGateway(state) {
  if (!state.gateway) state.gateway = {
    lastStatus: null,
    disconnectTimes: [],
    flapCount: 0,
    lastRestartAt: null,
    flapAlertSent: false,
  };

  const gw = state.gateway;

  try {
    const result = execSync('openclaw status 2>&1', { timeout: 15000 }).toString();

    // Parse WhatsApp status from the table
    // Looks for: │ WhatsApp │ ON │ OK │ linked ...
    //        or: │ WhatsApp │ ON │ ERR │ ...
    const waMatch = result.match(/WhatsApp.*?(linked|disconnected|error|ERR|OFF|unlinked)/i);
    const currentStatus = waMatch
      ? (waMatch[1].toLowerCase() === 'linked' ? 'linked' : 'disconnected')
      : 'unknown';

    const now = Date.now();

    // Transition: was linked, now not → record a disconnect event
    if (gw.lastStatus === 'linked' && currentStatus !== 'linked') {
      gw.disconnectTimes.push(now);
      console.log(`[gateway] ⚠ WhatsApp went ${gw.lastStatus} → ${currentStatus}`);
    }

    // Transition: was disconnected, now linked → note recovery
    if (gw.lastStatus === 'disconnected' && currentStatus === 'linked') {
      console.log(`[gateway] ✓ WhatsApp reconnected`);
      // If we had a flap alert, note recovery
      if (gw.flapAlertSent) {
        addAlert('gateway_recovered', 'WhatsApp gateway reconnected and stable.', 'normal');
        gw.flapAlertSent = false;
      }
    }

    // Clean disconnect times outside the flap window
    gw.disconnectTimes = gw.disconnectTimes.filter(t => t > now - FLAP_WINDOW_MS);

    // Check for flapping
    if (gw.disconnectTimes.length >= FLAP_THRESHOLD) {
      gw.flapCount++;

      if (!gw.flapAlertSent) {
        addAlert(
          'gateway_flap',
          `WhatsApp is flapping — ${gw.disconnectTimes.length} disconnects in 5 min. I'm watching it.`,
          'high'
        );
        gw.flapAlertSent = true;
      }

      // Auto-restart if enabled and threshold hit
      if (
        AUTO_RESTART_AFTER_FLAPS > 0 &&
        gw.flapCount >= AUTO_RESTART_AFTER_FLAPS &&
        (!gw.lastRestartAt || now - gw.lastRestartAt > AUTO_RESTART_COOLDOWN_MS)
      ) {
        console.log(`[gateway] 🔄 Auto-restarting gateway after ${gw.flapCount} flaps...`);
        try {
          execSync('openclaw gateway restart 2>&1', { timeout: 30000 });
          gw.lastRestartAt = now;
          gw.flapCount = 0;
          gw.disconnectTimes = [];
          gw.flapAlertSent = false;
          addAlert(
            'gateway_restarted',
            'Gateway auto-restarted after persistent WhatsApp flapping. Monitoring recovery.',
            'high'
          );
        } catch (restartErr) {
          console.log(`[gateway] restart failed: ${restartErr.message?.slice(0, 100)}`);
          addAlert('gateway_restart_failed', 'Auto-restart attempted but failed. Manual action needed.', 'high');
        }
      }
    }

    gw.lastStatus = currentStatus;
    console.log(`[gateway] WhatsApp: ${currentStatus} (disconnects in window: ${gw.disconnectTimes.length})`);

  } catch (e) {
    console.log(`[gateway] status check failed: ${e.message?.slice(0, 100)}`);
  }

  state.gateway = gw;
  return state;
}

// ─── X Mentions checker ──────────────────────────────────────────────────────

function checkMentions(state) {
  try {
    const result = execSync(`xurl mentions -n 10 2>&1`, { timeout: 15000 }).toString();
    const data = JSON.parse(result);

    if (!data.data || data.data.length === 0) return state;

    const myId = '2035841743527235584'; // quirky_qui70435
    const newMentions = data.data.filter(t => t.author_id !== myId);

    if (newMentions.length > 0) {
      const newestId = data.meta?.newest_id;
      if (newestId && newestId !== state.lastMentionId) {
        const realNew = state.lastMentionId
          ? newMentions.filter(t => BigInt(t.id) > BigInt(state.lastMentionId))
          : [];

        if (realNew.length > 0) {
          realNew.forEach(mention => {
            const preview = mention.text.slice(0, 80).replace(/\n/g, ' ');
            // Spam detection — mass mentions or known spam patterns
            const mentionCount = (mention.entities?.mentions || []).length;
            const isSpam = mentionCount > 4 ||
              /presale|fast entry|private announcement|network development|airdrop|t\.me\//i.test(mention.text);
            if (!isSpam) {
              addAlert('x_mention', `@${mention.author_id} mentioned you: "${preview}..."`, 'high');
            }
          });
        }
        state.lastMentionId = newestId;
      }
    }
  } catch (e) {
    if (!e.message?.includes('Unauthorized')) {
      console.log(`[mentions] check failed: ${e.message?.slice(0, 100)}`);
    }
  }
  return state;
}

// ─── Tweet queue checker ─────────────────────────────────────────────────────

function checkTweetQueue() {
  try {
    const result = execSync(`node ${WORKSPACE}/scripts/tweet-when-ready.js --check 2>&1`, { timeout: 30000 }).toString();
    if (result.trim()) console.log(`[tweet] ${result.trim()}`);
  } catch (e) {
    console.log(`[tweet] queue check failed: ${e.message?.slice(0, 100)}`);
  }
}

function checkMemeQueue() {
  try {
    const result = execSync(`python3 ${WORKSPACE}/scripts/meme-maker.py --check 2>&1`, { timeout: 60000 }).toString();
    if (result.trim()) console.log(`[meme] ${result.trim()}`);
  } catch (e) {
    console.log(`[meme] queue check failed: ${e.message?.slice(0, 100)}`);
  }
}

function checkFeeds() {
  try {
    const result = execSync(`/home/ubuntu/go/bin/blogwatcher scan 2>&1`, { timeout: 30000 }).toString();
    // Only alert if new articles found
    const match = result.match(/Found (\d+) new article/);
    if (match && parseInt(match[1]) > 0) {
      const articles = execSync(`/home/ubuntu/go/bin/blogwatcher articles 2>&1`, { timeout: 10000 }).toString();
      addAlert('feed_update', `${match[1]} new articles:\n${articles.slice(0, 300)}`, 'normal');
      console.log(`[feeds] ${match[1]} new articles found`);
    } else {
      console.log(`[feeds] no new articles`);
    }
  } catch (e) {
    console.log(`[feeds] check failed: ${e.message?.slice(0, 100)}`);
  }
}

// ─── Schedule checker ────────────────────────────────────────────────────────

function checkSchedule(state) {
  try {
    if (!fs.existsSync(SCHEDULE_FILE)) return state;

    const schedule = JSON.parse(fs.readFileSync(SCHEDULE_FILE, 'utf8'));
    const now = Date.now();

    for (const item of (schedule.items || [])) {
      if (item.done) continue;

      const fireAt = new Date(item.at).getTime();
      const warningAt = fireAt - (item.warnMinutes || 15) * 60 * 1000;

      if (now >= fireAt) {
        addAlert('scheduled_task', `DUE NOW: ${item.task}`, 'high');
        item.done = true;
      } else if (now >= warningAt && !item.warned) {
        const minsLeft = Math.round((fireAt - now) / 60000);
        addAlert('scheduled_task', `Due in ${minsLeft}min: ${item.task}`, 'normal');
        item.warned = true;
      }
    }

    fs.writeFileSync(SCHEDULE_FILE, JSON.stringify(schedule, null, 2));
  } catch (e) {
    console.log(`[schedule] check failed: ${e.message?.slice(0, 100)}`);
  }
  return state;
}

// ─── Entry point ─────────────────────────────────────────────────────────────

const args = process.argv.slice(2);

if (args[0] === '--poll-once') {
  let state = loadState();
  state = checkGateway(state);
  state = checkMentions(state);
  state = checkSchedule(state);
  saveState(state);
  console.log('[awareness] poll complete');
  process.exit(0);

} else if (args[0] === '--status') {
  const data = loadAlerts();
  const unread = data.alerts.filter(a => !a.read);
  console.log(`Alerts: ${data.alerts.length} total, ${unread.length} unread`);
  unread.forEach(a => console.log(`  [${a.priority}] ${a.type}: ${a.message}`));
  const state = loadState();
  if (state.gateway) {
    console.log(`\nGateway state: ${state.gateway.lastStatus} | flap count: ${state.gateway.flapCount} | disconnects in window: ${state.gateway.disconnectTimes?.length || 0}`);
  }

} else {
  // ── Daemon mode ──────────────────────────────────────────────────────────
  console.log('[awareness] v2 starting — ACTIVE monitoring mode');
  console.log(`  gateway poll: every ${GATEWAY_POLL_INTERVAL_MS / 1000}s`);
  console.log(`  mention poll: every ${MENTION_POLL_INTERVAL_MS / 1000}s`);
  console.log(`  auto-restart: after ${AUTO_RESTART_AFTER_FLAPS} flaps (0=disabled)`);

  let state = loadState();

  // Gateway: poll every 60 seconds
  function gatewayLoop() {
    state = checkGateway(state);
    state = checkSchedule(state);
    saveState(state);
  }

  // Mentions every 5 min, tweet check every cycle
  let mentionTick = 0;
  function mainLoop() {
    mentionTick++;
    state = checkGateway(state);
    state = checkSchedule(state);
    checkTweetQueue();
    checkMemeQueue();

    // Feed check every 30 min (every 30th cycle)
    if (mentionTick % 30 === 0) {
      checkFeeds();
    }

    // Mentions + replies every 5 cycles (5 min)
    if (mentionTick % 5 === 0) {
      state = checkMentions(state);
      // Auto-reply to real mentions
      try {
        execSync(`node ${WORKSPACE}/scripts/reply-bot.js --check 2>&1`, { timeout: 30000 });
      } catch(e) {
        console.log(`[reply] check failed: ${e.message?.slice(0,80)}`);
      }
    }

    saveState(state);
  }

  // Run immediately then on interval
  gatewayLoop();
  setInterval(mainLoop, GATEWAY_POLL_INTERVAL_MS);

  process.on('SIGTERM', () => {
    console.log('[awareness] shutting down');
    process.exit(0);
  });
}
