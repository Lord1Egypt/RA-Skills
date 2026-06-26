/**
 * RiskShield Test - Click and type instead of fill
 */

const { chromium } = require('playwright');

const CASE_FULL = '2604131000000597537';

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
        
        await page.waitForURL('**/anytask-web/**', { timeout: 20000 });
        await page.waitForTimeout(5000);
        
        log('Testing search...');
        
        // Get the case input
        const caseInput = page.locator('input[type="text"]').nth(2);
        
        // Click to focus
        await caseInput.click();
        await page.waitForTimeout(500);
        
        // Clear first
        await caseInput.clear();
        await page.waitForTimeout(500);
        
        // Type character by character
        const searchText = '26041310000005';
        for (const char of searchText) {
            await caseInput.type(char, { delay: 50 });
        }
        await page.waitForTimeout(500);
        
        // Check value
        const value = await caseInput.inputValue();
        log(`Input value: "${value}"`);
        
        // Press Enter instead of clicking Search
        log('Pressing Enter...');
        await caseInput.press('Enter');
        await page.waitForTimeout(5000);
        
        // Check results
        const pageText = await page.locator('body').textContent();
        log(`Case found: ${pageText.includes(CASE_FULL)}`);
        
        const rows = await page.locator('tbody tr').count();
        log(`Table rows: ${rows}`);
        
        if (rows > 0 && rows < 10) {
            for (let i = 0; i < rows; i++) {
                const text = await page.locator('tbody tr').nth(i).textContent();
                log(`Row ${i}: ${text.substring(0, 80)}...`);
            }
        }
        
        // If still not found, try clicking Search button
        if (!pageText.includes(CASE_FULL)) {
            log('Trying Search button...');
            await caseInput.fill(searchText);
            await page.waitForTimeout(500);
            await page.locator('button:has-text("Search")').click();
            await page.waitForTimeout(5000);
            
            const pageText2 = await page.locator('body').textContent();
            log(`Case found after Search click: ${pageText2.includes(CASE_FULL)}`);
        }
        
        await page.screenshot({ path: '/tmp/rs_final_test.png', fullPage: true });
        log('Screenshot saved');
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
        log('Done');
    }
})();
