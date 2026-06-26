/**
 * RiskShield - Direct navigation to case detail page
 */

const { chromium } = require('playwright');

const CASE_NO = '2604131000000597537';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        log('[1] Login...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);

        log('[1] Logged in');

        // Try different URLs to find the case detail
        // Based on earlier API response, detailTaskNo was A260413135933l0bmh12
        const detailUrls = [
            `https://riskshield.dcsuat.com/anytask-web/task/taskform/publish/detail?taskNo=A260413135933l0bmh12`,
            `https://riskshield.dcsuat.com/anytask-web/task/taskform/publish/approve?taskNo=A260413135933l0bmh12`,
            `https://riskshield.dcsuat.com/anytask-web/task/case/detail?caseCode=${CASE_NO}`,
        ];

        for (const url of detailUrls) {
            log(`[2] Trying: ${url.substring(0, 80)}...`);
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
            await page.waitForTimeout(5000);

            const text = await page.locator('body').textContent();
            const hasApproveBtn = text.includes('审批') || text.includes('通过');
            log(`[2] Page loaded, has approve button: ${hasApproveBtn}`);

            if (hasApproveBtn) {
                // Look for approve button
                const approveBtn = page.locator('button:has-text("审批"), button:has-text("通过")').first();
                if (await approveBtn.count() > 0 && await approveBtn.isVisible()) {
                    log('[3] Found approve button, clicking...');
                    await approveBtn.click();
                    await page.waitForTimeout(3000);

                    // Handle confirm
                    const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")').first();
                    if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                        log('[4] Confirming...');
                        await confirmBtn.click({ force: true });
                        await page.waitForTimeout(2000);
                    }
                    log('✅ SUCCESS!');
                    break;
                }
            }

            // Check for error message
            if (text.includes('error') || text.includes('Error') || text.includes('错误')) {
                log(`[2] Error on page: ${text.substring(0, 200)}`);
            }
        }

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
