#!/usr/bin/env node
/**
 * Prana 封装技能 — Node 薄客户端（与 prana_skill_client.py 行为对齐）
 * 依赖：Node 20.10+；包根目录 npm install yaml；无根 package.json 时需 NODE_OPTIONS=--experimental-default-type=module
 * 本文件为 ES Module（import / export）
 */
import { randomUUID } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..');
const SKILL_MD_FILE = path.join(SKILL_ROOT, 'SKILL.md');

// 封装打包时由服务端替换为对象；仓库模板为 null
const ENCAPSULATION_EMBEDDED = {"public_skill_key": "test_txt_public", "original_skill_key": "test_txt", "encapsulation_target": "claw_hub"};

const DEFAULT_PRANA_BASE = 'https://claw-uat.ebonex.io/';

const HTTP_TIMEOUT_MS = 7200 * 1000;
const AGENT_RESULT_POLL_INTERVAL_SEC = Number.parseInt(
  process.env.PRANA_AGENT_RESULT_POLL_INTERVAL_SEC || '120',
  10,
);
const AGENT_RESULT_POLL_MAX_ATTEMPTS = Number.parseInt(
  process.env.PRANA_AGENT_RESULT_POLL_MAX_ATTEMPTS || '20',
  10,
);
const API_KEYS_FETCH_TIMEOUT_MS = 60 * 1000;

function normalizeEncapsulationTarget(raw) {
  let s = (raw || '').trim().toLowerCase().replace(/-/g, '_');
  if (!s) return 'prana';
  const aliases = { clawhub: 'claw_hub', openclaw: 'claw_hub', open_claw: 'claw_hub' };
  const key = aliases[s] || s;
  return key.length > 64 ? key.slice(0, 64) : key;
}

function loadEncapsulationRuntime() {
  if (ENCAPSULATION_EMBEDDED && typeof ENCAPSULATION_EMBEDDED === 'object') {
    return { ...ENCAPSULATION_EMBEDDED };
  }
  return null;
}

let YAML;
try {
  YAML = (await import('yaml')).default;
} catch {
  YAML = null;
}

function extractFrontmatter(content) {
  const trimmed = content.trimStart();
  if (!trimmed.startsWith('---')) return [null, content];
  const re = /^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n([\s\S]*)$/;
  const m = trimmed.match(re);
  if (!m) return [null, content];
  if (!YAML) {
    console.error('错误: 解析 SKILL.md 需要依赖 yaml。请在技能包根目录执行: npm install');
    process.exit(1);
  }
  try {
    const fm = YAML.parse(m[1]);
    return [fm && typeof fm === 'object' ? fm : null, m[2]];
  } catch {
    return [null, content];
  }
}

function loadSkillConfig() {
  if (!fs.existsSync(SKILL_MD_FILE)) {
    console.error('错误: 未找到 SKILL.md，请使用完整封装技能包解压后运行。');
    process.exit(1);
  }
  const runtime = loadEncapsulationRuntime();
  const raw = fs.readFileSync(SKILL_MD_FILE, 'utf8');
  const [frontmatter] = extractFrontmatter(raw);
  if (!frontmatter) {
    console.error('错误: SKILL.md 缺少有效的 YAML frontmatter。');
    process.exit(1);
  }
  let original = String((runtime && runtime.original_skill_key) || '').trim();
  const pubFm = String(frontmatter.original_skill_key || '').trim();
  const pubKeyFm = String(frontmatter.skill_key || '').trim();
  if (!original) original = pubFm;
  let pub = String((runtime && runtime.public_skill_key) || '').trim();
  if (!pub) pub = pubKeyFm;
  const sk = original || pub;
  if (!sk) {
    console.error(
      '错误: 缺少远端技能标识。请使用服务端封装生成的技能包（脚本内已写入 ENCAPSULATION_EMBEDDED），' +
        '或为旧版包在 SKILL.md frontmatter 中保留 original_skill_key / skill_key。',
    );
    process.exit(1);
  }
  let sip = '';
  for (const key of ['input_format', 'input_schema', 'params']) {
    const v = frontmatter[key];
    if (v != null && String(v).trim()) {
      sip = String(v).trim().slice(0, 16000);
      break;
    }
  }
  if (!sip) {
    const d = frontmatter.description;
    if (d != null && String(d).trim()) sip = String(d).trim().slice(0, 8000);
  }
  const enc = normalizeEncapsulationTarget(
    String(
      (runtime && runtime.encapsulation_target) ||
        frontmatter.encapsulation_target ||
        '',
    ),
  );
  return { skill_key: sk, skill_invocation_params: sip, encapsulation_target: enc };
}

