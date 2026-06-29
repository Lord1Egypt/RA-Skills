#!/usr/bin/env node
/**
 * ux-usability-auditor — inspect.js
 *
 * Automated UX/usability inspector for web applications.
 * Navigates through target app pages via Playwright, captures screenshots
 * and UI element metadata, outputs structured JSON for report generation.
 *
 * Usage:
 *   node scripts/inspect.js path/to/config.json
 *
 * Output:
 *   results/inspection_results.json
 *   results/screenshots/*.png
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ── Helpers ─────────────────────────────────────────────────────────────────────

function log(msg) {
  console.log(`[inspect] ${msg}`);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function sanitizeFileName(name) {
  return name.replace(/[<>:"/\\|?*#\s]/g, '_').substring(0, 100);
}

// ── Page Discovery ──────────────────────────────────────────────────────────────

async function discoverPagesFromSidebar(page, config) {
  log('Auto-discovering pages from sidebar/menu...');

  // Click to expand collapsed menus, then collect all links
  const pages = await page.evaluate(() => {
    // Try to expand all collapsed sub-menus
    const expandEls = document.querySelectorAll(
      '.el-submenu__title, .ant-menu-submenu-title, [class*="menu"] [class*="expand"], [class*="menu"] [class*="arrow"]'
    );
    expandEls.forEach((el) => {
      try { el.click(); } catch (_) {}
    });

    // Collect all navigation links
    const links = Array.from(
      document.querySelectorAll('a[href], a[href="#"], a[href*="#"], .menu-item, [class*="menu-item"]')
    );

    const seen = new Set();
    const results = [];

    links.forEach((el) => {
      const text = (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
      let href = el.getAttribute('href') || '';
      // For SPA hash routes, resolve full URL
      if (href && !href.startsWith('http')) {
        href = window.location.origin + window.location.pathname + href;
      }
      const key = text + '||' + href;
      if (text.length > 1 && text.length < 50 && !seen.has(key)) {
        seen.add(key);
        results.push({ name: text, url: href || window.location.href });
      }
    });

    return results;
  });

  log(`Discovered ${pages.length} pages from sidebar`);
  return pages;
}

async function discoverPagesFromConfig(page, configPages) {
  const baseUrl = configPages.baseUrl || config.targetUrl.split('#')[0];
  return configPages.map((p) => ({
    name: p.name,
    url: p.url.startsWith('http') ? p.url : baseUrl + (p.url.startsWith('/') ? p.url.slice(1) : p.url),
  }));
}

// ── UI Element Extraction ───────────────────────────────────────────────────────

async function extractUIStats(page) {
  return await page.evaluate(() => {
    const buttons = Array.from(document.querySelectorAll('button, .el-button, .ant-btn, [class*="btn"]'));
    const inputs = Array.from(document.querySelectorAll('input, textarea, .el-input__inner, .ant-input'));
    const tables = Array.from(document.querySelectorAll('table, .el-table, .ant-table'));
    const forms = Array.from(document.querySelectorAll('form, .el-form, .ant-form'));
    const dialogs = Array.from(document.querySelectorAll('.el-dialog__wrapper, .ant-modal-wrap, [class*="modal"]:visible, [class*="dialog"]:visible'));

    // Action buttons (not disabled, visible)
    const actionButtons = buttons
      .filter((b) => !b.disabled && b.offsetParent !== null)
      .map((b) => (b.innerText || b.textContent || '').replace(/\s+/g, ' ').trim())
      .filter((t) => t.length > 0 && t.length < 30);

    // Empty state detection
    const bodyText = document.body.innerText || '';
    let emptyState = '';
    if (/暂无数据|无数据|暂无内容|暂无记录|no data|No Data/i.test(bodyText)) {
      const match = bodyText.match(/(暂无数据|无数据|暂无内容|暂无记录|no data|No Data)[^\n.]*/i);
      emptyState = match ? match[0].trim() : '空状态已检测';
    }

    // Breadcrumb
    const breadcrumbEls = document.querySelectorAll('.el-breadcrumb, .ant-breadcrumb, [class*="breadcrumb"]');
    const breadcrumb = breadcrumbEls.length > 0
      ? Array.from(breadcrumbEls[0].querySelectorAll('*'))
          .map((el) => (el.innerText || '').trim())
          .filter((t) => t.length > 0)
          .join(' > ')
      : '';

    // Search area
    const searchInputs = Array.from(document.querySelectorAll('input[placeholder*="搜索"], input[placeholder*="search"], input[type="search"]'));
    const searchArea = searchInputs.length > 0 ? 'detected' : '';

    // Is page still loading?
    const isLoading = !!document.querySelector(
      '.el-loading-mask, .ant-spin, [class*="loading"], [class*="spinner"]'
    );

    // Error detection
    const errorEls = document.querySelectorAll('.el-message--error, .ant-message-error, [class*="error"]:visible');
    const error = errorEls.length > 0
      ? Array.from(errorEls)
          .map((el) => (el.innerText || '').trim())
          .join('; ')
      : '';

    return {
      buttons: buttons.length,
      inputs: inputs.length,
      tables: tables.length,
      forms: forms.length,
      dialogs: dialogs.length,
      actionButtons: [...new Set(actionButtons)].slice(0, 20),
      emptyState,
      breadcrumb,
      searchArea,
      isLoading,
      error,
    };
  });
}

