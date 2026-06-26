// session-sync-detect Skill - Main Entry Point
// 跨会话同步检测与询问

/**
 * 检测用户话语是否涉及跨 session 内容
 * 
 * @param {string} userMessage - 用户输入的消息
 * @param {object} currentSessionContext - 当前 session 的上下文
 * @returns {boolean} - 是否需要询问跨 session 同步
 */
function detectCrossSessionSignal(userMessage, currentSessionContext) {
  // 时间引用信号
  const timeSignals = [
    '昨天', '前天', '上周', '上个月', '之前', '之前说',
    '刚才', '刚刚', ' earlier', 'previously',
    '那天', '那个时间', '当时'
  ];
  
  // 平台引用信号
  const platformSignals = [
    '微信', '飞书', '钉钉', '邮件', '短信', '群里',
    'wechat', 'lark', 'feishu', 'email', 'group'
  ];
  
  // 内容引用信号（模糊指代）
  const contentSignals = [
    '那个', '这个', '你说的', '我说的', '我们说的',
    '记得吧', '你知道', '你知道的', '你应该知道',
    '帮我查', '找找看', '查一下', '搜索一下',
    '同步一下', '看看有没有', '有没有提到'
  ];
  
  // 检查时间引用
  for (const signal of timeSignals) {
    if (userMessage.includes(signal)) {
      // 检查当前 session 是否有对应时间线的上下文
      if (!hasContextForTimeReference(signal, currentSessionContext)) {
        return true;
      }
    }
  }
  
  // 检查平台引用
  for (const signal of platformSignals) {
    if (userMessage.includes(signal)) {
      // 检查当前平台是否匹配
      if (!isCurrentPlatform(signal)) {
        return true;
      }
    }
  }
  
  // 检查内容引用
  for (const signal of contentSignals) {
    if (userMessage.includes(signal)) {
      // 检查当前 session 是否有相关上下文
      if (!hasRelevantContext(signal, currentSessionContext)) {
        return true;
      }
    }
  }
  
  return false;
}

/**
 * 检查当前 session 是否有对应时间线的上下文
 */
function hasContextForTimeReference(timeRef, context) {
  // 简化实现：检查最近消息中是否有时间相关内容
  // 实际实现需要更复杂的时间解析
  return false; // 默认返回 false，触发询问
}

/**
 * 检查当前平台是否匹配
 */
function isCurrentPlatform(platformRef) {
  // 简化实现：检查当前 channel 是否匹配
  return false; // 默认返回 false，触发询问
}

/**
 * 检查当前 session 是否有相关上下文
 */
function hasRelevantContext(signal, context) {
  // 简化实现：检查最近消息中是否有相关关键词
  return false; // 默认返回 false，触发询问
}

/**
 * 生成询问消息
 */
function generateInquiryMessage(userMessage, searchScopes) {
  return `🔍 检测到您可能在谈论其他 session 的内容：

"${userMessage}"

我可以在以下范围查找：
${searchScopes.map(scope => `- ✅ ${scope}`).join('\n')}

是否需要我帮您同步这些信息？`;
}

/**
 * 生成检索结果展示
 */
function generateResultsDisplay(results) {
  let display = `## 跨 Session 记忆检索结果\n\n`;
  display += `**搜索范围：** ${results.scope}\n`;
  display += `**搜索主题：** ${results.topic}\n\n`;
  display += `### 发现\n\n`;
  
  for (let i = 0; i < results.findings.length; i++) {
    const finding = results.findings[i];
    display += `#### ${i + 1}. ${finding.source}\n`;
    display += `- **时间：** ${finding.time}\n`;
    display += `- **内容：** ${finding.content}\n`;
    display += `- **来源：** \`${finding.location}\`\n\n`;
  }
  
  return display;
}

/**
 * 主入口函数
 */
export async function main(userMessage, currentSessionContext) {
  // Step 1: 检测是否需要询问
  const needsSync = detectCrossSessionSignal(userMessage, currentSessionContext);
  
  if (!needsSync) {
    return {
      shouldAsk: false,
      message: null
    };
  }
  
  // Step 2: 生成询问消息
  const searchScopes = [
    '记忆文件 (memory/YYYY-MM-DD.md, MEMORY.md)',
    '最近活跃的 session (过去 24 小时)'
  ];
  
  const inquiryMessage = generateInquiryMessage(userMessage, searchScopes);
  
  return {
    shouldAsk: true,
    message: inquiryMessage,
    userMessage: userMessage
  };
}

/**
 * 执行同步检索
 */
export async function executeSync(userMessage, confirmedScopes) {
  const results = {
    scope: confirmedScopes.join(', '),
    topic: extractKeywords(userMessage),
    findings: []
  };
  
  // Step 1: 搜索 memory 文件
  if (confirmedScopes.includes('记忆文件')) {
    const memoryResults = await searchMemoryFiles(userMessage);
    results.findings.push(...memoryResults);
  }
  
  // Step 2: 搜索 session 历史
  if (confirmedScopes.includes('最近活跃的 session')) {
    const sessionResults = await searchSessionHistory(userMessage);
    results.findings.push(...sessionResults);
  }
  
  return results;
}

/**
 * 提取关键词
 */
function extractKeywords(message) {
  // 简化实现：提取名词和专有名词
  return message.replace(/[？!，。？]/g, '').trim();
}

/**
 * 搜索 memory 文件
 */
async function searchMemoryFiles(query) {
  // 实现搜索 memory 文件的逻辑
  // 使用 grep 或类似工具
  return [];
}

/**
 * 搜索 session 历史
 */
async function searchSessionHistory(query) {
  // 实现搜索 session 历史的逻辑
  // 使用 sessions_list 和 sessions_history
  return [];
}

export default {
  main,
  executeSync,
  detectCrossSessionSignal,
  generateInquiryMessage,
  generateResultsDisplay
};
