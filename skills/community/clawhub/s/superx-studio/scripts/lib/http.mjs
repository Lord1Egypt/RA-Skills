/**
 * 极简 HTTP 客户端：带上技能版本和登录令牌，解析网站的两种返回。
 *
 * 网站接口有两种返回：
 *   · 普通 JSON：{ code: 0, data }，code 不为 0 就是失败
 *   · 流式：生图、音乐这类长任务一边算一边往回写 JSON 对象，**对象之间没有分隔符**
 *     （`{"ps":""}{"progress":"30%"}{"code":0,"data":...}`），不是 SSE 也不是一行一个。
 *     按花括号配对切开，最后一个带结果的对象就是终态。
 */

let UA = 'ai-studio-skill';
let agentOf = () => '';
export function setClientVersion(name, version) {
  UA = `${name}/${version} (+agent-skill)`;
}

// 每个带令牌的请求都报一下当前是哪个 AI 工具：令牌里记的是授权那一刻认出来的，可能是空的，也可能换了工具在用
export function setClientAgent(fn) {
  agentOf = fn;
}

export class ApiError extends Error {
  constructor(message, { code, status, body } = {}) {
    super(message);
    this.code = code;
    this.status = status;
    this.body = body;
  }
}

// 连接都没建起来，请求肯定没发出去，任何方法重试都安全；
// 连上之后被重置的，POST 可能已经在服务端扣了点数，只有 GET 才重试
const CONNECT_ERRORS = ['UND_ERR_CONNECT_TIMEOUT', 'ECONNREFUSED', 'ENOTFOUND', 'EAI_AGAIN', 'EHOSTUNREACH', 'ENETUNREACH'];
const RESET_ERRORS = ['ECONNRESET', 'UND_ERR_SOCKET', 'EPIPE'];

export async function request(url, { method = 'GET', headers = {}, body, timeout = 60_000, token } = {}) {
  const h = { 'User-Agent': UA, ...headers };
  if (token) {
    h.Authorization = `Bearer ${token}`;
    let agent = '';
    try {
      agent = agentOf();
    } catch {
      /* 认不出来就不带 */
    }
    if (agent) h['X-Studio-Agent'] = agent;
  }
  for (let attempt = 1; ; attempt += 1) {
    try {
      return await fetch(url, { method, headers: h, body, signal: AbortSignal.timeout(timeout) });
    } catch (e) {
      const code = e?.cause?.code || e?.code || '';
      const retry = attempt < 3 && (CONNECT_ERRORS.includes(code) || (method === 'GET' && RESET_ERRORS.includes(code)));
      if (retry) {
        await new Promise((r) => setTimeout(r, 1500 * attempt));
        continue;
      }
      const reason = e?.name === 'TimeoutError' ? `请求超时（${Math.round(timeout / 1000)}s）` : (e?.cause?.message || e.message);
      throw new ApiError(`访问 ${new URL(url).host} 失败：${reason}`, { code: 'NETWORK' });
    }
  }
}

/** 普通 JSON 接口。code 存在且不为 0 时抛 ApiError；有些老接口直接返回数组/对象，原样给出去 */
export async function requestJson(url, options = {}) {
  const { data, ...rest } = options;
  const init = { ...rest };
  if (data !== undefined) {
    init.method = init.method || 'POST';
    init.headers = { 'Content-Type': 'application/json', ...(init.headers || {}) };
    init.body = JSON.stringify(data);
  }
  const res = await request(url, init);
  const text = await res.text();
  let json;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    throw new ApiError(`${new URL(url).pathname} 返回的不是 JSON（HTTP ${res.status}）：${text.slice(0, 120).replace(/\s+/g, ' ')}`, { status: res.status });
  }
  if (json && typeof json === 'object' && !Array.isArray(json) && json.code !== undefined && json.code !== 0 && json.code !== '0') {
    throw new ApiError(json.message || json.msg || `接口返回错误码 ${json.code}`, { code: json.code, status: res.status, body: json });
  }
  if (!res.ok) throw new ApiError(`HTTP ${res.status}`, { status: res.status, body: json });
  return json;
}

/** 把流里攒下来的文本切成一个个完整的 JSON 对象，返回 [对象们, 剩下的半截] */
export function splitObjects(buffer) {
  const out = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  let consumed = 0;
  for (let i = 0; i < buffer.length; i += 1) {
    const ch = buffer[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') inString = true;
    else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}' && depth > 0) {
      depth -= 1;
      if (depth === 0 && start >= 0) {
        try {
          out.push(JSON.parse(buffer.slice(start, i + 1)));
        } catch {
          /* 坏掉的一段跳过，不影响后面的 */
        }
        consumed = i + 1;
        start = -1;
      }
    }
  }
  return [out, buffer.slice(consumed)];
}

/**
 * 流式接口：边收边把每个对象交给 onEvent，结束后返回全部对象。
 * 心跳（{ps:''}、{state:'pending'}）也会交出去，调用方自己挑。
 */
export async function requestStream(url, { data, token, timeout = 100 * 60_000, onEvent = () => {} } = {}) {
  const res = await request(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data ?? {}),
    token,
    timeout,
  });
  if (!res.body) throw new ApiError(`HTTP ${res.status}，没有返回内容`, { status: res.status });
  const decoder = new TextDecoder('utf-8');
  const events = [];
  let buffer = '';
  for await (const chunk of res.body) {
    buffer += decoder.decode(chunk, { stream: true });
    const [objs, rest] = splitObjects(buffer);
    buffer = rest;
    for (const obj of objs) {
      events.push(obj);
      onEvent(obj);
    }
  }
  buffer += decoder.decode();
  const [objs] = splitObjects(buffer);
  for (const obj of objs) {
    events.push(obj);
    onEvent(obj);
  }
  if (!events.length && !res.ok) throw new ApiError(`HTTP ${res.status}`, { status: res.status });
  return events;
}
