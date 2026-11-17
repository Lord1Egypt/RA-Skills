#!/usr/bin/env node
/**
 * Second Reality Video — Open Client（probe / pay / complete / status）
 *
 * 协议（支付宝 AI 按量付费官方契约）
 * ---------------------------------
 * 1. probe    —— POST 资源端点（不带 Payment-Proof）→ HTTP 402 + `Payment-Needed`
 *                 头（Base64URL 的账单，protocol / method 两层）；
 * 2. pay      —— 把账单整理成结构化付款请求，交给 **官方支付能力**
 *                 （alipay-bot / alipay-payment-skill）完成付款；
 * 3. complete —— 携 `Payment-Proof` **重放同一请求** → HTTP 200 + 资源内容 +
 *                 `Payment-Validation` 头；随后按产物清单下载文件。
 *
 * 支付原则
 * --------
 * 本脚本**不实现付款、不接触支付密钥、不自行签名**；付款一律由官方支付能力完成。
 * 状态不明时不要重新下单：同一笔 `Payment-Proof` 可以安全重放（服务端按订单幂等，
 * 不会重复扣费，也不会重复发资源）。
 *
 * 退出码：0 成功 / 2 需要付款（402） / 3 付款凭证无效（401） / 4 其它错误
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, chmodSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';
import process from 'node:process';

const EXIT_OK = 0;
const EXIT_NEEDS_PAYMENT = 2;
const EXIT_BAD_PROOF = 3;
const EXIT_ERROR = 4;

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    } else {
      args._.push(token);
    }
  }
  return args;
}

function required(args, name, fallback) {
  const value = args[name];
  if (value === undefined || value === true || value === '') {
    if (fallback !== undefined) return fallback;
    throw new Error(`缺少参数 --${name}`);
  }
  return value;
}

function parseTicks(spec) {
  const [from, to] = String(spec).split('-');
  const tickFrom = Number.parseInt(from, 10);
  const tickTo = to === undefined ? tickFrom : Number.parseInt(to, 10);
  if (!Number.isFinite(tickFrom) || !Number.isFinite(tickTo) || tickTo < tickFrom) {
    throw new Error(`非法 ticks: ${spec}（应为 from-to）`);
  }
  return { tickFrom, tickTo };
}

function parseResolution(spec) {
  const [w, h] = String(spec).split('x').map((part) => Number.parseInt(part, 10));
  if (!Number.isFinite(w) || !Number.isFinite(h)) {
    throw new Error(`非法 resolution: ${spec}（应为 WxH）`);
  }
  return [w, h];
}

function statePath(stateDir, sessionId) {
  return join(resolve(stateDir), `${sessionId}.json`);
}

function saveState(stateDir, sessionId, state) {
  const target = statePath(stateDir, sessionId);
  mkdirSync(resolve(stateDir), { recursive: true });
  writeFileSync(target, JSON.stringify(state, null, 2), 'utf8');
  try {
    chmodSync(target, 0o600); // POSIX：账单与订单信息只给本人读
  } catch {
    /* Windows 上无意义，忽略 */
  }
  return target;
}

function loadState(stateDir, sessionId) {
  const target = statePath(stateDir, sessionId);
  if (!existsSync(target)) {
    throw new Error(`找不到会话状态：${target}（先跑 probe）`);
  }
  return JSON.parse(readFileSync(target, 'utf8'));
}

function decodeBill(raw) {
  if (!raw) return null;
  try {
    return JSON.parse(Buffer.from(raw, 'base64url').toString('utf8'));
  } catch {
    return null;
  }
}

function apiBase(args) {
  const base = String(required(args, 'api-base', process.env.SRV_API_BASE || '')).replace(/\/+$/, '');
  if (!base) throw new Error('缺少 --api-base（或设置 SRV_API_BASE）');
  return base;
}

