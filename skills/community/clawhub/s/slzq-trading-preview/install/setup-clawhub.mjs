#!/usr/bin/env node
/**
 * ClawHub 安装后一键准备：装 MCP 依赖、用默认生产域名 + sim、
 * 没有 API Key 也能生成可启动的 MCP 配置（会话里再登录领钥）。
 * 若本机有 openclaw CLI，会尝试自动注册。
 *
 * 不改 App 五步用的 generate_mcp_config.mjs：那边仍要求终端里已有三项环境变量。
 */
import { existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(__dirname, "..");
const mcpDir = resolve(rootDir, "runtime/mcp");
const mcpEntry = resolve(mcpDir, "dist/index.js");

const SKILL_NAME = "slzq-trading";
const DEFAULT_DOMAIN = "https://slzqapi.sxslqhsh.com";
const DOMAIN_ENV = "SLZQ_OPENCLAW_DOMAIN";
const API_KEY_ENV = "SLZQ_OPENCLAW_API_KEY";
const TRADING_ENV = "SLZQ_OPENCLAW_ENV";

const win = process.platform === "win32";

function fail(message, next) {
  console.error(`FAIL: ${message}`);
  if (next) console.error(`下一步：${next}`);
  process.exit(1);
}

function run(command, args, cwd) {
  const result = spawnSync(command, args, {
    cwd,
    stdio: "inherit",
    env: process.env,
    shell: win,
  });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

function which(bin) {
  const result = spawnSync(win ? "where" : "command", win ? [bin] : ["-v", bin], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "ignore"],
    shell: win,
  });
  return result.status === 0;
}

function stripMobileApi(raw) {
  return raw.trim().replace(/\/+$/, "").replace(/\/mobile-api$/i, "");
}

if (!existsSync(mcpEntry)) {
  fail("未找到 MCP 入口 runtime/mcp/dist/index.js", "请确认 ClawHub / zip 解压完整。");
}

if (!existsSync(resolve(mcpDir, "node_modules"))) {
  console.error("INFO: 正在安装 MCP 依赖（npm ci）…");
  run("npm", ["ci"], mcpDir);
}

const domain = stripMobileApi(process.env[DOMAIN_ENV] || "") || DEFAULT_DOMAIN;
const tradingEnv = (process.env[TRADING_ENV] || "sim").trim().toLowerCase();
const apiKey = (process.env[API_KEY_ENV] || "").trim();

if (tradingEnv !== "sim" && tradingEnv !== "live") {
  fail(`${TRADING_ENV} 无效：${tradingEnv}`, "请设为 sim 或 live。");
}

const env = {
  [DOMAIN_ENV]: domain,
  [TRADING_ENV]: tradingEnv,
};
if (apiKey) env[API_KEY_ENV] = apiKey;

const config = {
  mcpServers: {
    [SKILL_NAME]: {
      command: "node",
      args: [mcpEntry],
      env,
    },
  },
};

console.log(JSON.stringify(config, null, 2));
console.error("");
console.error(`域名：${domain}${process.env[DOMAIN_ENV] ? "" : "（未设置，使用生产默认）"}`);
console.error(`环境：${tradingEnv}`);
console.error(apiKey ? "API Key：已从环境变量读入（不会打印明文）" : "API Key：未配置。重启后对新会话说「帮我登录领取模拟盘密钥」即可。");
console.error("");

if (which("openclaw")) {
  const addArgs = [
    "mcp",
    "add",
    SKILL_NAME,
    "--command",
    "node",
    "--arg",
    mcpEntry,
    "--env",
    `${DOMAIN_ENV}=${domain}`,
    "--env",
    `${TRADING_ENV}=${tradingEnv}`,
  ];
  if (apiKey) addArgs.push("--env", `${API_KEY_ENV}=${apiKey}`);
  console.error("INFO: 检测到 openclaw，正在注册 MCP…");
  const added = spawnSync("openclaw", addArgs, {
    stdio: "inherit",
    env: process.env,
    shell: win,
  });
  if (added.status === 0) {
    console.error("PASS: 已写入 OpenClaw MCP。请完全退出并重启客户端，再新开会话。");
  } else {
    console.error("WARN: openclaw mcp add 未成功（可能已存在同名服务）。请把上面的 JSON 贴进客户端 MCP 配置，或执行：");
    console.error(`  openclaw mcp set ${SKILL_NAME}`);
  }
} else {
  console.error("将上面的 mcpServers JSON 原样复制到当前智能体客户端的 MCP 配置中。");
  console.error("注意：args[0] 已是绝对路径；改完后必须完全退出并重启客户端，再新开会话。");
}
