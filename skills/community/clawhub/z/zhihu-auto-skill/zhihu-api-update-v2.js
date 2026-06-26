#!/usr/bin/env node
/**
 * Update Zhihu profile via API - try different field names
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
    await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    const xsrf = await page.evaluate(() => {
      const match = document.cookie.match(/_xsrf=([^;]+)/);
      return match ? match[1] : '';
    });
    console.log(`🔑 _xsrf: ${xsrf?.substring(0, 15)}...\n`);

    // Read current profile first
    const current = await page.evaluate(async (xsrf) => {
      const res = await fetch('https://www.zhihu.com/api/v4/me?include=headline,description,bio', {
        headers: { 'X-XSRF-TOKEN': xsrf, 'x-requested-with': 'fetch' },
        credentials: 'include',
      });
      return res.json();
    }, xsrf);
    console.log('📋 当前 profile 字段:');
    console.log(`  headline: "${current.headline}"`);
    console.log(`  description: "${current.description}"`);
    console.log(`  bio: "${current.bio}"`);
    console.log('');

    // Try 1: PUT with headline + description
    console.log('📡 尝试1: PUT /api/v4/me (headline + description)...');
    const r1 = await page.evaluate(async ({ headline, description, xsrf }) => {
      const res = await fetch('https://www.zhihu.com/api/v4/me', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'X-XSRF-TOKEN': xsrf, 'x-requested-with': 'fetch' },
        credentials: 'include',
        body: JSON.stringify({ headline, description }),
      });
      return { status: res.status, data: await res.json().catch(() => null) };
    }, { headline: NEW_HEADLINE, description: NEW_DESCRIPTION, xsrf });
    console.log(`  状态: ${r1.status}, headline: "${r1.data?.headline?.substring(0, 50)}..."`);

    // Try 2: PUT with headline + bio  
    console.log('\n📡 尝试2: PUT /api/v4/me (headline + bio)...');
    const r2 = await page.evaluate(async ({ headline, description, xsrf }) => {
      const res = await fetch('https://www.zhihu.com/api/v4/me', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'X-XSRF-TOKEN': xsrf, 'x-requested-with': 'fetch' },
        credentials: 'include',
        body: JSON.stringify({ headline, bio: description }),
      });
      return { status: res.status, data: await res.json().catch(() => null) };
    }, { headline: NEW_HEADLINE, description: NEW_DESCRIPTION, xsrf });
    console.log(`  状态: ${r2.status}, headline: "${r2.data?.headline?.substring(0, 50)}..."`);

    // Try 3: PATCH
    console.log('\n📡 尝试3: PATCH /api/v4/me (headline + description)...');
    const r3 = await page.evaluate(async ({ headline, description, xsrf }) => {
      const res = await fetch('https://www.zhihu.com/api/v4/me', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-XSRF-TOKEN': xsrf, 'x-requested-with': 'fetch' },
        credentials: 'include',
        body: JSON.stringify({ headline, description }),
      });
      return { status: res.status, data: await res.json().catch(() => null) };
    }, { headline: NEW_HEADLINE, description: NEW_DESCRIPTION, xsrf });
    console.log(`  状态: ${r3.status}, headline: "${r3.data?.headline?.substring(0, 50)}..."`);

    // Verify by re-fetching
    console.log('\n📡 验证: 重新获取 profile...');
    const verify = await page.evaluate(async (xsrf) => {
      const res = await fetch('https://www.zhihu.com/api/v4/me?include=headline,description,bio', {
        headers: { 'X-XSRF-TOKEN': xsrf, 'x-requested-with': 'fetch' },
        credentials: 'include',
      });
      return res.json();
    }, xsrf);
    console.log(`  headline: "${verify.headline}"`);
    console.log(`  description: "${verify.description}"`);
    console.log(`  bio: "${verify.bio}"`);

    if (verify.headline === NEW_HEADLINE) {
      console.log('\n✅ 一句话介绍更新成功！');
    }
    if (verify.description === NEW_DESCRIPTION || verify.bio === NEW_DESCRIPTION) {
      console.log('✅ 个人描述更新成功！');
    }

    // If headline not updated, try monitoring network during manual edit
    if (verify.headline !== NEW_HEADLINE) {
      console.log('\n⚠️ API 更新未生效，尝试监听网络请求...');
      console.log('  请在浏览器中手动编辑并保存，我会捕获API调用');
      
      await page.goto('https://www.zhihu.com/people/edit', { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(3000);
      
      // Monitor network
      page.on('request', req => {
        const url = req.url();
        if (url.includes('/api/') && (req.method() === 'PUT' || req.method() === 'PATCH' || req.method() === 'POST')) {
          console.log(`  📡 ${req.method()} ${url}`);
          if (req.postData()) console.log(`     body: ${req.postData()?.substring(0, 200)}`);
        }
      });
      
      page.on('response', async resp => {
        const url = resp.url();
        if (url.includes('/api/') && resp.request().method() === 'PUT') {
          try {
            const body = await resp.json();
            console.log(`  📥 PUT ${url} -> ${resp.status()}: ${JSON.stringify(body).substring(0, 200)}`);
          } catch(e) {}
        }
      });
      
      console.log('  ⏳ 等待手动操作（3分钟）...');
      await page.waitForTimeout(180000);
    }

  } catch (err) {
    console.error('❌ 错误:', err.message);
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

main();
