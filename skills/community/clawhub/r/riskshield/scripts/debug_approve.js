/**
 * 调试 Approve 选择
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
        console.log('   审批链接:', approvalUrl);

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

        // 列出所有 ant-select
        console.log('6. 列出所有 ant-select...');
        const allSelects = await detailPage.locator('.ant-select').all();
        console.log('   ant-select 总数:', allSelects.length);
        for (let i = 0; i < allSelects.length; i++) {
            const text = await allSelects[i].textContent();
            console.log(`   [${i}]: "${text}"`);
        }

        // 点击第 8 个下拉框 (ManualApprovalResult)
        console.log('7. 点击第 8 个下拉框...');
        await allSelects[7].click();
        await detailPage.waitForTimeout(1000);

        // 列出所有选项
        console.log('8. 列出所有选项...');
        const items = await detailPage.locator('.ant-select-item').all();
        console.log('   选项总数:', items.length);
        for (let i = 0; i < items.length; i++) {
            const text = await items[i].textContent();
            console.log(`   [${i}]: "${text}"`);
        }

        // 尝试点击 Approve
        console.log('9. 尝试点击 Approve...');
        const approveItem = detailPage.locator('.ant-select-item').filter({ hasText: /^Approve$/ });
        const approveCount = await approveItem.count();
        console.log('   Approve 选项数量:', approveCount);

        if (approveCount > 0) {
            await approveItem.click();
            console.log('   ✅ 已点击 Approve');
        } else {
            // 尝试模糊匹配
            const anyApprove = detailPage.locator('.ant-select-item').filter({ hasText: 'Approve' });
            const anyCount = await anyApprove.count();
            console.log('   模糊匹配 Approve 数量:', anyCount);
            if (anyCount > 0) {
                await anyApprove.first().click();
                console.log('   ✅ 已点击模糊匹配的 Approve');
            }
        }

        await detailPage.waitForTimeout(2000);

        // 检查状态
        console.log('10. 检查下拉框状态...');
        const selectsAfter = await detailPage.locator('.ant-select').all();
        for (let i = 0; i < selectsAfter.length; i++) {
            const text = await selectsAfter[i].textContent();
            console.log(`   [${i}]: "${text}"`);
        }

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();