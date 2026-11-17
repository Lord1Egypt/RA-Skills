#!/usr/bin/env node
/**
 * 仙踪问道·旅行咨询 —— 支付宝 AI 按量付费（HTTP 402）资源请求工具。
 *
 * 只用 Node.js 内置模块（fetch / fs / child_process），无第三方依赖，
 * 与官方买家能力 alipay-bot 共用同一运行时。
 *
 * 本脚本只做三件事：
 *   1. 组装并校验业务请求体（POST 资源接口）
 *   2. 发起无凭证请求拿到 402 账单，并将原始请求落盘复用
 *   3. 付款后取资源、渲染结果
 *
 * 付款、账单签名、交易查询、履约回执一律交给官方 alipay-bot：
 *   - alipay-bot 402-buyer-pay            （发起支付）
 *   - alipay-bot 402-query-payment-status （付款后查询原订单并取资源，自动回执）
 * 本脚本不生成账单签名、不发起支付、不查支付宝交易、不自行构造履约回执。
 *
 * 子命令：
 *   body    只组装并打印请求体（不发请求）
 *   probe   发起 402 挑战，产出账单文件与状态文件
 *   pay     调用官方 alipay-bot 发起支付（须 --confirm）
 *   complete 付款后取资源（优先官方查询；--proof 走带凭证直取）
 *   render  把交付结果渲染成可展示文本
 *
 * 退出码：
 *   0 成功   2 参数/请求错误   3 资源生成中(409)
 *   4 业务失败   5 凭证无效/需重新支付(402)   6 服务端错误(5xx/瞬时不可用)
 *
 * 取货轮询要点（2026-11-14 实测）：官方 `402-query-payment-status --output json` 的成功载荷
 * **没有** `resourceDelivered` 字段，判据是 `success: true` + `resourceResponse.status: 200`；
 * 409 与 `resourceResponse: null`（服务重启/网络瞬断）都属于「未交付但可重试」，
 * 用同一订单（--out-shake-no）反复查即可，**绝不重新付款**。
 * `complete --wait` 会按上述判据自动轮询。
 */

import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

// 资源地址与服务登记信息
const RESOURCE_URL = 'https://api.riyuexinzhu.com/aipay/travel_consultant';
const GOODS_NAME = '仙踪问道_旅行咨询';
const PRICE_CNY = '0.99';

const HEADER_PAYMENT_NEEDED = 'Payment-Needed';
const HEADER_PAYMENT_PROOF = 'Payment-Proof';
const HEADER_PAYMENT_VALIDATION = 'Payment-Validation';

const EMAIL_PATTERN = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const DEFAULT_TIMEOUT_MS = 600000;

const EXIT_OK = 0;
const EXIT_PARAM = 2;
const EXIT_IN_PROGRESS = 3;
const EXIT_BUSINESS_FAIL = 4;
const EXIT_NEED_PAY = 5;
const EXIT_SERVER_ERROR = 6;

// 可选整型字段：参数名 -> [body 字段名, 允许值]
const OPTIONAL_INTS = {
  'intro-type': ['intro_type', [0, 1, 2, 3, 4, 5, 6, 7, 8]],
  'topic-type': ['topic_type', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
  'is-group-suitable': ['is_group_suitable', [0, 1]],
  'is-family-suitable': ['is_family_suitable', [0, 1]],
  'is-leisure': ['is_leisure', [0, 1]],
  'is-with-ref': ['is_with_ref', [0, 1]],
};

const OPTIONAL_STRINGS = {
  'country-code': 'country_code',
  language: 'language',
};

// ---------------------------------------------------------------------------
// 参数解析
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const command = argv[0] && !argv[0].startsWith('--') ? argv[0] : null;
  const rest = command ? argv.slice(1) : argv;
  const flags = {};
  for (let i = 0; i < rest.length; i += 1) {
    const token = rest[i];
    if (!token.startsWith('--')) continue;
    const name = token.slice(2);
    const next = rest[i + 1];
    if (next === undefined || next.startsWith('--')) {
      flags[name] = true;
    } else {
      flags[name] = next;
      i += 1;
    }
  }
  return { command, flags };
}

