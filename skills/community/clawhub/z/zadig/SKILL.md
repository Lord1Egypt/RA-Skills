---
name: zadig
description: ⚠️ 需要 ZADIG_API_URL + ZADIG_API_KEY | Zadig DevOps 平台 API 客户端
---

# Zadig Skill 

基于 Zadig OpenAPI 规范实现的 DevOps 平台客户端。

## 配置

必须配置以下环境变量（添加到 ~/.openclaw/workspace/.env）：

```bash
# 必填
ZADIG_API_URL=https://your-zadig.example.com
ZADIG_API_KEY=your-jwt-token

# 可选
ZADIG_DEFAULT_PROJECT=your-project
```

## 权限说明

- read:env - 读取 .env 文件获取 API 凭证
- network:https - 向 Zadig API 服务器发起请求

## 核心功能

- 项目管理
- 工作流管理  
- 环境管理
- 服务管理
- 构建管理
- 测试管理

## 使用示例

```javascript
const zadig = require('./skills/zadig');

// 列出项目
const { projects } = await zadig.listProjects();

// 触发工作流
await zadig.triggerWorkflow({
  projectKey: 'yaml',
  workflowKey: 'build',
  inputs: [...]
});

// ===== 便捷方法 =====

// 获取服务状态（一步到位）
const status = await zadig.getServiceStatus({
  projectKey: 'yaml',
  envName: 'dev',
  serviceName: 'service1'
});
/* 返回:
{
  service_name: 'service1',
  env_name: 'dev',
  status: 'Running',
  image: 'koderover.tencentcloudcr.com/test/service1:xxx',
  pod_name: 'service1-xxx-xxx',
  node: '172.16.64.16',
  ip: '172.16.64.132',
  ports: [{ containerPort: 20221, protocol: 'TCP' }],
  service_endpoints: [{ name: 'service1', service_port: 20221, node_port: 31331 }]
}
*/

// 获取服务日志（同步返回文本）
const logs = await zadig.getServiceLogsSync({
  projectKey: 'yaml',
  envName: 'dev',
  serviceName: 'service1',
  tailLines: 100
});
// 返回日志文本

// 获取工作流任务状态
const task = await zadig.getWorkflowTask({
  workflowKey: 'dev-build',
  taskId: 67
});
```

## 安全建议

1. 使用最小权限的 API Token
2. 不要将 API Key 提交到版本控制
