/**
 * filter.js — 新闻过滤与分类脚本
 * 按关键词匹配新闻条目，归类到不同分类
 */

const fs = require('fs');
const path = require('path');

// 加载配置
const configPath = path.join(__dirname, '..', 'config.json');
const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf-8')) : { keywords: {} };

const keywords = config.keywords || {};

/**
 * 计算关键词匹配得分
 */
function matchScore(news, category, categoryKeywords) {
  const text = `${news.title} ${news.summary}`.toLowerCase();
  let score = 0;
  for (const kw of categoryKeywords) {
    const lower = kw.toLowerCase();
    if (text.includes(lower)) {
      // 标题匹配权重更高
      if (news.title.toLowerCase().includes(lower)) score += 2;
      else score += 1;
    }
  }
  return score;
}

/**
 * 将新闻分配到最佳分类
 */
function assignCategory(news) {
  let bestCategory = '其他';
  let bestScore = 0;
  for (const [category, kws] of Object.entries(keywords)) {
    const score = matchScore(news, category, kws);
    if (score > bestScore) {
      bestScore = score;
      bestCategory = category;
    }
  }
  return bestCategory;
}

/**
 * 过滤并分类新闻
 */
function filterAndCategorize(newsList) {
  const categorized = {};
  for (const [cat] of Object.entries(keywords)) {
    categorized[cat] = [];
  }
  categorized['其他'] = [];

  for (const news of newsList) {
    const category = assignCategory(news);
    if (categorized[category]) {
      categorized[category].push({ ...news, category });
    }
  }

  // 限制每个分类的数量
  const maxPerCategory = config.maxNewsPerCategory || 10;
  for (const cat of Object.keys(categorized)) {
    categorized[cat] = categorized[cat].slice(0, maxPerCategory);
  }

  return categorized;
}

async function main() {
  const inputPath = path.join(__dirname, '..', 'data', 'raw_news.json');
  if (!fs.existsSync(inputPath)) {
    console.error('[filter] 错误: data/raw_news.json 不存在，请先运行 fetch.js');
    return;
  }

  const rawNews = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  console.log(`[filter] 开始过滤 ${rawNews.length} 条新闻...`);

  const categorized = filterAndCategorize(rawNews);

  let total = 0;
  for (const [cat, news] of Object.entries(categorized)) {
    console.log(`[filter] ${cat}: ${news.length} 条`);
    total += news.length;
  }

  const outputPath = path.join(__dirname, '..', 'data', 'filtered_news.json');
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(categorized, null, 2));
  console.log(`[filter] 完成，共归类 ${total} 条`);

  return categorized;
}

module.exports = { main, filterAndCategorize, assignCategory };

if (require.main === module) {
  main().catch(console.error);
}
