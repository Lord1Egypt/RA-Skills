#!/usr/bin/env node

/**
 * Vibe Coding 增量更新分析器 v3.0
 * 
 * **重要**：使用 OpenClaw 的 LLM 能力，不直接调用 API
 * 通过 OpenClaw 会话调用或外部传入分析结果
 * 
 * 使用方式：
 * 1. OpenClaw 环境：通过 sessions_spawn 调用子 Agent
 * 2. 独立环境：传入预分析结果（用于测试）
 */

/**
 * 增量更新分析器
 */
class IncrementalUpdater {
  constructor(options = {}) {
    this.model = options.model || 'qwen3.5-plus';
    this.thinking = options.thinking || 'high';
    this.conservatism = options.conservatism || 'balanced';
    this.openclawSession = options.openclawSession; // OpenClaw sessions_spawn 函数
  }

  /**
   * 分析需求变化（OpenClaw 集成版）
   * 
   * @param {string} oldRequirement - 旧需求
   * @param {string} newRequirement - 新需求
   * @param {object} oldVersion - 旧版本信息
   * @param {function} llmCallback - OpenClaw LLM 调用回调（可选）
   * @returns {Promise<object>} 增量更新计划
   */
  async analyzeChanges(oldRequirement, newRequirement, oldVersion, llmCallback = null) {
    console.log('[IncrementalUpdater v3.0] 开始分层次分析...');
    console.log(`  保守度：${this.getConservatismLabel()}`);
    console.log(`  LLM 模式：${llmCallback ? 'OpenClaw 集成' : '外部传入'}`);

    // 如果有 LLM 回调，使用 OpenClaw 调用
    if (llmCallback) {
      return await this.analyzeWithOpenClaw(oldRequirement, newRequirement, oldVersion, llmCallback);
    }

    // 否则返回预分析结果（用于测试或外部已分析的情况）
    console.log('[IncrementalUpdater v3.0] 使用预分析结果...');
    return this.generateMockAnalysis(oldRequirement, newRequirement, oldVersion);
  }

  /**
   * 使用 OpenClaw 进行分析
   */
  async analyzeWithOpenClaw(oldReq, newReq, oldVersion, llmCallback) {
    // Step 1: 需求层分析
    console.log('[1/4] 需求层分析（调用 OpenClaw LLM）...');
    const requirementAnalysis = await this.analyzeRequirementLayerWithLLM(
      oldReq, newReq, llmCallback
    );

    // Step 2: 架构层分析
    console.log('[2/4] 架构层分析...');
    const architectureAnalysis = await this.analyzeArchitectureLayer(
      requirementAnalysis, oldVersion.architecture, llmCallback
    );

    // Step 3: 文件层分析
    console.log('[3/4] 文件层分析...');
    const fileAnalysis = await this.analyzeFileLayer(
      requirementAnalysis, architectureAnalysis, oldVersion.files, llmCallback
    );

    // Step 4: 整合生成更新计划
    console.log('[4/4] 整合生成更新计划...');
    const plan = await this.generateUpdatePlan(
      requirementAnalysis, architectureAnalysis, fileAnalysis, oldVersion
    );

    console.log(`[IncrementalUpdater v3.0] 分析完成：${plan.changeType} 类型更新`);
    return plan;
  }

  /**
   * 需求层分析（调用 OpenClaw LLM）
   */
  async analyzeRequirementLayerWithLLM(oldReq, newReq, llmCallback) {
    const prompt = this.buildRequirementAnalysisPrompt(oldReq, newReq);
    
    try {
      const response = await llmCallback(prompt, this.model, this.thinking);
      return this.parseLLMResponse(response);
    } catch (error) {
      console.error('[需求层分析] LLM 调用失败:', error.message);
      // 降级到简单分析
      return this.simpleRequirementAnalysis(oldReq, newReq);
    }
  }

