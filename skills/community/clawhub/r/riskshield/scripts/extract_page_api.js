/**
 * RiskShield - 从页面提取 API 请求并执行
 */

const { chromium } = require('playwright');

const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

const CASE_NO = process.argv[2] || '2604151000000599507';
const ACTION = (process.argv[3] || 'pass').toLowerCase();
const CREDIT_AMOUNT = process.argv[5] || '100';

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
        await page.locator('input[type="text"]').nth(2).fill(CASE_NO);
        await page.waitForTimeout(500);
        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const searchBtn = buttons.find(b => b.textContent.trim() === 'Search');
            if (searchBtn) searchBtn.click();
        });
        await page.waitForTimeout(5000);

        // 获取审批链接
        console.log('3. 获取审批链接...');
        const approvalUrl = await page.evaluate((caseNo) => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes(caseNo)) {
                    const links = row.querySelectorAll('a');
                    for (const link of links) {
                        if (link.textContent.trim() === 'Approval') {
                            return link.href;
                        }
                    }
                }
            }
            return null;
        }, CASE_NO);
        console.log('   审批链接:', approvalUrl);

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

        // 填写金额
        console.log('7. 填写金额...');
        const inputs = await detailPage.locator('input').all();
        for (const input of inputs) {
            const ph = await input.getAttribute('placeholder');
            if (ph && ph.toLowerCase().includes('please enter')) {
                await input.click();
                await input.pressSequentially(CREDIT_AMOUNT, { delay: 50 });
                const val = await input.inputValue();
                console.log('   输入框值:', val);
                break;
            }
        }

        await detailPage.waitForTimeout(2000);

        // 现在尝试通过页面的 JavaScript 获取 token 并构造 API 请求
        console.log('8. 获取页面认证信息...');

        const pageContext = await detailPage.evaluate(() => {
            // 尝试从页面找到 API 请求的构建逻辑
            // 检查 localStorage 和 sessionStorage
            let authToken = null;
            
            try {
                // 检查是否有 axios 或其他 HTTP 库
                if (typeof axios !== 'undefined') {
                    return { hasAxios: true };
                }
                
                // 检查 Vue 实例或 React 组件
                const vueApp = document.querySelector('#app').__vue_app__;
                if (vueApp) {
                    const instance = vueApp._instance;
                    if (instance && instance.proxy) {
                        // 尝试获取 token
                        const globalProperties = instance.proxy.$config || {};
                        authToken = globalProperties.token || globalProperties.apiKey;
                    }
                }
            } catch (e) {
                console.log('Vue app error:', e.message);
            }
            
            // 从 cookie 获取 token
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'sgin') {
                    authToken = value;
                    break;
                }
            }
            
            return { authToken: authToken || 'not found' };
        });

        console.log('   页面认证信息:', JSON.stringify(pageContext));

        // 截图
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/before_api_submit.png' });

        // 获取表单数据
        console.log('9. 获取表单数据...');
        const formData = await detailPage.evaluate(() => {
            // 尝试找到表单提交的数据
            const forms = document.querySelectorAll('form');
            for (const form of forms) {
                const inputs = form.querySelectorAll('input, textarea');
                const data = {};
                inputs.forEach(input => {
                    if (input.name) data[input.name] = input.value;
                });
                if (Object.keys(data).length > 0) {
                    return data;
                }
            }
            
            // 尝试从 Vue 组件获取数据
            const vueData = document.querySelector('#app').__vue_app__?._instance?.proxy?.$data;
            return vueData || 'no form data found';
        });
        console.log('   表单数据:', JSON.stringify(formData).substring(0, 200));

        // 直接使用页面的 JavaScript API
        console.log('10. 通过页面 JS API 提交...');
        
        // 尝试找到提交函数
        const submitResult = await detailPage.evaluate(() => {
            // 查找全局提交函数
            if (window.submitApproval) {
                window.submitApproval();
                return 'submitted via window.submitApproval';
            }
            
            if (window.approve) {
                window.approve();
                return 'submitted via window.approve';
            }
            
            // 查找 ant-design 表单提交
            const submitBtns = document.querySelectorAll('button');
            for (const btn of submitBtns) {
                if (btn.textContent.trim() === 'Submit' || btn.textContent.trim() === '提交') {
                    // 模拟点击
                    btn.click();
                    return 'clicked submit button';
                }
            }
            
            return 'no submit method found';
        });
        
        console.log('    提交结果:', submitResult);

        await detailPage.waitForTimeout(5000);
        await detailPage.screenshot({ path: '/Users/alan/.openclaw/workspace/after_api_submit.png' });

        // 检查案件状态
        console.log('11. 检查案件状态...');
        await page.bringToFront();
        await page.waitForTimeout(3000);

        const status = await page.evaluate((caseNo) => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes(caseNo)) {
                    return row.textContent;
                }
            }
            return null;
        }, CASE_NO);
        
        console.log('    状态:', status ? status.substring(0, 100) : 'NOT FOUND');

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();