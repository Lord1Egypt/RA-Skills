'use strict';
/**
 * lib/registry-fetch.js —— 无 npm 内置拉包通道（元阁 0.24.0，方案 A.1）。
 *
 * 零依赖：Node 内置 https/http 直连 registry，abbreviated packument 解析版本，
 * tarball 下载 + integrity(sha512) / shasum(sha1) fail-closed 校验；
 * 支持 HTTPS_PROXY / HTTP_PROXY（CONNECT 隧道简实现）与 NO_PROXY。
 *
 * 同步入口 fetchPackageSync 供安装管线（同步契约）使用：通过子进程执行同一套
 * 异步核心（lib/registry-fetch-child.js），stdin/stdout 传 JSON，不落任何状态。
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const tls = require('tls');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const OFFICIAL_REGISTRY = 'https://registry.npmjs.org/';
const DEFAULT_TIMEOUT = 15000;
const DEFAULT_DOWNLOAD_TIMEOUT = 120000;
const DEFAULT_MAX_BYTES = 64 * 1024 * 1024;
const INTEGRITY_RANK = { sha512: 1, sha384: 2, sha256: 3, sha1: 4 };

function registryBase(opts) {
  const raw = (opts && opts.registry) || process.env.YOTTA_SKILLS_REGISTRY || OFFICIAL_REGISTRY;
  return String(raw).replace(/\/+$/, '') + '/';
}

function packumentUrl(pkg, opts) {
  return registryBase(opts) + String(pkg).replace(/\//g, '%2f');
}

function tarballName(pkg, version) {
  const parts = String(pkg).replace(/^@/, '').split('/');
  const scope = parts.length > 1 ? parts[0] : '';
  const bare = parts.length > 1 ? parts[1] : parts[0];
  return (scope ? scope + '-' : '') + bare + '-' + version + '.tgz';
}

function majorRange(version) {
  return String(version).split('.')[0] + '.x';
}

function compareSemver(a, b) {
  const pa = String(a).split('.').map(Number);
  const pb = String(b).split('.').map(Number);
  for (let i = 0; i < 3; i += 1) {
    const x = pa[i] || 0;
    const y = pb[i] || 0;
    if (x !== y) return x - y;
  }
  return 0;
}

function parseIntegrity(value) {
  const entries = String(value || '')
    .split(/\s+/)
    .map((token) => {
      const match = token.match(/^(sha512|sha384|sha256|sha1)-(.+)$/);
      return match ? { algo: match[1], base64: match[2] } : null;
    })
    .filter(Boolean);
  if (!entries.length) return null;
  entries.sort((a, b) => INTEGRITY_RANK[a.algo] - INTEGRITY_RANK[b.algo]);
  return entries[0];
}

function noProxyMatch(hostname) {
  const raw = process.env.NO_PROXY || process.env.no_proxy || '';
  if (!raw) return false;
  const host = String(hostname || '').toLowerCase();
  return String(raw)
    .split(',')
    .map((entry) => entry.trim().toLowerCase())
    .filter(Boolean)
    .some((entry) => {
      if (entry === '*') return true;
      const clean = entry.replace(/^\./, '').replace(/:\d+$/, '');
      return host === clean || host.endsWith('.' + clean);
    });
}

function proxyFor(url) {
  if (noProxyMatch(url.hostname)) return null;
  const raw = url.protocol === 'https:'
    ? (process.env.HTTPS_PROXY || process.env.https_proxy || process.env.HTTP_PROXY || process.env.http_proxy)
    : (process.env.HTTP_PROXY || process.env.http_proxy);
  if (!raw) return null;
  try {
    const parsed = new URL(/^[a-z]+:\/\//i.test(raw) ? raw : 'http://' + raw);
    return { hostname: parsed.hostname, port: Number(parsed.port) || 80 };
  } catch (_) {
    return null;
  }
}

function tunneledAgent(socket) {
  const agent = new https.Agent({ keepAlive: false });
  agent.createConnection = function createConnection(options, callback) {
    if (typeof callback === 'function') callback(null, socket);
    return socket;
  };
  return agent;
}

function requestStreamOnce(rawUrl, opts) {
  return new Promise((resolve) => {
    let url;
    try {
      url = new URL(rawUrl);
    } catch (error) {
      resolve({ ok: false, error: 'URL 解析失败: ' + error.message });
      return;
    }
    const options = opts || {};
    const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT;
    const headers = Object.assign(
      { 'user-agent': 'yotta-skills-fetch', accept: '*/*' },
      options.headers || {},
    );
    const proxy = proxyFor(url);
    let settled = false;
    const done = (value) => {
      if (!settled) {
        settled = true;
        resolve(value);
      }
    };
    const fail = (error) => done({ ok: false, error: '网络错误: ' + ((error && error.message) || error) });
    const arm = (req) => {
      req.on('error', fail);
      req.setTimeout(timeoutMs, () => req.destroy(new Error('网络超时（' + timeoutMs + 'ms）')));
    };

    if (url.protocol === 'https:' && proxy) {
      const target = url.hostname + ':' + (url.port || 443);
      const connectReq = http.request({
        host: proxy.hostname,
        port: proxy.port,
        method: 'CONNECT',
        path: target,
        headers: { host: target },
      });
      connectReq.on('connect', (res, socket) => {
        if (res.statusCode !== 200) {
          socket.destroy();
          done({ ok: false, error: '代理 CONNECT 失败: HTTP ' + res.statusCode });
          return;
        }
        const tlsSocket = tls.connect({ socket, servername: url.hostname });
        tlsSocket.once('secureConnect', () => {
          const req = https.request({
            host: url.hostname,
            port: url.port || 443,
            path: url.pathname + url.search,
            method: 'GET',
            headers,
            agent: tunneledAgent(tlsSocket),
          });
          arm(req);
          req.on('response', (res2) => done({ ok: true, res: res2 }));
          req.end();
        });
        tlsSocket.once('error', fail);
      });
      connectReq.on('error', fail);
      connectReq.setTimeout(timeoutMs, () => connectReq.destroy(new Error('代理连接超时')));
      connectReq.end();
      return;
    }

    if (url.protocol === 'http:' && proxy) {
      const req = http.request({
        host: proxy.hostname,
        port: proxy.port,
        method: 'GET',
        path: url.href,
        headers: Object.assign({ host: url.host }, headers),
      });
      arm(req);
      req.on('response', (res) => done({ ok: true, res }));
      req.end();
      return;
    }

    const mod = url.protocol === 'https:' ? https : http;
    const req = mod.request({
      host: url.hostname,
      port: url.port || undefined,
      path: url.pathname + url.search,
      method: 'GET',
      headers,
    });
    arm(req);
    req.on('response', (res) => done({ ok: true, res }));
    req.end();
  });
}

