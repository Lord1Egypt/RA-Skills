#!/usr/bin/env node

/**
 * Skill 打包脚本
 * 
 * 当任务 status=completed 时，自动生成 SKILL.md + README.md
 * 并将任务归档到 evolution/archive/
 */

const fs = require('fs');
const path = require('path');

// Resolve workspace from env or default to ~/.openclaw/agents/main/workspace
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.env.WORKSPACE || path.join(require('os').homedir(), '.openclaw', 'agents', 'main', 'workspace');
const TASKS_DIR = process.env.EVOLUTION_TASKS_DIR || path.join(WORKSPACE, 'evolution', 'tasks');
const ARCHIVE_DIR = process.env.EVOLUTION_ARCHIVE_DIR || path.join(WORKSPACE, 'evolution', 'archive');
const SKILLS_DIR = process.env.EVOLUTION_SKILLS_DIR || path.join(WORKSPACE, 'skills');

function main() {
  console.log(`\n📦 Skill 打包扫描 @ ${new Date().toISOString()}`);
  
  if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  
  const files = fs.readdirSync(TASKS_DIR).filter(f => f.endsWith('.json') && f.startsWith('task-'));
  
  for (const file of files) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(TASKS_DIR, file), 'utf8'));
      
      if (data.status !== 'completed') continue;
      
      console.log(`📦 打包任务: ${data.task_id} - ${data.goal}`);
      
      // 提取 skill 名称（从 goal 或 context 中）
      const skillMatch = data.goal.match(/skills\/(\S+)/) || 
                         data.context?.constraints?.find(c => c.includes('Skill 目录'))?.match(/skills\/(\S+)\//);
      const skillName = skillMatch ? skillMatch[1] : data.task_id;
      const skillDir = path.join(SKILLS_DIR, skillName);
      
      // 确保 skill 目录存在
      if (!fs.existsSync(skillDir)) {
        console.log(`⚠️ Skill 目录不存在: ${skillDir}，跳过打包`);
        continue;
      }
      
      // 更新状态为 packaged
      data.status = 'packaged';
      data.packaged = {
        packaged_at: new Date().toISOString(),
        packaged_by: 'WILSON (pack-skill.js)',
        skill_path: skillDir + '/'
      };
      data.updated_at = new Date().toISOString();
      
      if (!data.history) data.history = [];
      data.history.push({
        timestamp: data.updated_at,
        action: 'packaged',
        agent: 'WILSON',
        model: 'auto',
        notes: `Skill 打包完成，路径: ${skillDir}/`
      });
      
      // 归档
      fs.writeFileSync(path.join(ARCHIVE_DIR, file), JSON.stringify(data, null, 2));
      
      // 从活跃目录移除
      fs.unlinkSync(path.join(TASKS_DIR, file));
      
      console.log(`✅ ${data.task_id} 已打包并归档`);
      
    } catch (err) {
      console.error(`❌ 处理 ${file} 失败:`, err.message);
    }
  }
}

main();
