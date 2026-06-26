/**
 * RiskShield - Direct React/AntD manipulation
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604131000000597537';

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

        // Find and click the cascader to change search field
        log('Looking for cascader selector...');

        // Try multiple approaches to find and click the cascader
        const clicked = await page.evaluate(() => {
            // Find all ant-cascader components
            const cascaders = document.querySelectorAll('.ant-cascader');
            
            for (const cascader of cascaders) {
                // Check if this cascader has "案件名称" text
                const trigger = cascader.querySelector('.ant-cascader-trigger');
                if (trigger && trigger.textContent.includes('案件名称')) {
                    trigger.click();
                    return 'clicked 案件名称 cascader';
                }
            }
            
            // Try ant-select
            const selects = document.querySelectorAll('.ant-select');
            for (const select of selects) {
                const trigger = select.querySelector('.ant-select-selection-search');
                if (trigger) {
                    trigger.click();
                    return 'clicked ant-select';
                }
            }
            
            // Try finding by placeholder
            const inputs = document.querySelectorAll('input[placeholder="请选择"]');
            for (const inp of inputs) {
                // Check if parent has search-related class
                const parent = inp.closest('.search') || inp.closest('.filter');
                if (parent) {
                    inp.click();
                    return 'clicked input in search area';
                }
            }
            
            return 'not found';
        });

        log(`Cascader click result: ${clicked}`);
        await page.waitForTimeout(2000);

        // Now look for 案件编号 option and click it
        if (clicked !== 'not found') {
            log('Looking for 案件编号 option...');
            
            const optionClicked = await page.evaluate(() => {
                // Look in ant-select-dropdown or cascader menus
                const options = document.querySelectorAll('.ant-select-item-option, .ant-cascader-menu-item, .ant-select-dropdown-menu-item');
                
                for (const opt of options) {
                    if (opt.textContent === '案件编号') {
                        opt.click();
                        return true;
                    }
                }
                
                // Also check for hidden/filtered options
                const allOptions = document.querySelectorAll('[class*="option"], [class*="item"]');
                for (const o of allOptions) {
                    if (o.textContent.trim() === '案件编号') {
                        o.click();
                        return true;
                    }
                }
                
                return false;
            });
            
            log(`Option click: ${optionClicked ? 'success' : 'not found'}`);
            await page.waitForTimeout(1000);
        }

        // Now type in the case number
        log(`Entering case number: ${CASE_NO}`);
        
        // The case input should be the one that appears after the cascader
        const inputs = await page.locator('input[type="text"]').all();
        log(`Found ${inputs.length} text inputs`);
        
        // Find the case input (should be the one after the cascader)
        for (let i = 0; i < inputs.length; i++) {
            const box = await inputs[i].boundingBox();
            const placeholder = await inputs[i].getAttribute('placeholder');
            log(`  Input ${i}: placeholder="${placeholder}", box=${box ? `${box.width}x${box.height}` : 'N/A'}`);
        }
        
        // Try to find and fill the case number input
        // Based on UI, it should be a visible input with width > 200
        for (let i = 0; i < inputs.length; i++) {
            const box = await inputs[i].boundingBox();
            if (box && box.width > 200) {
                await inputs[i].fill(CASE_NO);
                log(`Filled input ${i}`);
                break;
            }
        }
        
        await page.waitForTimeout(500);

        // Click Search
        log('Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // Check results
        const text = await page.locator('body').textContent();
        if (text.includes(CASE_NO)) {
            log(`✅ Case found!`);

            const rows = await page.locator('tbody tr').all();
            for (const row of rows) {
                const rowText = await row.textContent();
                if (rowText.includes(CASE_NO) && rowText.includes('审理中')) {
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
                    break;
                }
            }
        } else {
            log('❌ Case not found');
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
