#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { fileURLToPath } from "node:url";

import { parseDotEnv } from "./check-env.mjs";

const DEFAULT_API_BASE = "https://drive-pc.quark.cn";
const DEFAULT_TIMEOUT_MS = 60_000;
const DEFAULT_PAGE_SIZE = 50;
const DEFAULT_COOKIE_ENV = "QUARK_COOKIE";
const DEFAULT_ENV_FILE = ".env";
const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) quark-cloud-drive/3.14.2 Chrome/112.0.5615.165 Electron/24.1.3.8 Safari/537.36 Channel/pckk_other_ch";

if (isCliEntryPoint()) {
  main().catch((error) => {
    const message = error && error.message ? error.message : String(error);
    console.error(JSON.stringify({ ok: false, error: message }, null, 2));
    process.exit(1);
  });
}

async function main() {
  const args = applyEnvDefaults(parseArgs(process.argv.slice(2)));
  if (!args.shareUrl || !args.toUrl) {
    printUsage();
    process.exit(2);
  }

  const cookie = resolveCookie(args);
  const result = await prepareQuarkSave({ ...args, cookie });
  const jsonOutput = args.format === "json";

  if (args.dryRun) {
    if (jsonOutput) {
      console.log(JSON.stringify(buildQuarkSubagentPreview({ args, result }), null, 2));
    } else {
      console.log(renderShareItemsTable(result));
      console.log("\n--dry-run 已启用：只预览资源和重命名建议，不会调用转存接口。");
    }
    return;
  }

  if (!jsonOutput) {
    console.log(renderShareItemsTable(result));
  }

  if (!cookie) {
    throw new Error(`缺少夸克 Cookie。请设置 ${args.cookieEnv} 环境变量，或使用 --cookie-env 指向你的 Cookie 环境变量。`);
  }
  if (!result.destination?.fid) {
    throw new Error(`夸克保存目录无法解析为 fid：${args.toUrl}。如果使用 /备份资源 这种路径，请确认目录存在且 Cookie 有效。`);
  }
  if (jsonOutput && !args.yes) {
    throw new Error("--format json 保存模式必须在用户确认后搭配 --yes 使用；预览请使用 --dry-run。");
  }

  const selectedItems = args.yes
    ? result.selectedPreview
    : await askUserSelection(result.items, args.defaultSelection);

  if (selectedItems.length === 0) {
    console.log("没有选择任何资源，已退出。");
    return;
  }

  const saveResult = await saveSelectedItems({
    ...args,
    contextName: result.contextName,
    cookie,
    pwdId: result.share.pwdId,
    stoken: result.share.stoken,
    destinationFid: result.destination.fid,
    selectedItems
  });

  if (jsonOutput) {
    console.log(JSON.stringify(buildQuarkSubagentSave({ args, result, saveResult }), null, 2));
  } else {
    console.log(renderSaveSummary(saveResult));
  }
}

function parseArgs(argv) {
  const parsed = {
    shareUrl: "",
    toUrl: "",
    contextName: "",
    cookieEnv: DEFAULT_COOKIE_ENV,
    envFile: DEFAULT_ENV_FILE,
    apiBase: DEFAULT_API_BASE,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    defaultSelection: "all",
    resourceType: "auto",
    agentRenamePlan: null,
    yes: false,
    dryRun: false,
    noRename: false,
    format: "markdown"
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--share-url") {
      parsed.shareUrl = argv[++index] || "";
    } else if (arg === "--to-url" || arg === "--dest-url") {
      parsed.toUrl = argv[++index] || "";
    } else if (arg === "--context-name" || arg === "--resource-name") {
      parsed.contextName = argv[++index] || "";
    } else if (arg === "--cookie-env") {
      parsed.cookieEnv = argv[++index] || DEFAULT_COOKIE_ENV;
    } else if (arg === "--env-file") {
      parsed.envFile = argv[++index] || DEFAULT_ENV_FILE;
    } else if (arg === "--api-base") {
      parsed.apiBase = argv[++index] || DEFAULT_API_BASE;
    } else if (arg === "--timeout-ms") {
      parsed.timeoutMs = Number(argv[++index] || DEFAULT_TIMEOUT_MS);
    } else if (arg === "--select") {
      parsed.defaultSelection = argv[++index] || "all";
    } else if (arg === "--resource-type") {
      parsed.resourceType = normalizeResourceType(argv[++index] || "auto");
    } else if (arg === "--rename-plan-json") {
      parsed.agentRenamePlan = parseJson(argv[++index], "--rename-plan-json");
    } else if (arg === "--yes" || arg === "-y") {
      parsed.yes = true;
    } else if (arg === "--dry-run") {
      parsed.dryRun = true;
    } else if (arg === "--no-rename") {
      parsed.noRename = true;
    } else if (arg === "--json") {
      parsed.format = "json";
    } else if (arg === "--format") {
      parsed.format = argv[++index] || "markdown";
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else if (!parsed.shareUrl) {
      parsed.shareUrl = arg;
    } else if (!parsed.toUrl) {
      parsed.toUrl = arg;
    } else if (!parsed.contextName) {
      parsed.contextName = arg;
    } else {
      throw new Error(`Unexpected positional argument: ${arg}`);
    }
  }

  return parsed;
}

