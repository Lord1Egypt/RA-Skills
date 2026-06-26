#!/usr/bin/env node
/**
 * markdown-clip - CLI 网页转 Markdown（虾抓抓 v2.1.3）
 * 新增 --smart 模式：AI 内容识别（Readability）
 *
 * 用法: node markdown-clip.js <url> [输出目录] [--force] [--smart]
 */

const { chromium } = require('playwright');
const TurndownService = require('turndown');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { execSync } = require('child_process');
const os = require('os');

// ─── 分析器 ───────────────────────────────────────────────

function analyzeMarkdown(filePath) {
  const skillDir = path.dirname(__filename);
  const scriptPath = path.join(skillDir, 'analyzer.py');
  try {
    const result = execSync(
      `python "${scriptPath}" --file "${filePath}" --json`,
      { timeout: 30000, encoding: 'utf-8', errors: 'replace' }
    );
    return JSON.parse(result);
  } catch (err) {
    console.log(`  [analyze] 分析失败: ${err.message}`);
    return null;
  }
}

function buildAnalysisSection(analysis) {
  if (!analysis) return '';
  const lines = ['\n---\n\n## 📋 文章分析\n'];
  if (analysis.summary) {
    lines.push(`**摘要：** ${analysis.summary}\n`);
  }
  if (analysis.keywords && analysis.keywords.length > 0) {
    lines.push(`**关键词：** ${analysis.keywords.join(' / ')}\n`);
  }
  if (analysis.insights && analysis.insights.length > 0) {
    lines.push(`\n**关键洞察：**\n`);
    analysis.insights.forEach(insight => {
      lines.push(`- ${insight}\n`);
    });
  }
  lines.push(`\n> 📊 字数 ${analysis.char_count} | 句子 ${analysis.sentences_count} | 预计阅读 ${analysis.reading_time_minutes} 分钟\n`);
  return lines.join('');
}

const lib = require('./clip-lib');

const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
];

// ─── Smart 模式：Readability AI 内容识别 ──────────────────────
// "教它识字"模式：用算法自动识别主内容区域，不依赖预设选择器

function smartExtract(pageUrl, htmlContent) {
  const tmpDir = os.tmpdir();
  const tmpFile = path.join(tmpDir, `xiazhua-${Date.now()}.html`);
  fs.writeFileSync(tmpFile, htmlContent, 'utf8');

  const skillDir = path.dirname(__filename);
  const scriptPath = path.join(skillDir, 'smart-extract.py');

  try {
    const result = execSync(
      `python "${scriptPath}" --url "${pageUrl}" --html-file "${tmpFile}" --json`,
      { timeout: 30000, encoding: 'utf-8', errors: 'replace' }
    );
    const data = JSON.parse(result);
    return {
      html: data.content || '',
      title: data.title || '',
      excerpt: data.excerpt || '',
    };
  } catch (err) {
    console.log(`  [smart] readability 提取失败: ${err.message}`);
    return null;
  } finally {
    try { fs.unlinkSync(tmpFile); } catch {}
  }
}

// ─── 元数据提取 ────────────────────────────────────────────────

async function extractMetadata(page) {
  const getMeta = async (selectors) => {
    for (const sel of selectors) {
      try {
        const el = await page.$(sel);
        if (el) {
          const content = await el.getAttribute('content');
          if (content) return content;
        }
      } catch {}
    }
    return null;
  };

  const isWeChat = page.url().includes('mp.weixin.qq.com');
  if (isWeChat) {
    try {
      const wcMeta = await page.evaluate(() => {
        const get = (sel) => {
          const el = document.querySelector(sel);
          return el ? el.getAttribute('content') : null;
        };
        return {
          title: get('meta[property="og:title"]') || document.querySelector('#activity-name')?.innerText?.trim(),
          author: get('meta[name="author"]') || document.querySelector('#js_name')?.innerText?.trim(),
          description: get('meta[name="description"]') || get('meta[property="og:description"]'),
          cover: get('meta[property="og:image"]'),
        };
      });
      if (wcMeta.title || wcMeta.author) return wcMeta;
    } catch {}
  }

  return {
    title: await getMeta(['meta[property="og:title"]', 'meta[name="twitter:title"]']),
    author: await getMeta(['meta[name="author"]', 'meta[property="article:author"]']),
    description: await getMeta(['meta[property="og:description"]', 'meta[name="description"]']),
    cover: await getMeta(['meta[property="og:image"]', 'meta[name="twitter:image"]']),
  };
}

