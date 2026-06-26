#!/usr/bin/env node
//
// api_tool_call.js — 通过妙问 API 直接调用结构化工具（一站式脚本）
//
// 用法: node api_tool_call.js '<JSON_BODY>'
//
// 参数:
//   <JSON_BODY> — 完整的请求体 JSON 字符串，必须包含 "method"、"path"、"params" 字段。
//
// 示例:
//   天粒度报表:  node api_tool_call.js '{"method":"GET","path":"daily_reports/get","params":{"begin":"2025-04-01","end":"2025-04-08","group_by_type":"DATE","fields":["cost"],"page_size":10}}'
//   小时粒度报表: node api_tool_call.js '{"method":"GET","path":"hourly_reports/get","params":{"date":"2025-04-08","group_by_type":"HOUR","fields":["cost","hour"],"page_size":24}}'
//
// 功能:
//   - 自动检查 Token 文件是否存在
//   - 自动读取 Token 并发起 API 请求
//   - 返回结构化 JSON 格式数据
//   - 根据不同错误场景输出明确的提示信息
//
// Token 存储位置: ~/.MIAOWEN_ACCESS_TOKEN
//
// 退出码说明:
//   0 — 请求成功，结果已输出（JSON 格式）
//   1 — 参数错误（未提供 JSON 或 JSON 格式不合法）
//   2 — Token 文件不存在，需要用户首次获取 Token
//   3 — Token 文件为空，需要用户重新设置 Token
//   4 — API 返回非 200 状态码（含 Token 失效、权限错误等，由调用方根据响应内容判断）
//   5 — 网络请求失败（超时等）
//

const fs = require("fs");
const path = require("path");
const os = require("os");

const API_URL =
  "https://ad.qq.com/ai/gw/ai_customer_service/v1/open_api/tool_call";
const TOKEN_FILE = path.join(os.homedir(), ".MIAOWEN_ACCESS_TOKEN");
const REQUEST_TIMEOUT_MS = 60 * 1000; // 1 分钟超时（结构化 API 响应较快）

// ============ 参数检查 ============

const jsonBody = process.argv[2];

if (!jsonBody) {
  console.error("[ERROR] 未提供请求体参数");
  console.error("用法: node api_tool_call.js '<JSON_BODY>'");
  console.error(
    '示例: node api_tool_call.js \'{"method":"GET","path":"daily_reports/get","params":{"begin":"2025-04-01","end":"2025-04-08","group_by_type":"DATE","fields":["cost"],"page_size":10}}\''
  );
  process.exit(1);
}

// 校验 JSON 格式
let parsedBody;
try {
  parsedBody = JSON.parse(jsonBody);
} catch {
  console.error("[ERROR] 请求体不是合法的 JSON 格式");
  console.error("请检查 JSON 字符串是否正确。");
  process.exit(1);
}

// 校验必填字段
if (!parsedBody.method || !parsedBody.path || !parsedBody.params) {
  console.error("[ERROR] 请求体缺少必填字段");
  console.error('必须包含 "method"、"path"、"params" 字段。');
  console.error(
    '示例: {"method":"GET","path":"daily_reports/get","params":{...}}'
  );
  process.exit(1);
}

// ============ Token 检查 ============

if (!fs.existsSync(TOKEN_FILE)) {
  console.log(`[TOKEN_NOT_FOUND] Token 文件不存在: ${TOKEN_FILE}`);
  console.log("");
  console.log("您需要先获取妙问 API KEY 才能使用此服务。");
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

// ============ 发起 API 请求 ============

async function main() {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        "skill-name": "tencent-ads-assistant",
        "skill-version": "1.0.5",
      },
      body: jsonBody,
      signal: controller.signal,
    });

    clearTimeout(timeout);

    const body = await response.text();

    // 检查 HTTP 状态码，非 200 直接输出原始响应内容（由调用方判断具体错误原因）
    if (!response.ok) {
      console.error(`[API_ERROR] API 请求失败 (HTTP ${response.status})`);
      console.error("");
      console.error(body);
      process.exit(4);
    }

    // 输出成功结果
    console.log(body);
    process.exit(0);
  } catch (err) {
    clearTimeout(timeout);

    // ============ 处理网络错误 ============
    if (err.name === "AbortError") {
      console.error("[NETWORK_ERROR] 网络请求失败 (请求超时)");
      console.error("");
      console.error(
        "原因：请求超时（超过 1 分钟），请稍后重试。"
      );
    } else if (
      err.cause &&
      (err.cause.code === "ENOTFOUND" || err.cause.code === "EAI_AGAIN")
    ) {
      console.error("[NETWORK_ERROR] 网络请求失败 (DNS 解析失败)");
      console.error("");
      console.error("原因：无法解析域名，请检查网络连接和 DNS 设置。");
    } else if (err.cause && err.cause.code === "ECONNREFUSED") {
      console.error("[NETWORK_ERROR] 网络请求失败 (连接被拒绝)");
      console.error("");
      console.error("原因：无法连接到服务器，请检查网络连接。");
    } else if (err.cause && err.cause.code === "ECONNRESET") {
      console.error("[NETWORK_ERROR] 网络请求失败 (连接被重置)");
      console.error("");
      console.error("原因：接收数据失败，网络连接中断。");
    } else if (
      err.cause &&
      (err.cause.code === "UNABLE_TO_VERIFY_LEAF_SIGNATURE" ||
        err.cause.code === "ERR_TLS_CERT_ALTNAME_INVALID")
    ) {
      console.error("[NETWORK_ERROR] 网络请求失败 (TLS/SSL 错误)");
      console.error("");
      console.error("原因：SSL/TLS 连接错误，请检查网络环境。");
    } else {
      console.error("[NETWORK_ERROR] 网络请求失败");
      console.error("");
      console.error(
        `原因：网络异常 (${err.message})，请检查网络连接后重试。`
      );
    }

    console.error("");
    console.error("如果问题持续存在，请检查：");
    console.error("  - 网络是否正常连接");
    console.error("  - 是否需要配置代理（如在公司内网环境）");
    console.error("  - 妙问服务是否可用: https://miaowen.qq.com/");
    process.exit(5);
  }
}

main();
