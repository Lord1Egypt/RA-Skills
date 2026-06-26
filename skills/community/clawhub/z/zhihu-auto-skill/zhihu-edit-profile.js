#!/usr/bin/env node
/**
 * Edit Zhihu profile - final version with patience
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
    // Go directly to edit page
    console.log('📡 直接打开编辑页面...');
    await page.goto('https://www.zhihu.com/people/edit', { waitUntil: 'networkidle', timeout: 30000 });
    console.log('⏳ 等待页面完全渲染（React 挂载）...');
    await page.waitForTimeout(3000);
    
    // Scroll to load lazy content
    await page.evaluate(() => window.scrollTo(0, 300));
    await page.waitForTimeout(1000);
    await page.evaluate(() => window.scrollTo(0, 600));
    await page.waitForTimeout(1000);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(1000);

    console.log('\n🔍 页面内容分析:');
    
    // Find ALL elements that look like form fields
    const allFields = await page.evaluate(() => {
      const results = [];
      
      // Check for contenteditable divs (common in React)
      document.querySelectorAll('[contenteditable="true"]').forEach(el => {
        results.push({
          type: 'contenteditable',
          text: el.textContent?.substring(0, 60) || '',
          className: el.className?.substring(0, 60) || '',
          parentText: el.parentElement?.textContent?.substring(0, 80) || '',
        });
      });
      
      // Check inputs/textarea
      document.querySelectorAll('input, textarea').forEach(el => {
        results.push({
          type: el.tagName,
          inputType: el.getAttribute('type') || '',
          name: el.getAttribute('name') || '',
          placeholder: el.getAttribute('placeholder') || '',
          value: (el.value || '').substring(0, 80),
        });
      });
      
      // Check any element with role="textbox"
      document.querySelectorAll('[role="textbox"]').forEach(el => {
        results.push({
          type: 'role-textbox',
          text: el.textContent?.substring(0, 60) || '',
          className: el.className?.substring(0, 60) || '',
        });
      });
      
      return results;
    });
    
    console.log('  可编辑元素:');
    allFields.forEach(f => {
      console.log(`    [${f.type}] ${f.name || f.placeholder || f.inputType || ''} = "${f.value || f.text || ''}"`);
      if (f.parentText) console.log(`      父级文本: ${f.parentText}`);
    });

    // Find all texts containing key words
    console.log('\n  页面关键文本:');
    const keyTexts = await page.evaluate(() => {
      const texts = [];
      document.querySelectorAll('*').forEach(el => {
        if (el.children.length === 0 && el.textContent) {
          const t = el.textContent.trim();
          if (/一句话|介绍|描述|简介|headline|bio|名字|昵称|性别|所在地|行业|职业|教育|编辑/.test(t) && t.length < 50 && t.length > 1) {
            texts.push(t);
          }
        }
      });
      return [...new Set(texts)];
    });
    keyTexts.forEach(t => console.log(`    "${t}"`));

    // ── EDIT HEADLINE ──
    console.log('\n✏️ 寻找并编辑一句话介绍...');
    
    // Strategy: Use evaluate to find and click the right element
    let headlineEdited = false;
    
    // Try to find by text content
    const headlineResult = await page.evaluate(() => {
      // Search for "一句话介绍" label
      const allElements = document.querySelectorAll('*');
      let headlineLabel = null;
      for (const el of allElements) {
        if (el.textContent.trim() === '一句话介绍' && el.children.length <= 1) {
          headlineLabel = el;
          break;
        }
      }
      
      if (headlineLabel) {
        // Find the input/textarea next to this label
        let input = headlineLabel.nextElementSibling;
        while (input && !['INPUT', 'TEXTAREA'].includes(input.tagName) && !input.hasAttribute('contenteditable')) {
          input = input.querySelector('input, textarea, [contenteditable="true"]');
          if (!input) input = input.nextElementSibling;
          if (!input) {
            input = headlineLabel.parentElement?.querySelector('input, textarea, [contenteditable="true"]');
            break;
          }
        }
        
        if (input) {
          return { found: true, tag: input.tagName, parent: headlineLabel.parentElement?.className || '', inputTag: input.tagName };
        }
      }
      
      return { found: false, totalElements: allElements.length };
    });
    
    console.log(`  结果:`, JSON.stringify(headlineResult));

    // Try clicking on editable areas in the profile section
    console.log('\n🖱️ 尝试点击个人资料区域的可编辑元素...');
    
    // Find all clickable things in the profile edit area
    const clickTargets = await page.evaluate(() => {
      const targets = [];
      // Look for elements that might be editable profile fields
      const profileSection = document.querySelector('[class*="Profile"], [class*="profile"], [class*="edit"]');
      const container = profileSection || document.body;
      
      container.querySelectorAll('[class*="editable"], [class*="Editable"], [contenteditable="true"], input, textarea, [class*="headline"], [class*="description"], [class*="bio"]').forEach(el => {
        targets.push({
          tag: el.tagName,
          className: el.className?.substring(0, 60) || '',
          text: (el.textContent || el.value || '').substring(0, 80),
          rect: el.getBoundingClientRect(),
        });
      });
      return targets;
    });
    
    clickTargets.forEach(t => {
      console.log(`  <${t.tag}> class="${t.className}" text="${t.text}" pos=(${Math.round(t.rect.x)},${Math.round(t.rect.y)})`);
    });

    // If no editable elements found, try clicking on text areas
    if (clickTargets.length === 0) {
      console.log('\n  ⚠️ 无可编辑元素，尝试查找可点击的Div...');
      
      const divTexts = await page.evaluate(() => {
        const results = [];
        document.querySelectorAll('div, span').forEach(el => {
          const t = el.textContent?.trim() || '';
          if ((t.includes('一句话') || t.includes('电子政务') || t.includes('信息系统') || t.includes('介绍')) && t.length < 80) {
            results.push({
              tag: el.tagName,
              className: el.className?.substring(0, 60) || '',
              text: t.substring(0, 60),
              cursor: window.getComputedStyle(el).cursor,
              onClick: el.onclick !== null,
            });
          }
        });
        return results;
      });
      
      divTexts.forEach(t => console.log(`    <${t.tag}> "${t.text}" cursor=${t.cursor} hasOnClick=${t.onClick} class="${t.className}"`));
      
      // Try clicking divs that might trigger edit
      for (const dt of divTexts) {
        if (dt.text.includes('一句话')) {
          console.log(`\n  尝试点击: "${dt.text}"`);
          try {
            const el = await page.$(`.${dt.className.split(' ')[0]}`);
            if (el) {
              await el.click({ force: true });
              await page.waitForTimeout(1500);
              
              // Check if input appeared
              const newInputs = await page.$$('input:not([type="hidden"]), textarea');
              console.log(`  点击后出现 ${newInputs.length} 个输入框`);
            }
          } catch(e) {
            console.log(`  点击失败: ${e.message}`);
          }
        }
      }
    }

    // Take screenshot for manual inspection
    await page.screenshot({ path: '/tmp/zhihu_edit_page.png', fullPage: true });
    console.log('\n📸 截图保存到 /tmp/zhihu_edit_page.png');

    console.log('\n⏳ 浏览器保持打开30秒供你手动检查...');
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
