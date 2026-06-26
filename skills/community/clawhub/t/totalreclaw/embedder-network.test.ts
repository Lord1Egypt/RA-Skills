// scanner-sim: allow — test exercises the lazy-bundle fetch + extract path with a mocked global fetch and reads back extracted files via fs.readFileSync; not shipped in npm package (see files allowlist in package.json).
/**
 * embedder-network.test.ts — regressions for the lazy-embedder retrieval
 * layer shipped in 3.3.1-rc.22.
 *
 * Failure mode this guards against:
 *   rc.21 baseline ships `@huggingface/transformers` + `onnxruntime-node`
 *   in the plugin's npm `dependencies`, which OOM-kills the OpenClaw
 *   gateway during `openclaw plugins install` on small VPS hosts. The
 *   rc.22 fix moves those bundles into a GitHub-Releases tarball that
 *   the plugin streams in on first use. This test suite drives the
 *   fetch + verify + extract path with a mocked `fetch` so it runs in
 *   CI without network access. On the rc.21 baseline the file imports
 *   below fail (module not found), hard-failing this test in the
 *   expected way — proof that the file is genuinely new.
 *
 * Coverage:
 *   1. URL templating — `{rcTag}` + `{bundleVersion}` placeholders are
 *      substituted with URL-encoded values.
 *   2. Hash mismatch — `downloadAndExtractTarGz` refuses to extract when
 *      the streamed bytes hash differently from the manifest's
 *      `tarball_sha256` (security guarantee against silent tampering).
 *   3. Happy path — a hash-matching tarball gets extracted; output files
 *      land at the expected locations.
 *   4. Tar untar — the in-tree minimal USTAR reader correctly handles
 *      regular files and rejects path-traversal entries.
 *
 * Run with: `npx tsx embedder-network.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';

import {
  buildBundleUrl,
  buildManifestUrl,
  downloadAndExtractTarGz,
  fetchManifestJson,
  untarBuffer,
  streamSha256,
} from './embedder-network.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function mkTmpRoot(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-embedder-network-'));
}

function rmrf(p: string): void {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch { /* ignore */ }
}

// ---------------------------------------------------------------------------
// Tar writer (matches the reader in embedder-network.ts).
// Mirrors the production `scripts/build-embedder-bundle.mjs` output format.
// ---------------------------------------------------------------------------

function tarHeader(name: string, size: number): Buffer {
  const header = Buffer.alloc(512, 0);
  header.write(name, 0, 100, 'utf8');
  header.write('0000644 \0', 100, 8, 'utf8');
  header.write('0000000\0', 108, 8, 'utf8');
  header.write('0000000\0', 116, 8, 'utf8');
  header.write(size.toString(8).padStart(11, '0') + ' ', 124, 12, 'utf8');
  header.write(Math.floor(Date.now() / 1000).toString(8).padStart(11, '0') + ' ', 136, 12, 'utf8');
  header.write('        ', 148, 8, 'utf8'); // checksum placeholder
  header[156] = '0'.charCodeAt(0);
  header.write('ustar  \0', 257, 8, 'utf8');
  let sum = 0;
  for (let i = 0; i < 512; i++) sum += header[i];
  header.write(sum.toString(8).padStart(6, '0') + '\0 ', 148, 8, 'utf8');
  return header;
}

function makeTarBuffer(entries: Array<{ name: string; content: Buffer }>): Buffer {
  const chunks: Buffer[] = [];
  for (const { name, content } of entries) {
    chunks.push(tarHeader(name, content.length));
    chunks.push(content);
    const pad = Math.ceil(content.length / 512) * 512 - content.length;
    if (pad > 0) chunks.push(Buffer.alloc(pad, 0));
  }
  chunks.push(Buffer.alloc(1024, 0));
  return Buffer.concat(chunks);
}

function makeTarGz(entries: Array<{ name: string; content: Buffer }>): Buffer {
  const tar = makeTarBuffer(entries);
  return zlib.gzipSync(tar, { level: 6 });
}

function sha256(buf: Buffer): string {
  return crypto.createHash('sha256').update(buf).digest('hex');
}

// ---------------------------------------------------------------------------
// Fetch mock — feeds a Buffer body as a streaming Response.
// ---------------------------------------------------------------------------

function makeFetchMock(routes: Map<string, Buffer | string>): typeof fetch {
  return (async (url: string | URL | Request, _init?: RequestInit) => {
    const u = typeof url === 'string' ? url : (url as URL).toString();
    const body = routes.get(u);
    if (body === undefined) {
      return new Response(null, { status: 404, statusText: 'Not Found' });
    }
    if (typeof body === 'string') {
      return new Response(body, { status: 200 });
    }
    return new Response(body, {
      status: 200,
      headers: { 'content-type': 'application/octet-stream', 'content-length': String(body.length) },
    });
  }) as typeof fetch;
}

// ---------------------------------------------------------------------------
// 1. URL templating
// ---------------------------------------------------------------------------
{
  console.log('# URL templating');
  const u = buildBundleUrl({ rcTag: '3.3.1-rc.22', bundleVersion: 'v1' });
  assert(
    u === 'https://github.com/p-diogo/totalreclaw/releases/download/v3.3.1-rc.22/embedder-v1.tar.gz',
    'default bundle URL substitutes rcTag + bundleVersion',
  );
  const m = buildManifestUrl({ rcTag: '3.3.1-rc.22', bundleVersion: 'v1' });
  assert(
    m === 'https://github.com/p-diogo/totalreclaw/releases/download/v3.3.1-rc.22/embedder-v1.manifest.json',
    'default manifest URL substitutes both placeholders',
  );
  const overridden = buildBundleUrl(
    { rcTag: 'X', bundleVersion: 'v9' },
    'https://mirror.example.com/{rcTag}/foo-{bundleVersion}.tar.gz',
  );
  assert(overridden === 'https://mirror.example.com/X/foo-v9.tar.gz', 'custom template applied');
}

