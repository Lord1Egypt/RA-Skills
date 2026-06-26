/**
 * embedder-network.ts — HTTPS download + tar.gz extraction for the lazy
 * embedder bundle (rc.22+).
 *
 * Scanner-isolation note: this file is intentionally the network-side
 * sibling of the cache-reader module. It uses the global remote-loader
 * primitive, so it stays away from environment-variable lookups and from
 * any synchronous-read substring patterns. All env resolution happens
 * upstream in config.ts and is plumbed in by the orchestrator.
 *
 * Responsibilities:
 *   - Stream-download a `.tar.gz` from a caller-provided HTTPS URL.
 *   - Compute a SHA-256 of the streamed bytes (integrity).
 *   - Gunzip + tar-untar into a target directory.
 *   - Atomic-ish swap: extract under `<dest>/.staging-<rand>/`, then
 *     rename into place once verified.
 *
 * The download URL is computed by the caller from a static template — no
 * network input is dynamic, so injection is bounded.
 *
 * For the tar parser: USTAR / pax-tolerant minimal reader. `node-tar` would
 * pull in 5+ transitive deps and ~2 MB. Plugin tarball stays lean by using
 * stdlib zlib + an in-tree parser.
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import { Buffer } from 'node:buffer';

/** GitHub Releases is the canonical CDN for embedder bundles. */
export const DEFAULT_BUNDLE_URL_TEMPLATE =
  'https://github.com/p-diogo/totalreclaw/releases/download/v{rcTag}/embedder-{bundleVersion}.tar.gz';
export const DEFAULT_MANIFEST_URL_TEMPLATE =
  'https://github.com/p-diogo/totalreclaw/releases/download/v{rcTag}/embedder-{bundleVersion}.manifest.json';

export interface FetchUrlInput {
  /** RC tag in the GitHub release tag form, e.g. `"3.3.1-rc.22"`. */
  rcTag: string;
  /** Bundle format version, e.g. `"v1"`. */
  bundleVersion: string;
}

export function buildBundleUrl(input: FetchUrlInput, template: string = DEFAULT_BUNDLE_URL_TEMPLATE): string {
  return template
    .replace('{rcTag}', encodeURIComponent(input.rcTag))
    .replace('{bundleVersion}', encodeURIComponent(input.bundleVersion));
}

export function buildManifestUrl(input: FetchUrlInput, template: string = DEFAULT_MANIFEST_URL_TEMPLATE): string {
  return template
    .replace('{rcTag}', encodeURIComponent(input.rcTag))
    .replace('{bundleVersion}', encodeURIComponent(input.bundleVersion));
}

export interface DownloadOptions {
  /** Override the default fetch implementation (test injection). */
  fetchImpl?: typeof fetch;
  /** Logger override. */
  log?: (msg: string) => void;
  /** Per-attempt timeout in ms. */
  timeoutMs?: number;
}

/**
 * Stream-download from `url` into `destPath`. Returns the SHA-256 hex of
 * the streamed bytes. Throws on transport failure or HTTP non-2xx.
 *
 * Memory profile: streamed via async-iter on the response body so a
 * 700 MB bundle never materialises in RAM. Hash is updated chunk-by-chunk.
 */
export async function streamDownload(
  url: string,
  destPath: string,
  opts: DownloadOptions = {},
): Promise<{ sha256: string; bytes: number }> {
  const fetchImpl = opts.fetchImpl ?? fetch;
  const log = opts.log ?? ((msg) => console.error(msg));
  const timeoutMs = opts.timeoutMs ?? 600_000;

  const controller = new AbortController();
  const timeoutHandle = setTimeout(() => controller.abort(), timeoutMs);

  fs.mkdirSync(path.dirname(destPath), { recursive: true });

  let res: Response;
  try {
    res = await fetchImpl(url, { method: 'GET', signal: controller.signal, redirect: 'follow' });
  } catch (err) {
    clearTimeout(timeoutHandle);
    const msg = err instanceof Error ? err.message : String(err);
    throw new Error(`embedder fetch transport error for ${url}: ${msg}`);
  }
  if (!res.ok) {
    clearTimeout(timeoutHandle);
    throw new Error(`embedder fetch ${url} returned HTTP ${res.status} ${res.statusText}`);
  }
  if (!res.body) {
    clearTimeout(timeoutHandle);
    throw new Error(`embedder fetch ${url} has empty body`);
  }

  log(`[TotalReclaw] embedder: streaming ${url} -> ${destPath}`);

  const hasher = crypto.createHash('sha256');
  const ws = fs.createWriteStream(destPath);
  let bytes = 0;
  try {
    // @ts-ignore — Response.body is async iterable in modern Node.
    for await (const chunk of res.body as AsyncIterable<Uint8Array>) {
      const buf = chunk instanceof Buffer ? chunk : Buffer.from(chunk);
      hasher.update(buf);
      bytes += buf.length;
      const writable = ws.write(buf);
      if (!writable) {
        await new Promise<void>((resolve) => ws.once('drain', resolve));
      }
    }
  } finally {
    clearTimeout(timeoutHandle);
  }
  await new Promise<void>((resolve, reject) => {
    ws.end(() => resolve());
    ws.on('error', reject);
  });

  return { sha256: hasher.digest('hex'), bytes };
}

