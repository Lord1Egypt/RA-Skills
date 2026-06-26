# Skill Combo - 技能组合器

> 版本：v1.0 | 作者：Spark | 创建时间：2026-04-04

---

## 🎯 Skill 定位

**多技能协同引擎** - 允许用户同时启用多个技能，让它们相互协作、优势互补，完成复杂任务

**核心使命：** 打破单一技能的能力边界，通过技能组合实现 1+1>2 的效果

---

## ⚡ 触发规则

### 主触发词
- `/combo` - 标准触发
- `/skill+` - 快捷触发
- `技能组合` - 中文触发
- `多技能` - 多技能触发

### 组合语法

**语法 1：加号连接**
```
/thinking+heart+pua
```

**语法 2：逗号分隔**
```
/combo thinking,heart,pua
```

**语法 3：空格分隔**
```
/combo thinking heart pua
```

### 任务描述

**两步触发（推荐）：**
```
用户：/thinking+heart
Agent: 🎭 已加载技能组合：Thinking + Heart
      请描述您要处理的任务
用户：帮我分析一下这个项目，30 分钟后提醒我进度
```

**一步触发：**
```
用户：/thinking+heart 帮我分析这个项目，30 分钟后提醒
```

---

## 🏗️ 核心工作流程

### Step 1: 技能解析 (Skill Parsing)

**目标：** 识别用户请求的组合技能

**解析规则：**
```
输入：/thinking+heart+pua
解析：
  - thinking → thinking-skill
  - heart → temp-heartbeat
  - pua → pua-skill (假设存在)
```

**输出：**
```markdown
## 🎭 技能组合已加载

**已加载技能：**
1. ✅ thinking-skill - 深度思考与规划
2. ✅ temp-heartbeat - 临时心跳任务
3. ✅ pua-skill - PUA 技巧助手

**技能数量：** 3 个
**组合模式：** 协同工作
```

---

### Step 2: 能力映射 (Capability Mapping)

**目标：** 分析每个技能的能力，确定分工

**能力矩阵：**

| 技能 | 核心能力 | 适用场景 | 输出格式 |
|------|----------|----------|----------|
| **thinking** | 分析、规划、检索 | 复杂任务 | Markdown 报告 |
| **heart** | 定时、提醒、检查 | 时间相关 | 定时任务 |
| **pua** | 话术、沟通、技巧 | 人际交往 | 建议/话术 |

**分工方案：**
```markdown
## 📋 技能分工

**thinking-skill:**
- 负责任务分析和规划
- 检索相关记忆和经验
- 输出执行路径

**temp-heartbeat:**
- 负责时间相关的提醒
- 创建临时心跳任务
- 定时检查进度

**pua-skill:**
- 负责沟通话术优化
- 提供交往技巧建议
- 优化表达方式
```

---

### Step 3: 执行编排 (Execution Orchestration)

**目标：** 协调多个技能的执行顺序

**编排模式：**

#### 模式 1：顺序执行
```
thinking → 分析任务
   ↓
heart → 创建提醒
   ↓
pua → 优化表达
   ↓
输出最终结果
```

#### 模式 2：并行执行
```
thinking ──┬→ 分析任务
heart  ────┼→ 创建提醒
           ↓
       合并结果
```

#### 模式 3：条件执行
```
thinking → 分析任务
   ↓
[如果需要提醒] → heart
   ↓
[如果需要沟通] → pua
   ↓
输出最终结果
```

**输出：**
```markdown
## 🗺️ 执行编排

**执行模式：** 顺序执行

**执行流程：**
1. thinking-skill - 任务分析 [预计 5 秒]
2. temp-heartbeat - 创建提醒 [预计 2 秒]
3. pua-skill - 话术优化 [预计 3 秒]
4. 合并结果 [预计 1 秒]

**总耗时估计：** 11 秒
```

---

### Step 4: 结果整合 (Result Integration)

**目标：** 将多个技能的输出整合成统一结果

**整合策略：**

#### 策略 1：分层展示
```markdown
# 📊 完整分析报告

## 🤔 思考过程
[thinking-skill 的输出]

## ⏰ 定时提醒
[heart-skill 的输出]

## 💬 沟通建议
[pua-skill 的输出]
```

#### 策略 2：融合展示
```markdown
# 📊 分析报告

根据分析，建议您采用以下方案：

**核心策略：** [thinking 分析结果]

**执行时间：** [heart 创建的提醒]

**沟通话术：** [pua 优化的表达]
```

**输出：**
```markdown
## 📦 结果整合

**整合策略：** 分层展示

**输出结构：**
1. 思考过程（thinking）
2. 定时提醒（heart）
3. 沟通建议（pua）
4. 综合建议（整合）
```

