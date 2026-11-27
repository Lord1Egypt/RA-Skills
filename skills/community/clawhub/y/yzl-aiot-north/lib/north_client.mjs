// YZL-AIoT 北向客户端（Node.js ≥18，原生 fetch，无第三方依赖）。
//
// 一个接口一个方法：
//   import { NorthClient } from "./north_client.mjs";
//   const c = await NorthClient.fromEnv();
//   await c.listDevices({ maxResults: 5 });
//   await c.telemetry("DEV-1");
//   await c.sendCommand("DEV-1", "set", ["sw", "1"]);
//
// 限频：北向 REST 用户配额 = 基础配额 + 设备数 × 每台追加（次/秒）；
// 写接口（POST/PUT/DELETE）按 3 倍配额计；超限 429。

const DEFAULT_BASE_URL = process.env.AIOT_BASE_URL || "https://aiot.yzlkj.com";
const USER_AGENT = "yzl-aiot-north/2.0";

export class NorthError extends Error {
  constructor(message, { code = null, status = null, body = null } = {}) {
    super(message);
    this.name = "NorthError";
    this.code = code;
    this.status = status;
    this.body = body;
  }
}

const q = (v) => encodeURIComponent(String(v));

export class NorthClient {
  constructor({ baseUrl, token, apiKey, account, password, timeout = 15000 } = {}) {
    this.baseUrl = (baseUrl || DEFAULT_BASE_URL).replace(/\/$/, "");
    this.token = token || null;
    this.apiKey = apiKey || null;
    this.account = account || null;
    this.password = password || null;
    this.timeout = timeout;
  }

  static async fromEnv(extra = {}) {
    return new NorthClient({
      baseUrl: process.env.AIOT_BASE_URL,
      token: process.env.AIOT_TOKEN,
      apiKey: process.env.AIOT_API_KEY,
      account: process.env.AIOT_ACCOUNT,
      password: process.env.AIOT_PASSWORD,
      ...extra,
    });
  }

  setToken(token) { this.token = token || null; }
  setApiKey(key) { this.apiKey = key || null; }

  async login(account, password) {
    account = account || this.account;
    password = password || this.password;
    if (!account || !password) throw new Error("account 和 password 必填");
    const data = await this.request("POST", "/auth/login", { body: { account, password }, auth: false });
    if (!data?.token) throw new NorthError("登录响应中没有 token", { body: data });
    this.token = data.token;
    this.account = account;
    this.password = password;
    return data.user || {};
  }

  async request(method, path, { params, body, auth = true, retry = true } = {}) {
    const url = new URL(this.baseUrl + (path.startsWith("/") ? path : "/" + path));
    for (const [k, v] of Object.entries(params || {})) {
      if (v !== undefined && v !== null) url.searchParams.set(k, Array.isArray(v) ? v.join(",") : String(v));
    }
    const headers = { Accept: "application/json", "User-Agent": USER_AGENT };
    if (body !== undefined) headers["Content-Type"] = "application/json";
    if (auth && this.token) headers.Authorization = `Bearer ${this.token}`;
    if (auth && this.apiKey) {
      headers["X-API-Key"] = this.apiKey;
      headers["YZL-AIoT-KEY"] = this.apiKey;
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);
    let res;
    let text;
    try {
      res = await fetch(url, {
        method: method.toUpperCase(),
        headers,
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: controller.signal,
      });
      text = await res.text();
    } finally {
      clearTimeout(timer);
    }
    if (res.status === 401 && retry && this.account && this.password) {
      await this.login(this.account, this.password);
      return this.request(method, path, { params, body, auth, retry: false });
    }
    let envelope = {};
    try { envelope = text ? JSON.parse(text) : {}; } catch {
      throw new NorthError(`响应不是 JSON (HTTP ${res.status}): ${text.slice(0, 200)}`, { status: res.status });
    }
    const code = envelope.code;
    if (code !== 0 && code !== undefined && code !== null) {
      let hint = "";
      if (code === 429) hint = "（限频：用户配额=基础+设备数×每台追加；写接口 3 倍）";
      else if (code === 401 || code === 403) hint = "（检查 AIOT_TOKEN / API Key 权限）";
      throw new NorthError(`${envelope.msg || "接口错误"}${hint}`, { code, status: res.status, body: envelope });
    }
    if (res.status >= 400) throw new NorthError(`HTTP ${res.status}`, { status: res.status, body: envelope });
    return envelope.data;
  }

