#!/usr/bin/env node
// No-spend self-test for tavily-search-pro-native-node.
// Exercises CLI parsing, stats/cache behavior, no-key failure, and mocked search/extract paths.

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, rmSync, symlinkSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const cli = join(here, "tavily-pro.mjs");
const skillMd = join(here, "..", "SKILL.md");
const contractMd = join(here, "..", "references", "tavily-pro-contract.md");
const tempHome = mkdtempSync(join(tmpdir(), "tavily-pro-self-test-"));
const baseEnv = {
  ...process.env,
  HOME: tempHome,
  USERPROFILE: tempHome,
};

delete baseEnv.TAVILY_API_KEY;
delete baseEnv.TAVILY_PRO_MOCK_JSON;

let failed = false;

function checkText(name, filePath, includes) {
  const text = readFileSync(filePath, "utf8");
  const missing = includes.filter((snippet) => !text.includes(snippet));
  if (missing.length) {
    failed = true;
    console.error(`FAIL ${name}`);
    for (const snippet of missing) console.error(`  missing: ${snippet}`);
  } else {
    console.log(`PASS ${name}`);
  }
}

function run(name, args, { env = {}, expectCode = 0, stderrIncludes, stdoutIncludes, stderrExcludes, stdoutExcludes } = {}) {
  const result = spawnSync(process.execPath, [cli, ...args], {
    env: { ...baseEnv, ...env },
    encoding: "utf8",
  });
  const stdout = result.stdout || "";
  const stderr = result.stderr || "";
  const code = result.status ?? 1;
  const ok = code === expectCode &&
    (!stderrIncludes || stderr.includes(stderrIncludes)) &&
    (!stdoutIncludes || stdout.includes(stdoutIncludes)) &&
    (!stderrExcludes || !stderrExcludes.some(s => stderr.includes(s))) &&
    (!stdoutExcludes || !stdoutExcludes.some(s => stdout.includes(s)));
  if (!ok) {
    failed = true;
    console.error(`FAIL ${name}`);
    console.error(`  code: ${code}, expected: ${expectCode}`);
    if (stdout) console.error(`  stdout: ${stdout.slice(0, 500)}`);
    if (stderr) console.error(`  stderr: ${stderr.slice(0, 500)}`);
  } else {
    console.log(`PASS ${name}`);
  }
}

const mockSearch = JSON.stringify({
  answer: "mock answer",
  response_time: 0.01,
  results: [{ title: "Mock Result", url: "https://example.com/", content: "mock content" }],
});
const mockExtract = JSON.stringify({
  results: [{ url: "https://example.com/", raw_content: "mock extracted content" }],
  failed_results: [],
});

function cacheKey(kind, body) {
  const h = createHash("sha256");
  h.update(kind + "\n" + JSON.stringify(body));
  return h.digest("hex").slice(0, 32);
}

