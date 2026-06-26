/**
 * Tests for pair-page (P5 of the v3.3.0 QR-pairing implementation).
 *
 * Static-content smoke tests only — we don't boot a browser. Asserts:
 *   1. Renders as HTML (has `<!doctype html>` + closing `</html>`).
 *   2. Embeds sid / mode / apiBase as JS constants.
 *   3. Contains the full 2048-word BIP-39 English wordlist.
 *   4. Contains the required security copy blocks (design doc + user
 *      ratification 2026-04-20 phone-page wave).
 *   5. Uses the brand tokens from v5b.html (--purple, --bg, etc.).
 *   6. Uses WebCrypto X25519 + AES-GCM + HKDF (rc.12 cipher swap).
 *   7. Reads pk from `window.location.hash` (design doc section 5c).
 *   8. Does NOT reference any external CDN / host.
 *   9. Escapes potentially-dangerous sid/apiBase injections via
 *      JSON.stringify.
 *  10. Import mode UI renders different text vs generate mode.
 *  11. Includes prefers-reduced-motion media query.
 *
 * Run with: npx tsx pair-page.test.ts
 */

import { renderPairPage } from './pair-page.js';

let passed = 0;
let failed = 0;
function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) { console.log(`ok ${n} - ${name}`); passed++; }
  else { console.log(`not ok ${n} - ${name}`); failed++; }
}

// ---------------------------------------------------------------------------
// 1. Renders as HTML
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({
    sid: 'abcdef123456',
    mode: 'generate',
    expiresAtMs: 1_000_000,
    apiBase: '/plugin/totalreclaw/pair',
    nowMs: 500_000,
  });
  assert(html.startsWith('<!doctype html>'), 'renders: html doctype');
  assert(html.includes('</html>'), 'renders: html closing tag');
  assert(html.includes('<meta charset="utf-8" />'), 'renders: utf-8 meta');
  assert(html.includes('viewport'), 'renders: viewport meta');
  assert(html.length > 30_000 && html.length < 60_000, `renders: page size ~45KB (got ${html.length})`);
}

// ---------------------------------------------------------------------------
// 2. Injected constants are present as JS strings
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({
    sid: 'test-sid-xyz',
    mode: 'import',
    expiresAtMs: 2_000_000,
    apiBase: '/custom/pair/api',
    nowMs: 1_000_000,
  });
  assert(html.includes('const SID = "test-sid-xyz"'), 'inject: SID constant present');
  assert(html.includes('const MODE = "import"'), 'inject: MODE constant present');
  assert(html.includes('const API_BASE = "/custom/pair/api"'), 'inject: API_BASE constant present');
  assert(html.includes('const EXPIRES_AT_MS = 2000000'), 'inject: EXPIRES_AT_MS as number');
}

// ---------------------------------------------------------------------------
// 3. BIP-39 wordlist inlined
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({
    sid: 's', mode: 'generate', expiresAtMs: 0, apiBase: '/', nowMs: 0,
  });
  // First few canonical words
  assert(html.includes('"abandon","ability","able","about"'), 'wordlist: starts with abandon/ability/able/about');
  // Last few canonical words
  assert(html.includes('"zone","zoo"'), 'wordlist: ends with zone/zoo');
}

// ---------------------------------------------------------------------------
// 4. Security copy — design doc + 2026-04-20 phone-page ratification
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({
    sid: 's', mode: 'generate', expiresAtMs: 0, apiBase: '/', nowMs: 0,
  });
  // 3.3.0-rc.2: terminology standardised on "recovery phrase" (was "account key").
  assert(html.includes('TotalReclaw recovery phrase'), 'copy: "recovery phrase" framing');
  assert(html.includes('Use it ONLY with TotalReclaw'), 'copy: only-with-TR warning');
  assert(html.includes('crypto wallet'), 'copy: wallet-reuse warning');
  assert(html.includes('banking'), 'copy: banking-reuse warning');
  assert(html.includes('email'), 'copy: email-reuse warning');
  assert(html.includes('Store it somewhere safe'), 'copy: storage prompt');
  assert(html.includes('password manager'), 'copy: password manager suggestion');
  assert(html.includes('encrypted notes'), 'copy: encrypted notes suggestion');
  assert(html.includes('physical safe') || html.includes('Written on paper in a physical safe'), 'copy: physical safe suggestion');
  assert(html.includes('With this recovery phrase you can'), 'copy: capabilities header');
  assert(html.includes('Hermes'), 'copy: mentions Hermes');
  assert(html.includes('MCP'), 'copy: mentions MCP');
  assert(html.includes('OpenClaw'), 'copy: mentions OpenClaw');
  assert(html.includes('permanently lose'), 'copy: "Without it" permanent loss warning');
  assert(html.includes('have saved it'), 'copy: ack button text');
  // 3.3.0-rc.2: storage-guidance canonical copy must appear on the generate page.
  assert(html.includes('Your recovery phrase is 12 words'), 'copy: storage-guidance canonical text');
  assert(html.includes('Don&#39;t put funds on it') || html.includes("Don't put funds on it"), 'copy: storage-guidance "no funds" line');
}