async function requestWithRedirects(url, opts, depth) {
  const result = await requestStreamOnce(url, opts);
  if (!result.ok) return result;
  const res = result.res;
  const location = res.headers && res.headers.location;
  if (location && [301, 302, 303, 307, 308].includes(res.statusCode) && (depth || 0) < 3) {
    res.resume();
    let next;
    try {
      next = new URL(location, url).href;
    } catch (_) {
      return { ok: false, error: '重定向地址非法: ' + location };
    }
    return requestWithRedirects(next, opts, (depth || 0) + 1);
  }
  return result;
}

function collectBody(res, maxBytes) {
  return new Promise((resolve) => {
    const chunks = [];
    let size = 0;
    let settled = false;
    const done = (value) => {
      if (!settled) {
        settled = true;
        resolve(value);
      }
    };
    res.on('data', (chunk) => {
      size += chunk.length;
      if (size > maxBytes) {
        res.destroy();
        done({ ok: false, error: '响应超过大小上限（' + maxBytes + ' 字节）' });
        return;
      }
      chunks.push(chunk);
    });
    res.on('error', (error) => done({ ok: false, error: '读取响应失败: ' + error.message }));
    res.on('end', () => done({ ok: true, body: Buffer.concat(chunks), size }));
  });
}

async function fetchPackument(pkg, opts) {
  const options = opts || {};
  const url = packumentUrl(pkg, options);
  let lastError = null;
  for (let attempt = 0; attempt < 2; attempt += 1) {
    const result = await requestWithRedirects(url, {
      timeoutMs: options.timeoutMs || DEFAULT_TIMEOUT,
      headers: { accept: 'application/vnd.npm.install-v1+json' },
    }, 0);
    if (!result.ok) {
      lastError = result.error;
      continue;
    }
    const body = await collectBody(result.res, 8 * 1024 * 1024);
    if (!body.ok) {
      lastError = body.error;
      continue;
    }
    if (result.res.statusCode !== 200) {
      lastError = 'registry 返回 HTTP ' + result.res.statusCode;
      continue;
    }
    try {
      return { ok: true, packument: JSON.parse(body.body.toString('utf8')), url };
    } catch (error) {
      lastError = '解析 registry 响应失败: ' + error.message;
    }
  }
  return { ok: false, error: lastError || 'packument 获取失败' };
}

