const fs = require('fs');
const path = require('path');
const os = require('os');

const REPO_SLUG = 'felipeinf/fasterizy';

function packageRoot() {
  return path.join(__dirname, '..');
}

function claudeConfigDir() {
  return process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
}

function codexConfigDir() {
  return process.env.CODEX_CONFIG_DIR || path.join(os.homedir(), '.codex');
}

function findPluginCacheDirs(baseName, markerRel) {
  const base = path.join(os.homedir(), baseName, 'plugins', 'cache');
  const found = [];
  if (!fs.existsSync(base)) return found;

  const tryPush = (dir) => {
    const marker = path.join(dir, markerRel);
    try {
      if (fs.existsSync(marker) && fs.statSync(marker).isFile()) found.push(dir);
    } catch (e) {}
  };

  try {
    const entries = fs.readdirSync(base, { withFileTypes: true });
    for (const e of entries) {
      if (!e.isDirectory()) continue;
      const sub = path.join(base, e.name);
      let subEntries;
      try {
        subEntries = fs.readdirSync(sub, { withFileTypes: true });
      } catch (err) {
        continue;
      }
      for (const e2 of subEntries) {
        if (!e2.isDirectory()) continue;
        if (e2.name !== 'fasterizy') continue;
        tryPush(path.join(sub, e2.name));
      }
    }
  } catch (e) {}
  return [...new Set(found)];
}

function claudePluginCacheGlob() {
  return findPluginCacheDirs('.claude', path.join('.claude-plugin', 'plugin.json'));
}

function codexPluginCacheGlob() {
  return findPluginCacheDirs('.codex', path.join('.codex-plugin', 'plugin.json'));
}

const NPX_AGENT_PATHS = [
  {
    id: 'opencode',
    npxFlag: 'opencode',
    relPath: path.join('.config', 'opencode', 'skills', 'fasterizy', 'SKILL.md'),
  },
  {
    id: 'openclaw',
    npxFlag: 'openclaw',
    relPath: path.join('.openclaw', 'skills', 'fasterizy', 'SKILL.md'),
  },
  { id: 'cursor', npxFlag: 'cursor', relPath: path.join('.cursor', 'rules', 'fasterizy.mdc') },
  {
    id: 'cursor-skill',
    npxFlag: 'cursor',
    relPath: path.join('.cursor', 'skills', 'fasterizy', 'SKILL.md'),
  },
  {
    id: 'antigravity',
    npxFlag: 'antigravity',
    relPath: path.join('.gemini', 'antigravity', 'skills', 'fasterizy', 'SKILL.md'),
  },
  { id: 'windsurf', npxFlag: 'windsurf', relPath: path.join('.windsurf', 'rules', 'fasterizy.md') },
  { id: 'cline', npxFlag: 'cline', relPath: path.join('.clinerules', 'fasterizy.md') },
  {
    id: 'copilot',
    npxFlag: 'github-copilot',
    relPath: path.join('.github', 'copilot-instructions.md'),
  },
];

function findNpxSkillsInstalls(searchRoots) {
  const out = [];
  for (const root of searchRoots) {
    if (!root || !fs.existsSync(root)) continue;
    for (const spec of NPX_AGENT_PATHS) {
      const full = path.join(root, spec.relPath);
      try {
        if (fs.existsSync(full) && fs.statSync(full).isFile()) {
          const text = fs.readFileSync(full, 'utf8');
          if (text.toLowerCase().includes('fasterizy')) {
            out.push({ ...spec, path: full, root });
          }
        }
      } catch (e) {}
    }
  }
  return out;
}

function defaultSearchRoots() {
  const roots = [process.cwd(), os.homedir()];
  const extra = process.env.FASTERIZY_UPDATE_ROOTS;
  if (extra && String(extra).trim()) {
    for (const part of String(extra).split(/[,;]/)) {
      const p = part.trim();
      if (p) roots.push(path.resolve(p));
    }
  }
  return [...new Set(roots)];
}

module.exports = {
  REPO_SLUG,
  packageRoot,
  claudeConfigDir,
  codexConfigDir,
  claudePluginCacheGlob,
  codexPluginCacheGlob,
  NPX_AGENT_PATHS,
  findNpxSkillsInstalls,
  defaultSearchRoots,
};
