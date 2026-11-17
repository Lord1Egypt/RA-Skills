#!/usr/bin/env node
/**
 * weekly-gitlog — compact weekly changelog from a git repo.
 * Output: grouped by author, then by day. No dependencies.
 *
 * Usage:
 *   node weekly-gitlog.mjs [--days 7] [--repo /path] [--json] [--include-merges]
 */
import { execFileSync } from "node:child_process";

function parseArgs(argv) {
  const opts = { days: 7, repo: null, json: false, includeMerges: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--days") opts.days = Number(argv[++i]);
    else if (a === "--repo") opts.repo = argv[++i];
    else if (a === "--json") opts.json = true;
    else if (a === "--include-merges") opts.includeMerges = true;
    else if (a === "-h" || a === "--help") {
      console.log("usage: weekly-gitlog.mjs [--days N] [--repo PATH] [--json] [--include-merges]");
      process.exit(0);
    } else {
      console.error(`unknown argument: ${a}`);
      process.exit(2);
    }
  }
  if (!Number.isFinite(opts.days) || opts.days <= 0) {
    console.error("--days must be a positive integer");
    process.exit(2);
  }
  return opts;
}

function main() {
  const opts = parseArgs(process.argv);
  const gitArgs = ["log", `--since=${opts.days}.days`, "--no-merges", "--pretty=format:%ae%x1f%ad%x1f%h%x1f%s", "--date=short"];
  if (opts.includeMerges) {
    const i = gitArgs.indexOf("--no-merges");
    if (i >= 0) gitArgs.splice(i, 1);
  }
  const cwd = opts.repo || process.cwd();
  let raw;
  try {
    raw = execFileSync("git", gitArgs, { cwd, encoding: "utf8" });
  } catch (err) {
    const msg = err && err.stderr ? String(err.stderr).trim() : String(err.message);
    console.error(`git log failed: ${msg}`);
    process.exit(1);
  }
  if (!raw.trim()) {
    console.error(`no commits in the last ${opts.days} day(s)`);
    process.exit(3);
  }

  // group: author -> day -> [ {hash, subject} ]
  const authors = new Map();
  for (const line of raw.split("\n")) {
    if (!line) continue;
    const [author, day, hash, subject] = line.split("\x1f");
    if (!authors.has(author)) authors.set(author, new Map());
    const days = authors.get(author);
    if (!days.has(day)) days.set(day, []);
    days.get(day).push({ hash, subject });
  }

  if (opts.json) {
    const out = {};
    for (const [author, days] of authors) {
      out[author] = Object.fromEntries(days);
    }
    console.log(JSON.stringify(out, null, 2));
    return;
  }

  const authorNames = [...authors.keys()].sort();
  for (const author of authorNames) {
    console.log(`## ${author}`);
    const days = authors.get(author);
    for (const day of [...days.keys()].sort().reverse()) {
      console.log(`### ${day}`);
      for (const { hash, subject } of days.get(day)) {
        console.log(`  ${hash} ${subject}`);
      }
    }
    console.log("");
  }
}

main();
