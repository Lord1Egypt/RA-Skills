#!/usr/bin/env node
/**
 * 今日头条文章图片提取脚本
 * 功能：提取文章中的图片URL并下载
 * 
 * 用法：
 *   node parse-toutiao.js <文章URL> <输出目录>
 * 
 * 示例：
 *   node parse-toutiao.js "https://www.toutiao.com/w/1860414912331850/" ./toutiao-output
 * 
 * 说明：
 *   今日头条页面需要JavaScript渲染，此脚本通过解析页面HTML提取图片URL
 *   由于今日头条的反爬机制，建议在浏览器中打开页面后使用开发者工具提取图片URL
 *   或使用浏览器截图功能保存内容
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 解析命令行参数
const args = process.argv.slice(2);
const URL = args[0];
const OUTPUT_DIR = args[1] || './toutiao-download';

if (!URL) {
  console.log('用法：node parse-toutiao.js <文章URL> [输出目录]');
  console.log('示例：node parse-toutiao.js "https://www.toutiao.com/w/xxx/" ./output');
  console.log('\n说明：今日头条页面需要JavaScript渲染，建议在浏览器中打开后提取图片URL');
  process.exit(1);
}

// 创建输出目录
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log(`开始解析今日头条：${URL}`);
console.log(`输出目录：${OUTPUT_DIR}`);
console.log('---');

// 下载文件辅助函数
function downloadFile(url, filepath) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : require('http');
    client.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://www.toutiao.com/',
      }
    }, (res) => {
      if (res.statusCode === 302 || res.statusCode === 301) {
        // 跟随重定向
        downloadFile(res.headers.location, filepath).then(resolve).catch(reject);
        return;
      }
      
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
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

// 提取文章ID
function extractArticleId(url) {
  const patterns = [
    /\/w\/(\d+)\//,
    /\/article\/(\d+)\//,
    /\/item\/(\d+)/,
  ];
  
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }
  return null;
}

// 主函数
async function main() {
  const articleId = extractArticleId(URL);
  if (articleId) {
    console.log(`文章 ID: ${articleId}`);
  }

  // 访问页面获取HTML
  https.get(URL, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Referer': 'https://www.toutiao.com/',
    }
  }, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', async () => {
      try {
        // 检查是否需要登录或页面被拦截
        if (data.includes('请登录') || data.includes('验证码')) {
          console.log('⚠️ 页面需要登录或验证，无法直接获取内容');
          console.log('提示：请使用浏览器打开页面，手动提取图片URL');
          process.exit(1);
        }
        
        // 提取文章标题
        const titleMatch = data.match(/<title>([^<]*)<\/title>/);
        const title = titleMatch ? titleMatch[1].trim() : '未知标题';
        console.log(`标题: ${title}`);
        
        // 从HTML中提取图片URL（多种模式）
        const imageUrls = [];
        
        // 模式1: 标准图片URL
        const imgRegex = /https?:\/\/[^\s"'<>]+\.(jpg|jpeg|png|webp|gif)/gi;
        let match;
        while ((match = imgRegex.exec(data)) !== null) {
          imageUrls.push(match[0]);
        }
        
        // 模式2: 今日头条特定图片域名
        const toutiaoImgRegex = /https?:\/\/[a-z0-9-]+\.toutiaoimg\.com\/[^\s"'<>]+/gi;
        while ((match = toutiaoImgRegex.exec(data)) !== null) {
          imageUrls.push(match[0]);
        }
        
        // 去重并过滤
        const uniqueUrls = [...new Set(imageUrls)].filter(url => {
          // 过滤掉非文章图片
          return url.includes('toutiaoimg.com') && 
                 !url.includes('avatar') && 
                 !url.includes('icon') &&
                 !url.includes('logo') &&
                 !url.includes('.svg');
        });
        
        if (uniqueUrls.length === 0) {
          console.log('\n⚠️ 未从HTML中找到图片');
          console.log('说明：今日头条页面需要JavaScript渲染才能加载图片');
          console.log('建议：使用浏览器开发者工具提取图片URL，或使用以下方法：');
          console.log('  1. 在浏览器中打开页面');
          console.log('  2. 按F12打开开发者工具');
          console.log('  3. 在Console中执行：document.querySelectorAll("article img").forEach(img => console.log(img.src))');
          console.log('  4. 复制输出的URL并使用curl下载');
          
          // 输出页面中可能包含图片URL的JSON数据
          const jsonMatch = data.match(/"imageList":\s*(\[[^\]]+\])/);
          if (jsonMatch) {
            console.log('\n✅ 发现图片列表数据，尝试解析...');
            try {
              const imageList = JSON.parse(jsonMatch[1]);
              console.log(`找到 ${imageList.length} 张图片信息`);
            } catch (e) {
              // 解析失败
            }
          }
          
          process.exit(1);
        }
        
        console.log(`\n找到 ${uniqueUrls.length} 张图片`);
        console.log('开始下载...\n');
        
        // 下载图片（最多10张）
        const results = [];
        for (let i = 0; i < Math.min(uniqueUrls.length, 10); i++) {
          const imgUrl = uniqueUrls[i];
          const ext = imgUrl.match(/\.(jpg|jpeg|png|webp|gif)/i)?.[1] || 'jpg';
          const filename = path.join(OUTPUT_DIR, `image-${String(i + 1).padStart(2, '0')}.${ext}`);
          
          try {
            const size = await downloadFile(imgUrl, filename);
            console.log(`✅ [${i + 1}/${uniqueUrls.length}] ${path.basename(filename)} (${size}KB)`);
            results.push({ index: i + 1, filename, size, url: imgUrl });
          } catch (err) {
            console.log(`❌ [${i + 1}/${uniqueUrls.length}] 下载失败: ${err.message}`);
          }
        }
        
        // 输出结果
        console.log('\n---');
        console.log('下载完成！');
        console.log(JSON.stringify({
          title,
          articleId,
          totalImages: uniqueUrls.length,
          downloaded: results.length,
          outputDir: OUTPUT_DIR,
          images: results
        }, null, 2));
        
      } catch (err) {
        console.log('❌ 解析失败:', err.message);
        process.exit(1);
      }
    });
  }).on('error', (err) => {
    console.log('❌ 请求失败:', err.message);
    process.exit(1);
  });
}

main();
