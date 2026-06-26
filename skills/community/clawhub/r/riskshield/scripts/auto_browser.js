/**
 * RiskShield Auto Approve - Browser Only
 * Simulates user's actual manual operation
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604131000000597537';
const SEARCH_PARTIAL = CASE_NO.slice(-14);  // Last 14 chars like in user's screenshot

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`Starting browser auto approve for: ${CASE_NO}`);
    log(`Search partial: ${SEARCH_PARTIAL}`);

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        ignoreHTTPSErrors: true
    });

    const page = await context.newPage();

    try {
        // Step 1: Login
        log('Step 1: Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();

        // Wait for navigation
        await page.waitForTimeout(12000);
        log(`Current URL: ${page.url().substring(0, 80)}...`);

        // Verify we're on case list
        if (!page.url().includes('anytask-web')) {
            log('ERROR: Not on case list page');
            return;
        }
        log('On case list page');

        // Step 2: Clear any existing filters first
        log('Step 2: Clearing filters...');
        const clearBtn = page.locator('button:has-text("Clear")');
        if (await clearBtn.count() > 0) {
            await clearBtn.click();
            await page.waitForTimeout(2000);
        }

        // Step 3: Find the case number input and search
        log(`Step 3: Searching for: ${SEARCH_PARTIAL}`);

        // Get all text inputs
        const inputs = await page.locator('input[type="text"]').all();
        log(`Found ${inputs.length} text inputs`);

        // The case input is the 3rd one (index 2)
        const caseInput = inputs[2];

        // Click and clear
        await caseInput.click();
        await page.waitForTimeout(500);
        await caseInput.clear();
        await page.waitForTimeout(500);

        // Type character by character to simulate user
        for (const char of SEARCH_PARTIAL) {
            await caseInput.type(char, { delay: 30 });
        }
        await page.waitForTimeout(500);

        const inputVal = await caseInput.inputValue();
        log(`Input value: "${inputVal}"`);

        // Click Search button
        log('Step 4: Clicking Search...');
        const searchBtn = page.locator('button:has-text("Search")');
        await searchBtn.click();
        await page.waitForTimeout(5000);

        // Step 5: Check results
        const pageText = await page.locator('body').textContent();
        const found = pageText.includes(CASE_NO);
        log(`Case ${CASE_NO} found: ${found}`);

        if (!found) {
            // Debug: show what's in the table
            const rows = await page.locator('tbody tr').all();
            log(`Table has ${rows.length} rows`);

            if (rows.length === 1) {
                const firstCell = await page.locator('tbody tr td').first().textContent();
                log(`First cell: "${firstCell}"`);
            }

            // Try a different approach: use the exact number from user's screenshot
            log('Trying with 26041310000005...');
            await caseInput.clear();
            await page.waitForTimeout(300);
            await caseInput.fill('26041310000005');
            await page.waitForTimeout(500);
            await searchBtn.click();
            await page.waitForTimeout(5000);

            const pageText2 = await page.locator('body').textContent();
            log(`Case found with 26041310000005: ${pageText2.includes(CASE_NO)}`);
        }

        // Step 6: If found, try to approve
        const finalText = await page.locator('body').textContent();
        if (finalText.includes(CASE_NO)) {
            log(`✅ Case ${CASE_NO} found!`);

            // Find the row and check if it's in processing state
            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const text = await row.textContent();
                if (text.includes(CASE_NO)) {
                    log('Found case row');

                    if (text.includes('审理中')) {
                        log('Status: 审理中');

                        // Find approve button
                        const approveBtn = row.locator('a, button').filter({ hasText: '审批' }).first();
                        if (await approveBtn.count() > 0) {
                            log('Clicking 审批...');
                            await approveBtn.click();
                            await page.waitForTimeout(3000);

                            // Handle confirm dialog
                            const confirmBtn = page.locator('button').filter({ hasText: /确认|确定/ }).first();
                            if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                                log('Confirming...');
                                await confirmBtn.click({ force: true });
                                await page.waitForTimeout(2000);
                            }

                            log('✅ APPROVE SUCCESSFUL!');
                        } else {
                            log('No 审批 button found');
                        }
                    } else {
                        log(`Status: ${text.includes('已结案') ? '已结案' : 'Unknown'}`);
                    }
                    break;
                }
            }
        } else {
            log('❌ Case not found after all attempts');
            await page.screenshot({ path: `/tmp/rs_browser_final.png`, fullPage: true });
            log('Screenshot saved');
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
        await page.screenshot({ path: `/tmp/rs_browser_error.png`, fullPage: true });
    } finally {
        await browser.close();
        log('Done');
    }
})();
