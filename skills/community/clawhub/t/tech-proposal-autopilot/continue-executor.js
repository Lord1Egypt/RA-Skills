#!/usr/bin/env node
/**
 * 技术方案书自动续作执行器
 * 
 * 功能：扫描未完成项目，自动续作
 * 
 * 触发方式：
 * 1. Cron 定时任务（每5分钟）
 * 2. 心跳检查（用户交互时）
 * 
 * 使用方式：
 * node continue-executor.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');

const PROJECTS_DIR = path.expandHomeDir('~/\.openclaw/workspace/projects');
const LOG_FILE = path.expandHomeDir('~/.openclaw/logs/tech-proposal-monitor.log');
const DRY_RUN = process.argv.includes('--dry-run');

// 简单的 home 目录展开
function expandHomeDir(p) {
  if (p.startsWith('~/')) {
    return path.join(process.env.HOME, p.slice(2));
  }
  return p;
}

// 日志函数
function log(message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;
  console.log(message);
  
  // 确保日志目录存在
  const logDir = path.dirname(LOG_FILE);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  fs.appendFileSync(LOG_FILE, logLine);
}

// 检查单个项目
function checkProject(projectDir) {
  const progressFile = path.join(projectDir, 'progress.json');
  const triggerFile = path.join(projectDir, '.trigger-continue');
  const projectName = path.basename(projectDir);
  
  if (!fs.existsSync(progressFile)) {
    return null;
  }
  
  const progress = JSON.parse(fs.readFileSync(progressFile, 'utf8'));
  
  // 检查是否需要续作
  const needContinue = 
    progress.status === 'in_progress' && 
    progress.autoContinue !== false;
  
  if (!needContinue) {
    return null;
  }
  
  // 检查是否有触发文件
  const hasTrigger = fs.existsSync(triggerFile);
  
  // 检查是否超时（30分钟无更新）
  const lastUpdate = new Date(progress.lastUpdate);
  const now = new Date();
  const minutesSinceUpdate = (now - lastUpdate) / 1000 / 60;
  const isTimeout = minutesSinceUpdate > 30;
  
  return {
    project: projectName,
    path: projectDir,
    progress,
    hasTrigger,
    isTimeout,
    minutesSinceUpdate: Math.round(minutesSinceUpdate),
    needAction: hasTrigger || isTimeout
  };
}

// 生成续作命令
function generateContinueCommand(projectInfo) {
  const { progress, path: projectPath } = projectInfo;
  const nextChapter = progress.current || findNextChapter(progress);
  const agent = progress.agents[nextChapter] || 'milo';
  
  return {
    agent,
    nextChapter,
    command: `继续执行技术方案书项目: ${projectInfo.project}
    
当前状态:
- 已完成: ${progress.completed.length}/${progress.totalChapters} 章
- 下一章节: ${nextChapter}
- 负责智能体: ${agent}

执行步骤:
1. cd ${projectPath}
2. 读取 progress.json
3. 读取 outline.md
4. 生成 ${nextChapter}.md
5. 更新 progress.json
6. 删除 .trigger-continue (如果存在)

技能文档: skills/tech-proposal-autopilot/SKILL.md`
  };
}

// 找到下一个未完成的章节
function findNextChapter(progress) {
  const allChapters = Array.from({ length: progress.totalChapters }, (_, i) => 
    `chapter-${String(i + 1).padStart(2, '0')}`
  );
  
  for (const chapter of allChapters) {
    if (!progress.completed.includes(chapter)) {
      return chapter;
    }
  }
  return null;
}

// 主函数
function main() {
  log('=== 技术方案书自动续作检查 ===');
  
  if (!fs.existsSync(PROJECTS_DIR)) {
    log('项目目录不存在');
    return;
  }
  
  const projects = fs.readdirSync(PROJECTS_DIR, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => path.join(PROJECTS_DIR, dirent.name));
  
  const needActionProjects = [];
  
  for (const projectDir of projects) {
    const info = checkProject(projectDir);
    if (info && info.needAction) {
      needActionProjects.push(info);
      log(`发现待续作项目: ${info.project}`);
      log(`  - 状态: ${info.progress.status}`);
      log(`  - 进度: ${info.progress.completed.length}/${info.progress.totalChapters}`);
      log(`  - 触发文件: ${info.hasTrigger ? '存在' : '不存在'}`);
      log(`  - 超时: ${info.isTimeout ? `是 (${info.minutesSinceUpdate}分钟)` : '否'}`);
    }
  }
  
  if (needActionProjects.length === 0) {
    log('无需续作的项目');
    return;
  }
  
  // 生成续作指令
  for (const projectInfo of needActionProjects) {
    const cmd = generateContinueCommand(projectInfo);
    log(`\n续作指令 (${projectInfo.project}):`);
    log(`智能体: ${cmd.agent}`);
    log(`下一章节: ${cmd.nextChapter}`);
    
    if (DRY_RUN) {
      log('[DRY RUN] 不会实际执行');
    } else {
      // 输出续作指令，由调用者执行
      console.log('\n--- CONTINUE_COMMAND_START ---');
      console.log(JSON.stringify(cmd));
      console.log('--- CONTINUE_COMMAND_END ---\n');
    }
  }
  
  log(`检查完成，发现 ${needActionProjects.length} 个待续作项目`);
}

main();
