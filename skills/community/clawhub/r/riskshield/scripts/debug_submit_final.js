/**
 * RiskShield - 带更多调试信息的版本
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

        // 选择 ManualApprovalResult -> Pass
        console.log('6. 选择 ManualApprovalResult -> Pass...');
        const visibleSelects = await detailPage.locator('.ant-select:visible').all();
        await visibleSelects[0].click();
        await detailPage.waitForTimeout(1000);
        await detailPage.locator('.ant-select-item').filter({ hasText: 'Pass' }).click();
        console.log('   已选择 Pass');

        await detailPage.waitForTimeout(3000);

        // 填写金额 - 使用 pressSequentially 逐字输入
        console.log('7. 填写金额...');
        const inputs = await detailPage.locator('input').all();
        for (const input of inputs) {
            const ph = await input.getAttribute('placeholder');
            if (ph && ph.toLowerCase().includes('please enter')) {
                await input.click();
                await detailPage.waitForTimeout(200);
                
                // 使用 pressSequentially 逐字输入（模拟真实用户）
                await input.pressSequentially(CREDIT_AMOUNT, { delay: 50 });
                await detailPage.waitForTimeout(500);
                
                const val = await input.inputValue();
                console.log('   输入框值:', val);
                break;
            }
        }

        await detailPage.waitForTimeout(2000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/before_submit.png' });

        // 检查是否有任何验证错误
        console.log('8. 检查验证状态...');
        const validationError = await detailPage.evaluate(() => {
            // 查找所有红色边框的输入框（验证失败）
            const invalidInputs = document.querySelectorAll('.ant-form-item-has-error input');
            return invalidInputs.length > 0 ? '有验证错误' : '无验证错误';
        });
        console.log('   验证状态:', validationError);

        // 尝试使用更精确的方式点击 Submit 按钮
        console.log('9. 点击 Submit...');
        
        // 方法1: 直接使用 Playwright 的 click
        const submitBtn = detailPage.locator('button[type="submit"], button:has-text("Submit")').first();
        const submitBtnVisible = await submitBtn.isVisible().catch(() => false);
        console.log('   Submit 按钮可见:', submitBtnVisible);
        
        if (submitBtnVisible) {
            await submitBtn.click({ force: true });
            console.log('   已使用 force 点击');
        }
        
        await detailPage.waitForTimeout(5000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_submit_debug.png' });

        // 检查页面是否有错误提示
        console.log('10. 检查错误提示...');
        const errorText = await detailPage.evaluate(() => {
            const errors = document.querySelectorAll('.ant-message-error, .ant-notification-error, [class*="error"]');
            if (errors.length > 0) {
                return Array.from(errors).map(e => e.textContent).join(', ');
            }
            return '无错误提示';
        });
        console.log('   错误信息:', errorText);

        // 检查案件状态
        console.log('11. 检查案件状态...');
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