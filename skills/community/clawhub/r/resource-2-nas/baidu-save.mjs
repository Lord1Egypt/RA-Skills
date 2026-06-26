#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { fileURLToPath } from "node:url";

import {
  classifyResource,
  normalizeContextName,
  parseSelection
} from "./quark-save.mjs";
import { parseDotEnv } from "./check-env.mjs";

const DEFAULT_API_BASE = "https://pan.baidu.com";
const DEFAULT_APP_ID = "250528";
const DEFAULT_COOKIE_ENV = "BAIDU_COOKIE";
const DEFAULT_ENV_FILE = ".env";
const DEFAULT_TIMEOUT_MS = 60_000;
const DEFAULT_PAGE_SIZE = 100;
const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

if (isCliEntryPoint()) {
  main().catch((error) => {
    const message = error && error.message ? error.message : String(error);
    console.error(JSON.stringify({ ok: false, error: message }, null, 2));
    process.exit(1);
  });
}

async function main() {
  const args = applyEnvDefaults(parseArgs(process.argv.slice(2)));
  if (!args.shareUrl || !args.savePath) {
    printUsage();
    process.exit(2);
  }

  if (!isCloudDrivePath(parseBaiduSavePath(args.savePath))) {
    throw new Error(`百度保存目录必须是网盘内路径或百度目录 URL，例如 /我的资源/影视：${args.savePath}`);
  }

  const cookie = resolveCookie(args);
  if (!cookie && !args.dryRun) {
    throw new Error(`缺少百度网盘 Cookie。请设置 ${args.cookieEnv} 环境变量，或使用 --cookie-env 指向你的 Cookie 环境变量。`);
  }

  const result = await prepareBaiduSave({ ...args, cookie });
  const jsonOutput = args.format === "json";

  if (args.dryRun) {
    if (jsonOutput) {
      console.log(JSON.stringify(buildBaiduSubagentPreview({ args, result }), null, 2));
    } else {
      console.log(renderBaiduShareItemsTable(result));
      console.log("\n--dry-run 已启用：只预览资源和命名建议，不会调用转存接口。");
    }
    return;
  }

  if (!jsonOutput) {
    console.log(renderBaiduShareItemsTable(result));
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
    cookie: result.cookie || cookie,
    share: result.share,
    contextName: result.contextName,
    selectedItems,
    renamePlan: buildBaiduRenamePlanForSelection({
      args,
      result,
      selectedItems
    })
  });

  if (jsonOutput) {
    console.log(JSON.stringify(buildBaiduSubagentSave({ args, result, saveResult }), null, 2));
  } else {
    console.log(renderSaveSummary(saveResult));
  }
}

