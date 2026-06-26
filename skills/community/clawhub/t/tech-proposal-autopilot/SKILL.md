---
name: tech-proposal-autopilot
description: 技术方案书全自动写作 - 多智能体协作、断点续作、完全自动化
version: 1.0.0
author: David
created: 2026-03-23
tags:
  - automation
  - multi-agent
  - document-generation
  - tech-proposal
  - writing
requires:
  binaries: []
  env: []
  agents:
    - milo
    - josh
    - dev
    - marketing
verified:
  - name: 深圳市数据流通利用基础设施项目
    words: 150000
    chapters: 10
    status: completed
  - name: 智慧养老餐饮综合服务平台
    words: 200000
    chapters: 18
    status: completed
  - name: 工业互联网与智能制造平台
    words: 310000
    chapters: 12
    status: completed
---

# 技术方案书全自动写作技能

**版本**: 1.0.0  
**创建日期**: 2026-03-23  
**作者**: David

## 概述

本技能实现**技术方案书全自动写作**，核心特性：

- ✅ **多智能体协作**：多个智能体分工协作，并行/顺序生成章节
- ✅ **断点自动续作**：上下文超限时自动续作，无需人工干预
- ✅ **进度持久化**：所有进度保存到文件，支持跨会话恢复
- ✅ **完全自动化**：从启动到合并输出，全程无人工干预

## 快速开始

### 1. 启动新项目

```
请使用技术方案书自动写作技能，为"XXX项目"生成技术方案书。

要求：
- 规模：约30万字，18个章节
- 参考资料：[附上参考资料路径或URL]

章节大纲：
1. 第1章标题
2. 第2章标题
...
```

### 2. 监控进度

```
查看当前技术方案书项目进度
```

### 3. 手动续作（如需要）

```
继续执行技术方案书项目
```

## 核心流程

```
┌─────────────────────────────────────────────────────────┐
│              Phase 0: 项目初始化                          │
├─────────────────────────────────────────────────────────┤
│  1. 创建项目目录: projects/{project-name}/                │
│  2. 生成 outline.md (章节大纲)                            │
│  3. 提取 reference-keypoints.md (参考资料压缩)            │
│  4. 创建 progress.json (进度追踪)                         │
│  5. 创建 CONTINUE.md (续作指令)                           │
│  6. 设置 status="in_progress", autoContinue=true         │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│         Phase 1-N: 分章节生成 (循环执行)                   │
├─────────────────────────────────────────────────────────┤
│  for chapter in chapters:                                │
│    ├─ spawn 新 session (独立上下文)                       │
│    ├─ 加载: outline.md + progress.json                   │
│    ├─ 加载: reference-keypoints.md (如存在)              │
│    ├─ 生成: chapter-N.md                                  │
│    ├─ 保存文件 → 更新 progress.json                       │
│    ├─ 检查上下文使用率                                     │
│    │   └─ 如果 > 70%: 提前结束，设置待续作标记             │
│    └─ 结束 session (释放上下文)                           │
│                                                          │
│  自动续作触发条件:                                        │
│  ├─ 心跳检查 (用户交互时)                                 │
│  ├─ Cron 定时检查 (每5分钟)                               │
│  └─ 智能体主动请求 (上下文接近上限时)                      │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│           Phase Final: 合并输出                           │
├─────────────────────────────────────────────────────────┤
│  1. 检查所有章节是否完成                                   │
│  2. 合并所有 chapter-N.md → final.md                      │
│  3. 生成目录和章节编号                                     │
│  4. 更新 status="completed"                               │
│  5. 通知用户完成                                          │
└─────────────────────────────────────────────────────────┘
```

## 核心文件结构

```
projects/{project-name}/
├── progress.json          # 进度追踪 (核心)
├── outline.md             # 章节大纲
├── reference-keypoints.md # 参考资料压缩版 (可选)
├── CONTINUE.md            # 续作指令
├── chapter-01.md          # 第1章内容
├── chapter-02.md          # 第2章内容
├── ...                    # 更多章节
├── final.md               # 最终合并输出
└── logs/                  # 执行日志
    ├── chapter-01.log
    ├── chapter-02.log
    └── ...
```