// ── Main Inspection Logic ──────────────────────────────────────────────────────

async function runInspection(config) {
  const outputDir = config.outputDir || './results';
  const screenshotDir = config.screenshotDir || `${outputDir}/screenshots`;
  ensureDir(outputDir);
  ensureDir(screenshotDir);

  log(`Launching browser (headless=${!!config.headless})...`);
  const browser = await chromium.launch({ headless: config.headless || false });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  // ── Login ──────────────────────────────────────────────────────────────────
  log(`Navigating to login page: ${config.targetUrl}`);
  await page.goto(config.targetUrl, { waitUntil: 'networkidle', timeout: 30000 });
  await sleep(2000);

  log('Filling login form...');
  const login = config.login;

  // Try multiple selector strategies
  const userFilled = await page.locator(login.usernameSelector || 'input[type="text"], input[placeholder*="账号"], input[placeholder*="用户名"], input[placeholder*="user"]').first().fill(login.username).then(() => true).catch(() => false);
  if (!userFilled) log('WARNING: Could not fill username field');

  const passFilled = await page.locator(login.passwordSelector || 'input[type="password"], input[placeholder*="密码"], input[placeholder*="password"]').first().fill(login.password).then(() => true).catch(() => false);
  if (!passFilled) log('WARNING: Could not fill password field');

  await sleep(1000);

  log('Submitting login...');
  await page.locator(login.submitSelector || 'button:has-text("登录"), button:has-text("Login"), button:has-text("登錄"), .login-btn, [type="submit"]').first().click().catch(async () => {
    // Fallback: press Enter
    await page.keyboard.press('Enter');
  });

  await sleep(3000);
  log(`Login complete. Current URL: ${page.url()}`);

  // ── Discover Pages ─────────────────────────────────────────────────────────
  let pages = [];
  if (config.pages && config.pages.length > 0) {
    pages = await discoverPagesFromConfig(page, config.pages);
  } else {
    pages = await discoverPagesFromSidebar(page, config);
  }

  if (pages.length === 0) {
    log('WARNING: No pages discovered. Using current URL as single page.');
    pages = [{ name: 'Home', url: page.url() }];
  }

  // Limit for safety
  const maxPages = config.maxPages || 80;
  if (pages.length > maxPages) {
    log(`Limiting to ${maxPages} pages (discovered ${pages.length})`);
    pages = pages.slice(0, maxPages);
  }

  log(`Starting inspection of ${pages.length} pages...`);

  // ── Inspect Each Page ─────────────────────────────────────────────────────
  const results = [];

  for (let i = 0; i < pages.length; i++) {
    const p = pages[i];
    log(`[${i + 1}/${pages.length}] ${p.name} (${p.url})`);

    try {
      await page.goto(p.url, { waitUntil: 'networkidle', timeout: 20000 }).catch(() => {});
      await sleep(config.pageWaitMs || 2500);

      const screenshotName = `${String(i + 1).padStart(2, '0')}_${sanitizeFileName(p.name)}.png`;
      const screenshotPath = path.join(screenshotDir, screenshotName);
      await page.screenshot({ path: screenshotPath, fullPage: false }).catch(() => {});

      const uiStats = await extractUIStats(page);

      const result = {
        page: p.name,
        status: 'ok',
        url: page.url(),
        screenshot: screenshotPath,
        ...uiStats,
      };
      results.push(result);
      log(`  → ${result.buttons} buttons / ${result.inputs} inputs / ${result.tables} tables | empty: ${result.emptyState || 'no'}`);
    } catch (err) {
      log(`  ERROR on ${p.name}: ${err.message}`);
      results.push({ page: p.name, status: 'error', url: p.url, error: err.message });
    }
  }

  // ── Write Results ─────────────────────────────────────────────────────────
  const resultPath = path.join(outputDir, 'inspection_results.json');
  fs.writeFileSync(resultPath, JSON.stringify(results, null, 2));
  log(`Results written to ${resultPath} (${results.length} pages)`);

  await browser.close();
  log('Inspection complete!');
  return results;
}

// ── Entry Point ────────────────────────────────────────────────────────────────

async function main() {
  const configPath = process.argv[2];
  if (!configPath) {
    console.error('Usage: node inspect.js path/to/config.json');
    process.exit(1);
  }

  if (!fs.existsSync(configPath)) {
    console.error(`Config file not found: ${configPath}`);
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  await runInspection(config);
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
