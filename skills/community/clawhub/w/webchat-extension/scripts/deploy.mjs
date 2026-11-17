#!/usr/bin/env node
// deploy.mjs —— 把「网页划线对话」扩展 + 后端脚手架到目标目录，并安装依赖。
// 用法：node scripts/deploy.mjs [targetDir] [--no-install] [--no-protocol]
//
// 该脚本只负责「复制源码 + 安装依赖 +（Windows）注册协议」。真正的运行由 agent 按 SKILL.md 步骤完成：
//   1) 配置 backend/.env（填 CODEBUDDY_API_KEY，可选）
//   2) 后台启动后端：cd <target>/backend && npm start  （或用面板「🚀 启动后端」按钮）
//   3) 浏览器开发者模式加载 <target>/extension 目录
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import zlib from "node:zlib";
import { writeLauncherVbs } from "./gen-vbs.mjs"; // launcher.vbs 唯一 source of truth：部署时现生成，不随包分发

const __dirname = dirname(fileURLToPath(import.meta.url));

const SKILL_DIR = resolve(__dirname, "..");
const ASSETS = join(SKILL_DIR, "assets");

const args = process.argv.slice(2);
const noInstall = args.includes("--no-install");
const noProtocol = args.includes("--no-protocol");
const targetArg = args.find((a) => !a.startsWith("--"));

// 默认目标：当前目录下的 webchat-extension（若已存在），否则用户主目录下的 webchat-extension
const target = targetArg
  ? resolve(targetArg)
  : fs.existsSync(join(process.cwd(), "webchat-extension"))
  ? join(process.cwd(), "webchat-extension")
  : join(os.homedir(), "webchat-extension");

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const ent of fs.readdirSync(src, { withFileTypes: true })) {
    if (ent.name === 'icons') continue;   // 图标由 ensureIcons 现生成，不复制源 png
    const s = join(src, ent.name);
    const d = join(dest, ent.name);
    if (ent.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

// ---------- 图标：由 agent 在部署时现生成（分享包不含任何 png） ----------
// 用 Node 零依赖生成珊瑚橙纯色 PNG，保证「加载已解压」不会因缺图标而失败。
// 若想换成正式品牌图标，部署后直接替换 extension/icons/{16,32,48,128}.png 即可。
function crc32(buf) {
  let c = ~0;
  for (let i = 0; i < buf.length; i++) {
    c ^= buf[i];
    for (let k = 0; k < 8; k++) c = (c >>> 1) ^ (0xedb88320 & -(c & 1));
  }
  return (~c) >>> 0;
}
function pngChunk(type, data) {
  const t = Buffer.from(type, "ascii");
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length, 0);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(Buffer.concat([t, data])), 0);
  return Buffer.concat([len, t, data, crc]);
}
function writePng(filePath, size, [r, g, b]) {
  const stride = size * 3 + 1;
  const raw = Buffer.alloc(stride * size);
  for (let y = 0; y < size; y++) {
    raw[y * stride] = 0; // filter type 0
    for (let x = 0; x < size; x++) {
      const o = y * stride + 1 + x * 3;
      raw[o] = r; raw[o + 1] = g; raw[o + 2] = b;
    }
  }
  const sig = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8;   // bit depth
  ihdr[9] = 2;   // color type RGB
  const idat = zlib.deflateSync(raw, { level: 9 });
  fs.writeFileSync(filePath, Buffer.concat([
    sig,
    pngChunk("IHDR", ihdr),
    pngChunk("IDAT", idat),
    pngChunk("IEND", Buffer.alloc(0)),
  ]));
}
function ensureIcons(extDir) {
  const sizes = [16, 32, 48, 128];
  const iconsDir = join(extDir, "icons");
  fs.mkdirSync(iconsDir, { recursive: true });
  for (const s of sizes) writePng(join(iconsDir, `icon${s}.png`), s, [255, 122, 69]); // 珊瑚橙
  console.log(`✓ 已生成 ${sizes.length} 张珊瑚橙图标（extension/icons），可替换成正式品牌图标。`);
  return true;
}

console.log(`\n📦 部署「网页划线对话」→ ${target}\n`);

const extSrc = join(ASSETS, "extension");
const beSrc = join(ASSETS, "backend");
const rootSrc = join(ASSETS, "root");
const skillRoot = resolve(__dirname, ".."); // webchat-extension/（含 pack.mjs 等发布工具）
if (!fs.existsSync(extSrc) || !fs.existsSync(beSrc)) {
  console.error("✗ 找不到 skill 内的 assets/extension 或 assets/backend，请确认技能目录完整。");
  process.exit(1);
}
copyDir(extSrc, join(target, "extension"));
copyDir(beSrc, join(target, "backend"));
ensureIcons(join(target, "extension")); // 兜底：确保 icons 四张齐全，避免加载失败
console.log("✓ 已复制 extension/ 与 backend/（不含真实 .env 密钥）");

