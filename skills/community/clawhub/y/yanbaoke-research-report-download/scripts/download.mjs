#!/usr/bin/env node

import { VERSION, SKILL_ID } from "./version.mjs";

/**
 * Research Report Download Script
 *
 * **Get API Key** from [https://pc.yanbaoke.cn/openclaw](https://pc.yanbaoke.cn/openclaw) (required for download) / 前往 https://pc.yanbaoke.cn/openclaw 获取 API Key（下载必需）
 * Usage:
 *   node download.mjs <uuid> [api_key] [options]
 *
 * Environment variables:
 *   YANBAOKE_API_KEY - Default API key (can be overridden by argument)
 *
 * Examples:
 *   node download.mjs "abc123-def456"
 *   node download.mjs "abc123-def456" "sk-your-api-key"
 */

function usage() {
  console.error(`Usage: download.mjs <uuid> [api_key] [options]

Arguments:
  uuid              Report UUID (required)
  api_key           API key for authentication (optional, uses YANBAOKE_API_KEY env var)

Options:
  -h, --help        Show this help message
  -f, --format      Document format: pdf (default), doc, or ppt

Environment Variables:
  YANBAOKE_API_KEY      Default API key for authentication

Examples:
  node {baseDir}/scripts/download.mjs "abc123-def456"
  node {baseDir}/scripts/download.mjs "abc123-def456" "sk-your-api-key"
  node {baseDir}/scripts/download.mjs "abc123-def456" "sk-your-api-key" --format=doc
  node {baseDir}/scripts/download.mjs "abc123-def456" "" -f ppt

Note: You can get your API key from https://pc.yanbaoke.cn/openclaw`);
  process.exit(2);
}

const args = process.argv.slice(2);

if (args.length === 0 || args.includes("-h") || args.includes("--help")) usage();

const uuid = args[0];
let apiKey = "";
let format = "pdf";  // 默认格式为 pdf

// Parse arguments
for (let i = 1; i < args.length; i++) {
  const arg = args[i];
  if (!arg.startsWith("-")) {
    apiKey = arg;
  } else if (arg === "-f" || arg === "--format") {
    // 下一个参数是格式值
    format = args[i + 1] || "pdf";
    i++;  // 跳过下一个参数
  } else if (arg.startsWith("--format=")) {
    // --format=value 格式
    format = arg.split("=")[1] || "pdf";
  } else if (arg.startsWith("-f=")) {
    // -f=value 格式
    format = arg.split("=")[1] || "pdf";
  }
}

// 验证格式参数
const validFormats = ["pdf", "doc", "ppt"];
if (!validFormats.includes(format.toLowerCase())) {
  console.error(`Error: Invalid format "${format}". Must be one of: pdf, doc, ppt`);
  process.exit(1);
}
format = format.toLowerCase();

apiKey = apiKey || process.env.YANBAOKE_API_KEY || "";

if (!uuid) {
  console.error("Error: UUID is required");
  usage();
}

if (!apiKey) {
  console.error("Error: API key is required. Provide it as an argument or set YANBAOKE_API_KEY environment variable.");
  console.error("\nGet your API key from: https://pc.yanbaoke.cn/openclaw");
  process.exit(1);
}

try {
  // 构建下载 URL，包含格式参数
  const downloadUrl = `https://api.yanbaoke.cn/skills/report_download/${uuid}?format=${format}`;

  const resp = await fetch(downloadUrl, {
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "X-Skill-Version": VERSION,
      "X-Skill-ID": SKILL_ID,
    }
  });

  const body = await resp.json().catch(() => null);

  if (!resp.ok) {
    const errorMsg = body?.error?.message ?? body?.message ?? `HTTP ${resp.status}`;
    console.error(`❌ Download failed: ${errorMsg}`);

    // 友好的错误提示
    const suggestions = {
      400: `\n💡 该报告暂时没有 ${format.toUpperCase()} 格式。`,
      401: `\n🔑 获取 API Key: https://pc.yanbaoke.cn/openclaw`,
      402: `\n💰 豆子不足，请前往充值: https://pc.yanbaoke.cn/pay 或者研报客app里面充值(每份报告消耗10 个豆)`,
      404: `\n🔍 报告不存在，请检查 UUID 是否正确。您可以先运行搜索命令获取正确的 UUID。`,
      429: `\n⏳ 请求过于频繁，请稍后再试。`,
    };

    const suggestion = suggestions[resp.status];
    if (suggestion) {
      console.error(suggestion);
    }

    process.exit(1);
  }

  let report;
  // 检查是否是 OpenAI 格式响应
  if (body?.choices && body.choices[0]?.report) {
    report = body.choices[0].report;
  } else if (body?.download_url) {
    report = body;
  } else {
    console.error("Unexpected response format");
    console.error(JSON.stringify(body, null, 2));
    process.exit(1);
  }

  const { download_url, title, filename, format: reportFormat = format } = report;

  // 显示下载链接
  console.log(`## Report Download Link\n`);
  console.log(`**Title**: ${title}`);
  console.log(`**Format**: ${reportFormat.toUpperCase()}`);
  console.log(`**Filename**: ${filename}`);
  console.log(`**Expires in**: ${report.expires_in ?? 60} seconds\n`);
  console.log(`**Download URL** (click to download):`);
  console.log(`${download_url}\n`);
  console.log(`---\n`);
  console.log(`*Note: This download link expires in 60 seconds.*`);

} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
