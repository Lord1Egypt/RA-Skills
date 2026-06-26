/**
 * Agent - 统一入口（记忆系统 + 工作流引擎）
 * 
 * Usage:
 *   node agent.js "开发一个博客系统"
 *   node agent.js chat
 *   node agent.js history --task <task_id>
 */

import crypto from 'crypto';

// Try to import existing Node.js modules
let WorkflowEngine, RoleFactory;
try {
  const wfModule = await import('../system/workflow_engine.js').catch(() => null);
  const rolesModule = await import('./roles.js').catch(() => null);
  WorkflowEngine = wfModule?.WorkflowEngine;
  RoleFactory = rolesModule?.RoleFactory;
} catch (e) {
  // Modules not available
}

// ========== Role Factory (Standalone Fallback) ==========

const RoleType = {
  PM: 'pm',
  ARCHITECT: 'architect',
  ENGINEER: 'engineer',
  FRONTEND_ENGINEER: 'frontend',
  BACKEND_ENGINEER: 'backend',
  QA: 'qa',
  DEVOPS: 'devops',
  SECURITY: 'security',
  DATA_ENGINEER: 'data',
  DESIGNER: 'designer'
};

class Role {
  constructor(roleId, name, roleType, skills = []) {
    this.roleId = roleId;
    this.name = name;
    this.roleType = roleType;
    this.skills = skills;
    this.actions = {};
    this.inbox = [];
    this.outbox = [];
    this.context = {};
    this._initActions();
  }
  
  _initActions() {
    // Override in subclass
  }
  
  addAction(name, description, inputKeys = [], outputKey = '') {
    this.actions[name] = { name, description, inputKeys, outputKey };
  }
  
  canExecute(actionName) {
    return actionName in this.actions;
  }
  
  receive(message) {
    this.inbox.push(message);
  }
  
  send(receiver, content, msgType = 'action') {
    const msg = {
      sender: this.roleId,
      receiver,
      content,
      msgType,
      timestamp: new Date().toISOString()
    };
    this.outbox.push(msg);
    return msg;
  }
  
  toDict() {
    return {
      roleId: this.roleId,
      name: this.name,
      roleType: this.roleType,
      skills: this.skills,
      actions: Object.keys(this.actions)
    };
  }
}

class ProductManager extends Role {
  constructor(roleId = 'pm') {
    super(roleId, '产品经理', RoleType.PM, ['需求分析', '产品设计', '用户研究', '数据分析']);
  }
  
  _initActions() {
    this.addAction('analyze_requirements', '分析用户需求', ['user_input'], 'requirements');
    this.addAction('create_prd', '创建产品需求文档', ['requirements'], 'prd');
    this.addAction('prioritize_features', '功能优先级排序', ['features'], 'priority_list');
  }
  
  analyzeRequirements(context) {
    const userInput = context.user_input || context.project || '';
    
    const requirements = {
      raw_input: userInput,
      features: this._extractFeatures(userInput),
      constraints: this._extractConstraints(userInput),
      priority: /紧急|important/i.test(userInput) ? 'high' : 'normal'
    };
    
    return requirements;
  }
  
  _extractFeatures(text) {
    const features = [];
    const keywords = ['登录', '注册', '搜索', '支付', '管理', '分析', '导出', '导入'];
    for (const kw of keywords) {
      if (text.includes(kw)) features.push(kw);
    }
    if (!features.length) features.push('基础功能');
    return features;
  }
  
  _extractConstraints(text) {
    const constraints = [];
    if (/快速|fast/i.test(text)) constraints.push('性能优先');
    if (/安全|secure/i.test(text)) constraints.push('安全优先');
    return constraints;
  }
  
  createPRD(context) {
    const requirements = context.requirements || context;
    
    return {
      title: `${requirements.raw_input || '项目'} 产品需求文档`,
      features: requirements.features || [],
      constraints: requirements.constraints || [],
      created_at: new Date().toISOString(),
      sections: ['背景与目标', '用户画像', '功能列表', '非功能需求', '验收标准']
    };
  }
}

class Architect extends Role {
  constructor(roleId = 'architect') {
    super(roleId, '架构师', RoleType.ARCHITECT, ['架构设计', '系统设计', '技术选型', '性能优化']);
  }
  
  _initActions() {
    this.addAction('design_system', '设计系统架构', ['requirements'], 'design');
    this.addAction('select_tech_stack', '技术选型', ['requirements', 'constraints'], 'tech_stack');
    this.addAction('review_architecture', '架构评审', ['design'], 'review_comments');
  }
  
  designSystem(context) {
    const requirements = context.requirements || context;
    const features = requirements.features || [];
    
    let architecture;
    if (features.length > 5 || JSON.stringify(requirements).includes('微服务')) {
      architecture = 'microservices';
    } else if (features.length > 2) {
      architecture = 'modular_monolith';
    } else {
      architecture = 'simple';
    }
    
    return {
      architecture,
      components: this._designComponents(features),
      tech_stack: this._recommendStack(architecture),
      diagrams: ['系统架构图', '数据流图', '部署图'],
      created_at: new Date().toISOString()
    };
  }
  
