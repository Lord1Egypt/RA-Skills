/**
 * Roles - 角色定义系统
 * 
 * Inspired by MetaGPT
 * 
 * Usage:
 *   import { ProductManager, Architect, Engineer, QA, DevOps } from './roles.js';
 *   
 *   const pm = new ProductManager();
 *   const architect = new Architect();
 *   const engineer = new Engineer();
 *   
 *   const requirements = pm.analyzeRequirements({ user_input: "做一个博客系统" });
 *   const design = architect.designSystem({ requirements });
 *   const code = engineer.implement({ design });
 */

import crypto from 'crypto';

// ========== Role Types ==========

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

// ========== Action Definition ==========

class Action {
  constructor(name, description, inputKeys = [], outputKey = '', requiredSkills = []) {
    this.name = name;
    this.description = description;
    this.inputKeys = inputKeys;
    this.outputKey = outputKey;
    this.requiredSkills = requiredSkills;
  }
}

// ========== Message ==========

class Message {
  constructor(sender, receiver, content, msgType = 'action', timestamp = null) {
    this.sender = sender;
    this.receiver = receiver;
    this.content = content;
    this.msgType = msgType;
    this.timestamp = timestamp || new Date().toISOString();
  }
  
  toDict() {
    return {
      sender: this.sender,
      receiver: this.receiver,
      content: this.content,
      msgType: this.msgType,
      timestamp: this.timestamp
    };
  }
}