  /**
   * 构建需求分析提示词
   */
  buildRequirementAnalysisPrompt(oldReq, newReq) {
    return `
你是一个专业的产品经理，擅长需求变更分析。

## 旧需求
${oldReq}

## 新需求
${newReq}

## 分析任务

### 1. 语义相似度评估 (0-100)
- 90-100: 几乎相同，只是措辞微调
- 70-89: 核心相同，有细节调整
- 50-69: 部分相同，有重要变更
- 30-49: 差异较大，但有重叠
- 0-29: 完全不同的需求

### 2. 需求变化分类
**新增需求**：旧需求中没有，新需求中明确提出的功能
**修改需求**：旧需求中有，但新需求中改变了描述
**删除需求**：旧需求中有，但新需求中不再提及
**保持需求**：旧需求和新需求中都存在且描述一致

### 3. 变更意图推断
用户说"${newReq}"时，ta 真正想要的是什么？

## 输出格式（JSON）
{
  "similarityScore": 75,
  "changeCategories": {
    "added": [{"requirement": "...", "confidence": 0.9}],
    "modified": [{"from": "...", "to": "...", "changeType": "...", "confidence": 0.8}],
    "deleted": [{"requirement": "...", "confidence": 0.7}],
    "unchanged": [{"requirement": "...", "confidence": 0.95}]
  },
  "userIntent": {
    "primaryIntent": "功能增强 | 风格调整 | 新增功能 | 完全重构",
    "description": "用户真正想要的是什么"
  },
  "ambiguities": [
    {"term": "...", "possibleInterpretations": ["...", "..."], "needsClarification": true}
  ]
}

只返回 JSON，不要其他内容。
`;
  }

