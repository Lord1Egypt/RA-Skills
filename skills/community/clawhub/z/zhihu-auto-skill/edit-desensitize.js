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
  const iv = d.subarray(0,12), tag=d.subarray(12,28), ct=d.subarray(28);
  const dec = createDecipheriv('aes-256-gcm', key, iv);
  dec.setAuthTag(tag);
  return JSON.parse(Buffer.concat([dec.update(ct), dec.final()]).toString());
}

// Edit an article by ID
async function editArticle(page, articleId, filePath) {
  const newContent = readFileSync(filePath, 'utf-8');
  const editUrl = `https://zhuanlan.zhihu.com/p/${articleId}/edit`;
  console.log(`📝 编辑专栏: ${editUrl}`);
  
  await page.goto(editUrl, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);
  
  // Select all and replace in editor
  const editor = await page.$('.ProseMirror, [contenteditable="true"]');
  if (!editor) { console.log('  ❌ 未找到编辑器'); return false; }
  
  await editor.click();
  await page.waitForTimeout(500);
  
  // Select all content
  await page.keyboard.press('Meta+a'); // Cmd+A
  await page.waitForTimeout(300);
  
  // Paste new content
  await page.evaluate((text) => {
    const ed = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
    if (ed) {
      ed.focus();
      const dt = new DataTransfer();
      dt.setData('text/plain', text);
      ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
    }
  }, newContent);
  await page.waitForTimeout(2000);
  console.log('  ✅ 内容已替换');
  
  // Save
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      if (b.textContent.includes('发布') || b.textContent.includes('更新') || b.textContent.includes('保存')) { b.click(); return; }
    }
  });
  await page.waitForTimeout(3000);
  console.log('  ✅ 已保存');
  return true;
}

// Edit an answer on a question page
async function editAnswer(page, questionId) {
  const url = `https://www.zhihu.com/question/${questionId}`;
  console.log(`📝 编辑回答: ${url}`);
  
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  
  // Find edit button on my answer
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      if (b.textContent.includes('编辑') || b.textContent.includes('修改')) { b.click(); return; }
    }
  });
  await page.waitForTimeout(2000);
  
  // Find editor and do find-replace
  const replaced = await page.evaluate(() => {
    const ed = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
    if (!ed) return 'no editor';
    const text = ed.textContent || ed.innerText || '';
    let newText = text
      .replace(/沈北新区/g, '某区')
      .replace(/辽宁日报社/g, '某省级媒体集团')
      .replace(/辽宁报刊传媒集团/g, '某省级媒体集团')
      .replace(/蒲河新城/g, '某新城');
    
    ed.focus();
    // Select all
    document.execCommand('selectAll');
    const dt = new DataTransfer();
    dt.setData('text/plain', newText);
    ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
    return 'replaced';
  });
  console.log(`  结果: ${replaced}`);
  await page.waitForTimeout(1500);
  
  // Click save/submit
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      if (b.textContent.includes('发布') || b.textContent.includes('提交') || b.textContent.includes('保存')) { b.click(); return; }
    }
  });
  await page.waitForTimeout(3000);
  console.log('  ✅ 已保存');
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

  const DIR = '/Users/liubo/WorkBuddy/2026-05-13-task-11';

  // Edit articles
  await editArticle(page, '2037939403423741377', DIR + '/专栏第1篇-数字政府15年.md');
  await editArticle(page, '2038539291467461800', DIR + '/专栏第2篇-政务云迁移.md');
  
  // Edit answers
  await editAnswer(page, '551162843');  // 回答1
  await editAnswer(page, '541077100');  // 回答2
  await editAnswer(page, '405105043');  // 回答3
  await editAnswer(page, '3493591005'); // 回答4

  console.log('\n🎉 全部脱敏完成！');
  await page.waitForTimeout(5000);
  await browser.close();
}

main();
