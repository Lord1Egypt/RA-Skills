/**
 * Workflow Engine - SOP/DAG 混合工作流引擎 v1.0
 * 
 * 整合 MetaGPT 的工作流设计，支持：
 * - SOP（顺序执行）
 * - DAG（并行执行）
 * - 混合模式
 * 
 * Usage:
 *     import { Workflow, WorkflowEngine } from './system/workflow_engine.js';
 *     
 *     const workflow = new Workflow("software-dev", "hybrid");
 *     workflow.addStep({ id: "pm", agentId: "pm", action: "analyze" });
 *     workflow.addStep({ id: "dev", agentId: "dev", action: "code", dependsOn: ["pm"] });
 *     
 *     const engine = new WorkflowEngine(agents);
 *     const result = await engine.run(workflow, initialContext);
 */

// ============================================================
// Enums
// ============================================================

export const StepStatus = {
  PENDING: 'pending',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
  SKIPPED: 'skipped',
};

export const WorkflowType = {
  SOP: 'sop',           // 顺序执行
  DAG: 'dag',           // 并行执行
  HYBRID: 'hybrid',     // 混合模式
};

// ============================================================
// Step
// ============================================================

export class Step {
  constructor({
    id,
    agentId,
    action,
    dependsOn = [],
    outputKey = null,
    condition = null,
    retry = 0,
    timeout = 300,
  }) {
    this.id = id;
    this.agentId = agentId;
    this.action = action;
    this.dependsOn = dependsOn;
    this.outputKey = outputKey;
    this.condition = condition;
    this.retry = retry;
    this.timeout = timeout;
    this.status = StepStatus.PENDING;
    this.result = null;
    this.error = null;
    this.startTime = null;
    this.endTime = null;
  }

  toJSON() {
    return {
      id: this.id,
      agentId: this.agentId,
      action: this.action,
      dependsOn: this.dependsOn,
      outputKey: this.outputKey,
      condition: this.condition,
      status: this.status,
    };
  }
}

// ============================================================
// Workflow
// ============================================================

export class Workflow {
  constructor(name, type = WorkflowType.HYBRID) {
    this.name = name;
    this.type = type;
    /** @type {Map<string, Step>} */
    this.steps = new Map();
    this.stepOrder = [];
  }

  /**
   * Add a step to the workflow
   * @param {Object} config
   * @returns {Workflow}
   */
  addStep(config) {
    const step = new Step({
      id: config.id,
      agentId: config.agentId,
      action: config.action,
      dependsOn: config.dependsOn || [],
      outputKey: config.outputKey || null,
      condition: config.condition || null,
      retry: config.retry || 0,
      timeout: config.timeout || 300,
    });

    this.steps.set(step.id, step);
    this.stepOrder.push(step.id);
    return this;
  }

  /**
   * Get dependencies for a step
   * @param {string} stepId
   * @returns {string[]}
   */
  getDependencies(stepId) {
    const step = this.steps.get(stepId);
    return step ? step.dependsOn : [];
  }

  /**
   * Get steps that depend on this step
   * @param {string} stepId
   * @returns {string[]}
   */
  getDependents(stepId) {
    const dependents = [];
    for (const step of this.steps.values()) {
      if (step.dependsOn.includes(stepId)) {
        dependents.push(step.id);
      }
    }
    return dependents;
  }

  /**
   * Topological sort, returns levels that can run in parallel
   * @returns {string[][]}
   */
  topologicalSort() {
    const inDegree = new Map();
    for (const stepId of this.steps.keys()) {
      inDegree.set(stepId, 0);
    }

    // Calculate in-degrees
    for (const step of this.steps.values()) {
      for (const dep of step.dependsOn) {
        if (this.steps.has(dep)) {
          inDegree.set(step.id, (inDegree.get(step.id) || 0) + 1);
        }
      }
    }

    // Level-based sorting
    /** @type {string[][]} */
    const levels = [];
    const remaining = new Set(this.steps.keys());

    while (remaining.size > 0) {
      // Find steps with in-degree 0
      const ready = [...remaining].filter(s => (inDegree.get(s) || 0) === 0);

      if (ready.length === 0) {
        // Cycle detected
        throw new Error(`工作流存在循环依赖: ${[...remaining].join(', ')}`);
      }

      levels.push(ready);

      // Remove executed steps and update in-degrees
      for (const stepId of ready) {
        remaining.delete(stepId);
        for (const dependent of this.getDependents(stepId)) {
          if (remaining.has(dependent)) {
            inDegree.set(dependent, (inDegree.get(dependent) || 0) - 1);
          }
        }
      }
    }

    return levels;
  }

