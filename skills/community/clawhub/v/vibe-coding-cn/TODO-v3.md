# Vibe Coding v3.0 优化清单

**更新日期**: 2026-04-06  
**当前状态**: 核心功能完成，待优化细节

---

## ✅ 已完成的功能

| 功能 | 文件 | 状态 | 测试 |
|------|------|------|------|
| **版本管理器** | `executors/version-manager.js` | ✅ 完成 | ✅ 100% 通过 |
| **增量分析器 v3.0** | `executors/incremental-updater.js` | ✅ 完成 | ✅ OpenClaw 集成 |
| **缓存系统** | `executors/analysis-cache.js` | ✅ 完成 | ✅ LRU + 分层 |
| **LLM 客户端** | `executors/llm-client.js` | ✅ 完成 | ✅ 备用方案 |
| **UI v2.0** | `ui/vibe-dashboard-v2.html` | ✅ 完成 | ⏳ 待集成 |
| **测试套件** | `test-*.js` (4 个文件) | ✅ 完成 | ✅ 全部通过 |

---

## 🔧 需要优化的问题

### P0 - 高优先级

#### 1. vibe-executor 的 OpenClaw 集成

**问题**: `vibe-executor.js` 直接调用 `sessions_spawn`，没有降级方案

**当前代码**:
```javascript
// ❌ 硬编码依赖
const result = await sessions_spawn({...});
```

**优化方案**:
```javascript
// ✅ 支持传入 llmCallback
async function callAgent(agentType, prompt, options = {}) {
  const { llmCallback } = options;
  
  if (llmCallback) {
    // 使用 OpenClaw LLM
    return await llmCallback(prompt, this.model);
  } else if (typeof sessions_spawn !== 'undefined') {
    // OpenClaw 环境
    const result = await sessions_spawn({...});
    return result.output;
  } else {
    // 降级：抛出错误或返回模拟
    throw new Error('需要 OpenClaw 环境或传入 llmCallback');
  }
}
```

**影响**: 不修复的话，vibe-executor 只能在 OpenClaw 中运行

---

#### 2. 完整的端到端测试

**问题**: 缺少完整的 5 Agent 协作测试

**需要测试**:
```javascript
// 在 OpenClaw 环境中
const { run } = require('vibe-coding-cn');

// 定义 LLM 回调
async function callOpenClawLLM(prompt, model) {
  const result = await sessions_spawn({
    runtime: 'subagent',
    task: prompt,
    model
  });
  return result.output;
}

// 完整测试
const v1 = await run('做个个税计算器', {
  llmCallback: callOpenClawLLM
});

const v2 = await run('做个更专业的计算器', {
  projectId: v1.projectId,
  parentVersion: v1.version,
  llmCallback: callOpenClawLLM
});
```

**预期结果**:
- v1.0: 生成 5 个文件（需求/架构/代码/测试/报告）
- v2.0: 增量更新，保留核心逻辑，修改 UI

---

#### 3. 文档整合

**问题**: 文档分散在多个文件

**当前文档**:
- `SKILL.md` - 技能说明
- `QUICKSTART.md` - 快速开始
- `VERSIONING-GUIDE.md` - 版本管理
- `INCREMENTAL-ANALYSIS-v2.md` - 增量分析
- `OPENCLAW-INTEGRATION.md` - OpenClaw 集成
- `OPTIMIZATION-SUMMARY.md` - 优化总结

**优化方案**: 整合为一份主文档
```
README.md (主文档)
├── 快速开始
├── 使用方法
│   ├── OpenClaw 集成
│   ├── 版本管理
│   └── 增量更新
├── API 参考
├── 示例
└── FAQ
```

---

### P1 - 中优先级

#### 4. UI 集成到 server.js

**问题**: `vibe-dashboard-v2.html` 是静态文件，没有连接到后端

