import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const entry = resolve(__dirname, "../dist/index.js");
const required = [
  "slzq_open_v1_auth_status",
  "slzq_open_v1_auth_agreement",
  "slzq_open_v1_auth_send_code",
  "slzq_open_v1_auth_login",
  "slzq_open_v1_health",
  "slzq_open_v1_me",
  "slzq_open_v1_catalog_hot",
  "slzq_open_v1_market_snapshot",
  "slzq_open_v1_positions",
  "slzq_open_v1_orders_place",
  "slzq_open_v1_orders_cancel",
];

function fail(message, next) {
  console.error(`FAIL: ${message}`);
  console.error(`下一步：${next}`);
  process.exit(1);
}

if (!existsSync(entry)) {
  fail("未找到 MCP 入口 dist/index.js", "请先执行 npm run build，或重新下载包含预编译 dist 的能力包。");
}

const transport = new StdioClientTransport({
  command: "node",
  args: [entry],
  env: { ...process.env },
});
const client = new Client({ name: "slzq-trading-tool-check", version: "1.0.0" });

try {
  await client.connect(transport);
  const result = await client.listTools();
  const names = new Set((result.tools ?? []).map((tool) => tool.name));
  const missing = required.filter((name) => !names.has(name));
  if (missing.length > 0) {
    fail(`MCP tools/list 缺少核心工具：${missing.join(", ")}`, "请确认当前加载的是新版 slzq-trading MCP，并完全重启客户端后新开会话。");
  }
  console.log(`PASS: MCP tools/list 包含 ${required.length} 个核心工具`);
} catch (err) {
  fail(err instanceof Error ? err.message : String(err), "请检查 mcpServers.command/args/env，确保 node 可执行且 args 指向 dist/index.js 的绝对路径。");
} finally {
  await client.close().catch(() => {});
}
