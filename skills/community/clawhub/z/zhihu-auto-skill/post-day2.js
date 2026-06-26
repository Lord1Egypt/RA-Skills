#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';

const DIR = '/Users/liubo/WorkBuddy/2026-05-13-task-11';
const CP = resolve(homedir(), '.hermes', 'credentials', 'zhihu-cookies.enc');

function decrypt() {
  const key = Buffer.from(process.env.ZHIHU_COOKIE_KEY, 'hex');
  const d = readFileSync(CP);
  const iv = d.subarray(0, 12), tag = d.subarray(12, 28), ct = d.subarray(28);
  const dec = createDecipheriv('aes-256-gcm', key, iv);
  dec.setAuthTag(tag);
  return JSON.parse(Buffer.concat([dec.update(ct), dec.final()]).toString());
}

async function post(page, qid, file) {
  const content = readFileSync(file, 'utf-8');
  const url = `https://www.zhihu.com/question/${qid}`;
  console.log(`📝 ${url}`);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      if (b.textContent.includes('写回答')) { b.click(); return; }
    }
  });
  await page.waitForTimeout(2000);
  
  await page.evaluate((text) => {
    const ed = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
    if (ed) { ed.focus(); const dt = new DataTransfer(); dt.setData('text/plain', text); ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true })); }
  }, content);
  await page.waitForTimeout(2000);
  console.log('  ✅ 已填入');
  
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      if (b.textContent.includes('发布') || b.textContent.includes('提交回答')) { b.click(); return; }
    }
  });
  await page.waitForTimeout(3000);
  console.log('  ✅ 已发布');
}

async function main() {
  const cookies = decrypt();
  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  await ctx.addCookies(cookies);
  const page = await ctx.newPage();
  
  await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  if (!await page.$('.AppHeader-profileAvatar')) { console.log('❌ 未登录'); await browser.close(); return; }
  console.log('✅ 已登录\n');

  await post(page, '405105043', DIR + '/回答3-大数据管理局.md');
  await post(page, '3493591005', DIR + '/回答4-政务系统难用.md');
  
  console.log('\n🎉 完成！10秒后关闭...');
  await page.waitForTimeout(10000);
  await browser.close();
}

main();
