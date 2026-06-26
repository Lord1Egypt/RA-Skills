#!/usr/bin/env node

/** Douyin video downloader & transcript extractor (Node.js) */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// 配置
const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.9',
};


const DEFAULT_DOWNLOAD_PATH = 'C:\\Users\\Administrator\\.openclaw\\workspace\\outputs\\douyin\\';

// 工具函数：Promise 版本的 http 请求
function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const client = parsedUrl.protocol === 'https:' ? https : http;
    
    const opts = {
      method: options.method || 'GET',
      headers: { ...HEADERS, ...options.headers }
    };
    
    const req = client.request(url, opts, (res) => {
      // 处理重定向
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        httpRequest(res.headers.location, options)
          .then(resolve)
          .catch(reject);
        return;
      }
      
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({ 
          statusCode: res.statusCode, 
          headers: res.headers,
          body: data,
          url: url 
        });
      });
    });
    
    req.on('error', reject);
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    
    if (options.body) {
      req.write(options.body);
    }
    req.end();
  });
}

// 工具函数：下载文件
async function downloadFile(url, filepath, showProgress = true) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const client = parsedUrl.protocol === 'https:' ? https : http;
    
    const req = client.get(url, { headers: HEADERS }, (res) => {
      // 处理重定向
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        downloadFile(res.headers.location, filepath, showProgress)
          .then(resolve)
          .catch(reject);
        return;
      }
      
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      
      const totalSize = parseInt(res.headers['content-length'] || '0', 10);
      let downloaded = 0;
      
      const writer = fs.createWriteStream(filepath);
      
      res.on('data', (chunk) => {
        downloaded += chunk.length;
        if (showProgress && totalSize > 0) {
          const progress = (downloaded / totalSize * 100).toFixed(1);
          process.stdout.write(`\r下载进度: ${progress}%`);
        }
      });
      
      res.pipe(writer);
      
      writer.on('finish', () => {
        if (showProgress) console.log(`\n文件已保存: ${filepath}`);
        resolve(filepath);
      });
      
      writer.on('error', reject);
    });
    
    req.on('error', reject);
    req.setTimeout(120000, () => {
      req.destroy();
      reject(new Error('Download timeout'));
    });
  });
}

// 工具函数：运行 ffmpeg
function runFfmpeg(args) {
  return new Promise((resolve, reject) => {
    const proc = spawn('C:\\Users\\Administrator\\ffmpeg-8.1-full_build\\bin\\ffmpeg.exe', args);
    
    let stderr = '';
    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    proc.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`ffmpeg exited with code ${code}: ${stderr.slice(-500)}`));
      }
    });
    
    proc.on('error', reject);
  });
}

// 解析抖音分享链接或 modal_id（支持混杂文字的复制内容）
async function parseShareUrl(shareText) {
  // 1️⃣ 检查是否直接给出 modal_id（16+位数字或 modal_id=xxx 格式）
  const modalIdMatch = shareText.match(/(?:modal_id[=:])?(\d{16,})/);
  if (modalIdMatch) {
    const modalId = modalIdMatch[1];
    return await getVideoInfoByModalId(modalId);
  }

  // 2️⃣ 从任意文字块中提取第一个 http(s) URL
  const urlMatch = shareText.match(/https?:\/\/[^\s]+/);
  if (!urlMatch) {
    throw new Error('未找到有效的分享链接');
  }
  let shareUrl = urlMatch[0];

  // 3️⃣ 清理 URL：去掉常见的结尾标点（英文、中文）
  shareUrl = shareUrl.replace(/[\.,;!?，。！？]+$/g, '');

  // 4️⃣ 访问分享链接，获取重定向后的完整 URL
  const response1 = await httpRequest(shareUrl);
  const finalUrl = response1.url;

  // 5️⃣ 从最终 URL 中提取 video_id（可能出现在 /video/ 或 ?video_id=）
  let videoIdMatch = finalUrl.match(/\/video\/(\d+)/) || finalUrl.match(/[?&]video_id=(\d+)/);
  if (!videoIdMatch) {
    throw new Error('无法从URL中提取视频ID');
  }
  const videoId = videoIdMatch[1];

  return await getVideoInfoByModalId(videoId);
}

