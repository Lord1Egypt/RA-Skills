#!/usr/bin/env node
/**
 * probe-models.js — 依据 baseUrl + apiKey 列出该端点下所有模型 id
 *
 * 用法:
 *   node probe-models.js <baseUrl> <apiKey>
 *   node probe-models.js https://gpt.cosmoplat.com/v1 sk-xxxx
 *
 * 也支持从 openclaw.json 读某个 provider:
 *   node probe-models.js --provider cosmoplat-gptplan
 *   node probe-models.js --provider cosmoplat-gptplan --agent main
 *
 * 原理: GET {baseUrl}/models  Authorization: Bearer <apiKey>
 * 兼容: OpenAI / vLLM / Ollama / 各类 OpenAI-compatible 网关
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const HOME = process.env.USERPROFILE || process.env.HOME || '';
const CONFIG = path.join(HOME, '.openclaw', 'openclaw.json');

function loadProviderConfig(providerId, agentId) {
  // agent 级 models.json 优先
  if (agentId) {
    const p = path.join(HOME, '.openclaw', 'agents', agentId, 'agent', 'models.json');
    if (fs.existsSync(p)) {
      const j = JSON.parse(fs.readFileSync(p, 'utf8'));
      const v = (j.providers || {})[providerId];
      if (v) return { baseUrl: v.baseUrl, apiKey: v.apiKey, source: p };
    }
  }
  const cfg = JSON.parse(fs.readFileSync(CONFIG, 'utf8'));
  const v = ((cfg.models || {}).providers || {})[providerId];
  if (v) return { baseUrl: v.baseUrl, apiKey: v.apiKey, source: CONFIG };
  throw new Error(`provider "${providerId}" 未找到`);
}

function isGoogle(u) {
  return /generativelanguage\.googleapis\.com/.test(u.hostname || u);
}

function request(urlStr, apiKey, timeoutMs = 25000) {
  return new Promise((resolve, reject) => {
    const u = new URL(urlStr);
    const lib = u.protocol === 'https:' ? https : http;
    // Google Generative Language API 用 ?key= 而非 Bearer
    const google = isGoogle(u);
    const headers = {
      Accept: 'application/json',
      'User-Agent': 'probe-models/1.0',
    };
    if (!google) headers.Authorization = `Bearer ${apiKey}`;

    const opts = {
      hostname: u.hostname,
      port: u.port || (u.protocol === 'https:' ? 443 : 80),
      path: u.pathname + u.search,
      method: 'GET',
      headers,
      timeout: timeoutMs,
    };

    // 代理支持: HTTPS_PROXY / HTTP_PROXY / --proxy http://127.0.0.1:7890
    const proxyArg = (() => {
      const i = process.argv.indexOf('--proxy');
      return i >= 0 ? process.argv[i + 1] : null;
    })();
    const proxyUrl = proxyArg || process.env.HTTPS_PROXY || process.env.https_proxy || process.env.HTTP_PROXY || process.env.http_proxy;
    let transport = null;
    if (proxyUrl && u.protocol === 'https:') {
      const pu = new URL(proxyUrl);
      // HTTPS over HTTP CONNECT tunnel
      const connectMod = pu.protocol === 'https:' ? require('tls') : require('http');
      opts.hostname = pu.hostname;
      opts.port = pu.port || (pu.protocol === 'https:' ? 443 : 80);
      opts.path = `${u.protocol}//${u.hostname}:${u.port || 443}${u.pathname}${u.search}`;
      opts.headers = { ...headers, Host: u.hostname };
      connectMod.request;
      transport = 'proxy';
      // 用 http 模块发 CONNECT 更简单，这里交给 curl 兼容路径
    }

    // 若有代理，走 CONNECT 隧道（手写，避免依赖）
    if (transport === 'proxy') {
      const net = require('net');
      const pu = new URL(proxyUrl);
      const creq = http.request({
        host: pu.hostname,
        port: pu.port || 80,
        method: 'CONNECT',
        path: `${u.hostname}:${u.port || 443}`,
        headers: pu.username ? { 'Proxy-Authorization': 'Basic ' + Buffer.from(`${decodeURIComponent(pu.username)}:${decodeURIComponent(pu.password)}`).toString('base64') } : {},
        timeout: timeoutMs,
      });
      creq.on('connect', (res, socket) => {
        if (res.statusCode !== 200) {
          return reject(new Error(`proxy CONNECT ${res.statusCode}`));
        }
        const treq = https.request(
          {
            hostname: u.hostname,
            port: u.port || 443,
            path: u.pathname + u.search,
            method: 'GET',
            headers,
            socket,
            agent: false,
            servername: u.hostname,
            timeout: timeoutMs,
          },
          (r2) => {
            let body = '';
            r2.on('data', (c) => (body += c));
            r2.on('end', () => resolve({ status: r2.statusCode, body, via: 'proxy' }));
          }
        );
        treq.on('error', reject);
        treq.end();
      });
      creq.on('error', reject);
      creq.on('timeout', () => creq.destroy(new Error('proxy timeout')));
      creq.end();
      return;
    }

    const req = lib.request(opts,
      (res) => {
        let body = '';
        res.on('data', (c) => (body += c));
        res.on('end', () => resolve({ status: res.statusCode, body }));
      }
    );
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy(new Error(`timeout ${timeoutMs}ms`));
    });
    req.end();
  });
}

function extractModelIds(body) {
  let j;
  try {
    j = JSON.parse(body);
  } catch {
    return null;
  }
  // OpenAI 标准: { object:"list", data:[{id:...}] }
  if (Array.isArray(j.data)) {
    return j.data.map((m) => (typeof m === 'string' ? m : m.id || m.model || m.name)).filter(Boolean);
  }
  // 裸数组
  if (Array.isArray(j)) {
    return j.map((m) => (typeof m === 'string' ? m : m.id || m.model || m.name)).filter(Boolean);
  }
  // Ollama 原生 / Gemini: { models:[{name:...}] }
  if (Array.isArray(j.models)) {
    return j.models
      .map((m) => m.name || m.model || m.id)
      .filter(Boolean)
      .map((s) => s.replace(/^models\//, '')); // Gemini 返回 "models/gemini-3-pro"
  }
  // 某些网关: { result:[...] } / { models:{...} }
  if (Array.isArray(j.result)) return j.result.filter((x) => typeof x === 'string');
  if (j.models && typeof j.models === 'object') return Object.keys(j.models);
  return null;
}

function normalizeBase(baseUrl, apiKey) {
  // baseUrl 可能带或不带 /v1，也可能已带 /models
  let b = baseUrl.replace(/\/+$/, '');
  if (isGoogle(b)) {
    const base = /\/models$/.test(b) ? b : b + '/models';
    return `${base}?key=${encodeURIComponent(apiKey)}&pageSize=200`;
  }
  if (/\/models$/.test(b)) return b;
  return b + '/models';
}

async function retryable(fn, attempts = 3, delayMs = 1200) {
  let last;
  for (let i = 1; i <= attempts; i++) {
    try {
      return await fn();
    } catch (e) {
      last = e;
      const transient = /socket hang up|ECONNRESET|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|timeout|EPIPE/i.test(e.message);
      if (!transient || i === attempts) throw e;
      if (i === 1) console.log(`   (网络抖动，重试中… ${e.message})`);
      await new Promise((r) => setTimeout(r, delayMs * i));
    }
  }
  throw last;
}

async function probe(baseUrl, apiKey, label) {
  const url = normalizeBase(baseUrl, apiKey);
  console.log(`\n=== ${label || ''}`);
  console.log(`GET ${url.replace(/key=[^&]+/, 'key=***')}`);
  console.log(`Key  ${apiKey.slice(0, 6)}…${apiKey.slice(-4)} (len=${apiKey.length})`);

  let r;
  try {
    r = await retryable(() => request(url, apiKey));
  } catch (e) {
    const networkFail = /socket hang up|ECONNRESET|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|timeout/i.test(e.message);
    let hint = '';
    if (networkFail) {
      hint = isGoogle(url)
        ? '\n   💡 网络连不通。国内访问 Google 需代理，试试:\n      node probe-models.js --provider google --proxy http://127.0.0.1:7890'
        : '\n   💡 网络连不通。检查 baseUrl 是否正确、端点是否可达；如需代理:\n      node probe-models.js --proxy http://127.0.0.1:7890';
    }
    console.log(`❌ 请求失败: ${e.message}${hint}`);
    return { ok: false, url, error: e.message };
  }

  console.log(`HTTP ${r.status}`);
  if (r.status !== 200) {
    console.log(`❌ 响应: ${r.body.slice(0, 300)}`);
    return { ok: false, url, status: r.status, body: r.body };
  }

  const ids = extractModelIds(r.body);
  if (!ids) {
    console.log(`⚠️  200 但不是模型列表格式，原始响应前 300 字:`);
    console.log(r.body.slice(0, 300));
    return { ok: false, url, status: 200, parseable: false };
  }

  console.log(`✅ 共 ${ids.length} 个模型:`);
  for (const id of ids.sort()) console.log(`   ${id}`);
  return { ok: true, url, status: 200, models: ids };
}

// 校验：拿第一个模型真打一次 chat/completions，确认 key 有推理权限
async function verifyChat(baseUrl, apiKey, modelId) {
  const base = baseUrl.replace(/\/+$/, '').replace(/\/models$/, '');
  const url = new URL(base + '/chat/completions');
  const payload = JSON.stringify({
    model: modelId,
    messages: [{ role: 'user', content: 'say ok' }],
    max_tokens: 5,
  });
  return new Promise((resolve) => {
    const lib = url.protocol === 'https:' ? https : http;
    const req = lib.request(
      {
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: url.pathname,
        method: 'POST',
        headers: {
          Authorization: `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
        },
        timeout: 40000,
      },
      (res) => {
        let body = '';
        res.on('data', (c) => (body += c));
        res.on('end', () => resolve({ status: res.statusCode, body }));
      }
    );
    req.on('error', (e) => resolve({ status: 'ERR', body: e.message }));
    req.on('timeout', () => req.destroy(new Error('timeout')));
    req.write(payload);
    req.end();
  });
}

(async () => {
  const args = process.argv.slice(2);
  const flag = (name) => {
    const i = args.indexOf(name);
    return i >= 0 ? args[i + 1] : null;
  };

  // 自检：不需要网络，只验证解析/拼装逻辑
  if (args.includes('--self-test')) {
    let pass = 0,
      fail = 0;
    const ok = (name, cond) => {
      if (cond) {
        console.log(`  ✅ ${name}`);
        pass++;
      } else {
        console.log(`  ❌ ${name}`);
        fail++;
      }
    };

    console.log('--- extractModelIds ---');
    ok('OpenAI 标准', JSON.stringify(extractModelIds('{"object":"list","data":[{"id":"a"},{"id":"b"}]}')) === '["a","b"]');
    ok('裸数组', JSON.stringify(extractModelIds('["x","y"]')) === '["x","y"]');
    ok('Ollama 原生', JSON.stringify(extractModelIds('{"models":[{"name":"qwen3:1.7b"}]}')) === '["qwen3:1.7b"]');
    ok('Gemini 去 models/ 前缀', JSON.stringify(extractModelIds('{"models":[{"name":"models/gemini-3-pro"}]}')) === '["gemini-3-pro"]');
    ok('非 JSON 返回 null', extractModelIds('not json') === null);
    ok('未知格式返回 null', extractModelIds('{"foo":1}') === null);

    console.log('--- normalizeBase ---');
    ok('补 /models', normalizeBase('https://x.com/v1', 'k') === 'https://x.com/v1/models');
    ok('已带 /models 不重复', normalizeBase('https://x.com/v1/models', 'k') === 'https://x.com/v1/models');
    ok('去尾部斜杠', normalizeBase('https://x.com/v1/', 'k') === 'https://x.com/v1/models');
    ok('Google 用 ?key=', normalizeBase('https://generativelanguage.googleapis.com/v1beta', 'kk').includes('?key=kk'));
    ok('Google pageSize', normalizeBase('https://generativelanguage.googleapis.com/v1beta', 'kk').includes('pageSize=200'));

    console.log('--- isGoogle ---');
    ok('识别 Google host', isGoogle('https://generativelanguage.googleapis.com/v1beta/models') === true);
    ok('非 Google 返回 false', isGoogle('https://api.openai.com/v1/models') === false);

    console.log('--- retryable ---');
    let calls = 0;
    await retryable(async () => {
      calls++;
      if (calls < 2) throw new Error('ECONNRESET');
      return 'ok';
    }, 3, 1).then((v) => ok('可重试错误自动重试', v === 'ok' && calls === 2));
    let n = 0;
    await retryable(async () => {
      n++;
      throw new Error('401 unauthorized');
    }, 3, 1).catch(() => ok('不可重试错误不重试', n === 1));

    console.log(`\n${fail === 0 ? '✅ 全部通过' : '❌ 有失败'}  ${pass} passed, ${fail} failed`);
    process.exit(fail === 0 ? 0 : 1);
  }

  const providerId = flag('--provider');
  const agentId = flag('--agent');

  if (providerId) {
    const p = loadProviderConfig(providerId, agentId);
    console.log(`来源: ${p.source}`);
    const res = await probe(p.baseUrl, p.apiKey, providerId);
    if (res.ok) {
      // 顺便对比：配置里声明的模型 vs 端点真实返回的模型
      const cfg = JSON.parse(fs.readFileSync(CONFIG, 'utf8'));
      const declared = (((cfg.models || {}).providers || {})[providerId] || {}).models || [];
      const declaredIds = declared.map((m) => m.id);
      if (declaredIds.length) {
        const real = new Set(res.models);
        const missing = declaredIds.filter((id) => !real.has(id));
        const unused = res.models.filter((id) => !declaredIds.includes(id));
        console.log(`\n--- 配置校验 ---`);
        console.log(`配置声明 ${declaredIds.length} 个: ${declaredIds.join(', ')}`);
        // /models 列表可能不完整，对未列出的声明模型逐个真打验证
        let realMissing = [];
        for (const id of missing) {
          const v = await verifyChat(p.baseUrl, p.apiKey, id);
          if (v.status === 200) {
            console.log(`⚠️  ${id}: 不在 /models 列表中，但实测可调用 ✅（说明该端点 /models 返回不完整）`);
          } else {
            console.log(`❌ ${id}: 不在列表中且调用失败 HTTP ${v.status} ${String(v.body).slice(0, 80)}`);
            realMissing.push(id);
          }
        }
        if (unused.length) console.log(`💡 端点有但配置没写: ${unused.slice(0, 20).join(', ')}${unused.length > 20 ? ' …' : ''}`);
        if (!realMissing.length && !unused.length) console.log(`✅ 配置与端点一致（无缺失，无多余）`);
        // 真实可调用性验证
        const first = declaredIds.find((id) => real.has(id));
        if (first) {
          const v = await verifyChat(p.baseUrl, p.apiKey, first);
          console.log(`\n--- 推理验证 (${first}) ---`);
          console.log(`HTTP ${v.status} ${v.status === 200 ? '✅ 可调用' : '❌ ' + v.body.slice(0, 200)}`);
        }
      }
    }
    process.exit(res.ok ? 0 : 1);
  }

  const [baseUrl, apiKey] = args;
  if (!baseUrl || !apiKey) {
    console.log(`用法:
  node probe-models.js <baseUrl> <apiKey>
  node probe-models.js --provider <id> [--agent <agentId>]

示例:
  node probe-models.js https://gpt.cosmoplat.com/v1 sk-xxxx
  node probe-models.js --provider cosmoplat-gptplan`);
    process.exit(1);
  }
  const res = await probe(baseUrl, apiKey);
  process.exit(res.ok ? 0 : 1);
})();
