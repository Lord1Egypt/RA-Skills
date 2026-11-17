// 浏览器会话通道（browser session channel）
// ─────────────────────────────────────────────────────────────────────────────
// 为什么需要这个模块：
//   新帆 merchant_lead 这批接口在 edith 网关挂了 SSO 插件，只认「用户在浏览器里
//   完成公司 SSO(redpass) 登录后、由前端注入到请求里的登录态」，不认 agent 环境
//   自带的 ambient token（common-internal-access-token），也不存在可搬运的
//   access-token-<域名> cookie（真实令牌是 HttpOnly / localStorage，前端运行时
//   注入请求头）。因此「把 token 抠出来用 Node fetch 直发」这条路走不通。
//
// 本模块改走「浏览器会话通道」：连接 agent 环境里的 Chrome DevTools Protocol(CDP)，
// 找到一个已登录新帆的页面，在该页面的上下文里用页面自己的 fetch 发请求——身份、
// cookie、注入头全部由页面天然带上。请求发出的身份，就是当前这个 agent(DIBP) 实例
// 背后登录用户「本人」的身份，用的是他自己的权限，不存在借用他人会话。
//
// 依赖：仅 Node 内置能力（node:http / node:crypto / 全局 WebSocket，Node>=22）。
//   Node 22 起全局提供 WebSocket，无需第三方库。

import http from "node:http";
import crypto from "node:crypto";

// ── CDP 端点与目标域名 ────────────────────────────────────────────────────────
// CDP 地址可用环境变量覆盖；默认对齐 DIBP/OpenClaw 内置无头浏览器的调试端口。
export const CDP_URL =
  process.env.XINFAN_LEAD_CDP_URL || "http://127.0.0.1:18800";

function cdpHttpJson(path) {
  return new Promise((resolve, reject) => {
    const url = `${CDP_URL}${path}`;
    const req = http.get(url, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`CDP 响应解析失败(${path}): ${e.message}`));
        }
      });
    });
    req.on("error", (e) =>
      reject(new Error(`无法连接 CDP(${CDP_URL})：${e.message}`))
    );
    req.setTimeout(5000, () => {
      req.destroy(new Error(`连接 CDP 超时(${CDP_URL})`));
    });
  });
}

// 列出当前所有页面页签，挑出属于目标新帆域名的那个。
async function findXinfanTarget(domain) {
  let targets;
  try {
    targets = await cdpHttpJson("/json");
  } catch (e) {
    const err = new Error(
      `无法访问浏览器调试端点(${CDP_URL})。请确认 agent 环境的浏览器已启动，` +
        `或用 XINFAN_LEAD_CDP_URL 指定正确地址。原始错误：${e.message}`
    );
    err.code = "NO_CDP";
    throw err;
  }
  const pages = (targets || []).filter(
    (t) => t.type === "page" && typeof t.url === "string"
  );
  // 优先精确匹配目标域名的新帆页面
  const match = pages.find((p) => p.url.includes(domain));
  return match || null;
}

// ── 极简 CDP WebSocket 客户端（基于全局 WebSocket）────────────────────────────
function openCdp(wsUrl) {
  return new Promise((resolve, reject) => {
    // 注意：CDP 默认校验 Origin。全局 WebSocket 不发送 Origin 头（非浏览器环境），
    // 恰好满足 Chrome 对「无 Origin」连接的放行，无需 --remote-allow-origins。
    let ws;
    try {
      ws = new WebSocket(wsUrl);
    } catch (e) {
      return reject(new Error(`创建 CDP WebSocket 失败：${e.message}`));
    }
    const pending = new Map();
    const timer = setTimeout(() => {
      reject(new Error("连接 CDP WebSocket 超时"));
      try {
        ws.close();
      } catch {}
    }, 8000);

    ws.addEventListener("open", () => {
      clearTimeout(timer);
      resolve({
        send(method, params) {
          const id = crypto.randomInt(1, 2 ** 31);
          return new Promise((res, rej) => {
            pending.set(id, { res, rej });
            ws.send(JSON.stringify({ id, method, params: params || {} }));
          });
        },
        close() {
          try {
            ws.close();
          } catch {}
        },
      });
    });
    ws.addEventListener("message", (ev) => {
      let msg;
      try {
        msg = JSON.parse(ev.data);
      } catch {
        return;
      }
      if (msg.id && pending.has(msg.id)) {
        const { res, rej } = pending.get(msg.id);
        pending.delete(msg.id);
        if (msg.error) rej(new Error(msg.error.message || "CDP 调用出错"));
        else res(msg.result);
      }
    });
    ws.addEventListener("error", () => {
      clearTimeout(timer);
      reject(new Error(`CDP WebSocket 连接错误(${CDP_URL})`));
    });
  });
}

