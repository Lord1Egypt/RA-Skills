/**
 * RiskShield Browser Approve Script v6
 * Fixed: Proper dropdown handling for search type selector
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const API_BASE = 'riskshield.dcsuat.com';
const TOKEN_FILE = path.join(__dirname, '..', 'token.json');
const CASE_NO = process.argv[2] || '2604151000000598528';
const ACTION = (process.argv[3] || 'pass').toLowerCase();
const REFUSE_CODE = process.argv[4] || 'CA_TRUE_HIT';
const CREDIT_AMOUNT = process.argv[5] || '100';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`=== RiskShield Approve v6 (HEADLESS) ===`);
    log(`Case: ${CASE_NO}, Action: ${ACTION.toUpperCase()}`);

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 },
        ignoreHTTPSErrors: true
    });

    const page = await context.newPage();

    try {
        // ========== LOGIN ==========
        log('[1/8] Opening login page...');
        const loginUrl = `https://${API_BASE}/mc/page/login.html?redirect=${encodeURIComponent(`https://${API_BASE}/anytask-web/task/case/page/main.html`)}`;
        
        await page.goto(loginUrl, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(10000);
        
        if (!page.url().includes('anytask-web')) {
            log('❌ Login failed');
            return;
        }
        log('[1/8] ✅ Logged in');

        // ========== DATE RANGE (近7天) ==========
        log('[2/8] Selecting date range...');
        
        // The date picker should already show 近7天 by default
        // If not, click to open and select
        const dateInput = page.locator('input[placeholder="请选择"]').first();
        if (await dateInput.count() > 0) {
            const value = await dateInput.inputValue();
            log('[2/8] Date picker value:', value);
        }

        // ========== SEARCH TYPE SELECTOR ==========
        log('[3/8] Selecting search type: No. (案件编号)...');
        
        // The search type dropdown shows "Case Name" by default
        // We need to click it to open and select "No."
        // Looking for the dropdown-toggle or similar element near "Case Name" text
        
        // Find the element with "Case Name" text that is clickable
        const caseNameLabel = page.locator('span').filter({ hasText: /^Case Name$/ }).first();
        
        // Click on the parent or nearby element to open dropdown
        if (await caseNameLabel.count() > 0) {
            // Get the parent container
            const dropdownContainer = caseNameLabel.locator('..');
            
            // The dropdown trigger should be the parent div with arrow icon
            await page.locator('.ant-select, .dropdown-toggle, [class*="select"]').filter({ hasText: '' }).first().click().catch(() => {});
            
            // Try clicking directly on the Case Name label area
            await caseNameLabel.click({ force: true });
            await page.waitForTimeout(1500);
            
            // Now check if dropdown appeared
            // The dropdown should contain: Case Name, No., Name, Phone No., Id No.
            const dropdownVisible = await page.locator('.ant-select-dropdown, .dropdown-menu').filter({ isVisible: true }).count();
            log('[3/8] Dropdown visible count:', dropdownVisible);
            
            if (dropdownVisible === 0) {
                // Try clicking on the input next to "Case Name" label
                // The input field should be adjacent to the label
                const caseNameInput = page.locator('input').filter({ hasText: '' }).nth(1);
                await caseNameInput.click().catch(() => {});
                await page.waitForTimeout(1000);
            }
        }
        
        // Alternative: directly look for and click the dropdown trigger
        // The trigger has class containing "ant-select-selection"
        const selectTrigger = page.locator('.ant-select-selection').filter({ hasText: /Case Name/ }).first();
        if (await selectTrigger.count() > 0) {
            await selectTrigger.click();
            await page.waitForTimeout(1500);
            
            // Now look for No. in the dropdown
            const noOption = page.locator('.ant-select-item, .ant-select-dropdown li').filter({ hasText: /^No\.$/ }).first();
            if (await noOption.count() > 0) {
                await noOption.click();
                log('[3/8] ✅ Selected No.');
            } else {
                log('[3/8] ⚠️ No. option not found in dropdown');
            }
        }
        
        await page.waitForTimeout(500);

        // ========== ENTER CASE NUMBER ==========
        log(`[4/8] Entering case number: ${CASE_NO}...`);
        
        // Find the case number input - it's the input field next to the Case Name dropdown
        // Based on screenshot, it's a text input with placeholder or adjacent to the dropdown
        const allInputs = await page.locator('input[type="text"]').all();
        let caseInput = null;
        
        for (const inp of allInputs) {
            const box = await inp.boundingBox();
            if (box && box.x > 200 && box.x < 600 && box.width > 50) {
                const value = await inp.inputValue().catch(() => '');
                if (!value || value.length < 20) { // Don't fill if it's the date picker
                    caseInput = inp;
                    break;
                }
            }
        }
        
        if (caseInput) {
            await caseInput.click();
            await caseInput.clear();
            await caseInput.fill(CASE_NO);
            log('[4/8] ✅ Case number entered');
        } else {
            log('❌ Cannot find case number input');
            return;
        }

        // ========== CLICK SEARCH ==========
        log('[4/8] Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // ========== CHECK CASE ==========
        log('[5/8] Checking case status...');
        
        const pageText = await page.locator('body').textContent();
        
        if (!pageText.includes(CASE_NO)) {
            log(`❌ Case ${CASE_NO} not found`);
            await page.screenshot({ path: '/tmp/rs_not_found.png' });
            return;
        }
        
        log('[5/8] ✅ Case found');
        
        // Find the case row and check status
        const caseRow = page.locator('tbody tr').filter({ hasText: CASE_NO });
        if (await caseRow.count() === 0) {
            log('❌ Cannot find case row');
            return;
        }
        
        const rowText = await caseRow.textContent();
        if (rowText.includes('Closed') || rowText.includes('已结案')) {
            log('❌ Case is already closed');
            return;
        }
        
        // Click 审批 button
        const approveBtn = caseRow.locator('a').filter({ hasText: '审批' }).first();
        if (await approveBtn.count() === 0) {
            log('❌ No 审批 button found');
            return;
        }
        log('[5/8] Clicking 审批...');
        await approveBtn.click();
        await page.waitForTimeout(5000);

        // ========== SWITCH TO NEW TAB ==========
        log('[6/8] Waiting for case detail page...');
        
        const pages = context.pages();
        let detailPage = page;
        if (pages.length > 1) {
            detailPage = pages[pages.length - 1];
            await detailPage.waitForLoadState('domcontentloaded');
            await detailPage.waitForTimeout(3000);
            log('[6/8] ✅ Opened in new tab');
        }

        // ========== FILL APPROVAL FORM ==========
        log('[7/8] Filling approval form...');
        
        // Find ManualApprovalResult dropdown
        const manualDropdown = detailPage.locator('.ant-select').filter({ hasText: /ManualApprovalResult|人工审批|Please choose/ }).first();
        if (await manualDropdown.count() > 0) {
            await manualDropdown.click();
            await page.waitForTimeout(500);
            
            if (ACTION === 'pass') {
                await detailPage.locator('.ant-select-item').filter({ hasText: 'Pass' }).first().click();
                log('[7/8] Selected: Pass');
                
                // Enter Credit Amount
                const creditInput = detailPage.locator('input').filter({ hasText: '' }).nth(3);
                await creditInput.fill(CREDIT_AMOUNT);
                log(`[7/8] Entered Credit Amount: ${CREDIT_AMOUNT}`);
            } else {
                await detailPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).first().click();
                log('[7/8] Selected: Refuse');
                
                // Select Refuse Code
                const refuseCodeDropdown = detailPage.locator('.ant-select').filter({ hasText: /Refuse Code|拒绝代码/ }).first();
                if (await refuseCodeDropdown.count() > 0) {
                    await refuseCodeDropdown.click();
                    await page.waitForTimeout(500);
                    await detailPage.locator('.ant-select-item').filter({ hasText: REFUSE_CODE }).first().click();
                }
            }
        } else {
            log('⚠️ ManualApprovalResult dropdown not found, checking form structure...');
            await detailPage.screenshot({ path: '/tmp/rs_form_check.png' });
        }
        
        await page.waitForTimeout(500);
        
        // Click Submit
        const submitBtn = detailPage.locator('button').filter({ hasText: /提交|Submit/ }).last();
        if (await submitBtn.count() > 0) {
            await submitBtn.click();
            log('[7/8] ✅ Submit clicked');
            await page.waitForTimeout(3000);
        }

        // ========== VERIFY ==========
        log('[8/8] Verifying result...');
        
        if (detailPage !== page) {
            await detailPage.close();
            await page.bringToFront();
        }
        
        await page.waitForTimeout(2000);
        
        // Re-search the case
        await caseInput.fill(CASE_NO);
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);
        
        const finalText = await page.locator('body').textContent();
        if (finalText.includes('Closed') || finalText.includes('已结案')) {
            if (finalText.includes('Approved') || finalText.includes('同意')) {
                log('✅ APPROVE SUCCESS! Case is now Closed with result: Approved');
            } else if (finalText.includes('Reject') || finalText.includes('拒绝')) {
                log('✅ REFUSE SUCCESS! Case is now Closed with result: Reject');
            } else {
                log('✅ Case is now CLOSED');
            }
        } else {
            log('⚠️ Status unclear. Please verify manually.');
        }
        
        log('\n=== DONE ===');
        
    } catch (error) {
        log(`❌ ERROR: ${error.message}`);
        try {
            await page.screenshot({ path: `/tmp/rs_error.png` });
        } catch (e) {}
    } finally {
        await browser.close();
    }
})();
