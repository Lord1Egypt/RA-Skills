/**
 * RiskShield Auto Approve - Final Version
 * Fixed: Search button is "Search" not "搜索"
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
        log(`Logged in successfully`);
        
        // Step 4: Enter case number
        log(`Step 4: Entering case number: ${CONFIG.caseNo}`);
        
        // The case number input is the 3rd visible text input (index 2) - no placeholder
        const caseInput = page.locator('input.form-control').nth(2);
        await caseInput.fill(CONFIG.caseNo);
        log('Filled case number');
        await page.waitForTimeout(500);
        
        // Step 5: Click search button (text is "Search" not "搜索")
        log('Step 5: Clicking Search button...');
        const searchBtn = page.locator('button:has-text("Search")');
        await searchBtn.click();
        log('Clicked Search');
        await page.waitForTimeout(5000);
        
        // Step 6: Check if case found
        const pageText = await page.locator('body').textContent();
        if (pageText.includes(CONFIG.caseNo)) {
            log(`✅ Case ${CONFIG.caseNo} found!`);
            
            // Find the case row and check if it's "审理中" (processing)
            // Then click the "审批" link
            const tableRows = page.locator('tbody tr');
            const rowCount = await tableRows.count();
            log(`Found ${rowCount} table rows`);
            
            for (let i = 0; i < rowCount; i++) {
                const row = tableRows.nth(i);
                const rowText = await row.textContent();
                
                if (rowText.includes(CONFIG.caseNo)) {
                    log(`Row ${i} contains case`);
                    log(`Row status: ${rowText.includes('审理中') ? '审理中' : rowText.includes('已结案') ? '已结案' : '其他'}`);
                    
                    if (rowText.includes('审理中')) {
                        // Find and click approve link
                        const approveLink = row.locator('a:has-text("审批"), button:has-text("审批")');
                        if (await approveLink.count() > 0) {
                            log(`Clicking 审批 button...`);
                            await approveLink.first().click();
                            await page.waitForTimeout(3000);
                            
                            // Handle confirm dialog
                            const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")');
                            if (await confirmBtn.count() > 0 && await confirmBtn.first().isVisible()) {
                                log('Confirming...');
                                await confirmBtn.first().click({ force: true });
                                await page.waitForTimeout(2000);
                            }
                            
                            log('✅ APPROVE SUCCESSFUL!');
                        } else {
                            log('No 审批 button found in this row');
                        }
                    } else if (rowText.includes('已结案')) {
                        log('Case is already closed (已结案), cannot approve');
                    }
                    break;
                }
            }
        } else {
            log(`❌ Case ${CONFIG.caseNo} not found in results`);
            await page.screenshot({ path: `/tmp/rs_notfound_${Date.now()}.png`, fullPage: true });
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
