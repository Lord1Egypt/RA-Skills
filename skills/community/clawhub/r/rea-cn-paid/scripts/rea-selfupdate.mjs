#!/usr/bin/env node
/**
 * rea-selfupdate.mjs — REA-CN 引擎自更新器
 *
 * 将技能内嵌的 engine/ 基线更新到指定（或 config 默认）的 rea-agents 版本：
 *   1. 用国内镜像把目标版本安装到一个临时目录；
 *   2. 把其 dist / skills / bridge / native / LICENSE / package.json 同步进 engine/；
 *   3. 校验 engine/package.json 的版本号。
 *
 * 注意：engine/ 仅承载"离线基线"，与 SKILL.md / references / scripts / config 并列。
 * 本脚本不会触碰 references、scripts、config 与 SKILL.* 文件，避免覆盖本地化成果。
 *
 * 用法：
 *   node rea-selfupdate.mjs              # 更新到 config 默认版本
 *   node rea-selfupdate.mjs 6.4.0        # 指定版本
 *   node rea-selfupdate.mjs --dry-run    # 只打印步骤
 *
 * 仅使用 Node 内置模块；可通过 `node --check` 校验。
 */
import { spawnSync } from "node:child_process";
import {
  existsSync,
  readFileSync,
  writeFileSync,
  mkdirSync,
  rmSync,
  readdirSync,
  statSync,
} from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve, basename } from "node:path";
import { tmpdir } from "node:os";
import { copyDirSync } from "./lib/engine-assets.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = resolve(__dirname, "..");
const ENGINE_DIR = join(SKILL_ROOT, "engine");
const CONFIG_PATH = join(SKILL_ROOT, "config", "cn-config.json");

// engine 内需要保留的本地化无关产物（来自 npm 包）；其余一律不覆盖
const SYNC_ENTRIES = ["dist", "skills", "bridge", "native", "LICENSE", "package.json"];
// 来自 npm 包、应整体删除后重建的目录（确保干净同步）
const PKG_DIRS = ["dist", "skills", "bridge", "native"];

function loadConfig() {
  try {
    if (existsSync(CONFIG_PATH)) return JSON.parse(readFileSync(CONFIG_PATH, "utf8"));
  } catch {
    /* ignore */
  }
  return {};
}

function parseArgs(argv) {
  const out = { positional: [], dryRun: false };
  for (const a of argv) {
    if (a === "--dry-run" || a === "-n") out.dryRun = true;
    else out.positional.push(a);
  }
  return out;
}

function readVersion(pkgJsonPath) {
  if (!existsSync(pkgJsonPath)) return null;
  try {
    return JSON.parse(readFileSync(pkgJsonPath, "utf8")).version;
  } catch {
    return null;
  }
}

function main() {
  const cfg = loadConfig();
  const args = parseArgs(process.argv.slice(2));
  const version = args.positional[0] || cfg.engineVersion || "6.4.0";
  const registry = cfg.npmRegistry || "https://registry.npmmirror.com";

  console.log(`[selfupdate] 目标版本: ${version}`);

  if (args.dryRun) {
    console.log(`[selfupdate] 干跑：将在临时目录安装 rea-agents@${version}（${registry}），`);
    console.log(`[selfupdate] 然后同步 ${SYNC_ENTRIES.join(", ")} 到 engine/，并删除旧 ${PKG_DIRS.join(", ")}。`);
    return 0;
  }

  if (!existsSync(ENGINE_DIR)) mkdirSync(ENGINE_DIR, { recursive: true });

  const tmp = join(tmpdir(), `rea-update-${Date.now()}`);
  mkdirSync(tmp, { recursive: true });
  try {
    const install = spawnSync(
      "npm",
      ["install", `rea-agents@${version}`, `--registry=${registry}`, "--no-audit", "--no-fund"],
      { cwd: tmp, stdio: "inherit", shell: process.platform === "win32" }
    );
    if (install.status !== 0) {
      console.error(`[selfupdate] 临时安装失败（npm 退出码 ${install.status}）。`);
      return install.status || 1;
    }

    const src = join(tmp, "node_modules", "rea-agents");
    if (!existsSync(src)) {
      console.error(`[selfupdate] 临时安装目录缺少 rea-agents，中止同步以免破坏 engine/。`);
      return 1;
    }

    // 清掉 engine 内旧的产物目录，保证干净同步
    for (const d of PKG_DIRS) {
      const p = join(ENGINE_DIR, d);
      if (existsSync(p)) rmSync(p, { recursive: true, force: true });
    }

    // 同步条目
    for (const e of SYNC_ENTRIES) {
      const from = join(src, e);
      if (!existsSync(from)) {
        console.warn(`[selfupdate] 源缺少 ${e}，跳过。`);
        continue;
      }
      const to = join(ENGINE_DIR, e);
      copyDirSync(from, to);
      console.log(`[selfupdate] 已同步 ${e}。`);
    }

    const finalVersion = readVersion(join(ENGINE_DIR, "package.json"));
    console.log(`[selfupdate] engine/ 当前版本: ${finalVersion || "(未知)"}`);
    if (finalVersion && finalVersion !== version) {
      console.warn(`[selfupdate] 警告：engine 版本 ${finalVersion} 与请求 ${version} 不一致。`);
    }
    console.log(`[selfupdate] 完成。请重新加载 MCP 服务器以应用更新。`);
    return 0;
  } finally {
    try {
      rmSync(tmp, { recursive: true, force: true });
    } catch {
      /* ignore */
    }
  }
}

process.exit(main());
