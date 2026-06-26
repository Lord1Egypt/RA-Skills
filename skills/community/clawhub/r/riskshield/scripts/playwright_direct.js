/**
 * RiskShield Playwright - Direct case detail navigation
 */

const { chromium } = require('playwright');

const CONFIG = {
    username: 'alan.zhang',
    password: 'ZIdongshenpi1.'
};

async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

async function approveCase(caseNo, taskNo) {
    console.log(`\n========================================`);
    console.log(`RiskShield Playwright - Direct Approve`);
    console.log(`Case: ${caseNo}, Task: ${taskNo}`);
    console.log(`========================================\n`);

    let browser;
    
    try {
        console.log('[1/4] Launching browser...');
        browser = await chromium.launch({
            headless: false,
            args: ['--start-maximized']
        });
        
        const context = await browser.newContext({
            viewport: { width: 1920, height: 1080 }
        });
        
        const page = await context.newPage();
        
        // Step 1: Login
        console.log('[2/4] Logging in...');
        const loginUrl = `https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s`;
        await page.goto(loginUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await sleep(3000);
        
        await page.locator('input[placeholder*="user" i]').fill(CONFIG.username);
        await page.locator('input[type="password"]').fill(CONFIG.password);
        await page.locator('button').first().click();
        await sleep(10000);
        
        console.log('  Logged in, URL:', page.url().substring(0, 100));
        
        // Get cookies after login
        const cookies = await context.cookies();
        console.log('  Cookies:', cookies.map(c => c.name).join(', '));
        
        // Step 2: Navigate directly to case detail
        console.log('[3/4] Going to case detail...');
        const caseUrl = `https://riskshield.dcsuat.com/anytask-web/task/taskform/publish/detail?taskNo=${taskNo}`;
        console.log('  URL:', caseUrl);
        
        // Navigate to case list first to establish session
        await page.goto('https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html', { waitUntil: 'networkidle', timeout: 30000 });
        await sleep(3000);
        
        // Now try to navigate to case detail
        await page.goto(caseUrl, { waitUntil: 'networkidle', timeout: 30000 });
        await sleep(5000);
        
        console.log('  After navigation, URL:', page.url());
        
        // Check if we got the form or an error page
        const content = await page.content();
        if (content.includes('{"code":9999') || content.includes('"code":9999')) {
            console.log('  ⚠️ Got error JSON response');
        }
        
        // Take screenshot
        const screenshot = `/tmp/riskshield_detail_${Date.now()}.png`;
        await page.screenshot({ path: screenshot, fullPage: true });
        console.log(`\n  Screenshot: ${screenshot}`);
        
        // Step 3: Look for approve button
        console.log('\n[4/4] Looking for approve button...');
        
        const approveSelectors = [
            'button:has-text("通过")',
            'button:has-text("审批")',
            'button:has-text("同意")',
            'a:has-text("通过")',
            'a:has-text("审批")',
            'button:has-text("Pass")',
            'button:has-text("Approve")'
        ];
        
        for (const sel of approveSelectors) {
            const btns = page.locator(sel);
            const count = await btns.count();
            if (count > 0) {
                for (let i = 0; i < Math.min(count, 10); i++) {
                    const btn = btns.nth(i);
                    const text = (await btn.textContent()).trim();
                    const isVisible = await btn.isVisible();
                    const isEnabled = await btn.isEnabled();
                    console.log(`  ${sel}: "${text}" (visible: ${isVisible}, enabled: ${isEnabled})`);
                }
            }
        }
        
        // Try to click the most likely approve button
        try {
            const approveBtn = page.locator('button:has-text("通过"), button:has-text("审批")').first();
            if (await approveBtn.count() > 0 && await approveBtn.isVisible() && await approveBtn.isEnabled()) {
                const text = (await approveBtn.textContent()).trim();
                console.log(`\n  Clicking: "${text}"`);
                await approveBtn.click({ force: true });
                await sleep(2000);
                
                // Try to confirm
                try {
                    const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定")').first();
                    if (await confirmBtn.count() > 0 && await confirmBtn.isVisible()) {
                        await confirmBtn.click({ force: true });
                        await sleep(2000);
                        console.log('  ✅ Confirmed!');
                    }
                } catch (e) {
                    console.log('  Confirm not needed or failed:', e.message);
                }
                
                console.log('\n✅ APPROVE CLICKED!');
                return { success: true };
            }
        } catch (e) {
            console.log('  Click error:', e.message);
        }
        
        // Debug: list all buttons
        const allBtns = await page.locator('button').all();
        console.log(`\n  All ${allBtns.length} buttons:`);
        for (const btn of allBtns) {
            const text = (await btn.textContent()).trim();
            if (text) console.log(`    - "${text}"`);
        }
        
        return { success: false, error: 'Approve button not found or not clickable' };
        
    } catch (error) {
        console.error('\n❌ ERROR:', error.message);
        return { success: false, error: error.message };
    } finally {
        if (browser) {
            await sleep(30000);
            await browser.close();
        }
    }
}

const args = process.argv.slice(2);
const caseNo = args[0];
const taskNo = args[1] || 'A260413496274oxp633k';

approveCase(caseNo, taskNo)
    .then(result => {
        console.log('\n' + (result.success ? '✅ DONE' : '❌ FAILED') + ':', result.error || '');
        process.exit(result.success ? 0 : 1);
    });
