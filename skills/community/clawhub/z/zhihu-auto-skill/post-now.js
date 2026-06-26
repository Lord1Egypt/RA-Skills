#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';

const DIR = '/Users/liubo/WorkBuddy/2026-05-13-task-11';
const CP = resolve(homedir(), '.hermes', 'credentials', 'zhihu-cookies.enc');
const ALG = 'aes-256-gcm';

function decrypt() {
  const key = Buffer.from(process.env.ZHIHU_COOKIE_KEY, 'hex');
  const d = readFileSync(CP);
  const iv = d.subarray(0, 12);
  const tag = d.subarray(12, 28);
  const ct = d.subarray(28);
  const dec = createDecipheriv(ALG, key, iv);
  dec.setAuthTag(tag);
  return JSON.parse(Buffer.concat([dec.update(ct), dec.final()]).toString());
}

async function postAnswer(page, qid, file) {
  const content = readFileSync(file, 'utf-8');
  const url = `https://www.zhihu.com/question/${qid}`;
  console.log(`\n📝 ${url}`);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  // Click "写回答" via JS to bypass modals
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      if (b.textContent.includes('写回答')) { b.click(); return; }
    }
  });
  await page.waitForTimeout(2000);

  // Fill content
  await page.evaluate((text) => {
    const ed = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
    if (ed) {
      ed.focus();
      const dt = new DataTransfer();
      dt.setData('text/plain', text);
      ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
    }
  }, content);
  await page.waitForTimeout(2000);
  console.log('  ✅ 已填入');

  // Submit via JS
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      const t = b.textContent;
      if (t.includes('发布') || t.includes('提交回答')) { b.click(); return; }
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

  // Verify login
  await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  const ok = await page.$('.AppHeader-profileAvatar');
  if (!ok) { console.log('❌ 未登录'); await browser.close(); return; }
  console.log('✅ 已登录\n');

  // Answer 1
  await postAnswer(page, '551162843', DIR + '/回答1-数字政府建设.md');
  // Answer 2
  await postAnswer(page, '541077100', DIR + '/回答2-智慧城市挑战.md');

  // Thought
  console.log('\n💬 发布想法...');
  await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button, [class*="PublishBar"]')) {
      if (b.textContent.includes('写想法')) { b.click(); return; }
    }
  });
  await page.waitForTimeout(2000);

  const thought = '刚在专栏写了篇长文，复盘了从基层科员到高级工程师的15年政府信息化经历，聊聊数字政府那些「看不见的事」。\n\n如果你对政务云、数据安全、智慧城市这些话题感兴趣，欢迎来看看 👇\nhttps://zhuanlan.zhihu.com/p/2037939403423741377';

  const input = await page.$('[contenteditable="true"], textarea, .ProseMirror');
  if (input) {
    await input.click();
    await page.waitForTimeout(500);
    await page.evaluate((text) => {
      const ed = document.querySelector('[contenteditable="true"]') || document.querySelector('textarea') || document.querySelector('.ProseMirror');
      if (!ed) return;
      ed.focus();
      if (ed.tagName === 'TEXTAREA') {
        ed.value = text;
        ed.dispatchEvent(new Event('input', { bubbles: true }));
      } else {
        const dt = new DataTransfer();
        dt.setData('text/plain', text);
        ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
      }
    }, thought);
    await page.waitForTimeout(1500);
    
    await page.evaluate(() => {
      for (const b of document.querySelectorAll('button')) {
        if (b.textContent.includes('发布')) { b.click(); return; }
      }
    });
    await page.waitForTimeout(2000);
    console.log('  ✅ 想法已发布');
  }

  console.log('\n🎉 全部完成！30秒后关闭...');
  await page.waitForTimeout(30000);
  await browser.close();
}

main();
