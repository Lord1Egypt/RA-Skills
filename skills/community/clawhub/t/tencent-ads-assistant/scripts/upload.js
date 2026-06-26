#!/usr/bin/env node
//
// upload.js — 通过妙问 API 上传文件（图片/素材等）
//
// 用法: node upload.js <文件路径>
//
// 参数:
//   <文件路径> — 要上传的本地文件绝对路径或相对路径
//
// 示例:
//   node upload.js "/Users/user/images/ad_creative.png"
//   node upload.js ./my_image.jpg
//
// 功能:
//   - 自动检查 Token 文件是否存在
//   - 自动读取 Token 并发起文件上传请求
//   - 上传成功后输出文件 URL（JSON 格式）
//   - 根据不同错误场景输出明确的提示信息
//
// Token 存储位置: ~/.MIAOWEN_ACCESS_TOKEN
//
// 退出码说明:
//   0 — 上传成功，结果已输出（JSON 格式，含 file_url 字段）
//   1 — 参数错误（未提供文件路径、文件不存在等）
//   2 — Token 文件不存在，需要用户首次获取 Token
//   3 — Token 文件为空，需要用户重新设置 Token
//   4 — API 返回非 200 状态码或业务错误
//   5 — 网络请求失败（超时等）
//

const fs = require("fs");
const path = require("path");
const os = require("os");

const API_URL =
  "https://ad.qq.com/ai/gw/ai_customer_service/v1/file_tool/upload";
const TOKEN_FILE = path.join(os.homedir(), ".MIAOWEN_ACCESS_TOKEN");
const REQUEST_TIMEOUT_MS = 3 * 60 * 1000; // 3 分钟超时（大文件上传可能耗时）

// ============ 参数检查 ============

const filePath = process.argv[2];

if (!filePath) {
  console.error("[ERROR] 未提供文件路径参数");
  console.error("用法: node upload.js <文件路径>");
  console.error('示例: node upload.js "/Users/user/images/ad_creative.png"');
  process.exit(1);
}

// 解析为绝对路径
const absolutePath = path.resolve(filePath);

if (!fs.existsSync(absolutePath)) {
  console.error(`[ERROR] 文件不存在: ${absolutePath}`);
  console.error("请检查文件路径是否正确。");
  process.exit(1);
}

const stat = fs.statSync(absolutePath);
if (!stat.isFile()) {
  console.error(`[ERROR] 路径不是文件: ${absolutePath}`);
  console.error("请提供一个有效的文件路径，而非目录。");
  process.exit(1);
}

// ============ Token 检查 ============

if (!fs.existsSync(TOKEN_FILE)) {
  console.log(`[TOKEN_NOT_FOUND] Token 文件不存在: ${TOKEN_FILE}`);
  console.log("");
  console.log("您需要先获取妙问 API KEY 才能使用文件上传服务。");
  console.log("");
  console.log("获取步骤：");
  console.log("  1. 打开妙问官网 https://miaowen.qq.com/ 并登录");
  console.log("  2. 左侧导航栏点击【Skill 社区】");
  console.log(
    "  3. 在弹出页面中可以看到「你的 API KEY」，格式为 sk-mw-xxxxx"
  );
  console.log(
    "  4. 点击 API KEY 右侧的「刷新」按钮获取 Token，点击「复制」按钮复制"
  );
  console.log("");
  console.log("获取 Token 后请粘贴给我，我会帮您自动保存。");
  process.exit(2);
}

const token = fs.readFileSync(TOKEN_FILE, "utf-8").trim();

if (!token) {
  console.log(`[TOKEN_EMPTY] Token 文件为空: ${TOKEN_FILE}`);
  console.log("");
  console.log("Token 文件存在但内容为空，请重新获取 Token。");
  console.log("");
  console.log("获取步骤：");
  console.log("  1. 打开妙问官网 https://miaowen.qq.com/ 并登录");
  console.log("  2. 左侧导航栏点击【Skill 社区】");
  console.log(
    "  3. 点击 API KEY 右侧的「刷新」按钮获取新 Token，点击「复制」按钮复制"
  );
  console.log("");
  console.log("获取 Token 后请粘贴给我，我会帮您重新保存。");
  process.exit(3);
}

// ============ 构造 multipart/form-data 并上传 ============

async function main() {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    // 读取文件内容，构造 FormData
    const fileBuffer = fs.readFileSync(absolutePath);
    const fileName = path.basename(absolutePath);

    // Node.js 18+ 内置 FormData 和 Blob
    const blob = new Blob([fileBuffer]);
    const formData = new FormData();
    formData.append("file", blob, fileName);

    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeout);

    const body = await response.text();

    // 检查 HTTP 状态码
    if (!response.ok) {
      console.error(`[API_ERROR] 文件上传失败 (HTTP ${response.status})`);
      console.error("");
      console.error(body);
      process.exit(4);
    }

    // 解析业务响应
    let result;
    try {
      result = JSON.parse(body);
    } catch {
      console.error("[API_ERROR] 响应内容不是合法的 JSON 格式");
      console.error("");
      console.error(body);
      process.exit(4);
    }

    if (result.code !== 0) {
      console.error(
        `[API_ERROR] 文件上传失败 (业务错误码: ${result.code})`
      );
      console.error("");
      console.error(result.message || body);
      process.exit(4);
    }

    // 输出成功结果
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  } catch (err) {
    clearTimeout(timeout);

    // ============ 处理网络错误 ============
    if (err.name === "AbortError") {
      console.error("[NETWORK_ERROR] 文件上传失败 (请求超时)");
      console.error("");
      console.error("原因：请求超时（超过 3 分钟），请检查文件大小或网络状况。");
    } else if (
      err.cause &&
      (err.cause.code === "ENOTFOUND" || err.cause.code === "EAI_AGAIN")
    ) {
      console.error("[NETWORK_ERROR] 文件上传失败 (DNS 解析失败)");
      console.error("");
      console.error("原因：无法解析域名，请检查网络连接和 DNS 设置。");
    } else if (err.cause && err.cause.code === "ECONNREFUSED") {
      console.error("[NETWORK_ERROR] 文件上传失败 (连接被拒绝)");
      console.error("");
      console.error("原因：无法连接到服务器，请检查网络连接。");
    } else if (err.cause && err.cause.code === "ECONNRESET") {
      console.error("[NETWORK_ERROR] 文件上传失败 (连接被重置)");
      console.error("");
      console.error("原因：接收数据失败，网络连接中断。");
    } else if (
      err.cause &&
      (err.cause.code === "UNABLE_TO_VERIFY_LEAF_SIGNATURE" ||
        err.cause.code === "ERR_TLS_CERT_ALTNAME_INVALID")
    ) {
      console.error("[NETWORK_ERROR] 文件上传失败 (TLS/SSL 错误)");
      console.error("");
      console.error("原因：SSL/TLS 连接错误，请检查网络环境。");
    } else {
      console.error("[NETWORK_ERROR] 文件上传失败");
      console.error("");
      console.error(
        `原因：网络异常 (${err.message})，请检查网络连接后重试。`
      );
    }

    console.error("");
    console.error("如果问题持续存在，请检查：");
    console.error("  - 网络是否正常连接");
    console.error("  - 是否需要配置代理（如在公司内网环境）");
    console.error("  - 文件大小是否超出限制");
    console.error("  - 妙问服务是否可用: https://miaowen.qq.com/");
    process.exit(5);
  }
}

main();
