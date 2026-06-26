#!/usr/bin/env node

/**
 * Vibe Coding 版本管理器 v1.0
 * 
 * 核心功能：
 * 1. 版本管理 - 保存 v1.0/v2.0/v3.0
 * 2. 增量更新 - 基于上一版修改
 * 3. 需求演化追踪 - 记录需求变化历史
 * 4. 版本对比 - 显示差异
 */

const fs = require('fs').promises;
const path = require('path');

/**
 * 项目元数据结构
 */
class ProjectMetadata {
  constructor(projectId, initialRequirement) {
    this.projectId = projectId;
    this.createdAt = new Date().toISOString();
    this.currentVersion = null;
    this.versions = [];
    this.requirementEvolution = [];
    this.addRequirement(initialRequirement);
  }

  /**
   * 添加需求（记录演化历史）
   */
  addRequirement(requirement) {
    this.requirementEvolution.push({
      version: this.getNextVersion(),
      requirement,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 获取下一个版本号
   */
  getNextVersion() {
    const num = this.versions.length + 1;
    return `v${num}.0`;
  }

  /**
   * 添加新版本
   */
  addVersion(versionData) {
    const version = this.getNextVersion();
    
    this.versions.push({
      version,
      ...versionData,
      timestamp: new Date().toISOString(),
      status: 'current'
    });

    // 将之前的版本标记为 superseded
    this.versions.forEach(v => {
      if (v.version !== version) {
        v.status = 'superseded';
      }
    });

    this.currentVersion = version;
    return version;
  }

  /**
   * 获取当前版本
   */
  getCurrentVersion() {
    return this.versions.find(v => v.version === this.currentVersion);
  }

  /**
   * 获取指定版本
   */
  getVersion(versionNum) {
    return this.versions.find(v => v.version === versionNum);
  }

  /**
   * 获取版本列表
   */
  getVersions() {
    return this.versions.map(v => ({
      version: v.version,
      requirement: v.requirement,
      timestamp: v.timestamp,
      status: v.status,
      fileCount: v.files?.length || 0
    }));
  }

  /**
   * 版本对比
   */
  compareVersions(v1Num, v2Num) {
    const v1 = this.getVersion(v1Num);
    const v2 = this.getVersion(v2Num);
    
    if (!v1 || !v2) {
      throw new Error(`版本不存在：${v1Num} 或 ${v2Num}`);
    }

    return {
      from: v1Num,
      to: v2Num,
      requirementChange: {
        from: v1.requirement,
        to: v2.requirement
      },
      filesChanged: {
        added: v2.files?.filter(f => !v1.files?.find(f1 => f1.name === f.name)) || [],
        removed: v1.files?.filter(f => !v2.files?.find(f2 => f2.name === f.name)) || [],
        modified: v2.files?.filter(f => {
          const f1 = v1.files?.find(f1 => f1.name === f.name);
          return f1 && f1.size !== f.size;
        }) || []
      }
    };
  }

  /**
   * 序列化
   */
  toJSON() {
    return {
      projectId: this.projectId,
      createdAt: this.createdAt,
      currentVersion: this.currentVersion,
      versions: this.getVersions(),
      requirementEvolution: this.requirementEvolution
    };
  }
}

/**
 * 版本管理器
 */
class VersionManager {
  constructor(outputDir) {
    this.outputDir = outputDir;
    this.projects = new Map();
  }

  /**
   * 创建或加载项目
   */
  async loadOrCreateProject(projectId, initialRequirement) {
    const metaPath = path.join(this.outputDir, projectId, 'project-meta.json');
    
    try {
      // 尝试加载现有项目
      const metaContent = await fs.readFile(metaPath, 'utf-8');
      const meta = JSON.parse(metaContent);
      
      const project = new ProjectMetadata(projectId, initialRequirement);
      project.versions = meta.versions || [];
      project.currentVersion = meta.currentVersion;
      project.requirementEvolution = meta.requirementEvolution || [];
      
      this.projects.set(projectId, project);
      console.log(`[VersionManager] 加载现有项目：${projectId} (${project.versions.length} 个版本)`);
      
      return project;
    } catch (error) {
      // 创建新项目
      const project = new ProjectMetadata(projectId, initialRequirement);
      this.projects.set(projectId, project);
      console.log(`[VersionManager] 创建新项目：${projectId}`);
      
      return project;
    }
  }

  /**
   * 保存版本
   */
  async saveVersion(projectId, versionData) {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`项目不存在：${projectId}`);
    }

    const version = project.addVersion(versionData);
    const versionDir = path.join(this.outputDir, projectId, version);

    // 保存版本元数据
    const metaPath = path.join(versionDir, 'version-meta.json');
    await fs.mkdir(versionDir, { recursive: true });
    await fs.writeFile(metaPath, JSON.stringify({
      version,
      requirement: versionData.requirement,
      timestamp: new Date().toISOString(),
      parentVersion: versionData.parentVersion,
      changes: versionData.changes,
      files: versionData.files
    }, null, 2));

    // 保存项目总元数据
    await this.saveProjectMeta(project);

    console.log(`[VersionManager] 保存版本：${version} (${versionData.files?.length || 0} 个文件)`);
    
    return version;
  }

  /**
   * 保存文件到指定版本
   */
  async saveFile(projectId, version, filename, content) {
    const filePath = path.join(this.outputDir, projectId, version, filename);
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    await fs.writeFile(filePath, content);
  }

  /**
   * 保存项目元数据
   */
  async saveProjectMeta(project) {
    const projectDir = path.join(this.outputDir, project.projectId);
    const metaPath = path.join(projectDir, 'project-meta.json');
    
    await fs.mkdir(projectDir, { recursive: true });
    await fs.writeFile(metaPath, JSON.stringify(project.toJSON(), null, 2));
  }

  /**
   * 获取版本对比
   */
  async compareVersions(projectId, v1Num, v2Num) {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`项目不存在：${projectId}`);
    }

