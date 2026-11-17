#!/usr/bin/env node
// Extract one top-level slice of Tock's `window.$REDUX_STATE` store from SSR
// HTML piped in on stdin. A dependency-free standalone script for use outside
// the MCP; the server itself reads slices with `extractJsonKeyAfterMarker`
// from `@chrischall/mcp-utils/scrape`, which is the reference behaviour.
//
// The store is a JS *object literal*, not strict JSON — absent values are the
// bare identifier `undefined`, so we string/escape-aware locate the requested
// key's value, sanitize `undefined` -> `null`, and JSON.parse just that slice.
//
// Usage:
//   fpx get 'https://www.exploretock.com/city' -p tock \
//     | node extract-redux-slice.mjs app | jq '...'

const MARKERS = ['window.$REDUX_STATE', '"$REDUX_STATE"', '$REDUX_STATE'];

function findStoreStart(html) {
  let idx = -1;
  let markerLen = 0;
  for (const m of MARKERS) {
    const i = html.indexOf(m);
    if (i >= 0) {
      idx = i;
      markerLen = m.length;
      break;
    }
  }
  if (idx < 0) throw new Error('$REDUX_STATE marker not found in HTML');
  let start = idx + markerLen;
  while (start < html.length && html[start] !== '{') start++;
  if (start >= html.length) throw new Error('Could not locate start of $REDUX_STATE JSON');
  return start;
}

function consumeValue(src, start) {
  const ch = src[start];
  if (ch === '{' || ch === '[') {
    const open = ch;
    const close = ch === '{' ? '}' : ']';
    let depth = 0;
    let inString = false;
    let escape = false;
    for (let i = start; i < src.length; i++) {
      const c = src[i];
      if (escape) {
        escape = false;
        continue;
      }
      if (inString) {
        if (c === '\\') escape = true;
        else if (c === '"') inString = false;
        continue;
      }
      if (c === '"') inString = true;
      else if (c === open) depth++;
      else if (c === close) {
        depth--;
        if (depth === 0) return i + 1;
      }
    }
    throw new Error('Unmatched brackets in $REDUX_STATE value');
  }
  if (ch === '"') {
    let escape = false;
    for (let i = start + 1; i < src.length; i++) {
      const c = src[i];
      if (escape) escape = false;
      else if (c === '\\') escape = true;
      else if (c === '"') return i + 1;
    }
    throw new Error('Unterminated string in $REDUX_STATE value');
  }
  let i = start;
  while (i < src.length && !/[,}\]]/.test(src[i])) i++;
  return i;
}

function sanitizeJsLiterals(src) {
  let out = '';
  let inString = false;
  let escape = false;
  for (let i = 0; i < src.length; i++) {
    const ch = src[i];
    if (inString) {
      out += ch;
      if (escape) escape = false;
      else if (ch === '\\') escape = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') {
      inString = true;
      out += ch;
      continue;
    }
    if (ch === 'u' && src.startsWith('undefined', i)) {
      const prev = out.replace(/\s+$/, '').slice(-1);
      const after = src[i + 'undefined'.length];
      const boundedAfter = after === undefined || /[\s,}\]]/.test(after);
      if ((prev === ':' || prev === ',' || prev === '[') && boundedAfter) {
        out += 'null';
        i += 'undefined'.length - 1;
        continue;
      }
    }
    out += ch;
  }
  return out;
}

function extractReduxSlice(html, key) {
  const storeStart = findStoreStart(html);
  const needle = `"${key}":`;
  let depth = 0;
  let inString = false;
  let escape = false;
  for (let i = storeStart; i < html.length; i++) {
    const c = html[i];
    if (escape) {
      escape = false;
      continue;
    }
    if (inString) {
      if (c === '\\') escape = true;
      else if (c === '"') inString = false;
      continue;
    }
    if (c === '"') {
      if (depth === 1 && html.startsWith(needle, i)) {
        const valStart = i + needle.length;
        const valEnd = consumeValue(html, valStart);
        const raw = sanitizeJsLiterals(html.slice(valStart, valEnd));
        return JSON.parse(raw);
      }
      inString = true;
    } else if (c === '{') depth++;
    else if (c === '}') {
      depth--;
      if (depth === 0) break;
    }
  }
  throw new Error(`Slice "${key}" not found in $REDUX_STATE`);
}

const key = process.argv[2];
if (!key) {
  console.error('usage: extract-redux-slice.mjs <sliceKey>   (HTML on stdin)');
  process.exit(1);
}
let html = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (d) => (html += d));
process.stdin.on('end', () => {
  try {
    process.stdout.write(JSON.stringify(extractReduxSlice(html, key)));
  } catch (err) {
    console.error(String(err && err.message ? err.message : err));
    process.exit(1);
  }
});