function parseArgs(argv) {
  const parsed = {
    shareUrl: "",
    savePath: "",
    contextName: "",
    cookieEnv: DEFAULT_COOKIE_ENV,
    envFile: DEFAULT_ENV_FILE,
    apiBase: DEFAULT_API_BASE,
    appId: DEFAULT_APP_ID,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    defaultSelection: "all",
    resourceType: "auto",
    agentRenamePlan: null,
    passcode: "",
    yes: false,
    dryRun: false,
    noRename: false,
    format: "markdown"
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--share-url") {
      parsed.shareUrl = argv[++index] || "";
    } else if (arg === "--save-path" || arg === "--to-path" || arg === "--dest-path") {
      parsed.savePath = argv[++index] || "";
    } else if (arg === "--context-name" || arg === "--resource-name") {
      parsed.contextName = argv[++index] || "";
    } else if (arg === "--cookie-env") {
      parsed.cookieEnv = argv[++index] || DEFAULT_COOKIE_ENV;
    } else if (arg === "--env-file") {
      parsed.envFile = argv[++index] || DEFAULT_ENV_FILE;
    } else if (arg === "--api-base") {
      parsed.apiBase = argv[++index] || DEFAULT_API_BASE;
    } else if (arg === "--app-id") {
      parsed.appId = argv[++index] || DEFAULT_APP_ID;
    } else if (arg === "--timeout-ms") {
      parsed.timeoutMs = Number(argv[++index] || DEFAULT_TIMEOUT_MS);
    } else if (arg === "--select") {
      parsed.defaultSelection = argv[++index] || "all";
    } else if (arg === "--resource-type") {
      parsed.resourceType = argv[++index] || "auto";
    } else if (arg === "--rename-plan-json") {
      parsed.agentRenamePlan = parseJson(argv[++index], "--rename-plan-json");
    } else if (arg === "--passcode" || arg === "--pwd") {
      parsed.passcode = argv[++index] || "";
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
    } else if (!parsed.savePath) {
      parsed.savePath = arg;
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
  const rawSavePath = args.savePath || env.BAIDU_DEFAULT_SAVE_PATH || "";
  return {
    ...args,
    env,
    savePath: rawSavePath ? parseBaiduSavePath(rawSavePath) : ""
  };
}

function loadEnvFile(envFile = DEFAULT_ENV_FILE) {
  if (!envFile || !fs.existsSync(envFile)) return {};
  return parseDotEnv(fs.readFileSync(envFile, "utf8"));
}

function printUsage() {
  console.error("Usage: node scripts/baidu-save.mjs <share-url> <baidu-save-path> [options]");
  console.error("Options:");
  console.error("  --context-name \"资源名\"       用上下文资源名修正保存后的文件名");
  console.error("  --resource-type auto|series|movie|collection");
  console.error("  --rename-plan-json '[{\"rank\":1,\"name\":\"修正名\",\"reason\":\"Agent 判断\"}]'");
  console.error("  --passcode 8888               手动指定百度提取码；链接中的 pwd 会自动识别");
  console.error("  --env-file .env                从 ENV 文件读取默认保存目录和 Cookie");
  console.error("  --cookie-env BAIDU_COOKIE      从指定环境变量读取百度 Cookie");
  console.error("  --select all|1,3|2-5           默认选择，交互确认时可覆盖");
  console.error("  --yes                          跳过确认，直接使用 --select");
  console.error("  --dry-run                      只列资源和命名建议，不转存");
  console.error("  --no-rename                    转存后不执行重命名修正");
}

async function prepareBaiduSave(args) {
  const share = parseBaiduShareUrl(args.shareUrl);
  if (args.passcode) share.passcode = args.passcode;

  let cookie = args.cookie || "";
  let context = null;
  let pageHtml = "";

  try {
    pageHtml = await fetchBaiduText(share.sharePageUrl, {
      cookie,
      referer: share.sharePageUrl,
      timeoutMs: args.timeoutMs
    });
    context = extractBaiduShareContextFromHtml(pageHtml);
  } catch (error) {
    if (!share.passcode) throw error;
  }

  if (share.passcode) {
    const bdstoken = context?.bdstoken || (cookie ? await getBaiduBdstoken({
      apiBase: args.apiBase,
      timeoutMs: args.timeoutMs,
      cookie
    }) : "");
    const verifyResult = await verifyBaiduShare({
      apiBase: args.apiBase,
      timeoutMs: args.timeoutMs,
      cookie,
      bdstoken,
      verifySurl: share.verifySurl,
      passcode: share.passcode,
      referer: share.sharePageUrl
    });
    cookie = mergeCookieString(cookie, verifyResult.setCookies);
    share.sekey = verifyResult.randsk || "";
    pageHtml = await fetchBaiduText(share.sharePageUrl, {
      cookie,
      referer: share.sharePageUrl,
      timeoutMs: args.timeoutMs
    });
    context = extractBaiduShareContextFromHtml(pageHtml);
  }

  if (!context) {
    throw new Error("无法从百度分享页解析 shareid/share_uk/bdstoken，请确认链接有效且 Cookie 可访问该分享。");
  }

  if (!context.bdstoken && cookie) {
    context.bdstoken = await getBaiduBdstoken({
      apiBase: args.apiBase,
      timeoutMs: args.timeoutMs,
      cookie
    });
  }

  let rows = context.files || [];
  if (rows.length === 0 && context.shareId && context.shareUk) {
    rows = await listBaiduShareFiles({
      apiBase: args.apiBase,
      appId: args.appId,
      timeoutMs: args.timeoutMs,
      cookie,
      shareId: context.shareId,
      shareUk: context.shareUk,
      sekey: share.sekey || ""
    });
  }

  const items = normalizeBaiduShareItems(rows);
  const shareTitle = context.title || items[0]?.name || "";
  const contextName = normalizeContextName(args.contextName || shareTitle);
  const classification = classifyResource({
    resourceType: args.resourceType,
    contextName,
    shareTitle,
    items
  });
  const selectedPreview = parseSelection(args.defaultSelection, items);
  const renamePlan = buildBaiduRenamePlanForSelection({
    args,
    result: { contextName, shareTitle, items },
    selectedItems: selectedPreview
  });

  return {
    ok: true,
    cookie,
    share: {
      ...share,
      bdstoken: context.bdstoken,
      shareId: context.shareId,
      shareUk: context.shareUk,
      title: shareTitle
    },
    shareTitle,
    contextName,
    savePath: args.savePath,
    classification,
    items,
    defaultSelection: args.defaultSelection,
    selectedPreview,
    renamePlan
  };
}

async function saveSelectedItems(args) {
  const transferResponse = await transferBaiduShare({
    apiBase: args.apiBase,
    appId: args.appId,
    timeoutMs: args.timeoutMs,
    cookie: args.cookie,
    referer: args.share.sharePageUrl,
    bdstoken: args.share.bdstoken,
    shareId: args.share.shareId,
    shareUk: args.share.shareUk,
    savePath: args.savePath,
    selectedItems: args.selectedItems
  });

  const renameResults = args.noRename || args.renamePlan.length === 0
    ? []
    : await applyBaiduRenamePlan({
        apiBase: args.apiBase,
        appId: args.appId,
        timeoutMs: args.timeoutMs,
        cookie: args.cookie,
        bdstoken: args.share.bdstoken,
        savePath: args.savePath,
        renamePlan: args.renamePlan
      });

  return {
    ok: true,
    transferResponse,
    selectedItems: args.selectedItems,
    renamePlan: args.renamePlan,
    renameResults
  };
}

function parseBaiduShareUrl(value) {
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    throw new Error(`Invalid Baidu share URL: ${value}`);
  }
  if (!parsed.hostname.endsWith("pan.baidu.com")) {
    throw new Error(`Baidu share URL must be on pan.baidu.com: ${value}`);
  }

  let featureStr = "";
  const shareMatch = parsed.pathname.match(/\/s\/([^/?#]+)/);
  if (shareMatch) {
    featureStr = shareMatch[1];
  } else if (parsed.pathname === "/share/init" && parsed.searchParams.get("surl")) {
    const surl = parsed.searchParams.get("surl") || "";
    featureStr = surl.startsWith("1") ? surl : `1${surl}`;
  }

  if (!featureStr) {
    throw new Error(`Baidu share URL must include /s/<share-id> or /share/init?surl=...: ${value}`);
  }

  return {
    featureStr,
    verifySurl: featureStr.startsWith("1") ? featureStr.slice(1) : featureStr,
    passcode: parsed.searchParams.get("pwd") || parsed.searchParams.get("passcode") || parsed.searchParams.get("code") || "",
    sharePageUrl: `${DEFAULT_API_BASE}/s/${featureStr}`
  };
}

function extractBaiduShareContextFromHtml(html) {
  const text = String(html || "");
  const mergedContext = mergeBaiduShareContexts([
    extractYunDataContext(text),
    extractLocalsMsetContext(text),
    extractJsonLoginContext(text)
  ]);
  if (mergedContext.shareId && mergedContext.shareUk) return mergedContext;

  if (!/["']?loginstate["']?\s*:|window\.yunData|locals\.mset/.test(text)) {
    throw new Error("百度分享页中没有找到 loginstate 数据。");
  }

  throw new Error("无法解析百度分享页中的分享上下文。");
}

function extractJsonLoginContext(text) {
  const markerIndex = text.search(/["']?loginstate["']?\s*:/);
  if (markerIndex === -1) {
    return null;
  }

  for (let start = text.lastIndexOf("{", markerIndex); start >= 0; start = text.lastIndexOf("{", start - 1)) {
    const jsonText = extractBalancedJson(text, start);
    if (!jsonText) continue;
    try {
      const data = JSON.parse(jsonText);
      const context = normalizeBaiduShareContext(data);
      if (context.shareId && context.shareUk) return context;
    } catch {
      continue;
    }
  }

  return null;
}

function extractYunDataContext(text) {
  const match = String(text || "").match(/window\.yunData\s*=\s*\{([\s\S]*?)\};/);
  if (!match) return null;
  return {
    bdstoken: extractJsObjectProperty(match[1], "bdstoken"),
    shareId: extractJsObjectProperty(match[1], "shareid"),
    shareUk: extractJsObjectProperty(match[1], "share_uk"),
    files: []
  };
}

function extractLocalsMsetContext(text) {
  let searchIndex = 0;
  while (searchIndex < text.length) {
    const markerIndex = text.indexOf("locals.mset", searchIndex);
    if (markerIndex === -1) return null;
    const start = text.indexOf("{", markerIndex);
    if (start === -1) return null;
    const jsonText = extractBalancedJson(text, start);
    searchIndex = start + 1;
    if (!jsonText) continue;
    try {
      return normalizeBaiduShareContext(JSON.parse(jsonText));
    } catch {
      continue;
    }
  }
  return null;
}

function extractJsObjectProperty(body, key) {
  const pattern = new RegExp(`(?:^|,)\\s*${escapeRegExp(key)}\\s*:\\s*(?:"([^"]*)"|'([^']*)'|([^,}]+))`, "s");
  const match = String(body || "").match(pattern);
  if (!match) return "";
  return String(match[1] ?? match[2] ?? match[3] ?? "").trim();
}

function mergeBaiduShareContexts(contexts) {
  const merged = {
    bdstoken: "",
    shareId: "",
    shareUk: "",
    title: "",
    rootPath: "",
    files: []
  };

  for (const context of contexts) {
    if (!context) continue;
    if (!merged.bdstoken && context.bdstoken) merged.bdstoken = context.bdstoken;
    if (!merged.shareId && context.shareId) merged.shareId = context.shareId;
    if (!merged.shareUk && context.shareUk) merged.shareUk = context.shareUk;
    if (!merged.title && context.title) merged.title = context.title;
    if (!merged.rootPath && context.rootPath) merged.rootPath = context.rootPath;
    if (merged.files.length === 0 && Array.isArray(context.files) && context.files.length > 0) {
      merged.files = context.files;
    }
  }

  return merged;
}

function extractBalancedJson(text, startIndex) {
  let depth = 0;
  let inString = false;
  let quote = "";
  let escaped = false;

  for (let index = startIndex; index < text.length; index += 1) {
    const char = text[index];
    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (char === "\\") {
        escaped = true;
      } else if (char === quote) {
        inString = false;
      }
      continue;
    }

    if (char === '"' || char === "'") {
      inString = true;
      quote = char;
    } else if (char === "{") {
      depth += 1;
    } else if (char === "}") {
      depth -= 1;
      if (depth === 0) return text.slice(startIndex, index + 1);
    }
  }
  return "";
}

function normalizeBaiduShareContext(data) {
  const files = data.file_list || data.list || [];
  return {
    bdstoken: String(data.bdstoken || ""),
    shareId: stringOrEmpty(data.shareid ?? data.share_id ?? data.shareId),
    shareUk: stringOrEmpty(data.share_uk ?? data.uk ?? data.shareUk),
    title: data.title || data.share_title || data.server_filename || files[0]?.server_filename || "",
    rootPath: files[0]?.parent_path || data.share_root || "",
    files
  };
}

function normalizeBaiduShareItems(rows) {
  return (rows || []).map((row, index) => {
    const isDir = Number(row.isdir ?? row.is_dir ?? row.is_directory ?? 0) === 1 || row.isDirectory === true;
    return {
      rank: index + 1,
      fsId: row.fs_id ?? row.fsid ?? row.id,
      path: row.path || "",
      name: row.server_filename || row.filename || row.name || "未命名资源",
      isDir,
      typeLabel: isDir ? "文件夹" : "文件",
      size: Number(row.size || 0),
      sizeLabel: isDir ? "-" : formatBytes(Number(row.size || 0)),
      updatedAt: row.server_mtime || row.local_mtime || row.mtime || null,
      updatedAtLabel: formatTimestamp(row.server_mtime || row.local_mtime || row.mtime),
      raw: row
    };
  });
}

function buildBaiduTransferRequest({
  apiBase = DEFAULT_API_BASE,
  appId = DEFAULT_APP_ID,
  bdstoken,
  shareId,
  shareUk,
  savePath,
  selectedItems = []
}) {
  const url = new URL("/share/transfer", normalizeApiBase(apiBase));
  const query = {
    app_id: appId,
    channel: "chunlei",
    clienttype: "0",
    web: "1",
    shareid: shareId,
    from: shareUk,
    bdstoken,
    ondup: "newcopy"
  };
  for (const [key, value] of Object.entries(query)) {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, String(value));
    }
  }

  const body = new URLSearchParams();
  body.set("fsidlist", JSON.stringify(selectedItems.map((item) => item.fsId)));
  body.set("path", parseBaiduSavePath(savePath || "/"));
  return { url, body };
}

function buildBaiduRenamePlanForSelection({ args, result, selectedItems }) {
  if (args.noRename) return [];
  if (args.agentRenamePlan) {
    return resolveBaiduRenamePlan({
      selectedItems,
      savePath: args.savePath,
      agentRenamePlan: args.agentRenamePlan
    });
  }
  return buildBaiduRenamePlan({
    resourceType: args.resourceType,
    contextName: result.contextName || "",
    shareTitle: result.shareTitle || "",
    savePath: args.savePath,
    selectedItems
  });
}

function buildBaiduRenamePlan({ resourceType = "auto", contextName = "", shareTitle = "", savePath = "/", selectedItems = [] } = {}) {
  const baseName = sanitizeFileName(contextName || shareTitle || "");
  if (!baseName) return [];
  const classification = classifyResource({ resourceType, contextName: baseName, shareTitle, items: selectedItems });
  const plan = [];
  selectedItems.forEach((item) => {
    const suggestedName = suggestSavedName({
      baseName,
      item,
      selectedCount: selectedItems.length,
      isSeries: classification.isSeries
    });
    if (!suggestedName || suggestedName === item.name) return;
    plan.push({
      sourcePath: joinCloudPath(savePath, item.name),
      originalName: item.name,
      suggestedName,
      reason: classification.isSeries ? "按上下文资源名修正剧集文件名" : "按上下文资源名修正保存名称"
    });
  });
  return plan;
}

function resolveBaiduRenamePlan({ selectedItems = [], savePath = "/", agentRenamePlan = [] } = {}) {
  if (!Array.isArray(agentRenamePlan)) {
    throw new Error("Agent rename plan must be a JSON array");
  }
  const plan = [];
  for (const decision of agentRenamePlan) {
    const rank = Number(decision.rank ?? decision.index);
    if (!Number.isFinite(rank) || rank < 1) {
      throw new Error(`Agent rename plan item is missing a valid rank/index: ${JSON.stringify(decision)}`);
    }
    const selectedIndex = selectedItems.findIndex((item) => item.rank === rank);
    const fallbackIndex = selectedItems[rank - 1] ? rank - 1 : -1;
    const itemIndex = selectedIndex >= 0 ? selectedIndex : fallbackIndex;
    if (itemIndex < 0) {
      throw new Error(`Agent rename plan rank is not selected: ${rank}`);
    }

    const item = selectedItems[itemIndex];
    const suggestedName = sanitizeFileName(decision.name || decision.suggestedName || "");
    if (!suggestedName) {
      throw new Error(`Agent rename plan item is missing name/suggestedName: ${JSON.stringify(decision)}`);
    }
    if (suggestedName === item.name) continue;
    plan.push({
      sourcePath: joinCloudPath(savePath, item.name),
      originalName: item.name,
      suggestedName,
      reason: decision.reason || "Agent 指定重命名"
    });
  }
  return plan;
}

function renderBaiduShareItemsTable({
  shareTitle = "",
  contextName = "",
  savePath = "",
  items = [],
  classification,
  renamePlan = []
}) {
  const detected = classification || classifyResource({ contextName, shareTitle, items });
  const lines = [
    "### 百度网盘分享资源",
    "",
    `分享标题：${escapeMarkdownText(shareTitle || "-")}`,
    `修正资源名：${escapeMarkdownText(contextName || "-")}`,
    `目标目录：${escapeMarkdownText(savePath || "-")}`,
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
    "### 百度网盘转存结果",
    "",
    `已选择：${saveResult.selectedItems.length} 项`,
    `接口 errno：${saveResult.transferResponse.errno ?? 0}`
  ];
  if (saveResult.renameResults.length > 0) {
    lines.push("", "重命名修正：");
    saveResult.renameResults.forEach((item) => {
      lines.push(`- ${item.ok ? "成功" : "失败"}：${item.originalName} -> ${item.suggestedName}${item.error ? `（${item.error}）` : ""}`);
    });
  }
  return lines.join("\n");
}

function buildBaiduSubagentPreview({ args = {}, result }) {
  const selectedItems = result.selectedPreview || parseSelection(result.defaultSelection || args.defaultSelection || "all", result.items || []);
  return {
    ok: true,
    provider: "baidu",
    mode: "preview",
    nextAction: "confirm_before_save",
    source: {
      shareUrl: args.shareUrl || "",
      shareId: result.share?.featureStr || "",
      passcodePresent: Boolean(result.share?.passcode)
    },
    target: {
      provider: "baidu",
      pathOrUrl: result.savePath || args.savePath || ""
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
      selectedItems: selectedItems.map(serializeBaiduItem)
    },
    items: (result.items || []).map(serializeBaiduItem),
    renamePlan: serializeRenamePlan(result.renamePlan || []),
    confirmation: {
      source: args.shareUrl || "",
      selectedItems: selectedItems.map(serializeBaiduItem),
      target: {
        provider: "baidu",
        pathOrUrl: result.savePath || args.savePath || ""
      },
      finalNaming: serializeRenamePlan(result.renamePlan || []),
      commandHint: "Re-run scripts/baidu-save.mjs with --yes after the user confirms this payload."
    }
  };
}

function buildBaiduSubagentSave({ args = {}, result, saveResult }) {
  return {
    ok: true,
    provider: "baidu",
    mode: "save",
    nextAction: "verify_target_path_or_openlist",
    source: {
      shareUrl: args.shareUrl || "",
      shareId: result.share?.featureStr || "",
      passcodePresent: Boolean(result.share?.passcode)
    },
    target: {
      provider: "baidu",
      pathOrUrl: result.savePath || args.savePath || ""
    },
    resource: {
      shareTitle: result.shareTitle || "",
      canonicalName: result.contextName || "",
      type: result.classification?.type || "unknown",
      label: result.classification?.label || "",
      isSeries: Boolean(result.classification?.isSeries),
      reason: result.classification?.reason || ""
    },
    selectedItems: (saveResult.selectedItems || []).map(serializeBaiduItem),
    errno: saveResult.transferResponse?.errno ?? 0,
    transferResponse: summarizeBaiduTransferResponse(saveResult.transferResponse || {}),
    renamePlan: serializeRenamePlan(saveResult.renamePlan || []),
    renameResults: serializeRenameResults(saveResult.renameResults || [])
  };
}

function serializeBaiduItem(item) {
  return {
    rank: item.rank,
    id: item.fsId,
    path: item.path,
    name: item.name,
    typeLabel: item.typeLabel,
    isDir: item.isDir,
    size: item.size,
    sizeLabel: item.sizeLabel,
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

function summarizeBaiduTransferResponse(response) {
  return {
    errno: response.errno ?? 0,
    showMsg: response.show_msg || "",
    taskId: response.task_id || response.taskid || ""
  };
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

async function verifyBaiduShare({ apiBase, timeoutMs, cookie, bdstoken, verifySurl, passcode, referer }) {
  const url = new URL("/share/verify", normalizeApiBase(apiBase));
  const query = {
    surl: verifySurl,
    bdstoken,
    channel: "chunlei",
    web: "1",
    app_id: DEFAULT_APP_ID,
    clienttype: "0",
    t: Date.now()
  };
  for (const [key, value] of Object.entries(query)) {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  }
  const body = new URLSearchParams();
  body.set("pwd", passcode || "");
  body.set("vcode", "");
  body.set("vcode_str", "");

  const result = await fetchBaiduJsonWithMeta(url, {
    method: "POST",
    timeoutMs,
    cookie,
    referer,
    body
  });
  if (result.json.errno !== 0) {
    throw new Error(`百度提取码校验失败 errno=${result.json.errno}: ${result.json.show_msg || result.json.errmsg || "unknown error"}`);
  }
  return {
    randsk: result.json.randsk || "",
    setCookies: result.setCookies
  };
}

async function getBaiduBdstoken({ apiBase, timeoutMs, cookie }) {
  const url = new URL("/api/gettemplatevariable", normalizeApiBase(apiBase));
  url.searchParams.set("fields", '["bdstoken"]');
  const response = await fetchBaiduJson(url, {
    timeoutMs,
    cookie,
    referer: normalizeApiBase(apiBase)
  });
  return response.result?.bdstoken || response.bdstoken || "";
}

async function listBaiduShareFiles({ apiBase, appId, timeoutMs, cookie, shareId, shareUk, sekey = "", dir = "/" }) {
  const rows = [];
  let page = 1;
  while (true) {
    const url = new URL("/share/list", normalizeApiBase(apiBase));
    const query = {
      app_id: appId || DEFAULT_APP_ID,
      channel: "chunlei",
      clienttype: "0",
      web: "1",
      uk: shareUk,
      shareid: shareId,
      order: "name",
      desc: "0",
      showempty: "0",
      page,
      num: DEFAULT_PAGE_SIZE,
      dir
    };
    for (const [key, value] of Object.entries(query)) {
      url.searchParams.set(key, String(value));
    }
    if (sekey) url.searchParams.set("sekey", sekey);

    const response = await fetchBaiduJson(url, {
      timeoutMs,
      cookie,
      referer: normalizeApiBase(apiBase)
    });
    const list = response.list || [];
    rows.push(...list);
    if (list.length < DEFAULT_PAGE_SIZE) break;
    page += 1;
  }
  return rows;
}

async function transferBaiduShare({ apiBase, appId, timeoutMs, cookie, referer, bdstoken, shareId, shareUk, savePath, selectedItems }) {
  if (!bdstoken) {
    throw new Error("缺少百度 bdstoken，无法调用 share/transfer。请确认 BAIDU_COOKIE 有效且已登录百度网盘。");
  }
  const request = buildBaiduTransferRequest({
    apiBase,
    appId,
    bdstoken,
    shareId,
    shareUk,
    savePath,
    selectedItems
  });
  return fetchBaiduJson(request.url, {
    method: "POST",
    timeoutMs,
    cookie,
    referer,
    body: request.body
  });
}

async function listBaiduDir({ apiBase, appId, timeoutMs, cookie, bdstoken, dir }) {
  const url = new URL("/api/list", normalizeApiBase(apiBase));
  const query = {
    app_id: appId || DEFAULT_APP_ID,
    channel: "chunlei",
    clienttype: "0",
    web: "1",
    order: "name",
    desc: "0",
    showempty: "0",
    page: "1",
    num: "1000",
    dir,
    bdstoken
  };
  for (const [key, value] of Object.entries(query)) {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  }
  const response = await fetchBaiduJson(url, {
    timeoutMs,
    cookie,
    referer: normalizeApiBase(apiBase)
  });
  return normalizeBaiduShareItems(response.list || []);
}

async function applyBaiduRenamePlan({ apiBase, appId, timeoutMs, cookie, bdstoken, savePath, renamePlan }) {
  const targetRows = await listBaiduDir({
    apiBase,
    appId,
    timeoutMs,
    cookie,
    bdstoken,
    dir: savePath
  });
  const results = [];

  for (const item of renamePlan) {
    try {
      const matched = targetRows.find((row) => row.name === item.originalName);
      const sourcePath = matched?.path || item.sourcePath;
      const response = await renameBaiduPath({
        apiBase,
        appId,
        timeoutMs,
        cookie,
        bdstoken,
        sourcePath,
        newName: item.suggestedName
      });
      results.push({ ...item, ok: true, response });
    } catch (error) {
      results.push({ ...item, ok: false, error: error.message || String(error) });
    }
  }

  return results;
}

async function renameBaiduPath({ apiBase, appId, timeoutMs, cookie, bdstoken, sourcePath, newName }) {
  const url = new URL("/api/filemanager", normalizeApiBase(apiBase));
  const query = {
    app_id: appId || DEFAULT_APP_ID,
    channel: "chunlei",
    clienttype: "0",
    web: "1",
    opera: "rename",
    async: "2",
    onnest: "fail",
    bdstoken
  };
  for (const [key, value] of Object.entries(query)) {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  }
  const body = new URLSearchParams();
  body.set("filelist", JSON.stringify([{ path: sourcePath, newname: newName }]));
  return fetchBaiduJson(url, {
    method: "POST",
    timeoutMs,
    cookie,
    referer: normalizeApiBase(apiBase),
    body
  });
}

async function fetchBaiduText(url, options = {}) {
  const result = await fetchWithTimeout(url, options);
  const text = await result.response.text();
  if (!result.response.ok) {
    throw new Error(`HTTP ${result.response.status} from ${result.url}: ${text.slice(0, 200)}`);
  }
  return text;
}

async function fetchBaiduJson(url, options = {}) {
  return (await fetchBaiduJsonWithMeta(url, options)).json;
}

async function fetchBaiduJsonWithMeta(url, options = {}) {
  const result = await fetchWithTimeout(url, options);
  const text = await result.response.text();
  let json;
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(`Expected JSON from ${result.url}, got: ${text.slice(0, 200)}`);
  }
  if (!result.response.ok) {
    throw new Error(`HTTP ${result.response.status} from ${result.url}: ${JSON.stringify(json).slice(0, 300)}`);
  }
  if (json && typeof json === "object" && "errno" in json && Number(json.errno) !== 0) {
    throw new Error(`Baidu API error ${json.errno}: ${json.show_msg || json.errmsg || json.errno_msg || "unknown error"}`);
  }
  return {
    json,
    setCookies: getSetCookieHeaders(result.response.headers)
  };
}

async function fetchWithTimeout(url, options = {}) {
  const requestUrl = new URL(String(url));
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeoutMs || DEFAULT_TIMEOUT_MS);
  try {
    const headers = {
      Accept: options.accept || "application/json, text/plain, */*",
      "User-Agent": USER_AGENT
    };
    if (options.body instanceof URLSearchParams) {
      headers["Content-Type"] = "application/x-www-form-urlencoded";
    }
    if (options.cookie) headers.Cookie = options.cookie;
    if (options.referer) headers.Referer = options.referer;
    const response = await fetch(requestUrl, {
      method: options.method || "GET",
      headers,
      body: options.body,
      signal: controller.signal
    });
    return { response, url: requestUrl };
  } finally {
    clearTimeout(timeout);
  }
}

function getSetCookieHeaders(headers) {
  if (typeof headers.getSetCookie === "function") return headers.getSetCookie();
  const value = headers.get("set-cookie");
  return value ? [value] : [];
}

function mergeCookieString(cookie, setCookies = []) {
  const values = new Map();
  for (const part of String(cookie || "").split(";")) {
    const trimmed = part.trim();
    if (!trimmed) continue;
    const equalIndex = trimmed.indexOf("=");
    if (equalIndex === -1) continue;
    values.set(trimmed.slice(0, equalIndex), trimmed.slice(equalIndex + 1));
  }
  for (const setCookie of setCookies || []) {
    const first = String(setCookie || "").split(";")[0].trim();
    const equalIndex = first.indexOf("=");
    if (equalIndex === -1) continue;
    values.set(first.slice(0, equalIndex), first.slice(equalIndex + 1));
  }
  return [...values.entries()].map(([key, value]) => `${key}=${value}`).join("; ");
}

function resolveCookie(args) {
  return (args.env?.[args.cookieEnv] || process.env[args.cookieEnv] || "").trim();
}

function normalizeApiBase(value) {
  return String(value || DEFAULT_API_BASE).replace(/\/+$/g, "");
}

function isCloudDrivePath(value) {
  return String(value || "").startsWith("/") && !String(value).includes("..");
}

function parseBaiduSavePath(value) {
  const text = String(value || "").trim();
  if (!text) return "";
  if (isCloudDrivePath(text)) return text;

  let parsed;
  try {
    parsed = new URL(text);
  } catch {
    throw new Error(`百度保存目录必须是网盘内路径或百度目录 URL：${value}`);
  }
  if (!parsed.hostname.endsWith("pan.baidu.com")) {
    throw new Error(`百度保存目录 URL 必须来自 pan.baidu.com：${value}`);
  }

  const hashQuery = parsed.hash.includes("?") ? parsed.hash.slice(parsed.hash.indexOf("?") + 1) : "";
  const pathValue = new URLSearchParams(hashQuery).get("path") || parsed.searchParams.get("path") || "";
  if (!isCloudDrivePath(pathValue)) {
    throw new Error(`百度目录 URL 必须包含有效 path 参数：${value}`);
  }
  return pathValue;
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

function joinCloudPath(basePath, name) {
  const base = String(basePath || "/").replace(/\/+$/g, "") || "/";
  const cleanName = String(name || "").replace(/^\/+/g, "");
  return base === "/" ? `/${cleanName}` : `${base}/${cleanName}`;
}

function parseJson(value, label) {
  try {
    return JSON.parse(value || "[]");
  } catch (error) {
    throw new Error(`${label} must be valid JSON: ${error.message}`);
  }
}

function stringOrEmpty(value) {
  return value === undefined || value === null ? "" : String(value);
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
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
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return "-";
  const ms = numeric < 1_000_000_000_000 ? numeric * 1000 : numeric;
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

function isCliEntryPoint() {
  return Boolean(process.argv[1]) && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

export {
  applyEnvDefaults,
  buildBaiduRenamePlan,
  buildBaiduSubagentPreview,
  buildBaiduSubagentSave,
  buildBaiduTransferRequest,
  extractBaiduShareContextFromHtml,
  normalizeBaiduShareItems,
  parseBaiduSavePath,
  parseBaiduShareUrl,
  renderBaiduShareItemsTable
};
