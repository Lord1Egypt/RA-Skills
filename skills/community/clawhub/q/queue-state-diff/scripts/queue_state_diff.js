const fs = require('fs');
const path = require('path');
function arg(name) { const i = process.argv.indexOf(name); return i >= 0 ? process.argv[i + 1] : null; }
function readJson(p) { return JSON.parse(fs.readFileSync(path.resolve(p), 'utf8').replace(/^\uFEFF/, '')); }
function flatten(obj, prefix = '', out = {}) {
  if (Array.isArray(obj)) { out[prefix || '$'] = `[array:${obj.length}]`; return out; }
  if (!obj || typeof obj !== 'object') { out[prefix || '$'] = obj; return out; }
  for (const [k, v] of Object.entries(obj)) flatten(v, prefix ? `${prefix}.${k}` : k, out);
  return out;
}
const before = readJson(arg('--before'));
const after = readJson(arg('--after'));
const outPath = path.resolve(arg('--out'));
const a = flatten(before), b = flatten(after);
const keys = [...new Set([...Object.keys(a), ...Object.keys(b)])].sort();
const added = [], removed = [], changed = [];
for (const k of keys) {
  if (!(k in a)) added.push({ key: k, value: b[k] });
  else if (!(k in b)) removed.push({ key: k, value: a[k] });
  else if (JSON.stringify(a[k]) !== JSON.stringify(b[k])) changed.push({ key: k, before: a[k], after: b[k] });
}
const lines = ['# Queue / State Diff', '', `- Added keys: ${added.length}`, `- Removed keys: ${removed.length}`, `- Changed keys: ${changed.length}`, '', '## Changed'];
changed.slice(0, 100).forEach(x => lines.push(`- ${x.key}: ${JSON.stringify(x.before)} -> ${JSON.stringify(x.after)}`));
lines.push('', '## Added'); added.slice(0, 50).forEach(x => lines.push(`- ${x.key}: ${JSON.stringify(x.value)}`));
lines.push('', '## Removed'); removed.slice(0, 50).forEach(x => lines.push(`- ${x.key}: ${JSON.stringify(x.value)}`));
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, lines.join('\n'), 'utf8');
process.stdout.write(JSON.stringify({ ok: true, out: outPath, added: added.length, removed: removed.length, changed: changed.length }, null, 2) + '\n');
