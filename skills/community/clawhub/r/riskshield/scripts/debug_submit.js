/**
 * 调试提交按钮
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

        // 选择 ManualApprovalResult -> Refuse
        console.log('6. 选择 ManualApprovalResult -> Refuse...');
        const allSelects = await detailPage.locator('.ant-select').all();
        await allSelects[7].click();
        await detailPage.waitForTimeout(1000);
        await detailPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).click();
        await detailPage.waitForTimeout(2000);

        // 选择 Refuse Code
        console.log('7. 选择 Refuse Code...');
        const allSelectsAfter = await detailPage.locator('.ant-select').all();
        await allSelectsAfter[8].click();
        await detailPage.waitForTimeout(1000);
        await detailPage.locator('.ant-select-item').filter({ hasText: 'CA_TRUE_HIT' }).first().click();

        await detailPage.waitForTimeout(2000);

        // 查找所有按钮
        console.log('8. 查找所有按钮...');
        const buttons = await detailPage.locator('button').all();
        console.log('   按钮数量:', buttons.length);
        for (let i = 0; i < buttons.length; i++) {
            const text = await buttons[i].textContent();
            const className = await buttons[i].getAttribute('class');
            console.log(`   button[${i}]: "${text}" - class: ${className}`);
        }

        // 截图
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/submit_buttons.png' });
        console.log('   截图已保存');

        // 尝试找到提交按钮
        console.log('9. 尝试点击提交按钮...');

        // 方法1: 按文本内容查找
        const submitBtn = detailPage.locator('button').filter({ hasText: /^提交$/ });
        const submitCount = await submitBtn.count();
        console.log('   文本"提交"的按钮数量:', submitCount);

        if (submitCount > 0) {
            console.log('   点击第一个提交按钮...');
            await submitBtn.first().click();
            console.log('   ✅ 已点击提交按钮');
        } else {
            // 方法2: 查找包含中文的按钮
            console.log('   尝试查找中文按钮...');
            const chineseBtns = await detailPage.evaluate(() => {
                const btns = document.querySelectorAll('button');
                const result = [];
                btns.forEach(btn => {
                    if (/[\u4e00-\u9fa5]/.test(btn.textContent)) {
                        result.push({
                            text: btn.textContent,
                            class: btn.className,
                            visible: btn.offsetParent !== null
                        });
                    }
                });
                return result;
            });
            console.log('   中文按钮:', JSON.stringify(chineseBtns));

            // 方法3: 查找绿色按钮
            console.log('   尝试查找绿色按钮...');
            const greenBtns = await detailPage.evaluate(() => {
                const btns = document.querySelectorAll('button');
                const result = [];
                btns.forEach(btn => {
                    const style = window.getComputedStyle(btn);
                    if (style.backgroundColor.includes('green') || btn.className.includes('primary')) {
                        result.push({
                            text: btn.textContent,
                            class: btn.className
                        });
                    }
                });
                return result;
            });
            console.log('   绿色按钮:', JSON.stringify(greenBtns));

            // 最后尝试点击最后一个按钮（通常是提交）
            console.log('   尝试点击最后一个按钮...');
            await buttons[buttons.length - 1].click();
            console.log('   已点击最后一个按钮');
        }

        await detailPage.waitForTimeout(5000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_submit.png' });
        console.log('   提交后截图已保存');

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();