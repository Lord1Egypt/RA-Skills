/**
 * zhihu-bridge.js — Python 子进程桥接模块
 *
 * 在 Node.js 环境中调用 Python 版 zhihu_bot.py。
 * 支持：
 * - 子进程调用 + 超时控制
 * - 完整错误处理（I15）
 * - Plan B browser fallback（I20-PB）
 * - JSON 解析保护
 *
 * I13 | I15 | I20-PB
 *
 * @module zhihu-bridge
 */

import { execFile } from 'child_process';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { checkCookieExpiry } from './zhihu-core.js';
import { bridgeLog } from './zhihu-logger.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
/** @type {string} Python 脚本路径 */
const PYTHON_SCRIPT = resolve(__dirname, 'python', 'zhihu_bot.py');

// ──────────────────────────────────────────
// Python 环境预检
// ──────────────────────────────────────────

/** @type {string} Python 执行路径 */
let pythonPath = 'python3';
/** @type {boolean} Python 是否已检测 */
let pythonChecked = false;

/**
 * 检查 Python 环境是否可用
 * @returns {Promise<boolean>} 是否可用
 */
async function checkPython() {
  if (pythonChecked) return true;

  try {
    await new Promise((resolve, reject) => {
      execFile(pythonPath, ['--version'], { timeout: 5000 }, (err, stdout) => {
        if (err) reject(err);
        else resolve(stdout);
      });
    });
    pythonChecked = true;
    return true;
  } catch {
    try {
      await new Promise((resolve, reject) => {
        execFile('python', ['--version'], { timeout: 5000 }, (err, stdout) => {
          if (err) reject(err);
          else resolve(stdout);
        });
      });
      pythonPath = 'python';
      pythonChecked = true;
      return true;
    } catch {
      bridgeLog.error('Python3 不可用。请安装: brew install python3');
      return false;
    }
  }
}

/**
 * 前置检查：z_c0 Cookie 是否有效
 * @returns {boolean}
 */
function checkZhiHuCookie() {
  const { valid } = checkCookieExpiry();
  if (!valid) {
    bridgeLog.warn('⚠️ z_c0 Cookie 缺失或已过期，请重新登录并导出 Cookie');
    return false;
  }
  return true;
}

// ──────────────────────────────────────────
// 核心：调用 Python 脚本
// ──────────────────────────────────────────

/**
 * 调用 Python zhihu_bot.py 并解析 JSON 结果
 *
 * @param {string} scriptName - 脚本名称
 * @param {string[]} args - 命令行参数
 * @param {number} [timeout=30000] - 超时毫秒
 * @returns {Promise<object>} 解析后的 JSON 结果
 * @throws {Error} Python 不可用或执行失败
 */
async function callPythonScript(scriptName, args, timeout = 30000) {
  const pyAvail = await checkPython();
  if (!pyAvail) {
    throw new Error('Python3 不可用。请安装: brew install python3');
  }

  const hasCookie = checkZhiHuCookie();
  if (!hasCookie) {
    throw new Error('z_c0 Cookie 缺失或已过期，请先导出 Cookie（node scripts/zhihu-export-cookie.js）');
  }

  const fullArgs = [PYTHON_SCRIPT, '--json', ...args];

  let result;
  try {
    result = await new Promise((resolve, reject) => {
      execFile(pythonPath, fullArgs, { timeout, maxBuffer: 1024 * 1024 }, (err, stdout, stderr) => {
        if (err) {
          const enhancedErr = new Error(err.message);
          enhancedErr.code = err.code;
          enhancedErr.killed = err.killed;
          enhancedErr.stderr = stderr;
          reject(enhancedErr);
          return;
        }
        resolve({ stdout, stderr });
      });
    });
  } catch (e) {
    if (e.code === 'ERR_CHILD_PROCESS_STDIO_MAXBUFFER') {
      throw new Error(`Python 脚本输出过大 (>1MB): ${scriptName}`);
    }
    if (e.killed) {
      throw new Error(`Python 脚本执行超时 (${timeout}ms): ${scriptName}`);
    }
    const stderr = e.stderr || '';
    const traceback = stderr.split('\n').slice(-8).join('\n').trim();
    if (traceback) {
      throw new Error(`Python 脚本异常:\n${traceback}`);
    }
    throw new Error(`Python 脚本执行失败: ${e.message}`);
  }

  const stdout = result.stdout.trim();
  if (!stdout) {
    throw new Error(`Python 脚本无输出: ${scriptName}`);
  }

  try {
    return JSON.parse(stdout);
  } catch (e) {
    const preview = stdout.slice(0, 200);
    throw new Error(`Python 脚本输出不是合法 JSON (前 200 字符):\n${preview}`);
  }
}

