#!/usr/bin/env node
// new.mjs: start a sketchy file. Copies a template and the engine into a folder so the page previews from disk.
import fs from 'node:fs';
import path from 'node:path';
import {
  parseArgs, say, die, rel, SKILL_DIR, ENGINE_DIR, SCRIPT_DIR, sketchyHome, isMain,
} from './_lib.mjs';

export const TYPES = ['deck', 'explainer', 'report', 'chart', 'board', 'postcard'];
const NAME_RE = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;

const spec = {
  name: 'sketchy new', file: 'new.mjs', usage: '<deck|explainer|report|chart|board|postcard> <out-folder> [--theme <name>] [--title "..."] [--name slug]',
  summary: 'copy a template and the engine into a folder, ready to fill and preview.',
  details: [
    'Writes <out-folder>/<slug>.html and <out-folder>/engine/ (scripts, styles, fonts, the chosen theme).',
    'The template links ../engine/ and ../themes/; the copy links engine/ and engine/themes/.',
    'Templates and themes are looked up in ./.sketchy/, then ~/.sketchy/ (or $SKETCHY_HOME), then the skill.',
    'An existing file is never overwritten unless you pass --force. Engine files that are identical are skipped.',
  ],
  options: [
    { name: 'theme', type: 'string', arg: 'name', help: 'theme token file to link (day, night, blueprint, cartridge, graph, kraft, or your own)' },
    { name: 'title', type: 'string', arg: 'text', help: 'text of the page <title>' },
    { name: 'name', type: 'string', arg: 'slug', help: 'file name without .html (default: from --title, else the type)' },
    { name: 'force', type: 'boolean', help: 'overwrite files that already exist' },
    { name: 'list', type: 'boolean', help: 'list the templates and themes that can be used, then exit' },
  ],
  positionals: { min: 0, max: 2, name: '<type> <out-folder>' },
  examples: [
    'node new.mjs deck work/q3',
    'node new.mjs deck work/q3 --theme night --title "Q3 for the board" --name q3-board',
    'node new.mjs --list',
  ],
};

/* ---------- lookup: project, user, skill ---------- */
/** The three places user material lives, in priority order (duplicates removed). */
export function lookupRoots() {
  const list = [
    { name: 'project', base: path.resolve('.sketchy') },
    { name: 'user', base: sketchyHome() },
    { name: 'skill', base: SKILL_DIR },
  ];
  const seen = new Set();
  return list.filter((r) => { const k = process.platform === 'win32' ? r.base.toLowerCase() : r.base; if (seen.has(k)) return false; seen.add(k); return true; });
}

const isFile = (p) => { try { return fs.statSync(p).isFile(); } catch { return false; } };

function findIn(kind, name) {
  const dirName = kind === 'template' ? 'templates' : 'themes';
  const ext = kind === 'template' ? '.html' : '.css';
  for (const root of lookupRoots()) {
    const file = path.join(root.base, dirName, name + ext);
    if (isFile(file)) return { file, from: root.name, name };
  }
  return null;
}

function listAll(kind) {
  const dirName = kind === 'template' ? 'templates' : 'themes';
  const ext = kind === 'template' ? '.html' : '.css';
  const out = new Map();
  for (const root of lookupRoots()) {
    let names = [];
    try { names = fs.readdirSync(path.join(root.base, dirName)); } catch { /* folder missing */ }
    for (const f of names) {
      if (!f.endsWith(ext) || f.startsWith('_')) continue;
      const n = f.slice(0, -ext.length);
      if (!out.has(n)) out.set(n, root.name);
    }
  }
  return out;
}

const fmtList = (m) => [...m].map(([n, from]) => (from === 'skill' ? n : `${n} (${from})`)).join(', ') || '(none)';

export const slugify = (s) => String(s || '').normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60);
const escHtml = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/* ---------- the rewrite ---------- */
/**
 * Turn the template text into the page that sits next to its own engine/ folder.
 * Pure function: no files are touched.
 */
