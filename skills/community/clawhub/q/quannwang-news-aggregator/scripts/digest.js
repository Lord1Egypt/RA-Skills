/**
 * digest.js — 每日简报生成脚本
 * 将分类后的新闻渲染为 Markdown 格式的每日简报
 */

const fs = require('fs');
const path = require('path');

// 加载配置
const configPath = path.join(__dirname, '..', 'config.json');
const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf-8')) : {};

const CATEGORY_EMOJI = {
  '科技': '🖥️',
  '财经': '💰',
  '行业': '📊',
  '其他': '📰'
};

/**
 * 格式化日期为中文格式
 */
function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}年${month}月${day}日`;
}

/**
 * 格式化时间为相对时间
 */
function timeAgo(dateStr) {
  try {
    const diff = Date.now() - new Date(dateStr).getTime();
    const hours = Math.floor(diff / 3600000);
    if (hours < 1) return '刚刚';
    if (hours < 24) return `${hours}小时前`;
    const days = Math.floor(hours / 24);
    return `${days}天前`;
  } catch {
    return '';
  }
}

/**
 * 生成单条新闻的 Markdown 列表项
 */
function formatNewsItem(news, index) {
  const emoji = CATEGORY_EMOJI[news.category] || '📰';
  const ago = timeAgo(news.publishedAt);
  const timeStr = ago ? ` (${ago})` : '';
  const summary = news.summary ? `\n    > ${news.summary.slice(0, 100)}${news.summary.length > 100 ? '...' : ''}` : '';
  return `${index}. [${news.title}](${news.url})${timeStr}${summary}`;
}

/**
 * 生成完整简报
 */
function generateDigest(categorized, date) {
  const dateStr = formatDate(date || new Date());
  const lines = [];

  lines.push(`# 📰 每日新闻简报`);
  lines.push(`**${dateStr}** · ${new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })} UTC`);
  lines.push('');
  lines.push('---');
  lines.push('');

  let totalNews = 0;
  const categories = Object.keys(categorized).filter(cat => categorized[cat] && categorized[cat].length > 0);

  if (categories.length === 0) {
    lines.push('今日暂无符合关键词的新闻 🎉');
    lines.push('');
    return lines.join('\n');
  }

  for (const category of categories) {
    const newsList = categorized[category];
    if (!newsList || newsList.length === 0) continue;

    const emoji = CATEGORY_EMOJI[category] || '📰';
    lines.push(`## ${emoji} ${category}`);
    lines.push('');

    newsList.forEach((news, i) => {
      lines.push(formatNewsItem(news, i + 1));
      lines.push('');
    });

    totalNews += newsList.length;
  }

  lines.push('---');
  lines.push('');
  lines.push(`📌 共收录 **${totalNews}** 条新闻 | 由 **News Aggregator** 自动生成`);
  lines.push('');
  lines.push('> 💡 点击标题链接阅读原文。简报内容由算法自动筛选，内容的真实性与立场与本工具无关。');

  return lines.join('\n');
}

async function main() {
  const inputPath = path.join(__dirname, '..', 'data', 'filtered_news.json');
  if (!fs.existsSync(inputPath)) {
    console.error('[digest] 错误: data/filtered_news.json 不存在，请先运行 filter.js');
    return;
  }

  const categorized = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  console.log('[digest] 生成简报...');

  const digest = generateDigest(categorized, new Date());

  const outputPath = path.join(__dirname, '..', 'data', 'daily_digest.md');
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, digest);

  console.log(`[digest] 简报已生成: ${outputPath}`);
  return digest;
}

module.exports = { main, generateDigest };

if (require.main === module) {
  main().catch(console.error);
}
