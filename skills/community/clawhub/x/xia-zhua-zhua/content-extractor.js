#!/usr/bin/env node
/**
 * content-extractor - Content Catcher v4.0 增强版
 * 新增: 多模态提取 / PDF导出 / 结构化抽取 / 翻译
 */

const { chromium } = require('playwright');
const TurndownService = require('turndown');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');
const { URL } = require('url');

// ─── 配置 ───────────────────────────────────────────────

const CONFIG = {
  userAgents: [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36',
  ],
  timeout: 60000,
};

// ─── 工具函数 ───────────────────────────────────────────

function randomDelay(min = 1000, max = 3000) {
  return Math.floor(Math.random() * (max - min)) + min;
}

function getTimestamp() {
  return new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
}

// ─── Markdown转换 ───────────────────────────────────────

function buildTurndown() {
  const td = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced',
    bulletListMarker: '-',
    linkStyle: 'inlined',
  });

  td.addRule('images', {
    filter: 'img',
    replacement: (content, node) => {
      const alt = node.alt || '';
      const src = node.src || node.getAttribute('data-src') || '';
      if (!src) return '';
      return `![${alt}](${src})`;
    },
  });

  td.addRule('pre', {
    filter: 'pre',
    replacement: (content, node) => {
      const code = node.querySelector('code');
      const lang = code ? code.className.replace('language-', '') : '';
      return `\n\`\`\`${lang}\n${code ? code.innerText : node.innerText}\n\`\`\`\n`;
    },
  });

  td.keep(['table']);

  return td;
}

// ─── 多模态提取 ────────────────────────────────────────

// ─── 增强图片提取 ──────────────────────────────────────

const IMAGE_EXTENSIONS = {
  // 常见格式
  jpg: ['jpg', 'jpeg', 'jfif', 'pjp'],
  png: ['png'],
  gif: ['gif'],
  webp: ['webp'],
  avif: ['avif'],
  svg: ['svg'],
  bmp: ['bmp'],
  ico: ['ico'],
  // 高级格式
  apng: ['apng'],
  tiff: ['tif', 'tiff'],
  heic: ['heic', 'heif'],
  jxl: ['jxl'],
};

function getImageType(url) {
  try {
    const pathname = new URL(url).pathname.toLowerCase();
    const ext = pathname.split('.').pop().split('?')[0];
    for (const [type, exts] of Object.entries(IMAGE_EXTENSIONS)) {
      if (exts.includes(ext)) return type;
    }
  } catch {}
  return 'unknown';
}

async function extractImages(page) {
  console.log('  🖼️  提取图片资源...');
  const seen = new Set();
  const images = await page.evaluate(() => {
    const imgs = [];
    
    // 1. 普通img标签
    document.querySelectorAll('img').forEach(img => {
      const src = img.src || img.getAttribute('data-src') || img.getAttribute('data-original');
      if (src && !src.startsWith('data:') && !src.includes('base64')) {
        imgs.push({
          src,
          alt: img.alt || '',
          type: 'img',
          width: img.naturalWidth || img.width || 0,
          height: img.naturalHeight || img.height || 0,
        });
      }
    });
    
    // 2. picture/source元素
    document.querySelectorAll('picture source, picture img').forEach(el => {
      const src = el.src || el.getAttribute('srcset');
      if (src) {
        const srcset = el.getAttribute('srcset');
        if (srcset) {
          // 解析srcset
          srcset.split(',').forEach(s => {
            const [u, size] = s.trim().split(/\s+/);
            if (u && !u.startsWith('data:')) {
              imgs.push({ src: u, type: 'srcset', size });
            }
          });
        } else if (!src.startsWith('data:')) {
          imgs.push({ src, type: 'picture', alt: el.alt || '' });
        }
      }
    });
    
    // 3. CSS背景图片
    const cssImages = [];
    try {
      const sheets = document.styleSheets;
      for (const sheet of sheets) {
        try {
          for (const rule of sheet.cssRules) {
            if (rule.style && rule.style.backgroundImage) {
              const matches = rule.style.backgroundImage.match(/url\(["']?([^"'\)]+)["']?\)/g);
              if (matches) {
                matches.forEach(m => {
                  const src = m.match(/url\(["']?([^"'\)]+)["']?\)/)[1];
                  if (src && !src.startsWith('data:')) {
                    cssImages.push({ src, type: 'css', selector: rule.selectorText });
                  }
                });
              }
            }
          }
        } catch {}
      }
    } catch {}
    imgs.push(...cssImages);
    
    // 4. srcset属性
    document.querySelectorAll('[srcset]').forEach(el => {
      const srcset = el.getAttribute('srcset');
      srcset.split(',').forEach(s => {
        const [u, size] = s.trim().split(/\s+/);
        if (u && !u.startsWith('data:')) {
          imgs.push({ src: u, type: 'srcset', size });
        }
      });
    });
    
    return imgs;
  });
  
  // 去重 + 分类
  const result = { all: [], byType: {} };
  for (const img of images) {
    if (seen.has(img.src)) continue;
    seen.add(img.src);
    
    const type = getImageType(img.src);
    img.ext = type;
    result.all.push(img);
    
    if (!result.byType[type]) result.byType[type] = [];
    result.byType[type].push(img);
  }
  
  // 统计
  const total = result.all.length;
  const typeStats = Object.entries(result.byType)
    .map(([t, arr]) => `${t}(${arr.length})`)
    .join(', ');
  
  console.log(`     发现 ${total} 张图片 [${typeStats}]`);
  return result;
}