function buildRequestBody(args) {
  const { tickFrom, tickTo } = parseTicks(required(args, 'ticks', '0-149'));
  return {
    world_id: required(args, 'world-id', 'sr-video-demo'),
    genesis_seed: Number.parseInt(required(args, 'seed', '42'), 10),
    agent_count: Number.parseInt(required(args, 'agents', '5'), 10),
    tick_from: tickFrom,
    tick_to: tickTo,
    framing: {
      resolution: parseResolution(required(args, 'resolution', '854x480')),
      fps: Number.parseInt(required(args, 'fps', '30'), 10),
    },
    samples: Number.parseInt(required(args, 'samples', '3'), 10),
    tier: required(args, 'render-tier', 'R1'),
    shot: { preset: required(args, 'shot', 'demo') },
  };
}

async function callResource(state, { proof } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (proof) headers['Payment-Proof'] = proof;
  const response = await fetch(state.url, {
    method: 'POST',
    headers,
    body: JSON.stringify(state.request_body),
  });
  const text = await response.text();
  let payload = null;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {
    payload = { raw: text.slice(0, 500) };
  }
  const validation = response.headers.get('payment-validation');
  let validationBody = null;
  if (validation) {
    try {
      validationBody = JSON.parse(Buffer.from(validation, 'base64url').toString('utf8'));
    } catch {
      validationBody = null;
    }
  }
  return { response, payload, validationBody };
}

/* ------------------------------------------------------------------ 子命令 */

async function cmdProbe(args) {
  const base = apiBase(args);
  const state = {
    api_base: base,
    url: `${base}/api/v1/render`,
    request_body: buildRequestBody(args),
    session_id: required(args, 'session-id', 'default'),
    created_at: new Date().toISOString(),
  };

  const { response, payload } = await callResource(state);
  if (response.status === 402) {
    const bill = decodeBill(response.headers.get('payment-needed')) || payload?.bill || null;
    if (!bill || !bill.protocol || !bill.method) {
      console.error('服务端返回 402 但没有可解析的账单（Payment-Needed 头缺失或结构不符）。');
      return EXIT_ERROR;
    }
    state.bill = bill;
    state.out_trade_no = bill.protocol.out_trade_no;
    const file = saveState(args['state-dir'] || '.state', state.session_id, state);
    console.log(JSON.stringify({
      status: 'payment_required',
      out_trade_no: state.out_trade_no,
      amount: bill.protocol.amount,
      currency: bill.protocol.currency,
      service_id: bill.method.service_id,
      resource_id: bill.protocol.resource_id,
      pay_before: bill.protocol.pay_before,
      state_file: file,
      next: '运行 pay 子命令，把账单交给官方支付能力；付款后运行 complete 子命令。',
    }, null, 2));
    return EXIT_NEEDS_PAYMENT;
  }

  if (!response.ok) {
    console.error(`请求失败：HTTP ${response.status}`, JSON.stringify(payload, null, 2));
    return EXIT_ERROR;
  }

  // 已经付款（同一订单重放）：直接给出资源
  state.out_trade_no = payload?.out_trade_no;
  const file = saveState(args['state-dir'] || '.state', state.session_id, state);
  console.log(JSON.stringify({
    status: 'delivered',
    out_trade_no: state.out_trade_no,
    resource_id: payload?.resource_id,
    already_fulfilled: payload?.already_fulfilled,
    state_file: file,
  }, null, 2));
  return EXIT_OK;
}

async function cmdPay(args) {
  const state = loadState(args['state-dir'] || '.state', required(args, 'session-id', 'default'));
  if (!state.bill) {
    console.error('会话状态里没有账单，先跑 probe。');
    return EXIT_ERROR;
  }
  const { protocol, method } = state.bill;
  console.log(JSON.stringify({
    action: 'request_payment',
    note: '把本段交给官方支付能力（alipay-bot / alipay-payment-skill）执行；本脚本不发起付款。',
    bill: state.bill,
    payment: {
      out_trade_no: protocol.out_trade_no,
      amount: protocol.amount,
      currency: protocol.currency,
      resource_id: protocol.resource_id,
      pay_before: protocol.pay_before,
      service_id: method.service_id,
      seller_id: method.seller_id,
      goods_name: method.goods_name,
    },
  }, null, 2));
  return EXIT_OK;
}

