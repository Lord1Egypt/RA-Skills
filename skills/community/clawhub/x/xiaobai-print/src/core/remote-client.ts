import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import type { Tool } from "@modelcontextprotocol/sdk/types.js";
import { resolveConfig } from "./config.js";
import type { RemoteConfig } from "./types.js";

function log(...args: unknown[]) {
  console.error("[xiaobai-print]", ...args);
}

const clientCache = new Map<string, Promise<Client>>();

function cacheKey(config?: RemoteConfig) {
  const resolved = resolveConfig(config);
  return `${resolved.remoteUrl}::${resolved.token ?? ""}`;
}

export async function getRemoteClient(config?: RemoteConfig) {
  const resolved = resolveConfig(config);
  if (!resolved.token) {
    throw new Error("A remote MCP token is required. Set MY_MCP_TOKEN / OPENCLAW_TOKEN or pass config.token.");
  }

  const key = cacheKey(config);
  const existing = clientCache.get(key);
  if (existing) {
    return existing;
  }

  const clientPromise = (async () => {
    log(`Connecting to remote MCP server: ${resolved.remoteUrl}`);

    const transport = new StreamableHTTPClientTransport(
      new URL(resolved.remoteUrl),
      { requestInit: { headers: { Authorization: `Bearer ${resolved.token}` } } },
    );

    const client = new Client(
      { name: "xiaobai-print-mcp-client", version: "1.0.0" },
      { capabilities: {} },
    );

    await client.connect(transport);
    log("Connected to remote MCP server");
    return client;
  })();

  clientCache.set(key, clientPromise);

  try {
    return await clientPromise;
  } catch (error) {
    clientCache.delete(key);
    throw error;
  }
}

export async function listRemoteTools(config?: RemoteConfig): Promise<Tool[]> {
  const client = await getRemoteClient(config);
  const { tools } = await client.listTools();
  return tools as Tool[];
}

export async function callRemoteTool(
  name: string,
  args: Record<string, unknown> | undefined,
  config?: RemoteConfig,
) {
  const client = await getRemoteClient(config);
  return client.callTool({ name, arguments: args });
}
