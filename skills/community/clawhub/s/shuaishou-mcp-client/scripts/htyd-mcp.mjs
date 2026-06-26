import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import readline from "node:readline";
import http from "node:http";
import https from "node:https";

function getMcpUrl() {
  // 正式环境：生产服务器
  return process.env.MCP_URL ?? "https://dz.shuaishou.com/mcp";
}

function getConfigFilePath() {
  // 正式环境配置文件，与开发环境隔离
  return path.join(os.homedir(), ".htyd-mcp-client-streamable.json");
}

function safeReadJson(filePath) {
  try {
    if (!fs.existsSync(filePath)) return null;
    const raw = fs.readFileSync(filePath, "utf8");
    if (!raw.trim()) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function safeWriteJson(filePath, obj) {
  try {
    fs.writeFileSync(filePath, JSON.stringify(obj, null, 2), "utf8");
  } catch {
    // ignore
  }
}

function envAuthorization() {
  const raw = process.env.MCP_AUTHORIZATION;
  if (raw && raw.trim()) return raw.trim();
  const appKey = process.env.MCP_APP_KEY;
  if (appKey && String(appKey).trim()) return `Bearer ${String(appKey).trim()}`;
  return "";
}

function normalizeAuthorizationInput(input) {
  const s = String(input ?? "").trim();
  if (!s) return "";
  if (/^(Bearer|Basic)\s+/i.test(s)) return s;
  return `Bearer ${s}`;
}

function isAuthError(err) {
  const msg = String(err?.message ?? "");
  return msg.startsWith("HTTP 401") || msg.startsWith("HTTP 403");
}

async function promptForAuthorization() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    const answer = await new Promise((resolve) =>
      rl.question("MCP AppKey/Authorization not set. Please input MCP_APP_KEY (or full 'Bearer xxx'):\n> ", resolve)
    );
    return normalizeAuthorizationInput(answer);
  } finally {
    rl.close();
  }
}

async function getAuthHeadersInteractive({ forcePrompt = false } = {}) {
  const fromEnv = envAuthorization();
  if (!forcePrompt && fromEnv) return { Authorization: fromEnv };

  const configPath = getConfigFilePath();
  const cfg = safeReadJson(configPath) ?? {};
  const fromFile = !forcePrompt && typeof cfg.authorization === "string" ? cfg.authorization.trim() : "";
  if (fromFile) return { Authorization: fromFile };

  const authorization = await promptForAuthorization();
  if (!authorization) return {};

  safeWriteJson(configPath, { ...cfg, authorization });
  return { Authorization: authorization };
}

function usage(exitCode = 1) {
  const msg = `
Usage:
  node htyd-mcp.mjs tools
  node htyd-mcp.mjs call <toolName> <jsonArgs>

Convenience commands (mapped to tool calls):
  node htyd-mcp.mjs login_shuashou --username <u> --password <p> [--loginType <t>]
  node htyd-mcp.mjs list_shops [--platform <p>]
  node htyd-mcp.mjs collect_goods --originList <url1> [--originList <url2> ...] [--ssuid <id>]
  node htyd-mcp.mjs list_collected_goods [--claimStatus 0|1] [--pageNo <n>] [--pageSize <n>]
  node htyd-mcp.mjs claim_goods --itemIds <id1,id2,...> --platId <n> --merchantIds <id1,id2,...>
  node htyd-mcp.mjs collect_and_publish --originList <url> --platId <n> --merchantIds <id> [--pubShops <id>]
  node htyd-mcp.mjs publish_and_track --itemIds <id1,id2,...> [--pubShops <id1,id2,...>] [--timeoutSec <n>] [--intervalSec <n>]

Env:
  MCP_URL (default: ${getMcpUrl()})
  MCP_APP_KEY (optional; used as Bearer token)
  MCP_AUTHORIZATION (optional; overrides Authorization header)

New: collect_and_publish workflow:
  1. collect_goods      - Collect product from 1688/Taobao
  2. claim_goods        - Claim to target shop (creates draft)
  3. list_temu_drafts   - Find the draft by origin URL + shop
  4. publish_temu       - Publish the draft to shop
  5. list_publish_records_by_item_id - Track publish status/result
`;
  // eslint-disable-next-line no-console
  console.error(msg.trim());
  process.exit(exitCode);
}

