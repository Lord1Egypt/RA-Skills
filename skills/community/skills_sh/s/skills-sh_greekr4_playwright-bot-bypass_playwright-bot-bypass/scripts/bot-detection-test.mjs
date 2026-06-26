#!/usr/bin/env node
/**
 * Bot Detection Test Script
 * Tests if the stealth configuration bypasses bot detection
 *
 * Usage: node bot-detection-test.mjs
 * Requires: npm install rebrowser-playwright
 */

import os from 'node:os';
import path from 'node:path';
import { createStealthBrowser } from './stealth-template.mjs';

async function testBotDetection() {
  console.log('Bot Detection Test Starting...\n');

  const { browser, page } = await createStealthBrowser();

  try {
    console.log('Navigating to bot.sannysoft.com...\n');
    await page.goto('https://bot.sannysoft.com', { waitUntil: 'networkidle' });
    await page.waitForSelector('table tr td', { timeout: 10000 });

    const results = await page.evaluate(() => {
      const getResult = (testName) => {
        const rows = document.querySelectorAll('table tr');
        for (const row of rows) {
          const cells = row.querySelectorAll('td');
          if (cells.length >= 2 && cells[0].textContent.includes(testName)) {
            const resultCell = cells[1];
            const isRed = resultCell.style.backgroundColor === 'rgb(255, 102, 102)' ||
                         resultCell.style.backgroundColor === '#ff6666' ||
                         resultCell.classList.contains('failed');
            return {
              value: resultCell.textContent.trim(),
              passed: !isRed && !resultCell.textContent.includes('failed')
            };
          }
        }
        return { value: 'N/A', passed: true };
      };

      return {
        userAgent: getResult('User Agent'),
        webDriver: getResult('WebDriver'),
        webDriverAdvanced: getResult('WebDriver Advanced'),
        chrome: getResult('Chrome'),
        plugins: getResult('Plugins'),
        languages: getResult('Languages'),
        webglVendor: getResult('WebGL Vendor'),
        webglRenderer: getResult('WebGL Renderer')
      };
    });

    console.log('='.repeat(45));
    console.log('           BOT DETECTION RESULTS           ');
    console.log('='.repeat(45) + '\n');

    const tests = [
      ['User Agent', results.userAgent],
      ['WebDriver', results.webDriver],
      ['WebDriver Advanced', results.webDriverAdvanced],
      ['Chrome', results.chrome],
      ['Plugins', results.plugins],
      ['Languages', results.languages],
      ['WebGL Vendor', results.webglVendor],
      ['WebGL Renderer', results.webglRenderer]
    ];

    let allPassed = true;
    for (const [name, result] of tests) {
      const status = result.passed ? 'PASS' : 'FAIL';
      if (!result.passed) allPassed = false;
      console.log(`[${status}] ${name.padEnd(20)} ${result.value.substring(0, 50)}`);
    }

    console.log('\n' + '='.repeat(45));
    if (allPassed) {
      console.log('ALL TESTS PASSED - Bot detection bypassed!');
    } else {
      console.log('SOME TESTS FAILED - May be detected as bot');
    }
    console.log('='.repeat(45) + '\n');

    const outOk = path.join(os.tmpdir(), 'bot-detection-result.png');
    await page.screenshot({ path: outOk });
    console.log(`Screenshot saved: ${outOk}\n`);
  } catch (err) {
    console.error('Error:', err.message);
    await page.screenshot({ path: path.join(os.tmpdir(), 'bot-detection-error.png') }).catch(() => {});
  } finally {
    await browser.close();
  }
}

testBotDetection().catch(console.error);
