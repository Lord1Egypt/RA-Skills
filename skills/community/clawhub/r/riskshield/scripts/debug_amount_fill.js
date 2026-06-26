/**
 * 调试金额填写 - React 状态问题
 */

const { chromium } = require('playwright');

const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

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
        await page.locator('input[type="text"]').nth(2).fill('2604151000000599520');
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

        // 尝试多种方法填写金额
        console.log('7. 尝试填写金额...');

        // 方法1: React 模拟输入
        const result1 = await detailPage.evaluate(() => {
            // 找到所有可见的 input
            const inputs = document.querySelectorAll('input');
            for (const input of inputs) {
                if (input.offsetParent !== null && input.type !== 'hidden') {
                    const ph = input.placeholder || '';
                    if (ph.toLowerCase().includes('please enter') || ph === '') {
                        // 尝试多种方法触发 React 状态更新
                        const value = '100';
                        
                        // 方法1: 直接设置 value 属性
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(input, value);
                        
                        // 触发 input 事件
                        const inputEvent = new Event('input', { bubbles: true });
                        input.dispatchEvent(inputEvent);
                        
                        // 触发 change 事件
                        const changeEvent = new Event('change', { bubbles: true });
                        input.dispatchEvent(changeEvent);
                        
                        return input.value;
                    }
                }
            }
            return null;
        });
        console.log('   方法1 (nativeInputValueSetter):', result1);

        await detailPage.waitForTimeout(1000);

        // 检查当前值
        const currentValue = await detailPage.evaluate(() => {
            const inputs = document.querySelectorAll('input');
            for (const input of inputs) {
                if (input.offsetParent !== null && input.type !== 'hidden') {
                    const ph = input.placeholder || '';
                    if (ph.toLowerCase().includes('please enter')) {
                        return input.value;
                    }
                }
            }
            return 'NOT FOUND';
        });
        console.log('   当前输入框值:', currentValue);

        // 截图查看
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/amount_check.png' });

        // 尝试方法2: 使用 Playwright 的 fill
        console.log('8. 尝试 Playwright fill...');
        const inputs = await detailPage.locator('input[type="text"]').all();
        for (let i = 0; i < Math.min(inputs.length, 5); i++) {
            const visible = await inputs[i].isVisible();
            const ph = await inputs[i].getAttribute('placeholder');
            if (visible) {
                console.log(`   input[${i}]: visible=${visible}, placeholder="${ph}"`);
            }
        }

        // 找到正确的输入框
        const creditInput = detailPage.locator('input[type="text"]').filter({ has: detailPage.locator('.. label:has-text("Credit Amount")') }).first();
        const creditInputExists = await creditInput.count();
        console.log('   Credit Amount 输入框数量:', creditInputExists);

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();