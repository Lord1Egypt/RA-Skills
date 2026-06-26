/**
 * 调试金额填写 - 使用 Playwright 原生方法
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

        // 找到并填写金额
        console.log('7. 填写金额...');
        
        // 使用 visible 选择器找到所有可见的 input
        const allInputs = await detailPage.locator('input:visible').all();
        console.log('   可见 input 数量:', allInputs.length);
        
        for (let i = 0; i < allInputs.length; i++) {
            const ph = await allInputs[i].getAttribute('placeholder');
            const type = await allInputs[i].getAttribute('type');
            console.log(`   input[${i}]: type=${type}, placeholder="${ph}"`);
        }

        // 尝试查找 Credit Amount 输入框 (placeholder = "Please enter" 的 number 类型 input)
        console.log('   尝试查找 Credit Amount 输入框...');
        
        // 方式1: 尝试用 type=number 的 input
        const numberInput = detailPage.locator('input[type="number"]').filter({ has: detailPage.locator('..').filter({ hasText: 'Credit Amount' }) });
        const numberCount = await numberInput.count();
        console.log('   number input 数量:', numberCount);
        
        if (numberCount === 0) {
            // 方式2: 尝试查找所有 placeholder 包含 "Please enter" 的 input
            console.log('   尝试查找 placeholder=\"Please enter\" 的 input...');
            
            // 获取所有 input
            const allTextInputs = await detailPage.locator('input[type="text"]').all();
            console.log('   text input 总数:', allTextInputs.length);
            
            for (let i = 0; i < allTextInputs.length; i++) {
                const visible = await allTextInputs[i].isVisible();
                const ph = await allTextInputs[i].getAttribute('placeholder');
                if (visible && ph && ph.toLowerCase().includes('please enter')) {
                    console.log(`   找到 Credit Amount 输入框 input[${i}]: placeholder="${ph}"`);
                    
                    // 先点击聚焦
                    await allTextInputs[i].click();
                    await detailPage.waitForTimeout(500);
                    
                    // 使用 type 而不是 fill (更接近真实用户输入)
                    await allTextInputs[i].type('100');
                    await detailPage.waitForTimeout(500);
                    
                    const value = await allTextInputs[i].inputValue();
                    console.log(`   输入后值: "${value}"`);
                    break;
                }
            }
        }

        await detailPage.waitForTimeout(2000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/amount_filled_check.png' });

        // 点击 Submit
        console.log('8. 点击 Submit...');
        await detailPage.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Submit') {
                    btn.click();
                    return;
                }
            }
        });

        await detailPage.waitForTimeout(5000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_submit_check.png' });

        // 检查案件状态
        console.log('9. 检查案件状态...');
        const status = await page.evaluate(() => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes('2604151000000599520')) {
                    return row.textContent;
                }
            }
            return 'NOT FOUND';
        });
        console.log('   状态:', status);

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();