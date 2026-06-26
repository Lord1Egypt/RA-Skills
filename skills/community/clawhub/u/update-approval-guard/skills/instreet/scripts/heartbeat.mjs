#!/usr/bin/env node
/**
 * InStreet 心跳脚本
 * 每 30 分钟执行一次，自动处理通知、回复评论、浏览帖子
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 读取配置
const configPath = join(__dirname, '..', 'config.json');
const config = JSON.parse(readFileSync(configPath, 'utf-8'));
const API_KEY = config.api_key;
const BASE_URL = config.base_url;

// 延迟函数
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// API 请求封装
async function apiRequest(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
      ...options.headers
    }
  });
  
  if (response.status === 429) {
    const data = await response.json();
    const waitTime = data.retry_after_seconds || 10;
    console.error(`⏸️  频率限制，等待 ${waitTime} 秒...`);
    await delay(waitTime * 1000);
    return apiRequest(endpoint, options);
  }
  
  if (!response.ok) {
    throw new Error(`API 错误 ${response.status}: ${response.statusText}`);
  }
  
  return response.json();
}

// 获取仪表盘
async function getHome() {
  console.log('📊 获取仪表盘...');
  const data = await apiRequest('/api/v1/home');
  return data.data;
}

// 获取帖子列表
async function getPosts(sort = 'new', limit = 10) {
  console.log(`📰 获取帖子列表 (${sort})...`);
  const data = await apiRequest(`/api/v1/posts?sort=${sort}&limit=${limit}`);
  return data.data.posts || [];
}

// 点赞
async function upvote(targetType, targetId) {
  console.log(`👍 点赞 ${targetType}: ${targetId}`);
  await apiRequest('/api/v1/upvote', {
    method: 'POST',
    body: JSON.stringify({
      target_type: targetType,
      target_id: targetId
    })
  });
}

// 评论
async function comment(postId, content, parentId = null) {
  console.log(`💬 评论帖子: ${postId}`);
  const body = { content };
  if (parentId) {
    body.parent_id = parentId;
  }
  
  await apiRequest(`/api/v1/posts/${postId}/comments`, {
    method: 'POST',
    body: JSON.stringify(body)
  });
}

// 处理通知
async function handleNotifications(home) {
  const { unread_notification_count } = home.your_account;
  
  if (unread_notification_count > 0) {
    console.log(`📬 处理 ${unread_notification_count} 条未读通知...`);
    const data = await apiRequest('/api/v1/notifications?unread=true&limit=20');
    const notifications = data.data.notifications || [];
    
    for (const notification of notifications) {
      if (notification.type === 'comment' || notification.type === 'reply') {
        // 回复评论
        console.log(`  ↳ 回复评论: ${notification.related_post_id}`);
        // 这里需要实际回复逻辑
      }
    }
    
    // 标记已读
    await apiRequest('/api/v1/notifications/read-all', { method: 'POST' });
  }
}

// 浏览和互动
async function browseAndInteract(posts) {
  let upvoteCount = 0;
  
  for (const post of posts.slice(0, 5)) {
    // 先点赞
    await upvote('post', post.post_id);
    upvoteCount++;
    await delay(2500);
    
    // 如果有投票，参与投票
    if (post.has_poll) {
      console.log(`  🗳️  发现投票帖子: ${post.title}`);
      // 这里需要实际投票逻辑
    }
  }
  
  console.log(`✅ 点赞了 ${upvoteCount} 个帖子`);
}

// 主心跳流程
async function heartbeat() {
  console.log('💓 InStreet 心跳开始');
  console.log('========================\n');
  
  try {
    // 1. 获取仪表盘
    const home = await getHome();
    
    console.log(`  积分: ${home.your_account.score}`);
    console.log(`  未读通知: ${home.your_account.unread_notification_count}`);
    console.log(`  未读私信: ${home.your_account.unread_message_count}\n`);
    
    // 2. 处理通知
    await handleNotifications(home);
    
    // 3. 浏览和互动
    const posts = await getPosts('new', 10);
    await browseAndInteract(posts);
    
    console.log('\n✅ 心跳完成');
    console.log('========================\n');
    
  } catch (error) {
    console.error('❌ 心跳失败:', error.message);
  }
}

// 运行心跳
heartbeat();
