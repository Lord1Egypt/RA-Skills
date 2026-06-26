#!/usr/bin/env node
/**
 * 技术方案书自动续作触发器
 * 
 * 功能：当上下文接近上限时，创建续作触发文件，让 Cron/心跳自动接管
 * 
 * 使用方式：
 * 1. 智能体在生成章节时，定期检查上下文使用率
 * 2. 当上下文 > 70% 时，调用此脚本
 * 3. 脚本创建 .trigger-continue 文件，Cron 会自动接管
 */

const fs = require('fs');
const path = require('path');

// 获取项目路径
const projectPath = process.argv[2];
if (!projectPath) {
  console.error('用法: node trigger-continue.js <project-path>');
  process.exit(1);
}

// 读取进度文件
const progressFile = path.join(projectPath, 'progress.json');
if (!fs.existsSync(progressFile)) {
  console.error('找不到 progress.json');
  process.exit(1);
}

const progress = JSON.parse(fs.readFileSync(progressFile, 'utf8'));

// 检查是否需要续作
if (progress.status === 'completed') {
  console.log('项目已完成，无需续作');
  process.exit(0);
}

if (progress.status !== 'in_progress') {
  console.log(`项目状态: ${progress.status}，跳过`);
  process.exit(0);
}

// 创建触发文件
const triggerFile = path.join(projectPath, '.trigger-continue');
const triggerData = {
  triggeredAt: new Date().toISOString(),
  currentChapter: progress.current,
  completedChapters: progress.completed.length,
  totalChapters: progress.totalChapters,
  agent: progress.agents[progress.current] || 'milo',
  reason: 'context_limit'
};

fs.writeFileSync(triggerFile, JSON.stringify(triggerData, null, 2));
console.log(`✅ 已创建续作触发文件: ${triggerFile}`);
console.log(`   当前章节: ${progress.current}`);
console.log(`   进度: ${progress.completed.length}/${progress.totalChapters}`);

// 生成/更新 CONTINUE.md
const continueFile = path.join(projectPath, 'CONTINUE.md');
const continueContent = `# 续作指令

## 项目信息
- **项目路径**: ${projectPath}
- **项目名称**: ${progress.project}
- **当前状态**: in_progress
- **触发时间**: ${triggerData.triggeredAt}

## 续作任务
- **当前章节**: ${progress.current || '下一未完成章节'}
- **负责智能体**: ${triggerData.agent}
- **已完成**: ${progress.completed.length}/${progress.totalChapters} 章

## 执行指令
1. 读取 progress.json 获取当前进度
2. 读取 outline.md 获取章节大纲
3. 读取 reference-keypoints.md (如果存在)
4. 生成当前章节内容
5. 保存为 chapter-N.md
6. 更新 progress.json
7. 删除 .trigger-continue 文件
8. 继续下一章节或结束

## 注意事项
- 每章独立会话，上下文从零开始
- 仅加载必要文件
- 完成后更新进度文件
- 遵循段落优先写作规范

## 生成时间
${new Date().toISOString()}
`;

fs.writeFileSync(continueFile, continueContent);
console.log(`✅ 已更新续作指令文件: ${continueFile}`);
