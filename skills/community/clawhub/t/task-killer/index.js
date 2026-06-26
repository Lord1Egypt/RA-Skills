/**
 * Task Killer Skill - 快速中断正在执行的任务
 * 
 * 使用场景：
 * 1. 任务方向错误，立即中断
 * 2. 用户需求变更，停止当前任务
 * 3. 节省 token，提前止损
 */

import { subagents } from './tools/subagents.js';
import { process } from './tools/process.js';
import { write } from './tools/filesystem.js';

/**
 * 中断技能主函数
 */
export async function killTask(options = {}) {
  const {
    confirm = true,      // 是否需要用户确认
    cleanupSubagents = true,
    cleanupProcesses = true,
    cleanupTempFiles = true,
    tempDir = './.temp'
  } = options;

  const result = {
    interrupted: false,
    killedSubagents: 0,
    killedProcesses: 0,
    cleanedFiles: 0,
    message: ''
  };

  // 1. 检查并终止子代理
  if (cleanupSubagents) {
    try {
      const subagentsList = await subagents({ action: 'list' });
      if (subagentsList.active && subagentsList.active.length > 0) {
        for (const agent of subagentsList.active) {
          await subagents({ 
            action: 'kill', 
            target: agent.id 
          });
          result.killedSubagents++;
        }
      }
    } catch (error) {
      console.warn('清理子代理失败:', error.message);
    }
  }

  // 2. 检查并终止后台进程
  if (cleanupProcesses) {
    try {
      const processList = await process({ action: 'list' });
      if (processList.sessions && processList.sessions.length > 0) {
        for (const session of processList.sessions) {
          await process({ 
            action: 'kill', 
            sessionId: session.id 
          });
          result.killedProcesses++;
        }
      }
    } catch (error) {
      console.warn('清理后台进程失败:', error.message);
    }
  }

  // 3. 清理临时文件（可选）
  if (cleanupTempFiles) {
    try {
      // 创建中断标记文件
      await write({
        path: `${tempDir}/interrupted-${Date.now()}.md`,
        content: `# 任务中断记录\n\n时间：${new Date().toISOString()}\n原因：用户主动中断\n`
      });
      result.cleanedFiles = 1;
    } catch (error) {
      console.warn('清理临时文件失败:', error.message);
    }
  }

  result.interrupted = true;
  result.message = buildResultMessage(result);

  return result;
}

/**
 * 构建结果消息
 */
function buildResultMessage(result) {
  const lines = ['🛑 已中断当前任务'];

  if (result.killedSubagents > 0) {
    lines.push(`- 终止子代理：${result.killedSubagents}个`);
  }

  if (result.killedProcesses > 0) {
    lines.push(`- 终止后台进程：${result.killedProcesses}个`);
  }

  if (result.cleanedFiles > 0) {
    lines.push(`- 清理临时文件：${result.cleanedFiles}个`);
  }

  if (result.killedSubagents === 0 && 
      result.killedProcesses === 0 && 
      result.cleanedFiles === 0) {
    lines.push('- 无需清理的资源');
  }

  lines.push('');
  lines.push('准备好执行新任务了 👍');

  return lines.join('\n');
}

/**
 * 快速中断（无需确认）
 */
export async function quickKill() {
  console.log('⚡ 快速中断...');
  const result = await killTask({
    confirm: false,
    cleanupTempFiles: false
  });
  console.log(result.message);
  return result;
}

/**
 * 完整清理（包含临时文件）
 */
export async function fullClean() {
  console.log('🧹 完整清理...');
  const result = await killTask({
    confirm: false,
    cleanupTempFiles: true
  });
  console.log(result.message);
  return result;
}

// 如果直接运行此文件
const isMainModule = process.argv[1]?.includes('task-killer');
if (isMainModule) {
  quickKill().then(() => {
    process.exit(0);
  }).catch(error => {
    console.error('中断失败:', error);
    process.exit(1);
  });
}
