/**
 * 调试脚本 - 使用 networkidle 等待登录完成
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
        await page.goto(LOGIN_URL, { waitUntil: 'networkidle' });
        await page.waitForTimeout(3000);

        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();

        // 等待URL变化或网络空闲
        console.log('2. 等待跳转...');
        await page.waitForURL('**/main.html**', { timeout: 30000 }).catch(e => console.log('waitForURL错误:', e.message));
        await page.waitForTimeout(5000);

        console.log('3. 当前URL:', page.url());

        if (!page.url().includes('login')) {
            console.log('✅ 登录成功！');

            // 截图
            await page.screenshot({ path: '/Users/alan/.openclaw/workspace/main_page.png' });

            // 查找元素
            const spanVals = await page.locator('span.val').all();
            console.log('   span.val 数量:', spanVals.length);
            for (let i = 0; i < Math.min(5, spanVals.length); i++) {
                console.log(`   span.val[${i}]:`, await spanVals[i].textContent());
            }

            const textInputs = await page.locator('input[type="text"]').all();
            console.log('   input[type=text] 数量:', textInputs.length);

            const buttons = await page.locator('button').all();
            console.log('   button 数量:', buttons.length);

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