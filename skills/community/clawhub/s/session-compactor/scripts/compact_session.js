#!/usr/bin/env node

/**
 * Session Compactor - 智能会话压缩
 * 基于 claw-code compact.rs 设计理念
 *
 * 核心功能:
 * - 自动估算会话 token 数 (1 token ≈ 4 字符)
 * - 当超过阈值时，将早期消息压缩为结构化摘要
 * - 保留最新消息的完整上下文
 * - 提取关键事实、工具调用
 */

const readline = require('readline');

// 默认配置
const DEFAULT_CONFIG = {
  maxTokens: 3000,
  minMessagesToKeep: 5
};

/**
 * 估算文本的 token 数量 (启发式: 字符数 / 4)
 */
function estimateTokens(text) {
  if (typeof text !== 'string') {
    text = JSON.stringify(text);
  }
  return Math.ceil(text.length / 4);
}

/**
 * 从消息中提取关键事实 (正则匹配)
 */
function extractFacts(messages) {
  const facts = [];
  const patterns = [
    /\d{4}年/g,
    /[\d.]+%|涨|降|增加|减少/g,
    /(?:营收|收入|利润|销量|价格|成本)/g,
    /(?:必须|应该|建议|计划|需要)/g,
    /(?:重要|关键|核心|主要)/g,
    /https?:\/\/[^\s]+/g
  ];

  messages.forEach(msg => {
    const content = typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content);
    patterns.forEach(pattern => {
      const matches = content.match(pattern);
      if (matches) {
        matches.slice(0, 2).forEach(match => {
          if (!facts.includes(match)) facts.push(match);
        });
      }
    });
  });

  return facts.slice(0, 10);
}

/**
 * 生成会话摘要 (关键词提取版)
 */
function generateSummary(messages) {
  const userMsgs = messages.filter(m => m.role === 'user');
  const toolCalls = messages.filter(m => m.role === 'assistant' && m.tool_calls);
  const facts = extractFacts(messages);

  const firstUser = userMsgs[0]?.content || '';
  const topic = firstUser.substring(0, 80).trim() + (firstUser.length > 80 ? '...' : '');

  return `- **对话目标**: ${topic}\n- **消息数量**: 共 ${messages.length} 条 (已压缩)\n- **工具调用**: ${toolCalls.length} 次\n- **关键信息**: ${facts.length} 条\n- **保留上下文**: 最新 ${Math.floor(messages.length/3)} 条消息保持完整`;
}

/**
 * 核心压缩算法
 *
 * @param {Array} messages - 会话消息数组 (OpenAI 格式)
 * @param {Object} options - 配置选项
 * @param {number} [options.maxTokens] - token 阈值
 * @param {number} [options.minMessagesToKeep] - 最少保留消息数
 * @param {boolean} [options.force] - 是否强制压缩
 * @returns {Promise<Object>} 压缩结果
 */
async function compactSession(messages, options = {}) {
  const config = { ...DEFAULT_CONFIG, ...options };

  if (messages.length <= config.minMessagesToKeep) {
    return {
      compacted: false,
      reason: '消息数不足',
      originalMessages: messages.length,
      compressedMessages: messages.length,
      savedTokens: 0,
      summary: ''
    };
  }

  // 1. 估算总 tokens
  const totalTokens = messages.reduce((sum, msg) => {
    const content = typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content);
    return sum + estimateTokens(content);
  }, 0);

  if (!options.force && totalTokens <= config.maxTokens) {
    return {
      compacted: false,
      reason: '未超过阈值',
      originalMessages: messages.length,
      compressedMessages: messages.length,
      savedTokens: 0,
      summary: ''
    };
  }

  // 2. 确定保留的最新消息数 (保留约 1/3 或 minKeep，取较大者)
  const keepCount = Math.max(config.minMessagesToKeep, Math.floor(messages.length / 3));
  const toKeep = messages.slice(-keepCount);
  const toCompact = messages.slice(0, -keepCount);

  // 3. 生成摘要
  const summary = generateSummary(toCompact);

  // 4. 构建压缩后的消息数组
  const compressedMessages = [
    {
      role: 'system',
      content: `## 会话摘要 (已压缩早期 ${toCompact.length} 条消息)\n\n${summary}\n\n---\n*注: 为控制token使用量，早期对话已压缩为摘要。如需回顾细节，请询问。*`
    },
    ...toKeep
  ];

  // 5. 计算节省的 tokens
  const newTotalTokens = compressedMessages.reduce((sum, msg) => {
    const content = typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content);
    return sum + estimateTokens(content);
  }, 0);
  const savedTokens = totalTokens - newTotalTokens;

  return {
    compacted: true,
    originalMessages: messages.length,
    compressedMessages: compressedMessages.length,
    savedTokens,
    summary,
    reason: `压缩了 ${toCompact.length} 条早期消息，节省约 ${savedTokens} tokens`
  };
}

// CLI 测试模式
if (require.main === module) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('🔧 会话压缩器 CLI 测试模式');
  console.log(`默认配置: maxTokens=${DEFAULT_CONFIG.maxTokens}, minKeep=${DEFAULT_CONFIG.minMessagesToKeep}`);
  console.log('\n输入选项:');
  console.log('  "test" - 使用 20 条示例消息测试');
  console.log('  JSON数组 - 直接输入消息数组进行压缩');
  console.log('  "exit" 退出\n');

  rl.on('line', async (line) => {
    if (line === 'exit' || line === 'quit') {
      rl.close();
      return;
    }

    let messages;
    if (line === 'test') {
      // 生成测试数据 (模拟真实长会话)
      messages = [];
      const topics = [
        '请帮我分析赛力斯2025年报',
        '还需要2024年对比数据',
        '深信服2025预测怎么样？',
        '内存价格未来半年趋势如何？',
        '分布式存储市场竞争格局？'
      ];
      
      for (let i = 0; i < 25; i++) {
        const topic = topics[i % topics.length];
        const hasTool = i % 3 === 0;
        messages.push({
          role: i % 2 === 0 ? 'user' : 'assistant',
          content: `${topic}。请提供详细数据和分析。2025年关键指标：营收1648.88亿，净利润59.57亿元，销量47.23万辆。`,
          tool_calls: hasTool ? [{ name: 'tavily_search', arguments: { query: topic } }] : undefined
        });
      }
      console.log(`📝 创建了 ${messages.length} 条示例消息`);
    } else {
      try {
        messages = JSON.parse(line);
        if (!Array.isArray(messages)) throw new Error('必须是消息数组');
      } catch (e) {
        console.error('❌ 无效 JSON 数组:', e.message);
        console.log('格式示例: [{"role":"user","content":"..."},{"role":"assistant","content":"..."}]');
        return;
      }
    }

    try {
      const result = await compactSession(messages);
      console.log('\n📦 压缩结果:');
      console.log(JSON.stringify(result, null, 2));
      
      if (result.compacted && result.compressedMessages) {
        console.log('\n✨ 压缩后消息预览 (前3条):');
        const preview = result.compressedMessages.slice(0, 3).map(msg => 
          `${msg.role}: ${msg.content.substring(0, 100)}${msg.content.length > 100 ? '...' : ''}`
        );
        console.log(preview.join('\n'));
      }
    } catch (err) {
      console.error('❌ 压缩失败:', err.message);
    }
    
    console.log('\n继续输入 (或 "exit" 退出):');
  });

  rl.on('close', () => {
    console.log('👋 再见');
    process.exit(0);
  });
}

module.exports = {
  estimateTokens,
  compactSession,
  generateSummary,
  extractFacts,
  DEFAULT_CONFIG
};
