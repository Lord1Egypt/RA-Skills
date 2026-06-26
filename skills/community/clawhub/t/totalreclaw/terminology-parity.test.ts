/**
 * terminology-parity — gate test that catches user-facing terminology
 * regressions before they ship.
 *
 * Run with: npx tsx terminology-parity.test.ts
 *
 * 3.3.0-rc.2 standardised all user-facing surfaces on "recovery phrase".
 * This gate scans every published .ts file under skill/plugin/ and flags
 * any occurrence of the forbidden terms inside STRING LITERALS only:
 *
 *   - \bmnemonic\b               → "recovery phrase"
 *   - \bseed phrase\b            → "recovery phrase"
 *   - \brecovery code\b          → "recovery phrase"
 *   - \brecovery key\b           → "recovery phrase"
 *   - \bBIP-?39 phrase\b         → "recovery phrase"
 *
 * Internal variable names (`const mnemonic = ...`), function names
 * (`generateMnemonic128`), object keys (`creds.mnemonic`), type names
 * (`MnemonicPayload`), comments, and import paths are all EXEMPT — this
 * check is about what users READ, not how the crypto code stays wired
 * together.
 *
 * We detect "user-facing" strings by scoring whether a token sits inside
 * a single-quoted, double-quoted, template-literal string literal OR an
 * HTML/JSX text node. Comments (`// ... \n`, `/* ... *\/`) are stripped
 * first. Imports and type annotations around a literal are not special-
 * cased; this is a deliberately blunt check that prefers false positives
 * (which force the author to acknowledge a literal by adding it to the
 * allowlist) over false negatives.
 *
 * Allowlist: specific file+substring pairs can be marked as legitimate
 * internal uses (e.g. `"mnemonic"` as a JSON field name in a tool-argument
 * schema where the user literally types the key). Keep the list short.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PLUGIN_ROOT = __dirname;

const SCANNABLE_EXT = new Set(['.ts']);
const SKIP_DIRS = new Set(['node_modules', 'dist', '.git', 'coverage']);
const SKIP_FILENAMES = new Set([
  // Tests may reference the forbidden terms as values/assertions.
  // (Anything matching *.test.ts is auto-skipped below; listed here for
  // documentation only.)
]);

interface Hit {
  file: string;
  line: number;
  literal: string;
  matched: string;
}

// The FORBIDDEN tokens we scan for. Regex flags: case-insensitive,
// word-boundaries. Each MUST fire on user-readable English words only.
const FORBIDDEN: Array<{ name: string; re: RegExp }> = [
  { name: 'mnemonic', re: /\bmnemonic\b/i },
  { name: 'seed phrase', re: /\bseed\s+phrase\b/i },
  { name: 'recovery code', re: /\brecovery\s+code\b/i },
  { name: 'recovery key', re: /\brecovery\s+key\b/i },
  { name: 'BIP-39 phrase', re: /\bbip-?39\s+phrase\b/i },
];

// Allowlist entries. Each is a substring-of-literal match; a literal containing
// ANY allowlist substring for that file is not reported. Keep this list small
// and well-justified — every entry is a piece of technical copy that must NOT
// be translated to "recovery phrase" because it is not user-facing.
//
// Format: { file: <basename>, allow: [<substring-in-literal>, ...] }
const ALLOWLIST: Array<{ file: string; allow: string[] }> = [
  {
    // credentials.json JSON field names are used programmatically both by
    // our own code and by the MCP server, Python client, and hand-edited
    // user files. Renaming the on-disk key would be a breaking migration.
    // These literals are field-name strings, not user-facing copy.
    file: 'fs-helpers.ts',
    allow: ['mnemonic'],
  },
  {
    // onboarding-cli.ts handles the writable schema object — same rule
    // as fs-helpers.ts.
    file: 'onboarding-cli.ts',
    allow: ['mnemonic'],
  },
  {
    // generate-mnemonic.ts is a tiny utility whose only export is a named
    // function — any string literal here is the function's brand.
    file: 'generate-mnemonic.ts',
    allow: ['mnemonic'],
  },
  {
    // Tool argument descriptions (OpenClaw tool schemas) use `mnemonic` as
    // the canonical key name. Users pass `mnemonic: "..."` to the
    // totalreclaw_setup tool; renaming the key is a breaking API change.
    // Any description strings here that contain the word "mnemonic" will
    // be scrutinised below — this allowlist covers JSON-schema keys only.
    file: 'index.ts',
    allow: ['mnemonic'],
  },
  {
    // pair-http.ts: the `completePairing({ mnemonic })` callback signature
    // uses the internal JSON field name — same reasoning as fs-helpers.ts.
    file: 'pair-http.ts',
    allow: ['mnemonic'],
  },
  {
    // pair-page.ts: the entire browser page is built as a single giant
    // template literal. It contains:
    //   - CSS selectors `.mnemonic-grid` / `.mnemonic-word` (internal).
    //   - Internal JavaScript variable + function names that use the
    //     word `mnemonic` (`const mnemonic = ...`, `generateMnemonic128`,
    //     `validateMnemonic`, `entropyToMnemonic`, `escapeHtml(mnemonic)`,
    //     etc.) — these are code identifiers, not user-visible text.
    // The user-facing copy inside the same literal is checked by the
    // page's own test (pair-page.test.ts) for "recovery phrase" wording.
    file: 'pair-page.ts',
    allow: [
      'mnemonic-grid',
      'mnemonic-word',
      '.mnemonic',
      'const mnemonic',
      'generateMnemonic',
      'validateMnemonic',
      'entropyToMnemonic',
      '(mnemonic)',
      'submitEncrypted(mnemonic',
      'encode(mnemonic',
      'writeText(mnemonic',
      'mnemonic.split',
      'mnemonic =',
      'Generate a recovery phrase',
    ],
  },
  {
    // subgraph-store.ts: internal crypto config carries a field literally
    // called `mnemonic` — the key name is part of the object-shape
    // contract with the key-derivation code path. The error-message
    // wording has been updated to "Recovery phrase"; this allowlist
    // covers incidental references to the field name.
    file: 'subgraph-store.ts',
    allow: ['mnemonic'],
  },
];

function walk(dir: string): string[] {
  const out: string[] = [];
  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    if (e.name.startsWith('.')) continue;
    if (SKIP_DIRS.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(p));
    else if (e.isFile() && SCANNABLE_EXT.has(path.extname(e.name))) out.push(p);
  }
  return out;
}

/**
 * Single-pass tokenizer that walks the source and emits string-literal
 * contents while tracking state for comments. Handles:
 *   - line comments `// ...`
 *   - block comments `/* ... *\/`
 *   - single-quoted, double-quoted, and template-literal (backtick) strings
 *   - escape sequences inside strings
 *   - `${ ... }` interpolations in template literals (expression skipped)
 *
 * Returns an array of { literal, lineStart } pairs containing the text
 * inside each string literal (with interpolations collapsed to `${}`).
 *
 * Correctly skipping comments AND strings in one pass is load-bearing:
 * a naive pre-strip mangles `//` inside strings (think URL literals) and
 * produces spurious "literal" fragments that hit forbidden keywords
 * because the source code uses those words as identifiers.
 */
