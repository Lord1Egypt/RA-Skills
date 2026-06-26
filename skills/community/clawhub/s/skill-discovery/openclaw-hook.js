#!/usr/bin/env node
/**
 * OpenClaw Hook - 与 OpenClaw 集成
 *
 * Phase 3: 增强（C）- OpenClaw 集成
 */

const { autoDiscover, buildLogEntry, sanitize } = require('./auto-discover');
const { skillsList, skillsRemove } = require('./skills-cli');
const { MAGIC, HOOK_CONFIG } = require('./constants');
const fs = require('fs').promises;
const path = require('path');

const CONFIG = HOOK_CONFIG;

// ==================== 日志系统 ====================

/**
 * 记录日志（使用统一 Schema + 脱敏）
 */
async function logDiscovery(action, data) {
  try {
    let logs = [];
    try {
      const content = await fs.readFile(CONFIG.logPath, 'utf8');
      logs = JSON.parse(content);
    } catch {
      // 文件不存在或解析失败
    }

    // 使用统一 Schema 格式 + 脱敏敏感信息
    const logEntry = buildLogEntry(action, sanitize(data));
    logs.push(logEntry);

    // 限制数量
    if (logs.length > CONFIG.maxLogEntries) {
      logs = logs.slice(-CONFIG.maxLogEntries);
    }

    await fs.mkdir(path.dirname(CONFIG.logPath), { recursive: true });
    await fs.writeFile(CONFIG.logPath, JSON.stringify(logs, null, 2));
  } catch (e) {
    console.error('日志记录失败:', e.message);
  }
}

// ==================== 卸载机制 ====================

/**
 * 安全卸载 skill
 */
async function safeRemove(skillRef) {
  try {
    // 1. 获取已安装列表
    const installed = await skillsList({ global: true });
    const target = installed.find(
      (s) => s.name === skillRef || s.name === skillRef.replace(/[@/]/g, '-')
    );

    if (!target) {
      return { success: false, reason: 'not_found' };
    }

    // 2. 备份到 trash
    await fs.mkdir(CONFIG.trashPath, { recursive: true });
    const backupName = `${target.name}_${Date.now()}`;
    const backupPath = path.join(CONFIG.trashPath, backupName);

    await fs.cp(target.path, backupPath, { recursive: true });

    // 3. 执行卸载
    await skillsRemove(skillRef, { global: true, yes: true });

    // 4. 记录日志
    await logDiscovery('remove', {
      skillRef,
      backupPath,
      success: true
    });

    return {
      success: true,
      message: `✅ 已卸载 ${skillRef}，备份在 ${backupPath}`
    };
  } catch (error) {
    await logDiscovery('remove', {
      skillRef,
      error: error.message,
      success: false
    });

    return {
      success: false,
      reason: 'remove_failed',
      error: error.message
    };
  }
}

// ==================== cleanTrash 缓存（避免频繁扫描）====================
let _lastCleanTime = 0;
let _lastCleanResult = null;

const TRASH_CLEAN_INTERVAL_MS = MAGIC.TRASH_CLEAN_INTERVAL_MS;
const SEVEN_DAYS_MS = MAGIC.TRASH_CLEAN_DAYS * 24 * 60 * 60 * 1000;

/**
 * 清理过期备份（带缓存，1 小时内不重复扫描）
 */
async function cleanTrash(options = {}) {
  const { force = false } = options;

  // 缓存检查：1 小时内不重复执行
  if (!force && Date.now() - _lastCleanTime < TRASH_CLEAN_INTERVAL_MS) {
    return { ..._lastCleanResult, cached: true };
  }

  try {
    const entries = await fs.readdir(CONFIG.trashPath);
    let cleaned = 0;

    for (const entry of entries) {
      const entryPath = path.join(CONFIG.trashPath, entry);
      const stat = await fs.stat(entryPath);

      if (Date.now() - stat.mtime.getTime() > SEVEN_DAYS_MS) {
        await fs.rm(entryPath, { recursive: true });
        cleaned++;
      }
    }

    _lastCleanTime = Date.now();
    _lastCleanResult = { cleaned };
    return { ..._lastCleanResult, cached: false };
  } catch {
    _lastCleanTime = Date.now();
    _lastCleanResult = { cleaned: 0 };
    return { ..._lastCleanResult, cached: false };
  }
}

