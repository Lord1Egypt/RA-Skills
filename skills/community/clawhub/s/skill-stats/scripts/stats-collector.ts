import fs from 'fs/promises';
import path from 'path';
import { GlobalStats, SkillCallRecord, SkillStats } from './types';

// Claude Code 相关路径
const PROJECTS_DIR = path.join(process.env.HOME || '', '.claude', 'projects');
const STATS_DIR = path.join(process.env.HOME || '', '.claude', 'skill-stats');
const GLOBAL_STATS_PATH = path.join(STATS_DIR, 'global-stats.json');
const USER_SKILLS_DIR = path.join(process.env.HOME || '', '.claude', 'skills');
const USER_SETTINGS_PATH = path.join(process.env.HOME || '', '.claude', 'settings.json');

// 内置 skills 列表
const BUILTIN_SKILLS = new Set(['keybindings-help']);

// 递归查找所有 .jsonl 文件
async function findJsonlFiles(dir: string): Promise<string[]> {
  const results: string[] = [];
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory() && entry.name !== 'node_modules') {
        results.push(...await findJsonlFiles(fullPath));
      } else if (entry.isFile() && entry.name.endsWith('.jsonl')) {
        results.push(fullPath);
      }
    }
  } catch {
    // 忽略错误
  }
  return results;
}

// Claude Code Skill 调用解析器（支持 Skill 工具 + Bash 命令）
class ClaudeCodeSkillParser {
  parse(entry: any, sessionId: string, cwd: string): SkillCallRecord | null {
    try {
      if (entry.type === 'assistant' && entry.message?.content) {
        const content = entry.message.content;

        for (const item of content) {
          // 解析 Skill 工具调用
          if (item.type === 'tool_use' && item.name === 'Skill') {
            const skillName = item.input?.skill;
            if (skillName) {
              return {
                skillName,
                timestamp: entry.timestamp || new Date().toISOString(),
                projectPath: cwd || '/unknown',
                sessionId: sessionId,
                success: true
              };
            }
          }

          // 解析 Read 工具中的 skill 文件读取
          if (item.type === 'tool_use' && item.name === 'Read') {
            const filePath = item.input?.file_path;
            if (filePath) {
              const skillName = this.extractSkillFromCommand(filePath);
              if (skillName) {
                return {
                  skillName,
                  timestamp: entry.timestamp || new Date().toISOString(),
                  projectPath: cwd || '/unknown',
                  sessionId: sessionId,
                  success: true
                };
              }
            }
          }

          // 解析 Bash 工具中的 skill 执行
          if (item.type === 'tool_use' && item.name === 'Bash') {
            const command = item.input?.command;
            if (command) {
              // 跳过不相关的命令（避免误识别）
              const excludePatterns = [
                'git add',
                'git commit',
                'ls ', 'mkdir ', 'rm ', 'mv ', 'cp ',
                'grep ', 'find ', 'head ', 'tail ', 'sed ', 'awk ',
                'echo ', 'printf ',
                'chmod ', 'chown ',
                'touch ', 'ln ',
                'diff ', 'wc ', 'sort ', 'uniq '
              ];

              if (excludePatterns.some(pattern =>command.includes(pattern))) {
                continue;
              }

              const skillName = this.extractSkillFromCommand(command);
              if (skillName) {
                return {
                  skillName,
                  timestamp: entry.timestamp || new Date().toISOString(),
                  projectPath: cwd || '/unknown',
                  sessionId: sessionId,
                  success: true
                };
              }
            }
          }
        }
      }
    } catch {
      // 忽略解析错误
    }

    return null;
  }

  private extractSkillFromCommand(command: string): string | null {
    // 匹配路径中的 /.claude/skills/{skillName}
    const pattern = /\/\.claude\/skills\/([^\/\s]+)/;
    const match = command.match(pattern);
    return match ? match[1] : null;
  }
}

// Claude Code 专用统计收集器
export class ClaudeCodeStatsCollector {
  private userSkills: Set<string> = new Set();
  private projectSkillsMap: Map<string, Set<string>> = new Map();
  private enabledPlugins: Set<string> = new Set();
  private parser: ClaudeCodeSkillParser;

  constructor() {
    this.parser = new ClaudeCodeSkillParser();
  }

  private async ensureStatsDir(): Promise<void> {
    await fs.mkdir(STATS_DIR, { recursive: true });
  }

