/**
 * RiskShield - Fixed: Select "案件编号" from dropdown first
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604131000000597537';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

    try {
        log('[1] Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);
        log('[1] Logged in');

        // Wait for page to load
        await page.waitForSelector('tbody tr', { timeout: 15000 });
        await page.waitForTimeout(3000);

        // CRITICAL: First, click on the dropdown to change search field to "案件编号"
        log('[2] Selecting "案件编号" from search field dropdown...');

        // The dropdown is the element with placeholder "请选择" that appears before the case number input
        // It's a cascader/combobox element
        const dropdown = page.locator('.ant-cascader, .ant-select, input[placeholder="请选择"]').first();
        
        // Try clicking on it to open the dropdown
        await dropdown.click();
        await page.waitForTimeout(1000);

        // Look for "案件编号" option in the dropdown
        const option = page.locator('.ant-select-item, .ant-cascader-menu-item, li:has-text("案件编号")').first();
        if (await option.count() > 0) {
            log('[2] Found "案件编号" option, clicking...');
            await option.click();
            await page.waitForTimeout(1000);
        } else {
            log('[2] Trying alternative approach...');
            
            // Try clicking on the search box itself first to reveal the dropdown
            const searchBox = page.locator('input[type="text"]').nth(2);
            await searchBox.click();
            await page.waitForTimeout(500);
            
            // Press ArrowDown or try to find the selector
            await page.keyboard.press('ArrowDown');
            await page.waitForTimeout(500);
        }

        // Now the dropdown should be set to "案件编号"
        // Enter the case number
        log(`[3] Entering case number: ${CASE_NO}`);
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill(CASE_NO);
        await page.waitForTimeout(500);

        // Click Search
        log('[4] Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // Check results
        const text = await page.locator('body').textContent();
        if (text.includes(CASE_NO)) {
            log(`[5] ✅ Case ${CASE_NO} found!`);

            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const rowText = await row.textContent();
                if (rowText.includes(CASE_NO) && rowText.includes('审理中')) {
                    const approveBtn = row.locator('a:has-text("审批")').first();
                    if (await approveBtn.count() > 0) {
                        log('[6] Clicking 审批...');
                        await approveBtn.click();
                        await page.waitForTimeout(3000);

                        const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")').first();
                        if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                            await confirmBtn.click({ force: true });
                            log('[6] Confirmed!');
                        }
                        log('✅ APPROVE SUCCESS!');
                    }
                    break;
                }
            }
        } else {
            log(`[5] ❌ Case ${CASE_NO} not found`);
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
