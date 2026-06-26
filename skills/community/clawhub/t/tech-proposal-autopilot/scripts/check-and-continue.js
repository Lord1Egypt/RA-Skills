#!/usr/bin/env node
/**
 * 技术方案书自动续作检查脚本
 * 
 * 功能：
 * 1. 扫描所有未完成项目
 * 2. 检查是否需要续作
 * 3. 触发续作会话
 * 
 * 用法：
 * node check-and-continue.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PROJECTS_DIR = path.join(process.env.HOME, '.openclaw/workspace/projects');
const LOG_FILE = path.join(process.env.HOME, '.openclaw/logs/tech-proposal-monitor.log');

// 日志函数
function log(message) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}\n`;
  console.log(logMessage.trim());
  fs.appendFileSync(LOG_FILE, logMessage);
}

// 扫描所有项目
function scanProjects() {
  const projects = [];
  
  if (!fs.existsSync(PROJECTS_DIR)) {
    log('Projects directory not found');
    return projects;
  }
  
  const dirs = fs.readdirSync(PROJECTS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
  
  for (const dir of dirs) {
    const progressFile = path.join(PROJECTS_DIR, dir, 'progress.json');
    
    if (fs.existsSync(progressFile)) {
      try {
        const progress = JSON.parse(fs.readFileSync(progressFile, 'utf8'));
        
        // 筛选需要续作的项目
        if (progress.status === 'in_progress' && progress.autoContinue !== false) {
          projects.push({
            name: dir,
            path: path.join(PROJECTS_DIR, dir),
            progress
          });
        }
      } catch (e) {
        log(`Error reading progress.json for ${dir}: ${e.message}`);
      }
    }
  }
  
  return projects;
}

// 检查是否需要续作
function needsContinuation(project) {
  const { progress } = project;
  
  // 检查是否有当前章节
  if (!progress.current) {
    // 检查是否所有章节都完成
    if (progress.completed && progress.completed.length === progress.totalChapters) {
      return { need: false, reason: 'all_completed' };
    }
    // 找到第一个未完成的章节
    const nextChapter = findNextChapter(project);
    if (nextChapter) {
      return { need: true, reason: 'no_current', nextChapter };
    }
    return { need: false, reason: 'unknown_state' };
  }
  
  // 检查当前章节是否超时
  const lastUpdate = new Date(progress.lastUpdate || progress.startTime);
  const now = new Date();
  const minutesSinceUpdate = (now - lastUpdate) / 1000 / 60;
  
  // 超过30分钟未更新视为超时
  if (minutesSinceUpdate > 30) {
    return { need: true, reason: 'timeout', minutesSinceUpdate };
  }
  
  // 检查当前章节文件是否存在
  const chapterFile = path.join(project.path, `${progress.current}.md`);
  if (!fs.existsSync(chapterFile)) {
    return { need: true, reason: 'file_missing' };
  }
  
  return { need: false, reason: 'in_progress' };
}

// 找到下一个未完成的章节
function findNextChapter(project) {
  const { progress } = project;
  const total = progress.totalChapters;
  const completed = progress.completed || [];
  
  for (let i = 1; i <= total; i++) {
    const chapterId = `chapter-${String(i).padStart(2, '0')}`;
    if (!completed.includes(chapterId)) {
      return chapterId;
    }
  }
  
  return null;
}

// 生成续作指令
function generateContinueDirective(project, nextChapter) {
  const { progress } = project;
  
  // 确定负责智能体
  const agent = progress.agents?.[nextChapter] || 'milo';
  
  // 获取章节信息
  const chapterInfo = progress.chapters?.[nextChapter] || {};
  const targetWords = progress.wordCounts?.[nextChapter] || 15000;
  const title = chapterInfo.title || `${nextChapter} (待生成)`;
  
  const continueMd = `# 续作指令

## 项目信息
- **项目路径**: ${project.path}
- **项目名称**: ${progress.project}
- **当前状态**: in_progress

## 续作任务
- **当前章节**: ${nextChapter}
- **章节标题**: ${title}
- **负责智能体**: ${agent}
- **目标字数**: ${targetWords}

## 执行指令
1. 读取 progress.json 获取当前进度
2. 读取 outline.md 获取章节大纲
3. 读取 reference-keypoints.md (如果存在)
4. 生成当前章节内容
5. 保存为 ${nextChapter}.md
6. 更新 progress.json
7. 继续下一章节或结束

## 注意事项
- 每章独立会话，上下文从零开始
- 仅加载必要文件（outline.md, progress.json, reference-keypoints.md）
- 完成后更新进度文件
- 遵循段落优先写作规范

## 生成时间
${new Date().toISOString()}
`;
  
  const continuePath = path.join(project.path, 'CONTINUE.md');
  fs.writeFileSync(continuePath, continueMd);
  
  return { agent, nextChapter };
}

// 触发续作会话
async function triggerContinuation(project, agent, nextChapter, dryRun = false) {
  log(`Triggering continuation for ${project.name}: ${nextChapter} by ${agent}`);
  
  if (dryRun) {
    log('[DRY RUN] Would spawn continuation session');
    return;
  }
  
  // 更新 progress.json
  const progressPath = path.join(project.path, 'progress.json');
  const progress = JSON.parse(fs.readFileSync(progressPath, 'utf8'));
  progress.current = nextChapter;
  progress.lastUpdate = new Date().toISOString();
  fs.writeFileSync(progressPath, JSON.stringify(progress, null, 2));
  
  // 这里应该调用 OpenClaw 的 sessions_spawn
  // 但在脚本中我们只能设置标志，让心跳或其他机制来触发
  const triggerFile = path.join(project.path, '.trigger-continue');
  fs.writeFileSync(triggerFile, JSON.stringify({
    project: project.name,
    chapter: nextChapter,
    agent,
    timestamp: new Date().toISOString()
  }));
  
  log(`Created trigger file: ${triggerFile}`);
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  
  log('=== Tech Proposal Auto-Continue Check ===');
  log(`Mode: ${dryRun ? 'DRY RUN' : 'LIVE'}`);
  
  // 扫描项目
  const projects = scanProjects();
  log(`Found ${projects.length} in-progress projects`);
  
  // 检查每个项目
  for (const project of projects) {
    log(`\nChecking project: ${project.name}`);
    
    const check = needsContinuation(project);
    log(`Needs continuation: ${check.need} (${check.reason})`);
    
    if (check.need) {
      const nextChapter = check.nextChapter || project.progress.current;
      
      if (nextChapter) {
        const { agent } = generateContinueDirective(project, nextChapter);
        await triggerContinuation(project, agent, nextChapter, dryRun);
      }
    }
  }
  
  log('\n=== Check Complete ===');
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
