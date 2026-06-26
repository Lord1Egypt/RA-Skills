#!/usr/bin/env node

/**
 * Twitter Dance - 获取和回复评论 (GraphQL 版本)
 * 
 * 使用 apidance.pro GraphQL API
 * 
 * 用法：
 *   node get-comments-graphql.js --tweet-id=<ID> [--dry-run]
 */

require('dotenv').config();
const https = require('https');

const API_KEY = process.env.APIDANCE_API_KEY;
const AUTH_TOKEN = process.env.TWITTER_AUTH_TOKEN;

if (!API_KEY || !AUTH_TOKEN) {
  console.error('❌ 错误：缺少 APIDANCE_API_KEY 或 TWITTER_AUTH_TOKEN');
  process.exit(1);
}

// GraphQL 查询：获取推文的回复
const GET_REPLIES_QUERY = `
query TweetDetail($tweetId: String!) {
  tweet(id: $tweetId) {
    rest_id
    core {
      user_results {
        result {
          id
          legacy {
            screen_name
            name
          }
        }
      }
    }
    legacy {
      created_at
      full_text
      public_metrics {
        reply_count
        retweet_count
        favorite_count
        view_count
      }
    }
    replies(first: 10) {
      edges {
        node {
          rest_id
          core {
            user_results {
              result {
                id
                legacy {
                  screen_name
                  name
                }
              }
            }
          }
          legacy {
            created_at
            full_text
            public_metrics {
              reply_count
              retweet_count
              favorite_count
            }
          }
        }
      }
    }
  }
}
`;

// GraphQL 查询：获取用户时间线
const GET_TIMELINE_QUERY = `
query UserTimeline($userId: String!, $count: Int) {
  user(id: $userId) {
    result {
      timeline_v2(first: $count) {
        edges {
          node {
            tweet_results {
              result {
                rest_id
                legacy {
                  created_at
                  full_text
                }
              }
            }
          }
        }
      }
    }
  }
}
`;

// GraphQL Mutation：回复推文
const CREATE_REPLY_MUTATION = `
mutation CreateTweet($tweet_text: String!, $in_reply_to_tweet_id: String!) {
  create_tweet(
    tweet_text: $tweet_text
    reply: {
      in_reply_to_tweet_id: $in_reply_to_tweet_id
      exclude_reply_user_ids: []
    }
  ) {
    tweet_results {
      result {
        rest_id
      }
    }
  }
}
`;

// 发送 GraphQL 请求
async function graphqlRequest(query, variables = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      query,
      variables
    });

    const options = {
      hostname: 'api.apidance.pro',
      path: '/graphql',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'Authtoken': AUTH_TOKEN,  // 注意：大写 A
        'apikey': API_KEY,
        'User-Agent': 'Apidog/1.0.0 (https://apidog.com)'
      }
    };

    console.log(`[📡] GraphQL 请求...\n`);

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          console.log(`[✅] 状态: ${res.statusCode}\n`);
          resolve(json);
        } catch (e) {
          console.log(`[❌] 解析失败: ${data.substring(0, 200)}\n`);
          reject(new Error(`解析失败: ${data}`));
        }
      });
    });

    req.on('error', (err) => {
      reject(err);
    });

    req.write(body);
    req.end();
  });
}

// AI 回复模板
const replyTemplates = {
  感谢: ['感谢你的反馈！😊', '谢谢分享！', '感谢支持！💪'],
  询问: ['很好的问题！👇', '这是个有趣的观点', '能分享更多细节吗？'],
  同意: ['完全同意！👏', '说得太好了！', '100% 同意！'],
  鼓励: ['继续加油！🚀', '保持热情！', '你做得很好！'],
  默认: ['谢谢你的评论！😄', '感谢互动！', '期待继续讨论！']
};

