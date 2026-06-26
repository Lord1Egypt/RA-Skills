/**
 * RiskShield - Debug the exact dropdown structure
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
        await page.waitForTimeout(12000);
        log('Logged in');

        await page.waitForSelector('tbody tr', { timeout: 15000 });
        await page.waitForTimeout(3000);

        // Analyze the search bar structure
        log('Analyzing search bar...');
        
        const searchBarHTML = await page.evaluate(() => {
            // Find the search bar container
            const allElements = document.querySelectorAll('*');
            let searchBar = null;
            
            for (const el of allElements) {
                if (el.textContent === '案件名称案件编号客户姓名电话号码证件号码') {
                    searchBar = el;
                    break;
                }
            }
            
            if (searchBar) {
                return {
                    tag: searchBar.tagName,
                    className: searchBar.className,
                    parent: searchBar.parentElement?.className,
                    innerHTML: searchBar.innerHTML?.substring(0, 500)
                };
            }
            return null;
        });
        
        log('Search bar: ' + JSON.stringify(searchBarHTML, null, 2));

        // Try to find and click the dropdown
        log('Looking for cascader dropdown...');
        
        // Find the cascader input (with "Please Select" placeholder)
        const cascaderInput = page.locator('.ant-cascader-input, .ant-select-selection-search-input').first();
        if (await cascaderInput.count() > 0) {
            log('Found cascader input, clicking...');
            await cascaderInput.click();
            await page.waitForTimeout(2000);
            
            // Check if dropdown appeared
            const dropdown = page.locator('.ant-select-dropdown, .ant-cascader-dropdown');
            const dropdownVisible = await dropdown.first().isVisible();
            log(`Dropdown visible: ${dropdownVisible}`);
            
            if (dropdownVisible) {
                // Look for 案件编号 option
                const option = page.locator('.ant-select-item-option:has-text("案件编号"), .ant-cascader-menu-item:has-text("案件编号")').first();
                if (await option.count() > 0) {
                    log('Found 案件编号 option, clicking...');
                    await option.click();
                    await page.waitForTimeout(1000);
                }
            }
        }

        // Take screenshot
        await page.screenshot({ path: '/tmp/rs_dropdown.png' });
        log('Screenshot saved');

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
