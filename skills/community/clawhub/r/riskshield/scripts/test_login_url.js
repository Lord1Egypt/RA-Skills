/**
 * 调试脚本 - 测试不同登录 URL
 */

const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    try {
        const REDIRECT = encodeURIComponent('https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html');

        console.log('测试: login.html + logout=true + redirect');
        await page.goto(`https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=${REDIRECT}`, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3000);

        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();

        await page.waitForResponse(resp => resp.url().includes('auth/login'), { timeout: 15000 }).catch(() => {});
        await page.waitForTimeout(10000);

        console.log('URL:', page.url());
        console.log('登录成功:', !page.url().includes('login'));

        if (!page.url().includes('login')) {
            await page.screenshot({ path: '/Users/alan/.openclaw/workspace/test_success.png' });

            // 确认页面元素
            console.log('\n检查页面元素:');
            const caseNameVisible = await page.locator('span.val:has-text("Case Name")').first().isVisible().catch(() => false);
            console.log('  Case Name 可见:', caseNameVisible);

            const inputs = await page.locator('input[type="text"]').count();
            console.log('  input[type=text] 数量:', inputs);

            const buttons = await page.locator('button').count();
            console.log('  button 数量:', buttons);

            const spanVals = await page.locator('span.val').all();
            console.log('  span.val 列表:');
            for (const sv of spanVals) {
                console.log('    -', await sv.textContent());
            }
        }

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();