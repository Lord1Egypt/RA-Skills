/**
 * 调试脚本 - 混合等待策略
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

    try {
        console.log('1. 登录...');
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();

        // 等待网络响应
        console.log('2. 等待 auth/login 响应...');
        await page.waitForResponse(resp => resp.url().includes('auth/login'), { timeout: 15000 }).catch(e => console.log('响应等待:', e.message));

        // 额外等待
        console.log('3. 等待 12 秒...');
        await page.waitForTimeout(12000);

        console.log('4. 当前URL:', page.url());

        if (!page.url().includes('login')) {
            console.log('✅ 登录成功！');
            await page.screenshot({ path: '/Users/alan/.openclaw/workspace/main_page.png' });

            // 检查页面内容
            const bodyText = await page.evaluate(() => document.body.innerText);
            console.log('页面文本片段:', bodyText.substring(0, 500));
        } else {
            console.log('❌ 仍在登录页');
            await page.screenshot({ path: '/Users/alan/.openclaw/workspace/still_login.png' });
        }

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();