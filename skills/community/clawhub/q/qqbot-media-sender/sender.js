#!/usr/bin/env node
/**
 * QQBot Media Sender
 * 一键发送图片/视频/文件到 QQ
 */

import fs from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';

// 支持的文件类型
const MEDIA_TYPES = {
  image: ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
  video: ['.mp4', '.avi', '.mov', '.wmv'],
  file: ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.zip']
};

// 最大文件大小 (20MB)
const MAX_FILE_SIZE = 20 * 1024 * 1024;

/**
 * 获取文件类型
 */
function getFileType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  
  if (MEDIA_TYPES.image.includes(ext)) return 'image';
  if (MEDIA_TYPES.video.includes(ext)) return 'video';
  return 'file';
}

/**
 * 获取标签名
 */
function getTag(type) {
  switch (type) {
    case 'image': return 'qqimg';
    case 'video': return 'qqvideo';
    default: return 'qqfile';
  }
}

/**
 * 检查文件大小
 */
async function checkFileSize(filePath) {
  const stat = await fs.stat(filePath);
  if (stat.size > MAX_FILE_SIZE) {
    throw new Error(`文件过大：${formatSize(stat.size)} > 20MB`);
  }
  return stat.size;
}

/**
 * 格式化文件大小
 */
function formatSize(bytes) {
  if (bytes < 1024) return bytes + 'B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + 'KB';
  return (bytes / (1024 * 1024)).toFixed(1) + 'MB';
}

/**
 * 生成发送标签
 */
function generateTag(filePath, type) {
  const absPath = path.resolve(filePath);
  const tag = getTag(type);
  return `<${tag}>${absPath}</${tag}>`;
}

/**
 * 发送单个文件
 */
async function sendFile(filePath, options = {}) {
  try {
    // 检查文件是否存在
    await fs.access(filePath);
    
    // 获取文件类型
    const type = options.type || getFileType(filePath);
    
    // 检查文件大小
    const size = await checkFileSize(filePath);
    
    // 生成标签
    const tag = generateTag(filePath, type);
    
    console.log(`✅ 准备发送：${path.basename(filePath)} (${formatSize(size)})`);
    console.log(`   标签：${tag}`);
    
    return {
      success: true,
      path: filePath,
      type,
      tag,
      size
    };
  } catch (error) {
    console.error(`❌ 发送失败：${error.message}`);
    return {
      success: false,
      path: filePath,
      error: error.message
    };
  }
}

/**
 * 批量发送
 */
async function sendBatch(files, options = {}) {
  const results = [];
  const delay = options.delay || 1000;
  
  console.log(`🚀 开始批量发送 ${files.length} 个文件...\n`);
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    console.log(`[${i + 1}/${files.length}] 处理：${path.basename(file)}`);
    
    const result = await sendFile(file, options);
    results.push(result);
    
    if (i < files.length - 1 && delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  // 统计结果
  const success = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;
  
  console.log(`\n✅ 发送完成：${success} 成功，${failed} 失败`);
  
  return results;
}

/**
 * 扫描目录
 */
async function scanDirectory(dirPath, type = 'auto') {
  const files = [];
  const items = await fs.readdir(dirPath);
  
  for (const item of items) {
    const fullPath = path.join(dirPath, item);
    const stat = await fs.stat(fullPath);
    
    if (stat.isFile()) {
      const fileType = getFileType(fullPath);
      if (type === 'auto' || fileType === type) {
        files.push(fullPath);
      }
    }
  }
  
  return files;
}

// CLI
const args = process.argv.slice(2);
const options = {
  type: 'auto',
  group: null,
  compress: false,
  maxSize: 20,
  delay: 1000
};

// 解析参数
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--type' && args[i + 1]) {
    options.type = args[++i];
  } else if (args[i] === '--group' && args[i + 1]) {
    options.group = args[++i];
  } else if (args[i] === '--compress') {
    options.compress = true;
  } else if (args[i] === '--max-size' && args[i + 1]) {
    options.maxSize = parseFloat(args[++i]);
  } else if (args[i] === '--delay' && args[i + 1]) {
    options.delay = parseFloat(args[++i]);
  }
}

// 主逻辑
async function main() {
  if (args.length === 0) {
    console.log('QQBot Media Sender - 一键发送媒体文件到 QQ');
    console.log('');
    console.log('用法:');
    console.log('  qqbot-send-media <文件路径>');
    console.log('  qqbot-send-media <目录> --type image');
    console.log('  qqbot-send-media file1.jpg file2.jpg --group 843812FF4BA524086B77B60886C38AB3');
    console.log('');
    console.log('选项:');
    console.log('  --type <类型>     文件类型：image, video, file, auto (默认: auto)');
    console.log('  --group <群号>    目标 QQ 群号');
    console.log('  --compress        压缩大文件');
    console.log('  --max-size <MB>   最大文件大小 (默认: 20)');
    console.log('  --delay <ms>      发送间隔 (默认: 1000)');
    return;
  }
  
  // 移除选项参数，保留文件路径
  const files = args.filter(arg => !arg.startsWith('--'));
  
  if (files.length === 0) {
    console.error('错误：请提供文件路径');
    process.exit(1);
  }
  
  // 检查是否为目录
  const firstFile = files[0];
  try {
    const stat = await fs.stat(firstFile);
    if (stat.isDirectory()) {
      console.log(`📂 扫描目录：${firstFile}`);
      const dirFiles = await scanDirectory(firstFile, options.type);
      console.log(`找到 ${dirFiles.length} 个文件`);
      await sendBatch(dirFiles, options);
    } else {
      await sendBatch(files, options);
    }
  } catch (error) {
    console.error(`错误：${error.message}`);
    process.exit(1);
  }
}

main().catch(console.error);
