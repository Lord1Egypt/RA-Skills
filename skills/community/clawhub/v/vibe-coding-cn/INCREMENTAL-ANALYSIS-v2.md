# 增量分析优化 v2.0

**优化日期**: 2026-04-06  
**版本**: v2.0  
**核心改进**: 分层次分析 + 变更影响链 + 保守度控制

---

## 🎯 优化目标

**v1.0 的问题**：
- ❌ 只分析文件名，不了解文件内容
- ❌ 扁平化分析，没有层次结构
- ❌ 无法追踪变更如何传播
- ❌ 一刀切的分析策略

**v2.0 的改进**：
- ✅ 分层次分析（需求 → 架构 → 文件 → 代码）
- ✅ 变更影响链（修改 A 会影响哪些依赖）
- ✅ 保守度控制（保守/平衡/激进）
- ✅ 文件内容感知（分析内容摘要）

---

## 📊 四层分析架构

### Layer 1: 需求层分析

**目标**: 理解需求变更的本质

```javascript
输入:
- 旧需求："做个个税计算器"
- 新需求："做个更专业的个税计算器"

分析维度:
1. 语义相似度评分 (0-100)
2. 需求变化分类（新增/修改/删除/保持）
3. 变更意图推断（用户真正想要什么）
4. 模糊点识别（需要澄清的术语）

输出:
{
  "similarityScore": 75,
  "changeCategories": {
    "added": [...],
    "modified": [...],
    "deleted": [...],
    "unchanged": [...]
  },
  "userIntent": {
    "primaryIntent": "风格调整",
    "description": "用户希望界面更专业正式"
  },
  "ambiguities": [
    {
      "term": "专业",
      "possibleInterpretations": ["正式配色", "详细数据", "官方风格"],
      "needsClarification": true
    }
  ]
}
```

---

### Layer 2: 架构层分析

**目标**: 评估需求变更对架构的影响

```javascript
输入:
- 需求变更分析结果
- 当前架构描述

分析维度:
1. 架构影响评估（无影响/局部/重大/重构）
2. 模块变更映射
3. 影响传播链（修改 A → 影响 B → 影响 C）
4. 架构风险点

输出:
{
  "impact": "local",
  "moduleChanges": [
    {
      "module": "UI 组件层",
      "changeType": "修改",
      "impactLevel": "medium",
      "reason": "需要调整配色方案",
      "dependencies": ["样式模块"]
    }
  ],
  "riskPoints": [
    {
      "risk": "配色调整可能影响可读性",
      "severity": "low",
      "mitigation": "保留对比度检查"
    }
  ]
}
```

---

### Layer 3: 文件层分析

**目标**: 将变更映射到具体文件

```javascript
输入:
- 需求变更分析
- 架构影响分析
- 当前文件列表（含内容摘要）

分析维度:
1. 文件级变更映射（新增/修改/保持）
2. 修改内容细化（具体改哪里）
3. 依赖关系检查
4. 保守度策略应用

输出:
{
  "add": [
    {
      "file": "src/styles/professional-theme.css",
      "reason": "新增专业配色主题",
      "relatedRequirement": "更专业的风格",
      "estimatedLines": 150,
      "complexity": "low"
    }
  ],
  "modify": [
    {
      "file": "src/index.html",
      "reason": "应用新主题",
      "changes": [
        {
          "location": "<head> 部分",
          "changeType": "调整样式",
          "description": "引入专业主题 CSS",
          "complexity": "low"
        }
      ],
      "relatedRequirements": ["更专业的风格"],
      "riskLevel": "low",
      "estimatedChangePercent": 15
    }
  ],
  "keep": [
    {
      "file": "src/calculator.js",
      "reason": "核心计算逻辑无需修改"
    }
  ],
  "dependencyChain": [
    {
      "source": "src/index.html",
      "affects": ["src/styles/professional-theme.css"],
      "requiresSync": true
    }
  ]
}
```

---

### Layer 4: 整合生成

**目标**: 综合三层分析，生成完整更新计划

```javascript
输入:
- 需求层分析结果
- 架构层分析结果
- 文件层分析结果

处理:
1. 确定变更类型（incremental/major/rewrite）
2. 整合更新策略
3. 计算置信度
4. 收集风险点

输出:
{
  "changeType": "incremental",
  "updateStrategy": {
    "approach": "incremental",
    "reason": "需求基本一致（相似度 75%），主要是局部调整",
    "riskPoints": ["..."],
    "estimatedEffort": "low",
    "confidence": 0.85
  },
  // ... 合并三层分析结果
}
```

---

## 🎛️ 保守度控制

### 三种策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| **保守** 🟢 | 尽量保留现有代码，只在必要时修改 | 用户对现有功能满意，只想小修小补 |
| **平衡** 🟡 | 适度修改，在保留和重构之间取得平衡 | 默认策略，大多数场景 |
| **激进** 🔴 | 大胆重构，如果更好的设计就果断修改 | 用户对现有代码不满意，希望彻底改进 |

### 使用方式

```javascript
// 保守策略
const updater = new IncrementalUpdater({
  conservatism: 'conservative'
});

// 平衡策略（默认）
const updater = new IncrementalUpdater();

// 激进策略
const updater = new IncrementalUpdater({
  conservatism: 'aggressive'
});
```