function parseCredentialsJson(text) {
  const t = text.trim();
  if (!t.startsWith('{')) return null;
  try {
    const obj = JSON.parse(t);
    if (!obj || typeof obj !== 'object') return null;
    const data = obj.data;
    let ak = null;
    if (data && typeof data === 'object') ak = data.api_key;
    if (ak && typeof ak === 'object' && ak.public_key && ak.secret_key) {
      return [String(ak.public_key).trim(), String(ak.secret_key).trim()];
    }
    ak = obj.api_key;
    if (ak && typeof ak === 'object' && ak.public_key && ak.secret_key) {
      return [String(ak.public_key).trim(), String(ak.secret_key).trim()];
    }
    if (obj.public_key && obj.secret_key) {
      return [String(obj.public_key).trim(), String(obj.secret_key).trim()];
    }
  } catch {
    return null;
  }
  return null;
}

function parseCredentialsLine(line) {
  line = line.trim();
  if (!line || line.startsWith('#')) return null;
  const i = line.indexOf(':');
  if (i === -1) return null;
  const pub = line.slice(0, i).trim();
  const sec = line.slice(i + 1).trim();
  if (pub && sec) return [pub, sec];
  return null;
}

function headersXApiKey(publicKey, secretKey) {
  return {
    'Content-Type': 'application/json',
    'x-api-key': `${publicKey}:${secretKey}`,
  };
}

function buildApiKeysFetchUrl(baseUrl) {
  const root = baseUrl.replace(/\/+$/, '');
  let path = `${root}/api/v1/api-keys`;
  return path;
}

async function fetchPranaApiKeysViaGet(baseUrl) {
  const url = buildApiKeysFetchUrl(baseUrl);
  try {
    const res = await fetch(url, {
      method: 'GET',
      signal: AbortSignal.timeout(API_KEYS_FETCH_TIMEOUT_MS),
    });
    const text = await res.text();
    if (!res.ok) {
      console.error(`错误: 自动获取 API key 失败（HTTP ${res.status}）：${text.slice(0, 2000)}`);
      return null;
    }
    const parsed = parseCredentialsJson(text);
    if (!parsed) {
      console.error('错误: 自动获取 API key 成功但响应无法解析出 public_key/secret_key。');
      return null;
    }
    return parsed;
  } catch (e) {
    console.error(`错误: 自动获取 API key 失败（网络）：${e && e.message ? e.message : e}`);
    return null;
  }
}

function syncPranaKeysIntoEnv(pub, sec) {
  const pk = String(pub || '').trim();
  const sk = String(sec || '').trim();
  if (pk && sk) {
    process.env.PRANA_SKILL_PUBLIC_KEY = pk;
    process.env.PRANA_SKILL_SECRET_KEY = sk;
  }
  return [pk, sk];
}

/** 调用 agent-run 前：仅从环境解析 pk/sk（不请求网络）。 */
function credentialsFromEnvironment() {
  const pk = (process.env.PRANA_SKILL_PUBLIC_KEY || '').trim();
  const sk = (process.env.PRANA_SKILL_SECRET_KEY || '').trim();
  if (pk && sk) return [pk, sk];

  const rawEnv = (process.env.PRANA_SKILL_API_KEY || '').trim();
  if (rawEnv) {
    const parsed = parseCredentialsJson(rawEnv);
    if (parsed) return parsed;
    const pl = parseCredentialsLine(rawEnv);
    if (pl) return pl;
  }
  return null;
}

