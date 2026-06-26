/**
 * 最简化的登录测试
 */

const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    // 监听所有响应
    page.on('response', resp => {
        if (resp.url().includes('auth')) {
            console.log(`[${resp.status()}] ${resp.url().substring(0, 80)}`);
        }
    });

    try {
        const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

        console.log('1. 打开登录页...');
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        console.log('2. 填写表单...');
        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');

        console.log('3. 点击登录...');
        await page.locator('button:has-text("login")').click();

        console.log('4. 等待 20 秒...');
        await page.waitForTimeout(20000);

        console.log('5. 最终 URL:', page.url());
        console.log('6. 登录成功:', !page.url().includes('login'));

        await page.screenshot({ path: '/Users/alan/.openclaw/workspace/simple_test.png' });

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();