#!/usr/bin/env node
// Extract Thumbtack SSR data stores from a page on stdin.
// Usage: curl -sSL <url> | node tt-extract.mjs next|apollo|ldjson
//
// Dependency-free on purpose: this runs from a skills directory with no
// node_modules. Its semantics mirror the server's `@chrischall/mcp-utils`
// scrape helpers (extractNextData, extractJsonAfterMarker, extractJsonLdBlocks)
// and tests/skill-extract.test.ts pins the two together, so the skill and the
// MCP return the same data for the same page. Every scan below is linear.
const mode = process.argv[2] || 'next';
let html = '';
process.stdin.setEncoding('utf8');
for await (const c of process.stdin) html += c;
const lower = html.toLowerCase();

const isSpace = (c) => c === ' ' || c === '\t' || c === '\n' || c === '\r' || c === '\f';

// Index of the next real `<script` opener at or after `from`, or -1.
function nextScript(from) {
  for (let i = lower.indexOf('<script', from); i >= 0; i = lower.indexOf('<script', i + 1)) {
    const after = lower[i + 7];
    if (after === undefined || after === '>' || after === '/' || isSpace(after)) return i;
  }
  return -1;
}

// Walk one opening tag's attributes (quote-aware) to its `>`.
// Returns { end, attrs: Map<lowercased name, value> } or null if it never closes.
function scanTag(p) {
  const attrs = new Map();
  for (;;) {
    while (p < html.length && (isSpace(html[p]) || html[p] === '/')) p++;
    if (p >= html.length) return null;
    if (html[p] === '>') return { end: p, attrs };
    const nameStart = p;
    while (p < html.length && !isSpace(html[p]) && html[p] !== '/' && html[p] !== '>' && html[p] !== '=') p++;
    const name = html.slice(nameStart, p).toLowerCase();
    while (p < html.length && isSpace(html[p])) p++;
    if (html[p] !== '=') { attrs.set(name, ''); continue; }
    p++;
    while (p < html.length && isSpace(html[p])) p++;
    const q = html[p];
    let value;
    if (q === '"' || q === "'") {
      const close = html.indexOf(q, p + 1);
      if (close < 0) return null;
      value = html.slice(p + 1, close);
      p = close + 1;
    } else {
      const vs = p;
      while (p < html.length && !isSpace(html[p]) && html[p] !== '>') p++;
      value = html.slice(vs, p);
    }
    if (!attrs.has(name)) attrs.set(name, value);
  }
}

// Every complete <script> tag, in document order: { attrs, body }.
function* scripts() {
  let i = 0;
  for (;;) {
    const open = nextScript(i);
    if (open < 0) return;
    const tag = scanTag(open + 7);
    if (!tag) return;
    const bodyEnd = lower.indexOf('</script', tag.end + 1);
    if (bodyEnd < 0) return;
    yield { attrs: tag.attrs, body: html.slice(tag.end + 1, bodyEnd) };
    i = bodyEnd + 8;
  }
}

// Balanced `{…}` / `[…]` walk, aware of single- and double-quoted strings.
function matchBalanced(s, start) {
  const stack = [];
  let instr = null, esc = false;
  for (let i = start; i < s.length; i++) {
    const c = s[i];
    if (instr) {
      if (esc) esc = false;
      else if (c === '\\') esc = true;
      else if (c === instr) instr = null;
      continue;
    }
    if (c === '"' || c === "'") instr = c;
    else if (c === '{' || c === '[') stack.push(c);
    else if (c === '}' || c === ']') {
      const o = stack.pop();
      if ((c === '}' && o !== '{') || (c === ']' && o !== '[')) return -1;
      if (stack.length === 0) return i + 1;
    }
  }
  return -1;
}

function fail(msg) { console.error(msg); process.exit(3); }

let out;
if (mode === 'next') {
  // Only the real <script id="__NEXT_DATA__"> tag — never the marker text
  // appearing inside some other script.
  let body;
  for (const s of scripts()) if (s.attrs.get('id') === '__NEXT_DATA__') { body = s.body.trim(); break; }
  if (body === undefined) fail('no __NEXT_DATA__ on this page');
  try { out = JSON.parse(body); } catch { fail('__NEXT_DATA__ is not valid JSON'); }
} else if (mode === 'apollo') {
  const i = html.indexOf('window.__APOLLO_STATE__');
  if (i < 0) fail('no __APOLLO_STATE__ on this page');
  let start = i + 'window.__APOLLO_STATE__'.length;
  while (start < html.length && html[start] !== '{' && html[start] !== '[') start++;
  const end = start < html.length ? matchBalanced(html, start) : -1;
  if (end < 0) fail('unterminated __APOLLO_STATE__');
  try { out = JSON.parse(html.slice(start, end)); } catch { fail('__APOLLO_STATE__ is not valid JSON'); }
} else if (mode === 'ldjson') {
  // Script bodies are raw text: parse them as-is (no entity decoding), and
  // skip a malformed block rather than failing the page.
  out = [];
  for (const s of scripts()) {
    if (!/^application\/ld\+json$/i.test((s.attrs.get('type') ?? '').trim())) continue;
    try { out.push(JSON.parse(s.body.trim())); } catch { /* malformed — skip */ }
  }
  if (!out.length) fail('no ld+json on this page');
  if (out.length === 1) out = out[0];
} else { console.error(`unknown mode: ${mode}`); process.exit(2); }
process.stdout.write(JSON.stringify(out));
