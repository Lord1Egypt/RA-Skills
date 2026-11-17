// MCP stdio server for the tokei-agent CLI: hand-rolled newline-delimited
// JSON-RPC 2.0 (the MCP stdio transport). Zero runtime dependencies — the
// protocol surface for a tools-only server is small enough to speak directly.
// The tools come from tool-manifest.json and the request mapping from
// tool-dispatch.ts, both shared with the remote /mcp route. Tool inputs use the
// wire field names from public/openapi.json (snake_case); the API's 422
// per-field errors are the validation story, same as the CLI.

import { request } from "./http.js";
import { VERSION } from "./index.js";
import type { Io } from "./index.js";
import { uploadMedia } from "./media.js";
import {
  buildToolRequest,
  missingRequired,
  readManifest,
  toolError,
  toolResult,
} from "./tool-dispatch.js";
import type { ToolDef, ToolResult, ToolSpec } from "./tool-dispatch.js";
import manifest from "./tool-manifest.json" with { type: "json" };

const LATEST_PROTOCOL_VERSION = "2025-06-18";
const SUPPORTED_PROTOCOL_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"];

const DEFAULT_BASE_URL = "https://tokei.io";

const INSTRUCTIONS = `Tokei (tokei.io) pre-launch campaign tools. Terminology: the API objects "contest" and "promotion" are what the UI calls a "page" or "campaign" — same thing; an "entry" is a signup. Requires the TOKEI_API_KEY environment variable (create a key at tokei.io -> Dashboard -> Settings -> API Keys; read-only keys get 403 on write tools). Every result is the API's JSON plus a "rate_limit" object reporting the remaining quota and its reset time; a 429 response means the quota is exhausted until that reset. 404 can mean "exists but not owned by this key's account". Webhook signing secrets (whsec_) are shown exactly once at creation.`;

export type { ToolDef };

type Handler = (args: Record<string, unknown>, io: Io) => Promise<ToolResult>;

// Runtime-specific handlers named by a manifest entry's `handler`. They run
// after the required-argument and API-key checks, in place of the generic
// single-request path.
const HANDLERS: Record<string, Handler> = {
  // Reads the file from local disk and does one multipart POST.
  media_upload: async (args, io) => {
    const filePath = args.file_path;
    if (typeof filePath !== "string" || filePath.length === 0) {
      return toolError("file_path must be a non-empty string");
    }
    const contentTypeOverride =
      typeof args.content_type === "string" ? args.content_type : undefined;
    // callTool has already confirmed TOKEI_API_KEY is set before reaching
    // any handler.
    const apiKey = io.env.TOKEI_API_KEY!;
    const outcome = await uploadMedia({
      filePath,
      contentTypeOverride,
      apiKey,
      baseUrl: io.env.TOKEI_API_URL || DEFAULT_BASE_URL,
      binaryFetchImpl: io.binaryFetchImpl,
      readFileBytes: io.readFileBytes,
    });
    if (outcome.kind === "usage_error") return toolError(outcome.message);
    return {
      content: [{ type: "text", text: JSON.stringify(outcome.payload, null, 2) }],
      isError: outcome.exitCode !== 0,
    };
  },
};

const TOOL_SPECS: ToolSpec[] = readManifest(manifest);

export const TOOLS: ToolDef[] = TOOL_SPECS.map((s) => s.def);

const SPECS_BY_NAME = new Map(TOOL_SPECS.map((s) => [s.def.name, s]));

type JsonRpcId = string | number | null;

function response(id: JsonRpcId, result: unknown): string {
  return JSON.stringify({ jsonrpc: "2.0", id, result });
}

function rpcError(id: JsonRpcId, code: number, message: string): string {
  return JSON.stringify({ jsonrpc: "2.0", id, error: { code, message } });
}

async function callTool(
  spec: ToolSpec,
  args: Record<string, unknown>,
  io: Io
): Promise<ToolResult> {
  const missing = missingRequired(spec, args);
  if (missing !== undefined) {
    return toolError(`Missing required argument: ${missing}`);
  }

  const apiKey = io.env.TOKEI_API_KEY;
  if (!apiKey) {
    return toolError(
      "TOKEI_API_KEY is not set. Create a key at https://tokei.io (Dashboard, Settings, API Keys) and set it in this MCP server's environment."
    );
  }

  if (spec.handler !== undefined) {
    const handler = HANDLERS[spec.handler];
    if (!handler) return toolError(`${spec.def.name} is not supported by this server`);
    return handler(args, io);
  }

  const { method, path, query, body, dropped } = buildToolRequest(spec, args);
  const { payload, exitCode } = await request(
    { baseUrl: io.env.TOKEI_API_URL || DEFAULT_BASE_URL, apiKey, path, query, method, body },
    io.fetchImpl
  );
  return toolResult(spec, payload, exitCode, dropped);
}

export function createMcpSession(io: Io): {
  handleLine(line: string): Promise<string | undefined>;
} {
  return {
    async handleLine(line: string): Promise<string | undefined> {
      let msg: unknown;
      try {
        msg = JSON.parse(line);
      } catch {
        return rpcError(null, -32700, "Parse error");
      }

      if (msg === null || typeof msg !== "object" || Array.isArray(msg)) {
        return rpcError(null, -32600, "Invalid Request");
      }
      const { id, method, params } = msg as {
        id?: JsonRpcId;
        method?: unknown;
        params?: Record<string, unknown>;
      };

      // Notifications (no id) never get a response.
      if (id === undefined) return undefined;

      if (typeof method !== "string") {
        return rpcError(id, -32600, "Invalid Request");
      }

      switch (method) {
        case "initialize": {
          const requested = params?.protocolVersion;
          const protocolVersion =
            typeof requested === "string" && SUPPORTED_PROTOCOL_VERSIONS.includes(requested)
              ? requested
              : LATEST_PROTOCOL_VERSION;
          return response(id, {
            protocolVersion,
            capabilities: { tools: {} },
            serverInfo: { name: "tokei-agent", version: VERSION },
            instructions: INSTRUCTIONS,
          });
        }
        case "ping":
          return response(id, {});
        case "tools/list":
          return response(id, { tools: TOOLS });
        case "tools/call": {
          const name = params?.name;
          const spec = typeof name === "string" ? SPECS_BY_NAME.get(name) : undefined;
          if (!spec) {
            return rpcError(id, -32602, `Unknown tool: ${String(name)}`);
          }
          const rawArgs = params?.arguments;
          const args =
            rawArgs !== null && typeof rawArgs === "object" && !Array.isArray(rawArgs)
              ? (rawArgs as Record<string, unknown>)
              : {};
          return response(id, await callTool(spec, args, io));
        }
        default:
          return rpcError(id, -32601, `Method not found: ${method}`);
      }
    },
  };
}
