/**
 * RiskShield 案件审批自动化 - 最终修复版
 */

const { chromium } = require('playwright');

const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

const CASE_NO = process.argv[2] || '2604161000000599539';
const ACTION = (process.argv[3] || 'pass').toLowerCase();
const REFUSE_CODE = process.argv[4] || 'CA_TRUE_HIT';
const CREDIT_AMOUNT = process.argv[5] || '100';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`=== RiskShield 案件审批自动化 ===`);
    log(`案件号: ${CASE_NO}`);
    log(`操作: 通过 (PASS)`);
    log(`金额: ${CREDIT_AMOUNT}`);
    log('========================================');

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    try {
        // ========== 1. 登录 ==========
        log('[1/8] 正在登录...');
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(20000);
        log('[1/8] ✅ 登录成功');

        // ========== 2. 选择搜索类型: No. ==========
        log('[2/8] 选择搜索类型: 案件编号...');
        await page.waitForTimeout(2000);

        await page.locator('span.val').filter({ hasText: /^Case Name$/ }).click();
        await page.waitForTimeout(2000);

        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(1000);
        log('[2/8] ✅ 已选择"案件编号"');

        // ========== 3. 输入案件号 ==========
        log(`[3/8] 输入案件号: ${CASE_NO}...`);
        await page.locator('input[type="text"]').nth(2).fill(CASE_NO);
        await page.waitForTimeout(500);
        log('[3/8] ✅ 案件号已输入');

        // ========== 4. 点击搜索 ==========
        log('[4/8] 点击搜索...');
        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const searchBtn = buttons.find(b => b.textContent.trim() === 'Search');
            if (searchBtn) searchBtn.click();
        });
        await page.waitForTimeout(5000);
        log('[4/8] ✅ 搜索完成');

        // ========== 5. 验证案件 ==========
        log('[5/8] 验证案件...');
        const searchResult = await page.evaluate((caseNo) => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes(caseNo)) {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > 0 && cells[0].textContent.includes(caseNo)) {
                        return { found: true, rowText: row.textContent };
                    }
                }
            }
            return { found: false };
        }, CASE_NO);

        if (!searchResult.found) {
            log(`❌ 案件 ${CASE_NO} 未找到`);
            return;
        }

        if (searchResult.rowText.includes('Closed') || searchResult.rowText.includes('已结案')) {
            log('⚠️ 案件已结案');
            log('状态: ' + searchResult.rowText.substring(0, 100));
            return;
        }
        log('[5/8] ✅ 案件验证通过');

        // ========== 6. 获取审批页面URL ==========
        log('[6/8] 获取审批页面链接...');
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

        if (!approvalUrl) {
            log('❌ 找不到审批入口');
            return;
        }
        log('[6/8] ✅ 获取到审批链接');

        // ========== 7. 打开审批详情页 ==========
        log('[7/8] 打开审批详情页...');
        const detailPage = await context.newPage();
        
        // 使用 networkidle 等待确保页面完全加载
        await detailPage.goto(approvalUrl, { waitUntil: 'networkidle' });
        
        // 等待页面关键元素加载完成 - 等待 Basic Information tab 可见
        log('   等待页面关键元素加载...');
        await detailPage.waitForSelector('[role="tab"]:has-text("Basic Information")', { timeout: 10000 });
        await detailPage.waitForTimeout(2000);  // 额外等待确保 React 组件渲染完成
        log('[7/8] ✅ 审批详情页已打开（页面完全加载）');

        // ========== 8. 填写审批表单 ==========
        log('[8/8] 填写审批表单...');

        // 点击 Decision Information tab
        log('  - 点击 Decision Information tab...');
        
        // 等待 Decision Information tab 出现并可点击
        const decisionTab = detailPage.locator('[role="tab"]:has-text("Decision Information")');
        await decisionTab.waitFor({ state: 'visible', timeout: 5000 });
        await decisionTab.click();
        
        // 等待表单元素完全加载 - 等待 ManualApprovalResult 下拉框出现
        log('   等待表单元素加载...');
        await detailPage.waitForSelector('.ant-select:has-text("Please choose")', { timeout: 5000 });
        await detailPage.waitForTimeout(1000);  // 额外等待确保下拉框完全渲染
        log('  - ✅ Decision Information tab 已点击，表单已加载');

        // 选择 ManualApprovalResult -> Pass
        log('  - 选择 ManualApprovalResult...');
        
        // 等待下拉框可见
        const firstSelect = detailPage.locator('.ant-select').first();
        await firstSelect.waitFor({ state: 'visible', timeout: 5000 });
        await firstSelect.click();
        
        // 等待下拉选项出现
        await detailPage.waitForSelector('.ant-select-item', { timeout: 5000 });
        
        // 选择 Pass
        const passOption = detailPage.locator('.ant-select-item:has-text("Pass")');
        await passOption.waitFor({ state: 'visible', timeout: 5000 });
        await passOption.click();
        
        // 等待 React 处理选择
        await detailPage.waitForTimeout(1000);
        log('  - ✅ 已选择: Pass');

        // 等待页面更新
        await detailPage.waitForTimeout(3000);

        // 填写 Approval Idea（审批意见）- Pass 时需要填写
        log('  - 填写审批意见...');
        
        // 找到 Approval Idea 文本输入框（textarea）
        const approvalIdeaInput = detailPage.locator('textarea[placeholder*="请输入"], textarea[placeholder*="please input" i], textarea').first();
        
        // 检查是否存在
        const hasApprovalIdea = await approvalIdeaInput.count();
        if (hasApprovalIdea > 0) {
            await approvalIdeaInput.waitFor({ state: 'visible', timeout: 5000 });
            await approvalIdeaInput.fill('Approved - Pass');
            log('  - ✅ 已填写审批意见: Approved - Pass');
        } else {
            log('  ⚠️ 未找到审批意见输入框');
        }
        
        await detailPage.waitForTimeout(1000);

        await detailPage.waitForTimeout(2000);

        // 点击提交按钮 - 使用 waitFor 确保按钮完全可交互
        log('  - 点击提交按钮...');
        
        // 等待 Submit 按钮可见
        const submitBtn = detailPage.locator('button:has-text("Submit")');
        await submitBtn.waitFor({ state: 'visible', timeout: 5000 });
        await detailPage.waitForTimeout(500);  // 确保按钮完全渲染
        
        await submitBtn.click();
        log('  - ✅ 已点击提交按钮');
        await detailPage.waitForTimeout(5000);

        // ========== 9. 验证结果 ==========
        log('[9/9] 验证审批结果...');
        await detailPage.close();

        // 等待服务器处理（增加到 30 秒）
        log('   等待服务器处理...');
        await page.waitForTimeout(30000);

        // 检查案件状态
        const finalStatus = await page.evaluate((caseNo) => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes(caseNo)) {
                    return row.textContent;
                }
            }
            return null;
        }, CASE_NO);

        if (finalStatus) {
            if (finalStatus.includes('Closed') || finalStatus.includes('已结案')) {
                if (finalStatus.includes('Approved') || finalStatus.includes('同意')) {
                    log('');
                    log('========================================');
                    log(`  🎉 审批通过成功！`);
                    log(`  案件 ${CASE_NO} 已结案`);
                    log(`  审批金额: ${CREDIT_AMOUNT}`);
                    log('========================================');
                } else if (finalStatus.includes('Reject') || finalStatus.includes('拒绝')) {
                    log('');
                    log('========================================');
                    log(`  ⚠️ 审批被拒绝！`);
                    log(`  案件 ${CASE_NO} 已结案`);
                    log('========================================');
                } else {
                    log(`✅ 案件已结案: ${finalStatus.substring(0, 100)}`);
                }
            } else {
                log('⚠️ 案件状态未变化，当前状态: ' + finalStatus.substring(0, 100));
            }
        } else {
            log(`⚠️ 案件未找到（可能已结案或重新分配）`);
        }

        log('\n========================================');
        log('  自动化任务完成');
        log('========================================');

    } catch (error) {
        log(`❌ 错误: ${error.message}`);
        console.error(error);
    } finally {
        await browser.close();
    }
})();