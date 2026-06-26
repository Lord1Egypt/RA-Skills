#!/usr/bin/env node
/**
 * Update Zhihu profile v3 - properly handle the edit modal
 */
import { chromium } from 'playwright';
import { readFileSync, existsSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';

const COOKIE_PATH = resolve(homedir(), '.hermes', 'credentials', 'zhihu-cookies.enc');
const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 12;
const AUTH_TAG_LENGTH = 16;

function getEncryptionKey() {
  const key = process.env.ZHIHU_COOKIE_KEY;
  if (!key || key.length !== 64) throw new Error('ZHIHU_COOKIE_KEY not set');
  return Buffer.from(key, 'hex');
}

function decryptCookies() {
  if (!existsSync(COOKIE_PATH)) return null;
  const data = readFileSync(COOKIE_PATH);
  const iv = data.subarray(0, IV_LENGTH);
  const authTag = data.subarray(IV_LENGTH, IV_LENGTH + AUTH_TAG_LENGTH);
  const ciphertext = data.subarray(IV_LENGTH + AUTH_TAG_LENGTH);
  const decipher = createDecipheriv(ALGORITHM, getEncryptionKey(), iv);
  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  return JSON.parse(decrypted.toString('utf-8'));
}

const NEW_HEADLINE = '信息系统项目管理师（软考高级）｜高级工程师｜15年政府信息化经验，亲历智慧城市从规划到落地';
const NEW_DESCRIPTION = '沈北新区大数据管理中心 → 辽宁日报社高级工程师\n\n专注领域：数字政府 · 智慧城市 · AI+政务 · 政务信息化项目管理\n\n用一线实战经验，讲透政府数字化转型的现在与未来。';

async function main() {
  const cookies = decryptCookies();

  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    // Go to profile page
    console.log('📡 打开个人主页...');
    await page.goto('https://www.zhihu.com/people/liu-bo-94-4', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    // Get current headline
    const currentHeadline = await page.$eval('.ProfileHeader-headline', el => el.textContent.trim()).catch(() => '(未获取到)');
    console.log(`📋 当前一句话介绍: ${currentHeadline}`);

    // Click "编辑个人资料" button - use force to bypass header interception
    console.log('\n🖱️ 点击"编辑个人资料"...');
    
    // Method 1: JavaScript click
    await page.evaluate(() => {
      const buttons = document.querySelectorAll('button');
      for (const btn of buttons) {
        if (btn.textContent.includes('编辑个人资料')) {
          btn.click();
          break;
        }
      }
    });
    
    await page.waitForTimeout(2000);
    console.log(`  页面 URL: ${page.url()}`);

    // Check what appeared - modal or new page
    console.log('\n🔍 查找编辑表单...');
    
    // Dump visible form fields
    const formFields = await page.$$eval('input:not([type="hidden"]), textarea, select', els => els.map(e => ({
      tag: e.tagName,
      type: e.getAttribute('type') || '',
      name: e.getAttribute('name') || '',
      placeholder: e.getAttribute('placeholder') || '',
      label: (() => {
        // Try to find associated label
        const id = e.id;
        if (id) {
          const label = document.querySelector(`label[for="${id}"]`);
          if (label) return label.textContent.trim();
        }
        // Try parent label
        const parent = e.closest('label');
        if (parent) return parent.textContent.trim();
        return '';
      })(),
      value: (e.value || '').substring(0, 60),
      className: e.className?.substring(0, 40) || '',
    })));
    
    formFields.forEach(f => console.log(`  <${f.tag}${f.type ? ' type="'+f.type+'"' : ''} name="${f.name}" placeholder="${f.placeholder}" label="${f.label}" value="${f.value}">`));

    // Try to find and fill headline
    console.log('\n✏️ 查找并更新一句话介绍...');
    
    // Try by placeholder text containing "一句话"
    let headlineEl = await page.$('textarea[placeholder*="一句话"], input[placeholder*="一句话"]');
    if (!headlineEl) {
      // Try by name
      headlineEl = await page.$('[name="headline"]');
    }
    if (!headlineEl) {
      // Try by looking for an input near "一句话介绍" text
      headlineEl = await page.$('xpath=//*[contains(text(),"一句话")]/following::input[1]');
    }
    if (!headlineEl) {
      headlineEl = await page.$('xpath=//*[contains(text(),"一句话")]/following::textarea[1]');
    }
    
    if (headlineEl) {
      await headlineEl.click({ clickCount: 3 });
      await headlineEl.fill(NEW_HEADLINE);
      console.log('  ✅ 已填入新的一句话介绍');
    } else {
      console.log('  ⚠️ 未找到一句话介绍输入框');
      // If on new page, check all textareas
      const textareas = await page.$$('textarea');
      console.log(`  页面上有 ${textareas.length} 个 textarea`);
      for (let i = 0; i < textareas.length; i++) {
        const val = await textareas[i].inputValue().catch(() => '');
        const ph = await textareas[i].getAttribute('placeholder').catch(() => '');
        console.log(`  textarea[${i}]: placeholder="${ph}" value="${val?.substring(0, 50)}"`);
        
        // If it has the old headline value
        if (val.includes('信息系统项目管理师') || val.includes('电子政务')) {
          console.log(`    -> 这很可能就是一句话介绍！正在更新...`);
          await textareas[i].click({ clickCount: 3 });
          await textareas[i].fill(NEW_HEADLINE);
          headlineEl = textareas[i];
        }
      }
    }

    // Try to find and fill description
    console.log('\n✏️ 查找并更新个人描述...');
    
    let descEl = await page.$('textarea[placeholder*="介绍自己"], textarea[placeholder*="个人"], textarea[name="description"]');
    if (!descEl) {
      descEl = await page.$('xpath=//*[contains(text(),"个人简介") or contains(text(),"个人介绍") or contains(text(),"描述")]/following::textarea[1]');
    }
    
    if (!descEl) {
      // Look for any textarea that isn't the headline
      const textareas = await page.$$('textarea');
      for (const ta of textareas) {
        if (ta !== headlineEl) {
          const val = await ta.inputValue().catch(() => '');
          if (val !== NEW_HEADLINE) {
            descEl = ta;
            break;
          }
        }
      }
    }
    
    if (descEl) {
      await descEl.click({ clickCount: 3 });
      await descEl.fill(NEW_DESCRIPTION);
      console.log('  ✅ 已填入新的个人描述');
    } else {
      console.log('  ⚠️ 未找到个人描述输入框');
    }

    // Find and click save
    if (headlineEl || descEl) {
      console.log('\n💾 查找保存按钮...');
      
      const saveBtn = await page.$('button:has-text("保存"), button:has-text("提交"), button:has-text("完成"), button:has-text("确认"), button[type="submit"]');
      if (saveBtn) {
        const text = await saveBtn.textContent();
        console.log(`  找到按钮: "${text.trim()}"`);
        await saveBtn.click();
        await page.waitForTimeout(3000);
        console.log('  ✅ 已点击保存');
        
        // Wait for save to complete
        await page.waitForTimeout(2000);
        console.log('\n✅ 操作完成！请检查个人主页确认更新。');
      } else {
        console.log('  ⚠️ 未找到保存按钮');
      }
    }

    console.log('\n⏳ 浏览器保持打开30秒供你检查...');
    await page.waitForTimeout(30000);

  } catch (err) {
    console.error('❌ 错误:', err.message);
    console.error(err.stack);
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

main();
