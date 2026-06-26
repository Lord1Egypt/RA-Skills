#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Usage: node update-task-stats.js <path-to-TASKS.md>');
    process.exit(1);
  }

  let content;
  try {
    content = fs.readFileSync(filePath, 'utf8');
  } catch (err) {
    console.error(`Error reading file: ${err.message}`);
    process.exit(1);
  }

  const lines = content.split('\n');
  
  // Count statistics
  let totalTasks = 0;
  let running = 0;
  let completed = 0;
  let persistent = 0;
  let oneTime = 0;

  // Find all tasks (lines starting with "## [")
  for (const line of lines) {
    if (line.startsWith('## [')) {
      totalTasks++;
    } else if (line.includes('- **任务类型:**')) {
      if (line.includes('持续性任务')) {
        persistent++;
      } else if (line.includes('一次性任务')) {
        oneTime++;
      }
    } else if (line.includes('- **当前状态:**')) {
      if (line.includes('执行中')) {
        running++;
      } else if (line.includes('已完成')) {
        completed++;
      }
    }
  }

  // Generate new stats section
  const newStats = [
    '## 任务统计',
    '',
    `- 总任务数: ${totalTasks}`,
    `- 执行中: ${running}`,
    `- 已完成: ${completed}`,
    `- 持续性任务: ${persistent}`,
    `- 一次性任务: ${oneTime}`,
    '',
    '---'
  ].join('\n');

  // Replace old stats section
  const statsStart = content.indexOf('## 任务统计');
  const statsEnd = content.indexOf('---', statsStart) + 3;
  
  if (statsStart === -1 || statsEnd === -1) {
    console.error('Could not find stats section in file');
    process.exit(1);
  }

  const newContent = content.substring(0, statsStart) + newStats + content.substring(statsEnd);
  
  try {
    fs.writeFileSync(filePath, newContent, 'utf8');
    console.log('Task statistics updated successfully');
    console.log(`Total: ${totalTasks}, Running: ${running}, Completed: ${completed}`);
    console.log(`Persistent: ${persistent}, One-time: ${oneTime}`);
  } catch (err) {
    console.error(`Error writing file: ${err.message}`);
    process.exit(1);
  }
}

main();