  toJSON() {
    const stepsObj = {};
    for (const [id, step] of this.steps) {
      stepsObj[id] = step.toJSON();
    }
    return {
      name: this.name,
      type: this.type,
      steps: stepsObj,
    };
  }

  /**
   * Create workflow from JSON
   * @param {Object} data
   * @returns {Workflow}
   */
  static fromJSON(data) {
    const workflow = new Workflow(data.name, data.type || WorkflowType.HYBRID);
    for (const [stepId, stepData] of Object.entries(data.steps || {})) {
      workflow.addStep({
        id: stepId,
        agentId: stepData.agentId,
        action: stepData.action,
        dependsOn: stepData.dependsOn || [],
        outputKey: stepData.outputKey || null,
        condition: stepData.condition || null,
      });
    }
    return workflow;
  }
}

// ============================================================
// Environment
// ============================================================

export class Environment {
  constructor() {
    /** @type {Map<string, any>} */
    this.context = new Map();
    /** @type {Object[]} */
    this.history = [];
    /** @type {Map<string, {content: any, type: string, createdAt: string}>} */
    this.artifacts = new Map();
    this._lock = null; // Would use AsyncLock in production
  }

  /**
   * Put a value into context
   * @param {string} key
   * @param {any} value
   * @param {string} producer
   */
  put(key, value, producer = null) {
    this.context.set(key, value);
    this.history.push({
      action: 'put',
      key,
      producer,
      timestamp: new Date().toISOString(),
    });
  }

  /**
   * Get a value from context
   * @param {string} key
   * @param {any} defaultValue
   * @returns {any}
   */
  get(key, defaultValue = undefined) {
    return this.context.has(key) ? this.context.get(key) : defaultValue;
  }

  /**
   * Get all context
   * @returns {Object}
   */
  getAll() {
    return Object.fromEntries(this.context);
  }

  /**
   * Add an artifact
   * @param {string} name
   * @param {any} content
   * @param {string} artifactType
   */
  addArtifact(name, content, artifactType) {
    this.artifacts.set(name, {
      content,
      type: artifactType,
      createdAt: new Date().toISOString(),
    });
  }

  /**
   * Get an artifact
   * @param {string} name
   * @returns {Object|null}
   */
  getArtifact(name) {
    return this.artifacts.get(name) || null;
  }

  /**
   * Publish a message (for agent communication)
   * @param {string} topic
   * @param {Object} message
   * @param {string} sender
   */
  publish(topic, message, sender) {
    this.history.push({
      action: 'publish',
      topic,
      message,
      sender,
      timestamp: new Date().toISOString(),
    });
  }

  toJSON() {
    return {
      context: Object.fromEntries(this.context),
      artifacts: Object.fromEntries(this.artifacts),
      history: this.history,
    };
  }
}

// ============================================================
// Workflow Engine
// ============================================================

export class WorkflowEngine {
  /**
   * @param {Map<string, any>|Object} agents - Agent instances
   * @param {number} maxWorkers - Max parallel workers
   */
  constructor(agents = {}, maxWorkers = 4) {
    this.agents = agents instanceof Map ? agents : new Map(Object.entries(agents));
    this.maxWorkers = maxWorkers;
    this.env = new Environment();
    /** @type {Object[]} */
    this.executionLog = [];
  }

  /**
   * Run a workflow
   * @param {Workflow} workflow
   * @param {Object} initialContext
   * @param {Function} onStepComplete
   * @returns {Promise<Object>}
   */
  async run(workflow, initialContext = null, onStepComplete = null) {
    // Initialize environment
    if (initialContext) {
      for (const [k, v] of Object.entries(initialContext)) {
        this.env.put(k, v, 'init');
      }
    }

    // Get execution levels
    let levels;
    try {
      levels = workflow.topologicalSort();
    } catch (e) {
      return {
        workflow: workflow.name,
        status: 'error',
        error: e.message,
        totalSteps: workflow.steps.size,
        completed: 0,
        failed: 0,
      };
    }

    let totalSteps = workflow.steps.size;
    let completed = 0;
    let failed = 0;

    console.log(`\n🚀 工作流启动: ${workflow.name}`);
    console.log(`📊 总步骤: ${totalSteps}, 并行层级: ${levels.length}\n`);

    // Execute level by level
    for (let levelIdx = 0; levelIdx < levels.length; levelIdx++) {
      const level = levels[levelIdx];
      console.log(`📍 层级 ${levelIdx + 1}: ${level.join(', ')}`);

      if (level.length === 1 || workflow.type === WorkflowType.SOP) {
        // Sequential execution
        for (const stepId of level) {
          const result = await this._executeStep(workflow.steps.get(stepId), onStepComplete);
          if (result.status === 'completed') {
            completed++;
          } else {
            failed++;
            if (workflow.type === WorkflowType.SOP) {
              // Stop on first failure in SOP mode
              break;
            }
          }
        }
      } else {
        // Parallel execution
        const batchSize = Math.min(level.length, this.maxWorkers);
        const batches = [];

        for (let i = 0; i < level.length; i += batchSize) {
          batches.push(level.slice(i, i + batchSize));
        }

        for (const batch of batches) {
          const promises = batch.map(stepId =>
            this._executeStep(workflow.steps.get(stepId), onStepComplete)
          );
          const results = await Promise.all(promises);

          for (const result of results) {
            if (result.status === 'completed') {
              completed++;
            } else {
              failed++;
            }
          }
        }
      }
    }

    // Generate report
    const report = {
      workflow: workflow.name,
      status: failed === 0 ? 'completed' : 'partial',
      totalSteps,
      completed,
      failed,
      environment: this.env.toJSON(),
      executionLog: this.executionLog,
    };

    console.log(`\n✅ 工作流完成: ${completed}/${totalSteps} 成功`);

    return report;
  }

