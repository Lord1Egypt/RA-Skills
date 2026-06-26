/**
 * 视频列表获取器
 * 从抖音创作者中心获取当前用户发布的所有视频列表
 * 
 * 功能：
 * - 获取用户发布视频列表
 * - 提取视频ID、标题、评论数等
 * - 支持分页获取
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG_PATH = path.join(__dirname, '..', 'config', 'video_list_config.json');
const DATA_PATH = path.join(__dirname, '..', 'data', 'video_list.json');

// 默认配置
const DEFAULT_CONFIG = {
  // 创作者中心内容管理页面
  contentManageUrl: 'https://creator.douyin.com/creator-micro/content/manage',
  // 视频列表选择器
  selectors: {
    videoItem: '[class*="video-item"]',
    videoLink: 'a[href*="/video/"]',
    videoTitle: '[class*="title"]',
    commentCount: '[class*="comment"]',
    likeCount: '[class*="like"]',
    loadMoreBtn: '[class*="load-more"]'
  },
  // 滚动加载配置
  scrollConfig: {
    enabled: true,
    scrollTimes: 5,        // 滚动次数
    scrollDelay: 1000      // 滚动间隔(ms)
  },
  // 缓存配置
  cache: {
    enabled: true,
    ttl: 3600000          // 缓存有效期 1小时
  }
};

/**
 * 加载配置
 */
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      return {...DEFAULT_CONFIG, ...config};
    }
  } catch (error) {
    console.error('[VideoList] 配置加载失败:', error.message);
  }
  return DEFAULT_CONFIG;
}

/**
 * 保存视频列表到本地
 */
function saveVideoList(videos) {
  try {
    const data = {
      updatedAt: new Date().toISOString(),
      count: videos.length,
      videos: videos
    };
    
    const dir = path.dirname(DATA_PATH);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, {recursive: true});
    }
    
    fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2), 'utf8');
    console.log(`[VideoList] 已保存 ${videos.length} 个视频到本地`);
    return true;
  } catch (error) {
    console.error('[VideoList] 保存失败:', error.message);
    return false;
  }
}

/**
 * 从本地加载视频列表
 */
function loadVideoList() {
  try {
    if (fs.existsSync(DATA_PATH)) {
      const data = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
      return data;
    }
  } catch (error) {
    console.error('[VideoList] 本地数据加载失败:', error.message);
  }
  return null;
}

/**
 * 检查缓存是否有效
 */
function isCacheValid(cachedData, config) {
  if (!config.cache.enabled || !cachedData) return false;
  
  const now = Date.now();
  const updatedAt = new Date(cachedData.updatedAt).getTime();
  return (now - updatedAt) < config.cache.ttl;
}

/**
 * 通过浏览器页面提取视频列表
 * 这个函数需要在浏览器上下文中执行
 */
function extractVideosFromPage() {
  const videos = [];
  
  // 方法1：从DOM提取（需要根据实际页面结构调整选择器）
  const videoItems = document.querySelectorAll('[class*="video-item"], [class*="VideoItem"], [class*="content-item"]');
  
  videoItems.forEach((item, index) => {
    try {
      // 提取视频链接
      const linkElement = item.querySelector('a[href*="/video/"]') || 
                          item.querySelector('a');
      const videoUrl = linkElement ? linkElement.href : '';
      
      // 提取视频ID
      const videoIdMatch = videoUrl.match(/video\/(\w+)/);
      const videoId = videoIdMatch ? videoIdMatch[1] : `unknown_${index}`;
      
      // 提取标题
      const titleElement = item.querySelector('[class*="title"], [class*="Title"], h3, h4');
      const title = titleElement ? titleElement.textContent.trim() : '';
      
      // 提取数据统计
      const statsElement = item.querySelector('[class*="stats"], [class*="data"]');
      let commentCount = 0;
      let likeCount = 0;
      
      if (statsElement) {
        const text = statsElement.textContent;
        const commentMatch = text.match(/评论[：:\s]*(\d+)/);
        const likeMatch = text.match(/赞[：:\s]*(\d+)/);
        commentCount = commentMatch ? parseInt(commentMatch[1]) : 0;
        likeCount = likeMatch ? parseInt(likeMatch[1]) : 0;
      }
      
      // 提取发布时间
      const timeElement = item.querySelector('[class*="time"], [class*="date"], time');
      const publishTime = timeElement ? timeElement.textContent.trim() : '';
      
      if (videoId && videoUrl) {
        videos.push({
          id: videoId,
          url: videoUrl,
          title: title,
          commentCount: commentCount,
          likeCount: likeCount,
          publishTime: publishTime,
          extractedAt: new Date().toISOString()
        });
      }
    } catch (error) {
      console.error('提取视频信息失败:', error);
    }
  });
  
  return videos;
}