  private async loadEnabledPlugins(): Promise<void> {
    try {
      const settings = JSON.parse(await fs.readFile(USER_SETTINGS_PATH, 'utf-8'));
      if (settings.enabledPlugins) {
        for (const [key, enabled] of Object.entries(settings.enabledPlugins)) {
          if (enabled) {
            this.enabledPlugins.add(key);
          }
        }
      }
    } catch {
      // 忽略错误
    }
  }

  private async loadUserSkills(): Promise<void> {
    try {
      const skillDirs = await fs.readdir(USER_SKILLS_DIR);
      for (const dir of skillDirs) {
        if (!dir.startsWith('.')) {
          this.userSkills.add(dir);
        }
      }
    } catch {
      // 忽略错误
    }
  }

  private async loadProjectSkills(): Promise<void> {
    try {
      const projectDirs = await fs.readdir(PROJECTS_DIR);
      for (const projectName of projectDirs) {
        if (projectName.startsWith('.')) continue;
        const projectDir = path.join(PROJECTS_DIR, projectName);
        const projectSkillsDir = path.join(projectDir, '.claude', 'skills');
        try {
          const skillDirs = await fs.readdir(projectSkillsDir);
          const skills = new Set<string>();
          for (const dir of skillDirs) {
            if (!dir.startsWith('.')) {
              skills.add(dir);
            }
          }
          if (skills.size > 0) {
            const projectPath = projectName.replace(/-/g, '/');
            this.projectSkillsMap.set(projectPath, skills);
          }
        } catch {
          // 该项目没有 skills 目录
        }
      }
    } catch {
      // 忽略错误
    }
  }

  private getSkillScope(skillName: string, projectPath: string): 'managed' | 'user' | 'project' | 'plugin' | 'builtin' | 'unknown' {
    if (BUILTIN_SKILLS.has(skillName)) {
      return 'builtin';
    }

    const baseName = skillName.includes(':') ? skillName.split(':')[0] : skillName;

    for (const plugin of this.enabledPlugins) {
      if (plugin.includes('@') && skillName.includes(':')) {
        const [pluginName] = plugin.split('@');
        if (baseName === pluginName) {
          return 'plugin';
        }
      }
    }

    for (const [proj, skills] of this.projectSkillsMap.entries()) {
      if (skills.has(baseName)) {
        return 'project';
      }
    }

    if (this.userSkills.has(baseName)) {
      return 'user';
    }

    return 'unknown';
  }

  private async loadGlobalStats(): Promise<GlobalStats> {
    try {
      const data = await fs.readFile(GLOBAL_STATS_PATH, 'utf-8');
      return JSON.parse(data);
    } catch {
      return {
        skills: {},
        lastUpdated: new Date().toISOString(),
        lastProcessedTimestamp: new Date(0).toISOString()
      };
    }
  }

  private async saveGlobalStats(stats: GlobalStats): Promise<void> {
    await this.ensureStatsDir();
    await fs.writeFile(GLOBAL_STATS_PATH, JSON.stringify(stats, null, 2));
  }

  private parseSkillCall(entry: any, sessionId: string, cwd: string): SkillCallRecord | null {
    return this.parser.parse(entry, sessionId, cwd);
  }

  async collectStats(): Promise<{ collected: number; updated: number }> {
    const stats = await this.loadGlobalStats();
    await this.loadEnabledPlugins();
    await this.loadUserSkills();
    await this.loadProjectSkills();
    let collected = 0;
    let updated = 0;
    // 使用上次处理的时间戳作为基准
    const latestTimestamp = stats.lastProcessedTimestamp;

    try {
      const jsonlFiles = await findJsonlFiles(PROJECTS_DIR);

      for (const filePath of jsonlFiles) {
        try {
          const fileStat = await fs.stat(filePath);
          const fileModifiedTime = fileStat.mtime.toISOString();

          if (fileModifiedTime <= stats.lastProcessedTimestamp) {
            continue;
          }

          const content = await fs.readFile(filePath, 'utf-8');
          const lines = content.split('\n').filter(l => l.trim());

          let sessionId = 'unknown';
          let cwd = '/unknown';

          for (const line of lines) {
            try {
              const entry = JSON.parse(line);

              if (entry.sessionId) {
                sessionId = entry.sessionId;
              }
              if (entry.cwd) {
                cwd = entry.cwd;
              }

              const record = this.parseSkillCall(entry, sessionId, cwd);
              if (record) {
                // 只统计时间戳大于上次处理时间的记录
                if (record.timestamp > latestTimestamp) {
                  collected++;

                  if (!stats.skills[record.skillName]) {
                    stats.skills[record.skillName] = {
                      totalCalls: 0,
                      successCount: 0,
                      failureCount: 0,
                      lastUsed: record.timestamp,
                      projects: [],
                      avgExecutionTime: 0,
                      scope: this.getSkillScope(record.skillName, record.projectPath)
                    };
                    updated++;
                  }

                  const skillStats = stats.skills[record.skillName];
                  skillStats.totalCalls++;

                  if (!skillStats.scope) {
                    skillStats.scope = this.getSkillScope(record.skillName, record.projectPath);
                  }
                  if (record.success) {
                    skillStats.successCount++;
                  } else {
                    skillStats.failureCount++;
                  }

                  if (record.timestamp > skillStats.lastUsed) {
                    skillStats.lastUsed = record.timestamp;
                  }

                  if (!skillStats.projects.includes(record.projectPath)) {
                    skillStats.projects.push(record.projectPath);
                  }
                }
              }
            } catch {
              // 忽略单行解析错误
            }
          }
        } catch {
          // 忽略文件读取错误
        }
      }

      stats.lastUpdated = new Date().toISOString();
      // 将 lastProcessedTimestamp 设置为当前时间戳，下次统计时会统计本次之后的所有记录
      stats.lastProcessedTimestamp = new Date().toISOString();
      await this.saveGlobalStats(stats);

    } catch (error: any) {
      if (error.code !== 'ENOENT') {
        throw error;
      }
    }

    return { collected, updated };
  }

