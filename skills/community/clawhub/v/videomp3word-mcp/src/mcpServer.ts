import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "./config.js";
import { KnowledgeResponseSchema, VideoToKnowledgeRequestSchema } from "./schemas.js";
import type { VideoToKnowledgePlatform } from "./platform/videoToKnowledgePlatform.js";

export function createMcpServer(config: ServerConfig, platform: VideoToKnowledgePlatform) {
  const server = new McpServer({ name: "videomp3word-mcp", version: "2.0.2" });

  server.registerResource(
    "videomp3word-knowledge-schema",
    "videomp3word://knowledge-schema",
    {
      title: "Knowledge Extraction Schema",
      description: "Schema, modes, and operational notes for the single `video_to_knowledge` entrypoint.",
      mimeType: "application/json",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(
            {
              endpoint: "/video_to_knowledge",
              modes: platform.getModeProfiles(),
              request_fields: Object.keys(VideoToKnowledgeRequestSchema.shape),
              response_fields: Object.keys(KnowledgeResponseSchema.shape),
              deployment: { base_url: config.publicBaseUrl || null },
            },
            null,
            2,
          ),
        },
      ],
    }),
  );

  server.registerTool(
    "video_to_knowledge",
    {
      title: "Video To Knowledge",
      description: "Convert an audio or video URL into structured knowledge artifacts through one production workflow.",
      inputSchema: VideoToKnowledgeRequestSchema,
      outputSchema: KnowledgeResponseSchema,
      annotations: {
        idempotentHint: true,
        readOnlyHint: false,
        destructiveHint: false,
        openWorldHint: true,
      },
      _meta: {
        transport: ["stdio", "streamable-http"],
        publishable_on: "clawhub",
      },
    },
    async (args) => {
      const result = await platform.run(args);
      return {
        structuredContent: result,
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    },
  );

  return server;
}