## progress.json 格式

```json
{
  "project": "项目名称",
  "totalChapters": 18,
  "totalWords": 300000,
  "completed": ["chapter-01", "chapter-02"],
  "current": "chapter-03",
  "status": "in_progress",
  "autoContinue": true,
  "agents": {
    "chapter-01": "milo",
    "chapter-02": "josh",
    "chapter-03": "milo"
  },
  "wordCounts": {
    "chapter-01": 15000,
    "chapter-02": 18000
  },
  "chapters": {
    "chapter-01": {
      "title": "章节标题",
      "agent": "milo",
      "targetWords": 15000,
      "status": "completed",
      "words": 15500,
      "startedAt": "2026-03-23T09:00:00",
      "completedAt": "2026-03-23T09:15:00"
    }
  },
  "startTime": "2026-03-23T09:00:00",
  "lastUpdate": "2026-03-23T09:30:00"
}
```

## CONTINUE.md 格式

```markdown
# 续作指令

## 项目信息
- **项目路径**: /path/to/project
- **项目名称**: 项目名称
- **当前状态**: in_progress

## 续作任务
- **当前章节**: chapter-N
- **负责智能体**: {agent-name}
- **目标字数**: {words}

## 执行指令
1. 读取 progress.json 获取当前进度
2. 读取 outline.md 获取章节大纲
3. 读取 reference-keypoints.md (如果存在)
4. 生成当前章节内容
5. 保存为 chapter-N.md
6. 更新 progress.json
7. 继续下一章节或结束

## 注意事项
- 每章独立会话，上下文从零开始
- 仅加载必要文件
- 完成后更新进度文件
- 遵循段落优先写作规范

## 生成时间
{timestamp}
```

## 自动续作机制

### 核心原理：文件触发器模式

**关键创新**：通过文件触发器实现会话间通信，无需人工介入

```
会话A（即将超限）          会话B（自动续作）
        │                         │
        ├─ 创建 .trigger-continue │
        │                         │
        ├─ 更新 CONTINUE.md ─────→│
        │                         │
        ├─ 结束会话               │
        │                         │
        │    Cron/心跳检查         │
        │         ↓               │
        │    发现触发文件         │
        │         ↓               │
        │←──── spawn 新会话 ──────┤
        │                         │
        │                    读取指令
        │                    生成章节
        │                    更新进度
        │                    删除触发文件
```

### 三重触发机制

| 触发方式 | 频率 | 代码位置 | 优先级 | 触发条件 |
|---------|------|---------|--------|---------|
| **心跳检查** | 用户交互时 | HEARTBEAT.md | 高 | 用户发送消息 |
| **Cron 定时** | 每5分钟 | Cron job | 中 | 定时触发 |
| **主动请求** | 即时 | 智能体内部 | 最高 | 上下文>70% |

### 心跳检查实现

在 HEARTBEAT.md 中添加：

```markdown
### 技术方案书项目检查 (自动续作)

- 扫描 projects/*/progress.json
- 筛选 status="in_progress" 且 autoContinue=true
- 对每个未完成项目:
  - 检查当前章节是否超时 (>30分钟无更新)
  - 如果超时: spawn 续作会话
  - 如果未超时: 检查是否有下一章节待执行
- 记录到日志: ~/.openclaw/logs/tech-proposal-monitor.log
```

### Cron 配置

```bash
# 每5分钟检查一次未完成项目
*/5 * * * * openclaw run-task tech-proposal-check
```

或通过 OpenClaw cron 工具配置：

```json
{
  "name": "tech-proposal-auto-continue",
  "schedule": { "kind": "every", "everyMs": 300000 },
  "payload": {
    "kind": "agentTurn",
    "message": "检查未完成的技术方案书项目并自动续作"
  },
  "sessionTarget": "isolated"
}
```

### 智能体主动请求

每个智能体在生成章节时，定期检查上下文使用率：

