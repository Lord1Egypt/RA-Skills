/**
 * RiskShield Playwright Automation - Approve Case
 */

const { chromium } = require('playwright');

const CONFIG = {
    loginUrl: 'https://riskshield.dcsuat.com/mc/page/login.html',
    username: 'alan.zhang',
    password: 'ZIdongshenpi1.'
};

async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

async function approveCase(caseNo) {
    console.log(`\n========================================`);
    console.log(`RiskShield Playwright Approve`);
    console.log(`Case: ${caseNo}`);
    console.log(`========================================\n`);

    let browser;
    
    try {
        console.log('[1/5] Launching browser...');
        browser = await chromium.launch({
            headless: false,
            args: ['--start-maximized']
        });
        
        const context = await browser.newContext({
            viewport: { width: 1920, height: 1080 }
        });
        
        const page = await context.newPage();
        
        // Step 1: Login
        console.log('[2/5] Logging in...');
        const loginUrl = `${CONFIG.loginUrl}?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s`;
        await page.goto(loginUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await sleep(3000);
        
        await page.locator('input[placeholder*="user" i]').fill(CONFIG.username);
        await page.locator('input[type="password"]').fill(CONFIG.password);
        await page.locator('button').first().click();
        await sleep(10000);
        
        console.log('  ✅ Logged in');
        
        // Step 2: Go to case list
        console.log('[3/5] Going to case list...');
        await page.goto('https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html', { waitUntil: 'networkidle', timeout: 30000 });
        await sleep(5000);
        
        // Step 3: Find the case in list
        console.log('[4/5] Finding case...');
        
        let found = false;
        for (let attempt = 0; attempt < 10 && !found; attempt++) {
            const pageText = await page.locator('body').textContent();
            
            if (pageText.includes(caseNo)) {
                console.log(`  ✅ Found case on page ${attempt + 1}!`);
                
                // Click on the case - try different approaches
                // First, try to find the case row and click on it
                try {
                    // Find all cells/links containing the case number
                    const caseCells = page.locator(`td:has-text("${caseNo}")`);
                    if (await caseCells.count() > 0) {
                        // Get the parent row and click on a link in it
                        const parentRow = caseCells.first().locator('..');
                        console.log('  Clicking case row...');
                        await parentRow.click();
                        await sleep(3000);
                        found = true;
                    }
                } catch (e) {
                    console.log('  Error clicking case:', e.message);
                }
                
                // Alternative: find and click the case link directly
                if (!found) {
                    const caseLink = page.locator(`a:has-text("${caseNo}"), span:has-text("${caseNo}")`).first();
                    if (await caseLink.count() > 0) {
                        console.log('  Clicking case link...');
                        await caseLink.click();
                        await sleep(3000);
                        found = true;
                    }
                }
                
                // Another approach: look for 操作 (actions) column
                if (!found) {
                    const caseText = await page.locator(`text=${caseNo}`).first();
                    if (await caseText.count() > 0) {
                        console.log('  Clicking case text...');
                        await caseText.click();
                        await sleep(3000);
                        found = true;
                    }
                }
            } else {
                console.log(`  Not on page ${attempt + 1}, trying next...`);
                const nextBtn = page.locator('button:has-text("下一页"), button:has-text("⟩")').first();
                if (await nextBtn.count() > 0) {
                    await nextBtn.click();
                    await sleep(2000);
                }
            }
        }
        
        if (!found) {
            throw new Error('Case not found in list after searching all pages');
        }
        
        // Step 4: Take screenshot of current state
        const screenshot1 = `/tmp/riskshield_detail_${Date.now()}.png`;
        await page.screenshot({ path: screenshot1, fullPage: true });
        console.log(`\n  Screenshot: ${screenshot1}`);
        
        // Step 5: Find and click approve button
        console.log('\n[5/5] Looking for approve button...');
        
        // First check if we're on a detail page or if the case opened in a modal
        const pageUrl = page.url();
        console.log('  Current URL:', pageUrl);
        
        // Look for approve button with various selectors
        const approveSelectors = [
            'button:has-text("通过")',
            'button:has-text("审批")', 
            'button:has-text("同意")',
            'a:has-text("通过")',
            'a:has-text("审批")',
            '[class*="approve"]',
            '[class*="pass"]'
        ];
        
        for (const sel of approveSelectors) {
            const btns = page.locator(sel);
            const count = await btns.count();
            if (count > 0) {
                for (let i = 0; i < count; i++) {
                    const btn = btns.nth(i);
                    const text = await btn.textContent();
                    const isVisible = await btn.isVisible();
                    console.log(`  Found "${sel}": "${text.trim()}" (visible: ${isVisible})`);
                    
                    if (isVisible && (text.includes('通过') || text.includes('审批') || text.includes('同意'))) {
                        console.log(`  Clicking: "${text.trim()}"`);
                        await btn.click({ force: true });
                        await sleep(2000);
                        
                        // Try to find and click confirm button
                        try {
                            const confirmBtn = page.locator('button:has-text("确认"), button:has-text("确定"), button:has-text("OK")').first();
                            if (await confirmBtn.count() > 0) {
                                const confirmVisible = await confirmBtn.isVisible();
                                console.log(`  Confirm button visible: ${confirmVisible}`);
                                if (confirmVisible) {
                                    await confirmBtn.click({ force: true });
                                    await sleep(2000);
                                }
                            }
                        } catch (e) {
                            console.log('  Confirm error:', e.message);
                        }
                        
                        console.log('\n✅ APPROVE CLICKED!');
                        return { success: true };
                    }
                }
            }
        }
        
        // List all buttons for debugging
        const allButtons = await page.locator('button').all();
        console.log(`  All buttons (${allButtons.length}):`);
        for (const btn of allButtons.slice(0, 20)) {
            const text = (await btn.textContent()).trim();
            const isVisible = await btn.isVisible();
            if (text) console.log(`    - "${text}" (visible: ${isVisible})`);
        }
        
        console.log('\n⚠️ Approve button not found or not clickable');
        return { success: false, error: 'Approve button not found' };
        
    } catch (error) {
        console.error('\n❌ ERROR:', error.message);
        return { success: false, error: error.message };
    } finally {
        if (browser) {
            await sleep(30000);  // Keep open for user to see
            await browser.close();
        }
    }
}

const args = process.argv.slice(2);
const caseNo = args[0];

if (!caseNo) {
    console.log(`
RiskShield Playwright Approve Script
====================================

Usage:
  node playwright_approve.js <caseNo>

Example:
  node playwright_approve.js 2604131000000597543
`);
    process.exit(1);
}

approveCase(caseNo)
    .then(result => {
        console.log('\n' + (result.success ? '✅ DONE' : '❌ FAILED') + ':', result.error || '');
        process.exit(result.success ? 0 : 1);
    });
