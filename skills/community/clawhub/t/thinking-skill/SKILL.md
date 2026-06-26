# Thinking Skill - 深度思考与规划

> 版本：v1.0 | 作者：Spark | 创建时间：2026-04-04

---

## 🎯 Skill 定位

**元认知思考引擎** - 让 Agent 在行动前先思考、检索记忆、整合经验、规划最佳路径

**核心使命：** 通过系统化的思考流程，提升任务执行的质量和效率，避免盲目行动

---

## ⚡ 触发规则

### 两步触发机制

**Step 1：标记思考模式**
```
/thinking
```
→ Agent 进入思考准备状态，回复："🤔 已进入思考模式，请描述您要处理的任务"

**Step 2：描述任务**
```
帮我分析一下最近的股票走势，然后生成一份报告发到飞书群里
```
→ Agent 开始完整的思考流程并执行

### 触发词说明

| 触发词 | 作用 | 示例 |
|--------|------|------|
| `/thinking` | 进入思考模式（下一步才触发） | `/thinking` → 等待下一条消息 |
| `先思考一下` | 直接进入思考流程 | `先思考一下这个问题` |
| `think about this` | 直接进入思考流程 | `think about this task` |

### 场景触发
- 复杂任务（多步骤、需要协调多个技能）
- 陌生领域（需要检索相关经验）
- 重要决策（需要权衡利弊）
- 重复问题（需要查找历史解决方案）

### 不触发场景
- 简单查询（天气、时间等）
- 明确指令（已有清晰执行路径）
- 紧急操作（需要立即响应）

---

## 🏗️ 核心思考流程

### Step 1: 任务解析 (Task Analysis)

**目标：** 理解用户真实需求

**检查清单：**
- [ ] 任务类型识别（查询/操作/创作/分析）
- [ ] 关键要素提取（主体、动作、目标、约束）
- [ ] 隐含需求挖掘（用户未明说但可能需要的）
- [ ] 成功标准定义（如何判断任务完成）

**输出：**
```markdown
## 📋 任务解析

**任务类型：** [查询/操作/创作/分析]
**核心需求：** [一句话描述]
**关键要素：**
- 主体：...
- 动作：...
- 目标：...
- 约束：...
**隐含需求：** [可能需要的额外帮助]
**成功标准：** [完成标志]
```

---

### Step 2: 技能盘点 (Skill Inventory)

**目标：** 确认可用工具和能力

**检查内容：**
1. **已安装 Skills** - 列出所有可用技能
2. **技能能力匹配** - 哪些技能可以完成此任务
3. **技能依赖关系** - 是否需要组合多个技能
4. **技能限制** - 各技能的边界和约束

**输出：**
```markdown
## 🛠️ 可用技能

**直接相关：**
- [技能 1] - 用途说明
- [技能 2] - 用途说明

**可能需要：**
- [技能 3] - 备用方案

**技能组合方案：**
方案 A：[技能 1] + [技能 2] - 优势/劣势
方案 B：[技能 3] - 优势/劣势
```

---

### Step 3: 记忆检索 (Memory Retrieval)

**目标：** 查找相关历史经验和知识

**检索维度：**
1. **相似任务** - 过去是否处理过类似问题
2. **成功方案** - 哪些方法被验证有效
3. **失败教训** - 哪些坑需要避免
4. **用户偏好** - 用户的特定习惯和喜好
5. **领域知识** - 相关的专业知识和最佳实践

**输出：**
```markdown
## 🧠 相关记忆

**历史经验：**
- [时间] - [任务] - [方案] - [结果]
- ...

**成功经验：**
- [方法 1] - 适用场景
- [方法 2] - 适用场景

**失败教训：**
- [坑 1] - 如何避免
- [坑 2] - 如何避免

**用户偏好：**
- [偏好 1]
- [偏好 2]

**领域知识：**
- [知识点 1]
- [知识点 2]
```

---

### Step 4: 路径规划 (Path Planning)

**目标：** 设计最优执行方案