/**
 * 滚动页面以加载更多视频
 */
async function scrollToLoadMore(page, config) {
  if (!config.scrollConfig.enabled) return;
  
  for (let i = 0; i < config.scrollConfig.scrollTimes; i++) {
    await page.evaluate(() => {
      window.scrollBy(0, window.innerHeight);
    });
    await page.waitForTimeout(config.scrollConfig.scrollDelay);
    console.log(`[VideoList] 滚动 ${i + 1}/${config.scrollConfig.scrollTimes}`);
  }
}

/**
 * 获取视频列表（主函数）
 * @param {Object} page - Playwright page 对象
 * @param {Object} options - 选项
 * @returns {Promise<Array>} 视频列表
 */
async function getVideoList(page, options = {}) {
  const config = loadConfig();
  
  console.log('[VideoList] 开始获取视频列表...');
  
  // 检查缓存
  if (options.useCache !== false) {
    const cached = loadVideoList();
    if (isCacheValid(cached, config)) {
      console.log('[VideoList] 使用缓存数据');
      return cached.videos;
    }
  }
  
  // 导航到内容管理页面
  console.log('[VideoList] 导航到创作者中心...');
  await page.goto(config.contentManageUrl, {waitUntil: 'networkidle'});
  await page.waitForTimeout(2000);
  
  // 等待页面加载
  try {
    await page.waitForSelector('[class*="video"], [class*="content"]', {timeout: 10000});
  } catch (error) {
    console.error('[VideoList] 页面加载超时，可能需要登录');
    return [];
  }
  
  // 滚动加载更多
  await scrollToLoadMore(page, config);
  
  // 提取视频列表
  const videos = await page.evaluate(extractVideosFromPage);
  
  console.log(`[VideoList] 提取到 ${videos.length} 个视频`);
  
  // 保存到本地
  if (videos.length > 0) {
    saveVideoList(videos);
  }
  
  return videos;
}

/**
 * 获取需要监控的视频（有评论的视频）
 * @param {Array} videos - 视频列表
 * @param {Object} options - 过滤选项
 * @returns {Array} 需要监控的视频
 */
function getVideosToMonitor(videos, options = {}) {
  const {minComments = 0, maxVideos = 10} = options;
  
  return videos
    .filter(v => v.commentCount >= minComments)
    .sort((a, b) => b.commentCount - a.commentCount)  // 按评论数降序
    .slice(0, maxVideos);
}

/**
 * 生成监控配置
 * 将视频列表转换为监控目标格式
 */
function generateMonitorTargets(videos, options = {}) {
  return videos.map(v => ({
    id: v.id,
    url: v.url,
    title: v.title,
    commentCount: v.commentCount,
    enabled: true,
    monitorDepth: options.monitorDepth || 2,
    lastCheck: null,
    addedAt: new Date().toISOString()
  }));
}

// 导出
module.exports = {
  getVideoList,
  getVideosToMonitor,
  generateMonitorTargets,
  saveVideoList,
  loadVideoList,
  extractVideosFromPage,
  DEFAULT_CONFIG
};
