// 财经新闻抓取 + 存储脚本
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, 'data');
const DB_FILE = path.join(DATA_DIR, 'news_db.json');
const STATE_FILE = path.join(__dirname, 'state.json');
const MAX_DAYS = 7;

// 获取今天的日期字符串
function getTodayDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// 读取新闻数据库
function readNewsDB() {
  if (!fs.existsSync(DB_FILE)) {
    return {};
  }
  try {
    return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
  } catch (e) {
    return {};
  }
}

// 保存新闻到数据库
function saveNews(newsItems) {
  const db = readNewsDB();
  const today = getTodayDate();
  
  if (!db[today]) {
    db[today] = [];
  }
  
  const existingTimes = new Set(db[today].map(n => n.time));
  
  let newCount = 0;
  newsItems.forEach(item => {
    if (!existingTimes.has(item.time)) {
      db[today].push({
        ...item,
        savedAt: new Date().toISOString()
      });
      newCount++;
    }
  });
  
  db[today].sort((a, b) => b.time.localeCompare(a.time));
  
  // 清理旧数据
  const todayDate = new Date(today);
  Object.keys(db).forEach(date => {
    const newsDate = new Date(date);
    const diffDays = Math.floor((todayDate - newsDate) / (1000 * 60 * 60 * 24));
    if (diffDays >= MAX_DAYS) {
      delete db[date];
    }
  });
  
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
  
  return { today, newCount, totalToday: db[today].length };
}

// 抓取新闻
async function fetchNews() {
  const browser = await puppeteer.connect({ browserURL: 'http://localhost:9222' });
  const pages = await browser.pages();
  const page = pages.find(p => p.url().includes('finance.sina.com.cn/7x24')) || pages[0];
  
  await new Promise(r => setTimeout(r, 2000));
  
  const news = await page.evaluate(() => {
    const results = [];
    const items = document.querySelectorAll('.bd_i, .live-item, .news-item, [class*="bd_i"]');
    
    items.forEach(el => {
      const timeEl = el.querySelector('.bd_i_time, .time, [class*="time"]');
      const textEl = el.querySelector('.bd_i_txt_c, .txt, [class*="txt"]');
      
      if (timeEl && textEl) {
        results.push({
          time: timeEl.innerText.trim(),
          text: textEl.innerText.trim()
        });
      }
    });
    
    return results.slice(0, 15);
  });
  
  await browser.disconnect();
  return news;
}

// 主函数
async function main() {
  console.log('📰 抓取财经新闻并保存...');
  
  try {
    const news = await fetchNews();
    const result = saveNews(news);
    
    console.log(`✅ 已保存 ${result.newCount} 条新闻（今日共 ${result.totalToday} 条）`);
    
    // 更新 state.json
    if (news.length > 0) {
      const state = {
        lastRead: new Date().toISOString(),
        lastTime: news[0].time,
        cronJobId: null
      };
      fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
    }
    
  } catch (e) {
    console.error('❌ 错误:', e.message);
    process.exit(1);
  }
}

main();
