#!/usr/bin/env node

/**
 * Daily Report Generator
 * 自动生成日报/周报
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 获取 git 日志
function getGitLogs(since, until, repos = ['.']) {
  const commits = [];
  
  for (const repo of repos) {
    try {
      const cmd = `cd "${repo}" && git log --since="${since}" --until="${until}" --pretty=format:"%h|%s|%an|%ad" --date=short 2>/dev/null || echo ""`;
      const output = execSync(cmd, { encoding: 'utf-8' }).trim();
      
      if (output) {
        output.split('\n').forEach(line => {
          const [hash, message, author, date] = line.split('|');
          if (hash && message) {
            commits.push({ hash, message, author, date, repo });
          }
        });
      }
    } catch (e) {
      // 忽略错误
    }
  }
  
  return commits;
}

// 按日期分组提交
function groupByDate(commits) {
  const groups = {};
  commits.forEach(c => {
    if (!groups[c.date]) groups[c.date] = [];
    groups[c.date].push(c);
  });
  return groups;
}

// 生成报告
function generateReport(commits, options = {}) {
  const { language = 'zh-CN', includeStats = true } = options;
  const grouped = groupByDate(commits);
  const dates = Object.keys(grouped).sort().reverse();
  
  if (language === 'zh-CN') {
    let report = `# 工作日报\n\n`;
    report += `> 生成时间: ${new Date().toLocaleString('zh-CN')}\n\n`;
    
    for (const date of dates) {
      const dayCommits = grouped[date];
      report += `## ${date}\n\n`;
      
      // 按仓库分组
      const byRepo = {};
      dayCommits.forEach(c => {
        const repoName = path.basename(c.repo);
        if (!byRepo[repoName]) byRepo[repoName] = [];
        byRepo[repoName].push(c);
      });
      
      for (const [repo, repoCommits] of Object.entries(byRepo)) {
        report += `### ${repo}\n`;
        repoCommits.forEach(c => {
          report += `- \`${c.hash}\` ${c.message}\n`;
        });
        report += '\n';
      }
    }
    
    if (includeStats && commits.length > 0) {
      report += `---\n\n`;
      report += `**统计**\n`;
      report += `- 总提交数: ${commits.length}\n`;
      report += `- 涉及仓库: ${Object.keys(groupByDate(commits)).length}\n`;
    }
    
    return report;
  } else {
    let report = `# Work Report\n\n`;
    report += `> Generated: ${new Date().toLocaleString('en-US')}\n\n`;
    
    for (const date of dates) {
      const dayCommits = grouped[date];
      report += `## ${date}\n\n`;
      
      const byRepo = {};
      dayCommits.forEach(c => {
        const repoName = path.basename(c.repo);
        if (!byRepo[repoName]) byRepo[repoName] = [];
        byRepo[repoName].push(c);
      });
      
      for (const [repo, repoCommits] of Object.entries(byRepo)) {
        report += `### ${repo}\n`;
        repoCommits.forEach(c => {
          report += `- \`${c.hash}\` ${c.message}\n`;
        });
        report += '\n';
      }
    }
    
    if (includeStats && commits.length > 0) {
      report += `---\n\n`;
      report += `**Stats**\n`;
      report += `- Total commits: ${commits.length}\n`;
      report += `- Repositories: ${Object.keys(groupByDate(commits)).length}\n`;
    }
    
    return report;
  }
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'today';
  
  let since, until;
  const today = new Date();
  
  switch (command) {
    case 'today':
      since = today.toISOString().split('T')[0];
      until = new Date(today.getTime() + 86400000).toISOString().split('T')[0];
      break;
    case 'week':
      const weekStart = new Date(today);
      weekStart.setDate(today.getDate() - today.getDay() + 1);
      since = weekStart.toISOString().split('T')[0];
      until = new Date(today.getTime() + 86400000).toISOString().split('T')[0];
      break;
    case 'range':
      const fromIdx = args.indexOf('--from');
      const toIdx = args.indexOf('--to');
      since = fromIdx !== -1 ? args[fromIdx + 1] : today.toISOString().split('T')[0];
      until = toIdx !== -1 ? args[toIdx + 1] : new Date(today.getTime() + 86400000).toISOString().split('T')[0];
      break;
    default:
      console.error('Unknown command. Use: today, week, or range');
      process.exit(1);
  }
  
  // 读取配置
  let config = { git: { repos: ['.'] }, output: { language: 'zh-CN' } };
  const configPath = path.join(process.cwd(), '.reportrc.json');
  if (fs.existsSync(configPath)) {
    try {
      config = { ...config, ...JSON.parse(fs.readFileSync(configPath, 'utf-8')) };
    } catch (e) {}
  }
  
  // 获取提交并生成报告
  const commits = getGitLogs(since, until, config.git.repos);
  const report = generateReport(commits, config.output);
  
  console.log(report);
  
  // 保存到文件
  const outputPath = `report-${since}.md`;
  fs.writeFileSync(outputPath, report);
  console.log(`\n📄 Report saved to: ${outputPath}`);
}

main();