async function extractContent(page) {
  const selectors = [
    'article', '[role="main"]', 'main',
    '.post-content', '.article-content', '.entry-content', '.content', '#content',
    '#js_content',
    '.post', '.article', '.story',
    '.main-content', '.page-content',
    '.container', '.article-container',
    '.article-detail', '.article-cont', '.detail-content',
    '.detail', '.article-body',
  ];

  for (const sel of selectors) {
    try {
      const el = await page.$(sel);
      if (el) {
        const html = await page.evaluate((element) => {
          const clone = element.cloneNode(true);
          const junk = [
            'script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'noscript',
            '.login-banner', '.login-tip', '.login-bar',
            '[class*="login"]', '[class*="register"]',
            '[class*="sidebar"]', '[class*="related"]', '[class*="recommend"]',
            '[class*="advertisement"]', '[class*="ads"]', '[class*="track"]',
            '[class*="mathjax"]', '[class*="MathJax"]', '[class*="loading"]',
            '[id*="login"]', '[id*="sidebar"]',
            'form[action]', '.comments', '.comment',
            '.footer', '.header', '.nav',
            '.follow-bar', '.share-bar', '.action-bar',
            '.tags', '.tag-list',
            '#js_pc_qr_code', '.qr_code', '.qrcode',
          ];
          junk.forEach(sel => {
            try { clone.querySelectorAll(sel).forEach(n => n.remove()); } catch {}
          });
          clone.querySelectorAll('a[href=""], a[href="#"]').forEach(a => {
            const text = a.textContent.trim();
            a.replaceWith(document.createTextNode(text));
          });
          return clone.innerHTML;
        }, el);
        if (html && html.replace(/<[^>]+>/g, '').length > 200) {
          return html;
        }
      }
    } catch {}
  }

  return await page.evaluate(() => {
    const body = document.body.cloneNode(true);
    ['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'noscript',
     '.login-banner', '.login-tip', '.login-bar', '[class*="login"]', '[class*="sidebar"]',
     '[class*="related"]', '[class*="recommend"]', '[class*="advertisement"]',
     '[class*="mathjax"]', '[class*="MathJax"]', '[class*="loading"]',
     'form[action]', '.comments', '.comment', '.footer', '.header', '.nav',
     '.follow-bar', '.share-bar', '.action-bar'
    ].forEach(sel => {
      try { body.querySelectorAll(sel).forEach(n => n.remove()); } catch {}
    });
    return body.innerHTML;
  });
}

// ─── Turndown 规则 ────────────────────────────────────────────

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

  td.addRule('links', {
    filter: 'a',
    replacement: (content, node) => {
      const href = node.href || '';
      const text = node.innerText || content;
      if (!href || href === '#' || href === node.baseURI) return text;
      return `[${text}](${href})`;
    },
  });

  td.keep(['table']);

  return td;
}

// ─── Frontmatter ──────────────────────────────────────────────

function buildFrontmatter(metadata, pageUrl) {
  const lines = ['---'];
  if (metadata.title) lines.push(`title: "${metadata.title.replace(/"/g, '\\"')}"`);
  if (metadata.author) lines.push(`author: "${metadata.author.replace(/"/g, '\\"')}"`);
  if (metadata.description) lines.push(`description: "${metadata.description.replace(/"/g, '\\"')}"`);
  if (metadata.cover) lines.push(`cover: "${metadata.cover}"`);
  lines.push(`source: ${pageUrl}`);
  lines.push(`clipped: ${new Date().toISOString()}`);
  lines.push('---', '');
  return lines.join('\n');
}

// ─── 清理 Markdown ─────────────────────────────────────────────

