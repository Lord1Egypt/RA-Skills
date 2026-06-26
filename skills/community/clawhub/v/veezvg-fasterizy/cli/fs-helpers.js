const fs = require('fs');
const path = require('path');

function readJson(p) {
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function writeJson(p, data) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(data, null, 2) + '\n');
}

function backupIfExists(p) {
  if (fs.existsSync(p)) fs.copyFileSync(p, p + '.bak');
}

module.exports = { readJson, writeJson, backupIfExists };
