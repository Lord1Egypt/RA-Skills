/**
 * embedder-cache.test.ts — regressions for the lazy-embedder cache layer
 * shipped in 3.3.1-rc.22. Failure mode this guards against:
 *
 * rc.21 baseline: `embedder-cache.ts` does not exist, so the plugin
 * imports `@huggingface/transformers` eagerly from npm `dependencies`,
 * which OOM-kills the OpenClaw gateway during `openclaw plugins install`
 * on small VPS hosts. This test would fail to import in rc.21 (module
 * not found), proving the file is genuinely new and gating the fix.
 *
 * Coverage:
 *   1. Manifest shape validation — a known-good manifest passes; bad
 *      shapes (missing fields, bad hash format, path-traversal entries)
 *      are rejected.
 *   2. Cache-hit path — when files match the manifest, `verifyCache`
 *      returns ok=true.
 *   3. Cache-miss paths — missing file / size mismatch / hash mismatch
 *      / wrong manifest version each fail with a useful reason.
 *   4. Layout resolution — `resolveCacheLayout('/foo')` produces the
 *      expected `<root>/v1/manifest.json` etc.
 *
 * Run with: `npx tsx embedder-cache.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';

import {
  resolveCacheLayout,
  isValidManifestShape,
  readManifest,
  verifyCache,
  quickCacheProbe,
  BUNDLE_FORMAT_VERSION,
  type BundleManifest,
} from './embedder-cache.js';

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
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-embedder-cache-'));
}

function rmrf(p: string): void {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch { /* ignore */ }
}

