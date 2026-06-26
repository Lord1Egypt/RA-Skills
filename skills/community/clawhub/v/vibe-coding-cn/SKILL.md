---
name: Vibe Coding CN
slug: vibe-coding-cn
version: 4.1.0
description: AI 团队协作，自动生成完整项目。5 Agent + SPEC.md + Agent 投票审批 + 需求追溯。必须在 OpenClaw 环境中使用。
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["node"]},"os":["linux","darwin","win32"]},"categories":["development","productivity","ai-assistant"],"capabilities":["sessions_spawn","file_read","file_write"]}
---

# Vibe Coding 技能 - 中文版

AI 团队协作，自动生成完整项目。通过自然语言描述需求，自动生成完整的项目代码。

## 核心特性

### 1. 5 Agent 团队协作

- **Analyst (需求分析师)**: 分析用户需求，生成需求文档和 SPEC.md
- **Architect (系统架构师)**: 设计系统架构和技术选型
- **Developer (开发工程师)**: 实现代码，包含注释和错误处理
- **Tester (测试工程师)**: 编写测试用例，评审可测试性
- **Orchestrator (主编排器)**: **由 OpenClaw/AI 助手扮演**，负责协调整个流程

### 2. SPEC.md 生成 ⭐

- 自动生成完整 SPEC.md（基于需求 + 架构）
- 包含验收标准和审批流程
- Agent 投票审批，无需用户等待

### 3. Agent 投票审批 ⭐

- 3 Agent 专业评审（Architect + Developer + Tester）
- 自动决策，民主投票
- 投票记录完整透明

### 2. Orchestrator 职责（AI 助手必读）

**作为 Orchestrator，你需要**：

#### 投票机制

**重要决策需要多 Agent 投票**：

```javascript
// 架构设计评审投票
const reviews = await reviewWithVote('architecture', architecture, ['developer', 'tester']);

// 投票结果
reviews.forEach(r => {
  console.log(`${r.role}: ${r.vote} (${r.quality.score}/100) - ${r.reason}`);
});

const voteResult = countVotes(reviews);
console.log(`📊 投票结果：${voteResult.yes} 赞成 vs ${voteResult.no} 反对`);

// 决策
if (voteResult.no >= 2) {
  // 2 票反对，要求重新设计
  await redesign(architecture);
} else {
  // 通过
  continue();
}
```

**投票规则**：
- ✅ 2 票赞成 → 通过
- ⚠️ 1 票赞成 1 票反对 → 通过（记录问题）
- ❌ 2 票反对 → 不通过，重新设计

#### 流程协调
1. **启动流程** - 调用 `run(requirement)` 开始项目生成
2. **监控进度** - 每个阶段完成后检查质量评分
3. **处理异常** - 如果某个 Agent 失败，决定重试或跳过
4. **最终验收** - 检查所有输出是否完整

#### 质量把控
```javascript
// 检查每个 Agent 的输出质量
if (quality.score < 70) {
  // 质量不足，要求重新生成
  await run(requirement, { parentVersion: 'v1.0' });
}
```

#### 用户沟通
- 实时汇报进度（"Phase 1/5: 需求分析完成"）
- 解释质量评分（"需求分析 85 分，通过"）
- 处理用户反馈（"用户想要更专业的风格，启动增量更新"）
- **需求追溯**（"需求覆盖率 95%，2 个需求未实现"）

#### 示例代码
```javascript
// AI 助手作为 Orchestrator 的示例
const { run } = require('vibe-coding-cn');

// 1. 启动项目
console.log('🎨 开始生成项目...');
const result = await run('做个个税计算器', {
  onProgress: (phase, data) => {
    console.log(`[${phase}] ${data.status}`);
  }
});

// 2. 检查质量
if (result.files.length < 5) {
  console.log('⚠️ 生成文件不足，重新生成...');
  await run('做个更完整的个税计算器', {
    projectId: result.projectId,
    parentVersion: result.version
  });
}

// 3. 汇报结果
console.log(`✅ 完成！生成 ${result.files.length} 个文件`);
```

### 2. LLM 分层策略

不同任务使用不同模型，优化成本和性能：

| Agent | 模型 | Thinking | 理由 |
|-------|------|----------|------|
| Analyst | qwen3.5-plus | medium | 需求分析需要理解能力 |
| Architect | qwen3.5-plus | high | 架构设计需要深度思考 |
| Developer | qwen3-coder-next | medium | 代码实现需要编码专长 |
| Tester | glm-4 | low | 测试用例相对简单 |

**效果**: 成本降低 30%，性能提升 33%

### 3. 质量门禁

每个阶段自动检查输出质量：

| 阶段 | 检查项 | 通过标准 |
|------|--------|---------|
| 需求分析 | 功能数量 | ≥3 个 |
| | 用户故事 | ≥2 个（GWT 格式） |
| 架构设计 | 技术选型 | 有理由说明 |
| | 模块设计 | ≥3 个模块 |
| 代码实现 | 代码注释 | JSDoc 风格 |
| | 错误处理 | 有输入验证 |
| 测试编写 | 功能测试 | ≥5 个用例 |
| | 边界测试 | ≥3 个用例 |