---

## 📝 完整输出模板

### 技能加载

```markdown
## 🎭 技能组合已加载

**组合 ID:** `combo_{timestamp}_{random}`
**已加载技能:**
1. ✅ thinking-skill - 深度思考与规划
2. ✅ temp-heartbeat - 临时心跳任务

**技能数量:** 2 个
**组合模式:** 协同工作
**有效期:** 本次会话（完成任务后自动卸载）

---

请描述您要处理的任务，或直接输入任务内容。
```

### 执行计划

```markdown
## 🗺️ 执行计划

**任务:** {任务描述}

**技能分工:**
- **thinking-skill:** 任务分析、路径规划
- **temp-heartbeat:** 创建 30 分钟后提醒

**执行流程:**
1. thinking-skill 分析任务 - 预计 5 秒
2. temp-heartbeat 创建提醒 - 预计 2 秒
3. 整合输出 - 预计 1 秒

**总耗时:** 8 秒

---

开始执行...
```

### 执行结果

```markdown
# 📊 完整结果

## 🤔 思考过程

[thinking-skill 的输出]

## ⏰ 定时提醒

[temp-heartbeat 的输出]

---

## 💡 综合建议

[整合后的最终建议]

---

*技能组合已完成，已自动卸载*
```

---

## 🔧 技术实现

### 技能加载器

```typescript
interface LoadedSkill {
  name: string;
  path: string;
  capabilities: string[];
  instance: any;
}

async function loadSkills(skillNames: string[]): Promise<LoadedSkill[]> {
  const loadedSkills: LoadedSkill[] = [];
  
  for (const name of skillNames) {
    // 查找技能文件
    const skillPath = await findSkillPath(name);
    if (!skillPath) {
      throw new Error(`Skill not found: ${name}`);
    }
    
    // 加载技能
    const skillContent = await readFile(skillPath, 'utf-8');
    const capabilities = extractCapabilities(skillContent);
    
    loadedSkills.push({
      name,
      path: skillPath,
      capabilities,
      instance: await import(skillPath),
    });
  }
  
  return loadedSkills;
}
```

### 能力映射器

```typescript
function mapCapabilities(skills: LoadedSkill[], task: string): SkillAssignment[] {
  const assignments: SkillAssignment[] = [];
  
  // 分析任务关键词
  const taskKeywords = extractKeywords(task);
  
  for (const skill of skills) {
    // 匹配技能能力与任务需求
    const matchScore = calculateMatchScore(skill.capabilities, taskKeywords);
    
    if (matchScore > 0.5) {
      assignments.push({
        skill: skill.name,
        responsibilities: determineResponsibilities(skill, task),
        priority: matchScore,
      });
    }
  }
  
  // 按优先级排序
  return assignments.sort((a, b) => b.priority - a.priority);
}
```

### 执行编排器

```typescript
async function orchestrateExecution(
  assignments: SkillAssignment[],
  task: string,
  mode: 'sequential' | 'parallel' | 'conditional' = 'sequential'
): Promise<any[]> {
  const results: any[] = [];
  
  if (mode === 'sequential') {
    // 顺序执行
    for (const assignment of assignments) {
      const result = await executeSkill(assignment.skill, task);
      results.push({ skill: assignment.skill, result });
    }
  } else if (mode === 'parallel') {
    // 并行执行
    const promises = assignments.map(async (assignment) => {
      const result = await executeSkill(assignment.skill, task);
      return { skill: assignment.skill, result };
    });
    results.push(...(await Promise.all(promises)));
  }
  
  return results;
}
```

### 结果整合器

```typescript
function integrateResults(
  results: any[],
  strategy: 'layered' | 'fused' | 'summary' = 'layered'
): string {
  if (strategy === 'layered') {
    return results.map((r) => formatLayer(r.skill, r.result)).join('\n\n');
  } else if (strategy === 'fused') {
    return fuseResults(results);
  } else if (strategy === 'summary') {
    return summarizeResults(results);
  }
  
  return '';
}
```

---

## 💡 使用示例

### 示例 1：项目分析 + 提醒

**用户输入：**
```
/thinking+heart 帮我分析一下这个项目，30 分钟后提醒我进度
```

