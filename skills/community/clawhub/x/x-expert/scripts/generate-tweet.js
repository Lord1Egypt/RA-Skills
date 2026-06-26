#!/usr/bin/env node

/**
 * X Expert - 推文生成脚本
 * 根据主题、风格和参考内容生成推文
 * Usage: node generate-tweet.js "主题" "风格" [参考内容]
 */

const MAX_TWEET_LENGTH = 280;

/**
 * 推文风格模板
 */
const styleTemplates = {
  professional: {
    name: '专业',
    template: '【{topic}】{content}',
    emoji: '📊',
  },
  humorous: {
    name: '幽默',
    template: '{content} 😂',
    emoji: '😆',
  },
  casual: {
    name: '随意',
    template: '{content}',
    emoji: '👋',
  },
  formal: {
    name: '正式',
    template: '{topic}: {content}',
    emoji: '📝',
  },
  warm: {
    name: '温暖',
    template: '{content} 💕',
    emoji: '💕',
  },
  sharp: {
    name: '犀利',
    template: '{content} 🔥',
    emoji: '🔥',
  },
};

/**
 * 生成推文内容
 */
function generateTweet(options) {
  const {
    topic,
    style = 'professional',
    referenceContent = '',
    audience = 'general',
  } = options;

  const styleConfig = styleTemplates[style] || styleTemplates.professional;

  // 构建 prompt
  let prompt = `请帮我生成一条推文，主题是：${topic}\n`;
  prompt += `目标受众：${audience}\n`;
  prompt += `风格：${styleConfig.name}\n`;

  if (referenceContent) {
    prompt += `\n参考内容：\n${referenceContent}\n`;
  }

  prompt += `\n要求：
1. 推文长度控制在 ${MAX_TWEET_LENGTH} 字符以内
2. 内容要有价值，吸引人
3. 可以适当使用 emoji
4. 可以加话题标签
5. 如果是推文串，用 | 分隔每条
6. 只返回推文内容，不要其他解释`;

  return {
    prompt,
    style: styleConfig,
    topic,
  };
}

/**
 * 格式化推文（实际调用 LLM 时使用）
 */
function formatTweet(tweet, style = 'professional') {
  const styleConfig = styleTemplates[style] || styleTemplates.professional;

  // 处理推文串
  if (tweet.includes('|')) {
    const tweets = tweet.split('|').map((t) => t.trim());
    return {
      type: 'thread',
      tweets: tweets.map((t) => {
        if (t.length > MAX_TWEET_LENGTH) {
          return t.substring(0, MAX_TWEET_LENGTH - 3) + '...';
        }
        return t;
      }),
    };
  }

  // 单条推文
  if (tweet.length > MAX_TWEET_LENGTH) {
    return {
      type: 'too_long',
      content: tweet,
      warning: `内容超过 ${MAX_TWEET_LENGTH} 字符，请拆分或精简`,
    };
  }

  return {
    type: 'single',
    content: tweet,
  };
}

/**
 * CLI 入口
 */
function main() {
  const topic = process.argv[2];
  const style = process.argv[3] || 'professional';
  const referenceContent = process.argv[4] || '';

  if (!topic) {
    console.error('Usage: node generate-tweet.js "主题" [风格] [参考内容]');
    console.error('Styles:', Object.keys(styleTemplates).join(', '));
    process.exit(1);
  }

  const result = generateTweet({
    topic,
    style,
    referenceContent,
  });

  console.log('=== 推文生成请求 ===');
  console.log('主题:', result.topic);
  console.log('风格:', result.style.name);
  console.log('---');
  console.log('请使用 LLM 生成以下 prompt 的内容：');
  console.log('');
  console.log(result.prompt);
}

// 如果直接运行
if (require.main === module) {
  main();
}

module.exports = {
  generateTweet,
  formatTweet,
  styleTemplates,
  MAX_TWEET_LENGTH,
};
