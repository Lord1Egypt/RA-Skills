#!/usr/bin/env node

import { ClaudeCodeStatsCollector } from './stats-collector';
import { OpenClawStatsCollector } from './openclaw-stats-collector';
import { SkillStats } from './types';

type AgentContext = 'claude-code' | 'openclaw';

// 解析命令行参数
function parseArgs(): AgentContext | null {
  const args = process.argv.slice(2);

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--context' || args[i] === '-c') {
      const context = args[i + 1];
      if (context === 'claude-code' || context === 'openclaw') {
        return context;
      }
    }
  }

  return null;
}

async function main() {
  const context = parseArgs();

  if (!context) {
    console.error('错误: 未配置参数 context');
    console.error('使用方式: npx tsx main.ts --context <claude-code|openclaw>');
    process.exit(1);
  }

  if (context === 'claude-code') {
    await runClaudeCodeStats();
  } else {
    await runOpenClawStats();
  }

  // 输出提示词，引导模型分析
  console.log('\n---\n');
  console.log('请根据以上统计数据进行分析，并按以下要求输出：');
  console.log('1. 【必须】将统计数据整理为 Markdown 表格格式，清晰展示给用户');
  console.log('2. 识别从未使用或长时间未使用的 skill（如超过30天），建议是否删除或禁用');
  console.log('3. 分析成功率较低的 skill（如低于80%），建议排查问题');
  console.log('4. 评估 skill 的使用频率和价值，给出优先级建议');
  console.log('5. 提供其他可能的优化措施');
}

async function runClaudeCodeStats() {
  const collector = new ClaudeCodeStatsCollector();

  console.log(`正在收集 skill 统计数据... [Claude Code]\n`);

  const { collected, updated } = await collector.collectStats();
  console.log(`✓ 收集了 ${collected} 条新记录，更新了 ${updated} 个 skill\n`);

  const allSkills = await collector.getAllSkills();
  const stats = await collector.getStats();

  // 按 scope 分组
  const grouped: Record<string, Record<string, SkillStats>> = {
    builtin: {},
    plugin: {},
    user: {},
    project: {},
    unknown: {},
    deleted: {}
  };

  for (const [name, skill] of Object.entries(allSkills)) {
    const scope = skill.scope || 'unknown';
    const status = skill.status || 'active';

    if (status === 'deleted') {
      grouped.deleted[name] = skill;
    } else if (grouped[scope]) {
      grouped[scope][name] = skill;
    } else {
      grouped.unknown[name] = skill;
    }
  }

  // Scope 中文映射
  const scopeNames: Record<string, string> = {
    builtin: '内置',
    plugin: '插件',
    user: '用户',
    project: '项目',
    unknown: '未知',
    deleted: '已删除'
  };

  // 显示统计结果
  console.log('='.repeat(100));
  console.log('Skill 使用统计');
  console.log('='.repeat(100));
  console.log(`最后更新: ${stats.lastUpdated}`);
  console.log(`最后处理时间: ${stats.lastProcessedTimestamp}\n`);

  for (const [scope, skills] of Object.entries(grouped)) {
    if (Object.keys(skills).length === 0) continue;

    // 跳过已删除的 skill 展示
    if (scope === 'deleted') continue;

    const scopeCN = scopeNames[scope] || scope;
    console.log(`\n【${scope.toUpperCase()} - ${scopeCN}】`);
    console.log('-'.repeat(100));

    const sorted = Object.entries(skills).sort((a, b) => b[1].totalCalls - a[1].totalCalls);

    // 表格头
    console.log(
      '  ' +
      'Skill 名称'.padEnd(35) +
      '调用次数'.padEnd(10) +
      '成功率'.padEnd(10) +
      '最后使用时间'.padEnd(22) +
      '距今'.padEnd(15) +
      '状态'
    );
    console.log('  ' + '-'.repeat(95));

    const now = new Date();

    for (const [name, skill] of sorted) {
      const successRate = skill.totalCalls > 0
        ? ((skill.successCount / skill.totalCalls) * 100).toFixed(1) + '%'
        : '0.0%';

      const status = skill.status === 'never-used' ? '未使用' : '活跃';

      let lastUsed = '从未使用';
      let daysAgo = '-';

      if (skill.lastUsed) {
        const lastUsedDate = new Date(skill.lastUsed);
        lastUsed = lastUsedDate.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        });

        // 计算距今天数
        const diffMs = now.getTime() - lastUsedDate.getTime();
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
          daysAgo = '今天';
        } else if (diffDays === 1) {
          daysAgo = '1 天前';
        } else {
          daysAgo = `${diffDays} 天前`;
        }
      }

      console.log(
        '  ' +
        name.padEnd(35) +
        skill.totalCalls.toString().padEnd(10) +
        successRate.padEnd(10) +
        lastUsed.padEnd(22) +
        daysAgo.padEnd(15) +
        status
      );

      if (skill.projects.length > 0) {
        const projectsStr = skill.projects.slice(0, 2).join(', ');
        const more = skill.projects.length > 2 ? ` (+${skill.projects.length - 2})` : '';
        console.log('  ' + ' '.repeat(35) + `└─ 项目: ${projectsStr}${more}`);
      }
    }
    console.log();
  }

  console.log('='.repeat(100));
}

