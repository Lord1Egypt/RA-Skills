/**
 * RiskShield Browser Approve - Simple reliable version
 * Opens browser in background, searches case, approves
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604131000000597537';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`Starting RiskShield browser approve for: ${CASE_NO}`);

    // Launch browser in headless mode (no visible window but runs in background)
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });

    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });

    const page = await context.newPage();

    try {
        // Step 1: Open login page
        log('[1/6] Opening login page...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        // Step 2: Login
        log('[2/6] Logging in...');
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(10000);

        if (!page.url().includes('anytask-web')) {
            log('ERROR: Login failed');
            return;
        }
        log('[2/6] Login success');

        // Step 3: Wait for page to fully load
        log('[3/6] Waiting for case list to load...');
        await page.waitForSelector('tbody tr', { timeout: 10000 });
        await page.waitForTimeout(3000);

        // Step 4: Enter case number in the search box
        log(`[4/6] Searching for case: ${CASE_NO}`);
        
        // The case search input is the 3rd text input (index 2)
        const inputs = await page.locator('input[type="text"]').all();
        const caseInput = inputs[2];
        
        await caseInput.click();
        await caseInput.clear();
        await caseInput.fill(CASE_NO);
        log(`[4/6] Entered case number`);
        await page.waitForTimeout(500);

        // Step 5: Click Search button
        log('[5/6] Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // Step 6: Check if case found and approve
        const pageText = await page.locator('body').textContent();
        
        if (pageText.includes(CASE_NO)) {
            log(`[6/6] Case ${CASE_NO} found! Looking for approve button...`);

            // Find the row with the case
            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const rowText = await row.textContent();
                
                if (rowText.includes(CASE_NO)) {
                    log('Found case row');

                    // Check if status is 审理中 (processing)
                    if (rowText.includes('审理中')) {
                        // Find the 审批 button
                        const approveBtn = row.locator('a:has-text("审批"), button:has-text("审批")').first();
                        
                        if (await approveBtn.count() > 0 && await approveBtn.isVisible()) {
                            log('Clicking 审批...');
                            await approveBtn.click();
                            await page.waitForTimeout(3000);

                            // Handle confirmation dialog
                            const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")').first();
                            if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                                log('Confirming...');
                                await confirmBtn.click({ force: true });
                                await page.waitForTimeout(2000);
                            }

                            log('✅ APPROVE SUCCESSFUL!');
                        } else {
                            log('Approve button not visible or not found');
                        }
                    } else if (rowText.includes('已结案')) {
                        log('Case is closed (已结案), cannot approve');
                    }
                    break;
                }
            }
        } else {
            log(`❌ Case ${CASE_NO} not found`);
            
            // Debug: show what's in the table
            const rows = await page.locator('tbody tr').count();
            log(`Table has ${rows} rows`);
            
            if (rows === 1) {
                const cellText = await page.locator('tbody tr td').first().textContent();
                log(`Message: ${cellText}`);
            }
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
        log('Browser closed');
    }
})();