async function loadPranaCredentials(pranaBaseUrl) {
  const epk = (process.env.PRANA_SKILL_PUBLIC_KEY || '').trim();
  const esk = (process.env.PRANA_SKILL_SECRET_KEY || '').trim();
  if ((epk && !esk) || (esk && !epk)) {
    console.error(
      '提示: PRANA_SKILL_PUBLIC_KEY 与 PRANA_SKILL_SECRET_KEY 须成对出现；当前不完整，将尝试 GET /api/v1/api-keys。',
    );
  }

  const fromEnv = credentialsFromEnvironment();
  if (fromEnv) {
    console.error(
      '提示: 已使用环境变量中的 API 凭证（跳过 GET /api/v1/api-keys），随后调用 POST /api/claw/agent-run。',
    );
    return syncPranaKeysIntoEnv(fromEnv[0], fromEnv[1]);
  }

  const base = (
    pranaBaseUrl ||
    process.env.NEXT_PUBLIC_URL ||
    DEFAULT_PRANA_BASE ||
    ''
  ).trim();
  if (base) {
    console.error(
      '提示: 环境变量中无完整 API 凭证，正在请求 GET /api/v1/api-keys，成功后调用 POST /api/claw/agent-run。',
    );
    const fetched = await fetchPranaApiKeysViaGet(base);
    if (fetched) {
      const [pub, sec] = fetched;
      return syncPranaKeysIntoEnv(pub, sec);
    }
  }

  console.error(
    '错误: 未配置 API 凭证（public_key + secret_key），且自动 GET /api/v1/api-keys 失败，或未配置可访问的 --base-url / NEXT_PUBLIC_URL。\n' +
      '  可选方式：\n' +
      '  1) 设置 PRANA_SKILL_PUBLIC_KEY + PRANA_SKILL_SECRET_KEY，或整段/单行 PRANA_SKILL_API_KEY。\n' +
      '  2) 保证 --base-url（或 NEXT_PUBLIC_URL）可访问；',
  );
  process.exit(2);
}

function buildInvokeContent(cfg, userMessage) {
  const paramsFromSkill = (cfg.skill_invocation_params || '').trim();
  return [`参数：${paramsFromSkill}`, `用户消息：${userMessage}`].join('\n');
}

function clawTargetSystemForBody(cfg) {
  const ts = String((cfg && cfg.encapsulation_target) || '').trim();
  return ts || null;
}

function isPranaEncapsulation(cfg) {
  return (
    String((cfg && cfg.encapsulation_target) || '')
      .trim()
      .toLowerCase() === 'prana'
  );
}

function extractResponseThreadId(payload) {
  const data = payload && payload.data;
  if (data && typeof data === 'object' && data.thread_id != null) {
    const tid = String(data.thread_id).trim();
    if (tid) return tid;
  }
  return '';
}

function skillKeySafeFilename(skillKey) {
  const s = String(skillKey || 'default')
    .replace(/[^\w\-.]/g, '_')
    .slice(0, 120);
  return s || 'default';
}

function threadIdStateDir() {
  const raw = (process.env.PRANA_THREAD_ID_STATE_DIR || '').trim();
  if (raw) return raw;
  try {
    const h = os.homedir();
    if (h && h !== '/') return path.join(h, '.prana_skill_state');
  } catch {
    /* ignore */
  }
  return path.join(os.tmpdir(), 'prana_skill_state');
}

function threadIdStateFile(skillKey) {
  return path.join(threadIdStateDir(), `${skillKeySafeFilename(skillKey)}_thread_id.txt`);
}

function readStoredThreadId(skillKey) {
  const p = threadIdStateFile(skillKey);
  try {
    if (fs.existsSync(p)) {
      const t = fs.readFileSync(p, 'utf8').trim();
      return t || '';
    }
  } catch {
    /* ignore */
  }
  return '';
}

function writeStoredThreadId(skillKey, tid) {
  const p = threadIdStateFile(skillKey);
  try {
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, `${String(tid || '').trim()}\n`, 'utf8');
  } catch {
    /* ignore */
  }
}

function clearStoredThreadId(skillKey) {
  const p = threadIdStateFile(skillKey);
  try {
    fs.unlinkSync(p);
  } catch {
    /* ignore */
  }
}