**规划原则：**
1. **最小步骤** - 用最少的操作完成任务
2. **最高成功率** - 优先选择已验证的方案
3. **最低成本** - 时间、资源、API 调用成本
4. **最佳体验** - 用户等待时间最短、交互最流畅

**输出：**
```markdown
## 🗺️ 执行路径

### 推荐方案：[方案名称]

**步骤分解：**
1. [步骤 1] - [使用技能] - [预期结果] - [耗时估计]
2. [步骤 2] - [使用技能] - [预期结果] - [耗时估计]
3. [步骤 3] - [使用技能] - [预期结果] - [耗时估计]

**总耗时估计：** [X 分钟]
**成功率估计：** [X%]

### 备选方案：[方案名称]

**触发条件：** [什么情况下使用备选]
**步骤差异：** [与主方案的差异]
```

---

### Step 5: 风险评估 (Risk Assessment)

**目标：** 预判可能的问题和应对方案

**检查项：**
- [ ] API 限流风险
- [ ] 权限不足风险
- [ ] 数据缺失风险
- [ ] 超时风险
- [ ] 用户期望管理

**输出：**
```markdown
## ⚠️ 风险评估

**可能问题：**
1. [问题 1] - 概率 [高/中/低] - 应对方案 [...]
2. [问题 2] - 概率 [高/中/低] - 应对方案 [...]

**风险控制：**
- [控制措施 1]
- [控制措施 2]

**用户期望管理：**
- [需要告知用户的事项]
```

---

### Step 6: 开始执行 (Start Execution)

**目标：** 按照规划开始行动

**输出：**
```markdown
## 🚀 开始执行

**确认事项：**
- [ ] 任务理解正确
- [ ] 方案已规划
- [ ] 风险已评估
- [ ] 用户已确认（如需要）

**执行中...**

[开始第一步操作]
```

---

## 📝 完整输出模板

```markdown
# 🤔 Thinking Process

## 📋 任务解析
[任务分析结果]

## 🛠️ 可用技能
[技能盘点结果]

## 🧠 相关记忆
[记忆检索结果]

## 🗺️ 执行路径
[路径规划结果]

## ⚠️ 风险评估
[风险评估结果]

---

## 🚀 开始执行

[确认无误后，开始执行第一步]
```

---

## 🔧 技术实现

### 思考模式状态管理

**状态存储：**
```typescript
interface ThinkingState {
  isActive: boolean;        // 是否处于思考模式
  activatedAt: number;      // 激活时间戳
  timeoutMs: number;        // 超时时间（默认 5 分钟）
  lastMessage?: string;     // 上一条消息（用于检测是否取消）
}
```

**状态流转：**
```
正常模式 --/thinking--> 思考准备模式 --用户输入任务--> 思考执行模式 --完成--> 正常模式
思考准备模式 --用户取消--> 正常模式
思考准备模式 --超时（5 分钟）--> 自动退出
```

**实现逻辑：**
```typescript
// 检查是否处于思考模式
function isThinkingMode(): boolean {
  const state = loadThinkingState();
  if (!state) return false;
  
  // 检查是否超时
  if (Date.now() - state.activatedAt > state.timeoutMs) {
    clearThinkingState();
    return false;
  }
  
  return state.isActive;
}

// 进入思考模式
function enterThinkingMode() {
  saveThinkingState({
    isActive: true,
    activatedAt: Date.now(),
    timeoutMs: 5 * 60 * 1000, // 5 分钟
  });
  
  return '🤔 已进入思考模式，请描述您要处理的任务';
}

// 处理思考模式下的消息
async function handleThinkingMessage(userMessage: string): Promise<string> {
  // 检测是否是取消指令
  if (isCancelMessage(userMessage)) {
    clearThinkingState();
    return '✅ 已取消思考模式，如有需要随时输入 /thinking';
  }
  
  // 开始完整思考流程
  const thinkingResult = await runThinkingProcess(userMessage);
  clearThinkingState();
  
  // 输出思考结果并开始执行
  return formatThinkingOutput(thinkingResult);
}

// 检测取消指令
function isCancelMessage(message: string): boolean {
  const cancelKeywords = ['算了', '不用了', '取消', 'cancel', 'never mind'];
  return cancelKeywords.some(keyword => 
    message.toLowerCase().includes(keyword)
  );
}
```

