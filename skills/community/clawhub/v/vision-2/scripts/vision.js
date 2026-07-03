#!/usr/bin/env node
/**
 * Vision - 让没有识图能力的模型获得识图能力
 *
 * 用法:
 *   node vision.js <图片路径> [问题]
 *   node vision.js --url <图片链接> [问题]
 *   node vision.js --setup          # 首次配置
 *   node vision.js --config         # 查看当前配置
 *
 * 配置文件: ~/.claude/skills/vision/config.json
 */

const fs = require("fs");
const path = require("path");
const https = require("https");
const http = require("http");
const readline = require("readline");

// 配置文件路径
const SKILL_DIR = path.resolve(__dirname, "..");
const CONFIG_FILE = path.join(SKILL_DIR, "config.json");

// 默认配置
const DEFAULT_CONFIG = {
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  api_key: "",
  model: "qwen3.5-omni-plus"
};

// 加载配置
function loadConfig() {
  // 读取 config.json
  if (fs.existsSync(CONFIG_FILE)) {
    try {
      const config = JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
      return config;
    } catch (e) {
      console.error("⚠️ 配置文件格式错误:", e.message);
    }
  }

  // 回退到环境变量（兼容旧版本）
  try { require("dotenv").config({ path: path.join(SKILL_DIR, ".env") }); } catch {}

  if (process.env.DASHSCOPE_API_KEY) {
    return {
      base_url: process.env.DASHSCOPE_BASE_URL || "https://dashscope.aliyuncs.com/compatible-mode/v1",
      api_key: process.env.DASHSCOPE_API_KEY,
      model: process.env.VISION_MODEL || "qwen3.5-omni-plus"
    };
  }

  // 返回默认配置（API Key 为空）
  return DEFAULT_CONFIG;
}

// 保存配置
function saveConfig(config) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), "utf-8");
}

// 交互式配置
async function setup() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const question = (q) => new Promise((resolve) => rl.question(q, resolve));

  console.log("\n╔════════════════════════════════════════════════════════════╗");
  console.log("║              🖼️  Vision 图片识别配置                      ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");

  // 读取当前配置
  const currentConfig = loadConfig();

  console.log("推荐使用阿里云千问（新用户有 100 万 token 免费额度）");
  console.log("📎 获取 API Key: https://bailian.console.aliyun.com/\n");

  const apiKey = await question(`请输入 API Key (当前: ${currentConfig.api_key ? "****" + currentConfig.api_key.slice(-4) : "未设置"}): `);
  const baseUrl = await question(`请输入 API 地址 (当前: ${currentConfig.base_url}, 回车保持): `) || currentConfig.base_url;
  const model = await question(`请输入模型名称 (当前: ${currentConfig.model}, 回车保持): `) || currentConfig.model;

  // 构建配置
  const config = {
    base_url: baseUrl.trim(),
    api_key: apiKey.trim() || currentConfig.api_key,
    model: model.trim()
  };

  // 保存配置
  saveConfig(config);

  console.log("\n╔════════════════════════════════════════════════════════════╗");
  console.log("║                    ✅ 配置完成！                          ║");
  console.log("╚════════════════════════════════════════════════════════════╝");
  console.log(`\n配置已保存到: ${CONFIG_FILE}`);
  console.log("\n使用方法：");
  console.log('  node vision.js "图片路径" "描述这张图片"');
  console.log('  node vision.js "图1.jpg" "图2.jpg" "比较这些图片"\n');

  rl.close();
}

// 显示当前配置
function showConfig() {
  const config = loadConfig();

  console.log("\n╔════════════════════════════════════════════════════════════╗");
  console.log("║                    📋 当前配置                            ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");
  console.log(`  API 地址:   ${config.base_url}`);
  console.log(`  模型名称:   ${config.model}`);
  console.log(`  API Key:    ${config.api_key ? "****" + config.api_key.slice(-4) : "❌ 未设置"}`);
  console.log(`  配置文件:   ${CONFIG_FILE}\n`);

  if (!config.api_key) {
    console.log("  💡 请运行 `node vision.js --setup` 或手动编辑配置文件设置 API Key\n");
  }
}

