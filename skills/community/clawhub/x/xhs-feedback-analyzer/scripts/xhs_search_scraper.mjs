#!/usr/bin/env node
/**
 * xhs_search_scraper.mjs
 * 多关键词搜索小红书，过滤指定日期范围，去重后输出 JSON
 * 
 * 用法:
 *   node xhs_search_scraper.mjs --keywords "美团跑腿,跑腿" --days 3 --limit 50 --out ./output
 * 
 * 参数:
 *   --keywords   逗号分隔关键词（默认：美团跑腿,跑腿,跑腿帮忙,美团帮忙,美团帮送,跑腿帮送,帮买）
 *   --days       往前几天（默认3，即昨天+前天+大前天）
 *   --date       指定日期 YYYY-MM-DD（优先于 --days）
 *   --limit      总帖子数上限（默认50）
 *   --out        输出目录（默认./output）
 *   --cdp        CDP URL（默认 http://127.0.0.1:9222）
 */

import pkg from '/root/.nvm/versions/node/v24.14.0/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import fs from 'fs';
import path from 'path';

// ---- 参数解析 ----
const args = process.argv.slice(2);
const getArg = (name, def) => {
  const i = args.indexOf(name);
  return i !== -1 ? args[i + 1] : def;
};

const KEYWORDS = getArg('--keywords', '美团跑腿,跑腿,跑腿帮忙,美团帮忙,美团帮送,跑腿帮送,帮买,美团帮买').split(',').map(k => k.trim());
const DAYS = parseInt(getArg('--days', '3'));
const LIMIT = parseInt(getArg('--limit', '50'));
const OUT_DIR = getArg('--out', './output');
const CDP_URL = getArg('--cdp', 'http://127.0.0.1:9222');

// 相关性关键词（必须包含其中之一才算相关，已放宽：加入更多使用场景词）
const RELEVANCE_KEYWORDS = ['跑腿', '帮送', '帮买', '帮忙', '美团', '代买', '代送', '取件', '送件', '配送',
  '同城', '上门', '急送', '帮我买', '帮我送', '帮拿', '帮取', '代跑', '众包', '骑手', '快递员', '小哥'];

fs.mkdirSync(OUT_DIR, { recursive: true });

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// 生成目标日期列表（今天往前 DAYS 天，不含今天）
function getTargetDates(days) {
  const dates = [];
  for (let i = 1; i <= days; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    dates.push(d.toISOString().slice(0, 10)); // YYYY-MM-DD
  }
  return dates;
}

// 解析小红书显示的时间文字 → YYYY-MM-DD
// 支持格式：昨天 16:04 / 前天 10:00 / 30分钟前 / 1小时前 / 3天前 / 03-14 / 2026-03-14
function parseXhsDate(raw) {
  if (!raw) return null;
  const today = new Date();
  // 去掉多余空格，取最后一段（卡片里可能包含用户名+时间）
  const lines = raw.trim().split('\n');
  const text = lines[lines.length - 1].trim();
  
  // 今天（X分钟前 / X小时前 / 刚刚）
  if (text.match(/分钟前|小时前|刚刚/)) {
    return today.toISOString().slice(0, 10);
  }
  // 昨天
  if (text.includes('昨天')) {
    const d = new Date(today); d.setDate(d.getDate() - 1);
    return d.toISOString().slice(0, 10);
  }
  // 前天
  if (text.includes('前天')) {
    const d = new Date(today); d.setDate(d.getDate() - 2);
    return d.toISOString().slice(0, 10);
  }
  // X天前
  const daysAgo = text.match(/^(\d+)\s*天前/);
  if (daysAgo) {
    const d = new Date(today); d.setDate(d.getDate() - parseInt(daysAgo[1]));
    return d.toISOString().slice(0, 10);
  }
  // MM-DD 或 MM月DD日
  const md = text.match(/^(\d{1,2})[-月](\d{1,2})/);
  if (md) {
    const year = today.getFullYear();
    return `${year}-${md[1].padStart(2,'0')}-${md[2].padStart(2,'0')}`;
  }
  // YYYY-MM-DD 或 YYYY/MM/DD
  const full = text.match(/(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})/);
  if (full) {
    return `${full[1]}-${full[2].padStart(2,'0')}-${full[3].padStart(2,'0')}`;
  }
  return null;
}

