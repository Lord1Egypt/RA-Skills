/**
 * RiskShield - Test exact user search pattern
 */

const { chromium } = require('playwright');

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

    try {
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);

        log('Logged in');

        // Wait for page
        await page.waitForSelector('tbody tr', { timeout: 10000 });
        await page.waitForTimeout(3000);

        // Try the exact search pattern user showed in screenshot
        // First try with 26041410000005! to verify it works
        const searchTerm = '2604131000000597537';
        log(`Trying search: ${searchTerm}`);

        // Get the case input (3rd text input)
        const inputs = await page.locator('input[type="text"]').all();
        const caseInput = inputs[2];

        // Click to focus first
        await caseInput.click();
        await page.waitForTimeout(300);

        // Clear any existing value
        await caseInput.clear();
        await page.waitForTimeout(300);

        // Type character by character like a user would
        for (const char of searchTerm) {
            await caseInput.type(char, { delay: 50 });
        }
        await page.waitForTimeout(500);

        const inputVal = await caseInput.inputValue();
        log(`Input value after typing: "${inputVal}"`);

        // Click Search button
        log('Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // Check results
        const text = await page.locator('body').textContent();
        log(`Found case 2604131000000597537: ${text.includes('2604131000000597537')}`);

        if (text.includes('2604131000000597537')) {
            log('✅ Case found!');

            // Find approve button
            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const rowText = await row.textContent();
                if (rowText.includes('2604131000000597537')) {
                    if (rowText.includes('审理中')) {
                        const approveBtn = row.locator('a:has-text("审批"), button:has-text("审批")').first();
                        if (await approveBtn.count() > 0) {
                            log('Clicking 审批...');
                            await approveBtn.click();
                            await page.waitForTimeout(3000);

                            const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")').first();
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
            const rowCount = await page.locator('tbody tr').count();
            log(`Rows in table: ${rowCount}`);
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
