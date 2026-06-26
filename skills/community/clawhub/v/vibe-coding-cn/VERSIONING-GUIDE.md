# Vibe Coding 版本管理指南

**版本**: v2.0  
**特性**: 版本管理 + 增量更新 + 需求演化追踪

---

## 🎯 核心理念

**Vibe Coding 的迭代式开发**：

```
传统开发：需求 → 开发 → 测试 → 上线（需求变更=灾难）

Vibe Coding: 
  v1.0: "做个个税计算器" 
      → 预览 
      → "不够专业" 
  v2.0: "做个专业的个税计算器" 
      → 预览 
      → "加上历史记录" 
  v3.0: "专业个税计算器 + 历史记录" 
      → ✅ 满意
```

---

## 📁 目录结构

```
output/
└── 个税计算器-20260406-a1b2/       # 项目 ID
    ├── project-meta.json            # 项目总元数据
    ├── v1.0/                        # 版本 1.0
    │   ├── version-meta.json        # 版本元数据
    │   ├── docs/
    │   ├── index.html
    │   └── app.js
    ├── v2.0/                        # 版本 2.0
    │   ├── version-meta.json
    │   ├── docs/
    │   ├── index.html
    │   └── app.js
    └── v3.0/                        # 版本 3.0（当前）
        ├── version-meta.json
        ├── docs/
        ├── index.html
        └── app.js
```

---

## 🚀 使用方式

### 方式一：首次创建项目

```javascript
const { run } = require('vibe-coding');

// 第一次创建
const result = await run('做个个税计算器');

console.log(result);
// {
//   projectId: '个税计算器 -20260406-a1b2',
//   version: 'v1.0',
//   projectDir: 'output/个税计算器 -20260406-a1b2',
//   files: [...],
//   isIncremental: false
// }
```

### 方式二：增量更新（基于上一版）

```javascript
// 第二次迭代 - 增量更新
const result2 = await run('做个更专业的个税计算器，像税务局官网那种风格', {
  projectId: '个税计算器 -20260406-a1b2',  // 指定项目
  parentVersion: 'v1.0'                     // 基于 v1.0 更新
});

console.log(result2);
// {
//   projectId: '个税计算器 -20260406-a1b2',
//   version: 'v2.0',                        // 新版本
//   isIncremental: true,                    // 增量更新
//   files: [...]
// }
```

### 方式三：带进度回调

```javascript
const result = await run('做个个税计算器', {
  onProgress: (phase, data) => {
    console.log(`[${phase}]`, data);
  }
});
```

---

## 📊 版本元数据

### project-meta.json（项目总览）

```json
{
  "projectId": "个税计算器 -20260406-a1b2",
  "createdAt": "2026-04-06T13:00:00.000Z",
  "currentVersion": "v3.0",
  "versions": [
    {
      "version": "v1.0",
      "requirement": "做个个税计算器",
      "timestamp": "2026-04-06T13:00:00.000Z",
      "status": "superseded",
      "fileCount": 5
    },
    {
      "version": "v2.0",
      "requirement": "做个更专业的个税计算器",
      "timestamp": "2026-04-06T13:08:00.000Z",
      "status": "superseded",
      "fileCount": 6
    },
    {
      "version": "v3.0",
      "requirement": "加上历史记录功能",
      "timestamp": "2026-04-06T13:16:00.000Z",
      "status": "current",
      "fileCount": 8
    }
  ],
  "requirementEvolution": [
    {
      "version": "v1.0",
      "requirement": "做个个税计算器",
      "timestamp": "2026-04-06T13:00:00.000Z"
    },
    {
      "version": "v2.0",
      "requirement": "做个更专业的个税计算器",
      "timestamp": "2026-04-06T13:08:00.000Z"
    },
    {
      "version": "v3.0",
      "requirement": "加上历史记录功能",
      "timestamp": "2026-04-06T13:16:00.000Z"
    }
  ]
}
```

### version-meta.json（版本详情）

```json
{
  "version": "v2.0",
  "requirement": "做个更专业的个税计算器，像税务局官网那种风格",
  "timestamp": "2026-04-06T13:08:00.000Z",
  "parentVersion": "v1.0",
  "changes": {
    "added": ["专业配色方案", "税率表格"],
    "modified": ["界面风格"],
    "unchanged": ["核心计算逻辑"]
  },
  "files": [
    {"name": "index.html", "size": 4567},
    {"name": "app.js", "size": 8901}
  ],
  "architecture": "...",
  "qualityScore": 88
}
```

---

## 🔄 增量更新流程

### Step 1: 分析需求变化

