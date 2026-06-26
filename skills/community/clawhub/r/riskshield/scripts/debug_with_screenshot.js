/**
 * RiskShield - 带截图的调试版本
 */

const { chromium } = require('playwright');

const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

const CASE_NO = '2604151000000599520';
const ACTION = 'pass';
const CREDIT_AMOUNT = '100';

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    try {
        // 登录
        console.log('1. 登录...');
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(20000);

        // 搜索案件
        console.log('2. 搜索案件...');
        await page.locator('span.val').filter({ hasText: /^Case Name$/ }).click();
        await page.waitForTimeout(2000);
        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(1000);
        await page.locator('input[type="text"]').nth(2).fill(CASE_NO);
        await page.waitForTimeout(500);
        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const searchBtn = buttons.find(b => b.textContent.trim() === 'Search');
            if (searchBtn) searchBtn.click();
        });
        await page.waitForTimeout(5000);

        // 获取审批链接
        console.log('3. 获取审批链接...');
        const approvalUrl = await page.evaluate(() => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes('2604151000000599520')) {
                    const links = row.querySelectorAll('a');
                    for (const link of links) {
                        if (link.textContent.trim() === 'Approval') {
                            return link.href;
                        }
                    }
                }
            }
            return null;
        });

        // 打开审批页面
        console.log('4. 打开审批页面...');
        const detailPage = await context.newPage();
        await detailPage.goto(approvalUrl, { waitUntil: 'domcontentloaded' });
        await detailPage.waitForTimeout(5000);

        // 点击 Decision Information tab
        console.log('5. 点击 Decision Information tab...');
        await detailPage.evaluate(() => {
            const tabs = document.querySelectorAll('[role="tab"]');
            for (const tab of tabs) {
                if (tab.textContent.includes('Decision') && tab.getAttribute('aria-selected') === 'false') {
                    tab.click();
                    return;
                }
            }
        });
        await detailPage.waitForTimeout(3000);

        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/form_step1.png' });

        // 选择 ManualApprovalResult -> Pass
        console.log('6. 选择 ManualApprovalResult -> Pass...');
        const visibleSelects = await detailPage.locator('.ant-select:visible').all();
        await visibleSelects[0].click();
        await detailPage.waitForTimeout(1000);
        await detailPage.locator('.ant-select-item').filter({ hasText: 'Pass' }).click();
        console.log('   已选择 Pass');

        await detailPage.waitForTimeout(3000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/form_step2.png' });

        // 填写金额
        console.log('7. 填写金额...');
        const inputs = await detailPage.locator('input').all();
        for (const input of inputs) {
            const ph = await input.getAttribute('placeholder');
            if (ph && ph.toLowerCase().includes('please enter')) {
                await input.click();
                await detailPage.waitForTimeout(100);
                await input.type(CREDIT_AMOUNT);
                const val = await input.inputValue();
                console.log('   输入框值:', val);
                break;
            }
        }

        await detailPage.waitForTimeout(2000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/form_step3.png' });

        // 检查所有 input 的值
        console.log('8. 检查所有 input 值...');
        const allInputsCheck = await detailPage.evaluate(() => {
            const inputs = document.querySelectorAll('input');
            const result = [];
            for (const input of inputs) {
                const ph = input.placeholder || '';
                if (ph.toLowerCase().includes('please enter') || ph === '') {
                    result.push({
                        placeholder: ph,
                        value: input.value,
                        visible: input.offsetParent !== null
                    });
                }
            }
            return result;
        });
        console.log('   金额相关 input:', JSON.stringify(allInputsCheck));

        // 点击 Submit
        console.log('9. 点击 Submit...');
        await detailPage.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Submit') {
                    btn.click();
                    return;
                }
            }
        });
        console.log('   已点击');

        await detailPage.waitForTimeout(5000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/form_step4.png' });

        // 检查案件状态
        console.log('10. 检查案件状态...');
        await page.bringToFront();
        await page.waitForTimeout(2000);

        const status = await page.evaluate(() => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes('2604151000000599520')) {
                    return row.textContent;
                }
            }
            return 'NOT FOUND';
        });
        console.log('   状态:', status.substring(0, 100));

        console.log('\n完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();