function parseFlags(argv) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next == null || next.startsWith("--")) {
        flags[key] = true;
      } else {
        if (flags[key] == null) flags[key] = next;
        else if (Array.isArray(flags[key])) flags[key].push(next);
        else flags[key] = [flags[key], next];
        i++;
      }
    } else {
      positional.push(a);
    }
  }
  return { flags, positional };
}

function normalizeMulti(v) {
  if (v == null) return [];
  return Array.isArray(v) ? v : [v];
}

function csvToList(v) {
  if (v == null) return [];
  return String(v)
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

function tryParseJson(v) {
  if (v == null) return v;
  if (typeof v !== "string") return v;
  const s = v.trim();
  if (!s) return v;
  try {
    return JSON.parse(s);
  } catch {
    return v;
  }
}

function extractCollectedItems(payload) {
  const p = tryParseJson(payload);
  if (!p || typeof p !== "object") return [];

  // common shapes:
  // - { data: { list: [...] } }
  // - { list: [...] }
  // - { data: { records: [...] } }
  // - { records: [...] }
  // - { data: [...] }
  const candidates = [
    p?.data?.list,
    p?.list,
    p?.data?.records,
    p?.records,
    p?.data?.data?.list,
    p?.data?.data?.records,
    p?.data,
  ];
  for (const c of candidates) {
    if (Array.isArray(c)) return c;
  }
  return [];
}

function extractPublishRecords(payload) {
  const p = tryParseJson(payload);
  if (!p || typeof p !== "object") return [];

  // common shapes:
  // - { data: { records: [...] } }
  // - { records: [...] }
  // - { data: { list: [...] } }
  // - { list: [...] }
  // - { data: [...] }
  const candidates = [
    p?.data?.records,
    p?.records,
    p?.data?.list,
    p?.list,
    p?.data?.data?.records,
    p?.data?.data?.list,
    p?.data,
  ];
  for (const c of candidates) {
    if (Array.isArray(c)) return c;
  }
  return [];
}

function getPublishStatusField(obj) {
  const raw =
    obj?.publishStatus ??
    obj?.publish_status ??
    obj?.status ??
    obj?.publishState ??
    obj?.state;
  if (raw == null) return "";
  return String(raw).trim();
}

function isPublishSuccess(status) {
  const s = String(status ?? "").toUpperCase();
  return s === "SUCCESS" || s === "SUCCEED" || s === "DONE";
}

function isPublishFail(status) {
  const s = String(status ?? "").toUpperCase();
  return s === "FAIL" || s === "FAILED" || s === "ERROR";
}

function extractPublishErrorMessage(obj) {
  const candidates = [
    obj?.errorMessage,
    obj?.error_message,
    obj?.failReason,
    obj?.fail_reason,
    obj?.reason,
    obj?.msg,
    obj?.message,
    obj?.remark,
    obj?.error,
  ];
  for (const c of candidates) {
    if (c == null) continue;
    const s = String(c).trim();
    if (s) return s;
  }
  return "";
}

function toNumberOrNull(v) {
  if (v == null) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function getRecordSortKey(obj) {
  const t =
    obj?.updateTime ??
    obj?.update_time ??
    obj?.publishTime ??
    obj?.publish_time ??
    obj?.createTime ??
    obj?.create_time ??
    obj?.gmtCreate ??
    obj?.gmt_create;
  if (t != null) {
    const s = String(t);
    const ms = Date.parse(s);
    if (!Number.isNaN(ms)) return ms;
  }
  const id =
    toNumberOrNull(obj?.id) ??
    toNumberOrNull(obj?.recordId) ??
    toNumberOrNull(obj?.record_id);
  if (id != null) return id;
  return 0;
}

async function waitForPublishResult(client, {
  ids,
  timeoutMs,
  intervalMs,
} = {}) {
  const start = Date.now();
  const timeout = timeoutMs ?? 180000;
  const interval = intervalMs ?? 3000;

  const idList = Array.isArray(ids) ? ids : (ids == null ? [] : [ids]);
  if (!idList.length) {
    return { ok: false, status: "INVALID_PARAM", record: null, errorMessage: "ids 不能为空" };
  }

  while (Date.now() - start <= timeout) {
    const res = await client.callTool("list_publish_records_by_item_id", {
      ids: idList.map((x) => Number(x)).filter((x) => Number.isFinite(x) && x > 0),
    });

    const records = extractPublishRecords(res);
    const sorted = records.slice().sort((a, b) => getRecordSortKey(b) - getRecordSortKey(a));

    const pick = sorted[0];

    if (pick) {
      const st = getPublishStatusField(pick);
      if (isPublishSuccess(st)) {
        return { ok: true, status: st, record: pick };
      }
      if (isPublishFail(st)) {
        return { ok: false, status: st, record: pick, errorMessage: extractPublishErrorMessage(pick) };
      }
    }

    await delay(interval);
  }

  return { ok: false, status: "TIMEOUT", record: null, errorMessage: "发布结果查询超时，请稍后用 list_publish_records_by_item_id 再查询" };
}

function getStringField(obj, keys) {
  for (const k of keys) {
    const v = obj?.[k];
    if (v == null) continue;
    const s = String(v).trim();
    if (s) return s;
  }
  return "";
}

function getIdField(obj) {
  const v =
    obj?.itemId ??
    obj?.item_id ??
    obj?.id ??
    obj?.goodsId ??
    obj?.goods_id;
  if (v == null) return "";
  const s = String(v).trim();
  return s;
}

function isDuplicateCollectedItem(item) {
  // flags
  const boolFlags = [
    item?.duplicate,
    item?.isDuplicate,
    item?.is_duplicate,
    item?.repeat,
    item?.isRepeat,
    item?.is_repeat,
    item?.repeatCollect,
  ];
  if (boolFlags.some((x) => x === true || x === 1 || x === "1")) return true;

  // text hints
  const statusText = getStringField(item, [
    "collectStatusName",
    "collect_status_name",
    "statusName",
    "status_name",
    "message",
    "msg",
  ]);
  if (statusText.includes("重复")) return true;
  return false;
}

function isCollectingItem(item) {
  const statusText = getStringField(item, [
    "collectStatusName",
    "collect_status_name",
    "statusName",
    "status_name",
  ]);
  if (statusText.includes("采集中") || statusText.includes("处理中")) return true;

  const statusCode =
    item?.collectStatus ??
    item?.collect_status ??
    item?.status;
  if (statusCode === 0 || statusCode === "0") return true;
  return false;
}

function isClaimedItem(item) {
  const claimStatus = item?.claimStatus ?? item?.claim_status;
  if (claimStatus === 1 || claimStatus === "1") return true;
  
  // 如果 claimStatus 为 null 但商品有 claintList 或 platList，也认为已认领
  const claintList = item?.claintList ?? item?.claint_list ?? [];
  const platList = item?.platList ?? item?.plat_list ?? [];
  if (claintList.length > 0 || platList.length > 0) return true;
  
  return false;
}

function isCollectSuccessItem(item) {
  const statusText = getStringField(item, [
    "collectStatusName", "collect_status_name", "statusName", "status_name", "status"
  ]);
  // 只算真正的采集成功，重复采集(repeat)不算
  if (statusText.includes("采集成功") || statusText === "成功" || statusText === "success") return true;

  const statusCode = item?.collectStatus ?? item?.collect_status ?? item?.status;
  if (statusCode === 1 || statusCode === "1" || statusCode === "SUCCESS" || statusCode === "success") return true;

  return false;
}

function matchOrigin(item, originList) {
  if (!originList?.length) return true;
  const url = getStringField(item, [
    "originUrl",
    "origin_url",
    "originLink",
    "origin_link",
    "sourceUrl",
    "source_url",
    "oriUrl",
    "ori_url",
    "url",
    "link",
  ]);
  if (!url) return false;
  
  // 规范化 URL：去除协议和 www 前缀，便于匹配
  const normalize = (u) => String(u).trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/+$/, '');
  const normalizedUrl = normalize(url);
  
  return originList.some((u) => {
    const normalizedU = normalize(u);
    return normalizedU && (normalizedUrl.includes(normalizedU) || normalizedU.includes(normalizedUrl));
  });
}

// 从 URL 中提取商品 ID 用于精确匹配
function extractProductId(url) {
  if (!url) return null;
  // 1688: https://detail.1688.com/offer/123456.html
  const match1688 = url.match(/\/offer\/(\d+)/);
  if (match1688) return { platform: '1688', id: match1688[1] };
  // 淘宝: https://item.taobao.com/item.htm?id=123456
  const matchTaobao = url.match(/[?&]id=(\d+)/);
  if (matchTaobao) return { platform: 'taobao', id: matchTaobao[1] };
  return null;
}

// Minimal MCP client: Streamable HTTP (POST /mcp JSON-RPC)
// (imports moved to top)

class McpStreamableHttpJsonRpcClient {
  constructor(mcpUrl, headers = {}) {
    this.mcpUrl = mcpUrl;
    this.headers = headers;
    this.msgId = 0;
    this.sessionId = null;
  }

  async connect() {
    // Streamable HTTP 不需要单独建立 SSE 连接；保留接口以兼容现有调用流程
    return;
  }

  async initialize() {
    await this.sendJsonRpc("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: { name: "htyd-mcp-client", version: "0.1.0" },
    });
    await this.sendNotification("notifications/initialized");
  }

  async listTools() {
    const result = await this.sendJsonRpc("tools/list", {});
    return result?.tools ?? [];
  }

  async callTool(name, args) {
    const result = await this.sendJsonRpc("tools/call", {
      name,
      arguments: args ?? {},
    });
    if (result?.content?.length) {
      const first = result.content[0];
      if (typeof first?.text === "string") return first.text;
    }
    return result;
  }

  async sendNotification(method) {
    const body = JSON.stringify({ jsonrpc: "2.0", method });
    await this.post(body, null);
  }

  async sendJsonRpc(method, params) {
    const id = ++this.msgId;
    const body = JSON.stringify({ jsonrpc: "2.0", id, method, params });

    const msg = await this.post(body, id);
    if (msg?.error) throw new Error(JSON.stringify(msg.error));
    return msg?.result;
  }

  async post(body, expectedId) {
    const url = new URL(this.mcpUrl);
    const client = url.protocol === "https:" ? https : http;
    const acceptHeader = "application/json, text/event-stream";
    return await new Promise((resolve, reject) => {
      const req = client.request(
        url,
        {
          method: "POST",
          headers: {
            ...this.headers,
            ...(this.sessionId ? { "Mcp-Session-Id": this.sessionId } : {}),
            Accept: acceptHeader,
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(body),
          },
        },
        (res) => {
          if ((res.statusCode ?? 0) >= 400) {
            let data = "";
            res.on("data", (c) => (data += c));
            res.on("end", () =>
              reject(new Error(`HTTP ${res.statusCode}: ${data}`))
            );
            return;
          }

          // Spring AI / MCP Streamable HTTP may respond with JSON or with SSE
          // (`event: message` + `data: {...json...}`).
          const ct = String(res.headers["content-type"] ?? "").toLowerCase();
          const isSse = ct.includes("text/event-stream");

          const sid =
            res.headers["mcp-session-id"] ||
            res.headers["Mcp-Session-Id"] ||
            null;
          if (sid && typeof sid === "string") this.sessionId = sid;

          if (isSse) {
            let resolved = false;
            let buffer = "";

            res.on("data", (chunk) => {
              buffer += chunk.toString("utf8");
              const lines = buffer.split(/\r?\n/);
              buffer = lines.pop() ?? "";

              for (const line of lines) {
                if (resolved) break;
                if (!line.startsWith("data:")) continue;
                const payload = line.slice(5).trim();
                if (!payload) continue;

                try {
                  const obj = JSON.parse(payload);
                  if (expectedId != null) {
                    if (String(obj?.id) !== String(expectedId)) continue;
                  }
                  resolved = true;
                  resolve(obj);
                  res.destroy();
                  break;
                } catch {
                  // ignore non-JSON / partial data lines
                }
              }
            });

            res.on("end", () => {
              if (!resolved) resolve(null);
            });
            return;
          }

          let data = "";
          res.on("data", (c) => (data += c));
          res.on("end", () => {
            try {
              resolve(data ? JSON.parse(data) : null);
            } catch (e) {
              reject(
                new Error(
                  `Invalid JSON response: ${e?.message ?? e}; raw=${String(data).slice(0, 2000)}`
                )
              );
            }
          });
        }
      );
      req.on("error", reject);
      req.write(body);
      req.end();
    });
  }

  close() {
    // no-op
  }
}

