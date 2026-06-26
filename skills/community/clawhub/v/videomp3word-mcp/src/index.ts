#!/usr/bin/env node
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createHttpApp } from "./httpServer.js";
import { createMcpServer } from "./mcpServer.js";
import { serverConfig } from "./config.js";
import { createPlatform } from "./platform/serviceContainer.js";
import { logger } from "./logger.js";

const isStdio = process.argv.includes("stdio");

async function main() {
  const platform = await createPlatform(serverConfig);
  if (isStdio) {
    const server = createMcpServer(serverConfig, platform);
    const transport = new StdioServerTransport();
    await server.connect(transport);
    logger.info("videomp3word-mcp listening on stdio", { baseUrl: serverConfig.baseUrl });
    return;
  }

  const app = createHttpApp(serverConfig, platform);
  app.listen(serverConfig.port, serverConfig.host, () => {
    logger.info("videomp3word-mcp listening on http", {
      host: serverConfig.host,
      port: serverConfig.port,
      baseUrl: serverConfig.baseUrl,
    });
  });
}

main().catch((error) => {
  logger.error("Fatal error starting server", {
    message: error instanceof Error ? error.message : String(error),
  });
  process.exit(1);
});
