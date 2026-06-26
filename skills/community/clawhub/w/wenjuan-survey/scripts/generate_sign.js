#!/usr/bin/env node
/**
 * 问卷网 AI 技能签名工具（服务端代签）
 *
 * 说明：
 * - 本地不再持有 appkey/secret
 * - 通过签名服务获取 appkey、timestamp、signature
 */

const { URL, URLSearchParams } = require('url');
const { createSecureAxios } = require("./axios_secure");
const { wenjuanUrl } = require("./api_config");
const http = createSecureAxios();

// 配置
const CONFIG = {
  web_site: "ai_skills",
  sign_service_url: wenjuanUrl("/app_api/create/signature"),
};

/**
 * 请求服务端签名参数
 * @param {Object} params 业务参数
 * @param {boolean} includeTimestamp 是否由服务端补 timestamp（默认 true）
 * @returns {Promise<{appkey:string,web_site:string,timestamp:string,signature:string}>}
 */
async function requestSignedParams(params, includeTimestamp = true) {
  const cleanParams = { ...(params || {}) };
  delete cleanParams.signature;
  if (!includeTimestamp) {
    cleanParams.timestamp = String(cleanParams.timestamp || Math.floor(Date.now() / 1000));
  }

  const resp = await http.post(
    CONFIG.sign_service_url,
    {
      web_site: CONFIG.web_site,
      params: cleanParams,
    },
    { headers: { "Content-Type": "application/json" }, timeout: 30000 }
  );
  const body = resp.data || {};
  const d = body.data && typeof body.data === "object" ? body.data : body;
  const out = {
    appkey: String(d.appkey || ""),
    web_site: String(d.web_site || CONFIG.web_site),
    timestamp: String(d.timestamp || ""),
    signature: String(d.signature || ""),
  };
  if (!out.appkey || !out.signature || !out.timestamp) {
    throw new Error("签名服务返回缺少必要字段(appkey/timestamp/signature)");
  }
  return out;
}

/**
 * 解析URL中的参数
 * @param {string} url - 完整URL或查询字符串
 * @returns {Object} 参数字典
 */
function parseUrlParams(url) {
  // 如果只有查询字符串，添加一个dummy scheme
  let fullUrl = url;
  if (!url.includes("?") && !url.startsWith("http")) {
    fullUrl = "http://dummy.com/?" + url;
  }
  
  const parsed = new URL(fullUrl);
  const params = {};
  
  parsed.searchParams.forEach((value, key) => {
    params[key] = value;
  });
  
  return params;
}

/**
 * 生成带签名的完整URL（异步）
 * @param {string} baseUrl - 基础URL（不含查询参数）
 * @param {Object} params - 额外参数
 * @returns {Promise<string>} 带签名的完整URL
 */
async function buildSignedUrl(baseUrl, params = {}) {
  const signed = await requestSignedParams(params, true);
  const fullParams = { ...params, ...signed };
  const separator = baseUrl.includes("?") ? "&" : "?";
  const queryString = new URLSearchParams(fullParams).toString();
  return baseUrl + separator + queryString;
}

/**
 * 对已有URL进行签名
 * @param {string} url - 原始URL（可包含已有参数）
 * @returns {string} 带签名的完整URL
 */
