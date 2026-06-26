/**
 * RiskShield Browser Approve Script v7
 * Simplified and robust version
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604151000000598528';
const ACTION = (process.argv[3] || 'pass').toLowerCase();
const REFUSE_CODE = process.argv[4] || 'CA_TRUE_HIT';
const CREDIT_AMOUNT = process.argv[5] || '100';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`=== RiskShield Approve v7 ===`);
    log(`Case: ${CASE_NO}, Action: ${ACTION.toUpperCase()}`);

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    try {
        // LOGIN
        log('[1] Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);
        
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(10000);
        log('[1] ✅ Logged in');

        // SEARCH FOR CASE
        log('[2] Searching for case...');
        
        // Find the Case Name dropdown trigger and click it
        // Based on analysis: it's an ant-select with "Case Name" text
        const caseNameSelect = page.locator('.ant-select').filter({ hasText: 'Case Name' }).first();
        
        if (await caseNameSelect.count() > 0) {
            await caseNameSelect.click();
            await page.waitForTimeout(1500);
            
            // Click "No." in dropdown
            const noOption = page.locator('.ant-select-item').filter({ hasText: /^No\.$/ }).first();
            if (await noOption.count() > 0) {
                await noOption.click();
                log('[2] Selected: No.');
            }
        }
        
        await page.waitForTimeout(500);
        
        // Enter case number in the input next to Case Name dropdown
        const inputs = await page.locator('input[type="text"]').all();
        for (const inp of inputs) {
            const box = await inp.boundingBox();
            if (box && box.x > 200 && box.x < 600 && box.width > 50) {
                await inp.click();
                await inp.clear();
                await inp.fill(CASE_NO);
                log('[2] Entered case number');
                break;
            }
        }
        
        // Click Search
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // CHECK CASE STATUS
        log('[3] Checking case...');
        const pageText = await page.textContent('body');
        
        if (!pageText.includes(CASE_NO)) {
            log(`❌ Case ${CASE_NO} not found`);
            return;
        }
        log('[3] ✅ Case found');
        
        // Find case row and click 审批
        const caseRow = page.locator('tbody tr').filter({ hasText: CASE_NO });
        if (await caseRow.count() === 0) {
            log('❌ Case row not found');
            return;
        }
        
        const rowText = await caseRow.textContent();
        if (rowText.includes('Closed') || rowText.includes('已结案')) {
            log('❌ Case is already closed');
            return;
        }
        
        const approveBtn = caseRow.locator('a').filter({ hasText: '审批' }).first();
        if (await approveBtn.count() === 0) {
            log('❌ 审批 button not found');
            return;
        }
        
        log('[3] Clicking 审批...');
        await approveBtn.click();
        await page.waitForTimeout(5000);

        // SWITCH TO NEW TAB
        log('[4] Opening case detail...');
        const pages = context.pages();
        let detailPage = page;
        if (pages.length > 1) {
            detailPage = pages[pages.length - 1];
            await detailPage.waitForLoadState('domcontentloaded');
            await detailPage.waitForTimeout(3000);
        }

        // FILL APPROVAL FORM
        log('[5] Filling approval form...');
        
        // Find ManualApprovalResult dropdown
        const manualDropdown = detailPage.locator('.ant-select').filter({ hasText: /ManualApprovalResult|Please choose/ }).first();
        
        if (await manualDropdown.count() > 0) {
            await manualDropdown.click();
            await page.waitForTimeout(500);
            
            if (ACTION === 'pass') {
                await detailPage.locator('.ant-select-item').filter({ hasText: 'Pass' }).first().click();
                log('[5] Selected: Pass');
                
                // Enter Credit Amount
                const creditInput = detailPage.locator('input').nth(5);
                await creditInput.fill(CREDIT_AMOUNT);
                log(`[5] Credit Amount: ${CREDIT_AMOUNT}`);
            } else {
                await detailPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).first().click();
                log('[5] Selected: Refuse');
                
                // Select Refuse Code
                const refuseDropdown = detailPage.locator('.ant-select').filter({ hasText: /Refuse Code/ }).first();
                if (await refuseDropdown.count() > 0) {
                    await refuseDropdown.click();
                    await page.waitForTimeout(500);
                    await detailPage.locator('.ant-select-item').filter({ hasText: REFUSE_CODE }).first().click();
                }
            }
        }
        
        await page.waitForTimeout(500);
        
        // Submit
        log('[6] Submitting...');
        const submitBtn = detailPage.locator('button').filter({ hasText: /提交|Submit/ }).last();
        if (await submitBtn.count() > 0) {
            await submitBtn.click();
            log('[6] ✅ Submitted');
            await page.waitForTimeout(3000);
        }

        // VERIFY
        log('[7] Verifying...');
        if (detailPage !== page) {
            await detailPage.close();
            await page.bringToFront();
        }
        
        await page.waitForTimeout(2000);
        
        // Re-search
        const caseInput = page.locator('input[type="text"]').filter({ hasText: '' }).nth(1);
        await caseInput.fill(CASE_NO);
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);
        
        const finalText = await page.textContent('body');
        if (finalText.includes('Closed')) {
            log('✅ SUCCESS! Case is now CLOSED');
        } else {
            log('⚠️ Please verify manually');
        }
        
    } catch (error) {
        log(`❌ ERROR: ${error.message}`);
    } finally {
        await browser.close();
        log('Done');
    }
})();
