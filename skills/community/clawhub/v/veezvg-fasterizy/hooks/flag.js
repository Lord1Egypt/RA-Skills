#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

function agentConfigDir() {
  if (process.env.CLAUDE_CONFIG_DIR) return process.env.CLAUDE_CONFIG_DIR;
  if (process.env.CODEX_CONFIG_DIR) return process.env.CODEX_CONFIG_DIR;
  return path.join(os.homedir(), '.claude');
}

function flagPath() {
  return path.join(agentConfigDir(), '.fasterizy-active');
}

function defaultEnabled() {
  const v = process.env.FASTERIZY_ENABLED_BY_DEFAULT;
  if (v === undefined || v === '') return true;
  const lower = String(v).toLowerCase();
  return lower !== '0' && lower !== 'false' && lower !== 'off';
}

function enable() {
  const p = flagPath();
  const dir = path.dirname(p);
  try {
    fs.mkdirSync(dir, { recursive: true });
    if (fs.lstatSync(dir).isSymbolicLink()) return;
  } catch (e) {
    return;
  }
  try {
    const st = fs.lstatSync(p);
    if (st.isSymbolicLink()) return;
    if (st.isFile()) return;
    return;
  } catch (e) {
    if (e.code !== 'ENOENT') return;
  }
  try {
    const O_NOFOLLOW = typeof fs.constants.O_NOFOLLOW === 'number' ? fs.constants.O_NOFOLLOW : 0;
    const fd = fs.openSync(
      p,
      fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | O_NOFOLLOW,
      0o600
    );
    fs.closeSync(fd);
  } catch (e) {}
}

function disable() {
  const p = flagPath();
  try {
    let st;
    try {
      st = fs.lstatSync(p);
    } catch (e) {
      if (e.code === 'ENOENT') return;
      return;
    }
    if (st.isSymbolicLink()) return;
    fs.unlinkSync(p);
  } catch (e) {}
}

function isEnabled() {
  try {
    const p = flagPath();
    const st = fs.lstatSync(p);
    if (st.isSymbolicLink()) return false;
    return st.isFile();
  } catch (e) {
    return false;
  }
}

module.exports = {
  agentConfigDir,
  flagPath,
  defaultEnabled,
  enable,
  disable,
  isEnabled,
};