// 通过 modal_id 获取视频信息
async function getVideoInfoByModalId(modalId) {
  // 访问 iesdouyin.com 页面
  const pageUrl = `https://www.iesdouyin.com/share/video/${modalId}/`;
  const response = await httpRequest(pageUrl);
  
  // 从 HTML 中提取 window._ROUTER_DATA
  const match = response.body.match(/window\._ROUTER_DATA\s*=\s*(.*?)<\/script>/);
  if (!match || !match[1]) {
    throw new Error('从HTML中解析视频信息失败');
  }
  
  // 解析 JSON
  const jsonData = JSON.parse(match[1].trim());
  const loaderData = jsonData.loaderData || jsonData;
  
  let videoData;
  if (loaderData['video_(id)/page']) {
    videoData = loaderData['video_(id)/page'].videoInfoRes?.item_list?.[0];
  } else if (loaderData['note_(id)/page']) {
    videoData = loaderData['note_(id)/page'].videoInfoRes?.item_list?.[0];
  }
  
  if (!videoData) {
    throw new Error('无法从JSON中解析视频信息');
  }
  
  const videoUrl = videoData.video?.play_addr?.url_list?.[0]?.replace('playwm', 'play') ||
                   videoData.video?.download_addr?.url_list?.[0];
  const desc = videoData.desc || `douyin_${modalId}`;
  
  return {
    url: videoUrl,
    title: desc.replace(/[\\/:*?"<>|]/g, '_'),
    video_id: modalId
  };
}

// 下载视频
async function downloadVideo(videoInfo, outputDir, showProgress = true) {
  const outputPath = path.join(outputDir, `${videoInfo.video_id}.mp4`);
  
  if (showProgress) {
    console.log(`正在下载视频: ${videoInfo.title}`);
  }
  
  await downloadFile(videoInfo.url, outputPath, showProgress);
  
  return outputPath;
}

// 提取音频
async function extractAudio(videoPath, showProgress = true) {
  // 直接提取为 16kHz 单声道 PCM WAV，满足 Whisper 要求
  const audioPath = videoPath.replace(/\.mp4$/, '.wav');
  
  if (showProgress) {
    console.log('正在提取音频 (16kHz PCM WAV)...');
  }
  
  // 使用 spawnSync 调用 ffmpeg，避免 shell 转义问题
  const { spawnSync } = require('child_process');
  const result = spawnSync('C:\\Users\\Administrator\\ffmpeg-8.1-full_build\\bin\\ffmpeg.exe', ['-i', videoPath, '-vn', '-ac', '1', '-ar', '16000', '-f', 'wav', '-y', audioPath], { stdio: 'ignore' });
  if (result.status !== 0) {
    const errMsg = result.stderr ? result.stderr.toString() : '未知错误';
    throw new Error('音频提取失败: ' + errMsg);
  }
  
  if (showProgress) {
    console.log(`音频已保存: ${audioPath}`);
  }
  
  return audioPath;
}

// 语音转文字 - 使用 curl
async function transcribeAudio(audioPath, showProgress = true) {
  if (showProgress) {
    console.log('正在识别语音 (本地 Whisper)...');
  }
  
  // 使用本地 Whisper 命令行工具进行转写。假设系统已安装 `whisper` 可执行文件。
  // Whisper 将音频转写为 txt 文件，默认输出到当前目录，文件名为 audioPath 的 basename 加 .txt。
  return new Promise((resolve, reject) => {
    const { spawn } = require('child_process');
    const args = [
      '--model', 'base', // 可根据实际模型调整
      '--output_dir', path.dirname(audioPath),
      '--output_format', 'txt',
      '--language', 'zh',
      audioPath
    ];
    const proc = spawn('whisper', args);
    let stderr = '';
    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    proc.on('close', (code) => {
      if (code === 0) {
        // Whisper 会生成与音频同名的 .txt 文件
        const txtPath = audioPath.replace(/\.(mp3|wav|m4a|mp4)$/i, '.txt');
        try {
          const txt = require('fs').readFileSync(txtPath, 'utf-8');
          resolve(txt.trim());
        } catch (e) {
          reject(new Error('读取 Whisper 输出失败: ' + e.message));
        }
      } else {
        reject(new Error(`Whisper 转写失败: ${stderr}`));
      }
    });
    proc.on('error', reject);
  });
}

// 语义分段 - 使用本地 LLM（OpenClaw 默认模型）
async function semanticSegment(text, showProgress = true) {
  // 简单的本地分段实现：
  // 1. 按中文标点（句号、感叹号、问号）切分句子。
  // 2. 每 3~4 句合并为一个段落。
  // 3. 为每段自动添加小标题 "## 段落 X"（可自行编辑标题）。
  // 该实现不依赖外部 API，使用纯 JavaScript 完成。
  if (showProgress) {
    console.log('正在进行本地语义分段...');
  }

  const sentences = text.split(/(?<=[。！？])/);
  const chunks = [];
  let current = '';
  for (let i = 0; i < sentences.length; i++) {
    const s = sentences[i].trim();
    if (!s) continue;
    current += s;
    // 每 3 句或最后一次强制换段
    if ((i + 1) % 3 === 0 || i === sentences.length - 1) {
      chunks.push(current.trim());
      current = '';
    }
  }

  // 生成带标题的 markdown
  const segmented = chunks.map((chunk, idx) => {
    const title = `## 段落 ${idx + 1}`;
    return `${title}\n\n${chunk}`;
  }).join('\n\n');

  return segmented;
}


// 提取文案主函数
async function extractText(shareLink, apiKey, outputDir, saveVideo = false, showProgress = true, doSegment = true) {
  
  if (showProgress) {
    console.log('正在解析抖音分享链接...');
  }
  
  const videoInfo = await parseShareUrl(shareLink);
  
  if (showProgress) {
    console.log('正在下载视频...');
  }
  
  const videoPath = await downloadVideo(videoInfo, outputDir, showProgress);
  
  if (showProgress) {
    console.log('正在提取音频...');
  }
  
  const audioPath = await extractAudio(videoPath, showProgress);
  
  if (showProgress) {
    console.log('正在从音频中提取文本...');
  }
  
  let textContent = await transcribeAudio(audioPath, showProgress);
  
  // 语义分段
  if (doSegment) {
    textContent = await semanticSegment(textContent, null, showProgress);
  }
  
  // 保存文案
  const outputPath = path.join(outputDir, videoInfo.video_id, 'transcript.md');
  const outputFolder = path.dirname(outputPath);
  
  fs.mkdirSync(outputFolder, { recursive: true });
  
  const markdown = `# ${videoInfo.title}

| 属性 | 值 |
|------|-----|
| 视频ID | \`${videoInfo.video_id}\` |
| 提取时间 | ${new Date().toLocaleString('zh-CN')} |
| 下载链接 | [点击下载](${videoInfo.url}) |

---

## 文案内容

${textContent}
`;
  
  fs.writeFileSync(outputPath, markdown, 'utf-8');
  
  if (showProgress) {
    console.log(`文案已保存到: ${outputPath}`);
  }
  
  // 清理临时文件
  if (!saveVideo) {
    try { fs.unlinkSync(videoPath); } catch {}
  }
  try { fs.unlinkSync(audioPath); } catch {}
  
  return {
    video_info: videoInfo,
    text: textContent,
    output_path: outputPath
  };
}

// 主入口
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const shareLink = args[1];
  
  if (!command || !shareLink) {
    console.log(`
抖音无水印视频下载和文案提取工具

用法:
  node douyin.js info <分享链接|modal_id>         - 获取视频信息
  node douyin.js download <链接|modal_id> -o <目录>  - 下载视频（默认: /tmp/douyin-download/）
  node douyin.js extract <链接|modal_id> -o <目录>   - 提取文案（默认: /tmp/douyin-download/）
  node douyin.js extract <链接> --no-segment        - 提取文案（不语义分段）
  
支持输入:
  - 抖音分享链接: https://v.douyin.com/xxxxx
  - modal_id: 7597329042169220398
  - modal_id=xxx 格式

`);
    process.exit(1);
  }
  
  // 解析参数
  let outputDir = DEFAULT_DOWNLOAD_PATH;
  let saveVideo = false;
  let doSegment = true;
  
  for (let i = 2; i < args.length; i++) {
    if (args[i] === '-o' && args[i + 1]) {
      outputDir = args[i + 1];
      i++;
    } else if (args[i] === '-v' || args[i] === '--save-video') {
      saveVideo = true;
    } else if (args[i] === '--segment') {
      doSegment = true;
    } else if (args[i] === '--no-segment') {
      doSegment = false;
    }
  }
  
  try {
    if (command === 'info') {
      const info = await parseShareUrl(shareLink);
      console.log('\n' + '='.repeat(50));
      console.log('视频信息:');
      console.log('='.repeat(50));
      console.log(`视频ID: ${info.video_id}`);
      console.log(`标题: ${info.title}`);
      console.log(`下载链接: ${info.url}`);
      console.log('='.repeat(50));
      
    } else if (command === 'download') {
      const videoInfo = await parseShareUrl(shareLink);
      const videoPath = await downloadVideo(videoInfo, outputDir);
      console.log(`\n视频已保存到: ${videoPath}`);
      
    } else if (command === 'extract') {
      const result = await extractText(shareLink, null, outputDir, saveVideo, true, doSegment);
      console.log('\n' + '='.repeat(50));
      console.log('提取完成!');
      console.log('='.repeat(50));
      console.log(`视频ID: ${result.video_info.video_id}`);
      console.log(`标题: ${result.video_info.title}`);
      console.log(`保存位置: ${result.output_path}`);
      console.log('='.repeat(50));
      console.log('\n文案内容:\n');
      console.log(result.text.slice(0, 500) + '...' || result.text);
      console.log('\n' + '='.repeat(50));
    }
    
  } catch (error) {
    console.error(`错误: ${error.message}`);
    process.exit(1);
  }
}

main();