**需要实现**:
```javascript
// server.js 添加 API 路由
app.post('/api/analyze', async (req, res) => {
  const { requirement, parentVersion } = req.body;
  
  const updater = new IncrementalUpdater();
  const plan = await updater.analyzeChanges(
    oldReq, requirement, oldVersion,
    callOpenClawLLM  // 传入 LLM 回调
  );
  
  res.json({ plan });
});

app.post('/api/execute', async (req, res) => {
  const { requirement, options } = req.body;
  const result = await run(requirement, {
    ...options,
    llmCallback: callOpenClawLLM
  });
  res.json({ result });
});
```

---

#### 5. 保守度策略的实际效果验证

**问题**: 三种保守度策略（conservative/balanced/aggressive）的输出差异未验证

**需要测试**:
```javascript
for (const strategy of ['conservative', 'balanced', 'aggressive']) {
  const plan = await updater.analyzeChanges(req, req2, files, llmCallback, {
    conservatism: strategy
  });
  
  console.log(`${strategy}:`);
  console.log(`  新增文件：${plan.fileChanges.add.length}`);
  console.log(`  修改文件：${plan.fileChanges.modify.length}`);
}
```

**预期差异**:
- conservative: 新增 1 个，修改 0-1 个
- balanced: 新增 1-2 个，修改 1-2 个
- aggressive: 新增 2+ 个，修改 3+ 个

---

### P2 - 低优先级

#### 6. 性能优化

**当前性能**:
- 增量分析（无缓存）: ~3000ms（3 次 LLM 调用）
- 增量分析（有缓存）: ~50ms

**优化空间**:
- [ ] 并行调用 LLM（需求层/架构层/文件层可并行）
- [ ] 缓存持久化（保存到磁盘）
- [ ] 预热点分析（常见需求变更模式）

---

#### 7. 错误处理增强

**当前问题**:
- LLM 调用失败时降级逻辑不够完善
- 没有重试机制

**优化方案**:
```javascript
async function analyzeWithRetry(prompt, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await llmCallback(prompt);
    } catch (error) {
      if (i === retries - 1) throw error;
      console.log(`LLM 失败，重试 ${i + 1}/${retries}`);
      await sleep(1000 * (i + 1)); // 指数退避
    }
  }
}
```

---

## 📋 下一步行动计划

### 本周（2026-04-06 ~ 2026-04-12）

- [ ] **P0-1**: 修复 vibe-executor 的 OpenClaw 集成
- [ ] **P0-2**: 完成完整的端到端测试（5 Agent 协作）
- [ ] **P0-3**: 整合文档为一份 README

### 下周（2026-04-13 ~ 2026-04-19）

- [ ] **P1-4**: UI 集成到 server.js
- [ ] **P1-5**: 验证保守度策略效果
- [ ] **P2-6**: 性能优化（并行调用）

### 下下周（2026-04-20 ~ 2026-04-26）

- [ ] **P2-7**: 错误处理增强
- [ ] 发布到 ClawHub v3.0
- [ ] 编写使用教程

---

## 🎯 成功标准

### 功能完整性
- [ ] 版本管理 100% 可用
- [ ] 增量分析 100% 可用（OpenClaw LLM）
- [ ] 5 Agent 协作 100% 可用
- [ ] UI 界面可实际使用

### 性能指标
- [ ] 增量分析（有缓存）: <100ms
- [ ] 完整项目生成：3-5 分钟
- [ ] 缓存命中率：>80%

### 用户体验
- [ ] 文档清晰完整
- [ ] 示例丰富（5+ 个）
- [ ] 错误提示友好
- [ ] 支持中文需求

---

## 📊 当前进度

```
核心功能：████████████████████ 100%
版本管理：████████████████████ 100%
增量分析：████████████████████ 100%
缓存系统：████████████████████ 100%
OpenClaw 集成：████████████████░░░░ 80%
UI 集成：░░░░░░░░░░░░░░░░░░░░   0%
文档整合：████░░░░░░░░░░░░░░░░  20%
端到端测试：████████░░░░░░░░░░░  40%
```

**总体进度**: ~75%

---

**下一步**: 优先修复 P0 问题，然后进行完整端到端测试
