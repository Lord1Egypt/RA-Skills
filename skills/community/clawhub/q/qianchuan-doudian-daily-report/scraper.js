const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

function storageStateFromEnv() {
  const b64 = process.env.STORAGE_STATE_BASE64;
  if (!b64) return null;
  try {
    return JSON.parse(Buffer.from(b64, 'base64').toString('utf8'));
  } catch (e) {
    throw new Error(`STORAGE_STATE_BASE64 不是有效的 Playwright storage state JSON: ${e.message || e}`);
  }
}

function validateStorageState(value) {
  if (!value || typeof value !== 'object') {
    throw new Error('Playwright storage state 必须是对象');
  }
  if (!Array.isArray(value.cookies) || !Array.isArray(value.origins)) {
    throw new Error('Playwright storage state 必须包含 cookies 和 origins 数组');
  }
  return value;
}

function validateTargetUrl(targetUrl) {
  const url = new URL(targetUrl);
  if (url.protocol !== 'https:' || url.hostname !== 'business.oceanengine.com') {
    throw new Error('targetUrl 只允许 https://business.oceanengine.com 下的巨量引擎页面');
  }
  return url.toString();
}

async function scrape(config) {
  const {
    targetUrl,
    storageStatePath = 'storage_state.json',
    tableSelector = 'table',
    headersSelector = 'table thead th',
    rowSelector = 'table tbody tr'
  } = config;

  const safeTargetUrl = validateTargetUrl(targetUrl);
  const storageAbs = path.resolve(process.cwd(), storageStatePath);
  const envStorageState = storageStateFromEnv();
  const hasStorageFile = fs.existsSync(storageAbs);
  if (!envStorageState && hasStorageFile && config.allowLocalStorageState !== true) {
    throw new Error('检测到本地 storage_state.json，但未显式允许读取。若确认该文件来自可信账号且仅用于本次任务，请在 config.json 中设置 allowLocalStorageState=true。推荐使用 STORAGE_STATE_BASE64。');
  }
  if (!envStorageState && !hasStorageFile) {
    throw new Error('缺少登录态。请提供 STORAGE_STATE_BASE64，或在受控环境中放置 storage_state.json 并设置 allowLocalStorageState=true。');
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ storageState: envStorageState ? validateStorageState(envStorageState) : storageAbs });
  const page = await context.newPage();
  await page.goto(safeTargetUrl, { waitUntil: 'networkidle', timeout: 30000 });

  try {
    await page.waitForSelector(tableSelector, { timeout: 15000 });
  } catch (e) {
    console.warn('未检测到 tableSelector，继续尝试提取页面信息（可能仍能提取到数据）。');
  }

  const result = await page.evaluate(({ tableSelector, headersSelector, rowSelector }) => {
    const clean = value => String(value || '').replace(/\s+/g, ' ').trim();
    const parseRow = (tr, headers) => {
      const cells = Array.from(tr.querySelectorAll('td'));
      const obj = {};
      cells.forEach((td, i) => {
        const key = headers[i] || `col_${i}`;
        obj[key] = clean(td.innerText);
      });
      return obj;
    };
    const headers = Array.from(document.querySelectorAll(headersSelector)).map(h => h.innerText.trim());
    const rawRows = Array.from(document.querySelectorAll(rowSelector)).map(tr => parseRow(tr, headers));
    const summary = rawRows.find(row => Object.values(row).some(value => /^共\d+个账户$/.test(clean(value))));
    const rows = rawRows.filter(row => !Object.values(row).some(value => /^共\d+个账户$/.test(clean(value))));
    const table = document.querySelector(tableSelector);
    const tableText = clean(table ? table.innerText : '');
    return { headers, rows, summary, rawRows, tableText };
  }, { tableSelector, headersSelector, rowSelector });

  await browser.close();

  const rows = result.rows || [];
  const parsedSummary = result.summary || parseOceanEngineSummary(result.headers || [], result.tableText || '');
  Object.defineProperty(rows, 'summary', {
    value: parsedSummary,
    enumerable: false
  });
  Object.defineProperty(rows, 'rawRows', {
    value: result.rawRows || rows,
    enumerable: false
  });
  return rows;
}

function parseOceanEngineSummary(headers, text) {
  const match = String(text || '').match(/共\s*\d+\s*个账户\s+([\s\S]*?)(?=\s+[^ \n\r]+ID：|\s+共\s*\d+\s*条记录|$)/);
  if (!match) return null;
  const tokens = match[1].trim().split(/\s+/).filter(Boolean);
  if (!tokens.length) return null;

  const summary = {};
  const startIndex = headers.findIndex(header => header === '整体消耗');
  const valueHeaders = startIndex >= 0 ? headers.slice(startIndex) : headers;
  valueHeaders.forEach((header, index) => {
    if (tokens[index] !== undefined) summary[header] = tokens[index];
  });
  summary.col_0 = match[0].match(/共\s*\d+\s*个账户/)?.[0]?.replace(/\s+/g, '') || '总计';
  return summary;
}

module.exports = { scrape };
