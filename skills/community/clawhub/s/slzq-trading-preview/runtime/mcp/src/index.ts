#!/usr/bin/env node
/**
 * 三立智期 OpenClaw — HTTP Open API (`/open/v1`) 的 MCP 封装。
 * 环境变量：SLZQ_OPENCLAW_DOMAIN、SLZQ_OPENCLAW_API_KEY、SLZQ_OPENCLAW_ENV（sim|live）。
 *
 * 未配置 API Key 时服务端仍会启动：交易类工具会返回可执行的登录指引，
 * 用户可直接用 slzq_open_v1_auth_* 系列工具完成手机号验证码登录并自动落盘密钥。
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import type { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { chmod, mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { z } from "zod";

const SKILL_NAME = "slzq-trading";
const DEFAULT_DOMAIN = "https://slzqapi.sxslqhsh.com";
const DOMAIN_ENV = "SLZQ_OPENCLAW_DOMAIN";
const API_KEY_ENV = "SLZQ_OPENCLAW_API_KEY";
const TRADING_ENV = "SLZQ_OPENCLAW_ENV";

/** 登录后落盘的凭据文件：宿主不是 OpenClaw 时也能让密钥跨重启生效 */
const CREDENTIALS_DIR = join(homedir(), `.${SKILL_NAME}`);
const CREDENTIALS_FILE = join(CREDENTIALS_DIR, "credentials.json");
/** OpenClaw 网关自身的配置；仅在用户确实装了 OpenClaw（目录已存在）时才合并写入 */
const OPENCLAW_CONFIG_FILE = join(homedir(), ".openclaw", "openclaw.json");

const NO_API_KEY_HINT =
  `尚未配置 ${API_KEY_ENV}。有两种取钥方式，先把两种都告诉用户让其选择，不要替他决定：` +
  `【方式 A · 会话内登录领取，最快】选 A 就直接按顺序执行，不要复述步骤、不要解释原理、不要在步骤之间征求同意：` +
  `1) slzq_open_v1_auth_agreement → 把 highlights 原文发给用户，让其回复同意；` +
  `2) 向用户要 11 位手机号 → slzq_open_v1_auth_send_code；` +
  `3) 用户报出验证码（位数照第 2 步返回的 codeLength，当前为 4 位纯数字，不要自己猜长度）` +
  `→ slzq_open_v1_auth_login（只传 mobileNum 和 verifyCode，验证码原样传字符串、保留前导零）。` +
  `方式 A 只需要用户提供手机号和验证码；服务端若已有可用的模拟盘密钥会原样返回那把（keyCreated=false），` +
  `不会顶掉用户其它设备上的配置。登录成功后密钥自动落盘并在本会话立即生效，无需重启，随后直接继续用户原本的任务。` +
  `【方式 B · 去 App 复制已有密钥】请用户打开 App「我的 → 期货辅助交易」，有效密钥列表会显示完整密钥并支持一键复制，` +
  `粘贴过来后写入 ${API_KEY_ENV}（禁止回显完整密钥，只回前缀）。要用实盘（SIM_LIVE）密钥时只能走方式 B。` +
  `若 auth 工具返回 10411，说明该地址上的服务端未上线登录接口（不是要你补密钥）：停止重试，改走方式 B。`

interface RuntimeConfig {
  domain: string;
  /** 域名来源：env=用户显式配置；default=生产默认 https://slzqapi.sxslqhsh.com */
  domainSource: "env" | "default";
  apiBase: string;
  apiKey: string;
  /** 密钥来源：env=环境变量；file=本地凭据文件；login=本次会话登录所得；none=未配置 */
  apiKeySource: "env" | "file" | "login" | "none";
  tradingEnv: "sim" | "live";
}

let config: RuntimeConfig;

/** 只保留首尾若干字符，日志与工具返回一律用这个，避免完整密钥落到会话记录里 */
function maskApiKey(apiKey: string): string {
  if (!apiKey) return "";
  if (apiKey.length <= 12) return "***";
  return `${apiKey.slice(0, 7)}***${apiKey.slice(-4)}`;
}

