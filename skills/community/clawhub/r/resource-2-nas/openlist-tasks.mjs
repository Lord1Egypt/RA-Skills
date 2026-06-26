#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { parseDotEnv } from "./check-env.mjs";

const DEFAULT_ENV_FILE = ".env";
const DEFAULT_TIMEOUT_MS = 20_000;
const DEFAULT_GROUP = "copy";
const DEFAULT_STATE = "undone";
const TASK_GROUPS = new Set(["copy", "offline_download", "offline_download_transfer", "upload", "decompress", "decompress_upload"]);
const TASK_STATES = new Set(["undone", "done"]);

if (isCliEntryPoint()) {
  main().catch((error) => {
    console.error(JSON.stringify({ ok: false, error: error.message || String(error) }, null, 2));
    process.exit(1);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const env = loadEnv(args.envFile);
  const result = await runOpenListTasks({
    env,
    args,
    fetchImpl: globalThis.fetch
  });

  if (args.format === "text") {
    console.log(formatTaskResult(result));
  } else {
    console.log(JSON.stringify(result, null, 2));
  }

  if (!result.ok) process.exit(1);
}

function parseArgs(argv) {
  const parsed = {
    action: "list",
    group: DEFAULT_GROUP,
    state: DEFAULT_STATE,
    ids: [],
    match: "",
    provider: "",
    sourcePrefix: "",
    envFile: DEFAULT_ENV_FILE,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    yes: false,
    format: "json"
  };
  const positionals = [];

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--group") {
      parsed.group = normalizeGroup(argv[++index] || DEFAULT_GROUP);
    } else if (arg === "--state") {
      parsed.state = normalizeState(argv[++index] || DEFAULT_STATE);
    } else if (arg === "--ids" || arg === "--id") {
      parsed.ids.push(...parseList(argv[++index] || ""));
    } else if (arg === "--match") {
      parsed.match = argv[++index] || "";
    } else if (arg === "--provider") {
      parsed.provider = argv[++index] || "";
    } else if (arg === "--source-prefix" || arg === "--src-prefix") {
      parsed.sourcePrefix = argv[++index] || "";
    } else if (arg === "--env-file" || arg === "--dotenv" || arg === "--config") {
      parsed.envFile = argv[++index] || DEFAULT_ENV_FILE;
    } else if (arg === "--timeout-ms") {
      parsed.timeoutMs = Number(argv[++index] || DEFAULT_TIMEOUT_MS);
    } else if (arg === "--base-url") {
      parsed.baseUrl = argv[++index] || "";
    } else if (arg === "--token") {
      parsed.token = argv[++index] || "";
    } else if (arg === "--yes" || arg === "-y") {
      parsed.yes = true;
    } else if (arg === "--json") {
      parsed.format = "json";
    } else if (arg === "--format") {
      parsed.format = argv[++index] || "json";
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else {
      positionals.push(arg);
    }
  }

  if (positionals[0]) parsed.action = normalizeAction(positionals[0]);
  if (positionals[1]) parsed.group = normalizeGroup(positionals[1]);
  if (positionals[2]) parsed.state = normalizeState(positionals[2]);
  return parsed;
}

async function runOpenListTasks({ env = {}, args = {}, fetchImpl = globalThis.fetch }) {
  const group = normalizeGroup(args.group || DEFAULT_GROUP);
  const state = normalizeState(args.state || DEFAULT_STATE);
  const action = normalizeAction(args.action || "list");
  const context = buildOpenListContext(env, args, fetchImpl);
  const listed = await listTasks({ ...context, group, state });
  const filteredTasks = filterTasks(listed.tasks, args);
  const baseResult = {
    ok: true,
    tool: "openlist-tasks",
    mode: "agent-json",
    action,
    group,
    state,
    nextAction: "report_tasks",
    filter: {
      ids: args.ids || [],
      match: args.match || "",
      provider: args.provider || "",
      sourcePrefix: args.sourcePrefix || ""
    },
    totalCount: listed.tasks.length,
    matchedCount: filteredTasks.length,
    tasks: filteredTasks
  };

  if (action === "list") return baseResult;

  if (action === "cancel") {
    if (filteredTasks.length === 0) {
      return {
        ...baseResult,
        dryRun: !args.yes,
        nextAction: "no_matching_tasks",
        matchedIds: []
      };
    }
    const matchedIds = filteredTasks.map((task) => task.id).filter(Boolean);
    if (!args.yes) {
      return {
        ...baseResult,
        dryRun: true,
        nextAction: "confirm_task_cancel",
        matchedIds
      };
    }
    const cancelResult = await cancelTasks({ ...context, group, ids: matchedIds });
    return {
      ...baseResult,
      ok: cancelResult.ok,
      dryRun: false,
      nextAction: cancelResult.ok ? "verify_tasks_cancelled" : "inspect_cancel_errors",
      matchedIds,
      cancelledIds: cancelResult.cancelledIds,
      cancelErrors: cancelResult.errors
    };
  }

  throw new Error(`Unsupported action: ${action}`);
}

function filterTasks(tasks, filters = {}) {
  let result = tasks.map(normalizeTask).filter((task) => task.id);
  if (filters.ids && filters.ids.length > 0) {
    const ids = new Set(filters.ids);
    result = result.filter((task) => ids.has(task.id));
  }
  if (filters.provider) {
    const provider = String(filters.provider).toLowerCase();
    result = result.filter((task) => taskMatchesProvider(task, provider));
  }
  if (filters.sourcePrefix) {
    const sourcePrefix = String(filters.sourcePrefix);
    result = result.filter((task) => task.name.includes(`](${sourcePrefix}`) || task.name.includes(sourcePrefix));
  }
  if (filters.match) {
    const needle = String(filters.match);
    result = result.filter((task) => task.name.includes(needle) || task.id.includes(needle));
  }
  return result;
}

async function listTasks({ baseUrl, token, fetchImpl, timeoutMs, group, state }) {
  const response = await fetchOpenListJson({
    baseUrl,
    token,
    fetchImpl,
    timeoutMs,
    path: `/api/task/${group}/${state}`,
    method: "GET"
  });
  const success = response.ok && isOpenListSuccess(response.json);
  if (!success) {
    throw new Error(`OpenList task list failed: ${response.json?.message || response.status || "unknown"}`);
  }
  return {
    tasks: Array.isArray(response.json?.data) ? response.json.data.map(normalizeTask) : []
  };
}

async function cancelTasks({ baseUrl, token, fetchImpl, timeoutMs, group, ids }) {
  const response = await fetchOpenListJson({
    baseUrl,
    token,
    fetchImpl,
    timeoutMs,
    path: `/api/task/${group}/cancel_some`,
    method: "POST",
    body: JSON.stringify(ids)
  });
  const success = response.ok && isOpenListSuccess(response.json);
  const errors = response.json?.data && typeof response.json.data === "object" ? response.json.data : {};
  return {
    ok: success && Object.keys(errors).length === 0,
    cancelledIds: ids.filter((id) => !errors[id]),
    errors
  };
}

async function fetchOpenListJson({ baseUrl, token, fetchImpl, timeoutMs, path: apiPath, method, body }) {
  if (!baseUrl || !token) throw new Error("OPENLIST_BASE_URL 或 OPENLIST_TOKEN 缺失。");
  if (typeof fetchImpl !== "function") throw new Error("当前 Node.js 环境没有 fetch，请升级到 Node.js 20 或更新版本。");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs || DEFAULT_TIMEOUT_MS);
  try {
    const response = await fetchImpl(`${normalizeBaseUrl(baseUrl)}${apiPath}`, {
      method,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: token
      },
      body,
      signal: controller.signal
    });
    const text = await response.text();
    let json;
    try {
      json = text ? JSON.parse(text) : {};
    } catch {
      throw new Error(`接口没有返回 JSON：${text.slice(0, 120)}`);
    }
    return { ok: Boolean(response.ok), status: response.status, json };
  } finally {
    clearTimeout(timeout);
  }
}

