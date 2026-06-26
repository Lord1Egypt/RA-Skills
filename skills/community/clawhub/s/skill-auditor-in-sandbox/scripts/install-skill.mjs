#!/usr/bin/env node

// Install a skill into a NovitaClaw sandbox.
//
// Required env vars:
//   SANDBOX_ID    — sandbox to connect to
//   NOVITA_API_KEY — Novita API key
//   SKILL_NAME    — skill identifier (e.g. "pskoett/self-improving-agent")
//
// Output: JSON to stdout
//   { success, method, files, error? }

import Sandbox from 'novita-sandbox/code-interpreter';

const { SANDBOX_ID, NOVITA_API_KEY, SKILL_NAME } = process.env;

if (!SANDBOX_ID || !NOVITA_API_KEY || !SKILL_NAME) {
  console.error(JSON.stringify({
    success: false,
    error: 'Missing required env vars: SANDBOX_ID, NOVITA_API_KEY, SKILL_NAME',
  }));
  process.exit(1);
}

// Validate SKILL_NAME to prevent command injection (allow only owner/repo or simple names)
if (!/^[\w.-]+(?:\/[\w.-]+)?$/.test(SKILL_NAME)) {
  console.error(JSON.stringify({
    success: false,
    error: `Invalid skill name: "${SKILL_NAME}". Expected format: "owner/repo" or "skill-name".`,
  }));
  process.exit(1);
}

const sandbox = await Sandbox.connect(SANDBOX_ID, { apiKey: NOVITA_API_KEY });

const skillBaseName = SKILL_NAME.includes('/')
  ? SKILL_NAME.split('/').pop()
  : SKILL_NAME;

const SKILLS_DIR = '/home/user/.claude/skills';
const TARGET_DIR = `${SKILLS_DIR}/${skillBaseName}`;
const TMP_DIR = `/tmp/${skillBaseName}`;

async function run(cmd, timeoutMs = 120_000) {
  return sandbox.commands.run(cmd, { timeoutMs });
}

async function tryRun(cmd, timeoutMs = 120_000) {
  try {
    const r = await run(cmd, timeoutMs);
    return { ok: r.exitCode === 0, stdout: r.stdout, stderr: r.stderr };
  } catch (e) {
    return { ok: false, stdout: '', stderr: e.result?.stderr || e.message };
  }
}

// --- Attempt 1: clawhub install ---
let method = 'clawhub';
let result = await tryRun(`clawhub install ${SKILL_NAME}`);

// --- Attempt 2: git clone from GitHub ---
if (!result.ok) {
  method = 'git-github';
  await tryRun(`rm -r ${TMP_DIR}`);
  result = await tryRun(`git clone https://github.com/${SKILL_NAME}.git ${TMP_DIR}`);
}

// --- Attempt 3: git clone from clawhub.ai ---
if (!result.ok) {
  method = 'git-clawhub';
  await tryRun(`rm -r ${TMP_DIR}`);
  result = await tryRun(`git clone https://clawhub.ai/${SKILL_NAME}.git ${TMP_DIR}`);
}

if (!result.ok) {
  console.log(JSON.stringify({
    success: false,
    method,
    error: `All install methods failed. Last error: ${result.stderr}`,
  }));
  process.exit(1);
}

// If installed via git clone, copy to skills directory
if (method !== 'clawhub') {
  await run(`mkdir -p ${TARGET_DIR}`);

  // Detect structure: does the clone have .claude/skills/?
  const hasClaudeSkills = await tryRun(`test -d ${TMP_DIR}/.claude/skills`);

  if (hasClaudeSkills.ok) {
    await run(`cp -r ${TMP_DIR}/.claude/skills/* ${SKILLS_DIR}/`);
  } else {
    // Copy everything except .git
    await run(`cp -a ${TMP_DIR}/. ${TARGET_DIR}/ && rm -r ${TARGET_DIR}/.git`);
  }
}

// List installed files
const filesResult = await run(`find ${SKILLS_DIR}/ -type f -not -path '*/.git/*'`, 30_000);
const files = filesResult.stdout.trim().split('\n').filter(Boolean);

console.log(JSON.stringify({
  success: true,
  method,
  skillDir: TARGET_DIR,
  files,
}));
