#!/usr/bin/env node

/**
 * Twitter 推文交互工具
 * 
 * 用法：
 * node scripts/interact.js --like=1234567890              # 点赞某条推文
 * node scripts/interact.js --retweet=1234567890           # 转发某条推文
 * node scripts/interact.js --reply=1234567890 --text="你好"  # 回复某条推文
 * node scripts/interact.js --get=1234567890               # 获取推文详情
 * node scripts/interact.js --delete=1234567890            # 删除我的推文
 */

const TwitterDanceAPIClient = require('../src/twitter-api-client');
require('dotenv').config();

async function main() {
  try {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
      console.log(`
╔════════════════════════════════════════════╗
║   Twitter 推文交互工具                    ║
╚════════════════════════════════════════════╝

用法：
  点赞:     node scripts/interact.js --like=TWEET_ID
  转发:     node scripts/interact.js --retweet=TWEET_ID
  回复:     node scripts/interact.js --reply=TWEET_ID --text="内容"
  获取信息: node scripts/interact.js --get=TWEET_ID
  删除推文: node scripts/interact.js --delete=TWEET_ID

例子：
  node scripts/interact.js --like=1234567890
  node scripts/interact.js --reply=1234567890 --text="很棒！"
`);
      return;
    }

    const client = new TwitterDanceAPIClient({ verbose: true });

    // 解析参数
    let action = null;
    let tweetId = null;
    let text = null;

    for (const arg of args) {
      if (arg.startsWith('--like=')) {
        action = 'like';
        tweetId = arg.split('=')[1];
      } else if (arg.startsWith('--retweet=')) {
        action = 'retweet';
        tweetId = arg.split('=')[1];
      } else if (arg.startsWith('--reply=')) {
        action = 'reply';
        tweetId = arg.split('=')[1];
      } else if (arg.startsWith('--get=')) {
        action = 'get';
        tweetId = arg.split('=')[1];
      } else if (arg.startsWith('--delete=')) {
        action = 'delete';
        tweetId = arg.split('=')[1];
      } else if (arg.startsWith('--text=')) {
        text = arg.split('=')[1];
      }
    }

    if (!action) {
      console.error('❌ 请指定操作: --like, --retweet, --reply, --get, --delete');
      process.exit(1);
    }

    console.log('\n╔════════════════════════════════════════════╗');
    console.log(`║   推文交互: ${action.toUpperCase().padEnd(30)}║`);
    console.log('╚════════════════════════════════════════════╝\n');

    let result;

    switch (action) {
      case 'like':
        result = await client.likeTweet(tweetId);
        console.log(`✅ 点赞成功！\n`);
        break;

      case 'retweet':
        result = await client.retweet(tweetId);
        console.log(`✅ 转发成功！\n`);
        break;

      case 'reply':
        if (!text) {
          console.error('❌ 回复内容不能为空 (--text="内容")');
          process.exit(1);
        }
        result = await client.replyTweet(tweetId, text);
        console.log(`✅ 回复已发送！\n`);
        break;

      case 'get':
        result = await client.getTweet(tweetId);
        console.log('✅ 推文信息：');
        console.log(JSON.stringify(result.tweet, null, 2));
        console.log('');
        break;

      case 'delete':
        result = await client.deleteTweet(tweetId);
        console.log(`✅ 推文已删除！\n`);
        break;
    }

  } catch (err) {
    console.error(`\n❌ 错误: ${err.message}\n`);
    process.exit(1);
  }
}

main();