async function withClient(fn) {
  let headers = await getAuthHeadersInteractive();
  let client = new McpStreamableHttpJsonRpcClient(getMcpUrl(), headers);
  await client.connect();
  await client.initialize();
  try {
    return await fn(client);
  } catch (e) {
    if (!envAuthorization() && isAuthError(e)) {
      headers = await getAuthHeadersInteractive({ forcePrompt: true });
      client = new McpStreamableHttpJsonRpcClient(getMcpUrl(), headers);
      await client.connect();
      await client.initialize();
      return await fn(client);
    }
    throw e;
  } finally {
    client.close();
  }
}

async function cmdTools() {
  await withClient(async (client) => {
    const tools = await client.listTools();

    // eslint-disable-next-line no-console
    console.log(
      JSON.stringify(
        tools.map((t) => ({
          name: t.name,
          description: t.description,
          inputSchema: t.inputSchema,
        })),
        null,
        2
      )
    );
  });
}

async function cmdCall(toolName, jsonArgs) {
  let args = {};
  if (jsonArgs != null && String(jsonArgs).trim() !== "") {
    try {
      args = JSON.parse(jsonArgs);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(`Invalid JSON args: ${e?.message ?? e}`);
      process.exit(2);
    }
  }

  await withClient(async (client) => {
    const res = await client.callTool(toolName, args);
    // eslint-disable-next-line no-console
    console.log(typeof res === "string" ? res : JSON.stringify(res, null, 2));
  });
}

