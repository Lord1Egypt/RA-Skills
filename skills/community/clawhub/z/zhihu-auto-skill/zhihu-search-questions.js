#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
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
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  await ctx.addCookies(cookies);
  const page = await ctx.newPage();

  const queries = ['数字政府建设', '智慧城市', '政府数字化转型', '电子政务 信息化'];

  for (const q of queries) {
    console.log('\n=== 搜索: ' + q + ' ===');
    await page.goto('https://www.zhihu.com/search?type=content&q=' + encodeURIComponent(q), { waitUntil: 'networkidle', timeout: 20000 });
    await page.waitForTimeout(2000);
    
    const results = await page.evaluate(() => {
      const items = document.querySelectorAll('.List-item, .SearchResultCard, [class*="SearchResult"], .ContentItem');
      const found = [];
      items.forEach((item, i) => {
        if (i >= 8) return;
        const titleEl = item.querySelector('h2 a, [class*="title"] a, a[href*="/question/"], .QuestionItem-title a, [class*="QuestionItem"] a');
        const title = titleEl?.textContent?.trim() || '';
        const href = titleEl?.getAttribute('href') || '';
        const metaEl = item.querySelector('[class*="meta"], [class*="AnswerCount"], [class*="follow"]');
        const meta = metaEl?.textContent?.trim() || '';
        if (title && href.includes('/question/')) {
          found.push({ title, href, meta });
        }
      });
      return found;
    });
    
    results.forEach((r, i) => {
      console.log('  ' + (i+1) + '. ' + r.title.substring(0, 80));
      console.log('     ' + r.href + ' | ' + r.meta);
    });
  }

  await browser.close();
}

main();
