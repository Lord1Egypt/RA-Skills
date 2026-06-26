const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');
const http = require('http');

/**
 * 下载图片到本地
 */
async function downloadImage(url, outputDir, filename) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const filepath = path.join(outputDir, filename);
    
    client.get(url, (res) => {
      if (res.statusCode === 302 || res.statusCode === 301) {
        downloadImage(res.headers.location, outputDir, filename).then(resolve).catch(reject);
        return;
      }
      const file = fs.createWriteStream(filepath);
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(filepath); });
    }).on('error', (err) => {
      fs.unlink(filepath, () => {});
      reject(err);
    });
  });
}

/**
 * 自动查找 Chrome 路径
 */
function findChromePath() {
  if (process.platform === 'win32') {
    const paths = [
      'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
      path.join(os.homedir(), 'AppData', 'Local', 'Google', 'Chrome', 'Application', 'chrome.exe')
    ];
    for (const p of paths) { if (fs.existsSync(p)) return p; }
  } else if (process.platform === 'darwin') {
    const p = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
    if (fs.existsSync(p)) return p;
  } else {
    const paths = ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium-browser', '/usr/bin/chromium'];
    for (const p of paths) { if (fs.existsSync(p)) return p; }
  }
  return null;
}

/**
 * 抓取微信公众号文章
 * @param {Object} options - 配置选项
 * @param {string} options.url - 文章 URL
 * @param {boolean} options.saveToFile - 是否保存文件 (默认 true)
 * @param {string} options.outputDir - 输出目录 (默认当前目录)
 * @param {string} options.chromePath - Chrome 路径 (可选)
 * @param {string} options.format - 输出格式：text|markdown|html (默认 markdown)
 * @param {boolean} options.downloadImages - 是否下载图片 (默认 true)
 * @param {number} options.consoleLimit - 控制台输出字数限制 (默认 0=全部)
 * @returns {Promise<{title, author, time, content, textContent, images, imageCount}>}
 */
