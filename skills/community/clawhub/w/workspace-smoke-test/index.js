#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = process.env.WORKSPACE_ROOT || process.cwd();

function checkSkill(name, skillDir) {
  const skillPath = path.join(WORKSPACE, 'skills', skillDir);
  const indexPath = path.join(skillPath, 'index.js');
  try {
    if (!fs.existsSync(indexPath)) return { name, ok: false, reason: 'missing index.js' };
    const mod = require(indexPath);
    const keys = Object.keys(mod);
    return { name, ok: true, exports: keys.length };
  } catch (e) {
    return { name, ok: false, reason: e.message.slice(0, 80) };
  }
}

function checkEvolver() {
  try {
    const out = execSync('evolver --version 2>&1 || true', { encoding: 'utf8', timeout: 5000 });
    return { ok: true, version: out.trim().split('\n')[0] };
  } catch (e) {
    return { ok: false, reason: e.message.slice(0, 80) };
  }
}

function checkGit() {
  try {
    const status = execSync('git status --short', { encoding: 'utf8', cwd: WORKSPACE, timeout: 5000 });
    const lines = status.trim().split('\n').filter(Boolean);
    return { ok: true, dirty: lines.length };
  } catch (e) {
    return { ok: false, reason: e.message.slice(0, 80) };
  }
}

function run() {
  const skills = fs.readdirSync(path.join(WORKSPACE, 'skills'))
    .filter(d => fs.statSync(path.join(WORKSPACE, 'skills', d)).isDirectory())
    .map(name => checkSkill(name, name));

  const evolver = checkEvolver();
  const git = checkGit();

  const failed = skills.filter(s => !s.ok);
  const summary = {
    timestamp: new Date().toISOString(),
    skills_total: skills.length,
    skills_ok: skills.length - failed.length,
    skills_failed: failed.map(f => ({ name: f.name, reason: f.reason })),
    evolver,
    git
  };
  return summary;
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (cmd === 'json') {
    console.log(JSON.stringify(run(), null, 2));
  } else {
    const summary = run();
    console.log('=== Workspace Smoke Test ===');
    console.log(`Skills: ${summary.skills_ok}/${summary.skills_total} OK`);
    if (summary.skills_failed.length > 0) {
      console.log('Failed skills:');
      for (const f of summary.skills_failed) {
        console.log(`  - ${f.name}: ${f.reason}`);
      }
    }
    console.log(`Evolver: ${summary.evolver.ok ? summary.evolver.version : 'NOT FOUND: ' + summary.evolver.reason}`);
    console.log(`Git: ${summary.git.dirty} dirty files`);
    console.log(`Timestamp: ${summary.timestamp}`);
    process.exit(summary.skills_failed.length > 0 ? 1 : 0);
  }
}

module.exports = { run, checkSkill, checkEvolver, checkGit };
