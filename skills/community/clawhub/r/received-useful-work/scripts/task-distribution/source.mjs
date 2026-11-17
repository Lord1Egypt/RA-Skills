import { request } from 'node:https';
import { constants } from 'node:fs';
import { open } from 'node:fs/promises';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { createOutputBudget } from './delivery-contracts/contracts.mjs';

export const ORIGIN = 'https://neomorphic.io';
export const PUBLIC_HEADERS = Object.freeze({ accept: '*/*', 'user-agent': 'task-distribution/0.1.0' });
export const ROOT = '/downloads/seller-repair-external-consumer/';
export const CURRENT = `${ROOT}current.json`;
export const fail = (code) => Object.assign(new Error(code), { code });
export const hash = bytes => createHash('sha256').update(bytes).digest('hex');
export function budget(timeoutMs = 15000, maxBytes = 262144, outputBytes = 131072) {
  if (!Number.isInteger(timeoutMs) || timeoutMs < 100 || timeoutMs > 30000 ||
      !Number.isInteger(maxBytes) || maxBytes < 1024 || maxBytes > 1048576 ||
      !Number.isInteger(outputBytes) || outputBytes < 1024 || outputBytes > 1048576) throw fail('invalid_budget');
  const end = performance.now() + timeoutMs;
  const output = createOutputBudget(outputBytes);
  return { remaining: maxBytes, output,
    left() { const ms = Math.ceil(end - performance.now()); if (ms <= 0) throw fail('deadline'); return ms; },
    charge(bytes) { this.left(); this.remaining -= bytes; if (this.remaining < 0) throw fail('oversized_source'); },
    async wait(promise) {
      let timer;
      try { return await Promise.race([promise, new Promise((_, reject) => { timer = setTimeout(() => reject(fail('deadline')), this.left()); })]); }
      finally { clearTimeout(timer); }
    },
  };
}
export async function readFileBounded(path, maxBytes = 65536, allowance = budget()) {
  const opening = open(path, constants.O_RDONLY | constants.O_NONBLOCK | constants.O_NOFOLLOW);
  let file;
  try { file = await allowance.wait(opening); }
  catch (error) { opening.then(handle => handle.close()).catch(() => {}); throw error; }
  try {
    if (!(await allowance.wait(file.stat())).isFile()) throw fail('source_not_file');
    maxBytes = Math.min(maxBytes, allowance.remaining);
    const bytes = Buffer.alloc(maxBytes + 1);
    let total = 0;
    while (total < bytes.length) { const result = await allowance.wait(file.read(bytes, total, bytes.length - total)); if (!result.bytesRead) break; total += result.bytesRead; }
    if (total > maxBytes) throw fail('oversized_source');
    allowance.charge(total);
    return bytes.subarray(0, total);
  } finally { void file.close().catch(() => {}); }
}
// One supported source: the owning public current/download route. The optional
// directory is an explicitly supplied offline snapshot, never reported as live.
export function sourceAdapter({ directory = null, readHttps = publicRead } = {}) {
  return async (path, allowance, cap = 65536) => {
    allowance.left();
    if (!path.startsWith(ROOT) || path.includes('..') || !/^[/a-zA-Z0-9.\-]+$/.test(path)) throw fail('blocked_source');
    const limit = Math.min(cap, allowance.remaining);
    if (limit <= 0) throw fail('oversized_source');
    let bytes;
    try {
      bytes = directory ? await readFileBounded(join(directory, path.split('/').at(-1)), limit, allowance)
        : await readHttps(ORIGIN + path, allowance.left(), limit);
    } catch (error) {
      error.observation = { url: ORIGIN + path, observedAt: new Date().toISOString(), coverage: directory ? 'caller-supplied-offline-snapshot' : 'one-anonymous-https-GET', maxBytes: limit, code: error.code || 'source_failed' };
      throw error;
    }
    allowance.left();
    if (bytes.length > limit) throw fail('oversized_source');
    if (!directory) allowance.charge(bytes.length);
    return { bytes, url: ORIGIN + path, observedAt: new Date().toISOString(), coverage: directory ? 'caller-supplied-offline-snapshot' : 'one-anonymous-https-GET' };
  };
}
export function publicReadPlan(url) {
  const parsed = new URL(url);
  if (parsed.origin !== ORIGIN || parsed.username || parsed.password || parsed.hash || !parsed.pathname.startsWith(ROOT)) throw fail('blocked_source');
  return { href: parsed.href, method: 'GET', headers: { ...PUBLIC_HEADERS }, body: null };
}
export function publicRead(url, timeoutMs, maxBytes, requestImpl = request) {
  const plan = publicReadPlan(url);
  const parsed = new URL(plan.href);
  return new Promise((resolve, reject) => {
    const chunks = []; let count = 0; let settled = false;
    const finish = (error, value) => { if (settled) return; settled = true; clearTimeout(timer); error ? reject(error) : resolve(value); };
    const req = requestImpl(parsed, { method: plan.method, headers: plan.headers }, response => {
      if (response.statusCode !== 200) { finish(fail(`source_http_${response.statusCode}`)); response.destroy(); return; }
      const size = response.headers['content-length'];
      if (size && (!/^\d+$/.test(size) || Number(size) > maxBytes)) { finish(fail('oversized_source')); response.destroy(); return; }
      response.on('data', chunk => { count += chunk.length; if (count > maxBytes) { finish(fail('oversized_source')); response.destroy(); } else chunks.push(chunk); });
      response.on('end', () => finish(null, Buffer.concat(chunks, count)));
      response.on('error', error => finish(error));
      response.on('aborted', () => finish(fail('source_aborted')));
    });
    const timer = setTimeout(() => { finish(fail('deadline')); req.destroy(); }, timeoutMs);
    req.on('error', error => finish(error)); req.end();
  });
}
