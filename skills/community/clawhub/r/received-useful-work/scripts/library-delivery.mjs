#!/usr/bin/env node
// The existing dispatcher owns exact-byte extraction and child output limits.
// This adapter only receives current sidecars and stages its approved libraries.
import { mkdir, mkdtemp, writeFile, rm } from 'node:fs/promises';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { acquireFunction } from './dispatch.mjs';
import { budget, readFileBounded, hash, fail } from './task-distribution/source.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const ORIGIN = 'https://neomorphic.io';
export const LIBRARY_GET_HEADERS = Object.freeze({ accept: '*/*', 'user-agent': 'received-useful-work/0.1.1' });
async function receive(path, { publicRoot, origin }, allowance, cap) {
  if (!/^\/downloads\/[a-z0-9-]+\/(?:current\.json|[0-9.]+\/[a-zA-Z0-9.-]+)$/.test(path)) throw fail('source_path');
  if (publicRoot) return readFileBounded(join(publicRoot, path.slice(1)), cap, allowance);
  if (origin !== ORIGIN) throw fail('public_origin_required');
  const target = new URL(origin + path);
  if (target.origin !== ORIGIN || target.username || target.password || target.hash) throw fail('blocked_source');
  const limit = Math.min(cap, allowance.remaining), signal = AbortSignal.timeout(allowance.left());
  const pending = fetch(target.href, { method: 'GET', redirect: 'manual', signal, headers: { ...LIBRARY_GET_HEADERS } });
  let response;
  try { response = await allowance.wait(pending); }
  catch (error) { void pending.then(late => late.body?.cancel()).catch(() => {}); throw error; }
  if (response.status !== 200) { void response.body?.cancel(); throw fail('source_http_' + response.status); }
  const length = response.headers.get('content-length');
  if (length && (!/^\d+$/.test(length) || Number(length) > limit)) { void response.body?.cancel(); throw fail('oversized_source'); }
  const reader = response.body?.getReader(); if (!reader) throw fail('source_body_missing');
  const chunks = []; let bytes = 0;
  try {
    while (true) {
      const step = await allowance.wait(reader.read()); if (step.done) break;
      bytes += step.value.byteLength; if (bytes > limit) throw fail('oversized_source');
      allowance.charge(step.value.byteLength); chunks.push(Buffer.from(step.value));
    }
    return Buffer.concat(chunks, bytes);
  } finally { void reader.cancel().catch(() => {}); }
}