// 检查帖子相关性
function isRelevant(title, body) {
  const text = (title + ' ' + body).toLowerCase();
  return RELEVANCE_KEYWORDS.some(k => text.includes(k));
}

// 抓取「大家都在搜」模块
async function captureTrending(page, keyword) {
  try {
    await page.goto(
      `https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(keyword)}&source=web_search_result_notes&type=51&sort=time_descending`,
      { waitUntil: 'domcontentloaded', timeout: 20000 }
    );
    await sleep(2500);
    const trending = await page.evaluate(() => {
      // 找「大家都在搜」模块
      const blocks = Array.from(document.querySelectorAll('*'));
      const header = blocks.find(el => el.children.length === 0 && el.innerText && el.innerText.trim() === '大家都在搜');
      if (!header) return [];
      const container = header.closest('[class*="hot"], [class*="trending"], [class*="search"], section, div') || header.parentElement?.parentElement;
      if (!container) return [];
      const items = container.querySelectorAll('[class*="item"], li, a, div');
      const results = [];
      items.forEach(el => {
        const text = el.innerText?.trim();
        if (text && text.length > 3 && text.length < 30 && text !== '大家都在搜' && !results.includes(text)) {
          results.push(text);
        }
      });
      return results.slice(0, 10);
    });
    return trending;
  } catch(e) {
    return [];
  }
}

// 从搜索结果页收集笔记链接和基础信息
async function collectFromSearch(page, keyword, targetDates) {
  const searchUrl = `https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(keyword)}&source=web_search_result_notes&type=51&sort=time_descending`;
  console.log(`  🔍 搜索: "${keyword}"`);
  
  try {
    await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await sleep(2500);
  } catch(e) {
    console.log(`  ⚠️  搜索页加载失败: ${e.message}`);
    return [];
  }

  // 检查登录状态
  if (page.url().includes('login') || page.url().includes('signin')) {
    throw new Error('需要登录小红书');
  }

  const notes = [];
  let tooOld = false;
  let scrollCount = 0;

  while (notes.length < 30 && !tooOld && scrollCount < 8) {
    const items = await page.evaluate(() => {
      const cards = document.querySelectorAll('.note-item');
      const results = [];
      cards.forEach(card => {
        const linkEl = card.querySelector('a[href*="/explore/"]');
        if (!linkEl) return;
        const url = linkEl.href;
        const title = card.querySelector('.title, .note-title, h3, [class*="title"]')?.innerText?.trim() || '';
        // 时间在 div.time 里，可能包含"用户名\n昨天 16:04"格式
        const timeEl = card.querySelector('div.time, .time, [class*="time"]');
        const timeText = timeEl?.innerText?.trim() || '';
        results.push({ url, title, timeText });
      });
      return results;
    });

    for (const item of items) {
      if (notes.some(n => n.url === item.url)) continue; // 去重
      const date = parseXhsDate(item.timeText);
      if (date && targetDates.includes(date)) {
        notes.push({ ...item, date });
      }
      // 如果日期超过目标范围最早日期则停止
      if (date && date < targetDates[targetDates.length - 1]) {
        tooOld = true;
      }
    }

    await page.evaluate(() => window.scrollBy(0, 1500));
    await sleep(1800);
    scrollCount++;
  }

  console.log(`    找到 ${notes.length} 篇目标日期内的帖子`);
  return notes;
}

