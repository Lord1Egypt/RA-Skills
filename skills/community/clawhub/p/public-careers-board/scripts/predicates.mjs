#!/usr/bin/env node
// Apply the unselected Magnite title readings to an observation file.
// This command does not fetch a board and does not choose a predicate.
// Caller input, the pin, and the pinned source share one bounded regular-file
// read and one deadline. A symlink or other non-regular file is refused
// before the body is allocated.
import { createHash } from 'node:crypto';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import {
  INPUT_BYTE_CAP,
  PREDICATE_DEADLINE_MS,
  containedByRoots,
  createDeadline,
  createExclusiveChild,
  installedRoots,
  readBoundedRegular,
} from './file-boundary.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REFUSED = new Set(['--pay', '--settle', '--sign', '--wallet', '--purchase']);
const PIN_CAP = 65536;

function emit(code, body) {
  process.stdout.write(`${JSON.stringify(body)}\n`);
  process.exitCode = code;
}

function refused(reason) {
  return { result: 'refused', reason, appliedPredicate: null, employmentDecision: false };
}

function mapInput(error) {
  if (error?.code === 'oversized') return 'oversized_source';
  if (error?.code === 'deadline') return 'deadline';
  if (error?.code === 'not_regular') return 'seed_rejected';
  if (error?.code === 'ambiguous') return 'ambiguous';
  if (error?.code === 'descriptor_unavailable') return 'descriptor_unavailable';
  return 'failed';
}

async function main() {
  const args = process.argv.slice(2);
  if (args.some((arg) => REFUSED.has(arg))) {
    emit(2, refused('payment_refused'));
    return;
  }
  if (args.length !== 1 || args[0].startsWith('--') || args[0].includes('://')) {
    emit(2, refused('usage'));
    return;
  }
  const clock = createDeadline(PREDICATE_DEADLINE_MS);
  let scratch = null;
  try {
    const pinBytes = await readBoundedRegular(resolve(root, 'references/source-pins.json'), PIN_CAP, clock).catch((error) => {
      throw Object.assign(new Error('tampered_source'), { code: error?.code === 'deadline' ? 'deadline' : 'tampered_source' });
    });
    let pin;
    try { pin = JSON.parse(pinBytes.toString('utf8')); }
    catch { throw Object.assign(new Error('tampered_source'), { code: 'tampered_source' }); }
    const item = pin.files?.find((entry) => entry.path === 'sources/predicates.mjs');
    if (!item || !Number.isSafeInteger(item.bytes) || item.bytes < 1 || item.bytes > INPUT_BYTE_CAP || typeof item.sha256 !== 'string') {
      throw Object.assign(new Error('tampered_source'), { code: 'tampered_source' });
    }
    const bytes = await readBoundedRegular(resolve(root, 'sources/predicates.mjs'), item.bytes, clock).catch((error) => {
      throw Object.assign(new Error('tampered_source'), { code: error?.code === 'deadline' ? 'deadline' : 'tampered_source' });
    });
    const digest = createHash('sha256').update(bytes).digest('hex');
    if (bytes.length !== item.bytes || digest !== item.sha256) {
      throw Object.assign(new Error('tampered_source'), { code: 'tampered_source' });
    }
    const inputBytes = await readBoundedRegular(resolve(args[0]), INPUT_BYTE_CAP, clock);
    let input;
    try { input = JSON.parse(inputBytes.toString('utf8')); }
    catch { throw Object.assign(new Error('seed_rejected'), { code: 'seed_rejected' }); }
    const rows = Array.isArray(input) ? input : input?.rows;
    if (!Array.isArray(rows)) throw Object.assign(new Error('usage'), { code: 'usage' });
    scratch = await mkdtemp(join(tmpdir(), 'careers-predicates-'));
    const roots = installedRoots(root);
    let inside = true;
    try { inside = await containedByRoots(scratch, roots); }
    catch (error) {
      if (error?.code === 'descriptor_unavailable') throw error;
      inside = true;
    }
    if (inside) throw Object.assign(new Error('failed'), { code: 'failed' });
    await createExclusiveChild(scratch, 'predicates.mjs', bytes, roots);
    const written = await readBoundedRegular(join(scratch, 'predicates.mjs'), bytes.length, clock).catch(() => {
      throw Object.assign(new Error('tampered_source'), { code: 'tampered_source' });
    });
    if (!written.equals(bytes)) throw Object.assign(new Error('tampered_source'), { code: 'tampered_source' });
    const mod = await import(pathToFileURL(join(scratch, 'predicates.mjs')).href);
    emit(0, { result: 'predicates', ...mod.applyPredicates(rows) });
  } catch (error) {
    const reason = error?.code === 'tampered_source' || error?.code === 'seed_rejected' || error?.code === 'usage' || error?.code === 'deadline' || error?.code === 'descriptor_unavailable' || error?.code === 'ambiguous'
      ? error.code
      : mapInput(error);
    emit(2, refused(reason));
  } finally {
    clock.stop();
    if (scratch) await rm(scratch, { recursive: true, force: true });
  }
}

await main();