async function runOpenClawStats() {
  const collector = new OpenClawStatsCollector();

  console.log(`正在收集 skill 统计数据... [OpenClaw]\n`);

  const { collected, updated } = await collector.collectStats();
  console.log(`✓ 收集了 ${collected} 条新记录，更新了 ${updated} 个 skill\n`);

  const allSkills = await collector.getAllSkills();
  const stats = await collector.getStats();

  // 按 scope 分组
  const grouped: Record<string, Record<string, SkillStats>> = {
    'openclaw-workspace': {},
    'openclaw-global': {},
    unknown: {},
    deleted: {}
  };

  for (const [name, skill] of Object.entries(allSkills)) {
    const scope = skill.scope || 'unknown';
    const status = skill.status || 'active';

    if (status === 'deleted') {
      grouped.deleted[name] = skill;
    } else if (grouped[scope]) {
      grouped[scope][name] = skill;
    } else {
      grouped.unknown[name] = skill;
    }
  }

  // Scope 中文映射
  const scopeNames: Record<string, string> = {
    'openclaw-workspace': 'OpenClaw 工作区',
    'openclaw-global': 'OpenClaw 全局',
    unknown: '未知',
    deleted: '已删除'
  };

  // 显示统计结果
  console.log('='.repeat(100));
  console.log('Skill 使用统计');
  console.log('='.repeat(100));
  console.log(`最后更新: ${stats.lastUpdated}`);
  console.log(`最后处理时间: ${stats.lastProcessedTimestamp}\n`);

  for (const [scope, skills] of Object.entries(grouped)) {
    if (Object.keys(skills).length === 0) continue;

    // 跳过已删除的 skill 展示
    if (scope === 'deleted') continue;

    const scopeCN = scopeNames[scope] || scope;
    console.log(`\n【${scope.toUpperCase()} - ${scopeCN}】`);
    console.log('-'.repeat(100));

    const sorted = Object.entries(skills).sort((a, b) => b[1].totalCalls - a[1].totalCalls);

    // 表格头
    console.log(
      '  ' +
      'Skill 名称'.padEnd(35) +
      '调用次数'.padEnd(10) +
      '成功率'.padEnd(10) +
      '最后使用时间'.padEnd(22) +
      '距今'.padEnd(15) +
      '状态'
    );
    console.log('  ' + '-'.repeat(95));

    const now = new Date();

    for (const [name, skill] of sorted) {
      const successRate = skill.totalCalls > 0
        ? ((skill.successCount / skill.totalCalls) * 100).toFixed(1) + '%'
        : '0.0%';

      const status = skill.status === 'never-used' ? '未使用' : '活跃';

      let lastUsed = '从未使用';
      let daysAgo = '-';

      if (skill.lastUsed) {
        const lastUsedDate = new Date(skill.lastUsed);
        lastUsed = lastUsedDate.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        });

        // 计算距今天数
        const diffMs = now.getTime() - lastUsedDate.getTime();
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
          daysAgo = '今天';
        } else if (diffDays === 1) {
          daysAgo = '1 天前';
        } else {
          daysAgo = `${diffDays} 天前`;
        }
      }

      console.log(
        '  ' +
        name.padEnd(35) +
        skill.totalCalls.toString().padEnd(10) +
        successRate.padEnd(10) +
        lastUsed.padEnd(22) +
        daysAgo.padEnd(15) +
        status
      );

      if (skill.projects.length > 0) {
        const projectsStr = skill.projects.slice(0, 2).join(', ');
        const more = skill.projects.length > 2 ? ` (+${skill.projects.length - 2})` : '';
        console.log('  ' + ' '.repeat(35) + `└─ 项目: ${projectsStr}${more}`);
      }
    }
    console.log();
  }

  console.log('='.repeat(100));
}

main().catch(console.error);
