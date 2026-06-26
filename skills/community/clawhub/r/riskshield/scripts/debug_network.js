/**
 * 调试脚本 - 监听所有网络请求
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

    // 监听所有请求
    const requests = [];
    page.on('request', req => {
        if (req.url().includes('riskshield') || req.url().includes('auth')) {
            requests.push({ method: req.method(), url: req.url() });
        }
    });

    // 监听所有响应
    page.on('response', resp => {
        if (resp.url().includes('riskshield') || resp.url().includes('auth')) {
            requests.push({ status: resp.status(), url: resp.url() });
        }
    });

    try {
        console.log('1. 访问登录页...');
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3000);
        console.log('   当前URL:', page.url());

        console.log('2. 填写表单...');
        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');

        console.log('3. 点击登录...');
        await page.locator('button:has-text("login")').click();

        // 等待一段时间
        console.log('4. 等待 15 秒...');
        await page.waitForTimeout(15000);

        console.log('5. 当前URL:', page.url());
        console.log('\n网络请求记录:');
        requests.forEach((r, i) => console.log(`  ${i+1}.`, JSON.stringify(r)));

        await page.screenshot({ path: '/Users/alan/.openclaw/workspace/debug_network.png' });

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();