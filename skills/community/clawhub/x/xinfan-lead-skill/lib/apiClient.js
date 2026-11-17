import { BASE_URL, DOMAIN } from "./config.js";
import { requestViaBrowserSession } from "./browserSession.js";

export class UsageError extends Error {
  constructor(message) {
    super(message);
    this.exitCode = 1;
  }
}

export class AuthError extends Error {
  constructor(message) {
    super(message);
    this.exitCode = 2;
  }
}

export class UpstreamError extends Error {
  constructor(message, body) {
    super(message);
    this.exitCode = 3;
    this.body = body;
  }
}

export class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.exitCode = 4;
  }
}

// 引导文案：会话通道不可用时统一提示 agent「怎么建立这个通道」。
// 详细步骤见 SKILL.md「建立会话通道」一节；这里给的是可直接转达给用户/agent 的精简版。
const SESSION_HINT =
  "新帆会话通道未就绪。请让 agent 按以下步骤建立：\n" +
  `  1) 用浏览器打开 https://${DOMAIN}/seller/investClue\n` +
  "  2) 等待 3~5 秒让页面完成公司 SSO(redpass) 登录（若跳登录页，由用户本人扫码/登录一次）\n" +
  "  3) 确认页面右上角显示为当前用户本人后，重新执行本命令。\n" +
  "说明：本 skill 用「当前登录用户本人」的浏览器会话调用新帆，用的是用户自己的身份和权限，不搬运任何 token。";

// entry 是 lib/schemas.js 里 API_SCHEMAS 的一个条目（{path, method, ...}）。
// 会话通道模式下，请求身份由浏览器页面天然携带，这里只负责组装 method/path/body。
export function buildRequest(entry, bodyObj) {
  return {
    method: entry.method,
    url: `${BASE_URL}${entry.path}`,
    channel: "browser-session",
    bodyObj,
  };
}

// 判断响应是否表示「未登录 / 会话失效」。
// 已实测的�lead鉴权失效样本：HTTP 401 {"code":-100,"success":false,"msg":"无登录信息"}。
function looksLikeAuthExpired(status, contentType, text, json) {
  if (status === 401 || status === 403) return true;
  if (contentType && contentType.includes("text/html")) return true;
  if (/^\s*<!DOCTYPE|^\s*<html/i.test(text || "")) return true;
  if (json) {
    const code = json.code;
    const msg = String(json.msg ?? json.message ?? "");
    const suspiciousCode = [401, 403, -1, -100, 50110].includes(code);
    const suspiciousMsg =
      /login|登录|unauthor|token|过期|expire|无权限|无登录|未登录/i.test(msg);
    if (suspiciousCode && suspiciousMsg) return true;
  }
  return false;
}

export async function callApi(entry, bodyObj) {
  let resp;
  try {
    resp = await requestViaBrowserSession({
      domain: DOMAIN,
      baseUrl: BASE_URL,
      method: entry.method,
      path: entry.path,
      bodyObj,
    });
  } catch (err) {
    // 会话/通道类问题 → 归为 AuthError（退出码 2），并给出建立通道的引导。
    if (["NO_CDP", "NO_SESSION", "NO_WS"].includes(err.code)) {
      throw new AuthError(`${err.message}\n\n${SESSION_HINT}`);
    }
    if (err.code === "PAGE_FETCH_ERROR") {
      throw new NetworkError(
        `请求 ${entry.path} 失败（浏览器会话内网络错误）：${err.message}`
      );
    }
    throw new NetworkError(`请求 ${entry.path} 失败：${err.message}`);
  }

  const { status, contentType = "", text = "" } = resp;
  let json = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    // 非 JSON 响应，交给下面的鉴权失效判断处理
  }

  if (looksLikeAuthExpired(status, contentType, text, json)) {
    throw new AuthError(
      `认证已失效或未登录（HTTP ${status}）。\n\n${SESSION_HINT}`
    );
  }

  if (status < 200 || status >= 300) {
    throw new UpstreamError(`${entry.path} 返回 HTTP ${status}`, json ?? text);
  }

  return json ?? text;
}