const HELP = `仙踪问道·旅行咨询（支付宝 AI 按量付费 402）

用法：
  node scripts/travel_aipay.mjs body     --query '...' --email '...' [选项]
  node scripts/travel_aipay.mjs probe    --query '...' --email '...' [选项]
  node scripts/travel_aipay.mjs pay      --confirm [--session-id '...']
  node $SKILL_DIR/scripts/travel_aipay.mjs complete --out-shake-no '<官方查询单号>' [--wait] [选项]
  node scripts/travel_aipay.mjs complete --proof '<Payment-Proof>' [选项]
  node scripts/travel_aipay.mjs render   --response '<响应文件>'

业务选项：
  --query  <文本>   用户的旅行咨询问题（必填，目的地城市写在 query 里）
  --email  <邮箱>   接收 PDF 方案的邮箱（必填）
  --country-code / --intro-type / --topic-type
  --is-group-suitable / --is-family-suitable / --is-leisure / --is-with-ref / --language
  --options-json <JSON>   扩展参数对象

通用选项：
  --state-dir     本地状态目录，默认 ~/.xianzong-travel-aipay
  --timeout-ms    HTTP 超时毫秒，默认 600000
  --resource-url  覆盖资源地址（一般无需改动）

轮询选项（complete --out-shake-no 时生效）：
  --wait                 自动轮询直到交付或超时（409 / 服务瞬时不可用都会重试，不会重复扣费）
  --poll-interval-ms     轮询间隔毫秒，默认 40000
  --max-wait-ms          最长等待毫秒，默认 900000
`;

// ---------------------------------------------------------------------------
// 请求体组装与校验
// ---------------------------------------------------------------------------

function buildBody(flags) {
  const errors = [];

  const query = String(flags.query ?? '').trim();
  if (!query) errors.push('query 必填：请提供用户的旅行咨询问题');
  else if (query.length > 2000) errors.push('query 过长（上限 2000 字）');

  const email = String(flags.email ?? '').trim();
  if (!email) errors.push('email 必填：履约后会把排版化 PDF 方案发送到该邮箱');
  else if (email.length > 254 || !EMAIL_PATTERN.test(email)) errors.push(`email 格式非法：${email}`);

  const body = { query, email };

  for (const [argName, [field, allowed]] of Object.entries(OPTIONAL_INTS)) {
    if (flags[argName] === undefined || flags[argName] === true) continue;
    const value = Number(flags[argName]);
    if (!Number.isInteger(value)) {
      errors.push(`${argName} 必须是整数，收到 ${flags[argName]}`);
      continue;
    }
    if (!allowed.includes(value)) {
      errors.push(`${argName} 取值范围非法：${value}（允许 ${allowed.join(' / ')}）`);
      continue;
    }
    body[field] = value;
  }

  for (const [argName, field] of Object.entries(OPTIONAL_STRINGS)) {
    if (flags[argName] === undefined || flags[argName] === true) continue;
    const text = String(flags[argName]).trim();
    if (text) body[field] = text;
  }

  if (flags['city-code'] !== undefined) {
    errors.push('city_code 已移除：请把目的地城市直接写进 query（如「北京 4 天 3 晚亲子」）');
  }
  if (body.country_code && !/^[A-Za-z]{2}$/.test(body.country_code)) {
    errors.push('country_code 必须是 ISO 3166-1 alpha-2 两位代码（如 CN / IT）');
  }

  if (flags['options-json'] !== undefined && flags['options-json'] !== true) {
    try {
      const extra = JSON.parse(flags['options-json']);
      if (extra && typeof extra === 'object' && !Array.isArray(extra)) body.options = extra;
      else errors.push('options 必须是 JSON 对象');
    } catch {
      errors.push(`options 不是合法 JSON：${flags['options-json']}`);
    }
  }

  return { body, errors };
}

function resourceUrl(flags) {
  return String(flags['resource-url'] || RESOURCE_URL).trim();
}

function timeoutMs(flags) {
  const value = Number(flags['timeout-ms']);
  return Number.isFinite(value) && value > 0 ? value : DEFAULT_TIMEOUT_MS;
}

// ---------------------------------------------------------------------------
// HTTP（只发业务请求，不做任何签名）
// ---------------------------------------------------------------------------

async function postResource(url, body, { headers = {}, timeout } = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json', ...headers },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(timeout || DEFAULT_TIMEOUT_MS),
  });
  const text = await response.text();
  return { status: response.status, headers: response.headers, text };
}

