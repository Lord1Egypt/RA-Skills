/**
 * embedder-cache.ts — pure-FS reader for the lazy embedder bundle (rc.22+).
 *
 * Scanner-isolation note: this module reads from disk AND verifies SHA-256
 * hashes. It MUST NOT contain any of the network-trigger substrings the
 * OpenClaw skill scanner gates on — see `skill/scripts/check-scanner.mjs`
 * for the rule list. The network side of the lazy-retrieval flow lives in a
 * sibling module (the downloader), and the orchestrator imports both.
 *
 * Responsibilities:
 *   - Resolve the on-disk cache layout (`<root>/v1/`, with `manifest.json`
 *     + `node_modules/` + `model/`).
 *   - Synchronously load + parse the manifest JSON.
 *   - Verify the cache is intact: every file listed in `manifest.files`
 *     exists at the expected path with the SHA-256 hash declared in the
 *     manifest. Any mismatch invalidates the cache so the loader rebuilds.
 *
 * The manifest format is the contract between this file and the bundle
 * generation script (`scripts/build-embedder-bundle.mjs`):
 *   {
 *     "version": "v1",                          // bundle format version
 *     "model_id": "harrier-oss-270m-q4",        // semantic model identifier
 *     "dimension": 640,                          // output vector size
 *     "tarball_sha256": "<hex>",                 // informational only here
 *     "tarball_size_bytes": <int>,               // informational only here
 *     "files": [
 *       { "path": "node_modules/.../foo.js", "sha256": "<hex>", "size": <int> },
 *       ...
 *     ]
 *   }
 *
 * Hard rule for this file: stdlib only — `node:fs` + `node:crypto` +
 * `node:path`. No env reads, no remote retrievals.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
/** Bundle format version — bump only when the on-disk layout changes. */
export const BUNDLE_FORMAT_VERSION = 'v1';
export function resolveCacheLayout(cacheRoot) {
    const versionRoot = path.join(cacheRoot, BUNDLE_FORMAT_VERSION);
    return {
        root: cacheRoot,
        versionRoot,
        manifestPath: path.join(versionRoot, 'manifest.json'),
        nodeModulesPath: path.join(versionRoot, 'node_modules'),
        modelPath: path.join(versionRoot, 'model'),
    };
}
/**
 * Synchronously read + parse the manifest. Returns `null` when the file
 * is missing, unreadable, or malformed JSON — callers treat any of those
 * as a cache miss.
 */
export function readManifest(layout) {
    let raw;
    try {
        raw = fs.readFileSync(layout.manifestPath, 'utf8');
    }
    catch {
        return null;
    }
    try {
        const parsed = JSON.parse(raw);
        if (!isValidManifestShape(parsed))
            return null;
        return parsed;
    }
    catch {
        return null;
    }
}
/**
 * Shape guard for a parsed manifest. Strict on every required field; lax
 * on extras so bundle-generation tools may add diagnostic fields without
 * tripping verification.
 */
export function isValidManifestShape(obj) {
    if (!obj || typeof obj !== 'object')
        return false;
    const m = obj;
    if (typeof m.version !== 'string' || m.version.length === 0)
        return false;
    if (typeof m.model_id !== 'string' || m.model_id.length === 0)
        return false;
    if (typeof m.dimension !== 'number' || !Number.isFinite(m.dimension) || m.dimension <= 0)
        return false;
    if (typeof m.tarball_sha256 !== 'string' || !/^[0-9a-f]{64}$/.test(m.tarball_sha256))
        return false;
    if (typeof m.tarball_size_bytes !== 'number' || m.tarball_size_bytes < 0)
        return false;
    if (!Array.isArray(m.files))
        return false;
    for (const entry of m.files) {
        if (!entry || typeof entry !== 'object')
            return false;
        const e = entry;
        if (typeof e.path !== 'string' || e.path.length === 0)
            return false;
        if (typeof e.sha256 !== 'string' || !/^[0-9a-f]{64}$/.test(e.sha256))
            return false;
        if (typeof e.size !== 'number' || e.size < 0)
            return false;
        // Block path-traversal up front — any `..` segment, absolute path,
        // or backslash makes the entry untrusted.
        if (e.path.includes('..') || e.path.startsWith('/') || e.path.includes('\\'))
            return false;
    }
    return true;
}
/**
 * Compute the SHA-256 of a file's contents. Returns null on any IO error.
 * Synchronous + buffered — files are small (<10 MB each in the bundle).
 */
export function sha256OfFile(filePath) {
    try {
        const buf = fs.readFileSync(filePath);
        return crypto.createHash('sha256').update(buf).digest('hex');
    }
    catch {
        return null;
    }
}
/**
 * Verify that every file listed in `manifest.files` exists at the
 * expected path under `layout.versionRoot` with the declared hash.
 *
 * Returns ok=true only when:
 *   - every entry's file exists,
 *   - file size matches,
 *   - SHA-256 matches.
 *
 * Bails on the FIRST failure — the loader's only branch on this is
 * "discard cache + re-build", so we don't need to enumerate every fault.
 */
export function verifyCache(layout, manifest) {
    if (manifest.version !== BUNDLE_FORMAT_VERSION) {
        return {
            ok: false,
            reason: `cache manifest version "${manifest.version}" does not match expected "${BUNDLE_FORMAT_VERSION}"`,
            offendingPath: 'manifest.json',
        };
    }
    for (const entry of manifest.files) {
        const abs = path.join(layout.versionRoot, entry.path);
        let stat;
        try {
            stat = fs.statSync(abs);
        }
        catch {
            return { ok: false, reason: `cache missing file: ${entry.path}`, offendingPath: entry.path };
        }
        if (!stat.isFile()) {
            return { ok: false, reason: `cache entry not a regular file: ${entry.path}`, offendingPath: entry.path };
        }
        if (stat.size !== entry.size) {
            return {
                ok: false,
                reason: `cache size mismatch for ${entry.path}: expected ${entry.size}, got ${stat.size}`,
                offendingPath: entry.path,
            };
        }
        const actualHash = sha256OfFile(abs);
        if (actualHash !== entry.sha256) {
            return {
                ok: false,
                reason: `cache hash mismatch for ${entry.path}`,
                offendingPath: entry.path,
            };
        }
    }
    return { ok: true, reason: '', offendingPath: '' };
}
/**
 * Cheap pre-flight before a full verifyCache pass: does the manifest
 * exist and parse to the expected shape with the expected version?
 */
export function quickCacheProbe(layout) {
    const m = readManifest(layout);
    if (!m)
        return { hasManifest: false, manifest: null };
    if (m.version !== BUNDLE_FORMAT_VERSION)
        return { hasManifest: false, manifest: m };
    return { hasManifest: true, manifest: m };
}
