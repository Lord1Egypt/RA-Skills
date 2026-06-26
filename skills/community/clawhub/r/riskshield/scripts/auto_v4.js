/**
 * RiskShield Auto Approve - Fixed prefix
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604131000000597537';
// Use first 14 chars as prefix (like user did in screenshot)
const SEARCH_PREFIX = CASE_NO.substring(0, 14);

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`Case: ${CASE_NO}, Search prefix: ${SEARCH_PREFIX}`);

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

    try {
        // Login
        log('Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);

        if (!page.url().includes('anytask-web')) {
            log('Login failed');
            return;
        }
        log('Logged in');

        // Clear filters
        const clearBtn = page.locator('button:has-text("Clear")');
        if (await clearBtn.count() > 0) {
            await clearBtn.click();
            await page.waitForTimeout(2000);
            log('Filters cleared');
        }

        // Enter search term
        log(`Searching: ${SEARCH_PREFIX}`);
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill(SEARCH_PREFIX);
        await page.waitForTimeout(500);

        // Click Search
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // Check
        const text = await page.locator('body').textContent();
        log(`Case ${CASE_NO} found: ${text.includes(CASE_NO)}`);

        if (text.includes(CASE_NO)) {
            log('✅ Case found! Looking for approve...');

            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const t = await row.textContent();
                if (t.includes(CASE_NO) && t.includes('审理中')) {
                    const btn = row.locator('a, button').filter({ hasText: '审批' }).first();
                    if (await btn.count() > 0) {
                        log('Clicking 审批...');
                        await btn.click();
                        await page.waitForTimeout(3000);

                        const confirm = page.locator('button').filter({ hasText: /确认|确定/ }).first();
                        if (await confirm.count() > 0 && await confirm.isVisible()) {
                            await confirm.click({ force: true });
                            log('Confirmed!');
                        }
                        log('✅ APPROVE SUCCESS!');
                    }
                    break;
                }
            }
        } else {
            log('❌ Not found');
            await page.screenshot({ path: '/tmp/rs_v4.png', fullPage: true });
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
        log('Done');
    }
})();
