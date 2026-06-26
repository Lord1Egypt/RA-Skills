/**
 * RiskShield - Extract session info from browser after login
 */

const { chromium } = require('playwright');

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        log('[1] Opening login page...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        log('[2] Logging in...');
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);

        log('[2] Logged in');

        // Extract all storage data
        log('[3] Extracting session info...');
        
        const sessionData = await page.evaluate(() => {
            const result = {
                url: window.location.href,
                localStorage: {},
                sessionStorage: {},
                cookies: document.cookie
            };

            // Get localStorage
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                result.localStorage[key] = localStorage.getItem(key);
            }

            // Get sessionStorage
            for (let i = 0; i < sessionStorage.length; i++) {
                const key = sessionStorage.key(i);
                result.sessionStorage[key] = sessionStorage.getItem(key);
            }

            return result;
        });

        log(`URL: ${sessionData.url.substring(0, 100)}...`);
        log(`Cookies: ${sessionData.cookies.substring(0, 100)}...`);
        log('localStorage keys:', Object.keys(sessionData.localStorage));
        log('sessionStorage keys:', Object.keys(sessionData.sessionStorage));

        // Find sgin in URL
        const sginMatch = sessionData.url.match(/sgin=([^&]+)/);
        if (sginMatch) {
            log(`sgin found in URL: ${sginMatch[1].substring(0, 30)}...`);
        }

        // Find any Bearer token
        const allStorage = { ...sessionData.localStorage, ...sessionData.sessionStorage };
        for (const [key, value] of Object.entries(allStorage)) {
            if (value && value.includes('eyJ')) {
                log(`Token found in ${key}: ${value.substring(0, 50)}...`);
            }
        }

        // Try to get cookies from context
        const cookies = await context.cookies();
        log('\n[4] Context cookies:');
        cookies.forEach(c => {
            log(`  ${c.name}: ${c.value.substring(0, 30)}...`);
        });

        // Now try to make an API call using the page's fetch (should include cookies)
        log('\n[5] Testing API call from browser context...');
        
        const apiResult = await page.evaluate(async () => {
            try {
                // Get sgin from URL
                const urlParams = new URLSearchParams(window.location.search);
                const sgin = urlParams.get('sgin');
                
                const resp = await fetch('/anytask-web/task/case/list/all', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        startTime: 1775577600000,
                        endTime: Date.now(),
                        caseCode: '',
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
                
                const data = await resp.json();
                return { status: resp.status, ok: resp.ok, total: data?.data?.total, message: data?.message || 'ok' };
            } catch (e) {
                return { error: e.message };
            }
        });

        log(`API result: ${JSON.stringify(apiResult)}`);

    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
