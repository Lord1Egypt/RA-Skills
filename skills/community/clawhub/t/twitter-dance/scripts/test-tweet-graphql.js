#!/usr/bin/env node

/**
 * Twitter Dance - GraphQL CreateTweet 测试脚本
 * 
 * 直接使用 apidance.pro 的 GraphQL API 发推
 * 
 * 使用方法：
 *   node scripts/test-tweet-graphql.js "你的推文内容"
 */

const TwitterDanceAPIClient = require('../src/twitter-api-client');
const path = require('path');

require('dotenv').config({ path: path.join(__dirname, '../.env') });

async function main() {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║   🎭 Twitter Dance - GraphQL CreateTweet 测试         ║
║   使用 apidance.pro 的官方 GraphQL API                  ║
╚══════════════════════════════════════════════════════════╝
`);

  // 从命令行参数获取推文内容，或使用默认内容
  const tweetText = process.argv[2] || '🚀 Hello from Twitter Dance! #OpenClaw #Automation';

  console.log(`[📝] 推文内容: "${tweetText}"\n`);

  // 初始化客户端（verbose=2 显示完整 GraphQL 请求和响应）
  const client = new TwitterDanceAPIClient({
    apiKey: process.env.APIDANCE_API_KEY,
    authToken: process.env.TWITTER_AUTH_TOKEN,
    verbose: 2  // 显示完整的请求和响应日志
  });

  try {
    // 检查必要的环境变量
    console.log('[🔍] 检查环境变量...');
    
    if (!process.env.APIDANCE_API_KEY) {
      throw new Error('缺少 APIDANCE_API_KEY 环境变量');
    }
    console.log('  ✅ APIDANCE_API_KEY 已设置');

    if (!process.env.TWITTER_AUTH_TOKEN) {
      throw new Error('缺少 TWITTER_AUTH_TOKEN 环境变量');
    }
    console.log('  ✅ TWITTER_AUTH_TOKEN 已设置\n');

    // 方案 1：简单推文（纯文本）
    console.log('═══════════════════════════════════════════════════════════');
    console.log('方案 1：发送纯文本推文');
    console.log('═══════════════════════════════════════════════════════════\n');

    const result1 = await client.tweet(tweetText);
    console.log('\n✅ 发推成功！');
    console.log(`📊 推文 ID: ${result1.tweetId}`);
    console.log(`⏰ 发布时间: ${result1.timestamp}`);
    console.log(`📝 字数: ${result1.length}/280\n`);

    // 方案 2：带回复的推文（需要被回复推文的 ID）
    console.log('═══════════════════════════════════════════════════════════');
    console.log('方案 2：回复推文（需要现有推文 ID）');
    console.log('═══════════════════════════════════════════════════════════\n');
    console.log('示例用法：');
    console.log(`  await client.tweet("回复内容", {
    inReplyToTweetId: "1234567890123456789"
  });
\n`);

    // 方案 3：带媒体的推文（需要媒体 ID）
    console.log('═══════════════════════════════════════════════════════════');
    console.log('方案 3：带媒体的推文（需要媒体 ID）');
    console.log('═══════════════════════════════════════════════════════════\n');
    console.log('示例用法：');
    console.log(`  await client.tweet("图片推文内容", {
    media: [
      { media_id: "1869610428579606520" },  // 媒体 ID
      { media_id: "1869610428579606521" }   // 多个媒体
    ]
  });
\n`);

    // 完整 API 格式说明
    console.log('═══════════════════════════════════════════════════════════');
    console.log('完整 GraphQL 请求格式（供参考）');
    console.log('═══════════════════════════════════════════════════════════\n');
    console.log(`POST /graphql/CreateTweet

请求头：
  Authtoken: ${process.env.TWITTER_AUTH_TOKEN || '<your-token>'}
  apikey: ${process.env.APIDANCE_API_KEY || '<your-api-key>'}
  User-Agent: Apidog/1.0.0 (https://apidog.com)
  Content-Type: application/json
  Accept: */*

请求体（variables 格式）：
{
  "variables": {
    "tweet_text": "推文内容",
    "dark_request": false,
    "reply": {
      "in_reply_to_tweet_id": null,
      "exclude_reply_user_ids": []
    },
    "media": {
      "media_entities": [],
      "possibly_sensitive": false
    },
    "semantic_annotation_ids": [],
    "includePromotedContent": false
  }
}\n`);

    console.log('═══════════════════════════════════════════════════════════');
    console.log('✅ 测试完成！');
    console.log('═══════════════════════════════════════════════════════════\n');

    // 显示原始响应（用于调试）
    if (result1.rawResponse) {
      console.log('原始 API 响应：');
      console.log(JSON.stringify(result1.rawResponse, null, 2));
      console.log('\n');
    }

  } catch (err) {
    console.error('\n[❌] 错误：');
    console.error(`  ${err.message}\n`);
    
    if (err.message.includes('缺少')) {
      console.error('解决方案：');
      console.error('  1. 从 https://t.me/shingle 购买 APIDANCE_API_KEY');
      console.error('  2. 从 X.com/settings 获取 TWITTER_AUTH_TOKEN');
      console.error('  3. 导出环境变量：');
      console.error('     export APIDANCE_API_KEY="your-api-key"');
      console.error('     export TWITTER_AUTH_TOKEN="your-auth-token"\n');
    }

    process.exit(1);
  }
}

main();
