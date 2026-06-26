#!/usr/bin/env node
/**
 * Update Zhihu profile via API + browser (using fetch from logged-in page)
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
    // Navigate to zhihu first to establish session
    console.log('📡 打开知乎首页建立会话...');
    await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    // Get XSRF token
    const xsrf = await page.evaluate(() => {
      const match = document.cookie.match(/_xsrf=([^;]+)/);
      return match ? match[1] : '';
    });
    console.log(`🔑 _xsrf: ${xsrf?.substring(0, 10)}...`);

    // Method 1: Try PUT /api/v4/members/{id} 
    console.log('\n📡 方法1: 尝试 PUT /api/v4/me...');
    
    const result1 = await page.evaluate(async ({ headline, description, xsrf }) => {
      try {
        const res = await fetch('https://www.zhihu.com/api/v4/me', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-XSRF-TOKEN': xsrf,
            'x-requested-with': 'fetch',
          },
          credentials: 'include',
          body: JSON.stringify({ headline, description }),
        });
        const data = await res.json().catch(() => res.text());
        return { status: res.status, ok: res.ok, data };
      } catch (e) {
        return { error: e.message };
      }
    }, { headline: NEW_HEADLINE, description: NEW_DESCRIPTION, xsrf });

    console.log('  结果:', JSON.stringify(result1, null, 2));

    // Method 2: Try PATCH /api/v4/members/{id}
    if (!result1.ok) {
      console.log('\n📡 方法2: 尝试 PATCH /api/v4/me...');
      const result2 = await page.evaluate(async ({ headline, description, xsrf }) => {
        try {
          const res = await fetch('https://www.zhihu.com/api/v4/me', {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              'X-XSRF-TOKEN': xsrf,
              'x-requested-with': 'fetch',
            },
            credentials: 'include',
            body: JSON.stringify({ headline, description }),
          });
          const data = await res.json().catch(() => res.text());
          return { status: res.status, ok: res.ok, data };
        } catch (e) {
          return { error: e.message };
        }
      }, { headline: NEW_HEADLINE, description: NEW_DESCRIPTION, xsrf });
      console.log('  结果:', JSON.stringify(result2, null, 2));
    }

    // Method 3: Try the actual edit page and use keyboard to interact
    console.log('\n📡 方法3: 使用编辑页面+键盘交互...');
    await page.goto('https://www.zhihu.com/people/edit', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(5000);
    
    // Get the edit page's XSRF
    const editXsrf = await page.evaluate(() => {
      const match = document.cookie.match(/_xsrf=([^;]+)/);
      return match ? match[1] : '';
    });

    // Try the settings API
    console.log('\n📡 方法4: 尝试 settings API...');
    const result4 = await page.evaluate(async ({ headline, description, xsrf }) => {
      const endpoints = [
        { url: 'https://www.zhihu.com/api/v4/settings/profile', method: 'PUT' },
        { url: 'https://www.zhihu.com/api/v4/me/profile', method: 'PUT' },
        { url: 'https://www.zhihu.com/api/v4/members/liu-bo-94-4', method: 'PATCH' },
        { url: 'https://www.zhihu.com/api/v4/people/self', method: 'PUT' },
      ];
      
      for (const ep of endpoints) {
        try {
          const res = await fetch(ep.url, {
            method: ep.method,
            headers: {
              'Content-Type': 'application/json',
              'X-XSRF-TOKEN': xsrf,
              'x-requested-with': 'fetch',
            },
            credentials: 'include',
            body: JSON.stringify({ headline, description }),
          });
          
          if (res.ok) {
            const data = await res.json().catch(() => res.text());
            return { success: true, endpoint: ep.url, method: ep.method, data };
          }
          if (res.status === 200 || res.status === 201 || res.status === 204) {
            return { success: true, endpoint: ep.url, method: ep.method, status: res.status };
          }
        } catch (e) {
          // continue
        }
      }
      return { success: false, tried: endpoints.map(e => e.url) };
    }, { headline: NEW_HEADLINE, description: NEW_DESCRIPTION, xsrf: editXsrf });

    console.log('  结果:', JSON.stringify(result4, null, 2));

    // Method 5: Try to click and use keyboard directly
    console.log('\n📡 方法5: 直接键盘操作...');
    
    // Click on the 一句话介绍 的 Field-content
    await page.evaluate(() => {
      const labels = document.querySelectorAll('.Field-label');
      for (const label of labels) {
        if (label.textContent.trim() === '一句话介绍') {
          const field = label.closest('.Field');
          if (field) {
            const content = field.querySelector('.Field-content');
            if (content) {
              // Try to double-click or focus
              const event = new MouseEvent('dblclick', { bubbles: true });
              content.dispatchEvent(event);
            }
          }
        }
      }
    });
    await page.waitForTimeout(2000);
    
    // Check what appeared
    const state = await page.evaluate(() => {
      const edits = document.querySelectorAll('[contenteditable="true"], textarea, input:not([type="hidden"]):not([type="file"])');
      return Array.from(edits).map(e => ({
        tag: e.tagName,
        name: e.getAttribute('name') || '',
        placeholder: e.getAttribute('placeholder') || '',
        value: (e.value || e.textContent || '').substring(0, 80),
        active: document.activeElement === e,
      }));
    });
    console.log('  可编辑元素:', JSON.stringify(state, null, 2));

    // Check active element
    const activeInfo = await page.evaluate(() => ({
      tag: document.activeElement?.tagName,
      type: document.activeElement?.getAttribute('type'),
      name: document.activeElement?.getAttribute('name'),
      id: document.activeElement?.getAttribute('id'),
      className: document.activeElement?.className?.substring(0, 60),
    }));
    console.log('  当前焦点:', JSON.stringify(activeInfo));

    // If search bar is active, try pressing Tab or Escape to move focus
    if (activeInfo.tag === 'INPUT' && activeInfo.id?.includes('Popover')) {
      console.log('  搜索栏处于焦点，尝试 Tab 切换到编辑区域...');
      await page.keyboard.press('Escape');
      await page.waitForTimeout(500);
    }

    // Try pressing Enter on the Field-content
    console.log('\n  尝试聚焦一句话介绍区域...');
    const focused = await page.evaluate(() => {
      const labels = document.querySelectorAll('.Field-label');
      for (const label of labels) {
        if (label.textContent.trim() === '一句话介绍') {
          const field = label.closest('.Field');
          if (field) {
            const content = field.querySelector('.Field-content');
            if (content) {
              content.focus();
              content.click();
              return true;
            }
          }
        }
      }
      return false;
    });
    console.log(`  聚焦结果: ${focused}`);
    
    await page.waitForTimeout(1000);
    
    const activeInfo2 = await page.evaluate(() => ({
      tag: document.activeElement?.tagName,
      type: document.activeElement?.getAttribute('type'),
      name: document.activeElement?.getAttribute('name'),
      id: document.activeElement?.getAttribute('id'),
      value: document.activeElement?.value?.substring(0, 60) || document.activeElement?.textContent?.substring(0, 60) || '',
    }));
    console.log('  当前焦点:', JSON.stringify(activeInfo2));

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
