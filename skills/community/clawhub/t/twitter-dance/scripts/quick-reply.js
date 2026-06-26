#!/usr/bin/env node

/**
 * Twitter Dance - 快速回复特定推文的评论
 * 
 * 用法：
 *   # 为指定推文获取和回复评论
 *   node quick-reply.js --tweet-id=123456789 [--dry-run]
 * 
 *   # 示例：
 *   node quick-reply.js --tweet-id=2031936903918883025 --replies=5 --dry-run
 */

require('dotenv').config();
const TwitterDanceEnhanced = require('../src/twitter-api-enhanced');

// 解析命令行参数
const args = {
  tweetId: null,
  repliesCount: 10,
  dryRun: false,
  autoReply: true
};

process.argv.slice(2).forEach(arg => {
  if (arg.startsWith('--tweet-id=')) {
    args.tweetId = arg.split('=')[1];
  } else if (arg.startsWith('--replies=')) {
    args.repliesCount = parseInt(arg.split('=')[1]);
  } else if (arg === '--dry-run') {
    args.dryRun = true;
  } else if (arg === '--no-reply') {
    args.autoReply = false;
  }
});

// 检查必需参数
if (!args.tweetId) {
  console.log(`
📱 Twitter Dance - 快速回复脚本

用法：
  node quick-reply.js --tweet-id=<推文ID> [选项]

选项：
  --tweet-id=ID      推文 ID（必需）
  --replies=N        获取最多 N 条评论（默认 10）
  --dry-run          模拟模式，仅显示不发送
  --no-reply         仅显示评论，不进行回复

示例：
  node quick-reply.js --tweet-id=2031936903918883025 --replies=5 --dry-run

获取推文 ID：
  1. 在 Twitter 网页版，打开任何推文
  2. 链接格式：https://twitter.com/username/status/[推文ID]
  3. 或在推文页面按 F12，在网络标签页查看 API 调用

  `);
  process.exit(1);
}

// AI 回复模板库
const replyTemplates = {
  感谢: [
    '感谢你的反馈！😊',
    '谢谢分享！',
    '感谢支持！💪'
  ],
  询问: [
    '很好的问题！让我们继续讨论 👇',
    '这是个有趣的观点，你有什么建议吗？',
    '好奇你的看法，能分享更多细节吗？'
  ],
  同意: [
    '完全同意！👏',
    '说得太好了！',
    '100% 同意你的观点！'
  ],
  鼓励: [
    '继续加油！🚀',
    '保持热情！',
    '你做得很好，保持下去！'
  ],
  默认: [
    '谢谢你的评论！😄',
    '感谢互动！',
    '期待继续讨论！'
  ]
};

// 简单的情感分析
function generateReply(commentText) {
  if (!commentText) return replyTemplates.默认[0];
  
  const text = commentText.toLowerCase();
  
  if (text.includes('谢谢') || text.includes('感谢')) {
    return replyTemplates.感谢[Math.floor(Math.random() * replyTemplates.感谢.length)];
  }
  if (text.includes('怎么') || text.includes('为什么') || text.includes('如何') || text.includes('?') || text.includes('？')) {
    return replyTemplates.询问[Math.floor(Math.random() * replyTemplates.询问.length)];
  }
  if (text.includes('同意') || text.includes('赞成') || text.includes('对') || text.includes('好')) {
    return replyTemplates.同意[Math.floor(Math.random() * replyTemplates.同意.length)];
  }
  if (text.includes('加油') || text.includes('继续')) {
    return replyTemplates.鼓励[Math.floor(Math.random() * replyTemplates.鼓励.length)];
  }
  
  return replyTemplates.默认[Math.floor(Math.random() * replyTemplates.默认.length)];
}

async function main() {
  try {
    const client = new TwitterDanceEnhanced({
      authToken: process.env.TWITTER_AUTH_TOKEN,
      apiKey: process.env.APIDANCE_API_KEY,
      verbose: false
    });

    console.log('═══════════════════════════════════════════════════');
    console.log('💬 Twitter 快速回复评论');
    console.log('═══════════════════════════════════════════════════\n');

    console.log(`📌 推文 ID: ${args.tweetId}`);
    console.log(`📬 获取最多 ${args.repliesCount} 条评论\n`);

    // 获取评论
    console.log('⏳ 正在获取评论...\n');
    
    let replies = [];
    try {
      const response = await client.getReplies(args.tweetId, {
        count: args.repliesCount
      });

      // 处理响应格式
      if (response && response.replies && Array.isArray(response.replies)) {
        replies = response.replies;
      } else if (Array.isArray(response)) {
        replies = response;
      }
    } catch (err) {
      console.log(`❌ 获取评论失败: ${err.message}`);
      console.log('   请检查推文 ID 是否正确\n');
      return;
    }

    if (!replies || replies.length === 0) {
      console.log('😶 这条推文还没有评论\n');
      return;
    }

    console.log(`✅ 找到 ${replies.length} 条评论\n`);
    console.log('═══════════════════════════════════════════════════\n');

    // 显示评论
    const replyPlan = [];
    
    for (let i = 0; i < replies.length; i++) {
      const reply = replies[i];
      const author = reply.user?.screen_name || reply.from_user || 'unknown';
      const text = reply.text || reply.full_text || '';
      const replyText = generateReply(text);

      console.log(`${i + 1}. @${author}`);
      console.log(`   💬 "${text.substring(0, 80)}${text.length > 80 ? '...' : ''}"`);
      
      if (args.autoReply) {
        console.log(`   ↩️  计划回复: "${replyText}"`);
        replyPlan.push({
          id: reply.id_str || reply.id,
          author,
          text,
          reply: replyText
        });
      }
      
      console.log();
    }

    console.log('═══════════════════════════════════════════════════\n');

    // 实际发送回复
    if (!args.autoReply || replyPlan.length === 0) {
      console.log('✅ 完成');
      return;
    }

    if (args.dryRun) {
      console.log(`🔍 【模拟模式】准备发送 ${replyPlan.length} 条回复`);
      console.log('   移除 --dry-run 参数来真正发送\n');
      return;
    }

    console.log(`🚀 正在发送 ${replyPlan.length} 条回复...\n`);

    let successCount = 0;
    let failureCount = 0;

    for (const plan of replyPlan) {
      try {
        console.log(`⏳ 正在回复 @${plan.author}...`);
        
        const result = await client.autoReply(plan.id, plan.reply, {
          auto_mention: true
        });

        if (result && result.success) {
          console.log(`✅ 回复成功！\n`);
          successCount++;
        } else {
          console.log(`⚠️ 回复失败: ${result?.error || '未知错误'}\n`);
          failureCount++;
        }

        // 延迟避免速率限制
        await new Promise(r => setTimeout(r, Math.random() * 1000 + 1000));
      } catch (err) {
        console.log(`❌ 错误: ${err.message}\n`);
        failureCount++;
      }
    }

    console.log('═══════════════════════════════════════════════════');
    console.log('📊 完成统计');
    console.log(`✅ 成功: ${successCount}`);
    console.log(`❌ 失败: ${failureCount}`);
    console.log('═══════════════════════════════════════════════════\n');

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