// ---------------------------------------------------------------------------
// 本地状态目录（账单与请求体落盘；不进版本库、不打包）
// ---------------------------------------------------------------------------

function stateDir(flags) {
  // 默认放用户主目录，避免在任意 cwd（如仓库根）落下账单凭证文件
  const dir = path.resolve(String(flags['state-dir'] || path.join(os.homedir(), '.xianzong-travel-aipay')));
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  fs.chmodSync(dir, 0o700);
  return dir;
}

function writePrivate(filePath, content) {
  const tmp = `${filePath}.tmp`;
  fs.writeFileSync(tmp, content, { encoding: 'utf8', mode: 0o600 });
  fs.chmodSync(tmp, 0o600);
  fs.renameSync(tmp, filePath);
  return filePath;
}

function readState(dir) {
  const statePath = path.join(dir, 'state.json');
  if (!fs.existsSync(statePath)) throw new Error(`找不到状态文件：${statePath}，请先执行 probe`);
  return JSON.parse(fs.readFileSync(statePath, 'utf8'));
}

function readBodyFile(state) {
  return fs.readFileSync(state.bodyFile, 'utf8');
}

// ---------------------------------------------------------------------------
// 官方 CLI 调用（付款 / 查询 / 回执全部交给 alipay-bot）
// ---------------------------------------------------------------------------

function resolveSessionId(flags) {
  const explicit = String(flags['session-id'] || '').trim();
  if (explicit) return explicit;
  const candidates = ['AIPAY_SESSION_ID', 'CODEX_THREAD_ID', 'CONVERSATION_ID', 'SESSION_ID'];
  for (const name of candidates) {
    const value = String(process.env[name] || '').trim();
    if (value) return value;
  }
  return '';
}

function runAlipayBot(args, { quiet = false } = {}) {
  return new Promise((resolve) => {
    let child;
    const bin = String(process.env.ALIPAY_BOT_BIN || 'alipay-bot');
    try {
      child = spawn(bin, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    } catch {
      resolve({ exitCode: 127, stdout: '', stderr: '未找到 alipay-bot' });
      return;
    }
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => {
      const text = chunk.toString();
      stdout += text;
      if (!quiet) process.stdout.write(text);
    });
    child.stderr.on('data', (chunk) => {
      const text = chunk.toString();
      stderr += text;
      if (!quiet) process.stderr.write(text);
    });
    child.on('error', (error) => {
      if (error.code === 'ENOENT') {
        resolve({ exitCode: 127, stdout, stderr: `${stderr}未找到 alipay-bot（请安装官方 @alipay/agent-payment）` });
        return;
      }
      resolve({ exitCode: 1, stdout, stderr: `${stderr}${error.message}` });
    });
    child.on('close', (code) => resolve({ exitCode: code ?? 1, stdout, stderr }));
  });
}

// ---------------------------------------------------------------------------
// 输出
// ---------------------------------------------------------------------------

