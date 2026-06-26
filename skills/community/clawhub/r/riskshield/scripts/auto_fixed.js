/**
 * RiskShield Auto Approve - Fixed Version
 * Uses partial case number matching (last 12 digits)
 */

const { chromium } = require('playwright');

const CONFIG = {
    username: 'alan.zhang',
    password: 'ZIdongshenpi1.',
    caseNo: process.argv[2] || '2604131000000597537'
};

// Extract last 12 digits for search (UI only supports partial match)
function getPartialCaseNo(fullCaseNo) {
    return fullCaseNo.slice(-12);
}

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

async function run() {
    const searchNo = getPartialCaseNo(CONFIG.caseNo);
    log(`Starting auto approve for case: ${CONFIG.caseNo}`);
    log(`Using partial search: ${searchNo}`);
    
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
        log('Step 1: Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);
        
        await page.locator('input[placeholder*="user" i]').fill(CONFIG.username);
        await page.locator('input[placeholder*="password" i]').fill(CONFIG.password);
        await page.locator('button[type="submit"], button:has-text("login")').click();
        
        await page.waitForURL('**/anytask-web/**', { timeout: 20000 });
        await page.waitForTimeout(5000);
        log('Logged in');
        
        // Step 2: Enter partial case number
        log(`Step 2: Entering partial case number: ${searchNo}`);
        
        // Use 3rd text input (case number field)
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill(searchNo);
        log('Filled search');
        await page.waitForTimeout(500);
        
        // Step 3: Click Search
        log('Step 3: Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);
        
        // Step 4: Verify case found
        const pageText = await page.locator('body').textContent();
        if (!pageText.includes(CONFIG.caseNo)) {
            log(`❌ Case ${CONFIG.caseNo} not found after search`);
            await page.screenshot({ path: `/tmp/rs_notfound_${Date.now()}.png`, fullPage: true });
            return;
        }
        log(`✅ Case ${CONFIG.caseNo} found!`);
        
        // Step 5: Find and click the "审批" button
        log('Step 4: Looking for 审批 button...');
        
        // Find the table row with our case
        const rows = await page.locator('tbody tr').all();
        let found = false;
        
        for (const row of rows) {
            const rowText = await row.textContent();
            if (rowText.includes(CONFIG.caseNo)) {
                log('Found case row');
                
                // Look for 审批 link/button in this row
                const approveBtn = row.locator('a, button').filter({ hasText: '审批' }).first();
                if (await approveBtn.count() > 0) {
                    log('Clicking 审批...');
                    await approveBtn.click();
                    await page.waitForTimeout(3000);
                    
                    // Step 6: Handle confirm dialog
                    log('Step 5: Checking for confirm dialog...');
                    const confirmBtn = page.locator('button').filter({ hasText: /确认|确定/ }).first();
                    if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                        log('Confirming...');
                        await confirmBtn.click({ force: true });
                        await page.waitForTimeout(2000);
                    }
                    
                    log('✅ APPROVE SUCCESSFUL!');
                    found = true;
                } else {
                    log('No 审批 button found - case may not be in approvable state');
                }
                break;
            }
        }
        
        if (!found && !pageText.includes('审批')) {
            log('Case found but no 审批 button available');
        }
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
        await page.screenshot({ path: `/tmp/rs_error_${Date.now()}.png`, fullPage: true });
    } finally {
        await browser.close();
        log('Done');
    }
}

run().then(() => process.exit(0)).catch(err => { log(`Fatal: ${err.message}`); process.exit(1); });
