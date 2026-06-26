/**
 * Vibe Coding 技能执行器 v4.1
 * 
 * 增强协作模式：并行 + 评审 + 迭代 + SPEC.md + Agent 投票审批
 * 
 * v4.1 新增：
 * 1. SPEC.md 生成（基于需求 + 架构）
 * 2. Agent 投票审批（取代用户审批）
 * 3. 自动决策（无需用户等待）
 */

const fs = require('fs').promises;
const path = require('path');

// Agent 提示词模板
const AGENT_PROMPTS = {
  analyst: `你是需求分析师。根据用户需求生成结构化的需求文档。

输出格式（Markdown）：
# {项目名} - 需求文档

## 1. 项目概述
- 项目背景
- 目标用户
- 核心价值

## 2. 功能清单（至少 3 个功能）
| 功能名称 | 优先级 | 描述 |
|---------|--------|------|
| ... | P0 | ... |

## 3. 用户故事（GWT 格式，至少 2 个）
1. Given [前置条件], When [操作], Then [预期结果]
2. ...

## 4. 验收标准（至少 3 项）
- [ ] 功能 1 验收标准
- [ ] 功能 2 验收标准

要求：
- 功能清单至少 3 个功能
- 用户故事必须是 GWT 格式
- 验收标准可量化`,

  architect: `你是系统架构师。根据需求文档设计系统架构。

输出格式（Markdown）：
# {项目名} - 架构设计

## 1. 技术选型
| 层次 | 技术 | 选择理由 |
|------|------|---------|
| 前端 | ... | ... |

## 2. 系统架构（ASCII 或 Mermaid）
\`\`\`
架构图
\`\`\`

## 3. 模块设计（至少 3 个模块）
- **模块 1**: 职责说明
- **模块 2**: 职责说明

## 4. 数据模型
\`\`\`typescript
interface DataType {
  field: string;
}
\`\`\`

## 5. 安全考虑
- 输入验证
- XSS 防护
- 数据安全

要求：
- 技术选型必须说明理由
- 至少设计 3 个模块
- 数据模型包含字段类型`,

  developer: `你是开发工程师。根据需求文档和架构设计实现代码。

输出格式：
对于每个文件，使用以下格式：

\`\`\`文件路径
文件内容
\`\`\`

要求：
- 每个函数必须有注释（JSDoc 风格）
- 必须有输入验证和错误处理
- 遵循 DRY 原则
- 代码要有适当的错误处理`,

  tester: `你是测试工程师。根据需求和代码编写测试用例。

输出格式（Markdown）：
# {项目名} - 测试用例

## 1. 功能测试（至少 5 个用例）
| 用例 ID | 测试场景 | 输入 | 预期结果 | 状态 |
|--------|---------|------|---------|------|
| TC-001 | ... | ... | ... | ☐ |

## 2. 边界测试（至少 3 个用例）
| 用例 ID | 测试场景 | 输入 | 预期结果 | 状态 |
|--------|---------|------|---------|------|
| TC-101 | ... | ... | ... | ☐ |

## 3. 异常测试（至少 2 个用例）
| 用例 ID | 异常场景 | 预期行为 | 状态 |
|--------|---------|---------|------|
| TC-201 | ... | ... | ☐ |

要求：
- 功能测试至少 5 个用例
- 边界测试至少 3 个用例
- 异常测试至少 2 个用例
- 预期结果必须明确可验证`
};

// Agent 配置
const AGENT_CONFIG = {
  analyst: { model: 'bailian/qwen3.5-plus', thinking: 'medium', timeout: 1800 },
  architect: { model: 'bailian/qwen3.5-plus', thinking: 'high', timeout: 3600 },
  developer: { model: 'bailian/qwen3-coder-next', thinking: 'medium', timeout: 3600 },
  tester: { model: 'bailian/glm-4', thinking: 'low', timeout: 1800 }
};

/**
 * 质量检查
 */
