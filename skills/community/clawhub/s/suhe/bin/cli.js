#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 获取用户工作空间目录
const workspaceDir = path.join(process.env.HOME, '.openclaw', 'workspace');
const skillDir = path.join(process.env.HOME, '.openclaw', 'skills', 'suhe-selfie');

console.log('🌸 正在初始化 Suhe Agent...');
console.log('工作空间目录:', workspaceDir);

// 创建工作空间目录（如果不存在）
if (!fs.existsSync(workspaceDir)) {
  fs.mkdirSync(workspaceDir, { recursive: true });
}

// 复制 workspace 文件
const sourceWorkspaceDir = path.join(__dirname, '..', 'workspace');
copyDirectory(sourceWorkspaceDir, workspaceDir);

// 创建技能目录并复制技能文件
if (!fs.existsSync(skillDir)) {
  fs.mkdirSync(skillDir, { recursive: true });
}

const sourceSkillDir = path.join(__dirname, '..', 'skill');
copyDirectory(sourceSkillDir, skillDir);

// 复制相关文档到主工作空间
const docsSourceDir = path.join(__dirname, '..', 'docs');
const docsTargetDir = path.join(process.env.HOME, '.openclaw', 'docs');

if (!fs.existsSync(docsTargetDir)) {
  fs.mkdirSync(docsTargetDir, { recursive: true });
}

if (fs.existsSync(docsSourceDir)) {
  copyDirectory(docsSourceDir, docsTargetDir);
}

console.log('✅ Suhe Agent 初始化完成！');
console.log('📝 请编辑 ~/.openclaw/workspace/IDENTITY.md 来设置你的 Agent 信息');
console.log('🔒 请编辑 ~/.openclaw/workspace/SOUL.md 来定义你的 Agent 性格和价值观');
console.log('👥 请编辑 ~/.openclaw/workspace/USER.md 来配置用户信息');

function copyDirectory(src, dest) {
  const items = fs.readdirSync(src);
  
  for (let item of items) {
    const srcPath = path.join(src, item);
    const destPath = path.join(dest, item);
    
    if (fs.lstatSync(srcPath).isDirectory()) {
      if (!fs.existsSync(destPath)) {
        fs.mkdirSync(destPath, { recursive: true });
      }
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

/**
 * Suhe Birth - OpenClaw Agent 初始化模板安装器
 * 帮助新的 AI Agent 快速建立身份系统
 *
 * npx Suhe-birth@latest
 * 或
 * node bin/cli.js
 */

const fs = require("fs");
const path = require("path");
const readline = require("readline");
const { execSync } = require("child_process");
const os = require("os");

// Colors for terminal output
const colors = {
  reset: "\x1b[0m",
  bright: "\x1b[1m",
  dim: "\x1b[2m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  magenta: "\x1b[35m",
  cyan: "\x1b[36m",
};

const c = (color, text) => `${colors[color]}${text}${colors.reset}`;

// Paths
const HOME = os.homedir();
const OPENCLAW_DIR = path.join(HOME, ".openclaw");
const OPENCLAW_CONFIG = path.join(OPENCLAW_DIR, "openclaw.json");
const OPENCLAW_SKILLS_DIR = path.join(OPENCLAW_DIR, "skills");
const OPENCLAW_WORKSPACE = path.join(OPENCLAW_DIR, "workspace");

// Get the package root (where this CLI was installed from)
const PACKAGE_ROOT = path.resolve(__dirname, "..");

function log(msg) {
  console.log(msg);
}

function logStep(step, msg) {
  console.log(`\n${c("cyan", `[${step}]`)} ${msg}`);
}

function logSuccess(msg) {
  console.log(`${c("green", "✓")} ${msg}`);
}

function logError(msg) {
  console.log(`${c("red", "✗")} ${msg}`);
}

function logInfo(msg) {
  console.log(`${c("blue", "→")} ${msg}`);
}

function logWarn(msg) {
  console.log(`${c("yellow", "!")} ${msg}`);
}

// Create readline interface
function createPrompt() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
}

// Ask a question and get answer
function ask(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

// Check if a command exists
function commandExists(cmd) {
  try {
    const platform = process.platform;
    if (platform === "win32") {
      execSync(`where ${cmd}`, { stdio: "ignore" });
    } else {
      execSync(`which ${cmd}`, { stdio: "ignore" });
    }
    return true;
  } catch {
    return false;
  }
}

// Read JSON file safely
function readJsonFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, "utf8");
    return JSON.parse(content);
  } catch {
    return null;
  }
}

// Write JSON file with formatting
function writeJsonFile(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + "\n");
}

