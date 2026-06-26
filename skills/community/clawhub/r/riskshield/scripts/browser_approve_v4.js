/**
 * RiskShield Browser Approve Script v4
 * Headless mode - runs in background
 * 
 * Key fix: Properly handle the search type dropdown (Case Name → Case No)
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const https = require('https');

const API_BASE = 'riskshield.dcsuat.com';
const TOKEN_FILE = path.join(__dirname, '..', 'token.json');
const CASE_NO = process.argv[2] || '2604151000000598528';
const ACTION = (process.argv[3] || 'pass').toLowerCase();
const REFUSE_CODE = process.argv[4] || 'CA_TRUE_HIT';
const CREDIT_AMOUNT = process.argv[5] || '100';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

function httpsRequest(options, postData) {
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            const chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end', () => {
                const raw = Buffer.concat(chunks);
                try {
                    resolve({ statusCode: res.statusCode, body: JSON.parse(raw.toString()) });
                } catch (e) {
                    resolve({ statusCode: res.statusCode, body: raw.toString() });
                }
            });
        });
        req.on('error', reject);
        if (postData) req.write(postData);
        req.end();
    });
}

async function login() {
    const postData = JSON.stringify({
        username: 'alan.zhang',
        password: 'ZIdongshenpi1.',
        redirectUrl: 'aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s'
    });
    
    const options = {
        hostname: API_BASE,
        path: '/auth/login',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': `https://${API_BASE}`,
            'Referer': `https://${API_BASE}/mc/page/login.html`,
            'Content-Length': Buffer.byteLength(postData)
        }
    };
    
    const result = await httpsRequest(options, postData);
    
    if (result.statusCode === 200 && result.body?.token) {
        const tokenData = {
            token: result.body.token,
            secretToken: result.body.secretToken,
            expire: result.body.expire,
            obtainedAt: new Date().toISOString()
        };
        fs.writeFileSync(TOKEN_FILE, JSON.stringify(tokenData, null, 2));
        log('✅ Login successful');
        return result.body;
    } else {
        throw new Error(`Login failed: ${JSON.stringify(result.body)}`);
    }
}

function loadToken() {
    try {
        const data = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
        return data.token || null;
    } catch (e) {
        return null;
    }
}

async function ensureLoggedIn() {
    let token = loadToken();
    if (!token) {
        await login();
        token = loadToken();
    }
    return token;
}

(async () => {
    log(`=== RiskShield Browser Approve v4 (HEADLESS) ===`);
    log(`Case: ${CASE_NO}, Action: ${ACTION.toUpperCase()}`);

    await ensureLoggedIn();

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });

    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        ignoreHTTPSErrors: true
    });

    const page = await context.newPage();

    try {
        // ========== LOGIN ==========
        log('[1/7] Opening login page...');
        await page.goto(`https://${API_BASE}/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s`, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(10000);
        
        if (!page.url().includes('anytask-web')) {
            log('❌ Login failed');
            return;
        }
        log('[1/7] ✅ Logged in');

        // ========== DATE RANGE ==========
        log('[2/7] Selecting date range: 近7天...');
        const datePicker = page.locator('.ant-range-picker').first();
        if (await datePicker.count() > 0) {
            await datePicker.click();
            await page.waitForTimeout(1000);
            const preset = page.locator('.ant-picker-preset > span').filter({ hasText: '近7天' }).first();
            if (await preset.count() > 0) {
                await preset.click();
                log('[2/7] ✅ Selected 近7天');
            }
        }
        await page.waitForTimeout(500);

        // ========== SEARCH TYPE DROPDOWN ==========
        log('[3/7] Selecting search field: Case No (案件编号)...');
        
        // Find the search type dropdown - it should be a clickable element showing current selection
        // Look for the cascader or select that contains "Case Name" or "案件名称"
        const dropdown = page.locator('.ant-cascader, .ant-select, .search-type-selector, [class*="search"] [class*="selector"]').filter({ hasText: /Case Name|案件名称/ }).first();
        
        // Alternative: find by aria-label or placeholder
        const dropdownByPlaceholder = page.locator('input[placeholder*="Case"]').first();
        
        let dropdownToClick = null;
        if (await dropdown.count() > 0) {
            dropdownToClick = dropdown;
        } else if (await dropdownByPlaceholder.count() > 0) {
            dropdownToClick = dropdownByPlaceholder.locator('..').locator('.ant-select, .ant-cascader');
        }
        
        // Debug: list all potential dropdown elements
        log('[3/7] Debug: Looking for search type dropdown...');
        const allSelects = await page.locator('.ant-select').all();
        log(`  Found ${allSelects.length} ant-select elements`);
        for (let i = 0; i < Math.min(allSelects.length, 5); i++) {
            const text = await allSelects[i].textContent();
            const box = await allSelects[i].boundingBox();
            log(`  Select ${i}: "${text.substring(0, 40)}" at (${box?.x}, ${box?.y})`);
        }
        
        // Try clicking the first select that might be the search type
        if (allSelects.length > 0) {
            await allSelects[0].click();
            await page.waitForTimeout(1000);
            
            // Look for Case No / 案件编号 option
            const caseNoOption = page.locator('.ant-select-dropdown .ant-select-item, .ant-select-item-option').filter({ hasText: /Case No|案件编号|No\./ }).first();
            
            if (await caseNoOption.count() > 0) {
                await caseNoOption.click();
                log('[3/7] ✅ Selected Case No');
            } else {
                // Close dropdown by clicking elsewhere
                await page.click('body');
                log('[3/7] ⚠️ Case No not in dropdown, trying cascader...');
                
                // Try cascader
                const cascader = page.locator('.ant-cascader').first();
                if (await cascader.count() > 0) {
                    await cascader.click();
                    await page.waitForTimeout(1000);
                    const cascaderItem = page.locator('.ant-cascader-menu-item').filter({ hasText: /Case No|案件编号/ }).first();
                    if (await cascaderItem.count() > 0) {
                        await cascaderItem.click();
                        log('[3/7] ✅ Selected Case No (cascader)');
                    }
                }
            }
        }
        await page.waitForTimeout(500);

        // ========== ENTER CASE NUMBER ==========
        log(`[4/7] Entering case number: ${CASE_NO}...`);
        
        // Find the case number input - should be a text input near the search area
        // The input should be visible and have a reasonable width
        const inputs = await page.locator('input[type="text"]').all();
        let caseInput = null;
        
        for (const inp of inputs) {
            const box = await inp.boundingBox();
            if (box && box.width > 100 && await inp.isVisible()) {
                caseInput = inp;
                break;
            }
        }
        
        if (caseInput) {
            await caseInput.click();
            await caseInput.clear();
            await caseInput.fill(CASE_NO);
            log('[4/7] ✅ Case number entered');
        } else {
            log('❌ Cannot find case number input');
            return;
        }
        
        // Click Search
        log('[4/7] Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // ========== CHECK STATUS ==========
        log('[5/7] Checking case status...');
        
        await page.screenshot({ path: '/tmp/rs_search_result.png', fullPage: true });
        
        const pageText = await page.locator('body').textContent();
        
        if (pageText.includes('No Cases') || pageText.includes('没有案件')) {
            log(`❌ Case ${CASE_NO} not found - returned "No Cases"`);
            log('Hint: Search type dropdown may not have been set correctly to Case No');
            return;
        }
        
        if (!pageText.includes(CASE_NO)) {
            log(`❌ Case ${CASE_NO} not found`);
            return;
        }
        
        // Find the case row
        const rows = await page.locator('tbody tr').all();
        for (const row of rows) {
            const rowText = await row.textContent();
            if (rowText.includes(CASE_NO)) {
                log(`[5/7] Case found!`);
                
                if (rowText.includes('已结案') || rowText.includes('Closed')) {
                    log('❌ Case is CLOSED. Cannot approve.');
                    return;
                }
                
                // Find 审批 button
                const approveBtn = row.locator('a, button').filter({ hasText: /审批|Approve|Approval/ }).first();
                if (await approveBtn.count() === 0) {
                    log('❌ No 审批 button found in row');
                    return;
                }
                log('[5/7] ✅ Found 审批 button, clicking...');
                await approveBtn.click();
                break;
            }
        }

        // ========== NEW TAB ==========
        log('[6/7] Waiting for new tab...');
        await page.waitForTimeout(3000);
        
        const pages = context.pages();
        let detailPage = page;
        if (pages.length > 1) {
            detailPage = pages[pages.length - 1];
            await detailPage.waitForLoadState('domcontentloaded');
            await detailPage.waitForTimeout(2000);
            log(`[6/7] Switched to new tab`);
        }

        // ========== FILL FORM ==========
        log('[7/7] Filling approval form...');
        
        // ManualApprovalResult dropdown
        const manualDropdown = detailPage.locator('.ant-select').filter({ hasText: /ManualApprovalResult|人工审批|Please choose/ }).first();
        if (await manualDropdown.count() > 0) {
            await manualDropdown.click();
            await page.waitForTimeout(500);
            
            if (ACTION === 'pass') {
                await detailPage.locator('.ant-select-item').filter({ hasText: 'Pass' }).first().click();
                log('[7/7] Selected: Pass');
                
                // Credit Amount
                const creditInput = detailPage.locator('input').nth(5);
                await creditInput.fill(CREDIT_AMOUNT);
                log(`[7/7] Entered Credit Amount: ${CREDIT_AMOUNT}`);
            } else {
                await detailPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).first().click();
                log('[7/7] Selected: Refuse');
                
                // Refuse Code
                const refuseCodeDropdown = detailPage.locator('.ant-select').filter({ hasText: /Refuse Code|拒绝代码/ }).first();
                if (await refuseCodeDropdown.count() > 0) {
                    await refuseCodeDropdown.click();
                    await page.waitForTimeout(500);
                    await detailPage.locator('.ant-select-item').filter({ hasText: REFUSE_CODE }).first().click();
                }
            }
        }
        
        await page.waitForTimeout(500);
        
        // Submit
        const submitBtn = detailPage.locator('button').filter({ hasText: /提交|Submit/ }).last();
        if (await submitBtn.count() > 0) {
            await submitBtn.click();
            log('[7/7] ✅ Submit clicked');
            await page.waitForTimeout(3000);
        }
        
        // ========== VERIFY ==========
        log('Verifying result...');
        
        if (detailPage !== page) {
            await detailPage.close();
            await page.bringToFront();
        }
        
        await page.reload({ waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);
        
        const finalText = await page.locator('body').textContent();
        if (finalText.includes('已结案') && finalText.includes('同意')) {
            log('✅ APPROVE SUCCESS! Case closed with result: 同意');
        } else if (finalText.includes('已结案') && finalText.includes('拒绝')) {
            log('✅ REFUSE SUCCESS! Case closed with result: 拒绝');
        } else if (finalText.includes('已结案')) {
            log('✅ Case is now CLOSED');
        } else {
            log('⚠️ Status unclear. Please verify manually.');
        }
        
        log('\n=== DONE ===');
        
    } catch (error) {
        log(`❌ ERROR: ${error.message}`);
        try {
            await page.screenshot({ path: `/tmp/rs_error_${Date.now()}.png` });
        } catch (e) {}
    } finally {
        await browser.close();
    }
})();
