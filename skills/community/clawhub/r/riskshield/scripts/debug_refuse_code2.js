/**
 * 调试 Refuse Code 下拉框 - 更详细的检查
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
        console.log('   URL:', page.url().substring(0, 80));

        // 搜索案件
        console.log('2. 搜索案件...');
        await page.locator('span.val').filter({ hasText: /^Case Name$/ }).click();
        await page.waitForTimeout(2000);
        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(1000);
        await page.locator('input[type="text"]').nth(2).fill('2604161000000599527');
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
                if (row.textContent.includes('2604161000000599527')) {
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

        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/debug_before.png' });

        // 选择 ManualApprovalResult -> Refuse
        console.log('6. 选择 ManualApprovalResult -> Refuse...');
        const manualSelect = await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).first();
        await manualSelect.click();
        await detailPage.waitForTimeout(1000);
        await detailPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).click();
        console.log('   已选择 Refuse');

        // 等待页面更新
        await detailPage.waitForTimeout(3000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/debug_after_refuse.png' });

        // 检查所有可能的选择器
        console.log('7. 详细检查页面元素...');

        // 检查是否有其他下拉框
        console.log('   检查 .ant-select 总数:', await detailPage.locator('.ant-select').count());
        console.log('   检查 select 总数:', await detailPage.locator('select').count());
        console.log('   检查所有带 label 的元素:');

        const labels = await detailPage.locator('label, .label, [class*="label"]').all();
        for (const label of labels) {
            const text = await label.textContent();
            if (text && text.trim()) {
                console.log(`     label: "${text.trim()}"`);
            }
        }

        // 检查 Refuse Code 附近的元素
        console.log('   查找包含 "Refuse Code" 的元素:');
        const refuseCodeLabel = await detailPage.locator('*:has-text("Refuse Code")').first();
        if (await refuseCodeLabel.isVisible()) {
            const parent = await refuseCodeLabel.evaluateHandle(el => el.parentElement);
            const parentHtml = await parent.asElement().innerHTML();
            console.log('     Refuse Code 父元素:', parentHtml.substring(0, 300));
        }

        // 查找 Refuse Code 的下拉框 - 通过父元素查找
        console.log('   通过 Refuse Code 标签查找下拉框:');
        const refuseCodeContainer = await detailPage.evaluateHandle(() => {
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                if (el.textContent === 'Refuse Code') {
                    // 找到 Refuse Code 标签的父容器
                    let parent = el.parentElement;
                    // 向上查找包含 ant-select 的容器
                    while (parent && !parent.classList.contains('ant-select')) {
                        parent = parent.parentElement;
                    }
                    return parent;
                }
            }
            return null;
        });

        if (refuseCodeContainer) {
            const html = await refuseCodeContainer.asElement().innerHTML();
            console.log('     Refuse Code 下拉框 HTML:', html.substring(0, 200));
        }

        // 列出所有包含 "CA_" 的元素
        console.log('   查找包含 "CA_" 的元素:');
        const caElements = await detailPage.evaluate(() => {
            const result = [];
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                if (el.textContent && el.textContent.includes('CA_')) {
                    result.push({
                        tag: el.tagName,
                        class: el.className,
                        text: el.textContent.substring(0, 50)
                    });
                }
            }
            return result;
        });
        console.log('     CA_ 元素:', JSON.stringify(caElements.slice(0, 5)));

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();