#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';

const CP = resolve(homedir(), '.hermes', 'credentials', 'zhihu-cookies.enc');
function decrypt() {
  const key = Buffer.from(process.env.ZHIHU_COOKIE_KEY, 'hex');
  const d = readFileSync(CP);
  const iv = d.subarray(0, 12), tag = d.subarray(12, 28), ct = d.subarray(28);
  const dec = createDecipheriv('aes-256-gcm', key, iv);
  dec.setAuthTag(tag);
  return JSON.parse(Buffer.concat([dec.update(ct), dec.final()]).toString());
}

const thought = '刚在专栏写了篇长文，复盘了从基层科员到高级工程师的15年政府信息化经历，聊聊数字政府那些「看不见的事」。\n\n如果你对政务云、数据安全、智慧城市这些话题感兴趣，欢迎来看看 👇\nhttps://zhuanlan.zhihu.com/p/2037939403423741377';

const cookies = decrypt();
const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
await ctx.addCookies(cookies);
const page = await ctx.newPage();

await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
await page.waitForTimeout(2000);
console.log('✅ 已登录');

// Go to creator center
await page.goto('https://www.zhihu.com/creator', { waitUntil: 'networkidle', timeout: 30000 });
await page.waitForTimeout(3000);

// Click "写想法"
await page.evaluate(() => {
  for (const el of document.querySelectorAll('button, a, span, div')) {
    if (el.textContent.trim() === '写想法') { el.click(); return; }
  }
});
await page.waitForTimeout(3000);

// Fill and submit
await page.evaluate((text) => {
  const ed = document.querySelector('[contenteditable="true"]') || document.querySelector('textarea') || document.querySelector('.ProseMirror');
  if (!ed) return;
  ed.focus();
  if (ed.tagName === 'TEXTAREA') {
    ed.value = text;
    ed.dispatchEvent(new Event('input', { bubbles: true }));
  } else {
    ed.textContent = '';
    const dt = new DataTransfer();
    dt.setData('text/plain', text);
    ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
  }
}, thought);
await page.waitForTimeout(2000);
console.log('  ✅ 已填入');

// Click publish
await page.evaluate(() => {
  for (const b of document.querySelectorAll('button')) {
    if (b.textContent.includes('发布')) { b.click(); return; }
  }
});
await page.waitForTimeout(3000);
console.log('  ✅ 已发布');

console.log('\n🎉 想法发布成功！');
await page.waitForTimeout(5000);
await browser.close();
