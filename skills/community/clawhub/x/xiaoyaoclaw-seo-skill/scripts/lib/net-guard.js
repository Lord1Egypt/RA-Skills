'use strict';
/**
 * net-guard.js — 目标校验与地址边界（纯逻辑，除 DNS 查询外不产生网络流量）
 *
 * 三层：
 *   1. safe()                —— 远端字符串在打印前的净化（防终端注入）
 *   2. isBlockedIp()         —— 内网 / 回环 / 链路本地（含云元数据）/ CGNAT /
 *                               保留段 / IPv6 ULA 判定
 *   3. assertPublicTarget()  —— 请求前预检：协议、凭据、端口外的明显坏目标
 *      connectGuardedLookup() —— **真正的强制点**：每次建立 TCP 连接时重新解析
 *                               并逐个校验待连地址，命中内网段即让连接失败
 *                               （预检与实际连接之间存在 DNS 重绑定的时间差，
 *                                 只有建连那一刻的校验能堵住它）
 */
const dns = require('node:dns').promises;
const net = require('node:net');

/** 终端安全化：剥掉 ANSI/OSC 转义与控制字符，压缩空白，截断长度。
 *  远端页面可以把 title / meta 写成带转义序列的内容，直接打印会伪装审计输出。 */
function safe(value, max = 200) {
  if (value === null || value === undefined) return '';
  let s = String(value);
  s = s
    .replace(/\u001b\][^\u0007\u001b]*(?:\u0007|\u001b\\)/g, '')   // OSC ... BEL/ST
    .replace(/\u001b\[[0-9;?]*[ -/]*[@-~]/g, '')                   // CSI ... final
    .replace(/[\u0000-\u0008\u000b-\u001f\u007f-\u009f]/g, ' ')    // C0/C1（保留 \t \n）
    .replace(/[ \t]+/g, ' ')
    .trim();
  if (s.length > max) s = s.slice(0, max) + '…';
  return s;
}

/** 该 IP 是否属于内网 / 保留 / 元数据段 —— 命中即拒绝访问。 */
function isBlockedIp(ip) {
  const version = net.isIP(ip);
  if (version === 4) {
    const [a, b] = ip.split('.').map(Number);
    if (a === 0 || a === 10 || a === 127) return true;              // 本网络/私有/回环
    if (a === 169 && b === 254) return true;                        // 链路本地 + 云元数据
    if (a === 172 && b >= 16 && b <= 31) return true;               // 私有
    if (a === 192 && b === 168) return true;                        // 私有
    if (a === 100 && b >= 64 && b <= 127) return true;              // CGNAT
    if (a === 192 && b === 0) return true;                          // 保留/测试
    if (a === 198 && (b === 18 || b === 19)) return true;           // 基准测试
    if (a >= 224) return true;                                      // 组播 + 保留
    return false;
  }
  if (version === 6) {
    const v = ip.toLowerCase();
    if (v === '::' || v === '::1') return true;                     // 未指定 / 回环
    if (v.startsWith('::ffff:')) return isBlockedIp(v.slice(7));     // IPv4 映射
    if (v.startsWith('fe80')) return true;                          // 链路本地
    if (v.startsWith('fc') || v.startsWith('fd')) return true;      // ULA
    if (v.startsWith('ff')) return true;                            // 组播
    return false;
  }
  return true; // 非 IP：按"拒绝"处理，域名会解析后再判
}

/** 请求前预检：仅 http/https、无内嵌凭据、解析结果必须全部是公网地址。 */
async function assertPublicTarget(urlStr) {
  let url;
  try {
    url = new URL(urlStr);
  } catch {
    throw new Error(`非法 URL：${urlStr}`);
  }
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new Error(`仅允许 http/https：${url.protocol}`);
  }
  if (url.username || url.password) throw new Error('URL 不得内嵌凭据');
  const host = url.hostname.replace(/^\[|\]$/g, '');
  if (net.isIP(host)) {
    if (isBlockedIp(host)) throw new Error(`目标为内网/保留地址，已拒绝：${host}`);
    return url;
  }
  let addrs;
  try {
    addrs = await dns.lookup(host, { all: true });
  } catch {
    throw new Error(`DNS 解析失败：${host}`);
  }
  const blocked = addrs.filter((a) => isBlockedIp(a.address));
  if (blocked.length) {
    throw new Error(`目标解析到内网/保留地址，已拒绝：${host} -> ${blocked.map((a) => a.address).join(', ')}`);
  }
  return url;
}

/** 建连时的地址过滤：每次建立 TCP 连接都重新解析并逐个校验待连地址。
 *
 *  断言（预检）不是边界，这里才是：校验用的 DNS 结果和随后实际连接的地址
 *  可能是两次解析（DNS 重绑定）。命中内网/保留段就让连接失败，绝不回退。
 */
function connectGuardedLookup() {
  return (hostname, options, callback) => {
    dns
      .lookup(hostname, { all: true, verbatim: true })
      .then((addrs) => {
        const allowed = addrs.filter((a) => !isBlockedIp(a.address));
        if (!allowed.length) {
          callback(new Error(`拒绝连接：${hostname} 解析到的地址全部属于内网/保留段`));
          return;
        }
        if (options && options.all) {
          callback(null, allowed);
          return;
        }
        callback(null, allowed[0].address, allowed[0].family);
      })
      .catch((err) => callback(err));
  };
}

module.exports = { safe, isBlockedIp, assertPublicTarget, connectGuardedLookup };
