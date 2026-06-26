/**
 * Code Generator - 代码生成器 v1.0
 * 
 * 功能:
 * - 多语言支持（Python、JavaScript、Go、Java）
 * - 代码模板系统
 * - 项目脚手架生成
 * 
 * Usage:
 *     import { CodeGenerator } from './system/code_generator.js';
 *     
 *     const gen = new CodeGenerator();
 *     const file = gen.generateFile('python_api', { title: 'My API', endpoints: [...] });
 *     file.save('/path/to/project');
 *     
 *     const project = gen.generateProject({ name: 'my-api', type: 'fastapi' });
 *     for (const file of project) {
 *       file.save('/path/to/project');
 *     }
 */

// ============================================================
// Imports
// ============================================================

import { mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';

// ============================================================
// Code File
// ============================================================

export class CodeFile {
  /**
   * @param {string} name
   * @param {string} content
   * @param {string} language
   * @param {string} description
   */
  constructor(name, content, language = 'text', description = '') {
    this.name = name;
    this.content = content;
    this.language = language;
    this.description = description;
  }

  /**
   * Save file to disk
   * @param {string} basePath
   * @returns {string}
   */
  save(basePath) {
    const filePath = join(basePath, this.name);
    const dir = filePath.substring(0, filePath.lastIndexOf('/'));
    if (dir) mkdirSync(dir, { recursive: true });
    writeFileSync(filePath, this.content, 'utf-8');
    return filePath;
  }

  toString() {
    return this.content;
  }
}

// ============================================================
// Code Generator
// ============================================================

export class CodeGenerator {
  constructor() {
    this.templates = {
      // Python
      'python_main': this._pythonMainTemplate.bind(this),
      'python_api': this._pythonApiTemplate.bind(this),
      'python_model': this._pythonModelTemplate.bind(this),
      'python_test': this._pythonTestTemplate.bind(this),
      'python_requirements': this._pythonRequirementsTemplate.bind(this),

      // JavaScript/TypeScript
      'js_index': this._jsIndexTemplate.bind(this),
      'js_api': this._jsApiTemplate.bind(this),
      'js_package': this._jsPackageTemplate.bind(this),

      // Config
      'dockerfile': this._dockerfileTemplate.bind(this),
      'docker_compose': this._dockerComposeTemplate.bind(this),
      'gitignore': this._gitignoreTemplate.bind(this),
      'readme': this._readmeTemplate.bind(this),
    };

    this.projectTypes = {
      'fastapi': this._fastapiProject.bind(this),
      'flask': this._flaskProject.bind(this),
      'django': this._djangoProject.bind(this),
      'express': this._expressProject.bind(this),
      'cli': this._cliProject.bind(this),
    };
  }

  // ============================================================
  // Single File Generation
  // ============================================================

  /**
   * Generate a single file
   * @param {string} fileType
   * @param {Object} data
   * @param {string|null} name
   * @returns {CodeFile}
   */
  generateFile(fileType, data, name = null) {
    const templateFunc = this.templates[fileType];
    if (!templateFunc) {
      throw new Error(`不支持的文件类型: ${fileType}`);
    }

    const content = templateFunc(data);

    return new CodeFile(
      name || `${fileType}.py`,
      content,
      this._getLanguage(fileType),
      data.description || ''
    );
  }

  // ============================================================
  // Project Generation
  // ============================================================

  /**
   * Generate a project scaffold
   * @param {Object} config
   * @returns {CodeFile[]}
   */
  generateProject(config) {
    const projectType = config.type || 'fastapi';
    const generator = this.projectTypes[projectType];
    if (!generator) {
      throw new Error(`不支持的项目类型: ${projectType}`);
    }
    return generator(config);
  }

  // ============================================================
  // Templates - Python
  // ============================================================

  _pythonMainTemplate(data) {
    const name = data.name || 'main';
    const description = data.description || '';

    return `#!/usr/bin/env python3
"""
${name}

${description}
"""

import argparse
import sys
from datetime import datetime


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="${description}")
    parser.add_argument("--version", action="store_true", help="显示版本")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    args = parser.parse_args()

    if args.version:
        print("${name} v1.0.0")
        return 0

    print(f"Hello from ${name}!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
`;
  }

  _pythonApiTemplate(data) {
    const endpoints = data.endpoints || [];
    const title = data.title || 'API';
    const now = new Date().toISOString().split('T')[0];

    let endpointsCode = '';
    for (const ep of endpoints) {
      const method = (ep.method || 'GET').toLowerCase();
      const path = ep.path || '/';
      const epName = ep.name || 'endpoint';
      const desc = ep.description || '';

      if (method === 'get') {
        endpointsCode += `
@app.get("${path}")
async def ${epName}():
    """${desc}"""
    return {"status": "ok", "data": []}}
`;
      } else if (method === 'post') {
        endpointsCode += `
@app.post("${path}")
async def ${epName}(data: dict):
    """${desc}"""
    return {"status": "created", "data": data}
`;
      }
    }

    return `#!/usr/bin/env python3
"""
${title} - FastAPI 应用

生成时间: ${now}
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

app = FastAPI(
    title="${title}",
    version="1.0.0",
    description="自动生成的 API"
)


class HealthResponse(BaseModel):
    status: str
    timestamp: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )
${endpointsCode}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
`;
  }

  _pythonModelTemplate(data) {
    const modelName = data.name || 'Item';
    const fields = data.fields || [
      { name: 'id', type: 'int' },
      { name: 'name', type: 'str' },
      { name: 'created_at', type: 'datetime' },
    ];
    const now = new Date().toISOString().split('T')[0];

    let fieldDefs = '';
    for (const f of fields) {
      const fname = f.name;
      const ftype = f.type;
      const optional = f.optional || false;

      if (ftype === 'int') {
        fieldDefs += `    ${fname}: ${optional ? 'Optional[int]' : 'int'}\n`;
      } else if (ftype === 'str') {
        fieldDefs += `    ${fname}: ${optional ? 'Optional[str]' : 'str'}\n`;
      } else if (ftype === 'datetime') {
        fieldDefs += `    ${fname}: ${optional ? 'Optional[datetime]' : 'datetime'}\n`;
      } else if (ftype === 'bool') {
        fieldDefs += `    ${fname}: ${optional ? 'Optional[bool]' : 'bool'} = False\n`;
      }
    }

    let createFields = '';
    for (const f of fields) {
      if (f.name !== 'id') {
        createFields += `    ${f.name}: ${f.type}\n`;
      }
    }

    let updateFields = '';
    for (const f of fields) {
      if (f.name !== 'id') {
        updateFields += `    ${f.name}: Optional[${f.type}] = None\n`;
      }
    }

    return `#!/usr/bin/env python3
"""
数据模型 - ${modelName}

生成时间: ${now}
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ${modelName}(BaseModel):
    """${modelName} 模型"""
${fieldDefs}
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "示例"
            }
        }


class ${modelName}Create(BaseModel):
    """创建 ${modelName}"""
${createFields}


class ${modelName}Update(BaseModel):
    """更新 ${modelName}"""
${updateFields}
`;
  }

  _pythonTestTemplate(data) {
    const testName = data.name || 'test_main';
    const functions = data.functions || ['main'];
    const now = new Date().toISOString().split('T')[0];

    let testCases = '';
    for (const func of functions) {
      testCases += `
def test_${func}():
    """测试 ${func}"""
    # TODO: 实现测试
    assert True
`;
    }

    return `#!/usr/bin/env python3
"""
测试文件 - ${testName}

生成时间: ${now}
"""

import pytest
from unittest.mock import Mock, patch

${testCases}


class Test${testName.replace('_', '').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('')}:
    """测试类"""

    def setup_method(self):
        """每个测试方法前的设置"""
        pass

    def teardown_method(self):
        """每个测试方法后的清理"""
        pass

    def test_example(self):
        """示例测试"""
        assert 1 + 1 == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
`;
  }

  _pythonRequirementsTemplate(data) {
    const dependencies = data.dependencies || [
      'fastapi>=0.100.0',
      'uvicorn>=0.23.0',
      'pydantic>=2.0.0',
      'python-dotenv>=1.0.0',
    ];
    const now = new Date().toISOString().split('T')[0];

    return `# 自动生成的依赖
# 生成时间: ${now}

${dependencies.join('\n')}
`;
  }

  // ============================================================
  // Templates - JavaScript
  // ============================================================

  _jsIndexTemplate(data) {
    const name = data.name || 'app';
    const now = new Date().toISOString().split('T')[0];

    return `/**
 * ${name}
 * 
 * 生成时间: ${now}
 */

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(express.json());

// 路由
app.get('/', (req, res) => {
    res.json({ message: 'Hello from ${name}!' });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// 启动服务器
app.listen(PORT, () => {
    console.log(\`Server running on port \${PORT}\`);
});

module.exports = app;
`;
  }

  _jsApiTemplate(data) {
    const routes = data.routes || [];
    const now = new Date().toISOString().split('T')[0];

    let routeDefs = '';
    for (const r of routes) {
      const method = (r.method || 'get').toLowerCase();
      const path = r.path || '/';
      const rName = r.name || 'handler';
      routeDefs += `
router.${method}('${path}', async (req, res) => {
    try {
        // TODO: 实现 ${rName}
        res.json({ status: 'ok' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
`;
    }

    return `/**
 * API 路由
 * 
 * 生成时间: ${now}
 */

const express = require('express');
const router = express.Router();
${routeDefs}
module.exports = router;
`;
  }

  _jsPackageTemplate(data) {
    const name = data.name || 'my-app';
    const description = data.description || '';

    return `{
  "name": "${name}",
  "version": "1.0.0",
  "description": "${description}",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "nodemon": "^3.0.0"
  },
  "keywords": [],
  "author": "",
  "license": "MIT"
}
`;
  }

  // ============================================================
  // Templates - Config
  // ============================================================

  _dockerfileTemplate(data) {
    const language = data.language || 'python';
    const name = data.name || 'app';

    if (language === 'python') {
      return `# Python 应用 Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
`;
    } else {
      return `# Node.js 应用 Dockerfile
FROM node:18-slim

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm install

# 复制代码
COPY . .

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["npm", "start"]
`;
    }
  }

  _dockerComposeTemplate(data) {
    const name = data.name || 'app';
    const services = data.services || ['web', 'db'];
    const now = new Date().toISOString().split('T')[0];

    let serviceDefs = '';
    if (services.includes('web')) {
      serviceDefs += `  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/${name}
    depends_on:
      - db
`;
    }
    if (services.includes('db')) {
      serviceDefs += `  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=${name}
    volumes:
      - postgres_data:/var/lib/postgresql/data
`;
    }

    return `version: '3.8'
# 生成时间: ${now}

services:
${serviceDefs}
volumes:
  postgres_data:
`;
  }

  _gitignoreTemplate(data) {
    const language = data.language || 'python';

    const common = `# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Env
.env
.env.local
`;

    if (language === 'python') {
      return common + `
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/

# Virtual
venv/
env/
.venv/
`;
    } else {
      return common + `
# Node
node_modules/
npm-debug.log*
yarn-debug.log*
dist/
build/
`;
    }
  }

  _readmeTemplate(data) {
    const name = data.name || 'project';
    const description = data.description || '';
    const now = new Date().toISOString().split('T')[0];

    return `# ${name}

${description}

## 快速开始

### 安装

\`\`\`bash
# 安装依赖
pip install -r requirements.txt
\`\`\`

### 运行

\`\`\`bash
# 启动服务
python main.py

# 或使用 uvicorn
uvicorn main:app --reload
\`\`\`

### 测试

\`\`\`bash
pytest tests/
\`\`\`

## 项目结构

\`\`\`
${name}/
├── main.py           # 主入口
├── api.py            # API 路由
├── models.py         # 数据模型
├── requirements.txt  # 依赖
├── Dockerfile        # Docker 配置
└── tests/            # 测试
    └── test_main.py
\`\`\`

## API 文档

启动后访问: http://localhost:8000/docs

## 许可证

MIT
`;
  }

  // ============================================================
  // Project Generators
  // ============================================================

  _fastapiProject(config) {
    const name = config.name || 'fastapi-app';
    const features = config.features || [];

    const files = [
      new CodeFile('main.py', this._pythonMainTemplate(config), 'python'),
      new CodeFile('api.py', this._pythonApiTemplate({
        title: name,
        endpoints: config.endpoints || [],
      }), 'python'),
      new CodeFile('models.py', this._pythonModelTemplate({
        name: 'Item',
        fields: [
          { name: 'id', type: 'int' },
          { name: 'name', type: 'str' },
          { name: 'created_at', type: 'datetime' },
        ],
      }), 'python'),
      new CodeFile('requirements.txt', this._pythonRequirementsTemplate(config), 'text'),
      new CodeFile('Dockerfile', this._dockerfileTemplate({ language: 'python', name }), 'text'),
      new CodeFile('docker-compose.yml', this._dockerComposeTemplate({ name }), 'yaml'),
      new CodeFile('.gitignore', this._gitignoreTemplate({ language: 'python' }), 'text'),
      new CodeFile('README.md', this._readmeTemplate(config), 'markdown'),
    ];

    // Add test file
    files.push(new CodeFile(
      'tests/test_main.py',
      this._pythonTestTemplate({ name: 'main', functions: ['health_check'] }),
      'python'
    ));

    return files;
  }

  _flaskProject(config) {
    // Similar to FastAPI
    config.framework = 'flask';
    return this._fastapiProject(config);
  }

  _djangoProject(config) {
    // Similar to FastAPI
    config.framework = 'django';
    return this._fastapiProject(config);
  }

  _expressProject(config) {
    const name = config.name || 'express-app';

    return [
      new CodeFile('index.js', this._jsIndexTemplate(config), 'javascript'),
      new CodeFile('package.json', this._jsPackageTemplate(config), 'json'),
      new CodeFile('Dockerfile', this._dockerfileTemplate({ language: 'node', name }), 'text'),
      new CodeFile('.gitignore', this._gitignoreTemplate({ language: 'node' }), 'text'),
      new CodeFile('README.md', this._readmeTemplate(config), 'markdown'),
    ];
  }

  _cliProject(config) {
    return [
      new CodeFile('main.py', this._pythonMainTemplate(config), 'python'),
      new CodeFile('requirements.txt', this._pythonRequirementsTemplate({
        dependencies: ['click>=8.0.0', 'rich>=13.0.0'],
      }), 'text'),
      new CodeFile('.gitignore', this._gitignoreTemplate({ language: 'python' }), 'text'),
      new CodeFile('README.md', this._readmeTemplate(config), 'markdown'),
    ];
  }

  // ============================================================
  // Helper Methods
  // ============================================================

  _getLanguage(fileType) {
    if (fileType.startsWith('python')) return 'python';
    if (fileType.startsWith('js')) return 'javascript';
    if (fileType === 'dockerfile') return 'dockerfile';
    if (fileType === 'readme') return 'markdown';
    if (fileType === 'gitignore') return 'text';
    return 'text';
  }
}

// ============================================================
// CLI
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'demo';
  const typeArg = args.find(a => a.startsWith('--type='))?.split('=')[1] || 'fastapi';
  const nameArg = args.find(a => a.startsWith('--name='))?.split('=')[1] || 'my-app';

  const gen = new CodeGenerator();

  if (command === 'demo') {
    // Generate single file
    const apiFile = gen.generateFile('python_api', {
      title: 'Demo API',
      endpoints: [
        { method: 'GET', path: '/users', name: 'list_users' },
        { method: 'POST', path: '/users', name: 'create_user' },
      ],
    });
    console.log(`📄 生成文件: ${apiFile.name}`);
    console.log(apiFile.content.slice(0, 500) + '...\n');
    return;
  }

  if (command === 'project') {
    // Generate project
    const files = gen.generateProject({
      name: nameArg,
      type: typeArg,
      description: `${nameArg} - 自动生成的项目`,
    });

    console.log(`🚀 生成项目: ${nameArg}`);
    console.log(`📁 文件数: ${files.length}`);
    for (const f of files) {
      console.log(`  - ${f.name} (${f.content.length} bytes)`);
    }
    return;
  }

  if (command === 'list') {
    console.log('支持的文件类型:');
    for (const t of Object.keys(gen.templates)) {
      console.log(`  - ${t}`);
    }
    console.log('\n支持的项目类型:');
    for (const t of Object.keys(gen.projectTypes)) {
      console.log(`  - ${t}`);
    }
  }
}

const isMain = process.argv[1]?.endsWith('code_generator.js') || process.argv[1]?.endsWith('code_generator.mjs');
if (isMain) {
  main().catch(console.error);
}

export default CodeGenerator;