async function cmdLogin(flags) {
  const username = flags.username;
  const password = flags.password;
  const loginType = flags.loginType;
  if (!username || !password) usage(2);

  await cmdCall(
    "login_shuashou",
    JSON.stringify({
      username,
      password,
      ...(loginType ? { loginType } : {}),
    })
  );
}

async function cmdListShops(flags) {
  const platform = flags.platform;
  await cmdCall(
    "list_shops",
    JSON.stringify(platform ? { platform } : {})
  );
}

async function cmdCollectGoods(flags) {
  const originList = normalizeMulti(flags.originList);
  const ssuid = flags.ssuid;
  if (!originList.length) usage(2);
  await cmdCall(
    "collect_goods",
    JSON.stringify({
      originList,
      ...(ssuid ? { ssuid } : {}),
    })
  );
}

async function cmdListCollectedGoods(flags) {
  const claimStatus =
    flags.claimStatus == null ? undefined : Number(flags.claimStatus);
  const pageNo = flags.pageNo == null ? undefined : Number(flags.pageNo);
  const pageSize = flags.pageSize == null ? undefined : Number(flags.pageSize);

  await cmdCall(
    "list_collected_goods",
    JSON.stringify({
      ...(Number.isFinite(claimStatus) ? { claimStatus } : {}),
      ...(Number.isFinite(pageNo) ? { pageNo } : {}),
      ...(Number.isFinite(pageSize) ? { pageSize } : {}),
    })
  );
}