async function extractMedia(page) {
  console.log('  🎬 提取媒体资源...');
  const media = await page.evaluate(() => {
    const items = [];
    
    // 视频
    document.querySelectorAll('video').forEach(v => {
      items.push({
        type: 'video',
        src: v.src || v.currentSrc || '',
        poster: v.poster || '',
        duration: v.duration || 0,
      });
    });
    
    // 音频
    document.querySelectorAll('audio').forEach(a => {
      items.push({
        type: 'audio',
        src: a.src || a.currentSrc || '',
        duration: a.duration || 0,
      });
    });
    
    // source元素
    document.querySelectorAll('source').forEach(s => {
      const parent = s.parentElement;
      if (parent && (parent.tagName === 'VIDEO' || parent.tagName === 'AUDIO')) {
        return; // 已由上面处理
      }
      items.push({
        type: s.type || 'media',
        src: s.src || '',
      });
    });
    
    return items.filter(m => m.src);
  });
  
  console.log(`     发现 ${media.length} 个媒体资源`);
  return media;
}

// ─── 结构化抽取 ────────────────────────────────────────

async function extractTables(page) {
  console.log('  📊 提取表格数据...');
  const tables = await page.evaluate(() => {
    const result = [];
    document.querySelectorAll('table').forEach(table => {
      const rows = [];
      table.querySelectorAll('tr').forEach(tr => {
        const cells = [];
        tr.querySelectorAll('th, td').forEach(cell => {
          cells.push(cell.innerText.trim());
        });
        if (cells.length > 0) {
          rows.push(cells);
        }
      });
      if (rows.length > 0) {
        result.push({ rows });
      }
    });
    return result;
  });
  
  console.log(`     发现 ${tables.length} 个表格`);
  return tables;
}

async function extractLists(page) {
  console.log('  📋 提取列表数据...');
  const lists = await page.evaluate(() => {
    const result = [];
    
    // 有序列表
    document.querySelectorAll('ol').forEach(list => {
      const items = [];
      list.querySelectorAll('li').forEach(li => {
        items.push(li.innerText.trim());
      });
      if (items.length > 1) {
        result.push({ type: 'ol', items });
      }
    });
    
    // 无序列表
    document.querySelectorAll('ul').forEach(list => {
      // 排除导航菜单
      if (list.closest('nav') || list.querySelector('li[class*="menu"]')) {
        return;
      }
      const items = [];
      list.querySelectorAll('li').forEach(li => {
        items.push(li.innerText.trim());
      });
      if (items.length > 2) {
        result.push({ type: 'ul', items });
      }
    });
    
    return result;
  });
  
  console.log(`     发现 ${lists.length} 个列表`);
  return lists;
}

// ─── PDF导出 ────────────────────────────────────────────

