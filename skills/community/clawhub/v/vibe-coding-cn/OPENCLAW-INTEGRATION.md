# Vibe Coding OpenClaw 集成指南

**版本**: v3.0  
**核心改进**: 使用 OpenClaw 的 LLM 能力，不直接调用 API

---

## 🎯 核心设计理念

**v3.0 关键变更**：
- ❌ 不再直接调用 DashScope API
- ✅ 使用 OpenClaw 的 `sessions_spawn` 或传入的 LLM 回调
- ✅ 复用 OpenClaw 已有的模型配置和 API 密钥
- ✅ 支持两种模式：OpenClaw 集成 / 独立测试

---

## 📋 使用方式

### 方式一：在 OpenClaw 对话中使用（推荐）

**直接在对话中说**：
```
用 vibe-coding 做一个个税计算器
```

**OpenClaw 会自动**：
1. 调用 `sessions_spawn` 创建子 Agent
2. 传递 LLM 回调函数
3. 执行 vibe-coding 流程

---

### 方式二：在 OpenClaw 技能中调用

```javascript
// 在 OpenClaw 会话中
const { run } = require('./skills/vibe-coding-cn/index.js');

// 定义 LLM 回调（使用 OpenClaw 的模型）
async function callOpenClawLLM(prompt, model, thinking) {
  // 使用 OpenClaw 的 sessions_spawn 调用子 Agent
  const result = await sessions_spawn({
    runtime: 'subagent',
    task: `请分析以下问题并返回 JSON 格式的回答：\n\n${prompt}`,
    model: model || 'qwen3.5-plus',
    thinking: thinking || 'medium'
  });
  
  return result.output; // 或根据实际返回结构调整
}

// 执行 vibe-coding（带增量分析）
const result = await run('做个更专业的个税计算器', {
  projectId: '个税计算器 -001',
  parentVersion: 'v1.0',
  llmCallback: callOpenClawLLM,  // 传入 OpenClaw LLM 回调
  onProgress: (phase, data) => {
    console.log(`[${phase}]`, data);
  }
});
```

---

### 方式三：CLI 独立使用（测试模式）

```bash
# 不依赖 OpenClaw，使用模拟分析
node index.js "做个个税计算器"
```

**注意**：CLI 模式下增量分析使用启发式规则，不是真实 LLM 分析。

---

## 🔄 OpenClaw 集成架构

```
┌─────────────────────────────────────────┐
│  OpenClaw Gateway                        │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ 主会话 (Main Session)              │ │
│  │                                     │ │
│  │ 用户："用 vibe-coding 做个计算器"   │ │
│  │         ↓                          │ │
│  │ 调用 run(requirement, {            │ │
│  │   llmCallback: callOpenClawLLM     │ │
│  │ })                                 │ │
│  └────────────────────────────────────┘ │
│                    ↓                     │
│  ┌────────────────────────────────────┐ │
│  │ 子 Agent (sessions_spawn)          │ │
│  │                                     │ │
│  │ IncrementalUpdater.analyzeChanges()│ │
│  │   ↓                                │ │
│  │ llmCallback(prompt, model)         │ │
│  │   ↓                                │ │
│  │ OpenClaw LLM (qwen3.5-plus)        │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## 🔌 LLM 回调函数示例

### 示例 1: 使用 sessions_spawn

```javascript
async function callOpenClawLLM(prompt, model, thinking) {
  const result = await sessions_spawn({
    runtime: 'subagent',
    task: `请分析以下问题并返回 JSON 格式的回答：\n\n${prompt}`,
    model: model || 'qwen3.5-plus',
    thinking: thinking || 'medium',
    timeoutSeconds: 300
  });
  
  // 提取 JSON
  const jsonMatch = result.output.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    return JSON.parse(jsonMatch[0]);
  }
  throw new Error('LLM 响应格式错误');
}
```

### 示例 2: 使用 OpenClaw 内置工具（如果可用）

```javascript
// 如果 OpenClaw 提供内置 LLM 工具
async function callOpenClawLLM(prompt, model, thinking) {
  const response = await gateway.tool('llm.generate', {
    prompt,
    model,
    parameters: {
      temperature: thinking === 'high' ? 0.9 : 0.7,
      max_tokens: 8192
    }
  });
  
  return response.text;
}
```

### 示例 3: 使用 sessions_send（简单场景）

```javascript
async function callOpenClawLLM(prompt, model, thinking) {
  // 发送到专门的 LLM 会话
  const result = await sessions_send({
    sessionKey: 'llm-session',
    message: `请用 JSON 格式回答：${prompt}`,
    timeoutSeconds: 120
  });
  
  return result.message;
}
```

---

## 📊 增量分析流程（OpenClaw 集成）

```
1. 用户输入新需求
   "做个更专业的个税计算器"
   ↓
2. 检测增量更新模式
   parentVersion: "v1.0"
   ↓
3. 调用 IncrementalUpdater.analyzeChanges()
   ↓
4. LLM 回调 → sessions_spawn → OpenClaw LLM
   ↓
5. 需求层分析（调用 LLM）
   - 语义相似度评分
   - 需求变化分类
   - 用户意图推断
   ↓
6. 架构层分析（调用 LLM）
   - 架构影响评估
   - 模块变更映射
   ↓