function printJson(payload) {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

function parseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// body
// ---------------------------------------------------------------------------

function cmdBody(flags) {
  const { body, errors } = buildBody(flags);
  if (errors.length) {
    process.stderr.write(`参数校验失败：\n${errors.map((item) => ` - ${item}`).join('\n')}\n`);
    return EXIT_PARAM;
  }
  printJson(body);
  return EXIT_OK;
}

// ---------------------------------------------------------------------------
// probe：未付款请求，取得 402 账单
// ---------------------------------------------------------------------------

async function cmdProbe(flags) {
  const { body, errors } = buildBody(flags);
  if (errors.length) {
    process.stderr.write(`参数校验失败（未发起请求）：\n${errors.map((item) => ` - ${item}`).join('\n')}\n`);
    return EXIT_PARAM;
  }

  const url = resourceUrl(flags);
  const dir = stateDir(flags);

  if (flags['dry-run']) {
    process.stdout.write('[dry-run] 以下请求未发送：\n');
    printJson({ method: 'POST', url, headers: { 'Content-Type': 'application/json' }, body });
    return EXIT_OK;
  }

  const { status, headers, text } = await postResource(url, body, { timeout: timeoutMs(flags) });
  const payload = parseJson(text) || {};

  if (status === 402) {
    const needed = headers.get(HEADER_PAYMENT_NEEDED);
    if (!needed) {
      process.stderr.write(`402 响应缺少 ${HEADER_PAYMENT_NEEDED} 头，放弃继续（不猜测账单内容）\n`);
      return EXIT_PARAM;
    }

    const challengeFile = writePrivate(path.join(dir, 'payment-needed.txt'), needed.trim());
    const bodyFile = writePrivate(path.join(dir, 'body.json'), JSON.stringify(body));
    const state = {
      resourceUrl: url,
      method: 'POST',
      outTradeNo: payload.out_trade_no || '',
      amount: payload.amount || PRICE_CNY,
      currency: payload.currency || 'CNY',
      goodsName: payload.goods_name || GOODS_NAME,
      query: body.query,
      challengeFile,
      bodyFile,
      createdAt: new Date().toISOString(),
    };
    const stateFile = writePrivate(path.join(dir, 'state.json'), JSON.stringify(state, null, 2));

    process.stdout.write('═══ 需要支付 ═══\n');
    process.stdout.write(`服务：${state.goodsName}（单次 ${PRICE_CNY} 元，以支付宝账单为准）\n`);
    process.stdout.write(`订单号：${state.outTradeNo || '<未返回>'}\n`);
    process.stdout.write(`金额：${state.amount} ${state.currency}\n`);
    process.stdout.write(`资源地址：${url}\n`);
    process.stdout.write(`账单文件（仅本人可读）：${challengeFile}\n`);
    process.stdout.write(`状态文件（同订单复用）：${stateFile}\n`);
    process.stdout.write('\n下一步：确认用户同意付款后执行\n');
    process.stdout.write(`  node $SKILL_DIR/scripts/travel_aipay.mjs pay --confirm\n`);
    process.stdout.write('\n付款后取货（不要重新付款）：\n');
    process.stdout.write(`  node $SKILL_DIR/scripts/travel_aipay.mjs complete --out-shake-no '<官方查询单号>'\n`);
    printJson(state);
    return EXIT_OK;
  }

  if (status === 200) {
    process.stdout.write('资源已直接返回（未产生账单）：\n');
    process.stdout.write(`${renderResult(extractTravelResult(payload))}\n`);
    return EXIT_OK;
  }

  process.stderr.write(`预期 402（返回账单），实际 HTTP ${status}\n${text.slice(0, 2000)}\n`);
  return status >= 500 ? EXIT_SERVER_ERROR : EXIT_PARAM;
}

// ---------------------------------------------------------------------------
// pay：调用官方 CLI 发起支付（须显式 --confirm）
// ---------------------------------------------------------------------------

async function cmdPay(flags) {
  if (!flags.confirm) {
    process.stderr.write('未确认付款：需用户在本次对话中明确同意后，才可加 --confirm 执行。\n');
    return EXIT_PARAM;
  }

  const dir = stateDir(flags);
  const state = readState(dir);

  const sessionId = resolveSessionId(flags);
  if (!sessionId) {
    process.stderr.write('运行时未提供当前会话标识：请通过 --session-id 传入当前会话标识。\n');
    return EXIT_PARAM;
  }

  const bodyText = readBodyFile(state);
  const intent = `原始请求：用户请求仙踪问道旅行咨询（${String(state.query || '').slice(0, 60)}）`;

  const args = [
    '402-buyer-pay',
    '--session-id',
    sessionId,
    '--file',
    state.challengeFile,
    '--resource-url',
    state.resourceUrl,
    '--method',
    'POST',
    '--data',
    bodyText,
    '--header',
    'Content-Type: application/json',
    '--intent-summary',
    intent,
  ];

  const result = await runAlipayBot(args);
  return result.exitCode === 0 ? EXIT_OK : 1;
}

// ---------------------------------------------------------------------------
// complete：付款后取资源
// ---------------------------------------------------------------------------

const DEFAULT_POLL_INTERVAL_MS = 40000;
const DEFAULT_MAX_WAIT_MS = 900000;

function positiveInt(value, fallback) {
  const num = Number(value);
  return Number.isFinite(num) && num > 0 ? Math.floor(num) : fallback;
}

/** 从 CLI stdout 中取出 JSON（官方 --output json 可能夹带其他输出） */
function extractJsonObject(text) {
  const direct = parseJson(String(text || '').trim());
  if (direct) return direct;
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start === -1 || end <= start) return null;
  return parseJson(text.slice(start, end + 1));
}