function sha256(buf: Buffer | string): string {
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function writeFile(absPath: string, content: string | Buffer): void {
  fs.mkdirSync(path.dirname(absPath), { recursive: true });
  fs.writeFileSync(absPath, content);
}

function fakeBundleOnDisk(versionRoot: string): { manifest: BundleManifest } {
  // Build a small synthetic bundle: one file under node_modules/, one under model/.
  const fileA = Buffer.from('console.log("transformers shim");\n', 'utf8');
  const fileB = Buffer.from(JSON.stringify({ model: 'harrier-oss-270m-q4', dtype: 'q4' }), 'utf8');
  writeFile(path.join(versionRoot, 'node_modules/@huggingface/transformers/index.js'), fileA);
  writeFile(path.join(versionRoot, 'model/config.json'), fileB);
  const manifest: BundleManifest = {
    version: BUNDLE_FORMAT_VERSION,
    model_id: 'harrier-oss-270m-q4',
    dimension: 640,
    tarball_sha256: 'a'.repeat(64),
    tarball_size_bytes: fileA.length + fileB.length,
    files: [
      {
        path: 'node_modules/@huggingface/transformers/index.js',
        sha256: sha256(fileA),
        size: fileA.length,
      },
      {
        path: 'model/config.json',
        sha256: sha256(fileB),
        size: fileB.length,
      },
    ],
  };
  writeFile(path.join(versionRoot, 'manifest.json'), JSON.stringify(manifest));
  return { manifest };
}

// ---------------------------------------------------------------------------
// 1. Layout
// ---------------------------------------------------------------------------
{
  console.log('# Cache layout resolution');
  const layout = resolveCacheLayout('/tmp/.totalreclaw/embedder');
  assert(layout.root === '/tmp/.totalreclaw/embedder', 'root resolves verbatim');
  assert(layout.versionRoot.endsWith(`/embedder/${BUNDLE_FORMAT_VERSION}`), 'versionRoot includes BUNDLE_FORMAT_VERSION subdir');
  assert(layout.manifestPath.endsWith('manifest.json'), 'manifestPath ends with manifest.json');
  assert(layout.nodeModulesPath.endsWith('node_modules'), 'nodeModulesPath ends with node_modules');
  assert(layout.modelPath.endsWith('model'), 'modelPath ends with model');
}

// ---------------------------------------------------------------------------
// 2. Manifest shape validation
// ---------------------------------------------------------------------------
{
  console.log('# Manifest shape validation');
  const good: BundleManifest = {
    version: BUNDLE_FORMAT_VERSION,
    model_id: 'harrier-oss-270m-q4',
    dimension: 640,
    tarball_sha256: 'b'.repeat(64),
    tarball_size_bytes: 12345,
    files: [{ path: 'a/b.js', sha256: 'c'.repeat(64), size: 10 }],
  };
  assert(isValidManifestShape(good) === true, 'well-formed manifest passes');

  assert(isValidManifestShape(null) === false, 'null is rejected');
  assert(isValidManifestShape({}) === false, 'empty object is rejected');
  assert(
    isValidManifestShape({ ...good, dimension: -1 }) === false,
    'negative dimension is rejected',
  );
  assert(
    isValidManifestShape({ ...good, tarball_sha256: 'short' }) === false,
    'non-hex64 tarball_sha256 is rejected',
  );
  assert(
    isValidManifestShape({ ...good, files: [{ path: '../etc/passwd', sha256: 'c'.repeat(64), size: 1 }] }) === false,
    'path-traversal entry is rejected',
  );
  assert(
    isValidManifestShape({ ...good, files: [{ path: '/abs/path', sha256: 'c'.repeat(64), size: 1 }] }) === false,
    'absolute path entry is rejected',
  );
  assert(
    isValidManifestShape({ ...good, files: [{ path: 'a\\b', sha256: 'c'.repeat(64), size: 1 }] }) === false,
    'backslash path entry is rejected',
  );
}

// ---------------------------------------------------------------------------
// 3. Cache hit
// ---------------------------------------------------------------------------
{
  console.log('# Cache hit path');
  const root = mkTmpRoot();
  try {
    const layout = resolveCacheLayout(path.join(root, 'embedder'));
    fakeBundleOnDisk(layout.versionRoot);
    const probe = quickCacheProbe(layout);
    assert(probe.hasManifest === true, 'quickCacheProbe sees the manifest');
    assert(probe.manifest !== null, 'quickCacheProbe parses the manifest');
    if (probe.manifest) {
      const verify = verifyCache(layout, probe.manifest);
      assert(verify.ok === true, 'verifyCache reports ok on intact bundle');
      assert(verify.reason === '', 'no reason on success');
    }
  } finally {
    rmrf(root);
  }
}

// ---------------------------------------------------------------------------
// 4. Cache miss — file deleted
// ---------------------------------------------------------------------------
{
  console.log('# Cache miss — file deleted');
  const root = mkTmpRoot();
  try {
    const layout = resolveCacheLayout(path.join(root, 'embedder'));
    const { manifest } = fakeBundleOnDisk(layout.versionRoot);
    fs.unlinkSync(path.join(layout.versionRoot, 'model/config.json'));
    const verify = verifyCache(layout, manifest);
    assert(verify.ok === false, 'verifyCache fails when a listed file is missing');
    assert(verify.offendingPath === 'model/config.json', 'offendingPath identifies the missing file');
  } finally {
    rmrf(root);
  }
}

// ---------------------------------------------------------------------------
// 5. Cache miss — size mismatch
// ---------------------------------------------------------------------------
{
  console.log('# Cache miss — size mismatch');
  const root = mkTmpRoot();
  try {
    const layout = resolveCacheLayout(path.join(root, 'embedder'));
    const { manifest } = fakeBundleOnDisk(layout.versionRoot);
    // Append junk to one file → size grows.
    fs.appendFileSync(path.join(layout.versionRoot, 'model/config.json'), 'X');
    const verify = verifyCache(layout, manifest);
    assert(verify.ok === false, 'verifyCache fails when a file size differs from manifest');
    assert(/size mismatch/.test(verify.reason), 'reason mentions size mismatch');
  } finally {
    rmrf(root);
  }
}

// ---------------------------------------------------------------------------
// 6. Cache miss — hash mismatch (same size)
// ---------------------------------------------------------------------------
{
  console.log('# Cache miss — hash mismatch');
  const root = mkTmpRoot();
  try {
    const layout = resolveCacheLayout(path.join(root, 'embedder'));
    const { manifest } = fakeBundleOnDisk(layout.versionRoot);
    // Replace a file's content but keep size identical.
    const targetPath = path.join(layout.versionRoot, 'node_modules/@huggingface/transformers/index.js');
    const original = fs.readFileSync(targetPath);
    const tampered = Buffer.alloc(original.length, 'X');
    fs.writeFileSync(targetPath, tampered);
    const verify = verifyCache(layout, manifest);
    assert(verify.ok === false, 'verifyCache fails on hash mismatch with matching size');
    assert(/hash mismatch/.test(verify.reason), 'reason mentions hash mismatch');
  } finally {
    rmrf(root);
  }
}

// ---------------------------------------------------------------------------
// 7. Cache miss — wrong manifest version (bundle format drift)
// ---------------------------------------------------------------------------
{
  console.log('# Cache miss — wrong manifest version');
  const root = mkTmpRoot();
  try {
    const layout = resolveCacheLayout(path.join(root, 'embedder'));
    const { manifest } = fakeBundleOnDisk(layout.versionRoot);
    const drifted: BundleManifest = { ...manifest, version: 'v2-future' };
    fs.writeFileSync(layout.manifestPath, JSON.stringify(drifted));
    const probe = quickCacheProbe(layout);
    assert(probe.hasManifest === false, 'quickCacheProbe flags the version drift as a miss');
    const verify = verifyCache(layout, drifted);
    assert(verify.ok === false, 'verifyCache rejects manifest with a drifted version field');
  } finally {
    rmrf(root);
  }
}

// ---------------------------------------------------------------------------
// 8. Manifest read — missing / malformed
// ---------------------------------------------------------------------------
{
  console.log('# Manifest read — missing / malformed');
  const root = mkTmpRoot();
  try {
    const layout = resolveCacheLayout(path.join(root, 'embedder'));
    assert(readManifest(layout) === null, 'readManifest returns null when no manifest exists');
    fs.mkdirSync(layout.versionRoot, { recursive: true });
    fs.writeFileSync(layout.manifestPath, '{ this is not json }');
    assert(readManifest(layout) === null, 'readManifest returns null on malformed JSON');
    fs.writeFileSync(layout.manifestPath, JSON.stringify({ version: 'v1' /* missing fields */ }));
    assert(readManifest(layout) === null, 'readManifest returns null when shape validation fails');
  } finally {
    rmrf(root);
  }
}

console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) process.exit(1);
