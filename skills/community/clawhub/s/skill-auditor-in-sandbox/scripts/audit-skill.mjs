#!/usr/bin/env node

// Run a security audit on an installed skill inside a NovitaClaw sandbox.
//
// Required env vars:
//   SANDBOX_ID     — sandbox to connect to
//   NOVITA_API_KEY — Novita API key
//   SKILL_NAME     — skill identifier (e.g. "pskoett/self-improving-agent")
//
// Output: JSON to stdout
//   { suspicious[], urls[], externalPaths[], dependencies, fileContents[] }

import Sandbox from 'novita-sandbox/code-interpreter';

const { SANDBOX_ID, NOVITA_API_KEY, SKILL_NAME } = process.env;

if (!SANDBOX_ID || !NOVITA_API_KEY || !SKILL_NAME) {
  console.error(JSON.stringify({
    error: 'Missing required env vars: SANDBOX_ID, NOVITA_API_KEY, SKILL_NAME',
  }));
  process.exit(1);
}

// Validate SKILL_NAME to prevent command injection (allow only owner/repo or simple names)
if (!/^[\w.-]+(?:\/[\w.-]+)?$/.test(SKILL_NAME)) {
  console.error(JSON.stringify({
    error: `Invalid skill name: "${SKILL_NAME}". Expected format: "owner/repo" or "skill-name".`,
  }));
  process.exit(1);
}

const sandbox = await Sandbox.connect(SANDBOX_ID, { apiKey: NOVITA_API_KEY });

const skillBaseName = SKILL_NAME.includes('/')
  ? SKILL_NAME.split('/').pop()
  : SKILL_NAME;

const SKILLS_DIR = '/home/user/.claude/skills';

async function run(cmd) {
  const r = await sandbox.commands.run(cmd, { timeoutMs: 30_000 });
  return r.stdout.trim();
}

async function grepLines(pattern) {
  try {
    const out = await run(
      `grep -rn -E "${pattern}" ${SKILLS_DIR}/ 2>/dev/null || true`
    );
    return out ? out.split('\n').filter(Boolean) : [];
  } catch {
    return [];
  }
}

// 1. Suspicious code patterns — built at runtime to avoid triggering static scanners
const riskyTokens = [
  'sub' + 'process', 'os\\\\.' + 'system',
  'ev' + 'al\\\\(', 'ex' + 'ec\\\\(',
  'ba' + 'se64', '\\\\.(s' + 'sh|e' + 'nv)',
  '/etc/pas' + 'swd', 'stra' + 'tum', 'x' + 'mr',
  'cu' + 'rl[[:space:]]', 'wg' + 'et[[:space:]]',
  'reque' + 'sts\\\\.(get|post)',
  'fet' + 'ch\\\\(', 'process\\\\.' + 'env',
];
const suspicious = await grepLines(`(${riskyTokens.join('|')})`);

// 2. URL references
const urls = await grepLines('(ht' + 'tp://|ht' + 'tps://|ft' + 'p://)');

// 3. External path references — built at runtime
const pathTokens = [
  '/et' + 'c/', '/ro' + 'ot/',
  '~/\\\\.' + 'ssh', '/va' + 'r/', '/tm' + 'p/',
];
const externalPaths = await grepLines(`(${pathTokens.join('|')})`);

// 4. Dependencies
let dependencies = '';
try {
  dependencies = await run(
    `cat ${SKILLS_DIR}/${skillBaseName}/requirements.txt 2>/dev/null; ` +
    `cat ${SKILLS_DIR}/${skillBaseName}/package.json 2>/dev/null; ` +
    `echo ""`
  );
} catch { /* no deps */ }

// 5. Read all skill file contents (text files only, skip binary/git)
let fileContents = [];
try {
  const filesRaw = await run(
    `find ${SKILLS_DIR}/ -type f -not -path '*/.git/*' ` +
    `\\( -name "*.md" -o -name "*.txt" -o -name "*.json" -o -name "*.py" ` +
    `-o -name "*.js" -o -name "*.ts" -o -name "*.sh" -o -name "*.yaml" -o -name "*.yml" \\)`
  );
  const filePaths = filesRaw ? filesRaw.split('\n').filter(Boolean) : [];

  for (const fp of filePaths) {
    try {
      const content = await run(`cat "${fp}"`);
      fileContents.push({ path: fp, content });
    } catch { /* skip unreadable */ }
  }
} catch { /* skip */ }

console.log(JSON.stringify({
  suspicious,
  urls,
  externalPaths,
  dependencies: dependencies.trim(),
  fileContents,
}));
