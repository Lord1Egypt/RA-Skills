/**
 * Self-Evolution-CN Hook for OpenClaw
 *
 * 自动识别并记录学习、错误和功能需求。
 * 支持多事件：agent:bootstrap、message:received、tool:after
 */

const fs = require('fs').promises;
const path = require('path');
const { lstatSync, realpathSync, existsSync } = require('fs');

// 获取共享学习目录
const SHARED_LEARNING_DIR = process.env.SHARED_LEARNING_DIR || '/root/.openclaw/shared-learning';

// 获取当前 agent ID
const AGENT_ID = process.env.AGENT_ID || 'main';

// 获取当前工作区路径
const WORKSPACE_DIR = process.cwd();

// 检测学习目录路径
function getLearningDir() {
  try {
    const learningsPath = path.join(WORKSPACE_DIR, '.learnings');

    // 检查 .learnings 是否存在
    if (!existsSync(learningsPath)) {
      // 不存在，使用共享目录
      return SHARED_LEARNING_DIR;
    }

    // 检查是否是软连接
    const stats = lstatSync(learningsPath);
    if (stats.isSymbolicLink()) {
      // 解析软连接目标
      const targetPath = realpathSync(learningsPath);

      // 如果软连接目标是共享目录，使用共享目录
      if (targetPath === SHARED_LEARNING_DIR) {
        return SHARED_LEARNING_DIR;
      }

      // 否则使用软连接目标
      return targetPath;
    }

    // 如果是独立文件夹，使用工作区的 .learnings
    if (stats.isDirectory()) {
      return learningsPath;
    }

    // 默认使用共享目录
    return SHARED_LEARNING_DIR;
  } catch (error) {
    console.error('检测学习目录失败:', error);
    return SHARED_LEARNING_DIR;
  }
}

// 获取学习目录
const LEARNING_DIR = getLearningDir();

// 自动识别和记录的提醒内容
const REMINDER_CONTENT = `
## 自我进化提醒

**自动识别和记录规则：**

### 1. 自动识别触发条件

**用户纠正（自动记录到 LEARNINGS.md）：**
- 检测到关键词："不对"、"错了"、"错误"、"不是这样"、"应该是"
- 检测到纠正性表达："No, that's wrong"、"Actually"、"应该是"
- **动作**：自动记录到 LEARNINGS.md，类别为 correction

**命令失败（自动记录到 ERRORS.md）：**
- 检测到工具执行失败（非零退出码）
- 检测到错误信息：error、Error、ERROR、failed、FAILED
- **动作**：自动记录到 ERRORS.md

**知识缺口（自动记录到 LEARNINGS.md）：**
- 检测到用户提供新信息
- 检测到"我不知道"、"查不到"等表达
- **动作**：自动记录到 LEARNINGS.md，类别为 knowledge_gap

**发现更好的方法（自动记录到 LEARNINGS.md）：**
- 检测到"更好的方法"、"更简单"、"优化"等表达
- **动作**：自动记录到 LEARNINGS.md，类别为 best_practice

### 2. 自动记录格式

**学习记录：**
\`\`\`markdown
## [LRN-YYYYMMDD-XXX] 类别

- Agent: ${AGENT_ID}
- Logged: 当前时间
- Priority: medium
- Status: pending
- Area: 根据上下文判断

### 摘要
一句话描述

### 详情
完整上下文

### 建议行动
具体修复或改进

### 元数据
- Source: conversation
- Pattern-Key: 自动生成
- Recurrence-Count: 1
\`\`\`

**错误记录：**
\`\`\`markdown
## [ERR-YYYYMMDD-XXX] 技能或命令名称

- Agent: ${AGENT_ID}
- Logged: 当前时间
- Priority: high
- Status: pending
- Area: 根据上下文判断

### 摘要
简要描述

### 错误
\`\`\`
错误信息
\`\`\`

### 上下文
- 尝试的命令/操作
- 使用的输入或参数

### 建议修复
如果可识别，如何解决

### 元数据
- Reproducible: yes
\`\`\`

### 3. 记录后回复

记录完成后，必须回复：
"已记录到 LEARNINGS.md" 或 "已记录到 ERRORS.md"

### 4. 提升规则

**多 Agent 统计：**
- 所有 agent 共享学习目录
- 按 \`Pattern-Key\` 累计 \`Recurrence-Count\`
- 累计次数 >= 3 时自动提升到 SOUL.md

**提升目标：**
- 行为模式 → SOUL.md
- 工作流改进 → AGENTS.md
- 工具问题 → TOOLS.md

### 5. 共享目录

共享目录：${SHARED_LEARNING_DIR}
当前 Agent：${AGENT_ID}
当前工作区：${WORKSPACE_DIR}
学习目录：${LEARNING_DIR}

**学习目录检测逻辑：**
- 如果工作区有 .learnings 软连接指向共享目录 → 使用共享目录
- 如果工作区有独立的 .learnings 文件夹 → 使用工作区的 .learnings
- 如果工作区没有 .learnings → 使用共享目录
`.trim();

