/**
 * 调试脚本 - 检查登录后的页面结构
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

        await page.waitForResponse(resp => resp.url().includes('auth/login'), { timeout: 15000 }).catch(() => {});
        await page.waitForTimeout(10000);

        console.log('2. 当前URL:', page.url());

        // 截图
        await page.screenshot({ path: '/Users/alan/.openclaw/workspace/main_page.png' });

        console.log('3. 查找搜索区域元素...');

        // 查找所有 span.val
        const spanVals = await page.locator('span.val').all();
        console.log('   span.val 数量:', spanVals.length);
        for (let i = 0; i < spanVals.length; i++) {
            const text = await spanVals[i].textContent();
            console.log(`   span.val[${i}]:`, text);
        }

        // 查找所有 input[type="text"]
        const textInputs = await page.locator('input[type="text"]').all();
        console.log('   input[type=text] 数量:', textInputs.length);
        for (let i = 0; i < textInputs.length; i++) {
            const ph = await textInputs[i].getAttribute('placeholder');
            console.log(`   input[${i}] placeholder:`, ph);
        }

        // 查找所有 button
        const buttons = await page.locator('button').all();
        console.log('   button 数量:', buttons.length);
        for (let i = 0; i < buttons.length; i++) {
            const text = await buttons[i].textContent();
            console.log(`   button[${i}]:`, text);
        }

        // 查找所有 select
        const selects = await page.locator('select').all();
        console.log('   select 数量:', selects.length);

        // 查找包含 Case Name 的元素
        console.log('4. 查找 Case Name...');
        const caseNameEl = await page.locator('*:has-text("Case Name")').first();
        if (await caseNameEl.isVisible()) {
            console.log('   Case Name 元素可见');
            const tag = await caseNameEl.evaluate(el => el.tagName);
            const className = await caseNameEl.evaluate(el => el.className);
            console.log('   标签:', tag, '类:', className);
        }

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();