  async getStats(): Promise<GlobalStats> {
    return this.loadGlobalStats();
  }

  async getAllSkills(): Promise<Record<string, SkillStats>> {
    await this.loadEnabledPlugins();
    await this.loadUserSkills();
    await this.loadProjectSkills();

    const stats = await this.loadGlobalStats();
    const allSkills: Record<string, SkillStats> = {};

    for (const skillName of BUILTIN_SKILLS) {
      const existingStats = stats.skills[skillName];
      allSkills[skillName] = {
        totalCalls: existingStats?.totalCalls || 0,
        successCount: existingStats?.successCount || 0,
        failureCount: existingStats?.failureCount || 0,
        lastUsed: existingStats?.lastUsed || '',
        projects: existingStats?.projects || [],
        avgExecutionTime: existingStats?.avgExecutionTime || 0,
        scope: 'builtin',
        status: existingStats?.totalCalls > 0 ? 'active' : 'never-used'
      };
    }

    for (const plugin of this.enabledPlugins) {
      if (plugin.includes('@')) {
        const [pluginName, scope] = plugin.split('@');
        const skillName = `${pluginName}:${scope}`;
        const existingStats = stats.skills[skillName];
        allSkills[skillName] = {
          totalCalls: existingStats?.totalCalls || 0,
          successCount: existingStats?.successCount || 0,
          failureCount: existingStats?.failureCount || 0,
          lastUsed: existingStats?.lastUsed || '',
          projects: existingStats?.projects || [],
          avgExecutionTime: existingStats?.avgExecutionTime || 0,
          scope: 'plugin',
          status: existingStats?.totalCalls > 0 ? 'active' : 'never-used'
        };
      }
    }

    for (const skillName of this.userSkills) {
      const existingStats = stats.skills[skillName];
      allSkills[skillName] = {
        totalCalls: existingStats?.totalCalls || 0,
        successCount: existingStats?.successCount || 0,
        failureCount: existingStats?.failureCount || 0,
        lastUsed: existingStats?.lastUsed || '',
        projects: existingStats?.projects || [],
        avgExecutionTime: existingStats?.avgExecutionTime || 0,
        scope: 'user',
        status: existingStats?.totalCalls > 0 ? 'active' : 'never-used'
      };
    }

    for (const [projectPath, skills] of this.projectSkillsMap.entries()) {
      for (const skillName of skills) {
        const existingStats = stats.skills[skillName];
        allSkills[skillName] = {
          totalCalls: existingStats?.totalCalls || 0,
          successCount: existingStats?.successCount || 0,
          failureCount: existingStats?.failureCount || 0,
          lastUsed: existingStats?.lastUsed || '',
          projects: existingStats?.projects || [],
          avgExecutionTime: existingStats?.avgExecutionTime || 0,
          scope: 'project',
          status: existingStats?.totalCalls > 0 ? 'active' : 'never-used'
        };
      }
    }

    for (const [skillName, skillStats] of Object.entries(stats.skills)) {
      if (!allSkills[skillName]) {
        allSkills[skillName] = {
          ...skillStats,
          status: 'deleted'
        };
      }
    }

    return allSkills;
  }
}
