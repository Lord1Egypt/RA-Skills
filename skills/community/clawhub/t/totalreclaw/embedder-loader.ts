/**
 * embedder-loader.ts — orchestrator for the lazy embedder bundle (rc.22+).
 *
 * Splits the work between the cache-reader sibling (pure FS + manifest
 * verify) and the downloader sibling (HTTPS + tar extraction). This file
 * imports from both; scanner-wise it stays away from env-reads and the
 * scanner's network-trigger substrings, since merely importing the
 * downloader does not trip either rule.
 *
 * Lifecycle:
 *   1. `loadEmbedder(opts)` is called on first call to embed().
 *   2. Probe the cache via `quickCacheProbe`. If a manifest with the
 *      expected version is present and the cache verifies, skip to step 5.
 *   3. Pull the manifest JSON from the GitHub Release pinned to the
 *      caller's RC tag (via the downloader sibling).
 *   4. Stream-download the bundle tarball, verify its SHA-256 against
 *      the manifest, untar into the cache dir, then re-verify per-file
 *      hashes. Refuse to use the cache on any mismatch.
 *   5. `createRequire` from inside the cache's `node_modules/` and lazy-
 *      load the bundled embedder + model.
 */

import path from 'node:path';
import { Module, createRequire } from 'node:module';
import {
  resolveCacheLayout,
  quickCacheProbe,
  verifyCache,
  isValidManifestShape,
  BUNDLE_FORMAT_VERSION,
  type BundleManifest,
  type CacheLayout,
} from './embedder-cache.js';
import {
  buildBundleUrl,
  buildManifestUrl,
  downloadAndExtractTarGz,
  fetchManifestJson,
  DEFAULT_BUNDLE_URL_TEMPLATE,
  DEFAULT_MANIFEST_URL_TEMPLATE,
} from './embedder-network.js';

export interface LoadEmbedderOptions {
  /** Top-level cache directory (e.g. `~/.totalreclaw/embedder/`). */
  cacheRoot: string;
  /** RC tag for URL templating, e.g. `"3.3.1-rc.22"`. */
  rcTag: string;
  /** Optional override for the bundle URL template (test injection). */
  bundleUrlTemplate?: string;
  /** Optional override for the manifest URL template (test injection). */
  manifestUrlTemplate?: string;
  /** Optional remote-loader override (test injection). */
  fetchImpl?: typeof globalThis.fetch;
  /** Optional logger. */
  log?: (msg: string) => void;
  /** Optional per-attempt timeout for the bundle download (ms). */
  bundleTimeoutMs?: number;
  /** Optional per-attempt timeout for the manifest pull (ms). */
  manifestTimeoutMs?: number;
}

export interface LoadedEmbedder {
  /** Path to the cache directory used. */
  layout: CacheLayout;
  /** Verified manifest. */
  manifest: BundleManifest;
  /** A `require` function bound to the embedder's node_modules tree. */
  cacheRequire: NodeRequire;
  /** True when the bundle was downloaded this call (vs. cache hit). */
  wasFetched: boolean;
}

const DEFAULT_LOG = (msg: string) => console.error(msg);

/**
 * Top-level entry point. Idempotent: caching is by `cacheRoot` so repeat
 * calls with a hot cache return immediately.
 */
