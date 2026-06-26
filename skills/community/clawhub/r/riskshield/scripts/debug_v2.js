/**
 * RiskShield Debug - Check what's happening
 */

const { chromium } = require('playwright');

async function run() {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

    try {
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);

        console.log('Logged in');

        // Check date before clearing
        const dateInput = page.locator('input[type="text"]').first();
        const dateBefore = await dateInput.inputValue();
        console.log('Date before clear:', dateBefore);

        // DON'T clear - just search directly
        console.log('Searching without clearing...');
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill('26041310000005');
        await page.waitForTimeout(500);

        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // Check results
        const text = await page.locator('body').textContent();
        console.log('Found case:', text.includes('2604131000000597537'));
        console.log('Row count:', await page.locator('tbody tr').count());

        if (!text.includes('2604131000000597537')) {
            const rows = await page.locator('tbody tr').all();
            for (let i = 0; i < Math.min(rows.length, 3); i++) {
                const rowText = await rows[i].textContent();
                console.log(`Row ${i}:`, rowText.substring(0, 80));
            }
        }

        await page.screenshot({ path: '/tmp/rs_debug2.png', fullPage: true });
        console.log('Screenshot saved');

    } catch (error) {
        console.error('ERROR:', error.message);
    } finally {
        await browser.close();
    }
}

run();