// ---------------------------------------------------------------------------
// 2. Hash mismatch refuses to extract
// ---------------------------------------------------------------------------
{
  console.log('# Hash mismatch refuses extraction (security guarantee)');
  const root = mkTmpRoot();
  try {
    const tarGz = makeTarGz([{ name: 'foo.txt', content: Buffer.from('hello\n') }]);
    const fakeUrl = 'https://example.com/embedder-v1.tar.gz';
    const fetchImpl = makeFetchMock(new Map<string, Buffer | string>([[fakeUrl, tarGz]]));
    let threw = false;
    try {
      await downloadAndExtractTarGz(fakeUrl, root, /* expected */ 'd'.repeat(64), {
        fetchImpl,
        log: () => undefined,
      });
    } catch (err) {
      threw = true;
      assert(/hash mismatch/.test(String(err)), 'error message mentions hash mismatch');
    }
    assert(threw === true, 'downloadAndExtractTarGz throws on hash mismatch');
    // After failure, the staging tarball should be cleaned up.
    const lingering = fs.readdirSync(root).filter((n) => n.startsWith('.embedder-download-'));
    assert(lingering.length === 0, 'failed download cleans up staging tarball');
    // No `foo.txt` extracted on hash failure.
    assert(!fs.existsSync(path.join(root, 'foo.txt')), 'extraction did NOT proceed on hash mismatch');
  } finally {
    rmrf(root);
  }
}

// ---------------------------------------------------------------------------
// 3. Happy path — hash matches → extraction proceeds
// ---------------------------------------------------------------------------
{
  console.log('# Happy path — extract on matching hash');
  const root = mkTmpRoot();
  try {
    const tarGz = makeTarGz([
      { name: 'node_modules/@huggingface/transformers/index.js', content: Buffer.from('console.log("OK");\n') },
      { name: 'node_modules/@huggingface/transformers/package.json', content: Buffer.from('{"name":"@huggingface/transformers"}') },
      { name: 'model/config.json', content: Buffer.from('{"dim":640}') },
    ]);
    const expectedSha = sha256(tarGz);
    const fakeUrl = 'https://example.com/embedder-v1.tar.gz';
    const fetchImpl = makeFetchMock(new Map<string, Buffer | string>([[fakeUrl, tarGz]]));
    const result = await downloadAndExtractTarGz(fakeUrl, root, expectedSha, {
      fetchImpl,
      log: () => undefined,
    });
    assert(result.files === 3, 'extracts the 3 files in the bundle');
    assert(
      fs.existsSync(path.join(root, 'node_modules/@huggingface/transformers/index.js')),
      'transformers/index.js extracted',
    );
    assert(
      fs.existsSync(path.join(root, 'model/config.json')),
      'model/config.json extracted',
    );
    const back = fs.readFileSync(path.join(root, 'node_modules/@huggingface/transformers/index.js'), 'utf8');
    assert(back === 'console.log("OK");\n', 'extracted file matches the input bytes');
  } finally {
    rmrf(root);
  }
}

// ---------------------------------------------------------------------------
// 4. Tar reader rejects path-traversal entries
// ---------------------------------------------------------------------------
{
  console.log('# Tar reader rejects path-traversal entries');
  const root = mkTmpRoot();
  try {
    const tarBuf = makeTarBuffer([
      { name: '../escape.txt', content: Buffer.from('attempt') },
    ]);
    let threw = false;
    try {
      untarBuffer(tarBuf, root);
    } catch (err) {
      threw = true;
      assert(/path traversal|escapes/.test(String(err)), 'error mentions traversal/escapes');
    }
    assert(threw === true, 'untarBuffer rejects ../ entries');
  } finally {
    rmrf(root);
  }
}

// ---------------------------------------------------------------------------
// 5. fetchManifestJson — happy path + 404
// ---------------------------------------------------------------------------
{
  console.log('# fetchManifestJson — happy path + 404');
  const url = 'https://example.com/embedder-v1.manifest.json';
  const goodBody = JSON.stringify({ version: 'v1', model_id: 'harrier-oss-270m-q4', dimension: 640 });
  const fetchImpl = makeFetchMock(new Map<string, Buffer | string>([[url, goodBody]]));
  const parsed = await fetchManifestJson(url, { fetchImpl, log: () => undefined });
  assert(typeof parsed === 'object' && parsed !== null, 'fetchManifestJson returns parsed object');
  let threw = false;
  try {
    await fetchManifestJson('https://example.com/missing.json', {
      fetchImpl: makeFetchMock(new Map()),
      log: () => undefined,
    });
  } catch {
    threw = true;
  }
  assert(threw === true, 'fetchManifestJson throws on 404');
}

// ---------------------------------------------------------------------------
// 6. streamSha256 round-trip
// ---------------------------------------------------------------------------
{
  console.log('# streamSha256 round-trip');
  const root = mkTmpRoot();
  try {
    const file = path.join(root, 'sample.bin');
    const content = Buffer.from('the quick brown fox\n');
    fs.writeFileSync(file, content);
    const expected = sha256(content);
    const got = await streamSha256(file);
    assert(got === expected, 'streamSha256 matches buffer-hash for the same bytes');
  } finally {
    rmrf(root);
  }
}

console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) process.exit(1);
