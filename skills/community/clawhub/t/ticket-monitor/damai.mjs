// damai.mjs — 大麦网 H5 (mtop) 客户端
//
// 职责：空 sign 请求获取 mtop 签名 token → 发起签名的详情请求 → 解析为统一快照。
//
// 关键点（已在本环境实测验证）：
//  - 当前详情接口为 mtop.alibaba.damai.detail.getdetail/1.2（旧的 item.detail 已下线）
//  - appKey = 12574478
//  - 首次带 appKey 但 sign 为空发起请求，服务端返回 FAIL_SYS_TOKEN_EMPTY 并下发 _m_h5_tk
//  - sign = md5(token + '&' + t + '&' + appKey + '&' + data)
//
// 说明：大麦公开详情接口只暴露「可售(salable)/售罄」状态，精确余票张数一般不公开；
//       本模块会尽力提取任何数字型余票字段（如 residueNum/ticketNum 等），缺失则置 null。
import crypto from 'node:crypto';

const APP_KEY = '12574478';
const API = 'mtop.alibaba.damai.detail.getdetail';
const VERSION = '1.2';
const API_URL = `https://mtop.damai.cn/h5/${API}/${VERSION}/`;
const DEFAULT_UA =
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1';

// 状态码 → 中文（尽力映射，原始值始终保留在快照中）
const ITEM_STATUS = { 0: '未开售', 1: '在售', 2: '停售/下架', 3: '停售' };
const PERFORM_STATUS = { 0: '未开售', 1: '在售', 2: '售罄', 3: '停售' };

const md5 = (s) => crypto.createHash('md5').update(s, 'utf8').digest('hex');

class CookieJar {
  constructor() {
    this.map = new Map();
  }
  load(str) {
    if (!str) return;
    for (const part of String(str).split(/;\s*/)) {
      const i = part.indexOf('=');
      if (i > 0) this.map.set(part.slice(0, i).trim(), part.slice(i + 1).trim());
    }
  }
  setFromResponse(res) {
    const setCookies =
      typeof res.headers.getSetCookie === 'function' ? res.headers.getSetCookie() : [];
    for (const sc of setCookies) {
      const pair = sc.split(';')[0];
      const eq = pair.indexOf('=');
      if (eq <= 0) continue;
      const name = pair.slice(0, eq).trim();
      const value = pair.slice(eq + 1).trim();
      if (value === '') this.map.delete(name);
      else this.map.set(name, value);
    }
  }
  get(name) {
    return this.map.get(name) || '';
  }
  header() {
    return [...this.map.entries()].map(([k, v]) => `${k}=${v}`).join('; ');
  }
}

function firstRet(json) {
  return Array.isArray(json.ret) ? json.ret[0] : '';
}

// 从纯数字 / 完整 URL / 任意含 id= 的字符串中提取 itemId
export function extractItemId(input) {
  const s = String(input ?? '').trim();
  if (!s) throw new Error('缺少 itemId');
  if (/^\d+$/.test(s)) return s;
  const byId = s.match(/[?&]id=(\d+)/i);
  if (byId) return byId[1];
  const any = s.match(/(\d{6,})/);
  if (any) return any[1];
  throw new Error(`无法从「${s}」中解析 itemId`);
}

function buildData(itemId) {
  return {
    itemId: Number(itemId),
    platform: '8',
    comboChannel: '2',
    dmChannel: 'damai@damaih5_h5',
  };
}

async function signedRequest(jar, ua, appKey, dataStr, token) {
  const t = String(Date.now());
  const sign = token ? md5(`${token}&${t}&${appKey}&${dataStr}`) : '';
  const form = new URLSearchParams({
    jsv: '2.7.2',
    appKey,
    t,
    sign,
    api: API,
    v: VERSION,
    type: 'originaljson',
    dataType: 'json',
    data: dataStr,
    H5Request: 'true',
    timeout: '10000',
  });
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'User-Agent': ua,
      'Content-Type': 'application/x-www-form-urlencoded',
      Referer: 'https://detail.damai.cn/',
      Cookie: jar.header(),
    },
    body: form.toString(),
  });
  jar.setFromResponse(res);
  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`详情接口返回非 JSON（HTTP ${res.status}）`);
  }
  return json;
}

// 完整请求流程：拿 token → 签名请求 → 令牌/签名错误时自动重试
async function requestDetail(input, opts = {}) {
  const ua = opts.ua || DEFAULT_UA;
  const appKey = opts.appKey || APP_KEY;
  const jar = new CookieJar();
  if (opts.cookie) jar.load(opts.cookie);

  const itemId = extractItemId(input);
  const dataStr = JSON.stringify(buildData(itemId));

  // 1) 空 sign 请求，触发服务端下发 _m_h5_tk
  let json = await signedRequest(jar, ua, appKey, dataStr, '');

  // 2) 用拿到的 token 做签名请求；遇到令牌/签名错误则重新获取 token 再试
  for (let i = 0; i < 3; i++) {
    const token = jar.get('_m_h5_tk').split('_')[0];
    if (!token) {
      json = await signedRequest(jar, ua, appKey, dataStr, '');
      continue;
    }
    json = await signedRequest(jar, ua, appKey, dataStr, token);
    const ret = firstRet(json);
    if (ret && /TOKEN_(EMPTY|EXPIRED)|SIGN_ERROR|ILLEGAL/i.test(ret)) {
      jar.map.delete('_m_h5_tk');
      jar.map.delete('_m_h5_tk_enc');
      continue;
    }
    break;
  }
  return { json, itemId };
}