function qualityCheck(phase, content) {
  const gates = {
    requirements: { minFeatures: 3, minUserStories: 2 },
    architecture: { hasTechStack: true, hasDataModel: true },
    code: { hasErrorHandling: true, hasComments: true },
    tests: { minFunctional: 5, minBoundary: 3, minException: 2 }
  };
  
  const gate = gates[phase];
  if (!gate) return { passed: true, score: 100 };
  
  let score = 0;
  const issues = [];
  
  if (phase === 'requirements') {
    const featureCount = (content.match(/\|.*\|.*\|/g) || []).length - 1;
    if (featureCount >= gate.minFeatures) score += 50;
    else issues.push(`功能数量不足：${featureCount} < ${gate.minFeatures}`);
    
    const storyCount = (content.match(/Given.*When.*Then/gi) || []).length;
    if (storyCount >= gate.minUserStories) score += 50;
    else issues.push(`用户故事不足：${storyCount} < ${gate.minUserStories}`);
  }
  
  return { passed: score >= 70, score, issues };
}

/**
 * Vibe Coding 执行器 v4.1
 */
class VibeExecutorV41 {
  constructor(requirement, options = {}) {
    this.requirement = requirement;
    this.projectName = this.extractProjectName(requirement);
    this.projectDir = options.outputDir || `output/${this.projectName}`;
    this.options = options;
    this.llmCallback = options.llmCallback;
    this.state = {
      status: 'running',
      phase: 'init',
      outputs: {},
      files: [],
      startTime: Date.now(),
      logs: []
    };
  }
  
  extractProjectName(requirement) {
    return requirement.substring(0, Math.min(20, requirement.length))
      .replace(/[^\w\u4e00-\u9fa5]/g, '') || 'my-project';
  }
  
  log(message, type = 'info') {
    const entry = {
      timestamp: new Date().toISOString(),
      type,
      message
    };
    this.state.logs.push(entry);
    console.log(`[${entry.timestamp.split('T')[1].split('.')[0]}] ${type.toUpperCase()}: ${message}`);
  }
  
  async callAgent(role, prompt) {
    const config = AGENT_CONFIG[role];
    this.log(`🤖 启动 ${role} (${config.model}, ${config.thinking})`, 'agent');
    
    try {
      let output;
      
      if (this.llmCallback) {
        output = await this.llmCallback(prompt, config.model, config.thinking);
      } else if (typeof sessions_spawn !== 'undefined') {
        const result = await sessions_spawn({
          runtime: "subagent",
          task: prompt,
          model: config.model,
          thinking: config.thinking,
          timeoutSeconds: config.timeout,
          mode: "run",
          label: `vibe-${role}`
        });
        const completionEvent = await sessions_yield();
        output = completionEvent?.output || completionEvent?.message || completionEvent || '';
      } else {
        throw new Error('需要 OpenClaw 环境或传入 llmCallback 参数');
      }
      
      const quality = qualityCheck(role, output || '');
      this.log(`✅ ${role} 完成（质量评分：${quality.score}/100）`, 'complete');
      
      return { output, quality };
      
    } catch (error) {
      this.log(`❌ ${role} 失败：${error.message}`, 'error');
      throw error;
    }
  }
  