// 在页面上下文里执行 fetch，返回 {status, contentType, text}。
// requestSpec: { method, path, bodyObj }
async function evaluateFetchInPage(wsUrl, baseUrl, requestSpec) {
  const cdp = await openCdp(wsUrl);
  try {
    await cdp.send("Runtime.enable");
    const { method, path, bodyObj } = requestSpec;
    const url = `${baseUrl}${path}`;
    // 用页面自己的 fetch，credentials:'include' 让页面天然带上登录态。
    const expr = `
      (async () => {
        try {
          const r = await fetch(${JSON.stringify(url)}, {
            method: ${JSON.stringify(method)},
            credentials: 'include',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: ${JSON.stringify(JSON.stringify(bodyObj ?? {}))}
          });
          const text = await r.text();
          return JSON.stringify({
            status: r.status,
            contentType: r.headers.get('content-type') || '',
            text
          });
        } catch (e) {
          return JSON.stringify({ __fetchError: String(e && e.message || e) });
        }
      })()
    `;
    const result = await cdp.send("Runtime.evaluate", {
      expression: expr,
      awaitPromise: true,
      returnByValue: true,
    });
    if (result.exceptionDetails) {
      throw new Error(
        `页面内执行请求异常：${
          result.exceptionDetails.text ||
          result.exceptionDetails.exception?.description ||
          "unknown"
        }`
      );
    }
    const raw = result.result?.value;
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch {
      throw new Error(`页面返回结果解析失败：${String(raw).slice(0, 200)}`);
    }
    if (parsed.__fetchError) {
      const err = new Error(`页面内 fetch 失败：${parsed.__fetchError}`);
      err.code = "PAGE_FETCH_ERROR";
      throw err;
    }
    return parsed;
  } finally {
    cdp.close();
  }
}

// ── 对外主入口 ────────────────────────────────────────────────────────────────
// 通过已登录新帆页面发一次请求。
// 找不到已登录页面时抛 NO_SESSION，由上层给出「怎么建立会话通道」的引导。
export async function requestViaBrowserSession({ domain, baseUrl, method, path, bodyObj }) {
  const target = await findXinfanTarget(domain);
  if (!target) {
    const err = new Error(
      `未找到已登录新帆(${domain})的浏览器页面，无法建立会话通道。`
    );
    err.code = "NO_SESSION";
    throw err;
  }
  if (!target.webSocketDebuggerUrl) {
    const err = new Error(
      `已找到新帆页面，但它没有可用的调试通道(webSocketDebuggerUrl)。`
    );
    err.code = "NO_WS";
    throw err;
  }
  return evaluateFetchInPage(target.webSocketDebuggerUrl, baseUrl, {
    method,
    path,
    bodyObj,
  });
}

// 只做「探测当前是否已有可用新帆会话」，供 auth status / 引导流程使用。
export async function probeSession(domain) {
  try {
    const target = await findXinfanTarget(domain);
    if (!target) return { available: false, reason: "no_page" };
    if (!target.webSocketDebuggerUrl)
      return { available: false, reason: "no_ws" };
    return { available: true, targetId: target.id, url: target.url };
  } catch (e) {
    return { available: false, reason: e.code || "cdp_error", message: e.message };
  }
}
