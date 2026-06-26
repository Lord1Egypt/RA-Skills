#!/usr/bin/env node

/**
 * Twitter Dance - 自动发推脚本
 * 
 * 使用 apidance.pro API + Kimi 生成
 * 
 * 使用方法：
 *   node scripts/auto-tweet.js                    # 生成推文 + 发推
 *   node scripts/auto-tweet.js --draft-only      # 仅生成草稿，不发推
 *   node scripts/auto-tweet.js --count=5         # 发 5 条推文
 */

const TwitterDanceAPIClient = require('../src/twitter-api-client');
const TweetGenerator = require('../src/tweet-generator');
const fs = require('fs');
const path = require('path');

require('dotenv').config({ path: path.join(__dirname, '../.env') });

async function main() {
  console.log(`
╔════════════════════════════════════════════╗
║   🎭 Twitter Dance - 自动发推系统        ║
║   基于 apidance.pro + Kimi AI              ║
╚════════════════════════════════════════════╝
`);

  const args = process.argv.slice(2);
  const draftOnly = args.includes('--draft-only');
  const count = parseInt(args.find(a => a.startsWith('--count='))?.split('=')[1] || '1');

  console.log(`[⚙️] 配置：`);
  console.log(`  发推数量：${count}`);
  console.log(`  模式：${draftOnly ? '草稿模式' : '发推模式'}\n`);

  const generator = new TweetGenerator({
    kimiApiKey: process.env.KIMI_API_KEY,
    verbose: true
  });

  const client = new TwitterDanceAPIClient({
    apiKey: process.env.APIDANCE_API_KEY,
    authToken: process.env.TWITTER_AUTH_TOKEN,
    verbose: true
  });

  try {
    // 1. 检查配置
    console.log('[🔍] 检查 API 配置...\n');
    
    if (draftOnly) {
      console.log('[✅] 草稿模式：无需 AuthToken');
    } else {
      if (!process.env.TWITTER_AUTH_TOKEN) {
        console.error('[❌] 缺少 TWITTER_AUTH_TOKEN');
        console.error('获取方式：X.com 设置 → 账户与隐私 → 开发者设置\n');
        process.exit(1);
      }
      console.log('[✅] AuthToken 已配置');
    }

    // 2. 生成推文
    console.log('\n[步骤 1/3] 生成推文\n');
    
    const tweets = [];
    for (let i = 0; i < count; i++) {
      const tweet = await generator.generate();
      tweets.push(tweet);
      
      console.log(`\n推文 ${i + 1}/${count}：`);
      console.log('─'.repeat(50));
      console.log(tweet.text);
      console.log('─'.repeat(50));
      console.log(`📊 长度: ${tweet.length}/280 | 来源: ${tweet.source}`);
    }

    if (draftOnly) {
      console.log('\n[✅] 草稿已生成');
      saveToFile(tweets);
      return;
    }

    // 3. 发推
    console.log('\n[步骤 2/3] 发推中\n');
    
    const results = [];
    for (let i = 0; i < tweets.length; i++) {
      const tweet = tweets[i];
      
      try {
        console.log(`\n[${i + 1}/${count}] 发布推文...`);
        const result = await client.tweet(tweet.text);
        results.push({ success: true, ...result });
        
        console.log(`[✅] 推文已发布: ${result.tweetId}`);

        // 推文间隔（避免速率限制）
        if (i < tweets.length - 1) {
          const delay = 3000;
          console.log(`[⏳] 等待 ${delay / 1000} 秒...\n`);
          await new Promise(r => setTimeout(r, delay));
        }

      } catch (err) {
        results.push({ success: false, error: err.message });
        console.error(`[❌] 发推失败: ${err.message}`);
      }
    }

    // 4. 总结
    console.log('\n[步骤 3/3] 完成\n');
    
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;

    console.log('═'.repeat(50));
    console.log(`📊 结果汇总`);
    console.log('═'.repeat(50));
    console.log(`✅ 成功：${successful}/${count}`);
    console.log(`❌ 失败：${failed}/${count}`);
    
    if (successful > 0) {
      console.log('\n📝 已发布的推文：');
      results.filter(r => r.success).forEach((r, i) => {
        console.log(`  ${i + 1}. ${r.tweetId}`);
      });
    }

    // 5. 保存日志
    saveLog(tweets, results);

    console.log('\n[✅] 任务完成！\n');

  } catch (err) {
    console.error('\n[❌] 错误:', err.message);
    process.exit(1);
  }
}

/**
 * 保存推文到文件
 */
function saveToFile(tweets) {
  const logsDir = path.join(__dirname, '..', 'logs');
  
  if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true });
  }

  const filename = `tweets-${new Date().toISOString().split('T')[0]}.jsonl`;
  const filepath = path.join(logsDir, filename);

  tweets.forEach(tweet => {
    fs.appendFileSync(filepath, JSON.stringify({
      timestamp: new Date().toISOString(),
      ...tweet
    }) + '\n');
  });

  console.log(`\n[💾] 已保存到 ${filepath}`);
}

/**
 * 保存发推日志
 */
function saveLog(tweets, results) {
  const logsDir = path.join(__dirname, '..', 'logs');
  
  if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true });
  }

  const date = new Date().toISOString().split('T')[0];
  const filename = `results-${date}.jsonl`;
  const filepath = path.join(logsDir, filename);

  const entry = {
    timestamp: new Date().toISOString(),
    count: tweets.length,
    successful: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    tweets: tweets.map(t => ({
      text: t.text.substring(0, 100),
      length: t.length,
      topic: t.topic
    })),
    results
  };

  fs.appendFileSync(filepath, JSON.stringify(entry) + '\n');
}

main();
