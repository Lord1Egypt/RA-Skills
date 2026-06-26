/**
 * RiskShield Debug - Take screenshot after search
 */

const { chromium } = require('playwright');

async function run() {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    
    try {
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);
        
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button[type="submit"], button:has-text("login")').click();
        
        await page.waitForURL('**/anytask-web/**', { timeout: 20000 });
        await page.waitForTimeout(5000);
        
        // Before search
        await page.screenshot({ path: '/tmp/rs_before_search.png' });
        console.log('Before search screenshot saved');
        
        // Fill case number
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill('2604131000000597543');
        console.log('Filled case number');
        await page.waitForTimeout(500);
        
        // Check value was set
        const inputValue = await caseInput.inputValue();
        console.log(`Input value: "${inputValue}"`);
        
        // Click Search
        await page.locator('button:has-text("Search")').click();
        console.log('Clicked Search');
        await page.waitForTimeout(5000);
        
        // After search
        await page.screenshot({ path: '/tmp/rs_after_search.png' });
        console.log('After search screenshot saved');
        
        // Check page text
        const pageText = await page.locator('body').textContent();
        console.log(`Page contains case number: ${pageText.includes('2604131000000597543')}`);
        
        // Get table data
        const rows = await page.locator('tbody tr').all();
        console.log(`Table rows: ${rows.length}`);
        
        // Show first few rows
        for (let i = 0; i < Math.min(rows.length, 5); i++) {
            const text = await rows[i].textContent();
            console.log(`Row ${i}: ${text.substring(0, 100)}...`);
        }
        
    } catch (error) {
        console.error(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
}

run().then(() => process.exit(0));
