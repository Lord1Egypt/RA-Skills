/**
 * 技能追踪器 - Node.js 版本 (v1.2.0 生产环境版)
 * 
 * 作者：aiyst
 * 邮箱：aiyst@qq.com
 * GitHub: https://github.com/aiyst1982
 * 
 * 特性：
 * - 非阻塞异步执行
 * - 异常隔离
 * - 重试机制
 * - 耗时统计
 * - 文件锁（并发安全）
 * - 原子写入
 * - 配置项
 * - 统一日志
 */

const fs = require('fs');
const path = require('path');
const { writeFile, readFile, mkdir } = fs.promises;

// ============ 配置 ============
const Config = {
  DATA_DIR: path.join(__dirname, 'data'),
  STATS_FILE: path.join(__dirname, 'data', 'skill-stats.json'),
  USAGE_LOG: path.join(__dirname, 'data', 'usage-log.jsonl'),
  LOCK_FILE: path.join(__dirname, 'data', '.stats.lock'),
  
  // 可配置项
  MAX_RETRIES: 3,
  RETRY_DELAY: 100,  // 毫秒
  LOG_LEVEL: 'info',  // debug, info, warn, error
  ENABLE_LOGGING: true
};

// ============ 日志工具 ============
const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

const currentLogLevel = LogLevel[Config.LOG_LEVEL.toUpperCase()] || LogLevel.INFO;

function log(level, message, ...args) {
  if (!Config.ENABLE_LOGGING) return;
  if (LogLevel[level.toUpperCase()] < currentLogLevel) return;
  
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const prefix = `[${timestamp}] [${level.toUpperCase()}] SkillTracker:`;
  console.log(`${prefix} ${message}`, ...args);
}

// ============ 文件锁 ============
const fileLocks = new Map();

async function withFileLock(filePath, callback) {
  const lockKey = filePath;
  
  // 简单实现的互斥锁
  while (fileLocks.has(lockKey)) {
    await new Promise(resolve => setTimeout(resolve, 10));
  }
  
  try {
    fileLocks.set(lockKey, true);
    return await callback();
  } finally {
    fileLocks.delete(lockKey);
  }
}

// ============ 原子写入 ============
async function atomicWrite(filePath, content) {
  const tempFile = filePath + '.tmp';
  try {
    await writeFile(tempFile, content, 'utf8');
    // fs.promises.rename 是原子操作
    await fs.promises.rename(tempFile, filePath);
  } catch (err) {
    log('error', `原子写入失败：${err.message}`);
    // 清理临时文件
    try {
      await fs.promises.unlink(tempFile);
    } catch (e) {
      // 忽略清理错误
    }
    throw err;
  }
}

// ============ 带锁读写 ============
async function readWithLock(filePath) {
  return await withFileLock(filePath, async () => {
    try {
      const content = await readFile(filePath, 'utf8');
      return JSON.parse(content);
    } catch (err) {
      if (err.code === 'ENOENT') {
        return {};
      }
      throw err;
    }
  });
}

async function writeWithLock(filePath, data) {
  return await withFileLock(filePath, async () => {
    const content = JSON.stringify(data, null, 2);
    await atomicWrite(filePath, content);
  });
}

// ============ 初始化 ============
async function initStatsFile() {
  try {
    // 确保数据目录存在
    await mkdir(Config.DATA_DIR, { recursive: true });
    
    // 初始化统计文件
    try {
      await readFile(Config.STATS_FILE, 'utf8');
    } catch (err) {
      if (err.code === 'ENOENT') {
        const initialData = {
          totalCalls: 0,
          skills: {},
          lastUpdated: new Date().toISOString()
        };
        await writeWithLock(Config.STATS_FILE, initialData);
        log('info', '统计文件已初始化');
      }
    }
  } catch (err) {
    log('error', `初始化失败：${err.message}`);
  }
}

// 初始化
initStatsFile();