  _designComponents(features) {
    return features.map(feat => ({
      name: feat,
      type: ['支付', '搜索'].includes(feat) ? 'service' : 'module',
      dependencies: []
    }));
  }
  
  _recommendStack(architecture) {
    const stacks = {
      microservices: {
        backend: 'Python + FastAPI',
        frontend: 'React',
        database: 'PostgreSQL + Redis',
        message_queue: 'RabbitMQ'
      },
      modular_monolith: {
        backend: 'Python + Django',
        frontend: 'Vue',
        database: 'PostgreSQL'
      },
      simple: {
        backend: 'Python + Flask',
        frontend: '简单 HTML/JS',
        database: 'SQLite'
      }
    };
    return stacks[architecture] || stacks.simple;
  }
}

class Engineer extends Role {
  constructor(roleId = 'engineer', name = '工程师') {
    super(roleId, name, RoleType.ENGINEER, ['Python', 'JavaScript', '代码实现', '单元测试']);
  }
  
  _initActions() {
    this.addAction('implement', '实现功能', ['design'], 'code');
    this.addAction('write_tests', '编写测试', ['code'], 'tests');
    this.addAction('code_review', '代码审查', ['code'], 'review_comments');
  }
  
  implement(context) {
    const design = context.design || context;
    
    return {
      files: this._generateFiles(design),
      language: design.tech_stack?.backend?.includes('Python') ? 'python' : 'javascript',
      created_at: new Date().toISOString()
    };
  }
  
  _generateFiles(design) {
    const files = [];
    const architecture = design.architecture || 'simple';
    
    if (architecture === 'simple' || architecture === 'modular_monolith') {
      files.push({
        path: 'app.py',
        content: '# Main application file\nimport flask\napp = flask.Flask(__name__)\n\n@app.route("/")\ndef index():\n    return "Hello World"\n\nif __name__ == "__main__":\n    app.run(debug=True)\n'
      });
    }
    
    return files;
  }
}

class QA extends Role {
  constructor(roleId = 'qa') {
    super(roleId, '测试工程师', RoleType.QA, ['测试用例设计', '缺陷跟踪', '自动化测试', '性能测试']);
  }
  
  _initActions() {
    this.addAction('design_tests', '设计测试用例', ['requirements', 'design'], 'test_cases');
    this.addAction('execute_tests', '执行测试', ['code', 'test_cases'], 'test_results');
  }
  
  designTests(context) {
    const requirements = context.requirements || {};
    const features = requirements.features || [];
    
    const testCases = features.map(feature => ({
      feature,
      cases: [
        { scenario: '正常流程', expected: '成功' },
        { scenario: '异常输入', expected: '错误处理' }
      ]
    }));
    
    return { test_cases: testCases, created_at: new Date().toISOString() };
  }
}

class DevOps extends Role {
  constructor(roleId = 'devops') {
    super(roleId, 'DevOps 工程师', RoleType.DEVOPS, ['CI/CD', '容器化', '监控', '部署']);
  }
  
  _initActions() {
    this.addAction('setup_ci_cd', '配置 CI/CD', ['repo'], 'ci_cd_config');
    this.addAction('create_dockerfile', '创建 Dockerfile', [], 'dockerfile');
    this.addAction('deploy', '部署应用', ['environment'], 'deployment_info');
  }
  
  setupCI(repo) {
    return {
      pipeline: 'GitHub Actions',
      stages: ['test', 'build', 'deploy'],
      created_at: new Date().toISOString()
    };
  }
}

function createRoleFactory() {
  return {
    ProductManager,
    Architect,
    Engineer,
    QA,
    DevOps,
    create(roleType, roleId) {
      switch (roleType) {
        case RoleType.PM:
          return new ProductManager(roleId);
        case RoleType.ARCHITECT:
          return new Architect(roleId);
        case RoleType.ENGINEER:
          return new Engineer(roleId);
        case RoleType.QA:
          return new QA(roleId);
        case RoleType.DEVOPS:
          return new DevOps(roleId);
        default:
          return new Engineer(roleId);
      }
    }
  };
}

// ========== Main Agent ==========

class Agent {
  constructor({
    llmProvider = 'openai',
    llmModel = null,
    outputDir = './output',
    useMemory = true,
    useSandbox = true,
    verbose = false
  } = {}) {
    this.roles = {
      pm: new ProductManager(),
      architect: new Architect(),
      engineer: new Engineer(),
      qa: new QA(),
      devops: new DevOps()
    };
    
    this.outputDir = outputDir;
    this.verbose = verbose;
    
    // Memory system - simplified integration
    this.memory = null;
    this.useMemory = useMemory;
    
    // Workflow engine
    this.workflowEngine = null;
    if (WorkflowEngine) {
      try {
        this.workflowEngine = new WorkflowEngine();
      } catch (e) {
        // Workflow engine not available
      }
    }
  }
  