### 保守度如何影响分析

**保守策略**：
```
用户："加上历史记录功能"

分析结果:
- add: ["src/history.js", "src/history-ui.html"]
- modify: []  ← 尽量不修改现有文件
- keep: ["src/calculator.js", "src/index.html"]
```

**激进策略**：
```
用户："加上历史记录功能"

分析结果:
- add: ["src/history.js"]
- modify: [
    "src/calculator.js",  ← 重构计算器，集成历史记录
    "src/index.html",     ← 重新设计布局
    "src/app.js"          ← 重构应用架构
  ]
- keep: []
```

---

## 📈 置信度评估

### 置信度计算因素

| 因素 | 影响 |
|------|------|
| 需求清晰度 | 模糊需求 → 降低置信度 |
| 语义相似度 | 差异过大 → 降低置信度 |
| 文件信息完整度 | 缺少内容摘要 → 降低置信度 |
| 架构信息完整度 | 缺少架构描述 → 降低置信度 |

### 置信度的用途

```javascript
if (plan.confidence < 0.5) {
  console.log('⚠️ 置信度较低，建议先澄清需求');
  console.log('模糊点:', plan.ambiguities);
  // 暂停，等待用户确认
}
```

---

## 🔍 变更影响链

### 为什么要追踪影响链？

**问题场景**：
```
用户："修改按钮颜色"

v1.0 分析:
- modify: ["button.css"]  ← 只修改 CSS

实际问题:
- 按钮组件有 JS 事件监听颜色变化
- 只改 CSS 会导致功能异常
```

**v2.0 解决方案**：
```
v2.0 分析:
- modify: ["button.css"]
- dependencyChain: [
    {
      "source": "button.css",
      "affects": ["button.js"],  ← 检测到 JS 依赖
      "requiresSync": true
    }
  ]

建议:
"修改 button.css 后，建议检查 button.js 中的颜色相关逻辑"
```

---

## 📋 使用示例

### 示例 1: 基本增量更新

```javascript
const { IncrementalUpdater } = require('./executors/incremental-updater');

const updater = new IncrementalUpdater();

const plan = await updater.analyzeChanges(
  '做个个税计算器',
  '做个更专业的个税计算器',
  {
    files: [
      { name: 'index.html', size: 1234, type: 'html' },
      { name: 'calculator.js', size: 5678, type: 'javascript' }
    ],
    architecture: 'MVC 架构：View(index.html) + Model(calculator.js) + Controller(app.js)'
  }
);

console.log(updater.formatConfirmationMessage(plan));
```

### 示例 2: 带保守度控制

```javascript
const updater = new IncrementalUpdater({
  conservatism: 'conservative',  // 保守策略
  model: 'qwen3.5-plus',
  thinking: 'high'
});

const plan = await updater.analyzeChanges(...);
```

### 示例 3: 处理模糊需求

```javascript
if (plan.ambiguities.length > 0) {
  console.log('⚠️ 检测到模糊点，建议澄清：');
  plan.ambiguities.forEach(a => {
    console.log(`  "${a.term}" 可能指：${a.possibleInterpretations.join(' 或 ')}`);
  });
  
  // 等待用户澄清后再继续
  const clarification = await getUserClarification();
  // 重新分析...
}
```

---

## 🎯 输出质量对比

### v1.0 vs v2.0

| 维度 | v1.0 | v2.0 |
|------|------|------|
| **分析层次** | 扁平 | 四层（需求/架构/文件/整合） |
| **文件感知** | 仅文件名 | 文件名 + 类型 + 摘要 |
| **依赖追踪** | ❌ 无 | ✅ 影响链 |
| **保守度** | ❌ 固定 | ✅ 可配置 |
| **置信度** | ❌ 无 | ✅ 量化评估 |
| **模糊点识别** | ❌ 无 | ✅ 主动提示 |
| **变更分类** | 粗粒度 | 细粒度（新增/修改/删除/保持） |
| **用户意图** | ❌ 无 | ✅ 推断意图 |

---

## 🚀 性能优化

### 缓存策略

```javascript
// 相同需求变更，直接返回缓存结果
const cacheKey = `${oldReq}|${newReq}|${hash(files)}`;
if (cache.has(cacheKey)) {
  return cache.get(cacheKey);
}
```

### 分层缓存

```javascript
// 需求层分析结果可复用
if (reqCache.has(reqKey)) {
  reqAnalysis = reqCache.get(reqKey);
} else {
  reqAnalysis = await analyzeRequirementLayer(...);
  reqCache.set(reqKey, reqAnalysis);
}
```

---

## 📊 评估指标

### 分析质量指标

| 指标 | 计算方式 | 目标值 |
|------|---------|-------|
| **准确率** | 用户确认"分析正确"的比例 | ≥85% |
| **模糊点识别率** | 成功识别模糊需求的比例 | ≥90% |
| **影响链覆盖率** | 正确追踪依赖的比例 | ≥80% |
| **置信度校准** | 高置信度=高准确率 | ≥85% |

### 用户满意度

```javascript
// 每次分析后收集反馈
const feedback = await getUserFeedback(plan);
// { accurate: true, helpful: true, suggestions: [...] }
```

---

**优化完成！下一步：测试验证 + UI 集成**
