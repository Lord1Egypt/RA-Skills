/**
 * RiskShield Browser Approve Script v2
 * Based on actual UI analysis from screenshots
 * 
 * Workflow:
 * 1. Login → Case List Page
 * 2. Select date range (近7天)
 * 3. Select search field (案件编号) from dropdown
 * 4. Enter case number → Search
 * 5. Check case status:
 *    - 审理中 → Click 审批 → Opens in NEW TAB
 *    - 已结案 → Return "案件已结束" message
 * 6. Switch to new tab (case detail page)
 * 7. Fill approval form:
 *    - PASS: ManualApprovalResult → Pass, Credit Amount → 100 → Submit
 *    - REFUSE: ManualApprovalResult → Refuse, Refuse Code → CA_TRUE_HIT → Submit
 * 8. Close tab, verify status in case list
 */

const { chromium } = require('playwright');

const API_BASE = 'https://riskshield.dcsuat.com';
const CASE_NO = process.argv[2] || '2604151000000598520';
const ACTION = process.argv[3] || 'pass'; // 'pass' or 'refuse'
const REFUSE_CODE = process.argv[4] || 'CA_TRUE_HIT';
const CREDIT_AMOUNT = process.argv[5] || '100';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

async function waitAndClick(page, selector, options = {}) {
    await page.waitForSelector(selector, { state: 'visible', timeout: 10000 });
    await page.click(selector, options);
}

async function waitAndFill(page, selector, value) {
    await page.waitForSelector(selector, { state: 'visible', timeout: 10000 });
    await page.fill(selector, value);
}