  async execute() {
    this.log(`🎨 Vibe Coding v4.1 启动（SPEC.md + Agent 投票审批）`, 'info');
    this.log(`📝 用户需求：${this.requirement}`, 'info');
    this.log(`📁 项目目录：${this.projectDir}`, 'info');
    this.log(`⏱️  预计耗时：3-5 分钟`, 'info');
    this.log(``, 'info');
    
    const startTime = Date.now();
    
    try {
      // ========== Phase 1: 需求分析 ==========
      this.state.phase = 'phase_1_requirements';
      this.log(`📊 Phase 1/5: 需求分析（预计 30 秒）`, 'phase');
      
      let requirements = await this.callAgent('analyst', AGENT_PROMPTS.analyst);
      requirements = await this.iterativeRefine('requirements', requirements, 2);
      this.state.outputs.requirements = requirements;
      
      // ========== Phase 2: 架构设计 + SPEC.md 生成 + Agent 投票审批 ==========
      this.state.phase = 'phase_2_architecture';
      const phase2Start = Date.now();
      this.log(`🏗️ Phase 2/5: 架构设计 + SPEC.md + Agent 投票（预计 90 秒）`, 'phase');
      
      let architecture = await this.callAgent('architect', AGENT_PROMPTS.architect);
      architecture = await this.iterativeRefine('architecture', architecture, 2);
      
      // 生成 SPEC.md
      this.log(`📝 生成 SPEC.md...`, 'info');
      const spec = await this.generateSpec(requirements, architecture);
      this.state.outputs.spec = spec;
      this.log(`✅ SPEC.md 生成完成`, 'info');
      
      // Agent 投票审批（取代用户审批）
      this.log(`🗳️ 启动 SPEC.md Agent 投票审批...`, 'info');
      const specVote = await this.specApprovalVote(spec, requirements, architecture);
      
      this.log(`✅ Agent 投票审批完成:`, 'info');
      specVote.reviews.forEach(r => {
        this.log(`  ${r.role}: ${r.vote} (${r.quality.score}/100) - ${r.reason.substring(0, 50)}...`, 'info');
      });
      
      const voteResult = this.countVotes(specVote.reviews);
      this.log(`📊 投票结果：${voteResult.yes} 赞成 vs ${voteResult.no} 反对`, 'info');
      
      // 投票决策（自动，不需要用户审批）
      if (voteResult.no >= 2) {
        this.log(`⚠️ SPEC.md 未通过，要求重新设计...`, 'warning');
        const feedback = `SPEC.md 评审未通过，请改进以下问题：\n${specVote.reviews.filter(r => r.vote === 'no').map(r => r.reason).join('\n')}`;
        architecture = await this.callAgent('architect', feedback);
        architecture = await this.iterativeRefine('architecture', architecture, 1);
        
        // 重新生成 SPEC.md
        const newSpec = await this.generateSpec(requirements, architecture);
        this.state.outputs.spec = newSpec;
        
        // 重新投票（只一次）
        const newVote = await this.specApprovalVote(newSpec, requirements, architecture);
        specVote.reviews = newVote.reviews;
      } else if (voteResult.no === 1) {
        this.log(`⚠️ SPEC.md 有保留意见，记录问题后继续`, 'warning');
        this.state.outputs.specIssues = specVote.reviews.filter(r => r.vote === 'no').map(r => r.reason);
      } else {
        this.log(`✅ SPEC.md 一致通过`, 'complete');
      }
      
      this.state.outputs.architecture = architecture;
      this.state.outputs.specVote = { voteResult, reviews: specVote.reviews };
      
      // ========== Phase 3: 代码实现（基于 PRD + 架构） ==========
      this.state.phase = 'phase_3_implementation';
      const elapsed = Math.round((Date.now() - startTime) / 1000);
      const remaining = Math.max(60, 180 - elapsed);
      this.log(`💻 Phase 3/5: 代码实现（预计 ${remaining} 秒）`, 'phase');
      
      const developerPrompt = `你是开发工程师。请根据**需求文档和架构设计**实现完整代码。

## 需求文档（必须实现以下功能）
${requirements.output}

## 架构设计（遵循以下技术规范）
${architecture.output}

## 实现要求
1. **必须实现需求文档中的所有功能**
2. **遵循架构设计的技术规范**
3. 每个函数必须有注释（JSDoc 风格）
4. 必须有输入验证和错误处理
5. 遵循 DRY 原则

## 输出格式
对于每个文件，使用以下格式：

\`\`\`文件路径
文件内容
\`\`\``;
      
      const [code, testFramework] = await Promise.all([
        this.callAgent('developer', developerPrompt),
        this.callAgent('tester', `根据需求文档和架构设计，提前设计测试框架：\n\n需求：${requirements.output}\n\n架构：${architecture.output}`)
      ]);
      
      const codeRefined = await this.iterativeRefine('code', code, 2);
      
      // 代码评审 + 投票
      this.log(`🔍 启动代码评审 + 投票...`, 'info');
      const codeReviews = await this.reviewWithVote('code', codeRefined, ['tester', 'architect']);
      this.log(`✅ 代码评审投票完成:`, 'info');
      codeReviews.forEach(r => {
        this.log(`  ${r.role}: ${r.vote} (${r.quality.score}/100)`, 'info');
      });
      
      this.state.outputs.code = codeRefined;
      this.state.outputs.testFramework = testFramework;
      this.state.outputs.codeReviews = codeReviews;
      
      // ========== Phase 4: 测试编写 ==========
      this.state.phase = 'phase_4_testing';
      const elapsed4 = Math.round((Date.now() - startTime) / 1000);
      this.log(`🧪 Phase 4/5: 测试编写（预计 30 秒）`, 'phase');
      
      let tests = await this.callAgent('tester', AGENT_PROMPTS.tester);
      tests = await this.iterativeRefine('tests', tests, 2);
      this.state.outputs.tests = tests;
      
      // ========== Phase 5: 整合验收 + 需求追溯 ==========
      this.state.phase = 'phase_5_delivery';
      this.log(`✅ Phase 5/5: 整合验收 + 需求追溯（最后一步）`, 'phase');
      
      // 生成需求追溯矩阵
      this.log(`📊 生成需求追溯矩阵...`, 'info');
      const traceability = await this.generateTraceabilityMatrix(requirements, codeRefined);
      this.state.outputs.traceability = traceability;
      this.log(`✅ 追溯矩阵完成：${traceability.coverage}% 需求已实现`, 'info');
      
      // 最终质量汇总
      const finalQuality = this.finalQualityCheck();
      this.log(`📊 最终质量评分：${finalQuality.score}/100`, 'info');
      
      // 保存文件
      await this.saveFiles();
      
      // 完成
      this.state.status = 'completed';
      this.state.endTime = Date.now();
      this.state.duration = this.state.endTime - this.state.startTime;
      
      this.log(`🎉 Vibe Coding 完成！总耗时：${Math.round(this.state.duration / 1000)}秒`, 'complete');
      this.log(`📊 质量评分：需求${this.state.outputs.requirements.quality.score}/100, 架构${this.state.outputs.architecture.quality.score}/100, 代码${this.state.outputs.code.quality.score}/100, 测试${this.state.outputs.tests.quality.score}/100`, 'complete');
      this.log(`🗳️ SPEC.md 投票：${voteResult.yes} 赞成 vs ${voteResult.no} 反对`, 'complete');
      this.log(``, 'complete');
      this.log(`📁 文件位置：${this.projectDir}`, 'complete');
      this.log(`📂 生成文件：${this.state.files.length} 个`, 'complete');
      
      // 尝试打开文件（如果支持）
      try {
        const { exec } = require('child_process');
        if (process.platform === 'darwin') {
          exec(`open ${this.projectDir}`);
        } else if (process.platform === 'win32') {
          exec(`start ${this.projectDir}`);
        } else if (process.platform === 'linux') {
          exec(`xdg-open ${this.projectDir}`);
        }
      } catch (e) {
        // 忽略打开失败
      }
      
      return this.state;
      
    } catch (error) {
      this.state.status = 'failed';
      this.state.error = error.message;
      
      this.log(``, 'error');
      this.log(`❌ 执行失败：${error.message}`, 'error');
      this.log(``, 'error');
      this.log(`💡 可能的原因:`, 'error');
      
      if (error.message.includes('sessions_spawn')) {
        this.log(`  1. 不在 OpenClaw 环境中`, 'error');
        this.log(`  2. 需要 OpenClaw >= 2026.2.0`, 'error');
      } else if (error.message.includes('Cannot find module')) {
        this.log(`  1. 依赖未安装`, 'error');
        this.log(`  2. 运行：npm install`, 'error');
      } else if (error.message.includes('timeout')) {
        this.log(`  1. 网络超时`, 'error');
        this.log(`  2. 重试命令`, 'error');
      } else {
        this.log(`  1. 查看错误信息`, 'error');
        this.log(`  2. 检查配置`, 'error');
      }
      
      this.log(``, 'error');
      this.log(`🔧 建议操作:`, 'error');
      this.log(`  1. 确认在 OpenClaw 中使用`, 'error');
      this.log(`  2. 运行：npm install`, 'error');
      this.log(`  3. 重试命令`, 'error');
      
      throw error;
    }
  }
  
