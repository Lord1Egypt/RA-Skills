#!/usr/bin/env node
// No-spend self-test for tavily-search-pro-native-node.
// Exercises CLI parsing, stats/cache behavior, no-key failure, and mocked search/extract paths.

import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const cli = join(here, "tavily-pro.mjs");
const tempHome = mkdtempSync(join(tmpdir(), "tavily-pro-self-test-"));
const baseEnv = {
  ...process.env,
  HOME: tempHome,
  USERPROFILE: tempHome,
};

delete baseEnv.TAVILY_API_KEY;
delete baseEnv.TAVILY_PRO_MOCK_JSON;

let failed = false;

function run(name, args, { env = {}, expectCode = 0, stderrIncludes, stdoutIncludes } = {}) {
  const result = spawnSync(process.execPath, [cli, ...args], {
    env: { ...baseEnv, ...env },
    encoding: "utf8",
  });
  const stdout = result.stdout || "";
  const stderr = result.stderr || "";
  const code = result.status ?? 1;
  const ok = code === expectCode &&
    (!stderrIncludes || stderr.includes(stderrIncludes)) &&
    (!stdoutIncludes || stdout.includes(stdoutIncludes));
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

try {
  run("help", ["help"], { stdoutIncludes: "Tavily Pro" });
  run("stats json empty", ["stats", "--json"], { stdoutIncludes: "total_calls" });
  run("stats rejects unknown args", ["stats", "--json", "--bogus"], { expectCode: 1, stderrIncludes: "unknown argument for stats" });
  run("cache info json", ["cache", "info", "--json"], { stdoutIncludes: "count" });
  run("cache info rejects unknown args", ["cache", "info", "--json", "--bogus"], { expectCode: 1, stderrIncludes: "unknown argument for cache info" });
  run("no-key search fails before spend", ["search", "no key smoke", "--no-cache", "--no-log"], { expectCode: 1, stderrIncludes: "TAVILY_API_KEY not set" });
  run("cache clear rejects unknown args", ["cache", "clear", "--bogus"], { expectCode: 1, stderrIncludes: "unknown argument for cache clear" });
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