// ──────────────────────────────────────────
// 高层 API
// ──────────────────────────────────────────

/**
 * 获取圈子详情
 * @param {string} ringId - 圈子 ID
 * @param {number} [pageNum=1] - 页码
 * @param {number} [pageSize=20] - 每页条数
 * @returns {Promise<object>}
 */
async function getRingDetail(ringId, pageNum = 1, pageSize = 20) {
  return callPythonScript('zhihu_bot.py', [
    'ring', 'detail', ringId,
    '--page-num', String(pageNum),
    '--page-size', String(pageSize),
  ]);
}

/**
 * 发布想法
 * @param {string} ringId - 圈子 ID
 * @param {string} title - 标题
 * @param {string} content - 内容
 * @param {string} [images] - 图片路径
 * @returns {Promise<object>}
 */
async function publishPin(ringId, title, content, images) {
  const args = [
    'pin', 'publish',
    '--ring-id', ringId,
    '--title', title,
    '--content', content,
  ];
  if (images) args.push('--images', images);
  return callPythonScript('zhihu_bot.py', args);
}

/**
 * 点赞/取消点赞
 * @param {string} contentType - 内容类型
 * @param {string} contentToken - 内容标识
 * @param {string} action - 操作 (like/unlike)
 * @returns {Promise<object>}
 */
async function react(contentType, contentToken, action) {
  return callPythonScript('zhihu_bot.py', [
    'reaction', contentType, contentToken, action,
  ]);
}

/**
 * 创建评论
 * @param {string} contentType - 内容类型
 * @param {string} contentToken - 内容标识
 * @param {string} content - 评论内容
 * @returns {Promise<object>}
 */
async function createComment(contentType, contentToken, content) {
  return callPythonScript('zhihu_bot.py', [
    'comment', 'create', contentType, contentToken, content,
  ]);
}

/**
 * 删除评论
 * @param {string} commentId - 评论 ID
 * @returns {Promise<object>}
 */
async function deleteComment(commentId) {
  return callPythonScript('zhihu_bot.py', [
    'comment', 'delete', commentId,
  ]);
}

/**
 * 获取评论列表
 * @param {string} contentType - 内容类型
 * @param {string} contentToken - 内容标识
 * @param {number} [pageNum=1] - 页码
 * @param {number} [pageSize=10] - 每页条数
 * @returns {Promise<object>}
 */
async function listComments(contentType, contentToken, pageNum = 1, pageSize = 10) {
  return callPythonScript('zhihu_bot.py', [
    'comment', 'list', contentType, contentToken,
    '--page-num', String(pageNum),
    '--page-size', String(pageSize),
  ]);
}

/**
 * 当 Python 环境不可用时的 fallback
 * @param {string} operation - 操作名
 * @param {string} detail - 详情
 * @returns {{ status: string, module: string, operation: string, detail: string, message: string }}
 */
function createFallbackError(operation, detail) {
  return {
    status: 'fallback_needed',
    module: 'zhihu-bridge',
    operation,
    detail,
    message: `Python 环境不可用，${operation} 操作需要浏览器通道`,
  };
}

// ──────────────────────────────────────────
// 导出
// ──────────────────────────────────────────

export {
  callPythonScript,
  checkPython,
  getRingDetail,
  publishPin,
  react,
  createComment,
  deleteComment,
  listComments,
  createFallbackError,
};
