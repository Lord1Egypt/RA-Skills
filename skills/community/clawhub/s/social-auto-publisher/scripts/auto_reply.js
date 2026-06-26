#!/usr/bin/env node
/**
 * Auto-Reply Engine
 * Automatically reply to comments on each platform based on a chosen strategy
 *
 * Usage:
 *   node scripts/auto_reply.js --platform xiaohongshu --strategy warm --dry-run
 *   node scripts/auto_reply.js --platform twitter --strategy witty
 */

const path = require('path');
const fs = require('fs');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].replace(/^--/, '');
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : 'true';
      opts[key] = val;
      if (val !== 'true') i++;
    }
  }
  return opts;
}

// ─── Reply Strategy Templates ─────────────────────────────────────────
const REPLY_STRATEGIES = {
  warm: {
    name: 'Warm and Friendly',
    systemPrompt: `You are a social media account operator with a warm and friendly style.
When replying to comments:
- Address the other person with friendly terms like "dear," "friend," "sister"
- Sincerely thank them for their interaction
- Appropriately guide further discussion
- Each reply should be 20-50 words
- No mechanical copy-pasting`,
  },
  professional: {
    name: 'Professional and Concise',
    systemPrompt: `You are an operator of a professional brand account.
When replying to comments:
- Use formal but not stiff language
- Be concise and impactful, usually 15-30 words
- Respond positively to questions or express thanks
- Maintain brand tone`,
  },
  witty: {
    name: 'Humorous and Clever',
    systemPrompt: `You are an operator of a personal brand account with a humorous and clever style.
When replying to comments:
- Use lighthearted and humorous language
- Use memes appropriately but not excessively
- Show personality without being offensive
- Each reply should be 15-40 words`,
  },
  custom: {
    name: 'Custom',
    systemPrompt: 'Custom reply style (loaded from references/reply-templates.md)',
  },
};

// ─── Comment Classification and Reply Suggestions ───────────────────
function classifyComment(comment) {
  const text = (comment.text || comment.content || '').toLowerCase();

  const patterns = {
    praise: ['awesome', 'great', 'love', 'amazing', 'nice', 'like', 'save', 'favorite', '好棒', '厉害', '赞', '不错', '喜欢', '收藏'],
    question: ['how', 'what', 'where', 'why', '?', '？', '怎么', '如何', '什么', '哪里', '为什么'],
    complaint: ['bad', 'disappointed', 'terrible', 'poor', '不好', '失望', '垃圾', '差', '骗'],
    request: ['please', 'share', 'link', 'tutorial', '求', '分享', '链接', '教程'],
    engagement: ['check', 'interesting', 'try', '打卡', '来啦', '看看吧', '试试'],
  };

  for (const [category, keywords] of Object.entries(patterns)) {
    if (keywords.some(k => text.includes(k))) {
      return category;
    }
  }

  return 'general';
}

function getReplyTemplate(category, strategy) {
  const templates = {
    praise: {
      warm: 'Thanks so much for the love, dear! ❤️ Save it if you find it useful and review it later～',
      professional: 'Thank you for your recognition. We will continue to provide quality content.',
      witty: 'Great taste! 😎 Good stuff deserves to be seen～',
    },
    question: {
      warm: 'Great question! Can you elaborate more specifically, dear? I can explain in detail～',
      professional: 'Thank you for your question. Regarding this topic, we recommend referring to our detailed guide.',
      witty: 'You hit the nail on the head! Let me think about how to answer this soul-searching question 🤔',
    },
    complaint: {
      warm: 'So sorry you had a bad experience, dear 😢 Could you share more specifically what needs improvement?',
      professional: 'Thank you for your feedback. We will carefully assess and improve.',
      witty: 'Noted! I am writing this down in my little notebook 📝 Next time will be better～',
    },
    request: {
      warm: 'On it! Hold tight, dear, the related content is coming soon～',
      professional: 'Your request has been noted and will be covered in upcoming content.',
      witty: 'I get you! Good things are meant to be shared 😉 On it!',
    },
    engagement: {
      warm: 'Welcome, welcome! Feel free to drop by often, dear～ 🌸',
      professional: 'Thank you for following. We look forward to your continued engagement.',
      witty: 'Welcome! 🎉 Stop by often; there are always surprises～',
    },
    general: {
      warm: 'Thank you for your comment, dear! 💕',
      professional: 'Thank you for your comment.',
      witty: 'I have seen this comment! ✨',
    },
  };

  return (templates[category] && templates[category][strategy]) || templates.general[strategy] || 'Thank you!';
}

