#!/usr/bin/env node
/**
 * session-scribe — summarize OpenClaw session transcripts into daily memory files.
 *
 * Single session:
 *   node scribe.js --sessions ~/.openclaw/agents/main/sessions \
 *                  --session-id <uuid> \
 *                  --memory-dir ~/.openclaw/workspace/memory
 *
 * Auto-resolve by key suffix:
 *   node scribe.js --sessions ~/.openclaw/agents/main/sessions \
 *                  --auto-session "discord:channel:1234567890" \
 *                  --memory-dir ~/.openclaw/workspace/memory
 *
 * All sessions across all agents:
 *   node scribe.js --agents-dir ~/.openclaw/agents \
 *                  --all-sessions \
 *                  --memory-dir ~/.openclaw/workspace/memory
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// ── CLI args ──────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const get = (flag) => { const i = args.indexOf(flag); return i !== -1 ? args[i + 1] : null; };
const has = (flag) => args.includes(flag);

const sessionsDir  = get('--sessions');
const agentsDir    = get('--agents-dir');
const sessionIdArg = get('--session-id');
const autoSession  = get('--auto-session');
const allSessions  = has('--all-sessions');
const memoryDir    = get('--memory-dir');
const model        = get('--model') || 'gpt-4o-mini';
const agentLabel   = get('--agent') || 'agent';
const dryRun       = has('--dry-run');
const minTurns     = parseInt(get('--min-turns') || '3', 10);
// Only scribe sessions active within this window (default 1h — matches cron frequency)
const activeWithinHours = parseFloat(get('--active-within-hours') || '1');

// Provider: auto-detect from env, or explicit --provider
const provider = get('--provider') || (process.env.OPENAI_API_KEY ? 'openai' : 'anthropic');

// API key
let apiKey = process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY || get('--api-key');
const apiKeyFile = get('--api-key-file');
if (!apiKey && apiKeyFile) {
  try { apiKey = fs.readFileSync(apiKeyFile, 'utf8').trim(); }
  catch (e) { console.error('Failed to read api key file:', e.message); process.exit(1); }
}

// Validation
if (!memoryDir) { console.error('Error: --memory-dir required'); process.exit(1); }
if (!apiKey)    { console.error('Error: No API key. Set OPENAI_API_KEY or ANTHROPIC_API_KEY'); process.exit(1); }
if (allSessions && !agentsDir) { console.error('Error: --all-sessions requires --agents-dir'); process.exit(1); }
if (!allSessions && !sessionsDir) { console.error('Error: --sessions required (or use --all-sessions with --agents-dir)'); process.exit(1); }
if (!allSessions && !sessionIdArg && !autoSession) { console.error('Error: --session-id, --auto-session, or --all-sessions required'); process.exit(1); }

// ── State ─────────────────────────────────────────────────────────────────────

const stateFile = path.join(path.dirname(__filename), '.scribe-state.json');

function loadState() {
  try { return JSON.parse(fs.readFileSync(stateFile, 'utf8')); }
  catch { return {}; }
}

function saveState(state) {
  fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
}

// ── Session discovery ─────────────────────────────────────────────────────────

function loadSessionsJson(dir) {
  const file = path.join(dir, 'sessions.json');
  if (!fs.existsSync(file)) return {};
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch { return {}; }
}

function resolveSessionId(dir) {
  if (sessionIdArg) return { sessionId: sessionIdArg, label: sessionIdArg.slice(0, 8) };
  const sessions = loadSessionsJson(dir);
  const match = Object.entries(sessions).find(([key]) => key.includes(autoSession));
  if (!match) {
    console.error(`No session matching: ${autoSession}`);
    return null;
  }
  return { sessionId: match[1].sessionId, label: match[0] };
}

// Returns array of { agentId, sessionId, sessionKey, lastActivity } across all agents
function discoverAllSessions() {
  const results = [];
  // Only sessions active within the window (since last cron run)
  const activeSince = Date.now() - activeWithinHours * 3600 * 1000;

  const agentDirs = fs.readdirSync(agentsDir, { withFileTypes: true })
    .filter(e => e.isDirectory())
    .map(e => e.name);

  for (const agentId of agentDirs) {
    const dir = path.join(agentsDir, agentId, 'sessions');
    if (!fs.existsSync(dir)) continue;

    const sessions = loadSessionsJson(dir);
    for (const [key, entry] of Object.entries(sessions)) {
      if (!entry.sessionId) continue;

      // Use transcript file mtime as activity signal (lastActivityMs not always populated)
      const transcriptMtime = (() => {
        try { return fs.statSync(path.join(dir, `${entry.sessionId}.jsonl`)).mtimeMs; }
        catch { return 0; }
      })();
      const lastActivity = entry.lastActivityMs || entry.updatedAtMs || transcriptMtime;
      if (!lastActivity || lastActivity < activeSince) continue;

      // Skip cron/isolated sessions — only scribe real conversations
      if (key.includes(':cron:') || key.includes(':slash:')) continue;

      // Check transcript exists
      const transcriptFile = path.join(dir, `${entry.sessionId}.jsonl`);
      if (!fs.existsSync(transcriptFile)) continue;

      results.push({
        agentId,
        sessionsDir: dir,
        sessionId: entry.sessionId,
        sessionKey: key,
        lastActivity,
      });
    }
  }

  return results;
}

// ── Transcript reading ────────────────────────────────────────────────────────

function readTranscript(dir, sessionId) {
  const file = path.join(dir, `${sessionId}.jsonl`);
  if (!fs.existsSync(file)) return [];

  return fs.readFileSync(file, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map(line => { try { return JSON.parse(line); } catch { return null; } })
    .filter(Boolean);
}

function extractTurns(entries, afterIndex = 0) {
  const turns = [];
  entries.slice(afterIndex).forEach((entry, i) => {
    const absIndex = afterIndex + i;
    if (entry.type !== 'message') return;
    const role = entry.message?.role;
    if (role !== 'user' && role !== 'assistant') return;

    const content = entry.message?.content;
    let text = typeof content === 'string'
      ? content
      : Array.isArray(content)
        ? content.filter(b => b.type === 'text').map(b => b.text || '').join(' ')
        : '';

    text = text.trim();
    if (!text || text.startsWith('NO_REPLY')) return;

    if (role === 'user') {
      text = text
        .replace(/Conversation info \(untrusted metadata\):[\s\S]*?```\n/g, '')
        .replace(/Sender \(untrusted metadata\):[\s\S]*?```\n/g, '')
        .replace(/<<<EXTERNAL_UNTRUSTED_CONTENT[\s\S]*?>>>/g, '')
        .replace(/Untrusted context[\s\S]*?>>>/g, '')
        .replace(/Replied message[\s\S]*?```\n/g, '')
        .trim();
      if (!text) return;
      turns.push({ role: 'user', text: text.slice(0, 800), index: absIndex });
    } else {
      turns.push({ role: 'assistant', text: text.slice(0, 1500), index: absIndex });
    }
  });
  return turns;
}

// ── LLM API ───────────────────────────────────────────────────────────────────

function httpPost(options, body) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { reject(new Error('Parse error: ' + data.slice(0, 200))); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function llmRequest(prompt) {
  const body = JSON.stringify({ model, max_tokens: 1024, messages: [{ role: 'user', content: prompt }] });

  if (provider === 'openai') {
    const r = await httpPost({
      hostname: 'api.openai.com', path: '/v1/chat/completions', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}`, 'Content-Length': Buffer.byteLength(body) },
    }, body);
    if (r.error) throw new Error(r.error.message);
    return r.choices?.[0]?.message?.content || '';
  } else {
    const r = await httpPost({
      hostname: 'api.anthropic.com', path: '/v1/messages', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'Content-Length': Buffer.byteLength(body) },
    }, body);
    if (r.error) throw new Error(r.error.message);
    return r.content?.[0]?.text || '';
  }
}

async function summarize(turns, label) {
  const conversation = turns.map(t => `${t.role === 'user' ? 'User' : 'Agent'}: ${t.text}`).join('\n\n');
  const prompt = `You are a memory scribe for an AI agent. Extract the key facts from this conversation and organize them into 3-6 thematic memory documents. Consolidate related information — don't create separate entries for every small fact.

Each entry must follow this exact format:
TITLE: <short descriptive title, 3-8 words>
CONTENT: <3-8 plain prose sentences consolidating all related facts on this theme. No markdown, no bullets. Be specific and factual — include names, versions, paths, decisions, outcomes.>

Separate each entry with a line containing only: ---

Good themes to group by: a project or feature built, a set of related decisions, a tool or skill created/configured, a problem diagnosed and solved, a configuration change and its outcome.

Rules:
- Aim for 3-6 entries total — consolidate aggressively
- Each entry should cover a meaningful topic, not a single micro-fact
- Titles should be specific and searchable
- Plain prose only — no markdown, no bullets
- Skip small talk and filler

Session: ${label}

Conversation:
${conversation}

Output ONLY the entries in the format above. No preamble, no summary at the end.`;
  return llmRequest(prompt);
}

// ── Parse structured memory entries ──────────────────────────────────────────

function parseEntries(raw) {
  return raw.split(/^---$/m)
    .map(block => block.trim())
    .filter(Boolean)
    .map(block => {
      const titleMatch = block.match(/^TITLE:\s*(.+)$/m);
      const contentMatch = block.match(/^CONTENT:\s*([\s\S]+)$/m);
      if (!titleMatch || !contentMatch) return null;
      return {
        title: titleMatch[1].trim(),
        content: contentMatch[1].trim().replace(/\n+/g, ' '),
      };
    })
    .filter(Boolean);
}

// ── Memory writing ────────────────────────────────────────────────────────────

function appendToMemory(entries, label) {
  const date = new Date().toISOString().slice(0, 10);
  const file = path.join(memoryDir, `${date}.md`);
  const timestamp = new Date().toISOString().slice(11, 16) + ' UTC';
  const header = fs.existsSync(file) ? '' : `# ${date}\n\n`;

  // Write as structured entries to markdown file
  const blocks = entries.map(e => `### ${e.title}\n${e.content}`).join('\n\n');
  const block = `\n## Scribe [${timestamp}] ${label}\n\n${blocks}\n`;

  fs.mkdirSync(memoryDir, { recursive: true });
  fs.appendFileSync(file, header + block);
  return file;
}

async function writeToSupermemory(entries, label) {
  const smKey = process.env.SUPERMEMORY_API_KEY;
  if (!smKey) return 0;

  let Supermemory;
  try { Supermemory = require('supermemory').default; }
  catch { return 0; }

  const container = get('--sm-container') || agentLabel;
  const client = new Supermemory({ apiKey: smKey });
  let written = 0;

  for (const entry of entries) {
    try {
      await client.add({
        content: entry.content,
        containerTag: container,
        metadata: { title: entry.title, source: 'session-scribe', session: label, date: new Date().toISOString().slice(0, 10) }
      });
      written++;
      await new Promise(r => setTimeout(r, 200));
    } catch (e) {
      console.error(`  SM write failed for "${entry.title}": ${e.message}`);
    }
  }
  return written;
}

// ── Scribe one session ────────────────────────────────────────────────────────

async function scribeSession(dir, sessionId, label, state) {
  const lastIndex = state[sessionId]?.lastIndex || 0;
  const transcript = readTranscript(dir, sessionId);
  const turns = extractTurns(transcript, lastIndex);

  if (turns.length < minTurns) {
    console.log(`  [${label}] ${turns.length} new turns — skipping (min: ${minTurns})`);
    return false;
  }

  console.log(`  [${label}] Scribing ${turns.length} turns...`);
  const raw = await summarize(turns, label);
  if (!raw.trim()) return false;

  const entries = parseEntries(raw);
  if (!entries.length) {
    console.log(`  [${label}] No parseable entries — skipping.`);
    return false;
  }

  if (dryRun) {
    console.log(`\n--- DRY RUN [${label}] (${entries.length} entries) ---`);
    entries.forEach(e => console.log(`\nTITLE: ${e.title}\nCONTENT: ${e.content}`));
    console.log('--- END ---\n');
  } else {
    const file = appendToMemory(entries, label);
    const smCount = await writeToSupermemory(entries, label);
    const lastEntry = turns[turns.length - 1];
    state[sessionId] = { lastIndex: lastEntry.index + 1, lastRunAt: new Date().toISOString(), label };
    console.log(`  ✅ ${entries.length} entries → ${file}${smCount ? ` + ${smCount} to Supermemory` : ''}`);
  }
  return true;
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const state = loadState();
  let scribed = 0;

  console.log(`provider: ${provider}, model: ${model}`);

  if (allSessions) {
    const sessions = discoverAllSessions();
    console.log(`Discovered ${sessions.length} active session(s) across agents\n`);

    for (const s of sessions) {
      const label = `${s.agentId}/${s.sessionKey.split(':').slice(-2).join(':')}`;
      try {
        if (await scribeSession(s.sessionsDir, s.sessionId, label, state)) scribed++;
      } catch (e) {
        console.error(`  [${label}] Error: ${e.message}`);
      }
      // Rate limit between sessions
      await new Promise(r => setTimeout(r, 500));
    }
  } else {
    const resolved = resolveSessionId(sessionsDir);
    if (!resolved) process.exit(1);
    const label = agentLabel !== 'agent' ? agentLabel : resolved.label;
    if (await scribeSession(sessionsDir, resolved.sessionId, label, state)) scribed++;
  }

  if (!dryRun) saveState(state);
  console.log(`\nDone. ${scribed} session(s) scribed.`);
}

main().catch(e => { console.error('Scribe error:', e.message); process.exit(1); });
