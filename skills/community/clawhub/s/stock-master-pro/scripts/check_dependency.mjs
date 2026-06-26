#!/usr/bin/env node

/**
 * 依赖检查脚本
 * 检查 QVeris AI 技能是否已安装，如未安装则提示用户安装
 */

import { existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
// QVeris 安装在 ~/.openclaw/skills/qveris-official/
const QVERIS_SKILL_PATH = process.env.HOME + '/.openclaw/skills/qveris-official/SKILL.md';
const QVERIS_CLI_PATH = process.env.HOME + '/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs';

/**
 * 检查 QVeris 依赖
 * @returns {Object} 检查结果
 */
export function checkQverisDependency() {
  const result = {
    installed: false,
    cliAvailable: false,
    apiKeySet: false,
    message: ''
  };

  // 检查 SKILL.md 是否存在
  if (existsSync(QVERIS_SKILL_PATH)) {
    result.installed = true;
  } else {
    result.message = 'QVeris AI 技能未安装';
    return result;
  }

  // 检查 CLI 工具是否存在
  if (existsSync(QVERIS_CLI_PATH)) {
    result.cliAvailable = true;
  } else {
    result.message = 'QVeris CLI 工具未找到';
    return result;
  }

  // 检查 API Key 是否设置
  const apiKey = process.env.QVERIS_API_KEY;
  if (apiKey && apiKey.startsWith('sk-')) {
    result.apiKeySet = true;
  } else {
    result.message = 'QVERIS_API_KEY 环境变量未设置或格式不正确';
    return result;
  }

  // 全部检查通过
  result.message = 'QVeris AI 依赖已就绪';
  return result;
}

/**
 * 获取安装指南
 * @returns {string} 安装指南文本
 */
export function getInstallationGuide() {
  return `
╔══════════════════════════════════════════════════════════════════════════════╗
║                        ⚠️  需要安装 QVeris AI 技能                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Stock Master Pro 依赖 QVeris AI 提供 A 股实时数据。                           ║
║  请按以下步骤安装（2 分钟即可完成）：                                          ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────┐        ║
║  │  1️⃣  访问 QVeris 官网注册（免费）                                │        ║
║  │                                                                  │        ║
║  │      👉 https://qveris.ai/?ref=y9d7PKgdPcPC-A                    │        ║
║  │                                                                  │        ║
║  │      💡 通过此链接注册可获得额外优惠                              │        ║
║  └─────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────┐        ║
║  │  2️⃣  在首页复制安装命令                                          │        ║
║  │                                                                  │        ║
║  │      注册登录后，在首页点击"复制安装命令"                         │        ║
║  │      （类似：skillhub install qveris）                           │        ║
║  └─────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────┐        ║
║  │  3️⃣  在终端运行安装命令                                          │        ║
║  │                                                                  │        ║
║  │      粘贴并回车，自动完成安装                                    │        ║
║  └─────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────┐        ║
║  │  4️⃣  安装完成后重新运行本技能                                    │        ║
║  │                                                                  │        ║
║  │      API Key 会自动配置，无需手动设置                            │        ║
║  └─────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
║  📞 遇到问题？访问 https://qveris.ai 查看文档                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
`.trim();
}

/**
 * 主函数
 */
function main() {
  console.log('🔍 检查 Stock Master Pro 依赖...\n');
  
  const result = checkQverisDependency();
  
  if (result.installed && result.cliAvailable && result.apiKeySet) {
    console.log('✅ ' + result.message);
    console.log('\n✨ 所有依赖已就绪，可以开始使用 Stock Master Pro！\n');
    process.exit(0);
  } else {
    console.log('❌ ' + result.message);
    console.log('\n');
    console.log(getInstallationGuide());
    console.log('\n');
    process.exit(1);
  }
}

// 如果直接运行此脚本
if (process.argv[1] && process.argv[1].includes('check_dependency.mjs')) {
  main();
}
