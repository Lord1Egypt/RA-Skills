import { existsSync, readdirSync, statSync } from 'node:fs';
import { basename, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function safeStat(path) {
  try {
    return statSync(path);
  } catch {
    return undefined;
  }
}

function safeReaddir(path) {
  try {
    return readdirSync(path);
  } catch {
    return [];
  }
}

export function isOpenClawPackageDir(path) {
  const stats = safeStat(path);
  if (!stats?.isDirectory()) return false;
  return existsSync(join(path, 'package.json')) && safeStat(join(path, 'dist'))?.isDirectory();
}

function nodePathCandidates(nodePath) {
  return String(nodePath || '')
    .split(':')
    .flatMap((entry) => {
      if (!entry) return [];
      const resolved = resolve(entry);
      return basename(resolved) === 'openclaw' ? [resolved] : [join(resolved, 'openclaw')];
    });
}

function nvmCandidates(homeDir) {
  const versionsDir = join(homeDir, '.nvm', 'versions', 'node');
  return safeReaddir(versionsDir)
    .map((version) => join(versionsDir, version, 'lib', 'node_modules', 'openclaw'));
}

export function openClawPackageCandidates({ homeDir = process.env.HOME || '', env = process.env } = {}) {
  return unique([
    env.SAGE_ROUTER_OPENCLAW_SDK_DIR,
    env.OPENCLAW_SDK_DIR,
    ...nodePathCandidates(env.NODE_PATH),
    homeDir && join(homeDir, '.local', 'lib', 'node_modules', 'openclaw'),
    homeDir && join(homeDir, '.npm-global', 'lib', 'node_modules', 'openclaw'),
    ...nvmCandidates(homeDir),
    '/usr/local/lib/node_modules/openclaw',
    '/usr/lib/node_modules/openclaw',
  ].map((candidate) => candidate && resolve(candidate)));
}

export function findOpenClawPackageDir(options = {}) {
  const candidates = openClawPackageCandidates(options);
  const found = candidates.find(isOpenClawPackageDir);
  if (found) return found;
  throw new Error(`Cannot find OpenClaw SDK package. Checked: ${candidates.join(', ')}`);
}

function distFiles(packageDir, matcher) {
  const distDir = join(packageDir, 'dist');
  return safeReaddir(distDir)
    .filter(matcher)
    .map((name) => join(distDir, name));
}

function callModuleCandidates(packageDir) {
  return [
    ...distFiles(packageDir, (name) => /^call\.runtime.*\.js$/.test(name)),
    ...distFiles(packageDir, (name) => /^call-[^.]+\.js$/.test(name) && !/^call-status-/.test(name)),
  ];
}

function clientInfoModuleCandidates(packageDir) {
  return [
    ...distFiles(packageDir, (name) => /^client-info-[^.]+\.js$/.test(name)),
    ...distFiles(packageDir, (name) => /^message-channel.*\.js$/.test(name)),
  ];
}

async function importFirst(paths, pick, label) {
  const errors = [];
  for (const path of paths) {
    try {
      const mod = await import(pathToFileURL(path).href);
      const value = pick(mod);
      if (value) return { path, value };
    } catch (error) {
      errors.push(`${path}: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
  const suffix = errors.length ? ` Import errors: ${errors.join(' | ')}` : '';
  throw new Error(`Cannot load OpenClaw ${label} module.${suffix}`);
}

function pickCallGateway(mod) {
  return typeof mod.callGateway === 'function' ? mod.callGateway : typeof mod.r === 'function' ? mod.r : undefined;
}

function pickClientInfo(mod) {
  const names = mod.GATEWAY_CLIENT_NAMES || mod.i || mod.g;
  const modes = mod.GATEWAY_CLIENT_MODES || mod.r || mod.h;
  return {
    clientName: names?.CLI || 'cli',
    clientMode: modes?.CLI || 'cli',
  };
}

export async function loadOpenClawGatewaySdk(options = {}) {
  const packageDir = findOpenClawPackageDir(options);
  const callModule = await importFirst(callModuleCandidates(packageDir), pickCallGateway, 'gateway call');
  let clientInfo = { path: undefined, value: { clientName: 'cli', clientMode: 'cli' } };
  try {
    clientInfo = await importFirst(clientInfoModuleCandidates(packageDir), pickClientInfo, 'client info');
  } catch {
    // OpenClaw accepts these wire values; constants are only used when available.
  }

  return {
    callGateway: callModule.value,
    clientName: clientInfo.value.clientName,
    clientMode: clientInfo.value.clientMode,
    packageDir,
    callModulePath: callModule.path,
    clientInfoModulePath: clientInfo.path,
  };
}
