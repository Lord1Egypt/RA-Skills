'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');

function evidencePath(options) {
  const home = (options && options.homeDir) || os.homedir();
  return path.join(home, '.yottaskills', 'install-log.jsonl');
}

function appendEvidence(entry, options) {
  const file = evidencePath(options);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, JSON.stringify(entry) + '\n', 'utf8');
  return file;
}

module.exports = { evidencePath, appendEvidence };
