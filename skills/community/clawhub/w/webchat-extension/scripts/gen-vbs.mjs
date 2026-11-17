#!/usr/bin/env node
// gen-vbs.mjs —— 在 backend/ 下生成 launcher.vbs（Windows 隐藏窗口启动器）。
//
// 设计原则（重要）：
//   launcher.vbs 是「部署期产物」，**绝不等同于源码、绝不随分享包分发 / 上传**。
//   - pack.mjs 硬性禁止列表已排除 *.vbs；
//   - skills 仓库 .gitignore 已排除 launcher.vbs；
//   - 因此本文件是「唯一 source of truth」，由 agent 在部署时现生成，
//     保证分享包干净、且面板「🚀 启动后端」按钮在部署后免终端生效。
//
// 用法：
//   node scripts/gen-vbs.mjs [backendDir] [--force]
//     backendDir  目标 backend 目录；缺省时自动探测（cwd/backend、skill assets/backend、~/webchat-extension/backend）
//     --force     即使非 Windows 也写入（默认仅 win32 写入，因为 .vbs 是 Windows 专用）
//
// 本模块同时被 deploy.mjs 导入（writeLauncherVbs），保证「agent 部署」与「手动生成」产出一致。
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, join, resolve } from "node:path";
import fs from "node:fs";
import os from "node:os";

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------- launcher.vbs 内容（唯一 source of truth） ----------
// 注意：行尾用 \r\n（Windows 脚本规范）。内容与原 deploy.mjs 内联版一致。
export const LAUNCHER_VBS = [
  "' webchat backend launcher - invoked by webchat:// protocol handler",
  "' Runs launcher.mjs hidden (no console window)",
  "On Error Resume Next",
  "Set fso = CreateObject(\"Scripting.FileSystemObject\")",
  "Set sh = CreateObject(\"WScript.Shell\")",
  "scriptPath = WScript.ScriptFullName",
  "backendDir = fso.GetParentFolderName(scriptPath)",
  "",
  "' Minimal log for debugging (use %TEMP%, always exists across machines)",
  "logPath = sh.ExpandEnvironmentStrings(\"%TEMP%\") & \"\\webchat_vbs.log\"",
  "Set logFile = fso.OpenTextFile(logPath, 8, True)",
  "logFile.WriteLine Now & \" START backendDir=\" & backendDir",
  "logFile.Close",
  "",
  "' Resolve node: try PATH first, then managed path fallback",
  "nodeExe = \"\"",
  "Set oExec = sh.Exec(\"cmd /c where node 2>nul\")",
  "Do While oExec.Status = 0",
  "  WScript.Sleep 30",
  "Loop",
  "out = \"\"",
  "Err.Clear",
  "out = oExec.StdOut.ReadAll()",
  "Set logFile = fso.OpenTextFile(logPath, 8, True)",
  "logFile.WriteLine Now & \" where_result=\" & Left(out, 200) & \" err=\" & Err.Number",
  "If Err.Number = 0 And Len(out) > 0 Then",
  "  nodeExe = Trim(Split(out, vbCrLf)(0))",
  "  logFile.WriteLine Now & \" resolved=\" & nodeExe",
  "End If",
  "",
  "If Len(nodeExe) = 0 Then",
  "  home = sh.ExpandEnvironmentStrings(\"%USERPROFILE%\")",
  "  fallback = home & \"\\.workbuddy\\binaries\\node\\versions\\22.22.2\\node.exe\"",
  "  If fso.FileExists(fallback) Then",
  "    nodeExe = fallback",
  "    logFile.WriteLine Now & \" fallback=\" & nodeExe",
  "  Else",
  "    logFile.WriteLine Now & \" fallback_NOT_FOUND\"",
  "  End If",
  "End If",
  "",
  "If Len(nodeExe) = 0 Then nodeExe = \"node\"",
  "",
  "' 读取协议传入的 URL（webchat://start），透传给 launcher.mjs",
  "url = \"\"",
  "If WScript.Arguments.Count > 0 Then url = WScript.Arguments(0)",
  "",
  "cmd = \"\"\"\" & nodeExe & \"\"\"\" & \" \" & \"\"\"\" & backendDir & \"\\launcher.mjs\" & \"\"\"\" & \" \" & \"\"\"\" & url & \"\"\"\"",
  "logFile.WriteLine Now & \" RUN cmd=\" & cmd",
  "logFile.Close",
  "",
  "sh.Run cmd, 0, False",
  "",
  "Set logFile = fso.OpenTextFile(logPath, 8, True)",
  "logFile.WriteLine Now & \" Run returned\"",
  "logFile.Close"
].join("\r\n");

// 写出 launcher.vbs 到 backendDir。返回写出路径；未写出（非 Windows 且未 --force）返回 null。
export function writeLauncherVbs(backendDir, { force = false } = {}) {
  if (!force && process.platform !== "win32") {
    console.log("ℹ️ 非 Windows：跳过 launcher.vbs 生成（.vbs 仅 Windows 有效，webchat:// 协议按钮也是 Windows 专属）。");
    return null;
  }
  fs.mkdirSync(backendDir, { recursive: true });
  const vbsPath = join(backendDir, "launcher.vbs");
  fs.writeFileSync(vbsPath, LAUNCHER_VBS, "utf8");
  console.log(`✓ 已生成 launcher.vbs → ${vbsPath}`);
  return vbsPath;
}

// ---------- CLI ----------
function autoDetectBackendDir() {
  const cands = [
    join(process.cwd(), "backend"),
    join(__dirname, "..", "assets", "backend"),
    join(os.homedir(), "webchat-extension", "backend"),
  ];
  for (const c of cands) if (fs.existsSync(c)) return c;
  return null;
}

// 仅当作为脚本直接运行时执行 CLI（被 deploy.mjs import 时不触发）
// 注意：process.argv[1] 可能是相对路径，需解析成 file URL 再比较；
// 用 -e / 动态 import 等场景下 argv[1] 可能为 undefined，需先判空避免 resolve 抛错。
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const args = process.argv.slice(2);
  const force = args.includes("--force");
  const dirArg = args.find((a) => !a.startsWith("--"));
  const backendDir = dirArg ? resolve(dirArg) : autoDetectBackendDir();

  if (!backendDir) {
    console.error("✗ 找不到 backend 目录。请显式传入：node scripts/gen-vbs.mjs <backendDir>");
    process.exit(1);
  }
  writeLauncherVbs(backendDir, { force });
}
