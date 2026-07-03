#!/usr/bin/env node

/**
 * fetch_article.js - 抓取微信公众号文章正文
 *
 * 用法: node fetch_article.js <article_url> [options]
 *
 * 选项:
 *   --output, -o <path>  输出文件路径（默认 stdout）
 *   --fallback, -f       使用 curl 回退方案
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');
const { execSync } = require('child_process');

// 配置文件
const configPath = path.join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const result = { url: null, output: null, fallback: false };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--output' || args[i] === '-o') {
      result.output = args[++i];
    } else if (args[i] === '--fallback' || args[i] === '-f') {
      result.fallback = true;
    } else if (!args[i].startsWith('-')) {
      result.url = args[i];
    }
  }
  return result;
}

/**
 * 检查 URL 是否为合法的微信公众号文章链接
 */
function isValidWeChatUrl(url) {
  return url && (url.includes('mp.weixin.qq.com') || url.includes('weixin.qq.com'));
}

/**
 * 使用 Node.js https/http 抓取页面内容
 */
function fetchWithHttp(url) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const module = parsedUrl.protocol === 'https:' ? https : http;

    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      headers: {
        'User-Agent': config.user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
      },
      timeout: 30000,
    };

    const req = module.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => resolve(data));
    });

    req.on('error', (err) => reject(err));
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.end();
  });
}

/**
 * 使用 curl 回退方案抓取
 */
function fetchWithCurl(url) {
  try {
    const result = execSync(
      `curl -s -L -A '${config.user_agent}' -H 'Accept-Language: zh-CN,zh;q=0.9' '${url}'`,
      { encoding: 'utf-8', timeout: 30000 }
    );
    return result;
  } catch (err) {
    throw new Error(`curl 抓取失败: ${err.message}`);
  }
}

/**
 * 从 HTML 中提取微信公众号文章信息
 * 由于 cheerio 可能未安装，使用正则表达式提取
 */
function extractArticleInfo(html) {
  const result = {
    title: '',
    author: '',
    publishDate: '',
    contentHtml: '',
    contentText: '',
    coverImage: '',
  };

  // 提取标题
  const titleMatch = html.match(/<h1[^>]*class="rich_media_title[^"]*"[^>]*>([\s\S]*?)<\/h1>/);
  if (titleMatch) {
    result.title = titleMatch[1].replace(/<[^>]*>/g, '').trim();
  } else {
    // 备选：从 og:title 或 title 标签提取
    const ogTitle = html.match(/<meta[^>]*property="og:title"[^>]*content="([^"]*)"/);
    if (ogTitle) result.title = ogTitle[1];
    else {
      const titleTag = html.match(/<title>([\s\S]*?)<\/title>/);
      if (titleTag) result.title = titleTag[1].trim();
    }
  }

  // 提取公众号名称
  const authorMatch = html.match(/<strong[^>]*class="rich_media_meta[^"]*nickname[^"]*"[^>]*>([\s\S]*?)<\/strong>/);
  if (authorMatch) {
    result.author = authorMatch[1].replace(/<[^>]*>/g, '').trim();
  } else {
    const profileNick = html.match(/var\s+nickname\s*=\s*"([^"]+)"/);
    if (profileNick) result.author = profileNick[1];
  }

  // 提取发布时间
  const dateMatch = html.match(/var\s+ct\s*=\s*"(\d+)"/);
  if (dateMatch) {
    const timestamp = parseInt(dateMatch[1]) * 1000;
    const date = new Date(timestamp);
    result.publishDate = date.toISOString().split('T')[0];
  } else {
    const publishTime = html.match(/em[^>]*id="publish_time"[^>]*>([\s\S]*?)<\/em>/);
    if (publishTime) result.publishDate = publishTime[1].trim();
  }

  // 提取封面图
  const coverMatch = html.match(/<meta[^>]*property="og:image"[^>]*content="([^"]*)"/);
  if (coverMatch) result.coverImage = coverMatch[1];

  // 提取正文 HTML（最核心部分）
  // 尝试多种选择器
  let contentMatch = html.match(/<div[^>]*id="js_content"[^>]*>([\s\S]*?)<\/div>\s*<script[^>]*>/);
  if (!contentMatch) {
    contentMatch = html.match(/<div[^>]*class="rich_media_content[^"]*"[^>]*>([\s\S]*?)<\/div>\s*<script/);
  }
  if (!contentMatch) {
    contentMatch = html.match(/<div[^>]*id="js_content"[^>]*>([\s\S]*?)<\/div>/);
  }

  if (contentMatch) {
    result.contentHtml = contentMatch[1].trim();
    // 转成纯文本
    result.contentText = htmlToText(result.contentHtml);
  }

  return result;
}

/**
 * 将 HTML 转为纯文本（保留基本结构）
 */
function htmlToText(html) {
  let text = html
    // 移除 script/style
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    // 移除注释
    .replace(/<!--[\s\S]*?-->/g, '')
    // 块级标签换行
    .replace(/<\/?(p|div|h[1-6]|li|blockquote|section|br)[^>]*>/gi, '\n')
    // 移除其他标签
    .replace(/<[^>]*>/g, '')
    // 处理实体
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    // 压缩空白
    .replace(/\n{3,}/g, '\n\n')
    .replace(/[ \t]+/g, ' ')
    .trim();

  return text;
}

/**
 * 截断过长的内容
 */
function truncateContent(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '\n\n...（文章过长已截断）';
}

/**
 * 主函数
 */
async function main() {
  const args = parseArgs();

  if (!args.url) {
    console.error('❌ 请提供微信公众号文章链接');
    console.error('用法: node fetch_article.js <article_url> [--output <path>] [--fallback]');
    process.exit(1);
  }

  if (!isValidWeChatUrl(args.url)) {
    console.error('❌ 请提供有效的微信公众号文章链接（包含 mp.weixin.qq.com）');
    process.exit(1);
  }

  console.error(`🔍 正在抓取: ${args.url}`);

  let html;
  try {
    if (args.fallback) {
      console.error('📡 使用 curl 备用方案...');
      html = fetchWithCurl(args.url);
    } else {
      html = await fetchWithHttp(args.url);
    }
  } catch (err) {
    console.error(`⚠️  直接抓取失败: ${err.message}`);
    console.error('📡 尝试 curl 备用方案...');
    try {
      html = fetchWithCurl(args.url);
    } catch (err2) {
      console.error(`❌ 抓取失败: ${err2.message}`);
      console.error('💡 建议：手动复制文章内容粘贴给 agent');
      process.exit(1);
    }
  }

  const article = extractArticleInfo(html);
  article.url = args.url;

  if (!article.title) {
    console.error('⚠️  未能提取到文章标题，页面结构可能已变化');
    article.title = '未命名文章';
  }

  if (!article.contentText) {
    console.error('⚠️  未能提取到正文内容，页面可能需登录查看');
  }

  // 截断过长的内容
  article.contentText = truncateContent(article.contentText, config.max_content_length);

  // 输出结果
  const output = JSON.stringify(article, null, 2);

  if (args.output) {
    fs.writeFileSync(args.output, output, 'utf-8');
    console.error(`✅ 已保存到: ${args.output}`);
  } else {
    console.log(output);
  }
}

main().catch((err) => {
  console.error(`❌ 错误: ${err.message}`);
  process.exit(1);
});
