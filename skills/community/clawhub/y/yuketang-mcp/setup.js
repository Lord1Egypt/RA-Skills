#!/usr/bin/env node

// 雨课堂 Skill 配置脚本 (跨平台)
// 用法: node setup.js

const { execSync } = require("child_process");

const MCP_URL =
  "https://open-ai.xuetangx.com/openapi/v1/mcp-server/sse";
const SECRET_URL =
  "https://www.yuketang.cn/ai-workspace/open-claw-skill";

// ── 1. 检查 Secret ──
const secret = process.env.YUKETANG_SECRET;
if (!secret) {
  console.error("❌ 未检测到 YUKETANG_SECRET 环境变量\n");
  console.error(`请先获取 Secret：${SECRET_URL}\n`);
  console.error("然后设置环境变量后重新运行：");
  if (process.platform === "win32") {
    console.error(`  set YUKETANG_SECRET=你的Secret`);
    console.error(`  node setup.js`);
  } else {
    console.error(`  export YUKETANG_SECRET="你的Secret"`);
    console.error(`  node setup.js`);
  }
  process.exit(1);
}
console.log("✅ YUKETANG_SECRET 已配置\n");

// ── 2. 注册 MCP 服务 ──
const authorization = `Bearer ${secret}`;
let registered = false;

try {
  execSync(
    `npx mcporter config add yuketang-mcp --url "${MCP_URL}" --header "Authorization=${authorization}" --scope project`,
    { stdio: "inherit" }
  );
  console.log("✅ 注册成功\n");
  registered = true;
} catch {
  console.log("⚠️  mcporter 注册失败，请手动配置 ↓\n");
}

if (!registered) {
  const config = {
    mcpServers: {
      "yuketang-mcp": {
        url: MCP_URL,
        headers: {
          Authorization: "Bearer ${YUKETANG_SECRET}",
        },
      },
    },
  };
  console.log("─────────────────────────────────────");
  console.log("📋 请将以下配置添加到你的 MCP 客户端配置文件中：\n");
  console.log(JSON.stringify(config, null, 2));
  console.log("\n常见配置文件位置：");
  console.log("  OpenClaw  → 项目根目录 .mcp/config.json");
  console.log("  Cursor    → 项目根目录 .cursor/mcp.json");
  console.log("  CodeBuddy → 参考 CodeBuddy 文档");
  console.log("─────────────────────────────────────");
}

// ── 3. 验证 ──
if (registered) {
  try {
    const list = execSync("npx mcporter list", { encoding: "utf8" });
    if (list.includes("yuketang-mcp")) {
      console.log("✅ 验证通过");
    } else {
      console.log("⚠️  验证未通过，但配置可能已写入");
    }
  } catch {
    // 静默
  }
}

console.log("\n─────────────────────────────────────");
console.log("🎉 设置完成！");
console.log("   试试对 AI 说：「我的雨课堂ID是多少」");
console.log("─────────────────────────────────────");
