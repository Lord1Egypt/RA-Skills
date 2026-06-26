#!/usr/bin/env node

/**
 * 本地预览工具
 * 
 * 模拟公众号环境，预览文章经过 HTML 压缩后的最终效果
 * 运行后会打开浏览器展示预览
 */

import fs from 'fs';
import path from 'path';
import http from 'http';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * 从 HTML 文件中提取文章内容（和 publish.js 相同的逻辑）
 */
function extractArticleContent(htmlContent) {
  const startMarker = '<!-- ========== ARTICLE CONTENT START ========== -->';
  const endMarker = '<!-- ========== ARTICLE CONTENT END ========== -->';
  
  let content = htmlContent;
  const startIdx = content.indexOf(startMarker);
  const endIdx = content.indexOf(endMarker);
  
  if (startIdx !== -1 && endIdx !== -1) {
    content = content.substring(startIdx + startMarker.length, endIdx);
  }
  
  return content.trim();
}

function compressHTML(html) {
  return html
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/>\s+</g, '><')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

function sanitizeForWechat(html) {
  return html.replace(/font-family:[^;'"]+;?/g, '');
}

// 确定 HTML 文件路径
const htmlFile = process.argv[2] || path.join(__dirname, '..', 'blog-post-wechat.html');

if (!fs.existsSync(htmlFile)) {
  console.error(`找不到 HTML 文件: ${htmlFile}`);
  process.exit(1);
}

const rawHTML = fs.readFileSync(htmlFile, 'utf-8');
let articleContent = extractArticleContent(rawHTML);
articleContent = sanitizeForWechat(articleContent);
const compressed = compressHTML(articleContent);

// 生成预览页面（模拟公众号阅读环境）
const previewHTML = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>公众号预览 - 模拟最终效果</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { 
    background: #f5f5f5; 
    font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif; 
  }
  .header {
    background: #1B1642; color: #fff; padding: 16px 24px;
    text-align: center; font-size: 13px;
    position: sticky; top: 0; z-index: 10;
  }
  .header span { opacity: 0.6; }
  .header strong { color: #A5B4FC; }
  .phone-frame {
    max-width: 420px; margin: 30px auto; background: #fff;
    border-radius: 16px; overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.12);
  }
  .phone-top {
    background: #f7f7f7; padding: 12px 16px;
    display: flex; align-items: center; gap: 8px;
    border-bottom: 1px solid #eee;
  }
  .phone-top .dot { 
    width: 8px; height: 8px; border-radius: 50%; 
    background: #ccc; 
  }
  .phone-top .title { font-size: 13px; color: #999; }
  .article-area { 
    max-height: 80vh; overflow-y: auto; 
    /* 模拟公众号阅读器的基础样式 */
    font-size: 17px; 
    line-height: 1.6;
    word-wrap: break-word;
    -webkit-hyphens: auto;
  }
  .stats {
    background: #fff; max-width: 420px; margin: 16px auto;
    border-radius: 12px; padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 13px; color: #666; line-height: 2;
  }
  .stats strong { color: #1B1642; }
</style>
</head>
<body>

<div class="header">
  <span>这是</span> <strong>API 推送后</strong> <span>在公众号中的预览效果（已压缩 HTML）</span>
</div>

<div class="phone-frame">
  <div class="phone-top">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="title">微信公众号文章预览</div>
  </div>
  <div class="article-area">
    ${compressed}
  </div>
</div>

<div class="stats">
  <strong>HTML 统计</strong><br>
  原始字符数: ${articleContent.length}<br>
  压缩后字符数: ${compressed.length}<br>
  压缩率: ${Math.round((1 - compressed.length / articleContent.length) * 100)}%<br>
  API 限制: 20,000 字符 / 1MB — 
  <strong style="color: ${compressed.length < 20000 ? '#22C55E' : '#EF4444'}">
    ${compressed.length < 20000 ? '✓ 符合要求' : '✗ 超出限制'}
  </strong>
</div>

</body>
</html>`;

// 启动本地服务器
const PORT = 3456;
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(previewHTML);
});

server.listen(PORT, () => {
  console.log(`\n📱 公众号预览已启动: http://localhost:${PORT}`);
  console.log('   这是文章经过 HTML 压缩后在公众号环境中的模拟效果');
  console.log('   按 Ctrl+C 退出\n');
});
