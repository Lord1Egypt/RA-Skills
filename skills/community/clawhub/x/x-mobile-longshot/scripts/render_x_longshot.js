#!/usr/bin/env node
const { chromium, devices } = require('playwright');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function parseArgs(argv) {
  const out = {
    url: '',
    outPng: '',
    outPdf: '',
    mode: 'hybrid',
    device: 'iPhone 14 Pro Max',
    waitMs: 4500,
    topFixPx: 1450,
    noPdf: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => argv[++i];
    if (a === '--url') out.url = next();
    else if (a === '--out-png') out.outPng = next();
    else if (a === '--out-pdf') out.outPdf = next();
    else if (a === '--mode') out.mode = next();
    else if (a === '--device') out.device = next();
    else if (a === '--wait-ms') out.waitMs = Number(next());
    else if (a === '--top-fix-px') out.topFixPx = Number(next());
    else if (a === '--no-pdf') out.noPdf = true;
  }
  if (!out.url) throw new Error('Missing --url');
  if (!out.outPng) throw new Error('Missing --out-png');
  if (!out.outPdf && !out.noPdf) out.outPdf = out.outPng.replace(/\.png$/i, '.pdf');
  return out;
}

async function clickIgnore(page) {
  await page.evaluate(() => {
    const selectors = [
      'button[aria-label="忽略"]',
      'button[aria-label="Close"]',
      '[aria-label="忽略"]',
      '[aria-label="Close"]'
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el) { el.click(); break; }
    }
  }).catch(() => {});
}

async function hideOverlays(page) {
  await page.addStyleTag({
    content: `
      html, body { background: #000 !important; }
      ::-webkit-scrollbar { display: none !important; }
      [data-testid="BottomBar"], [aria-label="Messages"] { display: none !important; }
    `
  }).catch(() => {});

  await page.evaluate(() => {
    const nodes = Array.from(document.querySelectorAll('div, section, aside, [role="dialog"]'));
    for (const el of nodes) {
      const txt = (el.innerText || '').trim();
      const s = getComputedStyle(el);
      const fixed = s.position === 'fixed' || s.position === 'sticky';
      const z = Number(s.zIndex || 0);
      if ((fixed || z >= 20 || el.getAttribute('role') === 'dialog') && (
        txt.includes('在应用中查看此帖子') ||
        txt.includes('打开 X') ||
        txt.includes('在 X 上查看更多') ||
        txt.includes('获取应用') ||
        txt.includes('下载应用') ||
        txt.includes('Open app') ||
        txt.includes('See more on X') ||
        txt.includes('Get the app')
      )) {
        el.remove();
      }
    }
    document.body.style.overflow = 'auto';
    document.documentElement.style.overflow = 'auto';
  }).catch(() => {});
}

async function captureViewport(page, outPath) {
  await page.locator('body').screenshot({ path: outPath });
}

function runPython(code) {
  const r = spawnSync('python3', ['-c', code], { encoding: 'utf8' });
  if (r.status !== 0) {
    throw new Error(r.stderr || r.stdout || 'python3 failed');
  }
  return r.stdout.trim();
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  fs.mkdirSync(path.dirname(args.outPng), { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const device = devices[args.device] || devices['iPhone 14 Pro Max'];
  const context = await browser.newContext({
    ...device,
    colorScheme: 'dark',
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai'
  });
  const page = await context.newPage();

  try {
    await page.goto(args.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(args.waitMs);
    await clickIgnore(page);
    await page.waitForTimeout(700);
    await hideOverlays(page);
    await page.waitForTimeout(1000);

    const rawPng = args.outPng.replace(/\.png$/i, '.raw.png');
    const topPng = args.outPng.replace(/\.png$/i, '.top.png');

    await page.screenshot({ path: rawPng, fullPage: true });

    await page.goto(args.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(args.waitMs);
    await clickIgnore(page);
    await page.waitForTimeout(700);
    await hideOverlays(page);
    await page.waitForTimeout(1000);
    await captureViewport(page, topPng);

    const py = `
from PIL import Image
raw = Image.open(r'''${rawPng}''').convert('RGB')
top = Image.open(r'''${topPng}''').convert('RGB')
out = raw.copy()
crop_h = min(${args.topFixPx}, top.size[1], out.size[1])
out.paste(top.crop((0,0,top.size[0],crop_h)), (0,0))
out.save(r'''${args.outPng}''')
print(r'''${args.outPng}''')
`;
    runPython(py);

    if (!args.noPdf) {
      const pyPdf = `
from PIL import Image
img = Image.open(r'''${args.outPng}''').convert('RGB')
img.save(r'''${args.outPdf}''', 'PDF', resolution=144.0)
print(r'''${args.outPdf}''')
`;
      runPython(pyPdf);
    }

    console.log(JSON.stringify({
      ok: true,
      url: args.url,
      outPng: args.outPng,
      outPdf: args.noPdf ? null : args.outPdf,
      device: args.device,
      mode: args.mode,
      title: await page.title()
    }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch(err => {
  console.error(String(err && err.stack || err));
  process.exit(1);
});
