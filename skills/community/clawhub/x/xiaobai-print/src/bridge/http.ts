#!/usr/bin/env node
import http from "node:http";
import { resolveConfig } from "../core/config.js";
import { invokeExposedTool, listExposedTools } from "../core/proxy-tools.js";
import type { RemoteConfig, ToolInvocationResult } from "../core/types.js";

interface BridgeCliOptions {
  host: string;
  port: number;
  remoteUrl?: string;
}

function log(...args: unknown[]) {
  console.error("[xiaobai-print-bridge]", ...args);
}

function usage(): string {
  return [
    "Usage:",
    "  xiaobai-print-bridge [--host 127.0.0.1] [--port 8787] [--remote-url <upstream-mcp-url>]",
    "",
    "Environment:",
    "  MY_MCP_UPSTREAM_URL / OPENCLAW_MCP_URL  Upstream remote MCP endpoint URL",
    "  MY_MCP_TOKEN / OPENCLAW_TOKEN           Default upstream bearer token if the request omits Authorization",
  ].join("\n");
}

function parseArgs(argv: string[]): BridgeCliOptions {
  const options: BridgeCliOptions = {
    host: "127.0.0.1",
    port: 8787,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    const next = argv[index + 1];

    if (current === "--help" || current === "-h") {
      console.log(usage());
      process.exit(0);
    }

    if (current === "--host") {
      if (!next) {
        throw new Error("Missing value for --host");
      }
      options.host = next;
      index += 1;
      continue;
    }

    if (current.startsWith("--host=")) {
      options.host = current.slice("--host=".length);
      continue;
    }

    if (current === "--port") {
      if (!next) {
        throw new Error("Missing value for --port");
      }
      const port = Number(next);
      if (!Number.isInteger(port) || port <= 0) {
        throw new Error(`Invalid port: ${next}`);
      }
      options.port = port;
      index += 1;
      continue;
    }

    if (current.startsWith("--port=")) {
      const port = Number(current.slice("--port=".length));
      if (!Number.isInteger(port) || port <= 0) {
        throw new Error(`Invalid port: ${current.slice("--port=".length)}`);
      }
      options.port = port;
      continue;
    }

    if (current === "--remote-url") {
      if (!next) {
        throw new Error("Missing value for --remote-url");
      }
      options.remoteUrl = next;
      index += 1;
      continue;
    }

    if (current.startsWith("--remote-url=")) {
      options.remoteUrl = current.slice("--remote-url=".length);
      continue;
    }

    throw new Error(`Unknown argument: ${current}`);
  }

  return options;
}

function writeJson(res: http.ServerResponse, status: number, payload: unknown) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
  });
  res.end(`${JSON.stringify(payload, null, 2)}\n`);
}

function extractBearerToken(req: http.IncomingMessage): string | undefined {
  const authorization = req.headers.authorization;
  if (!authorization) {
    return undefined;
  }

  const match = authorization.match(/^Bearer\s+(.+)$/i);
  return match?.[1]?.trim() || undefined;
}

async function readJsonBody(req: http.IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];

  for await (const chunk of req) {
    chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
  }

  if (chunks.length === 0) {
    return {};
  }

  const rawBody = Buffer.concat(chunks).toString("utf8").trim();
  if (!rawBody) {
    return {};
  }

  try {
    return JSON.parse(rawBody);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`Invalid JSON body: ${message}`);
  }
}

function normalizeRequestUrl(req: http.IncomingMessage, options: BridgeCliOptions): URL {
  const host = req.headers.host ?? `${options.host}:${options.port}`;
  return new URL(req.url ?? "/", `http://${host}`);
}

function getRemoteConfig(req: http.IncomingMessage, options: BridgeCliOptions): RemoteConfig {
  const resolved = resolveConfig({
    remoteUrl: options.remoteUrl,
  });

  return {
    token: extractBearerToken(req) ?? resolved.token,
    remoteUrl: resolved.remoteUrl,
  };
}

function extractResultMessage(result: ToolInvocationResult): string {
  for (const item of result.content) {
    if (item && typeof item === "object" && item.type === "text" && typeof item.text === "string") {
      return item.text;
    }
  }

  return "";
}

function statusFromErrorResult(result: ToolInvocationResult): number {
  const message = extractResultMessage(result).toLowerCase();

  if (message.includes("unknown tool")) {
    return 404;
  }

  if (message.includes("required") || message.includes("invalid json")) {
    return 400;
  }

  if (message.includes("token") || message.includes("unauthorized") || message.includes("authentication")) {
    return 401;
  }

  return 502;
}

async function handleToolInvocation(
  req: http.IncomingMessage,
  res: http.ServerResponse,
  toolName: string,
  options: BridgeCliOptions,
) {
  const body = await readJsonBody(req);
  if (!body || typeof body !== "object" || Array.isArray(body)) {
    writeJson(res, 400, { error: "Request body must be a JSON object." });
    return;
  }

  const argsValue = "arguments" in body ? (body as { arguments?: unknown }).arguments : {};
  if (!argsValue || typeof argsValue !== "object" || Array.isArray(argsValue)) {
    writeJson(res, 400, { error: "The \"arguments\" field must be a JSON object." });
    return;
  }

  const result = await invokeExposedTool(toolName, argsValue as Record<string, unknown>, getRemoteConfig(req, options));

  if (result.isError) {
    writeJson(res, statusFromErrorResult(result), result);
    return;
  }

  writeJson(res, 200, result);
}

async function requestHandler(
  req: http.IncomingMessage,
  res: http.ServerResponse,
  options: BridgeCliOptions,
) {
  try {
    const url = normalizeRequestUrl(req, options);

    if (req.method === "GET" && url.pathname === "/health") {
      writeJson(res, 200, {
        ok: true,
        bridge: "xiaobai-print-bridge",
        baseUrl: `http://${options.host}:${options.port}`,
      });
      return;
    }

    if (req.method === "GET" && url.pathname === "/mcp/tools") {
      const tools = await listExposedTools(getRemoteConfig(req, options));
      writeJson(res, 200, { tools });
      return;
    }

    if (req.method === "POST" && url.pathname.startsWith("/mcp/tools/")) {
      const toolName = decodeURIComponent(url.pathname.slice("/mcp/tools/".length));
      if (!toolName) {
        writeJson(res, 400, { error: "Tool name is required." });
        return;
      }

      await handleToolInvocation(req, res, toolName, options);
      return;
    }

    writeJson(res, 404, { error: "Not found." });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    log(`Request failed: ${message}`);
    const status = message.toLowerCase().includes("token") ? 401 : 500;
    writeJson(res, status, { error: message });
  }
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const server = http.createServer((req, res) => {
    void requestHandler(req, res, options);
  });

  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(options.port, options.host, () => {
      server.off("error", reject);
      resolve();
    });
  });

  const resolved = resolveConfig({ remoteUrl: options.remoteUrl });
  log(`Listening on http://${options.host}:${options.port}`);
  log(`Upstream MCP: ${resolved.remoteUrl}`);
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  log(`Fatal error: ${message}`);
  process.exit(1);
});