function normalizeDomain(raw: string): string {
  let domain = raw.trim().replace(/\/+$/, "");
  // 用户常把 /mobile-api 一起填进来；这里纠正并提示，而不是让后续每个请求都 404
  if (/\/mobile-api\/?$/i.test(domain)) {
    domain = domain.replace(/\/mobile-api\/?$/i, "");
    console.error(`WARN: ${DOMAIN_ENV} 不应包含 /mobile-api，已自动去除，实际使用：${domain}`);
  }
  return domain;
}

/**
 * 环境变量优先；没有则回落到登录时落盘的凭据文件。
 * 凭据带域名限定：密钥按域名签发，配错域名会得到 10411。
 * 与其让用户对着"密钥无效"排查，不如当作未配置直接引导重新登录。
 */
async function resolveApiKey(domain: string): Promise<{ apiKey: string; source: RuntimeConfig["apiKeySource"] }> {
  const fromEnv = (process.env[API_KEY_ENV] ?? "").trim();
  if (fromEnv) {
    return { apiKey: fromEnv, source: "env" };
  }
  try {
    const raw = await readFile(CREDENTIALS_FILE, "utf8");
    const parsed = JSON.parse(raw) as { apiKey?: unknown; domain?: unknown };
    const apiKey = typeof parsed.apiKey === "string" ? parsed.apiKey.trim() : "";
    const savedDomain = typeof parsed.domain === "string" ? parsed.domain.trim() : "";
    if (apiKey && savedDomain && savedDomain !== domain) {
      console.error(`WARN: 本地凭据是为 ${savedDomain} 领取的，与当前域名 ${domain} 不符，已忽略；请重新登录领取。`);
      return { apiKey: "", source: "none" };
    }
    if (apiKey) {
      return { apiKey, source: "file" };
    }
  } catch {
    // 文件不存在或内容损坏都按「未配置」处理，交由登录流程重新写入
  }
  return { apiKey: "", source: "none" };
}

async function loadConfig(): Promise<RuntimeConfig> {
  const rawDomain = (process.env[DOMAIN_ENV] ?? "").trim();
  const domainSource: RuntimeConfig["domainSource"] = rawDomain ? "env" : "default";
  const domain = normalizeDomain(rawDomain || DEFAULT_DOMAIN);
  const rawEnv = (process.env[TRADING_ENV] ?? "sim").trim().toLowerCase();
  let tradingEnv: RuntimeConfig["tradingEnv"] = "sim";
  if (rawEnv === "live") {
    tradingEnv = "live";
  } else if (rawEnv !== "sim") {
    // 取值非法时退到 sim：模拟盘是更安全的一侧，总比启动失败或误入实盘好
    console.error(`WARN: ${TRADING_ENV}=${rawEnv} 非法，已按 sim 处理（合法值：sim 或 live）`);
  }
  const { apiKey, source } = await resolveApiKey(domain);
  if (!apiKey) {
    console.error(`WARN: 未配置 ${API_KEY_ENV}，交易类工具将返回登录指引；可用 slzq_open_v1_auth_login 完成登录。`);
  }
  return { domain, domainSource, apiBase: `${domain}/mobile-api`, apiKey, apiKeySource: source, tradingEnv };
}

/**
 * 原子写：先写同目录临时文件再 rename。直接覆盖写在中途被杀/磁盘满时会留下一个被截断的文件，
 * 而这两个文件（凭据、OpenClaw 配置）损坏的代价分别是"密钥丢失"和"把用户整份网关配置写坏"。
 */
async function writeFileAtomic(filePath: string, content: string, mode: number): Promise<void> {
  const tmpPath = `${filePath}.tmp-${process.pid}`;
  await writeFile(tmpPath, content, { mode });
  try {
    await chmod(tmpPath, mode);
    await rename(tmpPath, filePath);
  } catch (e) {
    await rm(tmpPath, { force: true }).catch(() => {});
    throw e;
  }
}

/**
 * 把密钥写入本地凭据文件（0600）；若本机装了 OpenClaw，再合并写入其配置的 skill 条目。
 * 返回给用户看的落盘说明；任何一处失败都只降级为提示，不影响本次会话已经生效的内存密钥。
 */
