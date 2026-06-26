# react-orchestrator

**ReAct 推理框架** - 双系统 AI 代理协调器（System 1 快速执行 + System 2 深度推理）

## 描述

基于 ReAct (Reason+Act) 框架和 Reflexion 自我反思机制，实现智能任务路由和分层推理：

- **System 1**: 快速直觉执行 (~3-5s)，适合简单查询、事实检索、单步工具调用
- **System 2**: 深度反思推理 (~10-15s)，适合复杂规划、多步推理、战略决策

自动评估任务复杂度，智能选择执行模式，最大化效率与质量的平衡。

## 功能

- ✅ **双系统架构**: System 1 (快速) + System 2 (深度) 自动切换
- ✅ **ReAct 循环**: Reason → Action → Observe → Repeat
- ✅ **Reflexion 反思**: 定期自我反思，调整策略，纠错优化
- ✅ **工具注册中心**: 统一注册、发现、执行外部技能
- ✅ **复杂度评估**: 基于关键词和语义自动判断任务难度
- ✅ **超时保护**: System 1 (30s) / System 2 (120s) 超时控制
- ✅ **执行历史**: 完整记录推理过程，支持审计和调试
- ✅ **语义工具匹配**: 基于关键词智能匹配可用工具

## 安装

```bash
# 从 ClawHub 安装（待发布）
clawhub install react-orchestrator

# 或手动克隆
git clone https://github.com/YOUR_GITHUB/skills/react-orchestrator
cd skills/react-orchestrator
npm install
```

## 快速开始

### 基础使用

```javascript
const { ReActOrchestrator } = require('./src/orchestrator');

// 创建协调器
const orchestrator = new ReActOrchestrator({
  complexityThreshold: 0.6,  // 复杂度阈值
  system1Timeout: 30,        // System 1 超时 (秒)
  system2Timeout: 120,       // System 2 超时 (秒)
  verbose: true,             // 详细日志
});

// 注册工具
orchestrator.registerTool('tavily-search', async (params) => {
  // 搜索实现
  return { results: [...] };
}, {
  description: '联网搜索工具',
  keywords: ['搜索', '查找', '调研', 'search'],
  timeout: 10,
});

// 执行任务（自动选择 System 1/2）
const result = await orchestrator.execute('搜索最新的 AI agent 发展趋势');
console.log(result.answer);
console.log(`执行模式：${result.mode}, 耗时：${result.duration}s, 迭代：${result.iterations}`);
```

### 强制模式

```javascript
// 强制使用 System 1（快速）
const fast = await orchestrator.execute('今天天气如何？', { mode: 'system1' });

// 强制使用 System 2（深度）
const deep = await orchestrator.execute('分析 AI 行业趋势并给出投资建议', { mode: 'system2' });
```

### 集成现有技能

```javascript
const { ReActOrchestrator } = require('react-orchestrator');
const { TavilySearch } = require('tavily-search');
const { RAGRetriever } = require('rag-retriever');

const orchestrator = new ReActOrchestrator();

// 注册 Tavily 搜索
const search = new TavilySearch({ apiKey: process.env.TAVILY_API_KEY });
orchestrator.registerTool('tavily-search', 
  (params) => search.search(params.query),
  {
    description: 'Tavily 联网搜索',
    keywords: ['搜索', '查找', '调研', '最新', '新闻'],
  }
);

// 注册 RAG 检索
const rag = new RAGRetriever();
orchestrator.registerTool('rag-retrieve',
  (params) => rag.retrieve(params.query),
  {
    description: '本地知识库检索',
    keywords: ['文档', '知识', '记忆', '检索'],
  }
);

// 执行复杂任务
const result = await orchestrator.execute('调研 MCP 协议的最新发展，并检索本地笔记中的相关记录');
// 自动使用 System 2，依次调用 tavily-search 和 rag-retrieve
```

