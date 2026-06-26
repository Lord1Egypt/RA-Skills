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

  // Navigate to zhihu first
  await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  // Use the explore/topic API to find questions
  console.log('📡 通过API获取话题热门问题...\n');
  
  // Known topic IDs (from Zhihu)
  const topics = [
    { name: '数字政府', id: '19568510' },
    { name: '智慧城市', id: '19551481' },
    { name: '电子政务', id: '19609863' },
  ];

  for (const topic of topics) {
    console.log(`=== ${topic.name} (话题ID: ${topic.id}) ===`);
    
    // Try topic API
    const result = await page.evaluate(async (topicId) => {
      try {
        const res = await fetch(`https://www.zhihu.com/api/v4/topics/${topicId}/feeds/essence?limit=10`, {
          headers: { 'Accept': 'application/json', 'x-requested-with': 'fetch' },
          credentials: 'include',
        });
        if (res.ok) {
          const data = await res.json();
          return { success: true, data };
        }
        // Try hot questions endpoint
        const res2 = await fetch(`https://www.zhihu.com/api/v4/topics/${topicId}/feeds/top_question?limit=10`, {
          headers: { 'Accept': 'application/json', 'x-requested-with': 'fetch' },
          credentials: 'include',
        });
        if (res2.ok) {
          const data = await res2.json();
          return { success: true, data, source: 'top_question' };
        }
        return { success: false, status: res.status, status2: res2.status };
      } catch(e) {
        return { success: false, error: e.message };
      }
    }, topic.id);
    
    if (result.success) {
      const items = result.data?.data || [];
      items.slice(0, 5).forEach((item, i) => {
        const target = item.target || item;
        const q = target.question || target;
        const title = q.title || target.title || '';
        const qid = q.id || target.id || '';
        const answerCount = q.answer_count || target.answer_count || 0;
        const followerCount = q.follower_count || target.follower_count || 0;
        if (title && qid) {
          console.log(`  ${i+1}. ${title.substring(0, 75)}`);
          console.log(`     https://www.zhihu.com/question/${qid} | ${answerCount}回答 ${followerCount}关注`);
        }
      });
    } else {
      console.log(`  失败: ${JSON.stringify(result)}`);
    }
    console.log('');
  }

  console.log('⏳ 30秒后关闭...');
  await page.waitForTimeout(30000);
  await browser.close();
}

main();