export async function acquireLibrary(id, { publicRoot = null, origin = ORIGIN, work, timeoutMs = 15000, maxBytes = 1048576, outputBytes = 131072, operationBudget = null } = {}) {
  const allowance = operationBudget || budget(timeoutMs, maxBytes, outputBytes), deadline = Date.now() + allowance.left();
  const registry = JSON.parse(await readFileBounded(join(root, 'references/library-delivery.json'), 65536, allowance));
  const declared = registry.entries.find(item => item.id === id); if (!declared) throw fail('unsupported_library');
  let publication, entry, acquiredPin;
  if (declared.staged === true) {
    publication = JSON.parse(await receive(declared.publicationCurrent, { publicRoot, origin }, allowance, 65536));
    if (publication.packageName !== id || publication.version !== declared.publicationVersion || publication.archive !== declared.publicationArchive ||
        publication.sha256 !== declared.publicationSha256 || publication.bytes !== declared.publicationBytes) throw fail('current_requires_source_review');
    entry = JSON.parse(await receive(declared.machineEntry, { publicRoot, origin }, allowance, 65536));
    if (entry.hostedAcquisitionVerified === true) throw fail('staged_hosting_not_descriptor_fact');
    if (entry.packageName !== id || entry.version !== declared.version || entry.sha256 !== declared.sha256 || entry.bytes !== declared.bytes ||
        (entry.publicPath || entry.archive) !== declared.archive || entry.paymentAuthority !== 'none' || entry.claimAuthority !== 'none') throw fail('entry_pin_mismatch');
    acquiredPin = { archive: declared.archive, sha256: declared.sha256, bytes: declared.bytes };
  } else {
    publication = JSON.parse(await receive(declared.current, { publicRoot, origin }, allowance, 65536));
    if (publication.packageName !== id || publication.version !== declared.version || publication.archive !== declared.archive ||
        publication.sha256 !== declared.sha256 || publication.bytes !== declared.bytes) throw fail('current_requires_source_review');
    entry = JSON.parse(await receive(publication.machineEntry, { publicRoot, origin }, allowance, 65536));
    if (entry.packageName !== id || entry.version !== publication.version || entry.sha256 !== publication.sha256 || entry.bytes !== publication.bytes ||
        entry.paymentAuthority !== 'none' || entry.claimAuthority !== 'none') throw fail('entry_pin_mismatch');
    acquiredPin = publication;
  }
  if (JSON.stringify(entry.dependencies || []) !== JSON.stringify(declared.dependencies || [])) throw fail('dependency_requires_source_review');
  const received = [];
  for (const spec of [acquiredPin, ...(entry.dependencies || []).filter(item => item.archive)]) {
    const bytes = await receive(spec.archive, { publicRoot, origin }, allowance, spec.bytes);
    if (bytes.length !== spec.bytes || hash(bytes) !== spec.sha256) throw fail('tampered_archive');
    received.push({ ...spec, data: bytes });
  }
  await allowance.wait(mkdir(work, { mode: 0o700 }));
  const cache = await allowance.wait(mkdtemp(join(work, '.received-')));
  try {
    for (const item of received) {
      const file = join(cache, item.archive.slice(1));
      await allowance.wait(mkdir(dirname(file), { recursive: true }));
      await allowance.wait(writeFile(file, item.data, { flag: 'wx', mode: 0o600 }));
    }
    const dependencies = received.slice(1).map(item => ({ ...item, data: undefined, required: true, layout: 'top-directory', role: item.env }));
    const acquired = await acquireFunction(cache, { ...declared, dependencies, layout: declared.top ? 'top-directory' : 'flat', extractTop: declared.top },
      join(work, 'acquired'), null, id, deadline, allowance.output, 'caller');
    const result = { schema: 'neomorphic.received-library-acquisition.v1', id, version: entry.version, archive: acquiredPin.archive,
      sha256: acquiredPin.sha256, bytes: acquiredPin.bytes, sourceCoverage: publicRoot ? 'caller-supplied-local-public-tree' : 'anonymous_https',
      hostedAcquisitionVerified: false, publicationVersion: publication.version, stagedCandidate: declared.staged === true,
      executed: false, useful: null, settlement: null, paymentAuthority: 'none',
      packageDir: acquired.packageDir, command: ['node', join(acquired.packageDir, declared.consumer)],
      dependencies: acquired.dependencies.map(item => ({ id: item.id, root: item.dir, environment: item.role })),
      nextAction: 'Supply your own task to the acquired command. Acquisition is separate from execution and usefulness.' };
    allowance.left(); allowance.output.charge(JSON.stringify(result) + '\n');
    return result;
  } finally { await allowance.wait(rm(cache, { recursive: true, force: true })); }
}

async function main(argv) {
  const [command, ...rest] = argv, opts = {};
  let allowance;
  const write = async bytes => {
    try { await allowance.wait(new Promise((resolve, reject) => process.stdout.write(bytes, error => error ? reject(error) : resolve()))); }
    catch (error) { process.stdout.destroy(); throw error; }
  };
  process.stdout.on('error', () => { process.stdout.destroy(); process.exitCode = 2; });
  try {
    if (argv.length > 32 || argv.reduce((n, value) => n + Buffer.byteLength(value), 0) > 65536) throw fail('caller_input_limit');
    for (let i = 0; i < rest.length; i += 2) {
      if (!['--library', '--public-root', '--origin', '--work', '--timeout-ms', '--max-bytes', '--output-bytes'].includes(rest[i]) || !rest[i + 1] || rest[i + 1].startsWith('--') || opts[rest[i]]) throw fail('usage');
      opts[rest[i]] = rest[i + 1];
    }
    allowance = budget(Number(opts['--timeout-ms'] || 15000), Number(opts['--max-bytes'] || 1048576), Number(opts['--output-bytes'] || 131072));
    allowance.charge(argv.reduce((n, value) => n + Buffer.byteLength(value), 0));
    if (command === 'discover') {
      const output = (await readFileBounded(join(root, 'references/library-delivery.json'), 65536, allowance)).toString() + '\n';
      allowance.output.charge(output); await write(output); return;
    }
    if (command !== 'acquire' || !opts['--library'] || !opts['--work']) throw fail('usage');
    const result = await acquireLibrary(opts['--library'], { publicRoot: opts['--public-root'], origin: opts['--origin'] || ORIGIN, work: opts['--work'],
      operationBudget: allowance });
    await write(JSON.stringify(result) + '\n');
  } catch (error) {
    const reason = /^[a-z][a-z0-9_]{0,79}$/.test(error?.code || '') ? error.code : 'acquisition_failed';
    const bytes = JSON.stringify({ executed: false, useful: null, reason, nextAction: 'Recheck the current descriptor and exact bytes. Use a fresh caller work directory.' }) + '\n';
    try {
      if (!allowance || process.stdout.destroyed) throw error;
      allowance.left(); allowance.output.charge(bytes); await write(bytes);
    } catch { process.stdout.destroy(); }
    process.exitCode = 2;
  }
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await main(process.argv.slice(2));
