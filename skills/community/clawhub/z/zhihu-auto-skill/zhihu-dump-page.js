#!/usr/bin/env node
/**
 * Dump page structure to understand Zhihu settings page
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
    // Go to settings
    await page.goto('https://www.zhihu.com/settings', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    console.log('=== PAGE URL ===');
    console.log(page.url());
    
    console.log('\n=== ALL LINKS on page ===');
    const links = await page.$$eval('a', els => els.map(e => ({
      text: e.textContent.trim(),
      href: e.href,
      className: e.className,
    })).filter(l => l.text.length > 0 && l.text.length < 30));
    links.forEach(l => console.log(`  [${l.text}] -> ${l.href.substring(0, 80)}`));

    console.log('\n=== ALL TEXTS containing "个人/资料/简介/修改/编辑/headline/desc" ===');
    const texts = await page.$$eval('*', els => els
      .map(e => e.textContent.trim())
      .filter(t => /个人|资料|简介|修改|编辑|一句话|Headline|desc|介绍|昵称|姓名|性别|所在地/.test(t) && t.length < 50 && t.length > 1)
    );
    console.log([...new Set(texts)].join('\n  '));

    console.log('\n=== ALL INPUT/TEXTAREA elements ===');
    const inputs = await page.$$eval('input, textarea', els => els.map(e => ({
      tag: e.tagName,
      type: e.getAttribute('type') || '',
      name: e.getAttribute('name') || '',
      id: e.getAttribute('id') || '',
      placeholder: e.getAttribute('placeholder') || '',
      className: e.className || '',
      value: (e.value || '').substring(0, 40),
    })));
    inputs.forEach(i => console.log(`  <${i.tag} name="${i.name}" id="${i.id}" placeholder="${i.placeholder}" value="${i.value}">`));

    console.log('\n=== ALL BUTTONS ===');
    const buttons = await page.$$eval('button, input[type="submit"]', els => els.map(e => ({
      text: e.textContent?.trim() || e.value,
      type: e.getAttribute('type') || '',
      className: e.className || '',
    })));
    buttons.forEach(b => console.log(`  [${b.text}] class="${b.className}" type="${b.type}"`));

    // Wait before closing
    console.log('\n⏳ 30秒后关闭...');
    await page.waitForTimeout(30000);

  } catch (err) {
    console.error('❌ 错误:', err.message);
  } finally {
    await browser.close();
  }
}

main();
