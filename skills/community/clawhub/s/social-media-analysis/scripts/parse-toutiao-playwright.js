#!/usr/bin/env node
/**
 * 今日头条文章图片提取脚本（Playwright 渲染版）
 * 功能：使用 Playwright 渲染页面后提取并下载图片
 * 
 * 适用场景：
 * - 静态脚本 (parse-toutiao.js) 无法提取图片时
 * - 页面需要 JavaScript 动态加载内容
 * 
 * 用法：
 *   node scripts/parse-toutiao-playwright.js <文章 URL> [输出目录]
 * 
 * 示例：
 *   node scripts/parse-toutiao-playwright.js "https://www.toutiao.com/w/7620088161695253044" ./output
 * 
 * 前置准备：
 *   npm install playwright
 *   npx playwright install chromium
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { buildAnalysis } = require('./build-content-analysis');

// 解析命令行参数
const args = process.argv.slice(2);
const URL = args[0];
const OUTPUT_DIR = args[1] || './toutiao-output';

if (!URL) {
  console.log('用法：node parse-toutiao-playwright.js <文章 URL> [输出目录]');
  console.log('示例：node parse-toutiao-playwright.js "https://www.toutiao.com/w/xxx" ./output');
  process.exit(1);
}

// 创建输出目录
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log(`开始解析今日头条：${URL}`);
console.log(`输出目录：${OUTPUT_DIR}`);
console.log('---');

// 主函数
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('加载页面...');
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(5000); // 等待图片完全加载
  
  // 提取文章信息和图片
  const content = await page.evaluate(() => {
    const article = document.querySelector('article') || 
                    document.querySelector('.article') || 
                    document.body;
    const title = document.querySelector('h1')?.textContent || '未知标题';
    
    // 提取所有文章相关图片（过滤小图）
    const allImages = Array.from(document.querySelectorAll('img'))
      .map(img => ({ 
        src: img.src, 
        width: img.width, 
        height: img.height,
        alt: img.alt 
      }))
      .filter(img => 
        img.src.includes('toutiaoimg.com') && 
        img.width > 100 && 
        img.height > 100
      );
    
    return { title, images: allImages };
  });
  
  console.log(`标题：${content.title}`);
  console.log(`找到图片：${content.images.length}`);
  
  if (content.images.length === 0) {
    console.log('\n⚠️ 未找到符合条件的图片');
    console.log('可能原因：');
    console.log('  1. 文章本身没有图片');
    console.log('  2. 图片 URL 不包含 toutiaoimg.com');
    console.log('  3. 页面加载失败');
    await browser.close();
    process.exit(1);
  }
  
  // 下载前 5 张大图
  const downloadCount = Math.min(content.images.length, 5);
  console.log(`\n开始下载前 ${downloadCount} 张图片...\n`);
  
  const results = [];
  for (let i = 0; i < downloadCount; i++) {
    const img = content.images[i];
    const filename = path.join(OUTPUT_DIR, `image-${String(i+1).padStart(2, '0')}.jpg`);
    
    console.log(`下载 ${i+1}/${downloadCount}...`);
    
    try {
      // 通过浏览器上下文下载图片（绕过防盗链）
      const imgData = await page.evaluate(async (imgUrl) => {
        const res = await fetch(imgUrl);
        const blob = await res.blob();
        const reader = new FileReader();
        return new Promise((resolve, reject) => {
          reader.onloadend = () => resolve(reader.result.split(',')[1]);
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });
      }, img.src);
      
      fs.writeFileSync(filename, Buffer.from(imgData, 'base64'));
      const size = (fs.statSync(filename).size / 1024).toFixed(1);
      console.log(`✅ image-${String(i+1).padStart(2, '0')}.jpg (${size}KB)`);
      results.push({ index: i+1, filename, size: `${size}KB` });
    } catch (err) {
      console.log(`❌ [${i+1}/${downloadCount}] 下载失败：${err.message}`);
    }
  }
  
  await browser.close();
  
  // 输出结果
  console.log('\n---');
  console.log('下载完成！');
  const visualSummary = results.length > 0
    ? `下载 ${results.length} 张文章配图`
    : '未下载到配图';
  const analysis = buildAnalysis({
    title: content.title || '',
    text: '',
    platform: '今日头条',
    mediaType: '图片',
    visual: visualSummary,
    maxChars: 100,
  });
  console.log(JSON.stringify({
    title: content.title,
    totalImages: content.images.length,
    downloaded: results.length,
    outputDir: OUTPUT_DIR,
    images: results,
    content_analysis: analysis.analysis,
    analysis_score: analysis.score,
    analysis_evidence: analysis.evidence,
  }, null, 2));
  
})().catch(err => {
  console.log('❌ 错误:', err.message);
  process.exit(1);
});
