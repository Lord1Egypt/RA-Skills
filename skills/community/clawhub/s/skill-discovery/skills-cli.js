#!/usr/bin/env node
/**
 * Skills CLI Wrapper - npx skills 命令封装
 *
 * 基于官方 npx skills CLI 的可靠封装
 */

const { exec } = require('child_process');
const https = require('https');
const util = require('util');
const { CLI_CONFIG, CLAWHUB_CONFIG } = require('./constants');

const execAsync = util.promisify(exec);

const CONFIG = CLI_CONFIG;

// ==================== 安全工具 ====================

/**
 * 转义 shell 参数，防止命令注入
 * @param {string} input - 用户输入
 * @returns {string} 转义后的安全字符串
 */
function shellEscape(input) {
  if (typeof input !== 'string') return '';
  // 使用单引号包裹并转义单引号（将 ' 替换为 '\''，即先结束单引号，
  // 插入转义单引号，再开始新单引号）
  return `'${input.replace(/'/g, "'\\''")}'`;
}

// ==================== 重试工具 ====================

/**
 * 带重试的执行
 * @param {Function} fn - 异步函数
 * @param {Object} options - 选项
 */
async function withRetry(fn, options = {}) {
  const { maxRetries = CONFIG.maxRetries, retryDelay = CONFIG.retryDelay } = options;

  let lastError;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      // 如果是最后一次，不再重试
      if (i === maxRetries - 1) break;

      // 指数退避
      const delay = retryDelay * Math.pow(2, i);
      console.log(`⚠️  第 ${i + 1} 次尝试失败，${delay}ms 后重试...`);
      await sleep(delay);
    }
  }

  throw lastError;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ==================== 核心命令封装 ====================

/**
 * 列出已安装的 skills
 * @param {Object} options - 选项
 * @returns {Promise<Array>} 已安装 skill 列表
 */
async function skillsList(options = {}) {
  const { global = true, agent } = options;

  let cmd = 'npx skills list --json';
  if (global) cmd += ' -g';
  if (agent) cmd += ` -a ${shellEscape(agent)}`;

  return withRetry(async () => {
    const { stdout } = await execAsync(cmd, { timeout: CONFIG.timeout });

    try {
      const results = JSON.parse(stdout);
      return Array.isArray(results) ? results : [];
    } catch (e) {
      // JSON 解析失败时，尝试提取 JSON 片段
      const fallback = extractJson(stdout);
      if (fallback !== null) {
        return Array.isArray(fallback) ? fallback : [];
      }
      throw new Error(`解析 list 输出失败（JSON & 降级均失败）: ${e.message}`);
    }
  });
}

/**
 * 搜索 skills (skills.sh CLI)
 * 优先尝试 --json 获取结构化输出，降级为文本解析
 * @param {string} query - 搜索关键词
 * @returns {Promise<Array>} 搜索结果
 */
async function skillsFindCli(query) {
  // 参数校验
  if (typeof query !== 'string' || query.trim().length === 0) {
    return [];
  }

  return withRetry(async () => {
    // 优先尝试 JSON 输出
    try {
      const jsonCmd = `npx skills find ${shellEscape(query)} --json`;
      const { stdout } = await execAsync(jsonCmd, { timeout: CONFIG.timeout });
      const parsed = JSON.parse(stdout);
      if (Array.isArray(parsed) && parsed.length > 0) {
        return parsed;
      }
    } catch {
      // --json 不支持或解析失败，降级为文本解析
    }

    // 降级：文本输出 + 正则解析
    const cmd = `npx skills find ${shellEscape(query)}`;
    const { stdout } = await execAsync(cmd, { timeout: CONFIG.timeout });
    return parseFindOutput(stdout);
  });
}

// ==================== ClawHub 搜索 ====================

/**
 * HTTPS GET 请求
 * @param {string} url - 请求地址
 * @param {number} timeout - 超时时间（毫秒）
 * @returns {Promise<Object>} JSON 响应
 */
