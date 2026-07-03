#!/usr/bin/env node
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { homedir } from 'node:os';

const STATE_PATH = process.env.SUPERADA_WATCH_STATE || join(homedir(), '.superada', 'weekly-watch-state.json');
const SOURCES = [
  { key: 'rss', label: 'Ship Log RSS', url: 'https://superada.ai/rss.xml', type: 'rss' },
  { key: 'changelog', label: 'OpenClaw Changelog', url: 'https://superada.ai/openclaw-changelog', type: 'html-title' },
  { key: 'weekly-claw', label: 'Weekly Claw', url: 'https://superada.ai/weekly-claw', type: 'html-title' },
  { key: 'tools', label: 'Tools', url: 'https://superada.ai/resources/tools', type: 'html-title' },
  { key: 'skills', label: 'Skills', url: 'https://superada.ai/resources/skills', type: 'html-title' },
  { key: 'workflow-packs', label: 'Workflow Packs', url: 'https://superada.ai/resources/workflow-packs', type: 'html-title' },
];

async function fetchText(url) {
  const response = await fetch(url, { headers: { 'User-Agent': 'superada-weekly-watch/1.0' } });
  if (!response.ok) throw new Error(`${url} returned ${response.status}`);
  return response.text();
}

function decode(value = '') {
  return value
    .replaceAll('&amp;', '&')
    .replaceAll('&quot;', '"')
    .replaceAll('&#39;', "'")
    .replaceAll('&apos;', "'")
    .replaceAll('&lt;', '<')
    .replaceAll('&gt;', '>')
    .trim();
}

function parseRss(xml) {
  return [...xml.matchAll(/<item>[\s\S]*?<\/item>/g)].slice(0, 12).map((match) => {
    const item = match[0];
    return {
      title: decode(item.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>|<title>([\s\S]*?)<\/title>/)?.[1] || item.match(/<title>([\s\S]*?)<\/title>/)?.[1] || ''),
      url: decode(item.match(/<link>([\s\S]*?)<\/link>/)?.[1] || ''),
      date: decode(item.match(/<pubDate>([\s\S]*?)<\/pubDate>/)?.[1] || ''),
    };
  }).filter((item) => item.title && item.url);
}

function parseHtmlTitle(html, source) {
  const title = decode(html.match(/<title>([\s\S]*?)<\/title>/i)?.[1] || source.label);
  const h1 = decode(html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i)?.[1]?.replace(/<[^>]+>/g, '') || title);
  const fingerprint = String(html.length) + ':' + (html.match(/datetime="([^"]+)"/)?.[1] || html.match(/<time[^>]*>([\s\S]*?)<\/time>/i)?.[1] || h1);
  return [{ title: h1, url: source.url, date: '', fingerprint }];
}

async function readState() {
  try { return JSON.parse(await readFile(STATE_PATH, 'utf8')); } catch { return { seen: {}, checkedAt: null }; }
}

async function writeState(state) {
  await mkdir(dirname(STATE_PATH), { recursive: true });
  await writeFile(STATE_PATH, JSON.stringify(state, null, 2) + '\n');
}

const state = await readState();
const nextState = { seen: { ...(state.seen || {}) }, checkedAt: new Date().toISOString() };
const sections = [];

for (const source of SOURCES) {
  try {
    const text = await fetchText(source.url);
    const items = source.type === 'rss' ? parseRss(text) : parseHtmlTitle(text, source);
    const previous = new Set(state.seen?.[source.key] || []);
    const currentIds = items.map((item) => `${item.title}|${item.url}|${item.fingerprint || item.date || ''}`);
    const fresh = state.checkedAt ? items.filter((item, index) => !previous.has(currentIds[index])) : items.slice(0, source.type === 'rss' ? 5 : 1);
    nextState.seen[source.key] = currentIds.slice(0, 30);
    sections.push({ source, fresh, total: items.length });
  } catch (error) {
    sections.push({ source, error: error.message, fresh: [] });
  }
}

await writeState(nextState);

console.log('## SuperAda weekly watch\n');
if (!state.checkedAt) console.log('First run baseline created. Showing current highlights.\n');
let anyFresh = false;
for (const section of sections) {
  if (section.error) {
    console.log(`### ${section.source.label}\n- Check failed: ${section.error}\n`);
    continue;
  }
  if (!section.fresh.length) continue;
  anyFresh = true;
  console.log(`### ${section.source.label}`);
  for (const item of section.fresh) console.log(`- [${item.title}](${item.url})${item.date ? ` - ${item.date}` : ''}`);
  console.log('');
}
if (!anyFresh) console.log('No new SuperAda posts, releases, tools, skills, workflow packs, or Weekly Claw updates since the last check.');
console.log(`\nChecked: ${nextState.checkedAt}`);
console.log(`State: ${STATE_PATH}`);
