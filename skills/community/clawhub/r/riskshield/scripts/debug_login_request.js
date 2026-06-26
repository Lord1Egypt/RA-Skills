/**
 * 调试脚本 - 分析登录请求的详细信息
 */

const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext();
    const page = await context.newPage();

    // 监听请求体
    page.on('request', req => {
        if (req.url().includes('auth/login') && req.method() === 'POST') {
            console.log('POST /auth/login');
            console.log('  URL:', req.url());
            console.log('  方法:', req.method());
            console.log('  请求头:', JSON.stringify(req.headers()));
            console.log('  体:', req.postData());
        }
    });

    // 监听响应
    page.on('response', resp => {
        if (resp.url().includes('auth/login')) {
            console.log('响应状态:', resp.status());
            console.log('响应头:', JSON.stringify(resp.headers()));
        }
    });

    try {
        const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

        console.log('1. 打开登录页...');
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3000);

        console.log('2. 填写表单...');
        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');

        console.log('3. 点击登录并等待请求...');
        await page.locator('button:has-text("login")').click();

        // 等待一段时间
        await page.waitForTimeout(15000);

        console.log('4. 最终URL:', page.url());

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();