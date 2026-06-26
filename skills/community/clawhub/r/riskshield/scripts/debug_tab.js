/**
 * 调试 Decision Information 选项卡切换
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

        // 截图初始状态
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/tab_initial.png' });

        // 检查所有 tabs
        console.log('5. 检查所有 tabs...');
        const tabs = await detailPage.locator('[role="tab"], .ant-tabs-tab').all();
        console.log('   tab 数量:', tabs.length);
        for (let i = 0; i < tabs.length; i++) {
            const text = await tabs[i].textContent();
            const isActive = await tabs[i].evaluate(el => el.classList.contains('ant-tabs-tab-active'));
            console.log(`   tab[${i}]: "${text}" ${isActive ? '(active)' : ''}`);
        }

        // 点击 Decision Information - 使用更精确的选择器
        console.log('6. 点击 Decision Information...');
        await detailPage.locator('[role="tab"]').filter({ hasText: 'Decision Information' }).click();
        console.log('   已点击 Decision tab');

        await detailPage.waitForTimeout(3000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/tab_after_click.png' });

        // 检查 Decision Information 选项卡的内容
        console.log('7. 检查 Decision Information 内容...');
        const decisionContent = await detailPage.evaluate(() => {
            // 查找 tab panel
            const panels = document.querySelectorAll('[role="tabpanel"]');
            for (const panel of panels) {
                if (panel.textContent.includes('ManualApprovalResult')) {
                    return panel.textContent.substring(0, 200);
                }
            }
            return '未找到 ManualApprovalResult';
        });
        console.log('   Decision 内容:', decisionContent);

        // 检查 ant-select 数量
        console.log('8. 检查 ant-select...');
        const selects = await detailPage.locator('.ant-select').all();
        console.log('   ant-select 数量:', selects.length);
        for (let i = 0; i < selects.length; i++) {
            const text = await selects[i].textContent();
            console.log(`   [${i}]: "${text}"`);
        }

        // 选择 ManualApprovalResult -> Pass
        console.log('9. 选择 ManualApprovalResult -> Pass...');
        if (selects.length >= 8) {
            await selects[7].click();
            await detailPage.waitForTimeout(1000);

            const items = await detailPage.locator('.ant-select-item').all();
            console.log('   下拉选项数量:', items.length);
            for (let i = 0; i < items.length; i++) {
                console.log(`   [${i}]:`, await items[i].textContent());
            }

            await detailPage.locator('.ant-select-item').filter({ hasText: 'Pass' }).click();
            console.log('   已选择 Pass');
        }

        await detailPage.waitForTimeout(2000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_pass.png' });

        // 检查输入框
        console.log('10. 检查输入框...');
        const inputs = await detailPage.locator('input[type="text"]').all();
        console.log('    text input 数量:', inputs.length);
        for (let i = 0; i < Math.min(inputs.length, 5); i++) {
            const ph = await inputs[i].getAttribute('placeholder');
            console.log(`    input[${i}]: placeholder="${ph}"`);
        }

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();