const { Scraper } = require('@the-convocation/twitter-scraper');
const { writeFile } = require('fs').promises;
const path = require('path');

// 免费无API版X爬虫
const scraper = new Scraper();

// 多维表格账号列表（已内置）
const ACCOUNTS = [
  "OpenAI", "GoogleDeepMind", "nvidia", "NVIDIAAI", "AnthropicAI", "MetaAI",
  "deepseek_ai", "Alibaba_Qwen", "midjourney", "Kimi_Moonshot", "MiniMax_AI",
  "BytedanceTalk", "DeepMind", "GoogleAI", "GroqInc", "Hailuo_AI", "MIT_CSAIL",
  "IBMData", "elonmusk", "sama", "zuck", "demishassabis", "DarioAmodei",
  "karpathy", "ylecun", "ilyasut", "AndrewYNg", "jeffdean", "drfeifei",
  "Thom_Wolf", "danielaamodei", "gdb", "GaryMarcus", "JustinLin610", "steipete",
  "ESYudkowsky", "erikbryn", "alliekmiller", "tunguz", "Ronald_vanLoon",
  "DeepLearn007", "nigewillson", "petitegeek", "YuHelenYu", "TamaraMcCleary"
];

// 计算活跃度评分
function calculateActivityScore(tweets) {
  if (tweets.length === 0) return { score: 0, level: '—', totalEngagement: 0 };
  
  const totalEngagement = tweets.reduce((sum, tweet) => {
    return sum + (tweet.likes || 0) + (tweet.retweets || 0) * 2 + (tweet.replies || 0) * 3;
  }, 0);
  
  // 评分规则：10000+ ⭐⭐⭐⭐⭐, 5000-9999 ⭐⭐⭐⭐, 1000-4999 ⭐⭐⭐, 100-999 ⭐⭐, 1-99 ⭐
  let score, level;
  if (totalEngagement >= 10000) {
    score = 5;
    level = '⭐⭐⭐⭐⭐';
  } else if (totalEngagement >= 5000) {
    score = 4;
    level = '⭐⭐⭐⭐';
  } else if (totalEngagement >= 1000) {
    score = 3;
    level = '⭐⭐⭐';
  } else if (totalEngagement >= 100) {
    score = 2;
    level = '⭐⭐';
  } else if (totalEngagement > 0) {
    score = 1;
    level = '⭐';
  } else {
    score = 0;
    level = '—';
  }
  
  return { score, level, totalEngagement };
}

// 获取账号过去24小时的推文
async function getAccountTweets(username, sinceHours = 24) {
  try {
    console.log(`正在获取 @${username} 的推文...`);
    const tweets = [];
    const sinceTime = new Date(Date.now() - sinceHours * 60 * 60 * 1000);
    
    for await (const tweet of scraper.getTweets(username, 10)) { // 最多获取10条最新推文
      if (new Date(tweet.createdAt) < sinceTime) break;
      
      tweets.push({
        id: tweet.id,
        text: tweet.text,
        createdAt: tweet.createdAt,
        likes: tweet.likes,
        retweets: tweet.retweets,
        replies: tweet.replies,
        views: tweet.views,
        url: `https://x.com/${username}/status/${tweet.id}`
      });
    }
    
    return tweets;
  } catch (error) {
    console.error(`获取 @${username} 推文失败:`, error.message);
    return [];
  }
}