export function rewriteTemplate(html, { themeName, dark, title, seed } = {}) {
  let out = html.replace(/^﻿/, '');
  const notes = [];
  out = out.replace(/\.\.\/engine\//g, 'engine/').replace(/\.\.\/themes\//g, 'engine/themes/');
  if (title) {
    if (/<title>[\s\S]*?<\/title>/i.test(out)) out = out.replace(/<title>[\s\S]*?<\/title>/i, () => `<title>${escHtml(title)}</title>`);
    else { out = out.replace(/<\/head>/i, () => `<title>${escHtml(title)}</title>\n</head>`); notes.push('the template had no <title>; added one'); }
  }
  if (themeName) {
    const link = `<link rel="stylesheet" href="engine/themes/${themeName}.css">`;
    const marker = /<!--\s*slot:theme\b[\s\S]*?-->/;
    if (marker.test(out)) out = out.replace(marker, () => link);
    else {
      const sheets = [...out.matchAll(/<link\b[^>]*rel=["']stylesheet["'][^>]*>/gi)];
      if (sheets.length) { const last = sheets[sheets.length - 1]; out = out.slice(0, last.index + last[0].length) + '\n' + link + out.slice(last.index + last[0].length); }
      else out = out.replace(/<\/head>/i, () => `${link}\n</head>`);
      notes.push('no <!-- slot:theme --> marker in the template; linked the theme after the last stylesheet');
    }
    if (dark) {
      if (/<html\b[^>]*\bdata-theme=/i.test(out)) out = out.replace(/(<html\b[^>]*\bdata-theme=")[^"]*(")/i, (_, a, b) => `${a}night${b}`);
      else out = out.replace(/<html\b/i, '<html data-theme="night"');
    }
  }
  if (seed) {
    let replaced = false;
    out = out.replace(/(\bdata-seed=")([^"]*)(")/, (_, a, old, b) => { replaced = true; return `${a}${seed}${b}`; });
    if (replaced) notes.push(`data-seed set to "${seed}" so this file draws its own lines`);
  }
  return { html: out, notes };
}

/** Local engine/ references in a page that do not exist next to it. */
export function missingRefs(htmlText, folder) {
  const missing = new Set();
  const live = htmlText.replace(/<!--[\s\S]*?-->/g, ''); // an example link inside a comment is not a request
  for (const m of live.matchAll(/\b(?:src|href)=["'](engine\/[^"'#?]+)["']/g)) {
    if (!isFile(path.join(folder, m[1]))) missing.add(m[1]);
  }
  return [...missing];
}

function sameBytes(a, b) {
  try {
    const sa = fs.statSync(a), sb = fs.statSync(b);
    if (sa.size !== sb.size) return false;
    return fs.readFileSync(a).equals(fs.readFileSync(b));
  } catch { return false; }
}

/** Copy a folder tree. Identical files are skipped; different files are kept unless force. */
function copyTree(src, dest, force, stats) {
  fs.mkdirSync(dest, { recursive: true });
  for (const ent of fs.readdirSync(src, { withFileTypes: true })) {
    if (ent.name.startsWith('.')) continue;
    const s = path.join(src, ent.name), d = path.join(dest, ent.name);
    if (ent.isDirectory()) { copyTree(s, d, force, stats); continue; }
    if (!ent.isFile()) continue;
    if (fs.existsSync(d)) {
      if (sameBytes(s, d)) { stats.same++; continue; }
      if (!force) { stats.kept.push(d); continue; }
    }
    fs.copyFileSync(s, d);
    stats.copied++;
  }
}

function main() {
  const { values, positionals } = parseArgs(process.argv.slice(2), spec);

  if (values.list) {
    say.info(`templates: ${fmtList(listAll('template'))}`);
    say.info(`themes:    ${fmtList(listAll('theme'))}`);
    return;
  }
  if (positionals.length < 2) die(positionals.length ? 'missing <out-folder>' : 'missing <type> and <out-folder>', [`node new.mjs <${TYPES.join('|')}> <out-folder>`, 'node new.mjs --list   (shows what can be used)']);

  const type = positionals[0];
  if (!NAME_RE.test(type)) die(`bad template name "${type}"`, `use one of: ${TYPES.join(', ')}`);
  const template = findIn('template', type);
  if (!template) die(`no template named "${type}"`, [`use one of: ${fmtList(listAll('template'))}`, 'or put your own at ./.sketchy/templates/<name>.html']);

  let theme = null;
  if (values.theme) {
    const t = String(values.theme);
    const asFile = path.resolve(t);
    if ((/[\\/]/.test(t) || /\.css$/i.test(t)) && isFile(asFile)) theme = { file: asFile, from: 'file', name: path.basename(asFile, '.css') };
    else {
      const n = t.replace(/\.css$/i, '');
      if (!NAME_RE.test(n)) die(`bad theme name "${t}"`, `use one of: ${fmtList(listAll('theme'))}`);
      theme = findIn('theme', n);
      if (!theme) die(`no theme named "${n}"`, [`use one of: ${fmtList(listAll('theme'))}`, 'or copy themes/_starter.css to ./.sketchy/themes/<name>.css and edit it']);
    }
    if (!NAME_RE.test(theme.name)) die(`theme file name "${theme.name}" has characters that do not belong in a URL`, 'rename the file to letters, digits, - and _');
  }

  const slug = slugify(values.name) || slugify(values.title) || slugify(type) || 'sketchy';
  if (values.name && slugify(values.name) !== values.name) say.warn(`--name "${values.name}" became "${slug}"`);
  const out = path.resolve(positionals[1]);
  const target = path.join(out, `${slug}.html`);
  if (fs.existsSync(out) && !fs.statSync(out).isDirectory()) die(`not a folder: ${positionals[1]}`, 'pass a folder path (it is created when missing)');
  if (fs.existsSync(target) && !values.force) die(`${rel(target)} already exists`, [`pick another name: --name <slug>`, 'or replace it: --force']);

  const css = theme ? fs.readFileSync(theme.file, 'utf8') : '';
  const dark = theme ? (theme.name === 'night' || /--sk-paper-kind\s*:\s*dark/i.test(css)) : false;
  const { html, notes } = rewriteTemplate(fs.readFileSync(template.file, 'utf8'), {
    themeName: theme && theme.name, dark, title: values.title, seed: slug,
  });

  fs.mkdirSync(out, { recursive: true });
  const stats = { copied: 0, same: 0, kept: [] };
  copyTree(ENGINE_DIR, path.join(out, 'engine'), values.force, stats);
  if (theme) {
    const dest = path.join(out, 'engine', 'themes', `${theme.name}.css`);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    if (!fs.existsSync(dest) || values.force || sameBytes(theme.file, dest)) { fs.copyFileSync(theme.file, dest); stats.copied++; }
    else stats.kept.push(dest);
  }
  fs.writeFileSync(target, html);

  say.ok(`${type}  ${rel(target)}  (template from ${template.from})`);
  say.ok(`engine  ${rel(path.join(out, 'engine'))}  (${stats.copied} copied${stats.same ? `, ${stats.same} already there` : ''})`);
  if (theme) say.ok(`theme   ${theme.name}  ${rel(path.join(out, 'engine', 'themes', `${theme.name}.css`))}  (from ${theme.from})${dark ? '  data-theme="night" set' : ''}`);
  for (const n of notes) say.info(n);
  for (const k of stats.kept) say.warn(`kept your existing ${rel(k)} (it differs from the skill's copy)`);
  if (stats.kept.length) say.fix('add --force to replace it with the skill copy');
  for (const m of missingRefs(html, out)) say.warn(`the page links ${m} but ${rel(path.join(out, m))} does not exist`);

  const q = (p) => (/\s/.test(p) ? `"${p}"` : p);
  const script = (n) => q(rel(path.join(SCRIPT_DIR, n)));
  const built = path.join(out, 'out', `${slug}.html`);
  say.line();
  say.line('next:');
  say.line(`  1. fill the <!-- slot:... --> parts in ${rel(target)}`);
  say.line(`  2. node ${script('build.mjs')} ${q(rel(target))}`);
  say.line(`  3. node ${script('lint.mjs')} ${q(rel(built))}`);
  say.line(`  4. node ${script('shoot.mjs')} ${q(rel(built))}`);
}

if (isMain(import.meta.url)) {
  try { main(); } catch (e) { die(`new failed: ${String(e && e.message ? e.message : e).split('\n')[0]}`, 'check that the folder is writable', 1); }
}
