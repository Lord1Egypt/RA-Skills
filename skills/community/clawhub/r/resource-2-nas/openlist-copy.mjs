#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { parseDotEnv } from "./check-env.mjs";

const DEFAULT_ENV_FILE = ".env";
const DEFAULT_TIMEOUT_MS = 20_000;
const DEFAULT_INTERVAL_MS = 2_000;
const DEFAULT_POLL_TIMEOUT_MS = 120_000;

if (isCliEntryPoint()) {
  main().catch((error) => {
    console.error(JSON.stringify({ ok: false, error: error.message || String(error) }, null, 2));
    process.exit(1);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const env = loadEnv(args.envFile);
  const result = await runOpenListCopy({
    env,
    args,
    fetchImpl: globalThis.fetch
  });

  if (args.format === "text") {
    console.log(formatCopyResult(result));
  } else {
    console.log(JSON.stringify(result, null, 2));
  }

  if (!result.ok) process.exit(1);
}

function parseArgs(argv) {
  const parsed = {
    srcDir: "",
    dstDir: "",
    names: [],
    envFile: DEFAULT_ENV_FILE,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    intervalMs: DEFAULT_INTERVAL_MS,
    pollTimeoutMs: DEFAULT_POLL_TIMEOUT_MS,
    poll: true,
    yes: false,
    format: "json",
    baseUrl: "",
    token: ""
  };
  const positionals = [];

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--src-dir" || arg === "--source") {
      parsed.srcDir = argv[++index] || "";
    } else if (arg === "--dst-dir" || arg === "--dest" || arg === "--target") {
      parsed.dstDir = argv[++index] || "";
    } else if (arg === "--name") {
      parsed.names.push(argv[++index] || "");
    } else if (arg === "--names") {
      parsed.names.push(...parseList(argv[++index] || ""));
    } else if (arg === "--env-file" || arg === "--dotenv" || arg === "--config") {
      parsed.envFile = argv[++index] || DEFAULT_ENV_FILE;
    } else if (arg === "--timeout-ms") {
      parsed.timeoutMs = Number(argv[++index] || DEFAULT_TIMEOUT_MS);
    } else if (arg === "--interval-ms") {
      parsed.intervalMs = Number(argv[++index] || DEFAULT_INTERVAL_MS);
    } else if (arg === "--poll-timeout-ms") {
      parsed.pollTimeoutMs = Number(argv[++index] || DEFAULT_POLL_TIMEOUT_MS);
    } else if (arg === "--no-poll") {
      parsed.poll = false;
    } else if (arg === "--poll") {
      parsed.poll = true;
    } else if (arg === "--yes" || arg === "-y") {
      parsed.yes = true;
    } else if (arg === "--json") {
      parsed.format = "json";
    } else if (arg === "--format") {
      parsed.format = argv[++index] || "json";
    } else if (arg === "--base-url") {
      parsed.baseUrl = argv[++index] || "";
    } else if (arg === "--token") {
      parsed.token = argv[++index] || "";
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else {
      positionals.push(arg);
    }
  }

  if (!parsed.srcDir && positionals[0]) parsed.srcDir = positionals[0];
  if (!parsed.dstDir && positionals[1]) parsed.dstDir = positionals[1];
  if (parsed.names.length === 0 && positionals.length > 2) parsed.names.push(...positionals.slice(2));
  parsed.names = parsed.names.map((name) => String(name || "").trim()).filter(Boolean);
  return parsed;
}

async function runOpenListCopy({ env = {}, args = {}, fetchImpl = globalThis.fetch }) {
  const srcDir = normalizeOpenListPath(args.srcDir);
  const dstDir = normalizeOpenListPath(args.dstDir || env.OPENLIST_DEFAULT_COPY_DST_PATH);
  const names = (args.names || []).map((name) => String(name || "").trim()).filter(Boolean);
  const context = buildOpenListContext(env, args, fetchImpl);

  if (!srcDir) throw new Error("缺少 OpenList 源目录。请传 --src-dir。");
  if (!dstDir) throw new Error("缺少 OpenList 目标目录。请传 --dst-dir 或配置 OPENLIST_DEFAULT_COPY_DST_PATH。");
  if (names.length === 0) throw new Error("缺少要复制的对象名。请传 --name 或 --names。");

  const sourceListing = await listDirectory({ ...context, dirPath: srcDir, refresh: true });
  const destinationListing = await listDirectory({ ...context, dirPath: dstDir, refresh: true });
  const sourceNames = new Set(sourceListing.items.map((item) => item.name));
  const destinationNames = new Set(destinationListing.items.map((item) => item.name));
  const missingNames = names.filter((name) => !sourceNames.has(name));
  const existingTargetNames = names.filter((name) => destinationNames.has(name));
  const expectedPaths = names.map((name) => joinOpenListPath(dstDir, name));
  const nextAction = missingNames.length > 0
    ? "fix_copy_source"
    : existingTargetNames.length > 0
      ? "confirm_copy_over_existing"
      : "confirm_before_copy";
  const baseResult = {
    ok: missingNames.length === 0,
    tool: "openlist-copy",
    mode: "agent-json",
    dryRun: !args.yes,
    nextAction,
    source: {
      dir: srcDir,
      itemCount: sourceListing.items.length,
      foundNames: names.filter((name) => sourceNames.has(name)),
      missingNames
    },
    destination: {
      dir: dstDir,
      itemCount: destinationListing.items.length,
      existingTargetNames
    },
    copyPlan: {
      srcDir,
      dstDir,
      names,
      expectedPaths
    },
    confirmation: {
      source: srcDir,
      selectedItems: names,
      target: dstDir,
      finalNaming: expectedPaths,
      commandHint: "Re-run this command with --yes --format json after the user confirms the copy plan."
    }
  };

  if (missingNames.length > 0) return baseResult;
  if (!args.yes) return baseResult;

  const copyResponse = await startCopyTask({ ...context, srcDir, dstDir, names });
  if (!copyResponse.ok) {
    return {
      ...baseResult,
      ok: false,
      dryRun: false,
      nextAction: "inspect_copy_error",
      copyRequest: copyResponse
    };
  }

  const copyTask = extractCopyTask(copyResponse.json);
  if (args.poll === false) {
    return {
      ...baseResult,
      ok: true,
      dryRun: false,
      nextAction: "verify_copy_result",
      copyRequest: publicCopyResponse(copyResponse),
      copyTask
    };
  }

  const verification = await pollCopyCompletion({
    ...context,
    srcDir,
    dstDir,
    names,
    taskId: copyTask.id,
    preExistingNames: existingTargetNames,
    pollTimeoutMs: args.pollTimeoutMs || DEFAULT_POLL_TIMEOUT_MS,
    intervalMs: args.intervalMs || DEFAULT_INTERVAL_MS
  });

  return {
    ...baseResult,
    ok: verification.ok,
    dryRun: false,
    nextAction: verification.ok ? "copy_complete" : "inspect_copy_error",
    copyRequest: publicCopyResponse(copyResponse),
    copyTask,
    verification
  };
}

async function pollCopyCompletion({ baseUrl, token, fetchImpl, timeoutMs, srcDir, dstDir, names, taskId, preExistingNames, pollTimeoutMs, intervalMs }) {
  const deadline = Date.now() + (pollTimeoutMs || DEFAULT_POLL_TIMEOUT_MS);
  const preExistingSet = new Set(preExistingNames || []);
  const allNamesPreExisting = names.every((name) => preExistingSet.has(name));
  let lastSnapshot = {
    targetFound: false,
    undoneTasks: [],
    doneTasks: [],
    errors: []
  };

  while (Date.now() <= deadline) {
    const undone = await listTaskGroup({ baseUrl, token, fetchImpl, timeoutMs, group: "copy", state: "undone" });
    const done = await listTaskGroup({ baseUrl, token, fetchImpl, timeoutMs, group: "copy", state: "done" });
    const matchingUndone = undone.tasks.filter((task) => matchesCopyTask(task, { taskId, srcDir, dstDir, names }));
    const matchingDone = done.tasks.filter((task) => matchesCopyTask(task, { taskId, srcDir, dstDir, names }));
    const targetListing = await listDirectory({ baseUrl, token, fetchImpl, timeoutMs, dirPath: dstDir, refresh: true });
    const targetFound = names.every((name) => targetListing.items.some((item) => item.name === name));
    const failedDone = matchingDone.filter((task) => task.error || String(task.status || "").toLowerCase().includes("fail"));

    lastSnapshot = {
      targetFound,
      undoneTasks: matchingUndone,
      doneTasks: matchingDone,
      errors: failedDone.map((task) => ({ id: task.id, name: task.name, error: task.error || task.status }))
    };

    if (failedDone.length > 0) {
      return {
        ok: false,
        state: "task_failed",
        ...lastSnapshot
      };
    }
    if (targetFound && (matchingDone.length > 0 || (!allNamesPreExisting && matchingUndone.length === 0))) {
      return {
        ok: true,
        state: "target_visible",
        ...lastSnapshot
      };
    }

    await sleep(intervalMs || DEFAULT_INTERVAL_MS);
  }

  return {
    ok: false,
    state: "timeout",
    ...lastSnapshot
  };
}

async function listDirectory({ baseUrl, token, fetchImpl, timeoutMs, dirPath, refresh }) {
  const response = await fetchOpenListJson({
    baseUrl,
    token,
    fetchImpl,
    timeoutMs,
    path: "/api/fs/list",
    method: "POST",
    body: JSON.stringify({
      path: dirPath,
      password: "",
      page: 1,
      per_page: 200,
      refresh: Boolean(refresh)
    })
  });
  if (!response.ok || !isOpenListSuccess(response.json)) {
    throw new Error(`OpenList list failed for ${dirPath}: ${response.json?.message || response.status || "unknown"}`);
  }
  return {
    path: dirPath,
    items: normalizeListItems(response.json)
  };
}

async function startCopyTask({ baseUrl, token, fetchImpl, timeoutMs, srcDir, dstDir, names }) {
  const response = await fetchOpenListJson({
    baseUrl,
    token,
    fetchImpl,
    timeoutMs,
    path: "/api/fs/copy",
    method: "POST",
    body: JSON.stringify({
      src_dir: srcDir,
      dst_dir: dstDir,
      names
    })
  });
  return {
    ok: response.ok && isOpenListSuccess(response.json),
    status: response.status,
    json: response.json
  };
}

async function listTaskGroup({ baseUrl, token, fetchImpl, timeoutMs, group, state }) {
  const response = await fetchOpenListJson({
    baseUrl,
    token,
    fetchImpl,
    timeoutMs,
    path: `/api/task/${group}/${state}`,
    method: "GET"
  });
  if (!response.ok || !isOpenListSuccess(response.json)) {
    return { tasks: [], error: response.json?.message || String(response.status || "unknown") };
  }
  return {
    tasks: Array.isArray(response.json?.data) ? response.json.data.map(normalizeTask) : []
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

function extractCopyTask(json = {}) {
  const task = json?.data?.task || (Array.isArray(json?.data?.tasks) ? json.data.tasks[0] : null) || {};
  return normalizeTask(task);
}

function publicCopyResponse(response) {
  return {
    ok: response.ok,
    status: response.status,
    code: response.json?.code ?? null,
    message: response.json?.message || "",
    task: extractCopyTask(response.json)
  };
}

function normalizeListItems(json = {}) {
  const rawItems = Array.isArray(json?.data?.content)
    ? json.data.content
    : Array.isArray(json?.data)
      ? json.data
      : [];
  return rawItems.map((item) => ({
    name: String(item.name || ""),
    type: item.type ?? null,
    isDir: Boolean(item.is_dir ?? item.isDir ?? item.type === 1),
    size: item.size ?? null,
    modified: item.modified || item.updated_at || ""
  })).filter((item) => item.name);
}

function normalizeTask(task = {}) {
  return {
    id: String(task.id || ""),
    name: String(task.name || ""),
    state: task.state ?? null,
    status: task.status || "",
    progress: task.progress ?? null,
    error: task.error || ""
  };
}

function matchesCopyTask(task, { taskId, srcDir, dstDir, names }) {
  if (taskId && task.id === taskId) return true;
  const haystack = `${task.name} ${task.status}`.toLowerCase();
  const hasName = names.some((name) => haystack.includes(String(name).toLowerCase()));
  if (!hasName) return false;
  const sourceHint = basenameFromPath(srcDir);
  const destHint = basenameFromPath(dstDir);
  return haystack.includes(sourceHint.toLowerCase()) || haystack.includes(destHint.toLowerCase());
}

function buildOpenListContext(env, args, fetchImpl) {
  return {
    baseUrl: args.baseUrl || env.OPENLIST_BASE_URL,
    token: args.token || env.OPENLIST_TOKEN,
    fetchImpl,
    timeoutMs: args.timeoutMs || DEFAULT_TIMEOUT_MS
  };
}

function formatCopyResult(result) {
  const lines = ["### OpenList Copy", ""];
  lines.push(`状态：${result.ok ? "OK" : "失败"}`);
  lines.push(`下一步：${result.nextAction}`);
  if (result.copyPlan) {
    lines.push(`来源：${result.copyPlan.srcDir}`);
    lines.push(`目标：${result.copyPlan.dstDir}`);
    lines.push(`对象：${result.copyPlan.names.join(", ")}`);
  }
  if (result.dryRun) lines.push("未执行复制：确认后加 --yes。");
  if (result.verification?.errors?.length) {
    for (const error of result.verification.errors) {
      lines.push(`错误：${error.id || "-"} ${error.error || ""}`);
    }
  }
  return lines.join("\n");
}

function loadEnv(envFile) {
  const fileEnv = envFile && fs.existsSync(envFile) ? parseDotEnv(fs.readFileSync(envFile, "utf8")) : {};
  return { ...fileEnv, ...process.env };
}

function normalizeOpenListPath(value) {
  const text = String(value || "").trim();
  if (!text) return "";
  return text.startsWith("/") ? text.replace(/\/+$/g, "") || "/" : `/${text.replace(/\/+$/g, "")}`;
}

function joinOpenListPath(dirPath, name) {
  if (dirPath === "/") return `/${name}`;
  return `${dirPath.replace(/\/+$/g, "")}/${name}`;
}

function basenameFromPath(value) {
  return String(value || "").split("/").filter(Boolean).at(-1) || "";
}

function parseList(value) {
  return String(value || "").split(",").map((item) => item.trim()).filter(Boolean);
}

function normalizeBaseUrl(value) {
  return String(value || "").replace(/\/+$/g, "");
}

function isOpenListSuccess(json) {
  return json?.code === 200 || json?.code === 0 || json?.message === "success";
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, Math.max(0, Number(ms) || 0)));
}

function isCliEntryPoint() {
  return Boolean(process.argv[1]) && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

export {
  parseArgs,
  runOpenListCopy
};