function generateReply(text) {
  if (!text) return replyTemplates.默认[0];
  
  const lower = text.toLowerCase();
  if (lower.includes('谢谢') || lower.includes('感谢')) {
    return replyTemplates.感谢[Math.floor(Math.random() * replyTemplates.感谢.length)];
  }
  if (lower.includes('?') || lower.includes('？') || lower.includes('怎么')) {
    return replyTemplates.询问[Math.floor(Math.random() * replyTemplates.询问.length)];
  }
  if (lower.includes('同意') || lower.includes('赞成') || lower.includes('好')) {
    return replyTemplates.同意[Math.floor(Math.random() * replyTemplates.同意.length)];
  }
  if (lower.includes('加油') || lower.includes('继续')) {
    return replyTemplates.鼓励[Math.floor(Math.random() * replyTemplates.鼓励.length)];
  }
  
  return replyTemplates.默认[Math.floor(Math.random() * replyTemplates.默认.length)];
}

async function main() {
  const args = {
    tweetId: null,
    dryRun: false
  };

  process.argv.slice(2).forEach(arg => {
    if (arg.startsWith('--tweet-id=')) {
      args.tweetId = arg.split('=')[1];
    } else if (arg === '--dry-run') {
      args.dryRun = true;
    }
  });

  if (!args.tweetId) {
    console.log(`
📱 Twitter Dance - GraphQL 评论获取和回复

用法:
  node get-comments-graphql.js --tweet-id=<推文ID> [--dry-run]

示例:
  node get-comments-graphql.js --tweet-id=2031936903918883025 --dry-run

    `);
    process.exit(1);
  }

  try {
    console.log('═══════════════════════════════════════════════════');
    console.log('💬 Twitter 评论获取 - GraphQL 版本');
    console.log('═══════════════════════════════════════════════════\n');

    console.log(`📌 推文 ID: ${args.tweetId}`);
    console.log(`🔍 获取评论中...\n`);

    // 查询推文的回复
    const result = await graphqlRequest(GET_REPLIES_QUERY, {
      tweetId: args.tweetId
    });

    // 检查是否有数据
    if (!result.data || !result.data.tweet) {
      console.log('❌ 找不到推文或没有权限访问\n');
      console.log('响应:', JSON.stringify(result, null, 2).substring(0, 500));
      return;
    }

    const tweet = result.data.tweet;
    const replies = tweet.replies?.edges || [];

    if (!replies || replies.length === 0) {
      console.log('😶 这条推文还没有评论\n');
      return;
    }

    console.log(`✅ 找到 ${replies.length} 条评论\n`);
    console.log('═══════════════════════════════════════════════════\n');

    // 显示评论
    const replyPlan = [];

    for (let i = 0; i < replies.length; i++) {
      const reply = replies[i].node;
      const author = reply.core?.user_results?.result?.legacy?.screen_name || 'unknown';
      const text = reply.legacy?.full_text || '';
      const replyText = generateReply(text);

      console.log(`${i + 1}. @${author}`);
      console.log(`   💬 "${text.substring(0, 80)}${text.length > 80 ? '...' : ''}"`);
      console.log(`   ↩️  计划回复: "${replyText}"`);
      console.log();

      replyPlan.push({
        id: reply.rest_id,
        author,
        text,
        reply: replyText
      });
    }

    console.log('═══════════════════════════════════════════════════\n');

    if (args.dryRun) {
      console.log(`🔍 【模拟模式】准备回复 ${replyPlan.length} 条评论`);
      console.log('   移除 --dry-run 参数来真正发送\n');
      return;
    }

    console.log(`🚀 正在发送 ${replyPlan.length} 条回复...\n`);

    let successCount = 0;
    let failureCount = 0;

    for (const plan of replyPlan) {
      try {
        console.log(`⏳ 回复 @${plan.author}...`);
        
        const replyResult = await graphqlRequest(CREATE_REPLY_MUTATION, {
          tweet_text: plan.reply,
          in_reply_to_tweet_id: plan.id
        });

        if (replyResult.data?.create_tweet?.tweet_results?.result?.rest_id) {
          console.log(`✅ 成功！\n`);
          successCount++;
        } else {
          console.log(`⚠️ 回复失败\n`);
          failureCount++;
        }

        // 延迟
        await new Promise(r => setTimeout(r, 1000 + Math.random() * 1000));
      } catch (err) {
        console.log(`❌ 错误: ${err.message}\n`);
        failureCount++;
      }
    }

    console.log('═══════════════════════════════════════════════════');
    console.log(`✅ 成功: ${successCount}`);
    console.log(`❌ 失败: ${failureCount}`);
    console.log('═══════════════════════════════════════════════════\n');

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