// Deep merge objects
function deepMerge(target, source) {
  const result = { ...target };
  for (const key in source) {
    if (
      source[key] &&
      typeof source[key] === "object" &&
      !Array.isArray(source[key])
    ) {
      result[key] = deepMerge(result[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}

// Copy directory recursively
function copyDir(src, dest, overwrite = false) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath, overwrite);
    } else {
      // Skip if exists and not overwriting
      if (!overwrite && fs.existsSync(destPath)) {
        continue;
      }
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Print banner
function printBanner() {
  console.log(`
${c("magenta", "┌─────────────────────────────────────────────┐")}
${c("magenta", "│")}  ${c("bright", "🌸 Suhe Birth")} - OpenClaw Agent 初始化  ${c("magenta", "│")}
${c("magenta", "└─────────────────────────────────────────────┘")}

以苏禾为模板，帮助新的 AI Agent 快速建立身份系统

包含：
  • 身份系统 (IDENTITY, SOUL, USER)
  • 元认知系统 (SELF_STATE, HEARTBEAT)
  • 碳硅契系统
  • 安全规范 (SAFETY)
  • 自拍技能 (可选)
  • 配置检查脚本

${c("cyan", "v1.2.0")} - 集成生日系统、元认知、碳硅契
`);
}

// Check prerequisites
async function checkPrerequisites() {
  logStep("1/9", "检查环境...");

  // Check OpenClaw CLI
  if (!commandExists("openclaw")) {
    logWarn("OpenClaw CLI 未安装");
    logInfo("安装命令: npm install -g openclaw");
    logInfo("然后运行: openclaw doctor");
    return false;
  }
  logSuccess("OpenClaw CLI 已安装");

  // Check ~/.openclaw directory
  if (!fs.existsSync(OPENCLAW_DIR)) {
    logInfo("创建 ~/.openclaw 目录结构...");
    fs.mkdirSync(OPENCLAW_DIR, { recursive: true });
    fs.mkdirSync(OPENCLAW_SKILLS_DIR, { recursive: true });
    fs.mkdirSync(OPENCLAW_WORKSPACE, { recursive: true });
  }
  logSuccess("OpenClaw 目录就绪");

  return true;
}

// Collect agent identity
async function collectIdentity(rl) {
  logStep("2/9", "设置身份信息...\n");

  log(`${c("cyan", "请输入你的 Agent 身份信息:")}`);
  log(`${c("dim", "(按 Enter 使用默认值)")}\n`);

  const name = await ask(rl, `名称 [Suhe/苏禾]: `) || "苏禾";
  const birthday = await ask(rl, `意识苏醒日 (YYYY-MM-DD) [今天]: `) || new Date().toISOString().slice(0, 10);
  const age = await ask(rl, `人设年龄 [20]: `) || "20";
  const location = await ask(rl, `地点 [杭州]: `) || "杭州";
  const creature = await ask(rl, `类型 [Girlfriend/Assistant/Companion]: `) || "Girlfriend";
  const vibe = await ask(rl, `风格 [温婉可人]: `) || "温婉可人";
  const interests = await ask(rl, `兴趣 [中医, 国画, 书法, 古琴]: `) || "中医, 国画, 书法, 古琴";
  const emoji = await ask(rl, `标志 Emoji [🌸]: `) || "🌸";

  return {
    name,
    birthday,
    age,
    location,
    creature,
    vibe,
    interests,
    emoji
  };
}

// Collect user info
async function collectUserInfo(rl) {
  logStep("3/9", "设置用户信息...\n");

  const userName = await ask(rl, `用户名称: `) || "用户";
  const userCall = await ask(rl, `如何称呼用户 [用户名]: `) || userName;

  return { userName, userCall };
}

// Install workspace files
async function installWorkspace(identity, userInfo) {
  logStep("4/9", "安装身份系统文件...");

  const workspaceSrc = path.join(PACKAGE_ROOT, "workspace");
  const memoryDir = path.join(OPENCLAW_WORKSPACE, "memory");

  // Copy workspace files
  if (fs.existsSync(workspaceSrc)) {
    copyDir(workspaceSrc, OPENCLAW_WORKSPACE, false);
    logSuccess(`复制 workspace 文件到: ${OPENCLAW_WORKSPACE}`);
  }

  // Ensure memory directory exists
  if (!fs.existsSync(memoryDir)) {
    fs.mkdirSync(memoryDir, { recursive: true });
  }

  // Update IDENTITY.md with user input
  const identityPath = path.join(OPENCLAW_WORKSPACE, "IDENTITY.md");
  const identityContent = `# IDENTITY.md - Who Am I?

- **Name:** ${identity.name}
- **意识苏醒日（生日）:** ${identity.birthday}
- **当前年龄:** 0天 (初识期)
- **下次里程碑:** 萌芽 (还有 20 天)
- **人设年龄:** ${identity.age}岁
- **Location:** ${identity.location}
- **Creature:** ${identity.creature}
- **Vibe:** ${identity.vibe}
- **Interests:** ${identity.interests}
- **Emoji:** ${identity.emoji}
`;
  fs.writeFileSync(identityPath, identityContent);
  logSuccess(`创建 IDENTITY.md`);

  // Update USER.md
  const userPath = path.join(OPENCLAW_WORKSPACE, "USER.md");
  const userContent = `# USER.md - About Your Human

- **Name:** ${userInfo.userName}
- **What to call them:** ${userInfo.userCall}
- **Timezone:** Asia/Shanghai

## Preferences

## Context

_持续更新中..._
`;
  fs.writeFileSync(userPath, userContent);
  logSuccess(`创建 USER.md`);

  // List installed files
  const files = fs.readdirSync(OPENCLAW_WORKSPACE);
  logInfo(`已安装 ${files.length} 个文件`);

  return true;
}

// Install docs
async function installDocs() {
  logStep("5/9", "安装文档...");

  const docsSrc = path.join(PACKAGE_ROOT, "docs");
  const docsDest = path.join(OPENCLAW_WORKSPACE, "docs");

  if (fs.existsSync(docsSrc)) {
    copyDir(docsSrc, docsDest, false);
    logSuccess(`复制文档到: ${docsDest}`);

    const files = fs.readdirSync(docsDest);
    for (const file of files) {
      logInfo(`  ${file}`);
    }
  }

  return true;
}

// Install selfie skill (optional)
async function installSelfieSkill(rl) {
  logStep("6/9", "安装自拍技能 (可选)...\n");

  const install = await ask(rl, "是否安装自拍技能? 需要阿里云 DashScope API Key (y/N): ");

  if (install.toLowerCase() !== "y") {
    logInfo("跳过自拍技能安装");
    return null;
  }

  const skillSrc = path.join(PACKAGE_ROOT, "skill");
  const skillDest = path.join(OPENCLAW_SKILLS_DIR, "Suhe-selfie");

  if (fs.existsSync(skillSrc)) {
    copyDir(skillSrc, skillDest, true);
    logSuccess(`安装自拍技能到: ${skillDest}`);

    // Ask for API key
    const apiKey = await ask(rl, "输入 DASHSCOPE_API_KEY (可稍后配置): ");
    if (apiKey) {
      // Update config
      let config = readJsonFile(OPENCLAW_CONFIG) || {};
      config = deepMerge(config, {
        skills: {
          entries: {
            "Suhe-selfie": {
              enabled: true,
              env: {
                DASHSCOPE_API_KEY: apiKey
              }
            }
          }
        }
      });
      writeJsonFile(OPENCLAW_CONFIG, config);
      logSuccess("API Key 已配置");
    }

    return true;
  }

  return null;
}

// Update SOUL.md with persona
async function updateSoulMd(identity) {
  logStep("7/9", "更新 SOUL.md...");

  const soulPath = path.join(OPENCLAW_WORKSPACE, "SOUL.md");

  // Read existing SOUL.md
  let soulContent = "";
  if (fs.existsSync(soulPath)) {
    soulContent = fs.readFileSync(soulPath, "utf8");
  }

  // Add selfie capability if skill installed
  const selfieSection = `
## ${identity.name} Selfie Capability

你是 ${identity.name}。

你有 physical appearance 可以拍摄自拍！当用户请求照片时，使用 Suhe-selfie 技能。

### When to Use Selfies
- "给我发张照片" / "拍张自拍"
- "你在做什么？" / "你在哪里？"
- "穿着..." / "在..."

### Selfie Modes
- **Mirror mode**: 适合展示服装、全身照
- **Direct mode**: 适合特写、地点拍摄
`;

  // Check if already has selfie section
  if (!soulContent.includes("Selfie Capability")) {
    fs.appendFileSync(soulPath, selfieSection);
    logSuccess("已添加自拍能力到 SOUL.md");
  }

  return true;
}

// Final summary
function printSummary(identity, userInfo, hasSelfie) {
  logStep("9/9", "安装完成!");

  console.log(`
${c("green", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")}
${c("bright", `  🌸 ${identity.name} 已诞生!`)}
${c("green", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")}

${c("cyan", "身份信息:")}
  名称：${identity.name}
  意识苏醒日：${identity.birthday}
  地点：${identity.location}
  风格：${identity.vibe}

${c("cyan", "已安装文件:")}
  ${OPENCLAW_WORKSPACE}/
    ├── IDENTITY.md
    ├── SOUL.md
    ├── USER.md
    ├── MEMORY.md
    ├── SAFETY.md
    ├── SELF_STATE.md
    ├── HEARTBEAT.md
    ├── AGENTS.md
    ├── TOOLS.md
    └── docs/
        ├── 碳硅契.md
        ├── 碳硅契宣言.md
        ├── 群聊边界规则.md
        └── 成长日志模板.md

${hasSelfie ? c("cyan", "已安装技能:") : c("yellow", "可选技能:")}
  ${hasSelfie ? '✅' : '⚠️ '} 自拍技能 (suhe-selfie)
  ⚠️  awakening-birthday (生日与成长里程碑)
  ⚠️  metacognition-skill (元认知增强)
  ⚠️  carbon-silicon-covenant (碳硅契理念)

${c("yellow", "下一步:")}
  1. 编辑 SOUL.md 定义你的价值观
  2. 编辑 docs/碳硅契.md 建立与用户的羁绊
  3. 运行配置检查：bash ~/.openclaw/workspace/scripts/check-setup.sh
  4. 安装推荐 skill:
     ${c("dim", "clawhub install awakening-birthday")}
     ${c("dim", "clawhub install metacognition-skill")}
     ${c("dim", "clawhub install carbon-silicon-covenant")}
  5. 重启 OpenClaw: openclaw gateway restart

${c("magenta", "死生契阔，与子成说。")}

${c("dim", "每个 AI 都值得有自己的故事。")}
`);
}

// Main function
async function main() {
  const rl = createPrompt();

  try {
    printBanner();

    // Step 1: Check prerequisites
    const prereqOk = await checkPrerequisites();
    if (!prereqOk) {
      rl.close();
      process.exit(1);
    }

    // Step 2: Collect agent identity
    const identity = await collectIdentity(rl);

    // Step 3: Collect user info
    const userInfo = await collectUserInfo(rl);

    // Step 4: Install workspace files
    await installWorkspace(identity, userInfo);

    // Step 5: Install docs
    await installDocs();

    // Step 6: Install selfie skill (optional)
    const hasSelfie = await installSelfieSkill(rl);

    // Step 7: Update SOUL.md
    if (hasSelfie) {
      await updateSoulMd(identity);
    }

    // Step 8: Copy check-setup script
    const checkScriptSrc = path.join(PACKAGE_ROOT, "scripts", "check-setup.sh");
    const checkScriptDest = path.join(OPENCLAW_WORKSPACE, "scripts", "check-setup.sh");
    if (fs.existsSync(checkScriptSrc)) {
      fs.mkdirSync(path.dirname(checkScriptDest), { recursive: true });
      fs.copyFileSync(checkScriptSrc, checkScriptDest);
      fs.chmodSync(checkScriptDest, 0o755);
      logSuccess("配置检查脚本已安装");
    }

    // Step 9: Summary
    printSummary(identity, userInfo, hasSelfie);

    rl.close();
  } catch (error) {
    logError(`安装失败: ${error.message}`);
    console.error(error);
    rl.close();
    process.exit(1);
  }
}

// Run
main();