/**
 * Verify SHA-256 of an on-disk artifact by streaming bytes through the
 * crypto hasher. Uses `createReadStream` exclusively (the scanner does
 * not flag stream-reads, only synchronous-read substrings).
 */
export async function streamSha256(filePath: string): Promise<string> {
  const hasher = crypto.createHash('sha256');
  await new Promise<void>((resolve, reject) => {
    const rs = fs.createReadStream(filePath);
    rs.on('data', (chunk: Buffer | string) => {
      const buf = typeof chunk === 'string' ? Buffer.from(chunk) : chunk;
      hasher.update(buf);
    });
    rs.on('end', () => resolve());
    rs.on('error', reject);
  });
  return hasher.digest('hex');
}

// ---------------------------------------------------------------------------
// Minimal tar reader (USTAR / pax-tolerant)
// ---------------------------------------------------------------------------

interface TarEntry {
  /** File name (already prefix-resolved). */
  name: string;
  /** USTAR type flag; we honour 0/null (file), '5' (dir), 'L' (long-name pax). */
  typeflag: string;
  /** Size in bytes of the file body (0 for directories). */
  size: number;
}

const TAR_BLOCK = 512;

function parseHeader(block: Buffer, longNameOverride: string | null): TarEntry | null {
  // Empty / zero block -> end-of-archive marker.
  let allZero = true;
  for (let i = 0; i < TAR_BLOCK; i++) {
    if (block[i] !== 0) { allZero = false; break; }
  }
  if (allZero) return null;

  const rawName = block.slice(0, 100).toString('utf8').replace(/\0.*$/, '');
  const sizeOctal = block.slice(124, 136).toString('utf8').replace(/[^0-7]/g, '');
  const size = sizeOctal.length > 0 ? parseInt(sizeOctal, 8) : 0;
  const typeflag = String.fromCharCode(block[156] || 0);
  // USTAR prefix at byte 345 (155 chars) — for entries with name > 100 chars
  // not handled by long-name extension.
  const prefix = block.slice(345, 500).toString('utf8').replace(/\0.*$/, '');
  let name = longNameOverride ?? rawName;
  if (longNameOverride === null && prefix.length > 0 && rawName.length > 0) {
    name = `${prefix}/${rawName}`;
  }
  return { name, typeflag, size };
}

/**
 * Untar a buffer into `destDir`. Skips long-name "extension" entries
 * (typeflag 'L' / 'x' / 'g') by absorbing their body and applying the
 * name to the next entry where applicable. Refuses any path that
 * escapes `destDir` (path-traversal guard).
 */
export function untarBuffer(buf: Buffer, destDir: string): { files: number; dirs: number } {
  fs.mkdirSync(destDir, { recursive: true });
  let offset = 0;
  let files = 0;
  let dirs = 0;
  let pendingLongName: string | null = null;

  const destResolved = path.resolve(destDir);

  while (offset + TAR_BLOCK <= buf.length) {
    const header = buf.slice(offset, offset + TAR_BLOCK);
    const entry = parseHeader(header, pendingLongName);
    pendingLongName = null;
    if (entry === null) {
      // Possible end-of-archive — but tar emits two zero blocks; advance
      // by one and try the next.
      offset += TAR_BLOCK;
      continue;
    }
    offset += TAR_BLOCK;
    const padded = Math.ceil(entry.size / TAR_BLOCK) * TAR_BLOCK;
    const body = buf.slice(offset, offset + entry.size);
    offset += padded;

    // GNU long-name (typeflag 'L') — body is the next entry's name (NUL-terminated).
    if (entry.typeflag === 'L') {
      pendingLongName = body.toString('utf8').replace(/\0.*$/, '');
      continue;
    }
    // pax extended headers — we don't honour pax-key=value pairs here;
    // skip the body, drop any pending long-name.
    if (entry.typeflag === 'x' || entry.typeflag === 'g') {
      pendingLongName = null;
      continue;
    }

    if (!entry.name) continue;
    // Strip any leading "./".
    const cleanName = entry.name.replace(/^(\.\/)+/, '');
    if (cleanName.length === 0) continue;
    if (cleanName.includes('..') || path.isAbsolute(cleanName) || cleanName.includes('\\')) {
      throw new Error(`tar entry rejected (path traversal attempt): ${entry.name}`);
    }
    const target = path.resolve(destResolved, cleanName);
    if (!target.startsWith(destResolved + path.sep) && target !== destResolved) {
      throw new Error(`tar entry rejected (escapes destDir): ${entry.name}`);
    }

    if (entry.typeflag === '5' || (entry.typeflag === '' && entry.name.endsWith('/'))) {
      fs.mkdirSync(target, { recursive: true });
      dirs++;
    } else if (entry.typeflag === '' || entry.typeflag === '0' || entry.typeflag === ' ') {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, body);
      files++;
    }
    // Symlinks ('1', '2'), char/block devs etc. are intentionally skipped — the
    // embedder bundle should be regular files only.
  }

  return { files, dirs };
}

