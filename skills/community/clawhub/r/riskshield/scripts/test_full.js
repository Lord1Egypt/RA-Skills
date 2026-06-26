/**
 * RiskShield - Use JavaScript to set input value directly
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
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        
        // Wait longer for redirect
        await page.waitForTimeout(15000);
        log(`URL after login: ${page.url().substring(0, 80)}...`);

        // Wait for table to fully load
        await page.waitForSelector('tbody tr', { timeout: 15000 });
        await page.waitForTimeout(5000);

        log('Page loaded');

        // Use JavaScript to set the input value directly
        log('Setting case number via JavaScript...');
        
        await page.evaluate(() => {
            const inputs = document.querySelectorAll('input[type="text"]');
            // Find the case input (the one that's not date picker and not business type)
            for (const inp of inputs) {
                if (inp.placeholder === '' || inp.placeholder === 'null') {
                    // This is likely the case number input
                    const rect = inp.getBoundingClientRect();
                    if (rect && rect.width === 240) {  // Case input has width 240
                        // Set value using native setter
                        const nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
                        nativeSetter.call(inp, '2604131000000597537');
                        // Dispatch events
                        inp.dispatchEvent(new Event('input', { bubbles: true }));
                        inp.dispatchEvent(new Event('change', { bubbles: true }));
                        break;
                    }
                }
            }
        });

        await page.waitForTimeout(1000);

        // Verify value was set
        const inputValue = await page.evaluate(() => {
            const inputs = document.querySelectorAll('input[type="text"]');
            for (const inp of inputs) {
                if (inp.placeholder === '' || inp.placeholder === 'null') {
                    const rect = inp.getBoundingClientRect();
                    if (rect && rect.width === 240) {
                        return inp.value;
                    }
                }
            }
            return 'not found';
        });
        log(`Input value: "${inputValue}"`);

        // Click Search button
        log('Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // Check results
        const text = await page.locator('body').textContent();
        log(`Found case: ${text.includes('2604131000000597537')}`);

        if (text.includes('2604131000000597537')) {
            log('✅ Case found!');
            
            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const rowText = await row.textContent();
                if (rowText.includes('2604131000000597537')) {
                    if (rowText.includes('审理中')) {
                        const approveBtn = row.locator('a:has-text("审批")').first();
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
            // Show what's in the table
            const rows = await page.locator('tbody tr td:first-child').allTextContents();
            log('First cells in table:');
            rows.slice(0, 5).forEach((c, i) => log(`  ${i}: ${c}`));
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
