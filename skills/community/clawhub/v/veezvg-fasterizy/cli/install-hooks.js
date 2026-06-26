const fs = require('fs');
const path = require('path');

const { claudeConfigDir, codexConfigDir } = require('./common');
const { readJson, writeJson, backupIfExists } = require('./fs-helpers');
const { hasFasterizyHook, stripFasterizyHookEntries } = require('./hooks-utils');

const HOOK_FILES = ['package.json', 'flag.js', 'skill-content.js', 'activate.js', 'tracker.js'];

function buildHookCommand(hooksDir, script) {
  return `FASTERIZY=1 node "${path.join(hooksDir, script)}"`;
}

function addFasterizyHooks(data, hooksDir, { includeMatcher } = {}) {
  if (!data.hooks) data.hooks = {};

  const sessionMsg = includeMatcher ? 'Loading fasterizy' : 'Loading fasterizy...';
  const promptMsg = includeMatcher ? 'Tracking fasterizy' : 'Tracking fasterizy...';

  const act = buildHookCommand(hooksDir, 'activate.js');
  const trk = buildHookCommand(hooksDir, 'tracker.js');

  if (!hasFasterizyHook(data, 'SessionStart')) {
    if (!data.hooks.SessionStart) data.hooks.SessionStart = [];
    const sessionEntry = {
      hooks: [
        {
          type: 'command',
          command: act,
          timeout: 5,
          statusMessage: sessionMsg,
        },
      ],
    };
    if (includeMatcher) sessionEntry.matcher = 'startup|resume';
    data.hooks.SessionStart.push(sessionEntry);
  }
  if (!hasFasterizyHook(data, 'UserPromptSubmit')) {
    if (!data.hooks.UserPromptSubmit) data.hooks.UserPromptSubmit = [];
    data.hooks.UserPromptSubmit.push({
      hooks: [
        {
          type: 'command',
          command: trk,
          timeout: 5,
          statusMessage: promptMsg,
        },
      ],
    });
  }
}

function registerMarketplace(settings, repoSlug) {
  if (!repoSlug) return;
  if (!settings.extraKnownMarketplaces) settings.extraKnownMarketplaces = {};
  if (!settings.extraKnownMarketplaces.fasterizy) {
    settings.extraKnownMarketplaces.fasterizy = {
      source: { source: 'github', repo: repoSlug },
    };
  }
}

function patchClaudeSettings(settingsPath, hooksDir, repoSlug) {
  const settings = readJson(settingsPath);
  if (settings === null) {
    throw new Error(`settings.json: not found at ${settingsPath}`);
  }
  addFasterizyHooks(settings, hooksDir);
  // Register fasterizy in extraKnownMarketplaces so /plugin can install it.
  // We do not auto-enable the plugin (would double-fire with hooks). Plugin path:
  // `/plugin install fasterizy` then `npx fasterizy uninstall-hooks`.
  registerMarketplace(settings, repoSlug);
  writeJson(settingsPath, settings);
}

function patchCodexHooksJson(hooksJsonPath, hooksDir) {
  const data = readJson(hooksJsonPath);
  if (data === null) {
    throw new Error(`hooks.json: not found at ${hooksJsonPath}`);
  }
  addFasterizyHooks(data, hooksDir, { includeMatcher: true });
  writeJson(hooksJsonPath, data);
}

function copyHooks(packageHooksDir, targetHooksDir) {
  for (const f of HOOK_FILES) {
    const src = path.join(packageHooksDir, f);
    const dst = path.join(targetHooksDir, f);
    fs.copyFileSync(src, dst);
  }
}

function installHookAgent({ configDir, targetFile, defaultContent, packageHooksDir, patcher }) {
  const hooksDir = path.join(configDir, 'hooks');
  fs.mkdirSync(hooksDir, { recursive: true });
  if (!fs.existsSync(packageHooksDir)) {
    throw new Error(`hooks not found in package: ${packageHooksDir}`);
  }
  copyHooks(packageHooksDir, hooksDir);

  const target = path.join(configDir, targetFile);
  if (fs.existsSync(target)) {
    backupIfExists(target);
  } else {
    fs.writeFileSync(target, defaultContent);
  }
  patcher(target, hooksDir);

  return {
    ok: true,
    backup: fs.existsSync(`${target}.bak`) ? `${target}.bak` : null,
  };
}

function installClaudeCode(packageRoot, opts) {
  const repoSlug = (opts && opts.repoSlug) || null;
  return installHookAgent({
    configDir: claudeConfigDir(),
    targetFile: 'settings.json',
    defaultContent: '{}\n',
    packageHooksDir: path.join(packageRoot, 'hooks'),
    patcher: (p, hooksDir) => patchClaudeSettings(p, hooksDir, repoSlug),
  });
}

function ensureCodexConfigToml(codexDir) {
  const cfg = path.join(codexDir, 'config.toml');
  if (!fs.existsSync(cfg)) {
    fs.writeFileSync(cfg, '[features]\ncodex_hooks = true\n');
    return;
  }
  const raw = fs.readFileSync(cfg, 'utf8');
  if (!raw.includes('codex_hooks')) {
    fs.appendFileSync(cfg, '\n[features]\ncodex_hooks = true\n');
  }
}

function installCodex(packageRoot) {
  const dir = codexConfigDir();
  fs.mkdirSync(dir, { recursive: true });
  ensureCodexConfigToml(dir);
  return installHookAgent({
    configDir: dir,
    targetFile: 'hooks.json',
    defaultContent: '{}\n',
    packageHooksDir: path.join(packageRoot, 'hooks'),
    patcher: patchCodexHooksJson,
  });
}

function unpatchFasterizyHooks(settingsPath) {
  if (!fs.existsSync(settingsPath)) return { changed: false };
  const settings = readJson(settingsPath);
  if (settings === null) {
    throw new Error(`settings.json: not found at ${settingsPath}`);
  }
  if (!settings.hooks) return { changed: false };

  const changed = stripFasterizyHookEntries(settings);
  if (changed) {
    backupIfExists(settingsPath);
    writeJson(settingsPath, settings);
  }
  return { changed };
}

function uninstallClaudeCodeHooks() {
  const claudeDir = claudeConfigDir();
  const hooksDir = path.join(claudeDir, 'hooks');
  const settings = path.join(claudeDir, 'settings.json');

  const result = { removedFiles: [], settingsChanged: false, backup: null };

  for (const f of HOOK_FILES) {
    const target = path.join(hooksDir, f);
    if (fs.existsSync(target)) {
      try {
        fs.unlinkSync(target);
        result.removedFiles.push(target);
      } catch (e) {}
    }
  }

  const r = unpatchFasterizyHooks(settings);
  result.settingsChanged = r.changed;
  if (r.changed) result.backup = `${settings}.bak`;

  return result;
}

module.exports = {
  installClaudeCode,
  installCodex,
  uninstallClaudeCodeHooks,
  HOOK_FILES,
};
