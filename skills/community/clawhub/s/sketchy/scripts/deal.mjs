#!/usr/bin/env node
// deal.mjs: deal a style (paper, cover, pencils, motif, opening) so decks do not all look alike.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { parseArgs, say, c, isMain, SKILL_DIR, sketchyHome, rel } from './_lib.mjs';

const spec = {
  name: 'sketchy deal', file: 'deal.mjs', usage: '[--brief "text"] [--json]',
  summary: 'deal a paper, cover, pencil set, motif and opening layout so decks do not converge.',
  details: [
    'Each run draws one card per pool. Words in --brief tilt the odds (finance leans to the night ledger',
    'and receipts, teaching to how-to columns and sticky tabs, tech to blueprint paper). The last five draws',
    'in ~/.sketchy/draws.json (or $SKETCHY_HOME/draws.json) are avoided; when a small pool would run dry the',
    'rule relaxes instead of repeating the newest card. A storage error never stops the deal.',
    'Use the draw as given: pass the paper as new.mjs --theme (night can also be <html data-theme="night">), data-cover on the cover, lead with the two',
    'pencils, use the motif on at least three slides, open with the layout.',
  ],
  options: [
    { name: 'brief', type: 'string', arg: 'text', help: 'what the artifact is about, in a sentence' },
    { name: 'json', type: 'boolean', help: 'print the draw as JSON' },
    { name: 'seed', type: 'string', arg: 'text', help: 'replay a draw: same seed, same brief, same history gives the same cards' },
    { name: 'no-save', type: 'boolean', help: 'do not remember this draw (dry run)' },
  ],
  positionals: { min: 0, max: 0 },
  examples: ['node deal.mjs --brief "Q3 board update, revenue and costs"', 'node deal.mjs --json', 'node deal.mjs --brief "intro to Rust ownership for beginners"'],
};

/* ---------- pools ---------- */
const PAPER = [
  { id: 'day', label: 'day sketchbook', theme: 'day' },
  { id: 'night', label: 'night ledger', theme: 'night' },
  { id: 'kraft', label: 'kraft', theme: 'kraft' },
  { id: 'blueprint', label: 'blueprint', theme: 'blueprint' },
  { id: 'graph', label: 'graph-paper', theme: 'graph' },
  { id: 'cartridge', label: 'white cartridge', theme: 'cartridge' },
];
const COVER = ['slate', 'oxblood', 'moss', 'ochre', 'ink'].map((id) => ({ id, label: id }));
const SERIES = ['blue', 'green', 'yellow', 'orange', 'violet'];
const PENCILS = [];
for (let i = 0; i < SERIES.length; i++) for (let j = i + 1; j < SERIES.length; j++) PENCILS.push({ id: `${SERIES[i]}+${SERIES[j]}`, label: `${SERIES[i]} + ${SERIES[j]}`, pair: [SERIES[i], SERIES[j]] });
// every motif maps to engine classes the agent can actually use (see references/components.md)
const MOTIF = [
  ['postage and postmarks', 'postage-stamp sketch, svg[data-postmark], .sk-stamp'],
  ['tape and labels', '.sk-tape, .sk-rlabel'],
  ['margin math', '.sk-maths with red § references'],
  ['receipts and stamps', '.sk-receipt, .sk-stamp, .sk-stamp.is-unearned'],
  ['plates and screws', '.sk-plate cards with sketches'],
  ['plain paper', 'no props: paper, pencil and the words'],
].map(([id, use]) => ({ id, label: id + ' (' + use + ')' }));
const OPENING = [
  { id: 'cover with label', label: 'cover with label', layout: 'cover' },
  { id: 'big question', label: 'big question', layout: 'title' },
  { id: 'big number', label: 'big number', layout: 'big-number' },
  { id: 'letter', label: 'letter', layout: 'letter' },
  { id: 'decision board', label: 'decision board', layout: 'board' },
];
const BUILT_IN_THEMES = new Set(['day', 'night']); // defined inside engine/sketchy.css

