/**
 * 批量监控管理器
 * 
 * 核心能力：
 * 1. 自动获取用户发布的视频列表
 * 2. 批量监控多个视频的评论
 * 3. 支持多层级评论结构
 * 4. 增量检查，只处理新评论
 * 
 * 使用方式：
 * const monitor = new BatchMonitor();
 * await monitor.start();  // 自动获取视频列表并开始监控
 */

const fs = require('fs');
const path = require('path');
const videoListFetcher = require('./video_list_fetcher');

// 路径配置
const CONFIG_DIR = path.join(__dirname, '..', 'config');
const DATA_DIR = path.join(__dirname, '..', 'data');
const MONITOR_TARGETS_PATH = path.join(DATA_DIR, 'monitor_targets.json');
const PROCESSED_PATH = path.join(DATA_DIR, 'processed_comments.json');

/**
 * 批量监控管理器类
 */
class BatchMonitor {
  constructor(options = {}) {
    this.page = options.page || null;
    this.browser = options.browser || null;
    this.targets = [];
    this.processedComments = {};
    this.isRunning = false;
    this.config = {
      maxVideos: options.maxVideos || 10,
      minComments: options.minComments || 0,
      checkInterval: options.checkInterval || 60000,  // 检查间隔
      monitorDepth: options.monitorDepth || 2,
      autoAddVideos: options.autoAddVideos !== false  // 默认自动添加视频
    };
    
    this.loadState();
  }
  
  /**
   * 加载持久化状态
   */
  loadState() {
    // 加载监控目标
    try {
      if (fs.existsSync(MONITOR_TARGETS_PATH)) {
        const data = JSON.parse(fs.readFileSync(MONITOR_TARGETS_PATH, 'utf8'));
        this.targets = data.targets || [];
        console.log(`[BatchMonitor] 加载 ${this.targets.length} 个监控目标`);
      }
    } catch (error) {
      console.error('[BatchMonitor] 加载监控目标失败:', error.message);
    }
    
    // 加载已处理评论
    try {
      if (fs.existsSync(PROCESSED_PATH)) {
        const data = JSON.parse(fs.readFileSync(PROCESSED_PATH, 'utf8'));
        this.processedComments = data.processed || {};
      }
    } catch (error) {
      console.error('[BatchMonitor] 加载已处理评论失败:', error.message);
    }
  }
  
  /**
   * 保存状态
   */
  saveState() {
    try {
      // 保存监控目标
      const targetsDir = path.dirname(MONITOR_TARGETS_PATH);
      if (!fs.existsSync(targetsDir)) {
        fs.mkdirSync(targetsDir, {recursive: true});
      }
      
      fs.writeFileSync(MONITOR_TARGETS_PATH, JSON.stringify({
        updatedAt: new Date().toISOString(),
        targets: this.targets
      }, null, 2), 'utf8');
      
      // 保存已处理评论
      fs.writeFileSync(PROCESSED_PATH, JSON.stringify({
        updatedAt: new Date().toISOString(),
        processed: this.processedComments
      }, null, 2), 'utf8');
      
    } catch (error) {
      console.error('[BatchMonitor] 保存状态失败:', error.message);
    }
  }
  
  /**
   * 初始化：自动获取视频列表
   * @param {Object} page - Playwright page 对象
   */
  async initialize(page) {
    this.page = page;
    
    console.log('[BatchMonitor] 初始化...');
    
    // 如果启用自动添加视频，或者当前没有目标
    if (this.config.autoAddVideos || this.targets.length === 0) {
      await this.refreshVideoList();
    }
    
    console.log(`[BatchMonitor] 初始化完成，当前监控 ${this.targets.length} 个视频`);
    return this.targets.length;
  }
  
  /**
   * 刷新视频列表
   * 从创作者中心获取最新发布的视频
   */
  async refreshVideoList() {
    console.log('[BatchMonitor] 正在获取视频列表...');
    
    try {
      // 获取所有视频
      const allVideos = await videoListFetcher.getVideoList(this.page, {
        useCache: false
      });
      
      if (allVideos.length === 0) {
        console.log('[BatchMonitor] 未获取到视频，可能需要先登录');
        return [];
      }
      
      // 筛选需要监控的视频
      const videosToMonitor = videoListFetcher.getVideosToMonitor(allVideos, {
        minComments: this.config.minComments,
        maxVideos: this.config.maxVideos
      });
      
      // 生成监控目标
      const newTargets = videoListFetcher.generateMonitorTargets(videosToMonitor, {
        monitorDepth: this.config.monitorDepth
      });
      
      // 合并到现有目标（保留已处理的记录）
      const existingIds = new Set(this.targets.map(t => t.id));
      for (const target of newTargets) {
        if (!existingIds.has(target.id)) {
          this.targets.push(target);
        }
      }
      
      // 保存状态
      this.saveState();
      
      console.log(`[BatchMonitor] 获取到 ${allVideos.length} 个视频，筛选出 ${videosToMonitor.length} 个进行监控`);
      return newTargets;
      
    } catch (error) {
      console.error('[BatchMonitor] 获取视频列表失败:', error.message);
      return [];
    }
  }
  
