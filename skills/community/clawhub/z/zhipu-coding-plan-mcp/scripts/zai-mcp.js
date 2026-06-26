#!/usr/bin/env node
/**
 * mcporter wrapper - 自动从 OpenClaw auth-profiles.json 读取智谱 API Key
 * 用法: node zai-mcp.js <mcporter 参数>
 * 例如: node zai-mcp.js call web-search-prime.web_search_prime --args '{"search_query": "test"}'
 */

import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { homedir } from "node:os";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = dirname(__dirname);
const AUTH_FILE = join(homedir(), ".openclaw", "agents", "main", "agent", "auth-profiles.json");
const MCP_CONFIG = join(SKILL_DIR, "mcporter.json");

if (!existsSync(AUTH_FILE)) {
  console.error(`Error: auth-profiles.json not found at ${AUTH_FILE}`);
  process.exit(1);
}

let apiKey;
try {
  const auth = JSON.parse(readFileSync(AUTH_FILE, "utf-8"));
  apiKey = auth?.profiles?.["zai:default"]?.key;
} catch (e) {
  console.error(`Error: Failed to parse auth-profiles.json: ${e.message}`);
  process.exit(1);
}

if (!apiKey) {
  console.error("Error: Failed to read API key from auth-profiles.json");
  process.exit(1);
}

process.env.ZAI_MCP_API_KEY = apiKey;

const args = process.argv.slice(2);
try {
  const result = execFileSync("npx", ["--prefix", SKILL_DIR, "mcporter", "--config", MCP_CONFIG, ...args], {
    env: process.env,
    stdio: "inherit",
    maxBuffer: 10 * 1024 * 1024,
  });
} catch (e) {
  process.exit(e.status || 1);
}