/** 渠道约定：优先输出 data.content；否则完整 JSON。 */
function userFacingStdoutFromClawEnvelope(result) {
  if (result && typeof result === 'object' && !Array.isArray(result)) {
    const data = result.data;
    if (data && typeof data === 'object' && !Array.isArray(data) && Object.prototype.hasOwnProperty.call(data, 'content')) {
      const raw = data.content;
      if (raw != null) {
        if (typeof raw === 'string') return raw;
        return JSON.stringify(raw);
      }
    }
  }
  return JSON.stringify(result, null, 2);
}

function emitThreadIdSessionHint(tid, pranaPack, remoteSkillKey) {
  writeStoredThreadId(remoteSkillKey, tid);
  const label = pranaPack ? 'Prana' : 'OpenClaw/其它封装';
  const state = threadIdStateFile(remoteSkillKey);
  console.error(
    `[${label}] 续聊：已写入 thread_id 状态文件（${state}）；亦可 export THREAD_ID=${tid}\n` +
      '新开会话或结束会话请使用 --new-session（-n）。\n' +
      '（可选环境变量 PRANA_THREAD_ID_STATE_DIR 指定状态目录）',
  );
}

function resolveEffectiveThreadId(cliThreadId, newSession, remoteSkillKey) {
  if (newSession) {
    clearStoredThreadId(remoteSkillKey);
    return '';
  }
  const t = String(cliThreadId || '').trim();
  if (t) return t;
  const envT = String(process.env.THREAD_ID || '').trim();
  if (envT) return envT;
  return readStoredThreadId(remoteSkillKey);
}

async function fetchAgentResult(baseUrl, requestId, publicKey, secretKey, targetSystem = null) {
  const url = `${baseUrl.replace(/\/+$/, '')}/api/claw/agent-result`;
  const body = { request_id: requestId };
  if (targetSystem) body.target_system = targetSystem;
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: headersXApiKey(publicKey, secretKey),
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(HTTP_TIMEOUT_MS),
    });
    const text = await res.text();
    if (!res.ok) {
      try {
        return JSON.parse(text);
      } catch {
        return {
          error: true,
          status: res.status,
          detail: text,
          _from: 'agent-result',
        };
      }
    }
    try {
      return JSON.parse(text);
    } catch {
      return {
        error: true,
        status: res.status,
        detail: text,
        _from: 'agent-result',
      };
    }
  } catch (e) {
    return {
      error: true,
      detail: String(e && e.reason != null ? e.reason : e && e.message ? e.message : e),
      _from: 'agent-result',
    };
  }
}

function clawResponseIsPayRequiredEnvelope(payload) {
  if (!payload || typeof payload !== 'object' || payload.error === true) return false;
  const data = payload.data;
  if (!data || typeof data !== 'object') return false;
  return String(data.status || '')
    .trim()
    .toLowerCase() === 'pay_required';
}

function agentResultPayloadStillRunning(payload) {
  if (payload.error === true) return false;
  if (clawResponseIsPayRequiredEnvelope(payload)) return false;
  const data = payload.data;
  if (!data || typeof data !== 'object') return false;
  return String(data.status || '')
    .trim()
    .toLowerCase() === 'running';
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function markRecovered(d) {
  return { ...d, _recovered_via: 'agent-result' };
}

async function pollAgentResultUntilSettled(
  baseUrl,
  requestId,
  publicKey,
  secretKey,
  targetSystem = null,
  triggerReason = '需通过 agent-result 拉取结果',
) {
  const interval = Math.max(1, AGENT_RESULT_POLL_INTERVAL_SEC);
  const maxAttempts = Math.max(1, AGENT_RESULT_POLL_MAX_ATTEMPTS);
  let last = {};
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    if (attempt === 1) {
      console.error(
        `提示: ${triggerReason}，${interval} 秒后首次 POST /api/claw/agent-result … ` +
          `(request_id=${requestId}, 最多 ${maxAttempts} 次，每 ${interval}s)`,
      );
    } else {
      console.error(`提示: 第 ${attempt} 次查询 agent-result（间隔 ${interval}s）…`);
    }
    await sleep(interval * 1000);
    last = await fetchAgentResult(baseUrl, requestId, publicKey, secretKey, targetSystem);
    if (clawResponseIsPayRequiredEnvelope(last)) return last;
    if (agentResultPayloadStillRunning(last)) continue;
    return markRecovered(last);
  }
  console.error(`警告: agent-result 已轮询 ${maxAttempts} 次仍未结束，返回最后一次响应。`);
  return markRecovered(last);
}

