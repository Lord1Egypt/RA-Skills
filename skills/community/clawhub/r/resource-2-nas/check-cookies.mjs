#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { maskSecret, parseDotEnv } from "./check-env.mjs";

const DEFAULT_ENV_FILE = ".env";
const DEFAULT_TIMEOUT_MS = 20_000;
const DEFAULT_BAIDU_APP_ID = "250528";

const PROVIDERS = {
  quark: {
    provider: "quark",
    label: "夸克网盘",
    cookieEnv: "QUARK_COOKIE",
    baseUrl: "https://drive-pc.quark.cn",
    buildUrl: ({ baseUrl }) => {
      const url = new URL(`${normalizeBaseUrl(baseUrl)}/1/clouddrive/file/sort`);
      url.searchParams.set("pr", "ucpro");
      url.searchParams.set("fr", "pc");
      url.searchParams.set("uc_param_str", "");
      url.searchParams.set("pdir_fid", "0");
      url.searchParams.set("_page", "1");
      url.searchParams.set("_size", "1");
      url.searchParams.set("_fetch_total", "1");
      url.searchParams.set("_fetch_sub_dirs", "0");
      url.searchParams.set("_sort", "file_type:asc,updated_at:desc");
      return url;
    },
    classify: classifyQuarkResponse
  },
  baidu: {
    provider: "baidu",
    label: "百度网盘",
    cookieEnv: "BAIDU_COOKIE",
    baseUrl: "https://pan.baidu.com",
    buildUrl: ({ baseUrl, appId }) => {
      const url = new URL(`${normalizeBaseUrl(baseUrl)}/rest/2.0/xpan/nas`);
      url.searchParams.set("method", "uinfo");
      url.searchParams.set("app_id", appId || DEFAULT_BAIDU_APP_ID);
      return url;
    },
    classify: classifyBaiduResponse
  }
};

