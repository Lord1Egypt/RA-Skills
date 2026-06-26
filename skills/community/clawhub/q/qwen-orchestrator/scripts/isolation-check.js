#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const SELF = 'qwen-orchestrator';
const OTHER = 'ai-orchestrator';
const root = path.resolve(__dirname, '..');
const otherRoot = path.resolve(root, '..', OTHER);

const local = {
  profile: path.join(root, '.profile'),
  sessions: path.join(root, '.sessions'),
  endpoint: path.join(root, '.daemon-ws-endpoint'),
};
const other = {
  profile: path.join(otherRoot, '.profile'),
  sessions: path.join(otherRoot, '.sessions'),
  endpoint: path.join(otherRoot, '.daemon-ws-endpoint'),
};

function fail(msg) {
  console.error(`❌ isolation-check (${SELF}): ${msg}`);
  process.exit(1);
}

function ok(msg) {
  console.log(`✅ ${msg}`);
}

function sameRealPath(a, b) {
  try {
    return fs.existsSync(a) && fs.existsSync(b) && fs.realpathSync(a) === fs.realpathSync(b);
  } catch {
    return path.resolve(a) === path.resolve(b);
  }
}

function assertDistinct(name, a, b) {
  if (path.resolve(a) === path.resolve(b) || sameRealPath(a, b)) {
    fail(`${name} must be distinct from ${OTHER}: ${a} vs ${b}`);
  }
  ok(`${name} is distinct`);
}

function scanFiles(dir, exts = new Set(['.js', '.sh'])) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...scanFiles(full, exts));
    } else if (exts.has(path.extname(entry.name))) {
      out.push(full);
    }
  }
  return out;
}

function assertNoCrossReferences() {
  const files = scanFiles(root).filter((file) => !file.endsWith(path.join('scripts', 'isolation-check.js')));
  const bad = [];
  const patterns = [
    '../ai-orchestrator',
    'ai-orchestrator/',
    'skills/ai-orchestrator',
  ];
  for (const file of files) {
    const text = fs.readFileSync(file, 'utf8');
    if (patterns.some((p) => text.includes(p))) {
      bad.push(path.relative(root, file));
    }
  }
  if (bad.length) {
    fail(`cross-skill runtime references detected: ${bad.join(', ')}`);
  }
  ok('no cross-skill runtime references found');
}

function main() {
  if (!fs.existsSync(root)) fail(`missing skill root: ${root}`);
  if (!fs.existsSync(otherRoot)) fail(`missing sibling skill root: ${otherRoot}`);

  assertDistinct('profile dir', local.profile, other.profile);
  assertDistinct('sessions dir', local.sessions, other.sessions);
  assertDistinct('daemon endpoint file', local.endpoint, other.endpoint);
  assertNoCrossReferences();

  console.log(`🧩 ${SELF} isolation check passed`);
}

main();
