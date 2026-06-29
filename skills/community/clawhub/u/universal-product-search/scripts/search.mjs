#!/usr/bin/env node

import { spawnSync } from "node:child_process";

const UCP_PACKAGE = "@shopify/ucp-cli@0.6.2";

function fail(message) {
  console.error(message);
  process.exit(2);
}

function parseArgs(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (key === "--init-profile") {
      const next = argv[index + 1];
      options.initProfile = next && !next.startsWith("--") ? argv[++index] : "agent";
      continue;
    }
    if (!key.startsWith("--")) fail(`Unexpected argument: ${key}`);
    const value = argv[++index];
    if (!value || value.startsWith("--")) fail(`Missing value for ${key}`);
    options[key.slice(2)] = value;
  }
  return options;
}

function validate(options) {
  if (options.business) {
    let url;
    try {
      url = new URL(options.business);
    } catch {
      fail("--business must be a valid HTTPS URL");
    }
    if (url.protocol !== "https:") fail("--business must use HTTPS");
  }
  if (options.country && !/^[A-Za-z]{2}$/.test(options.country)) {
    fail("--country must be a two-letter country code");
  }
  if (options.currency && !/^[A-Za-z]{3}$/.test(options.currency)) {
    fail("--currency must be a three-letter currency code");
  }
  if (options.limit) {
    const limit = Number(options.limit);
    if (!Number.isInteger(limit) || limit < 1 || limit > 50) {
      fail("--limit must be an integer from 1 to 50");
    }
  }
}

function commandArgs(options) {
  if (options.initProfile) {
    return ["profile", "init", "--name", options.initProfile];
  }
  if (!options.query) fail("--query is required");

  const args = [
    "catalog",
    "search",
    "--set-string",
    `/query=${options.query}`,
    "--set",
    `/pagination/limit=${options.limit ?? "10"}`,
    "--view",
    ":compact",
    "--format",
    "json",
  ];
  const context = [
    ["country", "address_country", (value) => value.toUpperCase()],
    ["currency", "currency", (value) => value.toUpperCase()],
    ["language", "language", (value) => value],
    ["intent", "intent", (value) => value],
  ];
  for (const [option, field, normalize] of context) {
    if (options[option]) args.push("--set-string", `/context/${field}=${normalize(options[option])}`);
  }
  if (options.business) args.push("--business", options.business);
  if (options.profile) args.push("--profile", options.profile);
  return args;
}

function runUcp(args) {
  const direct = spawnSync("ucp", args, { stdio: "inherit" });
  if (!direct.error || direct.error.code !== "ENOENT") return direct.status ?? 1;

  const npx = process.platform === "win32" ? "npx.cmd" : "npx";
  const fallback = spawnSync(npx, ["--yes", UCP_PACKAGE, ...args], { stdio: "inherit" });
  if (fallback.error) fail(`Unable to run Shopify UCP CLI: ${fallback.error.message}`);
  return fallback.status ?? 1;
}

const options = parseArgs(process.argv.slice(2));
validate(options);
process.exit(runUcp(commandArgs(options)));
