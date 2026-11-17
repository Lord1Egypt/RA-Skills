#!/usr/bin/env node
/**
 * vendor-offline.mjs — 将运行时依赖离线固化进 engine/node_modules
 *
 * 适用场景：需要把技能包带到**无网络/内网/离线**环境，或希望完全跳过首次自动安装。
 * 执行后 engine/node_modules 被填满（约 +90MB），技能包变为"自带依赖"的胖包，
 * 之后无论有无网络均可直接 `node scripts/run-mcp.mjs` 启动。
 *
 * 若只想保持瘦身包（默认），请勿运行本脚本——首次运行 run-mcp.mjs 会自动联网安装。
 *
 * 仅使用 Node 内置模块；语法可通过 `node --check` 校验。
 */
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";
import { installDeps, depsReady } from "./cn-installer.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ENGINE_DIR = join(resolve(__dirname, ".."), "engine");

function main() {
  console.log("[vendor-offline] 开始将依赖固化进 engine/node_modules（需联网一次）…");
  const code = installDeps();
  if (code !== 0) {
    console.error("[vendor-offline] 安装失败。");
    process.exit(code || 1);
  }
  const ok = depsReady(ENGINE_DIR);
  console.log(
    ok
      ? "[vendor-offline] 完成：依赖已固化。技能包现在可离线运行（包体约 +90MB）。"
      : "[vendor-offline] 警告：哨兵检查未通过，请重试。"
  );
  process.exit(ok ? 0 : 1);
}

main();