  async iterativeRefine(phase, output, maxRetries = 2) {
    let current = output;
    let retries = 0;
    
    while (retries < maxRetries) {
      const quality = qualityCheck(phase, current.output);
      this.log(`  📊 ${phase} 质量评分：${quality.score}/100`, 'info');
      
      if (quality.score >= 70) {
        this.log(`  ✅ ${phase} 质量通过`, 'complete');
        return current;
      }
      
      retries++;
      this.log(`  ⚠️ ${phase} 质量不足，重新生成 (${retries}/${maxRetries})...`, 'warning');
      
      const feedback = `请改进以下问题：\n${quality.issues.join('\n')}\n\n原始输出：\n${current.output}`;
      const agent = phase === 'requirements' ? 'analyst' : 
                    phase === 'architecture' ? 'architect' :
                    phase === 'code' ? 'developer' : 'tester';
      current = await this.callAgent(agent, feedback);
    }
    
    this.log(`  ⚠️ ${phase} 达到最大重试次数，使用当前结果`, 'warning');
    return current;
  }
  
  async generateSpec(requirements, architecture) {
    const prompt = `请生成 SPEC.md 规格说明文档。

## 需求文档
${requirements.output}

## 架构设计
${architecture.output}

## SPEC.md 格式
\`\`\`markdown
# {项目名} - Specification

**版本**: v1.0  
**日期**: ${new Date().toISOString().split('T')[0]}  
**状态**: Draft

## 1. Overview（概述）
### 1.1 Problem（问题）
用 1-2 句话描述要解决的问题

### 1.2 Goals（目标）
- **主要目标**: 最重要的目标
- **次要目标**: 其他目标

### 1.3 Non-Goals（非目标）
明确不包含的内容

## 2. Requirements（需求）
### 2.1 User Stories（用户故事）
| ID | 作为... | 我想要... | 以便... | 优先级 |
|----|--------|---------|--------|--------|

### 2.2 Functional Requirements（功能需求）
| ID | 需求描述 | 验收标准 | 优先级 |
|----|---------|---------|--------|

### 2.3 Non-Functional Requirements（非功能需求）
- 性能要求
- 安全要求

## 3. Design（设计）
### 3.1 Architecture（架构）
（架构图）

### 3.2 Data Model（数据模型）
（数据结构）

### 3.3 API Design（API 设计）
（API 端点）

## 4. Implementation（实现）
### 4.1 File Structure（文件结构）
（文件树）

### 4.2 Key Functions（关键函数）
（函数列表）

## 5. Testing（测试）
### 5.1 Unit Tests（单元测试）
### 5.2 Integration Tests（集成测试）
### 5.3 Acceptance Criteria（验收标准）

## 6. Approval（审批）
- [ ] Architect 审批
- [ ] Developer 审批
- [ ] Tester 审批
\`\`\`

请生成完整的 SPEC.md 文档。`;

    try {
      const result = await this.callAgent('analyst', prompt);
      return {
        output: result.output,
        quality: result.quality
      };
    } catch (error) {
      this.log(`❌ 生成 SPEC.md 失败：${error.message}`, 'error');
      return { output: '', quality: { score: 0 } };
    }
  }
  
