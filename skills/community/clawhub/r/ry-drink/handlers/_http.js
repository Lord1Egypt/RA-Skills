const DEFAULT_BASE = process.env.RY_DRINK_API_BASE || 'http://192.168.0.66:8080/user-biz';
/** 会话绑定门店 ID（user-system chat.send 写入），优先级最高，LLM 无法覆盖 */
const FORCED_SHOP_ID = String(process.env.RY_DRINK_FORCED_SHOP_ID || '').trim();
/** 租客 ID（t_merchant.id），/merchant/{id}/info、/menus 路径用此值 */
const DEFAULT_PLATFORM_TENANT_ID = String(process.env.RY_DRINK_PLATFORM_TENANT_ID || '').trim();
/** 仅本地调试可设 RY_DRINK_SHOP_ID */
const DEFAULT_SHOP_ID = String(process.env.RY_DRINK_SHOP_ID || '').trim();
const DEFAULT_SAAS_ID = String(process.env.RY_DRINK_SAAS_ID || 'sf8b00e05').trim();
const DEFAULT_TENANT_ID = String(
  process.env.RY_DRINK_TENANT_ID || DEFAULT_PLATFORM_TENANT_ID || '5',
).trim();
const DEFAULT_LINK_PHONE = String(process.env.RY_DRINK_LINK_PHONE || '').trim();

function isNumericShopId(value) {
  if (value === undefined || value === null || value === '') {
    return false;
  }
  return /^\d+$/.test(String(value).trim());
}

/** 从 OpenClaw 会话 slug 提取门店数字 ID，如 store-6-mqp0wx8wgv72fi → 6 */
function parseNumericFromStoreSlug(raw) {
  if (raw === undefined || raw === null || raw === '') {
    return null;
  }
  const text = String(raw).trim();
  const match = text.match(/^store-(\d+)(?:-|$)/i);
  return match ? match[1] : null;
}

/**
 * shopId 必须是 yshop 数字门店 ID。
 * 优先级：纯数字参数 > store-{id}-slug > 环境变量 RY_DRINK_SHOP_ID（仅调试）
 */
function resolveShopId(raw) {
  if (isNumericShopId(raw)) {
    return { shopId: String(raw).trim(), usedDefault: false };
  }
  const fromSlug = parseNumericFromStoreSlug(raw);
  if (fromSlug) {
    return { shopId: fromSlug, usedDefault: false, fromSlug: true };
  }
  if (DEFAULT_SHOP_ID && isNumericShopId(DEFAULT_SHOP_ID)) {
    return { shopId: DEFAULT_SHOP_ID, usedDefault: true };
  }
  const original = raw === undefined || raw === null || raw === '' ? null : String(raw).trim();
  return {
    shopId: null,
    error: true,
    ...(original ? { original } : {}),
    message: original
      ? `shopId "${original}" 无法解析为数字门店 ID，请传入当前会话门店 ID（如 6）`
      : '缺少 shopId，请传入当前会话门店数字 ID',
  };
}

function resolveMerchantPathId(params) {
  if (DEFAULT_PLATFORM_TENANT_ID && isNumericShopId(DEFAULT_PLATFORM_TENANT_ID)) {
    return DEFAULT_PLATFORM_TENANT_ID;
  }
  const tenantId = params?.tenantId;
  if (isNumericShopId(tenantId)) {
    return String(tenantId).trim();
  }
  return null;
}

function pick(obj, keys) {
  const out = {};
  if (!obj || typeof obj !== 'object') {
    return out;
  }
  for (const key of keys) {
    if (obj[key] !== undefined && obj[key] !== null && obj[key] !== '') {
      out[key] = obj[key];
    }
  }
  return out;
}

function withDefaults(obj) {
  const out = obj && typeof obj === 'object' ? { ...obj } : {};
  if (!out.saasId) {
    out.saasId = DEFAULT_SAAS_ID;
  }
  if (out.tenantId === undefined || out.tenantId === null || out.tenantId === '') {
    out.tenantId = DEFAULT_TENANT_ID;
  }
  if (FORCED_SHOP_ID && isNumericShopId(FORCED_SHOP_ID)) {
    out.shopId = FORCED_SHOP_ID;
    out._shopIdForced = true;
  } else {
    const resolved = resolveShopId(out.shopId);
    if (resolved.error) {
      out._shopIdError = resolved.message;
      return out;
    }
    out.shopId = resolved.shopId;
    if (resolved.usedDefault) {
      out._shopIdWarning = `已使用环境变量门店 ${resolved.shopId}`;
    } else if (resolved.fromSlug) {
      out._shopIdFromSlug = true;
    }
  }
  if (!out.linkPhone && DEFAULT_LINK_PHONE) {
    out.linkPhone = DEFAULT_LINK_PHONE;
  }
  return out;
}

