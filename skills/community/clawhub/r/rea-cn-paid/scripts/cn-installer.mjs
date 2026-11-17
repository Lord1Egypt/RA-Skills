#!/usr/bin/env node
/**
 * cn-installer.mjs — REA-CN 国内镜像依赖引导器（运行时依赖装到 engine/）
 *
 * 作用：把 rea-agents@6.4.0 引擎运行所需的依赖安装到 `engine/node_modules`，
 * 使技能包首次运行时"自动查缺补漏"，用户无需手动操作。
 *
 * 实现要点：
 *  - 直接对 engine/ 跑 `npm install` 会因原版 package.json 的 `packageManager`
 *    字段触发 npm 偶发的 edgesOut bug；故采用「干净临时目录安装 → 复制到 engine/」
 *    的稳健路径（已实测：143 包 / 15s）。
 *  - 依赖版本与随包引擎（6.4.0）严格绑定，写死在 DEPENDENCIES 中，不受版本参数漂移影响。
 *
 * 用法：
 *   node cn-installer.mjs                 # 安装到 engine/node_modules（默认）
 *   node cn-installer.mjs --registry=...  # 指定镜像
 *   node cn-installer.mjs --dry-run       # 只打印将执行的命令
 *   node cn-installer.mjs --check         # 仅检查已装依赖是否完整
 *
 * 仅使用 Node 内置模块；语法可通过 `node --check` 校验。
 */
import { spawnSync } from "node:child_process";
import {
  existsSync,
  readFileSync,
  rmSync,
  mkdirSync,
  mkdtempSync,
  writeFileSync,
} from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { copyDirSync } from "./lib/engine-assets.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = resolve(__dirname, "..");
const ENGINE_DIR = join(SKILL_ROOT, "engine");
const CONFIG_PATH = join(SKILL_ROOT, "config", "cn-config.json");

// 与随包引擎 rea-agents@6.4.0 绑定的依赖（取自 engine/package.json 的 dependencies）
const DEPENDENCIES = {
  "@babel/parser": "8.0.4",
  "@babel/types": "8.0.4",
  "@clack/prompts": "1.7.0",
  "@electron/asar": "4.2.0",
  "@jridgewell/trace-mapping": "0.3.31",
  "@lydell/node-pty": "1.1.0",
  "@modelcontextprotocol/client": "2.3.1",
  "@modelcontextprotocol/server": "2.3.1",
  "@xmldom/xmldom": "0.9.12",
  "@xterm/addon-serialize": "0.14.0",
  "@xterm/headless": "6.0.0",
  "@zip.js/zip.js": "2.15.0",
  ajv: "8.20.0",
  "ajv-formats": "3.0.1",
  canonicalize: "3.0.0",
  "cross-spawn": "7.0.6",
  diff: "9.0.0",
  "har-schema": "2.0.0",
  ignore: "7.0.6",
  incur: "0.6.1",
  "isomorphic-git": "1.38.7",
  "jsonc-parser": "3.3.1",
  "lossless-json": "4.3.1",
  parse5: "8.0.1",
  pino: "10.4.0",
  "playwright-core": "1.58.2",
  plist: "5.0.0",
  semver: "7.8.5",
  "smol-toml": "1.9.0",
  "stream-json": "3.7.0",
  "write-file-atomic": "7.0.0",
  ws: "8.21.0",
  zod: "4.4.3",
  evmole: "0.9.3",
  yaml: "2.9.0",
};

// 安装在 engine/node_modules 后即视为"依赖就绪"的最小哨兵集合
const SENTINELS = [
  "@modelcontextprotocol/server",
  "zod",
  "playwright-core",
  "pino",
  "@babel/parser",
];

function loadConfig() {
  try {
    if (existsSync(CONFIG_PATH)) return JSON.parse(readFileSync(CONFIG_PATH, "utf8"));
  } catch {
    /* 配置缺失时使用内置默认 */
  }
  return {};
}

function parseArgs(argv) {
  const out = { registry: undefined, dryRun: false, check: false, engine: false };
  for (const a of argv) {
    if (a === "--dry-run" || a === "-n") out.dryRun = true;
    else if (a === "--check") out.check = true;
    else if (a === "--engine") out.engine = true; // 兜底：安装引擎本体（非依赖）
    else if (a.startsWith("--registry=")) out.registry = a.slice("--registry=".length);
  }
  return out;
}

export function depsReady(engineDir = ENGINE_DIR) {
  const nm = join(engineDir, "node_modules");
  return SENTINELS.every((s) => existsSync(join(nm, s)));
}

/** 引擎本体是否就位（rea-agents 包结构：scripts/rea.mjs + dist/） */
export function enginePresent(engineDir = ENGINE_DIR) {
  return existsSync(join(engineDir, "scripts", "rea.mjs")) && existsSync(join(engineDir, "dist"));
}

/**
 * 兜底：从 npmmirror 拉取 rea-agents@<version> 引擎本体并解到 engine/。
 * 用于网关暂不可达时的第三路供给（引擎为 MIT 公开包，与随包基线逐字节一致）。
 * 用法：node cn-installer.mjs --engine
 */