## 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `complexityThreshold` | number | `0.6` | 任务复杂度阈值 (0-1)，超过则使用 System 2 |
| `system1Timeout` | number | `30` | System 1 超时秒数 |
| `system2Timeout` | number | `120` | System 2 超时秒数 |
| `maxIterationsSystem1` | number | `5` | System 1 最大迭代次数 |
| `maxIterationsSystem2` | number | `15` | System 2 最大迭代次数 |
| `verbose` | boolean | `false` | 是否输出详细日志 |
| `model` | string | `'qwen3.5-plus'` | 使用的 LLM 模型 |
| `temperature` | number | `0.3/0.7` | System 1=0.3, System 2=0.7 |

## API 参考

### ReActOrchestrator

#### `constructor(options)`
创建协调器实例。

#### `registerTool(name, fn, metadata)`
注册单个工具。
- `name`: 工具名称
- `fn`: 执行函数 `(params) => Promise<result>`
- `metadata`: 元数据（description, keywords, paramSchema, timeout）

#### `registerTools(tools)`
批量注册工具。`[{name, fn, metadata}, ...]`

#### `execute(query, options)`
执行 ReAct 推理。
- `query`: 用户查询
- `options.mode`: `'auto'|'system1'|'system2'`
- `options.timeout`: 覆盖默认超时
- 返回：`{answer, history, mode, iterations, duration}`

#### `evaluateComplexity(query)`
评估任务复杂度。
- 返回：`{mode, score, reasons}`

#### `getAvailableTools()`
获取已注册工具列表。

#### `exportHistory(history)`
导出执行历史（JSON 格式）。

### ToolRegistry

#### `register(name, fn, metadata)`
注册工具。

#### `get(name)`
获取工具。

#### `list()`
列出所有工具名称。

#### `match(query, limit)`
语义匹配工具。

## 执行流程

```
用户查询
    ↓
[复杂度评估] → score > 0.6? → System 2
    ↓                       ↓
  score ≤ 0.6              初始规划
    ↓                       ↓
System 1                 ReAct 循环
    ↓                    (最多 15 次)
ReAct 循环                   ↓
(最多 5 次)              定期反思
    ↓                    (每 3 次迭代)
最终答案                   ↓
    ↓                调整计划/继续
    └──────→ 最终答案 ←────┘
```

## 测试

```bash
npm test
```

测试覆盖：
- ✅ 工具注册与发现
- ✅ System 1 快速执行
- ✅ System 2 深度推理
- ✅ Reflexion 反思机制
- ✅ 超时保护
- ✅ 错误处理

## 使用场景

### 适合 System 1 的任务
- 事实查询："今天北京天气如何？"
- 简单搜索："搜索 Python 教程"
- 单步操作："读取文件 contents.md"
- 快速计算："123 * 456 = ?"

### 适合 System 2 的任务
- 复杂分析："分析 AI 行业趋势并给出投资建议"
- 多步规划："帮我创建一个完整的 Node.js 项目，包括测试和文档"
- 战略决策："评估是否应该迁移到 MCP 架构"
- 创造性任务："设计一个多智能体协作系统"

## 已知限制

- ⚠️ **LLM 集成**: 当前版本使用启发式规则模拟 Reason 阶段，需接入真实 LLM
- ⚠️ **参数提取**: 工具参数提取为简化实现，需 LLM 支持
- ⚠️ **语义匹配**: 工具匹配基于关键词，未来升级为向量相似度
- ⚠️ **记忆管理**: 长期记忆集成待完善（可结合 ontology 技能）

## 依赖

- Node.js >= 18.0.0
- zod (可选，用于参数验证)

## 版本历史

### v0.1.0 (2026-03-18)
- ✅ 初始版本
- ✅ 双系统架构实现
- ✅ ReAct + Reflexion 循环
- ✅ 工具注册中心
- ✅ 基础测试套件

## 许可证

MIT

## 作者

余永浩 (蒲萄爸)

## 贡献

欢迎提交 Issue 和 PR！
