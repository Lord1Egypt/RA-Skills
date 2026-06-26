/**
 * RiskShield - Debug API response
 */

const { chromium } = require('playwright');

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage();

    try {
        // Login
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);

        const url = page.url();
        const sginMatch = url.match(/sgin=([^&]+)/);
        const sgin = sginMatch ? sginMatch[1] : null;

        log(`sgin: ${sgin ? 'found' : 'not found'}`);

        // Check API response structure
        const result = await page.evaluate(async (sg) => {
            const resp = await fetch(`https://riskshield.dcsuat.com/anytask-web/task/case/list/all?sgin=${sg}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    startTime: 1775577600000,
                    endTime: Date.now(),
                    caseCode: '2604131000000597537',
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
            return await resp.json();
        }, sgin);

        log(`Full response: ${JSON.stringify(result).substring(0, 500)}`);

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
