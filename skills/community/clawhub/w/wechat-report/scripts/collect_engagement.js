#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function cleanText(value = '') {
  return String(value).replace(/\s+/g, ' ').trim();
}

function extractJsScalar(html, keys = []) {
  const result = {};
  for (const key of keys) {
    const patterns = [
      new RegExp(`var\\s+${key}\\s*=\\s*"([^"]+)"`),
      new RegExp(`var\\s+${key}\\s*=\\s*'([^']+)'`),
      new RegExp(`var\\s+${key}\\s*=\\s*(\\d+)`),
      new RegExp(`${key}\\s*:\\s*"([^"]+)"`),
      new RegExp(`${key}\\s*:\\s*'([^']+)'`),
      new RegExp(`${key}\\s*:\\s*(\\d+)`)
    ];
    for (const pattern of patterns) {
      const match = html.match(pattern);
      if (match && match[1] !== undefined) {
        result[key] = match[1];
        break;
      }
    }
  }
  return result;
}

function toNumberOrNull(value) {
  if (value === undefined || value === null || value === '') return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function buildMetricPayload(html = '') {
  const raw = extractJsScalar(html, [
    'read_num',
    'like_num',
    'old_like_num',
    'comment_count',
    'comment_id',
    'appmsgid',
    'reward_total_count',
    'friend_comment_enabled',
    'comment_enabled'
  ]);

  const metricsVisible = ['read_num', 'like_num', 'old_like_num', 'comment_count', 'reward_total_count']
    .some((key) => toNumberOrNull(raw[key]) !== null);

  return {
    read_count: toNumberOrNull(raw.read_num),
    like_count: toNumberOrNull(raw.like_num),
    old_like_count: toNumberOrNull(raw.old_like_num),
    comment_count: toNumberOrNull(raw.comment_count),
    reward_total_count: toNumberOrNull(raw.reward_total_count),
    comment_id: raw.comment_id || null,
    appmsg_id: raw.appmsgid || null,
    comment_enabled: raw.comment_enabled === '1' ? true : raw.comment_enabled === '0' ? false : null,
    friend_comment_enabled: raw.friend_comment_enabled === '1' ? true : raw.friend_comment_enabled === '0' ? false : null,
    metrics_visible: metricsVisible,
    status: metricsVisible ? 'visible_in_browser_session' : 'requires_logged_in_session',
    note: metricsVisible
      ? 'Playwright 浏览器会话识别到了互动数字。'
      : 'Playwright 已尝试抓取，但当前浏览器会话仍未暴露互动数字；通常需要有效登录态或页面运行时接口。'
  };
}

function resolvePlaywright(workspaceRoot) {
  const candidates = [
    'playwright',
    path.join(workspaceRoot, 'node_modules', 'playwright'),
    path.join(workspaceRoot, 'skills', 'wechat-studio', 'frontend', 'node_modules', 'playwright')
  ];

  for (const candidate of candidates) {
    try {
      return require(candidate);
    } catch (error) {
      continue;
    }
  }
  return null;
}

async function main() {
  const [, , workspaceRoot, sourceUrl, profileDir] = process.argv;
  if (!workspaceRoot || !sourceUrl || !profileDir) {
    throw new Error('Usage: node collect_engagement.js <workspaceRoot> <sourceUrl> <profileDir>');
  }

  const playwright = resolvePlaywright(workspaceRoot);
  if (!playwright) {
    throw new Error('Playwright dependency not found. Install playwright or reuse the existing frontend dependency first.');
  }

  fs.mkdirSync(profileDir, { recursive: true });
  const context = await playwright.chromium.launchPersistentContext(profileDir, {
    headless: true
  });

  try {
    const page = context.pages()[0] || await context.newPage();
    await page.goto(sourceUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(4000);
    const html = await page.content();
    const result = buildMetricPayload(html);
    result.page_title = cleanText(await page.title().catch(() => '')) || null;
    process.stdout.write(JSON.stringify(result));
  } finally {
    await context.close();
  }
}

main().catch((error) => {
  process.stderr.write(String(error && error.stack ? error.stack : error));
  process.exit(1);
});
