/**
 * 调试脚本 - 检查登录请求详情
 */

const { chromium } = require('playwright');

const REDIRECT_URL = encodeURIComponent('https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html');
const LOGIN_URL = `https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=${REDIRECT_URL}`;

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    // 监听登录请求
    page.on('response', async resp => {
        if (resp.url().includes('auth/login')) {
            console.log('登录响应状态:', resp.status());
            console.log('登录响应头:', JSON.stringify(resp.headers()));
            try {
                const body = await resp.text();
                console.log('登录响应体:', body.substring(0, 200));
            } catch (e) {}
        }
    });

    // 监听控制台消息
    page.on('console', msg => {
        if (msg.type() === 'error') {
            console.log('控制台错误:', msg.text());
        }
    });

    try {
        console.log('1. 访问登录页...');
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3000);

        console.log('2. 填写表单...');
        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');

        console.log('3. 点击登录...');
        await page.locator('button:has-text("login")').click();

        // 等待登录响应
        console.log('4. 等待登录响应...');
        await page.waitForTimeout(15000);

        console.log('5. 当前URL:', page.url());

        // 查看页面错误提示
        const errorEl = await page.locator('.ant-message, .error-message, [class*="error"]').first();
        if (await errorEl.isVisible().catch(() => false)) {
            console.log('页面错误:', await errorEl.textContent());
        }

        await page.screenshot({ path: '/Users/alan/.openclaw/workspace/login_check.png' });

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();