async function persistApiKey(apiKey: string): Promise<string[]> {
  const notes: string[] = [];
  try {
    await mkdir(CREDENTIALS_DIR, { recursive: true, mode: 0o700 });
    const payload = { apiKey, domain: config.domain, updatedAt: new Date().toISOString() };
    await writeFileAtomic(CREDENTIALS_FILE, `${JSON.stringify(payload, null, 2)}\n`, 0o600);
    notes.push(`已写入本地凭据文件（仅当前用户可读）：${CREDENTIALS_FILE}`);
  } catch (e) {
    notes.push(`本地凭据文件写入失败（${errorMessage(e)}），请手动设置环境变量 ${API_KEY_ENV}`);
  }
  notes.push(...(await mergeIntoOpenclawConfig(apiKey)));
  if (process.env[API_KEY_ENV] && process.env[API_KEY_ENV] !== apiKey) {
    notes.push(
      `注意：环境变量 ${API_KEY_ENV} 已存在且与本次密钥不同，重启后环境变量优先级更高；` +
        `请把该环境变量更新为新密钥，否则重启后会退回旧密钥。`
    );
  }
  return notes;
}

/** 合并写入 ~/.openclaw/openclaw.json 的 skills.entries.<skill>；配置损坏时宁可不动也不覆盖用户文件 */
async function mergeIntoOpenclawConfig(apiKey: string): Promise<string[]> {
  let raw: string;
  try {
    raw = await readFile(OPENCLAW_CONFIG_FILE, "utf8");
  } catch {
    // 没装 OpenClaw 或还没生成配置：本地凭据文件已够用，静默跳过
    return [];
  }
  let parsed: Record<string, any>;
  try {
    parsed = raw.trim() ? JSON.parse(raw) : {};
  } catch (e) {
    return [`${OPENCLAW_CONFIG_FILE} 不是合法 JSON（${errorMessage(e)}），已跳过写入以免破坏原文件，请手动填写 API Key。`];
  }
  try {
    const skills = (parsed.skills ??= {});
    const entries = (skills.entries ??= {});
    const entry = (entries[SKILL_NAME] ??= {});
    entry.apiKey = apiKey;
    // 只补空缺，不覆盖用户已填的域名/交易环境：本进程的环境变量未必等于用户在网关里的设置，
    // 覆盖会把人家配好的 live 悄悄改成 sim。
    const env = { ...(entry.env ?? {}) };
    if (!env[DOMAIN_ENV]) env[DOMAIN_ENV] = config.domain;
    if (!env[TRADING_ENV]) env[TRADING_ENV] = config.tradingEnv;
    entry.env = env;
    await writeFileAtomic(OPENCLAW_CONFIG_FILE, `${JSON.stringify(parsed, null, 2)}\n`, 0o600);
    return [`已合并写入 OpenClaw 配置：${OPENCLAW_CONFIG_FILE}（skills.entries.${SKILL_NAME}）`];
  } catch (e) {
    return [`写入 ${OPENCLAW_CONFIG_FILE} 失败（${errorMessage(e)}），请在 OpenClaw Skills 界面手动填写 API Key。`];
  }
}

function errorMessage(e: unknown): string {
  return e instanceof Error ? e.message : String(e);
}

function textResult(text: string, isError = false): CallToolResult {
  return { content: [{ type: "text", text }], isError };
}

function jsonResult(data: unknown, isError = false): CallToolResult {
  return {
    content: [{ type: "text", text: typeof data === "string" ? data : JSON.stringify(data, null, 2) }],
    isError,
  };
}

async function openApiFetch(
  path: string,
  options: {
    method?: string;
    auth: boolean;
    searchParams?: Record<string, string | number | boolean | undefined | null>;
    body?: unknown;
  }
): Promise<{ ok: boolean; status: number; body: unknown }> {
  const url = new URL(`${config.apiBase}/open/v1${path.startsWith("/") ? path : `/${path}`}`);
  if (options.searchParams) {
    for (const [k, v] of Object.entries(options.searchParams)) {
      if (v === undefined || v === null || v === "") continue;
      url.searchParams.set(k, String(v));
    }
  }
  const headers: Record<string, string> = {};
  if (options.auth) {
    if (!config.apiKey) {
      throw new Error(NO_API_KEY_HINT);
    }
    headers.Authorization = `Bearer ${config.apiKey}`;
    headers["X-Trading-Env"] = config.tradingEnv;
  }
  if (options.body !== undefined) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(url, {
    method: options.method ?? "GET",
    headers,
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  });
  const raw = await res.text();
  let parsed: unknown = raw;
  try {
    parsed = raw ? JSON.parse(raw) : null;
  } catch {
    /* keep text */
  }
  return { ok: res.ok, status: res.status, body: parsed };
}

