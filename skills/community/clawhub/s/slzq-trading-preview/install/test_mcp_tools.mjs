import { existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(__dirname, "..");
const runtimeDir = resolve(rootDir, "runtime/mcp");
const legacyDir = resolve(rootDir, "../slzq-trading-mcp");

function fail(message, next) {
  console.error(`FAIL: ${message}`);
  console.error(`下一步：${next}`);
  process.exit(1);
}

function run(command, args, cwd) {
  const result = spawnSync(command, args, { cwd, stdio: "inherit", env: process.env, shell: process.platform === "win32" });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

function pickMcpDir() {
  if (existsSync(resolve(runtimeDir, "scripts/test-mcp-tools.mjs"))) return runtimeDir;
  if (existsSync(resolve(legacyDir, "scripts/test-mcp-tools.mjs"))) return legacyDir;
  return null;
}

const mcpDir = pickMcpDir();
if (!mcpDir) {
  fail("未找到 MCP tools/list 自检脚本", "请确认已下载新版能力包，目录内应存在 runtime/mcp/scripts/test-mcp-tools.mjs。");
}

if (!existsSync(resolve(mcpDir, "node_modules"))) {
  console.log(`INFO: ${mcpDir} 缺少 node_modules，正在执行 npm ci...`);
  run("npm", ["ci"], mcpDir);
}

run("node", ["scripts/test-mcp-tools.mjs"], mcpDir);
