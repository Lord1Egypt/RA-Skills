/**
 * lib/state.mjs
 * System state detection and reconciliation.
 * Scans the actual system (MCP servers, extensions, CLIs) to find what's
 * really installed, regardless of what the LDM registry thinks.
 * Zero dependencies.
 */

import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, basename } from 'node:path';
import { execSync } from 'node:child_process';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const LDM_EXTENSIONS = join(LDM_ROOT, 'extensions');
const OC_ROOT = join(HOME, '.openclaw');
const OC_EXTENSIONS = join(OC_ROOT, 'extensions');
const CC_USER_PATH = join(HOME, '.claude.json');
const REGISTRY_PATH = join(LDM_EXTENSIONS, 'registry.json');

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

// ── Scanners ──

function detectMCPServers() {
  const ccUser = readJSON(CC_USER_PATH);
  const servers = {};
  if (!ccUser?.mcpServers) return servers;

  for (const [name, config] of Object.entries(ccUser.mcpServers)) {
    const args = config.args || [];
    servers[name] = {
      name,
      command: config.command,
      args,
      path: args[0] || null,
      env: config.env || {},
    };
  }
  return servers;
}

function scanExtensionDir(dir) {
  const extensions = {};
  if (!existsSync(dir)) return extensions;

  try {
    const entries = readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name === 'registry.json') continue;
      if (entry.name.startsWith('.') || entry.name.startsWith('_')) continue;
      if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;

      const dirPath = join(dir, entry.name);
      const pkg = readJSON(join(dirPath, 'package.json'));
      const plugin = readJSON(join(dirPath, 'openclaw.plugin.json'));

      extensions[entry.name] = {
        name: entry.name,
        path: dirPath,
        version: pkg?.version || null,
        packageName: pkg?.name || null,
        pluginId: plugin?.id || null,
        hasPackageJson: !!pkg,
        hasPluginJson: !!plugin,
        hasMcpServer: existsSync(join(dirPath, 'mcp-server.mjs'))
                      || existsSync(join(dirPath, 'mcp-server.js'))
                      || existsSync(join(dirPath, 'dist', 'mcp-server.js')),
        hasSkill: existsSync(join(dirPath, 'SKILL.md')),
        isSymlink: entry.isSymbolicLink(),
      };
    }
  } catch {}
  return extensions;
}

function detectCLIBinaries() {
  const knownBins = [
    'crystal', 'mdview', 'wip-release', 'wip-repos', 'wip-file-guard',
    'ldm', 'ldm-scaffold', 'wip-install', 'wip-license', 'openclaw',
  ];

  const binaries = {};
  for (const bin of knownBins) {
    try {
      const path = execSync(`which ${bin} 2>/dev/null`, { encoding: 'utf8', timeout: 5000 }).trim();
      if (path) {
        binaries[bin] = { path };
        try {
          const ver = execSync(`${bin} --version 2>/dev/null`, { encoding: 'utf8', timeout: 5000 }).trim().split('\n')[0];
          binaries[bin].version = ver;
        } catch {}
      }
    } catch {}
  }
  return binaries;
}

function detectSkills() {
  const skillsDir = join(OC_ROOT, 'skills');
  const skills = {};
  if (!existsSync(skillsDir)) return skills;

  try {
    const entries = readdirSync(skillsDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const skillPath = join(skillsDir, entry.name, 'SKILL.md');
      if (existsSync(skillPath)) {
        skills[entry.name] = { path: skillPath };
      }
    }
  } catch {}
  return skills;
}

// ── Main detection ──

export function detectSystemState() {
  const registry = readJSON(REGISTRY_PATH) || { _format: 'v1', extensions: {} };

  return {
    mcp: detectMCPServers(),
    ldmExtensions: scanExtensionDir(LDM_EXTENSIONS),
    ocExtensions: scanExtensionDir(OC_EXTENSIONS),
    cliBinaries: detectCLIBinaries(),
    skills: detectSkills(),
    registry: registry.extensions || {},
  };
}

// ── Reconciliation ──