/* ---------- brief keywords ---------- */
// Stems match at the start of a word; add \b to a stem to match the whole word.
const DOMAINS = [
  {
    name: 'finance', hint: 'ledger layout for the numbers, receipts as tape labels, figures in gold on the night paper',
    stems: ['financ', 'money', 'revenue', 'budget', 'invoice', 'audit', 'tax', 'bank', 'quarter', 'q[1-4]\\b', 'profit', 'cost', 'pric', 'invest', 'sales', 'fund', 'cash', 'accounting', 'ledger', 'receipt', 'umsatz', 'haushalt', 'rechnung', 'steuer', 'quartal'],
    boost: { paper: { night: 4, day: 1.3 }, cover: { oxblood: 3, ink: 2 }, motif: { 'margin math': 3, 'tape and labels': 2.5, 'receipts and stamps': 1.5 }, opening: { 'big number': 3, 'cover with label': 1.5 }, pencil: { yellow: 1.6, orange: 1.4, blue: 1.3 } },
  },
  {
    name: 'teaching', hint: 'how-to columns: the steps layout, one idea per slide, a worked example before the rule',
    stems: ['teach', 'lesson', 'course', 'learn', 'tutorial', 'how-to', 'howto', 'class\\b', 'workshop', 'onboarding', 'training', 'student', 'curriculum', 'explain', 'guide', 'beginner', 'intro', 'lehr', 'unterricht', 'kurs', 'schulung'],
    boost: { paper: { day: 2, graph: 2.5, kraft: 1.5, night: 0.25, blueprint: 0.6 }, cover: { moss: 2, slate: 1.5 }, motif: { 'plates and screws': 3, 'receipts and stamps': 2.5, 'margin math': 1.5 }, opening: { 'big question': 3, 'decision board': 2 }, pencil: { green: 1.6, blue: 1.4 } },
  },
  {
    // anything that ends up on a printer or a copier: light paper saves toner and stays legible
    name: 'print', hint: 'light paper for the copier: cartridge or day, no full-page dark sheets',
    stems: ['print', 'handout', 'worksheet', 'one-page', 'one page', 'one-pager', 'onepager', 'a4\b', 'letter size', 'flyer', 'poster', 'arbeitsblatt', 'ausdruck'],
    boost: { paper: { cartridge: 4, day: 2.5, graph: 1.5, night: 0.12, blueprint: 0.2 } },
  },
  {
    name: 'tech', hint: 'blueprint paper, tape labels for technical names, margin maths for the numbers',
    stems: ['tech', 'software', 'code', 'coding', 'api\\b', 'engineer', 'architect', 'infrastructure', 'system', 'data', 'cloud', 'devops', 'security', 'protocol', 'algorithm', 'machine learning', 'ai\\b', 'llm', 'model', 'database', 'network', 'rust\\b', 'python', 'kubernetes', 'backend', 'frontend', 'stack\\b', 'technik', 'architektur'],
    boost: { paper: { blueprint: 4, graph: 2.5, cartridge: 1.5 }, cover: { ink: 3, slate: 2 }, motif: { 'tape and labels': 3, 'margin math': 2 }, opening: { 'decision board': 2.5, 'big question': 1.5 }, pencil: { blue: 1.8, orange: 1.4, yellow: 1.3 } },
  },
  {
    name: 'story', hint: 'a letter or postcard feel; stamps and postmarks carry the story',
    stems: ['story', 'letter', 'personal', 'thank', 'travel', 'trip', 'journey', 'memoir', 'invitation', 'wedding', 'holiday', 'postcard', 'greeting', 'birthday', 'dear\\b', 'brief\\b', 'reise'],
    boost: { paper: { kraft: 2.5, day: 1.5 }, cover: { ochre: 2, oxblood: 2 }, motif: { 'postage and postmarks': 4 }, opening: { letter: 4, 'decision board': 1.5 }, pencil: { yellow: 1.5, orange: 1.5, violet: 1.3 } },
  },
  {
    name: 'pitch', hint: 'one claim per slide, the number or the question first, the ask last',
    stems: ['pitch', 'launch', 'startup', 'growth', 'investor', 'product', 'proposal', 'roadmap', 'strategy', 'vision'],
    boost: { opening: { 'big number': 2, 'big question': 2.5, 'decision board': 2 }, cover: { ochre: 1.5, oxblood: 1.5 }, paper: { day: 1.4, night: 1.4 } },
  },
  {
    name: 'research', hint: 'lead with the question, show the evidence, keep the maths in the margin',
    stems: ['research', 'study', 'science', 'scientific', 'hypothesis', 'experiment', 'finding', 'analysis', 'survey', 'report', 'why\\b', 'question'],
    boost: { opening: { 'big question': 3.5 }, paper: { graph: 2.5, cartridge: 2, day: 1.4 }, motif: { 'margin math': 3, 'receipts and stamps': 1.5 }, pencil: { violet: 1.4, blue: 1.4 } },
  },
  {
    name: 'nature', hint: 'warm paper, green and earth pencils, plain objects',
    stems: ['nature', 'garden', 'climate', 'environment', 'sustainab', 'farm', 'food', 'forest', 'ocean', 'wildlife', 'energy'],
    boost: { paper: { kraft: 3 }, cover: { moss: 4 }, motif: { 'receipts and stamps': 1.5, 'plain paper': 1.5 }, pencil: { green: 2, yellow: 1.4 } },
  },
  {
    name: 'minimal', hint: 'quiet: white paper, one motif at most, plenty of empty page',
    stems: ['minimal', 'clean', 'plain', 'simple', 'quiet', 'calm', 'elegant', 'formal', 'legal', 'contract'],
    boost: { motif: { 'plain paper': 4 }, paper: { cartridge: 3, day: 2 }, cover: { ink: 2, slate: 2 } },
  },
  {
    name: 'kids', hint: 'big shapes, bright pencils, sticky tabs to find your way',
    stems: ['kids', 'children', 'child\\b', 'school', 'fun\\b', 'play', 'game', 'family'],
    boost: { paper: { kraft: 2.5, graph: 2 }, motif: { 'plates and screws': 3, 'receipts and stamps': 2 }, cover: { ochre: 2.5, moss: 2 }, pencil: { yellow: 1.5, orange: 1.5, green: 1.4 } },
  },
];

