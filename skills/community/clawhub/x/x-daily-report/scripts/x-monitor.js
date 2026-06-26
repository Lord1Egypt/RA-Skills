const axios = require('axios');
const { writeFile } = require('fs').promises;
const path = require('path');

// 多维表格配置
const BITABLE_APP_TOKEN = 'LWnFbJuu3a4yJisz009cd4zznkf';
const BITABLE_TABLE_ID = 'tbl9bzVZgaglppwF';
const FEISHU_API_BASE = 'https://open.feishu.cn/open-apis';

// X API 配置
const X_API_KEY = 'THp2c1V4bW5JQVJ1S09IY1BzN1NubDoxaXJpUQ'; // 已自动获取
const X_API_SECRET = '••••••••••1ibiPw'; // 已自动获取，完整密钥请手动补充

// 记录最后检查时间
let lastCheckTime = new Date(Date.now() - 24 * 60 * 60 * 1000); // 初始为24小时前

// 获取多维表格账号列表
async function getBitableAccounts() {
  try {
    const response = await axios.get(
      `${FEISHU_API_BASE}/bitable/v1/apps/${BITABLE_APP_TOKEN}/tables/${BITABLE_TABLE_ID}/records`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.FEISHU_ACCESS_TOKEN}`
        }
      }
    );
    return response.data.data.records.map(record => ({
      id: record.record_id,
      name: record.fields['账号名称'][0].text,
      type: record.fields['类型'][0].text,
      xUrl: record.fields['x平台链接'].link,
      description: record.fields['简介'][0].text
    }));
  } catch (error) {
    console.error('获取多维表格账号列表失败:', error.message);
    return [];
  }
}

// 获取账号过去24小时的推文
async function getAccountTweets(accountName, sinceTime) {
  try {
    // 模拟 X API 调用，实际使用时替换为真实 API 请求
    console.log(`获取 @${accountName} 自 ${sinceTime.toISOString()} 以来的推文`);
    
    // 模拟返回数据（实际应替换为真实 API 响应）
    const mockTweets = [
      {
        id: 'mock_' + Math.random().toString(36).substr(2, 9),
        text: `这是 @${accountName} 的测试推文，发布于 ${new Date().toISOString()}`,
        created_at: new Date().toISOString(),
        public_metrics: {
          retweet_count: Math.floor(Math.random() * 1000),
          reply_count: Math.floor(Math.random() * 500),
          like_count: Math.floor(Math.random() * 5000),
          view_count: Math.floor(Math.random() * 100000)
        },
        url: `https://x.com/${accountName}/status/${Math.random().toString(36).substr(2, 18)}`
      }
    ];
    
    // 模拟 30% 的概率没有新推文
    if (Math.random() < 0.3) {
      return [];
    }
    
    return mockTweets;
  } catch (error) {
    console.error(`获取 @${accountName} 推文失败:`, error.message);
    return [];
  }
}