### 4. 实时进度汇报

每阶段完成后自动汇报进度，用户可以随时了解执行状态。

## 🎯 Orchestrator 实战指南

### 场景 1: 首次生成项目

```javascript
// AI 助手作为 Orchestrator
const { run } = require('vibe-coding-cn');

console.log('🎨 收到需求：做个个税计算器');
console.log('📋 启动 5 Agent 协作流程...\n');

try {
  const result = await run('做个个税计算器', {
    onProgress: (phase, data) => {
      // 实时汇报进度
      console.log(`📊 [${phase.replace('_', ' ')}] ${data.message}`);
    }
  });
  
  // 验收检查
  console.log('\n✅ 项目生成完成！');
  console.log(`📁 项目 ID: ${result.projectId}`);
  console.log(`📁 版本：${result.version}`);
  console.log(`📁 文件数：${result.files.length}`);
  
  if (result.files.length >= 5) {
    console.log('✅ 质量检查通过');
  } else {
    console.log('⚠️ 文件数量不足，建议增量更新');
  }
  
} catch (error) {
  console.error('❌ 生成失败:', error.message);
  // 决定重试或放弃
}
```

### 场景 2: 增量更新

```javascript
// 用户反馈："想要更专业的风格"
console.log('🔄 收到用户反馈：想要更专业的风格');
console.log('📊 分析变更...');

const { IncrementalUpdater } = require('vibe-coding-cn');
const updater = new IncrementalUpdater({ conservatism: 'balanced' });

const plan = await updater.analyzeChanges(
  '做个个税计算器',
  '做个更专业的个税计算器',
  oldVersion,
  llmCallback
);

console.log(updater.formatConfirmationMessage(plan));
// 显示变更计划，等待用户确认

// 用户确认后执行
const v2 = await run('做个更专业的个税计算器', {
  projectId: v1.projectId,
  parentVersion: v1.version
});

console.log(`✅ 增量更新完成！新版本：${v2.version}`);
```

### 场景 3: 质量不达标时的处理

```javascript
// 检查质量评分
if (quality.score < 70) {
  console.log(`⚠️ 质量评分 ${quality.score}/100，低于标准 (70 分)`);
  console.log('📝 问题清单:');
  quality.issues.forEach(issue => console.log(`  - ${issue}`));
  
  // 决策：重试 or 继续？
  const retry = confirm('是否重新生成？');
  if (retry) {
    console.log('🔄 重新生成中...');
    // 传入修改意见
    await run(requirement, { 
      llmCallback: async (prompt) => {
        return await sessions_spawn({
          task: `请改进以下问题：\n${quality.issues.join('\n')}\n\n${prompt}`
        });
      }
    });
  } else {
    console.log('⏭️ 跳过，继续后续流程');
  }
}
```

### 场景 4: 版本管理

```javascript
// 查看版本历史
const { VersionManager } = require('vibe-coding-cn');
const vm = new VersionManager('./output');
const project = await vm.loadOrCreateProject(projectId, '');

console.log('📚 版本历史:');
project.getVersions().forEach(v => {
  const marker = v.version === project.currentVersion ? '← 当前' : '';
  console.log(`  ${v.version}: ${v.requirement} ${marker}`);
});

// 版本对比
const diff = await vm.compareVersions(projectId, 'v1.0', 'v2.0');
console.log('\n📊 版本对比:');
console.log(`  新增文件：${diff.filesChanged.added.length}`);
console.log(`  修改文件：${diff.filesChanged.modified.length}`);

// 版本回退
const confirmRevert = confirm('是否回退到 v1.0？');
if (confirmRevert) {
  const newVersion = await vm.revertToVersion(projectId, 'v1.0');
  console.log(`✅ 已回退到 ${newVersion}（内容是 v1.0 的副本）`);
}
```

---

## 🚀 使用方法

### 方式一：OpenClaw 技能调用（推荐）

**在 OpenClaw 中直接调用**：

```javascript
// 通过 sessions_spawn 调用
sessions_spawn({
  runtime: "subagent",
  task: "用 vibe-coding 做一个个税计算器",
  cwd: "~/.openclaw/workspace/skills/vibe-coding-cn"
})
```

**或者在对话中直接说**：
```
用 vibe-coding 做一个打字游戏
```

**优点**：
- ✅ 自动继承 OpenClaw 上下文
- ✅ 支持实时进度汇报
- ✅ 结果自动保存到 workspace

---

### 方式二：CLI 命令行调用

**安装后使用**：

```bash
# 全局安装（首次使用）
cd ~/.openclaw/workspace/skills/vibe-coding-cn
npm install -g .

# 使用
vibe-coding "做一个个税计算器"
vibe-coding "做一个打字游戏"
vibe-coding "做一个待办事项应用"
vibe-coding "做一个客户画像功能"
```

