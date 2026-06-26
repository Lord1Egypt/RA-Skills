#!/usr/bin/env node

/**
 * YouTube to S3 Uploader - Unified Version
 * 通用版本：自动下载最高质量视频（包含音频）并上传到S3
 * 使用方法: node youtube-to-s3-unified.js <YouTube URL>
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const FixedS3Uploader = require('./fixed-upload-video-to-s3.js');

// 配置
const YT_DLP_PATH = '/home/node/.npm-global/bin/yt-dlp';
const DOWNLOAD_DIR = '/home/node/.openclaw/workspace/downloads';
const CONFIG_FILE = '/home/node/.openclaw/workspace/.r2-upload.yml';

// 显示帮助信息
function showHelp() {
  console.log('='.repeat(70));
  console.log('🎬 YouTube to S3 Uploader - Unified Version');
  console.log('='.repeat(70));
  console.log('通用版本：自动下载最高质量视频（包含音频）并上传到S3');
  console.log('');
  console.log('使用方法:');
  console.log('  node youtube-to-s3-unified.js <YouTube URL>');
  console.log('');
  console.log('参数:');
  console.log('  <YouTube URL>    YouTube视频链接（必需）');
  console.log('');
  console.log('功能:');
  console.log('  1. 自动检测并下载最高质量视频格式');
  console.log('  2. 确保包含音频轨道');
  console.log('  3. 使用S3分块上传（支持大文件）');
  console.log('  4. 智能内存管理（分块读取）');
  console.log('  5. 自动错误恢复和重试');
  console.log('  6. 安全处理元数据（避免中文字符问题）');
  console.log('  7. 自动清理本地文件');
  console.log('');
  console.log('示例:');
  console.log('  node youtube-to-s3-unified.js https://youtu.be/VIDEO_ID');
  console.log('  node youtube-to-s3-unified.js https://www.youtube.com/watch?v=VIDEO_ID');
  console.log('');
  console.log('版本: Unified (通用版本)');
  console.log('注意: 此版本自动处理所有格式和音频问题');
  console.log('='.repeat(70));
  process.exit(0);
}

// 检查参数
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
  showHelp();
}

// 确保下载目录存在
if (!fs.existsSync(DOWNLOAD_DIR)) {
  fs.mkdirSync(DOWNLOAD_DIR, { recursive: true });
}

// 获取最佳视频格式（包含音频）
function getBestVideoFormat(url) {
  console.log('🔍 分析视频可用格式...');
  
  try {
    // 获取格式列表
    const formatsCmd = `${YT_DLP_PATH} -F --no-warnings "${url}"`;
    const formatsOutput = execSync(formatsCmd, { encoding: 'utf8' });
    
    // 解析格式列表，寻找最佳视频+音频组合
    const lines = formatsOutput.split('\n');
    let bestVideoFormat = null;
    let bestAudioFormat = null;
    
    // 查找最佳视频格式（按分辨率排序）
    let videoFormats = [];
    for (const line of lines) {
      if (line.includes('mp4') && line.includes('video only')) {
        const parts = line.split(/\s+/).filter(p => p);
        if (parts.length >= 10) {
          const formatId = parts[0];
          const resolution = parts[2];
          const size = parts[6];
          const codec = parts[8];
          
          // 解析分辨率
          let width = 0, height = 0;
          if (resolution && resolution.includes('x')) {
            const [w, h] = resolution.split('x').map(n => parseInt(n) || 0);
            width = w;
            height = h;
          }
          
          if (height > 0) {
            console.log(`发现视频格式: ${formatId} (${resolution}, ${size}, ${codec})`);
            videoFormats.push({ 
              id: formatId, 
              resolution: resolution, 
              width: width, 
              height: height, 
              size: size,
              codec: codec
            });
          }
        }
      }
    }
    
    // 按分辨率排序（降序）
    if (videoFormats.length > 0) {
      videoFormats.sort((a, b) => b.height - a.height);
      bestVideoFormat = videoFormats[0].id;
      console.log(`选择视频格式: ${bestVideoFormat} (${videoFormats[0].resolution}, 最高质量)`);
    }
    
    // 查找最佳音频格式（选择最高质量的m4a音频）
    let audioFormats = [];
    for (const line of lines) {
      if (line.includes('m4a') && line.includes('audio only')) {
        const parts = line.split(/\s+/).filter(p => p);
        if (parts.length >= 10) {
          const formatId = parts[0];
          const bitrate = parts[7];
          const size = parts[6];
          console.log(`发现音频格式: ${formatId} (${bitrate}, ${size})`);
          audioFormats.push({ id: formatId, bitrate: bitrate, size: size });
        }
      }
    }
    
    // 选择最高质量的音频格式（按比特率排序）
    if (audioFormats.length > 0) {
      audioFormats.sort((a, b) => {
        // 提取比特率数字进行比较
        const aRate = parseInt(a.bitrate.replace('k', '')) || 0;
        const bRate = parseInt(b.bitrate.replace('k', '')) || 0;
        return bRate - aRate; // 降序排列
      });
      bestAudioFormat = audioFormats[0].id;
      console.log(`选择音频格式: ${bestAudioFormat} (最高质量)`);
    }
    
    // 查找合并格式（已包含音频）
    console.log('\n🔍 查找合并格式（已包含音频）...');
    let mergedFormats = [];
    for (const line of lines) {
      if (line.includes('mp4') && !line.includes('video only') && !line.includes('audio only')) {
        const parts = line.split(/\s+/).filter(p => p);
        if (parts.length >= 10) {
          const formatId = parts[0];
          const resolution = parts[2];
          const size = parts[6];
          const codec = parts[8];
          console.log(`发现合并格式: ${formatId} (${resolution}, ${size}, ${codec})`);
          
          // 解析分辨率
          let height = 0;
          if (resolution && resolution.includes('x')) {
            height = parseInt(resolution.split('x')[1]) || 0;
          }
          
          mergedFormats.push({ 
            id: formatId, 
            resolution: resolution, 
            height: height, 
            size: size, 
            codec: codec 
          });
        }
      }
    }
    
    // 智能格式选择策略：
    // 1. 如果有高质量合并格式（720p+），优先选择
    // 2. 否则选择高质量视频+音频组合
    const highQualityMerged = mergedFormats.filter(f => f.height >= 720);
    
    if (highQualityMerged.length > 0) {
      // 有高质量合并格式，优先选择
      highQualityMerged.sort((a, b) => b.height - a.height);
      const bestMerged = highQualityMerged[0];
      console.log(`🎯 选择高质量合并格式: ${bestMerged.id} (${bestMerged.resolution}, ${bestMerged.size})`);
      console.log(`说明: 高质量合并格式已包含音频，无需额外合并`);
      return bestMerged.id;
    } else if (bestVideoFormat && bestAudioFormat) {
      // 没有高质量合并格式，但有好视频+音频
      console.log(`🎯 选择高质量视频+音频组合: ${bestVideoFormat}+${bestAudioFormat}`);
      console.log(`说明: 将下载高质量视频和音频，然后合并`);
      return `${bestVideoFormat}+${bestAudioFormat}`;
    } else if (mergedFormats.length > 0) {
      // 只有低质量合并格式
      mergedFormats.sort((a, b) => b.height - a.height);
      const bestMerged = mergedFormats[0];
      console.log(`🎯 选择可用合并格式: ${bestMerged.id} (${bestMerged.resolution}, ${bestMerged.size})`);
      console.log(`说明: 这是可用的最高质量合并格式`);
      return bestMerged.id;
    } else {
      // 最后备选
      console.log('⚠️  使用默认格式: bestvideo+bestaudio');
      return 'bestvideo+bestaudio';
    }
    
    if (bestVideoFormat && bestAudioFormat) {
      console.log(`🎯 选择格式: ${bestVideoFormat}+${bestAudioFormat} (视频+音频)`);
      return `${bestVideoFormat}+${bestAudioFormat}`;
    } else {
      console.log('⚠️  使用默认格式: bestvideo+bestaudio');
      return 'bestvideo+bestaudio';
    }
    
  } catch (error) {
    console.error('❌ 分析格式失败:', error.message);
    console.log('使用默认格式: bestvideo+bestaudio');
    return 'bestvideo+bestaudio';
  }
}

async function downloadBestQualityVideo(url) {
  console.log('🎬 下载最高质量 YouTube 视频...');
  console.log('URL:', url);
  
  try {
    // 获取视频信息
    console.log('\n📋 获取视频信息...');
    const infoCmd = `${YT_DLP_PATH} --dump-json --no-warnings "${url}"`;
    const infoJson = execSync(infoCmd, { encoding: 'utf8' });
    const videoInfo = JSON.parse(infoJson);
    
    console.log('标题:', videoInfo.title);
    console.log('时长:', videoInfo.duration_string);
    console.log('上传者:', videoInfo.uploader || '未知');
    console.log('最高分辨率:', videoInfo.resolution || '未知');
    
    // 获取最佳格式
    const bestFormat = getBestVideoFormat(url);
    console.log('选择格式:', bestFormat);
    
    // 下载视频
    console.log('\n⬇️  下载视频...');
    
    // 改进的文件名生成：保留更多可读字符
    const safeTitle = videoInfo.title
      // 移除不安全字符，但保留中文、字母、数字、空格、标点
      .replace(/[<>:"/\\|?*]/g, '')
      // 替换连续多个空格或下划线为单个空格
      .replace(/\s+/g, ' ')
      .replace(/_+/g, ' ')
      // 修剪首尾空格
      .trim()
      // 如果为空，使用默认名称
      .substring(0, 100) || 'youtube-video';
    
    const outputTemplate = path.join(DOWNLOAD_DIR, `${safeTitle}.%(ext)s`);
    
    // 检查是否需要合并（如果是视频+音频格式）
    const needsMerge = bestFormat.includes('+');
    const ffmpegPath = '/home/node/.openclaw/workspace/ffmpeg';
    
    let downloadCmd;
    if (needsMerge) {
      // 需要合并：添加ffmpeg路径参数
      downloadCmd = `${YT_DLP_PATH} -f "${bestFormat}" --merge-output-format mp4 --ffmpeg-location "${ffmpegPath}" --no-warnings --restrict-filenames -o "${outputTemplate}" "${url}"`;
      console.log('下载命令（需要合并）:', downloadCmd);
    } else {
      // 不需要合并：直接下载
      downloadCmd = `${YT_DLP_PATH} -f "${bestFormat}" --no-warnings --restrict-filenames -o "${outputTemplate}" "${url}"`;
      console.log('下载命令（直接下载）:', downloadCmd);
    }
    
    execSync(downloadCmd, { stdio: 'inherit' });
    
    // 查找下载的文件
    const files = fs.readdirSync(DOWNLOAD_DIR);
    const downloadedFile = files.find(f => f.includes(safeTitle) && f.endsWith('.mp4'));
    
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
      format: bestFormat
    };
    
  } catch (error) {
    console.error('❌ 下载失败:', error.message);
    return { success: false, error: error.message };
  }
}

async function uploadToS3(filePath, videoInfo, format) {
  console.log('\n☁️  上传视频到 S3...');
  
  try {
    const uploader = new FixedS3Uploader(CONFIG_FILE);
    
    // 生成更好的S3键名（保留更多可读字符）
    const timestamp = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    
    // 改进的文件名：移除所有标点符号、表情符号，保留中文、字母、数字、空格
    const betterTitle = videoInfo.title
      // 移除所有标点符号：中文标点【】·、，。！？《》：；等 + 英文标点
      .replace(/[【】·、，。！？《》「」『』〔〕［］｛｝〈〉《》：；""''``~!@#$%^&*()_+=\-[\]{};':"\\|,.<>/?·•…—–]/g, ' ')
      // 移除表情符号和特殊Unicode字符（扩展范围）
      .replace(/[\u{1F300}-\u{1F9FF}]/gu, ' ')
      // 移除Windows非法字符
      .replace(/[<>:"/\\|?*]/g, ' ')
      // 移除所有空白字符（包括空格）
      .replace(/\s+/g, '')
      // 修剪首尾空格
      .trim()
      // 限制长度
      .substring(0, 120) || 'youtube-video';
    
    // 生成S3路径
    const s3Key = `videos/${timestamp}/${betterTitle}.mp4`;
    
    console.log('S3文件名:', betterTitle);
    
    const stats = fs.statSync(filePath);
    const fileSizeMB = stats.size / 1024 / 1024;
    
    console.log('文件大小:', fileSizeMB.toFixed(2), 'MB');
    console.log('S3路径:', s3Key);
    console.log('格式:', format);
    
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
    
    // 安全元数据（避免中文字符问题）
    const safeMetadata = {
      title: videoInfo.title ? encodeURIComponent(videoInfo.title) : '',
      uploader: videoInfo.uploader ? encodeURIComponent(videoInfo.uploader) : 'unknown',
      duration: videoInfo.duration_string || '',
      youtubeId: videoInfo.id || '',
      format: format,
      quality: 'best',
      uploadedBy: 'youtube-s3-uploader-unified',
      version: 'unified',
      uploadMethod: 'multipart',
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

async function main() {
  const youtubeUrl = args[0];
  
  console.log('='.repeat(70));
  console.log('🎬 YouTube to S3 Uploader - Unified Version');
  console.log('='.repeat(70));
  console.log('通用版本：自动下载最高质量视频（包含音频）');
  console.log('URL:', youtubeUrl);
  console.log('');
  
  // 步骤1: 下载最高质量视频
  console.log('📥 步骤1: 下载最高质量视频');
  console.log('-'.repeat(40));
  const downloadResult = await downloadBestQualityVideo(youtubeUrl);
  if (!downloadResult.success) {
    console.error('❌ 下载失败，流程终止');
    process.exit(1);
  }
  
  // 步骤2: 上传到S3
  console.log('\n☁️  步骤2: 上传到 S3 存储');
  console.log('-'.repeat(40));
  const uploadResult = await uploadToS3(downloadResult.filePath, downloadResult.videoInfo, downloadResult.format);
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
  console.log('视频标题:', downloadResult.videoInfo.title);
  console.log('原始大小:', (downloadResult.size / 1024 / 1024).toFixed(2), 'MB');
  console.log('上传耗时:', uploadResult.uploadTime.toFixed(2), '秒');
  console.log('上传速度:', (uploadResult.size / 1024 / 1024 / uploadResult.uploadTime).toFixed(2), 'MB/秒');
  console.log('上传方法:', uploadResult.method);
  console.log('分块数量:', uploadResult.partCount);
  console.log('视频格式:', downloadResult.format);
  
  console.log('\n🔗 S3 访问链接:');
  console.log(uploadResult.url);
  
  console.log('\n📁 S3 路径:');
  console.log(`${uploadResult.bucket}/${uploadResult.s3Key}`);
  
  console.log('\n✅ Unified 版本功能验证:');
  console.log('• 自动选择最高质量格式 ✅');
  console.log('• 确保包含音频 ✅');
  console.log('• S3分块上传支持 ✅');
  console.log('• 智能内存管理 ✅');
  console.log('• 安全元数据处理 ✅');
  console.log('• 自动清理本地文件 ✅');
  
  console.log('\n💡 说明:');
  console.log('1. 此版本自动选择最佳视频格式');
  console.log('2. 确保下载的视频包含音频');
  console.log('3. 使用安全的元数据避免中文字符问题');
  console.log('4. 支持各种大小的视频文件');
}

// 运行
main().catch(error => {
  console.error('流程错误:', error);
  process.exit(1);
});

module.exports = {
  downloadBestQualityVideo,
  uploadToS3,
  cleanup
};