async function runTool(
  fn: () => Promise<{ ok: boolean; status: number; body: unknown }>
): Promise<CallToolResult> {
  try {
    const { ok, status, body } = await fn();
    const payload =
      typeof body === "object" && body !== null
        ? { httpStatus: status, ...((body as object) as Record<string, unknown>) }
        : { httpStatus: status, raw: body };
    const apiFailed = typeof body === "object" && body !== null && (body as { success?: unknown }).success === false;
    return jsonResult(payload, !ok || apiFailed);
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return textResult(msg, true);
  }
}

const directionEnum = z.enum(["BUY", "SELL"]);
const offsetFlagEnum = z.enum([
  "OPEN",
  "CLOSE",
  "CLOSE_TODAY",
  "CLOSE_YESTERDAY",
]);
const priceTypeEnum = z.enum(["ANY", "LIMIT", "BEST", "LAST"]);

const placeOrderSchema = z.object({
  instrumentId: z.string().regex(/^[A-Za-z]+\d+$/, "instrumentId 必须为字母+数字，不带交易所后缀，如 cu2506 或 IF2506"),
  orderRef: z.string().regex(/^\d{1,13}$/, "orderRef 必须为 1～13 位纯数字").optional(),
  direction: directionEnum,
  offsetFlag: offsetFlagEnum,
  priceType: priceTypeEnum,
  limitPrice: z.number(),
  count: z.number().int().positive(),
  positionDateType: z.enum(["今", "昨"]).optional(),
  minCount: z.number().int().positive().optional(),
  timeCondition: z.enum(["GFD", "GTC"]).optional(),
  stopPriceType: z.number().int().min(1).max(5).optional(),
  orderPrice: z.number().optional(),
});

const cancelOrderSchema = z.object({
  instrumentId: z.string().regex(/^[A-Za-z]+\d+$/, "instrumentId 必须为字母+数字，不带交易所后缀，如 cu2506 或 IF2506"),
  exchangeId: z.string(),
  orderRef: z.string().regex(/^\d{1,13}$/, "orderRef 必须为 1～13 位纯数字"),
  orderSysId: z.string(),
  frontID: z.number().int(),
  sessionId: z.number().int().optional(),
});

const mobileNumSchema = z
  .string()
  .regex(/^\d{11}$/, "手机号必须是 11 位数字");

/**
 * 探测服务端是否支持免密钥登录。
 *
 * 关键点：老版本服务端上 /open/v1/auth/* 并不存在，但鉴权拦截器排在路由之前，
 * 会先返回 10411「缺少 API Key」——直接打 auth 接口是无法区分「未上线」和「真要密钥」的。
 * /open/v1/health 在新老版本上都免鉴权，新版会带 authLoginSupported=true，因此它才是权威判据。
 */
async function probeServerCapability(): Promise<{
  reachable: boolean;
  supported: boolean;
  skillName?: string;
  skillVersion?: string;
  apiBase?: string;
  detail: string;
}> {
  try {
    const { ok, status, body } = await openApiFetch("/health", { auth: false });
    const data = (body as { data?: Record<string, unknown> } | null)?.data;
    if (!ok || !data) {
      return { reachable: false, supported: false, detail: `health HTTP ${status}` };
    }
    return {
      reachable: true,
      supported: data.authLoginSupported === true,
      skillName: typeof data.skillName === "string" ? data.skillName : undefined,
      skillVersion: typeof data.skillVersion === "string" ? data.skillVersion : undefined,
      apiBase: typeof data.apiBase === "string" ? data.apiBase : undefined,
      detail:
        data.authLoginSupported === true
          ? "health 返回 authLoginSupported=true"
          : "health 未返回 authLoginSupported，服务端版本早于登录领钥功能",
    };
  } catch (e) {
    return { reachable: false, supported: false, detail: errorMessage(e) };
  }
}

