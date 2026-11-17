import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(__dirname, "..");
const mcpEntry = resolve(rootDir, "runtime/mcp/dist/index.js");

const skillName = "slzq-trading";
const domainEnv = "SLZQ_OPENCLAW_DOMAIN";
const apiKeyEnv = "SLZQ_OPENCLAW_API_KEY";
const tradingEnv = "SLZQ_OPENCLAW_ENV";

function valueOrPlaceholder(name, fallback = "") {
  return process.env[name] && process.env[name].trim()
    ? process.env[name].trim()
    : `<${name}${fallback ? ` ${fallback}` : ""}>`;
}

if (!existsSync(mcpEntry)) {
  console.error(`WARN: 未找到 MCP 入口：${mcpEntry}`);
  console.error("下一步：请确认能力包解压完整，目录内应存在 runtime/mcp/dist/index.js。");
}

const config = {
  mcpServers: {
    [skillName]: {
      command: "node",
      args: [mcpEntry],
      env: {
        [domainEnv]: valueOrPlaceholder(domainEnv, "仅 https:// + 主机名"),
        [apiKeyEnv]: valueOrPlaceholder(apiKeyEnv, "App 生成的完整 API Key"),
        [tradingEnv]: valueOrPlaceholder(tradingEnv, "sim 或 live"),
      },
    },
  },
};

console.log(JSON.stringify(config, null, 2));
console.error("");
console.error("将上面的 mcpServers 配置复制到你的智能体客户端 MCP 配置中。");
console.error("注意：args[0] 已自动生成绝对路径；修改配置后请完全重启客户端并新开会话。");
