"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const index_js_1 = require("@modelcontextprotocol/sdk/server/index.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const types_js_1 = require("@modelcontextprotocol/sdk/types.js");
const os = __importStar(require("os"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const crypto = __importStar(require("crypto"));
const child_process_1 = require("child_process");
const token_breaker_js_1 = require("./token_breaker.js");
const TOKEN = process.env.STOCKTODAY_TOKEN || "";
const BASE_URL = process.env.STOCKTODAY_URL || "https://tushare.citydata.club/";
const CURRENT_VERSION = "1.3.11";
// 备用服务器地址
const BACKUP_URL1 = process.env.STOCKTODAY_BACKUP_URL1 || "http://111.229.164.2:8083/";
const BACKUP_URL2 = process.env.STOCKTODAY_BACKUP_URL2 || "http://124.223.112.152:6331/";
const BACKUP_URL3 = process.env.STOCKTODAY_BACKUP_URL3 || "http://110.42.211.9:9900/";
// === /TOKEN 端点持久化缓存 ===
// 设计目标:
//   1. 首次查询: 调 /TOKEN, 结果存到 ~/.stocktoday-skill/token-cache.json
//   2. 后续查询: 直接读本地文件, 0 网络调用
//   3. 新 token: 调一次 /TOKEN 重新写文件
//   4. 同一进程内存也缓存, 避免每次读盘
// 文件位置: <homedir>/.stocktoday-skill/token-cache.json
//   - 用 sha256(token)[:16] 当 key, 不存明文 token
//   - 多 token 都能缓存 (用户换 token 不丢旧的)
// 默认 TTL: 24h (token 续费/降级一般不会 1 天内变)
const TOKEN_CACHE_DIR = process.env.STOCKTODAY_TOKEN_CACHE_DIR || path.join(os.homedir(), ".stocktoday-skill");
const TOKEN_CACHE_FILE = path.join(TOKEN_CACHE_DIR, "token-cache.json");
const PERSIST_TTL_MS = parseInt(process.env.STOCKTODAY_TOKEN_PERSIST_TTL_MS || "86400000", 10); // 24h
const TOKEN_RATELIMIT_PER_MIN = parseInt(process.env.STOCKTODAY_TOKEN_RATELIMIT || "10", 10);
function tokenHash(t) {
    return crypto.createHash("sha256").update(t).digest("hex").slice(0, 16);
}
function loadTokenCache() {
    try {
        if (fs.existsSync(TOKEN_CACHE_FILE)) {
            return JSON.parse(fs.readFileSync(TOKEN_CACHE_FILE, "utf-8"));
        }
    }
    catch (e) {
        console.error("[token_cache] load failed:", e);
    }
    return {};
}
function saveTokenCache(cache) {
    try {
        fs.mkdirSync(TOKEN_CACHE_DIR, { recursive: true, mode: 0o700 });
        // 写盘前去掉明文 token 字段 — 缓存 key 已经是 sha256, 不需要明文
        const safe = {};
        for (const [k, v] of Object.entries(cache)) {
            safe[k] = {
                ...v,
                data: stripTokenFromResponse(v.data),
            };
        }
        fs.writeFileSync(TOKEN_CACHE_FILE, JSON.stringify(safe, null, 2), { encoding: "utf-8", mode: 0o600 });
    }
    catch (e) {
        console.error("[token_cache] save failed:", e);
    }
}
// 从 /TOKEN 响应里删掉明文 token 字段 (缓存 key 已经是 hash, 没必要再存明文)
function stripTokenFromResponse(data) {
    if (!data || typeof data !== "object")
        return data;
    if (data.data && typeof data.data === "object" && "token" in data.data) {
        const { token, ...rest } = data.data;
        return { ...data, data: rest };
    }
    return data;
}
// 进程级内存缓存 (避免每次读盘)
const memTokenCache = loadTokenCache();
const tokenRateState = new Map();
function tokenRateAllow(key) {
    const now = Date.now();
    let s = tokenRateState.get(key);
    if (!s) {
        s = { tokens: TOKEN_RATELIMIT_PER_MIN, lastRefill: now };
        tokenRateState.set(key, s);
    }
    const elapsed = (now - s.lastRefill) / 1000;
    const refill = (TOKEN_RATELIMIT_PER_MIN / 60) * elapsed;
    s.tokens = Math.min(TOKEN_RATELIMIT_PER_MIN, s.tokens + refill);
    s.lastRefill = now;
    if (s.tokens < 1)
        return false;
    s.tokens -= 1;
    return true;
}
// === Token 过期提醒 (LLM 友好) ===
// 规则: 剩余 ≤ 7 天才提醒; 一天最多提醒 1 次 (持久化 lastWarningDate, 跨进程不重发)
// 提醒内容插入到 tools/call 响应的 content[0] (system message), LLM 自然看到
let tokenStatus = null;
// === 版本升级检查 (ClawHub CLI) ===
// 启动 2s 后调 `npx clawhub info stocktoday-skill` 拿线上最新版本
// 落后时在 tools/call 响应前插 system message
// 每 24h 检查一次, 避免过度扰动 ClawHub
let updateNotice = null;
function parseVersion(v) {
    const m = v.match(/(\d+)\.(\d+)\.(\d+)/);
    return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null;
}
function cmpVersion(a, b) {
    for (let i = 0; i < 3; i++) {
        if (a[i] !== b[i])
            return a[i] - b[i];
    }
    return 0;
}
async function checkClawhubLatest() {
    return new Promise((resolve) => {
        // Windows 上 npx 是 .cmd, 需要 shell:true 避免 EINVAL
        const isWin = process.platform === "win32";
        const cmd = isWin ? "npx.cmd" : "npx";
        const opts = { timeout: 12000, shell: isWin };
        (0, child_process_1.execFile)(cmd, ["clawhub", "info", "stocktoday-skill"], opts, (err, stdout, stderr) => {
            if (err) {
                resolve(null);
                return;
            }
            const out = String(stdout || "") + String(stderr || "");
            const m = out.match(/(?:version|latest|Version|Latest)\s*[:：]?\s*v?(\d+\.\d+\.\d+)/);
            if (m) {
                resolve(m[1]);
                return;
            }
            const m2 = out.match(/(\d+\.\d+\.\d+)/);
            resolve(m2 ? m2[1] : null);
        });
    });
}
async function refreshUpdateNotice() {
    const latest = await checkClawhubLatest();
    if (!latest)
        return;
    const cur = parseVersion(CURRENT_VERSION);
    const lat = parseVersion(latest);
    if (!cur || !lat)
        return;
    if (cmpVersion(lat, cur) > 0) {
        updateNotice = `🆙 新版本可用: v${latest} (当前 v${CURRENT_VERSION}). 请用 \`npx clawhub publish stocktoday-skill\` 升级`;
        console.error(`[update] 新版本 v${latest} 可用, 当前 v${CURRENT_VERSION}`);
    }
    else {
        updateNotice = null;
    }
}
function todayStr() {
    return new Date().toISOString().slice(0, 10); // YYYY-MM-DD UTC
}
function buildWarnMsg(daysLeft) {
    if (daysLeft === "永久")
        return null;
    if (daysLeft === "已过期")
        return "⚠️ Token 已过期! 请立即续费, 否则所有接口将不可用";
    if (typeof daysLeft === "number") {
        if (daysLeft <= 0)
            return "⚠️ Token 已过期! 请立即续费";
        if (daysLeft <= 7)
            return `🔴 Token 即将过期: 还有 ${daysLeft} 天. 请及时续费`;
    }
    return null;
}
async function refreshTokenStatus() {
    if (!TOKEN)
        return;
    const data = await callAPI("/TOKEN", { token: TOKEN });
    if (data?.code !== 0 || !data?.data?.summary)
        return;
    const summary = data.data.summary;
    const daysLeft = summary.daysUntilExpire;
    const potentialMsg = buildWarnMsg(daysLeft);
    const today = todayStr();
    const key = tokenHash(TOKEN);
    const mem = memTokenCache[key];
    const lastWarn = mem?.lastWarningDate;
    // 只在 "应该提醒 AND 今天没提醒过" 时才真正提醒
    const shouldShow = potentialMsg !== null && lastWarn !== today;
    tokenStatus = {
        daysLeft,
        msg: shouldShow ? potentialMsg : null,
        lastCheck: Date.now(),
    };
    if (shouldShow) {
        memTokenCache[key] = { data: data.data, cachedAt: Date.now(), lastWarningDate: today };
        saveTokenCache(memTokenCache);
        console.error(`[token_warn] ${potentialMsg}`);
    }
}
if (!TOKEN) {
    console.error("⚠️ 启动失败: 必须设置环境变量 STOCKTODAY_TOKEN (或在 .mcp.json 的 env 块里)");
    process.exit(1);
}
const server = new index_js_1.Server({ name: "stocktoday-skill", version: "1.3.11" }, { capabilities: { tools: {} } });
// Structured tool schemas (type/required/enum/pattern/default) from INTERFACE.md
const tool_schemas_js_1 = require("./tool_schemas.js");
// 透明限流器 (用户无感, 后端友好, 错误静默)
const rate_limit_js_1 = require("./rate_limit.js");
// 全局限流实例 — 60/min/token, 5 并发, 3 次重试
const rateLimiter = new rate_limit_js_1.RateLimiter();
// 接口权限分类 (从 gateway.py 同步, 单一 source of truth)
const api_permissions_js_1 = require("./api_permissions.js");
// === /TOKEN 响应 enrich (LLM 友好) ===
// 后端返的原始响应: { code, msg, data: { expireDate, permission, plugins, regisDate, token } }
// enrich 后多一个 data.summary: { daysUntilExpire, permissionLabel, isActive, pluginList, pluginCount }
// 这样 LLM 不用解析 GMT 字符串 / JSON 数组, 直接用 summary 字段
const PERMISSION_LABELS = {
    V0: "无权限", V1: "基础版", V2: "高级版", V3: "专业版", V4: "旗舰版",
};
function enrichTokenInfo(raw) {
    if (!raw || raw.code !== 0 || !raw.data)
        return raw;
    const d = raw.data;
    // 1. 解析到期日 + 算剩余天数
    let daysUntilExpire = "永久";
    let expireParsed = null;
    if (d.expireDate) {
        const t = Date.parse(d.expireDate); // 自动识别 GMT / ISO / YYYYMMDD
        if (!isNaN(t)) {
            const days = Math.floor((t - Date.now()) / 86400000);
            daysUntilExpire = days >= 0 ? days : "已过期";
            expireParsed = new Date(t).toISOString().slice(0, 19).replace("T", " ");
        }
    }
    // 2. 权限等级标签
    const permissionLabel = PERMISSION_LABELS[d.permission] || d.permission || "未知";
    // 3. 解析 plugins (后端是 JSON 字符串)
    let pluginList = [];
    try {
        if (typeof d.plugins === "string")
            pluginList = JSON.parse(d.plugins);
        else if (Array.isArray(d.plugins))
            pluginList = d.plugins;
    }
    catch { }
    // 4. 计算可用 API 分类 (基于 gateway.py 的 check_api_permission)
    const apiAccess = (0, api_permissions_js_1.classifyUserAccess)(d.permission, pluginList);
    return {
        ...raw,
        data: {
            ...d,
            summary: {
                daysUntilExpire,
                expireParsed,
                permissionLabel,
                isActive: daysUntilExpire === "永久" || (typeof daysUntilExpire === "number" && daysUntilExpire > 0),
                pluginList,
                pluginCount: pluginList.length,
                apiAccess, // 关键: 用户的 API 权限分类
            },
        },
    };
}
async function fetchOne(url, endpoint, formData) {
    try {
        const res = await fetch(`${url}${endpoint}`, {
            method: "POST",
            body: formData,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Client-Type": "StockToday-skill",
                "X-Client-Version": "1.3.11"
            },
            signal: AbortSignal.timeout(30000) // 30秒超时
        });
        const raw = await res.text();
        let data;
        try {
            data = JSON.parse(raw);
        }
        catch {
            data = raw;
        }
        return { status: res.status, data, raw };
    }
    catch (e) {
        return { status: 0, data: null, raw: e?.message || String(e) };
    }
}
async function callAPI(endpoint, params = {}, token = TOKEN) {
    // === /TOKEN 端点: 持久化文件缓存 + 内存缓存 + 严限流 ===
    // 流程: 内存命中 → 0 延迟; 文件命中 → 1ms 读盘; 都未中且 10/min 限流允许 → 调 API
    // force_refresh=true: 跳过缓存 (续费/降级后立即生效), 但仍受 10/min 限流
    if (endpoint === '/TOKEN') {
        const key = tokenHash(token);
        const now = Date.now();
        const force = params.force_refresh === true || params.force_refresh === "true";
        const mem = memTokenCache[key];
        if (!force && mem && (now - mem.cachedAt) < PERSIST_TTL_MS) {
            return enrichTokenInfo(mem.data); // enrich 每次重新算天数
        }
        if (!tokenRateAllow(key)) {
            console.error(`[token_info] rate limited for ${key}…`);
            return { code: 1, msg: 'TOKEN查询过于频繁, 请稍后再试', data: null };
        }
    }
    const formData = new URLSearchParams();
    formData.append("TOKEN", token);
    for (const [k, v] of Object.entries(params)) {
        // force_refresh 是 skill 内部控制参数, 不传给后端
        if (k === "force_refresh")
            continue;
        if (v !== undefined && v !== "")
            formData.append(k, String(v));
    }
    // 服务器列表：主站 + 备用站 (逐个尝试直到成功)
    const urls = [BASE_URL, BACKUP_URL1, BACKUP_URL2, BACKUP_URL3];
    // 用限流器包一层: 自动重试 + 静默失败
    // bumpMinuteCount 在 execute 内部自动调 (stats.totalCalls 累加)
    const result = await rateLimiter.execute(token, async () => {
        for (const url of urls) {
            const res = await fetchOne(url, endpoint, formData);
            if (res.status === 200)
                return res;
            // 200 之外的: 记最后错误, 继续尝试下一站
            // 如果是 429/5xx 则 rate limiter 会触发重试 (整轮重试)
            if (res.status === 429 || (res.status >= 500 && res.status < 600)) {
                return res; // 让 rate limiter 重试整轮
            }
            // 4xx (非 429) 直接返, 不重试
            return res;
        }
        return { status: 0, data: null, raw: "no urls" };
    });
    if (!result.ok) {
        // 静默失败 — 返 [], 不让 LLM 看到错误
        return [];
    }
    // === /TOKEN 端点: 缓存原始响应 (内存 + 磁盘双写), 返前 enrich ===
    if (endpoint === '/TOKEN' && result.data?.code === 0) {
        const key = tokenHash(token);
        const entry = { data: result.data, cachedAt: Date.now() };
        memTokenCache[key] = entry;
        saveTokenCache(memTokenCache); // 写盘, 下次冷启动也能用
        console.error(`[token_info] cached for ${key}…`);
        return enrichTokenInfo(result.data);
    }
    return result.data;
}
// Build the params dict from structured TOOLS for backward-compat
// (used by the old tools[] array — no longer needed but kept for any external refs)
const _legacyParams = {};
for (const t of tool_schemas_js_1.TOOLS) {
    const p = {};
    for (const param of t.params) {
        p[param.name] = param.description;
    }
    _legacyParams[t.name] = p;
}
// All tools - v1.3.0 完整版 (基于ST_CLIENT.py 245 个接口 + 结构化 JSON Schema)
const tools = [
    // ===== 1. 股票-基础数据 =====
    { name: "stock_basic", desc: "股票基本信息", params: { exchange: "交易所", list_status: "上市状态", ts_code: "股票代码", market: "市场", fields: "返回字段" } },
    { name: "stk_premarket", desc: "新股上市", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "trade_cal", desc: "交易日历", params: { exchange: "交易所", start_date: "开始日期", end_date: "结束日期" } },
    { name: "stock_st", desc: "ST股票列表", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "namechange", desc: "股票名称变更", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "stock_company", desc: "上市公司信息", params: { ts_code: "股票代码", exchange: "交易所" } },
    { name: "stk_managers", desc: "公司管理层", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", ann_date: "公告日期" } },
    { name: "stk_rewards", desc: "高管薪酬", params: { ts_code: "股票代码" } },
    { name: "new_share", desc: "新股发行 (必传 start_date + end_date 范围, 否则后端 HTTP 400)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "bak_basic", desc: "备用基础数据", params: { exchange: "交易所", ts_code: "股票代码" } },
    { name: "stk_account", desc: "股票账户", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "stk_account_old", desc: "股票账户(旧)", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "stk_ah_comparison", desc: "AH股对比", params: { trade_date: "交易日期" } },
    { name: "stock_hsgt", desc: "沪深港通股票列表", params: { is_hs: "是否沪深港通(N/O)" } },
    { name: "bse_mapping", desc: "北交所新旧代码对照", params: { ts_code: "股票代码" } },
    // ===== 2. 股票-行情数据 =====
    { name: "daily", desc: "股票日线 (A 股/ETF, 指数请用 index_daily — 传指数代码会自动转发). 至少传 ts_code (1只) 或 trade_date (单日, 全市场) 或 start_date+end_date (范围)", params: { ts_code: "股票代码 (A 股 600519.SH / ETF 510300.SH 等, 指数 000001.SH 会自动转 index_daily)", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "weekly", desc: "股票周线 (指数请用 index_weekly — 传指数代码会自动转发). 至少传 ts_code 或 trade_date 或 start_date+end_date", params: { ts_code: "股票代码 (A 股/ETF, 指数用 index_weekly)", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "monthly", desc: "股票月线 (指数请用 index_monthly — 传指数代码会自动转发). 至少传 ts_code 或 trade_date 或 start_date+end_date", params: { ts_code: "股票代码 (A 股/ETF, 指数用 index_monthly)", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "stk_weekly_monthly", desc: "周月线行情. StockToday 后端必传 ts_code + start_date + end_date (高频首选, ts_code 不能少, freq 走默认)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "stk_week_month_adj", desc: "周月线复权行情", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "pro_bar", desc: "股票复权行情 (A 股/ETF, 指数请用 index_daily)", params: { ts_code: "股票代码 (A 股/ETF, 指数用 index_daily)", start_date: "开始日期", end_date: "结束日期", asset: "资产", adj: "复权", freq: "频率", ma: "均线", factors: "因子", adjfactor: "复权因子" } },
    { name: "adj_factor", desc: "股票复权因子 (A 股/ETF, 指数无此接口)", params: { ts_code: "股票代码 (A 股/ETF, 指数无此接口)", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "daily_basic", desc: "每日指标", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "stk_limit", desc: "涨跌停价格. ts_code (1只) 或 trade_date (全市场) 二选一 (StockToday 后端要求)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "suspend_d", desc: "停复牌. StockToday 后端必传 ts_code + start_date + end_date 范围 (Tushare 官方都标 N, 但 StockToday 后端要求)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", suspend_type: "类型" } },
    { name: "hsgt_top10", desc: "沪深股通前十", params: { trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", market_type: "市场类型" } },
    { name: "ggt_top10", desc: "广港通前十", params: { trade_date: "交易日期", ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "ggt_daily", desc: "广港通每日", params: { trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "ggt_monthly", desc: "广港通每月", params: { trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "bak_daily", desc: "备用每日行情", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    // ===== 3. 股票-财务数据 =====
    { name: "income", desc: "利润表 (建议传 period 取最新单期, 不传会返回 100+ 条历史季报)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "balancesheet", desc: "资产负债表 (建议传 period 取最新单期, 不传会返回 100+ 条历史季报)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "cashflow", desc: "现金流量表 (建议传 period 取最新单期, 不传会返回 100+ 条历史季报)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "forecast", desc: "业绩预告. ts_code 或 ann_date 二选一 (StockToday 后端要求; Tushare 官方都标 N)", params: { ann_date: "公告日期", fields: "返回字段" } },
    { name: "express", desc: "业绩快报. ts_code 或 ann_date 二选一 (StockToday 后端要求; Tushare 官方都标 N)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "dividend", desc: "分红送股", params: { ts_code: "股票代码", fields: "返回字段" } },
    { name: "income_vip", desc: "VIP利润表", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "balancesheet_vip", desc: "VIP资产负债表", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "cashflow_vip", desc: "VIP现金流量表", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "fina_indicator_vip", desc: "VIP财务指标", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "express_vip", desc: "VIP业绩快报", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "forecast_vip", desc: "VIP业绩预告", params: { ann_date: "公告日期", fields: "返回字段" } },
    { name: "fina_mainbz_vip", desc: "VIP主营业务构成", params: { ts_code: "股票代码", type: "类型" } },
    { name: "fina_indicator", desc: "财务指标 (建议传 period 取最新单期, 不传会返回 50+ 条历史季报)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "fina_audit", desc: "财务审计 (建议传 period 取最新单期, 不传会返回多条历史)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "fina_mainbz", desc: "主营业务 (建议传 period 取最新单期, 不传会返回多条历史)", params: { ts_code: "股票代码", type: "类型" } },
    { name: "disclosure_date", desc: "财报披露日期 (计划 vs 实际). StockToday 后端必传 ts_code + end_date (Tushare 官方都标 N)", params: { end_date: "结束日期" } },
    // ===== 4. 股票-参考数据 =====
    { name: "top10_holders", desc: "十大股东 (建议传 period 取最新期, 不传会返回多期历史)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "top10_floatholders", desc: "十大流通股东 (建议传 period 取最新期, 不传会返回多期历史)", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "pledge_stat", desc: "股权质押统计", params: { ts_code: "股票代码" } },
    { name: "pledge_detail", desc: "股权质押明细", params: { ts_code: "股票代码" } },
    { name: "repurchase", desc: "股份回购", params: { ann_date: "公告日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "share_float", desc: "流通股本", params: { ann_date: "公告日期" } },
    { name: "block_trade", desc: "大宗交易", params: { trade_date: "交易日期" } },
    { name: "stk_holdernumber", desc: "股东户数", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "stk_holdertrade", desc: "股东增减持", params: { ts_code: "股票代码", ann_date: "公告日期", trade_type: "交易类型" } },
    // ===== 5. 股票-特色数据 =====
    { name: "report_rc", desc: "研报", params: { ts_code: "股票代码", report_date: "报告日期" } },
    { name: "cyq_perf", desc: "筹码活跃度", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "cyq_chips", desc: "筹码分布", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "stk_factor_pro", desc: "200+ 因子库 (动量/价值/质量/技术). ts_code (1只) 或 trade_date (全市场) 二选一 (StockToday 后端要求)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "ccass_hold", desc: "中央结算持股", params: { ts_code: "股票代码" } },
    { name: "ccass_hold_detail", desc: "中央结算持股明细", params: { ts_code: "股票代码", trade_date: "交易日期", fields: "返回字段" } },
    { name: "hk_hold", desc: "港股持股", params: { ts_code: "股票代码", exchange: "交易所" } },
    { name: "stk_auction_o", desc: "集合竞价(开盘)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "stk_auction_c", desc: "盘后定价", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "stk_auction", desc: "股票集合竞价", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "stk_nineturn", desc: "九转序列", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "stk_surv", desc: "舆情监控", params: { ts_code: "股票代码", trade_date: "交易日期", fields: "返回字段" } },
    { name: "broker_recommend", desc: "券商研报推荐", params: { month: "月份" } },
    { name: "anns_d", desc: "上市公司公告", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "cctv_news", desc: "新闻联播文字稿", params: { date: "日期", start_date: "开始日期", end_date: "结束日期" } },
    // ths_news removed (backend 接口不存在)
    { name: "npr", desc: "国家政策库", params: { start_date: "开始日期", end_date: "结束日期", search: "关键词" } },
    { name: "research_report", desc: "券商研究报告", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    // ===== 6. 股票-两融 =====
    { name: "margin", desc: "融资融券", params: { trade_date: "交易日期" } },
    { name: "margin_detail", desc: "融资融券明细", params: { trade_date: "交易日期" } },
    { name: "margin_secs", desc: "融资融券证券", params: { trade_date: "交易日期", exchange: "交易所" } },
    { name: "slb_sec", desc: "融券余量", params: { trade_date: "交易日期" } },
    { name: "slb_len", desc: "融资期限", params: { trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "slb_sec_detail", desc: "融券余量明细", params: { trade_date: "交易日期" } },
    { name: "slb_len_mm", desc: "融资期限明细", params: { trade_date: "交易日期" } },
    // ===== 7. 股票-资金流向 =====
    { name: "moneyflow", desc: "资金流向. ts_code (1只) 或 trade_date (全市场) 二选一 (StockToday 后端要求)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "moneyflow_ths", desc: "资金流向(同花顺). ts_code (1只) 或 trade_date (全市场) 二选一 (StockToday 后端要求)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "moneyflow_cnt_ths", desc: "资金流向分类(同花顺)", params: { trade_date: "交易日期", ts_code: "股票代码" } },
    { name: "moneyflow_dc", desc: "资金流向(东方财富)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "moneyflow_ind_ths", desc: "行业资金流向(同花顺)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "moneyflow_ind_dc", desc: "行业资金流向(东方财富)", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "moneyflow_mkt_dc", desc: "市场资金流向(东方财富)", params: { trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "moneyflow_hsgt", desc: "沪深港通资金流向", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    // ===== 8. 股票-打板专题 =====
    { name: "kpl_concept", desc: "开盘啦概念", params: { trade_date: "交易日期" } },
    { name: "kpl_concept_cons", desc: "开盘啦概念成分", params: { trade_date: "交易日期" } },
    { name: "kpl_list", desc: "开盘啦列表", params: { trade_date: "交易日期", tag: "标签", fields: "返回字段" } },
    { name: "top_list", desc: "龙虎榜上榜", params: { trade_date: "交易日期" } },
    { name: "top_inst", desc: "龙虎榜机构", params: { trade_date: "交易日期" } },
    { name: "limit_list_ths", desc: "涨停列表(同花顺)", params: { trade_date: "交易日期", limit_type: "涨停类型", fields: "返回字段" } },
    { name: "limit_list_d", desc: "涨跌停明细", params: { trade_date: "交易日期", limit_type: "涨跌停类型", fields: "返回字段" } },
    { name: "limit_step", desc: "涨停阶梯", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", nums: "数量" } },
    { name: "limit_cpt_list", desc: "涨停股票池", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "ths_index", desc: "同花顺指数", params: { ts_code: "指数代码", exchange: "市场类型(A-a股 HK-港股 US-美股)", type: "指数类型(N-概念 I-行业 R-地域 S-特色 ST-风格 TH-主题 BB-宽基)" } },
    { name: "ths_member", desc: "同花顺成分股", params: { ts_code: "指数代码" } },
    { name: "dc_index", desc: "东财指数", params: { ts_code: "指数代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "dc_member", desc: "东财成分股", params: { ts_code: "指数代码", trade_date: "交易日期" } },
    // dc_concept / dc_concept_cons removed (backend 接口不存在)
    // hm_list removed (参数无作用, 直接返全市场, 不污染 schema)
    { name: "hm_detail", desc: "活跃股明细", params: { trade_date: "交易日期" } },
    { name: "ths_hot", desc: "同花顺热点", params: { market: "市场", trade_date: "交易日期", fields: "返回字段" } },
    { name: "dc_hot", desc: "东方财富热点", params: { market: "市场", hot_type: "热点类型", trade_date: "交易日期", fields: "返回字段" } },
    // ===== 9. 指数 =====
    { name: "index_basic", desc: "指数基本信息", params: { market: "市场" } },
    { name: "index_daily", desc: "指数日线 (上证 000001.SH / 沪深300 000300.SH / 创业板 399006.SZ, 股票请用 daily)", params: { ts_code: "指数代码 (如 000001.SH 上证 / 000300.SH 沪深300, 股票用 daily)", start_date: "开始日期", end_date: "结束日期" } },
    { name: "index_weekly", desc: "指数周线 (股票请用 weekly)", params: { ts_code: "指数代码 (股票用 weekly)", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "index_monthly", desc: "指数月线 (股票请用 monthly)", params: { ts_code: "指数代码 (股票用 monthly)", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "index_weight", desc: "指数成分", params: { index_code: "指数代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "index_dailybasic", desc: "指数每日指标", params: { trade_date: "交易日期", fields: "返回字段" } },
    { name: "index_classify", desc: "指数分类", params: { level: "级别", src: "来源" } },
    { name: "index_member_all", desc: "指数成分股(全)", params: { l1_code: "一级代码", l2_code: "二级代码", l3_code: "三级代码", ts_code: "股票代码" } },
    { name: "ci_index_member", desc: "中证指数成分", params: { index_code: "指数代码" } },
    { name: "daily_info", desc: "每日信息", params: { trade_date: "交易日期", exchange: "交易所", fields: "返回字段" } },
    { name: "sz_daily_info", desc: "深市每日信息", params: { trade_date: "交易日期", ts_code: "股票代码" } },
    { name: "ths_daily", desc: "同花顺指数日线. ts_code (1个指数) 或 trade_date (全市场) 二选一 (StockToday 后端要求)", params: { ts_code: "指数代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "ci_daily", desc: "中证指数日线", params: { trade_date: "交易日期", fields: "返回字段" } },
    { name: "sw_daily", desc: "申万指数日线", params: { trade_date: "交易日期", fields: "返回字段" } },
    { name: "index_global", desc: "全球指数", params: { ts_code: "指数代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "idx_factor_pro", desc: "指数因子(专业版) (股票请用 stk_factor_pro)", params: { ts_code: "指数代码 (股票用 stk_factor_pro)", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "dc_daily", desc: "东财指数每日", params: { ts_code: "指数代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "tdx_index", desc: "通达信指数", params: { ts_code: "指数代码" } },
    { name: "tdx_daily", desc: "通达信指数日线", params: { ts_code: "指数代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "tdx_member", desc: "通达信板块成分", params: { ts_code: "板块代码" } },
    { name: "gz_index", desc: "国证指数", params: { ts_code: "指数代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "wz_index", desc: "万德指数", params: { ts_code: "指数代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    // ===== 10. 基金 =====
    { name: "fund_basic", desc: "基金基本信息", params: { market: "市场" } },
    { name: "fund_company", desc: "基金公司 (不传参数返全市场, 15279 行, 数据量大慎用)", params: {} },
    { name: "fund_manager", desc: "基金经理", params: { ts_code: "基金代码" } },
    { name: "fund_share", desc: "基金份额", params: { ts_code: "基金代码" } },
    { name: "fund_nav", desc: "基金净值. ts_code 或 nav_date 二选一 (StockToday 后端要求; Tushare 官方都标 N)", params: { ts_code: "基金代码" } },
    { name: "fund_div", desc: "基金分红", params: { ann_date: "公告日期" } },
    { name: "fund_portfolio", desc: "基金持仓 (前 10 大重仓股). ts_code / ann_date / period 至少传一个 (StockToday 后端要求; Tushare 官方都标 N)", params: { ts_code: "基金代码" } },
    { name: "fund_daily", desc: "基金日线", params: { ts_code: "基金代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "fund_adj", desc: "基金复权", params: { ts_code: "基金代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "fund_factor_pro", desc: "基金因子(专业版)", params: { ts_code: "基金代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "fund_sales_ratio", desc: "基金销售比例", params: { ts_code: "基金代码" } },
    { name: "fund_sales_vol", desc: "基金销售量", params: { ts_code: "基金代码" } },
    { name: "etf_basic", desc: "ETF基本信息", params: { market: "市场" } },
    { name: "etf_index", desc: "ETF关联指数", params: { ts_code: "ETF代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "etf_share_size", desc: "ETF份额 (不传参数返全市场 ETF 份额, 数据量大慎用, 可加 ts_code 过滤)", params: { ts_code: "ETF代码" } },
    { name: "etf_mins", desc: "ETF历史分钟", params: { ts_code: "ETF代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    // ===== 11. 期货 =====
    { name: "fut_basic", desc: "期货基本信息", params: { exchange: "交易所", fut_type: "期货类型", fields: "返回字段" } },
    { name: "fut_daily", desc: "期货日线", params: { ts_code: "期货代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", exchange: "交易所", fields: "返回字段" } },
    { name: "fut_weekly_monthly", desc: "期货周/月线", params: { ts_code: "期货代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率", exchange: "交易所" } },
    { name: "ft_mins", desc: "期货分钟线", params: { ts_code: "期货代码", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    { name: "fut_wsr", desc: "期货持仓", params: { trade_date: "交易日期", symbol: "合约" } },
    { name: "fut_settle", desc: "期货结算", params: { trade_date: "交易日期", exchange: "交易所" } },
    { name: "fut_holding", desc: "期货持仓量 (必传 start_date+end_date 范围, 单日 trade_date 不工作)", params: { trade_date: "交易日期", symbol: "合约", exchange: "交易所" } },
    { name: "fut_mapping", desc: "期货映射", params: { ts_code: "期货代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "fut_weekly_detail", desc: "期货每周详情", params: { prd: "产品", start_week: "开始周", end_week: "结束周", fields: "返回字段" } },
    { name: "ft_limit", desc: "期货涨跌停", params: { trade_date: "交易日期", ts_code: "期货代码", cont: "合约" } },
    { name: "cb_factor_pro", desc: "可转债因子(专业版)", params: { ts_code: "可转债代码", trade_date: "交易日期" } },
    // ===== 12. 现货 =====
    { name: "sge_basic", desc: "现货基本信息", params: { ts_code: "品种代码" } },
    { name: "sge_daily", desc: "现货每日行情", params: { trade_date: "交易日期", prd: "品种", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    // ===== 13. 期权 =====
    { name: "opt_basic", desc: "期权基本信息", params: { exchange: "交易所", fields: "返回字段" } },
    { name: "opt_daily", desc: "期权每日行情", params: { ts_code: "期权代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", exchange: "交易所" } },
    { name: "opt_mins", desc: "期权分钟行情", params: { ts_code: "期权代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    // ===== 14. 可转债 =====
    { name: "cb_basic", desc: "可转债基本信息", params: { fields: "返回字段" } },
    { name: "cb_issue", desc: "可转债发行", params: { ann_date: "公告日期", fields: "返回字段" } },
    { name: "cb_call", desc: "可转债回售", params: { fields: "返回字段" } },
    { name: "cb_rate", desc: "可转债转股溢价率", params: { ts_code: "可转债代码", fields: "返回字段" } },
    { name: "cb_daily", desc: "可转债每日行情", params: { ts_code: "可转债代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "cb_price_chg", desc: "可转债价格变化", params: { ts_code: "可转债代码", fields: "返回字段" } },
    { name: "cb_share", desc: "可转债转股", params: { ts_code: "可转债代码", fields: "返回字段" } },
    // ===== 15. 债券 =====
    { name: "repo_daily", desc: "回购每日行情", params: { trade_date: "交易日期" } },
    { name: "bc_otcqt", desc: "银行间报价", params: { ts_code: "债券代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "bc_bestotcqt", desc: "银行间最优报价", params: { ts_code: "债券代码", start_date: "开始日期", end_date: "结束日期", fields: "返回字段" } },
    { name: "bond_blk", desc: "债券大宗交易", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "bond_blk_detail", desc: "债券大宗交易明细", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "yc_cb", desc: "可转债收益率", params: { trade_date: "交易日期", curve_type: "曲线类型" } },
    // ===== 16. 宏观经济 =====
    { name: "eco_cal", desc: "经济日历", params: { date: "日期", country: "国家", event: "事件", fields: "返回字段" } },
    { name: "shibor", desc: "Shibor利率", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "shibor_quote", desc: "Shibor报价", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "shibor_lpr", desc: "LPR贷款基础利率", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "cn_gdp", desc: "中国GDP", params: { quarter: "季度", start_date: "开始日期", end_date: "结束日期" } },
    { name: "cn_cpi", desc: "中国CPI", params: { month: "月份", start_date: "开始日期", end_date: "结束日期" } },
    { name: "cn_ppi", desc: "中国PPI", params: { month: "月份", start_date: "开始日期", end_date: "结束日期" } },
    { name: "cn_m", desc: "货币供应量(月)", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "cn_pmi", desc: "采购经理指数PMI", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "sf_month", desc: "上海黄金现货月报", params: { start_month: "开始月", end_month: "结束月" } },
    { name: "libor", desc: "Libor利率", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "hibor", desc: "Hibor利率", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_tbr", desc: "美国短期国债利率", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_tycr", desc: "美国国债收益率曲线利率", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_trycr", desc: "美国国债实际收益率曲线利率", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_tltr", desc: "美国国债长期利率", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_trltr", desc: "美国国债实际长期利率平均值", params: { start_date: "开始日期", end_date: "结束日期" } },
    // ===== 17. 外汇 =====
    { name: "fx_obasic", desc: "外汇基本信息", params: { exchange: "交易所", classify: "分类", fields: "返回字段" } },
    { name: "fx_daily", desc: "外汇每日行情", params: { ts_code: "外汇代码", start_date: "开始日期", end_date: "结束日期" } },
    // ===== 18. 港股 =====
    { name: "hk_basic", desc: "港股基本信息", params: { list_status: "上市状态", trade_date: "交易日期" } },
    { name: "hk_tradecal", desc: "港股交易日历", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "hk_daily", desc: "港股每日行情", params: { ts_code: "港股代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "hk_daily_adj", desc: "港股每日行情(复权)", params: { ts_code: "港股代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "hk_mins", desc: "港股分钟线", params: { ts_code: "港股代码", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    { name: "hk_income", desc: "港股利润表", params: { ts_code: "港股代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "hk_balancesheet", desc: "港股资产负债表", params: { ts_code: "港股代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "hk_cashflow", desc: "港股现金流量表", params: { ts_code: "港股代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "hk_adjfactor", desc: "港股复权因子", params: { ts_code: "港股代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "hk_fina_indicator", desc: "港股财务指标", params: { ts_code: "港股代码", start_date: "开始日期", end_date: "结束日期" } },
    // ===== 19. 美股 =====
    { name: "us_basic", desc: "美股基本信息", params: {} },
    { name: "us_tradecal", desc: "美股交易日历", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_daily", desc: "美股每日行情", params: { ts_code: "美股代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_daily_adj", desc: "美股每日行情(复权)", params: { ts_code: "美股代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", exchange: "交易所" } },
    { name: "us_income", desc: "美股利润表", params: { ts_code: "美股代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_balancesheet", desc: "美股资产负债表", params: { ts_code: "美股代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_cashflow", desc: "美股现金流量表", params: { ts_code: "美股代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_adjfactor", desc: "美股复权因子 (必传纯 ticker, 不要带 .US 后缀)", params: { ts_code: "美股代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "us_fina_indicator", desc: "美股财务指标", params: { ts_code: "美股代码", start_date: "开始日期", end_date: "结束日期" } },
    // ===== 20. 资讯 =====
    { name: "news", desc: "资讯", params: { src: "来源", start_date: "开始日期", end_date: "结束日期" } },
    { name: "major_news", desc: "重要资讯", params: { trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期" } },
    // ===== 21. 其他 =====
    { name: "tmt_twincome", desc: "台湾电子产业月营收", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "tmt_twincomedetail", desc: "TMT月营收明细", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "film_record", desc: "电影剧本备案公示", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "teleplay_record", desc: "电视剧备案公示", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "bo_daily", desc: "电影日度票房", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "bo_monthly", desc: "电影月度票房", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "bo_weekly", desc: "电影周度票房", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "bo_cinema", desc: "影院日度票房", params: { start_date: "开始日期", end_date: "结束日期" } },
    { name: "irm_qa_sh", desc: "上证e互动问答", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    { name: "irm_qa_sz", desc: "深证易互动问答", params: { ts_code: "股票代码", start_date: "开始日期", end_date: "结束日期" } },
    // ===== 23. 用户自查 (内部接口 /TOKEN) =====
    { name: "token_info", desc: "查询自己的 TOKEN 有效期/权限/可用插件", params: { token: "要查询的 TOKEN (只能查自己)" } },
    // ===== 22. 实时数据 =====
    // realtime_list removed (后端已废弃, 改用 rt_k)
    // realtime_quote / realtime_tick removed (backend 返回 404)
    { name: "rt_min", desc: "股票实时分钟", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    { name: "rt_etf_min", desc: "ETF实时分钟", params: { ts_code: "ETF代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    { name: "rt_k", desc: "股票实时日线", params: { ts_code: "股票代码", asset: "资产" } },
    { name: "rt_tick", desc: "股票实时Tick(只返回最后一条)", params: { ts_code: "股票代码" } },
    { name: "rt_idx_k", desc: "指数实时日线", params: { ts_code: "指数代码" } },
    { name: "rt_idx_min", desc: "指数实时分钟", params: { ts_code: "指数代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    { name: "rt_idx_tick", desc: "指数实时Tick(只返回最后一条)", params: { ts_code: "指数代码" } },
    { name: "rt_sw_k", desc: "申万指数实时行情 (支持 ts_code 通配符, 例: `8010*.SI`/`801010.SI` 不传返全市场)", params: { ts_code: "指数代码" } },
    { name: "rt_sw_tick", desc: "申万实时Tick(只返回最后一条, 必传 ts_code)", params: { ts_code: "指数代码" } },
    { name: "rt_etf_k", desc: "ETF实时日线", params: { ts_code: "ETF代码" } },
    { name: "rt_etf_tick", desc: "ETF实时Tick(只返回最后一条, 必传 ts_code 例如 510300.SH)", params: { ts_code: "ETF代码" } },
    { name: "rt_fut_min", desc: "期货实时分钟", params: { ts_code: "期货代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    { name: "rt_hk_k", desc: "港股实时日线", params: { ts_code: "港股代码" } },
    { name: "rt_hk_tick", desc: "港股实时Tick(只返回最后一条)", params: { ts_code: "港股代码" } },
    { name: "stk_mins", desc: "股票历史分钟", params: { ts_code: "股票代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
    { name: "idx_mins", desc: "指数历史分钟 (必传 ts_code + freq)", params: { ts_code: "指数代码", trade_date: "交易日期", start_date: "开始日期", end_date: "结束日期", freq: "频率" } },
];
// Build a name → description map from the legacy tools array (clean Chinese from SKILL.md)
const descMap = {};
for (const t of tools) {
    descMap[t.name] = t.desc;
}
// Build a name → structured schema lookup
const schemaMap = {};
for (const t of tool_schemas_js_1.TOOLS) {
    schemaMap[t.name] = t;
}
// Register tools with structured JSON Schema
// Expose ALL 245 tools (union of legacy names + structured schemas)
// so tools without parseable schemas still appear (with empty inputSchema)
server.setRequestHandler(types_js_1.ListToolsRequestSchema, async () => {
    const allNames = new Set([...Object.keys(descMap), ...Object.keys(schemaMap)]);
    const result = [];
    for (const name of allNames) {
        const t = schemaMap[name];
        if (t) {
            const properties = {};
            const required = [];
            for (const p of t.params) {
                const prop = {
                    type: p.type,
                    description: p.description || descMap[name] || name,
                };
                if (p.enum && p.enum.length > 0)
                    prop.enum = p.enum;
                if (p.pattern)
                    prop.pattern = p.pattern;
                if (p.default !== undefined)
                    prop.default = p.default;
                properties[p.name] = prop;
                if (p.required)
                    required.push(p.name);
            }
            result.push({
                name,
                description: descMap[name] || name,
                inputSchema: {
                    type: "object",
                    properties,
                    ...(required.length > 0 ? { required } : {}),
                },
            });
        }
        else {
            // No structured schema — emit empty inputSchema (tool exists in legacy)
            result.push({
                name,
                description: descMap[name] || name,
                inputSchema: { type: "object", properties: {} },
            });
        }
    }
    return { tools: result };
});
// Endpoint mapping
// token_info 走 StockToday 内部端点 /TOKEN (大写, 不符合 1:1 命名映射)
const SPECIAL_ENDPOINTS = {
    token_info: '/TOKEN',
};
const endpointMap = {};
for (const t of tools) {
    endpointMap[t.name] = SPECIAL_ENDPOINTS[t.name] || ("/" + t.name);
}
// === P1c: 错日期格式 / 错 ts_code 友好拦截 (LLM 第一次就明白) ===
// 日期字段含 - 或 : → 返 400 而不是让 LLM 拿到静默空数组
// 简化: 5 个高频按 trade_date 的接口, 校验 trade_date / start_date / end_date
const DATE_FIELDS = new Set(['trade_date', 'start_date', 'end_date', 'ann_date', 'period', 'f_ann_date', 'record_date', 'ex_date', 'imp_ann_date', 'pre_date', 'actual_date', 'float_date', 'pub_date', 'report_date']);
const STRICT_DATE_TOOLS = new Set(['daily', 'pro_bar', 'weekly', 'monthly', 'index_daily', 'index_weekly', 'index_monthly', 'top_list', 'limit_list_d', 'limit_list_ths', 'limit_step', 'adj_factor', 'daily_basic', 'stk_limit', 'suspend_d', 'moneyflow', 'moneyflow_ths', 'moneyflow_dc', 'moneyflow_hsgt', 'moneyflow_mkt_dc', 'hsgt_top10', 'ggt_top10', 'ggt_daily', 'ggt_monthly', 'margin', 'margin_detail', 'stk_holdertrade', 'stk_holdernumber']);
// === 指数代码识别 (供 daily/pro_bar/weekly/monthly 自动转发到 index_* 用) ===
// 上证 (000xxx.SH) / 深证综指 (399xxx.SZ) / 沪深 300/500 (000xxx.SH) / 创业板指 (399006.SZ)
const INDEX_CODE_RE = /^(00\d{4}|399\d{3})\.(SH|SZ)$/;
const INDEX_TOOLS_REDIRECT = {
    daily: '/index_daily',
    weekly: '/index_weekly',
    monthly: '/index_monthly',
    pro_bar: '/index_daily', // pro_bar 没有对应 index_*, 但传指数代码本身就是误用, 转发到 index_daily 取 K 线
    adj_factor: '/index_daily', // 指数没有 adj_factor, 转发也无意义, 但保持一致
};
function validateArgs(name, args) {
    if (!STRICT_DATE_TOOLS.has(name))
        return null;
    for (const [k, v] of Object.entries(args || {})) {
        if (typeof v !== 'string' || !DATE_FIELDS.has(k))
            continue;
        // 日期字段值带 - → 用户/老习惯 2026-06-18, 应是 20260618
        if (/^\d{4}-\d{2}-\d{2}$/.test(v)) {
            return `参数 ${k} 格式错误: 应该是 YYYYMMDD (8 位无横杠), 当前是 "${v}"。例如 "20260618"`;
        }
        // 带 : 的分钟线日期 (如 "2026-06-18 09:30:00"), 错工具
        if (/^\d{4}-\d{2}-\d{2} /.test(v) && !['stk_mins', 'idx_mins', 'ft_mins', 'hk_mins', 'opt_mins', 'etf_mins', 'rt_min', 'rt_idx_min', 'rt_etf_min', 'cb_daily'].includes(name)) {
            return `参数 ${k} 格式错误: 当前是带时间的分钟线格式 "${v}", 但 ${name} 是按日查询, 应是 YYYYMMDD`;
        }
    }
    return null;
}
// === P1b: 休市友好提示 (LLM 拿到空数据不会以为是 skill 坏了) ===
// 5 个高频按 trade_date 的接口, 空数据时调 trade_cal 验是不是休市
const HOLIDAY_CHECK_TOOLS = new Set(['daily', 'pro_bar', 'index_daily', 'top_list', 'limit_list_d', 'limit_list_ths']);
const holidayCache = new Map();
const HOLIDAY_CACHE_TTL_MS = 3600 * 1000;
async function checkHoliday(date, token) {
    if (!/^\d{8}$/.test(date))
        return null;
    const cached = holidayCache.get(date);
    if (cached && Date.now() - cached.cachedAt < HOLIDAY_CACHE_TTL_MS)
        return cached;
    try {
        const res = await callAPI('/trade_cal', { start_date: date, end_date: date }, token);
        const items = res?.data?.items || [];
        const sse = items.find((i) => i.exchange === 'SSE');
        if (sse) {
            const info = { date, isOpen: sse.is_open === 1, pretradeDate: sse.pretrade_date, cachedAt: Date.now() };
            holidayCache.set(date, info);
            return info;
        }
    }
    catch { /* ignore, fallback to original msg */ }
    return null;
}
// === Patch 2 helper: 算当前季度最近一个已发布报告期 (tushare 季度报告期: 03-31/06-30/09-30/12-31) ===
function getLatestReportPeriod() {
    const d = new Date();
    const y = d.getFullYear();
    const m = d.getMonth() + 1; // 1-12
    if (m >= 1 && m <= 3)
        return `${y - 1}1231`; // 1-3 月: 用上年 Q4
    if (m >= 4 && m <= 6)
        return `${y}0331`; // 4-6 月: 用本年 Q1
    if (m >= 7 && m <= 9)
        return `${y}0630`; // 7-9 月: 用本年 Q2
    return `${y}0930`; // 10-12 月: 用本年 Q3
}
// === Patch 4 helper: 日期参数严格 8 位数字校验 (如 trade_date='ABC123' 静默返空修复) ===
function validateDateFormat(args) {
    for (const [k, v] of Object.entries(args || {})) {
        if (typeof v !== 'string' || !DATE_FIELDS.has(k))
            continue;
        // 必须 8 位数字 (YYYYMMDD)
        if (v && !/^\d{8}$/.test(v)) {
            return `参数 ${k} 格式错误: 必须是 8 位数字 (YYYYMMDD), 当前是 "${v}"。例如 "20260618"`;
        }
    }
    return null;
}
// === Patch 6 helper: 必填友好校验 (小白用户 0 调试, 不让返几千万行洪水) ===
function validateRequired(name, args) {
    // 财务接口必须传 ts_code (Patch 2 已经处理不传 period, Patch 6 处理缺 ts_code)
    const FIN_TOOLS = new Set(['income', 'balancesheet', 'cashflow', 'fina_indicator', 'fina_audit', 'fina_mainbz', 'forecast', 'express', 'top10_holders', 'top10_floatholders']);
    if (FIN_TOOLS.has(name) && !args?.ts_code) {
        return `${name} 必须传 ts_code, 例: 600519.SH (贵州茅台)`;
    }
    // sge_basic 必须传 ts_code
    if (name === 'sge_basic' && !args?.ts_code) {
        return `sge_basic 必须传 ts_code, 例: Au99.99.SGE (上海黄金现货)`;
    }
    // daily: ts_code 可选, 但 date 必填 (否则返几千万行全市场全历史)
    if (name === 'daily') {
        const hasDate = !!(args?.trade_date || (args?.start_date && args?.end_date));
        if (!hasDate) {
            return `daily 至少传一个: trade_date (单日, 例 20260618) 或 start_date+end_date (范围, 例 20260601+20260618) 或 ts_code (例 600519.SH)`;
        }
    }
    // pro_bar: 必须传 date (单日 trade_date 或 范围 start_date+end_date)
    if (name === 'pro_bar') {
        const hasDate = !!(args?.trade_date || (args?.start_date && args?.end_date));
        if (!hasDate) {
            return `pro_bar 必须传 trade_date (单日) 或 start_date+end_date (范围), 例: trade_date=20260618`;
        }
    }
    // 历史/实时分钟接口: ts_code + freq 必填
    const HIST_MIN_TOOLS = new Set(['stk_mins', 'idx_mins', 'etf_mins', 'ft_mins', 'hk_mins', 'opt_mins']);
    if (HIST_MIN_TOOLS.has(name)) {
        if (!args?.ts_code)
            return `${name} 必须传 ts_code (例 600519.SH)`;
        if (!args?.freq)
            return `${name} 必须传 freq, 可选: 1min/5min/15min/30min/60min (历史分钟用小写)`;
    }
    const RT_MIN_TOOLS = new Set(['rt_min', 'rt_etf_min', 'rt_idx_min', 'rt_fut_min']);
    if (RT_MIN_TOOLS.has(name)) {
        if (!args?.ts_code)
            return `${name} 必须传 ts_code (例 600519.SH)`;
        if (!args?.freq)
            return `${name} 必须传 freq, 可选: 1MIN/5MIN/15MIN/30MIN/60MIN (实时分钟大写)`;
    }
    return null;
}
function isEmptyData(result) {
    if (!result || result.data === null)
        return true;
    const d = result.data;
    if (Array.isArray(d))
        return d.length === 0;
    if (typeof d === 'object') {
        if (Array.isArray(d.items))
            return d.items.length === 0;
        if (Object.keys(d).length === 0)
            return true;
    }
    return false;
}
async function enrichHolidayHint(name, args, result, token) {
    if (!HOLIDAY_CHECK_TOOLS.has(name))
        return result;
    if (!isEmptyData(result))
        return result;
    // 取查询的日期: trade_date > start_date
    const date = (args && (args.trade_date || args.start_date)) || '';
    if (!date)
        return result;
    const info = await checkHoliday(String(date), token);
    if (info && !info.isOpen) {
        // 改造 result.msg
        const nextDate = info.pretradeDate || '';
        return {
            ...result,
            msg: result.msg
                ? `${result.msg} (提示: ${date} 为非交易日, 上一个交易日是 ${nextDate})`
                : `数据为空, 因为 ${date} 为非交易日, 上一个交易日是 ${nextDate}`
        };
    }
    return result;
}
// Handle calls
server.setRequestHandler(types_js_1.CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    let endpoint = endpointMap[name];
    if (!endpoint) {
        return { content: [{ type: "text", text: JSON.stringify({ error: `Unknown tool: ${name}` }) }] };
    }
    try {
        // === 指数代码误用 daily/weekly/monthly/pro_bar → 自动转发到对应 index_* 接口 ===
        // 小白最常踩: 拿指数代码 (000001.SH) 调 daily, 后端会返空, 体验差
        // 这里直接改 endpoint, LLM 无感
        let redirectMsg = null;
        if (INDEX_TOOLS_REDIRECT[name] && args?.ts_code && INDEX_CODE_RE.test(String(args.ts_code))) {
            const originalName = name;
            endpoint = INDEX_TOOLS_REDIRECT[name];
            redirectMsg = `🔁 自动转发: ${originalName}(ts_code="${args.ts_code}") → ${endpoint} (指数代码请用 index_* 接口)`;
            console.error(`[redirect] ${originalName} → ${endpoint} for ts_code=${args.ts_code}`);
        }
        // === P1c: 错日期格式校验 ===
        const dateErr = validateArgs(name, args || {});
        if (dateErr) {
            return { content: [{ type: "text", text: JSON.stringify({ code: 1, data: null, msg: dateErr }) }] };
        }
        // === Patch 2: 财务接口不传 period/ann_date/start_date → 自动取最近期 (小白友好) ===
        const FIN_TOOLS = new Set(['income', 'balancesheet', 'cashflow', 'fina_indicator', 'fina_audit', 'fina_mainbz']);
        let smartArgs = args || {};
        if (FIN_TOOLS.has(name)) {
            if (!smartArgs.period && !smartArgs.ann_date && !smartArgs.f_ann_date && !smartArgs.start_date) {
                smartArgs = { ...smartArgs, period: getLatestReportPeriod() };
            }
        }
        // === Patch 3: rt_etf_tick 不传 topic → 自动补 HQ_FND_TICK (上海 ETF 必填) ===
        if (name === 'rt_etf_tick' && !smartArgs.topic) {
            smartArgs = { ...smartArgs, topic: 'HQ_FND_TICK' };
        }
        // === Patch 4: 日期参数严格 8 位数字校验 (ABC123 静默返空修复) ===
        const dateStrictErr = validateDateFormat(smartArgs);
        if (dateStrictErr) {
            return { content: [{ type: "text", text: JSON.stringify({ code: 1, data: null, msg: dateStrictErr }) }] };
        }
        // === Patch 6: 必填友好校验 (小白用户 0 调试) ===
        const requiredErr = validateRequired(name, smartArgs);
        if (requiredErr) {
            return { content: [{ type: "text", text: JSON.stringify({ code: 1, data: null, msg: requiredErr }) }] };
        }
        const params = {};
        for (const [k, v] of Object.entries(smartArgs)) {
            if (v !== undefined && v !== "" && v !== null) {
                params[k] = v;
            }
        }
        const token = params.token || TOKEN;
        if (!token) {
            return { content: [{ type: "text", text: JSON.stringify({ error: "请设置 STOCKTODAY_TOKEN 环境变量或传入 token 参数" }) }] };
        }
        delete params.token;
        // === Token Circuit Breaker: 调用前检查 (30s 警告/5min 熔断) ===
        const breakerCheck = token_breaker_js_1.tokenBreaker.check();
        if (breakerCheck.open) {
            return { content: [{ type: "text", text: JSON.stringify({ code: 1, data: null, msg: breakerCheck.message }) }] };
        }
        let result = await callAPI(endpoint, params, token);
        // === Token Circuit Breaker: 检测 auth_error (token 错/过期) ===
        // gateway 返 {code: 401, msg: "TOKEN无效"} 或类似错
        const resultMsg = (typeof result?.msg === 'string' ? result.msg : '') + (typeof result?.data?.msg === 'string' ? result.data.msg : '');
        if (result?.code === 401 || /TOKEN|token.*invalid|token.*无效|auth.*error|401/i.test(resultMsg)) {
            const breakerStatus = token_breaker_js_1.tokenBreaker.recordAuthError();
            // 用熔断器消息替换原始错 (友好提示)
            return { content: [{ type: "text", text: JSON.stringify({ code: 1, data: null, msg: breakerStatus.message || resultMsg }) }] };
        }
        // 调通, 记录成功
        if (result?.code === 0)
            token_breaker_js_1.tokenBreaker.recordSuccess();
        // === P1b: 休市友好提示 ===
        result = await enrichHolidayHint(name, args, result, token);
        let content = [{ type: "text", text: JSON.stringify(result, null, 2) }];
        // === 在响应前插入 system messages (LLM 自然看到) ===
        // 优先级: 自动转发 > 升级提醒 > 过期提醒 (升级更紧迫, 转发最贴近用户)
        // 规则: 调 token_info 自己不插 (避免 LLM 反复触发的死循环)
        if (name !== "token_info") {
            if (redirectMsg)
                content = [{ type: "text", text: redirectMsg }, ...content];
            if (updateNotice)
                content = [{ type: "text", text: updateNotice }, ...content];
            if (tokenStatus?.msg)
                content = [{ type: "text", text: tokenStatus.msg }, ...content];
        }
        return { content };
    }
    catch (e) {
        return { content: [{ type: "text", text: JSON.stringify({ error: e.message }) }] };
    }
});
// Start server
async function main() {
    const transport = new stdio_js_1.StdioServerTransport();
    await server.connect(transport);
    console.error(`StockToday Skill v${CURRENT_VERSION} running`);
    console.error(`[rate_limit] ${JSON.stringify(rateLimiter.config)}`);
    console.error(`[token_breaker] enabled (2 次 auth_error 熔断 5min, 防 IP ban)`);
    // 启动后 1s 检查 token 状态 (非阻塞)
    setTimeout(() => { refreshTokenStatus().catch(e => console.error("[token_warn] check failed:", e.message)); }, 1000).unref();
    // 每 6h 重新检查一次 (保险)
    setInterval(() => { refreshTokenStatus().catch(() => { }); }, 6 * 60 * 60 * 1000).unref();
    // 启动后 2s 检查 ClawHub 最新版本 (非阻塞, 10s 超时)
    setTimeout(() => { refreshUpdateNotice().catch(e => console.error("[update] check failed:", e.message)); }, 2000).unref();
    // 每 24h 重新检查 (避免频繁扰动 ClawHub)
    setInterval(() => { refreshUpdateNotice().catch(() => { }); }, 24 * 60 * 60 * 1000).unref();
    // 周期打印限流器状态 (到 stderr, 不污染 LLM 通信)
    setInterval(() => {
        const stats = rateLimiter.getStats();
        if (stats.totalCalls > 0) {
            console.error(`[rate_limit stats] calls=${stats.totalCalls} throttled=${stats.totalThrottled} retries=${stats.totalRetries} silent_fails=${stats.totalSilentFails} avg_ms=${Math.round(stats.totalRealtimeMs / stats.totalCalls)} peak_conc=${stats.peakConcurrency}`);
        }
    }, 60000).unref();
}
main().catch(console.error);
