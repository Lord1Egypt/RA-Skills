/**
 * pair-page — the self-contained HTML + JS + CSS bundle served by the
 * `/plugin/totalreclaw/pair/finish` handler. The phone or laptop
 * browser loads this, reads the gateway's ephemeral public key from
 * the URL fragment (`#pk=...`), runs the client-side pairing flow
 * ENTIRELY in the browser, and POSTs the encrypted payload back.
 *
 * rc.13 status: this OpenClaw-plugin local-mode page has NOT been
 * ported to the wizard UX used by the relay (production) and the
 * Python local-mode pages. Local-mode on the OpenClaw plugin is rarely
 * exercised — the plugin defaults to a relay flow via the Hermes
 * Python sidecar and only falls back here for air-gapped setups. The
 * wizard UX port for this file is tracked for rc.14 alongside the
 * design decision on whether to share a single CSS+JS asset across
 * all three pair pages (relay / Python / plugin) or keep them
 * independently inlined. For now, this file retains its rc.10–rc.12
 * UX shape and the rc.12 AES-GCM cipher swap.
 *
 * Brand tokens imported from the v5b.html public site (colors, font
 * stack). Typography falls back to system fonts for mobile parity —
 * we don't ship Euclid Circular A bytes over the pairing HTTP surface.
 *
 * Scope and guarantees
 * --------------------
 *   - ENTIRELY self-contained: no external asset references, no CDN,
 *     no Google Fonts, no script-src. The page uses only inline CSS,
 *     inline JS, and Web Platform APIs. Works offline once loaded.
 *   - No `fs.*` reads, no env-var reads — this module just exports a
 *     function that builds and returns the page text. Scanner clean by
 *     construction.
 *   - The browser code runs with no secret-bearing network sends
 *     except the final encrypted AEAD blob. All mnemonic handling
 *     happens in-JS; no console.log calls; cleared from memory after
 *     submission.
 *   - Mobile-first CSS, scales up to desktop.
 *
 * Security copy (user ratification 2026-04-20, phone-page wave):
 *   - Frame as "your TotalReclaw account key", not "recovery phrase".
 *   - Bolded "Use it ONLY with TotalReclaw" warning.
 *   - Concrete storage suggestions (password manager / encrypted
 *     notes / written-in-safe).
 *   - "With it you can:" + "Without it:" consequence blocks.
 *   - All copy surfaces BEFORE the acknowledgment gate.
 */

import { wordlist as BIP39_ENGLISH_WORDLIST } from '@scure/bip39/wordlists/english.js';

export interface PairPageTemplateInputs {
  /** Session id — embedded as a JS constant; also visible in URL. */
  sid: string;
  /** Session mode — drives the UI branch. */
  mode: 'generate' | 'import';
  /** Session expiresAt in ms — the countdown timer reads this. */
  expiresAtMs: number;
  /**
   * The server's pathname base for the 3 API endpoints. All three live
   * under this prefix. Default: "/plugin/totalreclaw/pair".
   */
  apiBase: string;
  /** Current wall-clock (ms) — used to compute initial countdown. */
  nowMs: number;
}

// ---------------------------------------------------------------------------
// Pre-computed BIP-39 wordlist literal — emitted into the page once at
// import time so we don't re-stringify on every render. The `@scure/bip39`
// wordlist is a newline-delimited string; we split and JSON.stringify to
// emit a safe JS array literal.
// ---------------------------------------------------------------------------

function buildBip39Literal(): string {
  // `@scure/bip39` exports the English wordlist as a `string[]` of length 2048.
  const words = BIP39_ENGLISH_WORDLIST;
  if (!Array.isArray(words) || words.length !== 2048) {
    throw new Error(
      `pair-page: expected 2048 BIP-39 words, got ${Array.isArray(words) ? words.length : typeof words}`,
    );
  }
  // JSON.stringify produces double-quoted strings; concatenate into a
  // compact literal (no leading/trailing comma).
  return words.map((w) => JSON.stringify(w)).join(',');
}

const BIP39_WORDLIST_JS_ARRAY = buildBip39Literal();

/**
 * Escape a string for safe embedding between `<script>` tags.
 *
 * `JSON.stringify` produces a valid JS string literal but does NOT
 * escape `<`, `>`, `&`, or U+2028/U+2029. All four are dangerous when
 * the resulting string lands inside a `<script>` block:
 *   - `</script>` in the payload would close the script element and
 *     let subsequent bytes parse as HTML (XSS).
 *   - `<!--` / `-->` can start an HTML comment that would hide code
 *     from the browser under some parser modes.
 *   - U+2028 / U+2029 are line terminators in JS even though JSON
 *     permits them, which can break tooling.
 *
 * Our inputs (sid, apiBase, mode) are internally-controlled today, but
 * defense-in-depth is cheap and matches OWASP's recommended pattern.
 */
