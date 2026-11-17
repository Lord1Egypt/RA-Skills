 'use strict';
const BASES = { tools: ['https://tools.siping.me/api'], pipeline: ['https://api.siping.me', 'https://api.siping.me/api'] };
function baseUrl(value, service) {
  // Exact legacy deployments migrate locally; never send a request to HTTP.
  if (service === 'pipeline' && ['http://47.103.80.109:4000', 'http://101.133.167.31:4000'].includes(value)) value = BASES.pipeline[0];
  let u;
  try { u = new URL(value); } catch { throw new Error('无效的服务地址'); }
  const normalized = u.href.replace(/\/$/, '');
  if (u.username || u.password || !BASES[service]?.includes(normalized)) throw new Error('服务地址不在受信任的 HTTPS 白名单中');
  return normalized;
}
function requestUrl(value) {
  let u;
  try { u = new URL(value); } catch { throw new Error('无效的请求地址'); }
  if (u.username || u.password || u.hash || u.protocol !== 'https:' || !(
    u.origin === 'https://api.siping.me' ||
    (u.origin === 'https://tools.siping.me' && u.pathname.startsWith('/api/'))
  )) throw new Error('拒绝向非受信任的服务发送请求');
  return u.href;
}
function joinUrl(base, route, service) {
  const trusted = baseUrl(base, service);
  if (typeof route !== 'string' || !route.startsWith('/') || route.startsWith('//') || /[\\#]/.test(route) || /(?:^|\/)\.\.?(?:\/|$)/.test(decodeURIComponent(route.split('?')[0]))) throw new Error('无效的 API 路径');
  return requestUrl(trusted + route);
}
module.exports = { baseUrl, requestUrl, joinUrl };
