#!/usr/bin/env node
/**
 * Smart Web Scraper - 智能网页数据采集器
 */

const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const fs = require('fs');
const { parse } = require('json2csv');
const XLSX = require('xlsx');

class SmartScraper {
  constructor(options = {}) {
    this.options = {
      headless: true,
      delay: 1000,
      retries: 3,
      userAgent: getRandomUserAgent(),
      ...options
    };
    this.data = [];
  }

  async scrape(url, config) {
    console.log(`🔍 开始采集: ${url}`);
    
    const browser = await puppeteer.launch({
      headless: this.options.headless,
      args: ['--no-sandbox']
    });

    try {
      const page = await browser.newPage();
      await page.setUserAgent(this.options.userAgent);
      
      await page.goto(url, { waitUntil: 'networkidle2' });
      
      // 等待内容加载
      if (config.waitFor) {
        await page.waitForSelector(config.waitFor);
      }

      const html = await page.content();
      const $ = cheerio.load(html);
      
      // 提取数据
      const results = [];
      $(config.selector || 'body').each((i, el) => {
        const item = {};
        (config.fields || []).forEach(field => {
          const $el = $(el).find(field.selector);
          if (field.type === 'text') {
            item[field.name] = $el.text().trim();
          } else if (field.type === 'attr') {
            item[field.name] = $el.attr(field.attr);
          } else if (field.type === 'html') {
            item[field.name] = $el.html();
          }
        });
        if (Object.keys(item).length > 0) {
          results.push(item);
        }
      });

      console.log(`✅ 采集到 ${results.length} 条数据`);
      return results;
      
    } finally {
      await browser.close();
    }
  }

  async scrapeMultiple(urls, config) {
    const allData = [];
    for (const url of urls) {
      const data = await this.scrape(url, config);
      allData.push(...data);
      await new Promise(r => setTimeout(r, this.options.delay));
    }
    return allData;
  }

  export(data, format, filename) {
    if (format === 'json') {
      fs.writeFileSync(filename, JSON.stringify(data, null, 2));
    } else if (format === 'csv') {
      const csv = parse(data);
      fs.writeFileSync(filename, csv);
    } else if (format === 'excel') {
      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Data');
      XLSX.writeFile(wb, filename);
    }
    console.log(`💾 已导出到 ${filename}`);
  }
}

function getRandomUserAgent() {
  const agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
  ];
  return agents[Math.floor(Math.random() * agents.length)];
}

// CLI
const args = process.argv.slice(2);
const urlIdx = args.indexOf('--url');
const configIdx = args.indexOf('--config');
const formatIdx = args.indexOf('--format');
const outputIdx = args.indexOf('--output');

if (urlIdx === -1 && configIdx === -1) {
  console.log('用法: node scraper.js --url <url> [--config <file>] [--format json|csv|excel] [--output <file>]');
  process.exit(1);
}

(async () => {
  const scraper = new SmartScraper();
  
  let config = { selector: 'body', fields: [{ name: 'content', selector: '*', type: 'text' }] };
  
  if (configIdx !== -1) {
    const configFile = args[configIdx + 1];
    if (fs.existsSync(configFile)) {
      config = JSON.parse(fs.readFileSync(configFile));
    }
  }
  
  const url = urlIdx !== -1 ? args[urlIdx + 1] : config.target?.url;
  const format = formatIdx !== -1 ? args[formatIdx + 1] : 'json';
  const output = outputIdx !== -1 ? args[outputIdx + 1] : 'output.' + format;
  
  const data = await scraper.scrape(url, config);
  scraper.export(data, format, output);
})();