  async run(description, projectType = 'fastapi', projectName = null) {
    // Project name
    if (!projectName) {
      projectName = this._extractProjectName(description);
    }
    
    this._printHeader(description, projectType, projectName);
    
    const result = {
      description,
      project_type: projectType,
      project_name: projectName,
      output_dir: this.outputDir,
      steps: {},
      files: [],
      success: true,
      error: null,
      timestamp: new Date().toISOString(),
      memory_used: false
    };
    
    try {
      // Step 1: Analyze requirements (PM)
      if (this.verbose) console.log('\n📋 步骤 1: 需求分析 (PM)...');
      const requirements = this.roles.pm.analyzeRequirements({ user_input: description });
      result.steps.requirements = requirements;
      
      // Step 2: System design (Architect)
      if (this.verbose) console.log('\n🏗️ 步骤 2: 系统设计 (架构师)...');
      const design = this.roles.architect.designSystem({ requirements });
      result.steps.design = design;
      
      // Step 3: Implementation (Engineer)
      if (this.verbose) console.log('\n💻 步骤 3: 代码实现 (工程师)...');
      const implementation = this.roles.engineer.implement({ design });
      result.steps.implementation = implementation;
      result.files = implementation.files || [];
      
      // Step 4: Testing (QA)
      if (this.verbose) console.log('\n🧪 步骤 4: 测试设计 (QA)...');
      const tests = this.roles.qa.designTests({ requirements, design });
      result.steps.tests = tests;
      
      // Step 5: DevOps setup
      if (this.verbose) console.log('\n🚀 步骤 5: DevOps 配置...');
      const devops = this.roles.devops.setupCI(projectName);
      result.steps.devops = devops;
      
      console.log('\n✅ 项目生成完成!');
      console.log(`📁 输出目录: ${this.outputDir}`);
      console.log(`📝 生成文件: ${result.files.length} 个`);
      
    } catch (error) {
      result.success = false;
      result.error = error.message;
      console.error(`\n❌ 项目生成失败: ${error.message}`);
    }
    
    return result;
  }
  
  _extractProjectName(description) {
    // Simple extraction - first meaningful phrase
    const words = description.split(/\s+/).slice(0, 3);
    return words.join('_').replace(/[^a-zA-Z0-9_\u4e00-\u9fff]/g, '').toLowerCase() || 'project';
  }
  
  _printHeader(description, projectType, projectName) {
    console.log('\n' + '='.repeat(60));
    console.log('🤖 Agent - 统一工作流引擎');
    console.log('='.repeat(60));
    console.log(`\n📝 描述: ${description}`);
    console.log(`🏷️  类型: ${projectType}`);
    console.log(`📦 项目: ${projectName}`);
    console.log();
  }
  
  chat() {
    console.log('\n💬 进入对话模式 (按 Ctrl+C 退出)');
    console.log('提示: 输入您的需求，系统会自动选择合适的角色处理\n');
    
    // Simple REPL
    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    const prompt = () => {
      rl.question('\n👤 您: ', async (input) => {
        if (input.toLowerCase() === 'exit') {
          rl.close();
          return;
        }
        
        try {
          const result = await this.run(input);
          console.log('\n📤 Agent:', JSON.stringify(result, null, 2));
        } catch (e) {
          console.error('错误:', e.message);
        }
        
        prompt();
      });
    };
    
    prompt();
  }
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command || command === 'help') {
    console.log(`
Agent - 统一入口（记忆系统 + 工作流引擎）

Usage:
    node agent.js "开发一个博客系统"
    node agent.js "开发 API" --type fastapi
    node agent.js chat
    node agent.js history --task <task_id>
    node agent.js --help
`);
    process.exit(1);
  }
  
  if (command === 'chat') {
    const agent = new Agent({ verbose: true });
    agent.chat();
    return;
  }
  
  if (command === 'history') {
    const taskIdx = args.indexOf('--task');
    if (taskIdx !== -1) {
      console.log(`查看任务历史: ${args[taskIdx + 1]}`);
      // Would load from memory system
    }
    return;
  }
  
  // Run project generation
  const typeIdx = args.indexOf('--type');
  const llmIdx = args.indexOf('--llm');
  
  const description = args[0];
  const projectType = typeIdx !== -1 ? args[typeIdx + 1] : 'fastapi';
  const llmProvider = llmIdx !== -1 ? args[llmIdx + 1] : 'openai';
  
  const agent = new Agent({ llmProvider, verbose: true });
  await agent.run(description, projectType);
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export {
  Agent,
  Role,
  RoleType,
  ProductManager,
  Architect,
  Engineer,
  QA,
  DevOps,
  createRoleFactory
};

export default Agent;