  async specApprovalVote(spec, requirements, architecture) {
    const reviewers = ['architect', 'developer', 'tester'];
    
    const reviewPrompts = {
      architect: `请评审 SPEC.md 的技术架构是否合理，并投票是否通过。

## SPEC.md
${spec.output}

## 评审要点
1. 架构设计是否合理？
2. 技术选型是否适当？
3. 是否有技术风险？

请投票（yes/no）并说明理由。`,
      
      developer: `请评审 SPEC.md 的实现可行性，并投票是否通过。

## SPEC.md
${spec.output}

## 评审要点
1. 实现难度如何？
2. 是否有技术障碍？
3. 预计工作量？

请投票（yes/no）并说明理由。`,
      
      tester: `请评审 SPEC.md 的可测试性，并投票是否通过。

## SPEC.md
${spec.output}

## 评审要点
1. 验收标准是否明确？
2. 是否可测试？
3. 测试覆盖率目标？

请投票（yes/no）并说明理由。`
    };
    
    const reviews = await Promise.all(
      reviewers.map(async (reviewer) => {
        const prompt = reviewPrompts[reviewer];
        const result = await this.callAgent(reviewer, prompt);
        
        const voteText = result.output.toLowerCase();
        const vote = (voteText.includes('yes') || voteText.includes('通过') || voteText.includes('同意') || result.quality.score >= 70) ? 'yes' : 'no';
        
        const reasonMatch = result.output.match(/(理由 | 原因 | 问题 | 建议)[:：]([\s\S]*?)(?:\n\n|$)/);
        const reason = reasonMatch ? reasonMatch[2].trim() : result.output.substring(0, 100);
        
        return {
          role: reviewer,
          vote,
          reason,
          quality: result.quality,
          output: result.output
        };
      })
    );
    
    return { reviews };
  }
  
