/**
 * Context Usage Checker - 上下文使用率查询 Skill
 * 
 * 功能：实时查询当前会话的 Token 使用情况
 * 触发命令：/token
 * 自然语言：查上下文、token 使用情况、上下文还剩多少等
 */

// 模型上下文窗口映射表
const MODEL_CONTEXT_WINDOWS: Record<string, number> = {
  'qwen3.5-plus': 256000,
  'qwen3.5': 256000,
  'qwen-max': 32000,
  'qwen': 128000,
  'claude': 200000,
  'gpt-4': 128000,
  'gpt': 128000,
};

// 预警阈值
const WARNING_THRESHOLD = 70;      // 警告阈值（%）
const CRITICAL_THRESHOLD = 90;     // 严重警告阈值（%）

// 进度条配置
const PROGRESS_BAR_LENGTH = 20;
const PROGRESS_FILLED = '▓';
const PROGRESS_EMPTY = '░';

/**
 * 估算 Token 数量
 * 中文约 1.5 字符/token，英文约 4 字符/token
 */
function estimateTokens(text: string): number {
  if (!text) return 0;
  
  let chineseChars = 0;
  let asciiChars = 0;
  
  for (const char of text) {
    const code = char.charCodeAt(0);
    if (code >= 0x4e00 && code <= 0x9fff) {
      chineseChars++;
    } else {
      asciiChars++;
    }
  }
  
  // 中文 1.5 字符/token，英文 4 字符/token
  const chineseTokens = chineseChars / 1.5;
  const asciiTokens = asciiChars / 4;
  
  return Math.round(chineseTokens + asciiTokens);
}

/**
 * 获取模型的上下文窗口大小
 */
function getModelContextWindow(modelName: string): number {
  const lowerName = modelName.toLowerCase();
  
  // 精确匹配
  if (MODEL_CONTEXT_WINDOWS[lowerName]) {
    return MODEL_CONTEXT_WINDOWS[lowerName];
  }
  
  // 模糊匹配
  for (const [key, value] of Object.entries(MODEL_CONTEXT_WINDOWS)) {
    if (lowerName.includes(key)) {
      return value;
    }
  }
  
  // 默认值
  return 128000;
}

/**
 * 生成进度条
 */
function generateProgressBar(percentage: number): string {
  const filledCount = Math.round((percentage / 100) * PROGRESS_BAR_LENGTH);
  const emptyCount = PROGRESS_BAR_LENGTH - filledCount;
  
  return PROGRESS_FILLED.repeat(filledCount) + PROGRESS_EMPTY.repeat(emptyCount);
}

/**
 * 格式化数字（添加千分位分隔符）
 */
function formatNumber(num: number): string {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * 生成上下文使用状态报告
 */
function generateContextReport(usedTokens: number, modelContextWindow: number, modelName: string): string {
  const percentage = (usedTokens / modelContextWindow) * 100;
  const remainingTokens = modelContextWindow - usedTokens;
  
  let status: string;
  let icon: string;
  let suggestion: string;
  
  if (percentage >= CRITICAL_THRESHOLD) {
    status = '严重';
    icon = '🚨';
    suggestion = '🚨 **严重警告：** 上下文即将超限！建议立即使用 `/new` 开启新会话';
  } else if (percentage >= WARNING_THRESHOLD) {
    status = '警告';
    icon = '⚠️';
    suggestion = '💡 **建议：** 使用 `/new` 开启新会话 或 `/compact` 压缩上下文';
  } else {
    status = '正常';
    icon = '📊';
    suggestion = '> ✅ 上下文使用正常，可以继续对话';
  }
  
  const progressBar = generateProgressBar(percentage);
  
  return `### ${icon} 上下文使用状态

**状态：** ${status}
**模型：** ${modelName}

**使用率：** ${percentage.toFixed(1)}%
\`${progressBar}\`

**已使用：** ${formatNumber(usedTokens)} tokens
**剩余：** ${formatNumber(remainingTokens)} tokens
**总计：** ${formatNumber(modelContextWindow)} tokens

${suggestion}`;
}

/**
 * 匹配触发关键词
 */
function matchesTrigger(message: string): boolean {
  const triggers = [
    '/token',
    '查上下文',
    '查 token',
    '看上下文',
    '看 token',
    '上下文使用',
    'token 使用',
    '上下文还剩',
    'token 还剩',
    '上下文占用',
    'token 占用',
    '查看 token',
    '查询 token',
    'token usage',
    'context usage',
  ];
  
  const lowerMessage = message.toLowerCase().trim();
  return triggers.some(trigger => lowerMessage.includes(trigger.toLowerCase()));
}

/**
 * 主处理函数
 */
export async function handleContextUsageChecker(message: string, context?: any): Promise<string | null> {
  // 检查是否匹配触发条件
  if (!matchesTrigger(message)) {
    return null;
  }
  
  // 获取当前会话历史
  const sessionHistory = context?.sessionHistory || [];
  
  // 计算已使用的 Token
  let totalTokens = 0;
  for (const msg of sessionHistory) {
    totalTokens += estimateTokens(msg.content || '');
  }
  
  // 获取当前模型信息
  const modelName = context?.modelName || context?.model || 'qwen3.5-plus';
  const modelContextWindow = getModelContextWindow(modelName);
  
  // 生成报告
  const report = generateContextReport(totalTokens, modelContextWindow, modelName);
  
  return report;
}

// 导出给 OpenClaw 使用
export default {
  name: 'spark-context-monitor',
  version: '1.0.0',
  description: '上下文使用率查询 - 实时查看 Token 使用情况',
  triggers: ['/token', '查上下文', 'token 使用情况'],
  handler: handleContextUsageChecker,
};
