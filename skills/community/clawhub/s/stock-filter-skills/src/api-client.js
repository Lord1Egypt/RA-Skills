import { getApiUrl, getAuthHeaders, API_TIMEOUT } from "./config.js";

export async function apiRequest(path, { method = "GET", params, body } = {}) {
  let url = getApiUrl(path);
  if (params) {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v != null)
    ).toString();
    if (qs) url += `?${qs}`;
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const res = await fetch(url, {
      method,
      headers: getAuthHeaders(),
      body: body ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const detail = data.detail || data.message || "";
      const detailStr = Array.isArray(detail) ? detail.join("; ") : String(detail);
      const statusMap = {
        400: "请求参数有误",
        401: "认证失败，请检查 API Key",
        403: "没有权限访问该资源",
        404: "资源不存在",
        422: "请求参数验证失败",
        429: "请求频率超限，请稍后重试",
        500: "服务器内部错误",
      };
      const msg = statusMap[res.status] || `API 请求失败 (${res.status})`;
      throw new Error(detailStr ? `${msg}。详情: ${detailStr}` : msg);
    }
    return data;
  } catch (e) {
    if (e.name === "AbortError") throw new Error("请求超时，请检查网络或稍后重试");
    if (e.cause?.code === "ECONNREFUSED") throw new Error("无法连接到 API 服务器，请检查服务是否已启动");
    throw e;
  } finally {
    clearTimeout(timer);
  }
}

export function formatJson(data) {
  return JSON.stringify(data, null, 2);
}
