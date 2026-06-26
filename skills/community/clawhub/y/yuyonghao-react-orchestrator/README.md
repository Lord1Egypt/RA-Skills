# ReAct Orchestrator 🧠

**双系统 AI 代理协调器** - 基于 ReAct + Reflexion 框架的智能推理引擎

> System 1 快速执行 (~3-5s) + System 2 深度推理 (~10-15s) = 效率与质量的最佳平衡

## 🎯 核心理念

受人类认知双系统理论启发：

| 特性 | System 1 | System 2 |
|------|----------|----------|
| **速度** | 快速 (~3-5s) | 慢速 (~10-15s) |
| **迭代** | 最多 5 次 | 最多 15 次 |
| **适用** | 简单查询、事实检索 | 复杂规划、多步推理 |
| **反思** | 无 | Reflexion 自我纠错 |
| **温度** | 0.3 (确定性) | 0.7 (创造性) |

## 📦 安装

```bash
cd skills/react-orchestrator
npm install
```

## 🚀 快速开始

### 1. 基础示例

```javascript
const { ReActOrchestrator } = require('./src/orchestrator');

const orchestrator = new ReActOrchestrator({ verbose: true });

// 注册工具
orchestrator.registerTool('echo', 
  (params) => `Echo: ${params.message}`,
  {
    description: '回声测试工具',
    keywords: ['测试', 'echo'],
  }
);

// 执行任务
const result = await orchestrator.execute('测试一下这个系统');
console.log(result.answer);
```

### 2. 集成真实技能

```javascript
const { ReActOrchestrator } = require('react-orchestrator');
const { TavilySearch } = require('tavily-search');

const orchestrator = new ReActOrchestrator();

// 注册 Tavily 搜索
const search = new TavilySearch({ apiKey: 'tvly-xxx' });
orchestrator.registerTool('search',
  (params) => search.search(params.query, { limit: 5 }),
  {
    description: '联网搜索最新信息',
    keywords: ['搜索', '查找', '调研', '最新', '趋势'],
  }
);

// 自动选择 System 1/2
const result = await orchestrator.execute('搜索 2026 年 AI agent 最新发展');
console.log(`模式：${result.mode}, 耗时：${result.duration}s`);
```

### 3. 强制模式

```javascript
// 强制快速模式
const fast = await orchestrator.execute('2+2=?', { mode: 'system1' });

// 强制深度模式
const deep = await orchestrator.execute('分析 AI 行业并给出投资建议', { mode: 'system2' });
```

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    ReAct Orchestrator                   │
│  • 复杂度评估                                           │
│  • 模式选择 (System 1 / System 2)                       │
│  • 工具注册中心                                         │
└─────────────────────────────────────────────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌─────────────────┐
│   System 1      │      │   System 2      │
│   (快速执行)     │      │   (深度推理)     │
├─────────────────┤      ├─────────────────┤
│ • max 5 迭代     │      │ • max 15 迭代    │
│ • 无反思         │      │ • Reflexion     │
│ • 30s 超时       │      │ • 120s 超时      │
└─────────────────┘      └─────────────────┘
         │                        │
         └──────────┬─────────────┘
                    ▼
         ┌───────────────────┐
         │   Tool Registry   │
         ├───────────────────┤
         │ • tavily-search   │
         │ • rag-retriever   │
         │ • mcp-client      │
         │ • 自定义工具...   │
         └───────────────────┘
```

## 🔄 ReAct 循环

### System 1 流程
```
查询 → Reason → Action → Observe → [循环≤5 次] → 答案
```

### System 2 流程
```
查询 → 规划 → [Reason → Action → Observe] → 反思 → [循环≤15 次] → 答案
                ↑_______________↓
                    每 3 次迭代反思