**输出：**
```markdown
## 🎭 技能组合已加载

**已加载技能:**
1. ✅ thinking-skill - 深度思考与规划
2. ✅ temp-heartbeat - 临时心跳任务

**组合模式:** 协同工作

---

## 🗺️ 执行计划

**任务:** 分析项目，30 分钟后提醒进度

**技能分工:**
- **thinking-skill:** 项目分析、路径规划
- **temp-heartbeat:** 创建 30 分钟后提醒

**执行流程:**
1. thinking-skill 分析项目 - 预计 5 秒
2. temp-heartbeat 创建提醒 - 预计 2 秒
3. 整合输出 - 预计 1 秒

---

开始执行...

# 📊 完整结果

## 🤔 思考过程

**项目分析:**
- 项目类型：软件开发
- 关键要素：需求分析、开发、测试、部署
- 风险点：时间紧张、需求变更

**执行路径:**
1. 需求确认 - 2 天
2. 开发实现 - 5 天
3. 测试修复 - 2 天
4. 部署上线 - 1 天

## ⏰ 定时提醒

**提醒已创建:**
- 任务 ID: `task_1775246400000_xyz789`
- 执行时间: 30 分钟后
- 提醒内容: 检查项目进度

---

## 💡 综合建议

建议您先完成需求确认，30 分钟后我会提醒您检查进度。
根据分析，项目整体风险可控，按路径执行即可。

---

*技能组合已完成，已自动卸载*
```

---

### 示例 2：沟通分析 + 话术优化

**用户输入：**
```
/thinking+pua 老板让我加班，我怎么回复比较好？
```

**输出：**
```markdown
## 🎭 技能组合已加载

**已加载技能:**
1. ✅ thinking-skill - 深度思考与规划
2. ✅ pua-skill - PUA 技巧助手

---

# 📊 完整结果

## 🤔 思考过程

**情况分析:**
- 老板要求：加班
- 你的意愿：可能不想
- 关系影响：需要谨慎处理

**可选方案:**
1. 直接拒绝 - 风险高
2. 委婉拒绝 - 风险中
3. 条件接受 - 风险低
4. 完全接受 - 无风险

## 💬 沟通话术

**方案 1（条件接受）- 推荐:**
"好的老板，我可以加班。不过我手头还有 X 项目，您看优先级怎么安排？"

**方案 2（委婉拒绝）:**
"老板，我今天确实有急事。明天早点来赶进度可以吗？"

**方案 3（完全接受）:**
"好的老板，我马上处理。"

---

## 💡 综合建议

推荐使用方案 1，既展示了配合态度，又让老板了解你的工作负荷。

---

*技能组合已完成*
```

---

### 示例 3：三技能组合

**用户输入：**
```
/combo thinking,heart,pua 我要去相亲，帮我分析一下需要注意什么，见面前提醒我，还有教我怎么聊天
```

**输出：**
```markdown
## 🎭 技能组合已加载

**已加载技能:**
1. ✅ thinking-skill - 深度思考与规划
2. ✅ temp-heartbeat - 临时心跳任务
3. ✅ pua-skill - PUA 技巧助手

---

# 📊 完整结果

## 🤔 思考过程

**相亲分析:**
- 目标：建立良好第一印象
- 关键要素：外表、谈吐、态度
- 风险点：紧张、冷场、说错话

**准备清单:**
1. 外表准备：整洁、得体
2. 话题准备：工作、爱好、旅行
3. 心态准备：放松、真诚

## ⏰ 定时提醒

**提醒已创建:**
- 执行时间：见面前 1 小时
- 提醒内容：相亲准备检查
  - [ ] 整理外表
  - [ ] 准备话题
  - [ ] 调整心态

## 💬 聊天技巧

**开场白:**
"你好，很高兴认识你。今天天气不错，过来路上顺利吗？"

**话题建议:**
- 工作：轻松带过，不要炫耀
- 爱好：寻找共同点
- 旅行：分享有趣经历

**避免话题:**
- ❌ 前任
- ❌ 收入
- ❌ 负面抱怨

**肢体语言:**
- ✅ 保持眼神交流
- ✅ 适度微笑
- ✅ 身体微微前倾

---

## 💡 综合建议

相亲成功的关键是真诚和放松。做好准备工作，展现真实的自己就好。
我会在见面前 1 小时提醒你，祝你成功！

---

*技能组合已完成*
```

---

## ⚠️ 注意事项

### 1. 技能兼容性

- ✅ 大部分技能可以组合
- ⚠️ 冲突技能会提示（如两个输出格式冲突）
- ❌ 互斥技能无法组合

### 2. 性能考虑

- 建议组合技能数：2-4 个
- 最大组合数：10 个
- 超过 5 个技能时提示性能影响

### 3. 执行时间

- 单个技能：1-5 秒
- 组合技能：累加时间
- 超过 30 秒时显示进度

### 4. 结果整合

- 默认分层展示
- 可选择融合展示
- 支持自定义模板

---

## 🚀 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-04 | 初始版本，技能组合器 |

---

**Skill Combo 开发完成 · 让技能组合产生 1+1>2 的效果**
