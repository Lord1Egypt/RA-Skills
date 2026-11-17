#!/usr/bin/env node
/**
 * 首次使用：检测 node_modules；缺依赖则 npm install。
 * needBrowser=true 时再确保 Chromium（设备检测 / CDP）。
 */
import { existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const scriptsDir = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);

function run(cmd, args) {
  const r = spawnSync(cmd, args, {
    cwd: scriptsDir,
    stdio: "inherit",
    shell: process.platform === "win32",
  });
  if (r.error) throw r.error;
  if (r.status !== 0) {
    throw new Error(`${cmd} ${args.join(" ")} 失败 (exit ${r.status})`);
  }
}

export function ensureDeps({ needBrowser = false } = {}) {
  let hasPlaywright = false;
  try {
    require.resolve("playwright/package.json");
    hasPlaywright = true;
  } catch {
    hasPlaywright = false;
  }
  if (!hasPlaywright) {
    console.log("[依赖] 未找到 playwright，正在 scripts 目录执行 npm install …");
    run("npm", ["install"]);
  }
  if (needBrowser && !process.env.ZHANFU_SKIP_BROWSER_INSTALL) {
    let needInstall = true;
    try {
      const { chromium } = require("playwright");
      const exe = chromium.executablePath();
      needInstall = !exe || !existsSync(exe);
    } catch {
      needInstall = true;
    }
    if (needInstall) {
      console.log("[依赖] 正在安装 Playwright Chromium（设备检测 / CDP 用）…");
      run("npx", ["playwright", "install", "chromium"]);
    }
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const needBrowser = process.argv.includes("--browser");
  try {
    ensureDeps({ needBrowser });
    console.log("[依赖] 就绪");
    process.exit(0);
  } catch (e) {
    console.error(String(e?.message || e));
    process.exit(1);
  }
}