// 生成日报
async function generateDailyReport() {
  console.log('🚀 开始生成免费版X账号动态日报...');
  const now = new Date();
  const sinceTime = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  
  const accountUpdates = [];
  const topUpdates = [];
  
  // 使用已登录的浏览器会话（自动复用当前Chrome的X登录状态）
  await scraper.useCookiesFromBrowser('chrome');
  
  for (const username of ACCOUNTS) {
    const tweets = await getAccountTweets(username);
    if (tweets.length === 0) {
      accountUpdates.push({
        username,
        type: username.match(/^[A-Z]/) && !username.includes('_') ? '国际机构' : '国际个人',
        tweets: [],
        activity: { score: 0, level: '—', totalEngagement: 0 },
        summary: '无动态'
      });
      continue;
    }
    
    const activity = calculateActivityScore(tweets);
    const summary = tweets[0].text.substring(0, 50) + (tweets[0].text.length > 50 ? '...' : '');
    
    const accountData = {
      username,
      type: username.match(/^[A-Z]/) && !username.includes('_') ? '国际机构' : '国际个人',
      tweets,
      activity,
      summary
    };
    
    accountUpdates.push(accountData);
    
    // 活跃度≥4分的加入重点关注
    if (activity.score >= 4) {
      topUpdates.push(accountData);
    }
    
    // 避免请求过快
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  // 按活跃度排序
  accountUpdates.sort((a, b) => b.activity.score - a.activity.score);
  topUpdates.sort((a, b) => b.activity.score - a.activity.score);
  
  // 生成 Markdown 内容
  let report = `# AI Twitter/X 账号动态日报（免费版）· ${now.toLocaleDateString('zh-CN')}\n\n`;
  report += `**数据说明**：搜索时间范围为过去 24 小时（${sinceTime.toLocaleDateString('zh-CN')} - ${now.toLocaleDateString('zh-CN')}）\n`;
  report += `**技术说明**：使用无API开源爬虫，无需X开发者账号，完全免费\n\n`;
  
  // 重点内容
  if (topUpdates.length > 0) {
    report += `## 🔥 今日最值得关注的内容\n\n`;
    topUpdates.forEach((update, index) => {
      const topTweet = update.tweets[0];
      report += `### ${index + 1}. @${update.username} — ${update.summary}\n\n`;
      report += `**账号**：[@${update.username}](https://x.com/${update.username}) · **热度**：${(topTweet.views || 0).toLocaleString()} 浏览 · ${(topTweet.likes || 0).toLocaleString()} 点赞 · ${(topTweet.retweets || 0).toLocaleString()} 转发\n\n`;
      report += `**核心内容**：${topTweet.text}\n\n`;
      report += `**💡 为什么值得关注**：该账号今日活跃度达到 ${update.activity.level}，总互动量 ${update.activity.totalEngagement.toLocaleString()}，是近期行业重点动态。\n\n`;
    });
  }
  
  // 完整活跃度总览
  report += `## 📋 完整账号活跃度总览\n\n`;
  report += `| 账号 | 类别 | 今日活跃度 | 主要内容 |\n`;
  report += `|------|------|------------|----------|\n`;
  
  accountUpdates.forEach(update => {
    report += `| @${update.username} | ${update.type} | ${update.activity.level} | ${update.summary} |\n`;
  });
  
  // 关注建议
  report += `\n## 💡 关注建议\n\n`;
  
  const highValue = accountUpdates.filter(u => u.activity.score >= 4);
  const mediumValue = accountUpdates.filter(u => u.activity.score === 2 || u.activity.score === 3);
  const lowValue = accountUpdates.filter(u => u.activity.score <= 1);
  
  if (highValue.length > 0) {
    report += `### 强烈推荐关注（信噪比高）\n\n`;
    highValue.forEach(u => report += `- **@${u.username}**：${u.summary}\n`);
    report += '\n';
  }
  
  if (mediumValue.length > 0) {
    report += `### 选择性关注（特定兴趣时值得看）\n\n`;
    mediumValue.forEach(u => report += `- **@${u.username}**：${u.summary}\n`);
    report += '\n';
  }
  
  if (lowValue.length > 0) {
    report += `### 可暂缓关注（近期活跃度低）\n\n`;
    lowValue.forEach(u => report += `- **@${u.username}**：${u.summary}\n`);
    report += '\n';
  }
  
  report += `\n*日报生成时间：${now.toISOString()}*`;
  report += `\n*本版本为完全免费版，无需X API密钥，无使用成本*`;
  
  // 保存到本地文件
  const reportPath = path.join(__dirname, `x-daily-report-free-${now.toISOString().split('T')[0]}.md`);
  await writeFile(reportPath, report, 'utf-8');
  console.log(`✅ 日报已保存到: ${reportPath}`);
  
  return { report, reportPath };
}

// 运行主程序
if (require.main === module) {
  generateDailyReport()
    .then(({ report }) => {
      console.log('\n' + '='.repeat(100) + '\n');
      console.log(report);
      console.log('\n' + '='.repeat(100) + '\n');
      process.exit(0);
    })
    .catch(error => {
      console.error('❌ 日报生成失败:', error);
      process.exit(1);
    });
}

module.exports = { generateDailyReport, getAccountTweets };
