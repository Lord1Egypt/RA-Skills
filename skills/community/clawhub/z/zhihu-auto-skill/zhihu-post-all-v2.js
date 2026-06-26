#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';

const CONTENT_DIR = '/Users/liubo/WorkBuddy/2026-05-13-task-11';
const ALGORITHM = 'aes-256-gcm';

async function postAnswer(page, questionId, content) {
  const url = `https://www.zhihu.com/question/${questionId}`;
  console.log(`\n📝 ${url}`);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  const writeBtn = await page.$('button:has-text("写回答")');
  if (writeBtn) { await writeBtn.click(); await page.waitForTimeout(2000); }

  const editor = await page.$('.ProseMirror, [contenteditable="true"]');
  if (!editor) { console.log('  ❌ 未找到编辑器'); return false; }
  
  await editor.click();
  await page.waitForTimeout(500);
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
  console.log('  ✅ 内容已填入');

  await page.waitForTimeout(500);
  const submitBtn = await page.$('button:has-text("发布"), button:has-text("提交回答"), button:has-text("回答"), .AnswerForm-submit, [class*="submitButton"]');
  if (submitBtn) {
    await submitBtn.click();
    await page.waitForTimeout(3000);
    console.log('  ✅ 已发布');
    return true;
  }
  console.log('  ⚠️ 未找到提交按钮');
  return false;
}

async function main() {
  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  const page = await ctx.newPage();

  // LOGIN
  console.log('🔐 打开登录页，请扫码登录...');
  await page.goto('https://www.zhihu.com/signin', { waitUntil: 'networkidle', timeout: 60000 });
  console.log('⏳ 等待登录完成（最多8分钟）...');
  
  try {
    await page.waitForURL('https://www.zhihu.com/', { timeout: 8 * 60 * 1000 });
  } catch(e) {
    console.log('⚠️ 登录超时，尝试继续...');
  }
  await page.waitForTimeout(3000);
  
  // Save cookies for future use
  const cookies = await ctx.cookies();
  const { encryptAndSaveCookies } = await import('./scripts/zhihu-core.js');
  encryptAndSaveCookies(cookies);
  console.log('✅ 登录成功！Cookie已保存\n');

  // ANSWER 1
  const c1 = readFileSync(CONTENT_DIR + '/回答1-数字政府建设.md', 'utf-8');
  await postAnswer(page, '551162843', c1);

  // ANSWER 2
  const c2 = readFileSync(CONTENT_DIR + '/回答2-智慧城市挑战.md', 'utf-8');
  await postAnswer(page, '541077100', c2);

  // THOUGHT
  console.log('\n💬 发布想法...');
  await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  
  // Click the "写想法" or find the creator center
  const thoughtText = '刚在专栏写了篇长文，复盘了从基层科员到高级工程师的15年政府信息化经历，聊了聊数字政府建设的三个真相。\n\n如果你对政务云、数据安全、智慧城市感兴趣，欢迎来看看 👇\nhttps://zhuanlan.zhihu.com/p/2037939403423741377';
  
  // Try creator page
  await page.goto('https://www.zhihu.com/creator', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  
  const thoughtInput = await page.$('[contenteditable="true"], textarea, .ProseMirror, [class*="editor"]');
  if (thoughtInput) {
    await thoughtInput.click();
    await page.waitForTimeout(500);
    await page.evaluate((text) => {
      const els = [
        document.querySelector('[contenteditable="true"]'),
        document.querySelector('textarea'),
        document.querySelector('.ProseMirror'),
      ].filter(Boolean);
      const ed = els[0];
      if (ed) {
        ed.focus();
        if (ed.tagName === 'TEXTAREA') {
          ed.value = text;
          ed.dispatchEvent(new Event('input', { bubbles: true }));
        } else {
          const dt = new DataTransfer();
          dt.setData('text/plain', text);
          ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
        }
      }
    }, thoughtText);
    await page.waitForTimeout(2000);
    
    const pubBtn = await page.$('button:has-text("发布"), button:has-text("发表")');
    if (pubBtn) { await pubBtn.click(); await page.waitForTimeout(2000); console.log('  ✅ 想法已发布'); }
  } else {
    // Try directly from home page
    console.log('  尝试从首页发想法...');
    await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    // Look for "写想法" button
    const createBtn = await page.$('button:has-text("写想法"), [class*="PublishBar"] button');
    if (createBtn) {
      await createBtn.click();
      await page.waitForTimeout(2000);
      const input = await page.$('[contenteditable="true"], textarea');
      if (input) {
        await input.click();
        await page.waitForTimeout(500);
        await input.fill(thoughtText);
        await page.waitForTimeout(1000);
        const pub = await page.$('button:has-text("发布")');
        if (pub) { await pub.click(); await page.waitForTimeout(2000); console.log('  ✅ 想法已发布'); }
      }
    }
  }

  console.log('\n✅ 全部完成！浏览器30秒后关闭...');
  await page.waitForTimeout(30000);
  await browser.close();
}

main();
