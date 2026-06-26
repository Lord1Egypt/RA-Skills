import type { RemoteConfig } from "./types.js";

export const DEFAULT_REMOTE_URL =
  "https://mcp.gongfudou.com/mcp/openclaw/sse";

export function resolveConfig(config?: RemoteConfig) {
  const token =
    config?.token ??
    process.env.MY_MCP_TOKEN ??
    process.env.OPENCLAW_TOKEN;
  const remoteUrl =
    config?.remoteUrl ??
    process.env.MY_MCP_UPSTREAM_URL ??
    process.env.OPENCLAW_MCP_URL ??
    DEFAULT_REMOTE_URL;

  return { token, remoteUrl };
}
