#!/usr/bin/env node

/**
 * Tech Radar Daily - 数据收集器
 * 
 * 负责从 5 个情报源抓取数据
 */

const fetch = require('node-fetch');
const ProxyAgent = require('proxy-agent');
const { parseGitHubTrending, parseProductHunt, parseHackerNews, parseAwesomeList } = require('./html-parser');

// ============ 全局代理配置 ============
// 自动识别 http/https 协议，无需手动配置
// 读取 https_proxy 或 HTTPS_PROXY 环境变量
const globalAgent = new ProxyAgent(process.env.https_proxy || process.env.HTTPS_PROXY || process.env.http_proxy || process.env.HTTP_PROXY);

// 如果需要使用代理，请在运行前设置：
// export https_proxy=http://127.0.0.1:7897
// ====================================

/**
 * 情报源 1: GitHub Trending
 */
async function collectGitHubTrending() {
  console.log('  📡 抓取 GitHub Trending...');
  
  try {
    const response = await fetch('https://github.com/trending?since=daily', { agent: globalAgent });
    const html = await response.text();
    
    const projects = parseGitHubTrending(html);
    
    return projects;
    
  } catch (error) {
    console.error('  ⚠️ GitHub Trending 抓取失败:', error.message);
    return [];
  }
}

/**
 * 情报源 2: GitHub Topics（简化版，暂用模拟数据）
 */
async function collectGitHubTopics() {
  console.log('  📡 抓取 GitHub Topics...');
  
  // 暂用模拟数据，后续可扩展
  return [
    {
      name: 'ai-tools/awesome-ai',
      repoName: 'ai-tools/awesome-ai',
      url: 'https://github.com/ai-tools/awesome-ai',
      description: 'AI tools collection',
      stars: 1200,
      starsToday: 50,
      language: 'JavaScript',
      sourceType: 'github',
      source: 'github_topic',
      category: 'trending'
    }
  ];
}

/**
 * 情报源 3: Product Hunt
 */
async function collectProductHunt() {
  console.log('  📡 抓取 Product Hunt...');
  
  try {
    const response = await fetch('https://www.producthunt.com', { agent: globalAgent });
    await response.text(); // 需要时解析 HTML
    
    // 简化：返回模拟数据（实际需解析 HTML）
    return [{
      name: 'AI Writer Pro',
      url: 'https://www.producthunt.com/posts/ai-writer-pro',
      source: 'product_hunt',
      sourceType: 'product',
      category: 'money',
      rank: 1,
      targetUser: 'Content creators',
      pricing: '$29/month',
      replicability: '高',
      description: 'AI-powered content writing assistant'
    }];
    
  } catch (error) {
    console.error('  ⚠️ Product Hunt 抓取失败:', error.message);
    return [];
  }
}

/**
 * 情报源 4: Hacker News
 */
async function collectHackerNews() {
  console.log('  📡 抓取 Hacker News...');
  
  try {
    const response = await fetch('https://hacker-news.firebaseio.com/v0/topstories.json', { agent: globalAgent });
    const storyIds = (await response.json()).slice(0, 10);
    const stories = [];
    
    for (const id of storyIds.slice(0, 5)) {
      try {
        const storyResponse = await fetch(`https://hacker-news.firebaseio.com/v0/item/${id}.json`, { agent: globalAgent });
        const story = await storyResponse.json();
        
        if (story && story.url && isRelevant(story.title)) {
          stories.push({
            title: story.title,
            url: story.url,
            hnUrl: `https://news.ycombinator.com/item?id=${id}`,
            score: story.score || 0,
            sourceType: 'trend',
            source: 'hacker_news',
            category: 'trends'
          });
        }
      } catch (e) {
        // 忽略单个故事失败
      }
    }
    
    return stories;
    
  } catch (error) {
    console.error('  ⚠️ Hacker News 抓取失败:', error.message);
    return [];
  }
}

/**
 * 相关性检查
 */
function isRelevant(title) {
  if (!title) return false;
  const keywords = ['AI', 'ML', 'Open Source', 'JavaScript', 'Python', 'Tool', 'Framework'];
  return keywords.some(k => title.toLowerCase().includes(k.toLowerCase()));
}

/**
 * 情报源 5: Awesome Lists
 */
async function collectAwesomeLists() {
  const { collectAwesomeLists } = require('./collectors-awesome');
  return await collectAwesomeLists();
}

// ============ 导出 ============

module.exports = {
  collectGitHubTrending,
  collectGitHubTopics,
  collectProductHunt,
  collectHackerNews,
  collectAwesomeLists
};