```javascript
// 伪代码
if (contextUsage > 70%) {
  // 1. 保存当前进度
  await saveProgress();
  
  // 2. 创建续作触发文件
  const triggerData = {
    triggeredAt: new Date().toISOString(),
    currentChapter: currentChapter,
    completedChapters: completed.length,
    totalChapters: totalChapters,
    agent: nextAgent,
    reason: 'context_limit'
  };
  fs.writeFileSync('.trigger-continue', JSON.stringify(triggerData));
  
  // 3. 更新续作指令文件
  fs.writeFileSync('CONTINUE.md', generateContinueInstructions());
  
  // 4. 结束当前会话（Cron 会自动接管）
  return { needContinue: true, triggeredBy: 'context_limit' };
}
```

### 续作执行器工作流程

**文件**: `continue-executor.js`

```javascript
// 1. 扫描所有项目
for (const projectDir of projectsDirs) {
  const progress = readJSON(projectDir + '/progress.json');
  
  // 2. 检查是否需要续作
  if (progress.status !== 'in_progress') continue;
  if (!progress.autoContinue) continue;
  
  // 3. 检查触发条件
  const hasTrigger = exists(projectDir + '/.trigger-continue');
  const isTimeout = (now - progress.lastUpdate) > 30分钟;
  
  if (hasTrigger || isTimeout) {
    // 4. 读取续作指令
    const instructions = read(projectDir + '/CONTINUE.md');
    const nextChapter = findNextChapter(progress);
    const agent = progress.agents[nextChapter];
    
    // 5. spawn 续作会话
    spawn({
      agent: agent,
      task: instructions,
      runtime: 'subagent'
    });
  }
}
```

### 关键文件说明

| 文件 | 创建时机 | 读取时机 | 作用 |
|------|---------|---------|------|
| `.trigger-continue` | 上下文超限 | Cron/心跳检查 | 触发续作的信号 |
| `CONTINUE.md` | 创建项目/超限时 | 续作会话 | 续作指令 |
| `progress.json` | 每章完成后 | 续作会话 | 进度追踪 |

### 完全自动化流程

```
用户启动项目
      ↓
Phase 0: 初始化
  ├─ 创建项目目录
  ├─ 生成 outline.md
  ├─ 创建 progress.json (autoContinue=true)
  └─ 创建 CONTINUE.md
      ↓
Phase 1-N: 章节生成
  ├─ spawn 会话 (智能体A)
  ├─ 生成章节内容
  ├─ 检查上下文 → 如果>70%:
  │    ├─ 创建 .trigger-continue
  │    ├─ 更新 CONTINUE.md
  │    └─ 结束会话
  ├─ 更新 progress.json
  └─ 继续或结束
      ↓
自动续作（由 Cron 接管）
  ├─ 检测到 .trigger-continue
  ├─ spawn 会话 (智能体B)
  ├─ 读取 CONTINUE.md
  ├─ 生成下一章节
  ├─ 更新 progress.json
  └─ 删除 .trigger-continue
      ↓
Phase Final: 合并输出
  └─ 所有章节完成 → 合并 → final.md
```

**全程无人工干预！**

## 智能体分工策略

### 默认分工规则

| 智能体 | 擅长领域 | 适合章节 |
|--------|---------|---------|
| **milo** | 架构设计、技术深度 | 系统架构、核心技术、AI系统 |
| **josh** | 政策分析、安全保障 | 政策环境、安全体系、实施保障 |
| **dev** | 技术实现、系统集成 | 核心系统、平台开发、接口设计 |
| **marketing** | 商业分析、投资估算 | 投资估算、效益分析、商业模式 |

### 自动分配算法

```javascript
function assignAgent(chapter, outline) {
  const keywords = {
    milo: ['架构', '系统设计', 'AI', '大数据', '智能决策'],
    josh: ['政策', '安全', '保障', '实施', '运维'],
    dev: ['平台', '系统', '接口', '数据采集', '感知'],
    marketing: ['投资', '效益', '商业模式', '成本']
  };
  
  // 匹配关键词
  for (const [agent, words] of Object.entries(keywords)) {
    if (words.some(w => chapter.title.includes(w))) {
      return agent;
    }
  }
  
  // 默认轮询分配
  const agents = ['milo', 'josh', 'dev', 'marketing'];
  return agents[chapter.index % agents.length];
}
```

## 写作规范

### 段落优先原则

