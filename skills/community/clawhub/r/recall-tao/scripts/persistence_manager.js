/**
 * 数据持久化管理器 - 断点续传与状态管理
 * 支持：已处理评论记录、监控状态持久化、数据恢复
 * 
 * 版本：v1.0
 * 更新日期：2026-04-02
 */

const fs = require('fs');
const path = require('path');

// ==================== 路径配置 ====================

const DATA_DIR = path.join(__dirname, '../data');
const STATE_FILE = path.join(DATA_DIR, 'monitor_state.json');
const PROCESSED_FILE = path.join(DATA_DIR, 'processed_comments.json');
const PENDING_FILE = path.join(DATA_DIR, 'pending_replies.json');

// ==================== 初始化 ====================

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

function initializeFiles() {
  ensureDataDir();
  
  if (!fs.existsSync(STATE_FILE)) {
    writeJson(STATE_FILE, getDefaultState());
  }
  
  if (!fs.existsSync(PROCESSED_FILE)) {
    writeJson(PROCESSED_FILE, { comments: [], lastUpdated: null });
  }
  
  if (!fs.existsSync(PENDING_FILE)) {
    writeJson(PENDING_FILE, { items: [], lastUpdated: null });
  }
}

function getDefaultState() {
  return {
    version: '1.0',
    status: 'idle',
    lastCheck: null,
    videos: [],
    stats: {
      totalProcessed: 0,
      totalReplied: 0,
      totalSkipped: 0,
      totalManualReview: 0
    },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
}

// ==================== 工具函数 ====================

function readJson(filepath) {
  try {
    if (fs.existsSync(filepath)) {
      const content = fs.readFileSync(filepath, 'utf-8');
      return JSON.parse(content);
    }
    return null;
  } catch (error) {
    console.error(`读取文件失败 ${filepath}:`, error.message);
    return null;
  }
}

function writeJson(filepath, data) {
  ensureDataDir();
  data.lastUpdated = new Date().toISOString();
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
  return data;
}

// ==================== 监控状态管理 ====================

/**
 * 获取监控状态
 * @returns {object}
 */
function getMonitorState() {
  initializeFiles();
  return readJson(STATE_FILE);
}

/**
 * 更新监控状态
 * @param {object} updates 状态更新
 */
function updateMonitorState(updates) {
  const state = getMonitorState();
  const newState = {
    ...state,
    ...updates,
    updatedAt: new Date().toISOString()
  };
  writeJson(STATE_FILE, newState);
  return newState;
}

/**
 * 设置监控状态
 * @param {string} status 状态: idle | running | paused | error
 * @param {object} meta 附加信息
 */
function setMonitorStatus(status, meta = {}) {
  return updateMonitorState({
    status,
    ...meta
  });
}

/**
 * 记录检查时间
 */
function recordCheckTime() {
  return updateMonitorState({
    lastCheck: new Date().toISOString()
  });
}

/**
 * 更新统计数据
 * @param {object} statsDelta 统计增量
 */
function updateStats(statsDelta) {
  const state = getMonitorState();
  const newStats = {
    ...state.stats,
    totalProcessed: (state.stats.totalProcessed || 0) + (statsDelta.processed || 0),
    totalReplied: (state.stats.totalReplied || 0) + (statsDelta.replied || 0),
    totalSkipped: (state.stats.totalSkipped || 0) + (statsDelta.skipped || 0),
    totalManualReview: (state.stats.totalManualReview || 0) + (statsDelta.manualReview || 0)
  };
  return updateMonitorState({ stats: newStats });
}

// ==================== 已处理评论管理 ====================

/**
 * 获取已处理评论列表
 * @returns {Set<string>} 评论ID集合
 */
function getProcessedComments() {
  initializeFiles();
  const data = readJson(PROCESSED_FILE);
  // 提取 ID 列表（兼容新旧格式）
  const ids = (data?.comments || []).map(c => typeof c === 'string' ? c : c.id);
  return new Set(ids);
}

/**
 * 检查评论是否已处理
 * @param {string} commentId 评论ID
 * @returns {boolean}
 */
function isCommentProcessed(commentId) {
  const processed = getProcessedComments();
  return processed.has(commentId);
}

/**
 * 标记评论为已处理
 * @param {string} commentId 评论ID
 * @param {object} meta 处理信息
 */
function markCommentProcessed(commentId, meta = {}) {
  initializeFiles();
  const data = readJson(PROCESSED_FILE) || { comments: [] };
  
  // 限制列表大小（保留最近10000条）
  if (data.comments.length >= 10000) {
    data.comments = data.comments.slice(-9000);
  }
  
  data.comments.push({
    id: commentId,
    processedAt: new Date().toISOString(),
    ...meta
  });
  
  writeJson(PROCESSED_FILE, data);
  return data;
}

/**
 * 批量标记评论为已处理
 * @param {Array<{id: string, meta: object}>} comments 评论列表
 */
function markCommentsProcessed(comments) {
  initializeFiles();
  const data = readJson(PROCESSED_FILE) || { comments: [] };
  
  const now = new Date().toISOString();
  const newComments = comments.map(c => ({
    id: c.id,
    processedAt: now,
    ...(c.meta || {})
  }));
  
  data.comments.push(...newComments);
  
  // 限制大小
  if (data.comments.length >= 10000) {
    data.comments = data.comments.slice(-9000);
  }
  
  writeJson(PROCESSED_FILE, data);
  return data;
}

/**
 * 清理过期的已处理记录
 * @param {number} daysToKeep 保留天数
 */
function cleanProcessedComments(daysToKeep = 7) {
  initializeFiles();
  const data = readJson(PROCESSED_FILE);
  if (!data || !data.comments) return;
  
  const cutoff = Date.now() - daysToKeep * 86400000;
  const cutoffDate = new Date(cutoff).toISOString();
  
  data.comments = data.comments.filter(c => c.processedAt > cutoffDate);
  writeJson(PROCESSED_FILE, data);
  
  return {
    cleaned: true,
    remaining: data.comments.length
  };
}

// ==================== 待回复队列管理 ====================

/**
 * 获取待回复队列
 * @returns {Array}
 */
function getPendingReplies() {
  initializeFiles();
  const data = readJson(PENDING_FILE);
  return data?.items || [];
}

/**
 * 添加待回复项
 * @param {object} item 待回复项
 */
function addPendingReply(item) {
  initializeFiles();
  const data = readJson(PENDING_FILE) || { items: [] };
  
  data.items.push({
    ...item,
    addedAt: new Date().toISOString(),
    status: 'pending'
  });
  
  writeJson(PENDING_FILE, data);
  return data;
}

/**
 * 批量添加待回复项
 * @param {Array} items 待回复项列表
 */
function addPendingReplies(items) {
  initializeFiles();
  const data = readJson(PENDING_FILE) || { items: [] };
  
  const now = new Date().toISOString();
  const newItems = items.map(item => ({
    ...item,
    addedAt: now,
    status: 'pending'
  }));
  
  data.items.push(...newItems);
  writeJson(PENDING_FILE, data);
  
  return data;
}

/**
 * 移除待回复项
 * @param {string} commentId 评论ID
 */
function removePendingReply(commentId) {
  initializeFiles();
  const data = readJson(PENDING_FILE);
  if (!data || !data.items) return;
  
  data.items = data.items.filter(item => item.commentId !== commentId);
  writeJson(PENDING_FILE, data);
  
  return data;
}

/**
 * 更新待回复项状态
 * @param {string} commentId 评论ID
 * @param {string} status 状态: pending | processing | completed | failed
 * @param {object} meta 附加信息
 */
function updatePendingReplyStatus(commentId, status, meta = {}) {
  initializeFiles();
  const data = readJson(PENDING_FILE);
  if (!data || !data.items) return;
  
  const index = data.items.findIndex(item => item.commentId === commentId);
  if (index !== -1) {
    data.items[index] = {
      ...data.items[index],
      status,
      ...meta,
      updatedAt: new Date().toISOString()
    };
    writeJson(PENDING_FILE, data);
  }
  
  return data;
}

/**
 * 获取下一个待处理项
 * @returns {object|null}
 */
function getNextPendingReply() {
  const items = getPendingReplies();
  return items.find(item => item.status === 'pending') || null;
}

// ==================== 视频监控状态 ====================

/**
 * 获取视频监控列表
 * @returns {Array}
 */
function getMonitoredVideos() {
  const state = getMonitorState();
  return state.videos || [];
}

/**
 * 添加监控视频
 * @param {object} video 视频信息
 */
function addMonitoredVideo(video) {
  const state = getMonitorState();
  
  if (!state.videos.find(v => v.id === video.id)) {
    state.videos.push({
      ...video,
      addedAt: new Date().toISOString(),
      lastCheck: null,
      commentCount: 0
    });
    writeJson(STATE_FILE, state);
  }
  
  return state;
}

/**
 * 移除监控视频
 * @param {string} videoId 视频ID
 */
function removeMonitoredVideo(videoId) {
  const state = getMonitorState();
  state.videos = state.videos.filter(v => v.id !== videoId);
  writeJson(STATE_FILE, state);
  return state;
}

/**
 * 更新视频检查状态
 * @param {string} videoId 视频ID
 * @param {object} updates 更新内容
 */
function updateVideoStatus(videoId, updates) {
  const state = getMonitorState();
  const index = state.videos.findIndex(v => v.id === videoId);
  
  if (index !== -1) {
    state.videos[index] = {
      ...state.videos[index],
      ...updates,
      lastCheck: new Date().toISOString()
    };
    writeJson(STATE_FILE, state);
  }
  
  return state;
}

// ==================== 导出 ====================

module.exports = {
  // 监控状态
  getMonitorState,
  updateMonitorState,
  setMonitorStatus,
  recordCheckTime,
  updateStats,
  
  // 已处理评论
  getProcessedComments,
  isCommentProcessed,
  markCommentProcessed,
  markCommentsProcessed,
  cleanProcessedComments,
  
  // 待回复队列
  getPendingReplies,
  addPendingReply,
  addPendingReplies,
  removePendingReply,
  updatePendingReplyStatus,
  getNextPendingReply,
  
  // 视频监控
  getMonitoredVideos,
  addMonitoredVideo,
  removeMonitoredVideo,
  updateVideoStatus,
  
  // 工具
  initializeFiles
};

// 初始化
initializeFiles();
