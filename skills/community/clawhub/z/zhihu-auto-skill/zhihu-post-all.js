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

async function postAnswer(page, questionId, content) {
  const url = `https://www.zhihu.com/question/${questionId}`;
  console.log(`\n📝 回答: ${url}`);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  // Click "写回答"
  const writeBtn = await page.$('button:has-text("写回答")');
  if (writeBtn) {
    await writeBtn.click();
    await page.waitForTimeout(2000);
    console.log('  ✅ 点击"写回答"');
  }

  // Find editor and fill
  const editor = await page.$('.ProseMirror, [contenteditable="true"]');
  if (editor) {
    await editor.click();
    await page.waitForTimeout(500);
    
    // Use clipboard paste for speed
    await page.evaluate((text) => {
      const ed = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
      if (ed) {
        ed.focus();
        // Use execCommand for plain text or DataTransfer for HTML
        const dt = new DataTransfer();
        dt.setData('text/plain', text);
        ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
      }
    }, content);
    
    await page.waitForTimeout(2000);
    console.log('  ✅ 内容已填入');
  } else {
    console.log('  ❌ 未找到编辑器');
    return false;
  }

  // Click submit - try multiple selectors
  await page.waitForTimeout(1000);
  const submitBtn = await page.$('button:has-text("发布"), button:has-text("提交"), button:has-text("回答"), .AnswerForm-submit, [class*="submit"]');
  if (submitBtn) {
    await submitBtn.click();
    await page.waitForTimeout(3000);
    console.log('  ✅ 已提交');
    return true;
  } else {
    console.log('  ⚠️ 未找到提交按钮，尝试截图...');
    await page.screenshot({ path: '/tmp/zhihu_answer_debug.png' });
    return false;
  }
}

async function main() {
  const cookies = decryptCookies();
  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  await ctx.addCookies(cookies);
  const page = await ctx.newPage();

  // Check login
  await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  const loggedIn = await page.$('.AppHeader-profileAvatar');
  if (!loggedIn) { console.log('❌ 未登录'); await browser.close(); return; }
  console.log('✅ 已登录\n');

  // Answer 1: 数字政府建设
  const content1 = readFileSync('/Users/liubo/WorkBuddy/2026-05-13-task-11/回答1-数字政府建设.md', 'utf-8');
  await postAnswer(page, '551162843', content1);

  // Answer 2: 智慧城市挑战  
  const content2 = readFileSync('/Users/liubo/WorkBuddy/2026-05-13-task-11/回答2-智慧城市挑战.md', 'utf-8');
  await postAnswer(page, '541077100', content2);

  // Post thought
  console.log('\n💬 发布想法...');
  await page.goto('https://www.zhihu.com/creator', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  
  const thought = '刚在专栏写了篇长文《我在政府做了15年信息化，聊聊数字政府那些「看不见的事」》，复盘了从基层科员到高级工程师的15年经历，聊了聊数字政府建设的三个真相。\n\n如果你对政务云、数据安全、智慧城市这些话题感兴趣，欢迎来看看。\n\nhttps://zhuanlan.zhihu.com/p/2037939403423741377';
  
  // Find the thought input
  const thoughtInput = await page.$('[contenteditable="true"], textarea, .ProseMirror');
  if (thoughtInput) {
    await thoughtInput.click();
    await page.waitForTimeout(500);
    await page.evaluate((text) => {
      const ed = document.querySelector('[contenteditable="true"]') || document.querySelector('textarea') || document.querySelector('.ProseMirror');
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
    }, thought);
    await page.waitForTimeout(2000);
    console.log('  ✅ 想法内容已填入');
    
    const publishBtn = await page.$('button:has-text("发布"), button:has-text("发表"), button[type="submit"]');
    if (publishBtn) {
      await publishBtn.click();
      await page.waitForTimeout(3000);
      console.log('  ✅ 想法已发布');
    }
  }

  console.log('\n⏳ 浏览器30秒后关闭...');
  await page.waitForTimeout(30000);
  await browser.close();
}

main();