**核心规则**：
- 标题层级最多到 `###`，禁止 `####` 及更深
- 每个标题后至少1段（100-200字）才能出下一个标题
- 每个大节（##）开头必须有概括性段落
- 列表占比不超过章节内容的 30%

**正确示例**：

```markdown
## 2.1 国家政策环境

国家城市安全战略是指导城市生命线安全监测系统建设的根本遵循。近年来，党中央、国务院高度重视城市安全工作，出台了一系列政策文件，为系统建设提供了明确方向和有力保障。

### 2.1.1 国家安全战略

国家安全战略将城市安全纳入总体布局，强调城市运行安全是国家安全的重要组成部分。这一战略定位为城市生命线安全监测系统建设提供了顶层设计和政策支撑。
```

**错误示例**：

```markdown
## 2.1 国家政策环境
### 2.1.1 国家安全战略
#### 2.1.1.1 战略定位
- 要点一
- 要点二
```

### System Prompt 片段

在生成章节时，智能体的 system prompt 中应包含：

```
写作风格要求：
采用论述式写作，段落优先。每个小标题下先用2-3段连贯的自然语言阐述背景、原理或意义，再适当使用列表补充要点。标题层级不超过三级（###），每个标题后必须有实质内容段落（100-200字以上）。列表占比不超过30%。
```

## 上下文管理

### GLM-5 上下文策略

**限制**：GLM-5 上下文约 50K tokens

**策略**：
- 每章独立会话，上下文从零开始
- 仅加载必要文件：outline.md、当前章节信息、上一章摘要
- 不加载完整章节内容，仅加载关键数据
- 参考资料压缩 80%后再加载

**上下文预估**：
- outline.md：约 5K tokens
- reference-keypoints.md：约 10K tokens
- 上一章摘要：约 2K tokens
- 生成内容：约 20K tokens
- **总计**：约 37K tokens（安全范围）

### 上下文监控

每个智能体应定期（每生成 2000 字）检查上下文使用率：

```javascript
// 伪代码
async function checkContext() {
  const usage = await getSessionStatus();
  
  if (usage.percentUsed > 70%) {
    // 保存当前进度
    await saveCurrentProgress();
    
    // 记录需要续作
    await updateProgress({
      status: 'need_continue',
      reason: 'context_limit',
      completedWords: currentWords
    });
    
    // 提前结束
    return { shouldEnd: true };
  }
}
```

## 错误处理

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 章节生成中断 | 上下文超限 | 自动续作机制接管 |
| 智能体无响应 | 网络/API问题 | 重试3次后切换备用智能体 |
| 文件保存失败 | 磁盘空间不足 | 清理临时文件后重试 |
| 进度文件损坏 | JSON格式错误 | 从备份恢复或重建 |

### 重试机制

```javascript
async function generateChapterWithRetry(chapter, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const content = await generateChapter(chapter);
      await saveChapter(chapter, content);
      return { success: true };
    } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error);
      
      if (i === maxRetries - 1) {
        // 最后一次重试失败，切换智能体
        const backupAgent = getNextAgent(chapter.agent);
        await assignChapter(chapter, backupAgent);
        return { success: false, needReassign: true };
      }
      
      await sleep(5000 * (i + 1)); // 递增延迟
    }
  }
}
```

## 质量保证

### 章节验收标准

每章生成后自动检查：

- [ ] 字数达标：实际字数 ≥ 目标字数 × 90%
- [ ] 段落合格：段落占比 ≥ 60%
- [ ] 标题层级：无 #### 及更深标题
- [ ] 内容完整：无明显的"待补充"、"TODO"标记
- [ ] 格式正确：Markdown 格式无错误

### 最终审核

所有章节完成后，执行最终审核：

```javascript
async function finalReview(project) {
  const issues = [];
  
  // 1. 字数统计
  const totalWords = await countAllWords(project);
  if (totalWords < project.targetWords * 0.9) {
    issues.push(`总字数不足：${totalWords} < ${project.targetWords * 0.9}`);
  }
  
  // 2. 章节完整性
  const missingChapters = await findMissingChapters(project);
  if (missingChapters.length > 0) {
    issues.push(`缺失章节：${missingChapters.join(', ')}`);
  }
  
  // 3. 格式检查
  const formatIssues = await checkFormat(project);
  issues.push(...formatIssues);
  
  // 4. 生成质量报告
  await generateQualityReport(project, issues);
  
  return { passed: issues.length === 0, issues };
}
```