  /**
   * 解析 LLM 响应
   */
  parseLLMResponse(response) {
    try {
      // 提取 JSON
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        throw new Error('响应中未找到 JSON');
      }
      return JSON.parse(jsonMatch[0]);
    } catch (error) {
      console.error('[解析 LLM 响应] 失败:', error.message);
      throw error;
    }
  }

  /**
   * 简单需求分析（降级方案）
   */
  simpleRequirementAnalysis(oldReq, newReq) {
    // 简单字符串比较
    const isSimilar = oldReq.length > 0 && newReq.includes(oldReq.substring(0, 5));
    
    return {
      similarityScore: isSimilar ? 75 : 40,
      changeCategories: {
        added: [{ requirement: newReq, confidence: 0.8 }],
        modified: [],
        deleted: [],
        unchanged: [{ requirement: oldReq, confidence: 0.7 }]
      },
      userIntent: {
        primaryIntent: isSimilar ? '功能增强' : '完全重构',
        description: isSimilar ? '在原有基础上增强' : '全新的需求方向'
      },
      ambiguities: []
    };
  }

  /**
   * 架构层分析
   */
  async analyzeArchitectureLayer(requirementAnalysis, architecture, llmCallback) {
    if (!architecture) {
      return { impact: 'unknown', changes: [] };
    }

    if (!llmCallback) {
      return { impact: 'local', changes: [] };
    }

    const prompt = `
你是一个系统架构师，评估需求变更对架构的影响。

## 当前架构
${architecture}

## 需求变更
${JSON.stringify(requirementAnalysis.changeCategories)}

分析架构影响（JSON 格式）：
{
  "impact": "none" | "local" | "major" | "architectural",
  "moduleChanges": [{"module": "...", "changeType": "...", "impactLevel": "..."}],
  "riskPoints": [{"risk": "...", "severity": "..."}]
}
`;

    try {
      return await llmCallback(prompt, this.model, this.thinking);
    } catch (error) {
      console.error('[架构层分析] 失败:', error.message);
      return { impact: 'local', changes: [] };
    }
  }

  /**
   * 文件层分析
   */
  async analyzeFileLayer(requirementAnalysis, architectureAnalysis, files, llmCallback) {
    if (!files || files.length === 0) {
      return { add: [], modify: [], keep: [] };
    }

    if (!llmCallback) {
      // 简单分析：默认新增 1 个文件，修改 1 个文件
      return {
        add: [{ file: 'new-feature.js', reason: '新增功能' }],
        modify: [{ file: 'app.js', changes: [{ changeType: '功能集成' }], estimatedChangePercent: 20 }],
        keep: files.slice(0, Math.max(0, files.length - 1))
      };
    }

    const prompt = `
你是一个资深开发工程师，分析文件级变更。

## 当前文件
${this.formatFilesDetailed(files)}

## 需求变更
${JSON.stringify(requirementAnalysis.changeCategories)}

## 保守度策略
${this.getConservatismInstruction()}

分析文件变更（JSON 格式）：
{
  "add": [{"file": "...", "reason": "...", "estimatedLines": 100}],
  "modify": [{"file": "...", "changes": [...], "estimatedChangePercent": 20}],
  "keep": [{"file": "...", "reason": "..."}],
  "dependencyChain": [{"source": "...", "affects": [...], "requiresSync": true}]
}
`;

    try {
      return await llmCallback(prompt, this.model, this.thinking);
    } catch (error) {
      console.error('[文件层分析] 失败:', error.message);
      return {
        add: [],
        modify: [{ file: 'app.js', changes: [], estimatedChangePercent: 20 }],
        keep: files
      };
    }
  }

  /**
   * 生成更新计划
   */
  async generateUpdatePlan(reqAnalysis, archAnalysis, fileAnalysis, oldVersion) {
    const changeType = this.determineChangeType(reqAnalysis, archAnalysis, fileAnalysis);

    return {
      version: '3.0',
      changeType,
      requirementChanges: {
        added: reqAnalysis.changeCategories.added?.map(a => a.requirement) || [],
        modified: reqAnalysis.changeCategories.modified?.map(m => ({
          from: m.from,
          to: m.to,
          impact: m.changeType
        })) || [],
        deleted: reqAnalysis.changeCategories.deleted?.map(d => d.requirement) || [],
        unchanged: reqAnalysis.changeCategories.unchanged?.map(u => u.requirement) || []
      },
      fileChanges: {
        add: fileAnalysis.add || [],
        modify: fileAnalysis.modify || [],
        keep: fileAnalysis.keep || []
      },
      architectureChanges: archAnalysis.architectureChanges || [],
      dependencyChain: fileAnalysis.dependencyChain || [],
      updateStrategy: {
        approach: changeType === 'incremental' ? 'incremental' : 'rewrite',
        reason: this.getChangeTypeReason(changeType, reqAnalysis, archAnalysis),
        riskPoints: this.collectRiskPoints(archAnalysis, fileAnalysis),
        estimatedEffort: this.estimateEffort(fileAnalysis),
        confidence: this.calculateConfidence(reqAnalysis, fileAnalysis)
      },
      ambiguities: reqAnalysis.ambiguities || [],
      userIntent: reqAnalysis.userIntent
    };
  }

  /**
   * 生成模拟分析（用于测试）
   */
  generateMockAnalysis(oldReq, newReq, oldVersion) {
    // 基于需求文本的简单启发式分析
    const hasAddKeyword = /新增 | 加上 | 添加 | 支持/.test(newReq);
    const hasStyleKeyword = /风格 | 专业 | 美观 | 颜色 | 界面/.test(newReq);
    const hasRefactorKeyword = /重构 | 重写 | 重新 | 完全/.test(newReq);

    let changeType = 'incremental';
    if (hasRefactorKeyword) changeType = 'rewrite';
    else if (hasAddKeyword && hasStyleKeyword) changeType = 'major';

    return {
      version: '3.0',
      changeType,
      requirementChanges: {
        added: hasAddKeyword ? ['新功能'] : [],
        modified: hasStyleKeyword ? [{ from: '旧风格', to: '新风格', impact: '风格调整' }] : [],
        deleted: [],
        unchanged: ['核心功能']
      },
      fileChanges: {
        add: hasAddKeyword ? [{ file: 'new-feature.js', reason: '新增功能', estimatedLines: 150 }] : [],
        modify: [
          {
            file: 'app.js',
            changes: [{ changeType: '功能集成', description: '集成新功能' }],
            estimatedChangePercent: hasStyleKeyword ? 30 : 20
          }
        ],
        keep: oldVersion.files?.slice(0, 2) || [{ name: 'core.js' }]
      },
      updateStrategy: {
        approach: changeType === 'incremental' ? 'incremental' : 'rewrite',
        reason: changeType === 'incremental' ? '需求基本一致，局部调整' : '需求变化较大',
        riskPoints: [],
        estimatedEffort: changeType === 'incremental' ? 'low' : 'high',
        confidence: 0.75
      },
      ambiguities: [],
      userIntent: {
        primaryIntent: hasAddKeyword ? '功能增强' : hasStyleKeyword ? '风格调整' : '其他',
        description: newReq
      }
    };
  }

  // ===== 辅助方法 =====

  determineChangeType(reqAnalysis, archAnalysis, fileAnalysis) {
    const similarity = reqAnalysis.similarityScore || 75;
    if (similarity < 30) return 'rewrite';
    if (similarity < 50) return 'major';
    return 'incremental';
  }

  getChangeTypeReason(changeType, reqAnalysis, archAnalysis) {
    const similarity = reqAnalysis.similarityScore || 75;
    if (changeType === 'rewrite') return `需求差异较大（相似度${similarity}%）`;
    if (changeType === 'major') return `需求有重要变更（相似度${similarity}%）`;
    return `需求基本一致（相似度${similarity}%），主要是局部调整`;
  }

  collectRiskPoints(archAnalysis, fileAnalysis) {
    const risks = [];
    if (archAnalysis.riskPoints) {
      archAnalysis.riskPoints.forEach(r => risks.push(`${r.severity === 'high' ? '🔴' : '🟡'} ${r.risk}`));
    }
    return risks;
  }

  estimateEffort(fileAnalysis) {
    const addLines = (fileAnalysis.add || []).reduce((sum, f) => sum + (f.estimatedLines || 0), 0);
    if (addLines < 100) return 'low';
    if (addLines < 300) return 'medium';
    return 'high';
  }

  calculateConfidence(reqAnalysis, fileAnalysis) {
    const hasAmbiguities = reqAnalysis.ambiguities?.length > 0;
    return hasAmbiguities ? 0.6 : 0.85;
  }

  formatFilesDetailed(files) {
    if (!files || files.length === 0) return '无文件';
    return files.map(f => `  - ${f.name}${f.size ? ` (${f.size} bytes)` : ''}`).join('\n');
  }

  getConservatismLabel() {
    const labels = {
      conservative: '🟢 保守（尽量保留现有代码）',
      balanced: '🟡 平衡（适度修改）',
      aggressive: '🔴 激进（大胆重构）'
    };
    return labels[this.conservatism] || this.conservatism;
  }

  getConservatismInstruction() {
    const instructions = {
      conservative: '保守策略：尽量保留现有代码，只在必要时修改',
      balanced: '平衡策略：适度修改，在保留和重构之间取得平衡',
      aggressive: '激进策略：大胆重构，如果更好的设计就果断修改'
    };
    return instructions[this.conservatism] || instructions.balanced;
  }

  getChangeTypeLabel(type) {
    const labels = {
      incremental: '🟢 增量更新',
      major: '🟡 重大更新',
      rewrite: '🔴 完全重写'
    };
    return labels[type] || type;
  }

  getEffortLabel(effort) {
    const labels = { low: '低（快速）', medium: '中（正常）', high: '高（耗时）' };
    return labels[effort] || effort;
  }

  formatConfirmationMessage(plan) {
    let message = '📋 **增量更新计划 v3.0**\n\n';
    message += `**更新类型**: ${this.getChangeTypeLabel(plan.changeType)}\n`;
    message += `**置信度**: ${Math.round(plan.updateStrategy.confidence * 100)}%\n\n`;

    if (plan.userIntent) {
      message += `**用户意图**: ${plan.userIntent.description}\n\n`;
    }

    message += '**需求变化**:\n';
    if (plan.requirementChanges.added?.length > 0) {
      message += `➕ 新增：${plan.requirementChanges.added.join(', ')}\n`;
    }
    if (plan.requirementChanges.modified?.length > 0) {
      plan.requirementChanges.modified.forEach(m => {
        message += `🔄 修改：${m.from} → ${m.to} (${m.impact})\n`;
      });
    }

    message += '\n**文件变更**:\n';
    if (plan.fileChanges.add?.length > 0) {
      message += `➕ 新增文件 (${plan.fileChanges.add.length}):\n`;
      plan.fileChanges.add.forEach(f => message += `  - ${f.file}\n`);
    }
    if (plan.fileChanges.modify?.length > 0) {
      message += `✏️  修改文件 (${plan.fileChanges.modify.length}):\n`;
      plan.fileChanges.modify.forEach(f => message += `  - ${f.file}\n`);
    }
    if (plan.fileChanges.keep?.length > 0) {
      message += `✅ 保持不变 (${plan.fileChanges.keep.length})\n`;
    }

    message += `\n**预计工作量**: ${this.getEffortLabel(plan.updateStrategy.estimatedEffort)}\n`;
    message += '\n---\n';
    message += '确认开始更新？[确认] [修改计划]';

    return message;
  }
}

// 导出
module.exports = { IncrementalUpdater };