/**
 * 判定官方 402-query-payment-status 的 JSON 载荷。
 *
 * 【关键，2026-11-14 实测踩坑】成功载荷**没有** `resourceDelivered` 字段：
 *   成功   { success: true,  resourceResponse: { status: 200, body: { content, already_fulfilled, ... } } }
 *   生成中 { errorCode: RESOURCE_REQUEST_FAILED/DELIVERY_FAILED, errorMessage: "...returned HTTP 409", resourceResponse: { status: 409 } }
 *   瞬断   { errorCode: RESOURCE_REQUEST_FAILED, resourceResponse: null }   ← 服务重启/网络，重试即可
 * `resourceDelivered` 既不是 402 协议字段，也不是官方文档化约定，只是 CLI 结果信封的内部字段
 * （二进制里 `json:"resourceDelivered"` 与 `json:"resourceDelivered,omitempty"` 并存，成功路径会被省略），
 * 只能用于诊断。因此不能用它判成功，也不要用 CLI 退出码判断资源是否已交付。
 */
function classifyQueryPayload(payload) {
  if (!payload || typeof payload !== 'object') return { kind: 'unknown', note: '官方查询未返回可解析的 JSON' };
  const status = payload.resourceResponse?.status;
  if (status === 200) {
    if (payload.success === false) return { kind: 'business_fail', status, note: payload.errorMessage || '' };
    // 服务端业务响应已显式给出 resourceDelivered（成功 true / 生成中 false），
    // 若为 false 说明交付链路异常，按可重试处理
    if (payload.resourceResponse?.body?.resourceDelivered === false) {
      return { kind: 'transient', status, note: '服务端响应 resourceDelivered=false' };
    }
    return { kind: 'delivered', status };
  }
  if (status === 409) return { kind: 'generating', status };
  if (status === 402) return { kind: 'need_pay', status };
  if (status === 400) return { kind: 'param', status, note: payload.errorMessage || '' };
  if (typeof status === 'number' && status >= 500) return { kind: 'server_error', status };
  if (payload.resourceResponse === null || payload.resourceResponse === undefined) {
    return { kind: 'transient', note: payload.errorMessage || payload.errorCode || '' };
  }
  return { kind: 'unknown', status, note: payload.errorMessage || '' };
}

/** 从查询载荷中取出业务结果（body.content 是业务 JSON 字符串） */
function travelResultFromQueryPayload(payload) {
  const body = payload?.resourceResponse?.body;
  if (!body) return null;
  const raw = body.content !== undefined ? body.content : body;
  const parsed = typeof raw === 'string' ? extractJsonObject(raw) : raw;
  return extractTravelResult(parsed) || (parsed && typeof parsed === 'object' ? parsed : null);
}

