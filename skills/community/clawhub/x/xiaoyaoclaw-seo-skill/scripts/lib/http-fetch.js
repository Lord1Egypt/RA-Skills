'use strict';
/**
 * http-fetch.js — 只读 GET：字节上限、解压上限、逐跳重定向、超时
 *
 * 约束（与 SKILL.md 逐条对应）：
 *   - 只 http/https、只 80/443、无 cookie jar、无 Authorization、不读代理环境变量
 *   - UA 固定；单次请求硬超时（REQUEST_TIMEOUT_MS）
 *   - 不自动跟随重定向：每一跳都重跑公网校验 + 建连时再校验，最多 MAX_REDIRECTS 跳
 *   - 响应体按**解压后**大小设上限，超限立即 destroy 断开
 *   - 不需要正文时（探测 / 3xx / 4xx+）直接 destroy，**不下载**响应体
 */
const http = require('node:http');
const https = require('node:https');
const zlib = require('node:zlib');
const { safe, assertPublicTarget, connectGuardedLookup } = require('./net-guard');
const {
  UA,
  MAX_BYTES_TEXT,
  MAX_REDIRECTS,
  REQUEST_TIMEOUT_MS,
  ALLOWED_PORTS,
} = require('./limits');

const timeout = (ms) => new Promise((r) => setTimeout(r, ms));

/** 读响应体：按 Content-Encoding 解压，流式累计并按**解压后**大小设上限。 */
function readBodyCapped(res, maxBytes) {
  return new Promise((resolve) => {
    const declared = Number(res.headers['content-length'] || 0);
    // 压缩体的声明长度只能松判（解压后才是真正的内存占用），硬闸在下面的计数器
    if (declared && declared > maxBytes * 4) {
      res.destroy();
      resolve({ text: null, error: `响应体声明 ${declared} 字节，超过上限 ${maxBytes}` });
      return;
    }
    const encoding = String(res.headers['content-encoding'] || '').toLowerCase();
    let stream = res;
    if (encoding.includes('gzip')) stream = res.pipe(zlib.createGunzip());
    else if (encoding.includes('deflate')) stream = res.pipe(zlib.createInflate());
    else if (encoding.includes('br')) stream = res.pipe(zlib.createBrotliDecompress());

    const chunks = [];
    let total = 0;
    let settled = false;
    const finish = (payload) => {
      if (settled) return;
      settled = true;
      resolve(payload);
    };
    stream.on('data', (chunk) => {
      total += chunk.length;
      if (total > maxBytes) {
        res.destroy();
        stream.destroy();
        finish({ text: null, error: `响应体超过上限 ${maxBytes} 字节，已中止读取` });
        return;
      }
      chunks.push(chunk);
    });
    stream.on('end', () => finish({ text: Buffer.concat(chunks).toString('utf8'), error: null }));
    stream.on('error', (e) => finish({ text: null, error: safe(e.message, 120) }));
  });
}

/** 丢弃正文并立即断开（探测 / 重定向 / 错误响应用）。
 *
 *  ⚠️ 这里**不用 `res.resume()`**：resume 会把整段正文读完，遇到超大或无限长
 *  的响应就会一直占着连接与本机带宽。审计只需要状态码与响应头，因此直接
 *  destroy —— 不下载、不占连接。
 */
function discardBody(res) {
  res.destroy();
}

/** 单次 GET：手动重定向语义（本函数不跟跳），连接时过地址过滤。 */
async function httpGetOnce(urlStr, { maxBytes, bodyWanted }) {
  let url;
  try {
    url = await assertPublicTarget(urlStr);
  } catch (e) {
    return { status: null, location: null, ct: '', text: '', error: e.message };
  }
  if (url.port && !ALLOWED_PORTS.has(Number(url.port))) {
    return { status: null, location: null, ct: '', text: '', error: `仅允许 80/443 端口，已拒绝：${url.port}` };
  }
  const mod = url.protocol === 'https:' ? https : http;
  return new Promise((resolve) => {
    let settled = false;
    const finish = (payload) => {
      if (settled) return;
      settled = true;
      resolve(payload);
    };
    let req;
    try {
      req = mod.request(
        url,
        {
          method: 'GET',
          lookup: connectGuardedLookup(),                 // ★ 真正的边界：建连时校验实际地址
          signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
          headers: {
            'user-agent': UA,
            accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,text/plain;q=0.8,*/*;q=0.5',
            'accept-encoding': 'gzip, deflate, br',
            // 不发送任何凭据：不带 cookie、不带 authorization
          },
        },
        (res) => {
          const ct = String(res.headers['content-type'] || '').slice(0, 60);
          const location = res.headers.location || null;
          if (!bodyWanted || (res.statusCode >= 300 && res.statusCode < 400) || res.statusCode >= 400) {
            discardBody(res);                              // 立刻断开，不下载正文
            finish({ status: res.statusCode, location, ct, text: '', error: null });
            return;
          }
          readBodyCapped(res, maxBytes).then(({ text, error }) =>
            finish({ status: res.statusCode, location, ct, text: text || '', error })
          );
        }
      );
    } catch (e) {
      finish({ status: null, location: null, ct: '', text: '', error: safe(e.message, 120) });
      return;
    }
    req.on('error', (e) => finish({ status: null, location: null, ct: '', text: '', error: safe(e.message, 120) }));
    req.end();
  });
}

/** 只探响应头（不下载正文）：手动重定向，用来判 301/308 与 location。 */
async function probe(urlStr) {
  const r = await httpGetOnce(urlStr, { maxBytes: 0, bodyWanted: false });
  return {
    url: urlStr,
    status: r.status,
    location: r.location,
    ct: r.ct,
    error: r.error || undefined,
  };
}

/** 取文本：手动重定向（每跳都过公网校验 + 连接时再校验），带上限读取。 */
async function getText(urlStr, { maxBytes = MAX_BYTES_TEXT } = {}) {
  let current = urlStr;
  for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
    const res = await httpGetOnce(current, { maxBytes, bodyWanted: true });
    if (res.error) {
      return { ok: false, status: res.status, error: res.error, text: '', ct: res.ct, location: res.location };
    }
    if (res.status >= 300 && res.status < 400) {
      if (!res.location) {
        return { ok: false, status: res.status, error: null, text: '', ct: res.ct, location: null };
      }
      if (hop === MAX_REDIRECTS) {
        return {
          ok: false, status: res.status, location: res.location, ct: res.ct, text: '',
          error: `重定向超过 ${MAX_REDIRECTS} 跳，已停止`,
        };
      }
      current = new URL(res.location, new URL(current)).toString();
      continue;
    }
    if (res.status < 200 || res.status >= 300) {
      return { ok: false, status: res.status, error: null, text: '', ct: res.ct, location: res.location };
    }
    return { ok: true, status: res.status, error: null, text: res.text, ct: res.ct, location: res.location };
  }
  return { ok: false, status: null, error: '重定向未收敛', text: '', ct: '', location: null };
}

module.exports = { timeout, readBodyCapped, discardBody, httpGetOnce, probe, getText };
