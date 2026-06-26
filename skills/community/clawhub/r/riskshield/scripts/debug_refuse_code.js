/**
 * 调试 Refuse Code 下拉框
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

        // 截图看看当前状态
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/decision_tab.png' });
        console.log('   截图已保存');

        // 检查所有 ant-select 元素
        console.log('6. 检查 ant-select 元素...');
        const selects = await detailPage.locator('.ant-select').all();
        console.log('   .ant-select 数量:', selects.length);
        for (let i = 0; i < selects.length; i++) {
            const text = await selects[i].textContent();
            const className = await selects[i].getAttribute('class');
            console.log(`   [${i}] text: "${text}", class: ${className}`);
        }

        // 尝试找到 Refuse Code 下拉框
        console.log('7. 查找 Refuse Code 下拉框...');
        
        // 方法1: 查找包含 "Refuse Code" 文字的 ant-select
        const refuseCodeSelects = await detailPage.locator('.ant-select').filter({ hasText: 'Refuse Code' }).all();
        console.log('   方法1 (filter hasText "Refuse Code"):', refuseCodeSelects.length);

        // 方法2: 查找包含 "Please choose" 的 ant-select
        const pleaseChooseSelects = await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).all();
        console.log('   方法2 (filter hasText "Please choose"):', pleaseChooseSelects.length);

        // 方法3: 查找所有可点击的 ant-select
        console.log('   方法3: 列出所有 ant-select 的文本');
        for (let i = 0; i < selects.length; i++) {
            const text = await selects[i].textContent();
            console.log(`   ant-select[${i}]: "${text}"`);
        }

        // 截图
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/decision_tab2.png' });

        // 选择 ManualApprovalResult -> Refuse
        console.log('8. 选择 ManualApprovalResult -> Refuse...');
        const manualSelect = await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).first();
        await manualSelect.click();
        await detailPage.waitForTimeout(1000);
        await detailPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).click();
        console.log('   已选择 Refuse');

        // 等待页面更新
        await detailPage.waitForTimeout(3000);

        // 再次截图
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_refuse.png' });

        // 再次检查所有 ant-select
        console.log('9. 选择 Refuse 后检查 ant-select...');
        const selectsAfter = await detailPage.locator('.ant-select').all();
        console.log('   .ant-select 数量:', selectsAfter.length);
        for (let i = 0; i < selectsAfter.length; i++) {
            const text = await selectsAfter[i].textContent();
            console.log(`   [${i}]: "${text}"`);
        }

        // 尝试找到 Refuse Code 下拉框（包含 CA_TRUE_HIT）
        console.log('10. 尝试选择 Refuse Code...');
        
        // 找到所有 "Please choose" 的下拉框（排除已选择的 ManualApprovalResult）
        const allPleaseChoose = await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).all();
        console.log('    "Please choose" 数量:', allPleaseChoose.length);

        if (allPleaseChoose.length > 1) {
            // 第二个应该是 Refuse Code
            console.log('    点击第二个 Please choose...');
            await allPleaseChoose[1].click();
            await detailPage.waitForTimeout(1000);
            
            // 选择 CA_TRUE_HIT
            console.log('    选择 CA_TRUE_HIT...');
            await detailPage.locator('.ant-select-item').filter({ hasText: 'CA_TRUE_HIT' }).first().click();
            console.log('    ✅ 已选择');
        } else if (selectsAfter.length > 1) {
            // 尝试点击第二个下拉框
            console.log('    点击第二个下拉框...');
            await selectsAfter[1].click();
            await detailPage.waitForTimeout(1000);
            
            // 选择 CA_TRUE_HIT
            const items = await detailPage.locator('.ant-select-item').all();
            console.log('    下拉选项数量:', items.length);
            for (let i = 0; i < items.length; i++) {
                console.log(`    [${i}]:`, await items[i].textContent());
            }
            
            await detailPage.locator('.ant-select-item').filter({ hasText: 'CA_TRUE_HIT' }).first().click();
            console.log('    ✅ 已选择');
        }

        await detailPage.waitForTimeout(1000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/refuse_code_selected.png' });

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();