async function signUrl(url) {
  // 解析已有参数
  const params = parseUrlParams(url);
  
  // 获取基础URL
  let baseUrl = url;
  if (url.includes("?")) {
    baseUrl = url.split("?")[0];
  }
  
  return buildSignedUrl(baseUrl, params);
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  let url = null;
  const params = {};
  let format = "full";
  let timestamp = null;
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === "--url" && i + 1 < args.length) {
      url = args[++i];
    } else if (arg === "--param" && i + 1 < args.length) {
      const param = args[++i];
      if (param.includes("=")) {
        const [key, value] = param.split("=");
        params[key] = value;
      } else {
        params[param] = "";
      }
    } else if (arg === "--format" && i + 1 < args.length) {
      format = args[++i];
      if (!["full", "url", "signature"].includes(format)) {
        console.error("错误: format 必须是 full, url 或 signature");
        process.exit(1);
      }
    } else if (arg === "--timestamp" && i + 1 < args.length) {
      timestamp = args[++i];
    } else if (arg === "--help" || arg === "-h") {
      showHelp();
      process.exit(0);
    }
  }
  
  // 从URL解析参数
  if (url && url.includes("?")) {
    const urlParams = parseUrlParams(url);
    Object.assign(params, urlParams);
  }
  
  // 指定时间戳
  if (timestamp) {
    params.timestamp = timestamp;
  } else if (!params.timestamp) {
    params.timestamp = String(Math.floor(Date.now() / 1000));
  }
  
  // 远端签名
  const signed = await requestSignedParams(params, false);
  const signature = signed.signature;
  
  // 输出结果
  if (format === "signature") {
    console.log(signature);
  } else if (format === "url") {
    const baseUrl = url && url.includes("?") ? url.split("?")[0] : url || "";
    if (baseUrl) {
      const fullParams = { ...params };
      fullParams.web_site = CONFIG.web_site;
      fullParams.appkey = signed.appkey;
      fullParams.web_site = signed.web_site;
      fullParams.timestamp = signed.timestamp;
      fullParams.signature = signature;
      const queryString = new URLSearchParams(fullParams).toString();
      console.log(baseUrl + "?" + queryString);
    } else {
      console.error("错误: 使用--format url时必须提供--url参数");
      process.exit(1);
    }
  } else {
    // full 格式
    console.log("=".repeat(60));
    console.log("问卷网AI技能签名生成");
    console.log("=".repeat(60));
    console.log();
    console.log("【配置信息】");
    console.log(`  web_site: ${CONFIG.web_site}`);
    console.log(`  sign_service_url: ${CONFIG.sign_service_url}`);
    console.log();
    console.log("【请求参数】");
    // 添加固定参数用于显示
    const displayParams = { ...params };
    displayParams.web_site = signed.web_site;
    displayParams.appkey = signed.appkey;
    displayParams.timestamp = signed.timestamp;
    // 移除signature（如果存在）
    if (displayParams.signature) {
      console.log("  (移除了原有的signature参数)");
      delete displayParams.signature;
    }
    Object.keys(displayParams).sort().forEach(key => {
      console.log(`  ${key}: ${displayParams[key]}`);
    });
    console.log();
    console.log("【签名过程】");
    
    // 重新计算并显示中间步骤
    const signParams = { ...displayParams };
    const sortedItems = Object.entries(signParams).sort((a, b) => a[0].localeCompare(b[0]));
    
    console.log(`  1. 参数排序: ${sortedItems.map(([k]) => k).join(", ")}`);
    
    const valueStr = sortedItems.map(([_, v]) => String(v)).join("");
    console.log(`  2. 拼接值: ${valueStr}`);
    
    console.log(`  3. 服务端签名完成`);
    console.log(`  4. signature: ${signature}`);
    console.log();
    console.log("=".repeat(60));
    console.log(`最终 signature: ${signature}`);
    console.log("=".repeat(60));
    console.log();
    console.log("【最终请求参数（共4个固定参数 + 业务参数）】");
    console.log(`  appkey=${signed.appkey}`);
    console.log(`  web_site=${signed.web_site}`);
    console.log(`  timestamp=${signed.timestamp || 'N/A'}`);
    console.log(`  signature=${signature}`);
    const otherKeys = Object.keys(displayParams).filter(k => !['appkey', 'web_site', 'timestamp'].includes(k));
    if (otherKeys.length > 0) {
      console.log("  [业务参数]");
      otherKeys.sort().forEach(k => {
        console.log(`    ${k}=${displayParams[k]}`);
      });
    }
  }
}

function showHelp() {
  console.log(`
生成问卷网AI技能API签名（服务端代签）

用法: node generate_sign.js [选项]

选项:
  --url <url>           原始URL（可选）
  --param <key=value>   请求参数，格式: key=value，可多次使用
  --format <format>     输出格式: full=完整信息, url=完整URL, signature=仅签名
  --timestamp <ts>      指定时间戳（秒级），默认使用当前时间
  -h, --help            显示帮助信息

示例:
  # 生成签名（从URL解析参数）
  node generate_sign.js --url "https://api.example.com/test?user_id=123"

  # 指定参数生成签名
  node generate_sign.js --param user_id=123 --param action=get_list

  # 生成完整URL（自动添加appkey, web_site, timestamp, signature）
  node generate_sign.js --url "https://api.example.com/test" --param user_id=123 --format url

  # 仅输出生成的签名值
  node generate_sign.js --param project_id=abc123 --format signature

固定参数:
  appkey=<来自签名服务>
  web_site=ai_skills
  timestamp=<来自签名服务>
  signature=<来自签名服务>
`);
}

// 导出模块
module.exports = {
  requestSignedParams,
  parseUrlParams,
  buildSignedUrl,
  signUrl,
  CONFIG
};

// 如果是直接运行
if (require.main === module) {
  main().catch((e) => {
    console.error(`错误: ${e.message || e}`);
    process.exit(1);
  });
}
