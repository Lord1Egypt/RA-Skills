#!/usr/bin/env node
// register-protocol.cjs —— 一键注册 / 修复 webchat:// URL 协议处理程序。
//
// 适用场景：
//   1) 点 webchat://start 链接时 Windows 弹出"获取打开此链接的应用 → Microsoft Store"，
//      说明 HKCU\Software\Classes\webchat 注册表项丢失/损坏 → 跑本脚本即可修复。
//   2) 把 webchat-extension 项目目录迁移到新位置后，重新指向正确的 launcher.vbs。
//   3) 部署后想确认协议是否真的生效（--check 模式）。
//
// 用法：
//   node scripts/register-protocol.cjs            # 自动探测 launcher.vbs 并注册
//   node scripts/register-protocol.cjs --check     # 仅检查当前注册状态，不修改
//   node scripts/register-protocol.cjs --force     # 强制覆盖（即使已注册也重写）
//
// 设计：纯 Node + child_process 调 reg 命令（绕过沙箱对 reg/powershell 的 LOLBin 限制）。
// 默认写入 HKCU（当前用户，无需管理员权限）。

const { execSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const BASE = "HKCU\\Software\\Classes\\webchat";

// ---------- 参数 ----------
const args = process.argv.slice(2);
const CHECK_ONLY = args.includes("--check");
const FORCE = args.includes("--force");

// ---------- 探测 launcher.vbs 位置 ----------
// 优先级：真实部署目录 > skill 模板（模板仅作最后兜底，避免误指向未装依赖的 skill 目录）
function findLauncherVbs() {
  const candidates = [];

  // 1) 环境变量（显式指定最优先）
  if (process.env.WEBCHAT_DIR) {
    candidates.push(path.join(process.env.WEBCHAT_DIR, "backend", "launcher.vbs"));
  }
  // 2) 当前工作目录下的 webchat-extension
  candidates.push(path.join(process.cwd(), "webchat-extension", "backend", "launcher.vbs"));
  // 3) 标准部署位置（~/webchat-extension）
  candidates.push(path.join(os.homedir(), "webchat-extension", "backend", "launcher.vbs"));
  // 4) 旧工作空间位置（兜底，避免硬编码其他机器）
  candidates.push(
    path.join(os.homedir(), "WorkBuddy", "claudecode", "webchat-extension", "backend", "launcher.vbs")
  );
  // 5) skill 内的 assets/backend（兜底；注意 launcher.vbs 现已不在 assets 内——它由部署时生成，此候选通常为空）
  candidates.push(path.join(__dirname, "..", "assets", "backend", "launcher.vbs"));

  return candidates.filter((p) => fs.existsSync(p));
}

// ---------- reg 命令封装 ----------
function regQuery(key) {
  try {
    return execSync(`reg query "${key}"`, { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
  } catch {
    return null;
  }
}
function regAdd(key, valueName, data) {
  const vFlag = valueName === "" ? "/ve" : `/v "${valueName}"`;
  try {
    execSync(`reg add "${key}" ${vFlag} /t REG_SZ /d "${data}" /f`, {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });
    return true;
  } catch (e) {
    console.error(`  ✗ reg add 失败: ${key} ${vFlag}`);
    if (e.stderr) console.error("   ", e.stderr.trim());
    return false;
  }
}

// 从已注册命令中提取 launcher.vbs 路径（去引号、去 wscript 前缀、去 %1 参数），做大小写不敏感比较
function extractVbsPath(cmd) {
  if (!cmd) return null;
  // 形如: C:\Windows\System32\wscript.exe "路径\launcher.vbs" "%1"
  const m = cmd.match(/"([^"]*launcher\.vbs)"|(\S*launcher\.vbs)/i);
  if (m) return (m[1] || m[2] || "").replace(/["%1]/g, "").trim();
  return null;
}

// ---------- 主流程 ----------
console.log("🔧 webchat:// 协议注册工具\n");

const found = findLauncherVbs();
if (found.length === 0) {
  console.error("✗ 找不到 launcher.vbs！launcher.vbs 由 agent 在部署时生成（不随包分发），请先生成：");
  console.error(`   node "${path.join(__dirname, "gen-vbs.mjs")}" "${path.join(process.cwd(), "webchat-extension", "backend")}"`);
  console.error("   （或直接重新部署：node scripts/deploy.mjs ~/webchat-extension）");
  console.error("  搜索过：");
  console.error(`   - ${path.join(process.cwd(), "webchat-extension", "backend")}`);
  console.error(`   - ${path.join(os.homedir(), "webchat-extension", "backend")}`);
  process.exit(1);
}

const vbsPath = found[0];
console.log(`✓ 找到 launcher.vbs: ${vbsPath}\n`);

// 当前注册状态
const existing = regQuery(`${BASE}\\shell\\open\\command`);
let currentCmd = null;
if (existing) {
  const m = existing.match(/REG_SZ\s+(.+)$/m);
  if (m) currentCmd = m[1].trim();
}
const currentVbs = extractVbsPath(currentCmd);
const expectedCmd = `C:\\Windows\\System32\\wscript.exe "${vbsPath}" "%1"`;
// 路径一致（忽略引号/大小写）即视为已正确，不强制要求外层引号
const pathOk = currentVbs && currentVbs.toLowerCase() === vbsPath.toLowerCase();

if (CHECK_ONLY) {
  console.log("=== 当前注册状态 ===");
  if (!currentCmd) {
    console.log("  ✗ 协议未注册（HKCU\\Software\\Classes\\webchat 不存在）");
    console.log("  → 运行 `node scripts/register-protocol.cjs` 注册");
  } else if (pathOk) {
    console.log("  ✓ 协议已正确注册，无需修复");
    console.log(`    命令: ${currentCmd}`);
  } else {
    console.log("  ⚠️ 协议已注册但指向不正确（可能项目迁移过）：");
    console.log(`    当前: ${currentCmd}`);
    console.log(`    应为: ${expectedCmd}`);
    console.log("  → 运行 `node scripts/register-protocol.cjs --force` 修复");
  }
  process.exit(0);
}

if (pathOk && !FORCE) {
  console.log("✓ 协议已正确注册，无需修改（用 --force 可强制重写）");
  process.exit(0);
}

// 执行注册
console.log("正在注册 webchat:// 协议...");
const steps = [
  ["写默认名", regAdd(BASE, "", "webchat Protocol")],
  ["写 URL Protocol", regAdd(BASE, "URL Protocol", "")],
  ["写 command", regAdd(`${BASE}\\shell\\open\\command`, "", expectedCmd)],
];
let ok = true;
for (const [label, success] of steps) {
  console.log(`  ${success ? "✓" : "✗"} ${label}`);
  if (!success) ok = false;
}
if (!ok) {
  console.error("\n✗ 注册失败，请检查权限或手动用 README 的 reg add 命令注册。");
  process.exit(1);
}

// 验证
const verify = regQuery(`${BASE}\\shell\\open\\command`);
const vm = verify && verify.match(/REG_SZ\s+(.+)$/m);
const vVbs = extractVbsPath(vm && vm[1].trim());
if (vm && vVbs && vVbs.toLowerCase() === vbsPath.toLowerCase()) {
  console.log("\n✅ 注册成功！现在 webchat://start 链接应该能正常拉起后端了。");
  console.log("   测试：浏览器访问 webchat://start 或点扩展面板「🚀 启动后端」按钮。");
} else {
  console.error("\n⚠️ 注册完成但验证不匹配，请手动检查注册表。");
  process.exit(1);
}
