#!/usr/bin/env node

/**
 * Twitter Dance - 自动回复评论脚本
 * 
 * 功能：
 * 1. 获取你最近的推文
 * 2. 获取这些推文的最新评论
 * 3. 自动生成回复内容
 * 4. 发送回复
 * 
 * 用法：
 *   node auto-reply-comments.js [选项]
 * 
 * 选项：
 *   --tweets=N        获取最近N条推文（默认 5）
 *   --replies=N       每条推文获取最近N条评论（默认 10）
 *   --dry-run         仅显示将要回复的内容，不实际发送
 *   --replied-only    只对未回复的评论进行操作
 *   --skip-own        跳过自己的推文评论
 */

require('dotenv').config();
const TwitterDanceEnhanced = require('../src/twitter-api-enhanced');

// 解析命令行参数
const args = {
  tweetsCount: 5,
  repliesCount: 10,
  dryRun: false,
  repliedOnly: false,
  skipOwn: false
};

process.argv.slice(2).forEach(arg => {
  if (arg.startsWith('--tweets=')) {
    args.tweetsCount = parseInt(arg.split('=')[1]);
  } else if (arg.startsWith('--replies=')) {
    args.repliesCount = parseInt(arg.split('=')[1]);
  } else if (arg === '--dry-run') {
    args.dryRun = true;
  } else if (arg === '--replied-only') {
    args.repliedOnly = true;
  } else if (arg === '--skip-own') {
    args.skipOwn = true;
  }
});

// AI 回复模板库
const replyTemplates = {
  感谢: [
    '感谢你的反馈！',
    '谢谢分享！',
    '感谢支持！'
  ],
  询问: [
    '很好的问题，让我们继续讨论！',
    '这是个有趣的观点，你有什么建议吗？',
    '好奇你的看法，能分享更多细节吗？'
  ],
  同意: [
    '完全同意！',
    '说得好！',
    '100% 同意你的观点！'
  ],
  鼓励: [
    '继续加油！',
    '保持热情！',
    '你做得很好，保持下去！'
  ],
  默认: [
    '谢谢你的评论！',
    '感谢互动！',
    '期待继续讨论！'
  ]
};

// 简单的情感分析，选择合适的回复模板
function generateReply(commentText) {
  const text = commentText.toLowerCase();
  
  // 检测关键词
  if (text.includes('谢谢') || text.includes('感谢') || text.includes('thanks')) {
    return replyTemplates.感谢[Math.floor(Math.random() * replyTemplates.感谢.length)];
  }
  if (text.includes('怎么') || text.includes('为什么') || text.includes('如何') || text.includes('?') || text.includes('？')) {
    return replyTemplates.询问[Math.floor(Math.random() * replyTemplates.询问.length)];
  }
  if (text.includes('同意') || text.includes('赞成') || text.includes('对') || text.includes('👍')) {
    return replyTemplates.同意[Math.floor(Math.random() * replyTemplates.同意.length)];
  }
  if (text.includes('加油') || text.includes('继续') || text.includes('好')) {
    return replyTemplates.鼓励[Math.floor(Math.random() * replyTemplates.鼓励.length)];
  }
  
  return replyTemplates.默认[Math.floor(Math.random() * replyTemplates.默认.length)];
}

