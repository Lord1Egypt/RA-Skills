/**
 * src/integrations/git_manager.js
 * Git 集成 - 记忆版本化、不可变历史、跨设备同步
 */

import { execSync } from 'child_process';
import { existsSync, mkdirSync, writeFileSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { config } from '../config.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

export class GitManager {
  /**
   * @param {Object} opts
   * @param {string} [opts.repo_path] - Git 仓库路径，默认 memoryDir/.git
   */
  constructor({ repo_path } = {}) {
    this.repo_path = repo_path || join(config.memoryDir, '.git-repo');
  }

  /**
   * 初始化 git 仓库
   * @param {Object} opts
   * @param {string} [opts.remote_url] - 远程仓库 URL
   */
  async init({ remote_url } = {}) {
    mkdirSync(this.repo_path, { recursive: true });
    
    try {
      execSync('git init', { cwd: this.repo_path, stdio: 'pipe' });
    } catch (e) {
      // 可能已经初始化
    }

    // 添加 .gitignore
    const gitignore = join(this.repo_path, '.gitignore');
    if (!existsSync(gitignore)) {
      writeFileSync(gitignore, [
        'node_modules/',
        '*.log',
        'vector_cache/',
        'wal/',
        '.DS_Store',
        ''
      ].join('\n'));
      execSync('git add .gitignore', { cwd: this.repo_path, stdio: 'pipe' });
      try {
        execSync('git commit -m "chore: add .gitignore"', { cwd: this.repo_path, stdio: 'pipe' });
      } catch {}
    }

    if (remote_url) {
      try {
        execSync(`git remote add origin ${remote_url}`, { cwd: this.repo_path, stdio: 'pipe' });
      } catch {
        // remote 可能已存在
      }
    }

    return { repo_path: this.repo_path, initialized: true };
  }

  /**
   * Git add + commit
   * @param {Object} opts
   * @param {string} opts.message - 提交信息
   * @param {string[]} [opts.files] - 要提交的文件，默认全提交
   */
  async commit({ message, files = ['.'] } = {}) {
    const filesStr = files.join(' ');
    try {
      execSync(`git add ${filesStr}`, { cwd: this.repo_path, stdio: 'pipe' });
      execSync(`git commit -m "${message.replace(/"/g, '\\"')}"`, { cwd: this.repo_path, stdio: 'pipe' });
      return { committed: true, message };
    } catch (e) {
      const out = e.message || '';
      if (out.includes('nothing to commit')) {
        return { committed: false, reason: 'nothing to commit' };
      }
      throw e;
    }
  }

  /**
   * 保存 git notes（元数据标签）
   * @param {Object} opts
   * @param {string} [opts.ref='HEAD'] - commit ref
   * @param {string} opts.key - 标签 key
   * @param {string} opts.value - 标签值
   */
  async saveNote({ ref = 'HEAD', key, value } = {}) {
    const msg = `${key}: ${value}`;
    try {
      execSync(`git notes add -f -m "${msg}" ${ref}`, { cwd: this.repo_path, stdio: 'pipe' });
      return { saved: true, ref, key, value };
    } catch (e) {
      return { saved: false, error: e.message };
    }
  }

  /**
   * 获取提交历史
   * @param {Object} opts
   * @param {string} [opts.since] - 起始时间 ISO 字符串
   * @param {number} [opts.limit=50] - 条目数
   */
  async getHistory({ since, limit = 50 } = {}) {
    const sinceArg = since ? `--since="${since}"` : '';
    const cmd = `git log ${sinceArg} -n ${limit} --pretty=format:"%H|%ai|%s" ${sinceArg ? '' : '--'}`;
    
    try {
      const out = execSync(cmd, { cwd: this.repo_path, encoding: 'utf-8' });
      if (!out.trim()) return [];
      
      return out.split('\n').filter(Boolean).map(line => {
        const [hash, date, ...subjectParts] = line.split('|');
        return {
          hash: hash.trim(),
          date: date.trim(),
          subject: subjectParts.join('|').trim(),
        };
      });
    } catch (e) {
      return [];
    }
  }

  /**
   * Push 到远程
   */
  async push({ remote = 'origin', branch = 'main' } = {}) {
    try {
      execSync(`git push ${remote} ${branch}`, { cwd: this.repo_path, stdio: 'pipe' });
      return { pushed: true, remote, branch };
    } catch (e) {
      return { pushed: false, error: e.message };
    }
  }

  /**
   * Pull 从远程
   */
  async pull({ remote = 'origin', branch = 'main' } = {}) {
    try {
      execSync(`git pull ${remote} ${branch}`, { cwd: this.repo_path, stdio: 'pipe' });
      return { pulled: true, remote, branch };
    } catch (e) {
      return { pulled: false, error: e.message };
    }
  }

  /**
   * 获取当前状态
   */
  async status() {
    try {
      const out = execSync('git status --porcelain', { cwd: this.repo_path, encoding: 'utf-8' });
      return { clean: !out.trim(), changes: out.trim().split('\n').filter(Boolean) };
    } catch {
      return { clean: true, changes: [] };
    }
  }
}

// 导出单例（延迟初始化）
let _instance = null;
export function getGitManager(opts = {}) {
  if (!_instance) {
    _instance = new GitManager(opts);
  }
  return _instance;
}
