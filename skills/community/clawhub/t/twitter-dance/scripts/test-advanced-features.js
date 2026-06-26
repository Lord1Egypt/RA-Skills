#!/usr/bin/env node

/**
 * Twitter Dance - 高级功能测试脚本
 * 
 * 演示以下功能：
 * 1. 获取账户统计
 * 2. 获取通知
 * 3. 自动回复
 * 4. 获取推文指标
 * 5. 时间线分析
 * 6. 互动周期分析
 */

const TwitterDanceEnhanced = require('../src/twitter-api-enhanced');
const path = require('path');

require('dotenv').config({ path: path.join(__dirname, '../.env') });

async function main() {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║   🎭 Twitter Dance - 高级功能测试                       ║
║   增强 API: 通知、统计、自动回复、分析                  ║
╚═══════════════════════════════════════════════════════════╝
`);

  const client = new TwitterDanceEnhanced({
    apiKey: process.env.APIDANCE_API_KEY,
    authToken: process.env.TWITTER_AUTH_TOKEN,
    verbose: true
  });

  const args = process.argv.slice(2);
  const command = args[0] || 'menu';

  try {
    switch (command) {
      case 'stats':
        await getAccountStats(client);
        break;

      case 'notifications':
        await getNotifications(client);
        break;

      case 'notifications-v2':
        await getNotificationsV2(client);
        break;

      case 'reply':
        await autoReply(client, args[1], args[2]);
        break;

      case 'metrics':
        await getTweetMetrics(client, args[1]);
        break;

      case 'timeline-analytics':
        await getTimelineAnalytics(client);
        break;

      case 'engagement-hours':
        await getEngagementByHour(client);
        break;

      case 'bulk-like':
        await bulkLikeTweets(client, args.slice(1));
        break;

      case 'conversation':
        await getConversationThread(client, args[1]);
        break;

      case 'all':
        await runAllTests(client);
        break;

      default:
        showMenu();
    }

  } catch (err) {
    console.error('\n[❌] 错误:', err.message);
    process.exit(1);
  }
}

/**
 * 获取账户统计
 */
async function getAccountStats(client) {
  console.log('\n[1/8] 账户统计信息\n');

  const stats = await client.getAccountStats();

  if (stats.success) {
    console.log('═'.repeat(60));
    console.log('📱 账户信息');
    console.log('═'.repeat(60));
    console.log(`姓名: ${stats.account.name}`);
    console.log(`账户: @${stats.account.handle}`);
    console.log(`简介: ${stats.account.bio}`);
    console.log(`位置: ${stats.account.location || '未设置'}`);

    console.log('\n📊 统计数据');
    console.log('═'.repeat(60));
    console.log(`粉丝: ${stats.stats.followers.toLocaleString()}`);
    console.log(`关注: ${stats.stats.following.toLocaleString()}`);
    console.log(`推文: ${stats.stats.tweets.toLocaleString()}`);
    console.log(`点赞: ${stats.stats.likes.toLocaleString()}`);
    console.log(`媒体: ${stats.stats.mediaCount.toLocaleString()}`);
    console.log(`列表: ${stats.stats.listedCount}`);

    console.log('\n✅ 完成\n');
  }
}

/**
 * 获取通知
 */
async function getNotifications(client) {
  console.log('\n[2/8] 获取通知\n');

  const notifications = await client.getNotifications({ count: 10 });

  if (notifications.success) {
    console.log('═'.repeat(60));
    console.log('🔔 通知摘要（来源：' + notifications.source + '）');
    console.log('═'.repeat(60));
    console.log(`提及: ${notifications.summary.mentions}`);
    console.log(`回复: ${notifications.summary.replies}`);
    console.log(`点赞: ${notifications.summary.likes}`);
    console.log(`转发: ${notifications.summary.retweets}`);
    console.log(`关注: ${notifications.summary.follows}`);

    if (notifications.notifications.length > 0) {
      console.log('\n📝 最新互动:');
      console.log('═'.repeat(60));
      notifications.notifications.slice(0, 5).forEach((notif, i) => {
        console.log(`${i + 1}. @${notif.handle} - ${notif.likes}❤️ ${notif.retweets}🔄`);
        console.log(`   "${notif.text.substring(0, 50)}..."`);
      });
    }

    console.log('\n✅ 完成\n');
  }
}

/**
 * 获取完整通知（API v2）
 */
async function getNotificationsV2(client) {
  console.log('\n[2/8] 获取完整通知（API v2）\n');

  try {
    const notifications = await client.getNotificationsV2();

    if (notifications.success) {
      console.log('═'.repeat(60));
      console.log('🔔 完整通知摘要（Twitter API v2）');
      console.log('═'.repeat(60));
      console.log(`📊 总通知数: ${notifications.summary.total}`);
      console.log(`💬 提及: ${notifications.summary.mentions}`);
      console.log(`❤️ 点赞: ${notifications.summary.likes}`);
      console.log(`🔄 转发: ${notifications.summary.retweets}`);
      console.log(`👥 关注: ${notifications.summary.follows}`);
      console.log(`💭 引用: ${notifications.summary.quotes}`);
      console.log(`📝 回复: ${notifications.summary.replies}`);
      console.log(`🔷 其他: ${notifications.summary.other}`);

      if (notifications.notifications.length > 0) {
        console.log('\n📝 最新通知详情:');
        console.log('═'.repeat(60));
        notifications.notifications.slice(0, 5).forEach((notif, i) => {
          const message = notif.message?.text || notif.text || 'No message';
          console.log(`${i + 1}. ${message.substring(0, 55)}`);
          if (notif.template) {
            const templateType = typeof notif.template === 'object'
              ? Object.keys(notif.template).join(', ')
              : String(notif.template);
            console.log(`   类型: ${templateType}`);
          }
        });
      }
      
      console.log('\n💡 通知来源已确认：');
      console.log('   ✅ API 端点: /2/notifications/all.json');
      console.log('   ✅ 请求头: authtoken + apikey（小写）');
      console.log('   ✅ 格式: globalObjects.notifications');
    }
  } catch (err) {
    console.error(`[❌] 错误: ${err.message}`);
  }

  console.log('\n✅ 完成\n');
}

/**
 * 自动回复
 */
async function autoReply(client, tweetId, replyText) {
  if (!tweetId || !replyText) {
    console.log('[❌] 用法: node test-advanced-features.js reply <tweetId> <replyText>');
    return;
  }

  console.log(`\n[3/8] 自动回复\n`);

  try {
    const result = await client.autoReply(tweetId, replyText);

    if (result.success) {
      console.log('═'.repeat(60));
      console.log('✅ 回复成功');
      console.log('═'.repeat(60));
      console.log(`回复 ID: ${result.replyId}`);
      console.log(`原始推文 ID: ${result.originalTweetId}`);
      console.log(`内容: ${result.text}`);
      console.log(`时间: ${result.timestamp}`);
    }

    console.log('\n✅ 完成\n');
  } catch (err) {
    console.error(`[❌] 回复失败: ${err.message}`);
  }
}

/**
 * 获取推文指标
 */
async function getTweetMetrics(client, tweetId) {
  if (!tweetId) {
    console.log('[❌] 用法: node test-advanced-features.js metrics <tweetId>');
    return;
  }

  console.log(`\n[4/8] 推文指标\n`);

  const metrics = await client.getTweetMetrics(tweetId);

  if (metrics.success) {
    console.log('═'.repeat(60));
    console.log('📈 推文指标');
    console.log('═'.repeat(60));
    console.log(`❤️  点赞: ${metrics.metrics.likes}`);
    console.log(`🔄 转发: ${metrics.metrics.retweets}`);
    console.log(`💬 回复: ${metrics.metrics.replies}`);
    console.log(`💭 引用: ${metrics.metrics.quotes}`);
    console.log(`👀 浏览: ${metrics.metrics.views.toLocaleString()}`);
    console.log(`📊 总互动: ${metrics.engagement.totalEngagement}`);
  }

  console.log('\n✅ 完成\n');
}

/**
 * 时间线分析
 */
async function getTimelineAnalytics(client) {
  console.log('\n[5/8] 时间线分析\n');

  const analytics = await client.getTimelineAnalytics({ count: 100 });

  if (analytics.success) {
    console.log('═'.repeat(60));
    console.log('📊 时间线统计');
    console.log('═'.repeat(60));
    console.log(`总推文: ${analytics.totalTweets}`);
    console.log(`总点赞: ${analytics.totalLikes.toLocaleString()}`);
    console.log(`总转发: ${analytics.totalRetweets.toLocaleString()}`);
    console.log(`总回复: ${analytics.totalReplies.toLocaleString()}`);
    console.log(`平均点赞/条: ${analytics.averageLikes}`);
    console.log(`平均转发/条: ${analytics.averageRetweets}`);

    console.log('\n⭐ 最受欢迎的推文');
    console.log('═'.repeat(60));
    if (analytics.topTweet) {
      console.log(`"${analytics.topTweet.text}..."`);
      console.log(`互动数: ${analytics.topTweet.engagement}`);
      console.log(`发布时间: ${analytics.topTweet.createdAt}`);
    }
  }

  console.log('\n✅ 完成\n');
}

/**
 * 互动周期分析
 */
async function getEngagementByHour(client) {
  console.log('\n[6/8] 互动周期分析\n');

  const analysis = await client.getEngagementByHour();

  if (analysis.success) {
    console.log('═'.repeat(60));
    console.log('⏰ 按小时的互动情况');
    console.log('═'.repeat(60));

    // 找出前 5 个最佳时间段
    const top5 = analysis.hourlyStats
      .sort((a, b) => b.avgEngagement - a.avgEngagement)
      .slice(0, 5);

    console.log('🏆 最佳发推时间 (UTC):\n');
    top5.forEach((hour, i) => {
      if (hour.tweets > 0) {
        const timeStr = `${String(hour.hour).padStart(2, '0')}:00`.padEnd(10);
        const bar = '█'.repeat(Math.round(hour.avgEngagement / 5));
        console.log(`${i + 1}. ${timeStr} - 平均互动: ${hour.avgEngagement.toFixed(1)} ${bar}`);
      }
    });

    console.log(`\n💡 建议: 在 ${String(analysis.bestHour).padStart(2, '0')}:00 UTC 发推，获得最高互动`);
  }

  console.log('\n✅ 完成\n');
}

/**
 * 批量点赞
 */
async function bulkLikeTweets(client, tweetIds) {
  if (tweetIds.length === 0) {
    console.log('[❌] 用法: node test-advanced-features.js bulk-like <tweetId1> <tweetId2> ...');
    return;
  }

  console.log(`\n[7/8] 批量点赞\n`);

  const result = await client.bulkLikeTweets(tweetIds);

  if (result.success) {
    console.log('═'.repeat(60));
    console.log('✅ 批量点赞完成');
    console.log('═'.repeat(60));
    console.log(`成功: ${result.liked}`);
    console.log(`失败: ${result.failed}`);

    if (result.errors.length > 0) {
      console.log('\n⚠️  失败的推文:');
      result.errors.forEach(e => {
        console.log(`  - ${e.tweetId}: ${e.error}`);
      });
    }
  }

  console.log('\n✅ 完成\n');
}

/**
 * 获取对话线程
 */
async function getConversationThread(client, tweetId) {
  if (!tweetId) {
    console.log('[❌] 用法: node test-advanced-features.js conversation <tweetId>');
    return;
  }

  console.log(`\n[8/8] 获取对话线程\n`);

  const thread = await client.getConversationThread(tweetId);

  if (thread.success) {
    console.log('═'.repeat(60));
    console.log('🧵 对话线程');
    console.log('═'.repeat(60));
    console.log(`原始推文 ID: ${tweetId}`);
    if (thread.replies && thread.replies.success) {
      console.log(`回复数: ${thread.replies.replies.length}`);
    }
    console.log(`获取时间: ${thread.timestamp}`);
  }

  console.log('\n✅ 完成\n');
}

/**
 * 运行所有测试
 */
async function runAllTests(client) {
  console.log('\n🚀 运行所有测试\n');

  try {
    await getAccountStats(client);
    await getNotifications(client);
    await getTweetMetrics(client, '2031936903918883025'); // 使用之前发布的推文
    await getTimelineAnalytics(client);
    await getEngagementByHour(client);

    console.log('═'.repeat(60));
    console.log('✅ 所有测试完成');
    console.log('═'.repeat(60));
  } catch (err) {
    console.error(`[❌] 测试失败: ${err.message}`);
  }
}

/**
 * 显示菜单
 */
function showMenu() {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║   🎭 Twitter Dance - 高级功能菜单                       ║
╚═══════════════════════════════════════════════════════════╝

📋 命令列表:

1️⃣  账户统计
   node test-advanced-features.js stats

2️⃣  获取通知（Timeline 备用方案）
   node test-advanced-features.js notifications

2️⃣+ 获取完整通知（API v2 - 需要专业 API Key）
   node test-advanced-features.js notifications-v2

3️⃣  自动回复
   node test-advanced-features.js reply <tweetId> <replyText>

4️⃣  推文指标
   node test-advanced-features.js metrics <tweetId>

5️⃣  时间线分析
   node test-advanced-features.js timeline-analytics

6️⃣  互动周期分析
   node test-advanced-features.js engagement-hours

7️⃣  批量点赞
   node test-advanced-features.js bulk-like <tweetId1> <tweetId2> ...

8️⃣  对话线程
   node test-advanced-features.js conversation <tweetId>

🚀 运行所有测试
   node test-advanced-features.js all

📌 环境变量配置:
   export APIDANCE_API_KEY=your-api-key
   export TWITTER_AUTH_TOKEN=your-auth-token

`);
}

main();
