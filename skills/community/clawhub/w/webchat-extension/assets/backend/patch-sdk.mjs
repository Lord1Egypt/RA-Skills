// patch-sdk.mjs —— npm postinstall 自动运行
// 给 CodeBuddy Agent SDK 内部 spawn CLI 子进程的调用补上 windowsHide:true，
// 这样 Windows 上「每次对话生成」就不会再弹出 console 黑框。
// 原因：@tencent-ai/agent-sdk 的 lib/transport/process-transport.js 两处 spawn 默认
// windowsHide:false，Node 在 Windows 上会为 console 子进程新建可见控制台窗口。
// 该补丁在每次 npm install 后自动重打，避免重装后黑框复发；分享项目给他人也有效。
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const target = path.join(
  __dirname,
  "node_modules",
  "@tencent-ai",
  "agent-sdk",
  "lib",
  "transport",
  "process-transport.js"
);

if (!fs.existsSync(target)) {
  // 非 Windows / 尚未安装依赖等情况，跳过即可
  console.log("[patch-sdk] agent-sdk not found, skip.");
  process.exit(0);
}

const src = fs.readFileSync(target, "utf8");
if (src.includes("windowsHide: true")) {
  console.log("[patch-sdk] already patched, skip.");
  process.exit(0);
}

// 在两处 spawn 选项对象的 `env: finalEnv,` 后插入 windowsHide:true
const re = /(env: finalEnv,\n)(\s*\}\);)/g;
const patched = src.replace(re, "$1                windowsHide: true,\n$2");

if (patched === src) {
  console.warn(
    "[patch-sdk] WARNING: injection point not found, SDK may have changed. " +
      "Black console windows may appear on Windows."
  );
  process.exit(0);
}

fs.writeFileSync(target, patched);
console.log("[patch-sdk] OK: injected windowsHide:true into CLI spawn (no black windows on Windows).");
