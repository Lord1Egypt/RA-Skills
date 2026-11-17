'use strict';

/**
 * Agent skill directory mappings.
 *
 * This module is intentionally data-only. It is used by both the installer
 * CLI and the local discovery/inventory code so a host mapping is defined
 * once. `resolveUserDir` applies the documented environment overrides.
 */

const os = require('os');
const path = require('path');

const AGENT_DIRS = {
  'aider-desk':      { label: 'AiderDesk',             dirs: ['.aider-desk/skills'] },
  amp:               { label: 'Amp',                   dirs: ['.config/agents/skills', '.agents/skills'] },
  antigravity:       { label: 'Antigravity',           dirs: ['.gemini/antigravity/skills', '.agents/skills'] },
  'antigravity-cli': { label: 'Antigravity CLI',       dirs: ['.gemini/antigravity-cli/skills', '.agents/skills'] },
  'autohand-code':   { label: 'Autohand Code CLI',     dirs: ['.autohand/skills'] },
  augment:           { label: 'Augment',               dirs: ['.augment/skills'] },
  bob:               { label: 'IBM Bob',               dirs: ['.bob/skills'] },
  claude:            { label: 'Claude Code',           dirs: ['.claude/skills'] },
  cline:             { label: 'Cline',                 dirs: ['.agents/skills', '.cline/skills'] },
  codearts:          { label: 'CodeArts Agent',        dirs: ['.codeartsdoer/skills'] },
  codebuddy:         { label: 'CodeBuddy Code',        dirs: ['.codebuddy/skills'] },
  codemaker:         { label: 'Codemaker',             dirs: ['.codemaker/skills'] },
  codestudio:        { label: 'Code Studio',           dirs: ['.codestudio/skills'] },
  codex:             { label: 'Codex',                 dirs: ['.codex/skills', '.agents/skills'] },
  'command-code':    { label: 'Command Code',          dirs: ['.commandcode/skills'] },
  comate:            { label: 'Comate 文心快码',        dirs: ['.comate/skills'] },
  continue:          { label: 'Continue',              dirs: ['.continue/skills'] },
  cortex:            { label: 'Cortex Code',           dirs: ['.snowflake/cortex/skills'] },
  crush:             { label: 'Crush',                 dirs: ['.config/crush/skills'] },
  cursor:            { label: 'Cursor',                dirs: ['.cursor/skills', '.agents/skills'] },
  deepagents:        { label: 'Deep Agents',           dirs: ['.deepagents/agent/skills', '.agents/skills'] },
  devin:             { label: 'Devin for Terminal',    dirs: ['.config/devin/skills'] },
  droid:             { label: 'Droid',                 dirs: ['.factory/skills', '.agents/skills'] },
  firebender:        { label: 'Firebender',            dirs: ['.firebender/skills', '.agents/skills'] },
  forgecode:         { label: 'ForgeCode',             dirs: ['.forge/skills'] },
  fx:                { label: 'fx',                    dirs: ['.fx/skills'] },
  gemini:            { label: 'Gemini CLI',            dirs: ['.gemini/skills', '.agents/skills'] },
  copilot:           { label: 'GitHub Copilot',        dirs: ['.copilot/skills', '.agents/skills'] },
  goose:             { label: 'Goose',                 dirs: ['.config/goose/skills', '.agents/skills'] },
  grok:              { label: 'Grok Build',            dirs: ['.grok/skills'] },
  hermes:            { label: 'Hermes Agent',          dirs: ['.hermes/skills'] },
  'inference-sh':    { label: 'inference.sh',          dirs: ['.inferencesh/skills'] },
  jazz:              { label: 'Jazz',                  dirs: ['.jazz/skills'] },
  junie:             { label: 'Junie',                 dirs: ['.junie/skills'] },
  iflow:             { label: 'iFlow CLI',             dirs: ['.iflow/skills'] },
  kilo:              { label: 'Kilo Code',             dirs: ['.kilo/skills', '.agents/skills'] },
  kimchi:            { label: 'Kimchi',                dirs: ['.config/kimchi/harness/skills'] },
  kimi:              { label: 'Kimi Code CLI',         dirs: ['.kimi/skills', '.agents/skills'] },
  kiro:              { label: 'Kiro',                  dirs: ['.kiro/skills'] },
  kode:              { label: 'Kode',                  dirs: ['.kode/skills'] },
  lingma:            { label: 'Lingma',                dirs: ['.lingma/skills'] },
  mcpjam:            { label: 'MCPJam',                dirs: ['.mcpjam/skills'] },
  mimocode:          { label: 'MiMo Code',             dirs: ['.config/mimocode/skills'] },
  minimax:           { label: 'MiniMax Code',          dirs: ['.minimax/skills'] },
  'mistral-vibe':    { label: 'Mistral Vibe',          dirs: ['.vibe/skills'] },
  moxby:             { label: 'Moxby',                 dirs: ['.moxby/skills'] },
  mux:               { label: 'Mux',                   dirs: ['.mux/skills'] },
  opencode:          { label: 'OpenCode',              dirs: ['.config/opencode/skills', '.agents/skills'] },
  openhands:         { label: 'OpenHands',             dirs: ['.openhands/skills'] },
  ona:               { label: 'Ona',                   dirs: ['.ona/skills'] },
    openclaw:          { label: 'OpenClaw',              dirs: ['.openclaw/skills'] },
  pi:                { label: 'Pi',                    dirs: ['.agents/skills'] },
  posit:             { label: 'Posit Assistant',       dirs: ['.posit/assistant/skills'] },
  qoder:             { label: 'Qoder',                 dirs: ['.qoder/skills'] },
  'qoder-cn':        { label: 'Qoder CN',              dirs: ['.qoder-cn/skills'] },
  qwen:              { label: 'Qwen Code',             dirs: ['.qwen/skills'] },
  reasonix:          { label: 'Reasonix',              dirs: ['.reasonix/skills'] },
  replit:            { label: 'Replit',                dirs: ['.config/agents/skills'] },
  rovodev:           { label: 'Rovo Dev',              dirs: ['.rovodev/skills'] },
  roo:               { label: 'Roo Code',              dirs: ['.roo/skills'] },
  'sarvam-code':     { label: 'Sarvam Code',           dirs: ['.sarvam/skills', '.agents/skills'] },
  tabnine:           { label: 'Tabnine CLI',           dirs: ['.tabnine/agent/skills'] },
  terramind:         { label: 'Terramind',             dirs: ['.terramind/skills'] },
  tinycloud:         { label: 'Tinycloud',             dirs: ['.tinycloud/skills'] },
  trae:              { label: 'Trae Code CLI',         dirs: ['.traecli/skills', '.trae/skills'] },
  'trae-cn':         { label: 'Trae IDE（国内）',       dirs: ['.trae-cn/skills', '.trae/skills'] },
  warp:              { label: 'Warp',                  dirs: ['.agents/skills', '.warp/skills'] },
  windsurf:          { label: 'Windsurf',              dirs: ['.codeium/windsurf/skills', '.windsurf/skills'] },
  workbuddy:         { label: 'WorkBuddy',             dirs: ['.workbuddy/skills'] },
  zcode:             { label: 'ZCode',                 dirs: ['.zcode/skills'] },
  zencoder:          { label: 'Zencoder',              dirs: ['.zencoder/skills'] },
  neovate:           { label: 'Neovate',               dirs: ['.neovate/skills'] },
  pochi:             { label: 'Pochi',                 dirs: ['.pochi/skills'] },
  adal:              { label: 'AdaL',                  dirs: ['.adal/skills'] },
  dsh:               { label: 'DSH / DeepSeek Harness', dirs: ['.dsh/skills'] },
  // YottaCode 自带三层技能管理（skill-inventory / skill / user-skills），
  // 不纳入元阁接管：neverLink 表示发现 / 显示 / 链接全部跳过（0.29.1 U2）。
  yottacode:         { label: 'YottaCode',             dirs: ['.yottacode/skills'], verified: false, neverLink: true },
  box:               { label: 'Box Agent',             dirs: ['.box-agent/skills'], verified: false },
  lmstudio:          { label: 'LM Studio',             dirs: ['.lmstudio/skills'] },
  ccswitch:          { label: 'CC Switch',             dirs: ['.cc-switch/skills'] },
  agents:            { label: '通用 AGENTS.md',         dirs: ['.agents/skills'] },
  universal:         { label: 'Universal .agents',      dirs: ['.config/agents/skills', '.agents/skills'] },
};