  // ---------------------------------------------------------------- 账号
  profile() { return this.request("GET", "/auth/profile"); }
  accountSummary() { return this.request("GET", "/open/account"); }

  // ---------------------------------------------------------------- 设备
  async listDevices({ filter, groupId, online, maxResults = 50, offset = 0, includeSecrets = false } = {}) {
    const data = await this.request("GET", "/open/device/list", {
      params: { Filter: filter, GroupId: groupId, Online: online, MaxResultCount: maxResults, Offset: offset },
    });
    if (includeSecrets || !data?.items) return data;
    for (const item of data.items) for (const k of ["password", "bindCode"]) if (k in item) item[k] = "***";
    return data;
  }

  async getDevice(deviceId, { includeSecrets = false } = {}) {
    const data = await this.request("GET", `/open/device/${q(deviceId)}`);
    if (includeSecrets || !data) return data;
    for (const k of ["password", "bindCode"]) if (k in data) data[k] = "***";
    return data;
  }

  deviceStats(groupId) { return this.request("GET", "/open/device/stats", { params: { GroupId: groupId } }); }
  telemetry(deviceId) { return this.request("GET", `/open/device/${q(deviceId)}/telemetry`); }
  history(deviceId, { keys, start, end, limit } = {}) {
    return this.request("GET", `/open/device/${q(deviceId)}/history`,
      { params: { keys: Array.isArray(keys) ? keys.join(",") : keys, start, end, limit } });
  }
  aggregate(deviceId, { keys, start, end, bucket = "1h" } = {}) {
    return this.request("GET", `/open/device/${q(deviceId)}/aggregate`,
      { params: { keys: Array.isArray(keys) ? keys.join(",") : keys, start, end, bucket } });
  }
  backfillLogs(deviceId, { limit = 10 } = {}) {
    return this.request("GET", `/open/device/${q(deviceId)}/backfill-logs`, { params: { limit } });
  }

  sendCommand(deviceId, cmd, args = [], { tra } = {}) {
    if (cmd !== "set" && cmd !== "get") throw new Error("cmd 只能是 set 或 get");
    const list = [...args];
    if (list[0] !== deviceId) list.unshift(deviceId);
    const body = { cmd, args: list };
    if (tra) body.tra = tra;
    return this.request("POST", `/open/device/${q(deviceId)}/command`, { body });
  }

  // ---------------------------------------------------------------- 指令/告警
  listCommands({ deviceId, status, page = 1, pageSize = 20 } = {}) {
    return this.request("GET", "/open/command/list", { params: { deviceId, status, page, pageSize } });
  }
  getCommand(commandId) { return this.request("GET", `/open/command/${q(commandId)}`); }
  listAlarms({ status, page = 1, pageSize = 20 } = {}) {
    return this.request("GET", "/open/alarm/list", { params: { status, page, pageSize } });
  }

  // ---------------------------------------------------------------- 型号/设施
  listProducts() { return this.request("GET", "/open/product/list"); }
  async findProduct(productId) {
    const data = await this.listProducts();
    return (data?.items || []).find((x) => x.id === productId) || null;
  }
  gatewayPorts() { return this.request("GET", "/open/gateway/ports"); }

  updateMetric(productId, key, { dataType, access, label, unit, visible } = {}) {
    const body = {};
    if (dataType !== undefined) body.dataType = dataType;
    if (access !== undefined) body.access = access;
    if (label !== undefined) body.label = label;
    if (unit !== undefined) body.unit = unit;
    if (visible !== undefined) body.visible = Boolean(visible);
    if (!Object.keys(body).length) throw new Error("至少指定一个要修改的字段");
    return this.request("PATCH", `/open/product/${q(productId)}/metric/${q(key)}`, { body });
  }

  updateMetricsConfig(productId, { control, compare } = {}) {
    const body = {};
    if (control !== undefined) body.control = control;
    if (compare !== undefined) body.compare = compare;
    return this.request("PUT", `/open/product/${q(productId)}/metrics-config`, { body });
  }

  cleanMetrics(productId, keys) {
    return this.request("POST", `/open/product/${q(productId)}/clean-metrics`,
      { body: keys === undefined ? {} : { keys } });
  }
}
