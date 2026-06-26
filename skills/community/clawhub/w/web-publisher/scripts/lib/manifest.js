'use strict';

// Reads the version field from the colocated skill manifest (config.json).
// This module performs only a single, scoped read of a file that ships with
// the skill itself. It does not access environment variables and does not
// perform any network I/O.

const fs = require('fs');
const path = require('path');

function readSkillVersion() {
  try {
    const cfgPath = path.join(__dirname, '..', '..', 'config.json');
    const raw = fs.readFileSync(cfgPath, 'utf8');
    const cfg = JSON.parse(raw);
    return (cfg && cfg.version) || (cfg && cfg.skill && cfg.skill.version) || '0.0.0';
  } catch (_) {
    return '0.0.0';
  }
}

module.exports = { readSkillVersion };