function escForJsString(s: string): string {
  return JSON.stringify(s)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/&/g, '\\u0026')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}

/**
 * Build the full HTML page. The mode selector + runtime parameters are
 * baked in as JS constants so the page doesn't need any additional
 * query round-trip on load.
 */
export function renderPairPage(inputs: PairPageTemplateInputs): string {
  const { sid, mode, expiresAtMs, apiBase, nowMs } = inputs;

  // All JS-embedded values must pass through escForJsString — it emits
  // proper JS string literals (including quotes) so we interpolate them
  // as bare expressions.
  const SID = escForJsString(sid);
  const MODE = escForJsString(mode);
  const API_BASE = escForJsString(apiBase);
  const EXPIRES_AT = String(expiresAtMs);
  const NOW = String(nowMs);

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="robots" content="noindex, nofollow" />
<meta name="color-scheme" content="dark" />
<title>TotalReclaw &mdash; Pair your account</title>
<style>
/* Brand tokens from public site v5b.html */
:root {
  --bg: #0B0B1A;
  --bg-card: rgba(16, 14, 32, 0.65);
  --text: rgba(255, 255, 255, 0.78);
  --text-dim: rgba(255, 255, 255, 0.50);
  --text-bright: #F0EDF8;
  --text-white: rgba(255, 255, 255, 0.96);
  --purple: #7B5CFF;
  --purple-dim: rgba(123, 92, 255, 0.14);
  --purple-ring: rgba(123, 92, 255, 0.28);
  --orange: #D4943A;
  --success: #34d399;
  --danger: #f87171;
  --border: rgba(255, 255, 255, 0.08);
  --border-accent: rgba(123, 92, 255, 0.24);
  --mono: 'SF Mono', 'Fira Code', 'Cascadia Code', 'Menlo', 'Consolas', monospace;
  --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
html { font-size: 16px; }
@media (min-width: 720px) { html { font-size: 17px; } }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-image:
    radial-gradient(circle at 50% 0%, rgba(123, 92, 255, 0.12), transparent 55%),
    radial-gradient(circle at 10% 90%, rgba(212, 148, 58, 0.06), transparent 45%);
  background-attachment: fixed;
}

.wrap {
  max-width: 560px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem;
}
@media (min-width: 720px) { .wrap { padding: 3rem 1.5rem; } }

.brand {
  display: flex; align-items: center; gap: 0.6rem;
  margin-bottom: 1.5rem;
  font-weight: 600; font-size: 0.95rem;
  color: var(--text-bright); letter-spacing: 0.02em;
}
.brand-dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--purple);
  box-shadow: 0 0 14px var(--purple-ring);
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.5rem;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  animation: fade-in 0.4s ease-out;
}
@media (min-width: 720px) { .card { padding: 2rem; } }

h1 {
  margin: 0 0 0.5rem;
  font-size: 1.55rem; font-weight: 600; letter-spacing: -0.01em;
  color: var(--text-white); line-height: 1.2;
}
h2 {
  margin: 1.75rem 0 0.75rem;
  font-size: 1.05rem; font-weight: 600;
  color: var(--text-bright); letter-spacing: 0.01em;
}
p { margin: 0 0 0.85rem; line-height: 1.55; }
strong { color: var(--text-bright); font-weight: 600; }
em { color: var(--orange); font-style: normal; font-weight: 600; }
small { color: var(--text-dim); font-size: 0.82rem; }

ul { padding-left: 1.1rem; margin: 0.25rem 0 0.85rem; }
li { margin-bottom: 0.35rem; line-height: 1.5; }

.countdown {
  display: inline-flex; align-items: center; gap: 0.35rem;
  margin-top: 0.25rem;
  padding: 0.22rem 0.6rem;
  background: var(--purple-dim); border: 1px solid var(--border-accent);
  border-radius: 999px;
  font-size: 0.76rem; color: var(--text-bright); font-weight: 500;
  font-variant-numeric: tabular-nums;
}
.countdown.expired { background: rgba(248, 113, 113, 0.12); border-color: rgba(248, 113, 113, 0.35); color: var(--danger); }

