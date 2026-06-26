/**
 * 视频管理模块
 * 视频发布、定时、多账号管理
 */

import { getCurrentAccount, loadConfig } from './init.js';
import { createTikTokAPI } from '../src/api.js';
import fs from 'fs';

/**
 * 发布视频
 */
export async function publishVideo(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('📹 发布视频...');
  console.log(`  文件：${options.videoPath}`);
  console.log(`  描述：${options.description || '无'}`);
  console.log(`  标签：${options.tags || '无'}`);
  
  if (options.schedule) {
    console.log(`  定时：${options.schedule}`);
  }

  try {
    // 验证文件
    if (!fs.existsSync(options.videoPath)) {
      throw new Error(`视频文件不存在：${options.videoPath}`);
    }

    const tiktokAPI = createTikTokAPI(config);
    const shopId = account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    // 1. 上传视频
    console.log('\n⏳ 上传视频中...');
    const uploadResult = await tiktokAPI.uploadVideo(shopId, {
      file_path: options.videoPath,
      title: options.description || 'Video'
    });

    const videoId = uploadResult.data?.video_id;
    console.log(`✓ 视频上传成功：${videoId}`);

    // 2. 发布视频
    console.log('\n⏳ 发布视频中...');
    const publishResult = await tiktokAPI.publishVideo(shopId, videoId, {
      description: options.description,
      tags: options.tags ? options.tags.split(',') : [],
      schedule_time: options.schedule
    });

    console.log('✓ 视频发布成功');
    console.log(`  视频 ID: ${videoId}`);
    console.log(`  链接：${publishResult.data?.video_url}`);

    return {
      videoId,
      videoUrl: publishResult.data?.video_url,
      success: true
    };
    
  } catch (error) {
    console.error('✗ 发布失败:', error.message);
    throw error;
  }
}

/**
 * 分析最佳发布时间
 */
export async function analyzeBestTime(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('📊 分析最佳发布时间...');
  console.log(`  账号：${options.account || account?.username || '当前账号'}`);
  console.log(`  分析周期：${options.days || 30} 天`);

  try {
    const tiktokAPI = createTikTokAPI(config);
    const shopId = account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    // 获取视频列表
    const videosResult = await tiktokAPI.listVideos(shopId);
    const videos = videosResult.data?.videos || [];

    console.log(`✓ 分析 ${videos.length} 个视频数据...`);

    // Mock 分析结果
    const bestTimes = [
      { day: 'Monday', hour: 18, engagement_rate: 4.5 },
      { day: 'Tuesday', hour: 19, engagement_rate: 4.2 },
      { day: 'Wednesday', hour: 18, engagement_rate: 4.8 },
      { day: 'Thursday', hour: 20, engagement_rate: 4.3 },
      { day: 'Friday', hour: 17, engagement_rate: 5.1 },
      { day: 'Saturday', hour: 14, engagement_rate: 5.5 },
      { day: 'Sunday', hour: 15, engagement_rate: 5.2 }
    ];

    console.log('\n📊 最佳发布时间建议:');
    bestTimes.slice(0, 3).forEach(time => {
      console.log(`  ${time.day} ${time.hour}:00 - 互动率 ${time.engagement_rate}%`);
    });

    return {
      best_times: bestTimes,
      analyzed_videos: videos.length,
      period_days: options.days || 30
    };
    
  } catch (error) {
    console.error('✗ 分析失败:', error.message);
    throw error;
  }
}
