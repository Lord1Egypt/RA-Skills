#!/usr/bin/env node
/**
 * resume-mcp.js — OpenClaw skill bridge for the `resume` CLI.
 * Shells out to `resume show` or `resume notes`, caches in Redis, returns JSON.
 *
 * Usage:
 *   node resume-mcp.js show [project_path]
 *   node resume-mcp.js notes [project_path]
 */

import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { createClient } from "redis";
import path from "node:path";
import os from "node:os";

const execFileAsync = promisify(execFile);

const REDIS_URL = process.env.REDIS_URL;
const CACHE_TTL = parseInt(process.env.RESUME_CACHE_TTL ?? "300", 10);
const RESUME_BIN = process.env.RESUME_BIN ?? path.join(os.homedir(), ".cargo", "bin", "resume");

if (!REDIS_URL) {
  process.stderr.write("[resume-mcp] FATAL: REDIS_URL is not set.\n");
  process.exit(1);
}

const [, , command, rawProjectPath] = process.argv;

if (!["show", "notes"].includes(command)) {
  process.stderr.write(`[resume-mcp] FATAL: Unknown command "${command}". Use "show" or "notes".\n`);
  process.exit(1);
}

const projectPath = rawProjectPath
  ? path.resolve(rawProjectPath.replace(/^~/, os.homedir()))
  : process.cwd();

const redis = createClient({ url: REDIS_URL });
redis.on("error", (err) => process.stderr.write(`[resume-mcp] Redis error: ${err.message}\n`));
await redis.connect().catch(() => null);

function cacheKey() {
  if (command === "notes" && !rawProjectPath) return "resume:notes:__all__";
  return `resume:${command}:${projectPath.replace(/\/+$/, "")}`;
}

const key = cacheKey();

if (redis.isReady) {
  try {
    const cached = await redis.get(key);
    if (cached) {
      const ttl = await redis.ttl(key);
      const parsed = JSON.parse(cached);
      print({ cached: true, ttl_remaining_seconds: ttl, output: parsed.output, source: command, project_path: projectPath });
      await redis.disconnect();
      process.exit(0);
    }
  } catch (err) {
    process.stderr.write(`[resume-mcp] Cache read error: ${err.message}\n`);
  }
}

let stdout = "";
let stderr = "";

try {
  const result = await execFileAsync(RESUME_BIN, command === "show" ? ["show"] : ["notes"], {
    cwd: projectPath,
    env: { ...process.env, NO_COLOR: "1", TERM: "dumb" },
    timeout: 60_000,
    maxBuffer: 4 * 1024 * 1024,
  });
  stdout = result.stdout.trim();
  stderr = result.stderr.trim();
} catch (err) {
  const msg = err.stderr?.trim() || err.stdout?.trim() || err.message || "resume exited with error";
  print({ cached: false, error: true, error_message: msg, output: `resume error:\n\n${msg}`, source: command, project_path: projectPath });
  await redis.disconnect().catch(() => null);
  process.exit(0);
}

if (redis.isReady && stdout) {
  try {
    await redis.set(key, JSON.stringify({ output: stdout }), { EX: CACHE_TTL });
  } catch (err) {
    process.stderr.write(`[resume-mcp] Cache write error: ${err.message}\n`);
  }
}

print({ cached: false, ttl_remaining_seconds: CACHE_TTL, output: stdout || "(no output)", source: command, project_path: projectPath });
await redis.disconnect().catch(() => null);

function print(obj) { process.stdout.write(JSON.stringify(obj, null, 2) + "\n"); }
