/**
 * RiskShield Browser Approve Script v5
 * Headless mode - runs in background
 * Key fix: Properly handle new tab for case detail page
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
        log('✅ Login API success');
        return result.body;
    } else {
        throw new Error(`Login API failed: ${JSON.stringify(result.body)}`);
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
    log(`=== RiskShield Approve v5 (HEADLESS) ===`);
    log(`Case: ${CASE_NO}, Action: ${ACTION.toUpperCase()}`);

    await ensureLoggedIn();

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-popup-blocking']
    });

    // Create context with extra permissions
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        ignoreHTTPSErrors: true,
        acceptDownloads: true
    });

    const page = await context.newPage();

    try {
        // ========== LOGIN ==========
        log('[1/8] Login...');
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
        log('[1/8] ✅ Logged in');

        // ========== DATE RANGE ==========
        log('[2/8] Date range: 近7天...');
        const datePicker = page.locator('.ant-range-picker').first();
        if (await datePicker.count() > 0) {
            await datePicker.click();
            await page.waitForTimeout(1000);
            const preset = page.locator('.ant-picker-preset > span').filter({ hasText: '近7天' }).first();
            if (await preset.count() > 0) {
                await preset.click();
                log('[2/8] ✅ Selected 近7天');
            }
        }
        await page.waitForTimeout(500);

        // ========== SEARCH TYPE ==========
        log('[3/8] Search type: Case No...');
        
        // Click the search type dropdown (first ant-select with search-related text)
        const searchTypeSelect = page.locator('.ant-select').nth(1); // Usually the second select
        if (await searchTypeSelect.count() > 0) {
            await searchTypeSelect.click();
            await page.waitForTimeout(1000);
            
            // Look for Case No option (could be "Case No" or "案件编号" or "No.")
            const caseNoOption = page.locator('.ant-select-item').filter({ hasText: /Case No|案件编号|No\.|编号/ }).first();
            if (await caseNoOption.count() > 0) {
                await caseNoOption.click();
                log('[3/8] ✅ Selected Case No');
            } else {
                await page.keyboard.press('Escape');
                log('[3/8] ⚠️ Case No option not found, proceeding anyway');
            }
        }
        await page.waitForTimeout(500);

        // ========== ENTER CASE NUMBER ==========
        log(`[4/8] Entering case: ${CASE_NO}...`);
        
        // Find the case number input
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
            log('[4/8] ✅ Case entered');
        }
        
        // Click Search
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        // ========== CHECK STATUS ==========
        log('[5/8] Checking case...');
        
        const pageText = await page.locator('body').textContent();
        
        if (pageText.includes('No Cases') || !pageText.includes(CASE_NO)) {
            log(`❌ Case ${CASE_NO} not found`);
            await page.screenshot({ path: '/tmp/rs_no_case.png' });
            return;
        }
        
        log('[5/8] ✅ Case found');
        
        // Find case row and click 审批
        const rows = await page.locator('tbody tr').all();
        for (const row of rows) {
            const text = await row.textContent();
            if (text.includes(CASE_NO)) {
                if (text.includes('已结案') || text.includes('Closed')) {
                    log('❌ Case is closed');
                    return;
                }
                
                // Click 审批 button
                const approveBtn = row.locator('a').filter({ hasText: '审批' }).first();
                if (await approveBtn.count() > 0) {
                    log('[5/8] Clicking 审批...');
                    
                    // Use Promise.all to handle potential new tab
                    const [newPage] = await Promise.all([
                        context.waitForEvent('page', { timeout: 10000 }).catch(() => null),
                        approveBtn.click()
                    ]);
                    
                    await page.waitForTimeout(3000);
                    
                    // If newPage was created, use it; otherwise check if URL changed
                    let detailPage = page;
                    if (newPage) {
                        detailPage = newPage;
                        await detailPage.waitForLoadState('domcontentloaded');
                        await detailPage.waitForTimeout(2000);
                        log('[6/8] ✅ New tab opened');
                    } else {
                        // Check if current page changed
                        const currentUrl = page.url();
                        log(`[6/8] Current URL after click: ${currentUrl}`);
                        if (currentUrl.includes('detail') || currentUrl.includes('taskform')) {
                            log('[6/8] ✅ Page navigated to detail');
                        } else {
                            log('[6/8] ⚠️ No new tab, might be using same page');
                        }
                    }
                    
                    // Take screenshot of detail page
                    await detailPage.screenshot({ path: '/tmp/rs_detail.png', fullPage: true });
                    log('[6/8] Screenshot saved');
                    
                    // ========== FILL FORM ==========
                    log('[7/8] Filling approval form...');
                    
                    // Wait for form to load
                    await detailPage.waitForTimeout(2000);
                    
                    // Find ManualApprovalResult dropdown
                    const manualResultLabel = detailPage.locator('*').filter({ hasText: /ManualApprovalResult|人工审批结果|Approval Result/ }).first();
                    
                    // Try to find the dropdown near this label
                    let formPage = detailPage;
                    
                    // Alternative: use iframe if form is in iframe
                    const frames = detailPage.frames();
                    log(`[7/8] Found ${frames.length} frames`);
                    
                    for (const frame of frames) {
                        try {
                            const frameUrl = frame.url();
                            if (frameUrl.includes('form') || frameUrl.includes('task')) {
                                log(`[7/8] Found form frame: ${frameUrl.substring(0, 60)}...`);
                                formPage = frame;
                                break;
                            }
                        } catch (e) {}
                    }
                    
                    // Find and click ManualApprovalResult dropdown
                    const dropdowns = await formPage.locator('.ant-select').all();
                    log(`[7/8] Found ${dropdowns.length} dropdowns in form`);
                    
                    for (let i = 0; i < Math.min(dropdowns.length, 10); i++) {
                        const text = await dropdowns[i].textContent();
                        log(`  Dropdown ${i}: "${text.substring(0, 50)}"`);
                    }
                    
                    // Click the first dropdown (usually ManualApprovalResult)
                    if (dropdowns.length > 0) {
                        await dropdowns[0].click();
                        await page.waitForTimeout(1000);
                        
                        if (ACTION === 'pass') {
                            const passOpt = formPage.locator('.ant-select-item').filter({ hasText: 'Pass' }).first();
                            if (await passOpt.count() > 0) {
                                await passOpt.click();
                                log('[7/8] Selected: Pass');
                            }
                            
                            // Enter credit amount
                            const inputs2 = await formPage.locator('input').all();
                            for (const inp of inputs2) {
                                const placeholder = await inp.getAttribute('placeholder').catch(() => '');
                                if (placeholder.includes('enter') || placeholder.includes('Enter')) {
                                    await inp.fill(CREDIT_AMOUNT);
                                    log(`[7/8] Entered: ${CREDIT_AMOUNT}`);
                                    break;
                                }
                            }
                        } else {
                            const refuseOpt = formPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).first();
                            if (await refuseOpt.count() > 0) {
                                await refuseOpt.click();
                                log('[7/8] Selected: Refuse');
                            }
                            
                            // Select refuse code
                            if (dropdowns.length > 1) {
                                await dropdowns[1].click();
                                await page.waitForTimeout(500);
                                const rcOpt = formPage.locator('.ant-select-item').filter({ hasText: REFUSE_CODE }).first();
                                if (await rcOpt.count() > 0) {
                                    await rcOpt.click();
                                }
                            }
                        }
                    }
                    
                    await page.waitForTimeout(500);
                    
                    // Click Submit
                    const submitBtn = formPage.locator('button').filter({ hasText: /提交|Submit/ }).last();
                    if (await submitBtn.count() > 0) {
                        await submitBtn.click();
                        log('[7/8] ✅ Submit clicked');
                        await page.waitForTimeout(3000);
                    }
                    
                    // Close detail page if separate
                    if (detailPage !== page && newPage) {
                        await detailPage.close();
                    }
                    
                    break;
                } else {
                    log('❌ No 审批 button');
                    return;
                }
            }
        }

        // ========== VERIFY ==========
        log('[8/8] Verifying...');
        await page.bringToFront();
        await page.waitForTimeout(2000);
        
        // Re-search
        await caseInput.fill(CASE_NO);
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);
        
        const finalText = await page.locator('body').textContent();
        if (finalText.includes('已结案') || finalText.includes('Closed')) {
            if (finalText.includes('同意') || finalText.includes('Approved')) {
                log('✅ APPROVE SUCCESS!');
            } else if (finalText.includes('拒绝') || finalText.includes('Reject')) {
                log('✅ REFUSE SUCCESS!');
            } else {
                log('✅ Case CLOSED');
            }
        } else {
            log('⚠️ Status unclear');
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
