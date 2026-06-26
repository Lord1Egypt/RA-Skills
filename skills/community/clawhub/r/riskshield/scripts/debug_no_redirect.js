/**
 * 调试脚本 - 测试无 redirect 的登录
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
        console.log('1. 访问登录页 (无 redirect)...');
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?logout=true', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        console.log('2. 填写表单...');
        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');

        console.log('3. 点击登录...');
        await page.locator('button:has-text("login")').click();

        await page.waitForResponse(resp => resp.url().includes('auth/login'), { timeout: 15000 }).catch(() => {});
        await page.waitForTimeout(10000);

        console.log('4. 当前URL:', page.url());

        if (!page.url().includes('login')) {
            console.log('✅ 登录成功！');

            await page.screenshot({ path: '/Users/alan/.openclaw/workspace/main_no_redirect.png' });

            // 尝试访问 main.html
            console.log('5. 访问 main.html...');
            await page.goto('https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html', { waitUntil: 'domcontentloaded' });
            await page.waitForTimeout(5000);
            console.log('6. main.html URL:', page.url());

            // 检查页面元素
            const caseNameVisible = await page.locator('span.val:has-text("Case Name")').first().isVisible().catch(() => false);
            console.log('Case Name 可见:', caseNameVisible);

            const inputs = await page.locator('input[type="text"]').count();
            console.log('input[type=text] 数量:', inputs);

            const buttons = await page.locator('button').count();
            console.log('button 数量:', buttons);

        } else {
            console.log('❌ 登录失败');
            await page.screenshot({ path: '/Users/alan/.openclaw/workspace/login_failed_v2.png' });
        }

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();