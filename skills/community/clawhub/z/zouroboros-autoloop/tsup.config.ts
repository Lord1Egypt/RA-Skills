import { defineConfig } from "tsup";

export default defineConfig({
  entry: {
    autoloop: "src/autoloop.ts",
    "mcp-server": "src/mcp-server.ts",
  },
  format: ["esm"],
  dts: { entry: "src/autoloop.ts" },
  clean: true,
  target: "node22",
  splitting: false,
  external: ["@modelcontextprotocol/sdk"],
});