function convertToPdf(inputPath, outputPath) {
  console.log('  📄 转换为PDF...');
  try {
    // 尝试使用Python的weasyprint
    const scriptPath = path.join(os.tmpdir(), `pdf_convert_${Date.now()}.py`);
    const script = `
import sys
import subprocess
import os

html_file = sys.argv[1]
pdf_file = sys.argv[2]

# 读取HTML
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 创建完整HTML
full_html = f'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: system-ui, -apple-system, sans-serif; padding: 40px; }}
h1 {{ color: #333; }}
img {{ max-width: 100%; height: auto; }}
pre {{ background: #f5f5f5; padding: 10px; overflow-x: auto; }}
</style>
</head>
<body>
{html_content}
</body>
</html>
'''

# 保存完整HTML
full_html_file = html_file.replace('.md', '_full.html')
with open(full_html_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

try:
    subprocess.run(['weasyprint', full_html_file, pdf_file], check=True, capture_output=True)
    os.remove(full_html_file)
    print('PDF_OK')
except Exception as e:
    print(f'PDF_ERROR: {e}')
    sys.exit(1)
`;
    
    fs.writeFileSync(scriptPath, script, 'utf8');
    
    const result = execSync(`python "${scriptPath}" "${inputPath}" "${outputPath}"`, {
      encoding: 'utf-8',
      timeout: 60000,
    });
    
    fs.unlinkSync(scriptPath);
    
    if (result.includes('PDF_OK')) {
      console.log('     ✅ PDF导出成功');
      return true;
    }
  } catch (err) {
    console.log(`     ⚠️ PDF导出失败: ${err.message}`);
  }
  return false;
}

// ─── 翻译功能 ────────────────────────────────────────────

function translateText(text, targetLang = 'en') {
  console.log(`  🌐 翻译为 ${targetLang === 'en' ? '英文' : targetLang === 'jp' ? '日文' : targetLang}...`);
  try {
    const scriptPath = path.join(os.tmpdir(), `trans_${Date.now()}.py`);
    const script = `
# -*- coding: utf-8 -*-
import sys
import json

try:
    from googletrans import Translator
    t = Translator()
    text = sys.argv[1]
    lang = sys.argv[2]
    lang_map = {'en': 'en', 'jp': 'ja', 'ko': 'ko'}
    result = t.translate(text, dest=lang_map.get(lang, 'en'))
    print(json.dumps({'ok': True, 'text': result.text}))
except ImportError:
    print(json.dumps({'ok': False, 'error': 'pip install googletrans==4.0.0-rc1'}))
except Exception as e:
    print(json.dumps({'ok': False, 'error': str(e)}))
`;
    
    fs.writeFileSync(scriptPath, script, 'utf8');
    const result = execSync(`python "${scriptPath}" "${text.substring(0, 5000)}" ${targetLang}`, {
      encoding: 'utf-8',
      timeout: 30000,
    });
    
    fs.unlinkSync(scriptPath);
    
    const data = JSON.parse(result);
    if (data.ok) {
      console.log('     ✅ 翻译完成');
      return data.text;
    }
  } catch (err) {
    console.log(`     ⚠️ 翻译失败: ${err.message}`);
  }
  return text;
}

// ─── 核心抓取 ────────────────────────────────────────────

