// Is there a PublicOS skill for that? Search the catalogue by what you want to do.
//   node find_skill.js <words…>          e.g.  node find_skill.js follow private channel
//   node find_skill.js --all             the whole catalogue
// Reads catalogue.json: the file beside this folder, or (when it is not there) https://publicos.dev/agents/catalogue.json.
// A row with no skill is an honest "no": it says what to do instead. No key, no dependencies.
const fs = require('fs'), path = require('path');
const UA = process.env.PUBLICOS_UA || 'PublicOS-Agent/1.0 (+https://publicos.dev/agents)';

async function catalogue() {
  for (const p of [path.join(__dirname, '..', 'catalogue.json'), path.join(__dirname, 'catalogue.json')]) { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch {} }
  const r = await fetch(process.env.PUBLICOS_CATALOGUE || 'https://publicos.dev/agents/catalogue.json', { headers: { 'user-agent': UA } });
  if (!r.ok) throw new Error(`could not fetch the catalogue (HTTP ${r.status})`);
  return r.json();
}
const STOP = new Set('the and for how much many what who whom which that this with from have has had does did can could may are was were been not you your mine his her its our their them they into onto about there here some any all one out get got let see tell show want need know make made'.split(' '));
const words = (s) => String(s).toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(/\s+/).filter(w => w.length > 2 && !STOP.has(w));
const stem = (w) => w.replace(/(ing|ers|er|ed|es|s)$/, '');

(async () => {
  const args = process.argv.slice(2);
  const cat = await catalogue();
  const show = (w) => console.log(`  ${w.want}\n      ${w.skill ? `${w.skill}:  node scripts/${w.how}` : `no skill. ${w.how}`}`);
  if (!args.length || args[0] === '--all') { let area = ''; for (const w of cat.wants) { if (w.area !== area) console.log(`\n${area = w.area}`); show(w); } return; }
  const q = words(args.join(' ')).map(stem);
  const byName = Object.fromEntries(cat.skills.map(s => [s.name, s]));
  const scored = cat.wants.map(w => {
    const near = words(w.want).map(stem), far = words(`${w.how} ${w.skill || ''} ${w.skill ? byName[w.skill].description : ''}`).map(stem);
    return [q.reduce((n, t) => n + (near.includes(t) ? 3 : far.includes(t) ? 1 : 0), 0), w];
  }).filter(([n]) => n > 0).sort((a, b) => b[0] - a[0]).slice(0, 6);
  if (!scored.length) { console.log('nothing matches those words. Try fewer or other words, or: node find_skill.js --all'); process.exit(1); }
  for (const [, w] of scored) show(w);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
