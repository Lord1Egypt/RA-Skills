#!/usr/bin/env node
/**
 * Update Zhihu profile - headline + description
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

// ── Optimized profile content ──
const NEW_HEADLINE = '信息系统项目管理师（软考高级）｜高级工程师｜15年政府信息化经验，亲历智慧城市从规划到落地';

const NEW_DESCRIPTION = `沈北新区大数据管理中心 → 辽宁日报社高级工程师

专注领域：数字政府 · 智慧城市 · AI+政务 · 政务信息化项目管理

用一线实战经验，讲透政府数字化转型的现在与未来。`;

async function main() {
  const cookies = decryptCookies();
  console.log('🔍 Cookie 解密成功\n');

  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    // 1. Check login
    console.log('📡 检查登录状态...');
    await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    const loggedIn = await page.$('.AppHeader-profileAvatar');
    if (!loggedIn) throw new Error('未登录，Cookie可能已过期，请重新导出');
    console.log('✅ 已登录\n');

    // 2. Go to settings page
    console.log('📡 打开设置页面...');
    await page.goto('https://www.zhihu.com/settings', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    // 3. Click on "个人资料" in left sidebar
    console.log('📡 点击"个人资料"菜单...');
    
    // Try to find "个人资料" link
    const menuSelectors = [
      'a:has-text("个人资料")',
      'text="个人资料"',
      '.Tabs-link:has-text("个人资料")',
      '[class*="Tabs"] :has-text("个人资料")',
      '.SettingsMenu-item:has-text("个人资料")',
      '[class*="SettingsMenu"] [class*="item"]:has-text("个人资料")',
    ];
    
    let clicked = false;
    for (const sel of menuSelectors) {
      const el = await page.$(sel);
      if (el) {
        await el.click();
        await page.waitForTimeout(2000);
        clicked = true;
        console.log('  ✅ 已点击"个人资料"');
        break;
      }
    }
    
    if (!clicked) {
      console.log('  ⚠️ 未找到"个人资料"菜单，尝试直接打开 URL...');
      // Try direct URL
      await page.goto('https://www.zhihu.com/settings/profile', { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForTimeout(2000);
    }

    // 4. Read current values
    console.log('\n📋 当前简介:');
    const currentHeadline = await page.$eval('textarea[name="headline"], input[name="headline"]', el => el.value).catch(() => '未找到');
    const currentDesc = await page.$eval('textarea[name="description"]', el => el.value).catch(() => '未找到');
    console.log(`  一句话: ${currentHeadline}`);
    console.log(`  描述:   ${currentDesc?.substring(0, 60)}...`);

    // 5. Update headline
    console.log('\n✏️  正在更新一句话介绍...');
    let headlineUpdated = false;
    
    // Try to find by text content on page
    const pageContent = await page.content();
    const hasHeadlineField = pageContent.includes('一句话介绍') || pageContent.includes('headline');
    console.log(`  页面包含"一句话介绍"字段: ${hasHeadlineField ? '是' : '否'}`);
    
    const headlineSelectors = [
      'textarea[name="headline"]',
      'input[name="headline"]',
      '#headline',
      'textarea[placeholder*="一句话"]',
      'input[placeholder*="一句话"]',
      'label:has-text("一句话介绍") + * textarea',
      'label:has-text("一句话介绍") + * input',
    ];
    
    for (const sel of headlineSelectors) {
      try {
        const el = await page.$(sel);
        if (el) {
          console.log(`  找到元素: ${sel}`);
          await el.click({ clickCount: 3 });
          await el.fill(NEW_HEADLINE);
          headlineUpdated = true;
          break;
        }
      } catch (e) {}
    }
    
    if (!headlineUpdated) {
      // Try XPath
      try {
        const el = await page.$('xpath=//*[contains(text(),"一句话介绍") or contains(@placeholder,"一句话") or @name="headline"]');
        if (el) {
          await el.click({ clickCount: 3 });
          await el.fill(NEW_HEADLINE);
          headlineUpdated = true;
          console.log('  通过 XPath 找到并更新');
        }
      } catch (e) {}
    }
    
    if (!headlineUpdated) {
      console.log('  ⚠️ 未找到一句话介绍输入框，可能页面结构不同');
    } else {
      console.log('  ✅ 已填入新内容');
    }

    // 6. Update description
    console.log('✏️  正在更新个人描述...');
    let descUpdated = false;
    
    const descSelectors = [
      'textarea[name="description"]',
      '#description',
      'textarea[placeholder*="介绍"]',
      'label:has-text("个人简介") + * textarea',
      'label:has-text("个人介绍") + * textarea',
      '[class*="ProfileEdit"] textarea',
    ];
    
    for (const sel of descSelectors) {
      try {
        const el = await page.$(sel);
        if (el && !descUpdated) {
          // Skip if it's the headline field
          const value = await el.inputValue();
          if (value === NEW_HEADLINE) continue;
          
          console.log(`  找到元素: ${sel}`);
          await el.click({ clickCount: 3 });
          await el.fill(NEW_DESCRIPTION);
          descUpdated = true;
          break;
        }
      } catch (e) {}
    }
    
    if (!descUpdated) {
      console.log('  ⚠️ 未找到个人描述输入框');
    } else {
      console.log('  ✅ 已填入新内容');
    }

    // 7. Save
    if (headlineUpdated || descUpdated) {
      console.log('\n💾 查找保存按钮...');
      
      // Scroll to find save button
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(500);
      
      const saveSelectors = [
        'button:has-text("保存")',
        'button:has-text("提交")',
        'button[type="submit"]',
        '.Button--primary',
        'button.PrimaryButton',
        '[class*="save"]',
        '[class*="submit"]',
        'button:has-text("完成")',
      ];
      
      let saved = false;
      for (const sel of saveSelectors) {
        try {
          const btn = await page.$(sel);
          if (btn) {
            const text = await btn.textContent().catch(() => '');
            if (text.includes('保存') || text.includes('提交') || text.includes('完成') || text.includes('确认')) {
              console.log(`  找到按钮: "${text.trim()}" (${sel})`);
              await btn.click();
              await page.waitForTimeout(3000);
              saved = true;
              break;
            }
          }
        } catch (e) {}
      }
      
      if (saved) {
        console.log('\n✅ 已尝试保存');
        
        // Verify
        await page.reload({ waitUntil: 'networkidle', timeout: 15000 });
        await page.waitForTimeout(2000);
        
        const newHeadline = await page.$eval('textarea[name="headline"], input[name="headline"]', el => el.value).catch(() => '?');
        const newDesc = await page.$eval('textarea[name="description"]', el => el.value).catch(() => '?');
        
        console.log('\n📋 更新后:');
        console.log(`  一句话: ${newHeadline?.substring(0, 60)}`);
        console.log(`  描述:   ${newDesc?.substring(0, 60)}...`);
        
        if (newHeadline === NEW_HEADLINE && newDesc?.startsWith('沈北新区')) {
          console.log('\n✅ 保存成功！');
        } else {
          console.log('\n⚠️ 保存结果不确定，请手动检查');
        }
      } else {
        console.log('\n⚠️ 未找到保存按钮，请手动保存');
      }
    }

    console.log('\n⏳ 浏览器保持打开30秒供你检查...');
    await page.waitForTimeout(30000);
    
  } catch (err) {
    console.error('❌ 错误:', err.message);
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

main();
