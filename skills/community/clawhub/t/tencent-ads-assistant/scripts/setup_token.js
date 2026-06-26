#!/usr/bin/env node
//
// setup_token.js — 将妙问 Access Token 保存到文件
//
// 用法: node setup_token.js "<YOUR_TOKEN>"
//
// Token 存储位置: ~/.MIAOWEN_ACCESS_TOKEN
//

const fs = require("fs");
const path = require("path");
const os = require("os");

const TOKEN_FILE = path.join(os.homedir(), ".MIAOWEN_ACCESS_TOKEN");

const token = process.argv[2];

if (!token) {
  console.error("[ERROR] 请提供 Token 参数");
  console.error('用法: node setup_token.js "<YOUR_TOKEN>"');
  process.exit(1);
}

// 将 Token 写入文件（覆盖旧内容，不含换行符）
try {
  fs.writeFileSync(TOKEN_FILE, token.trim(), { encoding: "utf-8", mode: 0o600 });
} catch (err) {
  console.error(`[ERROR] 无法写入 Token 文件: ${TOKEN_FILE}`);
  console.error(`原因: ${err.message}`);
  process.exit(1);
}

// 尝试设置文件权限为 600（仅当前用户可读写）
// Windows 上 fs.chmodSync 可能不会实际生效，但 writeFileSync 的 mode 已指定
try {
  fs.chmodSync(TOKEN_FILE, 0o600);
  console.log(`[SUCCESS] Token 已成功保存到 ${TOKEN_FILE}`);
  console.log("  文件权限已设置为仅当前用户可读写 (600)");
} catch {
  console.log(`[SUCCESS] Token 已成功保存到 ${TOKEN_FILE}`);
  console.log(
    "  注意：当前系统不支持设置文件权限。如果您在 Windows 环境下，请确保该文件不被其他用户访问。"
  );
}

console.log("");
console.log("配置完成！现在可以直接使用妙问问答了。");