(async () => {
    log(`Starting RiskShield Browser Approve v2`);
    log(`Case: ${CASE_NO}, Action: ${ACTION.toUpperCase()}`);

    const browser = await chromium.launch({
        headless: false, // Visible for debugging
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        ignoreHTTPSErrors: true
    });

    const page = await context.newPage();

    let newTab = null;

    try {
        // ========== STEP 1: LOGIN ==========
        log('[1/8] Opening login page...');
        const loginURL = `${API_BASE}/mc/page/login.html?redirect=${encodeURIComponent(API_BASE + '/anytask-web/task/case/page/main.html')}`;
        await page.goto(loginURL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);

        log('[1/8] Filling login credentials...');
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();

        // Wait for redirect to case list
        await page.waitForTimeout(12000);
        
        if (!page.url().includes('anytask-web')) {
            log('ERROR: Login failed - not redirected to case list');
            return;
        }
        log('[1/8] ✅ Login successful');

        // ========== STEP 2: SELECT DATE RANGE (近7天) ==========
        log('[2/8] Selecting date range: 近7天...');
        
        // Click date picker to open it
        const datePicker = page.locator('.ant-picker, .ant-range-picker').first();
        if (await datePicker.count() > 0) {
            await datePicker.click();
            await page.waitForTimeout(1000);
            
            // Look for "近7天" option
            const quickDateOption = page.locator('.ant-picker-preset-tag:has-text("近7天"), .ant-radio-button-wrapper:has-text("近7天")').first();
            if (await quickDateOption.count() > 0) {
                await quickDateOption.click();
                log('[2/8] ✅ Selected 近7天');
            } else {
                log('[2/8] ⚠️ 近7天 option not found, trying alternative...');
            }
            await page.waitForTimeout(500);
        }

        // ========== STEP 3: SELECT SEARCH FIELD (案件编号) ==========
        log('[3/8] Selecting search field: 案件编号...');
        
        // Find the search field dropdown - it's an ant-select
        // The dropdown shows "案件名称" by default and we need "案件编号"
        const searchFieldDropdown = page.locator('.ant-select:not(.ant-select-disabled)').filter({ hasText: /案件名称|案件编号|客户姓名/ }).first();
        
        if (await searchFieldDropdown.count() > 0) {
            await searchFieldDropdown.click();
            await page.waitForTimeout(1000);
            
            // Select "案件编号" from dropdown
            const option = page.locator('.ant-select-item-option:has-text("案件编号"), .ant-select-item:has-text("案件编号")').first();
            if (await option.count() > 0) {
                await option.click();
                log('[3/8] ✅ Selected 案件编号');
            } else {
                log('[3/8] ⚠️ 案件编号 option not found in dropdown');
            }
        } else {
            log('[3/8] ⚠️ Search field dropdown not found, checking HTML structure...');
            // Debug: show available selects
            const selects = await page.locator('.ant-select').all();
            log(`Found ${selects.length} ant-select elements`);
            for (let i = 0; i < Math.min(selects.length, 5); i++) {
                const text = await selects[i].textContent();
                log(`  Select ${i}: "${text.substring(0, 50)}"`);
            }
        }
        await page.waitForTimeout(500);

        // ========== STEP 4: ENTER CASE NUMBER & SEARCH ==========
        log(`[4/8] Entering case number: ${CASE_NO}...`);
        
        // Find the case number input - it's the input adjacent to the search field dropdown
        const caseInput = page.locator('input[type="text"]').filter({ has: page.locator('..') }).nth(2);
        
        // Alternative: find by placeholder or proximity to search button
        const allInputs = await page.locator('input[type="text"]').all();
        let caseInputEl = null;
        
        for (const inp of allInputs) {
            const box = await inp.boundingBox();
            const parent = await inp.locator('..').textContent();
            if (box && box.width > 150 && parent.includes('案件编号')) {
                caseInputEl = inp;
                break;
            }
        }
        
        if (!caseInputEl) {
            // Fallback: use the 3rd text input
            caseInputEl = allInputs[2];
        }
        
        await caseInputEl.click();
        await caseInputEl.clear();
        await caseInputEl.fill(CASE_NO);
        log('[4/8] ✅ Case number entered');
        
        // Click Search
        log('[4/8] Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);
        
        // ========== STEP 5: CHECK CASE STATUS ==========
        log('[5/8] Checking case status...');
        
        const pageText = await page.locator('body').textContent();
        
        if (!pageText.includes(CASE_NO)) {
            log(`❌ Case ${CASE_NO} not found in results`);
            const rows = await page.locator('tbody tr').count();
            log(`Table has ${rows} rows`);
            if (rows === 1) {
                const msg = await page.locator('tbody tr td').first().textContent();
                log(`Message: ${msg}`);
            }
            return;
        }
        
        // Find the case row
        const rows = await page.locator('tbody tr').all();
        let caseRow = null;
        
        for (const row of rows) {
            const rowText = await row.textContent();
            if (rowText.includes(CASE_NO)) {
                caseRow = row;
                break;
            }
        }
        
        if (!caseRow) {
            log('ERROR: Cannot find case row');
            return;
        }
        
        const rowText = await caseRow.textContent();
        log(`[5/8] Case found. Row text: ${rowText.substring(0, 100)}...`);
        
        // Check case status
        if (rowText.includes('已结案')) {
            log('❌ Case is CLOSED (已结案). Cannot approve.');
            log('Please use a case with status "审理中" (processing).');
            return;
        }
        
        if (!rowText.includes('审理中')) {
            log(`⚠️ Case status is not "审理中". Status: ${rowText.includes('审批中') ? '审批中' : 'Unknown'}`);
        }
        
        // Check if 审批 button exists
        const approveBtn = caseRow.locator('a:has-text("审批"), button:has-text("审批")').first();
        if (await approveBtn.count() === 0 || !(await approveBtn.isVisible())) {
            log('❌ No "审批" button found. Case may not be actionable.');
            return;
        }
        
        log('[5/8] ✅ Case is processable (审理中), clicking 审批...');
        
        // ========== STEP 6: OPEN CASE DETAIL (NEW TAB) ==========
        log('[6/8] Opening case detail in new tab...');
        
        // Click审批 - it opens in new tab
        await approveBtn.click();
        await page.waitForTimeout(3000);
        
        // Get all pages/tabs
        const pages = context.pages();
        log(`Current pages/tabs: ${pages.length}`);
        
        if (pages.length > 1) {
            // Find the new tab (last one or one with different URL)
            newTab = pages[pages.length - 1];
            log(`Switching to new tab: ${newTab.url().substring(0, 80)}...`);
            await newTab.waitForLoadState('domcontentloaded');
            await newTab.waitForTimeout(3000);
        } else {
            log('⚠️ No new tab opened, using current page');
            newTab = page;
        }
        
        // ========== STEP 7: FILL APPROVAL FORM ==========
        log('[7/8] Filling approval form...');
        
        // Wait for ManualApprovalResult dropdown
        const manualResultDropdown = newTab.locator('.ant-select').filter({ hasText: /ManualApprovalResult|人工审批结果/ }).first();
        
        if (await manualResultDropdown.count() > 0) {
            await manualResultDropdown.click();
            await page.waitForTimeout(1000);
            
            if (ACTION.toLowerCase() === 'pass') {
                log('[7/8] Selecting: Pass');
                const passOption = newTab.locator('.ant-select-item-option:has-text("Pass"), .ant-select-item:has-text("Pass")').first();
                await passOption.click();
                await page.waitForTimeout(500);
                
                // Enter Credit Amount
                log(`[7/8] Entering Credit Amount: ${CREDIT_AMOUNT}`);
                const creditInput = newTab.locator('input[placeholder*="enter" i], input[id*="CreditAmount"]').first();
                if (await creditInput.count() > 0) {
                    await creditInput.fill(CREDIT_AMOUNT);
                } else {
                    // Try finding by label
                    const creditLabel = newTab.locator('*:has-text("Credit Amount")').locator('..').locator('input').first();
                    if (await creditLabel.count() > 0) {
                        await creditLabel.fill(CREDIT_AMOUNT);
                    }
                }
            } else {
                log('[7/8] Selecting: Refuse');
                const refuseOption = newTab.locator('.ant-select-item-option:has-text("Refuse"), .ant-select-item:has-text("Refuse")').first();
                await refuseOption.click();
                await page.waitForTimeout(500);
                
                // Select Refuse Code
                log(`[7/8] Selecting Refuse Code: ${REFUSE_CODE}`);
                const refuseCodeDropdown = newTab.locator('.ant-select').filter({ hasText: /Refuse Code|拒绝代码/ }).first();
                if (await refuseCodeDropdown.count() > 0) {
                    await refuseCodeDropdown.click();
                    await page.waitForTimeout(1000);
                    
                    const refuseCodeOption = newTab.locator(`.ant-select-item-option:has-text("${REFUSE_CODE}"), .ant-select-item:has-text("${REFUSE_CODE}")`).first();
                    if (await refuseCodeOption.count() > 0) {
                        await refuseCodeOption.click();
                    } else {
                        log(`⚠️ Refuse Code "${REFUSE_CODE}" not found, trying CA_TRUE_HIT...`);
                        const caHit = newTab.locator('.ant-select-item:has-text("CA_TRUE_HIT")').first();
                        await caHit.click();
                    }
                }
            }
            
            await page.waitForTimeout(500);
            
            // Click Submit button
            log('[7/8] Clicking Submit...');
            const submitBtn = newTab.locator('button:has-text("提交"), button:has-text("Submit")').last();
            
            if (await submitBtn.count() > 0 && await submitBtn.isVisible()) {
                await submitBtn.click();
                log('[7/8] ✅ Submit clicked');
                await page.waitForTimeout(3000);
            } else {
                log('⚠️ Submit button not found');
            }
        } else {
            log('ERROR: ManualApprovalResult dropdown not found');
            log('Current page URL: ' + newTab.url());
            
            // Debug: show form structure
            const formElements = await newTab.locator('.ant-form-item, .ant-select, input').all();
            log(`Found ${formElements.length} form elements on page`);
        }
        
        // ========== STEP 8: VERIFY RESULT ==========
        log('[8/8] Verifying result...');
        
        // Close new tab and switch back to main page
        if (newTab && newTab !== page) {
            await newTab.close();
            await page.bringToFront();
            await page.waitForTimeout(2000);
        }
        
        // Re-search to verify status
        await caseInputEl.click();
        await caseInputEl.clear();
        await caseInputEl.fill(CASE_NO);
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);
        
        const finalText = await page.locator('body').textContent();
        if (finalText.includes('已结案') && finalText.includes('同意')) {
            log('✅ APPROVE SUCCESSFUL! Case is now closed with result: 同意');
        } else if (finalText.includes('已结案') && finalText.includes('拒绝')) {
            log('✅ REFUSE SUCCESSFUL! Case is now closed with result: 拒绝');
        } else if (finalText.includes('已结案')) {
            log('✅ Case is now closed (已结案)');
        } else {
            log('⚠️ Could not verify final status. Please check manually.');
        }
        
        log('\n✅ Browser Approve v2 COMPLETED');
        
    } catch (error) {
        log(`❌ ERROR: ${error.message}`);
        log(error.stack);
        
        // Take screenshot for debugging
        try {
            await page.screenshot({ path: `/tmp/rs_error_${Date.now()}.png`, fullPage: true });
            log('Error screenshot saved to /tmp/');
        } catch (e) {}
    } finally {
        log('You can close the browser window now.');
        await page.waitForTimeout(10000);
        await browser.close();
    }
})();
