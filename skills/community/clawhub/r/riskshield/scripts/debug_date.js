/**
 * RiskShield Debug - Check and modify date filter
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
        
        // Check current date filter
        const dateInput = page.locator('input[type="text"]').first();
        const dateValue = await dateInput.inputValue();
        console.log(`Current date filter: "${dateValue}"`);
        
        // Try to clear or modify date filter
        // Click on the date input to open date picker
        await dateInput.click();
        await page.waitForTimeout(1000);
        
        // Take screenshot to see date picker
        await page.screenshot({ path: '/tmp/rs_date_picker.png' });
        console.log('Date picker screenshot saved');
        
        // Look for a "Clear" button or try to select a wider range
        // Common patterns: clear button, "Reset", or selecting a different preset
        const clearBtn = page.locator('button:has-text("清空"), button:has-text("Clear"), button:has-text("重置")');
        if (await clearBtn.count() > 0) {
            console.log('Found clear/reset button');
            await clearBtn.first().click();
            await page.waitForTimeout(1000);
        }
        
        // Try pressing Escape to close date picker without changes
        await page.keyboard.press('Escape');
        await page.waitForTimeout(500);
        
        // Now try searching without date filter
        console.log('Trying search without case number...');
        const searchBtn = page.locator('button:has-text("Search")');
        await searchBtn.click();
        await page.waitForTimeout(5000);
        
        // Check if cases appear
        const rows = await page.locator('tbody tr').all();
        console.log(`Table rows after clear: ${rows.length}`);
        
        // Show first few rows
        for (let i = 0; i < Math.min(rows.length, 3); i++) {
            const text = await rows[i].textContent();
            console.log(`Row ${i}: ${text.substring(0, 150)}`);
        }
        
        // Also try to get the page HTML structure
        const html = await page.content();
        console.log(`Page has date-related inputs: ${html.includes('date') || html.includes('Date')}`);
        
    } catch (error) {
        console.error(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
}

run().then(() => process.exit(0));