/** 路径 A：官方查询（命令自身在资源非空时自动发履约回执） */
async function completeViaQuery(flags, dir, state, { outShakeNo, tradeNo }) {
  const wait = Boolean(flags.wait);
  const pollIntervalMs = positiveInt(flags['poll-interval-ms'], DEFAULT_POLL_INTERVAL_MS);
  const maxWaitMs = positiveInt(flags['max-wait-ms'], DEFAULT_MAX_WAIT_MS);
  const deadline = Date.now() + maxWaitMs;
  let attempt = 0;

  for (;;) {
    attempt += 1;
    const args = ['402-query-payment-status'];
    if (outShakeNo) args.push('--out-shake-no', outShakeNo);
    else args.push('--trade-no', tradeNo);
    args.push(
      '--resource-url',
      state.resourceUrl,
      '--method',
      'POST',
      '--data',
      readBodyFile(state),
      '--header',
      'Content-Type: application/json',
      '--output',
      'json',
    );

    const { exitCode, stdout, stderr } = await runAlipayBot(args, { quiet: true });
    const payload = extractJsonObject(stdout);
    const verdict = classifyQueryPayload(payload);

    if (verdict.kind === 'delivered') {
      const result = travelResultFromQueryPayload(payload);
      const business = result?.resp_code;
      if (business !== undefined && business !== 200) {
        const raw = payload?.resourceResponse?.body ?? payload;
        writePrivate(path.join(dir, 'delivery.json'), JSON.stringify(raw, null, 2));
        process.stderr.write(`═══ 业务失败（已完成验付）═══\nresp_message：${result?.resp_message || ''}\n`);
        return EXIT_BUSINESS_FAIL;
      }
      const body = payload?.resourceResponse?.body || {};
      writePrivate(path.join(dir, 'delivery.json'), JSON.stringify(result || body, null, 2));
      process.stdout.write('═══ 交付成功 ═══\n');
      process.stdout.write(`资源：${body.resource_id || ''}\n`);
      process.stdout.write(`订单号：${body.out_trade_no || payload?.bizNo || ''}\n`);
      process.stdout.write(`交易号：${body.trade_no || payload?.tradeNo || ''}\n`);
      process.stdout.write(`同一订单幂等重放：${body.already_fulfilled ? '是' : '否'}\n`);
      process.stdout.write(`履约回执已发送：${body.fulfillment_confirmed ? '是' : '否（资源已交付，不影响取货）'}\n`);
      if (body.resourceDelivered !== undefined) process.stdout.write(`资源交付标记：resourceDelivered=${body.resourceDelivered}\n`);
      if (attempt > 1) process.stdout.write(`轮询次数：${attempt}\n`);
      if (result) process.stdout.write(`\n${renderResult(result)}\n`);
      return EXIT_OK;
    }

    const retryable = verdict.kind === 'generating' || verdict.kind === 'transient';
    const note = verdict.kind === 'generating' ? '方案生成中' : verdict.kind === 'transient' ? '服务端瞬时不可用（多为发布/重启或网络瞬断）' : '';
    if (!wait || !retryable || Date.now() + pollIntervalMs > deadline) {
      if (verdict.kind === 'generating') {
        process.stderr.write('═══ 支付已确认，方案生成中 ═══\n');
        process.stderr.write(`轮询第 ${attempt} 次：${note}；已付金额不会重复扣除，请勿重新付款。\n`);
        process.stderr.write(`继续等待：在同一条命令后加 --wait（或每隔 ${Math.round(pollIntervalMs / 1000)} 秒用【同一订单号】再查一次）。\n`);
        process.stderr.write('生成成功后会返回正文与 PDF 链接，同时 PDF 会自动发送到请求中填写的邮箱。\n');
        return EXIT_IN_PROGRESS;
      }
      if (verdict.kind === 'transient') {
        process.stderr.write('═══ 服务端瞬时不可用（资源未交付）═══\n');
        process.stderr.write(`轮询第 ${attempt} 次：${note}${verdict.note ? `（${verdict.note}）` : ''}\n`);
        process.stderr.write('不要重新付款；原样重跑本命令（或加 --wait 自动重试）即可。\n');
        return EXIT_SERVER_ERROR;
      }
      if (verdict.kind === 'need_pay') {
        process.stderr.write('═══ 凭证无效或已失效，返回新账单 ═══\n');
        process.stderr.write('不要重复付款；如需继续，请用本次新账单重新走支付确认流程。\n');
        return EXIT_NEED_PAY;
      }
      if (verdict.kind === 'param') {
        process.stderr.write(`═══ 请求被拒（未产生资源）═══\n${verdict.note || ''}\n`);
        return EXIT_PARAM;
      }
      if (verdict.kind === 'server_error') {
        process.stderr.write(`服务端错误 HTTP ${verdict.status}，原样重试一次；仍失败请报告服务端。\n`);
        return EXIT_SERVER_ERROR;
      }
      if (verdict.kind === 'business_fail') {
        process.stderr.write(`═══ 业务失败（已完成验付）═══\n${verdict.note || ''}\n`);
        return EXIT_BUSINESS_FAIL;
      }
      process.stderr.write(`未预期的查询结果（exit=${exitCode}）\nstdout=${String(stdout || '').slice(0, 500)}\nstderr=${String(stderr || '').slice(0, 500)}\n`);
      return EXIT_PARAM;
    }

    process.stderr.write(`[${attempt}] ${note}，${Math.round(pollIntervalMs / 1000)} 秒后重试（同一订单，不会重复扣费）…\n`);
    await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
  }
}

