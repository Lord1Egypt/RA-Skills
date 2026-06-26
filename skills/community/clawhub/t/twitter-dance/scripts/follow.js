#!/usr/bin/env node

/**
 * 关注管理工具
 * 
 * 用法：
 * node scripts/follow.js --follow=USER_ID              # 关注用户
 * node scripts/follow.js --unfollow=USER_ID            # 取消关注
 * node scripts/follow.js --followers --count=50        # 获取粉丝列表
 * node scripts/follow.js --following --count=50        # 获取关注列表
 */

const TwitterDanceAPIClient = require('../src/twitter-api-client');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

async function main() {
  try {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
      console.log(`
╔════════════════════════════════════════════╗
║   关注管理工具                              ║
╚════════════════════════════════════════════╝

用法：
  关注用户:     node scripts/follow.js --follow=USER_ID
  取消关注:     node scripts/follow.js --unfollow=USER_ID
  获取粉丝:     node scripts/follow.js --followers --count=50
  获取关注:     node scripts/follow.js --following --count=50

例子：
  node scripts/follow.js --follow=123456789
  node scripts/follow.js --followers --count=100
`);
      return;
    }

    const client = new TwitterDanceAPIClient({ verbose: true });

    // 解析参数
    let action = null;
    let userId = null;
    let count = 20;

    for (const arg of args) {
      if (arg.startsWith('--follow=')) {
        action = 'follow';
        userId = arg.split('=')[1];
      } else if (arg.startsWith('--unfollow=')) {
        action = 'unfollow';
        userId = arg.split('=')[1];
      } else if (arg === '--followers') {
        action = 'followers';
      } else if (arg === '--following') {
        action = 'following';
      } else if (arg.startsWith('--count=')) {
        count = parseInt(arg.split('=')[1]) || 20;
      }
    }

    if (!action) {
      console.error('❌ 请指定操作: --follow, --unfollow, --followers, --following');
      process.exit(1);
    }

    console.log('\n╔════════════════════════════════════════════╗');
    console.log(`║   关注管理: ${action.toUpperCase().padEnd(28)}║`);
    console.log('╚════════════════════════════════════════════╝\n');

    let result;

    switch (action) {
      case 'follow':
        if (!userId) {
          console.error('❌ 请指定用户 ID (--follow=USER_ID)');
          process.exit(1);
        }
        result = await client.followUser(userId);
        console.log(`✅ 已关注用户！\n`);
        break;

      case 'unfollow':
        if (!userId) {
          console.error('❌ 请指定用户 ID (--unfollow=USER_ID)');
          process.exit(1);
        }
        result = await client.unfollowUser(userId);
        console.log(`✅ 已取消关注！\n`);
        break;

      case 'followers':
        console.log(`[📥] 获取最近 ${count} 个粉丝...\n`);
        result = await client.getFollowers({ count });

        if (result.success && result.followers.length > 0) {
          console.log(`✅ 获取了 ${result.count} 个粉丝\n`);

          result.followers.forEach((user, index) => {
            console.log(`${index + 1}. @${user.screen_name}`);
            console.log(`   👤 ${user.name}`);
            console.log(`   👥 粉丝: ${user.followers_count.toLocaleString()}`);
            console.log('');
          });

          // 保存到文件
          const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
          const logPath = path.join(__dirname, '../logs', `followers-${timestamp}.jsonl`);
          
          if (!fs.existsSync(path.dirname(logPath))) {
            fs.mkdirSync(path.dirname(logPath), { recursive: true });
          }

          const lines = result.followers.map(user => 
            JSON.stringify({
              id: user.id_str,
              screen_name: user.screen_name,
              name: user.name,
              followers_count: user.followers_count
            })
          ).join('\n');

          fs.writeFileSync(logPath, lines);
          console.log(`💾 已保存到: ${logPath}\n`);
        } else {
          console.log('⚠️  没有找到粉丝\n');
        }
        break;

      case 'following':
        console.log(`[📤] 获取最近 ${count} 个关注...\n`);
        result = await client.getFollowing({ count });

        if (result.success && result.following.length > 0) {
          console.log(`✅ 获取了 ${result.count} 个关注\n`);

          result.following.forEach((user, index) => {
            console.log(`${index + 1}. @${user.screen_name}`);
            console.log(`   👤 ${user.name}`);
            console.log(`   👥 粉丝: ${user.followers_count.toLocaleString()}`);
            console.log('');
          });

          // 保存到文件
          const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
          const logPath = path.join(__dirname, '../logs', `following-${timestamp}.jsonl`);
          
          if (!fs.existsSync(path.dirname(logPath))) {
            fs.mkdirSync(path.dirname(logPath), { recursive: true });
          }

          const lines = result.following.map(user => 
            JSON.stringify({
              id: user.id_str,
              screen_name: user.screen_name,
              name: user.name,
              followers_count: user.followers_count
            })
          ).join('\n');

          fs.writeFileSync(logPath, lines);
          console.log(`💾 已保存到: ${logPath}\n`);
        } else {
          console.log('⚠️  没有找到关注\n');
        }
        break;
    }

  } catch (err) {
    console.error(`\n❌ 错误: ${err.message}\n`);
    process.exit(1);
  }
}

main();
