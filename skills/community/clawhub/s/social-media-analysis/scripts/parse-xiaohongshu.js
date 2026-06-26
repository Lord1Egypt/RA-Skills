#!/usr/bin/env node
/**
 * 小红书帖子解析脚本
 * 功能：判断类型（图集/视频）+ 下载图片/视频
 * 
 * 用法：
 *   node parse-xiaohongshu.js <URL> <输出目录> [--cookie <COOKIE_STRING>]
 * 
 * 示例：
 *   node parse-xiaohongshu.js "https://www.xiaohongshu.com/explore/69ba4a870000000028009ac0" ./output
 *   node parse-xiaohongshu.js "URL" ./output --cookie "unread=xxx; id_token=xxx"
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { buildAnalysis } = require('./build-content-analysis');

// 解析命令行参数
const args = process.argv.slice(2);
const URL = args[0];
const OUTPUT_DIR = args[1];
let COOKIE = '';

// 解析 --cookie 参数
for (let i = 2; i < args.length; i++) {
  if (args[i] === '--cookie' && args[i + 1]) {
    COOKIE = args[i + 1];
    i++;
  }
}

if (!URL || !OUTPUT_DIR) {
  console.log('用法：node parse-xiaohongshu.js <URL> <输出目录> [--cookie <COOKIE_STRING>]');
  console.log('示例：node parse-xiaohongshu.js "https://www.xiaohongshu.com/explore/xxx" ./output');
  process.exit(1);
}

// 创建输出目录
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// 提取笔记 ID
function extractNoteId(url) {
  const patterns = [
    /explore\/([a-f0-9]+)/,
    /discovery\/item\/([a-f0-9]+)/,
    /modal_id=([a-f0-9]+)/,
  ];
  
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }
  return null;
}

const NOTE_ID = extractNoteId(URL);
if (!NOTE_ID) {
  console.log('❌ 无法从小红书 URL 中提取笔记 ID');
  process.exit(1);
}

console.log(`开始解析小红书：${URL}`);
console.log(`笔记 ID: ${NOTE_ID}`);
console.log(`输出目录：${OUTPUT_DIR}`);
console.log('---');

// 默认 Cookie（如果用户提供则使用用户的）
const DEFAULT_COOKIE = COOKIE || process.env.XHS_COOKIE || '';

const options = {
  headers: {
    'Cookie': DEFAULT_COOKIE,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  }
};

// 下载文件辅助函数
function downloadFile(url, filepath) {
  return new Promise((resolve, reject) => {
    https.get(url, options, (res) => {
      if (res.statusCode === 302 || res.statusCode === 301) {
        // 重定向
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
  if (startIndex === -1) {
    return null;
  }
  
  const arrayStart = html.indexOf('[', startIndex);
  if (arrayStart === -1) {
    return null;
  }
  
  // 括号匹配找到数组结束位置
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
    console.log('⚠️ 解析 imageList 失败:', e.message);
    return null;
  }
}

// 判断类型并下载
https.get(URL, options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', async () => {
    try {
      // 尝试提取 imageList
      const imageList = extractImageList(data);
      
      if (imageList && imageList.length > 0) {
        // 图集类型
        console.log(`✅ 图集类型，找到 ${imageList.length} 张图片`);
        
        const imagesDir = path.join(OUTPUT_DIR, 'images');
        if (!fs.existsSync(imagesDir)) {
          fs.mkdirSync(imagesDir, { recursive: true });
        }
        
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
          
          // 转换 http 为 https
          let imgUrl = imgInfo.url.replace('http://', 'https://');
          
          // 去除水印参数（可选）
          // imgUrl = imgUrl.split('?')[0];
          
          const filename = path.join(imagesDir, `image-${String(i + 1).padStart(2, '0')}.webp`);
          
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
        console.log(`输出目录：${imagesDir}`);
        const analysis = buildAnalysis({
          title: '',
          text: '',
          platform: '小红书',
          mediaType: '图片',
          visual: `图集共 ${imageList.length} 张，成功下载 ${successCount} 张`,
          maxChars: 100,
        });
        console.log(JSON.stringify({
          type: 'album',
          note_id: NOTE_ID,
          total_images: imageList.length,
          downloaded_images: successCount,
          output_dir: imagesDir,
          content_analysis: analysis.analysis,
          analysis_score: analysis.score,
          analysis_evidence: analysis.evidence,
        }, null, 2));
        
      } else {
        // 可能是视频类型，尝试提取视频信息
        console.log('ℹ️ 未找到 imageList，可能是视频类型');
        
        // 尝试使用 yt-dlp 下载视频
        try {
          console.log('尝试使用 yt-dlp 下载视频...');
          
          const videoPath = path.join(OUTPUT_DIR, 'video.mp4');
          const cookieFile = '/tmp/xhs_cookies.txt';
          
          let cookieArg = '';
          if (DEFAULT_COOKIE) {
            // 创建临时 Cookie 文件
            const cookieContent = DEFAULT_COOKIE.split(';').map(c => {
              const [key, value] = c.trim().split('=');
              if (key && value) {
                return `.xiaohongshu.com\tTRUE\t/\tTRUE\t0\t${key.trim()}\t${value.trim()}`;
              }
              return '';
            }).filter(line => line).join('\n');
            
            fs.writeFileSync(cookieFile, cookieContent);
            cookieArg = `--cookies ${cookieFile}`;
          }
          
          const cmd = `yt-dlp ${cookieArg} -f best -o "${videoPath}" "${URL}" 2>&1`;
          const result = execSync(cmd, { encoding: 'utf8' });
          
          if (fs.existsSync(videoPath)) {
            const size = (fs.statSync(videoPath).size / 1024 / 1024).toFixed(1);
            console.log('---');
            console.log(`✅ 视频已下载：video.mp4 (${size}M)`);
            console.log(`输出目录：${OUTPUT_DIR}`);
            console.log('');
            console.log('提示：使用以下命令进行视频抽帧：');
            console.log(`  ffmpeg -i ${videoPath} -vf "fps=1/5" -q:v 2 ${path.join(OUTPUT_DIR, 'frame_%03d.jpg')}`);
            const analysis = buildAnalysis({
              title: '',
              text: '',
              platform: '小红书',
              mediaType: '视频',
              visual: `视频已下载，大小 ${size}MB`,
              maxChars: 100,
            });
            console.log(JSON.stringify({
              type: 'video',
              note_id: NOTE_ID,
              download_path: videoPath,
              file_size_mb: size,
              content_analysis: analysis.analysis,
              analysis_score: analysis.score,
              analysis_evidence: analysis.evidence,
            }, null, 2));
          } else {
            console.log('❌ 视频下载失败，文件不存在');
          }
          
        } catch (err) {
          console.log('❌ yt-dlp 下载失败:', err.message);
          console.log('');
          console.log('提示：');
          console.log('  1. 确保已安装 yt-dlp: brew install yt-dlp');
          console.log('  2. 提供有效的 Cookie: --cookie "unread=xxx; id_token=xxx"');
          console.log('  3. 检查 URL 是否有效');
        }
      }
      
    } catch (err) {
      console.log('❌ 解析失败:', err.message);
      process.exit(1);
    }
  });
}).on('error', (err) => {
  console.log('❌ 请求失败:', err.message);
  process.exit(1);
});
