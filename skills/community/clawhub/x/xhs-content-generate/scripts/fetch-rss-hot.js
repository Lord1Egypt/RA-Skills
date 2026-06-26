#!/usr/bin/env node
/**
 * Fetch hot topics from RSS feeds with simplified heat metrics
 * Sources: 36kr (with more sources possible via RSSHub)
 * Usage: node fetch-rss-hot.js [keyword]
 * 
 * Heat metrics (simplified):
 * - Rank position as heat indicator
 * - PubDate for 24h filtering
 * - No actual view/comment/share counts (RSS doesn't provide)
 */

const https = require('https');

const FEEDS = {
  '36kr': 'https://36kr.com/feed',
};

function fetchXML(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
      res.on('error', reject);
    }).on('error', reject);
  });
}

// Parse RSS items with pubDate
function parseRSSItems(xml) {
  const items = [];
  const itemMatches = xml.matchAll(/<item>([\s\S]*?)<\/item>/g);
  
  for (const match of itemMatches) {
    const itemXml = match[1];
    const titleMatch = itemXml.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>|<title>(.*?)<\/title>/);
    const linkMatch = itemXml.match(/<link><!\[CDATA\[(.*?)\]\]><\/link>|<link>(.*?)<\/link>/);
    const pubDateMatch = itemXml.match(/<pubDate>(.*?)<\/pubDate>/);
    
    if (titleMatch) {
      const title = (titleMatch[1] || titleMatch[2] || '').trim();
      const link = (linkMatch?.[1] || linkMatch?.[2] || '').trim();
      const pubDate = pubDateMatch?.[1]?.trim() || '';
      
      items.push({
        title,
        link,
        pubDate,
        pubDateObj: pubDate ? new Date(pubDate) : null
      });
    }
  }
  
  return items;
}

// Calculate hours since publication
function hoursSince(date) {
  if (!date) return Infinity;
  const now = new Date();
  return (now - date) / (1000 * 60 * 60);
}

// Format time ago
function timeAgo(date) {
  if (!date) return '时间未知';
  const hours = hoursSince(date);
  if (hours < 1) return '刚刚';
  if (hours < 24) return `${Math.floor(hours)}小时前`;
  if (hours < 48) return '昨天';
  return `${Math.floor(hours / 24)}天前`;
}

// Heat score based on rank and recency (simplified)
function calcHeatScore(rank, hoursAgo) {
  if (hoursAgo > 24) return 0;
  // Rank 1 = 100, Rank 50 = 20, decays with age
  const rankScore = Math.max(0, 110 - rank * 2);
  const timeDecay = Math.max(0.3, 1 - hoursAgo / 30); // 30h decay
  return Math.floor(rankScore * timeDecay);
}

// Heat level emoji
function heatEmoji(score) {
  if (score >= 80) return '🔥🔥🔥';
  if (score >= 60) return '🔥🔥';
  if (score >= 40) return '🔥';
  if (score >= 20) return '⚡';
  return '📌';
}

async function fetchHotTopics(keyword) {
  const results = [];
  
  for (const [name, url] of Object.entries(FEEDS)) {
    try {
      const xml = await fetchXML(url);
      const items = parseRSSItems(xml);
      
      // Add rank and calculate heat
      items.forEach((item, index) => {
        item.rank = index + 1;
        item.source = name;
        item.hoursAgo = hoursSince(item.pubDateObj);
        item.heatScore = calcHeatScore(item.rank, item.hoursAgo);
        item.timeAgo = timeAgo(item.pubDateObj);
      });
      
      if (keyword) {
        const filtered = items.filter(i => 
          i.title.toLowerCase().includes(keyword.toLowerCase())
        );
        results.push(...filtered);
      } else {
        // Filter 24h, sort by heat score
        const recent = items.filter(i => i.hoursAgo <= 24);
        results.push(...recent);
      }
    } catch (e) {
      console.error(`Failed to fetch ${name}: ${e.message}`);
    }
  }
  
  // Sort by heat score descending
  results.sort((a, b) => b.heatScore - a.heatScore);
  
  return results;
}

// Main
const keyword = process.argv[2];
fetchHotTopics(keyword).then(results => {
  if (results.length === 0) {
    console.log('未找到相关话题（24小时内）');
    console.log('💡 提示：换个关键词试试，或者不带关键词获取全部热点');
    return;
  }
  
  console.log('\n📰 热点话题列表（24小时内，按热度排序）\n');
  console.log('排名 | 热度 | 时间   | 标题');
  console.log('—'.repeat(60));
  
  results.slice(0, 15).forEach((r, i) => {
    const rank = String(i + 1).padStart(2);
    const heat = `${heatEmoji(r.heatScore)} ${r.heatScore}`.padEnd(12);
    const time = r.timeAgo.padEnd(6);
    const title = r.title.slice(0, 40) + (r.title.length > 40 ? '...' : '');
    console.log(`${rank}   | ${heat} | ${time} | ${title}`);
  });
  
  console.log('\n💡 选择一个话题编号，或输入新话题，或补充细节（角度/立场）');
  
}).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