  /**
   * Execute a single step
   * @param {Step} step
   * @param {Function} callback
   * @returns {Promise<Object>}
   */
  async _executeStep(step, callback = null) {
    console.log(`  ▶️  ${step.id} (${step.agentId}.${step.action})`);

    step.status = StepStatus.RUNNING;
    step.startTime = new Date();

    try {
      // Get agent
      const agent = this.agents.get(step.agentId);
      if (!agent) {
        throw new Error(`Agent not found: ${step.agentId}`);
      }

      // Build execution context
      const context = this.env.getAll();

      // Execute agent action
      let result;
      if (typeof agent[step.action] === 'function') {
        result = await agent[step.action](context);
      } else if (typeof agent === 'function') {
        result = await agent(step.action, context);
      } else {
        throw new Error(`Agent ${step.agentId} 无法执行 ${step.action}`);
      }

      // Store result
      if (step.outputKey) {
        this.env.put(step.outputKey, result, step.agentId);
      }

      step.result = result;
      step.status = StepStatus.COMPLETED;
      step.endTime = new Date();

      const duration = (step.endTime - step.startTime) / 1000;

      // Log execution
      this.executionLog.push({
        stepId: step.id,
        agentId: step.agentId,
        action: step.action,
        status: 'completed',
        duration,
        outputKey: step.outputKey,
      });

      console.log(`  ✅ ${step.id} 完成 (${duration.toFixed(2)}s)`);

      // Callback
      if (callback) {
        callback(step, result);
      }

      return { status: 'completed', result };
    } catch (e) {
      step.status = StepStatus.FAILED;
      step.error = e.message;
      step.endTime = new Date();

      const duration = (step.endTime - step.startTime) / 1000;

      this.executionLog.push({
        stepId: step.id,
        agentId: step.agentId,
        action: step.action,
        status: 'failed',
        error: e.message,
        duration,
      });

      console.log(`  ❌ ${step.id} 失败: ${e.message}`);

      // Retry
      if (step.retry > 0) {
        console.log(`  🔄 重试 ${step.id}...`);
        step.retry--;
        step.status = StepStatus.PENDING;
        return this._executeStep(step, callback);
      }

      return { status: 'failed', error: e.message };
    }
  }
}

// ============================================================
// Workflow Templates
// ============================================================

/**
 * Create a software development workflow
 * @returns {Workflow}
 */
export function createSoftwareDevWorkflow() {
  const workflow = new Workflow('software-development', WorkflowType.HYBRID);

  // PM analyzes requirements
  workflow.addStep({
    id: 'pm_analyze',
    agentId: 'pm',
    action: 'analyzeRequirements',
    outputKey: 'requirements',
  });

  // Architect designs system
  workflow.addStep({
    id: 'architect_design',
    agentId: 'architect',
    action: 'designSystem',
    dependsOn: ['pm_analyze'],
    outputKey: 'design',
  });

  // Frontend and backend develop in parallel
  workflow.addStep({
    id: 'frontend_code',
    agentId: 'frontend_engineer',
    action: 'implement',
    dependsOn: ['architect_design'],
    outputKey: 'frontend_code',
  });

  workflow.addStep({
    id: 'backend_code',
    agentId: 'backend_engineer',
    action: 'implement',
    dependsOn: ['architect_design'],
    outputKey: 'backend_code',
  });

  // QA tests
  workflow.addStep({
    id: 'qa_test',
    agentId: 'qa',
    action: 'test',
    dependsOn: ['frontend_code', 'backend_code'],
    outputKey: 'test_report',
  });

  // DevOps deploys
  workflow.addStep({
    id: 'deploy',
    agentId: 'devops',
    action: 'deploy',
    dependsOn: ['qa_test'],
    outputKey: 'deployment',
  });

  return workflow;
}

