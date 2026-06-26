/**
 * RiskShield Debug - Investigate date filter behavior
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
        
        // Check initial date filter
        const dateInput = page.locator('input[type="text"]').first();
        const initialDate = await dateInput.inputValue();
        log(`Initial date: "${initialDate}"`);
        
        // Try clicking on the date input to see what happens
        log('Clicking date input...');
        await dateInput.click();
        await page.waitForTimeout(2000);
        await page.screenshot({ path: '/tmp/rs_date1.png' });
        
        // Try pressing key to open date picker
        await dateInput.press('ArrowDown');
        await page.waitForTimeout(2000);
        await page.screenshot({ path: '/tmp/rs_date2.png' });
        
        // Press Escape to close
        await page.keyboard.press('Escape');
        await page.waitForTimeout(1000);
        
        // Now let's try a different approach: 
        // Use JavaScript to directly set the input value
        log('Setting date via JavaScript...');
        await page.evaluate(() => {
            const inputs = document.querySelectorAll('input[type="text"]');
            if (inputs[0]) {
                // Try to set the value and trigger change event
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(inputs[0], '2026-04-08 - 2026-04-14');
                inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
        
        const dateAfterJS = await dateInput.inputValue();
        log(`Date after JS set: "${dateAfterJS}"`);
        
        await page.waitForTimeout(1000);
        
        // Now try search
        log('Entering search...');
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill('26041310000005');
        await page.waitForTimeout(1000);
        
        log('Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);
        
        // Check
        const pageText = await page.locator('body').textContent();
        log(`Case found: ${pageText.includes(CASE_FULL)}`);
        
        const rows = await page.locator('tbody tr').count();
        log(`Table rows: ${rows}`);
        
        if (rows > 0 && rows < 10) {
            for (let i = 0; i < rows; i++) {
                const text = await page.locator('tbody tr').nth(i).textContent();
                log(`Row ${i}: ${text.substring(0, 100)}`);
            }
        }
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
