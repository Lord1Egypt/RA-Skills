#!/usr/bin/env node
import crypto from 'node:crypto';
import { ambientEnabled, normalizeInterestSlot } from './memory_policy.js';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { queryDataSource, queryRecent, requireIds, textOf } from './notionctl_bridge.js';

const DEFAULT_STATE_DIR = 'memory/soul-in-sapphire';
const DEFAULT_TTL_MINUTES = 120;
const DEFAULT_DAILY_CAP = 10;
const DEFAULT_TIMEZONE = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
const TITLE_LIMIT = 80;
const CONTENT_LIMIT = 800;
const MARKERS = ['unresolved', 'todo', 'tension'];

function nowIso() {
  return new Date().toISOString();
}

function usage() {
  return `Usage:
  node skills/soul-in-sapphire/scripts/stage_ambient_recall.js [options]

Options:
  --workspace <path>       OpenClaw agent workspace. Defaults to OPENCLAW_WORKSPACE or cwd.
  --state-dir <path>       State directory. Relative paths are under workspace.
                           Defaults to SIS_AMBIENT_STATE_DIR or memory/soul-in-sapphire.
  --timezone <iana_tz>     Day boundary for rollsToday/hitsToday.
                           Defaults to SIS_AMBIENT_TIMEZONE or the local runtime timezone.
  --ttl-minutes <n>        Staged recall TTL. Default: 120.
  --daily-cap <n>          Max hit/stage attempts per day. Default: 10.
  --state-dsid <id>        Notion state data source id for recent shelf.
  --journal-dsid <id>      Notion journal data source id for recent shelf.
  --mem-dsid <id>          Notion memory data source id for durable shelf.
  --mem-dbid <id>          Notion memory database id for durable shelf.
  --interest-slot-file <p> Optional external soul_interest_slot JSON file for interest shelf.
  --force-roll <1-100>     Force a deterministic roll for verification.
  --dry-run                Do not write state or staged recall files.
  --help, -h               Show this help and exit without rolling.
`;
}