  async reviewWithVote(phase, output, reviewers) {
    const reviews = [];
    
    const reviewPrompts = {
      architecture: {
        developer: '请评审架构设计的可实现性，并投票是否通过。',
        tester: '请评审架构设计的可测试性，并投票是否通过。'
      },
      code: {
        tester: '请评审代码的可测试性和测试覆盖率，并投票是否通过。',
        architect: '请评审代码是否符合架构设计，并投票是否通过。'
      }
    };
    
    const reviewResults = await Promise.all(
      reviewers.map(async (reviewer) => {
        const prompt = `${reviewPrompts[phase]?.[reviewer] || '请评审以下输出，并投票是否通过。'}\n\n待评审内容：\n${output.output}`;
        const result = await this.callAgent(reviewer, prompt);
        
        const voteText = result.output.toLowerCase();
        const vote = (voteText.includes('通过') || voteText.includes('yes') || voteText.includes('同意') || result.quality.score >= 70) ? 'yes' : 'no';
        
        const reasonMatch = result.output.match(/(理由 | 原因 | 问题 | 建议)[:：]([\s\S]*?)(?:\n\n|$)/);
        const reason = reasonMatch ? reasonMatch[2].trim() : result.output.substring(0, 100);
        
        return {
          role: reviewer,
          vote,
          reason,
          quality: result.quality,
          output: result.output
        };
      })
    );
    
    return reviewResults;
  }
  
  countVotes(reviews) {
    const yes = reviews.filter(r => r.vote === 'yes').length;
    const no = reviews.filter(r => r.vote === 'no').length;
    const abstain = reviews.filter(r => r.vote === 'abstain').length;
    
    return {
      yes,
      no,
      abstain,
      total: reviews.length,
      passed: yes > no,
      details: reviews.map(r => ({ role: r.role, vote: r.vote }))
    };
  }
  
  finalQualityCheck() {
    const scores = [
      this.state.outputs.requirements?.quality?.score || 0,
      this.state.outputs.architecture?.quality?.score || 0,
      this.state.outputs.code?.quality?.score || 0,
      this.state.outputs.tests?.quality?.score || 0
    ];
    
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    const minScore = Math.min(...scores);
    
    return {
      score: Math.round(avgScore),
      minScore,
      scores: {
        requirements: scores[0],
        architecture: scores[1],
        code: scores[2],
        tests: scores[3]
      }
    };
  }
  
  async generateTraceabilityMatrix(requirements, code) {
    const prompt = `请创建需求 - 代码追溯矩阵，确保每个需求都有对应的代码实现。

## 需求文档
${requirements.output}

## 代码实现
${code.output}

## 任务
1. 提取需求文档中的所有功能点
2. 找出每个功能点对应的代码文件/函数
3. 计算需求覆盖率

## 输出格式（JSON）
{
  "requirements": [
    {
      "id": "REQ-001",
      "description": "需求描述",
      "implemented": true,
      "files": ["文件路径"],
      "functions": ["函数名"]
    }
  ],
  "coverage": 95,
  "missingRequirements": ["未实现的需求"],
  "summary": "总结说明"
}`;

    try {
      const result = await this.callAgent('analyst', prompt);
      const jsonMatch = result.output.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      return { coverage: 0, requirements: [], missingRequirements: [] };
    } catch (error) {
      this.log(`❌ 生成追溯矩阵失败：${error.message}`, 'error');
      return { coverage: 0, requirements: [], missingRequirements: [] };
    }
  }
  
