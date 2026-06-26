#!/usr/bin/env node
/*
  Cheap OpenAPI YAML summarizer (no deps).
  Extracts:
  - servers
  - paths + methods

  Usage:
    node sure_openapi_summarize.js references/openapi.yaml
*/

const fs = require('fs');

const file = process.argv[2];
if (!file) {
  console.error('Usage: sure_openapi_summarize.js <openapi.yaml>');
  process.exit(2);
}

const text = fs.readFileSync(file, 'utf8');
const lines = text.split(/\r?\n/);

let inServers = false;
let inPaths = false;
let currentPath = null;

const servers = [];
const paths = new Map(); // path -> Set(method)

function addMethod(p, m) {
  if (!paths.has(p)) paths.set(p, new Set());
  paths.get(p).add(m.toUpperCase());
}

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  // Section toggles
  if (/^servers:\s*$/.test(line)) {
    inServers = true;
    inPaths = false;
    continue;
  }
  if (/^paths:\s*$/.test(line)) {
    inPaths = true;
    inServers = false;
    continue;
  }
  if (/^[A-Za-z_]+:\s*$/.test(line) && !/^servers:\s*$/.test(line) && !/^paths:\s*$/.test(line)) {
    // leaving servers/paths when another top-level key starts
    if (/^[^\s]/.test(line)) {
      inServers = false;
      inPaths = false;
      currentPath = null;
    }
  }

  if (inServers) {
    const m = line.match(/^\-\s+url:\s*(.+)\s*$/);
    if (m) {
      servers.push(m[1].trim());
    }
  }

  if (inPaths) {
    const p = line.match(/^\s+"?(\/[^\"]+)"?:\s*$/);
    if (p) {
      currentPath = p[1];
      continue;
    }
    const mm = line.match(/^\s{2,6}(get|post|put|patch|delete|options|head):\s*$/i);
    if (mm && currentPath) {
      addMethod(currentPath, mm[1]);
      continue;
    }
  }
}

const sortedPaths = [...paths.entries()]
  .map(([p, methods]) => ({ p, methods: [...methods].sort() }))
  .sort((a, b) => a.p.localeCompare(b.p));

console.log('# Sure API endpoints (generated)');
console.log('');
console.log(`Generated from: ${file}`);
console.log('');
console.log('## Servers');
for (const s of servers) console.log(`- ${s}`);
console.log('');
console.log('## Paths');
for (const { p, methods } of sortedPaths) {
  console.log('- `' + p + '`  (' + methods.join(', ') + ')');
}
