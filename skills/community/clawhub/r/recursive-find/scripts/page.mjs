// Page processing: decode the body, strip it to text, search it, extract its
// links. Pure functions; crawl.mjs runs processPage in a worker thread
// (page-worker.mjs) so a catastrophic regex or a pathological page can be
// stopped with a timeout instead of blocking the event loop.

import { kmpSearch } from "./kmp.mjs";

const SNIPPET_RADIUS = 60;
const MAX_URL_LENGTH = 8192;
export const SKIP_EXT =
  /\.(pdf|jpe?g|png|gif|webp|svg|ico|bmp|tiff?|mp[34]|m4a|wav|ogg|webm|mov|avi|zip|gz|tgz|bz2|7z|rar|dmg|exe|pkg|deb|rpm|iso|woff2?|ttf|otf|eot|css|js|mjs|json|xml|rss|atom|csv|md|markdown|xlsx?|docx?|pptx?)$/i;

// --- character encoding ---

const CHARSET_RE = /charset\s*=\s*["']?([^"'\s;>/]+)/i;
const SNIFF_BYTES = 4096;

// The canonical name of a WHATWG encoding label, or null if Node can't decode it.
function encodingFor(label) {
  try { return new TextDecoder(label).encoding; } catch { return null; }
}

// The body's encoding, as browsers decide it: byte order mark, then the
// Content-Type charset, then a <meta charset> / http-equiv near the top of the
// page. null = nothing declared (decodeBody then tries UTF-8, else windows-1252).
export function sniffEncoding(bytes, contentType = "") {
  if (bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) return "utf-8";
  if (bytes[0] === 0xfe && bytes[1] === 0xff) return "utf-16be";
  if (bytes[0] === 0xff && bytes[1] === 0xfe) return "utf-16le";
  const header = CHARSET_RE.exec(contentType)?.[1];
  const fromHeader = header && encodingFor(header);
  if (fromHeader) return fromHeader;
  const head = new TextDecoder("windows-1252").decode(bytes.subarray(0, SNIFF_BYTES));
  for (const [tag] of head.matchAll(/<meta\b[^>]*>/gi)) {
    const label = CHARSET_RE.exec(tag)?.[1];
    const enc = label && encodingFor(label);
    // A <meta> can't declare UTF-16: the bytes it was read from are ASCII-compatible.
    if (enc) return enc.startsWith("utf-16") ? "utf-8" : enc === "x-user-defined" ? "windows-1252" : enc;
  }
  return null;
}

export function decodeBody(bytes, contentType = "") {
  const enc = sniffEncoding(bytes, contentType);
  if (enc) return new TextDecoder(enc).decode(bytes);
  try {
    // stream: a multibyte character cut off by the size cap isn't an error.
    return new TextDecoder("utf-8", { fatal: true }).decode(bytes, { stream: true });
  } catch {
    return new TextDecoder("windows-1252").decode(bytes);
  }
}

// --- HTML to text ---

const ENTITY_RE = /&(nbsp|amp|lt|gt|quot|#39|apos);|&#(\d+);|&#[xX]([0-9a-fA-F]+);/g;
const NAMED_ENTITIES = { nbsp: " ", amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'", apos: "'" };

// Decodes the common named entities and numeric character references, once
// (so "&amp;#39;" stays "&#39;").
export function decodeEntities(text) {
  return text.replace(ENTITY_RE, (_, named, dec, hex) =>
    named ? NAMED_ENTITIES[named] : safeCodePoint(dec ? Number(dec) : parseInt(hex, 16)));
}

function safeCodePoint(n) {
  try { return String.fromCodePoint(n); } catch { return " "; }
}

// Blocks dropped with their content, removed one kind after another as the
// original chain of regex replaces did (`<script[\s\S]*?<\/script>`, then
// style, noscript and comments), so a "</style>" inside a script doesn't count.
const BLOCKS = [
  { open: /<script/gi, close: /<\/script>/gi },
  { open: /<style/gi, close: /<\/style>/gi },
  { open: /<noscript/gi, close: /<\/noscript>/gi },
  { open: /<!--/g, close: /-->/g },
];
const CHUNK_CHARS = 256 * 1024;

// [start, end, start, end, …] of the blocks to drop: sorted and disjoint.
// Each kind skips matches inside blocks of the kinds before it.
function blockRanges(html) {
  let ranges = [];
  for (const { open, close } of BLOCKS) {
    const found = [];
    let k = 0; // first earlier range that could contain the next match
    const outside = (re, from) => {
      for (;;) {
        re.lastIndex = from;
        const m = re.exec(html);
        if (!m) return null;
        while (k < ranges.length && ranges[k + 1] <= m.index) k += 2;
        if (k < ranges.length && ranges[k] <= m.index) from = ranges[k + 1];
        else return m;
      }
    };
    let from = 0;
    for (;;) {
      const o = outside(open, from);
      if (!o) break;
      const c = outside(close, o.index + o[0].length);
      if (!c) break;
      found.push(o.index, c.index + c[0].length);
      from = c.index + c[0].length;
    }
    ranges = mergeRanges(ranges, found);
  }
  return ranges;
}

// Union of two sorted range lists; a later block can contain earlier ones.
function mergeRanges(a, b) {
  if (!b.length) return a;
  const all = [];
  for (let i = 0, j = 0; i < a.length || j < b.length;) {
    const takeA = j >= b.length || (i < a.length && a[i] <= b[j]);
    const [s, e] = takeA ? [a[i], a[i + 1]] : [b[j], b[j + 1]];
    if (takeA) i += 2; else j += 2;
    if (all.length && s < all[all.length - 1]) all[all.length - 1] = Math.max(all[all.length - 1], e);
    else all.push(s, e);
  }
  return all;
}

// Page text: drops script/style/noscript blocks, comments and tags, decodes
// entities and collapses whitespace. Same result as the original chain of
// full-string regex replaces, but in one scan that builds the text in small
// chunks, so a 30 MB page doesn't need several full-size copies. Every search
// moves forward, which keeps it linear even on pages full of unclosed "<".
export function htmlToText(html) {
  const chunks = [];
  let parts = [];
  let partsChars = 0;
  let lastSpace = true; // drops leading whitespace (trim)
  const flush = () => {
    // A replacer function: with a replacement string, V8 keeps the result as
    // a tree of pieces several times the text's size.
    let s = decodeEntities(parts.join("")).replace(/\s+/g, () => " ");
    parts = [];
    partsChars = 0;
    if (lastSpace && s.charCodeAt(0) === 32) s = s.slice(1);
    if (s) {
      chunks.push(s);
      lastSpace = s.charCodeAt(s.length - 1) === 32;
    }
  };
  // Text up to `to`. Long runs are flushed after a whitespace character,
  // which no entity contains; whitespace at chunk edges collapses as usual.
  const text = (from, to) => {
    while (to - from > CHUNK_CHARS) {
      const cut = lastWhitespace(html, from + CHUNK_CHARS, from + 1);
      if (cut < 0) break;
      parts.push(html.slice(from, cut + 1));
      flush();
      from = cut + 1;
    }
    if (to > from) {
      parts.push(html.slice(from, to));
      partsChars += to - from;
    }
  };
  // A tag or block becomes one space. Entities can't span it, so it's a safe
  // place to flush.
  const space = () => {
    parts.push(" ");
    if (++partsChars > CHUNK_CHARS) flush();
  };

  const ranges = blockRanges(html);
  // First ">" at or after `from` that isn't inside a dropped block, or -1.
  let gtFrom = Infinity;
  let gtAt = -1;
  let gk = 0;
  const tagEnd = (from) => {
    if (from >= gtFrom && (gtAt === -1 || gtAt >= from)) return gtAt;
    gtFrom = from;
    for (;;) {
      gtAt = html.indexOf(">", from);
      if (gtAt === -1) return -1;
      while (gk < ranges.length && ranges[gk + 1] <= gtAt) gk += 2;
      if (gk < ranges.length && ranges[gk] <= gtAt) from = ranges[gk + 1];
      else return gtAt;
    }
  };

  let k = 0; // next block
  let cur = 0; // scan position
  let pos = 0; // start of text not yet added
  for (;;) {
    const block = k < ranges.length ? ranges[k] : Infinity;
    let lt = html.indexOf("<", cur);
    if (lt === -1) lt = Infinity;
    if (block === Infinity && lt === Infinity) break;
    if (block <= lt) {
      text(pos, block);
      space();
      cur = pos = ranges[k + 1];
      k += 2;
      continue;
    }
    // A tag is "<", at least one character, then the next ">" (`<[^>]+>`),
    // where a dropped block counts as a space.
    const gt = lt + 1 < html.length && html[lt + 1] !== ">" ? tagEnd(lt + 1) : -1;
    if (gt === -1) { // a literal "<"
      cur = lt + 1;
      continue;
    }
    text(pos, lt);
    space();
    while (k < ranges.length && ranges[k] < gt) k += 2; // blocks inside the tag
    cur = pos = gt + 1;
  }
  text(pos, html.length);
  flush();
  const out = chunks.join("");
  return lastSpace ? out.slice(0, -1) : out;
}

function lastWhitespace(s, from, min) {
  for (let i = from; i >= min; i--) if (/\s/.test(s[i])) return i;
  return -1;
}

export function pageTitle(html) {
  const m = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(html);
  return m ? decodeEntities(m[1]).replace(/\s+/g, " ").trim() : "";
}

// --- links ---

export function extractLinks(html, baseUrl) {
  const base = /<base\b[^>]*?\bhref\s*=\s*["']?([^"'\s>]+)/i.exec(html);
  if (base) {
    try { baseUrl = new URL(base[1], baseUrl).href; } catch { /* keep page url */ }
  }
  const links = new Set();
  const re = /<a\b[^>]*?\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s">]+))/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const raw = decodeEntities((m[1] ?? m[2] ?? m[3] ?? "").trim());
    if (!raw || raw.startsWith("#") || /^(javascript|mailto|tel|data):/i.test(raw)) continue;
    if (raw.length > MAX_URL_LENGTH) continue;
    try {
      const url = new URL(raw, baseUrl);
      // Not fetchable: other schemes, files we can't search, and URLs with
      // credentials (fetch() refuses them).
      if ((url.protocol === "http:" || url.protocol === "https:") && !SKIP_EXT.test(url.pathname) &&
          !url.username && !url.password) {
        url.hash = "";
        links.add(url.href);
      }
    } catch { /* skip malformed URLs */ }
  }
  return [...links];
}

export function normalizeUrl(href) {
  try {
    const u = new URL(href);
    u.hash = "";
    let s = u.href;
    if (s.endsWith("/") && u.pathname !== "/") s = s.slice(0, -1);
    return s;
  } catch {
    return href;
  }
}

// The page's main content: the first <main>, role="main" element or <article>,
// found by counting nested tags of the same name. Falls back to the whole page.
export function mainContent(html) {
  const open =
    /<main\b[^>]*>/i.exec(html) ||
    /<([a-z][a-z0-9]*)\b[^>]*\brole\s*=\s*["']?main\b[^>]*>/i.exec(html) ||
    /<article\b[^>]*>/i.exec(html);
  if (!open) return html;
  const tag = (open[1] || /^<([a-z0-9]+)/i.exec(open[0])[1]).toLowerCase();
  const re = new RegExp(`<(/?)${tag}\\b[^>]*>`, "gi");
  re.lastIndex = open.index + open[0].length;
  let depth = 1;
  let m;
  while ((m = re.exec(html)) !== null) {
    depth += m[1] ? -1 : 1;
    if (depth === 0) return html.slice(open.index, m.index);
  }
  return html.slice(open.index);
}

// --- matching ---

const WORD_RE = /\w/;
const isWordChar = (c) => c !== undefined && WORD_RE.test(c);

// Lowercase without changing the string's length (toLowerCase turns "İ" into
// two code units, which would shift every later match index).
export function foldCase(s) {
  const lower = s.toLowerCase();
  if (lower.length === s.length) return lower;
  let out = "";
  for (const ch of s) {
    const l = ch.toLowerCase();
    out += l.length === ch.length ? l : ch;
  }
  return out;
}

export function findMatches(text, { query, mode, caseSensitive }) {
  if (mode === "regex") {
    const re = new RegExp(query, caseSensitive ? "g" : "gi");
    const out = [];
    let m;
    let guard = 0;
    while ((m = re.exec(text)) !== null) {
      out.push({ index: m.index, length: m[0].length || 1 });
      if (m.index === re.lastIndex) re.lastIndex++;
      if (++guard > 100000) break;
    }
    return out;
  }
  const haystack = caseSensitive ? text : foldCase(text);
  const needle = caseSensitive ? query : foldCase(query);
  let indices = kmpSearch(haystack, needle);
  if (mode === "word") {
    indices = indices.filter((i) => !isWordChar(text[i - 1]) && !isWordChar(text[i + query.length]));
  }
  return indices.map((i) => ({ index: i, length: query.length }));
}

export function searchText(text, cfg, maxSnippets) {
  const matches = findMatches(text, cfg);
  const snippets = [];
  let lastEnd = -1;
  for (const { index, length } of matches) {
    if (snippets.length >= maxSnippets) break;
    if (index < lastEnd) continue; // skip matches inside the previous snippet
    const start = Math.max(0, index - SNIPPET_RADIUS);
    const end = Math.min(text.length, index + length + SNIPPET_RADIUS);
    snippets.push(
      (start > 0 ? "…" : "") + text.slice(start, index) + "[[" + text.slice(index, index + length) +
        "]]" + text.slice(index + length, end) + (end < text.length ? "…" : "")
    );
    lastEnd = end;
  }
  return { matchCount: matches.length, snippets };
}

// --- one page ---

// Everything the crawler needs from one fetched page. `job` is
// { bytes, contentType, url, query, mode, caseSensitive, snippets, mainOnly, links }.
export function processPage(job) {
  const html = decodeBody(job.bytes, job.contentType);
  job.bytes = null; // let the raw body go before the text is built
  const text = htmlToText(job.mainOnly ? mainContent(html) : html);
  const found = searchText(text, job, job.snippets);
  return {
    title: pageTitle(html),
    textLength: text.length,
    hasScripts: /<script\b/i.test(html),
    ...found,
    links: job.links ? extractLinks(html, job.url) : [],
  };
}
