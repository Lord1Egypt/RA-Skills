#!/usr/bin/env node
// wip-universal-installer/install.js
// Reference installer for agent-native software.
// Reads a repo, detects available interfaces, installs them all.
// Deploys to LDM OS (~/.ldm/extensions/) and OpenClaw (~/.openclaw/extensions/).
// Registers MCP servers at user scope via `claude mcp add --scope user`.
// Maintains a registry at ~/.ldm/extensions/registry.json.

import { execSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync, cpSync, mkdirSync, lstatSync, readlinkSync, unlinkSync, chmodSync, readdirSync } from 'node:fs';
import { join, basename, resolve } from 'node:path';
import { detectInterfaces, describeInterfaces, detectInterfacesJSON, detectToolbox } from './detect.mjs';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const LDM_EXTENSIONS = join(LDM_ROOT, 'extensions');
const OC_ROOT = join(HOME, '.openclaw');
const OC_EXTENSIONS = join(OC_ROOT, 'extensions');
const OC_MCP = join(OC_ROOT, '.mcp.json');
const REGISTRY_PATH = join(LDM_EXTENSIONS, 'registry.json');

// Flags
const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const JSON_OUTPUT = args.includes('--json');
const target = args.find(a => !a.startsWith('--'));

function log(msg) { if (!JSON_OUTPUT) console.log(`  ${msg}`); }
function ok(msg) { if (!JSON_OUTPUT) console.log(`  ✓ ${msg}`); }
function skip(msg) { if (!JSON_OUTPUT) console.log(`  - ${msg}`); }
function fail(msg) { if (!JSON_OUTPUT) console.error(`  ✗ ${msg}`); }

function ensureBinExecutable(binNames) {
  try {
    const npmPrefix = execSync('npm config get prefix', { encoding: 'utf8' }).trim();
    for (const bin of binNames) {
      const binPath = join(npmPrefix, 'bin', bin);
      try { chmodSync(binPath, 0o755); } catch {}
    }
  } catch {}
}

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

