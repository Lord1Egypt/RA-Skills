/**
 * RiskShield Debug - Capture network requests v2
 */

const { chromium } = require('playwright');

async function run() {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

    // Capture all responses
    page.on('response', async resp => {
        const url = resp.url();
        if (url.includes('anytask') || url.includes('anyform') || url.includes('list')) {
            console.log(`[RESP] ${resp.status()} ${url.substring(0, 80)}`);
            if (url.includes('list')) {
                try {
                    const body = await resp.text();
                    console.log(`    Body: ${body.substring(0, 300)}`);
                } catch (e) {}
            }
        }
    });

    try {
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);

        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(12000);

        console.log('Logged in');

        // Clear first
        const clearBtn = page.locator('button:has-text("Clear")');
        if (await clearBtn.count() > 0) {
            await clearBtn.click();
            await page.waitForTimeout(2000);
        }

        // Try search
        const caseInput = page.locator('input[type="text"]').nth(2);
        await caseInput.fill('26041310000005');
        await page.waitForTimeout(500);

        console.log('Clicking Search...');
        await page.locator('button:has-text("Search")').click();
        await page.waitForTimeout(5000);

        console.log('\nDone');

    } catch (error) {
        console.error('ERROR:', error.message);
    } finally {
        await browser.close();
    }
}

run();
