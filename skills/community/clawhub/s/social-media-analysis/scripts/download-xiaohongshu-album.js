#!/usr/bin/env node
/**
 * 小红书图集专用下载脚本
 * 功能：从页面提取 imageList 并下载所有图片
 * 
 * 用法：
 *   node download-xiaohongshu-album.js <URL> <输出目录> [--cookie <COOKIE_STRING>]
 * 
 * 示例：
 *   node download-xiaohongshu-album.js "https://www.xiaohongshu.com/explore/69ba4a870000000028009ac0" ./images
 *   node download-xiaohongshu-album.js "URL" ./images --cookie "unread=xxx; id_token=xxx"
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 解析命令行参数
const args = process.argv.slice(2);
const URL = args[0];
const OUTPUT_DIR = args[1];
let COOKIE = '';

for (let i = 2; i < args.length; i++) {
  if (args[i] === '--cookie' && args[i + 1]) {
    COOKIE = args[i + 1];
    i++;
  }
}

if (!URL || !OUTPUT_DIR) {
  console.log('用法：node download-xiaohongshu-album.js <URL> <输出目录> [--cookie <COOKIE_STRING>]');
  process.exit(1);
}

// 创建输出目录
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log(`开始下载小红书图集：${URL}`);
console.log(`输出目录：${OUTPUT_DIR}`);
console.log('---');

const DEFAULT_COOKIE = COOKIE || process.env.XHS_COOKIE || '';

const options = {
  headers: {
    'Cookie': DEFAULT_COOKIE,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
  }
};

// 下载文件辅助函数
function downloadFile(url, filepath) {
  return new Promise((resolve, reject) => {
    https.get(url, options, (res) => {
      if (res.statusCode === 302 || res.statusCode === 301) {
        downloadFile(res.headers.location, filepath).then(resolve).catch(reject);
        return;
      }
      
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        fs.writeFileSync(filepath, Buffer.concat(chunks));
        const size = (fs.statSync(filepath).size / 1024).toFixed(1);
        resolve(size);
      });
    }).on('error', reject);
  });
}

// 提取 imageList（使用括号匹配）
function extractImageList(html) {
  const startIndex = html.indexOf('"imageList":');
  if (startIndex === -1) return null;
  
  const arrayStart = html.indexOf('[', startIndex);
  if (arrayStart === -1) return null;
  
  let depth = 0;
  let endIndex = arrayStart;
  for (let i = arrayStart; i < html.length; i++) {
    if (html[i] === '[') depth++;
    else if (html[i] === ']') depth--;
    if (depth === 0) {
      endIndex = i;
      break;
    }
  }
  
  const imageListStr = html.substring(arrayStart, endIndex + 1);
  
  try {
    return JSON.parse(imageListStr);
  } catch (e) {
    return null;
  }
}

// 获取页面并下载图片
https.get(URL, options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', async () => {
    try {
      const imageList = extractImageList(data);
      
      if (!imageList || imageList.length === 0) {
        console.log('❌ 未找到图片数据');
        console.log('');
        console.log('可能原因：');
        console.log('  1. Cookie 已过期或无效，请使用 --cookie 参数提供有效 Cookie');
        console.log('  2. 该帖子是视频类型，请使用 parse-xiaohongshu.js 脚本');
        console.log('  3. 链接已失效或帖子被删除');
        process.exit(1);
      }
      
      console.log(`✅ 找到 ${imageList.length} 张图片`);
      
      // 下载所有图片
      let successCount = 0;
      for (let i = 0; i < imageList.length; i++) {
        const img = imageList[i];
        const infoList = img.infoList || [];
        const imgInfo = infoList.find(info => info.imageScene === 'WB_DFT') || infoList[0];
        
        if (!imgInfo || !imgInfo.url) {
          console.log(`⚠️ 图片 ${i + 1} 无有效 URL`);
          continue;
        }
        
        let imgUrl = imgInfo.url.replace('http://', 'https://');
        const filename = path.join(OUTPUT_DIR, `image-${String(i + 1).padStart(2, '0')}.webp`);
        
        try {
          const size = await downloadFile(imgUrl, filename);
          console.log(`✅ 已保存：image-${String(i + 1).padStart(2, '0')}.webp (${size}KB)`);
          successCount++;
        } catch (err) {
          console.log(`❌ 图片 ${i + 1} 下载失败：${err.message}`);
        }
      }
      
      console.log('---');
      console.log(`完成！共 ${imageList.length} 张图片，成功下载 ${successCount} 张`);
      console.log(`输出目录：${OUTPUT_DIR}`);
      
    } catch (err) {
      console.log('❌ 解析失败:', err.message);
      process.exit(1);
    }
  });
}).on('error', (err) => {
  console.log('❌ 请求失败:', err.message);
  process.exit(1);
});
