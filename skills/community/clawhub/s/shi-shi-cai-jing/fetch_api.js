// 财经新闻抓取 + 存储脚本 (API版 - 智能增量)
// 优化：以id为唯一标识，只有id大于现有最大id的才新增
// 优化：如果当前页最小id <= 已有最大id，则不再抓取下一页
const fs = require('fs');
const path = require('path');
const https = require('https');

const DATA_DIR = path.join(__dirname, 'data');
const DB_FILE = path.join(DATA_DIR, 'news_db.json');
const STATE_FILE = path.join(DATA_DIR, 'state.json');
const MAX_DAYS = 7;
const PAGE_SIZE = 30;
const MAX_PAGES = 5;

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

// 获取数据库中今日最大新闻ID
function getTodayMaxId() {
  const db = readNewsDB();
  const today = getTodayDate();
  const todayNews = db[today] || [];
  if (todayNews.length === 0) return 0;
  return Math.max(...todayNews.map(n => n.id));
}

// 保存新闻到数据库
function saveNews(newsItems) {
  const db = readNewsDB();
  const today = getTodayDate();
  
  if (!db[today]) {
    db[today] = [];
  }
  
  // 获取数据库中所有新闻的ID（全局去重）
  const allExistingIds = new Set();
  Object.keys(db).forEach(date => {
    db[date].forEach(n => allExistingIds.add(n.id));
  });
  
  let newCount = 0;
  newsItems.forEach(item => {
    if (!allExistingIds.has(item.id)) {
      db[today].push({
        ...item,
        savedAt: new Date().toISOString()
      });
      newCount++;
    }
  });
  
  db[today].sort((a, b) => b.id - a.id);
  
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

// 读取 state.json
function readState() {
  if (!fs.existsSync(STATE_FILE)) {
    return { maxId: 0 };
  }
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch (e) {
    return { maxId: 0 };
  }
}

// 保存 state.json
function saveState(maxId) {
  const state = {
    lastRead: new Date().toISOString(),
    maxId: maxId,
    cronJobId: null
  };
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// 通过API抓取新闻（智能增量）
function fetchNewsAPI() {
  return new Promise((resolve, reject) => {
    const newsList = [];
    let currentPage = 1;
    const dbMaxId = getTodayMaxId(); // 获取数据库中今日最大ID
    const seenIds = new Set(); // 记录已见过的ID
    
    console.log(`   数据库今日最大ID: ${dbMaxId}`);
    
    function fetchPage(page) {
      const url = `https://app.cj.sina.com.cn/api/news/pc?page=${page}&size=${PAGE_SIZE}`;
      
      https.get(url, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            if (json.result && json.result.status.code === 0) {
              const list = json.result.data.feed.list || [];
              
              if (list.length === 0) {
                resolve(newsList);
                return;
              }
              
              // 获取当前页的最大ID（最新新闻的ID）
              const pageIds = list.map(item => item.id);
              const currentPageMaxId = Math.max(...pageIds);
              
              console.log(`   第${page}页: 获取${list.length}条, 最大ID=${currentPageMaxId}`);
              
              // 关键优化：如果当前页最大ID <= 数据库最大ID，说明没有新内容了
              if (currentPageMaxId <= dbMaxId) {
                console.log(`   当前页最大ID(${currentPageMaxId}) <= 数据库最大ID(${dbMaxId})，停止抓取`);
                resolve(newsList);
                return;
              }
              
              // 只添加ID大于数据库最大ID且未见过的新新闻
              let newCountInPage = 0;
              list.forEach(item => {
                if (item.id > dbMaxId && !seenIds.has(item.id)) {
                  seenIds.add(item.id);
                  const newsItem = {
                    id: item.id,
                    time: item.create_time ? item.create_time.substring(11, 19) : '',
                    text: item.rich_text,
                    create_time: item.create_time,
                    tags: item.tag ? item.tag.map(t => t.name) : []
                  };
                  newsList.push(newsItem);
                  newCountInPage++;
                }
              });
              
              console.log(`   第${page}页: 新增${newCountInPage}条`);
              
              // 如果本页没有新新闻，停止抓取
              if (newCountInPage === 0) {
                console.log(`   第${page}页无新内容，停止抓取`);
                resolve(newsList);
                return;
              }
              
              // 继续获取下一页
              if (page < MAX_PAGES) {
                fetchPage(page + 1);
              } else {
                resolve(newsList);
              }
            } else {
              reject(new Error('API返回错误: ' + JSON.stringify(json.result)));
            }
          } catch (e) {
            reject(e);
          }
        });
      }).on('error', reject);
    }
    
    fetchPage(currentPage);
  });
}

// 主函数
async function main() {
  console.log('📰 通过API抓取财经新闻（智能增量）...');
  
  try {
    const allNews = await fetchNewsAPI();
    console.log(`   共获取 ${allNews.length} 条新闻`);
    
    // 读取上次保存的最大ID
    const state = readState();
    const lastMaxId = state.maxId || 0;
    
    // 过滤出ID大于上次最大ID的新闻（这是真正的增量）
    const newNews = allNews.filter(n => n.id > lastMaxId);
    
    console.log(`   其中 ID>${lastMaxId} 的新增: ${newNews.length} 条`);
    
    if (newNews.length > 0) {
      const result = saveNews(newNews);
      console.log(`✅ 已保存 ${result.newCount} 条新闻（今日共 ${result.totalToday} 条）`);
      
      // 更新最大ID
      const newMaxId = Math.max(...newNews.map(n => n.id));
      saveState(newMaxId);
    } else {
      console.log('⏭️ 没有新增新闻');
    }
    
  } catch (e) {
    console.error('❌ 错误:', e.message);
    process.exit(1);
  }
}

main();
