// Replicates `/plugin install fasterizy@fasterizy` in Claude Code: clone marketplace,
// copy plugin to cache by short sha, update known_marketplaces.json +
// installed_plugins.json, enable enabledPlugins. Lets the CLI finish without slash commands.
//
// Caveat: installed_plugins.json / cache layout / sha length are not a documented API.
// If Claude Code changes this, update here. Fallback: hook install via `npx fasterizy install`.

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const { REPO_SLUG, claudeConfigDir, packageRoot } = require('./common');
const { readJson, writeJson, backupIfExists } = require('./fs-helpers');
const { stripFasterizyHookEntries } = require('./hooks-utils');

const PLUGIN_NAME = 'fasterizy';
const MARKETPLACE_NAME = 'fasterizy';
const PLUGIN_KEY = `${PLUGIN_NAME}@${MARKETPLACE_NAME}`;
const SHORT_SHA_LEN = 12;
const FASTERIZY_HOOK_FILES = ['activate.js', 'tracker.js', 'flag.js', 'skill-content.js'];

function getGitSha(repoDir) {
  try {
    return execSync('git rev-parse HEAD', {
      cwd: repoDir,
      stdio: ['ignore', 'pipe', 'ignore'],
    })
      .toString()
      .trim();
  } catch (e) {
    return null;
  }
}

function ensureMarketplaceClone(claudeDir) {
  const mp = path.join(claudeDir, 'plugins', 'marketplaces', MARKETPLACE_NAME);
  if (fs.existsSync(path.join(mp, '.git'))) return mp;
  fs.mkdirSync(path.dirname(mp), { recursive: true });
  try {
    execSync(`git clone --depth 1 https://github.com/${REPO_SLUG}.git "${mp}"`, {
      stdio: 'inherit',
    });
  } catch (e) {
    throw new Error(
      `git clone of ${REPO_SLUG} failed (${e.message || e}). Need network and git available.`
    );
  }
  return mp;
}

function resolveMarketplaceSource(claudeDir) {
  const root = packageRoot();
  const hasManifest = fs.existsSync(path.join(root, '.claude-plugin', 'plugin.json'));
  const hasGit = fs.existsSync(path.join(root, '.git'));
  if (hasManifest && hasGit) {
    return { path: root, local: true };
  }
  return { path: ensureMarketplaceClone(claudeDir), local: false };
}

function patchKnownMarketplaces(claudeDir, marketplacePath) {
  const p = path.join(claudeDir, 'plugins', 'known_marketplaces.json');
  const data = readJson(p) || {};
  data[MARKETPLACE_NAME] = {
    source: { source: 'github', repo: REPO_SLUG },
    installLocation: marketplacePath,
    lastUpdated: new Date().toISOString(),
  };
  backupIfExists(p);
  writeJson(p, data);
}

function registerClaudeMarketplaceOnDisk(claudeDir) {
  const src = resolveMarketplaceSource(claudeDir);
  patchKnownMarketplaces(claudeDir, src.path);
  return { marketplacePath: src.path, local: src.local };
}

function patchInstalledPlugins(claudeDir, installPath, fullSha, shortSha) {
  const p = path.join(claudeDir, 'plugins', 'installed_plugins.json');
  const data = readJson(p) || { version: 2, plugins: {} };
  if (!data.plugins) data.plugins = {};
  const ts = new Date().toISOString();
  data.plugins[PLUGIN_KEY] = [
    {
      scope: 'user',
      installPath: installPath,
      version: shortSha,
      installedAt: ts,
      lastUpdated: ts,
      gitCommitSha: fullSha,
    },
  ];
  backupIfExists(p);
  writeJson(p, data);
}

function patchSettingsForPlugin(claudeDir) {
  const p = path.join(claudeDir, 'settings.json');
  const data = readJson(p) || {};
  if (!data.extraKnownMarketplaces) data.extraKnownMarketplaces = {};
  if (!data.extraKnownMarketplaces[MARKETPLACE_NAME]) {
    data.extraKnownMarketplaces[MARKETPLACE_NAME] = {
      source: { source: 'github', repo: REPO_SLUG },
    };
  }
  if (!data.enabledPlugins) data.enabledPlugins = {};
  data.enabledPlugins[PLUGIN_KEY] = true;

  const strippedHooks = stripFasterizyHookEntries(data);
  backupIfExists(p);
  writeJson(p, data);
  return { strippedHooks };
}

function removeOldHookFiles(claudeDir) {
  const hooksDir = path.join(claudeDir, 'hooks');
  const removed = [];
  for (const f of FASTERIZY_HOOK_FILES) {
    const p = path.join(hooksDir, f);
    if (!fs.existsSync(p)) continue;
    try {
      const content = fs.readFileSync(p, 'utf8');
      if (content.toLowerCase().includes('fasterizy') || /skill-content|flag/i.test(f)) {
        fs.unlinkSync(p);
        removed.push(p);
      }
    } catch (e) {}
  }
  return removed;
}

function installAsClaudePlugin() {
  const claudeDir = claudeConfigDir();

  const { marketplacePath, local } = registerClaudeMarketplaceOnDisk(claudeDir);
  const fullSha = getGitSha(marketplacePath);
  if (!fullSha) {
    throw new Error(`cannot read git sha at ${marketplacePath} (corrupt repo?)`);
  }
  const shortSha = fullSha.slice(0, SHORT_SHA_LEN);
  const versionTag = local ? `${shortSha}-local` : shortSha;
  const installPath = path.join(
    claudeDir,
    'plugins',
    'cache',
    MARKETPLACE_NAME,
    PLUGIN_NAME,
    versionTag
  );

  let copied = false;
  if (local && fs.existsSync(installPath)) {
    fs.rmSync(installPath, { recursive: true, force: true });
  }
  if (!fs.existsSync(installPath)) {
    fs.cpSync(marketplacePath, installPath, {
      recursive: true,
      filter: (src) => {
        const parts = src.split(path.sep);
        return !parts.includes('.git') && !parts.includes('node_modules');
      },
    });
    copied = true;
  }

  patchInstalledPlugins(claudeDir, installPath, fullSha, versionTag);
  const settingsResult = patchSettingsForPlugin(claudeDir);
  const removedHookFiles = removeOldHookFiles(claudeDir);

  return {
    marketplacePath: marketplacePath,
    installPath: installPath,
    shortSha: versionTag,
    fullSha: fullSha,
    copied: copied,
    local: local,
    strippedHooksFromSettings: settingsResult.strippedHooks,
    removedHookFiles: removedHookFiles,
  };
}

module.exports = { installAsClaudePlugin };
