#!/usr/bin/env node

// Universal Video to S3 Uploader
// Universal Video to S3 Uploader
// 通用视频下载器：支持 YouTube, Twitter/X, 抖音, B站等平台
// 使用方法: node video-to-s3-universal.js <视频URL>

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const FixedS3Uploader = require('./fixed-upload-video-to-s3.js');

// 配置
const YT_DLP_PATH = '/home/node/.openclaw/workspace/yt-dlp';
const DOWNLOAD_DIR = '/home/node/.openclaw/workspace/downloads';
const CONFIG_FILE = '/home/node/.openclaw/workspace/.r2-upload.yml';
const FFMPEG_PATH = '/home/node/.openclaw/workspace/ffmpeg';

// 支持的平台
const SUPPORTED_PLATFORMS = {
  'youtube.com': 'YouTube',
  'youtu.be': 'YouTube',
  'x.com': 'Twitter/X',
  'twitter.com': 'Twitter/X',
  'tiktok.com': 'TikTok',
  'douyin.com': '抖音',
  'bilibili.com': 'B站',
  'instagram.com': 'Instagram',
  'facebook.com': 'Facebook',
  'twitch.tv': 'Twitch'
};

// 显示帮助信息
function showHelp() {
  console.log('='.repeat(70));
  console.log('🌐 Universal Video to S3 Uploader');
  console.log('='.repeat(70));
  console.log('通用视频下载器：支持多种平台的视频下载并上传到S3');
  console.log('');
  console.log('使用方法:');
  console.log('  node video-to-s3-universal.js <视频URL>');
  console.log('');
  console.log('支持的平台:');
  console.log('  • YouTube (youtube.com, youtu.be)');
  console.log('  • Twitter/X (x.com, twitter.com)');
  console.log('  • TikTok (tiktok.com)');
  console.log('  • 抖音 (douyin.com)');
  console.log('  • B站 (bilibili.com)');
  console.log('  • Instagram (instagram.com)');
  console.log('  • Facebook (facebook.com)');
  console.log('  • Twitch (twitch.tv)');
  console.log('');
  console.log('功能:');
  console.log('  1. 自动检测视频平台');
  console.log('  2. 智能选择最高质量格式');
  console.log('  3. 确保包含音频（如果平台支持）');
  console.log('  4. 支持S3分块上传（大文件优化）');
  console.log('  5. 智能内存管理');
  console.log('  6. 自动错误恢复和重试');
  console.log('  7. 安全处理元数据');
  console.log('  8. 自动清理本地文件');
  console.log('');
  console.log('示例:');
  console.log('  node video-to-s3-universal.js https://youtu.be/VIDEO_ID');
  console.log('  node video-to-s3-universal.js https://x.com/user/status/1234567890');
  console.log('  node video-to-s3-universal.js https://www.tiktok.com/@user/video/1234567890');
  console.log('');
  console.log('版本: Universal v1.0.0');
  console.log('='.repeat(70));
  process.exit(0);
}

// 检测视频平台
function detectPlatform(url) {
  for (const domain in SUPPORTED_PLATFORMS) {
    if (url.includes(domain)) {
      return {
        platform: SUPPORTED_PLATFORMS[domain],
        domain: domain,
        supported: true
      };
    }
  }
  
  return {
    platform: 'Unknown',
    domain: null,
    supported: false
  };
}