```javascript
const { IncrementalUpdater } = require('vibe-coding');

const updater = new IncrementalUpdater();

const plan = await updater.analyzeChanges(
  '做个个税计算器',                    // 旧需求
  '做个专业的个税计算器',              // 新需求
  {
    files: [...],                      // 旧版本文件列表
    architecture: '...'                // 旧版本架构
  }
);

console.log(plan);
// {
//   changeType: 'incremental',
//   requirementChanges: {...},
//   fileChanges: {
//     add: [...],
//     modify: [...],
//     keep: [...]
//   },
//   updateStrategy: {...}
// }
```

### Step 2: 用户确认

```javascript
console.log(updater.formatConfirmationMessage(plan));

// 输出：
// 📋 增量更新计划
// 
// 更新类型：🟢 增量更新
// 
// 需求变化:
// ➕ 新增：专业风格
// 🔄 修改：界面风格
// 
// 文件变更:
// ✏️  修改文件 (2):
//   - index.html
//     • 改用专业配色
//     • 添加税率表格
// ✅ 保持不变 (3)
// 
// 预计工作量：中（正常）
// 
// 确认开始更新？[确认] [修改计划]
```

### Step 3: 执行更新

```javascript
// 用户确认后执行
await run('做个专业的个税计算器', {
  projectId: '个税计算器 -001',
  parentVersion: 'v1.0'
});
```

---

## 🔍 版本对比

```javascript
const { VersionManager } = require('vibe-coding');

const vm = new VersionManager('./output');

// 对比 v1.0 和 v2.0
const diff = await vm.compareVersions(
  '个税计算器 -001',
  'v1.0',
  'v2.0'
);

console.log(diff);
// {
//   from: 'v1.0',
//   to: 'v2.0',
//   requirementChange: {
//     from: '做个个税计算器',
//     to: '做个专业的个税计算器'
//   },
//   filesChanged: {
//     added: [...],
//     removed: [...],
//     modified: [...]
//   }
// }
```

---

## ⏮️ 版本回退

```javascript
const vm = new VersionManager('./output');

// 回退到 v1.0（会创建新版本 v4.0）
const newVersion = await vm.revertToVersion(
  '个税计算器 -001',
  'v1.0'
);

console.log(`已回退到 ${newVersion}（内容是 v1.0 的副本）`);
```

---

## 📈 需求演化历史

```javascript
const vm = new VersionManager('./output');

const evolution = vm.getRequirementEvolution('个税计算器 -001');

console.log('需求演化史:');
evolution.forEach(e => {
  console.log(`${e.version}: ${e.requirement}`);
});

// 输出：
// 需求演化史:
// v1.0: 做个个税计算器
// v2.0: 做个专业的个税计算器
// v3.0: 加上历史记录功能
```

---

## 💡 最佳实践

### 1. 渐进式细化需求

```
❌ 不要：一次描述所有细节
✅ 要：先模糊后精确

v1.0: "做个个税计算器"
v2.0: "更专业的风格"
v3.0: "加上历史记录"
v4.0: "历史记录支持导出 Excel"
```

### 2. 保留满意的部分

```
❌ 不要：每次都完全重写
✅ 要：增量修改

"保留界面，加上历史记录功能"
"保持功能不变，优化配色"
```

### 3. 频繁迭代

```
❌ 不要：憋大招（等完美了再发布）
✅ 要：小步快跑

每 3-5 分钟一个版本
不满意立即调整
```

### 4. 记录演化历史

```
✅ 好处：
- 知道需求是怎么变化的
- 可以随时回退
- 理解用户的真实需求
```

---

## 🎯 完整示例

```javascript
const { run, VersionManager } = require('vibe-coding');

async function demo() {
  // v1.0: 初始版本
  console.log('🎨 创建 v1.0...');
  const v1 = await run('做个个税计算器');
  console.log(`✅ v1.0 完成 (${v1.version})`);
  
  // v2.0: 增量更新
  console.log('\\n🎨 更新 v2.0...');
  const v2 = await run('做个更专业的个税计算器', {
    projectId: v1.projectId,
    parentVersion: v1.version
  });
  console.log(`✅ v2.0 完成 (${v2.version})`);
  
  // v3.0: 再加功能
  console.log('\\n🎨 更新 v3.0...');
  const v3 = await run('加上历史记录功能', {
    projectId: v2.projectId,
    parentVersion: v2.version
  });
  console.log(`✅ v3.0 完成 (${v3.version})`);
  
  // 查看版本历史
  const vm = new VersionManager('./output');
  const project = await vm.loadOrCreateProject(v3.projectId, '');
  
  console.log('\\n📚 版本历史:');
  project.getVersions().forEach(v => {
    console.log(`  ${v.version}: ${v.requirement}`);
  });
}

demo();
```

---

**Happy Iterating! 🔄**