// 计算活跃度评分
function calculateActivityScore(tweets) {
  if (tweets.length === 0) return { score: 0, level: '—', totalEngagement: 0 };
  
  const totalEngagement = tweets.reduce((sum, tweet) => {
    return sum + tweet.public_metrics.like_count + tweet.public_metrics.retweet_count * 2 + tweet.public_metrics.reply_count * 3;
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
  } else {
    score = 1;
    level = '⭐';
  }
  
  return { score, level, totalEngagement };
}

// 生成日报内容
async function generateDailyReport() {
  const accounts = await getBitableAccounts();
  if (accounts.length === 0) {
    return '⚠️ 未获取到账号列表，日报生成失败';
  }
  
  const now = new Date();
  const sinceTime = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  
  console.log(`开始生成 ${sinceTime.toLocaleDateString()} - ${now.toLocaleDateString()} 的账号动态日报`);
  
  const accountUpdates = [];
  const topUpdates = [];
  
  for (const account of accounts) {
    const tweets = await getAccountTweets(account.name, sinceTime);
    if (tweets.length === 0) {
      accountUpdates.push({
        ...account,
        tweets: [],
        activity: { score: 0, level: '—', totalEngagement: 0 },
        summary: '无动态'
      });
      continue;
    }
    
    const activity = calculateActivityScore(tweets);
    const summary = tweets.length > 0 ? tweets[0].text.substring(0, 50) + (tweets[0].text.length > 50 ? '...' : '') : '无内容';
    
    const accountData = {
      ...account,
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
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // 按活跃度排序
  accountUpdates.sort((a, b) => b.activity.score - a.activity.score);
  topUpdates.sort((a, b) => b.activity.score - a.activity.score);
  
  // 生成 Markdown 内容
  let report = `# AI Twitter/X 账号动态日报 · ${now.toLocaleDateString('zh-CN')}\n\n`;
  report += `**数据说明**：搜索时间范围为过去 24 小时（${sinceTime.toLocaleDateString('zh-CN')} - ${now.toLocaleDateString('zh-CN')}）\n\n`;
  
  // 重点内容
  if (topUpdates.length > 0) {
    report += `## 🔥 今日最值得关注的内容\n\n`;
    topUpdates.forEach((update, index) => {
      const topTweet = update.tweets[0];
      report += `### ${index + 1}. ${update.name} — ${update.summary}\n\n`;
      report += `**账号**：[@${update.name}](${update.xUrl}) · **热度**：${topTweet.public_metrics.view_count.toLocaleString()} 浏览 · ${topTweet.public_metrics.like_count.toLocaleString()} 点赞 · ${topTweet.public_metrics.retweet_count.toLocaleString()} 转发\n\n`;
      report += `**核心内容**：${topTweet.text}\n\n`;
      report += `**💡 为什么值得关注**：该账号今日活跃度达到 ${update.activity.level}，总互动量 ${update.activity.totalEngagement.toLocaleString()}，是近期行业重点动态。\n\n`;
    });
  }
  
  // 完整活跃度总览
  report += `## 📋 完整账号活跃度总览\n\n`;
  report += `| 账号 | 类别 | 今日活跃度 | 主要内容 |\n`;
  report += `|------|------|------------|----------|\n`;
  
  accountUpdates.forEach(update => {
    const type = update.type.includes('机构') ? '国际机构' : update.type.includes('个人') ? '国际个人' : '其他';
    report += `| @${update.name} | ${type} | ${update.activity.level} | ${update.summary} |\n`;
  });
  
  // 关注建议
  report += `\n## 💡 关注建议\n\n`;
  
  const highValue = accountUpdates.filter(u => u.activity.score >= 4);
  const mediumValue = accountUpdates.filter(u => u.activity.score === 2 || u.activity.score === 3);
  const lowValue = accountUpdates.filter(u => u.activity.score <= 1);
  
  if (highValue.length > 0) {
    report += `### 强烈推荐关注（信噪比高）\n\n`;
    highValue.forEach(u => report += `- **@${u.name}**：${u.description}\n`);
    report += '\n';
  }
  
  if (mediumValue.length > 0) {
    report += `### 选择性关注（特定兴趣时值得看）\n\n`;
    mediumValue.forEach(u => report += `- **@${u.name}**：${u.description}\n`);
    report += '\n';
  }
  
  if (lowValue.length > 0) {
    report += `### 可暂缓关注（近期活跃度低）\n\n`;
    lowValue.forEach(u => report += `- **@${u.name}**：${u.description}\n`);
    report += '\n';
  }
  
  report += `\n*日报生成时间：${now.toISOString()}*`;
  
  // 保存到本地文件
  const reportPath = path.join(__dirname, `x-daily-report-${now.toISOString().split('T')[0]}.md`);
  await writeFile(reportPath, report, 'utf-8');
  console.log(`日报已保存到: ${reportPath}`);
  
  // 更新最后检查时间
  lastCheckTime = now;
  
  return report;
}

// 运行主程序
if (require.main === module) {
  generateDailyReport()
    .then(report => {
      console.log('日报生成完成');
      // 这里可以添加推送逻辑，比如发送到飞书/邮件/微信等
      process.exit(0);
    })
    .catch(error => {
      console.error('日报生成失败:', error);
      process.exit(1);
    });
}

module.exports = { generateDailyReport, getBitableAccounts };