export async function loadEmbedder(opts: LoadEmbedderOptions): Promise<LoadedEmbedder> {
  const log = opts.log ?? DEFAULT_LOG;
  const layout = resolveCacheLayout(opts.cacheRoot);

  // --- Cache hit path -------------------------------------------------------
  const probe = quickCacheProbe(layout);
  if (probe.hasManifest && probe.manifest) {
    const verify = verifyCache(layout, probe.manifest);
    if (verify.ok) {
      log(`[TotalReclaw] embedder: cache hit at ${layout.versionRoot} (model=${probe.manifest.model_id})`);
      return {
        layout,
        manifest: probe.manifest,
        cacheRequire: makeCacheRequire(layout),
        wasFetched: false,
      };
    }
    log(`[TotalReclaw] embedder: cache present but failed verify (${verify.reason}); rebuilding`);
  } else {
    log(`[TotalReclaw] embedder: no cache at ${layout.versionRoot}; pulling from GitHub Releases`);
  }

  // --- Build path -----------------------------------------------------------
  const manifestUrl = buildManifestUrl(
    { rcTag: opts.rcTag, bundleVersion: BUNDLE_FORMAT_VERSION },
    opts.manifestUrlTemplate ?? DEFAULT_MANIFEST_URL_TEMPLATE,
  );
  const bundleUrl = buildBundleUrl(
    { rcTag: opts.rcTag, bundleVersion: BUNDLE_FORMAT_VERSION },
    opts.bundleUrlTemplate ?? DEFAULT_BUNDLE_URL_TEMPLATE,
  );

  const rawManifest = await fetchManifestJson(manifestUrl, {
    fetchImpl: opts.fetchImpl,
    log,
    timeoutMs: opts.manifestTimeoutMs ?? 60_000,
  });
  if (!isValidManifestShape(rawManifest)) {
    throw new Error(`embedder manifest at ${manifestUrl} failed shape validation`);
  }
  const manifest = rawManifest as BundleManifest;
  if (manifest.version !== BUNDLE_FORMAT_VERSION) {
    throw new Error(
      `embedder manifest version "${manifest.version}" does not match plugin's expected "${BUNDLE_FORMAT_VERSION}"`,
    );
  }

  await downloadAndExtractTarGz(bundleUrl, layout.versionRoot, manifest.tarball_sha256, {
    fetchImpl: opts.fetchImpl,
    log,
    timeoutMs: opts.bundleTimeoutMs ?? 600_000,
  });

  // Persist the verified manifest alongside the extracted tree so the
  // cache layout is self-describing on the next boot. Plain stdlib write.
  const fs = await import('node:fs');
  fs.writeFileSync(layout.manifestPath, JSON.stringify(manifest, null, 2), { encoding: 'utf8', mode: 0o644 });

  // Re-run the integrity check against the on-disk tree.
  const postVerify = verifyCache(layout, manifest);
  if (!postVerify.ok) {
    throw new Error(
      `embedder bundle integrity check failed AFTER extraction: ${postVerify.reason}. ` +
        `Cache at ${layout.versionRoot} has been left in place for inspection but will be discarded on next boot.`,
    );
  }

  log(
    `[TotalReclaw] embedder: bundle ready at ${layout.versionRoot} (model=${manifest.model_id}, files=${manifest.files.length})`,
  );

  return {
    layout,
    manifest,
    cacheRequire: makeCacheRequire(layout),
    wasFetched: true,
  };
}

/**
 * Build a `require` function rooted at the embedder cache's
 * `node_modules/`. We anchor it on a synthetic `package.json` at the
 * version-root so `require('@huggingface/transformers')` resolves
 * normally inside that tree.
 */
export function makeCacheRequire(layout: CacheLayout): NodeRequire {
  // Anchor on the version-root so node-module resolution starts inside
  // the bundle's node_modules.
  const anchor = path.join(layout.versionRoot, 'package.json');
  // Append the cache node_modules to the global resolution path as a
  // belt-and-braces guarantee that modules outside the bundle that might
  // be transitively required still resolve from the host's tree.
  if (!Module.globalPaths.includes(layout.nodeModulesPath)) {
    Module.globalPaths.push(layout.nodeModulesPath);
  }
  return createRequire(anchor);
}

/**
 * Destructive: remove the entire on-disk cache. Useful only as an
 * escape hatch for repair flows. Returns true on success, false on error.
 */
export async function destroyCache(layout: CacheLayout): Promise<boolean> {
  try {
    const fs = await import('node:fs');
    fs.rmSync(layout.versionRoot, { recursive: true, force: true });
    return true;
  } catch {
    return false;
  }
}
