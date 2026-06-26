/**
 * 调试 Tab 切换 - 使用更精确的方法
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
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/init.png' });

        // 检查 tabs 结构
        console.log('5. 检查 tabs 结构...');
        const tabInfo = await detailPage.evaluate(() => {
            const tabs = document.querySelectorAll('[role="tab"]');
            return Array.from(tabs).map(tab => ({
                text: tab.textContent,
                ariaSelected: tab.getAttribute('aria-selected'),
                id: tab.id,
                class: tab.className
            }));
        });
        console.log('   tabs:', JSON.stringify(tabInfo, null, 2));

        // 点击 Decision Information tab (aria-selected="false" 的那个)
        console.log('6. 点击 Decision Information...');
        await detailPage.evaluate(() => {
            const tabs = document.querySelectorAll('[role="tab"]');
            for (const tab of tabs) {
                if (tab.textContent.includes('Decision') && tab.getAttribute('aria-selected') === 'false') {
                    tab.click();
                    return;
                }
            }
        });
        console.log('   已点击');

        await detailPage.waitForTimeout(3000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_tab_click.png' });

        // 检查是否切换成功
        console.log('7. 检查 tab 切换状态...');
        const newTabInfo = await detailPage.evaluate(() => {
            const tabs = document.querySelectorAll('[role="tab"]');
            return Array.from(tabs).map(tab => ({
                text: tab.textContent,
                ariaSelected: tab.getAttribute('aria-selected')
            }));
        });
        console.log('   new tabs:', JSON.stringify(newTabInfo, null, 2));

        // 检查当前可见的 ant-select
        console.log('8. 检查 ant-select...');
        const selects = await detailPage.locator('.ant-select').all();
        console.log('   ant-select 数量:', selects.length);
        for (let i = 0; i < selects.length; i++) {
            const text = await selects[i].textContent();
            const visible = await selects[i].isVisible();
            console.log(`   [${i}]: "${text}" ${visible ? '(visible)' : '(hidden)'}`);
        }

        // 检查 ManualApprovalResult 是否存在
        console.log('9. 检查 ManualApprovalResult...');
        const manualApprovalExists = await detailPage.evaluate(() => {
            return document.body.textContent.includes('ManualApprovalResult');
        });
        console.log('   ManualApprovalResult 存在:', manualApprovalExists);

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();