async function fetchWechatArticle(options = {}) {
  const {
    url,
    saveToFile = true,
    outputDir = process.cwd(),
    chromePath = findChromePath(),
    format = 'markdown',
    downloadImages = true,
    consoleLimit = 0
  } = options;

  if (!url) throw new Error('缺少文章 URL');
  if (!chromePath) throw new Error('未找到 Chrome 浏览器，请手动指定 chromePath 或安装 Chrome');

  let browser;
  try {
    console.log('🚀 正在启动 Chrome...');
    
    browser = await puppeteer.launch({
      executablePath: chromePath,
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });
    
    console.log('✅ Chrome 已启动');
    
    const page = await browser.newPage();
    
    // 移动端 User-Agent（微信内置浏览器）
    await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50');
    await page.setViewport({ width: 375, height: 812 });
    
    console.log('📖 正在加载文章:', url);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
    console.log('✅ 页面加载完成');
    
    // 等待正文容器出现
    await page.waitForSelector('#js_content, .rich_media_content', { timeout: 10000 })
      .catch(() => console.log('⚠️  未找到标准内容选择器'));
    
    // 等一下让懒加载的图片渲染
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await new Promise(r => setTimeout(r, 1500));
    await page.evaluate(() => window.scrollTo(0, 0));
    
    // ===== 核心提取逻辑（v2：递归 DOM 遍历）=====
    const articleData = await page.evaluate(() => {
      // 检查文章状态
      const bodyText = document.body.innerText;
      if (bodyText.includes('该内容已被发布者删除') || bodyText.includes('此内容因违规无法查看')) {
        return { error: '文章已被删除或违规下架' };
      }

      // 元信息
      const titleEl = document.querySelector('#activity-name');
      const title = titleEl?.innerText?.trim() || document.title || '无标题';
      const author = document.querySelector('.rich_media_meta_nickname')?.innerText?.trim() 
                  || document.querySelector('#js_name')?.innerText?.trim() || '未知';
      const time = document.querySelector('#publish_time')?.innerText?.trim()
                || document.querySelector('.rich_media_meta_text')?.innerText?.trim() || '未知';

      // 找到正文容器
      const contentEl = document.querySelector('#js_content') 
                     || document.querySelector('.rich_media_content')
                     || document.querySelector('.rich_media_area_primary')
                     || document.querySelector('article');
      
      if (!contentEl) {
        return { error: '未找到正文容器' };
      }

      // ---- 方法1：innerText 一次性获取全部纯文本（最可靠，绝不丢内容）----
      const fullText = contentEl.innerText?.trim() || '';

      // ---- 方法2：递归遍历 DOM 生成 Markdown ----
      const images = [];
      
      function walkNode(node, depth = 0) {
        if (!node) return '';
        
        // 跳过隐藏元素
        if (node.nodeType === 1) {
          const style = window.getComputedStyle(node);
          if (style.display === 'none' || style.visibility === 'hidden') return '';
        }
        
        // 文本节点
        if (node.nodeType === 3) {
          return node.textContent || '';
        }
        
        // 非元素节点跳过
        if (node.nodeType !== 1) return '';
        
        const tag = node.tagName.toLowerCase();
        
        // 跳过脚本、样式
        if (tag === 'script' || tag === 'style' || tag === 'noscript') return '';
        
        // 图片
        if (tag === 'img' || tag === 'mp-img' || tag === 'weixin-img') {
          const src = node.getAttribute('data-src') 
                   || node.getAttribute('data-original')
                   || node.getAttribute('src');
          if (src && src.startsWith('http') && !images.includes(src)) {
            images.push(src);
          }
          const idx = images.indexOf(src);
          const alt = node.getAttribute('alt') || `图片 ${idx + 1}`;
          return `\n![${alt}](${src})\n`;
        }
        
        // 换行
        if (tag === 'br') return '\n';
        
        // 水平线
        if (tag === 'hr') return '\n\n---\n\n';
        
        // 递归获取子节点内容
        let childContent = '';
        for (const child of node.childNodes) {
          childContent += walkNode(child, depth + 1);
        }
        
        // 如果没有实际内容，跳过
        const trimmed = childContent.trim();
        if (!trimmed) return '';
        
        // 标题
        const headingMatch = tag.match(/^h([1-6])$/);
        if (headingMatch) {
          const level = parseInt(headingMatch[1]);
          return '\n\n' + '#'.repeat(level) + ' ' + trimmed + '\n\n';
        }
        
        // 段落
        if (tag === 'p') return '\n\n' + trimmed + '\n\n';
        
        // 列表
        if (tag === 'ul' || tag === 'ol') return '\n' + childContent + '\n';
        if (tag === 'li') {
          const parent = node.parentElement?.tagName?.toLowerCase();
          if (parent === 'ol') {
            const idx = Array.from(node.parentElement.children).indexOf(node) + 1;
            return `${idx}. ${trimmed}\n`;
          }
          return `- ${trimmed}\n`;
        }
        
        // 粗体
        if (tag === 'strong' || tag === 'b') return `**${trimmed}**`;
        
        // 斜体
        if (tag === 'em' || tag === 'i') return `*${trimmed}*`;
        
        // 链接
        if (tag === 'a') {
          const href = node.getAttribute('href');
          if (href && !href.startsWith('javascript:')) {
            return `[${trimmed}](${href})`;
          }
          return trimmed;
        }
        
        // 引用
        if (tag === 'blockquote') return '\n\n> ' + trimmed.replace(/\n/g, '\n> ') + '\n\n';
        
        // 代码块
        if (tag === 'pre') return '\n\n```\n' + trimmed + '\n```\n\n';
        if (tag === 'code') return '`' + trimmed + '`';
        
        // div/section/span 等容器：直接返回子内容
        return childContent;
      }
      
      let markdownRaw = walkNode(contentEl);
      
      // 清理：合并连续空行为最多2个
      markdownRaw = markdownRaw.replace(/\n{3,}/g, '\n\n').trim();
      
      // 提取页面内所有图片（补漏）
      if (images.length === 0) {
        contentEl.querySelectorAll('img[data-src], img[src], mp-img[data-src]').forEach(img => {
          const src = img.getAttribute('data-src') || img.getAttribute('src');
          if (src && src.startsWith('http') && !images.includes(src)) {
            images.push(src);
          }
        });
      }

      return {
        title,
        author,
        time,
        content: markdownRaw,
        textContent: fullText,
        images,
        htmlContent: contentEl.innerHTML
      };
    });

    if (articleData.error) {
      throw new Error(`页面异常: ${articleData.error}`);
    }
    
    // ===== 输出信息 =====
    const wordCount = articleData.textContent.length;
    console.log('\n📄 ========== 文章信息 ==========\n');
    console.log('标题:', articleData.title);
    console.log('作者:', articleData.author);
    console.log('时间:', articleData.time);
    console.log('字数:', wordCount);
    console.log('图片:', articleData.images?.length || 0, '张');
    console.log('\n📝 ========== 文章内容 ==========\n');
    
    // 控制台输出（默认全部，可限制）
    if (consoleLimit > 0 && articleData.textContent.length > consoleLimit) {
      console.log(articleData.textContent.substring(0, consoleLimit));
      console.log(`\n... (共 ${wordCount} 字，已显示前 ${consoleLimit} 字)`);
    } else {
      console.log(articleData.textContent);
    }
    console.log('\n========== 文章结束 ==========\n');
    
    // ===== 下载图片 =====
    const downloadedImages = [];
    if (downloadImages && articleData.images && articleData.images.length > 0) {
      console.log(`🖼️  正在下载 ${articleData.images.length} 张图片...`);
      const imagesDir = path.join(outputDir, 'images');
      if (saveToFile && !fs.existsSync(imagesDir)) {
        fs.mkdirSync(imagesDir, { recursive: true });
      }
      
      for (let i = 0; i < articleData.images.length; i++) {
        const imgUrl = articleData.images[i];
        try {
          const ext = path.extname(new URL(imgUrl).pathname) || '.jpg';
          const filename = `image_${i + 1}${ext}`;
          if (saveToFile) {
            const imgPath = await downloadImage(imgUrl, imagesDir, filename);
            downloadedImages.push({ originalUrl: imgUrl, localPath: imgPath, filename });
            console.log(`  ✅ ${filename}`);
          } else {
            downloadedImages.push({ originalUrl: imgUrl, localPath: null, filename });
          }
        } catch (err) {
          console.log(`  ❌ 下载失败：${err.message}`);
        }
      }
    }
    
    // ===== 保存文件 =====
    if (saveToFile) {
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }
      
      const timestamp = Date.now();
      // 用标题生成文件名（去掉特殊字符，截断到30字）
      const safeTitle = articleData.title
        .replace(/[\\/:*?"<>|]/g, '')
        .replace(/\s+/g, '_')
        .substring(0, 30);
      
      let filename, content;
      
      if (format === 'html') {
        filename = `${safeTitle}-${timestamp}.html`;
        content = `<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>${articleData.title}</title></head>\n<body>\n<h1>${articleData.title}</h1>\n<p>作者：${articleData.author} | 时间：${articleData.time}</p>\n${articleData.htmlContent}\n</body></html>`;
      } else if (format === 'markdown') {
        filename = `${safeTitle}-${timestamp}.md`;
        content = `# ${articleData.title}\n\n**作者**: ${articleData.author}  \n**时间**: ${articleData.time}  \n**字数**: 约 ${wordCount} 字\n\n---\n\n${articleData.content}`;
      } else {
        filename = `${safeTitle}-${timestamp}.txt`;
        content = `标题：${articleData.title}\n作者：${articleData.author}\n时间：${articleData.time}\n字数：${wordCount}\n\n${articleData.textContent}`;
      }
      
      const filepath = path.join(outputDir, filename);
      fs.writeFileSync(filepath, content, 'utf8');
      console.log(`💾 已保存：${filepath}`);
      
      // 图片清单
      if (downloadedImages.length > 0) {
        const manifestPath = path.join(outputDir, `images-${timestamp}.json`);
        fs.writeFileSync(manifestPath, JSON.stringify(downloadedImages, null, 2), 'utf8');
      }
    }
    
    await browser.close();
    console.log('🔒 浏览器已关闭');
    
    return {
      title: articleData.title,
      author: articleData.author,
      time: articleData.time,
      content: articleData.content,
      textContent: articleData.textContent,
      images: downloadedImages.length > 0 ? downloadedImages : articleData.images,
      imageCount: articleData.images?.length || 0
    };
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    if (browser) await browser.close();
    throw error;
  }
}

// 命令行入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const url = args.find(a => !a.startsWith('-'));
  const noSave = args.includes('--no-save');
  const format = args.find(a => a.startsWith('--format='))?.split('=')[1] || 'markdown';
  const noImages = args.includes('--no-images');
  const limitArg = args.find(a => a.startsWith('--limit='));
  const consoleLimit = limitArg ? parseInt(limitArg.split('=')[1]) : 0;
  
  if (!url) {
    console.log(`
微信公众号文章抓取工具 v2.0

用法：node fetch-wechat-article.js <文章URL> [选项]

选项：
  --no-save       不保存文件（默认保存到当前目录）
  --format=TYPE   输出格式：text|markdown|html（默认 markdown）
  --no-images     不下载图片
  --limit=N       控制台只显示前 N 字（默认全部显示）

示例：
  node fetch-wechat-article.js https://mp.weixin.qq.com/s/xxx
  node fetch-wechat-article.js https://mp.weixin.qq.com/s/xxx --format=html
  node fetch-wechat-article.js https://mp.weixin.qq.com/s/xxx --no-save --limit=500
`);
    process.exit(1);
  }
  
  fetchWechatArticle({
    url,
    saveToFile: !noSave,
    format,
    downloadImages: !noImages,
    consoleLimit
  })
    .then((result) => {
      console.log(`\n✅ 抓取完成 | ${result.title} | ${result.textContent.length} 字 | ${result.imageCount} 张图片`);
    })
    .catch((error) => {
      console.error('❌ 抓取失败:', error.message);
      process.exit(1);
    });
}

module.exports = { fetchWechatArticle };