function toNum(v) {
  if (typeof v === 'number' && Number.isFinite(v)) return v;
  if (typeof v === 'string' && /^\d+$/.test(v.trim())) return Number(v.trim());
  return null;
}

// 深挖对象树，寻找第一个匹配候选键名且为数字的字段（尽力提取余票张数）
const COUNT_KEYS = /residue|remain|stock|inventory|ticketnum|saleablecount|restnum|leftnum|surplus/i;

function findCount(node) {
  if (node == null) return null;
  if (Array.isArray(node)) {
    for (const item of node) {
      const v = findCount(item);
      if (v != null) return v;
    }
    return null;
  }
  if (typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) {
      if (COUNT_KEYS.test(k)) {
        const n = toNum(v);
        if (n != null) return n;
      }
    }
    for (const [k, v] of Object.entries(node)) {
      if (COUNT_KEYS.test(k)) {
        const nested = findCount(v);
        if (nested != null) return nested;
      }
    }
  }
  return null;
}

// 从候选键名里取第一个非空值
function pick(obj, keys) {
  if (!obj) return undefined;
  for (const k of keys) if (obj[k] != null && obj[k] !== '') return obj[k];
  return undefined;
}

// 判断「可售」状态：优先 salable/saleable/soldOut/onSale，返回 true/false/null(未知)
function isSalable(o) {
  if (o == null) return null;
  if (o.salable != null) return !!o.salable;
  if (o.saleable != null) return !!o.saleable;
  if (o.soldOut != null) return !o.soldOut;
  if (o.soldout != null) return !o.soldout;
  if (o.onSale != null) return !!o.onSale;
  return null;
}

// 解析 sku/价格档位列表
function parseSkus(list) {
  if (!Array.isArray(list)) return [];
  const out = [];
  for (const s of list) {
    if (!s || typeof s !== 'object') continue;
    const name = pick(s, ['priceName', 'skuName', 'ticketName', 'name', 'title']);
    const price = pick(s, ['price', 'amount', 'value']);
    if (name == null && price == null && s.skuId == null && s.ticketId == null) continue;
    out.push({
      name: name != null ? String(name) : price != null ? String(price) : String(s.skuId ?? s.ticketId ?? ''),
      price: price != null ? price : null,
      salable: isSalable(s) ?? (s.status === 1),
      remainCount: findCount(s),
    });
  }
  return out;
}

// 解析场次列表
function parseSessions(perform) {
  if (!Array.isArray(perform)) return [];
  return perform.map((p) => {
    const skus = parseSkus(p.skuList || p.priceList || p.ticketList || p.sku || p.price);
    const own = isSalable(p) ?? (p.status === 1);
    const salable = skus.length ? skus.some((s) => s.salable === true) || own === true : own;
    const name = pick(p, ['performName', 'sessionName', 'name', 'title']) || `场次 ${p.performId ?? ''}`;
    return {
      performId: p.performId != null ? String(p.performId) : null,
      name: String(name),
      status: p.status ?? null,
      statusLabel: PERFORM_STATUS[p.status] ?? '未知',
      salable: !!salable,
      remainCount: findCount(p),
      skus,
    };
  });
}

// 解析原始响应 data 为统一快照
function parseSnapshot(d, itemId) {
  const basic = d.itemBasicInfo || d.item || d.detail || {};
  const itemName =
    pick(basic, ['itemName', 'projectName', 'showName', 'name', 'title']) ||
    pick(d, ['itemName', 'projectName', 'showName', 'name', 'title']) ||
    '未知演出';

  const sessions = parseSessions(
    d.perform || d.performList || d.sessionList || d.itemList || d.sessions || (d.detail && d.detail.perform)
  );

  const anySale = sessions.length ? sessions.some((s) => s.salable) : true;
  const allSoldOut = sessions.length > 0 && sessions.every((s) => !s.salable);
  const itemStatus = basic.itemStatus ?? d.itemStatus ?? null;

  let overallLabel;
  if (itemStatus === 0) overallLabel = '未开售';
  else if (anySale) overallLabel = '在售';
  else if (allSoldOut) overallLabel = '售罄';
  else overallLabel = ITEM_STATUS[itemStatus] ?? '未知';

  return {
    itemId: String(itemId),
    itemName,
    itemStatus,
    itemStatusLabel: ITEM_STATUS[itemStatus] ?? '未知',
    overallLabel,
    remainCount: findCount(d),
    sessions,
    fetchedAt: new Date().toISOString(),
  };
}

// 原始响应导出（用于 --raw 调试/确认字段结构）
export async function fetchRaw(input, opts = {}) {
  const { json, itemId } = await requestDetail(input, opts);
  const ret = firstRet(json);
  if (ret && !String(ret).startsWith('SUCCESS')) throw new Error(`mtop 调用失败: ${ret}`);
  return { itemId, raw: json.data || {} };
}

// 主入口：抓取并解析为统一快照
export async function fetchItemDetail(input, opts = {}) {
  const { json, itemId } = await requestDetail(input, opts);
  const ret = firstRet(json);
  if (ret && !String(ret).startsWith('SUCCESS')) throw new Error(`mtop 调用失败: ${ret}`);

  const d = json.data || {};
  if (d.errorMsg) {
    throw new Error(
      `被大麦反爬拦截：${d.errorMsg}（本机 IP 可能被风控。建议在家庭网络运行，或配置 damai.cookie 注入登录会话）`
    );
  }
  return parseSnapshot(d, itemId);
}
