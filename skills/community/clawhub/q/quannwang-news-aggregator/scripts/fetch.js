/**
 * fetch.js — 新闻抓取脚本
 * 从配置的信源（RSS / 通用 URL）抓取最新新闻
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');
const Parser = require('rss-parser');

// 内置轻量 RSS 解析器（无第三方依赖时使用）
class SimpleRssParser {
  parse(xml) {
    const items = [];
    const itemMatches = xml.matchAll(/<item[^>]*>([\s\S]*?)<\/item>/gi);
    for (const match of itemMatches) {
      const itemXml = match[1];
      const getContent = (tag) => {
        const m = itemXml.match(new RegExp(`<${tag}[^>]*><!\[CDATA\[([\s\S]*?)\]\]><\/${tag}>`));
        if (m) return m[1].trim();
        const m2 = itemXml.match(new RegExp(`<${tag}[^>]*>([\s\S]*?)<\/${tag}>`));
        return m2 ? m2[1].replace(/<[^>]+>/g, '').trim() : '';
      };
      const title = getContent('title');
      const link = getContent('link');
      const pubDate = getContent('pubDate') || getContent('dc:date');
      const description = getContent('description');
      if (title && link) {
        items.push({ title, url: link, publishedAt: pubDate ? new Date(pubDate).toISOString() : new Date().toISOString(), summary: description });
      }
    }
    return items;
  }
}

const parser = new Parser({ customFields: { item: ['media:content', 'content:encoded'] } });
const simpleParser = new SimpleRssParser();

// 加载配置
const configPath = path.join(__dirname, '..', 'config.json');
const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf-8')) : { sources: [], maxNewsPerCategory: 10 };
const sources = config.sources || [];

async function fetchRss(source) {
  try {
    const response = await axios.get(source.url, { timeout: 15000, headers: { 'User-Agent': 'Mozilla/5.0 (compatible; NewsAggregator/1.0)' } });
    const contentType = response.headers['content-type'] || '';
    let items = [];
    if (contentType.includes('xml') || source.url.includes('rss') || source.url.includes('feed')) {
      try { items = (await parser.parseString(response.data)).items; } catch { items = simpleParser.parse(response.data); }
    } else {
      // 通用网页：尝试提取 <a> 链接
      const $ = cheerio.load(response.data);
      $('a[href]').each((_, el) => {
        const href = $(el).attr('href');
        const text = $(el).text().trim();
        if (href && text && text.length > 10 && href.startsWith('http')) {
          items.push({ title: text, url: href, publishedAt: new Date().toISOString(), summary: '' });
        }
      });
    }
    return (items || []).slice(0, 20).map(item => ({
      title: (item.title || '').replace(/<[^>]+>/g, '').trim(),
      url: item.link || item.url || '',
      source: source.name,
      publishedAt: item.pubDate || item.isoDate || new Date().toISOString(),
      summary: (item.contentSnippet || item.content || item.summary || '').replace(/<[^>]+>/g, '').slice(0, 200)
    })).filter(item => item.title && item.url);
  } catch (err) {
    console.error(`[fetch] ${source.name} 抓取失败:`, err.message);
    return [];
  }
}

async function main() {
  console.log(`[fetch] 开始抓取 ${sources.length} 个信源...`);
  const allNews = [];
  for (const source of sources) {
    const news = await fetchRss(source);
    allNews.push(...news);
    console.log(`[fetch] ${source.name}: ${news.length} 条`);
  }
  // 按时间排序，去标题重复
  allNews.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
  const seen = new Set();
  const unique = allNews.filter(n => {
    const key = n.title.slice(0, 50);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  const outputPath = path.join(__dirname, '..', 'data', 'raw_news.json');
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(unique, null, 2));
  console.log(`[fetch] 完成，共 ${unique.length} 条（已去重）`);
  return unique;
}

module.exports = { main, fetchRss };

if (require.main === module) {
  main().catch(console.error);
}
