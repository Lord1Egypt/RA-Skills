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
 */

import { execFile } from 'child_process';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PYTHON_SCRIPT = resolve(__dirname, 'python', 'zhihu_bot.py');

// ──────────────────────────────────────────
// Python 环境预检
// ──────────────────────────────────────────

let pythonPath = 'python3';
let pythonChecked = false;

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
    // 尝试 python
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
      console.error(`[zhihu-bridge] Python3 不可用。请安装: brew install python3`);
      return false;
    }
  }
}

// ──────────────────────────────────────────
// 前置检查：z_c0 Cookie
// ──────────────────────────────────────────

import { checkCookieExpiry } from './zhihu-core.js';

function checkZhiHuCookie() {
  const { valid } = checkCookieExpiry();
  if (!valid) {
    console.warn('[zhihu-bridge] ⚠️ z_c0 Cookie 缺失或已过期，请重新登录并导出 Cookie');
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
 */
async function callPythonScript(scriptName, args, timeout = 30000) {
  // 前置检查 1: Python3 是否可用
  const pyAvail = await checkPython();
  if (!pyAvail) {
    throw new Error('Python3 不可用。请安装: brew install python3');
  }

  // 前置检查 2: Cookie 是否有效
  const hasCookie = checkZhiHuCookie();
  if (!hasCookie) {
    throw new Error('z_c0 Cookie 缺失或已过期，请先导出 Cookie（node scripts/zhihu-export-cookie.js）');
  }

  // 构建参数：添加 --json 模式 + 自定义参数
  const fullArgs = [PYTHON_SCRIPT, '--json', ...args];

  // 执行子进程
  let result;
  try {
    result = await new Promise((resolve, reject) => {
      execFile(pythonPath, fullArgs, { timeout, maxBuffer: 1024 * 1024 }, (err, stdout, stderr) => {
        if (err) {
          // 非零退出码
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
    // 错误分类
    if (e.code === 'ERR_CHILD_PROCESS_STDIO_MAXBUFFER') {
      throw new Error(`Python 脚本输出过大 (>1MB): ${scriptName}`);
    }
    if (e.killed) {
      throw new Error(`Python 脚本执行超时 (${timeout}ms): ${scriptName}`);
    }
    // 非零退出码：解析 stderr 中的 traceback
    const stderr = e.stderr || '';
    const traceback = stderr.split('\n').slice(-8).join('\n').trim();
    if (traceback) {
      throw new Error(`Python 脚本异常:\n${traceback}`);
    }
    throw new Error(`Python 脚本执行失败: ${e.message}`);
  }

  // 解析 JSON 输出
  const stdout = result.stdout.trim();
  if (!stdout) {
    throw new Error(`Python 脚本无输出: ${scriptName}`);
  }

  try {
    return JSON.parse(stdout);
  } catch (e) {
    // 输出前 200 字符串用于调试
    const preview = stdout.slice(0, 200);
    throw new Error(`Python 脚本输出不是合法 JSON (前 200 字符):\n${preview}`);
  }
}

// ──────────────────────────────────────────
// 高层 API
// ──────────────────────────────────────────

/**
 * 获取圈子详情
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
 */
async function publishPin(ringId, title, content, images) {
  const args = [
    'pin', 'publish',
    '--ring-id', ringId,
    '--title', title,
    '--content', content,
  ];
  if (images) {
    args.push('--images', images);
  }
  return callPythonScript('zhihu_bot.py', args);
}

/**
 * 点赞/取消点赞
 */
async function react(contentType, contentToken, action) {
  return callPythonScript('zhihu_bot.py', [
    'reaction', contentType, contentToken, action,
  ]);
}

/**
 * 创建评论
 */
async function createComment(contentType, contentToken, content) {
  return callPythonScript('zhihu_bot.py', [
    'comment', 'create', contentType, contentToken, content,
  ]);
}

/**
 * 删除评论
 */
async function deleteComment(commentId) {
  return callPythonScript('zhihu_bot.py', [
    'comment', 'delete', commentId,
  ]);
}

/**
 * 获取评论列表
 */
async function listComments(contentType, contentToken, pageNum = 1, pageSize = 10) {
  return callPythonScript('zhihu_bot.py', [
    'comment', 'list', contentType, contentToken,
    '--page-num', String(pageNum),
    '--page-size', String(pageSize),
  ]);
}

// ──────────────────────────────────────────
// Plan B fallback 模式
// ──────────────────────────────────────────

/**
 * 当 Python 环境不可用时的 fallback
 * 返回标准错误结构，由上层决定是否降级到浏览器通道
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