function applyEnvDefaults(args, injectedEnv = null) {
  const fileEnv = injectedEnv || loadEnvFile(args.envFile);
  const env = { ...fileEnv, ...process.env };
  return {
    ...args,
    env,
    toUrl: args.toUrl || env.QUARK_DEFAULT_SAVE_URL || ""
  };
}

function loadEnvFile(envFile = DEFAULT_ENV_FILE) {
  if (!envFile || !fs.existsSync(envFile)) return {};
  return parseDotEnv(fs.readFileSync(envFile, "utf8"));
}

function printUsage() {
  console.error("Usage: node scripts/quark-save.mjs <share-url> <destination-folder-url> [options]");
  console.error("Options:");
  console.error("  --context-name \"资源名\"       用上下文资源名修正保存后的文件名");
  console.error("  --resource-type auto|series|movie|collection");
  console.error("  --rename-plan-json '[{\"rank\":1,\"name\":\"修正名\",\"reason\":\"Agent 判断\"}]'");
  console.error("  --env-file .env                从 ENV 文件读取默认保存目录和 Cookie");
  console.error("  --cookie-env QUARK_COOKIE      从指定环境变量读取夸克 Cookie");
  console.error("  --select all|1,3|2-5           默认选择，交互确认时可覆盖");
  console.error("  --yes                          跳过确认，直接使用 --select");
  console.error("  --dry-run                      只列资源和命名建议，不转存");
  console.error("  --no-rename                    转存后不执行重命名修正");
}

async function prepareQuarkSave(args) {
  const share = parseQuarkShareUrl(args.shareUrl);
  const destination = await resolveQuarkDestination({
    apiBase: args.apiBase,
    timeoutMs: args.timeoutMs,
    cookie: args.cookie,
    value: args.toUrl
  });
  const tokenResponse = await getShareToken({
    apiBase: args.apiBase,
    timeoutMs: args.timeoutMs,
    pwdId: share.pwdId,
    passcode: share.passcode
  });
  const stoken = tokenResponse.data?.stoken;
  if (!stoken) {
    throw new Error(`无法获取分享 stoken：${tokenResponse.message || "分享可能失效或需要提取码"}`);
  }

  const detailResponse = await listShareItems({
    apiBase: args.apiBase,
    timeoutMs: args.timeoutMs,
    pwdId: share.pwdId,
    stoken,
    pdirFid: share.pdirFid
  });
  const items = normalizeShareItems(detailResponse.data?.list || []);
  const shareTitle = tokenResponse.data?.title || "";
  const contextName = normalizeContextName(args.contextName || shareTitle);
  const classification = classifyResource({
    resourceType: args.resourceType,
    contextName,
    shareTitle: tokenResponse.data?.title || "",
    items
  });
  const selectedItems = parseSelection(args.defaultSelection, items);
  const renamePlan = args.agentRenamePlan
    ? resolveRenamePlan({
        selectedItems,
        savedFids: selectedItems.map((item) => item.fid),
        agentRenamePlan: args.agentRenamePlan
      })
    : buildRenamePlan({
        resourceType: args.resourceType,
        contextName,
        shareTitle: tokenResponse.data?.title || "",
        selectedItems,
        savedFids: selectedItems.map((item) => item.fid)
      });

  return {
    ok: true,
    share: {
      ...share,
      stoken,
      title: tokenResponse.data?.title || ""
    },
    destination,
    shareTitle,
    contextName,
    classification,
    items,
    defaultSelection: args.defaultSelection,
    selectedPreview: selectedItems,
    renamePlan
  };
}

