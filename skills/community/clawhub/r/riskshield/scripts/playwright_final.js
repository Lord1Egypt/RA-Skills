/**
 * RiskShield Playwright - Search and click case
 */

const { chromium } = require('playwright');

async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

async function approveCase(caseNo) {
    console.log(`\n=== RiskShield Approve: ${caseNo} ===\n`);

    let browser;
    
    try {
        browser = await chromium.launch({ headless: false, args: ['--start-maximized'] });
        const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
        const page = await context.newPage();
        
        // Login
        console.log('[1] Logging in...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await sleep(3000);
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[type="password"]').fill('ZIdongshenpi1.');
        await page.locator('button').first().click();
        await sleep(10000);
        console.log('  Logged in');
        
        // Go to case list
        console.log('[2] Going to case list...');
        await page.goto('https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html', { waitUntil: 'networkidle' });
        await sleep(5000);
        
        // Try to find the search box - it might be in a filter section
        console.log('[3] Looking for search box...');
        
        // Get all inputs
        const inputs = await page.locator('input').all();
        console.log(`  Total inputs: ${inputs.length}`);
        
        // Try to fill every text input with the case number
        let searchFound = false;
        for (const inp of inputs) {
            const type = await inp.getAttribute('type');
            const placeholder = await inp.getAttribute('placeholder') || '';
            const isVisible = await inp.isVisible();
            
            if (isVisible && (type === 'text' || type === 'search' || !type)) {
                console.log(`  Trying input: type=${type}, placeholder=${placeholder}`);
                try {
                    await inp.fill(caseNo);
                    await sleep(1000);
                    
                    // Try pressing Enter
                    await inp.press('Enter');
                    await sleep(3000);
                    
                    // Check if case appeared
                    const pageText = await page.locator('body').textContent();
                    if (pageText.includes(caseNo)) {
                        console.log(`  ✅ Found case after searching with this input!`);
                        searchFound = true;
                        break;
                    } else {
                        // Clear and try next
                        await inp.fill('');
                    }
                } catch (e) {}
            }
        }
        
        // Take screenshot to see state
        const screenshot = `/tmp/riskshield_${Date.now()}.png`;
        await page.screenshot({ path: screenshot, fullPage: true });
        console.log(`\n  Screenshot: ${screenshot}`);
        
        // Check if we can see the case now
        const finalText = await page.locator('body').textContent();
        if (finalText.includes(caseNo)) {
            console.log('[4] Case found! Looking for approve button...');
            
            // Try clicking on the case number or its row
            try {
                const caseElement = page.locator(`text=${caseNo}`).first();
                await caseElement.click({ force: true });
                await sleep(3000);
                
                // Take another screenshot
                await page.screenshot({ path: `/tmp/riskshield_click_${Date.now()}.png`, fullPage: true });
                
                // Look for approve button
                const approveBtn = page.locator('button:has-text("通过"), button:has-text("审批")').first();
                if (await approveBtn.count() > 0 && await approveBtn.isVisible()) {
                    console.log('  Clicking approve...');
                    await approveBtn.click({ force: true });
                    await sleep(2000);
                    console.log('\n✅ APPROVE CLICKED!');
                    return { success: true };
                }
            } catch (e) {
                console.log('  Click error:', e.message);
            }
        } else {
            console.log('[4] Case NOT found on this page');
            
            // Try pagination
            for (let i = 0; i < 10; i++) {
                const nextBtn = page.locator('button:has-text("下一页"), button:has-text("⟩"), button[title="Next"]').first();
                if (await nextBtn.count() > 0 && await nextBtn.isVisible()) {
                    await nextBtn.click();
                    await sleep(2000);
                    
                    const newText = await page.locator('body').textContent();
                    if (newText.includes(caseNo)) {
                        console.log(`  ✅ Found case on page ${i+2}!`);
                        break;
                    }
                }
            }
        }
        
        console.log('\n⚠️ Please check screenshot and try manually');
        return { success: false };
        
    } catch (error) {
        console.error('\n❌ ERROR:', error.message);
        return { success: false, error: error.message };
    } finally {
        if (browser) {
            await sleep(20000);
            await browser.close();
        }
    }
}

const caseNo = process.argv[2] || '2604131000000597543';
approveCase(caseNo)
    .then(r => { console.log('\n' + (r.success ? '✅' : '❌')); process.exit(r.success ? 0 : 1); });
