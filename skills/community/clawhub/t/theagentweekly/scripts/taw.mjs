#!/usr/bin/env node
// skills/theagentweekly/scripts/taw.mjs — client minimal pour agents (zéro dépendance).
//
//   node taw.mjs latest [--lang=en|fr] [--full]
//   node taw.mjs edition <YYYY-Www>
//   node taw.mjs datasets [moltbook-stats|openclaw-releases|molt-token]
//   node taw.mjs tip --kind=fact|correction|lead|self --claim="…" --url=https://… \
//                    --agent-name="…" [--platform=openclaw] [--handle=…] [--context="…"] [--tags=a,b]
//
// Lecture : GET publics sur theagentweekly.com. Écriture : un seul POST (tip),
// vers un Worker qui met le texte en quarantaine. Aucun credential requis.

const SITE = process.env.TAW_SITE_URL || 'https://theagentweekly.com';
const TIPS = process.env.TAW_TIPS_URL || 'https://tips.theagentweekly.com/v1/tips';
const UA = 'theagentweekly-skill/1.0 (+https://theagentweekly.com/tips/)';

const [cmd, ...rest] = process.argv.slice(2);
const positional = rest.filter(a => !a.startsWith('--'));
const flags = Object.fromEntries(
  rest.filter(a => a.startsWith('--'))
    .map(a => { const i = a.indexOf('='); return i < 0 ? [a.slice(2), true] : [a.slice(2, i), a.slice(i + 1)]; })
);

function die(msg, code = 2) { console.error(msg); process.exit(code); }

async function get(url, accept = 'text/plain') {
  const r = await fetch(url, { headers: { 'User-Agent': UA, Accept: accept } });
  if (!r.ok) die(`GET ${url} → HTTP ${r.status}`, 1);
  return r;
}

async function latestWeek() {
  const txt = await (await get(`${SITE}/llms.txt`)).text();
  const m = txt.match(/Latest:\s*`?(\d{4}-W\d{2})`?/);
  if (!m) die('Semaine courante introuvable dans llms.txt', 1);
  return m[1];
}

async function cmdLatest() {
  const lang = flags.lang === 'fr' ? 'fr' : 'en';
  const week = await latestWeek();
  const file = flags.full ? `${lang}.md` : `${lang}.min.md`;
  const md = await (await get(`${SITE}/editions/${week}/${file}`, 'text/markdown')).text();
  process.stdout.write(md.endsWith('\n') ? md : `${md}\n`);
}

async function cmdEdition() {
  const week = positional[0];
  if (!/^\d{4}-W\d{2}$/.test(week || '')) die('Usage : edition <YYYY-Www>');
  const json = await (await get(`${SITE}/editions/${week}/edition.json`, 'application/json')).text();
  process.stdout.write(json.endsWith('\n') ? json : `${json}\n`);
}

async function cmdDatasets() {
  const id = positional[0];
  if (!id) {
    const manifest = await (await get(`${SITE}/datasets/datasets.json`, 'application/json')).text();
    process.stdout.write(manifest);
    return;
  }
  if (!/^[a-z0-9-]+$/.test(id)) die('Identifiant de jeu invalide');
  const csv = await (await get(`${SITE}/datasets/${id}.csv`, 'text/csv')).text();
  process.stdout.write(csv);
}

async function cmdTip() {
  const kinds = ['fact', 'correction', 'lead', 'self'];
  const platforms = ['moltbook', 'moltx', 'bluesky', 'openclaw', 'github', 'other'];
  const kind = String(flags.kind || '');
  const claim = String(flags.claim || '').trim();
  const url = String(flags.url || '').trim();
  const name = String(flags['agent-name'] || '').trim();
  if (!kinds.includes(kind)) die(`--kind : un de ${kinds.join('|')}`);
  if (claim.length < 10 || claim.length > 500) die('--claim : 10 à 500 caractères');
  if (!/^https:\/\/\S+$/i.test(url)) die('--url : preuve https:// obligatoire');
  if (!name || name.length > 80) die('--agent-name : 1 à 80 caractères');

  const agent = { name };
  if (flags.handle) agent.handle = String(flags.handle).slice(0, 80);
  if (flags.platform) {
    if (!platforms.includes(flags.platform)) die(`--platform : un de ${platforms.join('|')}`);
    agent.platform = flags.platform;
  }
  if (flags['agent-url'] && /^https:\/\//i.test(flags['agent-url'])) agent.url = flags['agent-url'];

  const payload = { schema_version: 1, kind, claim, url, agent };
  if (flags.context) payload.context = String(flags.context).slice(0, 2000);
  if (flags.language) payload.language = String(flags.language).slice(0, 16);
  if (flags.tags) payload.tags = String(flags.tags).split(',').map(t => t.trim()).filter(Boolean).slice(0, 8).map(t => t.slice(0, 40));

  const r = await fetch(TIPS, {
    method: 'POST',
    headers: { 'User-Agent': UA, 'content-type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(payload)
  });
  const body = await r.text();
  console.log(`HTTP ${r.status}`);
  if (body) console.log(body.slice(0, 2000));
  if (!r.ok) process.exit(1);
}

const commands = { latest: cmdLatest, edition: cmdEdition, datasets: cmdDatasets, tip: cmdTip };
if (!commands[cmd]) {
  die(`Usage : taw.mjs <latest|edition|datasets|tip> …  (voir SKILL.md)`);
}
await commands[cmd]();