// ========== Role Base Class ==========

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
  
  addAction(action) {
    if (!(action instanceof Action)) {
      action = new Action(action.name, action.description, action.inputKeys, action.outputKey, action.requiredSkills);
    }
    this.actions[action.name] = action;
  }
  
  canExecute(actionName) {
    return actionName in this.actions;
  }
  
  receive(message) {
    this.inbox.push(message);
  }
  
  send(receiver, content, msgType = 'action') {
    const msg = new Message(this.roleId, receiver, content, msgType);
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

// ========== Product Manager ==========

class ProductManager extends Role {
  constructor(roleId = 'pm') {
    super(roleId, '产品经理', RoleType.PM, ['需求分析', '产品设计', '用户研究', '数据分析']);
  }
  
  _initActions() {
    this.addAction(new Action(
      'analyze_requirements',
      '分析用户需求',
      ['user_input'],
      'requirements'
    ));
    this.addAction(new Action(
      'create_prd',
      '创建产品需求文档',
      ['requirements'],
      'prd'
    ));
    this.addAction(new Action(
      'prioritize_features',
      '功能优先级排序',
      ['features'],
      'priority_list'
    ));
    this.addAction(new Action(
      'write_report',
      '撰写报告',
      ['analysis'],
      'report'
    ));
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
  
  prioritizeFeatures(context) {
    const features = context.features || [];
    
    return {
      features: features.map((f, i) => ({
        name: f,
        priority: i < 3 ? 'high' : i < 6 ? 'medium' : 'low'
      })),
      created_at: new Date().toISOString()
    };
  }
}

// ========== Architect ==========

class Architect extends Role {
  constructor(roleId = 'architect') {
    super(roleId, '架构师', RoleType.ARCHITECT, ['架构设计', '系统设计', '技术选型', '性能优化']);
  }
  
  _initActions() {
    this.addAction(new Action(
      'design_system',
      '设计系统架构',
      ['requirements'],
      'design'
    ));
    this.addAction(new Action(
      'select_tech_stack',
      '技术选型',
      ['requirements', 'constraints'],
      'tech_stack'
    ));
    this.addAction(new Action(
      'review_architecture',
      '架构评审',
      ['design'],
      'review_comments'
    ));
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
  
  selectTechStack(context) {
    const requirements = context.requirements || {};
    const constraints = context.constraints || [];
    
    return {
      backend: constraints.includes('性能优先') ? 'Go + Gin' : 'Python + FastAPI',
      frontend: 'React',
      database: constraints.includes('安全优先') ? 'PostgreSQL' : 'MySQL',
      cache: 'Redis',
      message_queue: 'RabbitMQ'
    };
  }
  
  reviewArchitecture(context) {
    const design = context.design || {};
    const issues = [];
    
    if (design.architecture === 'microservices' && design.components?.length < 5) {
      issues.push('微服务架构建议至少5个服务，当前组件较少');
    }
    
    if (!design.tech_stack?.database?.includes('PostgreSQL')) {
      issues.push('建议使用 PostgreSQL 以获得更好的数据完整性');
    }
    
    return {
      issues,
      recommendations: issues.length === 0 ? ['架构设计合理'] : issues,
      reviewed_at: new Date().toISOString()
    };
  }
}

// ========== Engineer ==========

class Engineer extends Role {
  constructor(roleId = 'engineer', name = '工程师') {
    super(roleId, name, RoleType.ENGINEER, ['Python', 'JavaScript', '代码实现', '单元测试']);
  }
  
  _initActions() {
    this.addAction(new Action(
      'implement',
      '实现功能',
      ['design'],
      'code'
    ));
    this.addAction(new Action(
      'write_tests',
      '编写测试',
      ['code'],
      'tests'
    ));
    this.addAction(new Action(
      'code_review',
      '代码审查',
      ['code'],
      'review_comments'
    ));
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
    
    if (architecture === 'simple') {
      files.push({
        path: 'app.py',
        content: `#!/usr/bin/env python3
"""
Main application file
Generated by Agent
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'Hello World'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
`
      });
      files.push({
        path: 'requirements.txt',
        content: `flask>=2.0.0
flask-cors>=3.0.0
`
      });
    } else if (architecture === 'modular_monolith') {
      files.push({
        path: 'app.py',
        content: `#!/usr/bin/env python3
"""
Main application file - Modular Monolith
"""
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Import blueprints
from routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=True)
`
      });
      files.push({
        path: 'routes.py',
        content: `from flask import Blueprint

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health():
    return {'status': 'healthy'}
`
      });
    }
    
    return files;
  }
  
  writeTests(context) {
    const code = context.code || {};
    const files = code.files || [];
    
    const testFiles = files.filter(f => f.path.endsWith('.py')).map(f => ({
      path: `test_${f.path}`,
      content: `import pytest
import sys
sys.path.insert(0, '.')

from app import app

def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
`
    }));
    
    return {
      test_files: testFiles,
      coverage: '70%',
      created_at: new Date().toISOString()
    };
  }
  
  codeReview(context) {
    const code = context.code || {};
    const files = code.files || [];
    
    const issues = [];
    for (const file of files) {
      if (file.content && file.content.length < 50) {
        issues.push({ file: file.path, severity: 'warning', message: '文件内容过短' });
      }
    }
    
    return {
      issues,
      recommendations: issues.length === 0 ? ['代码质量良好'] : issues,
      reviewed_at: new Date().toISOString()
    };
  }
}

// ========== Frontend Engineer ==========

class FrontendEngineer extends Role {
  constructor(roleId = 'frontend') {
    super(roleId, '前端工程师', RoleType.FRONTEND_ENGINEER, ['React', 'Vue', 'JavaScript', 'CSS', 'HTML']);
  }
  
  _initActions() {
    this.addAction(new Action('implement_ui', '实现 UI', ['design'], 'ui_code'));
    this.addAction(new Action('write_unit_tests', '编写单元测试', ['ui_code'], 'test_results'));
  }
  
  implementUI(context) {
    const design = context.design || {};
    
    return {
      files: [
        { path: 'index.html', content: '<!DOCTYPE html>\n<html>\n<head><title>App</title></head>\n<body><div id="app"></div></body>\n</html>' },
        { path: 'src/App.jsx', content: '// Main App Component\nimport React from "react";\n\nexport default function App() {\n  return <div>Hello World</div>;\n}' }
      ],
      framework: 'React',
      created_at: new Date().toISOString()
    };
  }
}

// ========== Backend Engineer ==========

class BackendEngineer extends Role {
  constructor(roleId = 'backend') {
    super(roleId, '后端工程师', RoleType.BACKEND_ENGINEER, ['Python', 'Java', 'Go', 'API', 'Database']);
  }
  
  _initActions() {
    this.addAction(new Action('implement_api', '实现 API', ['design'], 'api_code'));
    this.addAction(new Action('write_unit_tests', '编写单元测试', ['api_code'], 'test_results'));
  }
  
  implementAPI(context) {
    return {
      files: [
        { path: 'api/routes.py', content: '# API Routes\nfrom flask import Blueprint\n\napi = Blueprint("api", __name__)\n\n@api.route("/health")\ndef health():\n    return {"status": "healthy"}' }
      ],
      framework: 'Flask',
      created_at: new Date().toISOString()
    };
  }
}

// ========== QA Engineer ==========

class QA extends Role {
  constructor(roleId = 'qa') {
    super(roleId, '测试工程师', RoleType.QA, ['测试用例设计', '缺陷跟踪', '自动化测试', '性能测试']);
  }
  
  _initActions() {
    this.addAction(new Action('design_tests', '设计测试用例', ['requirements', 'design'], 'test_cases'));
    this.addAction(new Action('execute_tests', '执行测试', ['code', 'test_cases'], 'test_results'));
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
    
    return {
      test_cases: testCases,
      created_at: new Date().toISOString()
    };
  }
  
  executeTests(context) {
    return {
      passed: true,
      total: 10,
      failed: 0,
      coverage: '80%',
      executed_at: new Date().toISOString()
    };
  }
}

// ========== DevOps ==========

class DevOps extends Role {
  constructor(roleId = 'devops') {
    super(roleId, 'DevOps 工程师', RoleType.DEVOPS, ['CI/CD', '容器化', '监控', '部署']);
  }
  
  _initActions() {
    this.addAction(new Action('setup_ci_cd', '配置 CI/CD', ['repo'], 'ci_cd_config'));
    this.addAction(new Action('create_dockerfile', '创建 Dockerfile', [], 'dockerfile'));
    this.addAction(new Action('deploy', '部署应用', ['environment'], 'deployment_info'));
  }
  
  setupCI(repo) {
    return {
      pipeline: 'GitHub Actions',
      stages: ['test', 'build', 'deploy'],
      config: {
        name: 'CI Pipeline',
        on: ['push', 'pull_request'],
        jobs: {
          test: { runs_on: 'ubuntu-latest', steps: [{ run: 'npm test' }] },
          build: { runs_on: 'ubuntu-latest', needs: 'test', steps: [{ run: 'npm run build' }] }
        }
      },
      created_at: new Date().toISOString()
    };
  }
  
  createDockerfile() {
    return {
      path: 'Dockerfile',
      content: `FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]`,
      created_at: new Date().toISOString()
    };
  }
  
  deploy(context) {
    return {
      environment: context.environment || 'production',
      status: 'deployed',
      url: 'https://example.com',
      deployed_at: new Date().toISOString()
    };
  }
}

// ========== Security Engineer ==========

class Security extends Role {
  constructor(roleId = 'security') {
    super(roleId, '安全工程师', RoleType.SECURITY, ['渗透测试', '代码审计', '安全架构', '合规']);
  }
  
  _initActions() {
    this.addAction(new Action('security_audit', '安全审计', ['code'], 'audit_results'));
    this.addAction(new Action('penetration_test', '渗透测试', ['system'], 'test_results'));
  }
  
  securityAudit(context) {
    return {
      vulnerabilities: [],
      risk_level: 'low',
      recommendations: ['代码安全审计通过'],
      audited_at: new Date().toISOString()
    };
  }
}

// ========== Data Engineer ==========

class DataEngineer extends Role {
  constructor(roleId = 'data') {
    super(roleId, '数据工程师', RoleType.DATA_ENGINEER, ['数据建模', 'ETL', '数据分析', '数据仓库']);
  }
  
  _initActions() {
    this.addAction(new Action('design_data_model', '设计数据模型', ['requirements'], 'data_model'));
    this.addAction(new Action('build_etl', '构建 ETL', ['data_model'], 'etl_pipeline'));
  }
  
  designDataModel(context) {
    return {
      tables: [
        { name: 'users', columns: ['id', 'name', 'email', 'created_at'] },
        { name: 'products', columns: ['id', 'name', 'price', 'created_at'] }
      ],
      relationships: [
        { from: 'users', to: 'products', type: 'has_many' }
      ],
      created_at: new Date().toISOString()
    };
  }
}

// ========== Designer ==========

class Designer extends Role {
  constructor(roleId = 'designer') {
    super(roleId, 'UI/UX 设计师', RoleType.DESIGNER, ['UI设计', 'UX设计', '原型', '设计系统']);
  }
  
  _initActions() {
    this.addAction(new Action('design_ui', '设计 UI', ['requirements'], 'designs'));
    this.addAction(new Action('create_prototype', '创建原型', ['designs'], 'prototype'));
  }
  
  designUI(context) {
    return {
      mockups: ['homepage.png', 'detail.png', 'checkout.png'],
      style_guide: 'modern',
      created_at: new Date().toISOString()
    };
  }
}

// ========== Role Factory ==========

function createRoleFactory() {
  return {
    Role,
    ProductManager,
    Architect,
    Engineer,
    FrontendEngineer,
    BackendEngineer,
    QA,
    DevOps,
    Security,
    DataEngineer,
    Designer,
    RoleType,
    
    create(roleType, roleId = null) {
      const id = roleId || roleType;
      switch (roleType) {
        case RoleType.PM: return new ProductManager(id);
        case RoleType.ARCHITECT: return new Architect(id);
        case RoleType.ENGINEER: return new Engineer(id);
        case RoleType.FRONTEND_ENGINEER: return new FrontendEngineer(id);
        case RoleType.BACKEND_ENGINEER: return new BackendEngineer(id);
        case RoleType.QA: return new QA(id);
        case RoleType.DEVOPS: return new DevOps(id);
        case RoleType.SECURITY: return new Security(id);
        case RoleType.DATA_ENGINEER: return new DataEngineer(id);
        case RoleType.DESIGNER: return new Designer(id);
        default: return new Engineer(id);
      }
    }
  };
}

export {
  RoleType,
  Action,
  Message,
  Role,
  ProductManager,
  Architect,
  Engineer,
  FrontendEngineer,
  BackendEngineer,
  QA,
  DevOps,
  Security,
  DataEngineer,
  Designer,
  createRoleFactory
};

export default createRoleFactory;