    return project.compareVersions(v1Num, v2Num);
  }

  /**
   * 获取需求演化历史
   */
  getRequirementEvolution(projectId) {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`项目不存在：${projectId}`);
    }

    return project.requirementEvolution;
  }

  /**
   * 回退到指定版本
   */
  async revertToVersion(projectId, targetVersion) {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`项目不存在：${projectId}`);
    }

    const target = project.getVersion(targetVersion);
    if (!target) {
      throw new Error(`版本不存在：${targetVersion}`);
    }

    // 创建新版本，内容是目标版本的副本
    const sourceDir = path.join(this.outputDir, projectId, targetVersion);
    const newVersion = project.getNextVersion();
    const targetDir = path.join(this.outputDir, projectId, newVersion);

    // 复制文件
    await this.copyDirectory(sourceDir, targetDir);

    // 保存新版本元数据
    await this.saveVersion(projectId, {
      requirement: `回退到 ${targetVersion}: ${target.requirement}`,
      parentVersion: project.currentVersion,
      changes: [`回退到版本 ${targetVersion}`],
      files: target.files
    });

    console.log(`[VersionManager] 回退到版本：${targetVersion} → ${newVersion}`);
    
    return newVersion;
  }

  /**
   * 复制目录
   */
  async copyDirectory(src, dest) {
    await fs.mkdir(dest, { recursive: true });
    const entries = await fs.readdir(src, { withFileTypes: true });

    for (const entry of entries) {
      const srcPath = path.join(src, entry.name);
      const destPath = path.join(dest, entry.name);

      if (entry.isDirectory()) {
        await this.copyDirectory(srcPath, destPath);
      } else {
        await fs.copyFile(srcPath, destPath);
      }
    }
  }
}

// 导出
module.exports = { VersionManager, ProjectMetadata };