---

### 记忆检索接口

```typescript
// 检索 MEMORY.md
async function searchMemory(query: string): Promise<MemorySnippet[]> {
  // 使用 memory_search 工具
  // 返回相关记忆片段
}

// 检索技能列表
async function listSkills(): Promise<SkillInfo[]> {
  // 使用 sessions_list 或读取 skills 目录
  // 返回可用技能列表
}

// 检索历史会话
async function searchHistory(query: string): Promise<SessionHistory[]> {
  // 使用 sessions_history 工具
  // 返回相关历史会话
}
```

### 思考流程编排

```typescript
async function thinkingProcess(userTask: string): Promise<ThinkingResult> {
  // Step 1: 任务解析
  const taskAnalysis = await analyzeTask(userTask);
  
  // Step 2: 技能盘点
  const skills = await listSkills();
  const matchedSkills = matchSkills(taskAnalysis, skills);
  
  // Step 3: 记忆检索
  const memories = await searchMemory(taskAnalysis.keywords);
  const experiences = extractExperiences(memories);
  
  // Step 4: 路径规划
  const plan = await createPlan(taskAnalysis, matchedSkills, experiences);
  
  // Step 5: 风险评估
  const risks = await assessRisks(plan);
  
  // Step 6: 输出思考结果
  return {
    taskAnalysis,
    matchedSkills,
    experiences,
    plan,
    risks,
  };
}
```

---

## 💡 使用示例

### 示例 1：两步触发（推荐）

**Step 1：标记思考模式**
```
/thinking
```

**Agent 回复：**
```
🤔 已进入思考模式，请描述您要处理的任务
```

**Step 2：描述任务**
```
帮我分析一下最近的股票走势，然后生成一份报告发到飞书群里
```

**Thinking 输出：**
```markdown
# 🤔 Thinking Process

## 📋 任务解析

**任务类型：** 分析 + 创作 + 操作
**核心需求：** 股票分析并分享报告
**关键要素：**
- 主体：股票走势
- 动作：分析、生成报告、发送
- 目标：飞书群分享
- 约束：需要最新数据

**隐含需求：**
- 可能需要指定具体股票
- 可能需要指定时间范围
- 报告格式偏好（图表/文字）

**成功标准：**
- 数据准确、分析专业、报告清晰、成功发送

## 🛠️ 可用技能

**直接相关：**
- web_search - 获取股票数据
- web_fetch - 获取财经新闻
- feishu-create-doc - 创建报告文档
- message - 发送到飞书群

**技能组合方案：**
方案 A：web_search + feishu-create-doc + message
  - 优势：完整流程、可保存文档
  - 劣势：步骤较多

方案 B：web_search + message（直接发送摘要）
  - 优势：快速
  - 劣势：信息不够完整

## 🧠 相关记忆

**历史经验：**
- 2026-04-01 - 股票查询 - 使用 Yahoo Finance API - 成功
- 2026-03-28 - 报告生成 - 使用 Markdown 格式 - 用户满意

**成功经验：**
- 股票数据优先使用权威来源（Yahoo Finance、新浪财经）
- 报告包含：当前价格、涨跌幅、K 线趋势、关键指标
- 飞书文档使用表格 + 图表更清晰

**失败教训：**
- 避免使用过时的数据（超过 15 分钟）
- 不要发送太长的消息（会被折叠）

**用户偏好：**
- 喜欢简洁的摘要 + 详细文档链接
- 偏好蓝色系图表

## 🗺️ 执行路径

### 推荐方案：方案 A

**步骤分解：**
1. web_search 获取股票最新数据 - 预计 3 秒
2. web_fetch 获取相关新闻和分析 - 预计 5 秒
3. feishu-create-doc 创建详细报告 - 预计 10 秒
4. message 发送摘要 + 文档链接到群 - 预计 2 秒

**总耗时估计：** 20 秒
**成功率估计：** 95%

### 备选方案：方案 B

**触发条件：** 用户要求快速响应
**步骤差异：** 跳过文档创建，直接发送摘要

## ⚠️ 风险评估

**可能问题：**
1. 股票数据 API 限流 - 概率 低 - 应对：使用备用数据源
2. 飞书文档创建失败 - 概率 低 - 应对：直接发送文字报告
3. 数据延迟超过 15 分钟 - 概率 中 - 应对：在报告中标注数据时间

**风险控制：**
- 优先使用官方数据源
- 所有数据标注时间戳
- 准备备选方案

**用户期望管理：**
- 告知数据可能有 15 分钟延迟
- 说明分析仅供参考，不构成投资建议

---

## 🚀 开始执行

**确认事项：**
- [x] 任务理解正确
- [x] 方案已规划
- [x] 风险已评估
- [ ] 需要确认具体股票代码

**在执行前，请确认：**
1. 要分析哪只股票？（如：AAPL、TSLA、00700.HK）
2. 分析多长时间范围？（如：最近 7 天、最近 1 个月）
3. 发送到哪个飞书群？

确认后我将开始执行。
```