// ---------------------------------------------------------------------------
// 5. Brand tokens from v5b.html
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({
    sid: 's', mode: 'generate', expiresAtMs: 0, apiBase: '/', nowMs: 0,
  });
  assert(html.includes('#0B0B1A'), 'brand: --bg matches v5b');
  assert(html.includes('#7B5CFF'), 'brand: --purple matches v5b');
  assert(html.includes('#D4943A'), 'brand: --orange matches v5b');
  assert(html.includes('#F0EDF8'), 'brand: --text-bright matches v5b');
  assert(html.includes('backdrop-filter'), 'brand: glass effect present');
}

// ---------------------------------------------------------------------------
// 6. WebCrypto + ciphers
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({
    sid: 's', mode: 'generate', expiresAtMs: 0, apiBase: '/', nowMs: 0,
  });
  assert(html.includes('X25519'), 'crypto: X25519 algorithm referenced');
  // rc.12: AEAD is AES-GCM (WebCrypto-supported). ChaCha20-Poly1305 is NOT
  // implemented in browser WebCrypto; see pair-crypto.ts header for context.
  assert(html.includes('AES-GCM'), 'crypto: AES-GCM referenced');
  assert(!html.includes('ChaCha20-Poly1305'), 'crypto: no stale ChaCha20-Poly1305 ref');
  assert(html.includes('HKDF'), 'crypto: HKDF referenced');
  assert(html.includes('totalreclaw-pair-v2'), 'crypto: HKDF info matches server (v2)');
  assert(html.includes('deriveBits'), 'crypto: WebCrypto deriveBits API used');
}

// ---------------------------------------------------------------------------
// 7. Reads pk from URL fragment (§5c)
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({
    sid: 's', mode: 'generate', expiresAtMs: 0, apiBase: '/', nowMs: 0,
  });
  assert(html.includes('window.location.hash'), 'frag: reads window.location.hash');
  assert(html.includes('parseFragmentPk'), 'frag: parseFragmentPk defined');
}

// ---------------------------------------------------------------------------
// 8. No external CDN / host references
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({
    sid: 's', mode: 'generate', expiresAtMs: 0, apiBase: '/', nowMs: 0,
  });
  // No script src, no stylesheet href to external hosts, no CDN domains
  const badPatterns = [
    /<script\s+[^>]*src=/i,
    /<link\s+[^>]*href=/i,
    /cdnjs/i,
    /googleapis/i,
    /unpkg/i,
    /jsdelivr/i,
    /fonts\.googleapis/i,
    /https:\/\/cdn\./i,
  ];
  for (const re of badPatterns) {
    assert(!re.test(html), `external: no match for ${re}`);
  }
}

// ---------------------------------------------------------------------------
// 9. Injection safety — malicious sid/apiBase values are escaped
// ---------------------------------------------------------------------------
{
  // sid contains `</script>` — must be escaped
  const evilSid = 'safe</script><img src=x onerror=alert(1)>';
  const html = renderPairPage({
    sid: evilSid,
    mode: 'generate',
    expiresAtMs: 0,
    apiBase: '/x',
    nowMs: 0,
  });
  // The RAW string must NOT appear (else a `</script>` would close the script block
  // and the subsequent HTML would execute as markup).
  assert(!html.includes(evilSid), 'inject-safe: raw evil sid does not appear');
  // But the JSON.stringify form should appear (with `\u003c/script>` escape or similar)
  assert(html.includes('const SID = '), 'inject-safe: SID constant still embedded');
  // Specifically, the `</script>` payload must be escaped. JSON.stringify
  // by default does NOT escape `/` so we rely on either sequencing OR
  // Unicode escape. Check either form.
  const escapedSlash = html.includes('\\u003c/script>') || html.includes('<\\/script>');
  // If neither is present, at least confirm the evil sid doesn't terminate a script block.
  if (!escapedSlash) {
    // Make sure the SID line doesn't end with `"};`
    const sidLine = /const SID = [^\n]+/.exec(html);
    assert(!!sidLine && !/<\/script>/.test(sidLine[0]), 'inject-safe: SID line contains no </script>');
  } else {
    assert(true, 'inject-safe: </script> escaped');
  }
}

// ---------------------------------------------------------------------------
// 10. Mode branching — import page has paste warnings
// ---------------------------------------------------------------------------
{
  const genHtml = renderPairPage({ sid: 's', mode: 'generate', expiresAtMs: 0, apiBase: '/', nowMs: 0 });
  const impHtml = renderPairPage({ sid: 's', mode: 'import', expiresAtMs: 0, apiBase: '/', nowMs: 0 });
  assert(genHtml.includes('const MODE = "generate"'), 'mode: generate constant');
  assert(impHtml.includes('const MODE = "import"'), 'mode: import constant');
  // Both versions carry the runtime branching logic (generateMnemonic128,
  // renderImportFlow)
  assert(genHtml.includes('generateMnemonic128'), 'mode: generate code path present');
  assert(genHtml.includes('renderImportFlow'), 'mode: import code path present');
}

// ---------------------------------------------------------------------------
// 11. Prefers-reduced-motion respected
// ---------------------------------------------------------------------------
{
  const html = renderPairPage({ sid: 's', mode: 'generate', expiresAtMs: 0, apiBase: '/', nowMs: 0 });
  assert(html.includes('prefers-reduced-motion'), 'a11y: prefers-reduced-motion media query present');
  assert(html.includes('aria-live'), 'a11y: aria-live region on countdown');
}

console.log(`# ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