// ---------- Windows：部署时由 agent 生成 launcher.vbs（不随包分发） ----------
// 关键：这一步独立于协议注册，即使带 --no-protocol 也会生成，保证面板「🚀 启动后端」按钮可用。
function ensureLauncherVbs() {
  writeLauncherVbs(join(target, "backend")); // win32 才会写；非 Windows 自动跳过
}
ensureLauncherVbs();
if (fs.existsSync(rootSrc)) {
  copyDir(rootSrc, target); // README.md（.gitignore / 协议模板不随分享包分发）
  console.log("✓ 已复制根文档（README.md）");
}

// 复制发布工具（根 pack.mjs / gen-icons.mjs）到 target，使其可一键生成分享包
for (const tool of ["pack.mjs", "gen-icons.mjs"]) {
  const src = join(skillRoot, tool);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, join(target, tool));
    console.log(`✓ 已复制发布工具 ${tool}（可在 target 下 node ${tool} 生成分享包 / 图标）`);
  }
}

// 若目标没有 .env，提示用户从 .env.example 复制
const envPath = join(target, "backend", ".env");
const envExample = join(target, "backend", ".env.example");
if (!fs.existsSync(envPath) && fs.existsSync(envExample)) {
  console.log("\n⚠️ 后端还没配置 .env，请复制模板并填写（Key 可选：不填走登录模式真实 AI，需本机 codebuddy 已登录）：");
  console.log(`   cp "${envExample}" "${envPath}"`);
  console.log("   然后视情况设置 CODEBUDDY_API_KEY / CODEBUDDY_MODEL=deepseek-v4-flash / SERVER__PORT=40123");
}

// ---------- Windows：注册 webchat:// 协议（使面板「🚀 启动后端」按钮免终端生效） ----------
function registerProtocol() {
  if (process.platform !== "win32") {
    console.log("\nℹ️ 非 Windows：跳过协议注册。请按 README「四、一键启动后端」手动注册（或在浏览器用「📋 复制启动命令」手动 npm start）。");
    return;
  }
  const vbsPath = join(target, "backend", "launcher.vbs");
  // launcher.vbs 已由 ensureLauncherVbs()（上面的部署步骤）在 Windows 上生成；这里仅引用其路径注册协议。
  // 命令值里需要把路径与 %1 用引号包住： "wscript.exe" "launcher.vbs" "%1"
  const cmdValue = `"C:\\Windows\\System32\\wscript.exe" "${vbsPath}" "%1"`;
  const base = "HKCU\\Software\\Classes\\webchat";
  const cmds = [
    ["add", base, "/ve", "/t", "REG_SZ", "/d", "webchat Protocol", "/f"],
    ["add", base, "/v", "URL Protocol", "/t", "REG_SZ", "/d", "", "/f"],
    ["add", `${base}\\shell\\open\\command`, "/ve", "/t", "REG_SZ", "/d", cmdValue, "/f"],
  ];
  let ok = true;
  for (const c of cmds) {
    const r = spawnSync("reg", c, { stdio: "ignore" });
    if (r.status !== 0) {
      ok = false;
      break;
    }
  }
  if (ok) {
    console.log("✓ 已注册 webchat:// 协议（HKCU，无需管理员）。面板「🚀 启动后端」按钮现在可免终端拉起后端。");
  } else {
    console.log("⚠️ 协议注册失败（可能无权限）。可改用面板「📋 复制启动命令」手动 npm start。");
  }
}
if (noProtocol) {
  console.log("\n⏭️ 跳过协议注册（--no-protocol）。如需一键启动，请按 README 手动注册。");
} else {
  registerProtocol();
}

if (noInstall) {
  console.log("\n⏭️ 跳过 npm install（--no-install）。需要时用：cd backend && npm install");
} else {
  console.log("\n⏳ 安装后端依赖（npm install，可能需几十秒）…");
  // Windows 上 npm 是 npm.cmd，spawnSync 默认不解析 .cmd，需 shell:true（或显式 npm.cmd）
  const npmBin = process.platform === "win32" ? "npm.cmd" : "npm";
  const r = spawnSync(npmBin, ["install"], {
    cwd: join(target, "backend"),
    stdio: "inherit",
    shell: process.platform === "win32",
  });
  if (r.status !== 0) {
    console.error("\n✗ npm install 失败，请手动在 backend/ 运行 npm install 后重试启动。");
    process.exit(r.status || 1);
  }
  console.log("✓ 依赖安装完成");
}

console.log("\n──────────── 下一步（由 agent 或你执行） ────────────");
console.log("1) 启动后端（建议后台运行，关掉对话就断）：");
console.log(`   cd "${join(target, "backend")}" && npm start`);
console.log("   （Windows 已注册协议后，也可直接点面板「🚀 启动后端」按钮）");
console.log("2) 浏览器开发者模式 → 加载已解压的扩展 → 选目录：");
console.log(`   ${join(target, "extension")}`);
console.log("3) 验证：浏览器访问 http://localhost:3000/api/health 应返回 {status:ok}");
console.log("────────────────────────────────────────────────────\n");