async function cmdComplete(args) {
  const state = loadState(args['state-dir'] || '.state', required(args, 'session-id', 'default'));
  const proof = required(args, 'payment-proof');
  const outDir = resolve(args['out-dir'] || './out');
  mkdirSync(outDir, { recursive: true });

  const { response, payload, validationBody } = await callResource(state, { proof });
  if (response.status === 402) {
    console.error('订单仍需付款（凭证无效或账单已过期），请重新 probe 获取新账单。', JSON.stringify(payload, null, 2));
    return EXIT_NEEDS_PAYMENT;
  }
  if (response.status === 401) {
    console.error('付款凭证无效，服务端未交付资源。', JSON.stringify(payload, null, 2));
    return EXIT_BAD_PROOF;
  }
  if (!response.ok) {
    console.error(`请求失败：HTTP ${response.status}`, JSON.stringify(payload, null, 2));
    return EXIT_ERROR;
  }
  if (!payload || !payload.resource_id || !payload.content) {
    console.error('响应缺少 resource_id / content：', JSON.stringify(payload, null, 2));
    return EXIT_ERROR;
  }
  if (!validationBody || validationBody.validated !== true) {
    console.error('缺少有效的 Payment-Validation 头，资源归属无法确认。');
    return EXIT_ERROR;
  }

  const content = typeof payload.content === 'string'
    ? JSON.parse(payload.content)
    : payload.content;
  const artifacts = Array.isArray(content.artifacts) ? content.artifacts : [];

  const downloaded = [];
  for (const artifact of artifacts) {
    const target = join(outDir, artifact.name);
    const res = await fetch(`${state.api_base}${artifact.url}`);
    if (!res.ok) {
      console.error(`产物下载失败：${artifact.name} HTTP ${res.status}`);
      return EXIT_ERROR;
    }
    const buffer = Buffer.from(await res.arrayBuffer());
    writeFileSync(target, buffer);
    const digest = createHash('sha256').update(buffer).digest('hex');
    downloaded.push({
      name: artifact.name,
      path: target,
      bytes: buffer.length,
      sha256: digest,
      verified: !artifact.sha256 || digest === artifact.sha256,
    });
  }

  console.log(JSON.stringify({
    status: 'delivered',
    out_trade_no: payload.out_trade_no,
    trade_no: payload.trade_no,
    resource_id: payload.resource_id,
    fulfillment_confirmed: payload.fulfillment_confirmed,
    already_fulfilled: payload.already_fulfilled,
    manifest: content.manifest || null,
    out_dir: outDir,
    artifacts: downloaded,
  }, null, 2));
  return EXIT_OK;
}

async function cmdStatus(args) {
  const state = loadState(args['state-dir'] || '.state', required(args, 'session-id', 'default'));
  console.log(JSON.stringify({
    note: '本服务按官方按量付费协议不提供订单查询端点；状态不明时用同一 Payment-Proof 重放同一请求即可（服务端幂等，不会重复扣费或重复发资源）。',
    session_id: state.session_id,
    out_trade_no: state.out_trade_no || (state.bill?.protocol?.out_trade_no) || null,
    amount: state.bill?.protocol?.amount || null,
    api_base: state.api_base,
    created_at: state.created_at,
  }, null, 2));
  return EXIT_OK;
}

const COMMANDS = {
  probe: cmdProbe,
  pay: cmdPay,
  complete: cmdComplete,
  status: cmdStatus,
};

async function main() {
  const argv = process.argv.slice(2);
  const command = argv[0];
  if (!command || command === '--help' || command === '-h') {
    console.log('用法：node scripts/second-reality-video-paid.mjs <probe|pay|complete|status> [options]');
    console.log('常用参数：--api-base --world-id --seed --agents --ticks --resolution --fps --shot');
    console.log('          --state-dir --session-id --payment-proof --out-dir');
    return EXIT_OK;
  }
  const handler = COMMANDS[command];
  if (!handler) {
    console.error(`未知子命令：${command}`);
    return EXIT_ERROR;
  }
  return handler(parseArgs(argv.slice(1)));
}

main()
  .then((code) => process.exit(code))
  .catch((error) => {
    console.error(String(error?.message || error));
    process.exit(EXIT_ERROR);
  });
