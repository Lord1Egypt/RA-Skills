#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';

const COOKIE_PATH = resolve(homedir(), '.hermes', 'credentials', 'zhihu-cookies.enc');
const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 12;
const AUTH_TAG_LENGTH = 16;

function getKey() { return Buffer.from(process.env.ZHIHU_COOKIE_KEY, 'hex'); }
function decryptCookies() {
  const data = readFileSync(COOKIE_PATH);
  const iv = data.subarray(0, IV_LENGTH);
  const authTag = data.subarray(IV_LENGTH, IV_LENGTH + AUTH_TAG_LENGTH);
  const ciphertext = data.subarray(IV_LENGTH + AUTH_TAG_LENGTH);
  const decipher = createDecipheriv(ALGORITHM, getKey(), iv);
  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  return JSON.parse(decrypted.toString('utf-8'));
}

async function main() {
  const cookies = decryptCookies();
  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  await ctx.addCookies(cookies);
  const page = await ctx.newPage();

  const queries = [
    { term: '数字政府建设', topic: '数字政府' },
    { term: '智慧城市', topic: '智慧城市' },
    { term: '政府信息化', topic: '政府数字化转型' },
  ];

  const allQuestions = [];

  for (const { term, topic } of queries) {
    console.log(`\n🔍 搜索: "${term}" ...`);
    await page.goto('https://www.zhihu.com/search?type=content&q=' + encodeURIComponent(term), { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
    
    // Scroll to load more
    await page.evaluate(() => window.scrollTo(0, 800));
    await page.waitForTimeout(1000);

    // Extract all links
    const results = await page.evaluate(() => {
      const links = document.querySelectorAll('a[href*="/question/"]');
      const seen = new Set();
      const items = [];
      links.forEach(a => {
        const href = a.getAttribute('href') || '';
        const match = href.match(/\/question\/(\d+)/);
        if (!match || seen.has(match[1])) return;
        seen.add(match[1]);
        
        const text = a.textContent.trim();
        // Get parent text for metadata
        const parent = a.closest('[class*="List"], [class*="Result"], [class*="Card"], [class*="ContentItem"], [class*="SearchResultCard"], div');
        const metaText = parent?.textContent?.trim() || '';
        
        if (text.length > 10 && text.length < 200) {
          items.push({
            title: text,
            href: href,
            id: match[1],
            meta: metaText.substring(0, 100),
          });
        }
      });
      return items.slice(0, 10);
    });

    results.forEach((r, i) => {
      console.log(`  ${i+1}. ${r.title.substring(0, 75)}`);
      console.log(`     /question/${r.id}`);
    });
    
    allQuestions.push(...results.map(r => ({ ...r, topic })));
  }

  // Save results
  const outputPath = '/Users/liubo/WorkBuddy/2026-05-13-task-11/search_results.json';
  writeFileSync(outputPath, JSON.stringify(allQuestions, null, 2));
  console.log(`\n💾 保存了 ${allQuestions.length} 个问题到 search_results.json`);
  
  await browser.close();
}

main();