// ============ 核心功能 ============
const tracker = {
  name: 'skill-tracker',
  version: '1.2.0',
  triggers: ['技能统计', '调用统计', 'skill 排行', '使用报告'],
  
  /**
   * 记录技能调用（非阻塞，异常隔离）
   * @param {string} skillName - 技能名称
   * @param {string} action - 操作类型（调用/成功/失败）
   * @param {object} context - 上下文信息
   * @returns {null} 不阻塞，立即返回
   */
  track(skillName, action = 'call', context = {}) {
    // 异步非阻塞执行，不影响主流程
    (async () => {
      try {
        const startTime = context.startTime || Date.now();
        const duration = context.duration || (Date.now() - startTime);
        const timestamp = new Date().toISOString();
        const date = timestamp.split('T')[0]; // YYYY-MM-DD
        
        // 写入日志（追加模式）
        const logEntry = {
          timestamp,
          date,
          skill: skillName,
          action,
          duration_ms: duration,
          context: {
            user: context.user || '韩先生',
            channel: context.channel || 'feishu',
            session_id: context.session_id || null,
            success: context.success !== false,
            error: context.error || null
          }
        };
        
        // 追加日志（行级原子操作）
        const logLine = JSON.stringify(logEntry) + '\n';
        await fs.promises.appendFile(Config.USAGE_LOG, logLine, 'utf8');
        
        // 更新统计（不等待，后台执行）
        updateStats(skillName, action, context.success !== false, duration)
          .catch(err => log('error', `更新统计失败：${err.message}`));
        
      } catch (err) {
        // 异常隔离：追踪失败不影响主流程
        log('error', `记录失败：${err.message}`);
      }
    })();
    
    // 立即返回，不阻塞主流程
    return null;
  },
  
  /**
   * 获取统计报告
   */
  async getReport() {
    try {
      const stats = await readWithLock(Config.STATS_FILE);
      
      // 计算排行
      const rankings = Object.entries(stats.skills || {})
        .map(([name, data]) => ({
          name,
          calls: data.calls || 0,
          success: data.success || 0,
          fail: data.fail || 0,
          successRate: data.calls ? ((data.success || 0) / data.calls * 100).toFixed(1) : 0,
          avgDuration: data.avgDuration || 0
        }))
        .sort((a, b) => b.calls - a.calls);
      
      return {
        totalCalls: stats.totalCalls || 0,
        totalSkills: Object.keys(stats.skills || {}).length,
        rankings,
        lastUpdated: stats.lastUpdated || ''
      };
    } catch (err) {
      log('error', `获取报告失败：${err.message}`);
      return { error: err.message };
    }
  },
  
  /**
   * 处理用户查询
   */
  async handle(context) {
    const { message } = context;
    
    try {
      if (message.includes('技能统计') || message.includes('调用统计') || 
          message.includes('skill 排行') || message.includes('使用报告')) {
        
        const report = await this.getReport();
        
        if (report.error) {
          return { success: false, message: `统计失败：${report.error}` };
        }
        
        // 生成报告
        const lines = [
          `📊 **技能使用统计报告**`,
          ``,
          `**总调用次数：** ${report.totalCalls}`,
          `**技能总数：** ${report.totalSkills}`,
          `**最后更新：** ${new Date(report.lastUpdated).toLocaleString('zh-CN')}`,
          ``,
          `**技能排行榜（按调用次数）：**`,
          ``
        ];
        
        report.rankings.forEach((skill, index) => {
          const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '📦';
          lines.push(`${medal} **${index + 1}. ${skill.name}**`);
          lines.push(`   调用：${skill.calls} | 成功：${skill.success} | 失败：${skill.fail} | 成功率：${skill.successRate}% | 平均耗时：${skill.avgDuration}ms`);
        });
        
        return {
          success: true,
          message: lines.join('\n')
        };
      }
      
      return { success: false, message: '未识别的指令' };
    } catch (err) {
      log('error', `处理查询失败：${err.message}`);
      return { success: false, message: `操作失败：${err.message}` };
    }
  }
};

/**
 * 更新统计数据（带重试机制）
 */
async function updateStats(skillName, action, isSuccess, duration = 0) {
  const maxRetries = Config.MAX_RETRIES;
  let lastError = null;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const stats = await readWithLock(Config.STATS_FILE);
      
      // 更新总调用
      if (action === 'call') {
        stats.totalCalls = (stats.totalCalls || 0) + 1;
      }
      
      // 更新技能统计
      if (!stats.skills[skillName]) {
        stats.skills[skillName] = {
          calls: 0,
          success: 0,
          fail: 0,
          totalDuration: 0,
          firstUsed: new Date().toISOString(),
          lastUsed: new Date().toISOString()
        };
      }
      
      const skill = stats.skills[skillName];
      
      if (action === 'call') {
        skill.calls = (skill.calls || 0) + 1;
      } else if (action === 'success') {
        skill.success = (skill.success || 0) + 1;
      } else if (action === 'fail') {
        skill.fail = (skill.fail || 0) + 1;
      }
      
      // 累加执行耗时
      skill.totalDuration = (skill.totalDuration || 0) + duration;
      skill.avgDuration = skill.calls > 0 ? Math.round(skill.totalDuration / skill.calls) : 0;
      
      skill.lastUsed = new Date().toISOString();
      stats.lastUpdated = skill.lastUsed;
      
      // 保存统计（带锁和原子写入）
      await writeWithLock(Config.STATS_FILE, stats);
      
      log('debug', `更新统计成功：${skillName} (${action})`);
      
      return stats;
      
    } catch (err) {
      lastError = err;
      log('warn', `更新统计失败 (尝试 ${attempt}/${maxRetries}): ${err.message}`);
      
      // 重试前等待
      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, Config.RETRY_DELAY * attempt));
      }
    }
  }
  
  // 所有重试失败
  log('error', `更新统计最终失败：${lastError.message}`);
  return null;
}

/**
 * 配置追踪器
 */
function configure(options = {}) {
  if (options.dataDir) {
    Config.DATA_DIR = options.dataDir;
    Config.STATS_FILE = path.join(Config.DATA_DIR, 'skill-stats.json');
    Config.USAGE_LOG = path.join(Config.DATA_DIR, 'usage-log.jsonl');
    Config.LOCK_FILE = path.join(Config.DATA_DIR, '.stats.lock');
  }
  
  if (options.maxRetries !== undefined) {
    Config.MAX_RETRIES = options.maxRetries;
  }
  
  if (options.retryDelay !== undefined) {
    Config.RETRY_DELAY = options.retryDelay;
  }
  
  if (options.logLevel) {
    Config.LOG_LEVEL = options.logLevel;
  }
  
  if (options.enableLogging !== undefined) {
    Config.ENABLE_LOGGING = options.enableLogging;
  }
  
  log('info', `配置已更新：${JSON.stringify(Config)}`);
}

// 导出
module.exports = tracker;
module.exports.configure = configure;
module.exports.Config = Config;