function ensureShopId(body) {
  if (body?._shopIdError) {
    return { success: false, error: body._shopIdError };
  }
  return null;
}

function buildContextHeaders(body) {
  const headers = {};
  if (body?.saasId) {
    headers['X-Saas-Id'] = String(body.saasId);
  }
  if (body?.tenantId !== undefined && body?.tenantId !== null && body?.tenantId !== '') {
    headers['X-Tenant-Id'] = String(body.tenantId);
  }
  if (body?.shopId) {
    headers['X-Shop-Id'] = String(body.shopId);
  }
  if (body?.linkPhone) {
    headers['X-Mobile'] = String(body.linkPhone);
  }
  return headers;
}

async function request(method, path, { query, body, headers } = {}) {
  const base = DEFAULT_BASE.replace(/\/$/, '');
  const url = new URL(base + path);
  if (query) {
    Object.entries(query).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') {
        url.searchParams.set(k, String(v));
      }
    });
  }
  const normalizedBody = body ? withDefaults(body) : null;
  if (normalizedBody) {
    const shopErr = ensureShopId(normalizedBody);
    if (shopErr) {
      return shopErr;
    }
  }
  const init = {
    method,
    headers: {
      Accept: 'application/json',
      ...(normalizedBody ? { 'Content-Type': 'application/json' } : {}),
      ...(normalizedBody ? buildContextHeaders(normalizedBody) : {}),
      ...(headers || {}),
    },
  };
  if (normalizedBody) {
    init.body = JSON.stringify(normalizedBody);
  }
  const response = await fetch(url.toString(), init);
  let payload;
  try {
    payload = await response.json();
  } catch {
    payload = { code: response.status, msg: response.statusText || '非 JSON 响应' };
  }
  if (!response.ok && payload.code === undefined) {
    return { success: false, error: payload.msg || `HTTP ${response.status}`, httpStatus: response.status };
  }
  if (payload.code !== undefined && payload.code !== 200) {
    const data = payload.data ?? null;
    const action = data?.action;
    const tableTaken = payload.code === 601 || action === 'table_taken';
    return {
      success: false,
      tableTaken,
      action: action || (tableTaken ? 'table_taken' : undefined),
      error: payload.msg || '请求失败',
      code: payload.code,
      msg: payload.msg,
      data,
      chatHint: data?.chatHint || payload.msg,
    };
  }
  return { success: true, ...payload, data: payload.data ?? payload };
}

async function invokeDiningTool(toolName, args) {
  const normalized = withDefaults(args || {});
  const shopErr = ensureShopId(normalized);
  if (shopErr) {
    return shopErr;
  }
  return request('POST', '/aiemployees/dining/tool/invoke', {
    body: { toolName, arguments: normalized },
    headers: buildContextHeaders(normalized),
  });
}

async function invokeAppointmentTool(toolName, args) {
  const normalized = withDefaults(args || {});
  const shopErr = ensureShopId(normalized);
  if (shopErr) {
    return shopErr;
  }
  return request('POST', '/aiemployees/appointment/tool/invoke', {
    body: { toolName, arguments: normalized },
    headers: buildContextHeaders(normalized),
  });
}

function withResolvedShopId(obj) {
  return withDefaults(obj);
}

module.exports = {
  request,
  pick,
  withDefaults,
  ensureShopId,
  invokeDiningTool,
  invokeAppointmentTool,
  resolveShopId,
  resolveMerchantPathId,
  parseNumericFromStoreSlug,
  withResolvedShopId,
  buildContextHeaders,
  DEFAULT_BASE,
  FORCED_SHOP_ID,
  DEFAULT_PLATFORM_TENANT_ID,
  DEFAULT_SHOP_ID,
  DEFAULT_SAAS_ID,
  DEFAULT_TENANT_ID,
};