/**
 * Create a research workflow
 * @returns {Workflow}
 */
export function createResearchWorkflow() {
  const workflow = new Workflow('research', WorkflowType.DAG);

  // Data collection (parallel)
  workflow.addStep({
    id: 'collect_web',
    agentId: 'researcher',
    action: 'collectWebData',
    outputKey: 'web_data',
  });

  workflow.addStep({
    id: 'collect_api',
    agentId: 'researcher',
    action: 'collectApiData',
    outputKey: 'api_data',
  });

  // Data analysis (waits for collection)
  workflow.addStep({
    id: 'analyze',
    agentId: 'analyst',
    action: 'analyze',
    dependsOn: ['collect_web', 'collect_api'],
    outputKey: 'analysis',
  });

  // Generate report
  workflow.addStep({
    id: 'report',
    agentId: 'pm',
    action: 'writeReport',
    dependsOn: ['analyze'],
    outputKey: 'report',
  });

  return workflow;
}

/**
 * Create a code review workflow
 * @returns {Workflow}
 */
export function createCodeReviewWorkflow() {
  const workflow = new Workflow('code-review', WorkflowType.SOP);

  workflow.addStep({
    id: 'check_style',
    agentId: 'qa',
    action: 'checkCodeStyle',
    outputKey: 'style_report',
  });

  workflow.addStep({
    id: 'security_scan',
    agentId: 'security',
    action: 'scanSecurity',
    dependsOn: ['check_style'],
    outputKey: 'security_report',
  });

  workflow.addStep({
    id: 'review',
    agentId: 'architect',
    action: 'reviewCode',
    dependsOn: ['security_scan'],
    outputKey: 'review_comments',
  });

  return workflow;
}

// ============================================================
// CLI
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'demo';

  if (command === 'list') {
    console.log('可用工作流模板:');
    console.log('  - software-development (软件开发)');
    console.log('  - research (研究分析)');
    console.log('  - code-review (代码审查)');
    return;
  }

  if (command === 'demo') {
    // Mock agents
    const agents = new Map([
      ['pm', {
        name: '产品经理',
        analyzeRequirements: async (ctx) => {
          console.log('    [产品经理] 分析需求中...');
          return { features: ['用户登录', '数据管理'] };
        },
        writeReport: async (ctx) => {
          console.log('    [产品经理] 写报告中...');
          return { report: '分析报告已完成' };
        },
      }],
      ['architect', {
        name: '架构师',
        designSystem: async (ctx) => {
          console.log('    [架构师] 设计架构中...');
          return { architecture: '微服务', tech_stack: 'Python + FastAPI' };
        },
        reviewCode: async (ctx) => {
          console.log('    [架构师] 审查代码中...');
          return { comments: ['建议优化数据库查询', '添加缓存'] };
        },
      }],
      ['frontend_engineer', {
        name: '前端工程师',
        implement: async (ctx) => {
          console.log('    [前端工程师] 编写代码中...');
          return { files: ['main.py', 'api.py'] };
        },
      }],
      ['backend_engineer', {
        name: '后端工程师',
        implement: async (ctx) => {
          console.log('    [后端工程师] 编写代码中...');
          return { files: ['main.py', 'api.py'] };
        },
      }],
      ['qa', {
        name: 'QA',
        test: async (ctx) => {
          console.log('    [QA] 测试中...');
          return { passed: 10, failed: 0 };
        },
        checkCodeStyle: async (ctx) => {
          console.log('    [QA] 检查代码风格中...');
          return { style: 'ok' };
        },
      }],
      ['devops', {
        name: 'DevOps',
        deploy: async (ctx) => {
          console.log('    [DevOps] 部署中...');
          return { url: 'https://api.example.com' };
        },
      }],
    ]);

    // Create and run workflow
    const workflow = createSoftwareDevWorkflow();
    const engine = new WorkflowEngine(agents);
    const result = await engine.run(workflow, { project: 'Demo Project' });

    console.log('\n📦 最终产物:');
    for (const [key, value] of Object.entries(result.environment.context)) {
      console.log(`  - ${key}: ${JSON.stringify(value)}`);
    }
  }
}

const isMain = process.argv[1]?.endsWith('workflow_engine.js') || process.argv[1]?.endsWith('workflow_engine.mjs');
if (isMain) {
  main().catch(console.error);
}

export default {
  Workflow,
  WorkflowEngine,
  Environment,
  Step,
  StepStatus,
  WorkflowType,
  createSoftwareDevWorkflow,
  createResearchWorkflow,
  createCodeReviewWorkflow,
};
