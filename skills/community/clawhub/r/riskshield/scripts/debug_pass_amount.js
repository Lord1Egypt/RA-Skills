/**
 * 调试 Pass 后的金额输入
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

        // 点击 Decision Information
        console.log('5. 点击 Decision Information...');
        await detailPage.evaluate(() => {
            const tabs = document.querySelectorAll('[role="tab"], .ant-tabs-tab, div');
            for (const tab of tabs) {
                if (tab.textContent.includes('Decision')) {
                    tab.click();
                    return;
                }
            }
        });
        await detailPage.waitForTimeout(2000);

        // 选择 ManualApprovalResult -> Pass
        console.log('6. 选择 ManualApprovalResult -> Pass...');
        const allSelects = await detailPage.locator('.ant-select').all();
        await allSelects[7].click();
        await detailPage.waitForTimeout(1000);
        await detailPage.locator('.ant-select-item').filter({ hasText: 'Pass' }).click();
        console.log('   已选择 Pass');

        await detailPage.waitForTimeout(3000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/pass_selected.png' });

        // 查找所有 input
        console.log('7. 查找所有 input...');
        const inputs = await detailPage.locator('input').all();
        console.log('   input 总数:', inputs.length);
        for (let i = 0; i < inputs.length; i++) {
            const ph = await inputs[i].getAttribute('placeholder');
            const type = await inputs[i].getAttribute('type');
            const value = await inputs[i].inputValue().catch(() => '');
            console.log(`   input[${i}]: type=${type}, placeholder="${ph}", value="${value}"`);
        }

        // 尝试用不同的选择器填写金额
        console.log('8. 尝试填写金额...');

        // 方法1: placeholder 包含 "please enter" (不区分大小写)
        const enterInputs = await detailPage.locator('input').filter({ hasPlaceholder: /please enter/i }).all();
        console.log('   方法1 (placeholder 包含 please enter):', enterInputs.length);

        if (enterInputs.length > 0) {
            await enterInputs[0].fill('100');
            console.log('   ✅ 方法1 成功');
        } else {
            // 方法2: 查找 Credit Amount 相关标签的下一个 input
            console.log('   方法2: 查找 Credit Amount 标签附近的 input...');
            const creditLabel = await detailPage.locator('*:has-text("Credit Amount")').first();
            if (await creditLabel.isVisible()) {
                console.log('   找到 Credit Amount 标签');
                // 查找附近的 input
                const nearInputs = await detailPage.locator('input[type="text"]').all();
                console.log('   text input 数量:', nearInputs.length);
                for (const input of nearInputs) {
                    const visible = await input.isVisible();
                    if (visible) {
                        await input.fill('100');
                        console.log('   ✅ 方法2 成功，填写了 100');
                        break;
                    }
                }
            }
        }

        await detailPage.waitForTimeout(1000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/amount_filled.png' });

        // 点击提交按钮
        console.log('9. 点击提交按钮...');
        await detailPage.locator('button').filter({ hasText: 'Submit' }).click();
        console.log('   ✅ 已点击提交按钮');

        await detailPage.waitForTimeout(5000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_submit.png' });

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();