async function extractContent(pageUrl, options = {}) {
  const {
    outputDir = process.cwd(),
    smart = false,
    images = false,
    media = false,
    tables = false,
    lists = false,
    pdf = false,
    translateLang = null,
    force = false,
  } = options;

  console.log(`\n🔗 正在抓取: ${pageUrl}`);

  const ua = CONFIG.userAgents[Math.floor(Math.random() * CONFIG.userAgents.length)];
  
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled'],
  });

  const context = await browser.newContext({
    userAgent: ua,
    viewport: { width: 1920, height: 1080 },
    locale: 'zh-CN',
  });

  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
  });

  const page = await context.newPage();
  await new Promise(r => setTimeout(r, randomDelay()));

  try {
    await page.goto(pageUrl, { waitUntil: 'domcontentloaded', timeout: CONFIG.timeout });
    await page.waitForTimeout(3000);
  } catch {
    await page.goto(pageUrl, { waitUntil: 'commit', timeout: 30000 });
    await page.waitForTimeout(5000);
  }

  // 提取标题
  const title = await page.title();
  console.log(`  📄 标题: ${title}`);

  // 提取内容
  const htmlContent = await page.content();
  
  // Smart模式
  let contentHtml = htmlContent;
  if (smart) {
    console.log('  🧠 Smart模式处理...');
    // 简化处理，使用body内容
    contentHtml = await page.evaluate(() => {
      const body = document.body.cloneNode(true);
      ['script', 'style', 'nav', 'iframe', 'noscript'].forEach(tag => {
        body.querySelectorAll(tag).forEach(n => n.remove());
      });
      return body.innerHTML;
    });
  }

  // 转换Markdown
  const td = buildTurndown();
  let markdown = td.turndown(contentHtml);
  
  // 清理
  markdown = markdown
    .replace(/\n{3,}/g, '\n\n')
    .replace(/^\s+$/gm, '')
    .trim();

  // Frontmatter
  const frontmatter = `---
title: "${title}"
source: ${pageUrl}
date: ${new Date().toISOString()}
---

`;

  markdown = frontmatter + markdown;

  // 生成文件名
  const safeTitle = title.replace(/[<>:"/\\|?*]/g, '').substring(0, 50);
  const filename = `${getTimestamp()}-${safeTitle}.md`;
  const outputPath = path.join(outputDir, filename);

  fs.writeFileSync(outputPath, markdown, 'utf8');
  console.log(`  ✅ 已保存: ${outputPath}`);

  // 多模态提取
  const result = { path: outputPath, title };

  if (images || media) {
    await page.waitForTimeout(1000);
    
    if (images) {
      result.images = await extractImages(page);
    }
    if (media) {
      result.media = await extractMedia(page);
    }
  }

  if (tables) {
    result.tables = await extractTables(page);
  }

  if (lists) {
    result.lists = await extractLists(page);
  }

  // PDF导出
  if (pdf) {
    const pdfPath = outputPath.replace('.md', '.pdf');
    if (convertToPdf(outputPath, pdfPath)) {
      result.pdfPath = pdfPath;
    }
  }

  // 翻译
  if (translateLang) {
    result.translatedText = translateText(markdown.substring(0, 10000), translateLang);
  }

  await browser.close();

  // 追加额外信息到Markdown
  if (result.images && result.images.length > 0) {
    fs.appendFileSync(outputPath, '\n\n---\n\n## 🖼️ 图片资源\n\n');
    result.images.forEach(img => {
      fs.appendFileSync(outputPath, `- [${img.alt || '图片'}](${img.src})\n`);
    });
  }

  if (result.tables && result.tables.length > 0) {
    fs.appendFileSync(outputPath, '\n\n---\n\n## 📊 表格数据\n\n');
    result.tables.forEach((table, i) => {
      fs.appendFileSync(outputPath, `### 表格 ${i + 1}\n\n`);
      table.rows.forEach(row => {
        fs.appendFileSync(outputPath, `| ${row.join(' | ')} |\n`);
      });
      fs.appendFileSync(outputPath, '\n');
    });
  }

  console.log('\n✅ 抓取完成!');
  return result;
}

// ─── 主入口 ────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help') {
    console.log(`
📦 Content Catcher v4.0 - 超强内容抓取

用法:
  node content-extractor.js <url> [选项]

选项:
  --smart      Smart模式(AI内容识别)
  --images     提取图片资源
  --media      提取音视频资源
  --tables     提取表格数据
  --lists      提取列表数据
  --pdf        导出为PDF
  --translate <lang>  翻译(en/jp/ko)
  -o, --output <dir>  输出目录

示例:
  node content-extractor.js https://example.com --smart --images --pdf
  node content-extractor.js https://example.com --tables
`);
    process.exit(0);
  }

  const pageUrl = args[0];
  let outputDir = process.cwd();
  const options = {
    smart: args.includes('--smart'),
    images: args.includes('--images'),
    media: args.includes('--media'),
    tables: args.includes('--tables'),
    lists: args.includes('--lists'),
    pdf: args.includes('--pdf'),
  };

  // 翻译语言
  const translateIdx = args.indexOf('--translate');
  if (translateIdx !== -1 && args[translateIdx + 1]) {
    options.translateLang = args[translateIdx + 1];
  }

  // 输出目录
  const outputIdx = args.indexOf('--output') !== -1 
    ? args.indexOf('--output')
    : args.indexOf('-o');
  if (outputIdx !== -1 && args[outputIdx + 1] && !args[outputIdx + 1].startsWith('--')) {
    outputDir = args[outputIdx + 1];
  }

  options.outputDir = outputDir;

  try {
    await extractContent(pageUrl, options);
  } catch (err) {
    console.error(`❌ 抓取失败: ${err.message}`);
    process.exit(1);
  }
}

main();
