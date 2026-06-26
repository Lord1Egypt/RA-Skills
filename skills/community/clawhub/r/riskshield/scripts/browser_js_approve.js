/**
 * RiskShield - Direct API call from browser
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604131000000597537';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`Starting for case: ${CASE_NO}`);

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

    try {
        // Login
        log('[1] Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);
        log('[1] Logged in');

        // Get sgin from URL
        const url = page.url();
        const sginMatch = url.match(/sgin=([^&]+)/);
        const sgin = sginMatch ? sginMatch[1] : null;
        log(`[2] sgin: ${sgin ? 'found' : 'not found'}`);

        // Call API directly using fetch
        log('[3] Calling API directly...');
        const result = await page.evaluate(async (params) => {
            const { sgin, caseNo } = params;
            const startTime = 1775577600000;
            const endTime = Date.now();

            const resp = await fetch(`https://riskshield.dcsuat.com/anytask-web/task/case/list/all?sgin=${sgin}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    startTime,
                    endTime,
                    caseCode: caseNo,
                    caseName: '',
                    customerCardNo: '',
                    customerName: '',
                    customerPhone: '',
                    range: 'ALL',
                    sort: 'desc',
                    size: 20,
                    page: 0,
                    businessType: '',
                    approveUserId: '',
                    businessCode: 'All'
                })
            });

            return resp.json();
        }, { sgin, caseNo: CASE_NO });

        log(`[3] API response: total=${result.data?.total}`);

        if (result.data?.caseList?.length > 0) {
            const c = result.data.caseList[0];
            log(`[4] Case: ${c.caseCode}, Status: ${c.caseStatus}, ApproveUser: ${c.approveUser}`);
            log(`[4] TaskNo: ${c.taskNo}`);

            if (c.caseStatus === 'processing') {
                // Navigate to case detail
                const detailUrl = `https://riskshield.dcsuat.com/anytask-web/task/taskform/publish/detail?taskNo=${c.detailTaskNo}`;
                log(`[5] Going to detail: ${detailUrl}`);
                await page.goto(detailUrl, { waitUntil: 'domcontentloaded' });
                await page.waitForTimeout(5000);

                // Look for approve button
                const approveBtn = page.locator('button:has-text("通过"), button:has-text("审批")').first();
                if (await approveBtn.count() > 0 && await approveBtn.isVisible()) {
                    log('[6] Clicking approve...');
                    await approveBtn.click();
                    await page.waitForTimeout(3000);

                    const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")').first();
                    if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                        await confirmBtn.click({ force: true });
                        log('[6] Confirmed!');
                    }
                    log('✅ SUCCESS!');
                } else {
                    log('[6] Approve button not visible');
                }
            }
        } else {
            log('[4] Case not found');
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
