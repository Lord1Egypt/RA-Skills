#!/usr/bin/env node

/**
 * Skill Sync - 自动同步技能到 ClawHub 和 GitHub
 * 
 * 功能：
 * 1. 扫描所有 skills
 * 2. 检测需要同步的（新增/修改/未发布）
 * 3. 发布到 ClawHub
 * 4. 提交到 GitHub（独立仓库模式）
 * 5. 记录同步状态
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
  skillsDir: '/Users/xufan65/.openclaw/workspace/skills',
  statusFile: '/Users/xufan65/.openclaw/workspace/memory/skill-sync-status.json',
  logFile: '/Users/xufan65/.openclaw/workspace/memory/skill-sync-log.json',
};

class SkillSync {
  constructor() {
    this.skills = [];
    this.toSync = [];
    this.status = this.loadStatus();
    this.log = this.loadLog();
  }

  /**
   * 加载同步状态
   */
  loadStatus() {
    try {
      if (fs.existsSync(CONFIG.statusFile)) {
        return JSON.parse(fs.readFileSync(CONFIG.statusFile, 'utf8'));
      }
    } catch (e) {
      console.error('加载状态失败:', e.message);
    }
    return { skills: {} };
  }

  /**
   * 保存同步状态
   */
  saveStatus() {
    try {
      fs.writeFileSync(CONFIG.statusFile, JSON.stringify(this.status, null, 2));
    } catch (e) {
      console.error('保存状态失败:', e.message);
    }
  }

  /**
   * 加载同步日志
   */
  loadLog() {
    try {
      if (fs.existsSync(CONFIG.logFile)) {
        return JSON.parse(fs.readFileSync(CONFIG.logFile, 'utf8'));
      }
    } catch (e) {
      console.error('加载日志失败:', e.message);
    }
    return { entries: [] };
  }

  /**
   * 保存同步日志
   */
  saveLog() {
    try {
      // 只保留最近 100 条记录
      if (this.log.entries.length > 100) {
        this.log.entries = this.log.entries.slice(-100);
      }
      fs.writeFileSync(CONFIG.logFile, JSON.stringify(this.log, null, 2));
    } catch (e) {
      console.error('保存日志失败:', e.message);
    }
  }

  /**
   * 加载配置
   */
  loadConfig() {
    try {
      const configPath = '/Users/xufan65/.openclaw/workspace/skills/skill-sync/config/settings.json';
      if (fs.existsSync(configPath)) {
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        return config;
      }
    } catch (e) {
      console.error('加载配置失败:', e.message);
    }
    return { ownSkills: [] };
  }

  /**
   * 检查是否有独立 Git 仓库
   */
  hasOwnGitRepo(skillPath) {
    const gitDir = path.join(skillPath, '.git');
    return fs.existsSync(gitDir);
  }

  /**
   * 扫描所有 skills
   */
  scanSkills() {
    console.log('📁 扫描 skills 目录...\n');
    
    // 加载配置
    const config = this.loadConfig();
    const ownSkills = config.ownSkills || [];
    
    console.log(`📋 配置的自己的 skills (${ownSkills.length} 个):`);
    ownSkills.forEach(skill => console.log(`   • ${skill}`));
    console.log('');
    
    try {
      const dirs = fs.readdirSync(CONFIG.skillsDir, { withFileTypes: true });
      
      this.skills = dirs
        .filter(dirent => {
          if (!dirent.isDirectory()) return false;
          
          // 只包含自己创建的 skills
          if (ownSkills.length > 0 && !ownSkills.includes(dirent.name)) {
            return false;
          }
          
          return true;
        })
        .map(dirent => {
          const skillDir = path.join(CONFIG.skillsDir, dirent.name);
          const skillMdPath = path.join(skillDir, 'SKILL.md');
          
          // 检查是否有 SKILL.md
          if (!fs.existsSync(skillMdPath)) {
            return null;
          }

          // 读取 SKILL.md
          const skillMd = fs.readFileSync(skillMdPath, 'utf8');
          
          // 提取元数据
          const metadata = this.parseSkillMetadata(skillMd);
          
          // 检查是否有独立 Git 仓库
          const hasOwnRepo = this.hasOwnGitRepo(skillDir);
          
          return {
            name: dirent.name,
            path: skillDir,
            skillMdPath,
            metadata,
            modified: this.getFileModifiedTime(skillMdPath),
            hasOwnRepo
          };
        })
        .filter(skill => skill !== null);

      console.log(`✅ 找到 ${this.skills.length} 个自己的 skills:\n`);
      this.skills.forEach(skill => {
        const version = skill.metadata.version || 'unknown';
        const repoIcon = skill.hasOwnRepo ? '📦' : '📁';
        console.log(`   ${repoIcon} ${skill.name} (v${version}) ${skill.hasOwnRepo ? '[独立仓库]' : ''}`);
      });
    } catch (e) {
      console.error('❌ 扫描失败:', e.message);
      process.exit(1);
    }
  }

  /**
   * 解析 SKILL.md 元数据
   */
  parseSkillMetadata(content) {
    const metadata = {};
    
    // 提取 YAML front matter
    const frontMatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontMatterMatch) {
      const frontMatter = frontMatterMatch[1];
      
      // 提取 name
      const nameMatch = frontMatter.match(/^name:\s*(.+)$/m);
      if (nameMatch) metadata.name = nameMatch[1].trim();
      
      // 提取 version
      const versionMatch = frontMatter.match(/^version:\s*["']?(.+?)["']?\s*$/m);
      if (versionMatch) metadata.version = versionMatch[1].trim();
      
      // 提取 description
      const descMatch = frontMatter.match(/^description:\s*["']?(.+?)["']?\s*$/m);
      if (descMatch) metadata.description = descMatch[1].trim();
    }
    
    return metadata;
  }

  /**
   * 获取文件修改时间
   */
  getFileModifiedTime(filePath) {
    try {
      const stats = fs.statSync(filePath);
      return stats.mtime.toISOString();
    } catch (e) {
      return null;
    }
  }

  /**
   * 检测需要同步的 skills
   */
  detectNeedSync() {
    console.log('\n🔍 检测需要同步的 skills...\n');
    
    this.toSync = [];
    
    this.skills.forEach(skill => {
      // 只同步有独立仓库的 skills
      if (!skill.hasOwnRepo) {
        console.log(`   ⏭️  ${skill.name} - 跳过（无独立仓库）`);
        return;
      }
      
      const status = this.status.skills[skill.name];
      const needSync = this.checkIfNeedSync(skill, status);
      
      if (needSync) {
        this.toSync.push(skill);
        console.log(`   ✅ ${skill.name} - 需要同步`);
        console.log(`      原因: ${needSync}`);
      } else {
        console.log(`   ⏭️  ${skill.name} - 无需同步`);
      }
    });

    console.log(`\n📊 总计: ${this.toSync.length} 个 skills 需要同步\n`);
    
    return this.toSync.length > 0;
  }

  /**
   * 检查是否需要同步
   */
  checkIfNeedSync(skill, status) {
    // 从未同步
    if (!status) {
      return '从未同步';
    }
    
    // 文件已修改
    const lastModified = skill.modified;
    const lastSynced = status.lastSynced;
    
    if (lastModified && lastSynced && new Date(lastModified) > new Date(lastSynced)) {
      return '文件已修改';
    }
    
    // 同步失败
    if (status.status === 'failed') {
      return '上次同步失败';
    }
    
    // 未推送到 GitHub
    if (!status.gitCommit) {
      return '未推送到 GitHub';
    }
    
    return null;
  }

  /**
   * 发布到 ClawHub（单个 skill）
   */
  async publishToClawHub(skill) {
    console.log(`\n📤 发布 ${skill.name} 到 ClawHub...`);
    
    try {
      const cmd = `cd "${skill.path}" && clawhub publish . --slug ${skill.name} --name "${skill.metadata.name || skill.name}" --version ${skill.metadata.version || '1.0.0'}`;
      
      const result = execSync(cmd, { 
        encoding: 'utf8',
        timeout: 60000 
      });
      
      // 提取 ClawHub ID
      const idMatch = result.match(/Published .+? \((.+?)\)/);
      const clawhubId = idMatch ? idMatch[1] : null;
      
      if (clawhubId) {
        console.log(`   ✅ 发布成功！ID: ${clawhubId}`);
        return { success: true, clawhubId };
      } else {
        console.log(`   ⚠️  发布成功，但无法提取 ID`);
        return { success: true, clawhubId: null };
      }
    } catch (e) {
      console.error(`   ❌ 发布失败:`, e.message);
      return { success: false, error: e.message };
    }
  }

  /**
   * 提交到 GitHub（单个 skill，独立仓库）
   */
  async commitToGitHub(skill) {
    console.log(`\n📦 提交 ${skill.name} 到 GitHub...`);
    
    try {
      // 1. Git add
      console.log(`   1️⃣  Git add...`);
      const addCmd = `cd "${skill.path}" && git add .`;
      execSync(addCmd, { encoding: 'utf8' });
      
      // 2. Git commit
      console.log(`   2️⃣  Git commit...`);
      const version = skill.metadata.version || 'unknown';
      const commitMsg = `Update ${skill.name} to v${version}`;
      const commitCmd = `cd "${skill.path}" && git commit -m "${commitMsg}"`;
      
      try {
        const commitResult = execSync(commitCmd, { encoding: 'utf8' });
        
        // 提取 commit hash
        const hashMatch = commitResult.match(/\[main ([a-f0-9]+)\]/);
        const commitHash = hashMatch ? hashMatch[1] : null;
        
        if (commitHash) {
          console.log(`   ✅ 提交成功！Commit: ${commitHash}`);
        } else {
          console.log(`   ✅ 提交成功！`);
        }
        
        // 3. Git push
        console.log(`   3️⃣  Git push...`);
        const pushCmd = `cd "${skill.path}" && git push origin main`;
        execSync(pushCmd, { encoding: 'utf8' });
        console.log(`   ✅ 推送成功！`);
        
        return { success: true, commitHash };
        
      } catch (e) {
        if (e.message.includes('nothing to commit')) {
          console.log(`   ⏭️  没有需要提交的更改`);
          return { success: true, commitHash: null, noChanges: true };
        }
        throw e;
      }
    } catch (e) {
      console.error(`   ❌ 提交失败:`, e.message);
      return { success: false, error: e.message };
    }
  }

  /**
   * 更新同步状态
   */
  updateStatus(skill, clawhubResult, gitResult) {
    const now = new Date().toISOString();
    
    this.status.skills[skill.name] = {
      version: skill.metadata.version || 'unknown',
      clawhubId: clawhubResult.clawhubId || this.status.skills[skill.name]?.clawhubId,
      clawhubPublished: clawhubResult.success ? now : this.status.skills[skill.name]?.clawhubPublished,
      gitCommit: gitResult.commitHash || this.status.skills[skill.name]?.gitCommit,
      gitPushed: gitResult.success ? now : this.status.skills[skill.name]?.gitPushed,
      lastSynced: now,
      status: (clawhubResult.success || clawhubResult.success === undefined) && gitResult.success ? 'synced' : 'failed'
    };
    
    this.saveStatus();
  }

  /**
   * 记录日志
   */
  logSync(skill, clawhubResult, gitResult) {
    this.log.entries.push({
      timestamp: new Date().toISOString(),
      skill: skill.name,
      version: skill.metadata.version || 'unknown',
      clawhub: {
        success: clawhubResult.success || false,
        id: clawhubResult.clawhubId,
        error: clawhubResult.error
      },
      git: {
        success: gitResult.success,
        commit: gitResult.commitHash,
        error: gitResult.error
      }
    });
    
    this.saveLog();
  }

  /**
   * 生成同步报告
   */
  generateReport() {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    
    let report = `# 🔄 Skill Sync 同步报告\n\n`;
    report += `**时间**: ${timestamp}\n`;
    report += `**检查数量**: ${this.skills.length} 个 skills\n`;
    report += `**独立仓库**: ${this.skills.filter(s => s.hasOwnRepo).length} 个\n`;
    report += `**需要同步**: ${this.toSync.length} 个\n\n`;
    
    if (this.toSync.length === 0) {
      report += `✅ **所有 skills 已是最新状态！**\n`;
    } else {
      report += `## 📊 同步结果\n\n`;
      
      this.toSync.forEach(skill => {
        const status = this.status.skills[skill.name];
        const clawhubIcon = status?.clawhubId ? '✅' : '❌';
        const gitIcon = status?.gitCommit ? '✅' : '❌';
        
        report += `### ${skill.name} (v${skill.metadata.version || 'unknown'})\n`;
        report += `- **ClawHub**: ${clawhubIcon} ${status?.clawhubId ? `已发布 (${status.clawhubId})` : '未发布'}\n`;
        report += `- **GitHub**: ${gitIcon} ${status?.gitCommit ? `已提交 (${status.gitCommit})` : '未提交'}\n`;
        report += `- **状态**: ${status?.status || 'unknown'}\n\n`;
      });
    }
    
    return report;
  }

  /**
   * 主运行函数
   */
  async run() {
    console.log('🚀 Skill Sync 启动\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    // 1. 扫描 skills
    this.scanSkills();

    // 2. 检测需要同步的 skills
    const hasSkillsToSync = this.detectNeedSync();

    if (!hasSkillsToSync) {
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('✅ Skill Sync 完成\n');
      return;
    }

    // 3. 同步每个 skill
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🔄 开始同步...\n');

    for (const skill of this.toSync) {
      console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      console.log(`📝 处理: ${skill.name}\n`);

      // 发布到 ClawHub
      const clawhubResult = await this.publishToClawHub(skill);

      // 提交到 GitHub
      const gitResult = await this.commitToGitHub(skill);

      // 更新状态
      this.updateStatus(skill, clawhubResult, gitResult);

      // 记录日志
      this.logSync(skill, clawhubResult, gitResult);
    }

    // 4. 生成报告
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const report = this.generateReport();
    console.log('\n' + report);

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ Skill Sync 完成\n');
  }
}

// 运行
if (require.main === module) {
  const sync = new SkillSync();
  sync.run().catch(e => {
    console.error('❌ 运行失败:', e);
    process.exit(1);
  });
}

module.exports = SkillSync;
