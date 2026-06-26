# MCP Client Skill

**version**: 0.1.0

MCP (Model Context Protocol) 客户端技能，用于连接和管理外部 MCP 服务器。

## 功能特性

- **多传输支持**: stdio、SSE (Server-Sent Events)
- **完整协议实现**: 工具调用、资源读取、提示词获取
- **安全控制**: 权限验证、敏感操作确认、审计日志
- **错误处理**: 自动重试、详细错误码
- **事件系统**: 连接状态、工具调用事件监听

## 安装

```bash
# 进入技能目录
cd skills/mcp-client

# 安装依赖
npm install
```

## 配置

编辑 `src/mcp-config.json` 配置 MCP 服务器：

```json
{
  "filesystem": {
    "id": "filesystem",
    "name": "Filesystem Server",
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
    "description": "本地文件系统访问"
  },
  "github": {
    "id": "github",
    "name": "GitHub Server",
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "your-token-here"
    },
    "description": "GitHub API 集成"
  }
}
```

## 使用方法

### 命令行

```bash
# 列出已配置的服务器
npm run mcp list

# 连接到服务器
npm run mcp connect filesystem

# 列出可用工具
npm run mcp tools filesystem

# 调用工具
npm run mcp call filesystem read_file '{"path": "./package.json"}'

# 读取文件
npm run mcp read ./package.json

# 列出目录
npm run mcp ls ./src

# 搜索文件
npm run mcp search "*.js"

# 查看审计日志
npm run mcp audit
```

### JavaScript API

```javascript
import { OpenClawMCPSkill } from './src/mcp-skill.js';

// 创建技能实例
const skill = new OpenClawMCPSkill({
  autoApprove: false,        // 是否需要用户批准
  requireApproval: true,     // 强制要求批准
  autoApprovePatterns: ['*:read_*'],  // 自动批准模式
  blockedPatterns: ['*:delete_*']     // 禁止模式
});

// 列出服务器
skill.listServers();

// 连接到服务器
await skill.connect('filesystem');

// 获取服务器信息
const info = await skill.getServerInfo('filesystem');
console.log(info);

// 列出工具
const tools = await skill.listTools('filesystem');

// 调用工具
const result = await skill.callTool('filesystem', 'read_file', {
  path: './package.json'
});

// 快捷方法
const content = await skill.readFile('./package.json');
const listing = await skill.listDirectory('./src');
const matches = await skill.searchFiles('*.js');

// 批准工具（后续调用无需确认）
skill.approveTool('filesystem', 'read_file', true);

// 获取审计日志
const logs = skill.getAuditLog(100);

// 关闭所有连接
await skill.closeAll();
```

### 直接使用客户端

```javascript
import { MCPClient, MCPServerConfig, MCPClientConfig } from './src/client.js';
import { SecureMCPClient } from './src/secure-client.js';

// 基础客户端
const client = new MCPClient(new MCPClientConfig({
  name: 'my-client',
  autoApprove: true
}));

// 安全客户端（带审计和重试）
const secureClient = new SecureMCPClient(
  new MCPClientConfig(),
  {
    requireApproval: true,
    blockedPatterns: ['*:delete_*']
  }
);

// 配置服务器
const serverConfig = new MCPServerConfig({
  id: 'my-server',
  name: 'My Server',
  type: 'stdio',
  command: 'node',
  args: ['server.js']
});

// 连接
await client.connect(serverConfig);

// 获取能力
const capabilities = await client.getServerCapabilities('my-server');

// 列出工具
const tools = await client.listTools('my-server');

// 调用工具
const result = await client.callTool('my-server', 'tool_name', {
  arg1: 'value1'
});

// 列出资源
const resources = await client.listResources('my-server');

// 读取资源
const resource = await client.readResource('my-server', 'file:///path');

// 列出提示词
const prompts = await client.listPrompts('my-server');

// 获取提示词
const prompt = await client.getPrompt('my-server', 'prompt_name', {
  arg1: 'value1'
});

// 事件监听
client.on('connected', (data) => {
  console.log('Connected:', data.serverId);
});

client.on('toolCalled', (data) => {
  console.log('Tool called:', data.toolName);
});

client.on('resourceRead', (data) => {
  console.log('Resource read:', data.resourceUri);
});

// 断开连接
await client.disconnect('my-server');
```

## 支持的 MCP 服务器

### stdio 类型
- `@modelcontextprotocol/server-filesystem` - 文件系统访问
- `@modelcontextprotocol/server-github` - GitHub API
- `@modelcontextprotocol/server-postgres` - PostgreSQL 数据库
- `@modelcontextprotocol/server-sqlite` - SQLite 数据库

### SSE 类型
- 任何支持 MCP SSE 协议的服务器
- 配置示例：
```json
{
  "id": "remote-server",
  "name": "Remote MCP Server",
  "type": "sse",
  "url": "http://localhost:3000/sse",
  "headers": {
    "Authorization": "Bearer token"
  }
}
```

## 安全特性

### 权限控制
- 工具调用需要用户批准（可配置）
- 资源访问需要用户批准
- 敏感路径自动检测（.env、.git、/etc/passwd 等）

### 审计日志
```javascript
// 获取审计日志
const logs = client.getAuditLog(100);

// 日志格式
{
  timestamp: Date,
  action: 'tool_call' | 'resource_read' | 'connect' | ...,
  details: { ... }
}
```

### 错误处理
```javascript
try {
  await client.callTool('server', 'tool', args);
} catch (error) {
  console.log(error.code);      // 错误码
  console.log(error.message);   // 错误消息
  console.log(error.details);   // 详细信息
}
```

错误码：
- `CONNECTION_FAILED` - 连接失败
- `CONNECTION_NOT_FOUND` - 未找到连接
- `TOOL_EXECUTION_FAILED` - 工具执行失败
- `RESOURCE_READ_FAILED` - 资源读取失败
- `PERMISSION_DENIED` - 权限拒绝
- `UNSUPPORTED_TRANSPORT` - 不支持的传输类型

## 测试

```bash
# 运行所有测试
npm test

# 运行基础测试
npm run test

# 运行安全测试
npm run test:security

# 运行集成测试（需要实际 MCP 服务器）
npm run test:filesystem
```

## 项目结构

```
skills/mcp-client/
├── src/
│   ├── client.js        # 基础 MCP 客户端
│   ├── secure-client.js # 带安全控制的客户端
│   ├── mcp-skill.js     # OpenClaw 技能接口
│   └── mcp-config.json  # 服务器配置
├── test/
│   ├── client.test.js       # 基础功能测试
│   ├── security.test.js     # 安全控制测试
│   ├── mcp-servers.test.js  # 集成测试
│   └── github-server.js     # GitHub 服务器测试
├── package.json
├── SKILL.md
└── README.md
```

## 依赖

- `@modelcontextprotocol/sdk` - 官方 MCP SDK
- `zod` - 类型验证（可选）

## 协议版本

- MCP Protocol: 2024-11-05
- SDK Version: ^1.0.0

## 许可证

MIT