if (isCliEntryPoint()) {
  main().catch((error) => {
    console.error(JSON.stringify({ ok: false, error: error.message || String(error) }, null, 2));
    process.exit(1);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const fileEnv = loadEnvFile(args.envFile);
  const env = { ...fileEnv.values, ...process.env };
  const result = await validateCookieConfig(env, {
    providers: args.providers,
    envFile: args.envFile,
    envFileExists: fileEnv.exists,
    timeoutMs: args.timeoutMs,
    quarkBaseUrl: args.quarkBaseUrl,
    baiduBaseUrl: args.baiduBaseUrl,
    baiduAppId: args.baiduAppId,
    fetchImpl: globalThis.fetch
  });

  if (args.format === "json") {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(formatCookieCheckResult(result));
  }

  if (!result.ok) process.exit(1);
}

function parseArgs(argv) {
  const parsed = {
    providers: ["quark", "baidu"],
    envFile: DEFAULT_ENV_FILE,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    format: "json",
    quarkBaseUrl: PROVIDERS.quark.baseUrl,
    baiduBaseUrl: PROVIDERS.baidu.baseUrl,
    baiduAppId: DEFAULT_BAIDU_APP_ID
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--provider" || arg === "--providers") {
      parsed.providers = parseProviders(argv[++index] || "all");
    } else if (arg === "--env-file" || arg === "--dotenv" || arg === "--config") {
      parsed.envFile = argv[++index] || DEFAULT_ENV_FILE;
    } else if (arg === "--timeout-ms") {
      parsed.timeoutMs = Number(argv[++index] || DEFAULT_TIMEOUT_MS);
    } else if (arg === "--quark-base-url") {
      parsed.quarkBaseUrl = argv[++index] || PROVIDERS.quark.baseUrl;
    } else if (arg === "--baidu-base-url") {
      parsed.baiduBaseUrl = argv[++index] || PROVIDERS.baidu.baseUrl;
    } else if (arg === "--baidu-app-id") {
      parsed.baiduAppId = argv[++index] || DEFAULT_BAIDU_APP_ID;
    } else if (arg === "--json") {
      parsed.format = "json";
    } else if (arg === "--format") {
      parsed.format = argv[++index] || "text";
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else {
      parsed.providers = parseProviders(arg);
    }
  }

  return parsed;
}

async function validateCookieConfig(env = {}, options = {}) {
  const providers = normalizeProviders(options.providers || ["quark", "baidu"]);
  const results = [];

  for (const providerName of providers) {
    const config = PROVIDERS[providerName];
    const cookie = String(env[config.cookieEnv] || "").trim();
    const cookiePreview = cookie ? maskSecret(cookie) : "";

    if (!cookie) {
      results.push({
        provider: config.provider,
        label: config.label,
        ok: false,
        state: "missing",
        stateLabel: stateToLabel("missing"),
        cookieEnv: config.cookieEnv,
        cookieConfigured: false,
        cookiePreview,
        message: `未配置 ${config.cookieEnv}。请先登录${config.label}网页，复制完整 Cookie。`
      });
      continue;
    }

    try {
      const result = await checkProviderCookie({
        config,
        cookie,
        cookiePreview,
        fetchImpl: options.fetchImpl || globalThis.fetch,
        timeoutMs: options.timeoutMs || DEFAULT_TIMEOUT_MS,
        baseUrl: providerName === "quark" ? options.quarkBaseUrl : options.baiduBaseUrl,
        appId: options.baiduAppId
      });
      results.push(result);
    } catch (error) {
      const classified = classifyCookieCheckError(error);
      results.push({
        provider: config.provider,
        label: config.label,
        ok: false,
        state: classified.state,
        stateLabel: stateToLabel(classified.state),
        cookieEnv: config.cookieEnv,
        cookieConfigured: true,
        cookiePreview,
        message: classified.message
      });
    }
  }

  const validProviders = results.filter((item) => item.ok).map((item) => item.provider);
  const nextAction = decideNextAction(results);
  return {
    ok: validProviders.length > 0,
    tool: "check-cookies",
    mode: "agent-json",
    nextAction,
    validProviders,
    recommendations: nextAction === "ready" ? [] : buildRecommendations(results),
    secretsMasked: true,
    envFile: options.envFile || DEFAULT_ENV_FILE,
    envFileExists: options.envFileExists !== false,
    results
  };
}

async function checkProviderCookie({ config, cookie, cookiePreview, fetchImpl, timeoutMs, baseUrl, appId }) {
  if (typeof fetchImpl !== "function") {
    throw new Error("当前 Node.js 环境没有 fetch，请升级到 Node.js 20 或更新版本。");
  }
  const url = config.buildUrl({
    baseUrl: baseUrl || config.baseUrl,
    appId
  });
  const response = await fetchJsonWithTimeout(url, {
    fetchImpl,
    timeoutMs,
    cookie
  });
  const classified = config.classify(response);
  return {
    provider: config.provider,
    label: config.label,
    ok: classified.state === "valid",
    state: classified.state,
    stateLabel: stateToLabel(classified.state),
    cookieEnv: config.cookieEnv,
    cookieConfigured: true,
    cookiePreview,
    message: classified.message,
    account: classified.account || "",
    endpoint: String(url.origin)
  };
}

async function fetchJsonWithTimeout(url, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeoutMs || DEFAULT_TIMEOUT_MS);
  try {
    const response = await options.fetchImpl(url, {
      method: "GET",
      headers: {
        Accept: "application/json, text/plain, */*",
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        Cookie: options.cookie
      },
      signal: controller.signal
    });
    const text = await response.text();
    let json;
    try {
      json = text ? JSON.parse(text) : {};
    } catch {
      throw new Error(`接口没有返回 JSON：${text.slice(0, 120)}`);
    }
    return {
      ok: Boolean(response.ok),
      status: response.status,
      json
    };
  } finally {
    clearTimeout(timeout);
  }
}

function classifyQuarkResponse(response) {
  if (!response.ok) {
    return {
      state: response.status === 401 || response.status === 403 ? "invalid" : "network_error",
      message:
        response.status === 401 || response.status === 403
          ? "夸克 Cookie 已失效或权限不足，请重新登录夸克网盘后复制完整 Cookie。"
          : `夸克接口请求失败：HTTP ${response.status}。`
    };
  }
  const code = response.json?.code;
  if (code === 0 || code === "0") {
    return { state: "valid", message: "夸克 Cookie 有效，可以读取网盘目录。" };
  }
  return {
    state: "invalid",
    message: `夸克 Cookie 可能已失效，请重新复制夸克网盘 Cookie。接口返回：${response.json?.message || response.json?.status || code || "unknown"}`
  };
}

function classifyBaiduResponse(response) {
  if (!response.ok) {
    return {
      state: response.status === 401 || response.status === 403 ? "invalid" : "network_error",
      message:
        response.status === 401 || response.status === 403
          ? "百度 Cookie 已失效或权限不足，请重新登录百度网盘后复制完整 Cookie。"
          : `百度接口请求失败：HTTP ${response.status}。`
    };
  }
  const errno = Number(response.json?.errno ?? 0);
  if (errno === 0) {
    const account = response.json?.username || response.json?.baidu_name || response.json?.netdisk_name || "";
    return {
      state: "valid",
      message: account ? `百度 Cookie 有效，当前账号：${account}。` : "百度 Cookie 有效，可以读取账号信息。",
      account
    };
  }
  return {
    state: "invalid",
    message: `百度 Cookie 可能已失效，请重新复制百度网盘 Cookie。接口返回 errno=${errno}。`
  };
}

function classifyCookieCheckError(error) {
  const message = error?.message || String(error);
  if (error?.name === "AbortError") {
    return {
      state: "network_error",
      message: "网络请求超时，请确认当前机器能访问对应网盘网页。"
    };
  }
  if (/fetch failed|ECONN|ENOTFOUND|network/i.test(message)) {
    return {
      state: "network_error",
      message: "网络请求失败，请确认当前机器能访问对应网盘网页。"
    };
  }
  return {
    state: "unknown_error",
    message
  };
}

function formatCookieCheckResult(result) {
  const lines = ["### Cookie 有效性检查", ""];
  if (!result.envFileExists) {
    lines.push(`- 未找到配置文件：${result.envFile}`, "- 请先复制 `.env.example` 为 `.env`，再填写 Cookie。", "");
  }
  for (const item of result.results || []) {
    const stateLabel = stateToLabel(item.state);
    const preview = item.cookiePreview ? `，当前值：${item.cookiePreview}` : "";
    lines.push(`- ${item.label}: ${stateLabel}${preview}`);
    lines.push(`  ${item.message}`);
  }
  lines.push("");
  lines.push(result.ok ? "结果：Cookie 可用。" : "结果：有 Cookie 需要重新获取或补充。");
  return lines.join("\n");
}

function stateToLabel(state) {
  if (state === "valid") return "有效";
  if (state === "missing") return "未填写";
  if (state === "invalid") return "失效或不完整";
  if (state === "network_error") return "网络异常";
  return "检查失败";
}

function decideNextAction(results) {
  if (results.some((item) => item.ok)) return "ready";
  if (results.some((item) => item.state === "missing")) return "configure_missing_cookies";
  if (results.some((item) => item.state === "invalid")) return "refresh_invalid_cookies";
  if (results.some((item) => item.state === "network_error")) return "retry_network_or_check_access";
  if (results.some((item) => item.state === "unknown_error")) return "inspect_error";
  return "ready";
}

function buildRecommendations(results) {
  const recommendations = [];
  for (const item of results) {
    if (item.state === "missing") {
      recommendations.push(`填写 ${item.cookieEnv}。`);
    } else if (item.state === "invalid") {
      recommendations.push(`重新登录${item.label}，复制完整 Cookie 后更新 ${item.cookieEnv}。`);
    } else if (item.state === "network_error") {
      recommendations.push(`确认当前机器能访问${item.label}网页，然后重新运行检查。`);
    } else if (item.state === "unknown_error") {
      recommendations.push(`查看 ${item.label} 检查错误信息。`);
    }
  }
  return recommendations;
}

function loadEnvFile(envFile) {
  if (!envFile || !fs.existsSync(envFile)) return { exists: false, values: {} };
  return {
    exists: true,
    values: parseDotEnv(fs.readFileSync(envFile, "utf8"))
  };
}

function parseProviders(value) {
  if (!value || value === "all") return ["quark", "baidu"];
  return normalizeProviders(String(value).split(",").map((item) => item.trim()).filter(Boolean));
}

function normalizeProviders(providers) {
  const normalized = providers.map((item) => String(item).trim()).filter(Boolean);
  for (const provider of normalized) {
    if (!PROVIDERS[provider]) {
      throw new Error(`不支持的 Cookie 检查对象：${provider}。可选值：quark, baidu, all。`);
    }
  }
  return normalized;
}

function normalizeBaseUrl(value) {
  return String(value || "").replace(/\/+$/g, "");
}

function isCliEntryPoint() {
  return Boolean(process.argv[1]) && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

export {
  classifyCookieCheckError,
  classifyBaiduResponse,
  classifyQuarkResponse,
  formatCookieCheckResult,
  parseArgs,
  validateCookieConfig
};
