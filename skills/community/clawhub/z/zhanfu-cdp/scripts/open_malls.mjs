#!/usr/bin/env node
/** 批量打开店铺：串行一家接一家；取端口失败仍继续下一家。 */
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { ensureDeps } from "./ensure_deps.mjs";
ensureDeps();

import { attachCurrentProcessToKillJob, configureStdio, emit } from "./zhanfu_http.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parseNames(argv) {
  const names = [];
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--mall-name" && argv[i + 1]) names.push(String(argv[++i]).trim());
  }
  return names.filter(Boolean);
}

async function runOne(name) {
  const worker = path.join(__dirname, "open_mall.mjs");
  return new Promise((resolve) => {
    const proc = spawn(process.execPath, [worker, "--mall-name", name], {
      cwd: path.dirname(__dirname),
      stdio: "inherit",
    });
    console.log(`[批量] 串行打开 ${name} pid=${proc.pid}`);
    proc.on("exit", (code) => resolve(code == null ? 1 : code));
  });
}

async function main() {
  configureStdio();
  const names = parseNames(process.argv);
  if (!names.length) return emit({ ok: false, status: "no_mall" }, 1);

  attachCurrentProcessToKillJob();
  const results = [];
  for (const name of names) {
    const code = await runOne(name);
    results.push({ mall_name: name, exit: code });
    console.log(`[批量] ${name} exit=${code}，继续下一家`);
  }
  const ok = results.every((r) => r.exit === 0);
  return emit({ ok, status: "batch_done", results }, ok ? 0 : 1);
}

process.exit(await main());
