// 新闻数据库管理脚本
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, 'data');
const DB_FILE = path.join(DATA_DIR, 'news_db.json');
const MAX_DAYS = 7;

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 获取今天的日期字符串（YYYY-MM-DD）
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
  
  // 初始化当天的数组
  if (!db[today]) {
    db[today] = [];
  }
  
  // 获取数据库中最新的时间戳（避免重复）
  const existingTimes = new Set(db[today].map(n => n.time));
  
  // 添加不重复的新闻
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
  
  // 按时间倒序排列
  db[today].sort((a, b) => b.time.localeCompare(a.time));
  
  // 写入数据库
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
  
  // 清理超过7天的数据
  cleanupOldData(db);
  
  return { today, newCount, totalToday: db[today].length };
}

// 清理旧数据
function cleanupOldData(db) {
  const today = getTodayDate();
  const todayDate = new Date(today);
  
  Object.keys(db).forEach(date => {
    const newsDate = new Date(date);
    const diffDays = Math.floor((todayDate - newsDate) / (1000 * 60 * 60 * 24));
    
    if (diffDays >= MAX_DAYS) {
      delete db[date];
      console.log(`🗑️ 已删除 ${date} 的新闻（${diffDays}天前）`);
    }
  });
  
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
}

// 获取今天的新闻
function getTodayNews() {
  const db = readNewsDB();
  const today = getTodayDate();
  return db[today] || [];
}

// 获取所有新闻（调试用）
function getAllNews() {
  return readNewsDB();
}

// 导出函数
module.exports = {
  saveNews,
  getTodayNews,
  getAllNews,
  getTodayDate
};

// 命令行执行
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (command === 'save' && args[1]) {
    const news = JSON.parse(args[1]);
    const result = saveNews(news);
    console.log(JSON.stringify(result));
  } else if (command === 'get-today') {
    console.log(JSON.stringify(getTodayNews(), null, 2));
  } else if (command === 'get-all') {
    console.log(JSON.stringify(getAllNews(), null, 2));
  } else if (command === 'stats') {
    const db = readNewsDB();
    const today = getTodayDate();
    console.log(`📊 新闻数据库统计`);
    console.log(`   存储天数: ${Object.keys(db).length}`);
    console.log(`   今日新闻: ${(db[today] || []).length} 条`);
    console.log(`   日期范围: ${Object.keys(db).sort().join(' ~ ')}`);
  }
}