async function cmdComplete(flags) {
  const dir = stateDir(flags);

  // 路径 A（推荐）：官方查询原订单，命令自身会在资源非空时自动发履约回执
  if (!flags.proof) {
    const outShakeNo = String(flags['out-shake-no'] || '').trim();
    const tradeNo = String(flags['trade-no'] || '').trim();
    if (!outShakeNo && !tradeNo) {
      process.stderr.write('缺少查询单号：请传入官方 CLI 输出的 --out-shake-no（或 --trade-no）。\n');
      return EXIT_PARAM;
    }

    let state = null;
    try {
      state = readState(dir);
    } catch {
      state = null;
    }
    if (!state) {
      process.stderr.write('找不到本单状态文件：请先用 probe 生成同订单请求。\n');
      return EXIT_PARAM;
    }

    return completeViaQuery(flags, dir, state, { outShakeNo, tradeNo });
  }

  // 路径 B：带官方凭证直取
  const proof = String(flags.proof).trim();
  const bodyFile = flags['body-file'] ? String(flags['body-file']) : path.join(dir, 'body.json');
  if (!fs.existsSync(bodyFile)) {
    process.stderr.write(`找不到请求体文件：${bodyFile}，请先执行 probe\n`);
    return EXIT_PARAM;
  }
  const bodyText = fs.readFileSync(bodyFile, 'utf8');
  const url = String(flags['resource-url'] || (fs.existsSync(path.join(dir, 'state.json')) ? readState(dir).resourceUrl : RESOURCE_URL)).trim();

  if (flags['dry-run']) {
    process.stdout.write('[dry-run] 以下请求未发送：\n');
    printJson({ method: 'POST', url, headers: { 'Content-Type': 'application/json', [HEADER_PAYMENT_PROOF]: '<已隐去>' }, body: JSON.parse(bodyText) });
    return EXIT_OK;
  }

  const { status, headers, text } = await postResource(url, JSON.parse(bodyText), {
    headers: { [HEADER_PAYMENT_PROOF]: proof },
    timeout: timeoutMs(flags),
  });
  const payload = parseJson(text);

  writePrivate(path.join(dir, 'delivery.json'), text);

  if (status === 200) {
    const result = extractTravelResult(payload);
    const business = result?.resp_code;
    if (business !== undefined && business !== 200) {
      process.stderr.write(`═══ 业务失败（已完成验付）═══\nresp_message：${result.resp_message || ''}\n`);
      return EXIT_BUSINESS_FAIL;
    }
    process.stdout.write('═══ 交付成功 ═══\n');
    process.stdout.write(`资源：${payload.resource_id || ''}\n`);
    process.stdout.write(`订单号：${payload.out_trade_no || ''}\n`);
    process.stdout.write(`交易号：${payload.trade_no || ''}\n`);
    process.stdout.write(`同一订单幂等重放：${payload.already_fulfilled ? '是' : '否'}\n`);
    process.stdout.write(`履约回执已发送：${payload.fulfillment_confirmed ? '是' : '否（资源已交付，不影响取货）'}\n`);
    const validation = headers.get(HEADER_PAYMENT_VALIDATION);
    if (validation) process.stdout.write(`${HEADER_PAYMENT_VALIDATION}：${validation}\n`);
    process.stdout.write(`\n${renderResult(result)}\n`);
    return EXIT_OK;
  }

  if (status === 409) {
    process.stderr.write('═══ 支付已确认，方案生成中 ═══\n');
    process.stderr.write(`状态码：${payload?.code || 'UNKNOWN'}\n说明：${payload?.message || ''}\n`);
    const retryAfter = headers.get('Retry-After') || '30';
    process.stderr.write(`专业方案通常需要 2–3 分钟；建议每隔 ${retryAfter} 秒用【同一订单号】查一次进度（不要重新付款、不要更换请求体）\n`);
    if (payload?.out_trade_no) {
      process.stderr.write(`订单号：${payload.out_trade_no}\n`);
      process.stderr.write(`查询命令：node "$SKILL_DIR/scripts/travel_aipay.mjs" complete --out-shake-no '${payload.out_trade_no}'\n`);
    }
    process.stderr.write('生成成功后会返回正文与 PDF 链接，同时 PDF 会自动发送到请求中填写的邮箱。\n');
    return EXIT_IN_PROGRESS;
  }

  if (status === 402) {
    process.stderr.write('═══ 凭证无效或已失效，返回新账单 ═══\n');
    process.stderr.write(`说明：${payload?.message || ''}\n`);
    process.stderr.write('不要重复付款；如需继续，请用本次新账单重新走支付确认流程。\n');
    return EXIT_NEED_PAY;
  }

  if (status === 400) {
    process.stderr.write(`═══ 请求被拒（未产生资源）═══\ncode=${payload?.code || ''} message=${payload?.message || ''}\n`);
    return EXIT_PARAM;
  }

  if (status >= 500) {
    process.stderr.write(`服务端错误 HTTP ${status}：${String(text || '').slice(0, 500)}\n`);
    return EXIT_SERVER_ERROR;
  }

  process.stderr.write(`未预期的 HTTP ${status}：${String(text || '').slice(0, 500)}\n`);
  return EXIT_PARAM;
}