```

## 📊 复杂度评估

自动分析查询决定使用哪个系统：

```javascript
const assessment = await orchestrator.evaluateComplexity('分析 AI 行业趋势');
console.log(assessment);
// {
//   mode: 'system2',
//   score: 0.83,
//   reasons: ['multiStep', 'openEnded', 'knowledgeIntensive']
// }
```

评估维度：
- 多步推理信号（然后、接着、分步骤）
- 条件/分支信号（如果、否则、假设）
- 创造性/开放性（分析、评估、比较、设计）
- 知识密集型（最新、趋势、研究）
- 技术操作（代码、编程、调试）
- 查询长度（>100 字符）

## 🛠️ 工具注册

### 注册单个工具

```javascript
orchestrator.registerTool('weather',
  async (params) => {
    const response = await fetch(`https://wttr.in/${params.city}?format=j1`);
    return await response.json();
  },
  {
    description: '查询天气预报',
    keywords: ['天气', '温度', '预报', 'weather'],
    paramSchema: {
      type: 'object',
      properties: {
        city: { type: 'string', description: '城市名称' }
      },
      required: ['city']
    },
    timeout: 10,
  }
);
```

### 批量注册

```javascript
orchestrator.registerTools([
  {
    name: 'search',
    fn: (params) => tavily.search(params.query),
    metadata: { description: '搜索', keywords: ['搜索'] }
  },
  {
    name: 'retrieve',
    fn: (params) => rag.retrieve(params.query),
    metadata: { description: '检索', keywords: ['文档', '知识'] }
  }
]);
```

## 📝 执行结果

```javascript
const result = await orchestrator.execute('调研 MCP 协议');

console.log(result);
// {
//   answer: '根据搜索结果...',
//   history: [
//     {
//       iteration: 1,
//       thought: '使用 tavily-search 搜索 MCP 协议',
//       action: 'tavily-search',
//       params: { query: 'MCP 协议' },
//       observation: '...',
//       timestamp: 1710756000000
//     }
//   ],
//   mode: 'system2',
//   iterations: 5,
//   duration: 8.42,
//   reflections: [...]
// }
```

## 🧪 测试

```bash
npm test
```

测试覆盖：
- ✅ 工具注册与发现
- ✅ 复杂度评估
- ✅ System 1 执行
- ✅ System 2 执行
- ✅ Reflexion 反思
- ✅ 超时保护
- ✅ 错误处理

## 🔧 配置

```javascript
new ReActOrchestrator({
  complexityThreshold: 0.6,    // 复杂度阈值
  system1Timeout: 30,          // System 1 超时 (秒)
  system2Timeout: 120,         // System 2 超时 (秒)
  maxIterationsSystem1: 5,     // System 1 最大迭代
  maxIterationsSystem2: 15,    // System 2 最大迭代
  verbose: true,               // 详细日志
  model: 'qwen3.5-plus',       // LLM 模型
});
```

## 🎯 使用场景

### System 1 (快速)
- ✅ "今天北京天气？"
- ✅ "搜索 Python 教程"
- ✅ "读取文件 config.json"
- ✅ "123 * 456 = ?"

### System 2 (深度)
- ✅ "分析 AI 行业趋势并给出投资建议"
- ✅ "创建完整的 Node.js 项目，包括测试和文档"
- ✅ "评估是否应该迁移到 MCP 架构"
- ✅ "设计多智能体协作系统"

## ⚠️ 已知限制

- **LLM 集成**: 当前使用启发式规则，需接入真实 LLM
- **参数提取**: 简化实现，需 LLM 支持
- **语义匹配**: 基于关键词，未来升级为向量相似度

## 📚 参考资料

- [ReAct Paper](https://arxiv.org/abs/2210.03629) - Reason+Act 协同
- [Reflexion Paper](https://arxiv.org/abs/2303.11366) - 自我反思学习
- [ria-19/ai_agent](https://github.com/ria-19/ai_agent) - 双系统实现参考
- [LangGraph ReAct](https://github.com/webup/langgraph-up-react) - LangGraph 模板

## 📄 许可证

MIT