/**
 * Rel paths that follow XDG_CONFIG_HOME when it is set.
 *
 * Verified against the upstream Vercel Labs `skills` CLI v1.7.0 table
 * (2026-10-03): only amp / universal / replit (`configHome/agents/skills`),
 * devin (`configHome/devin/skills`) and opencode (`configHome/opencode/skills`)
 * resolve through the config home. Everything else uses the literal
 * `~/.config/...` path even when XDG_CONFIG_HOME is set (crush / kimchi per the
 * upstream table; goose follows the machine-verified `~/.config/goose`).
 */
const XDG_CONFIG_RELS = new Set([
  '.config/agents/skills',
  '.config/devin/skills',
  '.config/opencode/skills',
]);

function envPath(env, key) {
  const value = env && env[key];
  return value ? String(value) : null;
}

function homeDir(options) {
  return (options && options.homeDir) || os.homedir();
}

function envObject(options) {
  return (options && options.env) || process.env;
}

/**
 * Resolve one relative mapping. Environment overrides are intentionally
 * explicit rather than inferred: if an agent supports a custom home, the
 * caller must set that agent's documented variable.
 */
function resolveUserDir(rel, options) {
  const home = homeDir(options);
  const env = envObject(options);

  if (rel === '.codex/skills') {
    return path.join(envPath(env, 'CODEX_HOME') || path.join(home, '.codex'), 'skills');
  }
  if (rel.startsWith('.config/')) {
    const xdg = envPath(env, 'XDG_CONFIG_HOME');
    if (xdg && XDG_CONFIG_RELS.has(rel)) {
      return path.join(xdg, ...rel.slice('.config/'.length).split('/'));
    }
    return path.join(home, rel);
  }
  if (rel === '.openclaw/skills') {
    return path.join(envPath(env, 'OPENCLAW_STATE_DIR') || path.join(home, '.openclaw'), 'skills');
  }
  if (rel === '.claude/skills') {
    return path.join(envPath(env, 'CLAUDE_CONFIG_DIR') || path.join(home, '.claude'), 'skills');
  }
  if (rel === '.hermes/skills') {
    return path.join(envPath(env, 'HERMES_HOME') || path.join(home, '.hermes'), 'skills');
  }
  if (rel === '.vibe/skills') {
    return path.join(envPath(env, 'VIBE_HOME') || path.join(home, '.vibe'), 'skills');
  }
  if (rel === '.grok/skills') {
    return path.join(envPath(env, 'GROK_HOME') || path.join(home, '.grok'), 'skills');
  }
  if (rel === '.autohand/skills') {
    return path.join(envPath(env, 'AUTOHAND_HOME') || path.join(home, '.autohand'), 'skills');
  }
  if (rel === '.sarvam/skills') {
    return path.join(envPath(env, 'SARVAM_HOME') || path.join(home, '.sarvam'), 'skills');
  }
  return path.join(home, rel);
}