function cleanMarkdown(md) {
  return md
    .replace(/\n{3,}/g, '\n\n')
    .replace(/^\s+$/gm, '')
    .replace(/Loading .*MathJax.*/gi, '')
    .replace(/\[MathJax\].*/gi, '')
    .replace(/\[\]\([^)]*\?ad_trace=[^)]*\)/g, '')
    .replace(/\[[^\]]*\]\([^)]*utm_[^)]*\)/g, '')
    .replace(/\[[^\]]*\]\([^)]*fromSource=[^)]*\)/g, '')
    .replace(/^\[\]\(.*\)\s*$/gm, '')
    .replace(/^\[Login\/Register\].*/gm, '')
    .replace(/^\[首页\]\[\/.\].*/gm, '')
    .replace(/^\[建议反馈\].*/gm, '')
    .replace(/^\[文档\].*/gm, '')
    .replace(/^\[控制台\].*/gm, '')
    .replace(/^\*\*作者相关精选\*\*/gm, '')
    .replace(/^\[关注作者\].*/gm, '')
    .replace(/^\[\]\(#\)\s*$/gm, '')
    .trim();
}

// ─── 核心抓取 ────────────────────────────────────────────────

async function clipUrl(pageUrl, options = {}) {
  const {
    outputDir = '',
    timeout = 60000,
    force = false,
    skipDuplicates = true,
    smart = false,
  } = options;

  const normalizedUrl = lib.normalizeUrl(pageUrl);

  if (skipDuplicates && !force) {
    const existing = lib.findClip(normalizedUrl);
    if (existing) {
      console.log(`⏭️  已抓过，跳过: ${pageUrl}`);
      console.log(`   上次保存于: ${existing.clippedAt}`);
      console.log(`   路径: ${existing.path}`);
      return { skipped: true, existing };
    }
  }

  console.log(`🔗 正在抓取: ${pageUrl}`);

  const ua = USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled',
           '--no-first-run', '--no-zygote', '--disable-gpu'],
  });

  const context = await browser.newContext({
    userAgent: ua,
    viewport: { width: 1920, height: 1080 },
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    permissions: [],
  });

  // 反爬：隐藏 webdriver 标志（标准做法，不触发 AV）
  // 移除了过度指纹伪造（callPhantom/permissions.mock/window.chrome）
  // 这些是病毒常用技术，会被识别为恶意软件
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
  });

  const page = await context.newPage();
  await new Promise(r => setTimeout(r, Math.floor(Math.random() * 2000) + 1000));

  try {
    await page.goto(pageUrl, { waitUntil: 'domcontentloaded', timeout });
    await page.waitForTimeout(3000);
  } catch {
    console.log('  加载超时，尝试降级...');
    await page.goto(pageUrl, { waitUntil: 'commit', timeout: 30000 });
    await page.waitForTimeout(5000);
  }

  try {
    const metadata = await extractMetadata(page);

    // Smart 模式：先用 readability AI 识别主内容
    let htmlContent = null;
    let usedSmart = false;

    if (smart) {
      console.log('  🧠 Smart 模式：Readability AI 内容识别...');
      const rawHtml = await page.content();
      const smartResult = smartExtract(pageUrl, rawHtml);
      if (smartResult && smartResult.html) {
        htmlContent = smartResult.html;
        usedSmart = true;
        if (smartResult.title && !metadata.title) metadata.title = smartResult.title;
        console.log(`  ✅ Smart 提取成功`);
      }
    }

    // 标准模式或 Smart 回退
    if (!htmlContent) {
      htmlContent = await extractContent(page);
    }

    const td = buildTurndown();
    let markdown = td.turndown(htmlContent);
    markdown = cleanMarkdown(markdown);

    const frontmatter = buildFrontmatter(metadata, pageUrl);
    markdown = frontmatter + markdown;

    const filename = lib.buildFilename(pageUrl, metadata.title, '.md');
    const outDir = outputDir || process.cwd();
    const outputPath = path.join(outDir, filename);

    fs.writeFileSync(outputPath, markdown, 'utf8');

    const charCount = markdown.replace(/---[\s\S]*?---\n/, '').length;

    lib.recordClip(pageUrl, { path: outputPath, metadata });

    console.log(`✅ 已保存: ${outputPath}`);
    console.log(`📄 标题: ${metadata.title || '无标题'}`);
    console.log(`📝 字数: ${charCount} 字符`);
    if (usedSmart) console.log(`  🧠 模式: Smart Readability（自动识别内容区域）`);

    await browser.close();
    return { success: true, path: outputPath, markdown, metadata, charCount, smart: usedSmart };
  } catch (err) {
    await browser.close();
    throw err;
  }
}

