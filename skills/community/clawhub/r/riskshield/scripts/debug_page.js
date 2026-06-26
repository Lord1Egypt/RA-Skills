/**
 * RiskShield Debug - Check page structure
 */

const { chromium } = require('playwright');

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

async function run() {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    
    try {
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);
        
        await page.locator('input[placeholder*="user" i]').fill('alan.zhang');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button[type="submit"], button:has-text("login")').click();
        
        await page.waitForURL('**/anytask-web/**', { timeout: 20000 });
        await page.waitForTimeout(5000);
        
        log('=== Page Structure ===');
        
        // Get all inputs
        const inputs = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('input, textarea, select')).map(el => ({
                tag: el.tagName,
                type: el.type,
                id: el.id,
                name: el.name,
                placeholder: el.placeholder,
                className: el.className.substring(0, 80),
                visible: el.offsetWidth > 0 && el.offsetHeight > 0,
                rect: el.getBoundingClientRect ? `${Math.round(el.getBoundingClientRect().width)}x${Math.round(el.getBoundingClientRect().height)}` : 'N/A'
            }));
        });
        
        log(`Inputs (${inputs.length}):`);
        inputs.filter(i => i.visible).forEach((i, idx) => {
            log(`  [${idx}] ${i.tag} ${i.type} "${i.placeholder}" ${i.rect} ${i.className}`);
        });
        
        // Get all buttons
        const buttons = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('button')).map(el => ({
                text: el.textContent?.trim().substring(0, 50),
                className: el.className.substring(0, 60),
                visible: el.offsetWidth > 0 && el.offsetHeight > 0
            }));
        });
        
        log(`Buttons (${buttons.length}):`);
        buttons.filter(b => b.visible).forEach((b, idx) => {
            log(`  [${idx}] "${b.text}" ${b.className}`);
        });
        
        // Get case number container info
        log('=== Case Number Input ===');
        const caseContainer = await page.evaluate(() => {
            const all = document.querySelectorAll('*');
            for (const el of all) {
                if (el.childNodes.length === 1 && el.textContent === '案件名称案件编号客户姓名电话号码证件号码') {
                    return {
                        tag: el.tagName,
                        className: el.className,
                        childCount: el.childNodes.length,
                        nextSibling: el.nextElementSibling?.tagName + ' ' + el.nextElementSibling?.className?.substring(0, 50)
                    };
                }
            }
            return null;
        });
        log(JSON.stringify(caseContainer, null, 2));
        
        // Take screenshot
        await page.screenshot({ path: `/tmp/rs_debug_${Date.now()}.png`, fullPage: true });
        log('Screenshot saved');
        
    } catch (error) {
        log(`ERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
}

run().then(() => process.exit(0)).catch(err => { log(`Fatal: ${err.message}`); process.exit(1); });
