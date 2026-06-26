# 云效 MCP SSE 客户端

面向 AI agent 的云效 MCP 客户端，基于 Node.js，通过 MCP SSE 协议操作云效平台。

## 设计原则

- **`list` 输出 Markdown 表格** — 省 token，AI 据此选择工具
- **`schema` 输出 JSON** — 按需获取单个工具的完整参数定义
- **`call` 输出 JSON** — 业务数据保留结构，AI 精确读取字段
- **日志走 stderr** — 不干扰 stdout 结果数据
- **退出码语义化** — 0=成功，1=调用失败，2=连接失败
- **最少依赖** — 仅 1 个运行时依赖 (`eventsource-parser`)

## 安装

```bash
cd client
npm install

# 可选：注册为全局命令
npm link
```

要求 Node.js >= 18。

## CLI 使用

### 列出所有工具

```bash
yunxiao list
```

输出 Markdown 表格：

```
| Tool | Description |
|------|-------------|
| get_current_user | Get information about the current user... |
| search_projects | Search project list |
| ... | ... |
```

### 查看工具参数定义

```bash
yunxiao schema get_current_user
```

输出该工具的完整 JSON（含 `inputSchema`），AI agent 据此构造调用参数。

### 调用工具

```bash
# 命令行传参
yunxiao call get_current_user
yunxiao call search_projects '{"organizationId": "xxx", "perPage": 20}'

# 从 stdin 读取参数
echo '{"organizationId":"xxx"}' | yunxiao call search_projects --stdin

# 指定 MCP Server 地址
yunxiao --url http://10.0.0.1:3000 call get_current_user
```

输出 JSON 结果。

### 典型 AI agent 调用流程

```bash
# 1. 浏览工具列表，选定目标工具（低 token）
yunxiao list

# 2. 获取参数定义，构造参数（按需，单个工具）
yunxiao schema search_workitems

# 3. 执行调用，获取结果
yunxiao call search_workitems '{"organizationId":"xxx","spaceId":"yyy","category":"Req"}'
```

## API 使用

```js
import { createClient } from './src/index.mjs';

const client = await createClient('http://localhost:3000');

// 列出工具
const tools = client.listTools();

// 调用工具
const result = await client.callTool('search_workitems', {
  organizationId: '<org_id>',
  spaceId: '<project_id>',
  category: 'Req',
  perPage: 10,
});

console.log(JSON.stringify(result));

await client.close();
```

## 项目结构

```
client/
├── package.json
├── .env.example
├── README.md
├── examples/
│   └── demo.mjs           # 示例脚本
└── src/
    ├── index.mjs           # 模块导出
    ├── client.mjs          # MCP SSE 客户端核心
    └── cli.mjs             # CLI 入口
```

## MCP Server 部署

详见 [../DEPLOY.md](../DEPLOY.md)。
