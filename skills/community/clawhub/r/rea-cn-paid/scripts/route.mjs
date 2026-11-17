#!/usr/bin/env node
/**
 * route.mjs — REA-CN 环境探测与双路路由建议
 *
 * 探测运行环境并给出接入建议（路线 A：MCP 服务器；路线 B：rea CLI）。
 * 同时列出与 provider 相关的环境变量（详见 references/config-keys.md）。
 *
 * 用法：
 *   node route.mjs
 *
 * 仅使用 Node 内置模块；可通过 `node --check` 校验。
 */
import { existsSync, readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = resolve(__dirname, "..");
const ENGINE_DIR = join(SKILL_ROOT, "engine");
const CONFIG_PATH = join(SKILL_ROOT, "config", "cn-config.json");

// 与 provider 相关的 REA 环境变量（含义见 config-keys.md）
const PROVIDER_ENV_KEYS = [
  "REA_ADB_PATH",
  "REA_APKTOOL_COMMAND",
  "REA_JEB_MCP_URL",
  "REA_BROWSER_EXECUTABLE",
  "REA_PROCESS_RUN_ID",
];

// 外部二进制 provider（需用户自备；下载/安装见 references/providers.md）
// name: PATH 中探测的可执行文件名；label: 中文名；hint: 配置/用途提示
const BINARY_PROVIDERS = [
  { name: "ghidraRun", alt: ["analyzeHeadless", "ghidraRun.bat"], label: "Ghidra", hint: "通用反编译（需 JDK 21）" },
  { name: "jadx", alt: ["jadx.bat"], label: "JADX", hint: "Android/Dalvik 反编译" },
  { name: "apktool", alt: ["apktool.bat"], label: "apktool", hint: "Android 资源解码（需 Java）" },
  { name: "adb", alt: [], label: "adb", hint: "Android 设备交互（REA_ADB_PATH）" },
  { name: "ida", alt: ["ida64", "ida.exe"], label: "IDA", hint: "通用反汇编（provider_id:ida + IDA MCP）" },
  { name: "hopper", alt: ["Hopper"], label: "Hopper", hint: "仅 macOS（provider_id:hopper）" },
  { name: "chromium", alt: ["chrome", "google-chrome", "msedge"], label: "浏览器", hint: "Web 模块（REA_BROWSER_EXECUTABLE）" },
];

function whichAny(names) {
  return names.some((n) => {
    const res = spawnSync(process.platform === "win32" ? "where" : "which", [n], {
      stdio: ["ignore", "pipe", "ignore"],
    });
    return res.status === 0 && res.stdout.toString().trim().length > 0;
  });
}

function loadConfig() {
  try {
    if (existsSync(CONFIG_PATH)) return JSON.parse(readFileSync(CONFIG_PATH, "utf8"));
  } catch {
    /* ignore */
  }
  return {};
}

function which(bin) {
  const res = spawnSync(process.platform === "win32" ? "where" : "which", [bin], {
    stdio: ["ignore", "pipe", "ignore"],
  });
  return res.status === 0 && res.stdout.toString().trim().length > 0;
}

function main() {
  const cfg = loadConfig();
  const report = [];
  const add = (k, v) => report.push(`  ${k.padEnd(22)} ${v}`);

  console.log("=== REA-CN 环境探测 ===\n");

  add("Node 版本", process.version);
  const nodeOk = /^v(22|24|2[6-9])/.test(process.version);
  add("Node 是否达标", nodeOk ? "是（引擎要求 ^22.19 || ^24.11 || >=26）" : "否（建议升级）");

  add("技能根目录", SKILL_ROOT);
  add("engine/ 是否存在", existsSync(ENGINE_DIR) ? "是" : "否（需运行自更新/安装）");

  const engPkg = join(ENGINE_DIR, "package.json");
  add("engine 版本", existsSync(engPkg) ? JSON.parse(readFileSync(engPkg, "utf8")).version : "（未知）");

  const hasCli = which("rea");
  add("rea CLI 是否在 PATH", hasCli ? "是" : "否");

  console.log("运行环境：");
  report.forEach((l) => console.log(l));
  console.log("");

  // provider 环境变量（仅显示已设置的，未设置给出提示）
  const setEnv = PROVIDER_ENV_KEYS.filter((k) => process.env[k] !== undefined);
  console.log("Provider 环境变量：");
  if (setEnv.length === 0) {
    console.log("  （均未设置。可选；需要时参考 references/config-keys.md 配置，例如 REA_ADB_PATH 指向 adb 可执行文件）");
  } else {
    setEnv.forEach((k) => console.log(`  ${k} = ${process.env[k]}`));
  }
  console.log("");

  // 外部二进制 provider 就绪情况（需自备，见 references/providers.md）
  console.log("外部二进制 Provider（需自备，下载/安装见 references/providers.md）：");
  const ready = [];
  const missing = [];
  for (const p of BINARY_PROVIDERS) {
    const names = [p.name, ...p.alt];
    const envSet =
      (p.label === "adb" && process.env.REA_ADB_PATH) ||
      (p.label === "apktool" && process.env.REA_APKTOOL_COMMAND) ||
      (p.label === "JEB" && process.env.REA_JEB_MCP_URL) ||
      (p.label === "浏览器" && process.env.REA_BROWSER_EXECUTABLE);
    if (whichAny(names) || envSet) {
      ready.push(p.label);
      console.log(`  ✅ ${p.label.padEnd(8)} 就绪（${p.hint}）`);
    } else {
      missing.push(p.label);
      console.log(`  ⚠️  ${p.label.padEnd(8)} 未检测到（${p.hint}）`);
    }
  }
  if (missing.length > 0) {
    console.log(`  → 缺失的 provider 不影响 Node 引擎运行；按目标类型装齐即可，`);
    console.log(`    下载地址/体积/步骤见 references/providers.md。`);
  }
  console.log("");

  // 路由建议
  console.log("=== 接入建议 ===");
  if (hasCli) {
    console.log("✅ 推荐路线 B（CLI）：直接 `rea open <path>` / `rea inspect-evidence-bundle ...`；");
    console.log("   也可在支持 MCP 的客户端中挂载 engine/ 作为路线 A。");
  } else if (existsSync(ENGINE_DIR)) {
    console.log("✅ 推荐路线 A（MCP）：在 WorkBuddy 等客户端挂载 engine/ 启动 REA MCP 服务器；");
    console.log("   未检测到 rea CLI，如需 CLI 请先 `node scripts/cn-installer.mjs`。");
  } else {
    console.log("⚠️ 尚未就绪：engine/ 不存在且无 rea CLI。");
    console.log("   请先执行：`node scripts/cn-installer.mjs` 或 `node scripts/rea-selfupdate.mjs`。");
  }
  console.log("");
  console.log("无论哪条路线，调用工具时一律使用英文原名（见 references/tool-invocation-contract.md）。");
  return 0;
}

process.exit(main());
