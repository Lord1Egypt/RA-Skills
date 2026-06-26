/**
 * 调试脚本 - 提取正确的登录请求体
 */

const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext();
    const page = await context.newPage();

    page.on('request', req => {
        if (req.url().includes('auth/login') && req.method() === 'POST') {
            const body = req.postData();
            console.log('登录请求体:');
            console.log(body);
            console.log('\n解析后的 sign:');
            try {
                const json = JSON.parse(body);
                console.log(Buffer.from(json.sign, 'base64').toString());
            } catch (e) {}
        }
    });

    try {
        const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3000);

        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();

        await page.waitForTimeout(15000);

        console.log('\n最终URL:', page.url());

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();