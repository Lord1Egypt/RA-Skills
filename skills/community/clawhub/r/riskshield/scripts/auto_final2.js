/**
 * RiskShield Auto Approve - Final v2
 * Uses index-based selection for inputs
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
        log('Step 1: Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);
        
        await page.locator('input[placeholder*="user" i]').fill(CONFIG.username);
        await page.locator('input[placeholder*="password" i]').fill(CONFIG.password);
        await page.locator('button[type="submit"], button:has-text("login")').click();
        
        await page.waitForURL('**/anytask-web/**', { timeout: 20000 });
        await page.waitForTimeout(5000);
        log('Logged in');
        
        // Step 2: Enter case number - use nth(2) based on earlier debug
        log(`Step 2: Entering case number: ${CONFIG.caseNo}`);
        
        // Get all inputs first to understand the structure
        const allInputs = await page.locator('input[type="text"]').all();
        log(`Found ${allInputs.length} text inputs`);
        
        // Fill the 3rd text input (index 2) - this is the case number input
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill(CONFIG.caseNo);
        log('Filled case number');
        await page.waitForTimeout(500);
        
        // Step 3: Click Search button
        log('Step 3: Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        log('Clicked Search');
        await page.waitForTimeout(5000);
        
        // Step 4: Check if case found
        const pageText = await page.locator('body').textContent();
        if (pageText.includes(CONFIG.caseNo)) {
            log(`✅ Case ${CONFIG.caseNo} found!`);
            
            // Check case status and find approve button
            if (pageText.includes('审理中')) {
                log('Case status: 审理中 (Processing)');
                
                // Find the row with this case and click approve
                const rows = await page.locator('tbody tr').all();
                for (const row of rows) {
                    const rowText = await row.textContent();
                    if (rowText.includes(CONFIG.caseNo)) {
                        log('Found case row');
                        
                        // Click the 审批 link/button in this row
                        const approveBtn = row.locator('a, button').filter({ hasText: '审批' }).first();
                        if (await approveBtn.count() > 0) {
                            await approveBtn.click();
                            log('Clicked 审批');
                            await page.waitForTimeout(3000);
                            
                            // Confirm
                            const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")').first();
                            if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                                await confirmBtn.click({ force: true });
                                log('Confirmed');
                                await page.waitForTimeout(2000);
                            }
                            
                            log('✅ APPROVE SUCCESSFUL!');
                        }
                        break;
                    }
                }
            } else if (pageText.includes('已结案')) {
                log('Case status: 已结案 (Closed) - cannot approve');
            } else {
                log('Case status unknown or not processing');
            }
        } else {
            log(`❌ Case ${CONFIG.caseNo} not found`);
        }
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
        log('Done');
    }
}

run().then(() => process.exit(0)).catch(err => { log(`Fatal: ${err.message}`); process.exit(1); });