async function saveSelectedItems(args) {
  const payload = buildSavePayload({
    pwdId: args.pwdId,
    stoken: args.stoken,
    destinationFid: args.destinationFid,
    selectedItems: args.selectedItems
  });
  const saveResponse = await postSave({
    apiBase: args.apiBase,
    timeoutMs: args.timeoutMs,
    cookie: args.cookie,
    payload
  });
  const taskId = saveResponse.data?.task_id;
  if (!taskId) {
    throw new Error(`转存接口未返回 task_id：${saveResponse.message || JSON.stringify(saveResponse).slice(0, 200)}`);
  }

  const task = await queryTask({
    apiBase: args.apiBase,
    timeoutMs: args.timeoutMs,
    cookie: args.cookie,
    taskId
  });
  const savedFids = task.data?.save_as?.save_as_top_fids || [];
  const renamePlan = args.noRename
    ? []
    : args.agentRenamePlan
      ? resolveRenamePlan({
          selectedItems: args.selectedItems,
          savedFids,
          agentRenamePlan: args.agentRenamePlan
        })
      : buildRenamePlan({
          resourceType: args.resourceType,
          contextName: args.contextName || "",
          shareTitle: "",
          selectedItems: args.selectedItems,
          savedFids
        });
  const renameResults = args.noRename
    ? []
    : await applyRenamePlan({
        apiBase: args.apiBase,
        timeoutMs: args.timeoutMs,
        cookie: args.cookie,
        renamePlan
      });

  return {
    ok: true,
    taskId,
    task,
    selectedItems: args.selectedItems,
    savedFids,
    renamePlan,
    renameResults
  };
}

