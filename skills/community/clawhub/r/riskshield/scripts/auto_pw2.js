/**
 * RiskShield Auto Approve - Playwright v2
 * Fixed search button detection
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
        log(`Current URL: ${page.url().substring(0, 80)}...`);
        
        // Step 4: Enter case number using JavaScript to find the right input
        log('Step 4: Finding case number input...');
        
        // Get all inputs with their IDs and classes
        const inputsInfo = await page.evaluate(() => {
            const inputs = document.querySelectorAll('input[type="text"], input[type="hidden"]');
            return Array.from(inputs).map((inp, i) => ({
                index: i,
                id: inp.id,
                name: inp.name,
                placeholder: inp.placeholder,
                className: inp.className,
                value: inp.value,
                parentClass: inp.parentElement?.className?.substring(0, 50),
                rect: inp.getBoundingClientRect ? JSON.stringify(inp.getBoundingClientRect()) : null
            }));
        });
        
        log(`Found ${inputsInfo.length} inputs:`);
        inputsInfo.forEach((inp, i) => {
            if (inp.rect) {
                const r = JSON.parse(inp.rect);
                if (r.width > 50) {  // Only visible inputs
                    log(`  [${i}] ${inp.placeholder || '(no placeholder)'} | ${inp.parentClass} | rect: ${r.width}x${r.height}`);
                }
            }
        });
        
        // Find the case number input - look for the one in the filter bar
        // Based on snapshot: ref=e3 was the case number textbox
        // Let's find it by looking for the one with placeholder or position
        let caseInputIndex = -1;
        
        // Look for input with "案件" related parent or placeholder
        for (let i = 0; i < inputsInfo.length; i++) {
            const inp = inputsInfo[i];
            if (inp.placeholder && (inp.placeholder.includes('案件') || inp.placeholder.includes('编号'))) {
                caseInputIndex = i;
                log(`Found case input by placeholder: index ${i}`);
                break;
            }
        }
        
        // If not found, try the 3rd visible text input (after date pickers)
        if (caseInputIndex === -1) {
            const visibleInputs = inputsInfo.filter(inp => {
                if (!inp.rect) return false;
                const r = JSON.parse(inp.rect);
                return r.width > 50 && r.height > 20;
            });
            log(`Visible inputs count: ${visibleInputs.length}`);
            
            // The case number input is usually the 3rd one (0=date from, 1=date to, 2=caseNo)
            if (visibleInputs.length >= 3) {
                caseInputIndex = inputsInfo.indexOf(visibleInputs[2]);
                log(`Using 3rd visible input: index ${caseInputIndex}`);
            }
        }
        
        if (caseInputIndex >= 0) {
            const caseInput = page.locator('input[type="text"]').nth(caseInputIndex);
            await caseInput.fill(CONFIG.caseNo);
            log(`Filled case number: ${CONFIG.caseNo}`);
            await page.waitForTimeout(1000);
            
            // Step 5: Click the search button
            log('Step 5: Clicking search button...');
            
            // Look for button with "搜索" or "查询"
            const searchBtn = page.locator('button').filter({ hasText: /搜索|查询/ }).first();
            if (await searchBtn.count() > 0) {
                const btnText = await searchBtn.textContent();
                log(`Found search button: "${btnText.trim()}"`);
                await searchBtn.click();
                log('Clicked search button');
            } else {
                log('Search button not found, trying Enter...');
                await caseInput.press('Enter');
            }
            
            await page.waitForTimeout(5000);
            
            // Step 6: Check results
            const pageText = await page.locator('body').textContent();
            if (pageText.includes(CONFIG.caseNo)) {
                log(`✅ Case ${CONFIG.caseNo} found!`);
                
                // Find and click the approve link for this case
                // Cases with status "审理中" have an "审批" link
                const rows = page.locator('table tbody tr, .ant-table-row');
                const rowCount = await rows.count();
                log(`Found ${rowCount} table rows`);
                
                for (let i = 0; i < rowCount; i++) {
                    const row = rows.nth(i);
                    const rowText = await row.textContent();
                    if (rowText.includes(CONFIG.caseNo)) {
                        log(`Row ${i} contains case`);
                        
                        if (rowText.includes('审理中')) {
                            const approveLink = row.locator('a, button').filter({ hasText: '审批' }).first();
                            if (await approveLink.count() > 0) {
                                log(`Clicking approve in row ${i}...`);
                                await approveLink.click();
                                await page.waitForTimeout(3000);
                                
                                // Handle confirm dialog
                                const confirmBtn = page.locator('button').filter({ hasText: /确认|确定/ }).first();
                                if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                                    log('Confirming...');
                                    await confirmBtn.click({ force: true });
                                    await page.waitForTimeout(2000);
                                }
                                
                                log('✅ APPROVE SUCCESSFUL!');
                            }
                        } else {
                            log(`Case status is not "审理中": ${rowText.substring(0, 100)}`);
                        }
                        break;
                    }
                }
            } else {
                log(`❌ Case ${CONFIG.caseNo} not found in results`);
                // Take screenshot
                const ssPath = `/tmp/rs_notfound_${Date.now()}.png`;
                await page.screenshot({ path: ssPath, fullPage: true });
                log(`Screenshot: ${ssPath}`);
            }
        } else {
            log('❌ Could not find case number input');
        }
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
        const ssPath = `/tmp/rs_error_${Date.now()}.png`;
        await page.screenshot({ path: ssPath, fullPage: true });
        log(`Screenshot: ${ssPath}`);
    } finally {
        await browser.close();
        log('Done');
    }
}

run().then(() => process.exit(0)).catch(err => { log(`Fatal: ${err.message}`); process.exit(1); });