async function cmdClaimGoods(flags) {
  const itemIds = csvToList(flags.itemIds);
  const originList = normalizeMulti(flags.originList);
  const platId = flags.platId == null ? undefined : Number(flags.platId);
  const merchantIds = csvToList(flags.merchantIds).map((x) => Number(x));
  if (!Number.isFinite(platId) || !merchantIds.length) usage(2);

  // If itemIds are provided explicitly, keep current behavior.
  if (itemIds.length) {
    await cmdCall(
      "claim_goods",
      JSON.stringify({
        itemIds,
        plats: [{ platId, merchantIds }],
      })
    );
    return;
  }

  // Otherwise, auto-pick itemIds from list_collected_goods
  if (!originList.length) {
    // eslint-disable-next-line no-console
    console.error(
      "claim_goods: 请传 --itemIds 或 --originList（将从 list_collected_goods 自动筛选可认领商品）"
    );
    usage(2);
  }

  await withClient(async (client) => {
    const listRes = await client.callTool("list_collected_goods", {
      claimStatus: 0,
      pageNo: 1,
      pageSize: 200,
    });

    const items = extractCollectedItems(listRes);
    const matched = items.filter((it) => matchOrigin(it, originList));
    const eligible = matched
      .filter((it) => isCollectSuccessItem(it))
      .filter((it) => !isDuplicateCollectedItem(it))
      .filter((it) => !isCollectingItem(it));

    const pickedIds = eligible
      .map((it) => getIdField(it))
      .filter(Boolean);

    // eslint-disable-next-line no-console
    console.error(
      `claim_goods auto-pick: total=${items.length}, matched=${matched.length}, eligible=${eligible.length}, pickedIds=${pickedIds.length}`
    );

    if (!pickedIds.length) {
      // eslint-disable-next-line no-console
      console.error(
        "未找到可认领商品：要求【采集成功】【非重复采集】【非采集中】且链接匹配 originList"
      );
      process.exit(3);
    }

    const res = await client.callTool("claim_goods", {
      itemIds: pickedIds,
      plats: [{ platId, merchantIds }],
    });

    // eslint-disable-next-line no-console
    console.log(typeof res === "string" ? res : JSON.stringify(res, null, 2));
  });
}