function normalizeTask(task = {}) {
  return {
    id: String(task.id || ""),
    name: String(task.name || ""),
    creator: task.creator || "",
    creatorRole: task.creator_role ?? task.creatorRole ?? null,
    state: task.state ?? null,
    status: task.status || "",
    progress: task.progress ?? null,
    startTime: task.start_time || task.startTime || "",
    endTime: task.end_time || task.endTime || "",
    totalBytes: task.total_bytes ?? task.totalBytes ?? null,
    error: task.error || ""
  };
}

function taskMatchesProvider(task, provider) {
  if (provider === "baidu") {
    return task.name.includes("[/bdy]") || task.name.includes("/NAS资源下载") || task.name.includes("baidu");
  }
  if (provider === "quark") {
    return task.name.includes("[/pan/quark]") || task.name.includes("/备份资源") || task.name.includes("quark");
  }
  return task.name.toLowerCase().includes(provider);
}

function buildOpenListContext(env, args, fetchImpl) {
  return {
    baseUrl: args.baseUrl || env.OPENLIST_BASE_URL,
    token: args.token || env.OPENLIST_TOKEN,
    fetchImpl,
    timeoutMs: args.timeoutMs || DEFAULT_TIMEOUT_MS
  };
}

function formatTaskResult(result) {
  const lines = [`### OpenList ${result.group} ${result.action}`, ""];
  lines.push(`匹配任务：${result.matchedCount}/${result.totalCount}`);
  for (const task of result.tasks || []) {
    lines.push(`- ${task.id}: ${task.name} (${task.status || task.state || "-"}) ${task.progress ?? "-"}%`);
    if (task.error) lines.push(`  error: ${task.error}`);
  }
  if (result.action === "cancel") {
    lines.push("", result.dryRun ? "未取消：请确认后加 --yes。" : `已请求取消：${(result.cancelledIds || []).length} 个。`);
  }
  return lines.join("\n");
}

function loadEnv(envFile) {
  const fileEnv = envFile && fs.existsSync(envFile) ? parseDotEnv(fs.readFileSync(envFile, "utf8")) : {};
  return { ...fileEnv, ...process.env };
}

function parseList(value) {
  return String(value || "").split(",").map((item) => item.trim()).filter(Boolean);
}

function normalizeAction(value) {
  const action = String(value || "list").trim();
  if (["list", "cancel"].includes(action)) return action;
  throw new Error(`Unsupported action: ${value}. 可选值：list, cancel。`);
}

function normalizeGroup(value) {
  const group = String(value || DEFAULT_GROUP).trim();
  if (TASK_GROUPS.has(group)) return group;
  throw new Error(`Unsupported task group: ${value}`);
}

function normalizeState(value) {
  const state = String(value || DEFAULT_STATE).trim();
  if (TASK_STATES.has(state)) return state;
  throw new Error(`Unsupported task state: ${value}`);
}

function isOpenListSuccess(json) {
  return json?.code === 200 || json?.code === 0 || json?.message === "success";
}

function normalizeBaseUrl(value) {
  return String(value || "").replace(/\/+$/g, "");
}

function isCliEntryPoint() {
  return Boolean(process.argv[1]) && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

export {
  filterTasks,
  parseArgs,
  runOpenListTasks
};