/**
 * auth 系列专用包装：把 10411 翻译成「服务端未上线该接口」。
 * 免鉴权接口不可能真的缺密钥，收到 10411 只可能是老版本的鉴权拦截器拦下了不存在的路由。
 */
async function runAuthTool(
  fn: () => Promise<{ ok: boolean; status: number; body: unknown }>
): Promise<CallToolResult> {
  const result = await runTool(fn);
  const text = result.content?.[0];
  if (result.isError && text && text.type === "text" && text.text.includes("10411")) {
    return jsonResult(
      {
        raw: text.text,
        verdict: "SERVER_TOO_OLD",
        explain:
          "该接口免鉴权，收到 10411 只说明服务端版本过旧、路由尚未上线（旧版鉴权拦截器会先拦下不存在的 /open/v1/* 路径）。",
        nextStep:
          "不要再重试、也不要尝试其它域名或伪造密钥。请用户在 App「我的 → 期货辅助交易」生成模拟盘密钥，" +
          `再写入环境变量 ${API_KEY_ENV}。可用 slzq_open_v1_auth_status 查看服务端版本佐证。`,
      },
      true
    );
  }
  return result;
}

/** 首次安装引导：查看密钥状态、风险告知、发送验证码、登录领钥 */
function registerAuthTools(server: McpServer) {
  server.registerTool(
    "slzq_open_v1_auth_status",
    {
      description:
        "【任何工具报未配置密钥/10411 时，先且只需调用它】一次性给出终局判定：本机是否已配置密钥、" +
        "服务端是否支持免密钥登录、下一步该做什么（verdict 字段）。不要靠 curl 试错去猜服务端行为。",
    },
    async () => {
      const base = {
        configured: Boolean(config.apiKey),
        apiKeySource: config.apiKeySource,
        apiKeyMasked: maskApiKey(config.apiKey),
        domain: config.domain,
        domainSource: config.domainSource,
        apiBase: config.apiBase,
        tradingEnv: config.tradingEnv,
        credentialsFile: CREDENTIALS_FILE,
      };
      if (config.apiKey) {
        try {
          const { ok, status, body } = await openApiFetch("/me", { auth: true });
          const failed = typeof body === "object" && body !== null && (body as { success?: unknown }).success === false;
          return jsonResult(
            { ...base, verdict: ok && !failed ? "READY：密钥可用，直接开始业务调用" : "KEY_REJECTED：密钥被服务端拒绝，按 me 返回的 errorInfo 处理", httpStatus: status, me: body },
            !ok || failed
          );
        } catch (e) {
          return jsonResult({ ...base, verdict: "NETWORK_ERROR：请求失败，检查域名是否可达", error: errorMessage(e) }, true);
        }
      }

      // 没有密钥时先探测服务端能力：health 在新老版本上都免鉴权，是唯一可靠的判定信号
      const probe = await probeServerCapability();
      return jsonResult({
        ...base,
        serverAuthLoginSupported: probe.supported,
        serverSkillName: probe.skillName,
        serverSkillVersion: probe.skillVersion,
        serverApiBase: probe.apiBase,
        verdict: probe.supported
          ? "NEED_LOGIN：服务端支持免密钥登录。按 nextStep 把方式 A / 方式 B 两种取钥方式给用户选，选定后立即执行，不要再问是否继续"
          : probe.reachable
            ? config.domainSource === "default"
              ? `SERVER_TOO_OLD：当前生产域名 ${config.domain} 未上线登录接口，方式 A 不可用。不要改域名；改走方式 B（App「我的 → 期货辅助交易」复制已有密钥）后写入 ${API_KEY_ENV}`
              : `SERVER_TOO_OLD：${config.domain} 未上线登录接口，方式 A 不可用，不要再试 auth 工具；改走方式 B——请用户在 App「我的 → 期货辅助交易」的有效密钥列表一键复制已有密钥（没有就在该页面新建一把）后写入 ${API_KEY_ENV}`
            : "NETWORK_ERROR：域名不可达，请确认能访问生产地址 https://slzqapi.sxslqhsh.com/mobile-api（" + DOMAIN_ENV + " 不要带 /mobile-api）",
        nextStep: probe.supported ? NO_API_KEY_HINT : undefined,
        probeDetail: probe.detail,
      });
    }
  );

  server.registerTool(
    "slzq_open_v1_auth_agreement",
    {
      description:
        "GET /open/v1/auth/agreement — 登录前必须取回并向用户原文展示的风险告知，无需鉴权。" +
        "用户明确同意后，把返回的 version 作为 agreementVersion 传给 slzq_open_v1_auth_login。",
    },
    async () => runAuthTool(() => openApiFetch("/auth/agreement", { auth: false }))
  );

  server.registerTool(
    "slzq_open_v1_auth_send_code",
    {
      description:
        "发送登录/注册短信验证码（POST /open/v1/auth/sms/send，无需鉴权）。" +
        "codeKey 由服务端按手机号暂存，调用 slzq_open_v1_auth_login 时无需回传、也不必自己保存。" +
        "同一手机号 1 分钟内只能发 1 条，收到限流提示就等，不要立刻重发。" +
        "返回的 codeLength 就是本次验证码的位数（纯数字，当前为 4 位）——按它向用户索取，不要猜长度；该值由服务端动态决定，以每次返回为准，不要硬编码。",
      inputSchema: { mobileNum: mobileNumSchema },
    },
    async (args) =>
      runAuthTool(() =>
        openApiFetch("/auth/sms/send", { method: "POST", auth: false, body: { mobileNum: args.mobileNum } })
      )
  );

  server.registerTool(
    "slzq_open_v1_auth_login",
    {
      description:
        "手机号+验证码登录/注册并领取【模拟盘】API Key（POST /open/v1/auth/login，无需鉴权）。" +
        "拿到用户报的验证码后直接调用即可，只需 mobileNum + verifyCode（codeKey 由服务端按手机号取回）。" +
        "成功后密钥自动落盘并在本会话立即生效，无需重启；模拟盘账户同时自动开通，返回的 simAccountReady/simAccountBalance " +
        "即为账户状态，simAccountReady=false 时告知用户账户未就绪即可，不要去 App 找开户入口。" +
        "实盘权限不从这里开通，须回 App 验 CTP 交易密码。" +
        "返回内容不含完整密钥，不要要求用户或自行复述密钥明文。",
      inputSchema: {
        mobileNum: mobileNumSchema,
        verifyCode: z
          .string()
          .min(1, "验证码不能为空")
          .describe(
            "短信验证码，位数以 slzq_open_v1_auth_send_code 返回的 codeLength 为准（当前 4 位纯数字）；" +
              "原样传字符串，保留前导零，不要转成数字"
          ),
        codeKey: z
          .string()
          .optional()
          .describe("不用传：服务端按手机号自动取回本次发码的 codeKey"),
        agreementVersion: z
          .string()
          .optional()
          .describe("用户已确认的风险告知版本号，取自 slzq_open_v1_auth_agreement；首次登录必填"),
        name: z.string().optional().describe("密钥备注名，可选"),
        forceRotate: z
          .boolean()
          .optional()
          .describe("true=吊销原模拟盘密钥并重新签发（其它设备上的旧密钥会立即失效）。默认 false，复用已有密钥"),
      },
    },
    async (args) => {
      let response: { ok: boolean; status: number; body: unknown };
      try {
        response = await openApiFetch("/auth/login", { method: "POST", auth: false, body: args });
      } catch (e) {
        return textResult(errorMessage(e), true);
      }
      const body = response.body as { success?: boolean; data?: { apiKey?: string } } | null;
      const apiKey = typeof body?.data?.apiKey === "string" ? body.data.apiKey.trim() : "";
      if (!response.ok || body?.success === false || !apiKey) {
        return jsonResult({ httpStatus: response.status, ...(body as object) }, true);
      }

      // 先让本次会话立即可用，再落盘：即使写盘失败，用户当前会话也不至于卡住
      config = { ...config, apiKey, apiKeySource: "login" };
      const persistNotes = await persistApiKey(apiKey);

      // data 里剔除 apiKey 再回给模型，避免完整密钥进入会话上下文与日志
      const { apiKey: _omitted, ...safeData } = (body?.data ?? {}) as Record<string, unknown>;
      return jsonResult({
        httpStatus: response.status,
        success: true,
        data: { ...safeData, apiKeyMasked: maskApiKey(apiKey) },
        applied: `密钥已在本次会话生效（交易环境 ${config.tradingEnv}）`,
        persisted: persistNotes,
        nextStep: "调用 slzq_open_v1_auth_status 或 slzq_open_v1_me 确认权限档位，随后即可查询行情与持仓。",
      });
    }
  );
}

