import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  GetPromptRequestSchema,
  ListPromptsRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { resolveConfig } from "../core/config.js";
import { invokeExposedTool, listExposedTools } from "../core/proxy-tools.js";
import { PRINT_INSTRUCTIONS, PRINT_PROMPT_NAME } from "../core/tool-specs.js";

function log(...args: unknown[]) {
  console.error("[xiaobai-print]", ...args);
}

async function main() {
  const { token, remoteUrl } = resolveConfig();
  if (!token) {
    log("ERROR: OPENCLAW_TOKEN environment variable is required");
    process.exit(1);
  }

  log(`Connecting to remote MCP server: ${remoteUrl}`);
  const allTools = await listExposedTools();
  log(`Discovered ${allTools.length} exposed tools`);

  const server = new Server(
    { name: "xiaobai-print-mcp", version: "1.0.0" },
    { capabilities: { tools: {}, prompts: {} } },
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: allTools,
  }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    log(`Tool call: ${name}`);
    return await invokeExposedTool(name, args);
  });

  server.setRequestHandler(ListPromptsRequestSchema, async () => ({
    prompts: [
      {
        name: PRINT_PROMPT_NAME,
        description: "小白打印助手使用指南 — 打印工作流、纸张尺寸、注意事项",
      },
    ],
  }));

  server.setRequestHandler(GetPromptRequestSchema, async (request) => {
    if (request.params.name !== PRINT_PROMPT_NAME) {
      throw new Error(`Unknown prompt: ${request.params.name}`);
    }

    return {
      description: "小白打印助手使用指南",
      messages: [
        {
          role: "user" as const,
          content: { type: "text" as const, text: PRINT_INSTRUCTIONS },
        },
      ],
    };
  });

  const transport = new StdioServerTransport();
  await server.connect(transport);
  log("Local MCP server running on stdio");
}

main().catch((error) => {
  log("Fatal error:", error);
  process.exit(1);
});
