#!/usr/bin/env node
/**
 * 哔哩哔哩（B站）视频下载脚本
 * 功能：下载B站视频并提取信息
 * 
 * 用法：
 *   node parse-bilibili.js <视频URL> [输出目录]
 * 
 * 示例：
 *   node parse-bilibili.js "https://www.bilibili.com/video/BV1AUA3zcE2Z/" ./bilibili-output
 * 
 * 说明：
 *   本脚本调用 yt-dlp 下载视频，需要提前安装 yt-dlp
 *   安装方式：brew install yt-dlp
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { buildAnalysis } = require('./build-content-analysis');

// 解析命令行参数
const args = process.argv.slice(2);
const URL = args[0];
const OUTPUT_DIR = args[1] || './bilibili-download';

if (!URL) {
  console.log('用法：node parse-bilibili.js <视频URL> [输出目录]');
  console.log('示例：node parse-bilibili.js "https://www.bilibili.com/video/BV1AUA3zcE2Z/" ./output');
  console.log('\n说明：需要提前安装 yt-dlp（brew install yt-dlp）');
  process.exit(1);
}

// 创建输出目录
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log(`开始解析B站视频：${URL}`);
console.log(`输出目录：${OUTPUT_DIR}`);
console.log('---');

// 提取BV号
function extractBvid(url) {
  const match = url.match(/BV([a-zA-Z0-9]+)/);
  return match ? match[1] : null;
}

const bvid = extractBvid(URL);
if (bvid) {
  console.log(`BV号: BV${bvid}`);
}

// 主函数
async function main() {
  try {
    // 获取视频信息
    console.log('\n📊 获取视频信息...');
    const infoJson = execSync(
      `yt-dlp --dump-json "${URL}" 2>/dev/null`,
      { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
    );
    const info = JSON.parse(infoJson);
    
    console.log(`标题: ${info.title}`);
    console.log(`UP主: ${info.uploader}`);
    console.log(`时长: ${info.duration}秒`);
    console.log(`播放量: ${info.view_count}`);
    console.log(`点赞: ${info.like_count}`);
    console.log(`标签: ${info.tags?.join(', ')}`);
    
    // 下载视频（1080P + 最佳音频）
    console.log('\n📥 开始下载视频（1080P）...');
    const outputPath = path.join(OUTPUT_DIR, 'video.mp4');
    
    execSync(
      `yt-dlp -f "30080+30280" -o "${outputPath}" "${URL}" 2>&1`,
      { stdio: 'inherit' }
    );
    
    // 检查文件大小
    const stats = fs.statSync(outputPath);
    const sizeMB = (stats.size / 1024 / 1024).toFixed(2);
    
    console.log('\n✅ 下载完成！');
    console.log(`文件路径: ${outputPath}`);
    console.log(`文件大小: ${sizeMB}MB`);
    
    // 输出结果
    const result = {
      title: info.title,
      uploader: info.uploader,
      bvid: info.id,
      duration: info.duration,
      view_count: info.view_count,
      like_count: info.like_count,
      tags: info.tags,
      thumbnail: info.thumbnail,
      download_path: outputPath,
      file_size: `${sizeMB}MB`,
      webpage_url: info.webpage_url
    };
    const analysis = buildAnalysis({
      title: info.title || '',
      text: (info.description || '').toString(),
      platform: 'B站',
      mediaType: '视频',
      visual: `视频时长 ${info.duration || 0} 秒，UP主 ${info.uploader || '未知'}`,
      maxChars: 100,
    });
    result.content_analysis = analysis.analysis;
    result.analysis_score = analysis.score;
    result.analysis_evidence = analysis.evidence;
    
    console.log('\n---');
    console.log(JSON.stringify(result, null, 2));
    
  } catch (err) {
    console.error('❌ 错误:', err.message);
    console.log('\n提示：');
    console.log('  1. 确保已安装 yt-dlp: brew install yt-dlp');
    console.log('  2. 确保视频链接有效');
    console.log('  3. 如果需要下载1080P高码率或会员视频，需要添加Cookie');
    process.exit(1);
  }
}

main();
