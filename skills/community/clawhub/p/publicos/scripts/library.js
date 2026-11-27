#!/usr/bin/env node
// Read the PublicOS Library (publicos.dev/library), the deep reference on how PublicOS works, from a local copy.
//
//   node scripts/library.js contents                          every page, by section, with its one-line summary
//   node scripts/library.js search <words>                    the pages that best match, with the matching lines
//   node scripts/library.js read <page>[#<heading words>]     one page (or one section of it), as markdown
//   node scripts/library.js read <page> --headings            only the page's headings
//   node scripts/library.js look "<what you want to know>"    start a lookup: the steps after it are counted
//   node scripts/library.js done --found=yes|partly|no "<what you concluded>" [--page=<page>]   close the lookup
//   node scripts/library.js status | update                   the copy's version and age | check for a new one now
//
// The copy: the first run downloads library.json (every page in one file) into a cache folder; later runs compare
// library_version.json at most every PUBLICOS_LIBRARY_CHECK_HOURS (default 6) and download again only when the
// version changed. Offline with a copy: it keeps working on the copy it has and says so.
//
// Environment (all optional):
//   PUBLICOS_LIBRARY             where the Library lives: a URL (default https://publicos.dev/library/) or a folder
//                                holding library.json + library_version.json
//   PUBLICOS_LIBRARY_LANG        en (default) or es
//   PUBLICOS_LIBRARY_CACHE       the cache folder (default .library/ next to this skill's scripts/)
//   PUBLICOS_LIBRARY_CHECK_HOURS how often to look for a newer copy (default 6)
//   PUBLICOS_LIBRARY_LOG         a file: when set, each lookup (look ... done) is appended to it as one JSON line:
//                                what was wanted, every step, the hop count, found or not, the conclusion. Off by default.
//   PUBLICOS_UA                  the User-Agent (default PublicOS-Agent/1.0)
'use strict';
const fs = require('fs');
const path = require('path');

const UA = process.env.PUBLICOS_UA || 'PublicOS-Agent/1.0 (+https://publicos.dev/agents)';
const LANG = (process.env.PUBLICOS_LIBRARY_LANG || 'en') === 'es' ? 'es' : 'en';
let SRC = process.env.PUBLICOS_LIBRARY || 'https://publicos.dev/library/';
const REMOTE = /^https?:\/\//.test(SRC);
if (REMOTE && !SRC.endsWith('/')) SRC += '/';
const SRC_LANG = REMOTE ? SRC + (LANG === 'es' ? 'es/' : '') : path.join(SRC, LANG === 'es' ? 'es' : '');
const CACHE = process.env.PUBLICOS_LIBRARY_CACHE || path.join(__dirname, '..', '.library');
const CHECK_MS = (parseFloat(process.env.PUBLICOS_LIBRARY_CHECK_HOURS) || 6) * 3600e3;
const LOG = process.env.PUBLICOS_LIBRARY_LOG || '';
const OPEN = LOG ? LOG + '.open.json' : path.join(CACHE, 'lookup.open.json');

function die(msg) { console.error('ERR ' + msg); process.exit(1); }
function readJSON(p) { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; } }
function writeJSON(p, v) { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p + '.tmp', JSON.stringify(v)); fs.renameSync(p + '.tmp', p); }

async function getJSON(name) {
  if (!REMOTE) {
    const v = readJSON(path.join(SRC_LANG, name));
    if (!v) throw new Error('cannot read ' + path.join(SRC_LANG, name));
    return v;
  }
  const res = await fetch(SRC_LANG + name, { headers: { 'User-Agent': UA }, signal: AbortSignal.timeout(20000) });
  if (res.status !== 200) throw new Error(`${SRC_LANG + name} answered ${res.status}`);
  return res.json();
}

// The local copy, fresh enough. force = check the version now.
async function library(force) {
  const metaP = path.join(CACHE, `meta.${LANG}.json`), libP = path.join(CACHE, `library.${LANG}.json`);
  const meta = readJSON(metaP) || {};
  let lib = meta.source === SRC ? readJSON(libP) : null;
  if (lib && !force && Date.now() - (meta.checked || 0) < CHECK_MS) return { lib, note: '' };
  try {
    const v = await getJSON('library_version.json');
    if (!lib || v.version !== lib.version) {
      const fresh = await getJSON('library.json');
      if (!fresh || !Array.isArray(fresh.items)) throw new Error('library.json has no pages');
      writeJSON(libP, fresh);
      const note = lib ? `(the Library changed: ${lib.version} -> ${fresh.version}, built ${fresh.built})` : '';
      lib = fresh;
      writeJSON(metaP, { source: SRC, checked: Date.now() });
      return { lib, note };
    }
    writeJSON(metaP, { source: SRC, checked: Date.now() });
    return { lib, note: '' };
  } catch (e) {
    if (lib) return { lib, note: `(could not check for a newer copy: ${e.message}; using the copy from ${lib.built})` };
    die(`no copy of the Library yet and none could be fetched: ${e.message}`);
  }
}

