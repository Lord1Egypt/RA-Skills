#!/usr/bin/env node

/**
 * Vibe Coding CN v4.1 - OpenClaw 技能入口
 * 
 * **使用方式**：
 * 在 OpenClaw 对话中直接使用：
 *   用 vibe-coding 做一个个税计算器
 *   用 vibe-coding 做个打字游戏，mode: v4.1
 * 
 * **核心特性**：
 * - 5 Agent 团队协作
 * - SPEC.md 自动生成
 * - Agent 投票审批
 * - 版本管理
 * - 增量更新
 * - 需求追溯
 */

const { VibeExecutor } = require('./executors/vibe-executor');
const { VibeExecutorV4 } = require('./executors/vibe-executor-v4');  // 增强协作模式
const { VibeExecutorV41 } = require('./executors/vibe-executor-v4.1');  // SPEC.md + Agent 投票
const { VersionManager } = require('./executors/version-manager');
const { IncrementalUpdater } = require('./executors/incremental-updater');
const path = require('path');

// 全局版本管理器
const versionManager = new VersionManager(path.join(process.cwd(), 'output'));

/**
 * OpenClaw 技能调用入口
 * 
 * @param {string} requirement - 用户需求描述
 * @param {object} options - 可选配置
 * @param {string} options.mode - 执行模式（v3/v4，默认 v3）
 * @param {function} options.onProgress - 进度回调 (phase, data)
 * @param {string} options.outputDir - 输出目录（默认：./output）
 * @param {string} options.projectId - 项目 ID（用于版本管理）
 * @param {string} options.parentVersion - 父版本（用于增量更新）
 * @param {function} options.llmCallback - OpenClaw LLM 调用函数（可选）
 * @returns {Promise<object>} 执行结果
 */
async function run(requirement, options = {}) {
  const { mode = 'v4.1', onProgress, outputDir, projectId, parentVersion, llmCallback } = options;  // 默认 v4.1（最佳体验）
  
  if (!requirement) {
    throw new Error('需求描述不能为空');
  }
  
  // 生成项目 ID（从需求提取）
  const safeProjectId = projectId || generateProjectId(requirement);
  
  const versionNames = {
    'v3': 'v3.0 - OpenClaw 集成版',
    'v4': 'v4.0（增强协作模式）',
    'v4.1': 'v4.1（SPEC.md + Agent 投票审批）'
  };
  const versionName = versionNames[mode] || versionNames['v3'];
  console.log(`\n🎨 Vibe Coding ${versionName}\n`);
  console.log(`📝 项目 ID: ${safeProjectId}`);
  console.log(`📝 用户需求：${requirement}\n`);
  console.log(`🤖 LLM: ${llmCallback ? 'OpenClaw 集成' : '模拟模式'}\n`);
  
  // 加载或创建项目
  const project = await versionManager.loadOrCreateProject(safeProjectId, requirement);
  
  // 自动查找最新版本（如果没有指定）
  let actualParentVersion = parentVersion;
  if (!actualParentVersion && project.versions.length > 0) {
    actualParentVersion = project.currentVersion;
    console.log(`📚 自动使用最新版本：${actualParentVersion}`);
  }
  
  // 检查是否是增量更新
  let updatePlan = null;
  if (actualParentVersion && project.versions.length > 0) {
    console.log('🔄 检测到增量更新模式...\n');
    
    const oldVersion = project.getVersion(actualParentVersion);
    const updater = new IncrementalUpdater({
      conservatism: options.conservatism || 'balanced'
    });
    
    // 分析需求变化（使用 OpenClaw LLM 或模拟）
    updatePlan = await updater.analyzeChanges(
      oldVersion.requirement,
      requirement,
      {
        files: oldVersion.files,
        architecture: oldVersion.architecture
      },
      llmCallback // 传入 OpenClaw LLM 回调
    );
    
    // 显示更新计划，等待确认
    console.log(updater.formatConfirmationMessage(updatePlan));
    console.log('\n⏸️  等待用户确认...（按 Enter 继续，或修改需求）\n');
  }
  
  // 创建执行器（支持 v3, v4, v4.1 模式）
  const ExecutorClass = mode === 'v4.1' ? VibeExecutorV41 : mode === 'v4' ? VibeExecutorV4 : VibeExecutor;
  const executor = new ExecutorClass(requirement, { 
    outputDir: outputDir || path.join(process.cwd(), 'output', safeProjectId),
    parentVersion: actualParentVersion,
    updatePlan,
    llmCallback,  // 传入 LLM 回调
    conservatism: options.conservatism || 'balanced'
  });
  
  // 重写进度汇报函数，支持回调
  if (onProgress) {
    const originalReport = executor.reportProgress.bind(executor);
    executor.reportProgress = function(phase, data) {
      originalReport(phase, data);
      onProgress(phase, data);
    };
  }
  
  try {
    const state = await executor.execute();
    
    // 保存版本
    const version = await versionManager.saveVersion(safeProjectId, {
      requirement,
      parentVersion,
      changes: updatePlan ? updatePlan.requirementChanges : null,
      files: state.files,
      architecture: state.architecture,
      qualityScore: state.qualityScore
    });
    
    const result = {
      success: true,
      projectId: safeProjectId,
      version,
      projectDir: executor.projectDir,
      duration: state.duration,
      phases: state.phases,
      files: state.files,
      isIncremental: !!updatePlan,
      llmMode: !!llmCallback
    };
    
    console.log('\n✅ 项目完成！\n');
    console.log(`📁 项目 ID: ${safeProjectId}`);
    console.log(`📁 版本：${version}`);
    console.log(`📁 输出目录：${executor.projectDir}`);
    console.log(`⏱️  总耗时：${Math.round(state.duration / 1000)}秒\n`);
    
    // 显示版本历史
    const versions = project.getVersions();
    if (versions.length > 1) {
      console.log('📚 版本历史:');
      versions.forEach(v => {
        const marker = v.version === version ? '← 当前' : '';
        console.log(`  ${v.version} - ${v.requirement.substring(0, 30)}... ${marker}`);
      });
      console.log('');
    }
    
    return result;
    
  } catch (error) {
    console.error('\n❌ 执行失败:', error.message);
    console.error(error.stack);
    throw error;
  }
}

/**
 * 从需求生成项目 ID
 */
function generateProjectId(requirement) {
  // 提取关键词
  const keywords = requirement
    .replace(/[^\w\s\u4e00-\u9fa5]/g, '')
    .split(/\s+/)
    .filter(w => w.length > 1)
    .slice(0, 3)
    .join('-');
  
  // 添加时间戳
  const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const random = Math.random().toString(36).slice(2, 6);
  
  return `${keywords}-${timestamp}-${random}`;
}

// 导出（OpenClaw 技能调用）
module.exports = { run, VibeExecutor, VibeExecutorV4, VibeExecutorV41, VersionManager, IncrementalUpdater };