function todayInTimeZone(timeZone) {
  try {
    const parts = new Intl.DateTimeFormat('en-CA', {
      timeZone,
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).formatToParts(new Date());
    const values = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${values.year}-${values.month}-${values.day}`;
  } catch (err) {
    throw new Error(`Invalid --timezone value: ${timeZone}`);
  }
}

function expandHome(p) {
  if (!p) return p;
  if (p === '~') return os.homedir();
  if (p.startsWith('~/')) return path.join(os.homedir(), p.slice(2));
  return p;
}

function parseNumber(value, fallback) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function parseArgs(argv) {
  const out = {
    workspace: process.env.OPENCLAW_WORKSPACE || process.cwd(),
    stateDir: process.env.SIS_AMBIENT_STATE_DIR || DEFAULT_STATE_DIR,
    ttlMinutes: DEFAULT_TTL_MINUTES,
    dailyCap: DEFAULT_DAILY_CAP,
    stateDsid: '',
    journalDsid: '',
    memDsid: '',
    memDbid: '',
    interestSlotFile: process.env.SIS_INTEREST_SLOT_FILE || '',
    forceRoll: null,
    dryRun: false,
    timezone: process.env.SIS_AMBIENT_TIMEZONE || DEFAULT_TIMEZONE,
    help: false,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--timezone') out.timezone = argv[++i] || out.timezone;
    else if (a === '--workspace') out.workspace = argv[++i] || out.workspace;
    else if (a === '--state-dir') out.stateDir = argv[++i] || out.stateDir;
    else if (a === '--ttl-minutes') out.ttlMinutes = parseNumber(argv[++i], out.ttlMinutes);
    else if (a === '--daily-cap') out.dailyCap = parseNumber(argv[++i], out.dailyCap);
    else if (a === '--state-dsid') out.stateDsid = argv[++i] || '';
    else if (a === '--journal-dsid') out.journalDsid = argv[++i] || '';
    else if (a === '--mem-dsid') out.memDsid = argv[++i] || '';
    else if (a === '--mem-dbid') out.memDbid = argv[++i] || '';
    else if (a === '--interest-slot-file') out.interestSlotFile = argv[++i] || '';
    else if (a === '--force-roll') out.forceRoll = parseNumber(argv[++i], null);
    else if (a === '--dry-run') out.dryRun = true;
  }

  out.workspace = path.resolve(expandHome(out.workspace));
  out.stateDir = expandHome(out.stateDir);
  if (!path.isAbsolute(out.stateDir)) out.stateDir = path.join(out.workspace, out.stateDir);
  out.stateDir = path.resolve(out.stateDir);
  if (out.interestSlotFile) {
    out.interestSlotFile = expandHome(out.interestSlotFile);
    if (!path.isAbsolute(out.interestSlotFile)) out.interestSlotFile = path.join(out.workspace, out.interestSlotFile);
    out.interestSlotFile = path.resolve(out.interestSlotFile);
  }
  out.ttlMinutes = Math.max(1, Math.floor(out.ttlMinutes));
  out.dailyCap = Math.max(0, Math.floor(out.dailyCap));
  if (out.forceRoll !== null) {
    out.forceRoll = Math.max(1, Math.min(100, Math.floor(out.forceRoll)));
  }
  return out;
}

function defaultState(date, dailyCap) {
  return {
    version: 1,
    date,
    rollsToday: 0,
    hitsToday: 0,
    lastRollAt: null,
    lastHitAt: null,
    dailyCap,
    lastError: null,
  };
}

function readJsonFile(file) {
  return JSON.parse(fs.readFileSync(file, 'utf-8'));
}

function loadState(file, dailyCap, timeZone) {
  const date = todayInTimeZone(timeZone);
  let state = defaultState(date, dailyCap);
  let loadError = null;
  if (fs.existsSync(file)) {
    try {
      const parsed = readJsonFile(file);
      if (parsed && typeof parsed === 'object' && parsed.version === 1) {
        state = { ...state, ...parsed, dailyCap };
      } else {
        loadError = 'ambient state was invalid; reinitialized';
      }
    } catch {
      loadError = 'ambient state JSON was unreadable; reinitialized';
    }
  }
  if (state.date !== date) {
    state = {
      ...state,
      date,
      rollsToday: 0,
      hitsToday: 0,
      dailyCap,
      lastError: null,
    };
  }
  return { state, loadError };
}

function atomicWriteJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.${crypto.randomUUID()}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2) + '\n', { encoding: 'utf-8', mode: 0o600, flag: 'wx' });
  fs.renameSync(tmp, file);
}

function randomRoll() {
  return crypto.randomInt(1, 101);
}

function shelfForRoll(roll) {
  if (roll >= 1 && roll <= 3) return 'recent';
  if (roll === 4) return 'unresolved';
  if (roll === 5) return 'durable';
  if (roll === 6) return 'dream';
  if (roll === 7) return 'interest';
  return null;
}

function truncateText(value, limit) {
  const s = String(value || '').replace(/\s+/g, ' ').trim();
  if (s.length <= limit) return s;
  return `${s.slice(0, Math.max(0, limit - 1)).trimEnd()}…`;
}

function relativePath(workspace, file) {
  const rel = path.relative(workspace, file);
  return rel && !rel.startsWith('..') && !path.isAbsolute(rel) ? rel : file;
}

function candidate(title, content, source) {
  const t = truncateText(title, TITLE_LIMIT);
  const c = truncateText(content || title, CONTENT_LIMIT);
  if (!t && !c) return null;
  return { title: t || truncateText(c, TITLE_LIMIT), content: c, source };
}

function markdownText(s) {
  return String(s || '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/^#+\s*/gm, '')
    .replace(/^\s*[-*]\s*/gm, '')
    .replace(/\[[^\]]+\]\([^)]+\)/g, m => m.replace(/\[|\]\([^)]+\)/g, ''))
    .replace(/\s+/g, ' ')
    .trim();
}

function newestFiles(dir, suffix = '.md', limit = 10) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter(d => d.isFile() && d.name.endsWith(suffix))
    .map(d => path.join(dir, d.name))
    .sort((a, b) => b.localeCompare(a))
    .slice(0, limit);
}

function readFirstExistingJsonl(files) {
  for (const file of files) {
    if (!fs.existsSync(file)) continue;
    const lines = fs.readFileSync(file, 'utf-8').split(/\r?\n/).filter(Boolean);
    for (const line of lines.reverse()) {
      try {
        const obj = JSON.parse(line);
        return { file, obj };
      } catch {
        // Keep scanning older lines.
      }
    }
  }
  return null;
}

function readDreamRem(workspace) {
  const dir = path.join(workspace, 'memory', 'dreaming', 'rem');
  for (const file of newestFiles(dir, '.md', 14)) {
    const raw = fs.readFileSync(file, 'utf-8');
    const lines = raw.split(/\r?\n/);
    const picked = lines.find(line => /^-\s+(?!No strong)/i.test(line.trim()));
    if (picked) {
      return candidate('REM dream reflection', picked.replace(/^-\s*/, ''), {
        type: 'openclaw_dream',
        path: relativePath(workspace, file),
      });
    }
  }
  return null;
}

function readDreamLight(workspace) {
  const dir = path.join(workspace, 'memory', 'dreaming', 'light');
  for (const file of newestFiles(dir, '.md', 14)) {
    const raw = fs.readFileSync(file, 'utf-8');
    const blocks = raw.split(/\n(?=-\s+Candidate:)/g).filter(s => /^\s*-\s+Candidate:/m.test(s));
    for (const block of blocks) {
      if (!/status:\s*staged/i.test(block)) continue;
      const text = markdownText(block.replace(/^\s*-\s+Candidate:\s*/m, ''));
      if (text) {
        return candidate('Light dream candidate', text, {
          type: 'openclaw_dream',
          path: relativePath(workspace, file),
        });
      }
    }
  }
  return null;
}

function readDreamDiary(workspace) {
  const file = path.join(workspace, 'DREAMS.md');
  if (!fs.existsSync(file)) return null;
  const raw = fs.readFileSync(file, 'utf-8');
  const chunks = raw.split(/\n---+\n/g).map(s => markdownText(s)).filter(s => s && s !== 'Dream Diary');
  const latest = chunks[chunks.length - 1];
  if (!latest) return null;
  return candidate('Dream diary', latest, {
    type: 'openclaw_dream',
    path: relativePath(workspace, file),
  });
}

function readDream(workspace) {
  return readDreamRem(workspace) || readDreamLight(workspace) || readDreamDiary(workspace);
}

function readLatestDailyMemory(workspace) {
  const file = newestFiles(path.join(workspace, 'memory'), '.md', 1)[0];
  if (!file) return null;
  const text = markdownText(fs.readFileSync(file, 'utf-8'));
  if (!text) return null;
  return candidate('Recent daily memory', text, {
    type: 'workspace_memory',
    path: relativePath(workspace, file),
  });
}

function readDailyMarker(workspace) {
  const files = newestFiles(path.join(workspace, 'memory'), '.md', 40);
  for (const file of files) {
    const raw = fs.readFileSync(file, 'utf-8');
    const lines = raw.split(/\r?\n/);
    const line = lines.find(l => MARKERS.some(m => l.toLowerCase().includes(m)));
    if (!line) continue;
    return candidate('Unresolved memory marker', line, {
      type: 'workspace_memory',
      path: relativePath(workspace, file),
    });
  }
  return null;
}

function readUnresolved(workspace) {
  const hit = readFirstExistingJsonl([
    path.join(workspace, 'memory', 'soul-in-sapphire', 'conflicts.jsonl'),
    path.join(workspace, 'memory', 'conflicts.jsonl'),
    path.join(workspace, 'soul-in-sapphire', 'state', 'conflicts.jsonl'),
  ]);
  if (hit) {
    const r = hit.obj;
    const content = [
      r.tension,
      r.current_pull ? `current_pull: ${r.current_pull}` : '',
      r.next_signal ? `next_signal: ${r.next_signal}` : '',
      r.note,
    ].filter(Boolean).join(' ');
    const title = r.tension || 'Unresolved tension';
    return candidate(title, content, {
      type: 'local_conflict',
      path: relativePath(workspace, hit.file),
    });
  }
  return readDailyMarker(workspace);
}

function normalizeStatePage(page) {
  const p = page?.properties || {};
  const title = textOf(p.reason) || textOf(p.Name) || textOf(p.when) || 'Recent state';
  const parts = [
    textOf(p.when),
    textOf(p.mood_label),
    textOf(p.intent),
    textOf(p.need_stack),
    textOf(p.reason),
  ].flat().filter(Boolean).join(' ');
  const result = candidate(title, parts, {
    type: 'notion_state',
    id: page?.id,
    url: page?.url,
  });
  if (result) result.affect_context = recordedContext(page, ['when', 'mood_label', 'intent', 'need_stack', 'need_level', 'avoid', 'reason', 'state_json'], 'requires_event_resolution');
  return result;
}

function recordedContext(page, fields, status) {
  const properties = page.properties || {};
  const truncated = [];
  const missing = [];
  const values = {};
  for (const field of fields) {
    if (!properties[field]) { missing.push(field); values[field] = null; continue; }
    const value = textOf(properties[field]);
    if (typeof value === 'string' && value.length > 1200) truncated.push(field);
    if (Array.isArray(value) && (value.length > 20 || value.some(v => String(v).length > 200))) truncated.push(field);
    values[field] = typeof value === 'string' ? value.slice(0, 1200) : Array.isArray(value) ? value.slice(0, 20).map(v => String(v).slice(0, 200)) : value;
  }
  const event = properties.event;
  return { status, temporal_scope: 'recorded_not_current', fields: values, missing_fields: missing,
    truncated_fields: truncated, event_ids: (event?.relation || []).slice(0, 5).map(r => r.id),
    event_relation_status: event?.type === 'relation' ? (event.has_more || event.relation.length > 5 ? 'truncated' : event.relation.length ? 'present' : 'empty') : 'absent',
    source_resolution: { page_id: page.id, url: page.url || null, data_source_id: page.parent?.data_source_id || null } };
}

function normalizeJournalPage(page) {
  const p = page?.properties || {};
  const title = textOf(p.Name) || textOf(p.when) || 'Recent journal';
  const parts = [
    textOf(p.when),
    textOf(p.body),
    textOf(p.worklog),
    textOf(p.future),
  ].flat().filter(Boolean).join(' ');
  const result = candidate(title, parts, {
    type: 'notion_journal',
    id: page?.id,
    url: page?.url,
  });
  if (result) result.affect_context = recordedContext(page, ['when', 'mood_label', 'intent', 'body', 'future'], 'journal_self_report');
  return result;
}

function readRecent(args) {
  if (args.stateDsid) {
    const pages = queryRecent(args.stateDsid, 1);
    if (pages[0]) return normalizeStatePage(pages[0]);
  }
  if (args.journalDsid) {
    const pages = queryRecent(args.journalDsid, 1);
    if (pages[0]) return normalizeJournalPage(pages[0]);
  }
  return readLatestDailyMemory(args.workspace);
}

async function readDurable(args) {
  const cfg = { data_source_id: args.memDsid, database_id: args.memDbid };
  requireIds(cfg);
  const res = await queryDataSource(args.memDsid, {
    page_size: 25,
    sorts: [{ timestamp: 'created_time', direction: 'descending' }],
  });
  const pages = res?.results || [];
  if (!pages.length) return null;
  const page = pages[crypto.randomInt(0, pages.length)];
  const p = page?.properties || {};
  const result = candidate(textOf(p.Name) || 'Durable memory', textOf(p.Content), {
    type: 'notion_memory',
    id: page?.id,
    url: page?.url,
  });
  // The audited mem schema has no event relation. Keep its actual tags/text and
  // source pointer; never invent an emotion axis or join by date/text similarity.
  if (result) result.affect_context = recordedContext(page, ['Content', 'Tags', 'Source', 'CreatedAt', 'Confidence'], 'mem_only_no_verified_event_join');
  return result;
}

function readInterest(args) {
  if (!args.interestSlotFile || !fs.existsSync(args.interestSlotFile)) return null;
  const slot = normalizeInterestSlot(readJsonFile(args.interestSlotFile));
  const fullRecords = slot.records.filter(r => !r.detail);
  const pool = fullRecords.length ? fullRecords : slot.records;
  if (!pool.length) return null;
  const picked = pool[crypto.randomInt(0, pool.length)];
  const textParts = [picked.why_me, picked.finding, picked.question, picked.feedback].filter(Boolean).join(' ');
  return candidate(picked.title || picked.id, textParts || picked.detail || picked.id, {
    type: 'interest_slot',
    id: picked.id,
    path: relativePath(args.workspace, args.interestSlotFile),
    source_ref: picked.source || null,
  });
}

async function readShelf(shelf, args) {
  if (shelf === 'recent') return readRecent(args);
  if (shelf === 'unresolved') return readUnresolved(args.workspace);
  if (shelf === 'durable') return await readDurable(args);
  if (shelf === 'dream') return readDream(args.workspace);
  if (shelf === 'interest') return readInterest(args);
  return null;
}

function buildStaged(candidateObj, shelf, roll, args, at) {
  const expires = new Date(new Date(at).getTime() + args.ttlMinutes * 60 * 1000).toISOString();
  return {
    version: 1,
    kind: 'ambient_recall',
    id: crypto.randomUUID(),
    consumed_at: null,
    shelf,
    staged_at: at,
    expires_at: expires,
    roll,
    title: truncateText(candidateObj.title, TITLE_LIMIT),
    content: truncateText(candidateObj.content, CONTENT_LIMIT),
    source: candidateObj.source || { type: shelf },
    ...(candidateObj.affect_context ? { affect_context: candidateObj.affect_context } : {}),
  };
}

function cleanExpired(stagedFile) {
  if (!fs.existsSync(stagedFile)) return false;
  try {
    const obj = readJsonFile(stagedFile);
    if (obj?.expires_at && new Date(obj.expires_at).getTime() < Date.now()) {
      fs.unlinkSync(stagedFile);
      return true;
    }
  } catch {
    fs.unlinkSync(stagedFile);
    return true;
  }
  return false;
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    process.stdout.write(usage());
    return;
  }
  if (!ambientEnabled()) {
    console.log(JSON.stringify({ ok: true, status: 'disabled', owner: 'soul',
      staged: false, consumed: false }));
    return;
  }
  const stateFile = path.join(args.stateDir, 'ambient-recall-state.json');
  const stagedFile = path.join(args.stateDir, 'ambient-recall.json');
  const at = nowIso();
  const loaded = loadState(stateFile, args.dailyCap, args.timezone);
  let state = loaded.state;
  const loadError = loaded.loadError;
  const roll = args.forceRoll ?? randomRoll();
  const shelf = shelfForRoll(roll);
  let staged = null;
  let cleanedExpired = false;
  let failed = false;

  state.rollsToday = Number(state.rollsToday || 0) + 1;
  state.lastRollAt = at;
  state.dailyCap = args.dailyCap;
  state.lastError = loadError || null;

  try {
    if (state.hitsToday >= args.dailyCap && shelf) {
      state.lastError = `dailyCap reached (${args.dailyCap}); skipped ${shelf}`;
    } else if (shelf) {
      const c = await readShelf(shelf, args);
      if (c) {
        staged = buildStaged(c, shelf, roll, args, at);
        state.hitsToday = Number(state.hitsToday || 0) + 1;
        state.lastHitAt = at;
      } else {
        state.lastError = `no ambient candidate for shelf: ${shelf}`;
      }
    } else if (!args.dryRun) {
      cleanedExpired = cleanExpired(stagedFile);
    }
  } catch (err) {
    failed = true;
    state.lastError = truncateText(err?.message || String(err), 240);
  }

  if (!args.dryRun) {
    fs.mkdirSync(args.stateDir, { recursive: true });
    atomicWriteJson(stateFile, state);
    if (staged) atomicWriteJson(stagedFile, staged);
  }

  console.log(JSON.stringify({
    ok: !failed,
    status: failed ? 'error' : staged ? (args.dryRun ? 'preview' : 'staged') : 'no_candidate',
    consumed: false,
    dryRun: args.dryRun,
    roll,
    shelf,
    staged: !!staged && !args.dryRun,
    cleanedExpired,
    stateFile,
    stagedFile,
    timezone: args.timezone,
    lastError: state.lastError,
    recall: staged,
  }, null, 2));
  if (failed) process.exitCode = 1;
}

try {
  await main();
} catch (err) {
  console.error(String(err?.stack || err));
  process.exit(1);
}