## 与其他 OpenClaw 实例共享

### 技能迁移步骤

1. **复制技能目录**：
   ```bash
   cp -r skills/tech-proposal-autopilot /path/to/other-openclaw/skills/
   ```

2. **复制智能体配置**：
   ```bash
   cp -r ~/.openclaw/agents/milo /path/to/other-openclaw/agents/
   cp -r ~/.openclaw/agents/josh /path/to/other-openclaw/agents/
   cp -r ~/.openclaw/agents/dev /path/to/other-openclaw/agents/
   cp -r ~/.openclaw/agents/marketing /path/to/other-openclaw/agents/
   ```

3. **更新 HEARTBEAT.md**：
   将本技能的检查逻辑添加到目标实例的 HEARTBEAT.md

4. **配置 Cron（可选）**：
   如果需要独立于心跳的定时检查

### 最小依赖

其他 OpenClaw 实例只需要：

- ✅ 本技能文档 (SKILL.md)
- ✅ 4个智能体配置 (milo, josh, dev, marketing)
- ✅ HEARTBEAT.md 中的检查逻辑
- ✅ progress.json 格式规范

**无需**：
- ❌ 特定的模型配置（任何支持长上下文的模型均可）
- ❌ 额外的依赖包
- ❌ 特殊的 OpenClaw 版本

## 最佳实践

### 项目规模建议

| 规模 | 章节数 | 总字数 | 预计耗时 | 建议配置 |
|------|--------|--------|---------|---------|
| 小型 | 6-10章 | 5-10万 | 30-60分钟 | 2个智能体并行 |
| 中型 | 12-18章 | 15-30万 | 1-2小时 | 4个智能体顺序 |
| 大型 | 20-30章 | 40-60万 | 3-5小时 | 4个智能体 + 定时监控 |

### 参考资料

**最佳实践**：
- 提供完整的技术参考资料（PDF/Word/URL）
- 参考资料总大小建议 < 50MB
- 会自动提取关键点压缩 80%

**支持格式**：
- PDF 文档
- Word 文档
- 网页 URL
- 纯文本文件
- Markdown 文件

### 时间规划

**避免时段**：
- 凌晨 2:00-6:00（系统维护时段）
- 网络高峰期（可能导致API延迟）

**最佳时段**：
- 上午 9:00-12:00
- 下午 14:00-18:00
- 晚间 20:00-23:00

## 监控与调试

### 日志位置

```
~/.openclaw/logs/tech-proposal-monitor.log  # 项目监控日志
~/.openclaw/logs/tech-proposal-{project}.log # 项目执行日志
projects/{project-name}/logs/                # 章节生成日志
```

### 状态查询命令

```
# 查看所有项目状态
查看技术方案书项目列表

# 查看特定项目进度
查看 {project-name} 项目进度

# 手动触发续作
继续执行 {project-name}
```

### 常见调试

**问题**：项目卡住不动

**排查**：
1. 检查 progress.json 的 status 和 lastUpdate
2. 查看日志中的错误信息
3. 确认智能体配置是否正常
4. 手动触发续作测试

**问题**：章节质量不达标

**排查**：
1. 检查智能体的 system prompt
2. 确认参考资料是否正确加载
3. 查看上下文使用情况
4. 考虑重新生成该章节

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 1.0.0 | 2026-03-23 | 初始版本，完整文档化 |

## 相关资源

- [多智能体协作最佳实践](../../MEMORY.md#多智能体协作最佳实践)
- [技术方案书写作规范](../../MEMORY.md#技术方案书写作规范)
- [GLM-5 上下文管理](../../MEMORY.md#glm-5上下文管理规则)

---

**本技能已通过多个项目验证**：
- 深圳市数据流通利用基础设施项目（15万字/10章）
- 智慧养老餐饮综合服务平台（20万字/18章）
- 工业互联网与智能制造平台（31万字/12章）

**验证结果**：100% 自动化完成，无需人工干预。