// ---------------------------------------------------------------------------
// 结果解析与展示
// ---------------------------------------------------------------------------

/**
 * 兼容三种输入：
 * - 交付响应体 {resource_id, content(JSON 字符串), ...}
 * - 直接是旅行咨询结果 {resp_code, resp_message, data}
 * - 已是 data 字段 {content, pdf_oss_file_url, ...}
 */
function extractTravelResult(payload) {
  if (!payload || typeof payload !== 'object') return null;
  if ('resp_code' in payload) return payload;
  const content = payload.content;
  if (typeof content === 'string' && content.trim()) {
    const parsed = parseJson(content);
    if (parsed && typeof parsed === 'object') return parsed;
  }
  if (content && typeof content === 'object') return { resp_code: 200, ...content };
  if (payload.data) return { resp_code: 200, data: payload.data };
  return payload.data ? payload : null;
}

function renderResult(result) {
  if (!result) return '（未能解析交付结果）';
  const data = result.data || {};
  const lines = [];
  if (data.travel_destination) lines.push(`目的地：${data.travel_destination}`);
  lines.push(`模型：${data.model_name || 'deepseek'}`);

  const pdfUrl = String(data.pdf_oss_file_url || '').trim();
  if (pdfUrl) {
    lines.push(`PDF 方案：${pdfUrl}`);
    lines.push('  （链接有效期约 90 天；同时已发送到请求中填写的邮箱）');
  } else {
    lines.push('PDF 方案：未生成（正文仍可正常使用）');
  }
  const refs = data.ref_travel_infos || [];
  if (refs.length) lines.push(`参考资料：${refs.length} 条`);
  lines.push('');
  lines.push(String(data.content || '').trim() || '（正文为空）');
  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// render
// ---------------------------------------------------------------------------

function cmdRender(flags) {
  const source = flags.response ? String(flags.response) : path.join(stateDir(flags), 'delivery.json');
  if (!fs.existsSync(source)) {
    process.stderr.write(`找不到响应文件：${source}\n`);
    return EXIT_PARAM;
  }
  const payload = parseJson(fs.readFileSync(source, 'utf8'));
  if (!payload) {
    process.stderr.write('输入不是合法 JSON\n');
    return EXIT_PARAM;
  }
  const result = extractTravelResult(payload);
  if (!result) {
    process.stderr.write('未识别到旅行咨询结果结构\n');
    return EXIT_PARAM;
  }
  if (result.resp_code !== undefined && result.resp_code !== 200) {
    process.stderr.write(`业务失败：${result.resp_message || ''}\n`);
    return EXIT_BUSINESS_FAIL;
  }
  process.stdout.write(`${renderResult(result)}\n`);
  return EXIT_OK;
}

// ---------------------------------------------------------------------------

async function main() {
  const { command, flags } = parseArgs(process.argv.slice(2));

  switch (command) {
    case 'body':
      return cmdBody(flags);
    case 'probe':
      return cmdProbe(flags);
    case 'pay':
      return cmdPay(flags);
    case 'complete':
      return cmdComplete(flags);
    case 'render':
      return cmdRender(flags);
    case 'help':
    case undefined:
      process.stdout.write(HELP);
      return command === undefined ? EXIT_PARAM : EXIT_OK;
    default:
      process.stderr.write(`未知子命令：${command}\n\n${HELP}`);
      return EXIT_PARAM;
  }
}

main().then(
  (code) => process.exit(code),
  (error) => {
    process.stderr.write(`执行失败：${error.message}\n`);
    process.exit(EXIT_SERVER_ERROR);
  },
);
