#!/usr/bin/env node
// Installed client for the pinned free careers recipe.
// The byte bounds match the existing acquisition helper: 100–30000 ms,
// 1024–1048576 source bytes, and 1024–1048576 output bytes. This copy does
// not import a sibling skill, so an install stays self-contained. Local file
// reads and creates go through scripts/file-boundary.mjs, which stays inside
// the installed directory.
import { createHash } from 'node:crypto';
import { realpathSync } from 'node:fs';
import { chmod, mkdir, mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { basename, dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import {
  containedByRoots,
  createExclusiveChild,
  installedRoots,
  readBoundedRegular,
  writeNewFileOutside,
} from './file-boundary.mjs';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const REFUSED = new Set(['--pay', '--settle', '--sign', '--wallet', '--purchase']);
const FLAGS = new Set(['--board', '--source', '--out', '--seed', '--timeout-ms', '--max-bytes', '--output-bytes']);
const READERS = {
  acxiom: { id: 'acxiom', reader: 'fetchAcxiom', sourceKind: 'workday', boardKey: 'acxiom' },
  acxiomllc: { id: 'acxiom', reader: 'fetchAcxiom', sourceKind: 'workday', boardKey: 'acxiom' },
  liveramp: { id: 'liveramp', reader: 'fetchAshby', sourceKind: 'ashby', boardKey: 'liverampAshby' },
  'liveramp-inc': { id: 'liveramp', reader: 'fetchAshby', sourceKind: 'ashby', boardKey: 'liverampAshby' },
  liverampashby: { id: 'liveramp', reader: 'fetchAshby', sourceKind: 'ashby', boardKey: 'liverampAshby' },
  'liveramp-ashby': { id: 'liveramp', reader: 'fetchAshby', sourceKind: 'ashby', boardKey: 'liverampAshby' },
  magnite: { id: 'magnite', reader: 'fetchMagnite', sourceKind: 'magnite-workday', boardKey: 'magnite' },
  'magnite-careers': { id: 'magnite', reader: 'fetchMagnite', sourceKind: 'magnite-workday', boardKey: 'magnite' },
};
const SEED_FILE_CAP = 65536;

const fail = (code) => Object.assign(new Error(code), { code });

export function runtimeSupported(version) {
  const match = /^v?(\d+)\.(\d+)\.(\d+)/.exec(String(version || ''));
  if (!match) return false;
  const major = Number(match[1]);
  const minor = Number(match[2]);
  const patch = Number(match[3]);
  if (major > 22) return true;
  if (major < 22) return false;
  if (minor > 22) return true;
  if (minor < 22) return false;
  return patch >= 2;
}

function integer(value, min, max, code) {
  if (!/^[0-9]+$/.test(value || '')) throw fail(code);
  const number = Number(value);
  if (!Number.isSafeInteger(number) || number < min || number > max) throw fail(code);
  return number;
}

// One deadline for pin verification and the source read. Abort cancels owned
// work. Pin-file bytes use their own size cap and are not charged to the
// caller response budget: the pinned recipe is larger than the 1024 minimum.
function allowance(timeoutMs) {
  const end = Date.now() + timeoutMs;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  return {
    signal: controller.signal,
    end,
    left() {
      const ms = end - Date.now();
      if (ms <= 0 || controller.signal.aborted) throw fail('deadline');
      return ms;
    },
    async wait(promise) {
      if (controller.signal.aborted) throw fail('deadline');
      return await new Promise((resolvePromise, reject) => {
        const onAbort = () => reject(fail('deadline'));
        controller.signal.addEventListener('abort', onAbort, { once: true });
        Promise.resolve(promise).then(
          (value) => {
            controller.signal.removeEventListener('abort', onAbort);
            resolvePromise(value);
          },
          (error) => {
            controller.signal.removeEventListener('abort', onAbort);
            reject(error);
          },
        );
      });
    },
    stop() { clearTimeout(timer); },
  };
}

function sourceBudget(maxBytes, signal) {
  let used = 0;
  let over = false;
  return {
    signal,
    charge(bytes) {
      if (!Number.isSafeInteger(bytes) || bytes < 0) {
        over = true;
        return false;
      }
      used += bytes;
      if (used > maxBytes) {
        over = true;
        return false;
      }
      return true;
    },
    exceeded() { return over; },
  };
}

async function readRegular(filePath, maxBytes, clock) {
  try {
    return await readBoundedRegular(filePath, maxBytes, clock);
  } catch (error) {
    if (error.code === 'oversized') throw fail('oversized_source');
    if (error.code === 'deadline') throw error;
    if (error.code === 'ambiguous') throw fail('tampered_source');
    throw fail('tampered_source');
  }
}

async function readExact(filePath, expected, clock) {
  let bytes;
  try {
    bytes = await readBoundedRegular(filePath, expected.length, clock);
  } catch (error) {
    if (error.code === 'deadline') throw error;
    throw fail('tampered_source');
  }
  if (!bytes.equals(expected)) throw fail('tampered_source');
}

async function verifyRecipe(clock) {
  const pinBytes = await readRegular(resolve(root, 'references/pins.json'), 65536, clock);
  let pins;
  try { pins = JSON.parse(pinBytes.toString('utf8')); }
  catch { throw fail('tampered_source'); }
  if (!Array.isArray(pins.files) || pins.files.length !== 3 || typeof pins.revision !== 'string') throw fail('tampered_source');
  const files = new Map();
  for (const item of pins.files) {
    if (!item || typeof item.path !== 'string' || item.path.includes('..') || !item.path.startsWith('recipe/')) throw fail('tampered_source');
    if (!Number.isSafeInteger(item.bytes) || item.bytes < 0 || item.bytes > 1048576) throw fail('tampered_source');
    const bytes = await readRegular(resolve(root, item.path), item.bytes, clock);
    const digest = createHash('sha256').update(bytes).digest('hex');
    if (bytes.length !== item.bytes || digest !== item.sha256) throw fail('tampered_source');
    files.set(item.path, bytes);
  }
  if (!files.has('recipe/boards.mjs')) throw fail('tampered_source');
  return { pins, files };
}

function parseArgs(argv) {
  if (argv.length > 24) throw fail('usage');
  if (argv.reduce((sum, value) => sum + Buffer.byteLength(value), 0) > 8192) throw fail('usage');
  const refused = [];
  const opts = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (REFUSED.has(token)) { refused.push(token); continue; }
    if (!FLAGS.has(token)) throw fail('usage');
    const value = argv[i + 1];
    if (!value || value.startsWith('--') || opts[token]) throw fail('usage');
    opts[token] = value;
    i += 1;
  }
  return { refused, opts };
}

function sourceMatches(source, sourceKind, endpoint) {
  const token = source.trim();
  const lower = token.toLowerCase();
  if (lower === 'workday' || lower === 'ashby' || lower === 'magnite-workday') return lower === sourceKind;
  let url;
  try { url = new URL(token); }
  catch { return false; }
  if (url.protocol !== 'https:' || url.username || url.password || url.hash) return false;
  return url.href === endpoint;
}

function literalsFromRecipe(source) {
  const text = source.toString('utf8');
  const specs = {};
  for (const key of ['acxiom', 'liverampAshby']) {
    const match = new RegExp(`${key}:\\s*\\{[^}]*?boardUrl:\\s*"([^"]+)"[^}]*?endpoint:\\s*"([^"]+)"`).exec(text);
    if (!match) throw fail('tampered_source');
    let boardUrl;
    let endpoint;
    try {
      boardUrl = new URL(match[1]);
      endpoint = new URL(match[2]);
    } catch { throw fail('tampered_source'); }
    if (boardUrl.protocol !== 'https:' || endpoint.protocol !== 'https:' || boardUrl.username || endpoint.username) {
      throw fail('tampered_source');
    }
    specs[key] = { boardUrl: match[1], endpoint: match[2] };
  }
  return specs;
}

function assertImportsPinned(source, files) {
  const text = source.toString('utf8');
  for (const match of text.matchAll(/(?:from\s*|import\s*\(\s*)['"]([^'"]+)['"]/g)) {
    const spec = match[1];
    if (!spec.startsWith('.')) continue;
    const base = spec.split('/').filter(Boolean).pop();
    if (!base || !files.has(`recipe/${base}`)) throw fail('tampered_source');
  }
}

function boardClaim(coverage) {
  const status = coverage?.status;
  if (status === 'source_failure') return { boardClaim: 'source_failure', emptyBoard: false, complete: false };
  if (status === 'wrong_schema') return { boardClaim: 'wrong_schema', emptyBoard: false, complete: false };
  if (typeof status === 'string' && status.startsWith('partial')) {
    return { boardClaim: 'partial', emptyBoard: false, complete: false };
  }
  if (status === 'empty_board' || coverage?.emptyBoard === true) {
    return { boardClaim: 'empty', emptyBoard: true, complete: false };
  }
  if (typeof status === 'string' && status.startsWith('complete_')) {
    return { boardClaim: 'complete', emptyBoard: false, complete: true };
  }
  return { boardClaim: 'unclassified', emptyBoard: false, complete: false };
}

function base(extra) {
  return {
    schema: 'public-careers-board.result.v1',
    paymentSent: false,
    paidFallback: false,
    charged: false,
    useful: null,
    seeded: false,
    sourceCoverage: null,
    runtime: process.versions.node,
    ...extra,
  };
}

function declaredSize(item) {
  if (!item || typeof item !== 'object') throw fail('seed_rejected');
  if (item.drip === true) {
    if (item.dripIntervalMs !== undefined && (!Number.isSafeInteger(item.dripIntervalMs) || item.dripIntervalMs < 10 || item.dripIntervalMs > 200)) {
      throw fail('seed_rejected');
    }
    if (item.dripBytes !== undefined && (!Number.isSafeInteger(item.dripBytes) || item.dripBytes < 1 || item.dripBytes > 64)) {
      throw fail('seed_rejected');
    }
  }
  if (Object.hasOwn(item, 'padTo')) {
    if (!Number.isSafeInteger(item.padTo) || item.padTo < 0) throw fail('seed_rejected');
    return item.padTo;
  }
  if (typeof item.raw === 'string') return Buffer.byteLength(item.raw);
  if (item.body === undefined) return 0;
  return Buffer.byteLength(JSON.stringify(item.body));
}

function assertDeclaredBudget(responses, maxBytes) {
  let total = 0;
  for (const item of responses) {
    const size = declaredSize(item);
    if (size > maxBytes || total > maxBytes - size) throw fail('oversized_source');
    total += size;
  }
}

function seedFetch(responses, budget) {
  let index = 0;
  let reserved = 0;
  return async (url, init) => {
    const item = responses[index] || { httpStatus: 503, body: null };
    index += 1;
    const signal = init?.signal;
    if (item.hang === true || item.drip === true) {
      if (item.hang === true) {
        await new Promise((resolvePromise, reject) => {
          const onAbort = () => reject(Object.assign(new Error('aborted'), { name: 'AbortError' }));
          if (signal?.aborted) onAbort();
          else if (signal) signal.addEventListener('abort', onAbort, { once: true });
          else reject(fail('seed_rejected'));
          void resolvePromise;
        });
      }
    }
    if (item.drip === true) {
      const intervalMs = Number.isSafeInteger(item.dripIntervalMs) ? item.dripIntervalMs : 20;
      const chunk = Number.isSafeInteger(item.dripBytes) ? item.dripBytes : 16;
      let timer;
      const stream = new ReadableStream({
        start(controller) {
          const stop = () => {
            if (timer) clearInterval(timer);
            timer = undefined;
            try { controller.error(Object.assign(new Error('aborted'), { name: 'AbortError' })); }
            catch { /* already closed */ }
          };
          if (!signal || signal.aborted) {
            stop();
            return;
          }
          signal.addEventListener('abort', stop, { once: true });
          timer = setInterval(() => {
            try { controller.enqueue(Buffer.alloc(chunk, 0x62)); }
            catch {
              if (timer) clearInterval(timer);
              timer = undefined;
            }
          }, intervalMs);
        },
        cancel() {
          if (timer) clearInterval(timer);
          timer = undefined;
        },
      });
      return new Response(stream, {
        status: item.httpStatus ?? 200,
        headers: item.headers || { 'content-type': 'application/json' },
      });
    }
    let body;
    if (Object.hasOwn(item, 'padTo')) {
      if (!Number.isSafeInteger(item.padTo) || item.padTo < 0) throw fail('seed_rejected');
      if (item.padTo > budget.maxBytes || reserved > budget.maxBytes - item.padTo) {
        budget.markExceeded();
        throw fail('oversized_source');
      }
      reserved += item.padTo;
      body = Buffer.alloc(item.padTo, 0x61);
    } else if (typeof item.raw === 'string') body = Buffer.from(item.raw);
    else if (item.body === undefined) body = Buffer.alloc(0);
    else body = Buffer.from(JSON.stringify(item.body));
    return new Response(body, {
      status: item.httpStatus ?? 200,
      headers: item.headers || { 'content-type': 'application/json' },
    });
  };
}

function limitingFetch(inner, budget) {
  return async (url, init = {}) => {
    const signals = [init.signal, budget.signal].filter(Boolean);
    const signal = signals.length ? AbortSignal.any(signals) : undefined;
    const response = await inner(String(url), { ...init, signal });
    if (!response?.body) return response;
    const reader = response.body.getReader();
    let cancelled = false;
    const cancelReader = async (reason) => {
      if (cancelled) return;
      cancelled = true;
      await reader.cancel(reason).catch(() => {});
    };
    const onAbort = () => { void cancelReader('aborted'); };
    for (const item of signals) item.addEventListener('abort', onAbort, { once: true });
    const stream = new ReadableStream({
      async pull(controller) {
        if (signal?.aborted || budget.exceeded()) {
          await cancelReader('aborted');
          controller.error(Object.assign(new Error('aborted'), { name: 'AbortError' }));
          return;
        }
        let next;
        try { next = await reader.read(); }
        catch (error) {
          controller.error(error);
          return;
        }
        if (next.done) {
          controller.close();
          return;
        }
        const size = next.value?.byteLength || 0;
        if (!budget.charge(size)) {
          await cancelReader('oversized_source');
          controller.error(Object.assign(new Error('oversized_source'), { name: 'SourceBudgetError' }));
          return;
        }
        controller.enqueue(next.value);
      },
      cancel(reason) { return cancelReader(reason); },
    });
    return new Response(stream, {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
    });
  };
}

async function loadSeed(filePath, clock, maxBytes) {
  const bytes = await readRegular(filePath, SEED_FILE_CAP, clock).catch((error) => {
    if (error.code === 'oversized_source' || error.code === 'deadline') throw error;
    throw fail('seed_rejected');
  });
  let seed;
  try { seed = JSON.parse(bytes.toString('utf8')); }
  catch { throw fail('seed_rejected'); }
  if (seed?.schema !== 'public-careers-board.supplied-seed.v1' || !Array.isArray(seed.responses) || seed.responses.length > 8) {
    throw fail('seed_rejected');
  }
  assertDeclaredBudget(seed.responses, maxBytes);
  return seed.responses;
}

async function writeOwned(filePath, line) {
  await writeNewFileOutside(filePath, line, installedRoots(root));
}

function classifyTransport(observation) {
  const requests = observation?.coverage?.requests;
  if (!Array.isArray(requests)) throw fail('failed');
  for (const entry of requests) {
    if (entry?.error === 'timeout') throw fail('timeout');
    if (entry?.error === 'response_too_large') throw fail('oversized_source');
    if (entry?.error === 'wrong_host') throw fail('unexpected_origin');
  }
  return requests;
}

async function writeSnapshotFile(dir, rel, bytes, prefix, clock) {
  if (typeof rel !== 'string' || rel.includes('..') || !rel.startsWith(prefix)) throw fail('tampered_source');
  const dest = join(dir, rel);
  const relCheck = relative(dir, dest);
  if (relCheck.startsWith('..') || isAbsolute(relCheck)) throw fail('tampered_source');
  try {
    await createExclusiveChild(dirname(dest), basename(rel), bytes, installedRoots(root));
  } catch (error) {
    if (error?.code === 'overwrite_refused') throw fail('failed');
    throw error;
  }
  await readExact(dest, bytes, clock);
}

function httpsLiteral(value) {
  let url;
  try { url = new URL(value); }
  catch { throw fail('tampered_source'); }
  if (url.protocol !== 'https:' || url.username || url.password || url.hash) throw fail('tampered_source');
  return url;
}

async function verifyMagniteSource(clock, recipeBytes) {
  const pinBytes = await readRegular(resolve(root, 'references/source-pins.json'), 65536, clock);
  let pin;
  try { pin = JSON.parse(pinBytes.toString('utf8')); }
  catch { throw fail('tampered_source'); }
  if (pin?.schema !== 'public-careers-board.source-pins.v1' || pin.parent?.reusedExport !== 'normalizeWorkday') {
    throw fail('tampered_source');
  }
  const recipeSha = createHash('sha256').update(recipeBytes).digest('hex');
  if (pin.parent.recipeSha256 !== recipeSha) throw fail('tampered_source');
  const source = pin.source;
  if (!source || typeof source.tenant !== 'string' || typeof source.siteId !== 'string' || source.tenant === source.hostnameLabel) {
    throw fail('tampered_source');
  }
  const board = httpsLiteral(source.boardUrl);
  const endpoint = httpsLiteral(source.endpoint);
  httpsLiteral(source.careersPage);
  httpsLiteral(source.robotsUrl);
  if (board.host !== endpoint.host) throw fail('tampered_source');
  const built = `${board.origin}/wday/cxs/${source.tenant}/${source.siteId}/jobs`;
  if (built !== source.endpoint || source.endpoint.includes(`/${source.hostnameLabel}/`)) throw fail('tampered_source');
  if (!Array.isArray(pin.files)) throw fail('tampered_source');
  const item = pin.files.find((entry) => entry?.path === 'sources/magnite.mjs');
  if (!item || !Number.isSafeInteger(item.bytes) || item.bytes < 0 || item.bytes > 1048576 || typeof item.sha256 !== 'string') {
    throw fail('tampered_source');
  }
  const bytes = await readRegular(resolve(root, item.path), item.bytes, clock);
  const digest = createHash('sha256').update(bytes).digest('hex');
  if (bytes.length !== item.bytes || digest !== item.sha256) throw fail('tampered_source');
  return {
    bytes,
    spec: {
      boardUrl: source.boardUrl,
      endpoint: source.endpoint,
      careersPage: source.careersPage,
      robotsUrl: source.robotsUrl,
    },
  };
}

async function runSnapshot(files, fn, extraFiles = null, clock) {
  const dir = await mkdtemp(join(tmpdir(), `careers-snap-${process.pid}-`));
  try {
    let inside = true;
    try { inside = await containedByRoots(dir, installedRoots(root)); }
    catch (error) {
      if (error?.code === 'descriptor_unavailable') throw error;
      inside = true;
    }
    if (inside) throw fail('failed');
    await chmod(dir, 0o700);
    const recipeDir = join(dir, 'recipe');
    await mkdir(recipeDir, { mode: 0o700 });
    await chmod(recipeDir, 0o700);
    for (const [rel, bytes] of files) await writeSnapshotFile(dir, rel, bytes, 'recipe/', clock);
    if (extraFiles) {
      const sourceDir = join(dir, 'sources');
      await mkdir(sourceDir, { mode: 0o700 });
      await chmod(sourceDir, 0o700);
      for (const [rel, bytes] of extraFiles) await writeSnapshotFile(dir, rel, bytes, 'sources/', clock);
    }
    const mod = await import(pathToFileURL(join(dir, 'recipe/boards.mjs')).href);
    if (extraFiles) {
      const sourceMod = await import(pathToFileURL(join(dir, 'sources/magnite.mjs')).href);
      return await fn(mod, sourceMod);
    }
    return await fn(mod);
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

function refusal(reason) {
  return base({
    result: 'refused',
    reason,
    board: null,
    reader: null,
    source: null,
    rows: null,
    coverage: null,
    nextAction: reason === 'payment_refused'
      ? 'This command does not buy a careers board. Re-read the live challenge only on a separate authorized executor.'
      : 'The observation was not produced. A refusal is not an empty or complete board.',
  });
}

async function finish(code, body, opts, outputBytes, started) {
  let finalBody = { ...body, elapsedMs: Date.now() - started };
  let line = `${JSON.stringify(finalBody)}\n`;
  let finalCode = code;
  if (Buffer.byteLength(line) > outputBytes) {
    finalBody = { ...refusal('oversized_output'), elapsedMs: Date.now() - started };
    line = `${JSON.stringify(finalBody)}\n`;
    finalCode = 2;
  }
  if (opts?.['--out']) await writeOwned(resolve(opts['--out']), line);
  return { code: finalCode, body: finalBody, line };
}

export async function execute(argv) {
  const started = Date.now();
  let opts = {};
  let outputBytes = 1048576;
  let clock;
  try {
    if (!runtimeSupported(process.versions.node)) throw fail('unsupported_runtime');
    const command = argv[0];
    const parsed = parseArgs(argv.slice(1));
    opts = parsed.opts;
    if (parsed.refused.length) throw fail('payment_refused');
    if (command !== 'run') throw fail('usage');
    const timeoutMs = integer(opts['--timeout-ms'] || '15000', 100, 30000, 'usage');
    const maxBytes = integer(opts['--max-bytes'] || '1000000', 1024, 1048576, 'usage');
    outputBytes = integer(opts['--output-bytes'] || '1048576', 1024, 1048576, 'usage');
    clock = allowance(timeoutMs);
    const { pins, files } = await verifyRecipe(clock);
    const board = opts['--board']?.trim() || '';
    if (!board) {
      return await finish(0, base({
        result: 'missing_input',
        reason: 'missing_input',
        board: null,
        reader: null,
        source: null,
        rows: null,
        coverage: null,
        nextAction: 'Pass --board with one supported id: acxiom, acxiomllc, liveramp, liveramp-inc, liverampashby, liveramp-ashby, magnite, or magnite-careers.',
      }), opts, outputBytes, started);
    }
    const reader = READERS[board];
    if (!reader) {
      return await finish(0, base({
        result: 'unknown_board',
        reason: 'unknown_board',
        board,
        reader: null,
        source: null,
        rows: null,
        coverage: null,
        nextAction: 'That board is not supported. No source was read.',
      }), opts, outputBytes, started);
    }
    const recipeSource = files.get('recipe/boards.mjs');
    const specs = literalsFromRecipe(recipeSource);
    let spec = specs[reader.boardKey];
    let magniteBytes = null;
    if (reader.reader === 'fetchMagnite') {
      const loaded = await verifyMagniteSource(clock, recipeSource);
      spec = loaded.spec;
      magniteBytes = loaded.bytes;
    }
    if (!spec?.endpoint || !spec?.boardUrl) throw fail('tampered_source');
    if (opts['--source'] && !sourceMatches(opts['--source'], reader.sourceKind, spec.endpoint)) {
      return await finish(0, base({
        result: 'wrong_source',
        reason: 'wrong_source',
        board: reader.id,
        reader: reader.reader,
        source: null,
        rows: null,
        coverage: null,
        emptyBoard: false,
        complete: false,
        nextAction: reader.reader === 'fetchMagnite'
          ? 'Magnite reads only its declared Workday endpoint after the official careers handoff. A generic workday token and the SmartRecruiters host are not that source.'
          : 'That source is not the supported reader. Acxiom uses Workday. LiveRamp uses Ashby. No other origin is fetched.',
      }), opts, outputBytes, started);
    }
    assertImportsPinned(recipeSource, files);
    const responses = opts['--seed'] ? await loadSeed(resolve(opts['--seed']), clock, maxBytes) : null;
    const budget = sourceBudget(maxBytes, clock.signal);
    budget.maxBytes = maxBytes;
    budget.markExceeded = () => { budget.charge(maxBytes + 1); };
    const fetchImpl = limitingFetch(responses ? seedFetch(responses, budget) : globalThis.fetch.bind(globalThis), budget);
    const fetchedAt = new Date().toISOString();
    const ctx = { boardUrl: spec.boardUrl, source: spec.endpoint, fetchedAt };
    const observation = reader.reader === 'fetchMagnite'
      ? await runSnapshot(files, async (mod, sourceMod) => {
        if (typeof mod.normalizeWorkday !== 'function' || typeof sourceMod.fetchMagnite !== 'function') throw fail('tampered_source');
        const declared = sourceMod.MAGNITE;
        if (declared?.endpoint !== spec.endpoint || declared?.boardUrl !== spec.boardUrl || declared?.careersPage !== spec.careersPage || declared?.robotsUrl !== spec.robotsUrl) {
          throw fail('tampered_source');
        }
        if (declared.tenant === declared.hostnameLabel || sourceMod.endpointUsingHostnameLabel() === declared.endpoint) {
          throw fail('tampered_source');
        }
        return sourceMod.fetchMagnite({
          normalizeWorkday: mod.normalizeWorkday,
          timeoutMs: clock.left(),
          maxBytes,
          fetchImpl,
          signal: clock.signal,
        });
      }, new Map([['sources/magnite.mjs', magniteBytes]]), clock)
      : await runSnapshot(files, async (mod) => {
        const live = mod.BOARDS?.[reader.boardKey];
        if (typeof mod[reader.reader] !== 'function' || live?.endpoint !== spec.endpoint || live?.boardUrl !== spec.boardUrl) {
          throw fail('tampered_source');
        }
        return mod[reader.reader](ctx, { timeoutMs: clock.left(), maxBytes, fetchImpl });
      }, null, clock);
    if (budget.exceeded()) throw fail('oversized_source');
    if (clock.signal.aborted) throw fail('deadline');
    const requestList = observation?.kind === 'classified' ? observation.requests : observation?.coverage?.requests;
    const requests = classifyTransport({ coverage: { requests: requestList } });
    const allowedHosts = new Set([new URL(spec.endpoint).host]);
    if (spec.careersPage) allowedHosts.add(new URL(spec.careersPage).host);
    if (spec.robotsUrl) allowedHosts.add(new URL(spec.robotsUrl).host);
    if (requests.some((entry) => {
      try { return !allowedHosts.has(new URL(entry.url).host); }
      catch { return true; }
    })) throw fail('unexpected_origin');
    if (observation?.kind === 'classified') {
      return await finish(0, base({
        result: observation.result,
        reason: observation.reason,
        board: reader.id,
        reader: reader.reader,
        source: spec.endpoint,
        seeded: Boolean(opts['--seed']),
        sourceCoverage: opts['--seed'] ? 'supplied_seed' : 'live_public_https',
        recipeRevision: pins.revision,
        rows: null,
        coverage: null,
        boardClaim: observation.result,
        emptyBoard: false,
        complete: false,
        handoff: observation.handoff ?? null,
        identity: observation.identity ?? null,
        requests,
        nextAction: observation.nextAction,
      }), opts, outputBytes, started);
    }
    const rows = Array.isArray(observation.rows) ? observation.rows : [];
    const claim = boardClaim(observation.coverage);
    return await finish(0, base({
      result: 'observation',
      reason: observation.coverage?.status || null,
      board: reader.id,
      reader: reader.reader,
      source: spec.endpoint,
      seeded: Boolean(opts['--seed']),
      sourceCoverage: opts['--seed'] ? 'supplied_seed' : 'live_public_https',
      recipeRevision: pins.revision,
      rows,
      coverage: observation.coverage,
      ...claim,
      nextAction: 'Inspect coverage.status. A source failure is not an empty or complete board. Usefulness stays with the caller.',
    }), opts, outputBytes, started);
  } catch (error) {
    const reason = /^[a-z][a-z0-9_]{0,79}$/.test(error?.code || '') ? error.code : 'failed';
    const writeOpts = reason === 'overwrite_refused' ? {} : opts;
    try {
      return await finish(2, refusal(reason), writeOpts, outputBytes, started);
    } catch {
      const body = { ...refusal(reason), elapsedMs: Date.now() - started };
      return { code: 2, body, line: `${JSON.stringify(body)}\n` };
    }
  } finally {
    clock?.stop();
  }
}

async function main() {
  const result = await execute(process.argv.slice(2));
  const line = result.line || `${JSON.stringify(result.body)}\n`;
  try {
    await new Promise((resolvePromise, reject) => {
      process.stdout.write(line, (error) => (error ? reject(error) : resolvePromise()));
    });
  } catch {
    process.exitCode = 2;
    return;
  }
  process.exitCode = result.code;
}

function invokedDirectly() {
  const entry = process.argv[1];
  if (!entry) return false;
  try {
    return realpathSync(fileURLToPath(import.meta.url)) === realpathSync(resolve(entry));
  } catch {
    return false;
  }
}

if (invokedDirectly()) await main();
