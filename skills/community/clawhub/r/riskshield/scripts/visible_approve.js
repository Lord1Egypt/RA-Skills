/**
 * RiskShield - NON-HEADLESS mode for testing
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604131000000597537';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    // Launch with headless: false to see the browser
    const browser = await chromium.launch({ 
        headless: false,  // NOT headless!
        args: ['--no-sandbox']
    });
    
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

    try {
        log('[1] Opening login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        log('[2] Logging in...');
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        
        await page.waitForTimeout(12000);
        log('[2] Logged in');

        await page.waitForSelector('tbody tr', { timeout: 15000 });
        await page.waitForTimeout(3000);

        log('[3] Looking for cascader dropdown...');

        // The cascader dropdown is to the LEFT of the case number input
        // It shows "案件名称" by default and needs to be changed to "案件编号"
        // Let's try clicking on the cascader trigger
        
        // Find the cascader with "案件名称"
        const cascaderTriggers = await page.locator('.ant-cascader-trigger').all();
        log(`Found ${cascaderTriggers.length} cascader triggers`);
        
        for (let i = 0; i < cascaderTriggers.length; i++) {
            const text = await cascaderTriggers[i].textContent();
            log(`  Cascader ${i}: "${text}"`);
            if (text.includes('案件名称')) {
                log(`[3] Clicking cascader ${i}...`);
                await cascaderTriggers[i].click();
                await page.waitForTimeout(2000);
                break;
            }
        }

        // Now look for 案件编号 option
        log('[4] Looking for 案件编号 option...');
        const options = await page.locator('.ant-cascader-menu-item, .ant-select-item').all();
        
        for (let i = 0; i < options.length; i++) {
            const text = await options[i].textContent();
            log(`  Option ${i}: "${text}"`);
            if (text.includes('案件编号')) {
                log(`[4] Clicking 案件编号...`);
                await options[i].click();
                await page.waitForTimeout(1000);
                break;
            }
        }

        // Now enter case number
        log(`[5] Entering case number: ${CASE_NO}`);
        const inputs = await page.locator('input[type="text"]').all();
        // Find the case input (should be visible, width > 200)
        for (const inp of inputs) {
            const box = await inp.boundingBox();
            if (box && box.width > 200) {
                await inp.fill(CASE_NO);
                log('[5] Filled case number');
                break;
            }
        }
        
        await page.waitForTimeout(500);

        // Click Search
        log('[6] Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // Check
        const text = await page.locator('body').textContent();
        if (text.includes(CASE_NO)) {
            log(`[7] ✅ Case found!`);
            
            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const rowText = await row.textContent();
                if (rowText.includes(CASE_NO) && rowText.includes('审理中')) {
                    const approveBtn = row.locator('a:has-text("审批")').first();
                    if (await approveBtn.count() > 0) {
                        log('[8] Clicking 审批...');
                        await approveBtn.click();
                        await page.waitForTimeout(3000);

                        const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")').first();
                        if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                            await confirmBtn.click({ force: true });
                            log('[8] Confirmed!');
                        }
                        log('✅ APPROVE SUCCESS!');
                    }
                    break;
                }
            }
        } else {
            log('[7] ❌ Case not found');
        }

        log('Done - you can close the browser window now');
        await page.waitForTimeout(10000);

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
