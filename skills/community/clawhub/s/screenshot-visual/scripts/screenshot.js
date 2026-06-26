#!/usr/bin/env node
/**
 * screenshot-visual - Playwright-based screenshot capture + security analysis
 * Usage: node screenshot.js <url> [output_dir]
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node screenshot.js <url> [output_dir]');
  process.exit(1);
}

const targetUrl = args[0];
const outputBase = args[1] || 'screenshots';

async function main() {
  let parsed;
  try {
    parsed = new URL(targetUrl);
  } catch {
    console.error('Invalid URL:', targetUrl);
    process.exit(1);
  }

  const hostname = parsed.hostname.replace(/\./g, '_');
  const timestamp = Date.now();
  const runDir = path.join(outputBase, hostname);
  fs.mkdirSync(runDir, { recursive: true });

  console.log(`[screenshot-visual] Starting scan: ${targetUrl}`);
  console.log(`[screenshot-visual] Output: ${runDir}`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });

  const page = await context.newPage();
  const results = [];

  const pathsToTry = [
    parsed.pathname || '/',
    '/login',
    '/admin',
    '/dashboard',
    '/register',
    '/signup',
    '/api',
    '/debug',
    '/phpmyadmin',
    '/wp-admin',
    '/.env',
    '/config',
    '/swagger',
    '/swagger-ui',
    '/api-docs',
  ];

  for (const p of pathsToTry) {
    const url = `${parsed.origin}${p}`;
    const slug = p.replace(/\//g, '_').replace(/^_/, '') || 'index';
    const screenshotPath = path.join(runDir, `${slug}-${timestamp}.png`);
    const metaPath = path.join(runDir, `${slug}-${timestamp}.json`);

    try {
      const response = await page.goto(url, { timeout: 10000, waitUntil: 'domcontentloaded' });
      const status = response ? response.status() : 0;
      const headers = response ? response.headers() : {};

      // Take screenshot
      await page.screenshot({ path: screenshotPath, fullPage: true });

      // Collect page info
      const title = await page.title().catch(() => '');
      const hasForms = await page.$$eval('form', forms => forms.length);
      const inputs = await page.$$eval('input', inputs => inputs.map(i => ({ type: i.type, name: i.name, id: i.id })));
      const hasCSP = headers['content-security-policy'] ? true : false;
      const hasXFO = headers['x-frame-options'] ? true : false;
      const hasXXP = headers['x-xss-protection'] ? true : false;
      const server = headers['server'] || '';
      const poweredBy = headers['x-powered-by'] || '';

      // Collect interesting JS endpoints from page
      const jsLinks = await page.$$eval('a[href]', anchors =>
        anchors.map(a => a.href).filter(h => h.includes('/api') || h.includes('.json') || h.includes('swagger') || h.includes('debug'))
      );

      // Check for interesting content
      const bodyText = await page.evaluate(() => document.body ? document.body.innerText.slice(0, 500) : '');

      const meta = {
        url,
        status,
        title,
        timestamp,
        headers: {
          server,
          poweredBy,
          hasCSP,
          hasXFO,
          hasXXP,
          contentType: headers['content-type'] || '',
        },
        forms: hasForms,
        inputs: inputs.filter(i => ['password', 'email', 'token', 'secret', 'key', 'auth'].some(k => (i.name + i.id + i.type).toLowerCase().includes(k))),
        interestingLinks: jsLinks.slice(0, 10),
        snippet: bodyText.replace(/\s+/g, ' ').trim().slice(0, 300),
      };

      fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2));

      const severity = status === 200 ? (hasForms ? 'medium' : 'low') : status >= 400 && status < 500 ? 'info' : 'info';
      console.log(`  [${status}] ${url} → ${screenshotPath}`);

      results.push({ url, status, severity, screenshotPath, metaPath, meta });
    } catch (e) {
      console.log(`  [ERR] ${url} → ${e.message}`);
      results.push({ url, error: e.message });
    }
  }

  await browser.close();

  // Generate summary report
  const reportPath = path.join(runDir, `report-${timestamp}.md`);
  const critical = results.filter(r => r.meta && r.meta.forms && r.meta.inputs.length > 0);
  const missingCSP = results.filter(r => r.meta && !r.meta.headers.hasCSP);

  let report = `# Screenshot Visual Analysis Report\n`;
  report += `**Target:** ${targetUrl}\n`;
  report += `**Date:** ${new Date(timestamp).toISOString()}\n`;
  report += `**Pages scanned:** ${results.length}\n\n`;

  report += `## Summary\n\n`;
  report += `| Page | Status | Severity | Screenshot |\n`;
  report += `|------|--------|----------|------------|\n`;
  for (const r of results) {
    if (r.error) {
      report += `| ${r.url} | ERR | - | - |\n`;
    } else {
      report += `| ${r.url} | ${r.status} | ${r.severity} | \`${r.screenshotPath}\` |\n`;
    }
  }

  if (missingCSP.length > 0) {
    report += `\n## Missing CSP\n`;
    for (const r of missingCSP) {
      report += `- ${r.url} — no Content-Security-Policy header\n`;
    }
  }

  if (critical.length > 0) {
    report += `\n## Forms with Sensitive Inputs\n`;
    for (const r of critical) {
      const sensitive = r.meta.inputs.map(i => i.name || i.id).join(', ');
      report += `- ${r.url} — inputs: ${sensitive}\n`;
    }
  }

  fs.writeFileSync(reportPath, report);
  console.log(`\n[screenshot-visual] Report: ${reportPath}`);
  console.log(`[screenshot-visual] Done. ${results.filter(r => !r.error).length} pages captured.`);
}

main().catch(e => { console.error(e); process.exit(1); });