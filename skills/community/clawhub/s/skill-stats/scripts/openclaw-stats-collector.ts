import * as fs from 'fs';
import * as path from 'path';
import { SkillCallRecord, SkillStats, GlobalStats } from './types';

const OPENCLAW_ROOT = path.join(process.env.HOME || '', '.openclaw');
const SESSIONS_DIR = path.join(OPENCLAW_ROOT, 'agents', 'main', 'sessions');
const STATS_DIR = path.join(process.env.HOME || '', '.openclaw', 'skill-stats');
const GLOBAL_STATS_PATH = path.join(STATS_DIR, 'openclaw-global-stats.json');
const WORKSPACE_SKILLS_DIR = path.join(OPENCLAW_ROOT, 'workspace', 'skills');
const GLOBAL_SKILLS_DIR = path.join(OPENCLAW_ROOT, 'skills');

class OpenClawSkillParser {
  parse(entry: any, sessionId: string, cwd: string): SkillCallRecord | null {
    try {
      if (entry.type === 'message' && entry.message?.content) {
        const content = entry.message.content;

        for (const item of content) {
          // 解析 toolCall，name 为 "read"
          if (item.type === 'toolCall' && item.name === 'read') {
            const path = item.arguments?.path;
            if (path) {
              const skillName = this.extractSkillName(path);
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

          // 解析 toolCall，name 为 "exec"
          if (item.type === 'toolCall' && item.name === 'exec') {
            const command = item.arguments?.command;
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

              if (excludePatterns.some(pattern => command.includes(pattern))) {
                continue;
              }

              const skillName = this.extractSkillName(command);
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

  private extractSkillName(pathOrCommand: string): string | null {
    // 匹配路径中的 /.openclaw/skills/{skillName} 或 /.openclaw/workspace/skills/{skillName}
    const pattern = /\/\.?openclaw\/(?:workspace\/)?skills\/([^\/\s]+)/;
    const match = pathOrCommand.match(pattern);
    return match ? match[1] : null;
  }
}

export class OpenClawStatsCollector {
  private parser = new OpenClawSkillParser();
  private workspaceSkills = new Set<string>();
  private globalSkills = new Set<string>();

  constructor() {
    this.loadWorkspaceSkills();
    this.loadGlobalSkills();
  }

  private loadWorkspaceSkills() {
    if (!fs.existsSync(WORKSPACE_SKILLS_DIR)) return;

    try {
      const entries = fs.readdirSync(WORKSPACE_SKILLS_DIR, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isDirectory()) {
          const skillPath = path.join(WORKSPACE_SKILLS_DIR, entry.name, 'SKILL.md');
          if (fs.existsSync(skillPath)) {
            this.workspaceSkills.add(entry.name);
          }
        }
      }
    } catch {
      // 忽略错误
    }
  }

  private loadGlobalSkills() {
    if (!fs.existsSync(GLOBAL_SKILLS_DIR)) return;

    try {
      const entries = fs.readdirSync(GLOBAL_SKILLS_DIR, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isDirectory()) {
          const skillPath = path.join(GLOBAL_SKILLS_DIR, entry.name, 'SKILL.md');
          if (fs.existsSync(skillPath)) {
            this.globalSkills.add(entry.name);
          }
        }
      }
    } catch {
      // 忽略错误
    }
  }

  private getSkillScope(skillName: string): 'openclaw-workspace' | 'openclaw-global' | 'unknown' {
    if (this.workspaceSkills.has(skillName)) {
      return 'openclaw-workspace';
    }
    if (this.globalSkills.has(skillName)) {
      return 'openclaw-global';
    }
    return 'unknown';
  }

  async collectStats(): Promise<{ collected: number; updated: number }> {
    if (!fs.existsSync(SESSIONS_DIR)) {
      return { collected: 0, updated: 0 };
    }

    // 确保统计目录存在
    if (!fs.existsSync(STATS_DIR)) {
      fs.mkdirSync(STATS_DIR, { recursive: true });
    }

    // 加载现有统计数据
    let stats: GlobalStats = {
      skills: {},
      lastUpdated: new Date().toISOString(),
      lastProcessedTimestamp: '1970-01-01T00:00:00.000Z'
    };

    if (fs.existsSync(GLOBAL_STATS_PATH)) {
      try {
        const content = fs.readFileSync(GLOBAL_STATS_PATH, 'utf-8');
        stats = JSON.parse(content);
      } catch {
        // 使用默认值
      }
    }

    const lastProcessed = new Date(stats.lastProcessedTimestamp);
    const records: SkillCallRecord[] = [];

    // 扫描会话文件
    const sessionFiles = fs.readdirSync(SESSIONS_DIR)
      .filter((f: string) => f.endsWith('.jsonl'))
      .map((f: string) => path.join(SESSIONS_DIR, f));

    for (const sessionFile of sessionFiles) {
      try {
        const fileStat = fs.statSync(sessionFile);
        const fileModifiedTime = fileStat.mtime.toISOString();

        // 如果文件修改时间早于上次处理时间，跳过
        if (fileModifiedTime <= stats.lastProcessedTimestamp) {
          continue;
        }

        const sessionId = path.basename(sessionFile, '.jsonl');
        const content = fs.readFileSync(sessionFile, 'utf-8');
        const lines = content.split('\n').filter((l: string) => l.trim());

        let cwd = '/unknown';

        for (const line of lines) {
          try {
            const entry = JSON.parse(line);

            // 提取 cwd
            if (entry.type === 'message' && entry.message?.cwd) {
              cwd = entry.message.cwd;
            }

            // 检查时间戳
            const entryTime = new Date(entry.timestamp || 0);
            if (entryTime <= lastProcessed) continue;

            // 解析 skill 调用
            const record = this.parser.parse(entry, sessionId, cwd);
            if (record) {
              records.push(record);
            }
          } catch {
            // 忽略解析错误
          }
        }
      } catch {
        // 忽略文件读取错误
      }
    }

    // 更新统计数据
    const updatedSkills = new Set<string>();
    let maxTimestamp = stats.lastProcessedTimestamp;

    for (const record of records) {
      const { skillName, timestamp, projectPath, success } = record;

      if (!stats.skills[skillName]) {
        stats.skills[skillName] = {
          totalCalls: 0,
          successCount: 0,
          failureCount: 0,
          lastUsed: timestamp,
          projects: [],
          avgExecutionTime: 0,
          scope: this.getSkillScope(skillName),
          status: 'active'
        };
      }

      const skill = stats.skills[skillName];
      skill.totalCalls++;
      if (success) {
        skill.successCount++;
      } else {
        skill.failureCount++;
      }

      if (new Date(timestamp) > new Date(skill.lastUsed)) {
        skill.lastUsed = timestamp;
      }

      if (!skill.projects.includes(projectPath)) {
        skill.projects.push(projectPath);
      }

      updatedSkills.add(skillName);

      if (timestamp > maxTimestamp) {
        maxTimestamp = timestamp;
      }
    }

    // 更新时间戳
    stats.lastUpdated = new Date().toISOString();
    stats.lastProcessedTimestamp = maxTimestamp;

    // 保存统计数据
    fs.writeFileSync(GLOBAL_STATS_PATH, JSON.stringify(stats, null, 2));

    return {
      collected: records.length,
      updated: updatedSkills.size
    };
  }

  async getAllSkills(): Promise<Record<string, SkillStats>> {
    const stats = await this.getStats();
    const allSkills: Record<string, SkillStats> = { ...stats.skills };

    // 添加未使用的 workspace skills
    for (const skillName of this.workspaceSkills) {
      if (!allSkills[skillName]) {
        allSkills[skillName] = {
          totalCalls: 0,
          successCount: 0,
          failureCount: 0,
          lastUsed: '',
          projects: [],
          avgExecutionTime: 0,
          scope: 'openclaw-workspace',
          status: 'never-used'
        };
      }
    }

    // 添加未使用的 global skills
    for (const skillName of this.globalSkills) {
      if (!allSkills[skillName]) {
        allSkills[skillName] = {
          totalCalls: 0,
          successCount: 0,
          failureCount: 0,
          lastUsed: '',
          projects: [],
          avgExecutionTime: 0,
          scope: 'openclaw-global',
          status: 'never-used'
        };
      }
    }

    return allSkills;
  }

  async getStats(): Promise<GlobalStats> {
    if (!fs.existsSync(GLOBAL_STATS_PATH)) {
      return {
        skills: {},
        lastUpdated: new Date().toISOString(),
        lastProcessedTimestamp: '1970-01-01T00:00:00.000Z'
      };
    }

    try {
      const content = fs.readFileSync(GLOBAL_STATS_PATH, 'utf-8');
      return JSON.parse(content);
    } catch {
      return {
        skills: {},
        lastUpdated: new Date().toISOString(),
        lastProcessedTimestamp: '1970-01-01T00:00:00.000Z'
      };
    }
  }
}

