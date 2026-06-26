#!/usr/bin/env node

/**
 * 获取我的 Twitter 账户信息
 */

const TwitterDanceAPIClient = require('../src/twitter-api-client');
const fs = require('fs');
const path = require('path');

require('dotenv').config({ path: path.join(__dirname, '../.env') });

async function main() {
  try {
    const client = new TwitterDanceAPIClient({ verbose: true });

    console.log('\n╔════════════════════════════════════════════╗');
    console.log('║   获取账户信息                              ║');
    console.log('╚════════════════════════════════════════════╝\n');

    const info = await client.getMyInfo();

    if (info.success) {
      const user = info.user;

      console.log(`\n✅ 账户信息：\n`);
      console.log(`  👤 用户名: @${user.screen_name}`);
      console.log(`  📝 昵称: ${user.name}`);
      console.log(`  🆔 ID: ${user.id}`);
      console.log(`  📊 粉丝: ${user.followers_count.toLocaleString()}`);
      console.log(`  👥 关注: ${user.friends_count.toLocaleString()}`);
      console.log(`  📌 推文数: ${user.statuses_count.toLocaleString()}`);
      console.log(`  📖 简介: ${user.description || '无'}`);
      console.log(`\n`);

      // 保存到文件
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const logPath = path.join(__dirname, '../logs', `my-info-${timestamp}.json`);
      
      if (!fs.existsSync(path.dirname(logPath))) {
        fs.mkdirSync(path.dirname(logPath), { recursive: true });
      }

      fs.writeFileSync(logPath, JSON.stringify({
        timestamp: new Date().toISOString(),
        user
      }, null, 2));

      console.log(`💾 已保存到: ${logPath}\n`);
    }
  } catch (err) {
    console.error(`\n❌ 错误: ${err.message}\n`);
    process.exit(1);
  }
}

main();
