// Periodic cleanup. Keep core scripts + current outputs; drop scratch files.
// Run: node clean.js
const fs = require('fs');
const path = require('path');

const KEEP_FILES = new Set([
  // pipeline scripts
  'login.js', 'record.js', 'postprocess.js', 'review.js',
  'gen-cursor.js', 'gen-ripple.js', 'deploy.js', 'clean.js',
  // node project
  'package.json', 'package-lock.json',
  // session + assets
  'storageState.json', 'cursor.png', 'ripple.png',
  'post-login.png', 'post-login-summary.json',
  // current outputs
  'raw.webm', 'events.json', 'subs.srt', 'final.mp4',
]);
const KEEP_DIRS = new Set(['node_modules', 'videos', 'review', 'output']);
const ROOT = __dirname;

function rmRecurse(p) {
  if (!fs.existsSync(p)) return;
  const stat = fs.statSync(p);
  if (stat.isDirectory()) {
    fs.readdirSync(p).forEach((f) => rmRecurse(path.join(p, f)));
    fs.rmdirSync(p);
  } else {
    fs.unlinkSync(p);
  }
}

let removed = 0;
for (const name of fs.readdirSync(ROOT)) {
  const p = path.join(ROOT, name);
  const isDir = fs.statSync(p).isDirectory();
  if (isDir && KEEP_DIRS.has(name)) continue;
  if (!isDir && KEEP_FILES.has(name)) continue;
  console.log('rm', isDir ? `${name}/` : name);
  rmRecurse(p);
  removed++;
}
console.log(`Removed ${removed} entries. ${KEEP_FILES.size} files + ${KEEP_DIRS.size} dirs preserved.`);
