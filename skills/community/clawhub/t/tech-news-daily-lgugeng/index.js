#!/usr/bin/env node
/**
 * Tech News Daily - 每日科技资讯聚合脚本
 * 抓取 -> 去重 -> LLM总结 -> 生成日报 -> 推送
 */

const fs = require('fs');
const path = require('path');

// 配置
const configPath = path.join(__dirname, 'config.json');
const pushedPath = path.join(__dirname, 'data/pushed-articles.json');
const issuePath = path.join(__dirname, 'data/issue-count.json');

const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
const pushedData = JSON.parse(fs.readFileSync(pushedPath, 'utf-8'));
const issueData = JSON.parse(fs.readFileSync(issuePath, 'utf-8'));

// 关键词匹配
function matchesKeywords(text) {
  const lowerText = text.toLowerCase();
  return config.keywords.some(kw => lowerText.includes(kw.toLowerCase()));
}

function isExcluded(text) {
  const lowerText = text.toLowerCase();
  return config.exclude_keywords.some(kw => lowerText.includes(kw.toLowerCase()));
}

// 去重检查
function isPushed(url) {
  return pushedData.articles.some(a => a.url === url);
}

// 生成日报Markdown
function generateMarkdown(articles, date, issueNum) {
  const heavy = articles.filter(a => a.rating === '🔥🔥🔥');
  const tech = articles.filter(a => a.category === 'tech' && a.rating !== '🔥🔥🔥');
  const industry = articles.filter(a => a.category === 'industry' && a.rating !== '🔥🔥🔥');
  const ai = articles.filter(a => a.category === 'ai' && a.rating !== '🔥🔥🔥');
  const data = articles.filter(a => a.category === 'data' && a.rating !== '🔥🔥🔥');

  let md = `📅 **OpenClaw 科技早报** | ${date} | 第${issueNum}期\n\n`;
  
  if (heavy.length > 0) {
    md += `## 🚀 今日重磅\n`;
    heavy.forEach(a => {
      md += formatArticle(a);
    });
    md += '\n';
  }

  if (tech.length > 0) {
    md += `## 💡 技术前沿\n`;
    tech.forEach(a => md += formatArticle(a));
    md += '\n';
  }

  if (industry.length > 0) {
    md += `## 🏢 行业动态\n`;
    industry.forEach(a => md += formatArticle(a));
    md += '\n';
  }

  if (ai.length > 0) {
    md += `## 🤖 AI应用\n`;
    ai.forEach(a => md += formatArticle(a));
    md += '\n';
  }

  if (data.length > 0) {
    md += `## 📊 数据洞察\n`;
    data.forEach(a => md += formatArticle(a));
    md += '\n';
  }

  md += `---\n*本日报由OpenClaw自动聚合生成*\n`;
  md += `*信源：GitHub/机器之心/量子位/新智元/智东西/InfoQ/36氪/钛媒体/51CTO*\n`;

  return md;
}

function formatArticle(a) {
  let result = `\n### ${a.rating} ${a.title}\n`;
  a.highlights.forEach(h => {
    result += `- ${h}\n`;
  });
  result += `[原文链接](${a.url})\n`;
  return result;
}

// 导出给主进程使用
module.exports = {
  config,
  pushedData,
  issueData,
  matchesKeywords,
  isExcluded,
  isPushed,
  generateMarkdown
};

// CLI入口
if (require.main === module) {
  console.log('Tech News Daily - 请通过OpenClaw主进程调用');
  console.log('说 "生成日报" 或 "推送科技资讯" 触发执行');
}
