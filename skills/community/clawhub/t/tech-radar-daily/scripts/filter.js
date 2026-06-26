/**
 * 数据过滤器 - 过滤和去重
 */

const fs = require('fs');
const path = require('path');

// 去重数据库路径
const SEEN_REPOS_PATH = path.join(__dirname, '../data/seen_repos.json');

/**
 * 过滤和去重主函数
 */
async function filterAndDedupe(projects) {
  // 1. 加载历史记录
  const seenRepos = loadSeenRepos();
  
  // 2. 基础过滤
  let filtered = projects.filter(item => {
    // 必须有名称和链接
    if (!item.name || !item.url) return false;
    
    // GitHub 项目必须有一定 star 数
    if (item.sourceType === 'github' && item.stars < 50) return false;
    
    // 过滤掉太老的项目
    if (item.lastUpdate) {
      const daysSinceUpdate = getDaysSince(item.lastUpdate);
      if (daysSinceUpdate > 365) return false;
    }
    
    return true;
  });
  
  // 3. 去重过滤
  filtered = filtered.filter(item => {
    const key = getProjectKey(item);
    
    // 检查是否在 7 天内推荐过
    if (seenRepos[key]) {
      const daysSinceSeen = getDaysSince(seenRepos[key].last_recommended);
      if (daysSinceSeen < 7) {
        console.log(` 跳过重复项目：${key} (${daysSinceSeen}天前推荐过)`);
        return false;
      }
    }
    
    return true;
  });
  
  // 4. 同类型限制
  filtered = limitByType(filtered);
  
  // 5. 跨平台去重
  filtered = crossPlatformDedupe(filtered);
  
  return filtered;
}

/**
 * 加载去重数据库
 */
function loadSeenRepos() {
  try {
    const data = fs.readFileSync(SEEN_REPOS_PATH, 'utf-8');
    return JSON.parse(data);
  } catch (e) {
    return {};
  }
}

/**
 * 获取项目唯一标识
 */
function getProjectKey(item) {
  if (item.repoName) {
    return item.repoName.toLowerCase();
  }
  
  // 从 URL 提取
  const match = item.url.match(/github\.com\/([^/]+\/[^/]+)/);
  if (match) {
    return match[1].toLowerCase();
  }
  
  // 使用名称作为 fallback
  return item.name.toLowerCase().replace(/\s+/g, '-');
}

/**
 * 计算天数差
 */
function getDaysSince(dateStr) {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

/**
 * 限制同类型数量
 */
function limitByType(projects) {
  const typeCount = {};
  const limited = [];
  
  for (const item of projects) {
    const type = item.sourceType || 'other';
    typeCount[type] = (typeCount[type] || 0) + 1;
    
    // 每种类型最多保留的数量
    const limits = {
      'github': 3,
      'tools': 2,
      'product': 1,
      'trend': 2,
      'awesome': 1
    };
    
    const limit = limits[type] || 2;
    
    if (typeCount[type] <= limit) {
      limited.push(item);
    }
  }
  
  return limited;
}

/**
 * 跨平台去重
 */
function crossPlatformDedupe(projects) {
  const seen = new Map();
  const deduped = [];
  
  for (const item of projects) {
    // 生成标准化名称
    const normalizedName = item.name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '')
      .trim();
    
    if (!seen.has(normalizedName)) {
      seen.set(normalizedName, item);
      deduped.push(item);
    } else {
      // 如果已存在，选择更权威的来源
      const existing = seen.get(normalizedName);
      if (getSourcePriority(item) > getSourcePriority(existing)) {
        // 替换为更权威的来源
        const index = deduped.indexOf(existing);
        deduped[index] = item;
        seen.set(normalizedName, item);
      }
    }
  }
  
  return deduped;
}

/**
 * 获取来源优先级
 */
function getSourcePriority(item) {
  const priorities = {
    'github-trending': 10,
    'github-topic': 9,
    'product-hunt': 8,
    'hacker-news': 7,
    'awesome': 6
  };
  
  return priorities[item.source] || 5;
}

module.exports = {
  filterAndDedupe
};