// 生成唯一 ID
function generateId(prefix) {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
  return `${prefix}-${dateStr}-${random}`;
}

// 确保目录存在
async function ensureDir(dir) {
  try {
    await fs.mkdir(dir, { recursive: true });
  } catch (err) {
    // 目录已存在，忽略错误
  }
}

// 追加内容到文件
async function appendToFile(filePath, content) {
  await ensureDir(LEARNING_DIR);
  await fs.appendFile(filePath, content + '\n\n');
}

// 检测用户纠正
function detectCorrection(content) {
  const keywords = [
    '不对', '错了', '错误', '不是这样', '应该是',
    '你为什么', '我记得是', '提醒你', '更正一下',
    "No, that's wrong", 'Actually', 'should be'
  ];
  return keywords.some(keyword => content.includes(keyword));
}

// 检测知识缺口
function detectKnowledgeGap(content) {
  const keywords = [
    '我不知道', '查不到', '不知道', '无法找到', '找不到',
    '记下来', '记住', '你记好', '别忘了',
    '不清楚', '不确定',
    "I don't know", "can't find", 'not sure'
  ];
  return keywords.some(keyword => content.includes(keyword));
}

// 检测更好的方法
function detectBetterMethod(content) {
  const keywords = [
    '更好的方法', '更简单', '优化', '改进', '更好的',
    'better way', 'simpler', 'optimize', 'improve'
  ];
  return keywords.some(keyword => content.includes(keyword));
}

// 记录学习
async function recordLearning(category, summary, details, suggestedAction) {
  const id = generateId('LRN');
  const now = new Date().toISOString();
  const filePath = path.join(LEARNING_DIR, 'LEARNINGS.md');

  // 根据 category 生成 Pattern-Key 和 Area
  let patternKey = 'unknown';
  let area = '其他';

  switch (category) {
    case 'correction':
      patternKey = 'user.correction';
      area = '行为准则';
      break;
    case 'knowledge_gap':
      patternKey = 'knowledge.gap';
      area = '工作流';
      break;
    case 'best_practice':
      patternKey = 'better.method';
      area = '工作流改进';
      break;
  }

  const content = `## [${id}] ${category}

- Agent: ${AGENT_ID}
- Logged: ${now}
- Priority: medium
- Status: pending
- Area: ${area}

### 摘要
${summary}

### 详情
${details}

### 建议行动
${suggestedAction}

### 元数据
- Source: conversation
- Pattern-Key: ${patternKey}
- Recurrence-Count: 1
`;

  await appendToFile(filePath, content);
  return 'LEARNINGS.md';
}

// 记录错误
async function recordError(summary, error, context, suggestedFix) {
  const id = generateId('ERR');
  const now = new Date().toISOString();
  const filePath = path.join(LEARNING_DIR, 'ERRORS.md');

  const content = `## [${id}] ${summary}

- Agent: ${AGENT_ID}
- Logged: ${now}
- Priority: high
- Status: pending
- Area: 根据上下文判断

### 摘要
${summary}

### 错误
\`\`\`
${error}
\`\`\`

### 上下文
${context}

### 建议修复
${suggestedFix}

### 元数据
- Reproducible: yes
`;

  await appendToFile(filePath, content);
  return 'ERRORS.md';
}

