#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { chromium } = require('./playwright');

const mediaPath = process.argv[2];
const captionFile = process.argv[3];
const doPost = process.argv.includes('--post');
const targetIndex = process.argv.indexOf('--target-id');
const targetId = targetIndex >= 0 ? process.argv[targetIndex + 1] : '';
const cdpUrlIndex = process.argv.indexOf('--cdp-url');
const cdpUrl = cdpUrlIndex >= 0 ? process.argv[cdpUrlIndex + 1] : 'http://127.0.0.1:18800';

if (!mediaPath || !captionFile) {
  console.error(
    'Usage: node prepare-instagram-video-draft.js <media-path> <caption-file> [--target-id <id>] [--cdp-url <url>] [--post]'
  );
  process.exit(1);
}

if (!fs.existsSync(mediaPath)) {
  console.error(`Media file not found: ${mediaPath}`);
  process.exit(1);
}

if (!fs.existsSync(captionFile)) {
  console.error(`Caption file not found: ${captionFile}`);
  process.exit(1);
}

const caption = fs.readFileSync(captionFile, 'utf8').trim();

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

async function pageState(page) {
  return page.evaluate(() => {
    const bodyText = document.body ? document.body.innerText : '';
    return {
      title: document.title,
      url: location.href,
      bodySnippet: bodyText.slice(0, 1200),
      hasTryAgain: /Try again/i.test(bodyText),
      hasSomethingWentWrong: /Something went wrong/i.test(bodyText),
      hasSelectFromComputer: /Select from computer/i.test(bodyText),
      hasCropStep: /Crop/i.test(bodyText),
      textareaCount: document.querySelectorAll('textarea').length,
      editableCount: document.querySelectorAll('[contenteditable="true"]').length
    };
  });
}

async function capture(page, label) {
  const screenshotPath = path.join('/tmp', `ig-draft-${Date.now()}-${label}.png`);
  await page.screenshot({ path: screenshotPath });
  return {
    ...(await pageState(page)),
    screenshotPath
  };
}

async function resolveDraftPage(browser) {
  if (targetId) {
    const targeted = await findPageByTargetId(browser, targetId);
    if (targeted) return targeted;
  }

  for (const context of browser.contexts()) {
    for (const page of context.pages()) {
      try {
        const title = await page.title();
        const url = page.url();
        if (!url.startsWith('https://www.instagram.com/')) {
          continue;
        }
        if (!title.includes('Create new post')) {
          continue;
        }
        const state = await pageState(page);
        if (state.hasTryAgain || state.hasSomethingWentWrong) {
          continue;
        }
        if (state.hasSelectFromComputer || state.hasCropStep || state.textareaCount || state.editableCount) {
          return page;
        }
      } catch {}
    }
  }

  return null;
}

async function uploadIfNeeded(page, mediaFilePath) {
  const state = await pageState(page);
  if (!state.hasSelectFromComputer) {
    return 'upload-not-needed';
  }

  const input = page.locator('input[type="file"]').first();
  await input.setInputFiles(mediaFilePath);

  const startedAt = Date.now();
  while (Date.now() - startedAt < 20000) {
    const nextState = await pageState(page);
    if (nextState.hasTryAgain || nextState.hasSomethingWentWrong) {
      throw new Error('Instagram rejected the uploaded video.');
    }
    if (!nextState.hasSelectFromComputer) {
      return 'uploaded';
    }
    await page.waitForTimeout(500);
  }

  throw new Error('Timed out waiting for Instagram to ingest the uploaded video.');
}

async function ensureOriginalCrop(page) {
  const cropButton = page.getByRole('button', { name: 'Select crop' }).first();
  if (!(await cropButton.count().catch(() => 0))) {
    return 'crop-button-missing';
  }

  await cropButton.click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(500);

  const originalOption = page.getByRole('button', { name: /original/i }).first();
  if (await originalOption.count().catch(() => 0)) {
    await originalOption.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(500);
    return 'clicked-original-option';
  }

  return 'clicked-crop-button';
}

async function advanceToCaption(page) {
  for (let attempt = 0; attempt < 6; attempt += 1) {
    const textarea = page.locator('textarea').first();
    if (await textarea.count().catch(() => 0)) {
      return 'textarea-ready';
    }

    const editable = page.locator('[contenteditable="true"]').first();
    if (await editable.count().catch(() => 0)) {
      return 'editable-ready';
    }

    const nextButton = page.getByRole('button', { name: 'Next' }).first();
    if (await nextButton.count().catch(() => 0)) {
      await nextButton.click({ timeout: 5000 });
      await page.waitForTimeout(1500);
      continue;
    }

    break;
  }

  throw new Error('Caption field not found after advancing through the composer.');
}

async function fillCaption(page, text) {
  const textarea = page.locator('textarea').first();
  if (await textarea.count().catch(() => 0)) {
    await textarea.fill(text);
    return 'textarea';
  }

  const editable = page.locator('[contenteditable="true"]').first();
  if (await editable.count().catch(() => 0)) {
    await editable.click();
    await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A').catch(() => {});
    await page.keyboard.press('Backspace').catch(() => {});
    await page.keyboard.insertText(text);
    return 'editable';
  }

  throw new Error('Caption field not found.');
}

async function clickShare(page) {
  const shareButton = page.getByRole('button', { name: 'Share' }).first();
  if (await shareButton.count().catch(() => 0)) {
    await shareButton.click({ timeout: 5000 });
    return 'clicked-share';
  }

  throw new Error('Share button not found.');
}

async function main() {
  const browser = await chromium.connectOverCDP(cdpUrl);
  try {
    const page = await resolveDraftPage(browser);
    if (!page) {
      throw new Error('Could not find a healthy Instagram create draft tab.');
    }

    await page.bringToFront();
    await page.waitForTimeout(500);

    const before = await capture(page, 'before');
    const uploadResult = await uploadIfNeeded(page, mediaPath);
    const afterUpload = await capture(page, 'after-upload');
    const cropResult = await ensureOriginalCrop(page);
    const afterCrop = await capture(page, 'after-crop');
    const advanceResult = await advanceToCaption(page);
    const afterAdvance = await capture(page, 'after-advance');
    const captionKind = await fillCaption(page, caption);
    await page.waitForTimeout(1000);
    const afterCaption = await capture(page, 'after-caption');

    let shareResult = 'not-requested';
    let afterShare = null;
    if (doPost) {
      shareResult = await clickShare(page);
      await page.waitForTimeout(1500);
      afterShare = await capture(page, 'after-share');
    }

    console.log(JSON.stringify({
      ok: true,
      targetId,
      mediaPath,
      uploadResult,
      cropResult,
      advanceResult,
      captionKind,
      shareResult,
      before,
      afterUpload,
      afterCrop,
      afterAdvance,
      afterCaption,
      afterShare,
      screenshot: afterCaption.screenshotPath
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