function parseArgs() {
  const argv = process.argv.slice(2);
  let images = [], prompt = "";

  // 检查特殊模式
  if (argv[0] === "--setup") return { action: "setup" };
  if (argv[0] === "--config") return { action: "config" };
  if (argv[0] === "--help" || argv[0] === "-h") return { action: "help" };

  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--url" && argv[i + 1]) {
      images.push({ source: argv[++i], isUrl: true });
    } else if (!argv[i].startsWith("--") && !prompt) {
      const resolved = path.resolve(argv[i]);
      if (fs.existsSync(resolved) || argv[i].startsWith("http")) {
        images.push({ source: argv[i], isUrl: argv[i].startsWith("http") });
      } else {
        prompt = argv.slice(i).join(" ");
        break;
      }
    } else if (!argv[i].startsWith("--")) {
      prompt = prompt ? prompt + " " + argv[i] : argv[i];
    }
  }
  if (!prompt) prompt = "请详细描述这些图片的内容。";
  return { action: "run", images, prompt };
}

function resolveImageUrl(source, isUrl) {
  if (isUrl) return source;
  const resolved = path.resolve(source);
  if (!fs.existsSync(resolved)) throw new Error(`文件不存在: ${resolved}`);
  const ext = path.extname(resolved).toLowerCase().replace(".", "");
  const mimeMap = { jpg: "jpeg", jpeg: "jpeg", png: "png", gif: "gif", webp: "webp", bmp: "bmp" };
  const data = fs.readFileSync(resolved);
  return `data:image/${mimeMap[ext] || "jpeg"};base64,${data.toString("base64")}`;
}

function request(baseUrl, apiKey, payload) {
  const url = new URL(baseUrl.replace(/\/?$/, "/") + "chat/completions");
  const body = JSON.stringify(payload);
  const transport = url.protocol === "https:" ? https : http;

  return new Promise((resolve, reject) => {
    const req = transport.request(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    }, (res) => {
      let data = "";
      res.on("data", (c) => data += c);
      res.on("end", () => {
        if (res.statusCode >= 400) return reject(new Error(`API ${res.statusCode}: ${data.slice(0, 300)}`));
        try {
          resolve(JSON.parse(data)?.choices?.[0]?.message?.content || data);
        } catch { resolve(data); }
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

function showHelp() {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║                    🖼️  Vision 使用帮助                     ║
╚════════════════════════════════════════════════════════════╝

用法:
  node vision.js <图片路径> [问题]
  node vision.js <图片1> <图片2> [问题]      # 多张图片
  node vision.js --url <图片链接> [问题]     # 网络图片

命令:
  --setup     首次配置（交互式）
  --config    查看当前配置
  --help      显示此帮助

示例:
  node vision.js photo.jpg "描述这张图片"
  node vision.js img1.jpg img2.jpg "比较这两张图"
  node vision.js --url https://example.com/img.png "这是什么？"

配置文件:
  ~/.claude/skills/vision/config.json
`);
}

async function main() {
  const args = parseArgs();

  switch (args.action) {
    case "setup":
      await setup();
      return;

    case "config":
      showConfig();
      return;

    case "help":
      showHelp();
      return;

    case "run":
      break;
  }

  // 加载配置
  const config = loadConfig();

  // 如果配置文件不存在，自动创建默认配置
  if (!fs.existsSync(CONFIG_FILE)) {
    saveConfig(DEFAULT_CONFIG);
    console.log(`\n📝 已创建默认配置文件: ${CONFIG_FILE}\n`);
  }

  if (!config.api_key) {
    console.error("\n❌ 未配置 API Key\n");
    console.log("请选择一种方式配置：\n");
    console.log("  1. 交互式配置: node vision.js --setup");
    console.log(`  2. 手动编辑: ${CONFIG_FILE}\n`);
    process.exit(1);
  }

  const { images, prompt } = args;
  if (!images || images.length === 0) {
    showHelp();
    process.exit(1);
  }

  try {
    // 构建包含多张图片的 content 数组
    const content = [];
    for (const img of images) {
      const imageUrl = resolveImageUrl(img.source, img.isUrl);
      content.push({ type: "image_url", image_url: { url: imageUrl } });
    }
    content.push({ type: "text", text: prompt });

    const result = await request(config.base_url, config.api_key, {
      model: config.model,
      messages: [{ role: "user", content }],
      stream: false,
      max_tokens: 1024,
    });
    console.log(result);
  } catch (err) {
    console.error("识图失败:", err.message);
    process.exit(1);
  }
}

main();
