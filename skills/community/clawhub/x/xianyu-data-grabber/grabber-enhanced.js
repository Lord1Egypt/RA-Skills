#!/usr/bin/env node
/**
 * 增强版闲鱼数据抓取脚本
 * - 60+ 关键词
 * - 增强 OCR 识别
 * - 结构化数据输出
 * - 数据质量验证
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG_PATH = path.join(__dirname, '../../.xianyu-grabber-config.json');
const KEYWORDS_PATH = path.join(__dirname, 'keywords-full.json');

function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  }
  return {
    gitee: { token: '', owner: '', repo: '' },
    xianyu: { cookie: '' },
    grabber: { screenshotDir: 'legion/screenshots', dataDir: 'legion/data' }
  };
}

async function main() {
  const args = process.argv.slice(2);
  const config = loadConfig();
  
  console.log('🐾 闲鱼数据抓取工具 v2.0（增强版）\n');
  
  // 加载关键词
  let keywordsConfig = {};
  if (fs.existsSync(KEYWORDS_PATH)) {
    keywordsConfig = JSON.parse(fs.readFileSync(KEYWORDS_PATH, 'utf8'));
  }
  
  // 确定要抓取的关键词
  let categories = Object.keys(keywordsConfig);
  if (args.length > 0 && !args.includes('--all')) {
    categories = args.filter(a => !a.startsWith('--'));
  }
  
  const allKeywords = [];
  for (const cat of categories) {
    if (keywordsConfig[cat]) {
      allKeywords.push(...keywordsConfig[cat]);
    } else {
      allKeywords.push(cat); // 直接作为关键词
    }
  }
  
  console.log(`📋 分类：${categories.length} 个`);
  console.log(`🔑 关键词：${allKeywords.length} 个\n`);
  
  // 确保目录存在
  const screenshotDir = path.join(__dirname, '../../', config.grabber.screenshotDir || 'legion/screenshots');
  const dataDir = path.join(__dirname, '../../', config.grabber.dataDir || 'legion/data');
  fs.mkdirSync(screenshotDir, { recursive: true });
  fs.mkdirSync(dataDir, { recursive: true });
  
  // 启动浏览器
  console.log('🚀 启动浏览器...');
  const browser = await chromium.launch({
    headless: true,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=1920,1080',
      '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ]
  });
  
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai'
  });
  
  const page = await context.newPage();
  
  // 注入伪装脚本
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [{ name: 'Chrome PDF Plugin' }] });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
  });
  
  // 加载 Cookie
  if (config.xianyu && config.xianyu.cookie && config.xianyu.cookie.length > 10) {
    const cookies = config.xianyu.cookie.split(';').map(c => {
      const parts = c.trim().split('=');
      if (parts.length >= 2) {
        return { 
          name: parts[0].trim(), 
          value: parts.slice(1).join('=').trim(), 
          domain: '.goofish.com', 
          path: '/' 
        };
      }
      return null;
    }).filter(c => c !== null);
    
    if (cookies.length > 0) {
      await context.addCookies(cookies);
      console.log('✅ Cookie 已加载\n');
    } else {
      console.log('⚠️ Cookie 格式无效，跳过\n');
    }
  } else {
    console.log('⚠️ 未配置 Cookie，使用匿名模式\n');
  }
  
  // 抓取数据
  const allResults = [];
  const stats = { success: 0, failed: 0, detected: 0 };
  
  for (let i = 0; i < allKeywords.length; i++) {
    const keyword = allKeywords[i];
    const progress = `[${i+1}/${allKeywords.length}]`;
    console.log(`${progress} 搜索：${keyword}`);
    
    try {
      // 访问首页再搜索
      await page.goto('https://www.goofish.com/', { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000 + Math.random() * 1000); // 随机延迟
      
      const searchInput = await page.$('input[placeholder*="搜索"], input[type="text"]');
      if (searchInput) {
        await searchInput.fill(keyword);
        await searchInput.press('Enter');
        await page.waitForTimeout(4000 + Math.random() * 2000);
      } else {
        await page.goto(`https://www.goofish.com/search?keyword=${encodeURIComponent(keyword)}`, {
          waitUntil: 'domcontentloaded',
          timeout: 30000
        });
        await page.waitForTimeout(3000);
      }
      
      // 截图（更高分辨率）
      const screenshotPath = path.join(screenshotDir, `xianyu-${keyword.replace(/[/\\:*?"<>|]/g, '_')}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true, type: 'png' });
      
      // 检查是否被拦截
      const content = await page.content();
      if (content.includes('非法访问')) {
        console.log(`  ❌ 被检测到`);
        stats.detected++;
        continue;
      }
      
      console.log(`  📸 截图：${path.basename(screenshotPath)}`);
      allResults.push({ keyword, screenshot: screenshotPath, category: categories[Math.floor(i / (allKeywords.length / categories.length))] || 'unknown' });
      stats.success++;
      
    } catch (err) {
      console.log(`  ❌ 错误：${err.message}`);
      stats.failed++;
    }
    
    // 随机延迟，避免被封
    const delay = 2000 + Math.random() * 2000;
    await page.waitForTimeout(delay);
  }
  
  await browser.close();
  
  // 保存截图列表
  const screenshotsList = path.join(dataDir, 'screenshots-list-enhanced.json');
  fs.writeFileSync(screenshotsList, JSON.stringify(allResults, null, 2));
  console.log(`\n📸 截图统计:`);
  console.log(`  ✅ 成功：${stats.success}`);
  console.log(`  ❌ 失败：${stats.failed}`);
  console.log(`  ⚠️ 被检测：${stats.detected}`);
  console.log(`  📂 保存：${screenshotsList}`);
  
  // 增强 OCR
  console.log('\n🔍 增强 OCR 识别（图像预处理 + 多模式）...\n');
  
  const ocrResults = [];
  const pythonScript = path.join(__dirname, 'ocr-enhanced.py');
  
  for (const item of allResults) {
    try {
      try {
        const output = execSync(
          `python3 ${pythonScript} "${item.screenshot}" 2>/dev/null`,
          { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024, timeout: 60000 }
        );
        
        // 解析纯 JSON 输出
        const data = JSON.parse(output.trim());
        ocrResults.push({
          keyword: item.keyword,
          category: item.category,
          products: data.products || [],
          count: data.count || 0
        });
        console.log(`  ${item.keyword.padEnd(15)} ${data.count || 0} 个商品`);
      } catch (err) {
        console.log(`  ${item.keyword.padEnd(15)} OCR 失败：${err.message}`);
        ocrResults.push({ keyword: item.keyword, category: item.category, products: [], count: 0 });
      }
      
    } catch (err) {
      console.log(`  ${item.keyword.padEnd(15)} 错误：${err.message}`);
      ocrResults.push({ keyword: item.keyword, category: item.category, products: [], count: 0 });
    }
  }
  
  // 保存完整数据
  const fullDataPath = path.join(dataDir, 'xianyu-full-data-enhanced.json');
  fs.writeFileSync(fullDataPath, JSON.stringify(ocrResults, null, 2));
  console.log(`\n💾 数据已保存：${fullDataPath}`);
  
  // 生成统计报告
  const statsPath = path.join(dataDir, 'xianyu-stats.json');
  const statsReport = {
    timestamp: new Date().toISOString(),
    totalKeywords: allKeywords.length,
    totalProducts: ocrResults.reduce((sum, r) => sum + r.count, 0),
    categories: {},
    quality: {
      withPrice: ocrResults.reduce((sum, r) => sum + r.products.filter(p => p.price).length, 0),
      withWants: ocrResults.reduce((sum, r) => sum + r.products.filter(p => p.wants).length, 0),
      withTags: ocrResults.reduce((sum, r) => sum + r.products.filter(p => p.tags && p.tags.length > 0).length, 0)
    }
  };
  
  // 按分类统计
  for (const result of ocrResults) {
    if (!statsReport.categories[result.category]) {
      statsReport.categories[result.category] = { keywords: 0, products: 0 };
    }
    statsReport.categories[result.category].keywords++;
    statsReport.categories[result.category].products += result.count;
  }
  
  fs.writeFileSync(statsPath, JSON.stringify(statsReport, null, 2));
  console.log(`📊 统计：${statsPath}`);
  
  // 生成 Markdown 报告
  const reportPath = path.join(dataDir, 'xianyu-report-enhanced.md');
  let report = '# 🐾 闲鱼数据调研报告（增强版）\n\n';
  report += `**生成时间**: ${new Date().toISOString()}\n`;
  report += `**关键词总数**: ${allKeywords.length}\n`;
  report += `**商品总数**: ${statsReport.totalProducts}\n\n`;
  
  // 按分类输出
  for (const [category, data] of Object.entries(statsReport.categories)) {
    report += `## ${category}\n\n`;
    report += `- 关键词：${data.keywords} 个\n`;
    report += `- 商品：${data.products} 个\n\n`;
    
    // 该分类下的商品示例
    const categoryResults = ocrResults.filter(r => r.category === category);
    for (const result of categoryResults.slice(0, 5)) { // 只显示前 5 个
      if (result.products.length > 0) {
        report += `### ${result.keyword}\n`;
        report += '| 标题 | 价格 | 想要 | 标签 |\n|------|------|------|------|\n';
        for (const p of result.products.slice(0, 3)) { // 每个关键词显示前 3 个商品
          report += `| ${p.raw?.substring(0, 30) || ''}... | ¥${p.price || '-'} | ${p.wants || '-'} | ${p.tags?.join(',') || '-'} |\n`;
        }
        report += '\n';
      }
    }
  }
  
  // 质量分析
  report += `## 数据质量\n\n`;
  report += `- 含价格商品：${statsReport.quality.withPrice} (${(statsReport.quality.withPrice / statsReport.totalProducts * 100).toFixed(1)}%)\n`;
  report += `- 含想要人数：${statsReport.quality.withWants} (${(statsReport.quality.withWants / statsReport.totalProducts * 100).toFixed(1)}%)\n`;
  report += `- 含标签商品：${statsReport.quality.withTags} (${(statsReport.quality.withTags / statsReport.totalProducts * 100).toFixed(1)}%)\n`;
  
  fs.writeFileSync(reportPath, report);
  console.log(`📄 报告：${reportPath}`);
  
  console.log('\n👋 完成');
}

main().catch(console.error);
