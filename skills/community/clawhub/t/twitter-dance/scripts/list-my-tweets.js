#!/usr/bin/env node

/**
 * 列出我的推文
 * 
 * 用法：
 * node scripts/list-my-tweets.js              # 获取最近 20 条
 * node scripts/list-my-tweets.js --count=50   # 获取最近 50 条
 * node scripts/list-my-tweets.js --no-rt      # 排除转发
 */

const TwitterDanceAPIClient = require('../src/twitter-api-client');
const fs = require('fs');
const path = require('path');

require('dotenv').config({ path: path.join(__dirname, '../.env') });

async function main() {
  try {
    const args = process.argv.slice(2);
    
    // 解析参数
    let count = 20;
    let includeRetweets = true;
    let excludeReplies = false;

    args.forEach(arg => {
      if (arg.startsWith('--count=')) {
        count = parseInt(arg.split('=')[1]) || 20;
      }
      if (arg === '--no-rt') {
        includeRetweets = false;
      }
      if (arg === '--no-replies') {
        excludeReplies = true;
      }
    });

    const client = new TwitterDanceAPIClient({ verbose: false });

    console.log('\n╔════════════════════════════════════════════╗');
    console.log('║   我的推文列表                              ║');
    console.log('╚════════════════════════════════════════════╝\n');

    console.log(`[📝] 获取最近 ${count} 条推文...\n`);

    const result = await client.getMyTweets({
      count,
      includeRetweets,
      excludeReplies
    });

    if (result.success && result.tweets.length > 0) {
      console.log(`✅ 获取了 ${result.count} 条推文\n`);

      result.tweets.forEach((tweet, index) => {
        console.log(`${index + 1}. ${tweet.text.substring(0, 100)}${tweet.text.length > 100 ? '...' : ''}`);
        console.log(`   🆔 ID: ${tweet.id_str}`);
        console.log(`   ❤️  点赞: ${tweet.favorite_count} | 🔄 转发: ${tweet.retweet_count}`);
        console.log(`   📅 ${new Date(tweet.created_at).toLocaleString('zh-CN')}`);
        console.log('');
      });

      // 保存到文件
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const logPath = path.join(__dirname, '../logs', `my-tweets-${timestamp}.jsonl`);
      
      if (!fs.existsSync(path.dirname(logPath))) {
        fs.mkdirSync(path.dirname(logPath), { recursive: true });
      }

      const lines = result.tweets.map(tweet => 
        JSON.stringify({
          id: tweet.id_str,
          text: tweet.text,
          likes: tweet.favorite_count,
          retweets: tweet.retweet_count,
          created_at: tweet.created_at
        })
      ).join('\n');

      fs.writeFileSync(logPath, lines);

      console.log(`💾 已保存到: ${logPath}\n`);
    } else {
      console.log('⚠️  没有找到推文\n');
    }
  } catch (err) {
    console.error(`\n❌ 错误: ${err.message}\n`);
    process.exit(1);
  }
}

main();
