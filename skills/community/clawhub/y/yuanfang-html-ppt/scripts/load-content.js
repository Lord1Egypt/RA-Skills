// load-content.js — auto-detect and parse content.json / .yaml / .yml
//
// All three formats share the same schema. We use the extension to pick
// the parser. Keeps the data format flexible for AI agents (JSON is
// natural for code, YAML is friendlier for humans).

'use strict';

const fs = require('node:fs');
const yaml = require('js-yaml');

function loadContent(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const ext = filePath.toLowerCase().split('.').pop();
  if (ext === 'json') {
    return JSON.parse(raw);
  } else if (ext === 'yaml' || ext === 'yml') {
    return yaml.load(raw);
  }
  // Fallback: try JSON first, then YAML
  try { return JSON.parse(raw); }
  catch { return yaml.load(raw); }
}

module.exports = { loadContent };
