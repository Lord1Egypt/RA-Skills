#!/usr/bin/env node
/**
 * WSB Digest - ApeWisdom API with retry logic
 * 
 * 自动抓取 r/wallstreetbets 热股数据
 * 输出: JSON 格式的完整报告（包含 markdown 字段）
 */

const https = require('https');

function fetchWithRetry(url, options = {}, maxRetries = 3) {
  return new Promise((resolve, reject) => {
    let attempts = 0;
    
    const tryFetch = () => {
      attempts++;
      console.log(`🔄 Attempt ${attempts}/${maxRetries}...`);
      
      fetchApeWisdom()
        .then(resolve)
        .catch(err => {
          if (attempts < maxRetries) {
            console.log(`⚠️ Failed: ${err.message}, retrying in ${attempts * 2}s...`);
            setTimeout(tryFetch, attempts * 2000);
          } else {
            reject(new Error(`Failed after ${maxRetries} attempts: ${err.message}`));
          }
        });
    };
    
    tryFetch();
  });
}

function fetchApeWisdom(filter = 'wallstreetbets', page = 1) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'apewisdom.io',
      path: `/api/v1.0/filter/${filter}/page/${page}`,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          reject(new Error('Invalid JSON response'));
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    req.end();
  });
}

function calculateTrend(stock) {
  if (!stock.rank_24h_ago || stock.rank_24h_ago === 0) return '🆕 新上榜';
  const change = stock.rank_24h_ago - stock.rank;
  if (change > 0) return `↗️ 上升 ${change} 位`;
  if (change < 0) return `↘️ 下降 ${Math.abs(change)} 位`;
  return '➡️ 持平';
}

function calculateMentionChange(stock) {
  if (!stock.mentions_24h_ago) return null;
  const change = ((stock.mentions - stock.mentions_24h_ago) / stock.mentions_24h_ago * 100).toFixed(1);
  return change > 0 ? `+${change}%` : `${change}%`;
}

function getSentimentEmoji(upvotes) {
  if (upvotes >= 1000) return '🟢🟢🟢🔥';
  if (upvotes >= 100) return '🟢🟢🟢';
  if (upvotes >= 50) return '🟢🟢';
  if (upvotes >= 20) return '🟢';
  if (upvotes >= 0) return '⚪';
  return '🔴';
}

async function generateDigest() {
  try {
    console.log('🔍 Fetching WSB data from ApeWisdom API...');
    const data = await fetchWithRetry('wallstreetbets', {}, 3);
    
    if (!data.results || data.results.length === 0) {
      throw new Error('No data received from API');
    }
    
    console.log(`✅ Fetched ${data.results.length} stocks (Total: ${data.count})`);
    
    const stocks = data.results.slice(0, 15);
    const now = new Date().toLocaleString('zh-CN', { 
      timeZone: 'Asia/Shanghai',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
    
    let output = `📊 **WSB 每日热股报告**\n\n`;
    output += `⏰ ${now} (北京时间)\n`;
    output += `📈 数据来源: ApeWisdom (r/wallstreetbets)\n`;
    output += `📊 总提及股票: ${data.count} 只\n\n`;
    
    output += `## 🔥 TOP 15 热门股票\n\n`;
    
    stocks.forEach((stock, i) => {
      const trend = calculateTrend(stock);
      const mentionChange = calculateMentionChange(stock);
      const sentiment = getSentimentEmoji(stock.upvotes);
      
      output += `${i + 1}. **$${stock.ticker}** ${sentiment}\n`;
      output += `   📊 ${stock.mentions} 次提及${mentionChange ? ` (${mentionChange})` : ''}\n`;
      output += `   👍 ${stock.upvotes} upvotes\n`;
      output += `   📈 ${trend}\n`;
      output += `   🏢 ${stock.name.substring(0, 45)}${stock.name.length > 45 ? '...' : ''}\n\n`;
    });
    
    // Find trending stocks (biggest rank improvements)
    const trending = data.results
      .filter(s => s.rank_24h_ago && s.rank_24h_ago - s.rank > 10)
      .slice(0, 5);
    
    if (trending.length > 0) {
      output += `## 🚀 快速上升股票\n\n`;
      trending.forEach(stock => {
        const jump = stock.rank_24h_ago - stock.rank;
        output += `↗️ **$${stock.ticker}**: 上升 ${jump} 位 (从 #${stock.rank_24h_ago} → #${stock.rank})\n`;
      });
      output += '\n';
    }
    
    // New entries
    const newEntries = data.results
      .filter(s => !s.rank_24h_ago || s.rank_24h_ago === 0)
      .slice(0, 5);
    
    if (newEntries.length > 0) {
      output += `## 🆕 新上榜股票\n\n`;
      newEntries.forEach(stock => {
        output += `🆕 **$${stock.ticker}**: ${stock.mentions} 次提及\n`;
      });
      output += '\n';
    }
    
    output += `---\n`;
    output += `📝 数据来自 ApeWisdom API | ⏰ 每日 9:00 & 21:00 更新\n`;
    output += `⚠️ 仅供参考，不构成投资建议`;
    
    const result = {
      generated_at: new Date().toISOString(),
      source: 'apewisdom.io',
      total_stocks: data.count,
      stocks: stocks,
      trending: trending,
      new_entries: newEntries,
      digest_markdown: output
    };
    
    console.log('\n📤 OUTPUT:');
    console.log(JSON.stringify(result, null, 2));
    
    return result;
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  generateDigest();
}

module.exports = { fetchApeWisdom, generateDigest };
