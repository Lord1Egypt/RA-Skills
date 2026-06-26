#!/usr/bin/env node
/**
 * Edit Zhihu profile - click-to-edit approach
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

async function editField(page, labelText, newValue) {
  console.log(`\n✏️ 编辑"${labelText}"...`);
  
  // Find the label element and its associated edit area
  const result = await page.evaluate((text) => {
    // Find all elements with matching text
    const allEls = document.querySelectorAll('*');
    let labelEl = null;
    for (const el of allEls) {
      const t = el.textContent.trim();
      if (t === text && el.children.length <= 2) {
        // Prefer leaf-level elements
        if (!labelEl || el.children.length < labelEl.children.length) {
          labelEl = el;
        }
      }
    }
    
    if (!labelEl) return { found: false };
    
    // Get parent for context
    const parent = labelEl.closest('[class*="Profile"], [class*="profile"], [class*="Edit"], [class*="edit"], [class*="Form"], [class*="form"], [class*="Section"], [class*="section"], [class*="Field"], [class*="field"], .Settings-section, div') || labelEl.parentElement;
    
    return {
      found: true,
      labelClass: labelEl.className?.substring(0, 80) || '',
      labelTag: labelEl.tagName,
      parentClass: parent?.className?.substring(0, 80) || '',
      parentTag: parent?.tagName || '',
      parentHTML: parent?.outerHTML?.substring(0, 200) || '',
      innerText: parent?.innerText?.substring(0, 100) || '',
      rect: labelEl.getBoundingClientRect(),
    };
  }, labelText);
  
  console.log(`  查找结果:`, JSON.stringify({ found: result.found, labelTag: result.labelTag, parentTag: result.parentTag }));
  if (result.found) {
    console.log(`  parent innerText: "${result.innerText}"`);
  }
  
  if (!result.found) {
    console.log(`  ❌ 未找到"${labelText}"标签`);
    return false;
  }
  
  // Click on the area - try clicking the parent or the label
  // Use JavaScript click to bypass interception
  console.log('  🖱️ 点击触发编辑模式...');
  
  const clicked = await page.evaluate((text) => {
    const allEls = document.querySelectorAll('*');
    for (const el of allEls) {
      const t = el.textContent.trim();
      if (t === text && el.children.length <= 2) {
        // Try clicking this element
        el.click();
        return true;
      }
    }
    return false;
  }, labelText);
  
  if (clicked) {
    await page.waitForTimeout(1500);
    
    // Check if an input/textarea appeared
    const newInputs = await page.$$('input:not([type="hidden"]):not([type="file"]), textarea, [contenteditable="true"]');
    console.log(`  点击后出现 ${newInputs.length} 个可编辑元素`);
    
    for (const inp of newInputs) {
      try {
        const tag = await inp.evaluate(el => el.tagName);
        const placeholder = await inp.getAttribute('placeholder').catch(() => '');
        const value = await inp.inputValue().catch(() => '');
        const contentEditable = await inp.getAttribute('contenteditable').catch(() => '');
        console.log(`    <${tag}> placeholder="${placeholder}" value="${value?.substring(0, 60)}" contentEditable="${contentEditable}"`);
        
        // Fill in the new value
        if (contentEditable === 'true') {
          await inp.click();
          await inp.fill(newValue);
          console.log(`    ✅ 已填入 (contenteditable)`);
        } else if (tag === 'TEXTAREA' || tag === 'INPUT') {
          await inp.click({ clickCount: 3 });
          await inp.fill(newValue);
          console.log(`    ✅ 已填入 (${tag})`);
        }
        
        return true;
      } catch (e) {
        // skip
      }
    }
    
    // If no input appeared, the value area itself might be the editable thing
    // Try finding the parent container and clicking its value part
    console.log('  ⚠️ 未出现输入框，尝试点击值区域...');
  }
  
  // Alternative: try clicking the parent container
  const parentClicked = await page.evaluate((text) => {
    const allEls = document.querySelectorAll('*');
    for (const el of allEls) {
      const t = el.textContent.trim();
      if (t.startsWith(text) && t.length > text.length + 2) {
        // This element contains the label AND the value
        el.click();
        return { clicked: true, fullText: t.substring(0, 100) };
      }
    }
    return { clicked: false };
  }, labelText);
  
  if (parentClicked.clicked) {
    console.log(`  点击了包含标签和值的容器: "${parentClicked.fullText}"`);
    await page.waitForTimeout(1500);
    
    const newInputs = await page.$$('input:not([type="hidden"]):not([type="file"]), textarea, [contenteditable="true"]');
    console.log(`  出现 ${newInputs.length} 个元素`);
    
    for (const inp of newInputs) {
      try {
        const tag = await inp.evaluate(el => el.tagName);
        let value = '';
        try { value = await inp.inputValue(); } catch(e) { try { value = await inp.textContent() || ''; } catch(e2) {} }
        console.log(`    <${tag}> value="${value?.substring(0, 60)}"`);
      } catch(e) {}
    }
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
    console.log('⏳ 等待页面渲染...');
    await page.waitForTimeout(5000);
    
    // Scroll through the page to ensure all lazy content loads
    await page.evaluate(() => window.scrollTo(0, 200));
    await page.waitForTimeout(500);
    await page.evaluate(() => window.scrollTo(0, 500));
    await page.waitForTimeout(500);
    await page.evaluate(() => window.scrollTo(0, 800));
    await page.waitForTimeout(500);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(500);

    // Show page structure around key labels
    console.log('\n🔍 页面结构探查:');
    const structure = await page.evaluate(() => {
      const results = [];
      document.querySelectorAll('*').forEach(el => {
        const t = el.textContent.trim();
        if (['一句话介绍', '个人简介', '性别', '所在行业', '职业经历', '教育经历'].includes(t) && el.children.length <= 2) {
          const parent = el.parentElement;
          const grandparent = parent?.parentElement;
          
          results.push({
            label: t,
            elTag: el.tagName,
            elClass: el.className?.substring(0, 50) || '',
            parentTag: parent?.tagName || '',
            parentClass: parent?.className?.substring(0, 50) || '',
            grandparentTag: grandparent?.tagName || '',
            grandparentClass: grandparent?.className?.substring(0, 50) || '',
            siblings: Array.from(parent?.children || []).map(c => ({
              tag: c.tagName,
              text: c.textContent?.trim()?.substring(0, 40) || '',
              className: c.className?.substring(0, 40) || '',
            })),
          });
        }
      });
      return results;
    });
    
    structure.forEach(s => {
      console.log(`\n  📌 "${s.label}"`);
      console.log(`     标签: <${s.elTag}> class="${s.elClass}"`);
      console.log(`     父级: <${s.parentTag}> class="${s.parentClass}"`);
      console.log(`     爷级: <${s.grandparentTag}> class="${s.grandparentClass}"`);
      console.log(`     兄弟:`, JSON.stringify(s.siblings));
    });

    // Edit headline
    await editField(page, '一句话介绍', NEW_HEADLINE);
    
    // Wait a bit
    await page.waitForTimeout(2000);
    
    // Edit description
    await editField(page, '个人简介', NEW_DESCRIPTION);
    
    // Scroll and find save button
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1000);
    
    console.log('\n💾 查找保存按钮...');
    const saveBtn = await page.$('button:has-text("保存"), button:has-text("提交"), button:has-text("完成")');
    if (saveBtn) {
      const text = await saveBtn.textContent();
      console.log(`  找到: "${text.trim()}"`);
      await saveBtn.click();
      await page.waitForTimeout(3000);
      console.log('  ✅ 已点击保存');
    } else {
      console.log('  ⚠️ 未找到保存按钮');
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