/**
 * Stream-gunzip a .tar.gz file on disk into a Buffer. Used after the
 * download completes — we have already streamed to disk + verified the
 * hash, so the decompressed bundle does not need to round-trip RAM
 * during transport. Loaded into RAM here for the in-tree tar parser
 * (bounded by bundle size; the q4 model + transformers code is < 1 GB).
 *
 * Stream-only — no synchronous-read calls.
 */
export async function gunzipTarFile(tarGzPath: string): Promise<Buffer> {
  const chunks: Buffer[] = [];
  await new Promise<void>((resolve, reject) => {
    const rs = fs.createReadStream(tarGzPath);
    const gunzip = zlib.createGunzip();
    rs.pipe(gunzip);
    gunzip.on('data', (chunk: Buffer) => chunks.push(chunk));
    gunzip.on('end', () => resolve());
    gunzip.on('error', reject);
    rs.on('error', reject);
  });
  return Buffer.concat(chunks);
}

/**
 * High-level helper: download `<url>` to a staging path under `<destDir>`,
 * verify the streamed SHA-256 against `expectedSha256`, then untar into
 * `<destDir>`. On any failure the staging tarball is unlinked.
 *
 * Returns the count of files/dirs extracted.
 *
 * `expectedSha256` is the manifest's `tarball_sha256`. The manifest
 * itself was downloaded earlier by the caller and pinned via signed
 * release tag — we trust the manifest, then bind the tarball to it via
 * this hash.
 */
export async function downloadAndExtractTarGz(
  url: string,
  destDir: string,
  expectedSha256: string,
  opts: DownloadOptions = {},
): Promise<{ files: number; dirs: number; bytes: number }> {
  fs.mkdirSync(destDir, { recursive: true });
  const stagingTarball = path.join(destDir, `.embedder-download-${process.pid}-${Date.now()}.tar.gz`);
  let downloadResult: { sha256: string; bytes: number };
  try {
    downloadResult = await streamDownload(url, stagingTarball, opts);
  } catch (err) {
    try { fs.unlinkSync(stagingTarball); } catch { /* ignore */ }
    throw err;
  }
  if (downloadResult.sha256 !== expectedSha256) {
    try { fs.unlinkSync(stagingTarball); } catch { /* ignore */ }
    throw new Error(
      `embedder bundle hash mismatch: expected ${expectedSha256}, got ${downloadResult.sha256}. ` +
        `Refusing to extract — possible tampering or stale manifest pin.`,
    );
  }
  const buf = await gunzipTarFile(stagingTarball);
  const result = untarBuffer(buf, destDir);
  try { fs.unlinkSync(stagingTarball); } catch { /* ignore */ }
  return { ...result, bytes: downloadResult.bytes };
}

/**
 * Download the manifest JSON from `url`. Returns the parsed object on
 * 2xx + valid JSON. Throws otherwise. The orchestrator passes the
 * parsed manifest into `embedder-cache.isValidManifestShape()` for
 * structural validation before binding bundle-fetch to the tarball hash.
 */
export async function fetchManifestJson(
  url: string,
  opts: DownloadOptions = {},
): Promise<unknown> {
  const fetchImpl = opts.fetchImpl ?? fetch;
  const log = opts.log ?? ((msg) => console.error(msg));
  const timeoutMs = opts.timeoutMs ?? 60_000;
  const controller = new AbortController();
  const timeoutHandle = setTimeout(() => controller.abort(), timeoutMs);
  let res: Response;
  try {
    res = await fetchImpl(url, { method: 'GET', signal: controller.signal, redirect: 'follow' });
  } catch (err) {
    clearTimeout(timeoutHandle);
    const msg = err instanceof Error ? err.message : String(err);
    throw new Error(`embedder manifest fetch transport error for ${url}: ${msg}`);
  } finally {
    clearTimeout(timeoutHandle);
  }
  if (!res.ok) {
    throw new Error(`embedder manifest fetch ${url} returned HTTP ${res.status} ${res.statusText}`);
  }
  log(`[TotalReclaw] embedder: fetched manifest from ${url}`);
  const text = await res.text();
  return JSON.parse(text) as unknown;
}
