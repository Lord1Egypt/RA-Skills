#!/usr/bin/env node
/**
 * zentao-utils.js — 禅道脚本共享工具模块
 *
 * 提供跨脚本复用的通用功能：
 * - 命令行参数解析
 * - CDP 浏览器连接 + context/page 复用
 * - 配置文件读取
 *
 * 用法:
 *   const { parseArgs, connectAndGetPage, readConfig } = require('./zentao-utils');
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DEFAULT_ZENTAO_URL = 'http://zentao.gxatek.com:20080';

/**
 * 工作空间搜索路径（按优先级排列）。
 * 供 readConfig() 和 zentao-login.js 共用，避免硬编码重复。
 */
const WORKSPACE_DIRS = (() => {
  const home = process.env.USERPROFILE || process.env.HOME;
  return [
    path.join(home, '.openclaw-auto-bug-analyze', 'workspace'),
    path.join(home, '.openclaw', 'workspace'),
  ];
})();

/**
 * 从命令行参数解析配置。
 *
 * @param {Object} defaults - 默认值 { wsEndpoint, bugId, zentaoUrl, ... }
 * @returns {Object} 解析后的配置对象
 *
 * 支持的参数格式（统一处理 --key=value）：
 *   --ws=...  → wsEndpoint
 *   --bug-id=... → bugId (parseInt)
 *   --zentao-url=... → zentaoUrl
 *   --dir=... → outputDir
 *   --comment-file=... → commentFile
 *   --comment=... → comment
 *
 * 注意：--comment-file 优先于 --comment（在 post-comment 脚本中处理互斥）。
 */
function parseArgs(defaults = {}) {
  const args = process.argv.slice(2);
  const config = {
    wsEndpoint: defaults.wsEndpoint || '',
    bugId: defaults.bugId || 0,
    zentaoUrl: defaults.zentaoUrl || DEFAULT_ZENTAO_URL,
    ...defaults,
  };

  for (const arg of args) {
    if (arg.startsWith('--ws=')) config.wsEndpoint = arg.slice(5);
    else if (arg.startsWith('--bug-id=')) config.bugId = parseInt(arg.slice(9), 10);
    else if (arg.startsWith('--zentao-url=')) config.zentaoUrl = arg.split('=')[1];
    else if (arg.startsWith('--dir=')) config.outputDir = arg.slice(6);
    else if (arg.startsWith('--comment-file=')) config.commentFile = arg.slice(15);
    else if (arg.startsWith('--comment=')) config.comment = arg.slice(10);
    else if (arg.startsWith('--port=')) config.port = parseInt(arg.split('=')[1], 10);
    else if (arg.startsWith('--account=')) config.account = arg.split('=')[1];
    else if (arg.startsWith('--password=')) config.password = arg.split('=')[1];
  }

  return config;
}

/**
 * 连接到已运行的 Playwright 浏览器并返回复用的 page 对象。
 *
 * @param {string} wsEndpoint - CDP WebSocket endpoint（来自 zentao-login.js 输出）
 * @param {Object} opts - 可选 { timeout: 30000 }
 * @returns {Promise<{browser: Browser, page: Page}>}
 */
async function connectAndGetPage(wsEndpoint, opts = {}) {
  const timeout = opts.timeout || 30000;
  const browser = await chromium.connectOverCDP(wsEndpoint, { timeout });

  const contexts = browser.contexts();
  if (contexts.length === 0) {
    throw new Error('浏览器无可用 context，登录会话可能已过期，请重新运行 zentao-login.js');
  }
  const pages = contexts[0].pages();
  if (pages.length === 0) {
    throw new Error('浏览器无可用 page，登录会话可能已过期，请重新运行 zentao-login.js');
  }

  return { browser, page: pages[0] };
}

/**
 * 从 bug-analyzer-config.json 读取配置。
 * 按优先级搜索多个可能的路径。
 *
 * @returns {Object|null} 解析后的配置对象，未找到返回 null
 */
function readConfig() {
  for (const dir of WORKSPACE_DIRS) {
    const configPath = path.join(dir, 'bug-analyzer-config.json');
    if (fs.existsSync(configPath)) {
      try {
        return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
      } catch (e) {
        console.error(`[WARN] 配置文件解析失败: ${configPath} - ${e.message}`);
        return null;
      }
    }
  }
  return null;
}

module.exports = { parseArgs, connectAndGetPage, readConfig, WORKSPACE_DIRS, DEFAULT_ZENTAO_URL };
