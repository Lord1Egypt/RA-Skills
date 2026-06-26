import type { WTTCommandAccountContext } from "./types.js";

const DEFAULT_CLOUD_URL = "https://www.waxbyte.com";

export interface NormalizedAccountContext {
  accountId: string;
  source: string;
  cloudUrl: string;
  agentId: string;
  token: string;
  hasAgentId: boolean;
  hasToken: boolean;
  enabled: boolean;
  configured: boolean;
}

export function normalizeAccountContext(
  accountId: string,
  account?: WTTCommandAccountContext,
): NormalizedAccountContext {
  const source = account?.source?.trim() || "channels.wtt";
  const cloudUrl = account?.cloudUrl?.trim() || DEFAULT_CLOUD_URL;
  const agentId = account?.agentId?.trim() || "";
  const token = account?.token?.trim() || "";
  const hasAgentId = agentId.length > 0;
  const hasToken = token.length > 0;

  return {
    accountId,
    source,
    cloudUrl,
    agentId,
    token,
    hasAgentId,
    hasToken,
    enabled: account?.enabled !== false,
    configured: account?.configured ?? (hasAgentId && hasToken),
  };
}

export function maskToken(raw: string): string {
  const token = raw.trim();
  if (!token) return "未配置";
  if (token.length <= 8) return `${token[0]}***${token[token.length - 1]}`;
  return `${token.slice(0, 4)}***${token.slice(-4)}`;
}

export function missingRequiredFields(account: NormalizedAccountContext): string[] {
  const missing: string[] = [];
  if (!account.hasAgentId) missing.push("agentId");
  if (!account.hasToken) missing.push("token");
  return missing;
}