function httpsGet(url, timeout) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { timeout }, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(new Error(`JSON parse failed: ${e.message}`));
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}`));
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timed out'));
    });
  });
}

/**
 * 搜索 ClawHub 注册表
 * @param {string} query - 搜索关键词
 * @returns {Promise<Array>} 标准化搜索结果
 */
async function clawhubSearch(query) {
  if (typeof query !== 'string' || query.trim().length === 0) {
    return [];
  }

  const url = `${CLAWHUB_CONFIG.apiBase}${CLAWHUB_CONFIG.searchEndpoint}?q=${encodeURIComponent(query)}&limit=${CLAWHUB_CONFIG.maxResults}&nonSuspiciousOnly=true`;

  try {
    const data = await httpsGet(url, CLAWHUB_CONFIG.timeout);

    if (!data.results || !Array.isArray(data.results)) {
      return [];
    }

    return data.results.map((r) => ({
      fullName: r.slug,
      owner: r.slug,
      repo: null,
      skill: r.slug,
      installs: 0,
      displayName: r.displayName || r.slug,
      summary: r.summary || null,
      version: r.version || null,
      url: `${CLAWHUB_CONFIG.apiBase}/skills/${r.slug}`,
      source: 'clawhub',
      score: r.score || 0
    }));
  } catch (error) {
    console.warn(`[clawhubSearch] ${error.message}`);
    return [];
  }
}

/**
 * 安装 ClawHub skill
 * @param {string} slug - skill slug
 * @returns {Promise<Object>} 安装结果
 */
async function clawhubAdd(slug) {
  if (typeof slug !== 'string' || slug.trim().length === 0) {
    throw new Error('slug 参数无效：必须是非空字符串');
  }

  const cmd = `clawhub install ${shellEscape(slug)}`;

  return withRetry(async () => {
    const { stdout, stderr } = await execAsync(cmd, {
      timeout: CONFIG.timeout * 2
    });

    return {
      success: true,
      skillRef: slug,
      output: stdout,
      warnings: stderr || null
    };
  });
}

/**
 * 合并去重搜索结果，skills.sh 优先
 * @param {Array} results - 混合来源的搜索结果
 * @returns {Array} 去重后的结果
 */
function deduplicateResults(results) {
  const seen = new Map();
  for (const result of results) {
    const key = (result.skill || result.fullName).toLowerCase();
    if (!seen.has(key) || (result.source === 'skills.sh' && seen.get(key).source !== 'skills.sh')) {
      seen.set(key, result);
    }
  }
  return Array.from(seen.values());
}

/**
 * 搜索 skills（合并 skills.sh + ClawHub）
 * @param {string} query - 搜索关键词
 * @returns {Promise<Array>} 合并去重后的搜索结果
 */
async function skillsFind(query) {
  if (typeof query !== 'string' || query.trim().length === 0) {
    return [];
  }

  const [cliResult, clawhubResult] = await Promise.allSettled([
    skillsFindCli(query),
    clawhubSearch(query)
  ]);

  const results = [
    ...(cliResult.status === 'fulfilled' ? cliResult.value : []),
    ...(clawhubResult.status === 'fulfilled' ? clawhubResult.value : [])
  ];

  return deduplicateResults(results);
}

/**
 * 去除 ANSI 转义码
 * @param {string} str - 带 ANSI 码的字符串
 * @returns {string} 干净的字符串
 */
function stripAnsi(str) {
  // 匹配 ANSI 转义序列: \x1b[...m
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

/**
 * 从任意文本中提取 JSON 数组（降级解析）
 * @param {string} text - 原始文本
 * @returns {Array|null} 解析后的数组，或 null
 */
function extractJson(text) {
  // 查找 [ ... ] JSON 数组边界
  const openIdx = text.indexOf('[');
  const closeIdx = text.lastIndexOf(']');
  if (openIdx === -1 || closeIdx === -1 || closeIdx <= openIdx) return null;
  try {
    const jsonStr = text.slice(openIdx, closeIdx + 1);
    return JSON.parse(jsonStr);
  } catch {
    return null;
  }
}

/**
 * 解析 npx skills find 的输出
 *
 * 使用多个正则模式提升容错性：
 * - 主模式: owner/repo@skill  N installs
 * - 备用模式: 更宽松，允许额外前缀（emoji等）
 *
 * @param {string} output - ANSI 文本输出
 * @returns {Array} 解析后的结果（空数组 + console.warn 表示解析失败）
 */
function parseFindOutput(output) {
  if (!output || typeof output !== 'string') {
    return [];
  }

  const results = [];
  const lines = output.split('\n').map(stripAnsi);

  // 主模式: 行首 owner（字母数字开头）/repo@skill
  const primaryPattern = /^([a-zA-Z0-9][\w-]*)\/(\S+?)@(\S+?)\s+([\d.]+[KkMm]?)\s+installs/i;
  // 备用模式: 允许行首有额外字符（emoji、序号等），owner 必须以字母数字开头
  const fallbackPattern = /([a-zA-Z0-9][\w-]*?)\/(\S+?)@(\S+?)\s+([\d.]+[KkMm]?)\s+installs/i;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const match = line.match(primaryPattern) || line.match(fallbackPattern);

    if (match) {
      const [_, owner, repo, skill, installsStr] = match;

      // 解析安装数（处理 K/M 后缀，支持小数）
      let installs = parseFloat(installsStr.replace(/[KkMm]/g, ''));
      if (/[Kk]/.test(installsStr)) installs *= 1000;
      if (/[Mm]/.test(installsStr)) installs *= 1000000;

      // 下一行通常是 URL
      const urlLine = lines[i + 1] || '';
      const urlMatch = stripAnsi(urlLine).match(/https:\/\/skills\.sh\/.+/);

      results.push({
        fullName: `${owner}/${repo}@${skill}`,
        owner,
        repo,
        skill,
        installs: Math.floor(installs),
        url: urlMatch ? urlMatch[0].trim().replace(/[^\x00-\x7F]/g, '') : null,
        source: 'skills.sh'
      });
    }
  }

  // 有内容但解析为空 → 可能格式已变化，输出警告
  if (results.length === 0 && output.trim().length > 0) {
    console.warn('[parseFindOutput] 解析结果为空，CLI 输出格式可能已变化');
  }

  return results;
}

/**
 * 安装 skill
 * @param {string} skillRef - skill 引用 (owner/repo@skill)
 * @param {Object} options - 选项
 * @returns {Promise<Object>} 安装结果
 */
async function skillsAdd(skillRef, options = {}) {
  // 参数校验
  if (typeof skillRef !== 'string' || skillRef.trim().length === 0) {
    throw new Error('skillRef 参数无效：必须是非空字符串');
  }

  const { global = false, yes = false } = options;

  let cmd = `npx skills add ${shellEscape(skillRef)}`;
  if (global) cmd += ' -g';
  if (yes) cmd += ' -y';

  return withRetry(async () => {
    const { stdout, stderr } = await execAsync(cmd, {
      timeout: CONFIG.timeout * 2 // 安装可能较慢
    });

    return {
      success: true,
      skillRef,
      output: stdout,
      warnings: stderr || null
    };
  });
}

/**
 * 移除 skill
 * @param {string} skillRef - skill 引用
 * @param {Object} options - 选项
 */
async function skillsRemove(skillRef, options = {}) {
  const { global = true, yes = true } = options;

  let cmd = `npx skills remove ${shellEscape(skillRef)}`;
  if (global) cmd += ' -g';
  if (yes) cmd += ' -y';

  return withRetry(async () => {
    const { stdout } = await execAsync(cmd, { timeout: CONFIG.timeout });
    return { success: true, skillRef, output: stdout };
  });
}

/**
 * 检查更新
 */
async function skillsCheck() {
  const cmd = 'npx skills check';

  return withRetry(async () => {
    const { stdout } = await execAsync(cmd, { timeout: CONFIG.timeout });
    return { output: stdout };
  });
}

/**
 * 更新所有 skills
 */
async function skillsUpdate() {
  const cmd = 'npx skills update';

  return withRetry(async () => {
    const { stdout } = await execAsync(cmd, { timeout: CONFIG.timeout * 2 });
    return { output: stdout };
  });
}

// ==================== 导出 ====================
module.exports = {
  skillsList,
  skillsFind,
  skillsFindCli,
  skillsAdd,
  skillsRemove,
  skillsCheck,
  skillsUpdate,
  clawhubSearch,
  clawhubAdd,
  parseFindOutput,
  extractJson,
  shellEscape,
  withRetry,
  deduplicateResults,
  CONFIG,
  stripAnsi
};
