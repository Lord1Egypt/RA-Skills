---
name: tool-registry
description: >
  工具注册与发现系统。基于Token匹配的工具路由，支持权限控制和子代理工具白名单。
  当用户说"工具有哪些"、"搜索工具"、"查找技能"、"工具路由"时触发。
---

# Tool Registry - 工具注册与发现系统

## 核心概念

```
用户输入 → Token提取 → 匹配工具 → 权限过滤 → 返回结果
              ↓
         权重打分排序
```

## 工具注册表结构

```javascript
const registry = new ToolRegistry();

registry.register({
  name: 'read_file',
  aliases: ['read', 'cat'],        // 别名（短名称）
  description: '读取文件内容',
  permission: 'read',              // 权限级别
  agentTypes: ['explore', 'plan'], // 允许的子代理类型
  keywords: ['file', 'read', '文本'], // 搜索关键词
  execute: async (input) => { ... }
});

registry.register({
  name: 'bash',
  aliases: ['shell', 'exec'],
  description: '执行Shell命令',
  permission: 'danger',
  agentTypes: ['verification'],    // 只有验证代理能用
  keywords: ['shell', 'bash', '命令', '执行'],
  execute: async (input) => { ... }
});
```

## 权限级别

| 级别 | 值 | 说明 |
|------|-----|------|
| `read` | 1 | 只读文件/网络 |
| `write` | 2 | 写入文件 |
| `danger` | 3 | 危险操作（bash等） |
| `admin` | 4 | 完全权限 |

## 子代理类型

| 类型 | 允许的工具 | 典型用途 |
|------|----------|---------|
| `explore` | read, glob, grep, web_fetch | 文件探索 |
| `plan` | read, todo, search | 规划分析 |
| `verification` | bash, read, assert | 验证测试 |
| `general` | 全部 | 通用任务 |

## Token 匹配算法

```javascript
// 输入: "读取文件 test.py"
// Token化: ['读取', '文件', 'test.py']
// 匹配: read_file, file_read, cat 等
// 得分: 命中次数 + 位置权重 + 别名加权
// 排序: 得分从高到低
```

| 匹配位置 | 权重 |
|---------|------|
| 别名匹配 | ×2 |
| 关键词匹配 | ×1 |
| 描述匹配 | ×0.5 |

## API 使用

```javascript
const { ToolRegistry } = require('./scripts/tool-registry.mjs');

// 创建注册表
const registry = new ToolRegistry();

// 注册工具
registry.register({
  name: 'read_file',
  aliases: ['read', 'cat'],
  description: '读取文件内容',
  permission: 'read',
  agentTypes: ['explore', 'plan', 'general'],
  keywords: ['file', 'read', 'open'],
  execute: async (ctx, input) => {
    return { success: true, content: '...' };
  }
});

// 搜索工具（Token匹配）
const matches = registry.search('读文件');
// 返回: [{tool, score, matchType}] 数组

// 获取工具
const tool = registry.get('read_file');

// 按权限过滤
const allowedTools = registry.filterByPermission(currentPermission);

// 按代理类型过滤
const agentTools = registry.filterByAgentType('explore');

// 执行工具
const result = await registry.execute('read_file', { path: 'test.py' });
```

## 内置过滤器

```javascript
// 权限不足过滤器
registry.withPermissionFilter(userLevel);

// 代理类型过滤器
registry.withAgentFilter(agentType);

// 组合过滤器
registry.withFilters({
  permission: 'write',
  agentType: 'plan',
  exclude: ['dangerous_tool']
});
```

## 文件结构

```
tool-registry/
├── SKILL.md              # 本文件
└── scripts/
    └── tool-registry.mjs # 核心注册表实现
```

---

_龙虾王子自我进化的成果 🦞_
