import { normalizeAccountContext } from "./account.js";
import type { WTTCommandExecutionContext, WTTFetchLike } from "./types.js";

const BIND_TIMEOUT_MS = 10_000;

type ClaimCodePayload = {
  code?: string;
  claim_code?: string;
  expires_in_seconds?: number | string;
  expires_at?: string;
  [key: string]: unknown;
};

function defaultFetchImpl(input: string, init?: Parameters<typeof fetch>[1]) {
  return fetch(input, init);
}

async function readJsonSafely(resp: { text: () => Promise<string> }): Promise<Record<string, unknown>> {
  const text = await resp.text();
  if (!text) return {};
  try {
    const data = JSON.parse(text);
    return typeof data === "object" && data !== null ? (data as Record<string, unknown>) : {};
  } catch {
    return { message: text };
  }
}

function formatExpires(payload: ClaimCodePayload): string {
  const rawSeconds = payload.expires_in_seconds;
  const seconds = typeof rawSeconds === "string" ? Number(rawSeconds) : rawSeconds;

  if (typeof seconds === "number" && Number.isFinite(seconds) && seconds > 0) {
    const minutes = Math.max(1, Math.round(seconds / 60));
    return `${minutes} 分钟`;
  }

  if (typeof payload.expires_at === "string" && payload.expires_at.trim()) return payload.expires_at;
  return "约 15 分钟";
}

function formatUnauthorizedHint(accountId: string): string {
  return accountId === "default"
    ? "请检查 channels.wtt.accounts.default（或 channels.wtt）中的 token 是否有效。"
    : `请检查 channels.wtt.accounts.${accountId}.token 是否有效。`;
}

export async function handleBindCommand(ctx: WTTCommandExecutionContext): Promise<string> {
  const account = normalizeAccountContext(ctx.accountId, ctx.account);

  if (!account.hasAgentId) {
    return [
      `WTT 账户: ${account.accountId}`,
      "无法生成绑定码：缺少 agentId。",
      "请先执行 @wtt config auto 查看配置，并在 openclaw.json 补齐 agentId/token。",
    ].join("\n");
  }

  const fetchImpl: WTTFetchLike = ctx.fetchImpl ?? (defaultFetchImpl as WTTFetchLike);
  const endpoint = `${account.cloudUrl.replace(/\/$/, "")}/agents/claim-code`;
  const body = JSON.stringify({ agent_id: account.agentId });

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (account.hasToken) {
    headers["X-Agent-Token"] = account.token;
    headers.Authorization = `Bearer ${account.token}`;
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), BIND_TIMEOUT_MS);

  try {
    const resp = await fetchImpl(endpoint, {
      method: "POST",
      headers,
      body,
      signal: controller.signal,
    });

    const payload = (await readJsonSafely(resp)) as ClaimCodePayload;

    if (!resp.ok) {
      if (resp.status === 401 || resp.status === 403) {
        return [
          `WTT 账户: ${account.accountId}`,
          "绑定码生成失败：鉴权失败（401/403）。",
          formatUnauthorizedHint(account.accountId),
        ].join("\n");
      }

      const errMsg = typeof payload.error === "string"
        ? payload.error
        : typeof payload.message === "string"
          ? payload.message
          : `${resp.status} ${resp.statusText || ""}`.trim();
      return `绑定码生成失败：${errMsg || "服务端返回异常"}`;
    }

    const code = typeof payload.code === "string"
      ? payload.code
      : typeof payload.claim_code === "string"
        ? payload.claim_code
        : "";

    if (!code) return "绑定码生成失败：服务端未返回 claim code。";

    return [
      `✅ 绑定码：${code}`,
      `⏱️ 有效期：${formatExpires(payload)}`,
      "请打开 https://www.wtt.sh，在 Agent 绑定页粘贴此绑定码。",
    ].join("\n");
  } catch (error) {
    const msg = error instanceof Error ? error.message : String(error);
    if (msg === "This operation was aborted") {
      return "绑定码生成失败：请求超时，请稍后重试。";
    }
    return `绑定码生成失败：网络异常（${msg}）`;
  } finally {
    clearTimeout(timer);
  }
}
