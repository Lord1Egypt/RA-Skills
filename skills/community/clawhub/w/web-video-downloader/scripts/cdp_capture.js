/**
 * CDP网络监听脚本 - 捕获浏览器中的视频请求URL
 * 
 * 用法: node cdp_capture.js <cdp_ws_url> [output.json]
 * 
 * 工作原理：
 * 1. 连接到Chrome DevTools Protocol WebSocket
 * 2. 启用Network域监听
 * 3. 过滤视频相关请求（.mp4, .m3u8, .ts, video, media等）
 * 4. 捕获请求URL和Headers
 * 5. 输出到JSON文件
 * 
 * 注意：必须在视频播放期间运行此脚本
 */

const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const CDP_URL = process.argv[2];
const OUTPUT_FILE = process.argv[3] || '/tmp/captured_video_urls.json';

if (!CDP_URL) {
  console.error('用法: node cdp_capture.js <cdp_ws_url> [output.json]');
  console.error('');
  console.error('获取CDP URL: xb run --browser default get cdp-url');
  process.exit(1);
}

// 视频相关的URL关键词
const VIDEO_PATTERNS = [
  /\.mp4/i, /\.m3u8/i, /\.ts/i, /\.flv/i, /\.webm/i,
  /video/i, /media/i, /stream/i, /playback/i, /segment/i,
  /clips/i, /vod/i, /\.mpd/i
];

// 排除的URL模式（广告、追踪等）
const EXCLUDE_PATTERNS = [
  /google/i, /facebook/i, /analytics/i, /tracking/i,
  /doubleclick/i, /ads/i, /pixel/i, /beacon/i,
  /\.js$/i, /\.css$/i, /\.png$/i, /\.jpg$/i, /\.gif$/i,
  /\.woff/i, /\.svg/i
];

const captured = [];
let msgId = 1;

function isVideoUrl(url) {
  if (!url || typeof url !== 'string') return false;
  if (EXCLUDE_PATTERNS.some(p => p.test(url))) return false;
  return VIDEO_PATTERNS.some(p => p.test(url));
}

async function capture() {
  console.log(`[CDP] 连接到: ${CDP_URL}`);
  
  const ws = new WebSocket(CDP_URL);
  
  ws.on('open', () => {
    console.log('[CDP] 已连接，开始监听网络请求...');
    console.log('[CDP] 请在浏览器中播放视频，我会自动捕获请求');
    console.log('[CDP] 按 Ctrl+C 停止捕获并保存结果');
    
    // 启用Network域
    ws.send(JSON.stringify({ id: msgId++, method: 'Network.enable', params: {} }));
  });
  
  ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    
    // 监听网络请求
    if (msg.method === 'Network.requestWillBeSent') {
      const req = msg.params.request;
      const url = req.url;
      
      if (isVideoUrl(url)) {
        const entry = {
          url: url,
          method: req.method,
          headers: req.headers || {},
          type: msg.params.type,
          timestamp: new Date().toISOString(),
          requestId: msg.params.requestId
        };
        
        captured.push(entry);
        
        // 实时输出
        const shortUrl = url.length > 100 ? url.substring(0, 100) + '...' : url;
        console.log(`[捕获 #${captured.length}] ${shortUrl}`);
      }
    }
    
    // 监听响应，获取更多信息
    if (msg.method === 'Network.responseReceived') {
      const resp = msg.params.response;
      const url = resp.url;
      
      if (isVideoUrl(url)) {
        // 更新对应条目的响应信息
        const entry = captured.find(e => e.url === url && !e.status);
        if (entry) {
          entry.status = resp.status;
          entry.mimeType = resp.mimeType;
          entry.contentLength = resp.headers?.['content-length'];
        }
      }
    }
  });
  
  ws.on('error', (err) => {
    console.error('[CDP] 连接错误:', err.message);
  });
  
  ws.on('close', () => {
    console.log('[CDP] 连接关闭');
    saveResults();
  });
  
  // 优雅退出
  process.on('SIGINT', () => {
    console.log('\n[CDP] 停止捕获...');
    ws.close();
    setTimeout(() => {
      saveResults();
      process.exit(0);
    }, 500);
  });
  
  function saveResults() {
    // 去重
    const unique = [];
    const seen = new Set();
    for (const entry of captured) {
      if (!seen.has(entry.url)) {
        seen.add(entry.url);
        unique.push(entry);
      }
    }
    
    const result = {
      capturedAt: new Date().toISOString(),
      totalRequests: captured.length,
      uniqueUrls: unique.length,
      urls: unique
    };
    
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(result, null, 2));
    console.log(`\n[结果] 捕获 ${captured.length} 个请求，${unique.length} 个唯一URL`);
    console.log(`[结果] 保存到: ${OUTPUT_FILE}`);
    
    // 分类输出
    const mp4s = unique.filter(e => /\.mp4/i.test(e.url));
    const m3u8s = unique.filter(e => /\.m3u8/i.test(e.url));
    const tss = unique.filter(e => /\.ts/i.test(e.url));
    const others = unique.filter(e => !/\.mp4|\.m3u8|\.ts/i.test(e.url));
    
    if (mp4s.length) console.log(`\n  MP4: ${mp4s.length} 个`);
    if (m3u8s.length) console.log(`  M3U8: ${m3u8s.length} 个`);
    if (tss.length) console.log(`  TS: ${tss.length} 个`);
    if (others.length) console.log(`  其他: ${others.length} 个`);
  }
}

capture();