// 抓取单篇笔记详情
async function scrapeNote(page, note) {
  try {
    await page.goto(note.url, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await sleep(2000);

    const detail = await page.evaluate(() => {
      const title = document.querySelector('#detail-title, .title, h1[class*="title"]')?.innerText?.trim() || '';
      const body = document.querySelector('#detail-desc, .desc, [class*="content"] .note-text, .note-content')?.innerText?.trim() || '';
      const likes = document.querySelector('[class*="like-wrapper"] .count, [class*="like"] span.count')?.innerText?.trim() || '';
      const comments = document.querySelector('[class*="chat-wrapper"] .count, [class*="comment"] span.count')?.innerText?.trim() || '';
      // 抓取发布时间（详情页更准确）
      const timeEl = document.querySelector('.date, [class*="date"], .publish-date, span[class*="time"]');
      const timeText = timeEl?.innerText?.trim() || '';
      return { title, body, likes, comments, timeText };
    });

    // 详情页时间优先
    const date = parseXhsDate(detail.timeText) || note.date;
    return { ...note, ...detail, date };
  } catch (e) {
    return { ...note, body: '', likes: '', comments: '', error: e.message };
  }
}

async function main() {
  let targetDates = getTargetDates(DAYS);
  console.log(`\n📅 目标日期: ${targetDates.join(', ')}`);
  console.log(`🔑 关键词: ${KEYWORDS.join(', ')}`);
  console.log(`📊 目标总数: ${LIMIT} 篇\n`);

  let browser;
  try {
    // 获取 WebSocket debugger URL
    const http = await import('http');
    const wsUrl = await new Promise((resolve, reject) => {
      http.get(`${CDP_URL}/json/version`, res => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try { resolve(JSON.parse(data).webSocketDebuggerUrl); }
          catch(e) { reject(e); }
        });
      }).on('error', reject);
    });
    browser = await chromium.connectOverCDP(wsUrl);
    console.log('✅ 已连接到本地 Chrome\n');
  } catch (e) {
    console.error(`❌ 无法连接到 Chrome CDP (${CDP_URL}): ${e.message}`);
    process.exit(1);
  }

  const context = browser.contexts()[0] || await browser.newContext();
  const page = await context.newPage();

  // 抓取「大家都在搜」（用第一个关键词）
  console.log('🔥 抓取「大家都在搜」...');
  const trending = await captureTrending(page, KEYWORDS[0]);
  console.log(`   结果: ${trending.join(', ') || '未找到'}\n`);

  // 多关键词收集候选帖子，不足时自动扩展时间范围
  const candidates = new Map();
  let currentDays = DAYS;
  
  while (candidates.size < LIMIT && currentDays <= 30) {
    if (currentDays > DAYS) {
      targetDates = getTargetDates(currentDays);
      console.log(`⚠️  帖子不足 ${LIMIT} 篇，扩展到 ${currentDays} 天: ${targetDates.join(', ')}\n`);
    }
    
    for (const keyword of KEYWORDS) {
      if (candidates.size >= LIMIT * 2) break;
      try {
        const notes = await collectFromSearch(page, keyword, targetDates);
        for (const n of notes) {
          if (!candidates.has(n.url)) candidates.set(n.url, { ...n, matchedKeyword: keyword });
        }
      } catch (e) {
        console.log(`  ❌ 关键词"${keyword}"搜索失败: ${e.message}`);
      }
      await sleep(1000);
    }
    
    if (candidates.size >= LIMIT || currentDays >= 30) break;
    currentDays += 4; // 每次扩展4天
  }

  console.log(`\n📝 候选帖子: ${candidates.size} 篇，开始抓取详情...\n`);

  // 抓取详情 + 相关性过滤
  const results = [];
  const allCandidates = Array.from(candidates.values());
  
  for (let i = 0; i < allCandidates.length && results.length < LIMIT; i++) {
    const note = allCandidates[i];
    console.log(`  [${i + 1}/${allCandidates.length}] ${note.title || note.url}`);
    const detail = await scrapeNote(page, note);
    
    // 相关性过滤
    if (!isRelevant(detail.title, detail.body)) {
      console.log(`    ⏭️  不相关，跳过`);
      continue;
    }
    results.push(detail);
    await sleep(800 + Math.random() * 700);
  }

  // 按日期分组统计
  const byDate = {};
  for (const d of targetDates) byDate[d] = [];
  for (const note of results) {
    if (note.date && byDate[note.date]) byDate[note.date].push(note);
    else if (note.date) byDate[note.date] = [note]; // 保留超出范围的
  }

  const output = {
    keyword_list: KEYWORDS,
    target_dates: targetDates,
    total: results.length,
    by_date: byDate,
    notes: results,
    trending: trending,
    scraped_at: new Date().toISOString()
  };

  const outFile = path.join(OUT_DIR, `xhs_paotui_${targetDates[0]}.json`);
  fs.writeFileSync(outFile, JSON.stringify(output, null, 2), 'utf8');
  console.log(`\n✅ 完成！共抓取 ${results.length} 篇相关帖子`);
  console.log(`   数据保存至: ${outFile}`);
  
  for (const [date, notes] of Object.entries(byDate)) {
    console.log(`   ${date}: ${notes.length} 篇`);
  }

  await browser.close();
  return outFile;
}

main().catch(e => {
  console.error('失败:', e.message);
  process.exit(1);
});
