/**
 * RiskShield Simple Test - Fresh page, minimal actions
 */

const { chromium } = require('playwright');

const CASE_FULL = '2604131000000597537';
const SEARCH_PARTIAL = '26041310000005';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        ignoreHTTPSErrors: true
    });
    const page = await context.newPage();
    
    try {
        // Login with fresh context
        log('1. Loading login page...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html', { waitUntil: 'networkidle' });
        await page.waitForTimeout(3000);
        
        log('2. Logging in...');
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.waitForTimeout(200);
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.waitForTimeout(200);
        await page.locator('button:has-text("login")').click();
        
        await page.waitForURL('**/anytask-web/**', { timeout: 30000 });
        log('3. On case list page');
        await page.waitForTimeout(5000);
        
        // Check date filter before any changes
        const dateInput = page.locator('input[type="text"]').first();
        const dateVal = await dateInput.inputValue();
        log(`4. Initial date filter: "${dateVal}"`);
        
        // Check if case exists in default view (without any search)
        const defaultText = await page.locator('body').textContent();
        const caseExistsDefault = defaultText.includes(CASE_FULL);
        log(`5. Case exists in default view: ${caseExistsDefault}`);
        
        if (!caseExistsDefault) {
            // Try to find it by searching
            log(`6. Searching for partial: ${SEARCH_PARTIAL}`);
            
            // Use JavaScript to set the input value directly
            const caseInput = page.locator('input[type="text"]').nth(2);
            
            // Try using page.evaluate to set value like a real user would
            await page.evaluate((searchVal) => {
                const inputs = document.querySelectorAll('input[type="text"]');
                // The case input is typically the 3rd visible text input
                const caseInput = inputs[2];
                if (caseInput) {
                    caseInput.focus();
                    caseInput.value = searchVal;
                    caseInput.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }, SEARCH_PARTIAL);
            
            await page.waitForTimeout(1000);
            
            // Verify the value was set
            const setValue = await page.evaluate(() => {
                const inputs = document.querySelectorAll('input[type="text"]');
                return inputs[2]?.value;
            });
            log(`7. Case input value set to: "${setValue}"`);
            
            // Click Search button
            log('8. Clicking Search...');
            await page.locator('button:has-text("Search")').click();
            await page.waitForTimeout(5000);
            
            // Check results
            const afterSearch = await page.locator('body').textContent();
            const found = afterSearch.includes(CASE_FULL);
            log(`9. Case found after search: ${found}`);
            
            const rowCount = await page.locator('tbody tr').count();
            log(`10. Row count: ${rowCount}`);
            
            if (!found) {
                // Show first row content for debugging
                if (rowCount > 0) {
                    const firstRow = await page.locator('tbody tr').first().textContent();
                    log(`First row: ${firstRow.substring(0, 100)}`);
                }
            } else {
                // Try to approve
                log('11. Attempting to approve...');
                const rows = await page.locator('tbody tr').all();
                for (const row of rows) {
                    const text = await row.textContent();
                    if (text.includes(CASE_FULL)) {
                        if (text.includes('审理中')) {
                            const approveBtn = row.locator('a, button').filter({ hasText: '审批' });
                            if (await approveBtn.count() > 0) {
                                log('12. Clicking 审批...');
                                await approveBtn.first().click();
                                await page.waitForTimeout(3000);
                                
                                // Handle confirm
                                const confirmBtn = page.locator('button').filter({ hasText: /确认|确定/ });
                                if (await confirmBtn.count() > 0 && await confirmBtn.first().isVisible()) {
                                    log('13. Confirming...');
                                    await confirmBtn.first().click({ force: true });
                                    await page.waitForTimeout(2000);
                                }
                                log('✅ APPROVE SUCCESS!');
                            }
                        }
                        break;
                    }
                }
            }
        }
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await page.screenshot({ path: '/tmp/rs_simple_test.png', fullPage: true });
        log('Screenshot saved');
        await browser.close();
        log('Done');
    }
})();