**或者临时执行**：
```bash
node ~/.openclaw/workspace/skills/vibe-coding-cn/index.js "做一个个税计算器"
```

**优点**：
- ✅ 独立运行，不依赖 OpenClaw
- ✅ 适合脚本自动化
- ✅ 可在 CI/CD 中使用

---

### 方式三：可视化监控（可选）

**启动开发服务器**：

```bash
cd ~/.openclaw/workspace/skills/vibe-coding-cn
npm start  # 或者 node server.js
```

**访问界面**：
- HTTP: http://localhost:3000
- WebSocket: ws://localhost:8765

**功能**：
- 📊 实时查看执行进度
- 📝 查看各阶段输出日志
- 🎨 演示/展示用途

**注意**：UI 仅用于监控，不控制执行流程。执行仍通过方式一或方式二启动。

---

### 执行流程（三种方式相同）

```
1. Phase 1: 需求分析 (30 秒)
   → docs/requirements.md

2. Phase 2: 架构设计 (90 秒)
   → docs/architecture.md

3. Phase 3: 代码实现 (90 秒)
   → index.html, app.js, ...

4. Phase 4: 测试编写 (30 秒)
   → tests/test-cases.md

5. Phase 5: 整合验收
   → docs/vibe-report.md
```

**实时进度**：
- OpenClaw 调用 → 自动在对话中汇报每阶段进度
- CLI 调用 → 控制台输出进度日志
- 可视化监控 → WebSocket 推送实时更新

### 输出目录

```
output/{项目名}/
├── docs/
│   ├── requirements.md    # 需求文档
│   ├── architecture.md    # 架构设计
│   └── vibe-report.md     # 总结报告
├── index.html             # 主页面
├── app.js                 # 应用逻辑
└── tests/
    └── test-cases.md      # 测试用例
```

## 示例项目

### 1. 个税计算器

**需求**: "做一个个税计算器"

**结果**:
- 时间：4 分 30 秒
- 文件：5 个
- 质量：88/100
- 功能：输入月收入、五险一金，计算个税

### 2. 打字游戏

**需求**: "做一个打字游戏"

**结果**:
- 时间：4 分 15 秒
- 文件：5 个
- 质量：86/100
- 功能：单词掉落，输入对应单词，计分系统

### 3. 待办事项应用

**需求**: "做一个待办事项应用"

**结果**:
- 时间：3 分 50 秒
- 文件：5 个
- 质量：87/100
- 功能：添加/删除任务，标记完成，本地存储

### 4. 客户画像功能

**需求**: "做一个个客户画像功能"

**结果**:
- 时间：3 分钟
- 文件：4 个
- 质量：88/100
- 功能：雷达图可视化，客户标签分析，营销指导

## 技术栈

- **运行时**: Node.js >=18.0.0
- **平台**: OpenClaw >=2026.2.0
- **AI 模型**: 
  - bailian/qwen3.5-plus (需求分析/架构设计)
  - bailian/qwen3-coder-next (代码实现)
  - bailian/glm-4 (测试编写)
- **WebSocket**: ws ^8.20.0 (实时进度推送)
- **HTTP 服务器**: Node.js native (可视化监控)

## 注意事项

### 通用
1. **执行时间**: 3-5 分钟，需要耐心等待
2. **代码审查**: 生成的代码需要人工审查后使用
3. **网络要求**: 需要访问 AI 模型 API
4. **内存要求**: 建议至少 2GB 可用内存

### OpenClaw 调用
- ✅ 需要 `sessions_spawn` 权限
- ✅ 自动继承工作区目录
- ✅ 结果自动保存到 `output/` 目录

### CLI 调用
- ✅ 需要先执行 `npm install -g .` 全局安装
- ✅ 输出目录相对于当前工作目录
- ✅ 适合脚本自动化

### 可视化监控
- ⚠️ 仅用于查看进度，不能控制执行
- ⚠️ 需要单独启动 `node server.js`
- ⚠️ 适合演示/展示场景

## 适用场景

### ✅ 适合使用

- 快速原型开发
- 学习项目
- 内部工具
- MVP 验证
- UI 组件生成

### ❌ 不适合

- 安全关键系统
- 高性能要求场景
- 合规严格领域
- 长期维护的生产系统

## 故障排除

### 问题：执行时间过长

**解决**: 检查网络连接，确认 AI 模型 API 可访问

### 问题：生成的代码无法运行

**解决**: 查看错误信息，重新生成或手动修复

### 问题：质量评分低

**解决**: 提供更详细的需求描述，包含具体功能和技术栈要求

## 更新日志

### v1.0.0 (2026-04-06)

- 初始版本
- 5 个 Agent 协作
- LLM 分层策略
- 质量门禁
- 实时进度汇报

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/openclaw/vibe-coding