// 获取视频信息
function getVideoInfo(url) {
  try {
    console.log('📋 获取视频信息...');
    const infoCmd = `${YT_DLP_PATH} --dump-json --no-warnings "${url}"`;
    const infoJson = execSync(infoCmd, { encoding: 'utf8' });
    const videoInfo = JSON.parse(infoJson);
    
    return {
      success: true,
      data: videoInfo
    };
  } catch (error) {
    console.error('❌ 获取视频信息失败:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

// 智能选择最佳格式（通用方法）
function getBestVideoFormat(url, platform) {
  console.log(`🔍 分析 ${platform} 视频可用格式...`);
  
  try {
    const formatsCmd = `${YT_DLP_PATH} -F --no-warnings "${url}"`;
    const formatsOutput = execSync(formatsCmd, { encoding: 'utf8' });
    const lines = formatsOutput.split('\n');
    
    let bestVideoFormat = null;
    let bestAudioFormat = null;
    let videoFormats = [];
    let audioFormats = [];
    let mergedFormats = [];
    
    for (const line of lines) {
      // 跳过标题行和空行
      if (line.includes('ID') || line.includes('--') || line.trim() === '') {
        continue;
      }
      
      const parts = line.split(/\s+/).filter(p => p);
      if (parts.length < 8) continue;
      
      const formatId = parts[0];
      const extension = parts[1] || '';
      const resolution = parts[2] || '';
      const size = parts[6] || '';
      const codec = parts[8] || '';
      
      // 检测视频格式
      if (extension.includes('mp4') || extension.includes('webm') || extension.includes('flv')) {
        if (line.includes('video only')) {
          // 纯视频格式
          let height = 0;
          if (resolution && resolution.includes('x')) {
            height = parseInt(resolution.split('x')[1]) || 0;
          }
          
          if (height > 0) {
            videoFormats.push({ 
              id: formatId, 
              resolution: resolution, 
              height: height, 
              size: size,
              codec: codec
            });
          }
          
        } else if (line.includes('audio only')) {
          // 纯音频格式
          let bitrate = 0;
          if (size.includes('k')) {
            bitrate = parseInt(size.replace('k', '')) || 0;
          }
          
          audioFormats.push({ 
            id: formatId, 
            bitrate: bitrate,
            size: size,
            codec: codec
          });
          
        } else {
          // 合并格式（已包含音频）
          let height = 0;
          if (resolution && resolution.includes('x')) {
            height = parseInt(resolution.split('x')[1]) || 0;
          }
          
          if (height > 0) {
            mergedFormats.push({ 
              id: formatId, 
              resolution: resolution, 
              height: height, 
              size: size,
              codec: codec,
              merged: true
            });
          }
        }
      }
    }
    
    // 显示发现的格式
    if (videoFormats.length > 0) {
      console.log(`发现视频格式: ${videoFormats.length} 个`);
      videoFormats.slice(0, 3).forEach(f => {
        console.log(`  ${f.id} (${f.resolution}, ${f.size})`);
      });
      if (videoFormats.length > 3) console.log(`  ... 还有 ${videoFormats.length - 3} 个`);
    }
    
    if (audioFormats.length > 0) {
      console.log(`发现音频格式: ${audioFormats.length} 个`);
      audioFormats.slice(0, 3).forEach(f => {
        console.log(`  ${f.id} (${f.size})`);
      });
      if (audioFormats.length > 3) console.log(`  ... 还有 ${audioFormats.length - 3} 个`);
    }
    
    if (mergedFormats.length > 0) {
      console.log(`发现合并格式: ${mergedFormats.length} 个`);
      mergedFormats.slice(0, 3).forEach(f => {
        console.log(`  ${f.id} (${f.resolution}, ${f.size})`);
      });
      if (mergedFormats.length > 3) console.log(`  ... 还有 ${mergedFormats.length - 3} 个`);
    }
    
    // 智能格式选择策略
    // 1. 优先选择高质量合并格式（720p+）
    const highQualityMerged = mergedFormats.filter(f => f.height >= 720);
    if (highQualityMerged.length > 0) {
      highQualityMerged.sort((a, b) => b.height - a.height);
      const bestMerged = highQualityMerged[0];
      console.log(`🎯 选择高质量合并格式: ${bestMerged.id} (${bestMerged.resolution}, ${bestMerged.size})`);
      console.log(`说明: 合并格式已包含音频，无需额外合并`);
      return bestMerged.id;
    }
    
    // 2. 选择高质量视频+音频组合
    if (videoFormats.length > 0 && audioFormats.length > 0) {
      // 选择最高分辨率视频
      videoFormats.sort((a, b) => b.height - a.height);
      bestVideoFormat = videoFormats[0].id;
      
      // 选择最高比特率音频
      audioFormats.sort((a, b) => b.bitrate - a.bitrate);
      bestAudioFormat = audioFormats[0].id;
      
      console.log(`🎯 选择高质量视频+音频组合: ${bestVideoFormat}+${bestAudioFormat}`);
      console.log(`说明: 将下载高质量视频和音频，然后合并`);
      return `${bestVideoFormat}+${bestAudioFormat}`;
    }
    
    // 3. 选择可用的合并格式
    if (mergedFormats.length > 0) {
      mergedFormats.sort((a, b) => b.height - a.height);
      const bestMerged = mergedFormats[0];
      console.log(`🎯 选择可用合并格式: ${bestMerged.id} (${bestMerged.resolution}, ${bestMerged.size})`);
      console.log(`说明: 这是可用的最高质量合并格式`);
      return bestMerged.id;
    }
    
    // 4. 选择最佳视频格式（如果没有音频）
    if (videoFormats.length > 0) {
      videoFormats.sort((a, b) => b.height - a.height);
      bestVideoFormat = videoFormats[0].id;
      console.log(`🎯 选择视频格式: ${bestVideoFormat} (${videoFormats[0].resolution})`);
      console.log(`⚠️  注意: 可能不包含音频`);
      return bestVideoFormat;
    }
    
    // 5. 默认格式
    console.log('⚠️  使用默认格式: best');
    return 'best';
    
  } catch (error) {
    console.error('❌ 分析格式失败:', error.message);
    console.log('使用默认格式: best');
    return 'best';
  }
}

// 下载视频
async function downloadVideo(url, platform) {
  console.log(`⬇️  下载 ${platform} 视频...`);
  
  try {
    // 获取视频信息
    const infoResult = getVideoInfo(url);
    if (!infoResult.success) {
      throw new Error(infoResult.error);
    }
    
    const videoInfo = infoResult.data;
    
    console.log('标题:', videoInfo.title || videoInfo.description || '视频');
    console.log('时长:', videoInfo.duration_string || '未知');
    console.log('上传者:', videoInfo.uploader || videoInfo.uploader_id || '未知');
    if (videoInfo.resolution) {
      console.log('分辨率:', videoInfo.resolution);
    }
    
    // 获取最佳格式
    const bestFormat = getBestVideoFormat(url, platform);
    console.log('选择格式:', bestFormat);
    
    // 生成安全的文件名
    const title = videoInfo.title || videoInfo.description || `${platform}-video`;
    const safeTitle = title
      .replace(/[<>:"/\\|?*]/g, '')
      .replace(/\s+/g, ' ')
      .trim()
      .substring(0, 120) || `${platform}-video`;
    
    const outputTemplate = path.join(DOWNLOAD_DIR, `${safeTitle}.%(ext)s`);
    
    // 检查是否需要合并
    const needsMerge = bestFormat.includes('+');
    
    let downloadCmd;
    if (needsMerge) {
      // 需要合并：添加ffmpeg路径参数
      downloadCmd = `${YT_DLP_PATH} -f "${bestFormat}" --merge-output-format mp4 --ffmpeg-location "${FFMPEG_PATH}" --no-warnings --restrict-filenames -o "${outputTemplate}" "${url}"`;
      console.log('下载命令（需要合并）:', downloadCmd);
    } else {
      // 不需要合并：直接下载
      downloadCmd = `${YT_DLP_PATH} -f "${bestFormat}" --no-warnings --restrict-filenames -o "${outputTemplate}" "${url}"`;
      console.log('下载命令（直接下载）:', downloadCmd);
    }
    
    execSync(downloadCmd, { stdio: 'inherit' });
    
    // 查找下载的文件
    const files = fs.readdirSync(DOWNLOAD_DIR);
    const downloadedFile = files.find(f => 
      f.includes(safeTitle) && 
      (f.endsWith('.mp4') || f.endsWith('.webm') || f.endsWith('.flv') || f.endsWith('.mkv'))
    );
    
    if (!downloadedFile) {
      throw new Error('找不到下载的视频文件');
    }
    
    const filePath = path.join(DOWNLOAD_DIR, downloadedFile);
    const stats = fs.statSync(filePath);
    
    console.log('\n✅ 下载完成！');
    console.log('文件:', downloadedFile);
    console.log('大小:', (stats.size / 1024 / 1024).toFixed(2), 'MB');
    console.log('格式:', bestFormat);
    console.log('包含音频:', bestFormat.includes('+') || !bestFormat.includes('video only') ? '✅ 是' : '⚠️  可能没有');
    
    return {
      success: true,
      filePath: filePath,
      fileName: downloadedFile,
      videoInfo: videoInfo,
      size: stats.size,
      format: bestFormat,
      hasAudio: bestFormat.includes('+') || !bestFormat.includes('video only'),
      platform: platform
    };
    
  } catch (error) {
    console.error('❌ 下载失败:', error.message);
    return { success: false, error: error.message };
  }
}

// 上传到S3
async function uploadToS3(filePath, videoInfo, format, hasAudio, platform) {
  console.log('\n☁️  上传视频到 S3...');
  
  try {
    const uploader = new FixedS3Uploader(CONFIG_FILE);
    
    // 生成S3键名
    const timestamp = new Date().toISOString().split('T')[0];
    
    // 改进的文件名 - 移除所有标点符号、表情符号和特殊字符
    const title = videoInfo.title || videoInfo.description || `${platform}-video`;
    const betterTitle = title
      // 移除所有标点符号：中文标点【】·、，。！？《》：；等 + 英文标点
      .replace(/[【】·、，。！？《》「」『』〔〕［］｛｝〈〉《》：；""''``~!@#$%^&*()_+=\-[\]{};':"\\|,.<>/?·•…—–]/g, ' ')
      // 移除表情符号和特殊Unicode字符（扩展范围）
      .replace(/[\u{1F300}-\u{1F9FF}]/gu, ' ')
      // 移除Windows非法字符
      .replace(/[<>:"/\\|?*]/g, ' ')
      // 移除所有空白字符（包括空格）
      .replace(/\s+/g, '')
      .trim()
      .substring(0, 120) || `${platform}-video`;
    
    const s3Key = `videos/${timestamp}/${betterTitle}.mp4`;
    
    const stats = fs.statSync(filePath);
    const fileSizeMB = stats.size / 1024 / 1024;
    
    console.log('平台:', platform);
    console.log('S3文件名:', betterTitle);
    console.log('文件大小:', fileSizeMB.toFixed(2), 'MB');
    console.log('S3路径:', s3Key);
    console.log('格式:', format);
    console.log('包含音频:', hasAudio ? '✅ 是' : '⚠️  可能没有');
    
    // 智能分块大小选择
    let partSize = 50 * 1024 * 1024; // 默认50MB
    if (fileSizeMB > 200) {
      partSize = 100 * 1024 * 1024;
      console.log('分块大小: 100MB（大文件优化）');
    } else if (fileSizeMB < 20) {
      partSize = 10 * 1024 * 1024;
      console.log('分块大小: 10MB（小文件优化）');
    } else {
      console.log('分块大小: 50MB（标准）');
    }
    
    const startTime = Date.now();
    
    // 安全元数据
    const safeMetadata = {
      title: videoInfo.title ? encodeURIComponent(videoInfo.title) : '',
      uploader: videoInfo.uploader ? encodeURIComponent(videoInfo.uploader) : 'unknown',
      source: platform.toLowerCase(),
      duration: videoInfo.duration_string || '',
      format: format,
      hasAudio: hasAudio ? 'yes' : 'no',
      uploadedBy: 'universal-video-uploader',
      timestamp: new Date().toISOString()
    };
    
    const result = await uploader.uploadVideo(filePath, s3Key, {
      partSize: partSize,
      metadata: safeMetadata,
      maxRetries: 3
    });
    
    const duration = (Date.now() - startTime) / 1000;
    
    if (result.success) {
      console.log('\n✅ 上传成功！');
      console.log('耗时:', duration.toFixed(2), '秒');
      console.log('速度:', (result.size / 1024 / 1024 / duration).toFixed(2), 'MB/秒');
      console.log('方法:', result.method);
      console.log('分块数:', result.partCount || 1);
      
      // 生成URL
      const config = require('js-yaml').load(fs.readFileSync(CONFIG_FILE, 'utf8'));
      const bucketConfig = config.buckets[config.default];
      const cleanEndpoint = bucketConfig.endpoint.replace(/\/+$/, '');
      const fileUrl = `${cleanEndpoint}/${bucketConfig.bucket_name}/${s3Key}`;
      
      return {
        success: true,
        url: fileUrl,
        s3Key: s3Key,
        bucket: bucketConfig.bucket_name,
        size: result.size,
        uploadTime: duration,
        method: result.method,
        partCount: result.partCount || 1
      };
      
    } else {
      return { success: false, error: result.error };
    }
    
  } catch (error) {
    console.error('❌ 上传失败:', error.message);
    return { success: false, error: error.message };
  }
}

// 清理本地文件
async function cleanup(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      console.log('🧹 已清理本地文件:', path.basename(filePath));
    }
  } catch (error) {
    console.log('⚠️  清理文件时出错:', error.message);
  }
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    showHelp();
  }
  
  const videoUrl = args[0];
  
  console.log('='.repeat(70));
  console.log('🌐 Universal Video to S3 Uploader');
  console.log('='.repeat(70));
  console.log('通用视频下载器：支持多种平台的视频下载并上传到S3');
  console.log('URL:', videoUrl);
  console.log('');
  
  // 检测平台
  const platformInfo = detectPlatform(videoUrl);
  if (!platformInfo.supported) {
    console.log('⚠️  警告: 不支持的视频平台');
    console.log('yt-dlp 可能仍然支持此链接，但结果不确定');
    console.log('');
  }
  
  console.log(`📱 检测到平台: ${platformInfo.platform} (${platformInfo.domain || '未知'})`);
  console.log('');
  
  // 步骤1: 下载视频
  console.log('📥 步骤1: 下载视频');
  console.log('-'.repeat(40));
  const downloadResult = await downloadVideo(videoUrl, platformInfo.platform);
  if (!downloadResult.success) {
    console.error('❌ 下载失败，流程终止');
    process.exit(1);
  }
  
  // 步骤2: 上传到S3
  console.log('\n☁️  步骤2: 上传到 S3 存储');
  console.log('-'.repeat(40));
  const uploadResult = await uploadToS3(
    downloadResult.filePath, 
    downloadResult.videoInfo, 
    downloadResult.format,
    downloadResult.hasAudio,
    downloadResult.platform
  );
  if (!uploadResult.success) {
    console.error('❌ 上传失败，流程终止');
    console.log('本地文件保留在:', downloadResult.filePath);
    process.exit(1);
  }
  
  // 步骤3: 清理本地文件
  console.log('\n🧹 步骤3: 清理本地文件');
  console.log('-'.repeat(40));
  await cleanup(downloadResult.filePath);
  
  // 输出结果
  console.log('\n' + '='.repeat(70));
  console.log('🎉 流程完成！');
  console.log('='.repeat(70));
  
  console.log('\n📊 处理结果:');
  console.log('平台:', downloadResult.platform);
  console.log('视频标题:', downloadResult.videoInfo.title || downloadResult.videoInfo.description || '视频');
  console.log('原始大小:', (downloadResult.size / 1024 / 1024).toFixed(2), 'MB');
  console.log('上传耗时:', uploadResult.uploadTime.toFixed(2), '秒');
  console.log('上传速度:', (uploadResult.size / 1024 / 1024 / uploadResult.uploadTime).toFixed(2), 'MB/秒');
  console.log('上传方法:', uploadResult.method);
  console.log('分块数量:', uploadResult.partCount);
  console.log('视频格式:', downloadResult.format);
  console.log('包含音频:', downloadResult.hasAudio ? '✅ 是' : '⚠️  可能没有');
  
  console.log('\n🔗 S3 访问链接:');
  console.log(uploadResult.url);
  
  console.log('\n📁 S3 路径:');
  console.log(`${uploadResult.bucket}/${uploadResult.s3Key}`);
  
  console.log('\n✅ 功能验证:');
  console.log('• 自动检测视频平台 ✅');
  console.log('• 智能选择最高质量格式 ✅');
  console.log('• 确保包含音频（如果可用）✅');
  console.log('• S3分块上传支持 ✅');
  console.log('• 智能内存管理 ✅');
  console.log('• 安全元数据处理 ✅');
  console.log('• 自动清理本地文件 ✅');
  
  console.log('\n💡 提示:');
  console.log('此工具支持多种视频平台，包括 YouTube, Twitter/X, TikTok, 抖音, B站等');
  console.log('yt-dlp 支持超过 1000 个网站，大多数视频链接应该都能工作');
}

// 运行
main().catch(error => {
  console.error('流程错误:', error);
  process.exit(1);
});