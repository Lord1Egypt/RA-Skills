#!/usr/bin/env node
/**
 * SEO Article Generator - generates SEO-optimized HTML articles using DeepSeek AI
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8'));

// Try to get API key from OpenClaw config
let API_KEY = process.env.DEEPSEEK_API_KEY || '';
try {
  const openclawConfig = JSON.parse(
    fs.readFileSync('/home/admin/.openclaw/openclaw.json', 'utf8')
  );
  API_KEY = API_KEY || openclawConfig.models?.providers?.deepseek?.apiKey || '';
} catch(e) {}

const ARTICLE_DIR = path.join(__dirname, config.output_dir);

function callDeepSeek(prompt) {
  return new Promise((resolve, reject) => {
    if (!API_KEY) {
      reject(new Error('No API key found. Set DEEPSEEK_API_KEY env var.'));
      return;
    }
    const data = JSON.stringify({
      model: 'deepseek-v4-flash',
      messages: [
        { role: 'system', content: '你是一个SEO内容写手。生成高质量原创中文文章，不少于500字。' },
        { role: 'user', content: prompt }
      ],
      max_tokens: 4000
    });
    const req = https.request({
      hostname: 'api.deepseek.com',
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      }
    }, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(d);
          resolve(parsed.choices?.[0]?.message?.content || '');
        } catch(e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function buildHtml(title, content, topic) {
  const slug = topic.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '').substring(0, 20);
  const date = new Date().toISOString().split('T')[0];
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${title}</title>
<meta name="description" content="${title} - 完整教程和实用技巧">
<meta name="keywords" content="${topic}">
<meta name="date" content="${date}">
<style>
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;line-height:1.8;max-width:800px;margin:0 auto;padding:20px;color:#333}
h1{font-size:1.8em;border-bottom:2px solid #f0f0f0;padding-bottom:10px}
h2{font-size:1.4em;margin-top:30px;color:#222}
p{margin:15px 0;text-indent:2em}
a{color:#07c160}
.ad-box{background:#f9f9f9;border:1px solid #e0e0e0;border-radius:8px;padding:20px;margin:30px 0;text-align:center}
.ad-box h3{margin:0 0 10px;font-size:1.1em}
.ad-box p{margin:0;text-indent:0}
.ad-box .btn{display:inline-block;background:#07c160;color:#fff;padding:10px 30px;border-radius:5px;text-decoration:none;margin-top:10px}
.footer{text-align:center;color:#999;font-size:0.85em;margin-top:50px;padding-top:20px;border-top:1px solid #eee}
</style>
</head>
<body>
${content}
<div class="ad-box">
<h3>🎨 AI写真馆 - 9.9元生成专业写真</h3>
<p>上传照片，一键生成多种风格的AI写真，效果惊艳！</p>
<a class="btn" href="https://www.xn--ehqw44a690c.com/ai-photo" target="_blank">立即体验</a>
</div>
<div class="footer">
<p>本文由AI生成，仅供参考 | <a href="https://www.xn--ehqw44a690c.com">首页</a></p>
</div>
</body>
</html>`;
}

function updateSitemap(filename) {
  const sitemapPath = path.join(ARTICLE_DIR, 'sitemap.xml');
  const url = `https://www.xn--ehqw44a690c.com/article/${filename}`;
  const today = new Date().toISOString();
  let sitemap = '';
  if (fs.existsSync(sitemapPath)) {
    sitemap = fs.readFileSync(sitemapPath, 'utf8');
    sitemap = sitemap.replace('</urlset>', '');
  } else {
    sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
`;
  }
  sitemap += `  <url>
    <loc>${url}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>`;
  fs.writeFileSync(sitemapPath, sitemap);
}

async function generate() {
  fs.mkdirSync(ARTICLE_DIR, { recursive: true });

  // Pick a topic
  const topic = config.topics[Math.floor(Math.random() * config.topics.length)];
  const timestamp = Date.now();
  const filename = `seo-${timestamp}.html`;

  console.log(`[SEO Generator] Generating article about: ${topic}`);

  const prompt = `写一篇关于"${topic}"的SEO优化文章。
要求：
1. 标题要吸引人，包含关键词
2. 不少于500字
3. 有H2小标题分段
4. 内容实用，有价值
5. 语言自然，不要AI感太重`;

  try {
    const content = await callDeepSeek(prompt);
    const lines = content.trim().split('\n');
    const title = lines[0].replace(/^#+\s*/, '').replace(/^["""]|["""]$/g, '').trim() || topic;
    const body = lines.slice(1).join('\n');

    const html = buildHtml(title, body, topic);
    const filePath = path.join(ARTICLE_DIR, filename);
    fs.writeFileSync(filePath, html, 'utf8');
    updateSitemap(filename);

    console.log(`[SEO Generator] ✅ Article generated: ${filename}`);
    console.log(`[SEO Generator] Size: ${html.length} bytes`);
    console.log(`[SEO Generator] Title: ${title}`);
    return { filename, title, size: html.length };
  } catch (e) {
    console.error(`[SEO Generator] ❌ Error: ${e.message}`);
    throw e;
  }
}

// Run if executed directly
if (require.main === module) {
  generate().then(r => {
    console.log(JSON.stringify(r));
  }).catch(e => {
    console.error(e.message);
    process.exit(1);
  });
}

module.exports = { generate };