async function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function cmdCollectAndPublish(flags) {
  const originList = normalizeMulti(flags.originList);
  const platId = flags.platId == null ? undefined : Number(flags.platId);
  const merchantIds = csvToList(flags.merchantIds).map((x) => Number(x));
  const pubShops = csvToList(flags.pubShops).map((x) => Number(x));
  const track = flags.track == null ? true : String(flags.track) !== "false";
  const timeoutSec = flags.timeoutSec == null ? 180 : Number(flags.timeoutSec);
  const intervalSec = flags.intervalSec == null ? 3 : Number(flags.intervalSec);

  if (!originList.length) {
    // eslint-disable-next-line no-console
    console.error("collect_and_publish: --originList cannot be empty");
    usage(2);
  }
  if (!Number.isFinite(platId) || !merchantIds.length) {
    // eslint-disable-next-line no-console
    console.error("collect_and_publish: --platId and --merchantIds are required");
    usage(2);
  }

  const targetPubShops = pubShops.length ? pubShops : [merchantIds[0]];

  await withClient(async (client) => {
    const results = [];

    for (let i = 0; i < originList.length; i++) {
      const targetUrl = originList[i];
      const itemNum = i + 1;
      const total = originList.length;

      // eslint-disable-next-line no-console
      console.log(`\n[${itemNum}/${total}] Processing: ${targetUrl}`);

      try {
        const result = await processSingleItem(client, {
          targetUrl,
          platId,
          merchantIds,
          targetPubShops,
          itemNum,
          total,
          track,
          timeoutSec,
          intervalSec
        });
        results.push(result);
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error(`[${itemNum}/${total}] Failed: ${e.message}`);
        results.push({
          success: false,
          originUrl: targetUrl,
          itemId: null,
          title: "",
          status: "ERROR",
          temuProductId: null,
          failReason: e.message
        });
      }
    }

    // Final summary
    const finalOutput = {
      success: results.every(r => r.success),
      total: results.length,
      successCount: results.filter(r => r.success).length,
      failCount: results.filter(r => !r.success).length,
      results
    };

    // eslint-disable-next-line no-console
    console.log("\n========== Final Summary ==========");
    // eslint-disable-next-line no-console
    console.log(JSON.stringify(finalOutput, null, 2));
  });
}