export function reconcileState(systemState) {
  const all = new Set();

  // Collect all known names from every source
  for (const name of Object.keys(systemState.registry)) all.add(name);
  for (const name of Object.keys(systemState.ldmExtensions)) all.add(name);
  for (const name of Object.keys(systemState.ocExtensions)) all.add(name);
  for (const name of Object.keys(systemState.mcp)) all.add(name);

  const reconciled = {};

  for (const name of all) {
    const reg = systemState.registry[name];
    const ldm = systemState.ldmExtensions[name];
    const oc = systemState.ocExtensions[name];
    const mcp = systemState.mcp[name];

    const entry = {
      name,
      // Registry
      inRegistry: !!reg,
      registryVersion: reg?.version || null,
      registrySource: reg?.source || null,
      registryHasSource: !!(reg?.source && (typeof reg.source === 'string' ? existsSync(reg.source) : !!reg.source.repo)),
      registryInterfaces: reg?.interfaces || [],
      // Deployed
      deployedLdm: !!ldm,
      ldmVersion: ldm?.version || null,
      deployedOc: !!oc,
      ocVersion: oc?.version || null,
      // MCP
      mcpRegistered: !!mcp,
      mcpPath: mcp?.path || null,
      // Computed
      status: 'unknown',
      issues: [],
    };

    // ── Determine status ──

    if (entry.inRegistry && entry.deployedLdm && entry.registryHasSource) {
      entry.status = 'healthy';
    } else if (entry.inRegistry && (entry.deployedLdm || entry.deployedOc) && !entry.registryHasSource) {
      // Deployed and registered, but no source repo linked
      entry.status = 'installed-unlinked';
      if (!reg?.source) {
        entry.issues.push('No source repo linked. Run: ldm install <org/repo> to link.');
      } else {
        entry.issues.push(`Source not found at: ${reg.source}`);
      }
    } else if (entry.inRegistry && !entry.deployedLdm && !entry.deployedOc) {
      entry.status = 'registered-missing';
      entry.issues.push('In registry but not deployed anywhere.');
    } else if (!entry.inRegistry && (entry.deployedLdm || entry.deployedOc)) {
      entry.status = 'deployed-unregistered';
      entry.issues.push('Deployed but not in LDM registry.');
    } else if (!entry.inRegistry && !entry.deployedLdm && !entry.deployedOc && entry.mcpRegistered) {
      entry.status = 'mcp-only';
      entry.issues.push('MCP server registered but not managed by LDM.');
    }

    // Version mismatches
    if (entry.ldmVersion && entry.ocVersion && entry.ldmVersion !== entry.ocVersion) {
      entry.issues.push(`Version mismatch: LDM v${entry.ldmVersion} vs OC v${entry.ocVersion}`);
    }
    if (entry.registryVersion && entry.ldmVersion && entry.registryVersion !== entry.ldmVersion) {
      entry.issues.push(`Registry says v${entry.registryVersion} but deployed is v${entry.ldmVersion}`);
    }

    // MCP path sanity
    if (entry.mcpRegistered && entry.deployedLdm && entry.mcpPath) {
      const expectedBase = join(LDM_EXTENSIONS, name);
      if (!entry.mcpPath.startsWith(expectedBase)) {
        entry.issues.push(`MCP path does not match LDM extension location.`);
      }
    }

    reconciled[name] = entry;
  }

  return reconciled;
}

// ── Display ──

export function formatReconciliation(reconciled, { verbose = false } = {}) {
  const installed = [];
  const broken = [];

  for (const entry of Object.values(reconciled)) {
    // Hide internal registry issues from normal output
    if (entry.status === 'registered-missing') {
      if (verbose) broken.push(entry);
      continue;
    }

    // Everything that's actually deployed, registered, or has an MCP server = installed
    if (entry.deployedLdm || entry.deployedOc || entry.mcpRegistered || entry.inRegistry) {
      installed.push(entry);
    }
  }

  const sort = (a, b) => a.name.localeCompare(b.name);
  const lines = [];

  lines.push('');
  lines.push('  System State');
  lines.push('  ────────────────────────────────────');

  if (installed.length > 0) {
    lines.push('');
    lines.push(`  Installed (${installed.length}):`);
    for (const e of installed.sort(sort)) {
      const ver = e.ldmVersion || e.ocVersion || e.registryVersion || '?';
      const mcp = e.mcpRegistered ? ' [MCP connected]' : '';
      lines.push(`    [x] ${e.name} v${ver}${mcp}`);
    }
  }

  if (broken.length > 0) {
    lines.push('');
    lines.push(`  Needs cleanup (${broken.length}):`);
    for (const e of broken.sort(sort)) {
      lines.push(`    [!] ${e.name} ... ${e.status}`);
    }
  }

  lines.push('');
  return lines.join('\n');
}
