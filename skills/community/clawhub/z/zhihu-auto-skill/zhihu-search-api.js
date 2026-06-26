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

  // First navigate to zhihu to establish session
  await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  const queries = ['数字政府', '智慧城市', '政府数字化转型', '电子政务'];
  
  for (const q of queries) {
    console.log('\n=== ' + q + ' ===');
    const result = await page.evaluate(async (query) => {
      try {
        const res = await fetch('https://www.zhihu.com/api/v4/search_v3?q=' + encodeURIComponent(query) + '&t=general&lc_idx=0&correction=1&type=content&offset=0&limit=10', {
          headers: { 'Accept': 'application/json', 'x-requested-with': 'fetch' },
          credentials: 'include',
        });
        if (res.ok) {
          const data = await res.json();
          return { success: true, data };
        }
        return { success: false, status: res.status };
      } catch(e) {
        return { success: false, error: e.message };
      }
    }, q);

    if (result.success && result.data.data) {
      result.data.data.forEach((item, i) => {
        if (i >= 5) return;
        const obj = item.object || item;
        const type = obj.type || 'unknown';
        const id = obj.id;
        let title = '', url = '', answerCount = 0, followerCount = 0;
        
        if (type === 'question' || type === 'search_result') {
          title = obj.title || obj.question?.title || '';
          url = obj.url || `https://www.zhihu.com/question/${obj.id || obj.question?.id}`;
          answerCount = obj.answer_count || 0;
          followerCount = obj.follower_count || 0;
        } else if (type === 'answer') {
          title = obj.question?.title || '';
          url = `https://www.zhihu.com/question/${obj.question?.id}`;
          answerCount = obj.question?.answer_count || 0;
          followerCount = obj.question?.follower_count || 0;
        } else if (type === 'article') {
          title = obj.title || '';
          url = obj.url || `https://zhuanlan.zhihu.com/p/${obj.id}`;
          answerCount = obj.voteup_count || 0;
        }
        
        if (title) {
          console.log(`  ${i+1}. [${type}] ${title.substring(0, 80)}`);
          console.log(`     ${url} | 回答:${answerCount} 关注:${followerCount}`);
        }
      });
    } else {
      console.log('  搜索失败: ' + JSON.stringify(result));
    }
  }

  await browser.close();
}

main();