const YOTTACODE_PATH_RE = /(^|[\\/])\.yottacode([\\/]|$)/i;

/** YottaCode 路径判定（不接管红线；发现 / 链接 / 注册 / 标记统一 fail-closed）。 */
function isYottaCodeDir(dir) {
  if (!dir) return false;
  return YOTTACODE_PATH_RE.test(path.resolve(dir));
}

/** All known agent skill directories, including missing ones. */
function knownRoots(options) {
  const roots = [];
  const seen = new Set();
  const add = (dir, agentId, label, verified) => {
    if (!dir) return;
    const resolved = path.resolve(dir);
    if (seen.has(resolved)) return;
    seen.add(resolved);
    roots.push({ dir: resolved, agentId, label, known: true, verified: verified !== false });
  };
  for (const [agentId, info] of Object.entries(AGENT_DIRS)) {
    if (info.neverLink) continue;
    for (const rel of info.dirs) {
      const dir = resolveUserDir(rel, options);
      if (isYottaCodeDir(dir)) continue;
      add(dir, agentId, info.label, info.verified !== false);
    }
  }
  return roots;
}

/** Additional roots that are commonly used by desktop / portable agents. */
function envRoots(options) {
  const env = envObject(options);
  const roots = [];
  const add = (dir, agentId, label, extra) => {
    if (!dir) return;
    roots.push({
      dir: path.resolve(dir),
      agentId: agentId || null,
      label: label || '环境变量指定目录',
      known: false,
      env: true,
      verified: true,
      ...(extra || {}),
    });
  };

  add(envPath(env, 'CODEX_HOME') && path.join(env.CODEX_HOME, 'skills'), 'codex', 'Codex（CODEX_HOME）');
  add(envPath(env, 'XDG_CONFIG_HOME') && path.join(env.XDG_CONFIG_HOME, 'opencode', 'skills'), 'opencode', 'OpenCode（XDG_CONFIG_HOME）');
  add(envPath(env, 'XDG_STATE_HOME') && path.join(env.XDG_STATE_HOME, 'skills'), null,
    'XDG_STATE_HOME/skills（锁桥接，不链接）', { bridgeOnly: true });
  add(envPath(env, 'XDG_DATA_HOME') && path.join(env.XDG_DATA_HOME, 'skills'), null,
    'XDG_DATA_HOME/skills（数据桥接，不链接）', { bridgeOnly: true });
  add(envPath(env, 'DSH_HOME') && path.join(env.DSH_HOME, 'skills'), 'dsh', 'DSH（DSH_HOME）');
  add(envPath(env, 'DSH_AGENTS_HOME') && path.join(env.DSH_AGENTS_HOME, 'skills'), 'dsh', 'DSH Agents（DSH_AGENTS_HOME）');
  add(envPath(env, 'OPENCLAW_STATE_DIR') && path.join(env.OPENCLAW_STATE_DIR, 'skills'), 'openclaw', 'OpenClaw（OPENCLAW_STATE_DIR）');
  add(envPath(env, 'CLAUDE_CONFIG_DIR') && path.join(env.CLAUDE_CONFIG_DIR, 'skills'), 'claude', 'Claude Code（CLAUDE_CONFIG_DIR）');
  // YOTTACODE_HOME 不纳入元阁接管（YottaCode 自带三层技能管理，0.29.1 U2）。

  const extra = String(env.YOTTA_SKILLS_DISCOVERY_ROOTS || '')
    .split(path.delimiter)
    .map((item) => item.trim())
    .filter(Boolean);
  for (const dir of extra) add(dir, null, 'YOTTA_SKILLS_DISCOVERY_ROOTS', { verified: false });

  return roots;
}

/**
 * Lock / data bridge directories: the official `skills` CLI keeps its lock in
 * `$XDG_STATE_HOME/skills`, and `$XDG_DATA_HOME/skills` is a data bridge.
 * Neither is a host skill-loading directory, so both are never link targets.
 */
function bridgeOnlyDirs(options) {
  const env = envObject(options);
  const dirs = [];
  if (envPath(env, 'XDG_STATE_HOME')) dirs.push(path.join(env.XDG_STATE_HOME, 'skills'));
  if (envPath(env, 'XDG_DATA_HOME')) dirs.push(path.join(env.XDG_DATA_HOME, 'skills'));
  return dirs.map((dir) => path.resolve(dir));
}

function isBridgeOnlyDir(dir, options) {
  if (!dir) return false;
  const target = path.resolve(dir);
  for (const bridge of bridgeOnlyDirs(options)) {
    const relative = path.relative(bridge, target);
    if (relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative))) return true;
  }
  return false;
}

module.exports = {
  AGENT_DIRS,
  XDG_CONFIG_RELS,
  resolveUserDir,
  knownRoots,
  envRoots,
  bridgeOnlyDirs,
  isBridgeOnlyDir,
  isYottaCodeDir,
};
