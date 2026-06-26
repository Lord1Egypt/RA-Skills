#!/usr/bin/env node
/**
 * Edit Zhihu profile - final working version
 * Click "修改" button → edit field → save
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

async function editFieldByClickingModify(page, fieldName, newValue) {
  console.log(`\n✏️ 编辑"${fieldName}"...`);
  
  // Find the "修改" button within the correct Field-content
  const found = await page.evaluate((field) => {
    const labels = document.querySelectorAll('h3.Field-label, .Field-label');
    for (const label of labels) {
      if (label.textContent.trim() === field) {
        const fieldForm = label.closest('.Field');
        if (fieldForm) {
          const content = fieldForm.querySelector('.Field-content');
          if (content) {
            // Find the "修改" text/link within
            const modifyBtn = content.querySelector('button, a, span');
            // Click the content div itself (not just a child element)
            return { found: true, hasModifyBtn: !!modifyBtn };
          }
        }
      }
    }
    return { found: false };
  }, fieldName);
  
  console.log(`  找到: ${found.found}, hasModifyBtn: ${found.hasModifyBtn}`);
  
  if (!found.found) return false;
  
  // Click method 1: Click on the Field-content div (the value area)
  console.log('  🖱️ 点击值区域触发编辑...');
  
  const clicked = await page.evaluate((field) => {
    const labels = document.querySelectorAll('h3.Field-label, .Field-label');
    for (const label of labels) {
      if (label.textContent.trim() === field) {
        const fieldForm = label.closest('.Field');
        if (fieldForm) {
          const content = fieldForm.querySelector('.Field-content');
          if (content) {
            content.click();
            return true;
          }
        }
      }
    }
    return false;
  }, fieldName);
  
  if (!clicked) {
    console.log('  ❌ 点击失败');
    return false;
  }
  
  await page.waitForTimeout(2000);
  
  // After clicking, an input or textarea should appear inside the Field-content
  const inputAppeared = await page.evaluate((field) => {
    const labels = document.querySelectorAll('h3.Field-label, .Field-label');
    for (const label of labels) {
      if (label.textContent.trim() === field) {
        const fieldForm = label.closest('.Field');
        if (fieldForm) {
          const input = fieldForm.querySelector('input:not([type="hidden"]):not([type="file"]), textarea');
          if (input) {
            return { 
              tag: input.tagName, 
              name: input.getAttribute('name') || '',
              placeholder: input.getAttribute('placeholder') || '',
              value: (input.value || '').substring(0, 80),
            };
          }
          
          // Check for contenteditable
          const editable = fieldForm.querySelector('[contenteditable="true"]');
          if (editable) {
            return {
              tag: editable.tagName,
              contentEditable: true,
              text: editable.textContent?.substring(0, 80) || '',
            };
          }
        }
      }
    }
    return null;
  }, fieldName);
  
  console.log(`  出现的输入元素:`, JSON.stringify(inputAppeared));
  
  if (!inputAppeared) {
    // Maybe a modal appeared
    console.log('  🔍 检查是否有弹窗...');
    const modalInputs = await page.$$('.Modal input:not([type="hidden"]), .Modal textarea, .Modal-wrapper input, .Modal-wrapper textarea, [class*="modal"] input, [class*="modal"] textarea, [class*="Modal"] input, [class*="Modal"] textarea');
    console.log(`  弹窗中找到 ${modalInputs.length} 个输入框`);
    
    for (const inp of modalInputs) {
      try {
        const tag = await inp.evaluate(el => el.tagName);
        const placeholder = await inp.getAttribute('placeholder').catch(() => '');
        const value = await inp.inputValue().catch(() => '');
        console.log(`    <${tag}> placeholder="${placeholder}" value="${value?.substring(0, 60)}"`);
        await inp.click({ clickCount: 3 });
        await inp.fill(newValue);
        console.log(`    ✅ 已填入`);
        return true;
      } catch(e) {}
    }
    
    // Check if any input appeared anywhere new
    const allInputs = await page.$$('input:not([type="hidden"]):not([type="file"]), textarea, [contenteditable="true"]');
    console.log(`  页面总共 ${allInputs.length} 个可编辑元素`);
    for (const inp of allInputs) {
      try {
        const tag = await inp.evaluate(el => el.tagName);
        const name = await inp.getAttribute('name').catch(() => '');
        const placeholder = await inp.getAttribute('placeholder').catch(() => '');
        const value = await inp.inputValue().catch(() => '');
        
        // Skip search bar
        if (placeholder === '以色列宣布袭击伊朗') continue;
        
        console.log(`    <${tag}> name="${name}" placeholder="${placeholder}" value="${value?.substring(0, 60)}"`);
        
        if ((fieldName === '一句话介绍' && tag === 'INPUT' && placeholder === '') || 
            (fieldName === '个人简介' && tag === 'TEXTAREA')) {
          await inp.click({ clickCount: 3 });
          await inp.fill(newValue);
          console.log(`    ✅ 已填入`);
          return true;
        }
        
        // Try any non-search input that appeared
        if (tag !== 'INPUT' || (placeholder !== '以色列宣布袭击伊朗' && name !== '')) {
          await inp.click({ clickCount: 3 });
          await inp.fill(newValue);
          console.log(`    ✅ 已填入 (guess)`);
          return true;
        }
      } catch(e) {}
    }
    
    return false;
  }
  
  // Fill the appeared input
  try {
    const labels = await page.$$('h3.Field-label, .Field-label');
    for (const label of labels) {
      const text = await label.textContent();
      if (text.trim() === fieldName) {
        const fieldForm = await label.evaluateHandle(el => el.closest('.Field'));
        if (fieldForm) {
          const input = await fieldForm.$('input:not([type="hidden"]):not([type="file"]), textarea, [contenteditable="true"]');
          if (input) {
            await input.click({ clickCount: 3 });
            await input.fill(newValue);
            console.log('  ✅ 已填入');
            return true;
          }
        }
      }
    }
  } catch(e) {
    console.log(`  填入失败: ${e.message}`);
  }
  
  return false;
}

async function main() {
  const cookies = decryptCookies();

  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    console.log('📡 打开编辑页面...');
    await page.goto('https://www.zhihu.com/people/edit', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(5000);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(500);

    // Show current values
    const current = await page.evaluate(() => {
      const result = {};
      document.querySelectorAll('.Field').forEach(f => {
        const label = f.querySelector('.Field-label')?.textContent?.trim();
        const content = f.querySelector('.Field-content')?.textContent?.trim();
        if (label && content) result[label] = content;
      });
      return result;
    });
    console.log('📋 当前值:');
    Object.entries(current).forEach(([k, v]) => console.log(`  ${k}: ${v}`));

    // Edit headline
    await editFieldByClickingModify(page, '一句话介绍', NEW_HEADLINE);
    await page.waitForTimeout(1500);
    
    // Edit description
    await editFieldByClickingModify(page, '个人简介', NEW_DESCRIPTION);
    await page.waitForTimeout(1500);

    // Save
    console.log('\n💾 查找保存按钮...');
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1000);
    
    const saveBtns = await page.$$('button');
    for (const btn of saveBtns) {
      const text = await btn.textContent().catch(() => '');
      if (text.includes('保存') || text.includes('提交') || text.includes('完成')) {
        console.log(`  找到: "${text.trim()}"`);
        await btn.click();
        await page.waitForTimeout(3000);
        console.log('  ✅ 已点击保存');
        
        // Verify
        await page.reload({ waitUntil: 'networkidle', timeout: 15000 });
        await page.waitForTimeout(3000);
        const updated = await page.evaluate(() => {
          const result = {};
          document.querySelectorAll('.Field').forEach(f => {
            const label = f.querySelector('.Field-label')?.textContent?.trim();
            const content = f.querySelector('.Field-content')?.textContent?.trim();
            if (label && content) result[label] = content;
          });
          return result;
        });
        console.log('\n✅ 更新后:');
        Object.entries(updated).forEach(([k, v]) => console.log(`  ${k}: ${v?.substring(0, 80)}`));
        break;
      }
    }

    console.log('\n⏳ 浏览器保持打开30秒...');
    await page.waitForTimeout(30000);

  } catch (err) {
    console.error('❌ 错误:', err.message);
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

main();