function writeJSON(path, data) {
  mkdirSync(join(path, '..'), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
}

// ── Registry ──

function loadRegistry() {
  return readJSON(REGISTRY_PATH) || { _format: 'v1', extensions: {} };
}

function saveRegistry(registry) {
  writeJSON(REGISTRY_PATH, registry);
}

function updateRegistry(name, info) {
  const registry = loadRegistry();
  registry.extensions[name] = {
    ...registry.extensions[name],
    ...info,
    updatedAt: new Date().toISOString(),
  };
  saveRegistry(registry);
}

// ── Migration detection ──

/**
 * Scan existing extension directories for installs that match this tool
 * but live under a different directory name. Matches on:
 *   1. Same package name in package.json
 *   2. Same plugin id in openclaw.plugin.json
 * Returns array of { dirName, matchType, path } for each match.
 */
function findExistingInstalls(toolName, pkg, ocPluginConfig) {
  const matches = [];
  const packageName = pkg?.name;
  const pluginId = ocPluginConfig?.id;

  // Scan both LDM and OC extension dirs
  for (const extDir of [LDM_EXTENSIONS, OC_EXTENSIONS]) {
    if (!existsSync(extDir)) continue;
    let entries;
    try {
      entries = readdirSync(extDir, { withFileTypes: true });
    } catch { continue; }

    for (const entry of entries) {
      if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
      const dirName = entry.name;
      // Skip if it's already the target name
      if (dirName === toolName) continue;
      // Skip registry.json
      if (dirName === 'registry.json') continue;

      const dirPath = join(extDir, dirName);

      // Check package.json name match
      if (packageName) {
        const dirPkg = readJSON(join(dirPath, 'package.json'));
        if (dirPkg?.name === packageName) {
          if (!matches.some(m => m.dirName === dirName)) {
            matches.push({ dirName, matchType: 'package', path: dirPath });
          }
          continue;
        }
      }

      // Check openclaw.plugin.json id match
      if (pluginId) {
        const dirPlugin = readJSON(join(dirPath, 'openclaw.plugin.json'));
        if (dirPlugin?.id === pluginId) {
          if (!matches.some(m => m.dirName === dirName)) {
            matches.push({ dirName, matchType: 'plugin-id', path: dirPath });
          }
          continue;
        }
      }
    }
  }

  return matches;
}

/**
 * Migrate an existing install from an old directory name to the new one.
 * Removes old extension dirs (LDM + OC), old MCP registrations, old skills.
 */
function migrateExistingInstall(oldName, newName) {
  // 1. Remove old extension directories (check lstat too for broken symlinks)
  for (const extDir of [LDM_EXTENSIONS, OC_EXTENSIONS]) {
    const oldPath = join(extDir, oldName);
    let pathExists = existsSync(oldPath);
    if (!pathExists) {
      try { lstatSync(oldPath); pathExists = true; } catch {}
    }
    if (pathExists) {
      try {
        execSync(`rm -rf "${oldPath}"`, { stdio: 'pipe' });
        ok(`Migrated: removed ${oldPath}`);
      } catch (e) {
        fail(`Migration: could not remove ${oldPath}. ${e.message}`);
      }
    }
  }

  // 2. Remove old MCP registrations (Claude Code)
  try {
    execSync(`claude mcp remove ${oldName} --scope user`, { stdio: 'pipe' });
    ok(`Migrated: removed MCP registration "${oldName}" from Claude Code`);
  } catch {}

  // Also clean ~/.claude/.mcp.json fallback
  const ccMcpPath = join(HOME, '.claude', '.mcp.json');
  const ccMcp = readJSON(ccMcpPath);
  if (ccMcp?.mcpServers?.[oldName]) {
    delete ccMcp.mcpServers[oldName];
    writeJSON(ccMcpPath, ccMcp);
  }

  // Also clean ~/.claude.json (user-level MCP)
  const ccUserPath = join(HOME, '.claude.json');
  const ccUser = readJSON(ccUserPath);
  if (ccUser?.mcpServers?.[oldName]) {
    delete ccUser.mcpServers[oldName];
    writeJSON(ccUserPath, ccUser);
    ok(`Migrated: removed MCP registration "${oldName}" from ~/.claude.json`);
  }

  // 3. Remove old OpenClaw MCP registration
  if (existsSync(OC_MCP)) {
    const ocMcp = readJSON(OC_MCP);
    if (ocMcp?.mcpServers?.[oldName]) {
      delete ocMcp.mcpServers[oldName];
      writeJSON(OC_MCP, ocMcp);
      ok(`Migrated: removed MCP registration "${oldName}" from OpenClaw`);
    }
  }

  // 4. Remove old skill directory
  const oldSkillDir = join(OC_ROOT, 'skills', oldName);
  if (existsSync(oldSkillDir)) {
    try {
      execSync(`rm -rf "${oldSkillDir}"`, { stdio: 'pipe' });
      ok(`Migrated: removed old skill at ${oldSkillDir}`);
    } catch {}
  }

  // 5. Remove old registry entry
  const registry = loadRegistry();
  if (registry.extensions[oldName]) {
    delete registry.extensions[oldName];
    saveRegistry(registry);
  }
}

// ── Install functions ──

function installCLI(repoPath, door) {
  const pkg = readJSON(join(repoPath, 'package.json'));
  const binNames = typeof door.bin === 'string' ? [basename(repoPath)] : Object.keys(door.bin || {});
  const newVersion = pkg?.version;

  // Check if already installed at this version
  if (newVersion && binNames.length > 0) {
    try {
      const installed = execSync(`npm list -g ${pkg.name} --json 2>/dev/null`, { encoding: 'utf8' });
      const data = JSON.parse(installed);
      const deps = data.dependencies || {};
      if (deps[pkg.name]?.version === newVersion) {
        // Still ensure bins are executable (git doesn't preserve +x)
        ensureBinExecutable(binNames);
        skip(`CLI: ${binNames.join(', ')} already at v${newVersion}`);
        return true;
      }
    } catch {}
  }

  if (DRY_RUN) {
    ok(`CLI: would install ${binNames.join(', ')} globally (dry run)`);
    return true;
  }

  // If the package has a build script and dist/ is missing, build first
  if (pkg?.scripts?.build && !existsSync(join(repoPath, 'dist'))) {
    try {
      log(`CLI: building ${binNames.join(', ')} (TypeScript)...`);
      execSync('npm run build', { cwd: repoPath, stdio: 'pipe' });
    } catch (e) {
      fail(`CLI: build failed. ${e.stderr?.toString()?.slice(0, 200) || e.message}`);
    }
  }

  try {
    execSync('npm install -g .', { cwd: repoPath, stdio: 'pipe' });
    // Safety net: ensure bin files are executable (git doesn't always preserve +x)
    ensureBinExecutable(binNames);
    ok(`CLI: ${binNames.join(', ')} installed globally`);
    return true;
  } catch (e) {
    const stderr = e.stderr?.toString() || '';
    // EEXIST: a binary with the same name exists from a different package.
    // Remove the stale symlink and retry.
    if (stderr.includes('EEXIST')) {
      for (const bin of binNames) {
        try {
          const binPath = execSync(`npm config get prefix`, { encoding: 'utf8' }).trim() + '/bin/' + bin;
          if (existsSync(binPath) && lstatSync(binPath).isSymbolicLink()) {
            const target = readlinkSync(binPath);
            // Only remove if it points to a different package
            if (!target.includes(pkg.name.replace(/^@[^/]+\//, ''))) {
              unlinkSync(binPath);
            }
          }
        } catch {}
      }
      try {
        execSync('npm install -g .', { cwd: repoPath, stdio: 'pipe' });
        ensureBinExecutable(binNames);
        ok(`CLI: ${binNames.join(', ')} installed globally (replaced stale symlink)`);
        return true;
      } catch {}
    }
    try {
      execSync('npm link', { cwd: repoPath, stdio: 'pipe' });
      ensureBinExecutable(binNames);
      ok(`CLI: linked globally via npm link`);
      return true;
    } catch {
      fail(`CLI: install failed. Run manually: cd "${repoPath}" && npm install -g .`);
      return false;
    }
  }
}

function deployExtension(repoPath, name) {
  const ldmDest = join(LDM_EXTENSIONS, name);
  const ocDest = join(OC_EXTENSIONS, name);

  // Check if already deployed at the same version
  const sourcePkg = readJSON(join(repoPath, 'package.json'));
  const installedPkg = readJSON(join(ldmDest, 'package.json'));
  const newVersion = sourcePkg?.version;
  const currentVersion = installedPkg?.version;

  if (newVersion && currentVersion && newVersion === currentVersion) {
    skip(`LDM: ${name} already at v${currentVersion}`);
    // Still check OpenClaw copy exists
    if (existsSync(ocDest)) {
      skip(`OpenClaw: ${name} already at v${currentVersion}`);
    } else if (!DRY_RUN) {
      // LDM has it but OpenClaw doesn't. Copy it over.
      mkdirSync(ocDest, { recursive: true });
      cpSync(ldmDest, ocDest, { recursive: true });
      ok(`OpenClaw: deployed to ${ocDest} (synced from LDM)`);
    }
    return true;
  }

  if (DRY_RUN) {
    if (currentVersion) {
      ok(`LDM: would upgrade ${name} v${currentVersion} -> v${newVersion} (dry run)`);
    } else {
      ok(`LDM: would deploy ${name} v${newVersion || 'unknown'} to ${ldmDest} (dry run)`);
    }
    ok(`OpenClaw: would deploy to ${ocDest} (dry run)`);
    return true;
  }

  try {
    // LDM path (remove existing to get clean copy)
    if (existsSync(ldmDest)) {
      execSync(`rm -rf "${ldmDest}"`, { stdio: 'pipe' });
    }
    mkdirSync(ldmDest, { recursive: true });
    cpSync(repoPath, ldmDest, {
      recursive: true,
      filter: (src) => !src.includes('.git') && !src.includes('node_modules') && !src.includes('ai/')
    });
    if (currentVersion) {
      ok(`LDM: upgraded ${name} v${currentVersion} -> v${newVersion}`);
    } else {
      ok(`LDM: deployed to ${ldmDest}`);
    }

    // Install deps in LDM
    if (existsSync(join(ldmDest, 'package.json'))) {
      try {
        execSync('npm install --omit=dev', { cwd: ldmDest, stdio: 'pipe' });
        ok(`LDM: dependencies installed`);
      } catch {
        skip(`LDM: no deps needed`);
      }
    }

    // OpenClaw path (copy from LDM to keep them identical)
    if (existsSync(ocDest)) {
      execSync(`rm -rf "${ocDest}"`, { stdio: 'pipe' });
    }
    mkdirSync(ocDest, { recursive: true });
    cpSync(ldmDest, ocDest, { recursive: true });
    ok(`OpenClaw: deployed to ${ocDest}`);

    return true;
  } catch (e) {
    fail(`Deploy failed: ${e.message}`);
    return false;
  }
}

function installOpenClaw(repoPath, door, toolName) {
  // Use toolName (from package.json name, stripped of scope) for the directory.
  // Never use door.config.name (display name) ... it can have spaces.
  const name = toolName || door.config?.id || basename(repoPath);
  return deployExtension(repoPath, name);
}

function registerMCP(repoPath, door, toolName) {
  // Use toolName for the MCP registration name and LDM path lookup.
  // Strip npm scope (@org/) from name for claude mcp add compatibility.
  const rawName = toolName || door.name || basename(repoPath);
  const name = rawName.replace(/^@[\w-]+\//, '');
  const serverPath = join(repoPath, door.file);
  // Use LDM-deployed path if it exists, otherwise repo path.
  // Try toolName first (correct), then basename(repoPath) as fallback.
  const ldmServerPath = join(LDM_EXTENSIONS, name, door.file);
  const ldmFallbackPath = join(LDM_EXTENSIONS, basename(repoPath), door.file);
  const mcpPath = existsSync(ldmServerPath) ? ldmServerPath
    : existsSync(ldmFallbackPath) ? ldmFallbackPath
    : serverPath;

  // Check if already registered with the same path
  const ccMcpPath = join(HOME, '.claude', '.mcp.json');
  const ccMcp = readJSON(ccMcpPath);
  const ccAlreadyRegistered = ccMcp?.mcpServers?.[name]?.args?.includes(mcpPath);

  let ocAlreadyRegistered = false;
  if (existsSync(OC_MCP)) {
    const ocMcp = readJSON(OC_MCP);
    ocAlreadyRegistered = ocMcp?.mcpServers?.[name]?.args?.includes(mcpPath);
  }

  if (ccAlreadyRegistered && (ocAlreadyRegistered || !existsSync(OC_MCP))) {
    skip(`MCP: ${name} already registered at ${mcpPath}`);
    return true;
  }

  if (DRY_RUN) {
    if (!ccAlreadyRegistered) ok(`MCP (CC): would register ${name} at user scope (dry run)`);
    if (!ocAlreadyRegistered && existsSync(OC_MCP)) ok(`MCP (OC): would add to ${OC_MCP} (dry run)`);
    return true;
  }

  // 1. Register with Claude Code CLI at user scope
  let ccRegistered = ccAlreadyRegistered;
  if (!ccAlreadyRegistered) {
    try {
      // Remove first if exists (update behavior)
      try {
        execSync(`claude mcp remove ${name} --scope user`, { stdio: 'pipe' });
      } catch {}
      const envFlag = existsSync(OC_ROOT) ? ` -e OPENCLAW_HOME="${OC_ROOT}"` : '';
      execSync(`claude mcp add --scope user ${name}${envFlag} -- node "${mcpPath}"`, { stdio: 'pipe' });
      ok(`MCP (CC): registered ${name} at user scope`);
      ccRegistered = true;
    } catch (e) {
      // Fallback: write to ~/.claude/.mcp.json
      try {
        const mcpConfig = readJSON(ccMcpPath) || { mcpServers: {} };
        mcpConfig.mcpServers[name] = {
          command: 'node',
          args: [mcpPath],
        };
        writeJSON(ccMcpPath, mcpConfig);
        ok(`MCP (CC): registered ${name} in ~/.claude/.mcp.json (fallback)`);
        ccRegistered = true;
      } catch (e2) {
        fail(`MCP (CC): registration failed. ${e.message}`);
      }
    }
  } else {
    skip(`MCP (CC): ${name} already registered`);
  }

  // 2. Register in OpenClaw's .mcp.json (only if the file already exists)
  if (existsSync(OC_MCP) && !ocAlreadyRegistered) {
    try {
      const ocMcp = readJSON(OC_MCP) || { mcpServers: {} };
      ocMcp.mcpServers[name] = {
        command: 'node',
        args: [mcpPath],
      };
      if (existsSync(OC_ROOT)) {
        ocMcp.mcpServers[name].env = { OPENCLAW_HOME: OC_ROOT };
      }
      writeJSON(OC_MCP, ocMcp);
      ok(`MCP (OC): registered ${name} in ${OC_MCP}`);
    } catch (e) {
      fail(`MCP (OC): registration failed. ${e.message}`);
    }
  } else if (existsSync(OC_MCP) && ocAlreadyRegistered) {
    skip(`MCP (OC): ${name} already registered`);
  }

  return ccRegistered;
}

function installClaudeCodeHook(repoPath, door) {
  const settingsPath = join(HOME, '.claude', 'settings.json');
  let settings = readJSON(settingsPath);

  if (!settings) {
    skip(`Claude Code: no settings.json found at ${settingsPath}`);
    return false;
  }

  // Always use the installed extension path, never repo clones or /tmp/
  const toolName = basename(repoPath);
  const installedGuard = join(LDM_EXTENSIONS, toolName, 'guard.mjs');
  const hookCommand = existsSync(installedGuard)
    ? `node ${installedGuard}`
    : (door.command || `node "${join(repoPath, 'guard.mjs')}"`);

  if (DRY_RUN) {
    ok(`Claude Code: would add ${door.event || 'PreToolUse'} hook (dry run)`);
    return true;
  }

  if (!settings.hooks) settings.hooks = {};
  const event = door.event || 'PreToolUse';

  if (!settings.hooks[event]) settings.hooks[event] = [];

  // Match by tool name in the command path, not exact string.
  // This prevents duplicates when the same tool is installed from different paths.
  const guardFile = basename(door.command || 'guard.mjs').replace(/^node\s+/, '').replace(/"/g, '');
  const existingIdx = settings.hooks[event].findIndex(entry =>
    entry.hooks?.some(h => {
      const cmd = h.command || '';
      return cmd.includes(`/${toolName}/`) || cmd === hookCommand;
    })
  );

  if (existingIdx !== -1) {
    const existingCmd = settings.hooks[event][existingIdx].hooks?.[0]?.command || '';
    if (existingCmd === hookCommand) {
      skip(`Claude Code: ${event} hook already configured`);
      return true;
    }
    // Update the existing hook to point to the installed location
    settings.hooks[event][existingIdx].hooks[0].command = hookCommand;
    settings.hooks[event][existingIdx].hooks[0].timeout = door.timeout || 10;
    try {
      writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
      ok(`Claude Code: ${event} hook updated to installed path`);
      return true;
    } catch (e) {
      fail(`Claude Code: failed to update settings.json. ${e.message}`);
      return false;
    }
  }

  settings.hooks[event].push({
    matcher: door.matcher || undefined,
    hooks: [{
      type: 'command',
      command: hookCommand,
      timeout: door.timeout || 10
    }]
  });

  try {
    writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
    ok(`Claude Code: ${event} hook added to settings.json`);
    return true;
  } catch (e) {
    fail(`Claude Code: failed to update settings.json. ${e.message}`);
    return false;
  }
}

function installSkill(repoPath, toolName) {
  const skillSrc = join(repoPath, 'SKILL.md');
  const ocSkillDir = join(OC_ROOT, 'skills', toolName);
  const ocSkillDest = join(ocSkillDir, 'SKILL.md');

  // Check if already deployed with same content
  if (existsSync(ocSkillDest)) {
    try {
      const srcContent = readFileSync(skillSrc, 'utf8');
      const destContent = readFileSync(ocSkillDest, 'utf8');
      if (srcContent === destContent) {
        skip(`Skill: ${toolName} already deployed to OpenClaw`);
        return true;
      }
    } catch {}
  }

  if (DRY_RUN) {
    ok(`Skill: would deploy ${toolName}/SKILL.md to ${ocSkillDir} (dry run)`);
    return true;
  }

  try {
    mkdirSync(ocSkillDir, { recursive: true });
    cpSync(skillSrc, ocSkillDest);
    ok(`Skill: deployed to ${ocSkillDir}`);
    return true;
  } catch (e) {
    fail(`Skill: deploy failed. ${e.message}`);
    return false;
  }
}

// ── Worktree gitignore ──

function ensureWorktreeGitignore(repoPath) {
  // Only for local repos, not /tmp/ clones
  if (repoPath.startsWith('/tmp/')) return;
  if (!existsSync(join(repoPath, '.git'))) return;

  const gitignorePath = join(repoPath, '.gitignore');
  const entry = '.claude/worktrees/';

  if (existsSync(gitignorePath)) {
    const content = readFileSync(gitignorePath, 'utf8');
    if (content.includes(entry)) return; // already present
    if (DRY_RUN) {
      ok(`Gitignore: would add ${entry} to ${gitignorePath} (dry run)`);
      return;
    }
    const separator = content.endsWith('\n') ? '' : '\n';
    writeFileSync(gitignorePath, content + separator + entry + '\n');
  } else {
    if (DRY_RUN) {
      ok(`Gitignore: would create ${gitignorePath} with ${entry} (dry run)`);
      return;
    }
    writeFileSync(gitignorePath, entry + '\n');
  }
  ok(`Gitignore: added ${entry} to .gitignore`);
}

// ── Single tool install ──

function installSingleTool(toolPath) {
  const { interfaces, pkg } = detectInterfaces(toolPath);
  const ifaceNames = Object.keys(interfaces);

  if (ifaceNames.length === 0) return 0;

  const toolName = pkg?.name?.replace(/^@\w+\//, '') || basename(toolPath);

  if (!JSON_OUTPUT) {
    console.log('');
    console.log(`  Installing: ${toolName}${DRY_RUN ? ' (dry run)' : ''}`);
    console.log(`  ${'─'.repeat(40)}`);
    log(`Detected ${ifaceNames.length} interface(s): ${ifaceNames.join(', ')}`);
    console.log('');
  }

  if (DRY_RUN && !JSON_OUTPUT) {
    console.log(describeInterfaces(interfaces));

    // Show migration preview in dry run
    const existing = findExistingInstalls(toolName, pkg, interfaces.openclaw?.config);
    if (existing.length > 0) {
      console.log('');
      for (const m of existing) {
        log(`Migration: would rename "${m.dirName}" -> "${toolName}" (matched by ${m.matchType})`);
      }
    }

    return ifaceNames.length;
  }

  // Detect and migrate existing installs under different names
  const existing = findExistingInstalls(toolName, pkg, interfaces.openclaw?.config);
  if (existing.length > 0) {
    console.log('');
    const migrated = new Set();
    for (const m of existing) {
      if (!migrated.has(m.dirName)) {
        log(`Found existing install: "${m.dirName}" (matched by ${m.matchType}). Migrating to "${toolName}"...`);
        migrateExistingInstall(m.dirName, toolName);
        migrated.add(m.dirName);
      }
    }
    console.log('');
  }

  let installed = 0;
  const registryInfo = {
    name: toolName,
    version: pkg?.version || 'unknown',
    source: toolPath,
    interfaces: ifaceNames,
  };

  if (interfaces.cli) {
    if (installCLI(toolPath, interfaces.cli)) installed++;
  }

  // Deploy to LDM + OpenClaw (for plugins or any extension with MCP)
  if (interfaces.openclaw) {
    if (installOpenClaw(toolPath, interfaces.openclaw, toolName)) {
      installed++;
      registryInfo.ldmPath = join(LDM_EXTENSIONS, toolName);
      registryInfo.ocPath = join(OC_EXTENSIONS, toolName);
    }
  } else if (interfaces.mcp) {
    // Even without openclaw.plugin.json, deploy to LDM for MCP server access
    const extName = basename(toolPath);
    if (deployExtension(toolPath, extName)) {
      registryInfo.ldmPath = join(LDM_EXTENSIONS, extName);
      registryInfo.ocPath = join(OC_EXTENSIONS, extName);
    }
  }

  if (interfaces.mcp) {
    if (registerMCP(toolPath, interfaces.mcp, toolName)) installed++;
  }

  if (interfaces.claudeCodeHook) {
    if (installClaudeCodeHook(toolPath, interfaces.claudeCodeHook)) installed++;
  }

  if (interfaces.skill) {
    if (installSkill(toolPath, toolName)) installed++;
  }

  if (interfaces.module) {
    ok(`Module: import from "${interfaces.module.main}"`);
    installed++;
  }

  // Update registry
  if (!DRY_RUN) {
    try {
      mkdirSync(LDM_EXTENSIONS, { recursive: true });
      updateRegistry(toolName, registryInfo);
      ok(`Registry: updated`);
    } catch (e) {
      fail(`Registry: update failed. ${e.message}`);
    }
  }

  // Ensure .claude/worktrees/ is in the repo's .gitignore
  ensureWorktreeGitignore(toolPath);

  return installed;
}

// ── Main ──

async function main() {
  if (!target || target === '--help' || target === '-h') {
    console.log('');
    console.log('  wip-install ... the reference installer for agent-native software');
    console.log('');
    console.log('  Usage:');
    console.log('    wip-install /path/to/repo');
    console.log('    wip-install https://github.com/org/repo');
    console.log('    wip-install org/repo');
    console.log('');
    console.log('  Flags:');
    console.log('    --dry-run   Detect interfaces without installing anything');
    console.log('    --json      Output detection results as JSON');
    console.log('');
    console.log('  Interfaces it detects and installs:');
    console.log('    CLI        ... package.json bin entry -> npm install -g');
    console.log('    Module     ... ESM main/exports -> importable');
    console.log('    MCP Server ... mcp-server.mjs -> claude mcp add --scope user');
    console.log('    OpenClaw   ... openclaw.plugin.json -> ~/.ldm/extensions/ + ~/.openclaw/extensions/');
    console.log('    Skill      ... SKILL.md -> ~/.openclaw/skills/<tool>/');
    console.log('    CC Hook    ... guard.mjs or claudeCode.hook -> ~/.claude/settings.json');
    console.log('');
    console.log('  Modes:');
    console.log('    Single repo  ... installs one tool');
    console.log('    Toolbox      ... detects tools/ subdirectories, installs each sub-tool');
    console.log('');
    console.log('  Paths:');
    console.log('    LDM:       ~/.ldm/extensions/<name>/     (primary, for Claude Code)');
    console.log('    OpenClaw:  ~/.openclaw/extensions/<name>/ (for Lesa/OpenClaw)');
    console.log('    Registry:  ~/.ldm/extensions/registry.json');
    console.log('');
    process.exit(0);
  }

  // ── LDM bootstrap ──
  // If ldm is not on PATH, try to install it silently before falling back.
  function bootstrapLdmOs() {
    try {
      execSync('npm install -g @wipcomputer/wip-ldm-os', { stdio: 'pipe', timeout: 120000 });
      execSync('ldm --version', { stdio: 'pipe', timeout: 5000 });
      return true;
    } catch {
      return false;
    }
  }

  // ── LDM delegation ──
  // If the ldm CLI is on PATH, delegate the entire install to it.
  // ldm install understands all the same interfaces and adds LDM OS orchestration.
  // Check early, before URL/path resolution, so we don't clone unnecessarily.
  let ldmAvailable = false;
  try {
    execSync('ldm --version', { stdio: 'pipe' });
    ldmAvailable = true;

    // ldm is available, delegate
    if (!JSON_OUTPUT) {
      console.log('');
      console.log('  LDM OS detected. Delegating to ldm install...');
      console.log('');
    }

    const flags = args.filter(a => a.startsWith('--'));
    const rawTarget = process.argv[2];

    execSync(`ldm install ${rawTarget} ${flags.join(' ')}`, { stdio: 'inherit' });

    if (!JSON_OUTPUT) {
      console.log('');
      console.log('  Tip: Run "ldm install" to see more components you can add.');
    }
    process.exit(0);

  } catch (e) {
    if (!ldmAvailable) {
      // ldm not on PATH, try bootstrap
      if (!JSON_OUTPUT) {
        console.log('');
        console.log('  Installing LDM OS infrastructure...');
        console.log('');
      }
      if (bootstrapLdmOs()) {
        ldmAvailable = true;
        if (!JSON_OUTPUT) {
          console.log('  LDM OS installed. Delegating to ldm install...');
          console.log('');
        }
        // Now delegate
        const flags = args.filter(a => a.startsWith('--'));
        const rawTarget = process.argv[2];
        try {
          execSync(`ldm install ${rawTarget} ${flags.join(' ')}`, { stdio: 'inherit' });
          process.exit(0);
        } catch (delegateErr) {
          if (!JSON_OUTPUT) console.error('  ldm install failed. Falling back to standalone installer.');
        }
      } else {
        if (!JSON_OUTPUT) {
          console.log('  LDM OS install skipped (npm offline or permissions issue). Using standalone.');
          console.log('');
        }
      }
    } else {
      // ldm exists but install command failed
      if (!JSON_OUTPUT) console.error('  ldm install failed. Falling back to standalone installer.');
    }
  }

  // Resolve target: GitHub URL, org/repo shorthand, or local path
  let repoPath;

  if (target.startsWith('http') || target.startsWith('git@') || target.match(/^[\w-]+\/[\w.-]+$/)) {
    const isShorthand = target.match(/^[\w-]+\/[\w.-]+$/);
    const httpsUrl = isShorthand
      ? `https://github.com/${target}.git`
      : target;
    const sshUrl = isShorthand
      ? `git@github.com:${target}.git`
      : target.replace(/^https:\/\/github\.com\//, 'git@github.com:');
    const repoName = basename(httpsUrl).replace('.git', '');
    repoPath = join('/tmp', `wip-install-${repoName}`);

    log('');
    log(`Cloning ${httpsUrl}...`);
    try {
      if (existsSync(repoPath)) {
        execSync(`rm -rf "${repoPath}"`);
      }
      try {
        execSync(`git clone "${httpsUrl}" "${repoPath}"`, { stdio: 'pipe' });
      } catch {
        // HTTPS failed (private repo or no auth). Fall back to SSH.
        log(`HTTPS clone failed. Trying SSH...`);
        if (existsSync(repoPath)) execSync(`rm -rf "${repoPath}"`);
        execSync(`git clone "${sshUrl}" "${repoPath}"`, { stdio: 'pipe' });
      }
      ok(`Cloned to ${repoPath}`);
    } catch (e) {
      fail(`Clone failed (tried HTTPS + SSH): ${e.message}`);
      process.exit(1);
    }
  } else {
    repoPath = resolve(target);
    if (!existsSync(repoPath)) {
      fail(`Path not found: ${repoPath}`);
      process.exit(1);
    }
  }

  // Check for toolbox mode (tools/ subdirectories with package.json)
  const subTools = detectToolbox(repoPath);

  if (subTools.length > 0) {
    // Toolbox mode: install each sub-tool
    const toolboxPkg = readJSON(join(repoPath, 'package.json'));
    const toolboxName = toolboxPkg?.name?.replace(/^@\w+\//, '') || basename(repoPath);

    if (!JSON_OUTPUT) {
      console.log('');
      console.log(`  Toolbox: ${toolboxName}`);
      console.log(`  ${'═'.repeat(50)}`);
      log(`Found ${subTools.length} sub-tool(s): ${subTools.map(t => t.name).join(', ')}`);
    }

    let totalInstalled = 0;
    let toolsProcessed = 0;

    for (const subTool of subTools) {
      const count = installSingleTool(subTool.path);
      totalInstalled += count;
      if (count > 0) toolsProcessed++;
    }

    if (!JSON_OUTPUT) {
      console.log('');
      console.log(`  ${'═'.repeat(50)}`);
      if (DRY_RUN) {
        console.log(`  Dry run complete. ${toolsProcessed} tool(s) scanned, ${totalInstalled} interface(s) detected.`);
      } else {
        console.log(`  Done. ${toolsProcessed} tool(s), ${totalInstalled} interface(s) processed.`);
      }
      console.log('');
    }
  } else {
    // Single repo mode
    if (JSON_OUTPUT) {
      const result = detectInterfacesJSON(repoPath);
      console.log(JSON.stringify(result, null, 2));
      if (DRY_RUN) process.exit(0);
    }

    const installed = installSingleTool(repoPath);

    if (installed === 0) {
      skip('No installable interfaces detected.');
      process.exit(0);
    }

    if (!JSON_OUTPUT) {
      console.log('');
      if (DRY_RUN) {
        console.log('  Dry run complete. No changes made.');
      } else {
        console.log(`  Done. ${installed} interface(s) processed.`);
      }
      console.log('');
    }
  }

  // ── LDM OS tip (standalone install only) ──
  // We only reach here if ldm was not available or ldm install failed.
  if (!JSON_OUTPUT && !DRY_RUN) {
    if (ldmAvailable) {
      console.log('  Tip: Run "ldm install" to see more components you can add.');
    } else {
      console.log('  Tip: LDM OS could not be installed automatically. Try: npm install -g @wipcomputer/wip-ldm-os');
    }
    console.log('');
  }
}

main().catch(e => {
  fail(e.message);
  process.exit(1);
});
