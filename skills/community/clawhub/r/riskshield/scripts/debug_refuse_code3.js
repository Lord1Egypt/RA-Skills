/**
 * 调试 - 检查选择 Refuse 后的页面状态
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

        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/before_refuse.png' });

        // 选择 ManualApprovalResult -> Refuse
        console.log('6. 选择 ManualApprovalResult -> Refuse...');
        const manualSelect = await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).first();
        await manualSelect.click();
        await detailPage.waitForTimeout(1000);

        // 先点击第一个选项查看
        const items = await detailPage.locator('.ant-select-item').all();
        console.log('   下拉选项:');
        for (let i = 0; i < Math.min(items.length, 5); i++) {
            console.log(`   [${i}]:`, await items[i].textContent());
        }

        await detailPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).click();
        console.log('   已选择 Refuse');

        await detailPage.waitForTimeout(3000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_refuse_select.png' });

        // 列出所有 .ant-select 的文本
        console.log('7. 选择 Refuse 后的下拉框状态:');
        const selects = await detailPage.locator('.ant-select').all();
        for (let i = 0; i < selects.length; i++) {
            const text = await selects[i].textContent();
            const isOpen = await selects[i].evaluate(el => el.classList.contains('ant-select-open'));
            console.log(`   [${i}]: "${text}" ${isOpen ? '(open)' : ''}`);
        }

        // 检查是否有包含 "Refuse" 或 "Code" 的文本
        console.log('8. 查找包含 Refuse/Code 的元素:');
        const elements = await detailPage.evaluate(() => {
            const result = [];
            const els = document.querySelectorAll('span, div, label');
            for (const el of els) {
                const text = el.textContent.trim();
                if (text === 'Refuse Code' || text === 'Code') {
                    result.push({
                        tag: el.tagName,
                        class: el.className,
                        text: text,
                        id: el.id
                    });
                }
            }
            return result;
        });
        console.log('   找到的元素:', JSON.stringify(elements));

        // 检查 Refuse Code 下拉框是否可见
        console.log('9. 检查 Refuse Code 下拉框是否已出现:');
        const refuseCodeSelectVisible = await detailPage.locator('.ant-select').filter({ hasText: /^Refuse Code/ }).isVisible().catch(() => false);
        console.log('   Refuse Code 选择器可见:', refuseCodeSelectVisible);

        // 尝试点击第二个 "Please choose"
        console.log('10. 尝试点击第二个 Please choose...');
        const pleaseChooseSelects = await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).all();
        console.log('    Please choose 数量:', pleaseChooseSelects.length);

        if (pleaseChooseSelects.length >= 2) {
            console.log('    点击第二个 Please choose...');
            await pleaseChooseSelects[1].click();
            await detailPage.waitForTimeout(2000);

            const dropdownItems = await detailPage.locator('.ant-select-item').all();
            console.log('    下拉选项数量:', dropdownItems.length);
            for (let i = 0; i < Math.min(dropdownItems.length, 20); i++) {
                const text = await dropdownItems[i].textContent();
                console.log(`    [${i}]: ${text}`);
            }
        } else {
            console.log('    只有 1 个 Please choose，尝试其他方法...');

            // 找所有 ant-select 并尝试点击
            const allSelects = await detailPage.locator('.ant-select').all();
            console.log('    所有 ant-select 数量:', allSelects.length);

            // 找到包含 "Refuse" 的那个（已经是 Refuse）
            for (let i = 0; i < allSelects.length; i++) {
                const text = await allSelects[i].textContent();
                if (text.includes('Refuse')) {
                    console.log(`    找到包含 Refuse 的下拉框 [${i}]: ${text}`);
                }
            }

            // 尝试点击第 8 个下拉框（根据之前的调试）
            console.log('    尝试点击第 8 个下拉框...');
            if (allSelects.length > 8) {
                await allSelects[8].click();
                await detailPage.waitForTimeout(2000);

                const newItems = await detailPage.locator('.ant-select-item').all();
                console.log('    新下拉选项数量:', newItems.length);
                for (let i = 0; i < Math.min(newItems.length, 20); i++) {
                    const text = await newItems[i].textContent();
                    console.log(`    [${i}]: ${text}`);
                }
            }
        }

        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_try.png' });

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();