  /**
   * 添加单个视频到监控列表
   */
  addTarget(videoUrl, options = {}) {
    // 从URL提取视频ID
    const videoIdMatch = videoUrl.match(/video\/(\w+)/);
    if (!videoIdMatch) {
      console.error('[BatchMonitor] 无效的视频URL');
      return null;
    }
    
    const videoId = videoIdMatch[1];
    
    // 检查是否已存在
    if (this.targets.some(t => t.id === videoId)) {
      console.log(`[BatchMonitor] 视频 ${videoId} 已在监控列表中`);
      return videoId;
    }
    
    const target = {
      id: videoId,
      url: videoUrl,
      title: options.title || '',
      enabled: true,
      monitorDepth: options.monitorDepth || this.config.monitorDepth,
      lastCheck: null,
      addedAt: new Date().toISOString()
    };
    
    this.targets.push(target);
    this.saveState();
    
    console.log(`[BatchMonitor] 已添加视频 ${videoId} 到监控列表`);
    return videoId;
  }
  
  /**
   * 移除监控目标
   */
  removeTarget(videoId) {
    const index = this.targets.findIndex(t => t.id === videoId);
    if (index > -1) {
      this.targets.splice(index, 1);
      this.saveState();
      console.log(`[BatchMonitor] 已移除视频 ${videoId}`);
      return true;
    }
    return false;
  }
  
  /**
   * 获取监控状态
   */
  getStatus() {
    return {
      isRunning: this.isRunning,
      targetCount: this.targets.length,
      enabledCount: this.targets.filter(t => t.enabled).length,
      targets: this.targets.map(t => ({
        id: t.id,
        title: t.title || '未命名',
        enabled: t.enabled,
        lastCheck: t.lastCheck,
        processedCount: (this.processedComments[t.id] || []).length
      }))
    };
  }
  
  /**
   * 检查单个视频的评论
   */
  async checkVideoComments(target) {
    if (!this.page) {
      throw new Error('Page 未初始化');
    }
    
    console.log(`[BatchMonitor] 检查视频: ${target.id}`);
    
    // 导航到视频评论页面
    const commentUrl = target.url.includes('comment') 
      ? target.url 
      : target.url.replace('/video/', '/comment/');
    
    await this.page.goto(commentUrl, {waitUntil: 'networkidle'});
    await this.page.waitForTimeout(1500);
    
    // 提取评论
    const comments = await this.extractComments();
    
    // 过滤出新评论
    const processedIds = new Set(this.processedComments[target.id] || []);
    const newComments = comments.filter(c => !processedIds.has(c.id));
    
    // 更新最后检查时间
    target.lastCheck = new Date().toISOString();
    
    return {
      videoId: target.id,
      total: comments.length,
      newCount: newComments.length,
      comments: newComments
    };
  }
  
  /**
   * 从当前页面提取评论
   */
  async extractComments() {
    return await this.page.evaluate(() => {
      const comments = [];
      
      // 评论项选择器（需要根据实际页面调整）
      const commentElements = document.querySelectorAll(
        '[class*="comment-item"], [class*="CommentItem"], [class*="reply-item"]'
      );
      
      commentElements.forEach((element, index) => {
        try {
          // 提取评论ID（可能需要从data属性或URL中获取）
          const commentId = element.getAttribute('data-id') || 
                           element.id || 
                           `comment_${Date.now()}_${index}`;
          
          // 提取作者
          const authorElement = element.querySelector(
            '[class*="author"], [class*="name"], [class*="username"]'
          );
          const author = authorElement ? authorElement.textContent.trim() : '';
          
          // 提取内容
          const contentElement = element.querySelector(
            '[class*="content"], [class*="text"]'
          );
          const content = contentElement ? contentElement.textContent.trim() : '';
          
          // 检查是否已回复（是否有作者的嵌套回复）
          const hasAuthorReply = element.querySelector('[class*="author-reply"]') !== null;
          
          // 检查是否有回复按钮
          const hasReplyButton = element.querySelector('button:has-text("回复")') !== null;
          
          if (content) {
            comments.push({
              id: commentId,
              author: author,
              content: content,
              hasAuthorReply: hasAuthorReply,
              canReply: hasReplyButton && !hasAuthorReply
            });
          }
        } catch (error) {
          // 忽略单个评论提取错误
        }
      });
      
      return comments;
    });
  }
  
  /**
   * 标记评论已处理
   */
  markProcessed(videoId, commentId) {
    if (!this.processedComments[videoId]) {
      this.processedComments[videoId] = [];
    }
    
    if (!this.processedComments[videoId].includes(commentId)) {
      this.processedComments[videoId].push(commentId);
      this.saveState();
    }
  }
  
  /**
   * 批量检查所有视频
   */
  async checkAllVideos() {
    const results = [];
    
    for (const target of this.targets) {
      if (!target.enabled) continue;
      
      try {
        const result = await this.checkVideoComments(target);
        results.push(result);
        
        // 间隔一段时间，避免请求过快
        await this.page.waitForTimeout(2000);
        
      } catch (error) {
        console.error(`[BatchMonitor] 检查视频 ${target.id} 失败:`, error.message);
        results.push({
          videoId: target.id,
          error: error.message
        });
      }
    }
    
    return results;
  }
}

// 导出
module.exports = {
  BatchMonitor
};
