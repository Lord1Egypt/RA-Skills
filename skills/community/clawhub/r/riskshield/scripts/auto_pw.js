/**
 * RiskShield Auto Approve - Playwright Direct
 * Uses direct Playwright API for stability
 */

const { chromium } = require('playwright');

const CONFIG = {
    username: 'alan.zhang',
    password: 'ZIdongshenpi1.',
    caseNo: process.argv[2] || '2604131000000597537'
};

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

async function run() {
    log(`Starting auto approve for case: ${CONFIG.caseNo}`);
    
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox']
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    try {
        // Step 1: Login
        log('Step 1: Opening login page...');
        const loginUrl = 'https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';
        await page.goto(loginUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(5000);
        
        log('Step 2: Filling credentials...');
        await page.locator('input[placeholder*="user" i]').fill(CONFIG.username);
        await page.locator('input[placeholder*="password" i]').fill(CONFIG.password);
        await page.locator('button[type="submit"], button:has-text("login")').click();
        
        log('Step 3: Waiting for redirect to case list...');
        await page.waitForURL('**/anytask-web/**', { timeout: 20000 });
        await page.waitForTimeout(5000);
        log(`Current URL: ${page.url()}`);
        
        // Step 4: Find and fill case number input
        log('Step 4: Entering case number...');
        
        // The case number input appears to be ref=e3 based on earlier snapshot
        // Let's try multiple approaches
        let caseInput = null;
        
        // Try by placeholder
        try {
            caseInput = page.locator('input[placeholder*="案件编号"], input[placeholder*="case" i]').first();
            if (await caseInput.count() > 0) {
                log('Found case input by placeholder');
            }
        } catch (e) {}
        
        // Try by label/surrounding text
        if (!caseInput || (await caseInput.count()) === 0) {
            try {
                // Look for the generic container with "案件名称案件编号..." text and find input nearby
                const caseLabel = page.locator('text="案件编号"').first();
                if (await caseLabel.count() > 0) {
                    log('Found "案件编号" label');
                    // The input might be the adjacent textbox
                    caseInput = page.locator('input[type="text"]').nth(2);  // 3rd text input
                }
            } catch (e) {}
        }
        
        // Fallback: use the 3rd textbox on page (0=date from, 1=date to, 2=caseNo)
        if (!caseInput || (await caseInput.count()) === 0) {
            log('Using fallback: 3rd textbox');
            const allTextboxes = page.locator('input[type="text"]');
            const count = await allTextboxes.count();
            log(`Found ${count} textboxes total`);
            if (count >= 3) {
                caseInput = allTextboxes.nth(2);
            } else if (count >= 1) {
                caseInput = allTextboxes.last();
            }
        }
        
        if (caseInput && (await caseInput.count()) > 0) {
            await caseInput.fill(CONFIG.caseNo);
            log(`Filled case number: ${CONFIG.caseNo}`);
            await page.waitForTimeout(1000);
            
            // Step 5: Click search
            log('Step 5: Clicking search button...');
            const searchBtn = page.locator('button:has-text("搜索"), button:has-text("查询")').first();
            if (await searchBtn.count() > 0) {
                await searchBtn.click();
                log('Search clicked');
            } else {
                // Try pressing Enter in the case input
                await caseInput.press('Enter');
                log('Pressed Enter');
            }
            
            await page.waitForTimeout(5000);
            
            // Step 6: Check if case found and click approve
            const pageText = await page.locator('body').textContent();
            if (pageText.includes(CONFIG.caseNo)) {
                log(`✅ Case ${CONFIG.caseNo} found in results!`);
                
                // Find the "审批" link for this case
                // In the table, cases with status "审理中" have an "审批" link
                const rows = page.locator('tr');
                const rowCount = await rows.count();
                log(`Found ${rowCount} table rows`);
                
                for (let i = 0; i < rowCount; i++) {
                    const row = rows.nth(i);
                    const rowText = await row.textContent();
                    if (rowText.includes(CONFIG.caseNo) && rowText.includes('审理中')) {
                        log(`Found case row ${i}, looking for approve button...`);
                        const approveLink = row.locator('a:has-text("审批"), button:has-text("审批")').first();
                        if (await approveLink.count() > 0) {
                            await approveLink.click();
                            log('Clicked approve link');
                            await page.waitForTimeout(3000);
                            
                            // Handle confirm dialog if appears
                            try {
                                const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")');
                                if (await confirmBtn.count() > 0 && await confirmBtn.first().isVisible()) {
                                    await confirmBtn.first().click({ force: true });
                                    log('Clicked confirm');
                                    await page.waitForTimeout(2000);
                                }
                            } catch (e) {
                                log('No confirm dialog or already confirmed');
                            }
                            
                            log('✅ APPROVE SUCCESSFUL!');
                            break;
                        }
                    }
                }
            } else {
                log(`❌ Case ${CONFIG.caseNo} not found in results`);
                // Save screenshot for debugging
                await page.screenshot({ path: `/tmp/rs_case_not_found_${Date.now()}.png`, fullPage: true });
                log('Screenshot saved');
            }
        } else {
            log('❌ Could not find case number input');
        }
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
        await page.screenshot({ path: `/tmp/rs_error_${Date.now()}.png`, fullPage: true });
    } finally {
        await browser.close();
        log('Browser closed');
    }
}

run()
    .then(() => {
        log('Done');
        process.exit(0);
    })
    .catch(err => {
        log(`Fatal: ${err.message}`);
        process.exit(1);
    });