async function main() {
  try {
    const client = new TwitterDanceEnhanced({
      authToken: process.env.TWITTER_AUTH_TOKEN,
      apiKey: process.env.APIDANCE_API_KEY,
      verbose: true
    });

    console.log('═══════════════════════════════════════════════════');
    console.log('🤖 Twitter 自动回复评论 - 开始执行');
    console.log('═══════════════════════════════════════════════════\n');

    // Step 1: 获取我的最近推文
    console.log(`📝 第一步：获取你最近的 ${args.tweetsCount} 条推文...\n`);
    
    let myTweets = [];
    
    try {
      const tweetsResponse = await client.getMyTweets({
        count: args.tweetsCount,
        excludeReplies: false,
        includeRetweets: false
      });

      // 处理返回值格式（可能是对象或数组）
      if (tweetsResponse) {
        if (tweetsResponse.tweets && Array.isArray(tweetsResponse.tweets)) {
          myTweets = tweetsResponse.tweets;
        } else if (Array.isArray(tweetsResponse)) {
          myTweets = tweetsResponse;
        } else if (typeof tweetsResponse.tweets === 'number') {
          // API 错误代码
          throw new Error(`API 返回错误代码: ${tweetsResponse.tweets}`);
        }
      }
    } catch (err) {
      console.log(`⚠️ 获取推文失败: ${err.message}`);
      console.log(`💡 可能的原因：`);
      console.log(`   - 账户没有推文`);
      console.log(`   - API 认证失败`);
      console.log(`   - API Key 过期\n`);
      return;
    }

    if (!myTweets || myTweets.length === 0) {
      console.log('❌ 找不到你的推文');
      return;
    }

    console.log(`✅ 找到 ${myTweets.length} 条推文\n`);

    let totalReplies = 0;
    const replyPlan = [];

    // Step 2: 获取每条推文的评论
    console.log(`📬 第二步：获取评论（每条推文最多 ${args.repliesCount} 条）...\n`);

    for (const tweet of myTweets) {
      const tweetId = tweet.id_str;
      const tweetText = tweet.text?.substring(0, 50) + '...';
      
      console.log(`  推文: ${tweetText}`);
      
      try {
        const replies = await client.getReplies(tweetId, {
          count: args.repliesCount
        });

        if (replies && replies.length > 0) {
          console.log(`  ├─ 找到 ${replies.length} 条评论`);
          
          for (const reply of replies) {
            const commentAuthor = reply.user?.screen_name || 'unknown';
            const commentText = reply.text?.substring(0, 40) + '...';
            const replyText = generateReply(reply.text);
            
            // 检查是否已回复
            const hasReplied = replies.some(r => 
              r.in_reply_to_screen_name === commentAuthor
            );

            if (args.repliedOnly && hasReplied) {
              console.log(`  │  ├─ 【已回复】@${commentAuthor}: ${commentText}`);
              continue;
            }

            replyPlan.push({
              replyToId: reply.id_str,
              replyToUser: commentAuthor,
              originalTweet: tweetText,
              comment: reply.text,
              plannedReply: replyText,
              createdAt: reply.created_at
            });

            console.log(`  │  ├─ @${commentAuthor}: ${commentText}`);
            totalReplies++;
          }
        } else {
          console.log(`  ├─ 没有评论`);
        }
      } catch (err) {
        console.log(`  ├─ ❌ 获取评论失败: ${err.message}`);
      }
      
      console.log();
    }

    console.log('═══════════════════════════════════════════════════\n');

    if (replyPlan.length === 0) {
      console.log('✅ 没有需要回复的评论');
      return;
    }

    // Step 3: 显示回复计划
    console.log(`📋 回复计划 (共 ${replyPlan.length} 条评论):\n`);
    
    replyPlan.forEach((plan, index) => {
      console.log(`${index + 1}. @${plan.replyToUser}`);
      console.log(`   原推文: ${plan.originalTweet}`);
      console.log(`   评论: ${plan.comment?.substring(0, 60)}`);
      console.log(`   💬 计划回复: "${plan.plannedReply}"`);
      console.log();
    });

    console.log('═══════════════════════════════════════════════════\n');

    // Step 4: 实际发送回复（如果不是 dry-run）
    if (args.dryRun) {
      console.log('🔍 【模拟模式】这是一个演习，未实际发送回复');
      console.log(`   如需真正发送，请移除 --dry-run 参数\n`);
      return;
    }

    console.log(`🚀 第三步：发送 ${replyPlan.length} 条回复...\n`);

    let successCount = 0;
    let failureCount = 0;

    for (const plan of replyPlan) {
      try {
        console.log(`⏳ 正在回复 @${plan.replyToUser}...`);
        
        const result = await client.autoReply(plan.replyToId, plan.plannedReply, {
          auto_mention: true
        });

        if (result.success) {
          console.log(`✅ 回复成功！推文ID: ${result.replyId}\n`);
          successCount++;
        } else {
          console.log(`⚠️ 回复失败: ${result.error || '未知错误'}\n`);
          failureCount++;
        }

        // 避免速率限制，延迟 1-2 秒
        await new Promise(r => setTimeout(r, Math.random() * 1000 + 1000));
      } catch (err) {
        console.log(`❌ 回复错误: ${err.message}\n`);
        failureCount++;
      }
    }

    console.log('═══════════════════════════════════════════════════');
    console.log('📊 执行完成');
    console.log(`✅ 成功: ${successCount}`);
    console.log(`❌ 失败: ${failureCount}`);
    console.log('═══════════════════════════════════════════════════\n');

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
