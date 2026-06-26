/**
 * RiskShield Browser Approve Script v3
 * Headless mode - runs in background, no visible browser window
 * 
 * Workflow:
 * 1. Login via API (get token)
 * 2. Open browser with saved cookies/token
 * 3. Navigate to case list
 * 4. Search for case
 * 5. Check status (审理中/已结案)
 * 6. If 审理中 → click 审批 → new tab opens
 * 7. Fill approval form (Pass/Refuse)
 * 8. Submit and verify
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const https = require('https');

const API_BASE = 'riskshield.dcsuat.com';
const TOKEN_FILE = path.join(__dirname, '..', 'token.json');
const CASE_NO = process.argv[2] || '2604151000000598528';
const ACTION = (process.argv[3] || 'pass').toLowerCase(); // 'pass' or 'refuse'
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
    log('Logging in via API...');
    
    const loginUrl = `https://${API_BASE}/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s`;
    
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
            'Referer': loginUrl,
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
        log('✅ Login successful, token saved');
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
    log(`Starting RiskShield Browser Approve v3 (HEADLESS)`);
    log(`Case: ${CASE_NO}, Action: ${ACTION.toUpperCase()}`);

    // Ensure logged in
    const token = await ensureLoggedIn();
    log(`Token loaded: ${token.substring(0, 20)}...`);

    // Launch browser in headless mode
    const browser = await chromium.launch({
        headless: true, // HEADLESS MODE - no visible window
        args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });

    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        ignoreHTTPSErrors: true
    });

    const page = await context.newPage();

    try {
        // ========== STEP 1: NAVIGATE TO LOGIN PAGE ==========
        log('[1/7] Opening login page...');
        const loginURL = `https://${API_BASE}/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s`;
        await page.goto(loginURL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3000);

        // Fill credentials
        log('[1/7] Filling credentials...');
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        
        // Wait for redirect
        await page.waitForTimeout(8000);
        
        if (!page.url().includes('anytask-web')) {
            // Check if login error
            const errorText = await page.locator('body').textContent();
            if (errorText.includes('Server request error')) {
                log('❌ Login failed: Server request error');
                await page.screenshot({ path: `/tmp/rs_login_error.png` });
                return;
            }
            log(`Current URL: ${page.url()}`);
        }
        log('[1/7] ✅ Logged in');

        // ========== STEP 2: DATE RANGE (近7天) ==========
        log('[2/7] Selecting date range: 近7天...');
        
        // Click date picker
        const datePicker = page.locator('.ant-range-picker, .ant-picker').first();
        if (await datePicker.count() > 0) {
            await datePicker.click();
            await page.waitForTimeout(1000);
            
            // Look for 近7天
            const presetTag = page.locator('.ant-picker-preset > span:has-text("近7天"), .ant-radio-wrapper:has-text("近7天")').first();
            if (await presetTag.count() > 0) {
                await presetTag.click();
                log('[2/7] ✅ Selected 近7天');
            } else {
                log('[2/7] ⚠️ 近7天 not found, proceeding anyway');
            }
        }
        await page.waitForTimeout(500);

        // ========== STEP 3: SEARCH FIELD SELECTOR ==========
        log('[3/7] Selecting search field: 案件编号...');
        
        // Find the search type dropdown - click on it to open options
        // Looking for a dropdown that contains "案件名称" (default) and needs to change to "案件编号"
        const searchTypeDropdown = page.locator('.ant-select').filter({ hasText: /案件名称|案件编号|客户姓名/ }).first();
        
        if (await searchTypeDropdown.count() > 0) {
            await searchTypeDropdown.click();
            await page.waitForTimeout(1000);
            
            // Select 案件编号
            const option = page.locator('.ant-select-item:has-text("案件编号"), .ant-select-item-option:has-text("案件编号")').first();
            if (await option.count() > 0) {
                await option.click();
                log('[3/7] ✅ Selected 案件编号');
            } else {
                log('[3/7] ⚠️ 案件编号 option not found');
            }
        } else {
            log('[3/7] ⚠️ Search type dropdown not found, checking for cascader...');
            // Maybe it's a cascader component
            const cascader = page.locator('.ant-cascader').first();
            if (await cascader.count() > 0) {
                await cascader.click();
                await page.waitForTimeout(1000);
                const cascaderOption = page.locator('.ant-cascader-menu-item:has-text("案件编号")').first();
                if (await cascaderOption.count() > 0) {
                    await cascaderOption.click();
                    log('[3/7] ✅ Selected 案件编号 (cascader)');
                }
            }
        }
        await page.waitForTimeout(500);

        // ========== STEP 4: ENTER CASE NUMBER & SEARCH ==========
        log(`[4/7] Entering case number: ${CASE_NO}...`);
        
        // Find all text inputs and locate the case number input
        const inputs = await page.locator('input[type="text"]').all();
        let caseInput = null;
        
        for (const inp of inputs) {
            const box = await inp.boundingBox();
            if (box && box.width > 100 && box.x > 0) {
                const value = await inp.inputValue().catch(() => '');
                const placeholder = await inp.getAttribute('placeholder').catch(() => '');
                log(`  Input ${inputs.indexOf(inp)}: placeholder="${placeholder}", value="${value}", width=${box.width}`);
                
                // The case input should be visible and have reasonable width
                if (box.width > 150 && await inp.isVisible()) {
                    caseInput = inp;
                    break;
                }
            }
        }
        
        if (!caseInput) {
            // Fallback: try to find by placeholder or text
            caseInput = page.locator('input[type="text"]').filter({ hasText: '' }).nth(2);
        }
        
        await caseInput.click();
        await caseInput.clear();
        await caseInput.fill(CASE_NO);
        log('[4/7] ✅ Case number entered');
        
        // Click Search
        log('[4/7] Clicking Search...');
        const searchBtn = page.locator('button:has-text("Search")').first();
        await searchBtn.click();
        await page.waitForTimeout(5000);

        // ========== STEP 5: CHECK CASE STATUS ==========
        log('[5/7] Checking case status...');
        
        const pageText = await page.locator('body').textContent();
        
        if (!pageText.includes(CASE_NO)) {
            log(`❌ Case ${CASE_NO} not found`);
            await page.screenshot({ path: `/tmp/rs_case_not_found.png` });
            return;
        }
        
        // Find case row
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
        log(`[5/7] Case found. Status check:`);
        
        if (rowText.includes('已结案')) {
            log('❌ Case is CLOSED (已结案). Cannot approve.');
            log('Please use a case with status "审理中".');
            return;
        }
        
        if (rowText.includes('审理中')) {
            log('[5/7] ✅ Case is in progress (审理中)');
        }
        
        // Find 审批 button
        const approveBtn = caseRow.locator('a:has-text("审批")').first();
        if (await approveBtn.count() === 0 || !(await approveBtn.isVisible())) {
            log('❌ No "审批" button found');
            return;
        }
        log('[5/7] ✅ Found 审批 button');

        // ========== STEP 6: OPEN CASE DETAIL (NEW TAB) ==========
        log('[6/7] Clicking 审批 to open case detail...');
        
        await approveBtn.click();
        await page.waitForTimeout(3000);
        
        // Switch to new tab
        const pages = context.pages();
        log(`[6/7] Total tabs: ${pages.length}`);
        
        let detailPage = page;
        if (pages.length > 1) {
            detailPage = pages[pages.length - 1];
            await detailPage.waitForLoadState('domcontentloaded');
            await detailPage.waitForTimeout(2000);
            log(`[6/7] Switched to new tab: ${detailPage.url().substring(0, 60)}...`);
        }

        // ========== STEP 7: FILL APPROVAL FORM ==========
        log('[7/7] Filling approval form...');
        
        // Find ManualApprovalResult dropdown
        const manualResultDropdown = detailPage.locator('.ant-select').filter({ hasText: /ManualApprovalResult|人工审批结果|Please choose/ }).first();
        
        if (await manualResultDropdown.count() === 0) {
            log('ERROR: ManualApprovalResult dropdown not found');
            await detailPage.screenshot({ path: `/tmp/rs_form_not_found.png` });
            return;
        }
        
        await manualResultDropdown.click();
        await detailPage.waitForTimeout(1000);
        
        if (ACTION === 'pass') {
            log('[7/7] Selecting: Pass');
            const passOption = detailPage.locator('.ant-select-item:has-text("Pass")').first();
            if (await passOption.count() > 0) {
                await passOption.click();
            } else {
                log('WARNING: Pass option not found');
            }
            
            // Enter Credit Amount
            log(`[7/7] Entering Credit Amount: ${CREDIT_AMOUNT}`);
            const creditInput = detailPage.locator('input').filter({ hasText: '' }).nth(5);
            await creditInput.fill(CREDIT_AMOUNT);
            
        } else {
            log('[7/7] Selecting: Refuse');
            const refuseOption = detailPage.locator('.ant-select-item:has-text("Refuse")').first();
            if (await refuseOption.count() > 0) {
                await refuseOption.click();
            }
            
            await detailPage.waitForTimeout(500);
            
            // Select Refuse Code
            log(`[7/7] Selecting Refuse Code: ${REFUSE_CODE}`);
            const refuseCodeDropdown = detailPage.locator('.ant-select').filter({ hasText: /Refuse Code|拒绝代码/ }).first();
            if (await refuseCodeDropdown.count() > 0) {
                await refuseCodeDropdown.click();
                await detailPage.waitForTimeout(500);
                
                const refuseCodeOption = detailPage.locator(`.ant-select-item:has-text("${REFUSE_CODE}")`).first();
                if (await refuseCodeOption.count() > 0) {
                    await refuseCodeOption.click();
                }
            }
        }
        
        await detailPage.waitForTimeout(500);
        
        // Click Submit button (bottom right, green)
        log('[7/7] Clicking Submit...');
        const submitBtn = detailPage.locator('button').filter({ hasText: /提交|Submit/ }).last();
        
        if (await submitBtn.count() > 0 && await submitBtn.isVisible()) {
            await submitBtn.click();
            log('[7/7] ✅ Submit clicked');
            await detailPage.waitForTimeout(3000);
        } else {
            log('WARNING: Submit button not found or not visible');
        }
        
        // ========== VERIFY ==========
        log('Verifying result...');
        
        // Close detail tab
        if (detailPage !== page) {
            await detailPage.close();
            await page.bringToFront();
            await page.waitForTimeout(1000);
        }
        
        // Re-search to verify
        await caseInput.fill(CASE_NO);
        await searchBtn.click();
        await page.waitForTimeout(5000);
        
        const finalText = await page.locator('body').textContent();
        if (finalText.includes('已结案')) {
            if (finalText.includes('同意')) {
                log('✅ APPROVE SUCCESS! Case closed with result: 同意');
            } else if (finalText.includes('拒绝')) {
                log('✅ REFUSE SUCCESS! Case closed with result: 拒绝');
            } else {
                log('✅ Case is now closed (已结案)');
            }
        } else {
            log('⚠️ Could not verify final status. Please check manually.');
        }
        
        log('\n✅ Browser Approve v3 COMPLETED');
        
    } catch (error) {
        log(`❌ ERROR: ${error.message}`);
        try {
            await page.screenshot({ path: `/tmp/rs_error_${Date.now()}.png` });
            log('Screenshot saved to /tmp/rs_error_*.png');
        } catch (e) {}
    } finally {
        await browser.close();
    }
})();
