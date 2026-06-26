/**
 * RiskShield Auto Approve - Test with Clear button first
 */

const { chromium } = require('playwright');

const CASE_FULL = '2604131000000597537';
const SEARCH_PREFIX = '26041310000005';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`Starting test for case ${CASE_FULL}`);
    
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    
    try {
        // Login
        log('Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);
        
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        
        await page.waitForURL('**/anytask-web/**', { timeout: 20000 });
        await page.waitForTimeout(5000);
        log('Logged in');
        
        // First, click Clear to reset any filters
        log('Clicking Clear button...');
        const clearBtn = page.locator('button:has-text("Clear")');
        if (await clearBtn.count() > 0) {
            await clearBtn.click();
            await page.waitForTimeout(2000);
            log('Cleared filters');
        }
        
        // Check date filter value
        const dateInput = page.locator('input[type="text"]').first();
        const dateValue = await dateInput.inputValue();
        log(`Date filter after clear: "${dateValue}"`);
        
        // Now enter search term
        log(`Entering search: ${SEARCH_PREFIX}`);
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill(SEARCH_PREFIX);
        await page.waitForTimeout(1000);
        
        // Click Search
        log('Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);
        
        // Check results
        const pageText = await page.locator('body').textContent();
        const found = pageText.includes(CASE_FULL);
        log(`Case ${CASE_FULL} found: ${found}`);
        
        if (found) {
            log('✅ Case found! Looking for 审批 button...');
            await page.screenshot({ path: '/tmp/rs_found.png' });
            
            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const text = await row.textContent();
                if (text.includes(CASE_FULL)) {
                    if (text.includes('审理中')) {
                        const approveBtn = row.locator('a, button').filter({ hasText: '审批' }).first();
                        if (await approveBtn.count() > 0) {
                            log('Clicking 审批...');
                            await approveBtn.click();
                            await page.waitForTimeout(3000);
                            
                            const confirmBtn = page.locator('button').filter({ hasText: /确认|确定/ }).first();
                            if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                                await confirmBtn.click({ force: true });
                                log('Confirmed!');
                            }
                            log('✅ APPROVE SUCCESS!');
                        }
                    }
                    break;
                }
            }
        } else {
            log('❌ Case not found');
            await page.screenshot({ path: '/tmp/rs_notfound.png', fullPage: true });
            log(`Rows in table: ${await page.locator('tbody tr').count()}`);
        }
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
        log('Done');
    }
})();