// ─── 主入口 ──────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args[0] === '--config') {
    const cfg = lib.loadConfig();
    console.log('📋 当前配置:');
    console.log(JSON.stringify(cfg, null, 2));
    console.log(`\n配置文件: ${lib.getConfigPath()}`);
    return;
  }

  if (args[0] === '--log') {
    const log = lib.loadClipsLog();
    const entries = Object.values(log);
    console.log(`📋 Clip Log (共 ${entries.length} 条)\n`);
    entries.slice(-10).reverse().forEach(e => {
      console.log(`[${e.clippedAt.slice(0, 10)}] ${e.title || '无标题'}`);
      console.log(`  ${e.url}`);
      console.log(`  → ${e.path}\n`);
    });
    return;
  }

  if (args[0] === '--set') {
    const cfg = lib.loadConfig();
    const key = args[1];
    const value = args[2];
    if (!key || value === undefined) {
      console.error('用法: --set <key> <value>');
      process.exit(1);
    }
    cfg[key] = value;
    lib.saveConfig(cfg);
    console.log(`✅ 已设置 ${key} = ${value}`);
    return;
  }

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(`
🛍️  markdown-clip - 网页转 Markdown（虾抓抓 v2.1.3）

新增 --smart 模式：
  用 Readability 算法自动识别网页主内容区域
  不依赖预设 CSS 选择器，真正"教它识字"

用法:
  node markdown-clip.js <url> [输出目录] [选项]

选项:
  --force        强制重新抓取
  --smart        AI 模式：用 Readability 自动识别内容（推荐）
  --analyze      抓取后自动分析文章（摘要 + 关键词 + 关键洞察）
  --config       查看配置
  --log          查看抓取历史
  --set <k> <v> 设置配置

示例:
  node markdown-clip.js https://mp.weixin.qq.com/s/xxxxx
  node markdown-clip.js https://example.com --smart
  node markdown-clip.js https://example.com --analyze

批量:
  node batch-clip.js <url文件> [并发数] [输出目录]
`);
    process.exit(0);
  }

  const pageUrl = args[0];
  let outputDir = '';
  let force = false;
  let smart = false;

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--force') { force = true; continue; }
    if (args[i] === '--smart') { smart = true; continue; }
    if (args[i] === '--analyze') { continue; } // 在主流程处理
    if (!args[i].startsWith('--')) outputDir = args[i];
  }

  const cfg = lib.loadConfig();
  if (!outputDir && cfg.outputDir) outputDir = cfg.outputDir;

  try {
    new url.URL(pageUrl);
  } catch {
    console.error('❌ 无效的URL');
    process.exit(1);
  }

  try {
    const result = await clipUrl(pageUrl, { outputDir, force, skipDuplicates: cfg.skipDuplicates, smart });
    if (result.skipped) process.exit(0);

    // 分析模式
    if (args.includes('--analyze')) {
      console.log('\n🧠 正在分析文章...');
      const analysis = analyzeMarkdown(result.path);
      if (analysis) {
        const section = buildAnalysisSection(analysis);
        fs.appendFileSync(result.path, section, 'utf8');
        console.log('  ✅ 分析完成，已追加到文件末尾');
        console.log(`  关键词: ${analysis.keywords.join(' / ')}`);
        console.log(`  摘要: ${analysis.summary.substring(0, 100)}...`);
      } else {
        console.log('  ⚠️ 分析未能完成');
      }
    }
  } catch (err) {
    console.error(`❌ 抓取失败: ${err.message}`);
    process.exit(1);
  }
}

main();