export function installEngineFromRegistry(opts = {}) {
  const cfg = loadConfig();
  const registry = opts.registry || cfg.npmRegistry || "https://registry.npmmirror.com";
  const version = cfg.engineVersion || "6.4.0";
  const isWin = process.platform === "win32";

  console.log(`[cn-installer] 从 ${registry} 拉取 rea-agents@${version}（引擎本体兜底安装）…`);
  const work = mkdtempSync(join(tmpdir(), "rea-engine-"));
  const pack = spawnSync("npm", ["pack", `rea-agents@${version}`, `--registry=${registry}`, "--silent"], {
    cwd: work, stdio: "inherit", shell: isWin,
  });
  if (pack.status !== 0) {
    console.error(`[cn-installer] npm pack 失败（退出码 ${pack.status}）。请检查网络或改用网关下载。`);
    return pack.status || 1;
  }
  const tgz = readdirSync(work).find((f) => f.endsWith(".tgz"));
  if (!tgz) {
    console.error("[cn-installer] 未找到下载的 tarball。");
    return 1;
  }
  mkdirSync(ENGINE_DIR, { recursive: true });
  // npm tarball 根目录为 package/，strip 一层后即 engine/
  const ex = spawnSync("tar", ["-xzf", join(work, tgz), "-C", ENGINE_DIR, "--strip-components=1"], {
    stdio: "inherit", shell: isWin,
  });
  try { rmSync(work, { recursive: true, force: true }); } catch { /* ignore */ }
  if (ex.status !== 0 || !enginePresent()) {
    console.error("[cn-installer] 引擎解压失败或结构不完整。");
    return ex.status || 1;
  }
  console.log(`[cn-installer] 引擎本体已就位（rea-agents@${version} → engine/）。接下来可安装依赖：node cn-installer.mjs`);
  return 0;
}

function checkOnly() {
  const ok = depsReady();
  console.log(
    ok
      ? "[cn-installer] 依赖已就绪（engine/node_modules 哨兵齐全）。"
      : "[cn-installer] 依赖缺失（engine/node_modules 未齐备），需运行安装。"
  );
  process.exit(ok ? 0 : 1);
}

function install({ registry, dryRun }) {
  console.log(`[cn-installer] 引擎目录:   ${ENGINE_DIR}`);
  console.log(`[cn-installer] 镜像源:     ${registry}`);
  console.log(`[cn-installer] 依赖数量:   ${Object.keys(DEPENDENCIES).length}（绑定 rea-agents@6.4.0）`);

  const work = mkdtempSync(join(tmpdir(), "rea-deps-"));
  const pkgJson = JSON.stringify(
    { name: "rea-cn-deps", private: true, dependencies: DEPENDENCIES },
    null,
    2
  );
  writeFileSync(join(work, "package.json"), pkgJson);

  const npmArgs = [
    "install",
    `--registry=${registry}`,
    "--no-audit",
    "--no-fund",
    "--no-package-lock",
  ];

  if (dryRun) {
    console.log(`[cn-installer] 干跑模式，将执行: npm ${npmArgs.join(" ")} (于 ${work})`);
    return 0;
  }

  console.log(`[cn-installer] 在临时目录安装依赖（规避 edgesOut bug）…`);
  const res = spawnSync("npm", npmArgs, {
    cwd: work,
    stdio: "inherit",
    shell: process.platform === "win32",
  });
  if (res.status !== 0) {
    console.error(`[cn-installer] 安装失败，npm 退出码 ${res.status}。`);
    return res.status || 1;
  }

  const src = join(work, "node_modules");
  const dest = join(ENGINE_DIR, "node_modules");
  console.log(`[cn-installer] 复制 node_modules → engine/ …`);
  // 注意：用 copyDirSync（copyFileSync 逐文件复制）而非 fs.cpSync——
  // 部分 Node 构建在目标路径含中文等非 ASCII 字符时 cpSync 会静默失败（此坑实测复现）。
  if (existsSync(dest)) rmSync(dest, { recursive: true, force: true });
  copyDirSync(src, dest);

  // 清理临时目录
  try { rmSync(work, { recursive: true, force: true }); } catch { /* ignore */ }

  console.log(`[cn-installer] 完成。engine/node_modules 已就绪，可启动 MCP 服务器。`);
  return 0;
}

export function installDeps(opts = {}) {
  const cfg = loadConfig();
  const registry = opts.registry || cfg.npmRegistry || "https://registry.npmmirror.com";
  return install({ registry, dryRun: false });
}

function main() {
  const cfg = loadConfig();
  const args = parseArgs(process.argv.slice(2));
  const registry = args.registry || cfg.npmRegistry || "https://registry.npmmirror.com";
  if (args.check) return checkOnly();
  if (args.engine) return installEngineFromRegistry({ registry });
  return install({ registry, dryRun: args.dryRun });
}

// 作为脚本直接运行（非被 import）时才执行
if (process.argv[1] && fileURLToPath(import.meta.url) === resolve(process.argv[1])) {
  process.exit(main());
}
