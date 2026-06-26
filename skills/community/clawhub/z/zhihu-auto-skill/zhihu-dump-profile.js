#!/usr/bin/env node
/**
 * Dump personal profile page structure
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

async function main() {
  const cookies = decryptCookies();

  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'zh-CN' });
  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    // Go to personal profile page
    console.log('📡 打开个人主页...');
    await page.goto('https://www.zhihu.com/people/liu-bo-94-4', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    console.log('=== PAGE URL ===');
    console.log(page.url());

    console.log('\n=== ALL BUTTONS ===');
    const buttons = await page.$$eval('button, a.Button', els => els.map(e => ({
      text: e.textContent?.trim() || '',
      tag: e.tagName,
      href: e.href || '',
      className: e.className?.substring(0, 50) || '',
    })).filter(b => b.text.length > 0));
    buttons.forEach(b => console.log(`  <${b.tag}> [${b.text}] class="${b.className}" href="${b.href.substring(0, 80)}"`));

    console.log('\n=== ALL TEXTS containing "编辑/个人/资料/设置/修改" ===');
    const texts = await page.$$eval('*', els => els
      .map(e => e.textContent.trim())
      .filter(t => /编辑|资料|设置|修改|简介|一句话|介绍|描述|headline|desc|bio/i.test(t) && t.length < 80 && t.length > 1)
    );
    const unique = [...new Set(texts)];
    unique.slice(0, 30).forEach(t => console.log(`  ${t}`));

    console.log('\n=== LINKS near "编辑" text ===');
    const editLinks = await page.$$eval('a, button', els => els
      .filter(e => /编辑|资料|设置/.test(e.textContent?.trim() || ''))
      .map(e => ({
        text: e.textContent?.trim(),
        tag: e.tagName,
        href: e.href || '',
        className: e.className?.substring(0, 60) || '',
      }))
    );
    editLinks.forEach(l => console.log(`  <${l.tag}> [${l.text}] href="${l.href}"`));

    // Check if there's an "编辑个人资料" button on the profile
    console.log('\n=== 查找编辑入口 ===');
    const editBtn = await page.$('button:has-text("编辑个人资料"), a:has-text("编辑个人资料"), [class*="ProfileHeader-edit"]');
    if (editBtn) {
      console.log('  ✅ 找到编辑按钮');
      await editBtn.click();
      await page.waitForTimeout(2000);
      console.log('  点击后 URL:', page.url());
      
      console.log('\n=== 编辑页所有 INPUT/TEXTAREA ===');
      const inputs = await page.$$eval('input, textarea', els => els.map(e => ({
        tag: e.tagName,
        type: e.getAttribute('type') || '',
        name: e.getAttribute('name') || '',
        id: e.getAttribute('id') || '',
        placeholder: e.getAttribute('placeholder') || '',
        value: (e.value || '').substring(0, 60),
      })));
      inputs.forEach(i => console.log(`  <${i.tag} name="${i.name}" id="${i.id}" placeholder="${i.placeholder}" value="${i.value}">`));
    } else {
      console.log('  ❌ 未找到编辑按钮');
    }

    console.log('\n⏳ 30秒后关闭...');
    await page.waitForTimeout(30000);

  } catch (err) {
    console.error('❌ 错误:', err.message);
  } finally {
    await browser.close();
  }
}

main();
