/**
 * RiskShield - Call API directly from browser context
 */

const { chromium } = require('playwright');

async function run() {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

    try {
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);

        console.log('Logged in');

        // Get the sgin token from URL
        const url = page.url();
        const sginMatch = url.match(/sgin=([^&]+)/);
        const sgin = sginMatch ? sginMatch[1] : null;
        console.log('sgin found:', !!sgin);

        // Make API call directly from browser with the same cookies/session
        const response = await page.evaluate(async (sgin) => {
            const startTime = 1775577600000; // 2026-04-08
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
            return resp.json();
        }, sgin);

        console.log('API Response:');
        console.log('Total:', response.data?.total);
        if (response.data?.caseList?.length > 0) {
            const c = response.data.caseList[0];
            console.log('Case:', c.caseCode, '| Status:', c.caseStatus, '| ApproveUser:', c.approveUser);
            console.log('TaskNo:', c.taskNo);
            console.log('DetailTaskNo:', c.detailTaskNo);
        }

    } catch (error) {
        console.error('ERROR:', error.message);
    } finally {
        await browser.close();
    }
}

run();
