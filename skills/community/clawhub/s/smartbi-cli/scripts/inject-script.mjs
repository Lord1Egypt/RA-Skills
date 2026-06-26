#!/usr/bin/env node
// 用法: node inject-script.mjs <script.js> <meta.json> <output.json>
// 将多行 Rhino JS 脚本 JSON 转义后注入到元数据模板的 script 字段，输出完整请求体。
// 元数据模板中 script 字段可为空占位（如 "script": ""），本工具会覆盖为转义后的脚本内容。

import { readFileSync, writeFileSync, existsSync } from "node:fs";

function usage(exitCode) {
  const msg = [
    "Usage: node inject-script.mjs <script.js> <meta.json> <output.json>",
    "",
    "参数:",
    "  script.js   Rhino JS 脚本文件路径（原始多行 JS）",
    "  meta.json   请求体元数据模板（含 selfDefineTaskUpsertRequest 且 script 为空占位）",
    "  output.json 输出文件路径（合并后的完整请求体 JSON）",
    "",
    "示例:",
    "  node inject-script.mjs task.js task_meta.json task.json",
  ].join("\n");
  console.log(msg);
  process.exit(exitCode);
}

function errorExit(reason) {
  console.error("ERROR: " + reason);
  process.exit(1);
}

if (process.argv.includes("--help") || process.argv.includes("-h")) {
  usage(0);
}

const args = process.argv.slice(2);
if (args.length < 3) {
  console.error("ERROR: 需要 3 个参数，实际收到 " + args.length + " 个");
  usage(1);
}

const scriptPath = args[0];
const metaPath = args[1];
const outPath = args[2];

if (!existsSync(scriptPath)) errorExit("脚本文件不存在: " + scriptPath);
if (!existsSync(metaPath)) errorExit("元数据模板不存在: " + metaPath);

let scriptContent;
try {
  scriptContent = readFileSync(scriptPath, "utf8");
} catch (e) {
  errorExit("读取脚本文件失败: " + e.message);
}

if (!scriptContent.trim()) errorExit("脚本文件内容为空: " + scriptPath);

let metaJson;
try {
  metaJson = JSON.parse(readFileSync(metaPath, "utf8"));
} catch (e) {
  errorExit("元数据模板 JSON 解析失败: " + e.message);
}

let reqKey;
if (metaJson.selfDefineTaskUpsertRequest) {
  reqKey = "selfDefineTaskUpsertRequest";
} else if (metaJson.customTaskUpsertRequest) {
  reqKey = "customTaskUpsertRequest";
} else {
  const topKeys = Object.keys(metaJson);
  if (topKeys.length === 1 && typeof metaJson[topKeys[0]] === "object") {
    reqKey = topKeys[0];
  } else {
    metaJson = { selfDefineTaskUpsertRequest: metaJson };
    reqKey = "selfDefineTaskUpsertRequest";
  }
}

const req = metaJson[reqKey];
if (!req || typeof req !== "object") {
  errorExit("元数据模板中未找到有效的请求对象（key: " + reqKey + "）");
}

if (!req.name) errorExit("元数据模板缺少必填字段: name");
if (!req.script && req.script !== "") {
  req.script = "";
}

req.script = scriptContent;

try {
  const output = JSON.stringify(metaJson, null, 2);
  writeFileSync(outPath, output, "utf8");
} catch (e) {
  errorExit("写入输出文件失败: " + e.message);
}

const lineCount = scriptContent.split("\n").length;
const byteSize = Buffer.byteLength(scriptContent, "utf8");
console.log("OK");
console.log("  script: " + scriptPath + " (" + lineCount + " lines, " + byteSize + " bytes)");
console.log("  meta:   " + metaPath);
console.log("  output: " + outPath);