/** pin=true 取精确版本；pin=false 过滤同 major 取最高正式版本。 */
function resolveVersion(packument, skill, pin) {
  const versions = (packument && packument.versions) || {};
  if (pin && String(skill.version) === 'latest') {
    const latest = (packument && packument['dist-tags'] && packument['dist-tags'].latest) || null;
    if (!latest || !versions[latest]) {
      return { error: 'registry 无 dist-tags.latest（' + skill.pkg + '）' };
    }
    return { version: String(latest), dist: versions[latest].dist || {} };
  }
  if (pin) {
    const exact = versions[String(skill.version)];
    if (!exact) {
      const latest = (packument && packument['dist-tags'] && packument['dist-tags'].latest) || null;
      return { error: 'registry 无 ' + skill.pkg + '@' + skill.version + (latest ? '（latest=' + latest + '）' : '') };
    }
    return { version: String(skill.version), dist: exact.dist || {} };
  }
  const major = String(skill.version).split('.')[0];
  const matches = Object.keys(versions).filter((v) => (
    /^[0-9]+\.[0-9]+\.[0-9]+$/.test(v) && v.split('.')[0] === major
  ));
  if (!matches.length) return { error: 'registry 无 ' + major + '.x 版本（' + skill.pkg + '）' };
  matches.sort(compareSemver);
  const best = matches[matches.length - 1];
  return { version: best, dist: versions[best].dist || {} };
}

function streamToFile(res, destFile, options) {
  return new Promise((resolve) => {
    const hasher = crypto.createHash(options.algo);
    const out = fs.createWriteStream(destFile);
    let size = 0;
    let settled = false;
    const done = (value) => {
      if (!settled) {
        settled = true;
        resolve(value);
      }
    };
    const fail = (message) => {
      if (settled) return;
      res.destroy();
      out.destroy();
      done({ ok: false, error: message });
    };
    res.on('data', (chunk) => {
      size += chunk.length;
      if (size > options.maxBytes) {
        fail('下载超过大小上限（' + options.maxBytes + ' 字节）');
        return;
      }
      hasher.update(chunk);
      out.write(chunk);
    });
    res.on('aborted', () => fail('下载中断'));
    res.on('error', (error) => fail('下载失败: ' + error.message));
    out.on('error', (error) => fail('写入临时文件失败: ' + error.message));
    res.on('end', () => {
      if (settled) return;
      out.end(() => {
        if (settled) return;
        done({ ok: true, size, digest: hasher.digest() });
      });
    });
  });
}

