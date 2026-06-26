/**
 * 调试 - 检查选择 Pass 后的页面
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
        await page.locator('input[type="text"]').nth(2).fill('2604161000000599539');
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
                if (row.textContent.includes('2604161000000599539')) {
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
        await detailPage.goto(approvalUrl, { waitUntil: 'networkidle' });
        await detailPage.waitForSelector('[role="tab"]:has-text("Basic Information")', { timeout: 10000 });
        await detailPage.waitForTimeout(2000);
        console.log('   页面已加载');

        // 点击 Decision Information tab
        console.log('5. 点击 Decision Information tab...');
        await detailPage.locator('[role="tab"]:has-text("Decision Information")').click();
        await detailPage.waitForSelector('.ant-select:has-text("Please choose")', { timeout: 5000 });
        await detailPage.waitForTimeout(1000);
        console.log('   Tab 已点击');

        // 选择 ManualApprovalResult -> Pass
        console.log('6. 选择 ManualApprovalResult -> Pass...');
        await detailPage.locator('.ant-select').first().click();
        await detailPage.waitForSelector('.ant-select-item', { timeout: 5000 });
        await detailPage.locator('.ant-select-item:has-text("Pass")').click();
        console.log('   已选择 Pass');

        // 等待页面更新
        await detailPage.waitForTimeout(3000);

        // 截图
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_pass_select.png' });

        // 检查所有 input 元素
        console.log('7. 检查所有 input 元素...');
        const inputs = await detailPage.locator('input').all();
        console.log('   input 总数:', inputs.length);
        for (let i = 0; i < inputs.length; i++) {
            const ph = await inputs[i].getAttribute('placeholder');
            const type = await inputs[i].getAttribute('type');
            const visible = await inputs[i].isVisible();
            console.log(`   input[${i}]: type=${type}, placeholder="${ph}", visible=${visible}`);
        }

        // 尝试找到金额输入框
        console.log('8. 尝试找到金额输入框...');
        
        // 方法1: placeholder 包含 please enter
        const pleaseEnterInputs = await detailPage.locator('input[placeholder*="please enter" i]').all();
        console.log('   placeholder 包含 "please enter":', pleaseEnterInputs.length);

        // 方法2: 查找 type=number 的 input
        const numberInputs = await detailPage.locator('input[type="number"]').all();
        console.log('   type=number:', numberInputs.length);

        // 方法3: 查找所有可见的 input
        const visibleInputs = await detailPage.locator('input:visible').all();
        console.log('   可见 input:', visibleInputs.length);
        for (const input of visibleInputs) {
            const ph = await input.getAttribute('placeholder');
            console.log(`     placeholder="${ph}"`);
        }

        // 检查 Credit Amount 标签附近
        console.log('9. 查找 Credit Amount 相关元素...');
        const creditAmountExists = await detailPage.evaluate(() => {
            const allText = document.body.innerText;
            return allText.includes('Credit Amount');
        });
        console.log('   Credit Amount 文本存在:', creditAmountExists);

        // 尝试使用备用选择器
        console.log('10. 尝试使用金额输入框的备用方法...');
        
        // 尝试找到 label 为 Credit Amount 的输入框
        const creditInput = detailPage.locator('input').filter({ has: detailPage.locator('..label:has-text("Credit Amount")') }).first();
        const creditInputCount = await creditInput.count();
        console.log('    Credit Amount 输入框数量:', creditInputCount);

        console.log('\n调试完成');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();