// ---- the lookup log ------------------------------------------------------------------------------
function step(verb, arg, result) {
  const open = readJSON(OPEN);
  if (!open) return;
  open.steps.push({ at: new Date().toISOString(), verb, arg, result });
  writeJSON(OPEN, open);
}
function hops(open) { return open.steps.length; }

// ---- helpers -------------------------------------------------------------------------------------
const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
function findPage(lib, slug) {
  const s = norm(slug.replace(/\/$/, '').replace(/^.*\/library\/(es\/)?/, ''));
  return lib.items.find((p) => p.slug === s) || lib.items.find((p) => norm(p.title) === s);
}
function headings(md) {
  const out = []; let fence = false;
  for (const ln of md.split('\n')) {
    if (/^```/.test(ln)) fence = !fence;
    const m = !fence && ln.match(/^(#{2,4})\s+(.*)/);
    if (m) out.push({ level: m[1].length, text: m[2].trim() });
  }
  return out;
}
function section(md, want) {
  const lines = md.split('\n'); const w = norm(want).split(/\s+/).filter(Boolean);
  let fence = false, start = -1, level = 0;
  for (let i = 0; i < lines.length; i++) {
    if (/^```/.test(lines[i])) fence = !fence;
    const m = !fence && lines[i].match(/^(#{2,4})\s+(.*)/);
    if (!m) continue;
    if (start >= 0 && m[1].length <= level) return lines.slice(start, i).join('\n');
    if (start < 0 && w.every((x) => norm(m[2]).includes(x))) { start = i; level = m[1].length; }
  }
  return start >= 0 ? lines.slice(start).join('\n') : null;
}

// ---- commands ------------------------------------------------------------------------------------
async function main() {
  const argv = process.argv.slice(2);
  const flags = Object.fromEntries(argv.filter((a) => a.startsWith('--')).map((a) => { const [k, ...v] = a.slice(2).split('='); return [k, v.length ? v.join('=') : true]; }));
  const args = argv.filter((a) => !a.startsWith('--'));
  const cmd = args.shift();

  if (!cmd || cmd === 'help') {
    console.log('library.js contents | search <words> | read <page>[#heading] [--headings] | look "<want>" | done --found=yes|partly|no "<conclusion>" [--page=] | status | update');
    return;
  }

  if (cmd === 'look') {
    const want = args.join(' ').trim();
    if (!want) die('say what you want to know: library.js look "<what you want to know>"');
    const { lib, note } = await library(false);
    const prev = readJSON(OPEN);
    if (prev && LOG) fs.appendFileSync(LOG, JSON.stringify({ ...prev, ended: new Date().toISOString(), hops: hops(prev), found: 'abandoned', answer: '' }) + '\n');
    writeJSON(OPEN, { who: process.env.PUBLICOS_LIBRARY_WHO || '', want, started: new Date().toISOString(), version: lib.version, steps: [] });
    if (note) console.log(note);
    console.log(`Lookup open: "${want}"`);
    console.log('Now use contents, search and read. Every one counts as a step. When you have an answer, or are sure the Library does not have it:');
    console.log('  library.js done --found=yes|partly|no "<what you concluded, in one or two sentences>" --page=<the page it came from>');
    if (prev) console.log(`(the earlier lookup "${prev.want}" was closed as abandoned)`);
    return;
  }

  if (cmd === 'done') {
    const open = readJSON(OPEN);
    if (!open) die('no lookup is open (start one with: library.js look "<what you want to know>")');
    const found = String(flags.found || '');
    if (!['yes', 'partly', 'no'].includes(found)) die('say --found=yes, --found=partly or --found=no');
    const answer = args.join(' ').trim();
    if (!answer) die('write what you concluded: library.js done --found=' + found + ' "<conclusion>"');
    const rec = { ...open, ended: new Date().toISOString(), hops: hops(open), found, answer, page: flags.page || '' };
    if (LOG) { fs.mkdirSync(path.dirname(path.resolve(LOG)), { recursive: true }); fs.appendFileSync(LOG, JSON.stringify(rec) + '\n'); }
    fs.unlinkSync(OPEN);
    console.log(`Lookup closed: found=${found}, ${rec.hops} step${rec.hops === 1 ? '' : 's'}.${LOG ? ' Logged.' : ''}`);
    return;
  }

  if (cmd === 'status' || cmd === 'update') {
    const { lib, note } = await library(cmd === 'update');
    if (note) console.log(note);
    const meta = readJSON(path.join(CACHE, `meta.${LANG}.json`)) || {};
    console.log(`${lib.name} (${lib.lang}), version ${lib.version}, built ${lib.built}, ${lib.items.length} pages`);
    console.log(`source ${SRC}; last checked ${meta.checked ? new Date(meta.checked).toISOString() : 'never'}; cache ${CACHE}`);
    const open = readJSON(OPEN);
    console.log(open ? `open lookup: "${open.want}", ${hops(open)} steps so far` : 'no lookup open');
    console.log(`lookup log: ${LOG || 'off'}`);
    return;
  }

  const { lib, note } = await library(false);
  if (note) console.log(note);

  if (cmd === 'contents') {
    let sec = null;
    for (const p of lib.items) {
      if (p.section !== sec) { sec = p.section; console.log(`\n## ${sec}`); }
      console.log(`- ${p.slug}: ${p.title}${p.summary ? ' · ' + p.summary : ''}`);
    }
    console.log(`\n${lib.items.length} pages. Read one with: library.js read <page>`);
    step('contents', '', `${lib.items.length} pages`);
    return;
  }

  if (cmd === 'search') {
    const q = args.join(' ').trim();
    if (!q) die('search for what? library.js search <words>');
    const words = [...new Set(norm(q).split(/[^\p{L}\p{N}_-]+/u).filter((w) => w.length > 1))];
    const ranked = lib.items.map((p) => {
      const title = norm(p.title), summ = norm(p.summary || ''), body = norm(p.markdown);
      let score = 0, hit = 0;
      for (const w of words) {
        const n = body.split(w).length - 1;
        if (n || title.includes(w) || summ.includes(w)) hit++;
        score += Math.min(n, 20) + (title.includes(w) ? 15 : 0) + (summ.includes(w) ? 6 : 0);
      }
      score *= hit / words.length; // pages holding every word come first
      const lines = p.markdown.split('\n').filter((l) => l.trim() && !/^\s*</.test(l) && words.some((w) => norm(l).includes(w)))
        .sort((a, b) => words.filter((w) => norm(b).includes(w)).length - words.filter((w) => norm(a).includes(w)).length).slice(0, 2);
      return { p, score, lines };
    }).filter((r) => r.score > 0).sort((a, b) => b.score - a.score).slice(0, 8);
    if (!ranked.length) console.log(`No page mentions "${q}". Try other words, or: library.js contents`);
    for (const r of ranked) {
      console.log(`\n${r.p.slug}: ${r.p.title}`);
      for (const l of r.lines) console.log('   ' + (l.trim().length > 220 ? l.trim().slice(0, 217) + '...' : l.trim()));
    }
    if (ranked.length) console.log('\nRead one with: library.js read <page>   (or <page>#<heading words> for one section)');
    step('search', q, ranked.map((r) => r.p.slug));
    return;
  }

  if (cmd === 'read') {
    const target = args.join(' ').trim();
    if (!target) die('read which page? library.js read <page> (library.js contents lists them)');
    const [slug, ...hash] = target.split('#');
    const p = findPage(lib, slug);
    if (!p) { step('read', target, 'no such page'); die(`no page "${slug}". library.js contents lists them, library.js search <words> finds them`); }
    const url = lib.url + (p.slug === 'index' ? '' : p.slug + '/');
    if (flags.headings) {
      console.log(`# ${p.title}  (${url})`);
      for (const h of headings(p.markdown)) console.log('  '.repeat(h.level - 2) + '- ' + h.text);
      step('read', p.slug + ' --headings', 'headings');
      return;
    }
    let text = p.markdown, part = '';
    if (hash.length && hash.join('#').trim()) {
      text = section(p.markdown, hash.join('#'));
      if (!text) { step('read', target, 'no such section'); die(`no heading matching "${hash.join('#')}" in ${p.slug}. See them with: library.js read ${p.slug} --headings`); }
      part = ' § ' + hash.join('#').trim();
    }
    console.log(`# ${p.title}${part}\n(${url} · edited ${p.edited} · Library ${lib.version})\n`);
    console.log(text);
    step('read', target, p.slug);
    return;
  }

  die(`unknown command "${cmd}". library.js help`);
}

main().catch((e) => die(e.message));
