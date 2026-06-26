#!/usr/bin/env node

const path = require('path');
const { chromium } = require('./playwright');

const targetIndex = process.argv.indexOf('--target-id');
const targetId = targetIndex >= 0 ? process.argv[targetIndex + 1] : '';
const cdpUrlIndex = process.argv.indexOf('--cdp-url');
const cdpUrl = cdpUrlIndex >= 0 ? process.argv[cdpUrlIndex + 1] : 'http://127.0.0.1:18800';

async function findPageByTargetId(browser, expectedTargetId) {
  for (const context of browser.contexts()) {
    for (const page of context.pages()) {
      try {
        const cdp = await page.context().newCDPSession(page);
        const info = await cdp.send('Target.getTargetInfo');
        if (info && info.targetInfo && info.targetInfo.targetId === expectedTargetId) {
          return page;
        }
      } catch {}
    }
  }
  return null;
}

async function readState(page) {
  return page.evaluate(() => {
    const bodyText = document.body ? document.body.innerText : '';
    return {
      title: document.title,
      url: location.href,
      bodySnippet: bodyText.slice(0, 1200),
      textareaCount: document.querySelectorAll('textarea').length,
      editableCount: document.querySelectorAll('[contenteditable="true"]').length,
      hasShare: /Share/i.test(bodyText),
      hasNext: /Next/i.test(bodyText),
      hasTryAgain: /Try again/i.test(bodyText)
    };
  });
}

async function resolvePreviewPage(browser) {
  if (targetId) {
    const targeted = await findPageByTargetId(browser, targetId);
    if (targeted) {
      return targeted;
    }
  }

  for (const context of browser.contexts()) {
    for (const page of context.pages()) {
      try {
        const state = await readState(page);
        if (!state.url.startsWith('https://www.instagram.com/')) {
          continue;
        }
        if (state.textareaCount || state.editableCount || state.hasShare || state.hasNext) {
          return page;
        }
      } catch {}
    }
  }

  return null;
}

async function main() {
  const browser = await chromium.connectOverCDP(cdpUrl);
  try {
    const page = await resolvePreviewPage(browser);
    if (!page) {
      throw new Error('Could not find an Instagram composer page to capture.');
    }

    await page.bringToFront();
    await page.waitForTimeout(500);

    const screenshotPath = path.join('/tmp', `ig-preview-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath });

    console.log(JSON.stringify({
      ok: true,
      screenshotPath,
      state: await readState(page)
    }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(JSON.stringify({
    ok: false,
    error: error.message || String(error)
  }, null, 2));
  process.exit(1);
});
