/**
 * RiskShield - Check actual page content and try UI search
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

        // Wait for table to load
        await page.waitForSelector('tbody tr', { timeout: 10000 });
        await page.waitForTimeout(3000);

        // Take screenshot
        await page.screenshot({ path: '/tmp/rs_check.png', fullPage: false });
        log('Screenshot: /tmp/rs_check.png');

        // Get all text content quickly
        const bodyText = await page.locator('body').textContent();
        
        // Check for our case
        log(`Page contains 2604131000000597537: ${bodyText.includes('2604131000000597537')}`);
        
        // Show first few cases in the table
        const caseLinks = await page.locator('tbody td:first-child').allTextContents();
        log(`First 5 cases in table:`);
        caseLinks.slice(0, 5).forEach((c, i) => log(`  ${i}: ${c.substring(0, 50)}`));

        // Now try the search - click on the search input and type
        log('Trying UI search...');
        
        // Get the search inputs
        const inputs = await page.locator('input[type="text"]').all();
        log(`Found ${inputs.length} text inputs`);
        
        for (let i = 0; i < inputs.length; i++) {
            const inp = inputs[i];
            const placeholder = await inp.getAttribute('placeholder');
            const value = await inp.inputValue();
            const box = await inp.boundingBox();
            log(`  Input ${i}: placeholder="${placeholder}", value="${value}", box=${box ? `${box.width}x${box.height}` : 'N/A'}`);
        }

        // The case search input appears to be the one with empty placeholder or specific position
        // Let's try filling each input and searching
        for (let i = 0; i < inputs.length; i++) {
            const inp = inputs[i];
            const box = await inp.boundingBox();
            if (box && box.width > 100) {  // Only visible text inputs
                log(`Trying input ${i}...`);
                await inp.fill('26041310000005');
                await page.waitForTimeout(500);
                
                // Click search
                await page.locator('button:has-text("Search")').click();
                await page.waitForTimeout(3000);
                
                const text = await page.locator('body').textContent();
                if (text.includes('2604131000000597537')) {
                    log(`✅ SUCCESS with input ${i}!`);
                    break;
                } else {
                    log(`Input ${i} did not find case`);
                    await inp.clear();
                    await page.waitForTimeout(500);
                }
            }
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
