// Copy final.mp4 to a deploy directory with a timestamped name.
// Defaults: ./output/  +  prefix "screencast"
// Override via env: DEPLOY_DIR, DEPLOY_PREFIX
const fs = require('fs');
const path = require('path');

const DEPLOY_DIR = process.env.DEPLOY_DIR || path.join(__dirname, 'output');
const PREFIX = process.env.DEPLOY_PREFIX || 'screencast';
const SRC = path.join(__dirname, 'final.mp4');

if (!fs.existsSync(SRC)) {
  console.error('final.mp4 not found — run `npm run demo` first.');
  process.exit(1);
}

if (!fs.existsSync(DEPLOY_DIR)) fs.mkdirSync(DEPLOY_DIR, { recursive: true });

const stamp = new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-');
const dst = path.join(DEPLOY_DIR, `${PREFIX}-${stamp}.mp4`);
fs.copyFileSync(SRC, dst);
const sizeMB = (fs.statSync(dst).size / 1024 / 1024).toFixed(2);
console.log(`DEPLOYED: ${dst}  (${sizeMB} MB)`);

// Optional: list 5 most recent deploys for context
const recent = fs.readdirSync(DEPLOY_DIR)
  .filter((f) => f.startsWith(PREFIX) && f.endsWith('.mp4'))
  .map((f) => ({ name: f, mtime: fs.statSync(path.join(DEPLOY_DIR, f)).mtime }))
  .sort((a, b) => b.mtime - a.mtime)
  .slice(0, 5);
console.log('\nrecent:');
recent.forEach((r) => {
  const mb = (fs.statSync(path.join(DEPLOY_DIR, r.name)).size / 1024 / 1024).toFixed(2);
  console.log(`  ${r.name}  ${mb} MB`);
});