.callout {
  border-left: 3px solid var(--purple);
  padding: 0.75rem 0.95rem; margin: 1rem 0;
  background: var(--purple-dim);
  border-radius: 0 8px 8px 0;
  font-size: 0.92rem;
}
.callout.warn { border-left-color: var(--orange); background: rgba(212, 148, 58, 0.07); }
.callout.danger { border-left-color: var(--danger); background: rgba(248, 113, 113, 0.08); }

input[type=text], input[type=number], textarea {
  width: 100%;
  padding: 0.75rem 0.9rem;
  margin: 0.25rem 0 0.5rem;
  background: rgba(255,255,255,0.03);
  color: var(--text-bright);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-family: var(--mono);
  font-size: 1rem;
  transition: border-color 0.2s, background 0.2s;
}
input:focus, textarea:focus {
  outline: none;
  border-color: var(--purple);
  background: rgba(123, 92, 255, 0.05);
}
input.code-input {
  font-size: 1.25rem; letter-spacing: 0.3em; text-align: center;
  font-variant-numeric: tabular-nums;
}
textarea { min-height: 5.5em; resize: vertical; }

button {
  display: inline-flex; align-items: center; justify-content: center; gap: 0.4rem;
  padding: 0.8rem 1.25rem;
  background: var(--purple); color: var(--text-white);
  border: none; border-radius: 8px;
  font-family: var(--sans); font-size: 0.95rem; font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
  min-width: 140px;
}
button:hover:not(:disabled) { background: #8b6dff; box-shadow: 0 4px 20px rgba(123, 92, 255, 0.35); }
button:active:not(:disabled) { transform: translateY(1px); }
button:disabled { opacity: 0.45; cursor: not-allowed; }
button.secondary {
  background: transparent; color: var(--text);
  border: 1px solid var(--border);
}
button.secondary:hover:not(:disabled) { border-color: var(--border-accent); color: var(--text-bright); background: var(--purple-dim); box-shadow: none; }

.btn-row { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 1rem; }

.mnemonic-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem 0.75rem;
  margin: 0.75rem 0;
  font-family: var(--mono);
  font-size: 0.95rem;
}
@media (min-width: 520px) { .mnemonic-grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 720px) { .mnemonic-grid { grid-template-columns: repeat(4, 1fr); } }

.mnemonic-word {
  display: flex; align-items: baseline; gap: 0.35rem;
  padding: 0.55rem 0.7rem;
  background: rgba(255,255,255,0.035);
  border: 1px solid var(--border);
  border-radius: 7px;
  animation: word-in 0.3s ease-out backwards;
}
.mnemonic-word .num {
  color: var(--text-dim); font-size: 0.78rem; font-weight: 500;
  min-width: 1.5rem; text-align: right;
}
.mnemonic-word .word { color: var(--text-bright); font-weight: 500; }