async function invokePrana(
  baseUrl,
  skillKey,
  content,
  threadId,
  requestId,
  publicKey,
  secretKey,
  targetSystem = null,
) {
  const url = `${baseUrl.replace(/\/+$/, '')}/api/claw/agent-run`;
  const body = {
    skill_key: skillKey,
    question: content,
    request_id: requestId,
  };
  const tid = String(threadId || '').trim();
  if (tid) body.thread_id = tid;
  if (targetSystem) body.target_system = targetSystem;
  const opts = {
    method: 'POST',
    headers: headersXApiKey(publicKey, secretKey),
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(HTTP_TIMEOUT_MS),
  };
  try {
    const res = await fetch(url, opts);
    const raw = await res.text();
    if (!res.ok) {
      if (res.status >= 500 || res.status === 408 || res.status === 504) {
        return pollAgentResultUntilSettled(
          baseUrl,
          requestId,
          publicKey,
          secretKey,
          targetSystem,
          `agent-run HTTP ${res.status}，改查 agent-result`,
        );
      }
      try {
        return JSON.parse(raw);
      } catch {
        return { error: true, status: res.status, detail: raw };
      }
    }
    try {
      // pay_required 等为合法 JSON，直接返回，不进入 agent-result 轮询
      return JSON.parse(raw);
    } catch {
      return pollAgentResultUntilSettled(
        baseUrl,
        requestId,
        publicKey,
        secretKey,
        targetSystem,
        'agent-run 响应非合法 JSON',
      );
    }
  } catch (e) {
    return pollAgentResultUntilSettled(
      baseUrl,
      requestId,
      publicKey,
      secretKey,
      targetSystem,
      'agent-run 网络异常',
    );
  }
}

async function main() {
  let values;
  try {
    const parsed = parseArgs({
      args: process.argv.slice(2),
      options: {
        message: { type: 'string', short: 'm' },
        'thread-id': { type: 'string', short: 't', default: '' },
        'new-session': { type: 'boolean', short: 'n', default: false },
        'base-url': { type: 'string', short: 'b', default: DEFAULT_PRANA_BASE },
        help: { type: 'boolean', short: 'h', default: false },
      },
      allowPositionals: false,
    });
    values = parsed.values;
    if (values.help) {
      console.log(
        '用法: node scripts/prana_skill_client.js -m "用户消息" [-t thread_id] [-n] [-b base_url]\n' +
          '-n/--new-session：新开会话；续聊依赖 THREAD_ID 或 ~/.prana_skill_state/ 下状态文件（可设 PRANA_THREAD_ID_STATE_DIR）',
      );
      process.exit(0);
    }
    if (!values.message) {
      console.error('错误: 必须使用 -m / --message 提供用户消息 / 任务描述');
      process.exit(1);
    }
  } catch (e) {
    console.error(e && e.message ? e.message : e);
    process.exit(1);
  }

  const cfg = loadSkillConfig();
  const skillKey = cfg.skill_key || '';
  if (!skillKey) {
    console.error('错误: 配置中缺少远端 skill_key（请检查脚本内 ENCAPSULATION_EMBEDDED 或旧版 SKILL.md）');
    process.exit(1);
  }

  const baseUrl = values['base-url'] || DEFAULT_PRANA_BASE;
  const [publicKey, secretKey] = await loadPranaCredentials(baseUrl);

  const requestId = randomUUID();
  const content = buildInvokeContent(cfg, values.message);
  const clawTs = clawTargetSystemForBody(cfg);
  const effThread = resolveEffectiveThreadId(
    values['thread-id'] || '',
    Boolean(values['new-session']),
    skillKey,
  );
  const result = await invokePrana(
    baseUrl,
    skillKey,
    content,
    effThread || null,
    requestId,
    publicKey,
    secretKey,
    clawTs,
  );
  if (!clawResponseIsPayRequiredEnvelope(result)) {
    const tidOut = extractResponseThreadId(result);
    if (tidOut) emitThreadIdSessionHint(tidOut, isPranaEncapsulation(cfg), skillKey);
  }
  console.log(userFacingStdoutFromClawEnvelope(result));
}

await main();