function matchDomains(brief) {
  if (!brief) return [];
  return DOMAINS.filter((d) => new RegExp(`(?:^|[^a-z])(?:${d.stems.join('|')})`, 'i').test(brief));
}

/* ---------- seeded random ---------- */
function hash32(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
function mulberry32(a) {
  return () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ---------- history ---------- */
const historyFile = () => path.join(sketchyHome(), 'draws.json');
function readHistory() {
  try {
    const data = JSON.parse(fs.readFileSync(historyFile(), 'utf8'));
    return Array.isArray(data.draws) ? data.draws : [];
  } catch { return []; }
}
function saveHistory(draws, note) {
  try {
    fs.mkdirSync(sketchyHome(), { recursive: true });
    fs.writeFileSync(historyFile(), JSON.stringify({ draws: draws.slice(0, 20) }, null, 2));
  } catch (e) { note(`could not remember this draw in ${historyFile()} (${e.code || e.message}); the deal still stands`); }
}

/* ---------- drawing ---------- */
function pick(rng, pool, key, weightOf, recent) {
  const ids = pool.map((p) => p.id);
  let cand = ids;
  const need = Math.min(2, ids.length);
  for (let k = Math.min(5, recent.length); k >= 0; k--) {
    const used = new Set(recent.slice(0, k).map((d) => d[key]));
    const fresh = ids.filter((i) => !used.has(i));
    if (fresh.length >= need) { cand = fresh; break; }
  }
  const weights = cand.map((id) => Math.max(0.05, weightOf(id)));
  const total = weights.reduce((a, b) => a + b, 0);
  let r = rng() * total;
  for (let i = 0; i < cand.length; i++) { r -= weights[i]; if (r <= 0) return pool.find((p) => p.id === cand[i]); }
  return pool.find((p) => p.id === cand[cand.length - 1]);
}

export function deal({ brief = '', seed, recent = [] } = {}) {
  const domains = matchDomains(brief);
  const rng = mulberry32(hash32(`${seed}|${brief}|${recent.slice(0, 5).map((d) => d.paper + d.cover + d.pencils + d.motif + d.opening).join(',')}`));
  const boost = (pool, id) => Math.min(8, domains.reduce((m, d) => m * ((d.boost[pool] && d.boost[pool][id]) || 1), 1));
  const paper = pick(rng, PAPER, 'paper', (id) => boost('paper', id), recent);
  const cover = pick(rng, COVER, 'cover', (id) => boost('cover', id), recent);
  const pencils = pick(rng, PENCILS, 'pencils', (id) => { const p = PENCILS.find((x) => x.id === id).pair; return boost('pencil', p[0]) * boost('pencil', p[1]); }, recent);
  const motif = pick(rng, MOTIF, 'motif', (id) => boost('motif', id), recent);
  const opening = pick(rng, OPENING, 'opening', (id) => boost('opening', id), recent);
  const themeFile = path.join(SKILL_DIR, 'themes', `${paper.theme}.css`);
  const exists = fs.existsSync(themeFile);
  return {
    seed, brief: brief || null, matched: domains.map((d) => d.name),
    paper: paper.id, paperLabel: paper.label, theme: paper.theme, themeFile: `themes/${paper.theme}.css`,
    themeStatus: exists ? 'file' : BUILT_IN_THEMES.has(paper.theme) ? 'built-in' : 'planned',
    cover: cover.id, pencils: pencils.id, leadPencils: pencils.pair,
    motif: motif.id, opening: opening.id, openingLayout: opening.layout,
    hints: domains.map((d) => d.hint),
  };
}

function printDraw(d) {
  const themeNote = d.themeStatus === 'built-in' ? 'built into engine/sketchy.css' : d.themeStatus === 'file' ? 'file present' : 'file not shipped yet, falls back to day';
  const w = 9;
  const row = (k, v, extra = '') => say.line(`  ${k.padEnd(w)}${extra ? v.padEnd(24) + c.dim(extra) : v}`);
  say.line(c.bold(`deal  seed ${d.seed}${d.brief ? `  brief: ${d.brief}` : ''}${d.matched.length ? `  (reads as ${d.matched.join(', ')})` : ''}`));
  row('paper', d.paperLabel, d.theme === 'day' ? 'default, nothing to add' : d.theme === 'night' ? '<html data-theme="night">' : `new.mjs --theme ${d.theme}  (themes/${d.theme}.css)`);
  row('cover', d.cover, `data-cover="${d.cover}"`);
  row('pencils', `${d.leadPencils[0]} + ${d.leadPencils[1]} lead`, 'red stays for the one thing to look at');
  row('motif', d.motif);
  row('opening', d.opening, `data-layout="${d.openingLayout}"`);
  d.hints.forEach((h, i) => row(i === 0 ? 'hints' : '', h));
  say.line(`theme file: ${d.themeFile} (${themeNote})`);
}

function main() {
  const { values } = parseArgs(process.argv.slice(2), spec);
  const seed = values.seed || crypto.randomBytes(4).toString('hex');
  const history = readHistory();
  const draw = deal({ brief: values.brief || '', seed, recent: history });
  const notes = [];
  if (!values.noSave) {
    saveHistory([{ at: new Date().toISOString(), seed, brief: draw.brief, paper: draw.paper, cover: draw.cover, pencils: draw.pencils, motif: draw.motif, opening: draw.opening }, ...history], (m) => notes.push(m));
  }
  if (values.json) process.stdout.write(JSON.stringify(draw, null, 2) + '\n');
  else printDraw(draw);
  for (const n of notes) console.error(`note  ${n}`);
}

if (isMain(import.meta.url)) main();