function registerSlzqTools(server: McpServer) {
  registerAuthTools(server);

  server.registerTool(
    "slzq_open_v1_health",
    {
      description: "GET /open/v1/health — 健康检查，无需 Api-Key",
    },
    async () =>
      runTool(() => openApiFetch("/health", { auth: false }))
  );

  server.registerTool(
    "slzq_open_v1_skill_version",
    {
      description: "GET /open/v1/skill/version — skill 版本检查，无需 Api-Key",
      inputSchema: { clientVersion: z.string().optional() },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/skill/version", {
          auth: false,
          searchParams: { clientVersion: args?.clientVersion },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_skill_upgrade",
    {
      description: "GET /open/v1/skill/upgrade — 升级指引，无需 Api-Key",
    },
    async () => runTool(() => openApiFetch("/skill/upgrade", { auth: false }))
  );

  server.registerTool(
    "slzq_open_v1_me",
    { description: "GET /open/v1/me — 当前密钥上下文" },
    async () => runTool(() => openApiFetch("/me", { auth: true }))
  );

  server.registerTool(
    "slzq_open_v1_account_summary",
    { description: "GET /open/v1/account/summary — 账户摘要（sim/live）" },
    async () => runTool(() => openApiFetch("/account/summary", { auth: true }))
  );

  server.registerTool(
    "slzq_open_v1_account_pnl_history",
    {
      description: "GET /open/v1/account/pnl/history — 账户历史盈亏",
      inputSchema: {
        preset: z.enum(["last7d", "last30d", "last90d", "monthToDate"]).optional(),
        startTradingDay: z.string().optional(),
        endTradingDay: z.string().optional(),
      },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/account/pnl/history", {
          auth: true,
          searchParams: {
            preset: args?.preset,
            startTradingDay: args?.startTradingDay,
            endTradingDay: args?.endTradingDay,
          },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_positions",
    {
      description: "GET /open/v1/positions — 持仓列表；sim 可选 positionDateType 今|昨",
      inputSchema: { positionDateType: z.enum(["今", "昨"]).optional() },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/positions", {
          auth: true,
          searchParams: { positionDateType: args?.positionDateType },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_catalog_goods",
    {
      description: "GET /open/v1/catalog/goods — 品种与主力合约分页",
      inputSchema: {
        excode: z.string().optional(),
        page: z.number().int().optional(),
        pageSize: z.number().int().optional(),
        sortType: z.number().int().optional(),
        category: z.string().optional(),
        productId: z.string().optional(),
        onlyMainInCategory: z.boolean().optional(),
        allContractsByExcode: z.boolean().optional(),
      },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/catalog/goods", {
          auth: true,
          searchParams: {
            excode: args?.excode,
            page: args?.page,
            pageSize: args?.pageSize,
            sortType: args?.sortType,
            category: args?.category,
            productId: args?.productId,
            onlyMainInCategory: args?.onlyMainInCategory,
            allContractsByExcode: args?.allContractsByExcode,
          },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_catalog_goods_detail",
    {
      description: "GET /open/v1/catalog/goods/detail — 品种详情",
      inputSchema: { excode: z.string(), code: z.string() },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/catalog/goods/detail", {
          auth: true,
          searchParams: { excode: args.excode, code: args.code },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_catalog_contract",
    {
      description: "GET /open/v1/catalog/contract — 合约详情",
      inputSchema: { contractCode: z.string() },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/catalog/contract", { auth: true, searchParams: { contractCode: args.contractCode } })
      )
  );

  server.registerTool(
    "slzq_open_v1_catalog_contract_f10",
    {
      description: "GET /open/v1/catalog/contract/f10 — 合约 F10",
      inputSchema: { contractCode: z.string() },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/catalog/contract/f10", {
          auth: true,
          searchParams: { contractCode: args.contractCode },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_catalog_hot",
    { description: "GET /open/v1/catalog/hot — 热门合约 TOP10" },
    async () => runTool(() => openApiFetch("/catalog/hot", { auth: true }))
  );

  server.registerTool(
    "slzq_open_v1_catalog_exchanges",
    { description: "GET /open/v1/catalog/exchanges — 交易所列表" },
    async () => runTool(() => openApiFetch("/catalog/exchanges", { auth: true }))
  );

  server.registerTool(
    "slzq_open_v1_catalog_session_night_today",
    { description: "GET /open/v1/catalog/session/night-today — 当晚是否有夜盘" },
    async () => runTool(() => openApiFetch("/catalog/session/night-today", { auth: true }))
  );

  server.registerTool(
    "slzq_open_v1_market_snapshot",
    {
      description: "GET /open/v1/market/snapshot — 单合约快照；instrumentId 与 contractCode 至少填一个",
      inputSchema: {
        instrumentId: z.string().optional(),
        contractCode: z.string().optional(),
      },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/market/snapshot", {
          auth: true,
          searchParams: {
            instrumentId: args?.instrumentId,
            contractCode: args?.contractCode,
          },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_market_snapshots",
    {
      description: "GET /open/v1/market/snapshots — 批量快照，instrumentIds 逗号分隔",
      inputSchema: { instrumentIds: z.string() },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/market/snapshots", {
          auth: true,
          searchParams: { instrumentIds: args.instrumentIds },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_market_tick",
    {
      description: "GET /open/v1/market/tick — 分时",
      inputSchema: { exchangeId: z.string(), instrumentId: z.string() },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/market/tick", {
          auth: true,
          searchParams: { exchangeId: args.exchangeId, instrumentId: args.instrumentId },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_market_kline",
    {
      description: "GET /open/v1/market/kline — K 线",
      inputSchema: {
        exchangeId: z.string(),
        instrumentId: z.string(),
        type: z.number().int(),
      },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/market/kline", {
          auth: true,
          searchParams: {
            exchangeId: args.exchangeId,
            instrumentId: args.instrumentId,
            type: args.type,
          },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_orders_open",
    { description: "GET /open/v1/orders/open — 当前委托" },
    async () => runTool(() => openApiFetch("/orders/open", { auth: true }))
  );

  server.registerTool(
    "slzq_open_v1_trades",
    {
      description: "GET /open/v1/trades — 成交列表",
      inputSchema: {
        instrumentId: z.string().optional(),
        exchangeId: z.string().optional(),
        insertTimeStart: z.string().optional(),
        insertTimeEnd: z.string().optional(),
      },
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/trades", {
          auth: true,
          searchParams: {
            instrumentId: args?.instrumentId,
            exchangeId: args?.exchangeId,
            insertTimeStart: args?.insertTimeStart,
            insertTimeEnd: args?.insertTimeEnd,
          },
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_orders_place",
    {
      description:
        "POST /open/v1/orders — 下单（sim/live）。未经用户明确指令请勿对 live 自动下单。body 同 CnCtpInputOrderRequest",
      inputSchema: placeOrderSchema,
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/orders", {
          method: "POST",
          auth: true,
          body: args,
        })
      )
  );

  server.registerTool(
    "slzq_open_v1_orders_cancel",
    {
      description: "POST /open/v1/orders/cancel — 撤单",
      inputSchema: cancelOrderSchema,
    },
    async (args) =>
      runTool(() =>
        openApiFetch("/orders/cancel", {
          method: "POST",
          auth: true,
          body: args,
        })
      )
  );
}

async function main() {
  config = await loadConfig();
  const server = new McpServer({
    name: "slzq-trading-mcp",
    version: "1.1.0",
  });
  registerSlzqTools(server);
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