async function downloadTarball(url, destFile, dist, opts) {
  const options = opts || {};
  const integrity = parseIntegrity(dist && dist.integrity);
  const shasum = dist && dist.shasum ? String(dist.shasum).trim().toLowerCase() : null;
  if (!integrity && !shasum) {
    return { ok: false, error: 'registry 缺少 integrity / shasum（fail-closed 拒绝）' };
  }
  const result = await requestWithRedirects(url, {
    timeoutMs: options.downloadTimeoutMs || DEFAULT_DOWNLOAD_TIMEOUT,
  }, 0);
  if (!result.ok) return { ok: false, error: result.error };
  const res = result.res;
  if (res.statusCode !== 200) {
    res.resume();
    return { ok: false, error: '下载失败：HTTP ' + res.statusCode };
  }
  const algo = integrity ? integrity.algo : 'sha1';
  const saved = await streamToFile(res, destFile, {
    maxBytes: options.maxBytes || DEFAULT_MAX_BYTES,
    algo,
  });
  if (!saved.ok) {
    fs.rmSync(destFile, { force: true });
    return { ok: false, error: saved.error };
  }
  const expected = integrity ? integrity.base64 : shasum;
  const got = integrity ? saved.digest.toString('base64') : saved.digest.toString('hex');
  if (got !== expected) {
    fs.rmSync(destFile, { force: true });
    return { ok: false, error: 'integrity 校验失败（' + algo + '），已删除下载文件（fail-closed）' };
  }
  return { ok: true, size: saved.size, algo };
}

/** 异步核心：拉 packument → 解析版本 → 下载校验 → 落 packDir；返回 { ok, ... }。 */
async function fetchPackage(skill, opts, packDir) {
  const options = opts || {};
  const pin = options.pin !== false;
  const spec = skill.pkg + '@' + (pin ? skill.version : majorRange(skill.version));
  const packument = await fetchPackument(skill.pkg, options);
  if (!packument.ok) return { ok: false, error: 'packument 获取失败: ' + packument.error };
  const resolved = resolveVersion(packument.packument, skill, pin);
  if (resolved.error) return { ok: false, error: '版本解析失败: ' + resolved.error };
  const dist = resolved.dist || {};
  if (!dist.tarball) return { ok: false, error: 'registry 版本缺少 dist.tarball（' + spec + '）' };
  fs.mkdirSync(packDir, { recursive: true });
  const destFile = path.join(packDir, tarballName(skill.pkg, resolved.version));
  const downloaded = await downloadTarball(dist.tarball, destFile, dist, options);
  if (!downloaded.ok) return { ok: false, error: '下载失败: ' + downloaded.error };
  return {
    ok: true,
    tarball: destFile,
    resolved: resolved.version,
    spec,
    registry: registryBase(options),
    integrity: dist.integrity || null,
    shasum: dist.shasum || null,
    size: downloaded.size,
  };
}

/** 同步入口：子进程执行同一套异步核心（安装管线为同步契约）。 */
function fetchPackageSync(skill, opts, packDir) {
  const child = path.join(__dirname, 'registry-fetch-child.js');
  const payload = JSON.stringify({
    skill: { slug: skill.slug, pkg: skill.pkg, version: skill.version },
    opts: { pin: opts.pin, registry: opts.registry || null },
    packDir,
  });
  const result = spawnSync(process.execPath, [child], {
    input: payload,
    encoding: 'utf8',
    timeout: 240000,
    maxBuffer: 16 * 1024 * 1024,
    env: process.env,
  });
  if (result.error) return { error: '内置拉包通道启动失败: ' + result.error.message };
  const line = String(result.stdout || '').trim().split(/\r?\n/).filter(Boolean).pop();
  let parsed = null;
  if (line) {
    try {
      parsed = JSON.parse(line);
    } catch (_) {
      parsed = null;
    }
  }
  if (!parsed) {
    const brief = String(result.stderr || '').trim().split(/\r?\n/).filter(Boolean).slice(-2).join(' | ');
    return { error: '内置拉包通道异常（exit ' + result.status + '）' + (brief ? ': ' + brief : '') };
  }
  if (!parsed.ok) return { error: parsed.error || '内置拉包失败' };
  const out2 = parsed.result || {};
  out2.channel = 'builtin';
  return out2;
}

module.exports = {
  OFFICIAL_REGISTRY,
  registryBase,
  packumentUrl,
  tarballName,
  majorRange,
  parseIntegrity,
  proxyFor,
  noProxyMatch,
  resolveVersion,
  fetchPackument,
  downloadTarball,
  fetchPackage,
  fetchPackageSync,
};
