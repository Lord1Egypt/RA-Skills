#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { parseBaiduSavePath } from "./baidu-save.mjs";
import { parseDotEnv, validateSkillEnv } from "./check-env.mjs";
import { validateCookieConfig } from "./check-cookies.mjs";
import { parseQuarkFolderUrl } from "./quark-save.mjs";

const DEFAULT_ENV_FILE = ".env";
const DEFAULT_TIMEOUT_MS = 20_000;
const DEFAULT_BAIDU_APP_ID = "250528";
const QUARK_API_BASE = "https://drive-pc.quark.cn";
const BAIDU_API_BASE = "https://pan.baidu.com";

if (isCliEntryPoint()) {
  main().catch((error) => {
    console.error(JSON.stringify({ ok: false, error: error.message || String(error) }, null, 2));
    process.exit(1);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const loaded = loadEnvFile(args.envFile);
  const env = { ...loaded.values, ...process.env };
  const result = await validateReadyConfig(env, {
    envFile: args.envFile,
    envFileExists: loaded.exists,
    timeoutMs: args.timeoutMs,
    fetchImpl: globalThis.fetch
  });

  if (args.format === "text") {
    console.log(formatReadyResult(result));
  } else {
    console.log(JSON.stringify(result, null, 2));
  }

  if (!result.ok) process.exit(1);
}

function parseArgs(argv) {
  const parsed = {
    envFile: DEFAULT_ENV_FILE,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    format: "json"
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--env-file" || arg === "--dotenv" || arg === "--config") {
      parsed.envFile = argv[++index] || DEFAULT_ENV_FILE;
    } else if (arg === "--timeout-ms") {
      parsed.timeoutMs = Number(argv[++index] || DEFAULT_TIMEOUT_MS);
    } else if (arg === "--json") {
      parsed.format = "json";
    } else if (arg === "--format") {
      parsed.format = argv[++index] || "json";
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else {
      parsed.envFile = arg;
    }
  }

  return parsed;
}

async function validateReadyConfig(env = {}, options = {}) {
  const fetchImpl = options.fetchImpl || globalThis.fetch;
  const envCheck = validateSkillEnv(env, {
    envFile: options.envFile || DEFAULT_ENV_FILE,
    envFileExists: options.envFileExists !== false
  });
  const configuredProviders = envCheck.providerResults
    .filter((item) => item.ok)
    .map((item) => item.provider);
  const cookieCheck = await validateCookieConfig(env, {
    providers: configuredProviders.length > 0 ? configuredProviders : ["quark", "baidu"],
    envFile: options.envFile || DEFAULT_ENV_FILE,
    envFileExists: options.envFileExists !== false,
    timeoutMs: options.timeoutMs || DEFAULT_TIMEOUT_MS,
    fetchImpl
  });
  const validProviders = configuredProviders.filter((provider) => cookieCheck.validProviders?.includes(provider));

  const openList = await checkOpenListTarget({
    baseUrl: env.OPENLIST_BASE_URL,
    token: env.OPENLIST_TOKEN,
    targetPath: env.OPENLIST_DEFAULT_COPY_DST_PATH,
    timeoutMs: options.timeoutMs || DEFAULT_TIMEOUT_MS,
    fetchImpl
  });

  const providerTargets = [];
  if (validProviders.includes("quark")) {
    providerTargets.push(await checkQuarkSaveTarget({
      cookie: env.QUARK_COOKIE,
      target: env.QUARK_DEFAULT_SAVE_URL,
      timeoutMs: options.timeoutMs || DEFAULT_TIMEOUT_MS,
      fetchImpl
    }));
  }
  if (validProviders.includes("baidu")) {
    providerTargets.push(await checkBaiduSaveTarget({
      cookie: env.BAIDU_COOKIE,
      target: env.BAIDU_DEFAULT_SAVE_PATH,
      timeoutMs: options.timeoutMs || DEFAULT_TIMEOUT_MS,
      fetchImpl
    }));
  }

  const nextAction = decideReadyNextAction({
    envCheck,
    cookieCheck,
    openList,
    providerTargets
  });
  return {
    ok: nextAction === "ready",
    tool: "check-ready",
    mode: "agent-json",
    nextAction,
    recommendations: buildReadyRecommendations({
      envCheck,
      cookieCheck,
      openList,
      providerTargets
    }),
    env: {
      ok: envCheck.ok,
      nextAction: envCheck.nextAction,
      providerOk: envCheck.providerOk,
      missing: envCheck.missing,
      invalid: envCheck.invalid
    },
    cookies: cookieCheck,
    openList,
    validProviders,
    providerTargets
  };
}

async function checkOpenListTarget({ baseUrl, token, targetPath, timeoutMs, fetchImpl }) {
  if (!baseUrl || !token || !targetPath) {
    return {
      ok: false,
      state: "missing",
      path: targetPath || "",
      message: "OpenList 地址、Token 或 NAS 备份目标路径未配置完整。"
    };
  }
  try {
    const url = `${normalizeBaseUrl(baseUrl)}/api/fs/list`;
    const response = await fetchJsonWithTimeout(url, {
      fetchImpl,
      timeoutMs,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: token
      },
      body: JSON.stringify({
        path: targetPath,
        password: "",
        page: 1,
        per_page: 20,
        refresh: true
      })
    });
    const success = response.ok && (response.json?.code === 200 || response.json?.code === 0 || response.json?.message === "success");
    return {
      ok: success,
      state: success ? "reachable" : "unreachable",
      path: targetPath,
      status: response.status,
      code: response.json?.code ?? null,
      message: success ? "OpenList/NAS 目标目录可访问。" : response.json?.message || "OpenList/NAS 目标目录不可访问。",
      itemCount: Array.isArray(response.json?.data?.content) ? response.json.data.content.length : null
    };
  } catch (error) {
    return {
      ok: false,
      state: "network_error",
      path: targetPath,
      message: error.message || String(error)
    };
  }
}

async function checkBaiduSaveTarget({ cookie, target, timeoutMs, fetchImpl }) {
  try {
    const targetPath = parseBaiduSavePath(target);
    const url = new URL(`${BAIDU_API_BASE}/rest/2.0/xpan/file`);
    url.searchParams.set("method", "list");
    url.searchParams.set("app_id", DEFAULT_BAIDU_APP_ID);
    url.searchParams.set("dir", targetPath);
    url.searchParams.set("page", "1");
    url.searchParams.set("num", "1");
    const response = await fetchJsonWithTimeout(url, {
      fetchImpl,
      timeoutMs,
      headers: {
        Accept: "application/json, text/plain, */*",
        Cookie: cookie
      }
    });
    const errno = Number(response.json?.errno ?? 0);
    return {
      provider: "baidu",
      label: "百度网盘",
      ok: response.ok && errno === 0,
      state: response.ok && errno === 0 ? "reachable" : "unreachable",
      targetPath,
      message: response.ok && errno === 0 ? "百度默认保存目录可访问。" : `百度默认保存目录不可访问：errno=${errno}。`
    };
  } catch (error) {
    return {
      provider: "baidu",
      label: "百度网盘",
      ok: false,
      state: "error",
      targetPath: target || "",
      message: error.message || String(error)
    };
  }
}

async function checkQuarkSaveTarget({ cookie, target, timeoutMs, fetchImpl }) {
  try {
    const parsed = parseQuarkFolderUrl(target);
    if (parsed.needsResolution) {
      const resolved = await resolveQuarkPath({
        cookie,
        targetPath: parsed.path,
        timeoutMs,
        fetchImpl
      });
      return {
        provider: "quark",
        label: "夸克网盘",
        ok: true,
        state: "reachable",
        targetPath: parsed.path,
        fid: resolved.fid,
        message: "夸克默认保存路径可解析并访问。"
      };
    }
    await listQuarkDirectory({
      cookie,
      pdirFid: parsed.fid,
      timeoutMs,
      fetchImpl
    });
    return {
      provider: "quark",
      label: "夸克网盘",
      ok: true,
      state: "reachable",
      targetPath: target,
      fid: parsed.fid,
      message: "夸克默认保存目录可访问。"
    };
  } catch (error) {
    return {
      provider: "quark",
      label: "夸克网盘",
      ok: false,
      state: "error",
      targetPath: target || "",
      message: error.message || String(error)
    };
  }
}

async function resolveQuarkPath({ cookie, targetPath, timeoutMs, fetchImpl }) {
  const segments = splitCloudDrivePath(targetPath);
  let pdirFid = "0";
  let current = { fid: "0", name: "/", path: "/" };
  for (const segment of segments) {
    const items = await listQuarkDirectory({ cookie, pdirFid, timeoutMs, fetchImpl });
    const match = items.find((item) => item.isDir && item.name === segment);
    if (!match) throw new Error(`夸克目录不存在：${joinCloudPath(current.path, segment)}。`);
    current = {
      fid: match.fid,
      name: match.name,
      path: joinCloudPath(current.path, match.name)
    };
    pdirFid = match.fid;
  }
  return current;
}

async function listQuarkDirectory({ cookie, pdirFid, timeoutMs, fetchImpl }) {
  const url = new URL(`${QUARK_API_BASE}/1/clouddrive/file/sort`);
  url.searchParams.set("pr", "ucpro");
  url.searchParams.set("fr", "pc");
  url.searchParams.set("uc_param_str", "");
  url.searchParams.set("pdir_fid", pdirFid || "0");
  url.searchParams.set("_page", "1");
  url.searchParams.set("_size", "200");
  url.searchParams.set("_fetch_total", "1");
  url.searchParams.set("_fetch_sub_dirs", "0");
  url.searchParams.set("_sort", "file_type:asc,updated_at:desc");
  const response = await fetchJsonWithTimeout(url, {
    fetchImpl,
    timeoutMs,
    headers: {
      Accept: "application/json, text/plain, */*",
      Cookie: cookie
    }
  });
  const code = response.json?.code;
  if (!response.ok || !(code === 0 || code === "0")) {
    throw new Error(`夸克目录读取失败：${response.json?.message || response.status || code || "unknown"}。`);
  }
  return (response.json?.data?.list || []).map((item) => ({
    fid: item.fid,
    name: item.file_name || item.name || "",
    isDir: Boolean(item.dir)
  }));
}

async function fetchJsonWithTimeout(url, options = {}) {
  if (typeof options.fetchImpl !== "function") {
    throw new Error("当前 Node.js 环境没有 fetch，请升级到 Node.js 20 或更新版本。");
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeoutMs || DEFAULT_TIMEOUT_MS);
  try {
    const response = await options.fetchImpl(url, {
      method: options.method || "GET",
      headers: {
        Accept: "application/json, text/plain, */*",
        ...(options.headers || {})
      },
      body: options.body,
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

function decideReadyNextAction({ envCheck, cookieCheck, openList, providerTargets }) {
  if (!envCheck.ok) return envCheck.nextAction;
  if (!cookieCheck.ok) return cookieCheck.nextAction;
  if (!openList.ok) return "fix_openlist_target";
  if (!providerTargets.some((item) => item.ok)) return "fix_provider_target";
  return "ready";
}

function buildReadyRecommendations({ envCheck, cookieCheck, openList, providerTargets }) {
  const recommendations = [];
  if (!envCheck.ok) {
    recommendations.push(...envCheck.missing.map((item) => `填写 ${item.key}。`));
    recommendations.push(...envCheck.invalid.map((item) => `修正 ${item.key} 的格式。`));
    if (!envCheck.providerOk) {
      recommendations.push("至少配置一个完整网盘：夸克需要 QUARK_COOKIE + QUARK_DEFAULT_SAVE_URL，百度需要 BAIDU_COOKIE + BAIDU_DEFAULT_SAVE_PATH。");
    }
  }
  if (!cookieCheck.ok) recommendations.push(...(cookieCheck.recommendations || []));
  if (!openList.ok) recommendations.push(`检查 OpenList/NAS 目标路径：${openList.path || "-"}`);
  for (const target of providerTargets.filter((item) => !item.ok)) {
    recommendations.push(`检查${target.label}保存目录：${target.targetPath || "-"}`);
  }
  return [...new Set(recommendations)];
}

function formatReadyResult(result) {
  const lines = ["### Resource 2 NAS 全面检查", ""];
  lines.push(`- ENV: ${result.env.ok ? "通过" : "需要处理"} (${result.env.nextAction})`);
  lines.push(`- Cookie: ${result.cookies.ok ? "通过" : "需要处理"} (${result.cookies.nextAction})`);
  lines.push(`- OpenList/NAS: ${result.openList.ok ? "通过" : "需要处理"} (${result.openList.path || "-"})`);
  for (const target of result.providerTargets) {
    lines.push(`- ${target.label}保存目录: ${target.ok ? "通过" : "需要处理"} (${target.targetPath || "-"})`);
  }
  if (result.recommendations.length > 0) {
    lines.push("", "需要处理：");
    for (const item of result.recommendations) lines.push(`- ${item}`);
  }
  lines.push("", result.ok ? "结果：配置和只读连通性检查通过。" : "结果：还不能开始完整保存/复制流程。");
  return lines.join("\n");
}

function loadEnvFile(envFile) {
  if (!envFile || !fs.existsSync(envFile)) return { exists: false, values: {} };
  return {
    exists: true,
    values: parseDotEnv(fs.readFileSync(envFile, "utf8"))
  };
}

function normalizeBaseUrl(value) {
  return String(value || "").replace(/\/+$/g, "");
}

function splitCloudDrivePath(value) {
  return String(value || "")
    .split("/")
    .map((item) => item.trim())
    .filter(Boolean);
}

function joinCloudPath(basePath, name) {
  const base = `/${splitCloudDrivePath(basePath).join("/")}`;
  const cleanName = String(name || "").replace(/^\/+/g, "");
  return base === "/" ? `/${cleanName}` : `${base}/${cleanName}`;
}

function isCliEntryPoint() {
  return Boolean(process.argv[1]) && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

export {
  parseArgs,
  validateReadyConfig
};