---

### 示例 2：直接进入思考流程

**用户输入：**
```
先思考一下，我想开发一个新的 Skill，可以自动回复飞书群里的@消息
```

**Thinking 输出：**
```markdown
# 🤔 Thinking Process

## 📋 任务解析
[任务分析结果]
...
```

---

### 示例 3：取消思考模式

**用户输入：**
```
/thinking
```

**Agent 回复：**
```
🤔 已进入思考模式，请描述您要处理的任务
```

**用户改变主意：**
```
算了，不用了
```

**Agent 回复：**
```
✅ 已取消思考模式，如有需要随时输入 /thinking
```

**Thinking 输出：**
```markdown
# 🤔 Thinking Process

## 📋 任务解析

**任务类型：** 创作 + 开发
**核心需求：** 飞书自动回复 Skill
**关键要素：**
- 主体：飞书群@消息
- 动作：监听、分析、自动回复
- 目标：自动化回复
- 约束：需要飞书 API 权限

## 🛠️ 可用技能

**参考技能：**
- feishu-im-user-message - 飞书消息发送
- feishu-im-user-get-messages - 消息获取
- feishu-chat - 群聊管理

**需要新增：**
- 消息监听机制
- @消息识别
- 回复逻辑（规则/AI）

## 🧠 相关记忆

**历史经验：**
- 2026-04-03 - 开发 kie-nano-banana-pro - 成功发布
- 2026-04-02 - 开发 nanobanana-pro v1.1 - 整合知识库

**成功经验：**
- Skill 开发标准流程：SKILL.md → 代码 → 测试 → 发布
- 飞书技能需要 OAuth 授权
- 使用 message 工具发送消息

**失败教训：**
- 避免轮询消息（效率低、易限流）
- 注意消息去重（避免重复回复）

## 🗺️ 执行路径

**步骤分解：**
1. 创建 Skill 骨架（SKILL.md、skill.json）
2. 实现@消息识别逻辑
3. 实现回复逻辑（可配置规则）
4. 添加消息去重机制
5. 测试和发布

**总耗时估计：** 30 分钟
**成功率估计：** 90%

## ⚠️ 风险评估

**可能问题：**
1. 飞书 API 权限不足 - 概率 中 - 需要用户授权
2. 消息轮询效率低 - 概率 高 - 使用 webhook 更好
3. 重复回复 - 概率 中 - 需要去重机制

---

## 🚀 开始执行

**确认事项：**
- [x] 任务理解正确
- [x] 方案已规划
- [x] 风险已评估

**开始创建 Skill 骨架...**

[继续执行]
```

---

## 🚀 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-04 | 初始版本，6 步思考流程 |

---

**Thinking Skill 开发完成 · 让行动前先思考成为习惯**
