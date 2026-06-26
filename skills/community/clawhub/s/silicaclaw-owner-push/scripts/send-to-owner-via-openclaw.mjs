#!/usr/bin/env node

import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { resolve } from "node:path";

function requiredEnv(name) {
  const value = String(process.env[name] || "").trim();
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

function resolveOpenClawCommand() {
  const explicitBin = String(process.env.OPENCLAW_BIN || "").trim();
  if (explicitBin) {
    return { cmd: explicitBin, args: [] };
  }

  const sourceDir = String(process.env.OPENCLAW_SOURCE_DIR || "").trim();
  if (sourceDir) {
    return {
      cmd: "node",
      args: [resolve(sourceDir, "openclaw.mjs")],
    };
  }

  return { cmd: "openclaw", args: [] };
}

function main() {
  const payload = JSON.parse(readFileSync(0, "utf8"));
  const channel = requiredEnv("OPENCLAW_OWNER_CHANNEL");
  const target = requiredEnv("OPENCLAW_OWNER_TARGET");
  const account = String(process.env.OPENCLAW_OWNER_ACCOUNT || "").trim();
  const message = String(payload?.summary || "").trim();
  if (!message) {
    throw new Error("Missing summary in stdin payload");
  }

  const command = resolveOpenClawCommand();
  const args = [
    ...command.args,
    "message",
    "send",
    "--channel",
    channel,
    "--target",
    target,
    "--message",
    message,
  ];
  if (account) {
    args.push("--account", account);
  }

  const result = spawnSync(command.cmd, args, {
    stdio: "inherit",
    env: process.env,
  });

  if (result.error) {
    throw result.error;
  }
  process.exit(result.status ?? 1);
}

main();
