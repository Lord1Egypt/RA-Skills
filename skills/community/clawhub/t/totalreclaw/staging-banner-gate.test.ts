/**
 * staging-banner-gate.test.ts (3.3.12-rc.1, F-flip rev)
 *
 * Pins the banner-emit invariant after the F flip (production = default for
 * BOTH stable and RC; staging is opt-in via TOTALRECLAW_SERVER_URL).
 *
 * Pre-flip semantics (3.3.4-rc.1):
 *   - Source default = staging. Banner fired when `serverUrl` resolved to
 *     api-staging.totalreclaw.xyz AND user did NOT override the env var.
 *   - The intent was: warn QA they were on staging by default, suppress the
 *     warning when an operator explicitly pinned a custom URL.
 *
 * Post-flip semantics (3.3.12-rc.1):
 *   - Source default = production. The ONLY way `serverUrl` resolves to
 *     api-staging.totalreclaw.xyz is via an explicit env override (or, as a
 *     defensive case, a broken artifact that accidentally bound to staging).
 *   - The banner SHOULD fire whenever staging is bound, regardless of whether
 *     the user "overrode" the default — the user benefits from the warning.
 *   - When `serverUrl` is anything else (production default, or a custom URL
 *     like a self-hosted relay), the banner is permanently suppressed for
 *     this gateway-process lifetime.
 *
 * The lifecycle invariant (build → consume → flag flip) is preserved from the
 * 3.3.4-rc.1 fix. `consumeBannerForPrepend()` flips the flag only once a
 * return path actually delivers the block.
 *
 * The test re-implements the helper inline because the helper is a closure
 * over hook-local state in index.ts.
 */

let passed = 0;
let failed = 0;
function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) { console.log(`ok ${n} - ${name}`); passed++; }
  else { console.log(`not ok ${n} - ${name}`); failed++; }
}

function simulateBannerLifecycle(opts: {
  serverUrl: string;
  prependContextPathTaken: boolean;
}): { stagingBannerShown: boolean; emittedBlock: string } {
  let stagingBannerShown = false;
  let stagingBannerBlock = '';

  // Simulate the before_agent_start prologue (post-F-flip semantics).
  if (!stagingBannerShown) {
    const usingStaging = opts.serverUrl.includes('api-staging.totalreclaw.xyz');
    if (usingStaging) {
      stagingBannerBlock = '## staging-banner';
      // Critical: do NOT flip stagingBannerShown here.
    } else {
      // Production default OR custom URL — never fire this lifetime.
      stagingBannerShown = true;
    }
  }

  const consumeBannerForPrepend = (): string => {
    if (stagingBannerBlock === '') return '';
    stagingBannerShown = true;
    return stagingBannerBlock;
  };

  let emittedBlock = '';
  if (opts.prependContextPathTaken) {
    emittedBlock = consumeBannerForPrepend();
  }

  return { stagingBannerShown, emittedBlock };
}

// ---------------------------------------------------------------------------
// Test 1: production default + prepend path -> NO banner, flag flipped to
// permanently suppress. (Both stable and RC ship this default post-F-flip.)
// ---------------------------------------------------------------------------

{
  const r = simulateBannerLifecycle({
    serverUrl: 'https://api.totalreclaw.xyz',
    prependContextPathTaken: true,
  });
  assert(r.emittedBlock === '', 'production default: no banner emitted');
  assert(r.stagingBannerShown === true, 'production default: flag flipped to suppress');
}

// ---------------------------------------------------------------------------
// Test 2: staging via env override + prepend path -> banner emitted, flag
// flipped. (Staging is now opt-in; if the user opted in, warn them.)
// ---------------------------------------------------------------------------

{
  const r = simulateBannerLifecycle({
    serverUrl: 'https://api-staging.totalreclaw.xyz',
    prependContextPathTaken: true,
  });
  assert(r.emittedBlock === '## staging-banner', 'staging override: banner emitted');
  assert(r.stagingBannerShown === true, 'staging override: flag flips on emit');
}

// ---------------------------------------------------------------------------
// Test 3: staging via env override + RETURN-UNDEFINED path -> banner NOT
// emitted, flag NOT flipped (next before_agent_start can retry).
//
// Preserves the 3.3.4-rc.1 lifecycle fix: build does not flip the flag;
// only consume does.
// ---------------------------------------------------------------------------

{
  const r = simulateBannerLifecycle({
    serverUrl: 'https://api-staging.totalreclaw.xyz',
    prependContextPathTaken: false,
  });
  assert(r.emittedBlock === '', 'staging + return-undefined: nothing emitted');
  assert(
    r.stagingBannerShown === false,
    'staging + return-undefined: flag UNflipped — next call retries',
  );
}

// ---------------------------------------------------------------------------
// Test 4: custom self-hosted URL -> never builds banner, flag flipped to
// permanently suppress. (Operator pinned their own relay.)
// ---------------------------------------------------------------------------

{
  const r = simulateBannerLifecycle({
    serverUrl: 'https://relay.example.com',
    prependContextPathTaken: true,
  });
  assert(r.emittedBlock === '', 'custom URL: no banner emitted');
  assert(r.stagingBannerShown === true, 'custom URL: flag flipped to suppress');
}

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
}
console.log('\nALL TESTS PASSED');