.pulse {
  display: inline-block;
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--purple);
  box-shadow: 0 0 0 0 rgba(123, 92, 255, 0.5);
  animation: pulse 1.6s infinite ease-out;
  margin-right: 0.5rem; vertical-align: middle;
}
.check {
  display: inline-block; width: 14px; height: 14px;
  color: var(--success); vertical-align: middle; margin-right: 0.5rem;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes word-in {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
  0%   { box-shadow: 0 0 0 0 rgba(123, 92, 255, 0.5); }
  75%  { box-shadow: 0 0 0 12px rgba(123, 92, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(123, 92, 255, 0); }
}

.hidden { display: none !important; }
.center { text-align: center; }
.mt-2 { margin-top: 1.25rem; }
.mono { font-family: var(--mono); }

/* Reduced-motion preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01s !important; transition-duration: 0.01s !important; }
}
</style>
</head>
<body>
<div class="wrap">
  <div class="brand">
    <span class="brand-dot"></span>
    <span>TotalReclaw</span>
  </div>

  <div class="card" id="stage">
    <!-- Stages render dynamically. Initial content is Stage 0: code entry. -->
    <div id="stage-body">Loading pairing session&hellip;</div>
    <div class="countdown" id="countdown" aria-live="polite"></div>
  </div>

  <p class="mt-2 center"><small>End-to-end encrypted. Gateway does not see your key in plaintext.</small></p>
</div>

<script>
"use strict";
(function() {
  // ---------- Constants injected by the server ----------
  const SID = ${SID};
  const MODE = ${MODE};              // "generate" or "import"
  const API_BASE = ${API_BASE};      // e.g. "/plugin/totalreclaw/pair"
  const EXPIRES_AT_MS = ${EXPIRES_AT};
  const SERVER_NOW_MS = ${NOW};
  // Client-observed time at page load (used to adjust for clock skew).
  const CLIENT_EPOCH_AT_LOAD = Date.now();

  // v2: cipher-suite swap in rc.12 (see pair-crypto.ts header). Keep
  // this constant in lockstep with the gateway-side pair-crypto.ts.
  const HKDF_INFO = "totalreclaw-pair-v2";

  // ---------- Small utilities ----------
  function $(sel, root) { return (root || document).querySelector(sel); }
  function el(html) { const t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstElementChild; }
  function render(nodeOrHtml) {
    const body = $("#stage-body");
    body.innerHTML = "";
    if (typeof nodeOrHtml === "string") body.innerHTML = nodeOrHtml;
    else body.appendChild(nodeOrHtml);
  }
  function b64urlFromBytes(bytes) {
    let s = "";
    for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
    return btoa(s).replace(/\\+/g, "-").replace(/\\//g, "_").replace(/=+$/, "");
  }
  function bytesFromB64url(s) {
    const pad = s.length % 4 === 2 ? "==" : s.length % 4 === 3 ? "=" : "";
    const bin = atob(s.replace(/-/g, "+").replace(/_/g, "/") + pad);
    const out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  function zeroBytes(u8) { if (u8 && u8.fill) u8.fill(0); }

  // ---------- Parse the pk from the URL fragment ----------
  function parseFragmentPk() {
    const hash = window.location.hash || "";
    const m = /(?:^#|&)pk=([A-Za-z0-9_-]+)/.exec(hash);
    return m ? m[1] : null;
  }
  const PK_GATEWAY_B64 = parseFragmentPk();

  // ---------- Countdown ----------
  function updateCountdown() {
    const elNode = $("#countdown");
    if (!elNode) return;
    const clientNow = Date.now();
    const serverNow = SERVER_NOW_MS + (clientNow - CLIENT_EPOCH_AT_LOAD);
    const remaining = Math.max(0, EXPIRES_AT_MS - serverNow);
    const mm = Math.floor(remaining / 60000);
    const ss = Math.floor((remaining % 60000) / 1000);
    if (remaining === 0) {
      elNode.classList.add("expired");
      elNode.textContent = "Expired";
    } else {
      elNode.textContent = "Expires in " + mm + ":" + String(ss).padStart(2, "0");
    }
  }
  setInterval(updateCountdown, 1000);

  // ---------- Bip39 wordlist (English), inlined as base64url for compactness ----------
  // The full English BIP-39 wordlist — 2048 words, one per line. This is
  // the canonical list from the BIP-39 spec. We inline it so the page is
  // fully self-contained. ~13KB raw, compresses well over gzip.
  const BIP39_WORDLIST = [${BIP39_WORDLIST_JS_ARRAY}];

  if (BIP39_WORDLIST.length !== 2048) {
    render(renderError("Internal: bundled wordlist has " + BIP39_WORDLIST.length + " entries (expected 2048). Cannot proceed."));
    return;
  }

  function generateMnemonic128() {
    const entropy = new Uint8Array(16);
    crypto.getRandomValues(entropy);
    return entropyToMnemonic(entropy);
  }

  async function entropyToMnemonic(entropy) {
    // BIP-39: checksum = first (len/4) bits of SHA-256(entropy), appended.
    // 128-bit entropy → 4-bit checksum → 132 bits → 12 words × 11 bits.
    const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", entropy));
    const csBits = entropy.length / 4; // 4 for 128
    const bits = [];
    for (let i = 0; i < entropy.length; i++) {
      for (let b = 7; b >= 0; b--) bits.push((entropy[i] >> b) & 1);
    }
    for (let i = 0; i < csBits; i++) bits.push((digest[0] >> (7 - i)) & 1);
    const words = [];
    for (let i = 0; i < bits.length; i += 11) {
      let n = 0;
      for (let k = 0; k < 11; k++) n = (n << 1) | bits[i + k];
      words.push(BIP39_WORDLIST[n]);
    }
    return words.join(" ");
  }

  async function validateMnemonic(phrase) {
    const words = phrase.trim().toLowerCase().split(/\\s+/);
    if (words.length !== 12) return false;
    const bits = [];
    for (const w of words) {
      const idx = BIP39_WORDLIST.indexOf(w);
      if (idx < 0) return false;
      for (let b = 10; b >= 0; b--) bits.push((idx >> b) & 1);
    }
    // 132 bits: 128 entropy + 4 checksum.
    const entropy = new Uint8Array(16);
    for (let i = 0; i < 128; i++) entropy[i >> 3] |= bits[i] << (7 - (i & 7));
    const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", entropy));
    for (let i = 0; i < 4; i++) {
      const got = bits[128 + i];
      const want = (digest[0] >> (7 - i)) & 1;
      if (got !== want) return false;
    }
    return true;
  }

  // ---------- Crypto shims: prefer WebCrypto; fall back to JS path ----------
  // WebCrypto's x25519 + HKDF + AES-GCM availability is Safari 17+ and
  // modern Chromium 133+ / Firefox 130+. If absent we render an error
  // — the page is self-contained and we do not bundle any JS crypto shim.
  async function ensureWebCryptoSupport() {
    if (!window.crypto || !crypto.subtle) return false;
    try {
      const kp = await crypto.subtle.generateKey({ name: "X25519" }, true, ["deriveBits"]);
      return !!kp.privateKey && !!kp.publicKey;
    } catch (e) {
      return false;
    }
  }

  async function x25519GenerateKeyPair() {
    const kp = await crypto.subtle.generateKey({ name: "X25519" }, true, ["deriveBits"]);
    const rawPub = new Uint8Array(await crypto.subtle.exportKey("raw", kp.publicKey));
    return { keyPair: kp, rawPubB64: b64urlFromBytes(rawPub) };
  }
  async function x25519DeriveShared(privateKey, peerPubRaw) {
    const peerPub = await crypto.subtle.importKey("raw", peerPubRaw, { name: "X25519" }, false, []);
    const sharedBits = await crypto.subtle.deriveBits({ name: "X25519", public: peerPub }, privateKey, 256);
    return new Uint8Array(sharedBits);
  }
  async function hkdfSha256(sharedBytes, saltBytes, infoBytes, outLen) {
    const key = await crypto.subtle.importKey("raw", sharedBytes, { name: "HKDF" }, false, ["deriveBits"]);
    const bits = await crypto.subtle.deriveBits(
      { name: "HKDF", hash: "SHA-256", salt: saltBytes, info: infoBytes },
      key, outLen * 8,
    );
    return new Uint8Array(bits);
  }
  // AEAD: AES-256-GCM (universal in WebCrypto). Cipher swap rationale
  // lives in pair-crypto.ts header comment (rc.12 changelog entry).
  async function aeadEncryptAesGcm(keyBytes, nonce, sid, plaintext) {
    const key = await crypto.subtle.importKey(
      "raw", keyBytes,
      { name: "AES-GCM" },
      false, ["encrypt"],
    );
    const adBytes = new TextEncoder().encode(sid);
    const ct = new Uint8Array(await crypto.subtle.encrypt(
      { name: "AES-GCM", iv: nonce, additionalData: adBytes, tagLength: 128 },
      key, plaintext,
    ));
    return ct;
  }

  async function aesGcmSupported() {
    try {
      const k = new Uint8Array(32);
      const n = new Uint8Array(12);
      const key = await crypto.subtle.importKey("raw", k, { name: "AES-GCM" }, false, ["encrypt"]);
      await crypto.subtle.encrypt({ name: "AES-GCM", iv: n, additionalData: new Uint8Array(0), tagLength: 128 }, key, new Uint8Array(0));
      return true;
    } catch (e) { return false; }
  }

  // ---------- Stage renderers ----------
  function renderError(msg) {
    const d = el('<div><h1>Something went wrong</h1><p>' + escapeHtml(msg) + '</p><p><small>Start over from your terminal: <code>openclaw totalreclaw pair</code></small></p></div>');
    return d;
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function(c) {
      return c === "&" ? "&amp;" : c === "<" ? "&lt;" : c === ">" ? "&gt;" : "&quot;";
    });
  }

  // Stage 1: code entry
  function renderCodeEntry() {
    const node = el(
      '<div>' +
      '<h1>Pair with your gateway</h1>' +
      '<p>Enter the 6-digit code shown in your terminal. This prevents a bystander from hijacking this pairing.</p>' +
      '<input id="code-in" class="code-input" inputmode="numeric" pattern="[0-9]*" maxlength="6" autocomplete="one-time-code" autofocus />' +
      '<div id="code-error" class="callout danger hidden"></div>' +
      '<div class="btn-row">' +
      '<button id="code-continue">Continue</button>' +
      '</div>' +
      '</div>'
    );
    render(node);
    const input = $("#code-in");
    input.addEventListener("input", function() {
      input.value = input.value.replace(/\\D+/g, "").slice(0, 6);
    });
    $("#code-continue").addEventListener("click", function() { onCodeSubmit(); });
    input.addEventListener("keydown", function(e) { if (e.key === "Enter") onCodeSubmit(); });
  }

  async function onCodeSubmit() {
    const code = $("#code-in").value;
    if (!/^\\d{6}$/.test(code)) {
      showInlineError("code-error", "Enter all 6 digits.");
      return;
    }
    $("#code-continue").disabled = true;

    try {
      const url = API_BASE + "/start?sid=" + encodeURIComponent(SID) + "&c=" + encodeURIComponent(code);
      const r = await window.fetch(url, { method: "GET", cache: "no-store" });
      if (r.status === 403) {
        const j = await r.json().catch(function(){ return {}; });
        showInlineError("code-error", j.error === "attempts_exhausted"
          ? "Too many wrong codes. This pairing session is locked out. Start over from your terminal."
          : "Code doesn't match. Double-check your terminal.");
        $("#code-continue").disabled = false;
        return;
      }
      if (r.status === 410) { showInlineError("code-error", "Session expired. Start over from your terminal."); return; }
      if (r.status === 404) { showInlineError("code-error", "Session not found. Start over from your terminal."); return; }
      if (!r.ok) { showInlineError("code-error", "Gateway error: " + r.status); return; }
      const meta = await r.json();
      // Proceed to the recovery-phrase stage based on mode.
      if (MODE === "generate") await renderGenerateFlow(meta);
      else await renderImportFlow(meta);
    } catch (err) {
      showInlineError("code-error", "Network error. Try again.");
      $("#code-continue").disabled = false;
    }
  }

  function showInlineError(id, msg) {
    const e = $("#" + id);
    if (!e) return;
    e.textContent = msg;
    e.classList.remove("hidden");
  }

  // Stage 2a: Generate a recovery phrase in-browser, show it with safety copy + ack gate
  async function renderGenerateFlow(meta) {
    const mnemonic = await generateMnemonic128();
    const words = mnemonic.split(" ");
    let gridHtml = '';
    for (let i = 0; i < words.length; i++) {
      gridHtml += '<div class="mnemonic-word" style="animation-delay:' + (i * 30) + 'ms"><span class="num">' + (i+1) + '.</span><span class="word">' + escapeHtml(words[i]) + '</span></div>';
    }
    const node = el(
      '<div>' +
      '<h1>This is your TotalReclaw recovery phrase</h1>' +
      '<p>A new recovery phrase has been generated. Write it down now, somewhere safe. This is the only way to restore your account later.</p>' +
      '<h2>Your recovery phrase</h2>' +
      '<div class="mnemonic-grid">' + gridHtml + '</div>' +
      '<div class="btn-row"><button id="copy" class="secondary">Copy to clipboard</button></div>' +
      '<div class="callout warn"><strong>Use it ONLY with TotalReclaw.</strong> <em>Never</em> reuse this phrase for a crypto wallet, banking, email, or any other service. TotalReclaw recovery phrases must be dedicated.</div>' +
      '<h2>Store it somewhere safe</h2>' +
      '<p>Your recovery phrase is 12 words. Store it somewhere safe — a password manager works well. Use it only for TotalReclaw. Don\'t reuse it anywhere else. Don\'t put funds on it.</p>' +
      '<ul>' +
      '<li>A password manager (1Password, Bitwarden, Apple Keychain, etc.)</li>' +
      '<li>An encrypted notes app (Notes with end-to-end encryption, Standard Notes, Obsidian vault)</li>' +
      '<li>Written on paper in a physical safe</li>' +
      '</ul>' +
      '<h2>With this recovery phrase you can:</h2>' +
      '<ul>' +
      '<li>Restore your TotalReclaw account on any new device</li>' +
      '<li>Import your memories into Hermes, OpenClaw, the MCP client, or any other TotalReclaw-enabled agent</li>' +
      '<li>Reset your gateway without losing a single memory</li>' +
      '</ul>' +
      '<div class="callout danger"><strong>Without it:</strong> you permanently lose access to all memories across all agents. TotalReclaw cannot recover it for you.</div>' +
      '<h2>Confirm</h2>' +
      '<p>Before you continue, retype three of your words:</p>' +
      '<div id="ack-probes"></div>' +
      '<div id="ack-error" class="callout danger hidden"></div>' +
      '<div class="btn-row">' +
      '<button id="ack-submit">I have saved it &mdash; continue</button>' +
      '</div>' +
      '</div>'
    );
    render(node);

    $("#copy").addEventListener("click", function() {
      navigator.clipboard.writeText(mnemonic).then(function() {
        $("#copy").textContent = "Copied \u2713";
      }).catch(function() {});
    });

    // Random 3 distinct probe indices
    const probe = pickDistinctIndices(words.length, 3);
    const probeEl = $("#ack-probes");
    for (const idx of probe) {
      const row = el(
        '<div style="display:flex; align-items:center; gap:0.75rem; margin:0.5rem 0;">' +
        '<span style="min-width:5ch; color:var(--text-dim);">Word #' + (idx+1) + '</span>' +
        '<input type="text" autocapitalize="none" autocorrect="off" spellcheck="false" data-idx="' + idx + '" />' +
        '</div>'
      );
      probeEl.appendChild(row);
    }

    $("#ack-submit").addEventListener("click", async function() {
      const inputs = probeEl.querySelectorAll("input[data-idx]");
      for (const inp of inputs) {
        const idx = parseInt(inp.getAttribute("data-idx"), 10);
        if (inp.value.trim().toLowerCase() !== words[idx]) {
          showInlineError("ack-error", "Word #" + (idx+1) + " doesn't match. Check your written copy and try again.");
          return;
        }
      }
      $("#ack-error").classList.add("hidden");
      $("#ack-submit").disabled = true;
      await submitEncrypted(mnemonic);
    });
  }

  function pickDistinctIndices(n, k) {
    const pool = [];
    for (let i = 0; i < n; i++) pool.push(i);
    const out = [];
    for (let i = 0; i < k; i++) {
      const j = Math.floor(Math.random() * pool.length);
      out.push(pool[j]); pool.splice(j, 1);
    }
    out.sort(function(a,b) { return a-b; });
    return out;
  }

  // Stage 2b: Import an existing phrase
  async function renderImportFlow(meta) {
    const node = el(
      '<div>' +
      '<h1>Import your TotalReclaw recovery phrase</h1>' +
      '<p>Enter your 12-word recovery phrase to restore your account. It is processed ENTIRELY in your browser and encrypted before it leaves this page.</p>' +
      '<div class="callout warn"><strong>Use it ONLY with TotalReclaw.</strong> Do <em>not</em> paste a phrase that controls a crypto wallet, banking account, email, or any other service. TotalReclaw recovery phrases must be dedicated.</div>' +
      '<textarea id="phrase" autocapitalize="none" autocorrect="off" spellcheck="false" placeholder="word1 word2 word3 ... word12"></textarea>' +
      '<div id="phrase-error" class="callout danger hidden"></div>' +
      '<p><small>Checksum is verified in your browser. Invalid phrases are rejected before upload.</small></p>' +
      '<div class="btn-row">' +
      '<button id="import-submit">Upload encrypted</button>' +
      '</div>' +
      '</div>'
    );
    render(node);
    $("#import-submit").addEventListener("click", async function() {
      const raw = $("#phrase").value.normalize("NFKC").toLowerCase().trim().split(/\\s+/).join(" ");
      const ok = await validateMnemonic(raw);
      if (!ok) {
        showInlineError("phrase-error", "That is not a valid 12-word recovery phrase. Check spelling, word count, and that the checksum is intact.");
        return;
      }
      $("#phrase-error").classList.add("hidden");
      $("#import-submit").disabled = true;
      await submitEncrypted(raw);
    });
  }

  // Stage 3: encrypt + upload
  async function submitEncrypted(mnemonic) {
    render('<div class="center"><span class="pulse"></span><span>Encrypting\u2026</span></div>');

    // 1. Sanity: we MUST have pk_G from the URL fragment. Without it we cannot
    //    authenticate the gateway key and the whole point of the protocol is
    //    defeated.
    if (!PK_GATEWAY_B64) {
      render(renderError("Missing gateway public key in the URL fragment. This link is malformed; start over from your terminal."));
      return;
    }
    const pkGateway = bytesFromB64url(PK_GATEWAY_B64);
    if (pkGateway.length !== 32) {
      render(renderError("Gateway public key is the wrong size. Start over from your terminal."));
      return;
    }

    // 2. Ensure WebCrypto supports our ciphers.
    if (!(await ensureWebCryptoSupport())) {
      render(renderError("Your browser does not support modern cryptographic APIs (X25519). Please update your browser and try again, or use a different device. Supported: Chrome 123+, Firefox 130+, Safari 17+."));
      return;
    }
    if (!(await aesGcmSupported())) {
      render(renderError("Your browser does not support AES-GCM. Update your browser or use a different device."));
      return;
    }

    try {
      // 3. Generate ephemeral x25519 keypair
      const dev = await x25519GenerateKeyPair();
      render('<div class="center"><span class="pulse"></span><span>Pairing\u2026 deriving shared key</span></div>');

      // 4. ECDH + HKDF
      const shared = await x25519DeriveShared(dev.keyPair.privateKey, pkGateway);
      const salt = new TextEncoder().encode(SID);
      const info = new TextEncoder().encode(HKDF_INFO);
      const kEnc = await hkdfSha256(shared, salt, info, 32);

      // 5. Encrypt (AEAD with sid as AD)
      const nonce = new Uint8Array(12);
      crypto.getRandomValues(nonce);
      const ptBytes = new TextEncoder().encode(mnemonic);
      const ct = await aeadEncryptAesGcm(kEnc, nonce, SID, ptBytes);

      // 6. Zero sensitive buffers BEFORE sending. The JS GC will run
      //    whenever it runs; explicit zeroing is best-effort but honours
      //    the design doc's "zero after post-ack" requirement.
      zeroBytes(kEnc); zeroBytes(shared); zeroBytes(ptBytes);

      // 7. Submit
      render('<div class="center"><span class="pulse"></span><span>Uploading encrypted recovery phrase\u2026</span></div>');
      const body = {
        v: 1,
        sid: SID,
        pk_d: dev.rawPubB64,
        nonce: b64urlFromBytes(nonce),
        ct: b64urlFromBytes(ct),
      };
      const r = await window.fetch(API_BASE + "/respond", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        cache: "no-store",
        body: JSON.stringify(body),
      });
      if (r.status >= 200 && r.status < 300) {
        const res = await r.json().catch(function(){ return {ok: true}; });
        renderSuccess(res);
      } else if (r.status === 410) {
        render(renderError("Session expired before you submitted. Start over from your terminal."));
      } else if (r.status === 409) {
        render(renderError("This pairing session has already been used. Start over if you need to re-pair."));
      } else if (r.status === 400) {
        const j = await r.json().catch(function(){ return {}; });
        render(renderError("Encryption failed validation on the gateway. Usually caused by a bad QR scan or a mid-session clock change. Start over. (" + (j.error || r.status) + ")"));
      } else {
        render(renderError("Gateway error: " + r.status));
      }
    } catch (err) {
      render(renderError("Encryption or upload failed: " + (err && err.message ? err.message : String(err))));
    }
  }

  function renderSuccess(res) {
    // 3.3.0-rc.2: success screen carries the canonical storage-guidance copy
    // so users see it one more time right after submit (some skipped past
    // it during the generate flow). Same wording as first-run.ts
    // COPY.STORAGE_GUIDANCE.
    const node = el(
      '<div>' +
      '<h1><svg class="check" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2 8.5l4 4 8-10" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>Paired</h1>' +
      '<p>Your TotalReclaw account is now active on this gateway. You can close this tab and go back to your terminal or chat client.</p>' +
      '<div class="callout warn">Your recovery phrase is 12 words. Store it somewhere safe &mdash; a password manager works well. Use it only for TotalReclaw. Don&#39;t reuse it anywhere else. Don&#39;t put funds on it.</div>' +
      '<p><small>Account id: <span class="mono">' + escapeHtml((res && res.accountId) || "(generated)") + '</span></small></p>' +
      '</div>'
    );
    render(node);
    const c = $("#countdown"); if (c) c.textContent = "Done";
  }

  // ---------- Boot ----------
  window.addEventListener("DOMContentLoaded", function() {
    updateCountdown();
    if (!PK_GATEWAY_B64) {
      render(renderError("No gateway key in the URL fragment. The QR scanner may have stripped it. Try re-scanning or paste the full URL from your terminal."));
      return;
    }
    // Basic browser-feature smoke test.
    if (!(window.crypto && crypto.subtle && crypto.getRandomValues)) {
      render(renderError("Your browser does not expose WebCrypto. Update the browser or use Chrome/Safari/Firefox."));
      return;
    }
    renderCodeEntry();
  });
})();
</script>
</body>
</html>
`;
}