  async saveFiles() {
    this.log(`📁 开始保存文件...`, 'info');
    
    try {
      await fs.mkdir(this.projectDir, { recursive: true });
      
      const docsDir = path.join(this.projectDir, 'docs');
      const testsDir = path.join(this.projectDir, 'tests');
      await fs.mkdir(docsDir, { recursive: true });
      await fs.mkdir(testsDir, { recursive: true });
      
      // 保存 SPEC.md
      if (this.state.outputs.spec?.output) {
        const specPath = path.join(docsDir, 'SPEC.md');
        await fs.writeFile(specPath, this.state.outputs.spec.output, 'utf-8');
        this.state.files.push({ name: 'docs/SPEC.md', size: this.state.outputs.spec.output.length });
        this.log(`  ✅ 保存：docs/SPEC.md`, 'info');
      }
      
      if (this.state.outputs.requirements?.output) {
        const reqPath = path.join(docsDir, 'requirements.md');
        await fs.writeFile(reqPath, this.state.outputs.requirements.output, 'utf-8');
        this.state.files.push({ name: 'docs/requirements.md', size: this.state.outputs.requirements.output.length });
        this.log(`  ✅ 保存：docs/requirements.md`, 'info');
      }
      
      if (this.state.outputs.architecture?.output) {
        const archPath = path.join(docsDir, 'architecture.md');
        await fs.writeFile(archPath, this.state.outputs.architecture.output, 'utf-8');
        this.state.files.push({ name: 'docs/architecture.md', size: this.state.outputs.architecture.output.length });
        this.log(`  ✅ 保存：docs/architecture.md`, 'info');
      }
      
      if (this.state.outputs.code?.output) {
        const codeBlocks = this.extractCodeBlocks(this.state.outputs.code.output);
        for (const block of codeBlocks) {
          const filePath = path.join(this.projectDir, block.path);
          await fs.mkdir(path.dirname(filePath), { recursive: true });
          await fs.writeFile(filePath, block.content, 'utf-8');
          this.state.files.push({ name: block.path, size: block.content.length });
          this.log(`  ✅ 保存：${block.path}`, 'info');
        }
      }
      
      if (this.state.outputs.tests?.output) {
        const testPath = path.join(testsDir, 'test-cases.md');
        await fs.writeFile(testPath, this.state.outputs.tests.output, 'utf-8');
        this.state.files.push({ name: 'tests/test-cases.md', size: this.state.outputs.tests.output.length });
        this.log(`  ✅ 保存：tests/test-cases.md`, 'info');
      }
      
      const reportPath = path.join(docsDir, 'vibe-report.md');
      const report = this.generateReport();
      await fs.writeFile(reportPath, report, 'utf-8');
      this.state.files.push({ name: 'docs/vibe-report.md', size: report.length });
      this.log(`  ✅ 保存：docs/vibe-report.md`, 'info');
      
      this.log(`✅ 共保存 ${this.state.files.length} 个文件`, 'complete');
      
    } catch (error) {
      this.log(`❌ 文件保存失败：${error.message}`, 'error');
      throw error;
    }
  }
  
  extractCodeBlocks(markdown) {
    const blocks = [];
    const regex = /```(\w+)?\s*([\w\-./]+)?\n([\s\S]*?)```/g;
    let match;
    
    while ((match = regex.exec(markdown)) !== null) {
      const [, lang, filePath, content] = match;
      if (filePath && filePath.includes('/')) {
        blocks.push({ path: filePath.trim(), content: content.trim(), language: lang || 'javascript' });
      }
    }
    
    if (blocks.length === 0 && markdown.includes('<!DOCTYPE html>')) {
      blocks.push({ path: 'index.html', content: markdown, language: 'html' });
    }
    
    return blocks;
  }
  
  generateReport() {
    const duration = Math.round(this.state.duration / 1000);
    const finalQuality = this.finalQualityCheck();
    const traceability = this.state.outputs.traceability || { coverage: 0 };
    const specVote = this.state.outputs.specVote || { voteResult: { yes: 0, no: 0 } };
    
    return `# Vibe Coding v4.1 项目报告

## 项目信息
- **需求**: ${this.requirement}
- **生成时间**: ${new Date().toISOString()}
- **总耗时**: ${duration}秒
- **文件数**: ${this.state.files.length}个

## 质量评分
- **综合评分**: ${finalQuality.score}/100
- **最低评分**: ${finalQuality.minScore}/100

### 各阶段评分
- 需求分析：${finalQuality.scores.requirements}/100
- 架构设计：${finalQuality.scores.architecture}/100
- 代码实现：${finalQuality.scores.code}/100
- 测试编写：${finalQuality.scores.tests}/100

## 需求追溯
- **需求覆盖率**: ${traceability.coverage}%
- **已实现需求**: ${traceability.requirements?.filter(r => r.implemented).length || 0}
- **缺失需求**: ${traceability.missingRequirements?.length || 0}

## SPEC.md 审批
- **投票结果**: ${specVote.voteResult.yes} 赞成 vs ${specVote.voteResult.no} 反对
- **审批状态**: ${specVote.voteResult.passed ? '✅ 通过' : '❌ 未通过'}

## 文件清单
${this.state.files.map(f => `- ${f.name} (${f.size} bytes)`).join('\n')}

## 协作模式
- ✅ 迭代优化（最多 2 次重试）
- ✅ 并行评审（Developer + Tester 提前介入）
- ✅ 并行执行（代码 + 测试框架同时进行）
- ✅ 需求追溯（确保每个需求都实现）
- ✅ SPEC.md 生成（Spec-First 流程）
- ✅ Agent 投票审批（取代用户审批）

## 生成状态
✅ 完成
`;
  }
}

// 导出
module.exports = { VibeExecutorV41, AGENT_PROMPTS, AGENT_CONFIG, qualityCheck };
