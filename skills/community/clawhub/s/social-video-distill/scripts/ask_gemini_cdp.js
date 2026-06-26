#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function arg(name) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : null;
}

const promptFile = arg('--prompt-file');
const promptInline = arg('--prompt');
const browserUrl = arg('--browser-url') || 'http://127.0.0.1:9222';
const appUrl = arg('--app-url') || 'https://gemini.google.com/app';

if (!promptFile && !promptInline) {
  console.error('Usage: ask_gemini_cdp.js --prompt-file /abs/path.txt | --prompt "text" [--browser-url ...]');
  process.exit(2);
}

const prompt = promptInline || fs.readFileSync(path.resolve(promptFile), 'utf8');
const skillDir = path.resolve(__dirname, '..');
const puppeteerPath = path.join(skillDir, '.runtime', 'gemini', 'node_modules', 'puppeteer-core');
if (!fs.existsSync(puppeteerPath)) {
  console.error('INSTALL_RUNTIME_REQUIRED');
  console.error(`Run: bash ${path.join(skillDir, 'scripts', 'install_runtime.sh')}`);
  process.exit(1);
}

const puppeteer = require(puppeteerPath);

async function findInput(page) {
  const selectors = [
    'div[contenteditable="true"]',
    'textarea',
    '[role="textbox"]',
    'rich-textarea div[contenteditable="true"]'
  ];
  for (const sel of selectors) {
    const el = await page.$(sel);
    if (el) return {sel, el};
  }
  return null;
}

async function bodyText(page) {
  return page.evaluate(() => document.body.innerText || '');
}

(async () => {
  const browser = await puppeteer.connect({ browserURL: browserUrl, protocolTimeout: 120000 });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 1100, deviceScaleFactor: 1 });
  await page.goto(appUrl, { waitUntil: 'networkidle2', timeout: 120000 });
  await new Promise(r => setTimeout(r, 4000));

  const initial = await bodyText(page);
  if (/Sign in|登入|登录/.test(initial) && !/Gemini/.test(initial)) {
    console.log('GEMINI_NOT_LOGGED_IN');
    await page.close();
    await browser.disconnect();
    process.exit(1);
  }

  const input = await findInput(page);
  if (!input) {
    console.log('INPUT_NOT_FOUND');
    console.log(initial.slice(0, 4000));
    await page.close();
    await browser.disconnect();
    process.exit(1);
  }

  await page.click(input.sel);
  await page.keyboard.type(prompt, { delay: 1 });
  await page.keyboard.press('Enter');

  let last = await bodyText(page);
  let stable = 0;
  for (let i = 0; i < 60; i++) {
    await new Promise(r => setTimeout(r, 2000));
    const current = await bodyText(page);
    if (current !== last) {
      last = current;
      stable = 0;
      continue;
    }
    stable += 1;
    if (stable >= 2 && current.length > initial.length + 120) break;
  }

  const idx = last.lastIndexOf('Gemini said');
  const out = idx >= 0 ? last.slice(idx + 'Gemini said'.length).trim() : last.slice(Math.max(0, last.length - 5000)).trim();
  console.log(out);

  await page.close();
  await browser.disconnect();
})().catch(async (err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
