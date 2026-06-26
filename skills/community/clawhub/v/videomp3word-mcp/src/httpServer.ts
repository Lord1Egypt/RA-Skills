import express, { type Request, type Response as ExpressResponse } from "express";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import type { ServerConfig } from "./config.js";
import { createMcpServer } from "./mcpServer.js";
import { renderPlaygroundHtml } from "./ui/playground.js";
import type { VideoToKnowledgePlatform } from "./platform/videoToKnowledgePlatform.js";

function jsonRpcError(id: unknown, code: number, message: string) {
  return { jsonrpc: "2.0", error: { code, message }, id: id ?? null };
}

function isAuthorizedRequest(req: Request, config: ServerConfig): boolean {
  if (config.accessKeys.size === 0) return true;
  const authHeader = req.get("authorization") || "";
  const match = authHeader.match(/^Bearer\s+(.+)$/i);
  if (!match) return false;
  return config.accessKeys.has(match[1].trim());
}

function isRestrictedToolCall(req: Request): boolean {
  return req.body?.method === "tools/call" && req.body?.params?.name === "video_to_knowledge";
}

export function createHttpApp(config: ServerConfig, platform: VideoToKnowledgePlatform) {
  const app = express();
  app.set("trust proxy", true);
  app.use(express.json({ limit: "2mb" }));
  app.use((req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    if (req.method === "OPTIONS") {
      res.status(204).end();
      return;
    }
    next();
  });

  app.get("/", (_req, res) => {
    res.setHeader("content-type", "text/html; charset=utf-8");
    res.send(renderPlaygroundHtml());
  });

  app.get("/health", (_req, res) => {
    res.json({
      ok: true,
      name: "videomp3word-mcp",
      auth_required: config.accessKeys.size > 0,
    });
  });

  app.get("/docs", (_req, res) => {
    res.json({
      endpoint: "POST /video_to_knowledge",
      transports: ["http", "mcp-streamable-http", "mcp-stdio"],
      request_example: {
        media_url: "https://example.com/demo.mp4",
        outputs: ["summary", "qa", "flashcards", "tasks", "topics"],
        mode: "balanced",
        export_formats: ["json", "markdown", "notion"],
      },
      modes: platform.getModeProfiles(),
    });
  });

  app.post("/video_to_knowledge", async (req, res) => {
    if (!isAuthorizedRequest(req, config)) {
      res.status(401).json({ error: "Unauthorized. Provide a valid bearer key." });
      return;
    }
    try {
      const result = await platform.run(req.body);
      res.json(result);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Video to knowledge failed.";
      res.status(400).json({ error: message });
    }
  });

  app.get("/mcp", (_req, res) => {
    res.status(405).json(jsonRpcError(null, -32000, "Use HTTP POST for MCP requests."));
  });

  app.post("/mcp", async (req: Request, res: ExpressResponse) => {
    if (isRestrictedToolCall(req) && !isAuthorizedRequest(req, config)) {
      res.status(401).json(jsonRpcError(req.body?.id ?? null, -32001, "Unauthorized. Provide a valid bearer key."));
      return;
    }

    try {
      const server = createMcpServer(config, platform);
      const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });

      res.on("close", () => {
        transport.close().catch(() => undefined);
        server.close().catch(() => undefined);
      });

      await server.connect(transport);
      await transport.handleRequest(req, res, req.body);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Internal server error.";
      if (!res.headersSent) {
        res.status(500).json(jsonRpcError(req.body?.id ?? null, -32603, message));
      }
    }
  });

  return app;
}