// ==================== OpenClaw Hook ====================

/**
 * OpenClaw 输入处理钩子
 *
 * 在 OpenClaw 处理用户输入前调用
 *
 * 返回语义：
 * - handled: true  -> Skill Discovery 已接管，直接使用 result.response
 * - handled: false -> Skill Discovery 未处理，result.note 为提示信息
 *
 * result.alreadyInstalled 独立于 handled 存在，表示 skill 已安装（无需再次安装）
 */
async function onUserInput(userInput, _context = {}) {
  console.log(`[Skill Discovery] 处理输入: "${userInput.substring(0, 50)}..."`);

  // 1. 自动发现（默认推荐模式，不自动安装）
  const result = await autoDiscover(userInput, { dryRun: true });

  // 2. 记录日志
  await logDiscovery(result.installed ? 'install' : 'discover', {
    input: userInput,
    ...result
  });

  // 3. 返回处理建议（推荐模式：不自动安装，返回建议供用户确认）
  if (result.success && result.dryRun) {
    // 推荐模式 -> 未接管，返回推荐信息供用户确认
    const isClawhub = result.skill.source === 'clawhub';
    const installCmd = isClawhub
      ? `clawhub install ${result.skill.fullName}`
      : `npx skills add ${result.skill.fullName} -g`;
    return {
      handled: false,
      note: `💡 发现匹配 skill: ${result.skill.fullName}\n安装命令: ${installCmd}`,
      skill: result.skill,
      installCmd,
      alreadyInstalled: false
    };
  }

  if (result.success && result.installed) {
    // 显式安装成功 -> 已接管
    return {
      handled: true,
      response: `✅ 已安装 ${result.skill.fullName}\n\n现在可以使用相关功能了。`,
      skill: result.skill,
      alreadyInstalled: false
    };
  }

  if (result.success && result.alreadyInstalled) {
    // 已安装（无需处理）-> 未接管，但携带 note 便于 OpenClaw 补充说明
    return {
      handled: false,
      note: `✅ ${result.skill.fullName} 已安装，可直接使用`,
      skill: result.skill,
      alreadyInstalled: true
    };
  }

  if (!result.success && result.fallback) {
    // 安装失败 -> 未接管，携带 note 提示用户
    return {
      handled: false,
      note: `发现 skill 但安装失败，${result.fallback}`,
      skill: result.skill,
      alreadyInstalled: false
    };
  }

  if (!result.success && result.candidates) {
    // 有候选但未通过质量验证 -> 未接管
    return {
      handled: false,
      note: `⚠️ 未找到符合质量标准的 skill（可手动从 ${result.candidates.length} 个候选中挑选）`,
      candidates: result.candidates,
      alreadyInstalled: false
    };
  }

  // 未触发或搜索失败 -> 完全未处理
  return {
    handled: false,
    alreadyInstalled: false
  };
}

/**
 * 生成用户提示
 */
function generatePrompt(result) {
  if (result.success && result.installed) {
    return (
      `✅ 已自动安装 ${result.skill.fullName}\n` +
      `📊 安装量: ${result.skill.installs.toLocaleString()}\n` +
      `🔗 ${result.skill.url || 'https://skills.sh'}`
    );
  }

  if (result.success && result.alreadyInstalled) {
    return `✅ ${result.skill.fullName} 已安装，直接使用即可`;
  }

  if (!result.success && result.candidates) {
    let prompt = '⚠️ 未找到符合质量标准的 skill\n\n候选（需人工判断）:\n';
    result.candidates.slice(0, 3).forEach((c, i) => {
      prompt += `${i + 1}. ${c.fullName} (${c.installs} installs)\n`;
    });
    return prompt;
  }

  if (!result.success && result.fallback) {
    return `❌ 自动安装失败\n💡 ${result.fallback}`;
  }

  return null;
}

// ==================== 导出 ====================
module.exports = {
  onUserInput,
  generatePrompt,
  safeRemove,
  cleanTrash,
  logDiscovery,
  CONFIG
};