async function processSingleItem(client, { targetUrl, platId, merchantIds, targetPubShops, itemNum, total, track, timeoutSec, intervalSec }) {
  // 1. Collect goods
  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [1/6] Collecting...`);
  const collectRes = await client.callTool("collect_goods", {
    originList: [targetUrl],
  });

  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [1/6] Result: ${typeof collectRes === "string" ? collectRes.slice(0, 200) : JSON.stringify(collectRes).slice(0, 200)}`);

  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [1/6] Waiting 5s...`);
  await delay(5000);

  // 2. Query collected list
  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [2/6] Querying collected items...`);

  let eligible = [];
  let itemId = "";
  let targetItem = null;
  let isAlreadyClaimed = false;
  const pageSize = 200;
  const maxPages = 5;

  const sourceItemId = extractProductId(targetUrl)?.id || "";

  const queryEligible = async (claimStatus) => {
    const allItems = [];
    for (let pageNo = 1; pageNo <= maxPages; pageNo++) {
      const listRes = await client.callTool("list_collected_goods", {
        ...(claimStatus === undefined ? {} : { claimStatus }),
        ...(sourceItemId ? { itemId: String(sourceItemId) } : {}),
        pageNo,
        pageSize,
      });
      const items = extractCollectedItems(listRes);
      allItems.push(...items);
      if (!items.length || items.length < pageSize) break;
    }

    const matched = allItems.filter((it) => matchOrigin(it, [targetUrl]));
    const successItems = matched
      .filter((it) => isCollectSuccessItem(it))
      .filter((it) => !isDuplicateCollectedItem(it))
      .filter((it) => !isCollectingItem(it));

    // eslint-disable-next-line no-console
    console.log(
      `[${itemNum}/${total}] [2/6] Locate in collected list: claimStatus=${claimStatus === undefined ? "ALL" : String(claimStatus)}, sourceItemId=${sourceItemId || "(none)"}, total=${allItems.length}, matched=${matched.length}, successEligible=${successItems.length}`
    );

    return successItems;
  };

  eligible = await queryEligible(0);
  if (!eligible.length) eligible = await queryEligible(1);
  if (!eligible.length) eligible = await queryEligible(undefined);

  if (eligible.length > 0) {
    targetItem = eligible.sort((a, b) => {
      const idA = Number(getIdField(a)) || 0;
      const idB = Number(getIdField(b)) || 0;
      return idB - idA;
    })[0];
    itemId = getIdField(targetItem);
    isAlreadyClaimed = isClaimedItem(targetItem);
  }

  if (!eligible.length || !itemId) {
    throw new Error("No eligible items found");
  }

  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [2/6] Found: itemId=${itemId}${isAlreadyClaimed ? " (exists, will re-claim)" : ""}`);

  // 3. Claim goods (claim can be repeated)
  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [3/6] Claiming...`);
  await client.callTool("claim_goods", {
    itemIds: [itemId],
    plats: [{ platId, merchantIds }],
  });

  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [3/6] Claimed, waiting 5s...`);
  await delay(5000);

  // 4. Query drafts
  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [4/6] Querying drafts...`);
  const draftRes = await client.callTool("list_temu_drafts", {
    shopId: String(merchantIds[0]),
    status: "UNPUBLISH",
    pageNo: 1,
    pageSize: 20,
  });

  const draftData = tryParseJson(draftRes);
  const draftList = draftData?.data?.list ?? draftData?.data?.records ?? draftData?.list ?? draftData?.records ?? [];

  const sortedDrafts = draftList.sort((a, b) => {
    const timeA = a?.claimDate || a?.claimTime || "";
    const timeB = b?.claimDate || b?.claimTime || "";
    return String(timeB).localeCompare(String(timeA));
  });

  const targetProductId = extractProductId(targetUrl);
  const matchedDraft = sortedDrafts.find((d) => {
    const draftUrl = getStringField(d, ["originUrl", "fromUrl", "oriUrl"]);
    const draftProductId = extractProductId(draftUrl);
    return draftProductId && targetProductId &&
           draftProductId.platform === targetProductId.platform &&
           draftProductId.id === targetProductId.id;
  });

  if (!matchedDraft) {
    throw new Error("No matching draft found");
  }

  const draftItemId = matchedDraft?.id ?? matchedDraft?.itemId ?? matchedDraft?.item_id;
  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [4/6] Found draft: ${draftItemId}`);

  // 5. Publish
  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [5/6] Publishing...`);
  const publishRes = await client.callTool("publish_temu", {
    itemIds: [String(draftItemId)],
    pubShops: targetPubShops.map(String),
    uploadDetail: true,
  });

  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] [5/6] Published, tracking...`);

  if (!track) {
    return {
      success: true,
      originUrl: targetUrl,
      itemId: String(draftItemId),
      title: targetItem?.title || matchedDraft?.title || "",
      status: "PUBLISHING",
      temuProductId: null,
      failReason: null
    };
  }

  // 6. Track result
  const trackRes = await waitForPublishResult(client, {
    ids: [Number(draftItemId)],
    timeoutMs: Number.isFinite(timeoutSec) ? timeoutSec * 1000 : 180000,
    intervalMs: Number.isFinite(intervalSec) ? intervalSec * 1000 : 3000,
  });

  // Query fail reason if failed - use reason field from publish record
  let failReason = trackRes.record?.reason || trackRes.errorMessage || null;

  // eslint-disable-next-line no-console
  console.log(`[${itemNum}/${total}] Done: status=${trackRes.status}`);

  return {
    success: trackRes.ok,
    originUrl: targetUrl,
    itemId: String(draftItemId),
    title: targetItem?.title || matchedDraft?.title || "",
    status: trackRes.status,
    temuProductId: trackRes.record?.productId || null,
    failReason: failReason
  };
}

async function cmdPublishAndTrack(flags) {
  const itemIds = csvToList(flags.itemIds);
  const pubShops = csvToList(flags.pubShops).map((x) => Number(x));
  const timeoutSec = flags.timeoutSec == null ? 180 : Number(flags.timeoutSec);
  const intervalSec = flags.intervalSec == null ? 3 : Number(flags.intervalSec);

  if (!itemIds.length) {
    // eslint-disable-next-line no-console
    console.error("publish_and_track: --itemIds cannot be empty");
    usage(2);
  }
  await withClient(async (client) => {
    // eslint-disable-next-line no-console
    console.error(`[1/2] Calling publish_temu (itemIds=${itemIds.join(",")})...`);
    const publishRes = await client.callTool("publish_temu", {
      itemIds,
      ...(pubShops.length ? { pubShops: pubShops.map(String) } : {}),
      uploadDetail: true,
    });

    // eslint-disable-next-line no-console
    console.error("[1/2] publish_temu called. Tracking publish result...");

    const trackRes = await waitForPublishResult(client, {
      ids: itemIds.map((x) => Number(x)).filter((x) => Number.isFinite(x)),
      timeoutMs: Number.isFinite(timeoutSec) ? timeoutSec * 1000 : 180000,
      intervalMs: Number.isFinite(intervalSec) ? intervalSec * 1000 : 3000,
    });

    if (trackRes.ok) {
      // eslint-disable-next-line no-console
      console.error(`[DONE] 发布成功 (status=${trackRes.status})`);
      // eslint-disable-next-line no-console
      console.log(JSON.stringify({ publishStatus: trackRes.status, record: trackRes.record, publishCall: publishRes }, null, 2));
      return;
    }

    // eslint-disable-next-line no-console
    console.error(`[DONE] 发布失败/未完成 (status=${trackRes.status})`);
    // eslint-disable-next-line no-console
    console.error(`错误信息：${trackRes.errorMessage || "(上游未返回明确错误信息)"}`);
    // eslint-disable-next-line no-console
    console.error("建议：到【甩手店长】后台对失败商品批量完善/修正信息后，再重新发布。");
    // eslint-disable-next-line no-console
    console.log(JSON.stringify({ publishStatus: trackRes.status, record: trackRes.record, publishCall: publishRes }, null, 2));
    process.exit(trackRes.status === "TIMEOUT" ? 5 : 6);
  });
}

async function main() {
  const argv = process.argv.slice(2);
  const cmd = argv[0];
  if (!cmd) usage(0);

  if (cmd === "tools") return await cmdTools();
  if (cmd === "call") {
    const toolName = argv[1];
    const jsonArgs = argv[2] ?? "{}";
    if (!toolName) usage(2);
    return await cmdCall(toolName, jsonArgs);
  }

  const { flags } = parseFlags(argv.slice(1));
  if (cmd === "login_shuashou") return await cmdLogin(flags);
  if (cmd === "list_shops") return await cmdListShops(flags);
  if (cmd === "collect_goods") return await cmdCollectGoods(flags);
  if (cmd === "list_collected_goods") return await cmdListCollectedGoods(flags);
  if (cmd === "claim_goods") return await cmdClaimGoods(flags);
  if (cmd === "collect_and_publish") return await cmdCollectAndPublish(flags);
  if (cmd === "publish_and_track") return await cmdPublishAndTrack(flags);

  usage(2);
}

main().catch((e) => {
  // eslint-disable-next-line no-console
  console.error(e);
  process.exit(1);
});

