/**
 * 调试脚本 - 提取完整的登录流程
 */

const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    page.on('request', req => {
        if (req.url().includes('auth/login') && req.method() === 'POST') {
            console.log('>>> POST /auth/login');
            console.log('    body:', req.postData());
        }
    });

    page.on('response', resp => {
        if (resp.url().includes('auth/login')) {
            console.log('<<< 响应:', resp.status());
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

        console.log('4. 等待 auth/login 响应...');
        const authResp = await page.waitForResponse(resp => resp.url().includes('auth/login'), { timeout: 15000 }).catch(e => {
            console.log('   等待响应失败:', e.message);
            return null;
        });

        if (authResp) {
            console.log('   auth/login 状态:', authResp.status());
        }

        console.log('5. 等待 15 秒...');
        await page.waitForTimeout(15000);

        console.log('6. 最终 URL:', page.url());

        if (!page.url().includes('login')) {
            console.log('✅ 登录成功！');
            await page.screenshot({ path: '/Users/alan/.openclaw/workspace/login_final.png' });
        } else {
            console.log('❌ 登录失败');
            await page.screenshot({ path: '/Users/alan/.openclaw/workspace/login_failed_final.png' });
        }

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();