7. 文件层分析（调用 LLM）
   - 文件级变更映射
   - 依赖关系检查
   ↓
8. 生成更新计划
   ↓
9. 显示确认消息
   "📋 增量更新计划..."
   ↓
10. 用户确认 → 执行更新
```

---

## 🎛️ 配置选项

### 完整配置示例

```javascript
const result = await run('做个更专业的个税计算器', {
  // 项目配置
  projectId: '个税计算器 -001',
  parentVersion: 'v1.0',
  
  // LLM 配置
  llmCallback: callOpenClawLLM,  // OpenClaw LLM 回调
  model: 'qwen3.5-plus',         // 模型（可选）
  thinking: 'high',              // 思考级别（可选）
  
  // 保守度配置
  conservatism: 'balanced',      // conservative | balanced | aggressive
  
  // 输出配置
  outputDir: './output',
  
  // 进度回调
  onProgress: (phase, data) => {
    console.log(`[${phase}]`, data);
  }
});
```

### 保守度选项

| 选项 | 说明 | 适用场景 |
|------|------|---------|
| `conservative` | 尽量保留现有代码 | 小修小补 |
| `balanced` | 适度修改（默认） | 大多数场景 |
| `aggressive` | 大胆重构 | 大幅改进 |

---

## 🧪 测试模式

**不使用 OpenClaw LLM 时**（测试/演示）：

```javascript
// 不传 llmCallback，使用模拟分析
const result = await run('做个更专业的计算器', {
  projectId: '个税计算器 -001',
  parentVersion: 'v1.0'
  // 不传 llmCallback → 使用启发式规则
});
```

**模拟分析特点**：
- ✅ 快速（不调用 API）
- ✅ 无需配置
- ⚠️ 基于关键词匹配，不是真实 LLM 分析
- ⚠️ 适合测试流程，不适合生产

---

## 📋 完整示例

```javascript
/**
 * OpenClaw 中使用 vibe-coding 的完整示例
 */
async function demoInOpenClaw() {
  // 1. 定义 LLM 回调
  async function callOpenClawLLM(prompt, model, thinking) {
    const result = await sessions_spawn({
      runtime: 'subagent',
      task: `请分析并返回 JSON：\n\n${prompt}`,
      model: model || 'qwen3.5-plus',
      thinking: thinking || 'high'
    });
    
    const jsonMatch = result.output.match(/\{[\s\S]*\}/);
    return jsonMatch ? JSON.parse(jsonMatch[0]) : null;
  }
  
  // 2. 创建 v1.0
  console.log('🎨 创建 v1.0...');
  const v1 = await run('做个个税计算器');
  
  // 3. 增量更新 v2.0（使用 OpenClaw LLM）
  console.log('\n🎨 增量更新 v2.0...');
  const v2 = await run('做个更专业的个税计算器', {
    projectId: v1.projectId,
    parentVersion: v1.version,
    llmCallback: callOpenClawLLM,  // 使用 OpenClaw LLM
    conservatism: 'balanced'
  });
  
  // 4. 增量更新 v3.0
  console.log('\n🎨 增量更新 v3.0...');
  const v3 = await run('加上历史记录功能', {
    projectId: v2.projectId,
    parentVersion: v2.version,
    llmCallback: callOpenClawLLM
  });
  
  // 5. 查看版本历史
  console.log('\n📚 版本历史:');
  console.log(`  v1.0: ${v1.requirement}`);
  console.log(`  v2.0: ${v2.requirement}`);
  console.log(`  v3.0: ${v3.requirement}`);
  
  return { v1, v2, v3 };
}
```

---

## ⚠️ 注意事项

### 1. LLM 回调是可选的

```javascript
// 有 llmCallback → 真实 LLM 分析
await run('需求', { llmCallback: myLLM });

// 无 llmCallback → 模拟分析
await run('需求');
```

### 2. OpenClaw 会话管理

```javascript
// 确保 sessions_spawn 在当前会话可用
// 如果不在 OpenClaw 环境中，会报错
```

### 3. 错误处理

```javascript
try {
  const plan = await updater.analyzeChanges(..., llmCallback);
} catch (error) {
  // LLM 调用失败时，降级到模拟分析
  console.log('LLM 失败，使用模拟分析');
  const plan = updater.generateMockAnalysis(...);
}
```

### 4. 超时设置

```javascript
// 建议设置超时，避免长时间等待
const result = await sessions_spawn({
  timeoutSeconds: 300  // 5 分钟
});
```

---

## 🔍 调试技巧

### 查看 LLM 调用

```javascript
async function callOpenClawLLM(prompt, model, thinking) {
  console.log('🤖 LLM 调用:');
  console.log(`  Model: ${model}`);
  console.log(`  Thinking: ${thinking}`);
  console.log(`  Prompt: ${prompt.substring(0, 100)}...`);
  
  const result = await sessions_spawn({...});
  
  console.log('✅ LLM 响应:', result.output.substring(0, 100) + '...');
  return result.output;
}
```

### 检查分析结果

```javascript
const plan = await updater.analyzeChanges(..., llmCallback);
console.log('📊 分析结果:', JSON.stringify(plan, null, 2));
```

---

**集成完成！在 OpenClaw 中直接使用即可。**
