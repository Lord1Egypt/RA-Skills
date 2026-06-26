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

  const topicUrls = [
    { name: '数字政府', url: 'https://www.zhihu.com/topic/19568510/hot' },
    { name: '智慧城市', url: 'https://www.zhihu.com/topic/19551481/hot' },
  ];

  const allQuestions = [];

  for (const { name, url } of topicUrls) {
    console.log(`\n=== ${name} ===`);
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
    
    // Scroll to load content
    await page.evaluate(() => window.scrollTo(0, 500));
    await page.waitForTimeout(1000);
    await page.evaluate(() => window.scrollTo(0, 1000));
    await page.waitForTimeout(1000);

    // Extract ALL question links from the rendered page
    const questions = await page.evaluate(() => {
      const results = [];
      // Find all links that go to questions
      const allLinks = document.querySelectorAll('a');
      const seen = new Set();
      
      allLinks.forEach(a => {
        const href = a.getAttribute('href') || '';
        const match = href.match(/\/question\/(\d+)/);
        if (!match || seen.has(match[1])) return;
        
        const text = (a.textContent || '').trim();
        // Only include substantive question titles
        if (text.length > 10 && text.length < 200 && !text.includes('...')) {
          seen.add(match[1]);
          results.push({
            title: text,
            id: match[1],
            url: 'https://www.zhihu.com' + href.split('?')[0],
          });
        }
      });
      return results.slice(0, 15);
    });

    questions.forEach((q, i) => {
      console.log(`  ${i+1}. ${q.title.substring(0, 75)}`);
      console.log(`     ${q.url}`);
    });
    
    allQuestions.push(...questions.map(q => ({ ...q, topic: name })));
  }

  // Also try search page directly
  console.log('\n=== 搜索: 政府数字化转型 ===');
  await page.goto('https://www.zhihu.com/search?type=content&q=政府数字化转型', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(5000);
  await page.evaluate(() => window.scrollTo(0, 600));
  await page.waitForTimeout(2000);

  const searchQs = await page.evaluate(() => {
    const results = [];
    const allLinks = document.querySelectorAll('a');
    const seen = new Set();
    allLinks.forEach(a => {
      const href = a.getAttribute('href') || '';
      const match = href.match(/\/question\/(\d+)/);
      if (!match || seen.has(match[1])) return;
      const text = (a.textContent || '').trim();
      if (text.length > 10 && text.length < 200) {
        seen.add(match[1]);
        results.push({ title: text, id: match[1], url: 'https://www.zhihu.com/question/' + match[1] });
      }
    });
    return results.slice(0, 10);
  });

  searchQs.forEach((q, i) => {
    console.log(`  ${i+1}. ${q.title.substring(0, 75)}`);
    console.log(`     ${q.url}`);
  });
  allQuestions.push(...searchQs.map(q => ({ ...q, topic: '搜索' })));

  // Save
  const outPath = '/Users/liubo/WorkBuddy/2026-05-13-task-11/search_results.json';
  writeFileSync(outPath, JSON.stringify(allQuestions, null, 2));
  console.log(`\n💾 共 ${allQuestions.length} 个问题保存到 search_results.json`);

  console.log('\n⏳ 浏览器30秒后关闭...');
  await page.waitForTimeout(30000);
  await browser.close();
}

main();