// ─── Platform Reply Commands ─────────────────────────────────────────
const PLATFORM_REPLY_COMMANDS = {
  xiaohongshu: (commentId, reply) => [
    { step: 1, action: 'navigate', command: 'browser navigate https://creator.xiaohongshu.com/notifications' },
    { step: 2, action: 'click', command: `browser act ref=<reply-button-for-comment${commentId}> kind=click` },
    { step: 3, action: 'type', command: `browser act ref=<reply-input> kind=type text="${reply}"` },
    { step: 4, action: 'click', command: 'browser act ref=<send-reply-button> kind=click' },
  ],
  weibo: (commentId, reply) => [
    { step: 1, action: 'api', endpoint: 'https://api.weibo.com/2/comments/reply.json', method: 'POST', params: { cid: commentId, comment: reply } },
  ],
  twitter: (commentId, reply) => [
    { step: 1, action: 'api', endpoint: 'https://api.twitter.com/2/tweets', method: 'POST', params: { text: reply, reply: { in_reply_to_tweet_id: commentId } } },
  ],
};

function main() {
  const opts = parseArgs();

  if (!opts.platform || !opts.strategy) {
    console.error('Usage: node auto_reply.js --platform <platform> --strategy <warm|professional|witty|custom> [--dry-run]');
    process.exit(1);
  }

  const platform = opts.platform;
  const strategy = opts.strategy;
  const dryRun = !!opts['dry-run'];

  if (!REPLY_STRATEGIES[strategy]) {
    console.error(`[error] Unsupported strategy: ${strategy}`);
    console.error(`  Options: ${Object.keys(REPLY_STRATEGIES).join(', ')}`);
    process.exit(1);
  }

  if (!PLATFORM_REPLY_COMMANDS[platform]) {
    console.error(`[error] Unsupported platform: ${platform}`);
    console.error(`  Options: ${Object.keys(PLATFORM_REPLY_COMMANDS).join(', ')}`);
    process.exit(1);
  }

  const strategyConfig = REPLY_STRATEGIES[strategy];

  console.log('─── Auto-Reply Configuration ───');
  console.log(`Platform: ${platform}`);
  console.log(`Strategy: ${strategyConfig.name}`);
  console.log(`Mode: ${dryRun ? 'Preview (dry-run)' : 'Execution'}`);
  console.log('');
  console.log('System Prompt:');
  console.log(strategyConfig.systemPrompt);
  console.log('');

  if (strategy === 'custom') {
    console.log('Custom strategy: Please refer to references/reply-templates.md to configure reply templates');
  }

  // Example: Show categorized reply templates
  console.log('─── Reply Template Preview ───');
  const categories = ['praise', 'question', 'complaint', 'request', 'engagement', 'general'];
  for (const cat of categories) {
    const template = getReplyTemplate(cat, strategy);
    console.log(`  [${cat}] ${template}`);
  }

  console.log('');
  if (dryRun) {
    console.log('[DRY RUN] No replies were actually sent');
  } else {
    console.log('Please use the above templates to reply based on actual comment content');
    console.log(`Refer to platform reply commands: ${JSON.stringify(PLATFORM_REPLY_COMMANDS[platform], null, 2)}`);
  }
}

main();