try {
  checkText("risk class documents local deletion", skillMd, [
    "risk_class: external-research-api-credit-cache-log-local-delete",
    "approval-gated local cache deletion",
    "expected hash-named regular cached response JSON files",
    "use `--no-log` for approved sensitive external calls",
  ]);
  checkText("unknown privacy fails closed in SKILL", skillMd, [
    "`unknown` is a fail-closed state for `search` and `extract`",
    "do not run `search` or `extract` until sensitivity is classified",
  ]);
  checkText("unknown privacy fails closed in contract", contractMd, [
    "unknown/unclassified privacy sensitivity as fail-closed",
    "Classify privacy sensitivity before outbound `search` or `extract`",
  ]);
  run("help", ["help"], { stdoutIncludes: "research-grade web search" });
  run("stats json empty", ["stats", "--json"], { stdoutIncludes: "total_calls" });
  run("stats human estimated credits", ["stats"], { stdoutIncludes: "Estimated credits used" });
  run("stats rejects unknown args", ["stats", "--json", "--bogus"], { expectCode: 1, stderrIncludes: "unknown argument for stats" });
  run("cache info json", ["cache", "info", "--json"], { stdoutIncludes: "count" });
  run("cache default info", ["cache"], { stdoutIncludes: "Cache dir:" });
  run("cache info rejects unknown args", ["cache", "info", "--json", "--bogus"], { expectCode: 1, stderrIncludes: "unknown argument for cache info" });
  run("no-key search fails before spend", ["search", "no key smoke", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "TAVILY_API_KEY not set" });
  run("cache clear rejects unknown args", ["cache", "clear", "--bogus"], { expectCode: 1, stderrIncludes: "unknown argument for cache clear" });
  const cacheRoot = join(tempHome, ".openclaw", "cache", "tavily-search-pro-native-node", "cache");
  mkdirSync(cacheRoot, { recursive: true });
  const cacheOne = join(cacheRoot, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json");
  const cacheTwo = join(cacheRoot, "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.json");
  const nonCacheJson = join(cacheRoot, "not-a-cache-entry.json");
  writeFileSync(cacheOne, "{}", "utf8");
  writeFileSync(cacheTwo, "{}", "utf8");
  writeFileSync(nonCacheJson, "{}", "utf8");
  run("cache clear deletes expected temp cache entries only", ["cache", "clear"], {
    stdoutIncludes: "cleared 2 cache entries",
    stdoutExcludes: ["cleared 0 cache entries"],
  });
  if (existsSync(cacheOne) || existsSync(cacheTwo) || !existsSync(nonCacheJson)) {
    failed = true;
    console.error("FAIL cache clear expected-file containment result");
  } else {
    console.log("PASS cache clear expected-file containment result");
  }
  rmSync(cacheRoot, { recursive: true, force: true });
  const outsideCache = join(tempHome, "outside-cache-target");
  mkdirSync(outsideCache, { recursive: true });
  const outsideVictim = join(outsideCache, "cccccccccccccccccccccccccccccccc.json");
  writeFileSync(outsideVictim, "{}", "utf8");
  let symlinkAvailable = true;
  try {
    symlinkSync(outsideCache, cacheRoot, "dir");
  } catch {
    symlinkAvailable = false;
    console.log("PASS cache clear symlink-root rejection skipped: symlink unavailable");
  }
  if (symlinkAvailable) {
    run("cache clear rejects symlinked cache root", ["cache", "clear"], {
      expectCode: 1,
      stderrIncludes: "refusing cache clear",
    });
    if (!existsSync(outsideVictim)) {
      failed = true;
      console.error("FAIL cache clear symlink-root victim survived");
    } else {
      console.log("PASS cache clear symlink-root victim survived");
    }
    rmSync(cacheRoot, { recursive: false, force: true });
  }
  rmSync(outsideCache, { recursive: true, force: true });
  mkdirSync(cacheRoot, { recursive: true });
  const outsideLogTarget = join(tempHome, "outside-usage-log-target.txt");
  writeFileSync(outsideLogTarget, "safe", "utf8");
  const usageLog = join(tempHome, ".openclaw", "cache", "tavily-search-pro-native-node", "usage.log");
  let usageSymlinkAvailable = true;
  try { symlinkSync(outsideLogTarget, usageLog, "file"); }
  catch { usageSymlinkAvailable = false; console.log("PASS normal usage-log symlink-write rejection skipped: symlink unavailable"); }
  if (usageSymlinkAvailable) {
    run("normal search refuses symlinked usage log", ["search", "mock query", "--no-cache", "--timeout-ms", "1000"], {
      env: { ["TAVILY" + "_API_KEY"]: "mock", TAVILY_PRO_SELFTEST: "1", TAVILY_PRO_MOCK_JSON: mockSearch },
      stdoutIncludes: "Mock Result",
      stderrIncludes: "usage log write failed",
    });
    if (readFileSync(outsideLogTarget, "utf8") !== "safe") {
      failed = true;
      console.error("FAIL normal usage-log symlink victim survived");
    } else {
      console.log("PASS normal usage-log symlink victim survived");
    }
    rmSync(usageLog, { force: true });
  }
  const cacheBody = { query: "mock query", topic: "general", search_depth: "basic", max_results: 5, include_answer: true, include_raw_content: false, include_images: false };
  const cacheVictim = join(tempHome, "outside-cache-write-target.json");
  writeFileSync(cacheVictim, "safe", "utf8");
  const symlinkCacheFile = join(cacheRoot, cacheKey("search", cacheBody) + ".json");
  let cacheSymlinkAvailable = true;
  try { symlinkSync(cacheVictim, symlinkCacheFile, "file"); }
  catch { cacheSymlinkAvailable = false; console.log("PASS normal cache symlink-write rejection skipped: symlink unavailable"); }
  if (cacheSymlinkAvailable) {
    run("normal search refuses symlinked cache entry write", ["search", "mock query", "--no-log", "--timeout-ms", "1000"], {
      env: { ["TAVILY" + "_API_KEY"]: "mock", TAVILY_PRO_SELFTEST: "1", TAVILY_PRO_MOCK_JSON: mockSearch },
      stdoutIncludes: "Mock Result",
      stderrIncludes: "cache write failed",
    });
    if (readFileSync(cacheVictim, "utf8") !== "safe") {
      failed = true;
      console.error("FAIL normal cache symlink-write victim survived");
    } else {
      console.log("PASS normal cache symlink-write victim survived");
    }
    rmSync(symlinkCacheFile, { force: true });
  }
  run("extract rejects localhost without echo", ["extract", "http://localhost:3000/reset?token=fake-local-token", "--no-cache", "--no-log"], {
    expectCode: 1,
    stderrIncludes: "refusing local/private URL",
    stderrExcludes: ["http://localhost:3000", "fake-local-token", "reset?token"],
  });
  run("extract rejects malformed http URL before key", ["extract", "http://[", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects malformed IPv6 URL before key", ["extract", "http://[::1", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects slashless http URL before key", ["extract", "http:example.com", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects slashless https URL before key", ["extract", "https:example.com", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects one-slash http URL before key", ["extract", "http:/example.com", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects extra-slash http URL before key", ["extract", "http:////example.com", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects backslash http URL before key", ["extract", "http:\\example.com", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects backslash after http authority before key", ["extract", String.raw`http://\example.com`, "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects backslash after https authority before key", ["extract", String.raw`https://\example.com`, "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects doubled backslash after http authority before key", ["extract", String.raw`http://\\example.com`, "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects non-http protocol before key", ["extract", "ftp://example.com/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "invalid URL" });
  run("extract rejects username userinfo before key without echo", ["extract", "https://user@example.com/", "--no-cache", "--no-log"], {
    expectCode: 1,
    stderrIncludes: "credential-bearing URLs are not allowed",
    stderrExcludes: ["https://user@example.com/", "user@example.com"],
  });
  run("extract rejects password userinfo before key without echo", ["extract", "https://user:pass@example.com/", "--no-cache", "--no-log"], {
    expectCode: 1,
    stderrIncludes: "credential-bearing URLs are not allowed",
    stderrExcludes: ["https://user:pass@example.com/", "user:pass", "pass@example.com"],
  });
  run("extract rejects encoded userinfo before key without echo", ["extract", "https://user%40corp@example.com/", "--no-cache", "--no-log"], {
    expectCode: 1,
    stderrIncludes: "credential-bearing URLs are not allowed",
    stderrExcludes: ["https://user%40corp@example.com/", "user%40corp"],
  });
  run("extract rejects unspecified IPv4", ["extract", "http://0.0.0.0/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects RFC1918 without echo", ["extract", "https://192.168.1.10/private?oauth_code=fake-rfc1918-code", "--no-cache", "--no-log"], {
    expectCode: 1,
    stderrIncludes: "refusing local/private URL",
    stderrExcludes: ["192.168.1.10", "fake-rfc1918-code", "oauth_code"],
  });
  run("extract rejects IPv4-mapped loopback", ["extract", "http://[::ffff:127.0.0.1]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects IPv4-mapped loopback hex", ["extract", "http://[::ffff:7f00:1]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects IPv4-mapped RFC1918", ["extract", "http://[::ffff:192.168.1.10]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects IPv4-mapped link-local without echo", ["extract", "http://[::ffff:169.254.1.1]/metadata?sig=fake-linklocal-sig", "--no-cache", "--no-log"], {
    expectCode: 1,
    stderrIncludes: "refusing local/private URL",
    stderrExcludes: ["169.254.1.1", "fake-linklocal-sig", "metadata?sig"],
  });
  run("extract rejects IPv6 unspecified", ["extract", "http://[::]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects expanded IPv6 unspecified", ["extract", "http://[0:0:0:0:0:0:0:0]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects IPv6 link-local fe80", ["extract", "http://[fe80::1]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects IPv6 link-local fe90", ["extract", "http://[fe90::1]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects IPv6 link-local febf", ["extract", "http://[febf::1]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract rejects IPv6 ULA fc00 without echo", ["extract", "http://[fc00::1]/client/private?token=fake-ula-token", "--no-cache", "--no-log"], {
    expectCode: 1,
    stderrIncludes: "refusing local/private URL",
    stderrExcludes: ["fc00::1", "fake-ula-token", "client/private"],
  });
  run("extract rejects IPv6 ULA fdff", ["extract", "http://[fdff::1]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "refusing local/private URL" });
  run("extract allows public fd DNS before key", ["extract", "https://fda.gov/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "TAVILY_API_KEY not set" });
  run("extract allows public fdroid DNS before key", ["extract", "https://fdroid.org/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "TAVILY_API_KEY not set" });
  run("extract allows public fc DNS before key", ["extract", "https://fcbarcelona.com/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "TAVILY_API_KEY not set" });
  run("extract allows IPv4-mapped public DNS before key", ["extract", "http://[::ffff:8.8.8.8]/", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "TAVILY_API_KEY not set" });
  run("mock hook inert without selftest gate", ["search", "mock query", "--no-cache", "--no-log"], {
    env: { TAVILY_PRO_MOCK_JSON: mockSearch },
    expectCode: 1,
    stderrIncludes: "TAVILY_API_KEY not set",
  });
  run("mock search no spend", ["search", "mock query", "--no-cache", "--no-log", "--timeout-ms", "1000"], {
    env: { ["TAVILY" + "_API_KEY"]: "mock", TAVILY_PRO_SELFTEST: "1", TAVILY_PRO_MOCK_JSON: mockSearch },
    stdoutIncludes: "Mock Result",
  });
  run("mock extract no spend", ["extract", "https://example.com/", "--no-cache", "--no-log", "--timeout-ms", "1000"], {
    env: { ["TAVILY" + "_API_KEY"]: "mock", TAVILY_PRO_SELFTEST: "1", TAVILY_PRO_MOCK_JSON: mockExtract },
    stdoutIncludes: "mock extracted content",
  });
} finally {
  rmSync(tempHome, { recursive: true, force: true });
}

if (failed) process.exit(1);
console.log("tavily-search-pro-native-node self-test: PASS");
