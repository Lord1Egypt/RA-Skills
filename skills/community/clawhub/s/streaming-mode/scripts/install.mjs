#!/usr/bin/env node
import { createHash } from 'node:crypto';
import {
  accessSync,
  appendFileSync,
  constants,
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  realpathSync,
  renameSync,
  rmSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import { homedir } from 'node:os';
import { delimiter, dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gunzipSync } from 'node:zlib';

export const ID = 'openclaw-streaming-mode';
export const HOST_VERSION = '2026.9.6';
const here = dirname(fileURLToPath(import.meta.url));
const packageDir = resolve(here, '..');

function packageAt(candidate) {
  try {
    const root = realpathSync(candidate);
    const manifest = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'));
    return manifest.name === 'openclaw' ? { root, manifest } : null;
  } catch {
    return null;
  }
}

function ancestors(start) {
  const rows = [];
  let current = start;
  while (current && !rows.includes(current)) {
    rows.push(current);
    const parent = dirname(current);
    if (parent === current) break;
    current = parent;
  }
  return rows;
}

export function findOpenClawRoot({
  env = process.env,
  platform = process.platform,
  home = homedir(),
  execPath = process.execPath,
} = {}) {
  const candidates = [];
  if (env.OPENCLAW_INSTALL_ROOT) {
    const found = packageAt(env.OPENCLAW_INSTALL_ROOT);
    if (!found) throw new Error('OPENCLAW_INSTALL_ROOT is not an OpenClaw package directory.');
    return found;
  }

  for (const directory of (env.PATH || '').split(delimiter).filter(Boolean)) {
    const names = platform === 'win32' ? ['openclaw.cmd', 'openclaw.ps1', 'openclaw.exe', 'openclaw'] : ['openclaw'];
    for (const name of names) {
      const executable = join(directory, name);
      if (!existsSync(executable)) continue;
      // npm shims sit beside node_modules on Windows; POSIX commands normally
      // symlink into the package. A local .bin shim uses its parent node_modules.
      candidates.push(join(directory, 'node_modules', 'openclaw'), join(directory, '..', 'openclaw'));
      try {
        candidates.push(...ancestors(dirname(realpathSync(executable))));
      } catch {
        // Ignore stale or unreadable PATH entries.
      }
    }
  }

  for (const nodePath of (env.NODE_PATH || '').split(delimiter).filter(Boolean)) {
    candidates.push(join(nodePath, 'openclaw'));
  }
  candidates.push(
    join(dirname(execPath), 'node_modules', 'openclaw'),
    resolve(dirname(execPath), '..', 'lib', 'node_modules', 'openclaw'),
    join(home, '.local', 'lib', 'node_modules', 'openclaw'),
    '/usr/local/lib/node_modules/openclaw',
    '/usr/lib/node_modules/openclaw',
  );
  if (platform === 'win32' && env.APPDATA) {
    candidates.push(join(env.APPDATA, 'npm', 'node_modules', 'openclaw'));
  }
  // Resolve Homebrew/version-manager Node symlinks without invoking npm or a shell.
  try {
    candidates.push(resolve(dirname(realpathSync(execPath)), '..', 'lib', 'node_modules', 'openclaw'));
  } catch {
    // An unavailable runtime fallback does not invalidate PATH discovery.
  }

  for (const candidate of candidates) {
    const found = packageAt(candidate);
    if (found) return found;
  }
  throw new Error('Could not locate the OpenClaw package. Set OPENCLAW_INSTALL_ROOT to the folder containing its package.json.');
}

function tarString(header, offset, length) {
  const end = header.indexOf(0, offset);
  return header.subarray(offset, end >= offset && end < offset + length ? end : offset + length)
    .toString('utf8')
    .trim();
}

function tarNumber(header, offset, length) {
  const value = tarString(header, offset, length).replace(/^0+/, '') || '0';
  if (!/^[0-7]+$/.test(value)) throw new Error('Streaming Mode payload contains an invalid tar size.');
  return Number.parseInt(value, 8);
}

function verifyTarChecksum(header) {
  const expected = tarNumber(header, 148, 8);
  let actual = 0;
  for (let index = 0; index < header.length; index += 1) {
    actual += index >= 148 && index < 156 ? 32 : header[index];
  }
  if (actual !== expected) throw new Error('Streaming Mode payload contains an invalid tar header checksum.');
}

function paxPath(data) {
  let cursor = 0;
  let path = null;
  while (cursor < data.length) {
    const space = data.indexOf(32, cursor);
    if (space < 0) throw new Error('Streaming Mode payload contains invalid tar metadata.');
    const length = Number.parseInt(data.subarray(cursor, space).toString('ascii'), 10);
    if (!Number.isSafeInteger(length) || length < 4 || cursor + length > data.length) {
      throw new Error('Streaming Mode payload contains invalid tar metadata.');
    }
    const record = data.subarray(space + 1, cursor + length - 1).toString('utf8');
    const separator = record.indexOf('=');
    if (separator > 0 && record.slice(0, separator) === 'path') path = record.slice(separator + 1);
    cursor += length;
  }
  return path;
}

function safeArchivePath(destination, archivePath) {
  if (!archivePath || archivePath.includes('\\') || archivePath.startsWith('/')) {
    throw new Error('Streaming Mode payload contains an unsafe path.');
  }
  const parts = archivePath.split('/').filter((part) => part && part !== '.');
  if (parts.length === 0) return destination;
  if (parts.some((part) => part === '..' || /[\x00-\x1f<>:"|?*]/u.test(part)
    || /[. ]$/u.test(part)
    || /^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/iu.test(part))) {
    throw new Error('Streaming Mode payload contains an unsafe path.');
  }
  const output = resolve(destination, ...parts);
  const rootPrefix = resolve(destination).replace(/[\\/]+$/u, '') + sep;
  if (output !== resolve(destination) && !output.startsWith(rootPrefix)) {
    throw new Error('Streaming Mode payload contains an unsafe path.');
  }
  return output;
}

function extractPayload(archive, destination) {
  const tar = gunzipSync(readFileSync(archive));
  let offset = 0;
  let pendingPath = null;
  while (offset + 512 <= tar.length) {
    const header = tar.subarray(offset, offset + 512);
    if (header.every((byte) => byte === 0)) return;
    verifyTarChecksum(header);
    if (tarString(header, 257, 6) !== 'ustar') {
      throw new Error('Streaming Mode payload is not a supported ustar archive.');
    }
    const size = tarNumber(header, 124, 12);
    const dataStart = offset + 512;
    const dataEnd = dataStart + size;
    if (!Number.isSafeInteger(size) || dataEnd > tar.length) {
      throw new Error('Streaming Mode payload tar entry is truncated.');
    }
    const type = String.fromCharCode(header[156] || 48);
    const name = tarString(header, 0, 100);
    const prefix = tarString(header, 345, 155);
    const headerPath = prefix ? `${prefix}/${name}` : name;

    if (type === 'x') {
      pendingPath = paxPath(tar.subarray(dataStart, dataEnd)) || pendingPath;
    } else if (type === 'L') {
      pendingPath = tar.subarray(dataStart, dataEnd).toString('utf8').replace(/\0.*$/su, '').trim();
    } else if (type === 'g') {
      // Global PAX metadata does not name an extracted entry.
    } else {
      const output = safeArchivePath(destination, pendingPath || headerPath);
      pendingPath = null;
      if (type === '5') {
        mkdirSync(output, { recursive: true });
      } else if (type === '0') {
        mkdirSync(dirname(output), { recursive: true });
        writeFileSync(output, tar.subarray(dataStart, dataEnd));
      } else {
        throw new Error(`Streaming Mode payload contains unsupported tar entry type ${type}.`);
      }
    }
    offset = dataStart + Math.ceil(size / 512) * 512;
  }
  throw new Error('Streaming Mode payload tar archive is incomplete.');
}

function sha256(path) {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

function hostBuildId(root) {
  try {
    const buildInfo = JSON.parse(readFileSync(join(root, 'dist', 'build-info.json'), 'utf8'));
    if (
      buildInfo.version !== HOST_VERSION
      || typeof buildInfo.buildId !== 'string'
      || !/^[a-zA-Z0-9._-]{1,96}$/.test(buildInfo.buildId)
    ) {
      throw new Error('invalid build identity');
    }
    return buildInfo.buildId;
  } catch {
    throw new Error('Could not verify the installed Gateway build identity. No files were changed.');
  }
}

function controlUiBuildId(indexPath) {
  try {
    const html = readFileSync(indexPath, 'utf8');
    const publicBuildId = /data-openclaw-control-ui-build-id=["']([^"']+)["']/.exec(html)?.[1];
    return publicBuildId?.match(/^([a-zA-Z0-9._-]{1,96})-[a-f0-9]{64}$/)?.[1] || null;
  } catch {
    return null;
  }
}

function requireMatchingUiBuild(indexPath, expectedBuildId, label) {
  const actualBuildId = controlUiBuildId(indexPath);
  if (actualBuildId !== expectedBuildId) {
    throw new Error(`${label} does not match this Gateway build (${actualBuildId || 'unknown'}; expected ${expectedBuildId}). No files were changed.`);
  }
}

function resolvePayloadArchive(payloadRoot, payloadManifest, temporaryArchive) {
  if (payloadManifest.schema === 1) {
    const archive = join(payloadRoot, payloadManifest.archive);
    if (!existsSync(archive) || sha256(archive) !== payloadManifest.sha256) {
      throw new Error('Streaming Mode payload checksum verification failed. No files were changed.');
    }
    return archive;
  }

  if (payloadManifest.schema !== 2 || !Array.isArray(payloadManifest.chunks) || payloadManifest.chunks.length === 0) {
    throw new Error('Unexpected Streaming Mode payload manifest.');
  }

  writeFileSync(temporaryArchive, Buffer.alloc(0), { mode: 0o600 });
  const seen = new Set();
  for (const chunk of payloadManifest.chunks) {
    if (
      typeof chunk?.file !== 'string'
      || !/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(chunk.file)
      || seen.has(chunk.file)
      || !Number.isSafeInteger(chunk.size)
      || chunk.size < 1
      || !/^[a-f0-9]{64}$/.test(chunk.sha256)
    ) {
      throw new Error('Unexpected Streaming Mode payload chunk metadata.');
    }
    seen.add(chunk.file);
    const chunkPath = join(payloadRoot, chunk.file);
    if (!existsSync(chunkPath) || statSync(chunkPath).size !== chunk.size || sha256(chunkPath) !== chunk.sha256) {
      throw new Error(`Streaming Mode payload chunk verification failed: ${chunk.file}. No files were changed.`);
    }
    appendFileSync(temporaryArchive, readFileSync(chunkPath));
  }
  if (sha256(temporaryArchive) !== payloadManifest.sha256) {
    throw new Error('Streaming Mode payload checksum verification failed. No files were changed.');
  }
  return temporaryArchive;
}

function atomicJson(path, value) {
  mkdirSync(dirname(path), { recursive: true });
  const temporary = `${path}.tmp-${process.pid}`;
  writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
  renameSync(temporary, path);
}

function verifyExtracted(stage, payloadManifest, expectedBuildId) {
  for (const name of ['index.html', 'asset-manifest.json', 'sw.js']) {
    if (!existsSync(join(stage, name))) throw new Error(`Streaming Mode payload is missing ${name}.`);
  }
  const assets = JSON.parse(readFileSync(join(stage, 'asset-manifest.json'), 'utf8')).assets;
  if (!Array.isArray(assets)) throw new Error('Streaming Mode asset manifest is invalid.');
  for (const asset of assets) {
    if (typeof asset?.path !== 'string' || !existsSync(join(stage, asset.path))) {
      throw new Error(`Streaming Mode payload is missing a manifest asset: ${asset?.path ?? 'unknown'}.`);
    }
  }
  requireMatchingUiBuild(join(stage, 'index.html'), expectedBuildId, 'The Streaming Mode payload');
  atomicJson(join(stage, 'streaming-mode-build.json'), payloadManifest);
}

function swapDirectory(target, stage) {
  const displaced = `${target}.streaming-mode-previous-${process.pid}`;
  renameSync(target, displaced);
  try {
    renameSync(stage, target);
  } catch (error) {
    renameSync(displaced, target);
    throw error;
  }
  rmSync(displaced, { recursive: true, force: true });
}

export function install({
  action = 'install',
  root: suppliedRoot,
  stateDir = process.env.OPENCLAW_STATE_DIR || join(homedir(), '.openclaw'),
  payloadRoot = join(packageDir, 'payload'),
  log = console.log,
} = {}) {
  if (!['install', 'rollback', 'status'].includes(action)) {
    throw new Error('Usage: node scripts/install.mjs [install|rollback|status]');
  }

  const found = suppliedRoot ? packageAt(suppliedRoot) : findOpenClawRoot();
  if (!found) throw new Error('OPENCLAW_INSTALL_ROOT is not an OpenClaw package directory.');
  const { root, manifest: hostManifest } = found;
  if (hostManifest.version !== HOST_VERSION) {
    throw new Error(`This release requires OpenClaw ${HOST_VERSION}; found ${hostManifest.version}. No files were changed.`);
  }

  const target = join(root, 'dist', 'control-ui');
  const expectedBuildId = hostBuildId(root);
  const statePath = join(stateDir, 'streaming-mode-installer.json');
  const backup = join(stateDir, 'streaming-mode-original-control-ui');
  const marker = join(target, 'streaming-mode-build.json');
  const state = existsSync(statePath) ? JSON.parse(readFileSync(statePath, 'utf8')) : null;
  if (state && (state.schema !== 1 || state.id !== ID || state.root !== root)) {
    throw new Error(`The installer record does not match this OpenClaw installation: ${statePath}`);
  }

  if (action === 'status') {
    const active = existsSync(marker);
    const installedBuildId = controlUiBuildId(join(target, 'index.html'));
    const healthy = installedBuildId === expectedBuildId;
    log(active
      ? `Streaming Mode is installed for OpenClaw ${HOST_VERSION}; build identity ${healthy ? 'matches' : 'DOES NOT MATCH'} the Gateway.`
      : `Streaming Mode is not active; Control UI build identity ${healthy ? 'matches' : 'DOES NOT MATCH'} the Gateway.`);
    return { active, healthy, expectedBuildId, installedBuildId, state };
  }

  if (!existsSync(join(target, 'index.html'))) {
    throw new Error(`OpenClaw Control UI was not found at ${target}. No files were changed.`);
  }
  accessSync(dirname(target), constants.W_OK);
  if (state && existsSync(backup)) {
    requireMatchingUiBuild(join(backup, 'index.html'), expectedBuildId, 'The saved original Control UI');
  }

  const stage = `${target}.streaming-mode-stage-${process.pid}`;
  const temporaryArchive = `${target}.streaming-mode-payload-${process.pid}.tar.gz`;
  rmSync(stage, { recursive: true, force: true });
  rmSync(temporaryArchive, { force: true });
  try {
    if (action === 'rollback') {
      if (!state || !existsSync(backup)) throw new Error(`No tracked backup is available at ${backup}.`);
      if (!existsSync(marker)) throw new Error('Streaming Mode is not the active Control UI; refusing to overwrite the current UI.');
      requireMatchingUiBuild(join(backup, 'index.html'), expectedBuildId, 'The saved original Control UI');
      log('Restoring the original Control UI. This can take a couple more minutes. Please do not interrupt it.');
      cpSync(backup, stage, { recursive: true, errorOnExist: true });
      swapDirectory(target, stage);
      atomicJson(statePath, { ...state, status: 'rolled-back', updatedAt: new Date().toISOString() });
      log('Original Control UI restored. Hard-refresh the browser tab. The Gateway does not need a restart.');
      return { status: 'rolled-back', target };
    }

    const payloadManifestPath = join(payloadRoot, 'manifest.json');
    const payloadManifest = JSON.parse(readFileSync(payloadManifestPath, 'utf8'));
    if (
      ![1, 2].includes(payloadManifest.schema)
      || payloadManifest.id !== ID
      || payloadManifest.hostVersion !== HOST_VERSION
      || payloadManifest.gatewayBuildId !== expectedBuildId
    ) {
      throw new Error('Unexpected Streaming Mode payload manifest.');
    }
    const archive = resolvePayloadArchive(payloadRoot, payloadManifest, temporaryArchive);

    log('Preparing the Control UI backup and verified Streaming Mode payload. This can take a couple more minutes. Please do not interrupt it.');
    mkdirSync(stage, { recursive: true });
    extractPayload(archive, stage);
    verifyExtracted(stage, payloadManifest, expectedBuildId);

    if (!state) {
      if (existsSync(backup)) throw new Error(`An untracked backup already exists at ${backup}.`);
      requireMatchingUiBuild(join(target, 'index.html'), expectedBuildId, 'The current Control UI');
      cpSync(target, backup, { recursive: true, errorOnExist: true });
      atomicJson(statePath, {
        schema: 1,
        id: ID,
        root,
        hostVersion: HOST_VERSION,
        gatewayBuildId: expectedBuildId,
        backup,
        status: 'prepared',
        createdAt: new Date().toISOString(),
      });
    }

    swapDirectory(target, stage);
    const nextState = JSON.parse(readFileSync(statePath, 'utf8'));
    atomicJson(statePath, { ...nextState, status: 'installed', updatedAt: new Date().toISOString(), payloadSha256: payloadManifest.sha256 });
    log('Streaming Mode installed and verified. Hard-refresh the Control UI, then use the Streaming Mode button. The Gateway does not need a restart.');
    return { status: 'installed', target };
  } finally {
    rmSync(stage, { recursive: true, force: true });
    rmSync(temporaryArchive, { force: true });
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    install({ action: process.argv[2] || 'install' });
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
