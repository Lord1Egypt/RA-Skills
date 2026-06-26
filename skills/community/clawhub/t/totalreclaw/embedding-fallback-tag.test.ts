/**
 * embedding-fallback-tag.test.ts (3.3.4-rc.1)
 *
 * Asserts the embedder runtime config has a fallback `rcTag` that
 * resolves to a real GitHub Release.
 *
 * Bug: 3.3.3-rc.1 used the literal string `'0.0.0-dev'` as the
 * fallback when `readPluginVersion()` returned null. That URL is
 * `https://github.com/p-diogo/totalreclaw/releases/download/v0.0.0-dev/...`
 * which 404s. QA on 3.3.3-rc.1 (Pedro 2026-04-30) caught this because
 * the cascade-cause (broken `readPluginVersion()` resolution) made the
 * fallback fire on every cold start, so `prefetchEmbedderBundle` failed
 * silently and the first `generateEmbedding()` retried the network.
 *
 * Fix: the fallback now points at `LAST_KNOWN_GOOD_RC_TAG` — pinned to
 * the most recent RC with a published bundle at fix-time.
 *
 * What this test pins:
 *   - The fallback tag matches `^[0-9]+\.[0-9]+\.[0-9]+-rc\.[0-9]+$`
 *     (a real RC tag, not a dev placeholder).
 *   - `buildBundleUrl()` + the fallback tag form a URL whose origin is
 *     `https://github.com/p-diogo/totalreclaw/releases/download/v<tag>/...`
 *     — i.e. the publish workflow's canonical layout.
 */

import { configureEmbedder } from './embedding.js';
import { buildBundleUrl, buildManifestUrl } from './embedder-network.js';

let passed = 0;
let failed = 0;
function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) { console.log(`ok ${n} - ${name}`); passed++; }
  else { console.log(`not ok ${n} - ${name}`); failed++; }
}

// ---------------------------------------------------------------------------
// Fallback tag shape — semver -rc.N or PEP-440 rcN, never a placeholder.
// ---------------------------------------------------------------------------

// We can't import the constant directly (it's module-private). Read the
// module source to assert the shape — same approach as scanner / drift
// guards. This keeps the constant private to embedding.ts while letting
// the test pin the invariant.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const embeddingSrc = fs.readFileSync(path.join(here, 'embedding.ts'), 'utf-8');

const constMatch = embeddingSrc.match(/LAST_KNOWN_GOOD_RC_TAG\s*=\s*'([^']+)'/);
assert(
  constMatch !== null,
  'embedding.ts: LAST_KNOWN_GOOD_RC_TAG constant present',
);
const tag = constMatch?.[1] ?? '';
assert(
  tag.length > 0,
  'embedding.ts: LAST_KNOWN_GOOD_RC_TAG is non-empty',
);
assert(
  /^\d+\.\d+\.\d+-rc\.\d+$/.test(tag),
  `embedding.ts: LAST_KNOWN_GOOD_RC_TAG ("${tag}") matches a real RC tag (^x.y.z-rc.N$, not a placeholder)`,
);
assert(
  tag !== '0.0.0-dev',
  `embedding.ts: fallback tag is NOT the broken placeholder "0.0.0-dev" (3.3.3-rc.1 regression)`,
);

// ---------------------------------------------------------------------------
// URL shape — bundle + manifest URLs use the GitHub-Releases canonical layout.
// ---------------------------------------------------------------------------

{
  const bundleUrl = buildBundleUrl({ rcTag: tag, bundleVersion: 'v1' });
  const manifestUrl = buildManifestUrl({ rcTag: tag, bundleVersion: 'v1' });
  const expectedPrefix = `https://github.com/p-diogo/totalreclaw/releases/download/v${tag}/`;
  assert(
    bundleUrl.startsWith(expectedPrefix),
    'buildBundleUrl: prefix matches GitHub Releases canonical layout',
  );
  assert(
    manifestUrl.startsWith(expectedPrefix),
    'buildManifestUrl: prefix matches GitHub Releases canonical layout',
  );
  assert(
    bundleUrl.endsWith('/embedder-v1.tar.gz'),
    'buildBundleUrl: emits embedder-v1.tar.gz',
  );
  assert(
    manifestUrl.endsWith('/embedder-v1.manifest.json'),
    'buildManifestUrl: emits embedder-v1.manifest.json',
  );
}

// ---------------------------------------------------------------------------
// configureEmbedder is callable + accepts a real RC tag — pure smoke.
// ---------------------------------------------------------------------------

{
  let crashed = false;
  try {
    configureEmbedder({ cacheRoot: '/tmp/__never_used__', rcTag: '3.3.4-rc.1' });
  } catch {
    crashed = true;
  }
  assert(!crashed, 'configureEmbedder: accepts a real RC tag without throwing');
}

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
}
console.log('\nALL TESTS PASSED');