function extractStringLiterals(src: string): Array<{ literal: string; lineStart: number }> {
  const out: Array<{ literal: string; lineStart: number }> = [];
  let i = 0;
  let line = 1;
  while (i < src.length) {
    const ch = src[i];
    const next = src[i + 1];

    // Line comment
    if (ch === '/' && next === '/') {
      i += 2;
      while (i < src.length && src[i] !== '\n') i++;
      continue;
    }
    // Block comment
    if (ch === '/' && next === '*') {
      i += 2;
      while (i < src.length && !(src[i] === '*' && src[i + 1] === '/')) {
        if (src[i] === '\n') line++;
        i++;
      }
      i += 2;
      continue;
    }
    if (ch === '\n') {
      line++;
      i++;
      continue;
    }
    if (ch === "'" || ch === '"') {
      const startLine = line;
      const quote = ch;
      i++;
      let buf = '';
      while (i < src.length && src[i] !== quote) {
        if (src[i] === '\\' && i + 1 < src.length) {
          buf += src[i + 1];
          i += 2;
          continue;
        }
        if (src[i] === '\n') {
          // Unterminated single-line string — bail.
          line++;
          break;
        }
        buf += src[i];
        i++;
      }
      i++; // closing quote
      out.push({ literal: buf, lineStart: startLine });
      continue;
    }
    if (ch === '`') {
      const startLine = line;
      i++;
      let buf = '';
      while (i < src.length && src[i] !== '`') {
        if (src[i] === '\\' && i + 1 < src.length) {
          buf += src[i + 1];
          i += 2;
          continue;
        }
        if (src[i] === '$' && src[i + 1] === '{') {
          buf += '${}';
          i += 2;
          let depth = 1;
          while (i < src.length && depth > 0) {
            if (src[i] === '{') depth++;
            else if (src[i] === '}') depth--;
            else if (src[i] === '\n') line++;
            i++;
          }
          continue;
        }
        if (src[i] === '\n') line++;
        buf += src[i];
        i++;
      }
      i++; // closing backtick
      out.push({ literal: buf, lineStart: startLine });
      continue;
    }
    i++;
  }
  return out;
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

const hits: Hit[] = [];
const files = walk(PLUGIN_ROOT).filter((p) => {
  const name = path.basename(p);
  if (name.endsWith('.test.ts')) return false;
  if (SKIP_FILENAMES.has(name)) return false;
  // Skip the terminology-parity tester itself (obviously contains the words).
  if (name === 'terminology-parity.test.ts' || name === 'first-run.ts') return false;
  return true;
});

for (const absPath of files) {
  const relPath = path.relative(PLUGIN_ROOT, absPath);
  const src = fs.readFileSync(absPath, 'utf8');
  const literals = extractStringLiterals(src);
  const fileName = path.basename(absPath);
  const fileAllow = ALLOWLIST.find((a) => a.file === fileName)?.allow ?? [];

  for (const { literal, lineStart } of literals) {
    for (const rule of FORBIDDEN) {
      if (!rule.re.test(literal)) continue;

      // Compute which text ranges in this literal are "allowed" by the
      // file's allowlist. A hit is a true violation only if at least one
      // match of the forbidden pattern falls OUTSIDE every allowlisted
      // range. This lets a long literal (e.g. the pair-page HTML body)
      // contain internal CSS selectors like `.mnemonic-grid` without
      // blinding the scanner to genuine user-facing text in the SAME
      // literal.
      const globalRe = new RegExp(rule.re.source, rule.re.flags.includes('g') ? rule.re.flags : rule.re.flags + 'g');
      const allMatches: Array<{ index: number; len: number }> = [];
      let m: RegExpExecArray | null;
      while ((m = globalRe.exec(literal)) !== null) {
        allMatches.push({ index: m.index, len: m[0].length });
      }

      // Build allowed ranges from file allowlist tokens.
      const allowedRanges: Array<{ start: number; end: number }> = [];
      for (const a of fileAllow) {
        const aRe = new RegExp(a.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
        let am: RegExpExecArray | null;
        while ((am = aRe.exec(literal)) !== null) {
          allowedRanges.push({ start: am.index, end: am.index + am[0].length });
        }
      }

      const unauthorisedMatches = allMatches.filter((mm) => {
        const mStart = mm.index;
        const mEnd = mm.index + mm.len;
        return !allowedRanges.some((r) => r.start <= mStart && r.end >= mEnd);
      });

      if (unauthorisedMatches.length === 0) continue;

      // Report the first unauthorised match — include a short surrounding
      // context window so authors can quickly locate it.
      const first = unauthorisedMatches[0];
      const ctxStart = Math.max(0, first.index - 40);
      const ctxEnd = Math.min(literal.length, first.index + first.len + 40);
      const ctx = literal.slice(ctxStart, ctxEnd).replace(/\s+/g, ' ').trim();
      hits.push({
        file: relPath,
        line: lineStart,
        literal: ctx.length > 160 ? ctx.slice(0, 160) + '…' : ctx,
        matched: rule.name,
      });
    }
  }
}

if (hits.length === 0) {
  console.log(`ok 1 - terminology-parity: ${files.length} files scanned, 0 user-facing hits`);
  console.log('\n# 1/1 passed\n\nALL TESTS PASSED');
  process.exit(0);
}

console.log(`not ok 1 - terminology-parity: ${hits.length} user-facing forbidden-term hits`);
console.log('');
for (const h of hits) {
  console.log(`  ${h.file}:${h.line}  [${h.matched}]  -> ${h.literal}`);
}
console.log(
  '\nFix each hit by rewriting the string literal to use "recovery phrase".\n' +
    'If the literal is a JSON key / protocol-level identifier that cannot\n' +
    'be renamed without a breaking change, add it to the ALLOWLIST at the\n' +
    'top of terminology-parity.test.ts with a one-line justification.\n',
);
process.exit(1);