function parseQuarkShareUrl(value) {
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    throw new Error(`Invalid Quark share URL: ${value}`);
  }
  const match = parsed.pathname.match(/\/s\/([^/?#]+)/);
  if (!match) throw new Error(`Quark share URL must include /s/<share-id>: ${value}`);

  return {
    pwdId: match[1],
    passcode: parsed.searchParams.get("pwd") || parsed.searchParams.get("passcode") || "",
    pdirFid: extractFidFromHash(parsed.hash, "share") || "0"
  };
}

function parseQuarkFolderUrl(value) {
  const text = String(value || "").trim();
  if (isCloudDrivePath(text)) {
    return {
      fid: "",
      name: getCloudPathBasename(text),
      path: normalizeCloudDrivePath(text),
      inputType: "path",
      needsResolution: true
    };
  }
  let parsed;
  try {
    parsed = new URL(text);
  } catch {
    throw new Error(`Invalid Quark folder URL: ${value}`);
  }
  const fid = extractFidFromHash(parsed.hash, "all");
  if (!fid) throw new Error(`Destination folder URL must include /list/all/<fid-name>: ${value}`);
  const name = extractNameFromHash(parsed.hash, fid);
  return { fid, name: name || fid };
}

async function resolveQuarkDestination({ apiBase, timeoutMs, cookie, value }) {
  const parsed = parseQuarkFolderUrl(value);
  if (!parsed.needsResolution) return parsed;
  if (!cookie) return parsed;
  const resolved = await resolveQuarkFolderPath({
    apiBase,
    timeoutMs,
    cookie,
    targetPath: parsed.path
  });
  return {
    ...parsed,
    ...resolved,
    needsResolution: false
  };
}

async function resolveQuarkFolderPath({ apiBase, timeoutMs, cookie, targetPath }) {
  const normalizedPath = normalizeCloudDrivePath(targetPath);
  const segments = splitCloudDrivePath(normalizedPath);
  let pdirFid = "0";
  let current = { fid: "0", name: "/", path: "/" };
  for (const segment of segments) {
    const items = await listQuarkFolderItems({ apiBase, timeoutMs, cookie, pdirFid });
    const match = items.find((item) => item.isDir && item.name === segment);
    if (!match) {
      throw new Error(`夸克目录不存在：${joinCloudPath(current.path, segment)}。请先在夸克网盘创建该目录，或改用完整文件夹 URL。`);
    }
    current = {
      fid: match.fid,
      name: match.name,
      path: joinCloudPath(current.path, match.name)
    };
    pdirFid = match.fid;
  }
  return current;
}

async function listQuarkFolderItems({ apiBase, timeoutMs, cookie, pdirFid }) {
  const response = await fetchQuarkJson(`${normalizeApiBase(apiBase)}/1/clouddrive/file/sort`, {
    method: "GET",
    timeoutMs,
    cookie,
    query: {
      pr: "ucpro",
      fr: "pc",
      uc_param_str: "",
      pdir_fid: pdirFid || "0",
      _page: "1",
      _size: "200",
      _fetch_total: "1",
      _fetch_sub_dirs: "0",
      _sort: "file_type:asc,updated_at:desc"
    }
  });
  return normalizeShareItems(response.data?.list || []);
}

function isCloudDrivePath(value) {
  return String(value || "").startsWith("/") && !String(value).includes("..");
}

function normalizeCloudDrivePath(value) {
  const parts = splitCloudDrivePath(value);
  return `/${parts.join("/")}`;
}

function splitCloudDrivePath(value) {
  return String(value || "")
    .split("/")
    .map((item) => item.trim())
    .filter(Boolean);
}

function getCloudPathBasename(value) {
  const parts = splitCloudDrivePath(value);
  return parts.at(-1) || "/";
}

function joinCloudPath(basePath, name) {
  const base = normalizeCloudDrivePath(basePath || "/");
  const cleanName = String(name || "").replace(/^\/+/g, "");
  return base === "/" ? `/${cleanName}` : `${base}/${cleanName}`;
}

function extractFidFromHash(hash, scope) {
  const decoded = safeDecode(hash || "");
  const match = decoded.match(new RegExp(`/list/${scope}/([a-zA-Z0-9]{16,64})(?:-|/|$)`));
  return match ? match[1] : "";
}

function extractNameFromHash(hash, fid) {
  const decoded = safeDecode(hash || "");
  const marker = `${fid}-`;
  const markerIndex = decoded.indexOf(marker);
  if (markerIndex === -1) return "";
  return decoded.slice(markerIndex + marker.length).split("/")[0].trim();
}

function safeDecode(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

function normalizeShareItems(rows) {
  return (rows || []).map((row, index) => {
    const isDir = Boolean(row.dir);
    return {
      rank: index + 1,
      fid: row.fid,
      shareFidToken: row.share_fid_token,
      name: row.file_name || row.file_name_re || row.name || "未命名资源",
      isDir,
      typeLabel: isDir ? "文件夹" : "文件",
      size: Number(row.size || 0),
      sizeLabel: isDir ? "-" : formatBytes(Number(row.size || 0)),
      itemCount: isDir ? Number(row.include_items || row.file_count || 0) || null : null,
      updatedAt: row.updated_at || row.l_updated_at || row.created_at || row.l_created_at || null,
      updatedAtLabel: formatTimestamp(row.updated_at || row.l_updated_at || row.created_at || row.l_created_at),
      raw: row
    };
  });
}

function classifyResource({ resourceType = "auto", contextName = "", shareTitle = "", items = [] } = {}) {
  const explicitType = normalizeResourceType(resourceType);
  if (explicitType === "series") {
    return {
      type: "series",
      isSeries: true,
      label: "剧集",
      reason: "Agent 根据上下文判定为剧集"
    };
  }
  if (explicitType === "movie") {
    return {
      type: "movie",
      isSeries: false,
      label: "电影",
      reason: "Agent 根据上下文判定为电影"
    };
  }
  if (explicitType === "collection") {
    return {
      type: "collection",
      isSeries: false,
      label: "合集",
      reason: "Agent 根据上下文判定为合集"
    };
  }

  const haystack = [contextName, shareTitle, ...items.map((item) => item.name)].join(" ");
  const seriesPattern =
    /(S\d{1,2}E\d{1,3}|EP?\d{1,3}|第[一二三四五六七八九十百\d]+[季集]|全\d{1,4}集|完结|剧集|电视剧|美剧|英剧|韩剧|日剧|番剧|动漫|连载)/i;
  if (seriesPattern.test(haystack)) {
    return {
      type: "series",
      isSeries: true,
      label: "剧集",
      reason: "匹配到剧集/季/集关键词"
    };
  }
  return {
    type: "unknown",
    isSeries: false,
    label: "电影/合集",
    reason: "未匹配到明显剧集关键词"
  };
}

function buildRenamePlan({ resourceType = "auto", contextName = "", shareTitle = "", selectedItems = [], savedFids = [] } = {}) {
  const baseName = sanitizeFileName(contextName || shareTitle || "");
  if (!baseName) return [];
  const classification = classifyResource({ resourceType, contextName: baseName, shareTitle, items: selectedItems });
  const plan = [];
  selectedItems.forEach((item, index) => {
    const savedFid = savedFids[index];
    if (!savedFid) return;
    const suggestedName = suggestSavedName({
      baseName,
      item,
      selectedCount: selectedItems.length,
      isSeries: classification.isSeries
    });
    if (!suggestedName || suggestedName === item.name) return;
    plan.push({
      fid: savedFid,
      originalName: item.name,
      suggestedName,
      reason: classification.isSeries ? "按上下文资源名修正剧集文件名" : "按上下文资源名修正保存名称"
    });
  });
  return plan;
}

function resolveRenamePlan({ selectedItems = [], savedFids = [], agentRenamePlan = [] } = {}) {
  if (!Array.isArray(agentRenamePlan)) {
    throw new Error("Agent rename plan must be a JSON array");
  }
  const plan = [];
  for (const decision of agentRenamePlan) {
    const rank = Number(decision.rank ?? decision.index);
    if (!Number.isFinite(rank) || rank < 1) {
      throw new Error(`Agent rename plan item is missing a valid rank/index: ${JSON.stringify(decision)}`);
    }
    const itemIndex = selectedItems.findIndex((item) => item.rank === rank);
    const fallbackIndex = selectedItems[rank - 1] ? rank - 1 : -1;
    const selectedIndex = itemIndex >= 0 ? itemIndex : fallbackIndex;
    if (selectedIndex < 0) {
      throw new Error(`Agent rename plan rank is not selected: ${rank}`);
    }

    const item = selectedItems[selectedIndex];
    const savedFid = savedFids[selectedIndex];
    const suggestedName = sanitizeFileName(decision.name || decision.suggestedName || "");
    if (!suggestedName) {
      throw new Error(`Agent rename plan item is missing name/suggestedName: ${JSON.stringify(decision)}`);
    }
    if (!savedFid || suggestedName === item.name) continue;
    plan.push({
      fid: savedFid,
      originalName: item.name,
      suggestedName,
      reason: decision.reason || "Agent 指定重命名"
    });
  }
  return plan;
}

function suggestSavedName({ baseName, item, selectedCount, isSeries }) {
  const extension = item.isDir ? "" : getExtension(item.name);
  if (item.isDir) {
    if (selectedCount === 1) return baseName;
    return sanitizeFileName(`${baseName} - ${item.name}`);
  }
  if (isSeries) {
    const episode = extractEpisodeLabel(item.name);
    if (episode) return sanitizeFileName(`${baseName} ${episode}${extension}`);
  }
  if (selectedCount === 1) return sanitizeFileName(`${baseName}${extension}`);
  return sanitizeFileName(`${baseName} - ${stripExtension(item.name)}${extension}`);
}

function extractEpisodeLabel(value) {
  const text = String(value || "");
  const seasonEpisode = text.match(/S(\d{1,2})E(\d{1,3})/i);
  if (seasonEpisode) {
    return `S${seasonEpisode[1].padStart(2, "0")}E${seasonEpisode[2].padStart(2, "0")}`;
  }
  const cnEpisode = text.match(/第([一二三四五六七八九十百\d]+)集/);
  if (cnEpisode) return `第${cnEpisode[1]}集`;
  const ep = text.match(/\bEP?\.?(\d{1,3})\b/i);
  if (ep) return `E${ep[1].padStart(2, "0")}`;
  return "";
}

function getExtension(value) {
  const ext = path.extname(String(value || ""));
  return ext.length <= 12 ? ext : "";
}

function stripExtension(value) {
  const ext = getExtension(value);
  return ext ? String(value).slice(0, -ext.length) : String(value || "");
}

function sanitizeFileName(value) {
  return String(value || "")
    .replace(/[\\/:*?"<>|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeContextName(value) {
  return String(value || "")
    .replace(/[丨｜|]/g, "")
    .replace(/[\u200b-\u200f\uFEFF]/g, "")
    .replace(/^[A-Z]\s+(?=.*[\u4e00-\u9fff])/, "")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeResourceType(value) {
  const normalized = String(value || "auto").trim().toLowerCase();
  if (["auto", "series", "movie", "collection"].includes(normalized)) return normalized;
  throw new Error(`Unsupported resource type: ${value}`);
}

function parseJson(value, label) {
  try {
    return JSON.parse(value || "[]");
  } catch (error) {
    throw new Error(`${label} must be valid JSON: ${error.message}`);
  }
}

function parseSelection(selection, items) {
  const value = String(selection || "").trim().toLowerCase();
  if (!value || value === "all" || value === "*") return [...items];
  const ranks = new Set();
  for (const part of value.split(",")) {
    const trimmed = part.trim();
    if (!trimmed) continue;
    const range = trimmed.match(/^(\d+)-(\d+)$/);
    if (range) {
      const start = Number(range[1]);
      const end = Number(range[2]);
      if (end < start) throw new Error(`Invalid selection range: ${trimmed}`);
      for (let rank = start; rank <= end; rank += 1) ranks.add(rank);
    } else if (/^\d+$/.test(trimmed)) {
      ranks.add(Number(trimmed));
    } else {
      throw new Error(`Invalid selection: ${trimmed}`);
    }
  }

  const selected = [...ranks].sort((a, b) => a - b).map((rank) => {
    const item = items[rank - 1];
    if (!item) throw new Error(`Selection index out of range: ${rank}`);
    return item;
  });
  return selected;
}

function buildSavePayload({ pwdId, stoken, destinationFid, selectedItems }) {
  return {
    fid_list: selectedItems.map((item) => item.fid),
    fid_token_list: selectedItems.map((item) => item.shareFidToken),
    to_pdir_fid: destinationFid,
    pwd_id: pwdId,
    stoken,
    pdir_fid: "0",
    scene: "link"
  };
}

function renderShareItemsTable({
  shareTitle = "",
  contextName = "",
  destinationName = "",
  destination = null,
  items = [],
  classification,
  renamePlan = []
}) {
  const detected = classification || classifyResource({ contextName, shareTitle, items });
  const targetName = destinationName || destination?.name || "";
  const lines = [
    "### 夸克分享资源",
    "",
    `分享标题：${escapeMarkdownText(shareTitle || "-")}`,
    `修正资源名：${escapeMarkdownText(contextName || "-")}`,
    `目标目录：${escapeMarkdownText(targetName || "-")}`,
    `资源类型：${escapeMarkdownText(detected.label)}（${escapeMarkdownText(detected.reason)}）`,
    "",
    "| # | 类型 | 名称 | 大小 | 更新时间 |",
    "|---:|---|---|---|---|"
  ];

  for (const item of items) {
    lines.push(
      [
        item.rank,
        escapeMarkdownCell(item.typeLabel),
        escapeMarkdownCell(item.name),
        escapeMarkdownCell(item.sizeLabel),
        escapeMarkdownCell(item.updatedAtLabel)
      ].join(" | ").replace(/^/, "| ").replace(/$/, " |")
    );
  }

  if (renamePlan.length > 0) {
    lines.push("", "建议保存后重命名：", "", "| # | 原名称 | 建议名称 | 原因 |", "|---:|---|---|---|");
    renamePlan.forEach((item, index) => {
      lines.push(
        [
          index + 1,
          escapeMarkdownCell(item.originalName),
          escapeMarkdownCell(item.suggestedName),
          escapeMarkdownCell(item.reason)
        ].join(" | ").replace(/^/, "| ").replace(/$/, " |")
      );
    });
  }

  return lines.join("\n");
}

function renderSaveSummary(saveResult) {
  const lines = [
    "",
    "### 夸克转存结果",
    "",
    `任务 ID：${saveResult.taskId}`,
    `已选择：${saveResult.selectedItems.length} 项`,
    `保存后的顶层 fid：${saveResult.savedFids.length > 0 ? saveResult.savedFids.join(", ") : "-"}`
  ];
  if (saveResult.renameResults.length > 0) {
    lines.push("", "重命名修正：");
    saveResult.renameResults.forEach((item) => {
      lines.push(`- ${item.ok ? "成功" : "失败"}：${item.originalName} -> ${item.suggestedName}${item.error ? `（${item.error}）` : ""}`);
    });
  }
  return lines.join("\n");
}

function buildQuarkSubagentPreview({ args = {}, result }) {
  const selectedItems = result.selectedPreview || parseSelection(result.defaultSelection || args.defaultSelection || "all", result.items || []);
  return {
    ok: true,
    provider: "quark",
    mode: "preview",
    nextAction: "confirm_before_save",
    source: {
      shareUrl: args.shareUrl || "",
      shareId: result.share?.pwdId || "",
      passcodePresent: Boolean(result.share?.passcode)
    },
    target: {
      provider: "quark",
      pathOrUrl: args.toUrl || "",
      fid: result.destination?.fid || "",
      name: result.destination?.name || ""
    },
    resource: {
      shareTitle: result.shareTitle || "",
      canonicalName: result.contextName || "",
      type: result.classification?.type || "unknown",
      label: result.classification?.label || "",
      isSeries: Boolean(result.classification?.isSeries),
      reason: result.classification?.reason || ""
    },
    selection: {
      defaultSelection: result.defaultSelection || args.defaultSelection || "all",
      selectedRanks: selectedItems.map((item) => item.rank),
      selectedItems: selectedItems.map(serializeQuarkItem)
    },
    items: (result.items || []).map(serializeQuarkItem),
    renamePlan: serializeRenamePlan(result.renamePlan || []),
    confirmation: {
      source: args.shareUrl || "",
      selectedItems: selectedItems.map(serializeQuarkItem),
      target: {
        provider: "quark",
        pathOrUrl: args.toUrl || "",
        name: result.destination?.name || ""
      },
      finalNaming: serializeRenamePlan(result.renamePlan || []),
      commandHint: "Re-run scripts/quark-save.mjs with --yes after the user confirms this payload."
    }
  };
}

function buildQuarkSubagentSave({ args = {}, result, saveResult }) {
  return {
    ok: true,
    provider: "quark",
    mode: "save",
    nextAction: "verify_in_openlist_or_report_saved",
    source: {
      shareUrl: args.shareUrl || "",
      shareId: result.share?.pwdId || "",
      passcodePresent: Boolean(result.share?.passcode)
    },
    target: {
      provider: "quark",
      pathOrUrl: args.toUrl || "",
      fid: result.destination?.fid || "",
      name: result.destination?.name || ""
    },
    resource: {
      shareTitle: result.shareTitle || "",
      canonicalName: result.contextName || "",
      type: result.classification?.type || "unknown",
      label: result.classification?.label || "",
      isSeries: Boolean(result.classification?.isSeries),
      reason: result.classification?.reason || ""
    },
    selectedItems: (saveResult.selectedItems || []).map(serializeQuarkItem),
    taskId: saveResult.taskId || "",
    savedFids: saveResult.savedFids || [],
    renamePlan: serializeRenamePlan(saveResult.renamePlan || []),
    renameResults: serializeRenameResults(saveResult.renameResults || [])
  };
}

function serializeQuarkItem(item) {
  return {
    rank: item.rank,
    id: item.fid,
    name: item.name,
    typeLabel: item.typeLabel,
    isDir: item.isDir,
    size: item.size,
    sizeLabel: item.sizeLabel,
    itemCount: item.itemCount,
    updatedAtLabel: item.updatedAtLabel
  };
}

function serializeRenamePlan(plan) {
  return (plan || []).map((item, index) => ({
    rank: index + 1,
    id: item.fid || item.sourcePath || "",
    originalName: item.originalName,
    suggestedName: item.suggestedName,
    reason: item.reason
  }));
}

function serializeRenameResults(results) {
  return (results || []).map((item) => ({
    ok: Boolean(item.ok),
    id: item.fid || item.sourcePath || "",
    originalName: item.originalName,
    suggestedName: item.suggestedName,
    reason: item.reason,
    error: item.error || ""
  }));
}

async function askUserSelection(items, defaultSelection) {
  const rl = readline.createInterface({ input, output });
  try {
    const answer = await rl.question(`请选择要转存的序号（默认 ${defaultSelection}，支持 all、1,3、2-5）：`);
    return parseSelection(answer.trim() || defaultSelection, items);
  } finally {
    rl.close();
  }
}

async function getShareToken({ apiBase, timeoutMs, pwdId, passcode }) {
  return fetchQuarkJson(`${normalizeApiBase(apiBase)}/1/clouddrive/share/sharepage/token`, {
    method: "POST",
    timeoutMs,
    body: { pwd_id: pwdId, passcode },
    query: { pr: "ucpro", fr: "pc", uc_param_str: "" }
  });
}

async function listShareItems({ apiBase, timeoutMs, pwdId, stoken, pdirFid }) {
  const allItems = [];
  let page = 1;
  let lastResponse = null;
  while (true) {
    lastResponse = await fetchQuarkJson(`${normalizeApiBase(apiBase)}/1/clouddrive/share/sharepage/detail`, {
      method: "GET",
      timeoutMs,
      query: {
        pr: "ucpro",
        fr: "pc",
        uc_param_str: "",
        pwd_id: pwdId,
        stoken,
        pdir_fid: pdirFid || "0",
        force: "0",
        _page: String(page),
        _size: String(DEFAULT_PAGE_SIZE),
        _fetch_banner: "0",
        _fetch_share: "0",
        _fetch_total: "1",
        _sort: "file_type:asc,updated_at:desc",
        ver: "2"
      }
    });
    const items = lastResponse.data?.list || [];
    allItems.push(...items);
    const total = Number(lastResponse.metadata?._total || allItems.length);
    if (items.length === 0 || allItems.length >= total) break;
    page += 1;
  }
  return {
    ...lastResponse,
    data: {
      ...(lastResponse?.data || {}),
      list: allItems
    }
  };
}

async function postSave({ apiBase, timeoutMs, cookie, payload }) {
  return fetchQuarkJson(`${normalizeApiBase(apiBase)}/1/clouddrive/share/sharepage/save`, {
    method: "POST",
    timeoutMs,
    cookie,
    body: payload,
    query: buildMutationQuery()
  });
}

async function queryTask({ apiBase, timeoutMs, cookie, taskId }) {
  let retryIndex = 0;
  while (retryIndex < 120) {
    const response = await fetchQuarkJson(`${normalizeApiBase(apiBase)}/1/clouddrive/task`, {
      method: "GET",
      timeoutMs,
      cookie,
      query: {
        ...buildMutationQuery(),
        task_id: taskId,
        retry_index: String(retryIndex)
      }
    });
    if (response.data?.status === 2) return response;
    if (response.data?.status === 3 || response.data?.status === 4) {
      throw new Error(`转存任务失败：${response.data?.fail_msg || response.data?.message || JSON.stringify(response.data).slice(0, 200)}`);
    }
    retryIndex += 1;
    await delay(500);
  }
  throw new Error(`等待转存任务超时：${taskId}`);
}

async function applyRenamePlan({ apiBase, timeoutMs, cookie, renamePlan }) {
  const results = [];
  for (const item of renamePlan) {
    try {
      const response = await fetchQuarkJson(`${normalizeApiBase(apiBase)}/1/clouddrive/file/rename`, {
        method: "POST",
        timeoutMs,
        cookie,
        body: {
          fid: item.fid,
          file_name: item.suggestedName
        },
        query: { pr: "ucpro", fr: "pc", uc_param_str: "" }
      });
      results.push({ ...item, ok: true, response });
    } catch (error) {
      results.push({ ...item, ok: false, error: error.message || String(error) });
    }
  }
  return results;
}

async function fetchQuarkJson(url, options = {}) {
  const requestUrl = new URL(url);
  for (const [key, value] of Object.entries(options.query || {})) {
    requestUrl.searchParams.set(key, String(value));
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeoutMs || DEFAULT_TIMEOUT_MS);
  try {
    const headers = {
      Accept: "application/json",
      "User-Agent": USER_AGENT
    };
    if (options.method === "POST") headers["Content-Type"] = "application/json";
    if (options.cookie) headers.Cookie = options.cookie;
    const response = await fetch(requestUrl, {
      method: options.method || "GET",
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: controller.signal
    });
    const text = await response.text();
    let json;
    try {
      json = text ? JSON.parse(text) : {};
    } catch {
      throw new Error(`Expected JSON from ${requestUrl}, got: ${text.slice(0, 200)}`);
    }
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} from ${requestUrl}: ${JSON.stringify(json).slice(0, 300)}`);
    }
    if (json && typeof json === "object" && "code" in json && json.code !== 0) {
      throw new Error(`Quark API error ${json.code}: ${json.message || json.status || "unknown error"}`);
    }
    return json;
  } finally {
    clearTimeout(timeout);
  }
}

function buildMutationQuery() {
  return {
    pr: "ucpro",
    fr: "pc",
    uc_param_str: "",
    app: "clouddrive",
    __dt: String(Math.floor(60_000 + Math.random() * 240_000)),
    __t: String(Date.now())
  };
}

function resolveCookie(args) {
  return (args.env?.[args.cookieEnv] || process.env[args.cookieEnv] || "").trim();
}

function normalizeApiBase(value) {
  return String(value || DEFAULT_API_BASE).replace(/\/+$/g, "");
}

function formatBytes(bytes) {
  if (!bytes) return "-";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let value = bytes;
  let unitIndex = 0;
  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024;
    unitIndex += 1;
  }
  const rounded = value >= 10 || Number.isInteger(value) ? Math.round(value) : Math.round(value * 10) / 10;
  return `${rounded} ${units[unitIndex]}`;
}

function formatTimestamp(value) {
  if (!value) return "-";
  const ms = Number(value);
  if (!Number.isFinite(ms)) return "-";
  const date = new Date(ms);
  if (Number.isNaN(date.getTime())) return "-";
  return date.toISOString().slice(0, 10);
}

function escapeMarkdownCell(value) {
  return escapeMarkdownText(value).replace(/\|/g, "\\|");
}

function escapeMarkdownText(value) {
  return String(value ?? "")
    .replace(/\r?\n+/g, " ")
    .trim();
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isCliEntryPoint() {
  return Boolean(process.argv[1]) && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

export {
  applyEnvDefaults,
  buildQuarkSubagentPreview,
  buildQuarkSubagentSave,
  buildRenamePlan,
  buildSavePayload,
  classifyResource,
  normalizeShareItems,
  normalizeContextName,
  parseQuarkFolderUrl,
  parseQuarkShareUrl,
  parseSelection,
  resolveQuarkFolderPath,
  resolveRenamePlan,
  renderShareItemsTable
};
