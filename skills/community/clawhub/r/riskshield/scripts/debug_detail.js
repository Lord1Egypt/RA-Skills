/**
 * 调试 Tab 切换后手动审批表单
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

        // 截图
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/detail_initial.png' });

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

        // 截图
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/detail_after_tab.png' });

        // 检查 ant-select 数量
        console.log('6. 检查 ant-select...');
        const selects = await detailPage.locator('.ant-select').all();
        console.log('   ant-select 数量:', selects.length);

        // 检查可见的 ant-select
        console.log('7. 检查可见的 ant-select...');
        for (let i = 0; i < selects.length; i++) {
            const visible = await selects[i].isVisible();
            const text = await selects[i].textContent();
            if (visible) {
                console.log(`   [${i}]: "${text}" (visible)`);
            }
        }

        // 点击第一个 "Please choose"
        console.log('8. 点击第一个 Please choose...');
        const firstPleaseChoose = detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).first();
        await firstPleaseChoose.click();
        await detailPage.waitForTimeout(1000);

        // 截图
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/detail_dropdown.png' });

        // 检查下拉选项
        console.log('9. 检查下拉选项...');
        const items = await detailPage.locator('.ant-select-item').all();
        console.log('   选项数量:', items.length);
        for (let i = 0; i < items.length; i++) {
            const text = await items[i].textContent();
            console.log(`   [${i}]: "${text}"`);
        }

        // 选择 Pass
        console.log('10. 选择 Pass...');
        const passItem = detailPage.locator('.ant-select-item').filter({ hasText: 'Pass' });
        const passCount = await passItem.count();
        console.log('    Pass 选项数量:', passCount);

        if (passCount > 0) {
            await passItem.click();
            console.log('    ✅ 已选择 Pass');
        }

        await detailPage.waitForTimeout(2000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/detail_after_pass.png' });

        // 检查输入框
        console.log('11. 检查输入框...');
        const textInputs = await detailPage.locator('input[type="text"]').all();
        console.log('    text input 数量:', textInputs.length);

        // 找到可见的 "Please enter" 输入框
        for (let i = 0; i < textInputs.length; i++) {
            const visible = await textInputs[i].isVisible();
            const ph = await textInputs[i].getAttribute('placeholder');
            if (visible && ph && ph.toLowerCase().includes('please enter')) {
                console.log(`    找到金额输入框 input[${i}]: placeholder="${ph}"`);
                await textInputs[i].fill('100');
                console.log('    ✅ 已填写金额 100');
                break;
            }
        }

        await detailPage.waitForTimeout(1000);

        // 点击 Submit
        console.log('12. 点击 Submit...');
        const submitClicked = await detailPage.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Submit') {
                    btn.click();
                    return true;
                }
            }
            return false;
        });
        console.log('    Submit 点击:', submitClicked ? '成功' : '失败');

        await detailPage.waitForTimeout(5000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/detail_final.png' });

        // 检查案件状态
        console.log('13. 检查案件状态...');
        const status = await page.evaluate(() => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes('2604151000000599520')) {
                    return row.textContent;
                }
            }
            return 'NOT FOUND';
        });
        console.log('    状态:', status);

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();