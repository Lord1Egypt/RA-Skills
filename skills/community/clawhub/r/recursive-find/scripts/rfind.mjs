#!/usr/bin/env node
// rfind — Ctrl+F, but recursive. Headless port of grtwrn/recursive-find
// (worker.js + kmp.js): fetch a page, strip it to text, search it, follow its
// links breadth-first to --depth, and print only the pages that match.
// The crawler lives in crawl.mjs; this file parses arguments and prints.

import { crawl, formatText, resolveOptions, startError, toJSON } from "./crawl.mjs";

const USAGE = `usage: rfind <url> <query> [options]

  --depth N         0 = start page only, 1 = + pages it links to (default 1, max 3)
  --max-pages N     stop fetching after N pages (default 100, max 1000)
  --max-seconds S   stop the whole crawl after S seconds (default 120)
  --mode M          text (default) | word | regex
  --case            case-sensitive
  --any-site        follow links to other sites (default: same origin only)
  --within PATH     only follow links whose path starts with PATH (e.g. /docs/)
  --first           stop at the first page that matches
  --limit N         print at most N matching pages (default 20)
  --snippets N      snippets per page (default 3)
  --concurrency N   parallel fetches (default 4, max 8)
  --timeout S       per-page timeout in seconds (default 10)
  --main            search only the page's main content (<main>, role="main" or
                    <article>), skipping nav, sidebars and footers when present
  --ignore-robots   don't honor robots.txt
  --json            JSON output`;

function parseArgs(argv) {
  const opts = { json: false };
  const pos = [];
  const num = (v, name) => {
    const n = Number(v);
    if (!Number.isFinite(n) || n < 0) die(`bad value for ${name}: ${v}`);
    return Math.floor(n);
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) die(`${a} needs a value`);
      return argv[++i];
    };
    switch (a) {
      case "-h": case "--help": console.log(USAGE); process.exit(0);
      case "--depth": opts.depth = num(next(), a); break;
      case "--max-pages": opts.maxPages = num(next(), a); break;
      case "--max-seconds": opts.maxSeconds = num(next(), a); break;
      case "--mode": opts.mode = next(); break;
      case "--case": opts.caseSensitive = true; break;
      case "--any-site": opts.anySite = true; break;
      case "--within": opts.within = next(); break;
      case "--first": opts.first = true; break;
      case "--limit": opts.limit = num(next(), a); break;
      case "--snippets": opts.snippets = num(next(), a); break;
      case "--concurrency": opts.concurrency = num(next(), a); break;
      case "--timeout": opts.timeout = num(next(), a); break;
      case "--main": opts.mainOnly = true; break;
      case "--ignore-robots": opts.robots = false; break;
      case "--json": opts.json = true; break;
      default:
        if (a.startsWith("--")) die(`unknown option ${a}`);
        pos.push(a);
    }
  }
  if (pos.length !== 2) die(USAGE);
  [opts.url, opts.query] = pos;
  if (opts.mode !== undefined && !["text", "word", "regex"].includes(opts.mode)) {
    die(`--mode must be text, word or regex`);
  }
  try {
    return { ...resolveOptions(opts), json: opts.json };
  } catch (e) {
    die(e.message);
  }
}

function die(msg) {
  console.error(msg);
  process.exit(2);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const result = await crawl(opts);
  console.log(opts.json ? JSON.stringify(toJSON(result, opts), null, 2) : formatText(result, opts));
  process.exit(startError(result) ? 1 : 0);
}

main().catch((e) => {
  console.error(e?.stack || String(e));
  process.exit(1);
});
