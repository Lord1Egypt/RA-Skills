'use strict';

// Host roots are an explicit inventory boundary for collision analysis; this
// module does not crawl arbitrary home-directory content.
const fs = require('fs');
const os = require('os');
const path = require('path');

const AGENT_ALIASES = new Map([
  ['claude-code', 'claude'],
  ['github-copilot', 'copilot'],
  ['copilot-cli', 'copilot'],
  ['agent-skills', 'agents'],
]);

function findRepoRoot(cwd) {
  let current = path.resolve(cwd);
  while (true) {
    if (fs.existsSync(path.join(current, '.git'))) return current;
    const parent = path.dirname(current);
    if (parent === current) return path.resolve(cwd);
    current = parent;
  }
}

function ancestors(from, stop) {
  const result = [];
  let current = path.resolve(from);
  const boundary = path.resolve(stop);
  while (true) {
    result.push(current);
    if (current === boundary || path.dirname(current) === current) return result;
    current = path.dirname(current);
  }
}

function platformRoots(options = {}) {
  const cwd = path.resolve(options.cwd || process.cwd());
  const home = path.resolve(options.home || os.homedir());
  const repoRoot = path.resolve(options.repoRoot || findRepoRoot(cwd));
  const xdg = process.env.XDG_CONFIG_HOME || path.join(home, '.config');
  const projectLevels = ancestors(cwd, repoRoot);
  const roots = [];
  const add = (agent, scope, root, depth = 4, direct = false) => roots.push({ agent, scope, root, depth, direct });

  for (const level of projectLevels) {
    add('agents', 'project', path.join(level, '.agents', 'skills'), 3);
  }
  add('agents', 'user', path.join(home, '.agents', 'skills'), 3);

  add('codex', 'project', path.join(repoRoot, '.codex', 'skills'), 3);
  add('codex', 'user', path.join(home, '.codex', 'skills'), 4);
  add('codex', 'system', path.join(home, '.codex', 'skills', '.system'), 3, true);
  add('codex', 'plugin', path.join(home, '.codex', 'plugins', 'cache'), 8);
  add('codex', 'plugin', path.join(home, '.agents', 'plugins', 'cache'), 8);
  add('codex', 'admin', '/etc/codex/skills', 3);

  add('claude', 'project', path.join(repoRoot, '.claude', 'skills'), 3);
  add('claude', 'user', path.join(home, '.claude', 'skills'), 3);
  add('claude', 'plugin', path.join(home, '.claude', 'plugins', 'cache'), 8);

  add('gemini', 'project', path.join(repoRoot, '.gemini', 'skills'), 3);
  add('gemini', 'user', path.join(home, '.gemini', 'skills'), 3);
  add('gemini', 'extension', path.join(home, '.gemini', 'extensions'), 7);

  add('copilot', 'project', path.join(repoRoot, '.github', 'skills'), 3);
  add('copilot', 'user', path.join(home, '.copilot', 'skills'), 3);
  add('copilot', 'plugin', path.join(home, '.vscode', 'agent-plugins'), 8);

  for (const agent of ['cursor', 'windsurf', 'cline', 'qoder', 'kiro', 'grok']) {
    add(agent, 'project', path.join(repoRoot, `.${agent}`, 'skills'), 3);
    add(agent, 'user', path.join(home, `.${agent}`, 'skills'), 3);
  }

  add('opencode', 'project', path.join(repoRoot, '.opencode', 'skills'), 3);
  add('opencode', 'user', path.join(xdg, 'opencode', 'skills'), 3);
  add('swival', 'project', path.join(repoRoot, '.swival', 'skills'), 3);
  add('swival', 'user', path.join(xdg, 'swival', 'skills'), 3);
  add('openclaw', 'project', path.join(repoRoot, '.openclaw', 'skills'), 3);
  add('openclaw', 'user', path.join(home, '.openclaw', 'skills'), 3);

  if (!options.agent) return roots;
  const requested = new Set(String(options.agent).split(',')
    .map((value) => value.trim().toLowerCase())
    .filter(Boolean)
    .map((value) => AGENT_ALIASES.get(value) || value));
  const supported = new Set(roots.map((origin) => origin.agent));
  const unknown = [...requested].filter((agent) => !supported.has(agent));
  if (unknown.length) throw new Error(`Unknown agent: ${unknown.join(', ')}`);

  // Codex loads portable Agent Skills alongside its Codex-specific roots.
  if (requested.has('codex')) requested.add('agents');
  return roots.filter((origin) => requested.has(origin.agent));
}

module.exports = { AGENT_ALIASES, ancestors, findRepoRoot, platformRoots };