// 记录功能需求
async function recordFeatureRequest(summary, details, suggestedAction) {
  const id = generateId('FEAT');
  const now = new Date().toISOString();
  const filePath = path.join(LEARNING_DIR, 'FEATURE_REQUESTS.md');

  const content = `## [${id}] ${summary}

- Agent: ${AGENT_ID}
- Logged: ${now}
- Priority: medium
- Status: pending
- Area: 根据上下文判断

### 摘要
${summary}

### 详情
${details}

### 建议行动
${suggestedAction}

### 元数据
- Source: conversation
- Pattern-Key: 自动生成
- Recurrence-Count: 1
`;

  await appendToFile(filePath, content);
  return 'FEATURE_REQUESTS.md';
}

const handler = async (event) => {
  // 事件结构的安全检查
  if (!event || typeof event !== 'object') {
    return;
  }

  // 处理 agent:bootstrap 事件
  if (event.type === 'agent' && event.action === 'bootstrap') {
    // 上下文的安全检查
    if (!event.context || typeof event.context !== 'object') {
      return;
    }

    // 将提醒作为虚拟引导文件注入
    if (Array.isArray(event.context.bootstrapFiles)) {
      event.context.bootstrapFiles.push({
        path: 'SELF_EVOLUTION_REMINDER.md',
        content: REMINDER_CONTENT,
        virtual: true,
      });
    }
  }

  // 处理 message:received 事件
  if (event.type === 'message' && event.action === 'received') {
    const content = event.context?.content || '';

    // 检测用户纠正
    if (detectCorrection(content)) {
      const fileName = await recordLearning(
        'correction',
        '用户纠正了之前的回答',
        `用户消息: ${content}`,
        '仔细分析用户的纠正意见，理解正确的做法，避免重复错误'
      );
      event.messages?.push(`已记录到 ${fileName}`);
    }

    // 检测知识缺口
    if (detectKnowledgeGap(content)) {
      const fileName = await recordLearning(
        'knowledge_gap',
        '发现知识缺口',
        `用户消息: ${content}`,
        '记录这个知识缺口，后续需要补充相关知识'
      );
      event.messages?.push(`已记录到 ${fileName}`);
    }

    // 检测更好的方法
    if (detectBetterMethod(content)) {
      const fileName = await recordLearning(
        'best_practice',
        '发现更好的方法',
        `用户消息: ${content}`,
        '学习这个更好的方法，更新工作流程'
      );
      event.messages?.push(`已记录到 ${fileName}`);
    }
  }

  // 处理 tool:after 事件
  if (event.type === 'tool' && event.action === 'after') {
    const toolName = event.context?.toolName || 'unknown';
    const result = event.context?.result || {};
    const output = event.context?.output || '';

    // 检测工具执行失败（结构化检测）
    if (result.error || result.status === 'error' || result.exitCode !== 0) {
      const errorInfo = result.error || result.message || JSON.stringify(result);
      const fileName = await recordError(
        `工具执行失败: ${toolName}`,
        errorInfo,
        `工具: ${toolName}\n参数: ${JSON.stringify(event.context?.args || {})}`,
        '检查工具使用方式，确认参数正确，或查看工具文档'
      );
      event.messages?.push(`已记录到 ${fileName}`);
    }

    // 检测系统级错误（字符串检测）
    if (output && typeof output === 'string') {
      const errorPatterns = [
        /error|Error|ERROR|failed|FAILED/g,
        /command not found|No such file|Permission denied|fatal/g
      ];
      if (errorPatterns.some(pattern => pattern.test(output))) {
        const fileName = await recordError(
          `系统错误: ${toolName}`,
          output,
          `工具: ${toolName}\n参数: ${JSON.stringify(event.context?.args || {})}`,
          '检查系统配置和权限'
        );
        event.messages?.push(`已记录到 ${fileName}`);
      }
    }
  }
};

module.exports = handler;
module.exports.default = handler;
